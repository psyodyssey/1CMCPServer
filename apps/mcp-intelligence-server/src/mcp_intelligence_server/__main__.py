"""Entrypoint for ``mcp-intelligence-server`` (Track G stdio + Track H HTTP).

Run as ``python -m mcp_intelligence_server`` or via the
``mcp-intelligence-server`` console script declared in
``pyproject.toml``. Two transports are supported:

- ``--transport stdio`` (default; Track G / Step 4) — line-delimited
  JSON-RPC 2.0 over stdin/stdout; trusted local subprocess model.
- ``--transport http`` (Track H / Step 4) — HTTP/1.1 ``/mcp``
  endpoint with bearer-token authentication; trusted-network
  deployment behind operator's reverse proxy.

Diagnostic output is written to stderr. Tool dispatch goes through
the existing ``server.py`` boundary (``list_tools`` / ``get_tool``)
on both transports; the read-only-by-construction contract of the
intelligence package (no ``run_write_flow``, no
``check_write_allowed``) is preserved unchanged on both transports.
"""

from mcp_common._network_transport import run_main_http

from .server import get_tool, list_tools

SERVER_NAME = "mcp-intelligence-server"
SERVER_VERSION = "0.4.0"


def main() -> int:
    return run_main_http(
        prog="python -m mcp_intelligence_server",
        description=(
            "MCP server exposing the read-only 1C intelligence tools "
            "registered in mcp_intelligence_server.server. Defaults to "
            "local stdio transport (Track G); use --transport http for "
            "the Track H HTTP transport with bearer-token "
            "authentication."
        ),
        server_name=SERVER_NAME,
        server_version=SERVER_VERSION,
        list_tools_fn=list_tools,
        get_tool_fn=get_tool,
    )


if __name__ == "__main__":
    raise SystemExit(main())
