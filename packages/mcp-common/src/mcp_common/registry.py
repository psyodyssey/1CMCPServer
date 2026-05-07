"""Shared tool registry helpers used by all MCP servers of the platform."""

from typing import Callable

ToolCallable = Callable[..., object]


def build_tool_registry(tools: dict[str, ToolCallable]) -> dict[str, ToolCallable]:
    """Return a shallow copy of the given tool mapping."""
    return dict(tools)


def list_registered_tools(registry: dict[str, ToolCallable]) -> list[str]:
    """Return names of registered tools, sorted alphabetically."""
    return sorted(registry)


def get_registered_tool(
    registry: dict[str, ToolCallable], name: str
) -> ToolCallable | None:
    """Return the registered tool callable by name, or ``None`` if absent."""
    return registry.get(name)
