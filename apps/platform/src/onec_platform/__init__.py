"""onec_platform — product layer of 1C Agent Platform.

This package wraps the existing read / write / intelligence MCP
servers into a **product-layer** surface. It is **not** an MCP
server itself — it does not register MCP tools and it is not loaded
by the dev-check selfcheck.

Phase 5 surface as of Step 3:

- **Step 2 (bootstrap contract).** product-config schema +
  JSON loader + prereqs doctor + bootstrap entrypoint:
  :class:`ProductConfig`, :class:`ProductServerToggles`,
  :class:`ProductBootstrapSettings`, :class:`DoctorFinding`,
  :class:`DoctorReport`, :class:`BootstrapResult`,
  :func:`load_product_config`,
  :func:`load_product_config_from_json_file`,
  :func:`run_prereqs_doctor`, :func:`bootstrap_product`,
  :func:`bootstrap_product_from_json_file`.
- **Step 3 (runtime orchestration / single entry point).**
  Declarative runtime contract + atomic state file + cross-platform
  process supervision over operator-declared argv lists:
  :class:`ProductServiceSpec`, :class:`ProductRuntimeSettings`,
  :class:`RuntimeServiceState`, :class:`RuntimeStateFile`,
  :class:`RuntimeOperationResult`, :class:`RuntimeStatusResult`,
  :func:`start_product_runtime`, :func:`stop_product_runtime`,
  :func:`get_product_runtime_status`,
  :func:`reload_product_runtime`, plus their ``_from_json_file``
  variants.
- **Step 4 (environment doctor / health dashboard).** Single
  product-level read-only aggregator over Step 2 bootstrap, Step 3
  runtime, read-side health/diagnosis, intelligence-side
  runtime/risk: :class:`DashboardSectionResult`,
  :class:`DashboardVerdict`, :class:`EnvironmentDashboardResult`,
  :func:`build_environment_dashboard`,
  :func:`build_environment_dashboard_from_json_file`. Verdict is a
  hand-written, deterministic ruleset documented in the product
  README; ``ready_for_workflows=True`` is reserved for the
  ``healthy`` verdict.
- **Step 5 (guided workflow layer).** Three end-to-end product
  workflows that orchestrate intelligence + write surfaces with an
  explicit operator confirm gate: ``safe-add-attribute``,
  ``safe-add-module-method``, ``stand-health-check``.
  Models: :class:`WorkflowStepResult`, :class:`WorkflowPlan`,
  :class:`WorkflowRunResult`. Boundary helpers:
  :func:`run_guided_workflow`,
  :func:`run_guided_workflow_from_json_file`. Mutating workflows
  refuse to execute unless ``confirm_execute=True`` AND the Step 4
  dashboard is in ``ready_for_workflows`` state. Every mutating
  step goes through the existing public write-tool (which itself
  wraps :func:`mcp_write_server.runtime.run_write_flow`); the
  product layer never bypasses preflight / snapshot / verify /
  audit.
- **Step 6 (rollback / recovery / audit UX).** Three boundary
  helpers over the existing audit JSONL plus
  :func:`mcp_write_server.tools.prepare_rollback_hint` /
  :func:`mcp_write_server.tools.describe_last_write_operation`:
  :func:`get_operation_history` (history viewer),
  :func:`inspect_operation` (focus on one ``operation_id``), and
  :func:`run_rollback_assistant` (preview / advisory by default;
  honest ``mode=unsupported`` for any current write-tool family
  when ``confirm_execute=True``, because Step 6 ships **no**
  automatic content-level rollback path — there are no public
  ``delete_*`` write-tools and the product layer must not
  back-door write to the dump). Models:
  :class:`OperationHistoryEntry`, :class:`OperationHistorySummary`,
  :class:`OperationHistoryResult`, :class:`OperationInspectResult`,
  :class:`RollbackPlan`, :class:`RollbackAssistantResult`.
- **Step 7 (real-stand / 1cv8 binary integration track).** Two
  boundary helpers built on top of the new
  :class:`onec_config.EnvironmentConfig.onec_binary_path` /
  :class:`onec_config.EnvironmentConfig.onec_binary_probe_args`
  optional fields: :func:`get_real_stand_readiness` (read-only
  doctor — binary file exists / file vs. directory / executable
  bit on POSIX / dashboard verdict / paths consistency) and
  :func:`run_real_stand_smoke_test` (preview by default;
  ``confirm_execute=True`` runs a controlled subprocess via
  :mod:`onec_process_runner` using **operator-declared** probe
  argv — the platform never invents 1cv8-specific CLI flags).
  Note: flipping ``create_dump_snapshot`` /
  ``apply_config_from_files`` / ``update_database_configuration``
  onto an honest dual-mode contract was a separate parallel track
  (Track A / Steps 2–4) and lives in ``mcp-write-server``; the
  platform-layer smoke surface itself is still a bounded probe and
  does not chain those tools end-to-end. Models:
  :class:`RealStandReadinessResult`, :class:`RealStandSmokeResult`.

Phase 5 / Step 3 honesty:

- The product layer does **not** introduce MCP transport into
  read / write / intelligence on this step. It manages whatever
  long-lived argv-list commands the operator declared in
  ``ProductConfig.runtime``. If a service has no command, the
  orchestrator fails closed for that service rather than guessing.
- ``reload`` is a controlled stop-then-start, **not** a hot reload.
- Boundary helpers
  (:func:`bootstrap_product`, :func:`bootstrap_product_from_json_file`,
  :func:`start_product_runtime`, :func:`stop_product_runtime`,
  :func:`get_product_runtime_status`,
  :func:`reload_product_runtime`, plus ``_from_json_file`` variants)
  **never raise**; they return structured results.
- Inner helpers (:func:`load_product_config`,
  :func:`load_product_config_from_json_file`) raise
  :class:`ValueError` on bad input — fail-closed by design.
- ``onec_platform`` does **not** import :mod:`onec_policy_engine`
  and does **not** depend on it. The product layer never performs
  write operations against an infobase from inside the orchestrator;
  any mutation still goes through ``mcp-write-server`` and its
  ``run_write_flow``.
"""

from .bootstrap import (
    bootstrap_product,
    bootstrap_product_from_json_file,
)
from .dashboard import (
    build_environment_dashboard,
    build_environment_dashboard_from_json_file,
)
from .doctor import run_prereqs_doctor
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .enterprise import (
    inspect_enterprise_foundation,
    inspect_enterprise_foundation_from_json_file,
)
from .models import (
    BootstrapResult,
    DASHBOARD_OVERALL_STATUSES,
    DEPLOYMENT_TIERS,
    DashboardSectionResult,
    DashboardVerdict,
    DoctorFinding,
    DoctorReport,
    EnterpriseFoundationResult,
    EnterpriseFoundationSettings,
    EnvironmentDashboardResult,
    FOUNDATION_LEVELS,
    INSTALL_MODES,
    InstallFastPathResult,
    OperationHistoryEntry,
    OperationHistoryResult,
    OperationHistorySummary,
    OperationInspectResult,
    ProductBootstrapSettings,
    ProductConfig,
    ProductConfigTemplateResult,
    ProductRuntimeSettings,
    ProductServerToggles,
    ProductServiceSpec,
    REAL_STAND_SMOKE_MODES,
    RECOVERY_MODES,
    RUNTIME_STATE_SCHEMA_VERSION,
    RUNTIME_STATUSES,
    RealStandReadinessResult,
    RealStandSmokeResult,
    ReleaseLayoutReport,
    RollbackAssistantResult,
    RollbackPlan,
    RuntimeOperationResult,
    RuntimeServiceState,
    RuntimeStateFile,
    RuntimeStatusResult,
    WORKFLOW_MODES,
    WORKFLOW_NAMES,
    WorkflowPlan,
    WorkflowRunResult,
    WorkflowStepResult,
)
from .installer import (
    inspect_release_layout,
    run_install_fast_path,
    run_install_fast_path_from_json_file,
)
from .realstand import (
    get_real_stand_readiness,
    get_real_stand_readiness_from_json_file,
    run_real_stand_smoke_test,
    run_real_stand_smoke_test_from_json_file,
)
from .recovery import (
    get_operation_history,
    get_operation_history_from_json_file,
    inspect_operation,
    inspect_operation_from_json_file,
    run_rollback_assistant,
    run_rollback_assistant_from_json_file,
)
from .templates import build_product_config_template
from .runtime import (
    get_product_runtime_status,
    get_product_runtime_status_from_json_file,
    reload_product_runtime,
    reload_product_runtime_from_json_file,
    start_product_runtime,
    start_product_runtime_from_json_file,
    stop_product_runtime,
    stop_product_runtime_from_json_file,
)
from .state import runtime_dir, state_file_path
from .workflow import (
    run_guided_workflow,
    run_guided_workflow_from_json_file,
)

__all__ = [
    # Step 2 surface (unchanged).
    "ProductConfig",
    "ProductServerToggles",
    "ProductBootstrapSettings",
    "DoctorFinding",
    "DoctorReport",
    "BootstrapResult",
    "load_product_config",
    "load_product_config_from_json_file",
    "run_prereqs_doctor",
    "bootstrap_product",
    "bootstrap_product_from_json_file",
    # Step 3 surface — runtime models.
    "ProductServiceSpec",
    "ProductRuntimeSettings",
    "RUNTIME_STATUSES",
    "RUNTIME_STATE_SCHEMA_VERSION",
    "RuntimeServiceState",
    "RuntimeStateFile",
    "RuntimeOperationResult",
    "RuntimeStatusResult",
    # Step 3 surface — boundary helpers.
    "start_product_runtime",
    "stop_product_runtime",
    "get_product_runtime_status",
    "reload_product_runtime",
    "start_product_runtime_from_json_file",
    "stop_product_runtime_from_json_file",
    "get_product_runtime_status_from_json_file",
    "reload_product_runtime_from_json_file",
    # Step 3 surface — state helpers (path discovery only).
    "runtime_dir",
    "state_file_path",
    # Step 4 surface — environment doctor / health dashboard.
    "DASHBOARD_OVERALL_STATUSES",
    "DashboardSectionResult",
    "DashboardVerdict",
    "EnvironmentDashboardResult",
    "build_environment_dashboard",
    "build_environment_dashboard_from_json_file",
    # Step 5 surface — guided workflow layer.
    "WORKFLOW_NAMES",
    "WORKFLOW_MODES",
    "WorkflowStepResult",
    "WorkflowPlan",
    "WorkflowRunResult",
    "run_guided_workflow",
    "run_guided_workflow_from_json_file",
    # Step 6 surface — rollback / recovery / audit UX.
    "RECOVERY_MODES",
    "OperationHistoryEntry",
    "OperationHistorySummary",
    "OperationHistoryResult",
    "OperationInspectResult",
    "RollbackPlan",
    "RollbackAssistantResult",
    "get_operation_history",
    "get_operation_history_from_json_file",
    "inspect_operation",
    "inspect_operation_from_json_file",
    "run_rollback_assistant",
    "run_rollback_assistant_from_json_file",
    # Step 7 surface — real-stand / 1cv8 binary integration track.
    "REAL_STAND_SMOKE_MODES",
    "RealStandReadinessResult",
    "RealStandSmokeResult",
    "get_real_stand_readiness",
    "get_real_stand_readiness_from_json_file",
    "run_real_stand_smoke_test",
    "run_real_stand_smoke_test_from_json_file",
    # Phase 6 / Step 3 surface — installer / setup fast path.
    "INSTALL_MODES",
    "ProductConfigTemplateResult",
    "ReleaseLayoutReport",
    "InstallFastPathResult",
    "build_product_config_template",
    "inspect_release_layout",
    "run_install_fast_path",
    "run_install_fast_path_from_json_file",
    # Phase 6 / Step 8 surface — enterprise foundation inspector.
    "DEPLOYMENT_TIERS",
    "FOUNDATION_LEVELS",
    "EnterpriseFoundationSettings",
    "EnterpriseFoundationResult",
    "inspect_enterprise_foundation",
    "inspect_enterprise_foundation_from_json_file",
]
