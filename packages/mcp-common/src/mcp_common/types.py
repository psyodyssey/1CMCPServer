"""Shared typed structures used across MCP servers."""

from dataclasses import dataclass


@dataclass
class OperationContext:
    """Context of a single MCP tool invocation."""

    operation_id: str
    environment: str
    base_id: str
    tool_name: str
    allow_write: bool = False
