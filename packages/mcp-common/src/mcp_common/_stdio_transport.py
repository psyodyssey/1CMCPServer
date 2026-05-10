"""Internal stdio JSON-RPC transport helper for Track G MCP server entrypoints.

Not part of the public ``mcp_common`` API. Underscore-prefixed module
deliberately marked private. Imported only by the three MCP server
``__main__.py`` entrypoints (``mcp_read_server``, ``mcp_write_server``,
``mcp_intelligence_server``); not exported from ``mcp_common.__init__``
and not intended for use elsewhere.

Track G / Step 4 contract anchors honoured here:
  - stdlib-only (``sys``, ``json``, ``argparse``, ``logging``,
    ``inspect``); no third-party JSON-RPC library, no MCP SDK;
  - stdio JSON-RPC 2.0 line-delimited framing; never network;
  - ``sys.stdout`` reserved for JSON-RPC response envelopes only;
    diagnostic output goes to ``sys.stderr`` via ``logging``;
  - tool registry consumed only through ``list_tools()`` /
    ``get_tool(name)`` injected callables;
  - no auth, no supervision, no daemon loop.
"""

import argparse
import inspect
import json
import logging
import sys
from typing import Callable

from .result import ToolResult

ListToolsFn = Callable[[], list[str]]
GetToolFn = Callable[[str], object]

PROTOCOL_VERSION = "2024-11-05"
ALLOWED_TRANSPORTS = ("stdio",)
ALLOWED_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def _build_arg_parser(prog: str, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "--config-path",
        default=None,
        help=(
            "Optional path to a product config JSON; loaded via "
            "onec_platform.bootstrap_product_from_json_file at startup."
        ),
    )
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=ALLOWED_TRANSPORTS,
        help="Transport mode. Track G ships stdio only.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=ALLOWED_LOG_LEVELS,
        help="Diagnostic log level. Logs are written to stderr.",
    )
    return parser


def _configure_logging(level_name: str, server_name: str) -> logging.Logger:
    logging.basicConfig(
        stream=sys.stderr,
        level=getattr(logging, level_name),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    return logging.getLogger(server_name)


def _maybe_load_product_config(path: str | None, logger: logging.Logger) -> int:
    if path is None:
        return 0
    from onec_platform import bootstrap_product_from_json_file

    bootstrap_product_from_json_file(path)
    logger.info("Loaded product config from %s", path)
    return 0


def _tool_description(tool: object, name: str, server_name: str) -> str:
    doc = inspect.getdoc(tool) if tool is not None else None
    if doc:
        return doc.splitlines()[0].strip()
    return f"{server_name} tool {name}"


def _serialize_tool_result(result: object) -> dict:
    if isinstance(result, ToolResult):
        envelope: dict = {
            "content": [{"type": "text", "text": result.message}],
            "isError": not result.ok,
        }
        if result.payload is not None:
            envelope["structuredContent"] = result.payload
        return envelope
    return {"content": [{"type": "text", "text": str(result)}]}


def _make_error(req_id: object, code: int, message: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message},
    }


def _make_result(req_id: object, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _handle_request(
    req: dict,
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    logger: logging.Logger,
) -> dict | None:
    is_notification = "id" not in req
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params") or {}

    if method == "initialize":
        return _make_result(
            req_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": server_name, "version": server_version},
            },
        )
    if method in ("notifications/initialized", "initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return _make_result(req_id, {})
    if method == "tools/list":
        names = list_tools_fn()
        tools = []
        for name in names:
            tool = get_tool_fn(name)
            tools.append(
                {
                    "name": name,
                    "description": _tool_description(tool, name, server_name),
                    "inputSchema": {"type": "object"},
                }
            )
        return _make_result(req_id, {"tools": tools})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        tool = get_tool_fn(name) if isinstance(name, str) else None
        if tool is None:
            return _make_error(req_id, -32601, f"Unknown tool: {name!r}")
        if not isinstance(arguments, dict):
            return _make_error(req_id, -32602, "tools/call arguments must be an object")
        try:
            result = tool(**arguments)
        except TypeError as exc:
            logger.exception("Bad arguments for tool %s", name)
            return _make_error(req_id, -32602, f"Invalid params for {name!r}: {exc}")
        except Exception as exc:
            logger.exception("Tool %s raised", name)
            return _make_error(req_id, -32603, f"Tool {name!r} failed: {exc}")
        return _make_result(req_id, _serialize_tool_result(result))

    if is_notification:
        return None
    return _make_error(req_id, -32601, f"Method not found: {method!r}")


def _serve_stdio(
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    logger: logging.Logger,
) -> int:
    logger.info("Starting %s stdio transport (JSON-RPC 2.0).", server_name)
    stdin = sys.stdin
    stdout = sys.stdout
    try:
        for raw in stdin:
            line = raw.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                response = _make_error(None, -32700, f"Parse error: {exc}")
                stdout.write(json.dumps(response) + "\n")
                stdout.flush()
                continue
            if not isinstance(req, dict):
                response = _make_error(None, -32600, "Invalid Request: expected JSON object")
                stdout.write(json.dumps(response) + "\n")
                stdout.flush()
                continue
            response = _handle_request(
                req, server_name, server_version, list_tools_fn, get_tool_fn, logger
            )
            if response is None:
                continue
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()
    except KeyboardInterrupt:
        logger.info("Interrupted (KeyboardInterrupt); exiting cleanly.")
        return 0
    logger.info("EOF on stdin; exiting cleanly.")
    return 0


def run_main(
    *,
    prog: str,
    description: str,
    server_name: str,
    server_version: str,
    list_tools_fn: ListToolsFn,
    get_tool_fn: GetToolFn,
    argv: list[str] | None = None,
) -> int:
    """Run a Track G stdio MCP server entrypoint.

    Returns process exit code; 0 = clean exit, non-zero = error.
    Uncaught exceptions are caught at the boundary and converted to a
    logged error + non-zero exit, so operators never see a raw Python
    traceback on stderr from this layer.
    """
    parser = _build_arg_parser(prog, description)
    args = parser.parse_args(argv)
    logger = _configure_logging(args.log_level, server_name)
    try:
        rc = _maybe_load_product_config(args.config_path, logger)
        if rc != 0:
            return rc
        return _serve_stdio(
            server_name, server_version, list_tools_fn, get_tool_fn, logger
        )
    except Exception:
        logger.exception("Fatal error in %s entrypoint", server_name)
        return 1
