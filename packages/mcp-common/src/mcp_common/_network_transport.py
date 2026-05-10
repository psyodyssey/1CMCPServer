"""Internal HTTP MCP transport helper for Track H Step 4.

Not part of the public ``mcp_common`` API. Underscore-prefixed module
deliberately marked private. Imported only by the three MCP server
``__main__.py`` entrypoints (``mcp_read_server``, ``mcp_write_server``,
``mcp_intelligence_server``); not exported from ``mcp_common.__init__``
and not intended for use elsewhere.

Track H / Step 3 contract anchors honoured here (see
`docs/architecture/track-h-network-transport-and-auth-contract.md`):

  - stdlib only (``http.server``, ``socketserver``, ``hmac``, ``os``,
    ``re``, ``json``, ``argparse``, ``logging``, ``sys``, ``signal``,
    ``socket``, ``urllib.parse``); no third-party HTTP framework, no
    JSON-RPC library, no MCP SDK;
  - HTTP/1.1 ``ThreadingHTTPServer``; single endpoint ``/mcp``; POST
    only; one JSON-RPC message per body; ``application/json``;
    1 MiB body cap;
  - bearer auth: ``Authorization: <scheme> <token>``, scheme matched
    case-insensitively (``Bearer`` / ``bearer`` / ``BEARER`` / mixed
    case all accepted), token compared byte-exactly via
    ``hmac.compare_digest``;
  - failure-equivalence: missing / empty / malformed / invalid token
    map to identical 401 + ``WWW-Authenticate: Bearer realm="mcp"``
    + JSON-RPC ``-32001`` envelope;
  - multiple ``Authorization`` headers map to 400 + ``-32600``;
  - complete redaction discipline: token value / length / prefix /
    suffix / hash / fingerprint MUST NOT appear in stderr / structured
    logs / response bodies / error messages;
  - tool registry consumed only through ``list_tools()`` /
    ``get_tool(name)`` injected callables (zero new MCP tools);
  - existing Track G stdio transport delegated to
    ``_stdio_transport._serve_stdio`` byte-identically;
  - no auth on stdio path (Track G threat model preserved).

Exposes exactly one public-to-package function:

    run_main_http(
        *, prog, description, server_name, server_version,
        list_tools_fn, get_tool_fn, argv=None,
    ) -> int

Per Step 3 contract §11.4 the three ``__main__.py`` entrypoints
dispatch through this one function; the unified argparser handles
both transports in a single ``--help`` output (see §16.1.1
verification clause). Existing ``_stdio_transport.run_main`` is left
in place for backward compatibility but is no longer the live
entrypoint for the three MCP server packages.
"""

from __future__ import annotations

import argparse
import hmac
import json
import logging
import os
import re
import socket
import sys
import threading
from email.message import Message
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable, NoReturn

from ._stdio_transport import (
    ALLOWED_LOG_LEVELS,
    PROTOCOL_VERSION,  # noqa: F401  -- imported for cross-module reference
    _configure_logging,
    _handle_request,
    _make_error,
    _maybe_load_product_config,
    _serve_stdio,
)

ListToolsFn = Callable[[], list[str]]
GetToolFn = Callable[[str], object]

ALLOWED_TRANSPORTS = ("stdio", "http")
MAX_BODY_BYTES = 1024 * 1024  # 1 MiB per Step 3 contract §4.6.

# Track D ${ENV:NAME} env-substitution regex, byte-identical to
# apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py.
ENV_TOKEN_RE = re.compile(r"^\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}$")
VARNAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
BIND_RE = re.compile(r"^(.+):(\d+)$")
# Authorization header: scheme (any case, ASCII letters) + single
# space + non-empty token. Step 3 contract §8.3 pins single ASCII
# space; tabs / multiple spaces / other whitespace MUST be rejected.
AUTH_HEADER_RE = re.compile(r"^([A-Za-z]+) ([^\s].*)$")
EXPECTED_SCHEME_LOWER = "bearer"

JSONRPC_AUTH_FAIL_CODE = -32001  # implementation-defined per §6.2
JSONRPC_PARSE_ERROR = -32700
JSONRPC_INVALID_REQUEST = -32600


# ---------------------------------------------------------------------------
# Argument parsing and startup-failure helpers
# ---------------------------------------------------------------------------


def _build_arg_parser(prog: str, description: str) -> argparse.ArgumentParser:
    """Unified argparser supporting both Track G stdio and Track H http.

    Existing four flags (``--config-path``, ``--transport``,
    ``--log-level``, ``--help``) preserved with byte-identical
    semantics for ``--transport stdio`` per Step 3 contract §10.1 /
    §12.3. New flags ``--bind`` and ``--auth-token-env`` accepted at
    parse time; ``--bind`` requirement-when-http is enforced
    post-parse so ``--help`` works regardless of selected transport.
    """
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "--config-path",
        default=None,
        help=(
            "Optional path to a product config JSON; loaded via "
            "onec_platform at startup."
        ),
    )
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=ALLOWED_TRANSPORTS,
        help=(
            "Transport mode. 'stdio' (default) is the Track G local "
            "stdio loop. 'http' is the Track H HTTP/1.1 transport "
            "with bearer-token authentication."
        ),
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=ALLOWED_LOG_LEVELS,
        help="Diagnostic log level. Logs are written to stderr.",
    )
    parser.add_argument(
        "--bind",
        default=None,
        metavar="HOST:PORT",
        help=(
            "HOST:PORT for --transport http. Required when --transport "
            "http; ignored for stdio. There is no default; binding "
            "must be explicit."
        ),
    )
    parser.add_argument(
        "--auth-token-env",
        default=None,
        metavar="VARNAME",
        help=(
            "Name of an environment variable holding the bearer token. "
            "Optional. Meaningful only with --transport http. When "
            "supplied, takes precedence over auth.tokens in product "
            "config (replace, not merge)."
        ),
    )
    return parser


def _fail(prog: str, message: str) -> NoReturn:
    """Single-line stderr failure + non-zero exit, per §10.6.

    No Python traceback is emitted to operator stderr; the exit code
    matches argparse-style usage failure (2).
    """
    print(f"{prog}: {message}", file=sys.stderr)
    raise SystemExit(2)


def _parse_bind(bind_value: str, prog: str) -> tuple[str, int]:
    """Parse and validate --bind HOST:PORT. Fail-closed on any error."""
    m = BIND_RE.match(bind_value)
    if not m:
        _fail(prog, "--bind value must be HOST:PORT")
    host, port_str = m.group(1), m.group(2)
    if not host:
        _fail(prog, "--bind HOST must be non-empty")
    try:
        port = int(port_str)
    except ValueError:
        _fail(prog, "--bind PORT must be an integer in 1..65535")
    if not 1 <= port <= 65535:
        _fail(prog, "--bind PORT must be in 1..65535")
    try:
        socket.gethostbyname(host)
    except OSError:
        # Do not echo the OSError message; it may include resolver
        # internals. Operators get the host they typed.
        _fail(prog, f"--bind HOST resolution failed: {host}")
    return host, port


def _resolve_env_token(varname: str, source_label: str, prog: str) -> str:
    """Resolve a token value from os.environ. Fail-closed on missing/empty."""
    value = os.environ.get(varname, "")
    if not value:
        _fail(
            prog,
            f"env var {varname} is not set or empty ({source_label})",
        )
    return value


def _resolve_config_tokens(config_path: str | None, prog: str) -> list[str]:
    """Load product config (if any) and return resolved auth.tokens list.

    Uses ``load_product_config_from_json_file`` directly (not
    ``bootstrap_product_from_json_file``) because we need the
    ``ProductConfig`` object itself, not a ``BootstrapResult`` that
    discards it. ``load_product_config_from_json_file`` raises
    ``ValueError`` on any structural problem; this boundary catches
    it and converts to fail-closed startup.
    """
    if config_path is None:
        return []
    try:
        from onec_platform import load_product_config_from_json_file
    except ImportError:  # pragma: no cover -- defensive
        _fail(prog, "onec_platform package not importable from PYTHONPATH")
    try:
        config = load_product_config_from_json_file(config_path)
    except ValueError as exc:
        _fail(prog, f"product config rejected: {exc}")
    auth = getattr(config, "auth", None)
    if auth is None:
        return []
    specs = list(getattr(auth, "tokens", []) or [])
    resolved: list[str] = []
    for spec in specs:
        m = ENV_TOKEN_RE.match(spec)
        if not m:
            # Loader should already reject this; defensive double-check.
            _fail(
                prog,
                "auth.tokens entry must match ${ENV:NAME} form",
            )
        env_name = m.group(1)
        resolved.append(_resolve_env_token(env_name, "auth.tokens", prog))
    return resolved


def _resolve_token_sources(
    args: argparse.Namespace,
    prog: str,
    logger: logging.Logger,
) -> list[str]:
    """Resolve effective valid token list per §10.5 precedence rule.

    --auth-token-env wins over auth.tokens (replace, not merge). Result
    is the list of resolved token values held only in process memory
    for the lifetime of the server process; never written to disk and
    never logged.
    """
    if args.auth_token_env is not None:
        varname = args.auth_token_env
        if not VARNAME_RE.match(varname):
            _fail(prog, "--auth-token-env value must be a valid env var name")
        value = _resolve_env_token(varname, "--auth-token-env", prog)
        # Length / prefix / suffix / hash / fingerprint MUST NOT be
        # logged. We log only that auth was sourced from CLI flag and
        # what the env var name was (env var names are not secrets).
        logger.debug(
            "auth source: --auth-token-env=%s (resolved at startup)", varname
        )
        return [value]
    config_tokens = _resolve_config_tokens(args.config_path, prog)
    if not config_tokens:
        _fail(
            prog,
            "--transport http requires --auth-token-env or "
            "auth.tokens in product config",
        )
    logger.debug(
        "auth source: auth.tokens (%d entry/entries resolved at startup)",
        len(config_tokens),
    )
    return config_tokens


# ---------------------------------------------------------------------------
# HTTP request handler
# ---------------------------------------------------------------------------


class _MCPHandler(BaseHTTPRequestHandler):
    """HTTP handler for the /mcp endpoint.

    Subclassed per-server-instance; the per-server context (registry
    callables, logger, tokens, server identity) is attached by
    ``_make_handler_class`` as class attributes so we can keep the
    stdlib ``BaseHTTPRequestHandler`` constructor signature.
    """

    # These are populated by _make_handler_class:
    server_name: str = ""
    server_version: str = ""
    list_tools_fn: ListToolsFn | None = None
    get_tool_fn: GetToolFn | None = None
    valid_tokens: tuple[str, ...] = ()
    diag_logger: logging.Logger | None = None

    # Tighten BaseHTTPRequestHandler defaults to keep the wire surface
    # small. Default protocol_version "HTTP/1.0" forces close-after-
    # response which matches Step 3 contract §4.7. We do not promise
    # keep-alive.
    protocol_version = "HTTP/1.1"
    server_version_header = "1c-agent-platform/0.4.0-track-h"

    # ---- Stdlib hooks ---------------------------------------------------

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
        """Route BaseHTTPRequestHandler access logs to stderr via logging.

        BaseHTTPRequestHandler defaults to writing to stderr directly
        with a different format; routing through the platform logger
        keeps a uniform log-line discipline (no token data, structured
        prefix). Token values cannot reach this path because they live
        only in headers and validation results, not in URL/path data.
        """
        if self.diag_logger is not None:
            self.diag_logger.info(
                "http %s - %s",
                self.address_string(),
                fmt % args,
            )

    # ---- HTTP method dispatch ------------------------------------------

    def do_GET(self) -> None:
        self._reject_non_post()

    def do_PUT(self) -> None:
        self._reject_non_post()

    def do_DELETE(self) -> None:
        self._reject_non_post()

    def do_PATCH(self) -> None:
        self._reject_non_post()

    def do_OPTIONS(self) -> None:
        self._reject_non_post()

    def do_HEAD(self) -> None:
        self._reject_non_post()

    def do_POST(self) -> None:
        if self.path != "/mcp":
            self._send_plain(HTTPStatus.NOT_FOUND, b"Not Found\n")
            return
        # ContentType: must be application/json (parameters allowed).
        ctype_raw = self.headers.get("Content-Type", "") or ""
        if not _content_type_is_json(ctype_raw):
            self._send_jsonrpc_error(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                req_id=None,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        # Multiple Authorization headers => 400 (§8.6 / §6.4).
        auth_values = self.headers.get_all("Authorization") or []
        if len(auth_values) > 1:
            self._send_jsonrpc_error(
                HTTPStatus.BAD_REQUEST,
                req_id=None,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        # Auth gate: missing / empty / malformed / invalid → identical
        # 401 (§6.2 / §8.4). Order: header presence, regex, scheme,
        # token compare. All branches converge on the same response.
        auth_header = auth_values[0] if auth_values else ""
        if not _auth_header_passes(auth_header, self.valid_tokens):
            self._send_auth_failure()
            return
        # Body length: enforce cap (§4.6).
        try:
            content_length = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            self._send_jsonrpc_error(
                HTTPStatus.BAD_REQUEST,
                req_id=None,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        if content_length < 0 or content_length > MAX_BODY_BYTES:
            self._send_jsonrpc_error(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                req_id=None,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        # Read body (exact length).
        body = self.rfile.read(content_length) if content_length else b""
        # Parse body.
        try:
            req = json.loads(body.decode("utf-8")) if body else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_jsonrpc_error(
                HTTPStatus.BAD_REQUEST,
                req_id=None,
                code=JSONRPC_PARSE_ERROR,
                message="Parse error",
            )
            return
        if not isinstance(req, dict):
            self._send_jsonrpc_error(
                HTTPStatus.BAD_REQUEST,
                req_id=None,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        # Reject batch arrays implicitly via the isinstance(dict) gate
        # above. Accept only single-object envelopes.
        # JSON-RPC envelope sanity: jsonrpc + method must exist.
        if req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
            req_id = req.get("id") if isinstance(req.get("id"), (int, str)) else None
            self._send_jsonrpc_error(
                HTTPStatus.BAD_REQUEST,
                req_id=req_id,
                code=JSONRPC_INVALID_REQUEST,
                message="Invalid Request",
            )
            return
        # Notification (no id) → 204 + empty body, no envelope.
        is_notification = "id" not in req
        # Dispatch.
        assert self.list_tools_fn is not None
        assert self.get_tool_fn is not None
        assert self.diag_logger is not None
        response = _handle_request(
            req,
            self.server_name,
            self.server_version,
            self.list_tools_fn,
            self.get_tool_fn,
            self.diag_logger,
        )
        if is_notification or response is None:
            self._send_no_content()
            return
        body_bytes = json.dumps(response).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    # ---- Response helpers ----------------------------------------------

    def _reject_non_post(self) -> None:
        if self.path != "/mcp":
            self._send_plain(HTTPStatus.NOT_FOUND, b"Not Found\n")
            return
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header("Allow", "POST")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send_plain(self, status: HTTPStatus, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _send_no_content(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send_jsonrpc_error(
        self,
        http_status: HTTPStatus,
        req_id: object,
        code: int,
        message: str,
    ) -> None:
        envelope = _make_error(req_id, code, message)
        body_bytes = json.dumps(envelope).encode("utf-8")
        self.send_response(http_status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def _send_auth_failure(self) -> None:
        envelope = _make_error(None, JSONRPC_AUTH_FAIL_CODE, "Unauthorized")
        body_bytes = json.dumps(envelope).encode("utf-8")
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("WWW-Authenticate", 'Bearer realm="mcp"')
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)


def _content_type_is_json(value: str) -> bool:
    """Return True iff value's media type (ignoring parameters) is application/json.

    Uses ``email.message.Message`` to parse parameters per RFC 7231;
    matches case-insensitively on the bare media type.
    """
    msg = Message()
    msg["Content-Type"] = value
    media_type = msg.get_content_type()  # already lowercased
    return media_type == "application/json"


def _auth_header_passes(header: str, valid_tokens: tuple[str, ...]) -> bool:
    """Validate the Authorization header per Step 3 contract §8.

    Returns False on any of: empty / missing format / wrong scheme /
    mismatched token. All failure modes converge so that callers map
    them to one identical 401 response (§8.4 failure-equivalence).
    """
    if not header:
        return False
    m = AUTH_HEADER_RE.match(header)
    if not m:
        return False
    scheme, presented = m.group(1), m.group(2)
    if scheme.lower() != EXPECTED_SCHEME_LOWER:
        return False
    if not presented:
        return False
    presented_bytes = presented.encode("utf-8")
    # Iterate valid tokens; per-token constant-time compare.
    for valid in valid_tokens:
        if hmac.compare_digest(presented_bytes, valid.encode("utf-8")):
            return True
    return False


def _make_handler_class(
    *,
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    valid_tokens: tuple[str, ...],
    diag_logger: logging.Logger,
) -> type[_MCPHandler]:
    """Build a per-server-instance handler subclass with bound context."""
    # Subclass with per-instance class attributes; one class per
    # ThreadingHTTPServer instance.
    return type(
        "_MCPHandlerBound",
        (_MCPHandler,),
        {
            "server_name": server_name,
            "server_version": server_version,
            "list_tools_fn": staticmethod(list_tools_fn),
            "get_tool_fn": staticmethod(get_tool_fn),
            "valid_tokens": tuple(valid_tokens),
            "diag_logger": diag_logger,
        },
    )


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------


def _serve_http(
    *,
    bind_host: str,
    bind_port: int,
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    valid_tokens: tuple[str, ...],
    logger: logging.Logger,
) -> int:
    """Run the HTTP/1.1 ThreadingHTTPServer loop.

    Graceful shutdown on KeyboardInterrupt (SIGINT). Stdlib
    ``ThreadingHTTPServer`` is one-thread-per-request; per Step 3
    contract §7.2 / §7.3 there is no per-client session state and no
    ordering guarantee.
    """
    handler_class = _make_handler_class(
        server_name=server_name,
        server_version=server_version,
        list_tools_fn=list_tools_fn,
        get_tool_fn=get_tool_fn,
        valid_tokens=valid_tokens,
        diag_logger=logger,
    )
    try:
        httpd = ThreadingHTTPServer((bind_host, bind_port), handler_class)
    except OSError as exc:
        logger.error("Failed to bind %s:%s: %s", bind_host, bind_port, exc)
        return 2
    # Daemon threads so a Ctrl-C does not wait for in-flight requests.
    httpd.daemon_threads = True
    actual_host, actual_port = httpd.server_address[:2]
    logger.info(
        "Starting %s HTTP transport (JSON-RPC 2.0) on %s:%s with %d valid token(s).",
        server_name,
        actual_host,
        actual_port,
        len(valid_tokens),
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Interrupted (KeyboardInterrupt); shutting down HTTP server.")
        return 0
    finally:
        httpd.shutdown()
        httpd.server_close()
    return 0


# ---------------------------------------------------------------------------
# Public-to-package entrypoint
# ---------------------------------------------------------------------------


def run_main_http(
    *,
    prog: str,
    description: str,
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    argv: list[str] | None = None,
) -> int:
    """Run a Track H MCP server entrypoint with unified stdio/http dispatch.

    Per Step 3 contract §11.2 the signature is parallel to existing
    ``_stdio_transport.run_main(...)``. Per §16.1.1 the argparser
    presents both transports in a single ``--help`` output. Per
    §11.4 the dispatch logic lives inside this single function rather
    than being split between ``run_main`` and ``run_main_http`` in
    each ``__main__.py`` -- a deliberate narrow interpretation
    documented in the Step 4 commit message; the alternative would
    require modifying ``_stdio_transport.py``'s ``ALLOWED_TRANSPORTS``
    constant which §11.3 disfavours by default.

    Returns process exit code; 0 = clean exit, non-zero = error.
    Uncaught exceptions are caught at the top-level boundary and
    converted to a logged error + non-zero exit so operators never
    see a raw Python traceback on stderr from this layer (see also
    ``_fail`` for argparse-style operator-readable startup failures).
    """
    parser = _build_arg_parser(prog, description)
    args = parser.parse_args(argv)
    logger = _configure_logging(args.log_level, server_name)

    if args.transport == "stdio":
        # --bind / --auth-token-env are silently ignored for stdio per
        # §10.3 / §10.4. This preserves Track G behaviour byte-
        # identically (stdio operators who never pass network flags
        # are unaffected; operators who pass them by mistake on stdio
        # path do not get spurious failures).
        try:
            rc = _maybe_load_product_config(args.config_path, logger)
            if rc != 0:
                return rc
            return _serve_stdio(
                server_name,
                server_version,
                list_tools_fn,
                get_tool_fn,
                logger,
            )
        except Exception:  # noqa: BLE001
            logger.exception("Fatal error in %s entrypoint (stdio)", server_name)
            return 1

    # args.transport == "http" -- §10.3 / §10.4 / §10.6 startup gates.
    if args.bind is None:
        _fail(prog, "--transport http requires --bind HOST:PORT")
    bind_host, bind_port = _parse_bind(args.bind, prog)
    valid_tokens = _resolve_token_sources(args, prog, logger)
    try:
        return _serve_http(
            bind_host=bind_host,
            bind_port=bind_port,
            server_name=server_name,
            server_version=server_version,
            list_tools_fn=list_tools_fn,
            get_tool_fn=get_tool_fn,
            valid_tokens=tuple(valid_tokens),
            logger=logger,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Fatal error in %s entrypoint (http)", server_name)
        return 1


# Threading import used only in handler-class type construction tests
# upstream; kept as an explicit import so static analyzers do not
# strip it. ThreadingHTTPServer already pulls threading in implicitly.
_THREADING_IMPORT_KEEPALIVE = threading
