"""Shared response envelope returned by MCP tools across all platform servers."""

from dataclasses import dataclass


@dataclass
class ToolResult:
    """Standard result envelope returned by MCP tools."""

    ok: bool
    tool_name: str
    message: str
    payload: dict | None = None
