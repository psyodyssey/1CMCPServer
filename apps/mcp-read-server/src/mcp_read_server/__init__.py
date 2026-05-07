"""mcp_read_server — read-only MCP server of 1C Agent Platform (skeleton)."""

from .models import ToolResult
from .server import get_tool, list_tools
from .tools import health_summary, ping

__all__ = [
    "ToolResult",
    "ping",
    "health_summary",
    "list_tools",
    "get_tool",
]
