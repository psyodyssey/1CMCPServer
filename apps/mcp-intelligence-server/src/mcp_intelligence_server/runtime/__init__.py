"""Internal analysis helper layer for mcp-intelligence-server (Phase 4 / Step 3).

Stays strictly below the public tool layer. Nothing here is a
``ToolResult`` and nothing here is registered in
``server.REGISTERED_TOOLS``. This subpackage is the foundation that
future public intelligence-tools (Phase 4 Steps 4–6) will stand on:

- dependency / reference analysis (``find_references_to_object``,
  ``analyze_object_dependencies``, ``find_module_method_usages``,
  ``build_dependency_subgraph``);
- change-impact analysis
  (``estimate_change_impact``, ``find_affected_forms``,
  ``find_affected_modules``);
- troubleshooting (``analyze_runtime_issue``,
  ``diagnose_missing_method_or_attribute``);
- recommendations (``suggest_fix_for_issue``,
  ``prepare_intelligence_report``).

Read-only by construction (Phase 4 guardrail):

- Does **not** import :mod:`onec_policy_engine`.
- Does **not** write files, mutate the infobase, or emit audit
  records.
- Allowed cross-app direction only: ``intelligence → read`` (see
  :mod:`mcp_read_server.runtime`) and ``intelligence → write`` via
  pure / read-only helpers (e.g.
  ``mcp_write_server.runtime.metadata_ops.module_contains_method``).
"""

from .context import build_runtime_context
from .dump_scanner import (
    list_bsl_files,
    list_files_by_extensions,
    list_xml_files,
    read_utf8_text,
)
from .graph import (
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
    add_edge,
    add_node,
    empty_graph,
    neighbors,
)
from .models import IntelligenceRuntimeContext
from .reference_finder import ReferenceMatch, count_references, find_references

__all__ = [
    "IntelligenceRuntimeContext",
    "build_runtime_context",
    "list_xml_files",
    "list_bsl_files",
    "list_files_by_extensions",
    "read_utf8_text",
    "ReferenceMatch",
    "find_references",
    "count_references",
    "DependencyNode",
    "DependencyEdge",
    "DependencyGraph",
    "empty_graph",
    "add_node",
    "add_edge",
    "neighbors",
]
