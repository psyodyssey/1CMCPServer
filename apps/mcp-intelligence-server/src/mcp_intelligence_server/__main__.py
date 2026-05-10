"""Stdio entrypoint for ``mcp-intelligence-server`` (Track G / Step 4).

Run as ``python -m mcp_intelligence_server`` or via the
``mcp-intelligence-server`` console script declared in
``pyproject.toml``. The transport is line-delimited JSON-RPC 2.0 over
stdin/stdout; diagnostic output is written to stderr. Tool dispatch
goes through the existing ``server.py`` boundary (``list_tools`` /
``get_tool``); the read-only-by-construction contract of the
intelligence package (no ``run_write_flow``, no ``check_write_allowed``)
is preserved unchanged.
"""

from mcp_common._stdio_transport import run_main

from .server import get_tool, list_tools

SERVER_NAME = "mcp-intelligence-server"
SERVER_VERSION = "0.3.0"


def main() -> int:
    return run_main(
        prog="python -m mcp_intelligence_server",
        description=(
            "Local stdio MCP server exposing the read-only 1C "
            "intelligence tools registered in mcp_intelligence_server.server."
        ),
        server_name=SERVER_NAME,
        server_version=SERVER_VERSION,
        list_tools_fn=list_tools,
        get_tool_fn=get_tool,
    )


if __name__ == "__main__":
    raise SystemExit(main())
