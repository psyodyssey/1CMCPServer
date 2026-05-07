"""Skeleton server bootstrap for mcp-read-server.

Holds only a tool registry and lookup helpers. Real MCP transport and
framework wiring will be added in a later step.
"""

from mcp_common import (
    ToolCallable,
    build_tool_registry,
    get_registered_tool,
    list_registered_tools,
)

from .tools import (
    check_runtime_health,
    diagnose_connectivity_issue,
    execute_read_query,
    get_configuration_info,
    get_event_log,
    get_form_structure,
    get_metadata_object,
    get_metadata_tree,
    get_object_structure,
    health_summary,
    ping,
    read_module_code_from_dump,
    search_code,
    search_metadata,
    validate_query,
)

REGISTERED_TOOLS: dict[str, ToolCallable] = build_tool_registry(
    {
        "ping": ping,
        "health_summary": health_summary,
        "get_configuration_info": get_configuration_info,
        "get_metadata_tree": get_metadata_tree,
        "get_metadata_object": get_metadata_object,
        "read_module_code_from_dump": read_module_code_from_dump,
        "search_code": search_code,
        "search_metadata": search_metadata,
        "validate_query": validate_query,
        "execute_read_query": execute_read_query,
        "get_event_log": get_event_log,
        "get_object_structure": get_object_structure,
        "get_form_structure": get_form_structure,
        "check_runtime_health": check_runtime_health,
        "diagnose_connectivity_issue": diagnose_connectivity_issue,
    }
)


def list_tools() -> list[str]:
    """Return names of registered tools, sorted alphabetically."""
    return list_registered_tools(REGISTERED_TOOLS)


def get_tool(name: str) -> ToolCallable | None:
    """Return the registered tool callable by name, or ``None``."""
    return get_registered_tool(REGISTERED_TOOLS, name)
