"""mcp_common — shared building blocks for 1C Agent Platform MCP servers."""

from .errors import (
    HealthCheckError,
    PlatformError,
    PolicyDeniedError,
    ProcessExecutionError,
)
from .registry import (
    ToolCallable,
    build_tool_registry,
    get_registered_tool,
    list_registered_tools,
)
from .result import ToolResult
from .types import OperationContext

__all__ = [
    "OperationContext",
    "PlatformError",
    "PolicyDeniedError",
    "ProcessExecutionError",
    "HealthCheckError",
    "ToolResult",
    "ToolCallable",
    "build_tool_registry",
    "list_registered_tools",
    "get_registered_tool",
]
