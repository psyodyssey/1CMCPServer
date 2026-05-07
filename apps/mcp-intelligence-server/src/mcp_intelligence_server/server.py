"""Skeleton server bootstrap for mcp-intelligence-server.

Holds only a tool registry and lookup helpers. Real MCP transport,
dependency analysis, linting, impact analysis and troubleshooting logic
will be added later.

Phase 4 contract: this module and every tool it registers are
read-only by construction. In particular, this bootstrap does
**not** import ``onec_policy_engine``; intelligence operations are
not routed through ``check_write_allowed``. See the package-level
docstring in ``mcp_intelligence_server/__init__.py`` for the full
read-only contract and allowed cross-app import directions.
"""

from mcp_common import (
    ToolCallable,
    build_tool_registry,
    get_registered_tool,
    list_registered_tools,
)

from .tools import (
    analyze_event_log_patterns,
    analyze_object_dependencies,
    analyze_runtime_issue,
    diagnose_broken_form_binding,
    diagnose_missing_method_or_attribute,
    estimate_change_impact,
    find_affected_forms,
    find_affected_modules,
    find_module_method_usages,
    find_references_to_object,
    ping,
    prepare_intelligence_report,
    suggest_fix_for_issue,
    suggest_metadata_patch_plan,
    suggest_safe_change_order,
    summarize_configuration_risk,
)

REGISTERED_TOOLS: dict[str, ToolCallable] = build_tool_registry(
    {
        "ping": ping,
        "find_references_to_object": find_references_to_object,
        "find_module_method_usages": find_module_method_usages,
        "analyze_object_dependencies": analyze_object_dependencies,
        "analyze_runtime_issue": analyze_runtime_issue,
        "analyze_event_log_patterns": analyze_event_log_patterns,
        "diagnose_broken_form_binding": diagnose_broken_form_binding,
        "diagnose_missing_method_or_attribute": diagnose_missing_method_or_attribute,
        "estimate_change_impact": estimate_change_impact,
        "find_affected_forms": find_affected_forms,
        "find_affected_modules": find_affected_modules,
        "suggest_safe_change_order": suggest_safe_change_order,
        "suggest_fix_for_issue": suggest_fix_for_issue,
        "suggest_metadata_patch_plan": suggest_metadata_patch_plan,
        "summarize_configuration_risk": summarize_configuration_risk,
        "prepare_intelligence_report": prepare_intelligence_report,
    }
)


def list_tools() -> list[str]:
    """Return names of registered tools, sorted alphabetically."""
    return list_registered_tools(REGISTERED_TOOLS)


def get_tool(name: str) -> ToolCallable | None:
    """Return the registered tool callable by name, or ``None``."""
    return get_registered_tool(REGISTERED_TOOLS, name)
