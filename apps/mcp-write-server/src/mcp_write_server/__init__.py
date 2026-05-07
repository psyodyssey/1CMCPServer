"""mcp_write_server — write MCP server of 1C Agent Platform (skeleton)."""

from .models import ToolResult
from .server import get_tool, list_tools
from .tools import ping

__all__ = [
    "ToolResult",
    "ping",
    "list_tools",
    "get_tool",
]
