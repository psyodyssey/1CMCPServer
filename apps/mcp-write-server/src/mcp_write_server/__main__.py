"""Stdio entrypoint for ``mcp-write-server`` (Track G / Step 4).

Run as ``python -m mcp_write_server`` or via the ``mcp-write-server``
console script declared in ``pyproject.toml``. The transport is
line-delimited JSON-RPC 2.0 over stdin/stdout; diagnostic output is
written to stderr. Tool dispatch goes through the existing
``server.py`` boundary (``list_tools`` / ``get_tool``); the
``run_write_flow`` discipline applied inside the tool callables is
preserved unchanged.
"""

from mcp_common._stdio_transport import run_main

from .server import get_tool, list_tools

SERVER_NAME = "mcp-write-server"
SERVER_VERSION = "0.3.0"


def main() -> int:
    return run_main(
        prog="python -m mcp_write_server",
        description=(
            "Local stdio MCP server exposing the 1C write tools "
            "registered in mcp_write_server.server."
        ),
        server_name=SERVER_NAME,
        server_version=SERVER_VERSION,
        list_tools_fn=list_tools,
        get_tool_fn=get_tool,
    )


if __name__ == "__main__":
    raise SystemExit(main())
