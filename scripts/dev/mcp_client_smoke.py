"""Track K closure-gate harness: minimum-viable real MCP client smoke.

Exercises the platform's existing MCP server surface
(``mcp-read-server`` / ``mcp-write-server`` /
``mcp-intelligence-server``) end-to-end via JSON-RPC 2.0
over both ``--transport stdio`` and ``--transport http``.

Step 4 PATH B deliverable for Parallel Track K — Real MCP
Client Integration Test. Pinned by
``docs/architecture/track-k-real-mcp-client-integration-test-contract.md``
§9 (PATH B) / §10.1 (this file location) / §7 (minimum
scenario) / §6 (transport coverage).

Stdlib-only. Does NOT:
  - import ``mcp_common._stdio_transport`` /
    ``mcp_common._network_transport`` (server-side
    internals; per contract §10.3);
  - rely on any third-party MCP SDK, HTTP client library,
    or test framework;
  - require operator-supplied credentials, hostnames, or
    certificates;
  - run ``1cv8.exe`` or touch a 1C infobase;
  - modify any production code.

Synthetic bearer tokens are generated via
``secrets.token_urlsafe`` at run time and exported into the
server subprocess via the ``--auth-token-env`` flag. The
token value is never printed at any verbosity level.

Usage (PYTHONPATH bootstrap optional — the harness builds
its own ``PYTHONPATH`` for the server subprocess)::

    python scripts/dev/mcp_client_smoke.py --server read --transport both

Success: exit code 0 + final ``OK`` line on stdout.
Failure: exit code != 0 + clear ``FAIL: ...`` description.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import secrets
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

PROTOCOL_VERSION = "2024-11-05"
JSONRPC_AUTH_FAIL_CODE = -32001
TOKEN_ENV_VARNAME = "MCP_CLIENT_SMOKE_TOKEN"
SERVER_MODULES = {
    "read": "mcp_read_server",
    "write": "mcp_write_server",
    "intelligence": "mcp_intelligence_server",
}
HTTP_STARTUP_TIMEOUT_S = 10.0
HTTP_REQUEST_TIMEOUT_S = 10.0
SHUTDOWN_TIMEOUT_S = 5.0


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        print(f"FAIL: {msg}", file=sys.stderr)
        raise SystemExit(1)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _build_env_with_pythonpath() -> dict[str, str]:
    """Construct env for the server subprocess with PYTHONPATH preset.

    Mirrors ``scripts/dev/bootstrap_paths.ps1`` so the harness works
    whether or not the operator has already dot-sourced that script.
    Existing ``PYTHONPATH`` (if any) is appended after, not replaced.
    """
    root = _project_root()
    src_paths = [
        root / "apps" / "mcp-read-server" / "src",
        root / "apps" / "mcp-write-server" / "src",
        root / "apps" / "mcp-intelligence-server" / "src",
        root / "apps" / "platform" / "src",
        root / "packages" / "mcp-common" / "src",
        root / "packages" / "onec-process-runner" / "src",
        root / "packages" / "onec-policy-engine" / "src",
        root / "packages" / "onec-audit" / "src",
        root / "packages" / "onec-health" / "src",
        root / "packages" / "onec-troubleshooting" / "src",
        root / "packages" / "onec-config" / "src",
    ]
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    joined = os.pathsep.join(str(p) for p in src_paths)
    env["PYTHONPATH"] = joined + (os.pathsep + existing if existing else "")
    return env


def _pick_ephemeral_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _shutdown(proc: subprocess.Popen) -> None:
    """Close stdin (if open), terminate, escalate to kill on timeout."""
    if proc.stdin is not None and not proc.stdin.closed:
        with contextlib.suppress(Exception):
            proc.stdin.close()
    try:
        proc.terminate()
        proc.wait(timeout=SHUTDOWN_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=SHUTDOWN_TIMEOUT_S)


def _send_stdio(proc: subprocess.Popen, req: dict[str, Any]) -> dict[str, Any]:
    assert proc.stdin is not None
    assert proc.stdout is not None
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    reply = proc.stdout.readline()
    _assert(reply.strip() != "", f"stdio: empty response for method={req.get('method')!r}")
    try:
        return json.loads(reply)
    except json.JSONDecodeError as exc:
        _assert(False, f"stdio: response not JSON for method={req.get('method')!r}: {exc}")
        raise  # unreachable


def _http_post(
    url: str, body: dict[str, Any], *, auth_header: str | None
) -> tuple[int, dict[str, str], bytes]:
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if auth_header is not None:
        headers["Authorization"] = auth_header
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=HTTP_REQUEST_TIMEOUT_S) as resp:
            return resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()


def _assert_initialize(resp: dict[str, Any]) -> None:
    _assert(resp.get("jsonrpc") == "2.0", "initialize: missing jsonrpc=2.0")
    _assert("result" in resp, f"initialize: missing 'result' (keys={sorted(resp.keys())})")
    result = resp["result"]
    _assert(
        result.get("protocolVersion") == PROTOCOL_VERSION,
        f"initialize.protocolVersion != {PROTOCOL_VERSION!r}",
    )
    si = result.get("serverInfo")
    _assert(isinstance(si, dict), "initialize.serverInfo not a dict")
    _assert(isinstance(si.get("name"), str) and si["name"], "initialize.serverInfo.name empty")
    _assert(isinstance(si.get("version"), str) and si["version"], "initialize.serverInfo.version empty")
    caps = result.get("capabilities")
    _assert(isinstance(caps, dict) and "tools" in caps, "initialize.capabilities.tools missing")


def _assert_tools_list(resp: dict[str, Any]) -> list[dict[str, Any]]:
    _assert("result" in resp, "tools/list: missing 'result'")
    tools = resp["result"].get("tools")
    _assert(isinstance(tools, list) and len(tools) >= 1, "tools/list: empty or non-list")
    for entry in tools:
        _assert(isinstance(entry, dict), "tools/list: entry not a dict")
        _assert(isinstance(entry.get("name"), str) and entry["name"], "tools/list: name empty")
        _assert(isinstance(entry.get("description"), str), "tools/list: description missing")
        _assert(isinstance(entry.get("inputSchema"), dict), "tools/list: inputSchema not a dict")
    return tools


def _assert_tools_call(resp: dict[str, Any]) -> None:
    """Accept either a well-shaped result envelope or a well-shaped error.

    Per contract §7.1.4: a read-only tool invoked with synthetic empty
    arguments may legitimately return ``isError=True`` (well-shaped) or
    a JSON-RPC error envelope from server-side argument validation
    (also well-shaped). Both prove the dispatch + envelope-shaping
    pipeline; either is acceptable closure-gate evidence.
    """
    _assert("result" in resp or "error" in resp, "tools/call: missing both result and error")
    if "result" in resp:
        result = resp["result"]
        _assert(isinstance(result, dict), "tools/call: result not a dict")
        content = result.get("content")
        _assert(isinstance(content, list) and len(content) >= 1, "tools/call: content empty")
        first = content[0]
        _assert(isinstance(first, dict) and "type" in first, "tools/call: content[0] missing type")
        if first.get("type") == "text":
            _assert(isinstance(first.get("text"), str), "tools/call: content[0].text not a string")
    else:
        err = resp["error"]
        _assert(isinstance(err, dict), "tools/call: error not a dict")
        _assert(isinstance(err.get("code"), int), "tools/call: error.code not int")
        _assert(isinstance(err.get("message"), str), "tools/call: error.message not str")


def _exercise_envelope(send: Callable[[dict[str, Any]], dict[str, Any]], tag: str) -> None:
    print(f"  [{tag}] initialize ...")
    _assert_initialize(send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}))
    print(f"  [{tag}] tools/list ...")
    tools = _assert_tools_list(
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    )
    chosen = tools[0]["name"]
    print(f"  [{tag}] tools/call name={chosen!r} (synthetic empty args) ...")
    _assert_tools_call(
        send({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": chosen, "arguments": {}},
        })
    )
    print(f"  [{tag}] envelope shape OK")


def run_stdio_scenario(server_key: str, env: dict[str, str]) -> None:
    module = SERVER_MODULES[server_key]
    print(f"[stdio] launching python -m {module} --transport stdio")
    proc = subprocess.Popen(
        [sys.executable, "-m", module, "--transport", "stdio", "--log-level", "WARNING"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        env=env, text=True, encoding="utf-8", bufsize=1,
    )
    try:
        _exercise_envelope(lambda req: _send_stdio(proc, req), f"{server_key}/stdio")
    finally:
        _shutdown(proc)
    print("[stdio] shutdown clean")


def _wait_for_http(port: int) -> None:
    deadline = time.time() + HTTP_STARTUP_TIMEOUT_S
    while time.time() < deadline:
        try:
            with contextlib.closing(socket.create_connection(("127.0.0.1", port), timeout=0.5)):
                return
        except OSError:
            time.sleep(0.1)
    _assert(False, f"http: server did not bind 127.0.0.1:{port} within {HTTP_STARTUP_TIMEOUT_S}s")


def _assert_auth_failure(status: int, headers: dict[str, str], body: bytes) -> None:
    _assert(status == 401, f"missing-auth probe: expected 401, got {status}")
    _assert(
        headers.get("www-authenticate") == 'Bearer realm="mcp"',
        f"missing-auth probe: WWW-Authenticate != 'Bearer realm=\"mcp\"' "
        f"(got {headers.get('www-authenticate')!r})",
    )
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        _assert(False, "missing-auth probe: response body not JSON")
        return
    err = envelope.get("error")
    _assert(isinstance(err, dict), "missing-auth probe: 'error' missing in envelope")
    _assert(
        err.get("code") == JSONRPC_AUTH_FAIL_CODE,
        f"missing-auth probe: error.code != {JSONRPC_AUTH_FAIL_CODE} (got {err.get('code')!r})",
    )


def run_http_scenario(server_key: str, env: dict[str, str]) -> None:
    module = SERVER_MODULES[server_key]
    port = _pick_ephemeral_port()
    token_value = secrets.token_urlsafe(32)  # NEVER print this value.
    child_env = dict(env)
    child_env[TOKEN_ENV_VARNAME] = token_value
    print(
        f"[http] launching python -m {module} --transport http "
        f"--bind 127.0.0.1:{port} --auth-token-env {TOKEN_ENV_VARNAME}"
    )
    proc = subprocess.Popen(
        [
            sys.executable, "-m", module, "--transport", "http",
            "--bind", f"127.0.0.1:{port}",
            "--auth-token-env", TOKEN_ENV_VARNAME,
            "--log-level", "WARNING",
        ],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env=child_env,
    )
    try:
        _wait_for_http(port)
        url = f"http://127.0.0.1:{port}/mcp"
        auth_header = f"Bearer {token_value}"

        def send(body: dict[str, Any]) -> dict[str, Any]:
            status, _h, payload = _http_post(url, body, auth_header=auth_header)
            _assert(status == 200, f"http /mcp expected 200, got {status}")
            return json.loads(payload)

        _exercise_envelope(send, f"{server_key}/http")

        print("[http] missing-Authorization probe ...")
        status, headers, payload = _http_post(
            url,
            {"jsonrpc": "2.0", "id": 99, "method": "tools/list", "params": {}},
            auth_header=None,
        )
        _assert_auth_failure(status, headers, payload)
        print("[http] missing-Authorization probe OK (401 + WWW-Authenticate + -32001)")
    finally:
        _shutdown(proc)
    print("[http] shutdown clean")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mcp_client_smoke",
        description="Track K closure-gate harness: stdio + HTTP MCP client smoke.",
    )
    parser.add_argument("--server", choices=sorted(SERVER_MODULES.keys()), default="read",
                        help="MCP server to exercise (default: read).")
    parser.add_argument("--transport", choices=["stdio", "http", "both"], default="both",
                        help="Transport(s) to exercise (default: both).")
    args = parser.parse_args(argv)

    env = _build_env_with_pythonpath()
    print(f"== mcp_client_smoke server={args.server} transport={args.transport} ==")

    if args.transport in ("stdio", "both"):
        run_stdio_scenario(args.server, env)
    if args.transport in ("http", "both"):
        run_http_scenario(args.server, env)

    print(f"OK (server={args.server} transport={args.transport})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
