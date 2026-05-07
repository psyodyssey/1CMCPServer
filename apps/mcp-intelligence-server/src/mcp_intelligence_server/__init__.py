"""mcp_intelligence_server — intelligence MCP server of 1C Agent Platform.

Phase 4 contract (read-only by construction):

- Intelligence-tools never mutate state. No file write, no live
  update, no ``run_write_flow``, no audit record. Any mutation
  remains the responsibility of ``mcp-write-server``.
- This package deliberately does **not** import
  ``onec_policy_engine.check_write_allowed``. Intelligence
  operations are not routed through the write-policy engine,
  mirroring the existing ``mcp-read-server`` pattern.
- Allowed cross-app imports go **forward only**:
  ``intelligence → read`` and ``intelligence → write`` only via
  pure / read-only helpers (e.g.
  ``mcp_write_server.runtime.metadata_ops.module_contains_method``).
  Read- and write-servers never import from intelligence.

Public tool surface as of Phase 4 / Step 6 — sixteen tools across
four groups:

- liveness: ``ping``;
- group A (dependency / reference analysis, Step 4):
  ``find_references_to_object``, ``find_module_method_usages``,
  ``analyze_object_dependencies``;
- group C (diagnostics / troubleshooting, Step 5):
  ``analyze_runtime_issue``, ``analyze_event_log_patterns``,
  ``diagnose_broken_form_binding``,
  ``diagnose_missing_method_or_attribute``;
- group B (impact / affected scope, Step 6):
  ``estimate_change_impact``, ``find_affected_forms``,
  ``find_affected_modules``, ``suggest_safe_change_order``;
- group D (recommendations / planning / summarization, Step 6):
  ``suggest_fix_for_issue``, ``suggest_metadata_patch_plan``,
  ``summarize_configuration_risk``, ``prepare_intelligence_report``.
"""

from .models import ToolResult
from .server import get_tool, list_tools
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

__all__ = [
    "ToolResult",
    "ping",
    "find_references_to_object",
    "find_module_method_usages",
    "analyze_object_dependencies",
    "analyze_runtime_issue",
    "analyze_event_log_patterns",
    "diagnose_broken_form_binding",
    "diagnose_missing_method_or_attribute",
    "estimate_change_impact",
    "find_affected_forms",
    "find_affected_modules",
    "suggest_safe_change_order",
    "suggest_fix_for_issue",
    "suggest_metadata_patch_plan",
    "summarize_configuration_risk",
    "prepare_intelligence_report",
    "list_tools",
    "get_tool",
]
