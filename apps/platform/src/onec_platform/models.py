"""Dataclasses for the product layer.

All models are plain dataclasses. They carry no behavior of their
own; behavior lives in dedicated helper modules (``loader.py``,
``doctor.py``, ``bootstrap.py``, ``runtime.py``, ``state.py``,
``process_control.py``).

The product layer is anchored to ``onec_config.ProjectConfig`` for
the actual environments dict — the product layer does not duplicate
that schema, only adds product-level wrapping (product name, profile
name, default environment pointer, server toggles, bootstrap settings,
runtime contract).

Phase split:

- Phase 5 / Step 2 surface — ``ProductConfig`` + ``ProductServerToggles``
  + ``ProductBootstrapSettings`` + ``DoctorFinding`` / ``DoctorReport``
  + ``BootstrapResult``.
- Phase 5 / Step 3 surface — ``ProductServiceSpec`` +
  ``ProductRuntimeSettings`` + ``RuntimeServiceState`` +
  ``RuntimeStateFile`` + ``RuntimeOperationResult`` +
  ``RuntimeStatusResult``. ``ProductConfig`` is extended with a
  ``runtime`` field; missing-runtime-section in product-config is
  honest degradation, not a load error.
"""

from dataclasses import dataclass, field

from onec_config import ProjectConfig


@dataclass
class ProductBootstrapSettings:
    """Bootstrap/setup behavior toggles.

    ``work_dir`` is an optional product working directory; if set, the
    doctor checks that it exists and is a directory.

    ``require_*`` flags let an operator explicitly disable individual
    prereqs checks. Disabling is loud — the absence of a check is
    visible in the doctor report rather than silently skipped.
    """

    work_dir: str | None = None
    require_dump_path: bool = True
    require_base_path: bool = True
    require_python: bool = True


@dataclass
class ProductServerToggles:
    """Which platform MCP servers this product profile expects.

    The doctor checks importability of the selected server packages
    only. Disabling a server here suppresses its importability check;
    it does NOT remove the server from the platform itself.
    """

    read: bool = True
    write: bool = True
    intelligence: bool = True


# Allowed values for ``ProductServiceSpec.restart_policy``. Phase 6 /
# Step 6 deliberately ships only two: a default that does nothing and
# an opt-in policy that re-spawns a service whose persisted PID has
# gone stale, but **only** on a boundary call (start/status/reload).
# There is no background watcher / daemon / timer loop. Anything
# else (exponential backoff, max-restarts, on-crash, …) is out of
# scope for this slice and explicitly documented as such.
RESTART_POLICIES: tuple[str, ...] = (
    "never",
    "restart-if-stale",
)

# Default per-service log size threshold for the rotate-if-exceeds-
# size shim. 1 MiB is small enough to keep operator-visible diffs
# manageable, large enough to absorb a normal startup banner without
# rotating immediately. Operators can override per service via the
# loader's ``log_max_bytes`` field.
DEFAULT_LOG_MAX_BYTES: int = 1024 * 1024


@dataclass
class ProductServiceSpec:
    """Declarative spec for one long-lived product service (Step 3 + 6).

    ``command`` is a **list of arguments** (not a shell string) —
    no shell interpolation, no quoting traps. ``None`` means "the
    operator did not configure a runtime command for this service";
    in that case the service is reported as ``status="missing"``
    and orchestration fails closed for it instead of guessing.

    ``working_dir`` is the cwd of the spawned subprocess; ``None``
    means inherit from the orchestrator's cwd.

    ``env_overrides`` is a small dict of additional environment
    variables for the subprocess; the spawn helper merges them on
    top of the parent's environment. All keys/values must be
    strings (validated by the loader).

    Phase 6 / Step 6 fields (all optional, all backward-compatible —
    Step 3 configs continue to load unchanged):

    - ``restart_policy`` — one of :data:`RESTART_POLICIES`
      (``"never"`` or ``"restart-if-stale"``). Default
      ``"never"``. ``"restart-if-stale"`` only triggers on a
      boundary call (``start`` / ``reload`` / ``status``); there is
      no background watcher.
    - ``logs_enabled`` — when True, ``stdout`` / ``stderr`` of the
      child are routed to per-service log files under
      ``<work_dir>/.runtime/logs/<service>.{out,err}.log``. When
      False, both streams go to ``DEVNULL`` (legacy behaviour).
      Default True.
    - ``log_max_bytes`` — rotate-if-exceeds-size threshold in bytes.
      Before each new spawn, an existing log larger than this is
      renamed to ``<file>.1`` (overwriting any previous ``.1``).
      One generation only — no gzip, no .2/.3 chain. Defaults to
      :data:`DEFAULT_LOG_MAX_BYTES`. Must be a positive int.
    """

    name: str
    enabled: bool = True
    command: list[str] | None = None
    working_dir: str | None = None
    env_overrides: dict[str, str] = field(default_factory=dict)
    restart_policy: str = "never"
    logs_enabled: bool = True
    log_max_bytes: int = DEFAULT_LOG_MAX_BYTES


@dataclass
class ProductRuntimeSettings:
    """Runtime contract section of the product config (Step 3).

    ``services`` keys are operator-chosen names. The recommended
    convention is ``read`` / ``write`` / ``intelligence`` to mirror
    :class:`ProductServerToggles`, but the runtime layer does not
    enforce that — it manages whatever processes the operator
    declared. If a runtime section is absent in the product config,
    a default empty :class:`ProductRuntimeSettings` is used and
    orchestration boundary helpers degrade honestly.
    """

    services: dict[str, ProductServiceSpec] = field(default_factory=dict)


@dataclass
class ProductConfig:
    """Top-level product config of 1C Agent Platform.

    ``project`` is the existing :class:`onec_config.ProjectConfig` —
    the product layer does not redefine environments, it points at
    them. ``default_environment`` must be a key inside
    ``project.environments`` (validated by the loader).

    ``runtime`` (Step 3) is the optional declarative runtime contract.
    It defaults to an empty :class:`ProductRuntimeSettings` so any
    Step 2 product config keeps loading without changes.
    """

    product_name: str
    profile_name: str
    project: ProjectConfig
    default_environment: str
    servers: ProductServerToggles
    bootstrap: ProductBootstrapSettings
    runtime: ProductRuntimeSettings = field(default_factory=ProductRuntimeSettings)
    # Phase 6 / Step 8 — narrow, optional enterprise-foundation
    # contract. Absent / partial values are perfectly valid; the
    # foundation inspector reports their absence as findings, not
    # as crashes. See :class:`EnterpriseFoundationSettings`.
    enterprise: "EnterpriseFoundationSettings" = field(
        default_factory=lambda: EnterpriseFoundationSettings()
    )


# Allowed deployment tiers for ``EnterpriseFoundationSettings.deployment_tier``.
# Phase 6 / Step 8 ships exactly four — no "preview" / "qa" /
# "uat" / "perf" / "dr-replica" etc. The enum is deliberately small
# so the foundation verdict has stable rules.
DEPLOYMENT_TIERS: tuple[str, ...] = (
    "dev",
    "test",
    "stage",
    "prod-like",
)

# Allowed values for ``EnterpriseFoundationResult.foundation_level``.
# The wording is deliberately humble: the platform reports
# *foundation level*, not *enterprise readiness*. Step 8 is a
# foundation slice, not an enterprise version.
FOUNDATION_LEVELS: tuple[str, ...] = (
    "absent",   # no enterprise section declared at all
    "minimal",  # section declared but most discipline knobs missing
    "partial",  # core identity + operability present, gaps remain
    "strong",   # identity + operability + traceability + binary contract
)


@dataclass
class EnterpriseFoundationSettings:
    """Narrow, optional enterprise-foundation contract (Phase 6 / Step 8).

    This section is **not** a security boundary, **not** a policy
    engine, **not** a vault, and **not** a multi-tenant descriptor.
    It is a small declarative block of operator-supplied identity
    and discipline flags that the foundation inspector
    (:func:`onec_platform.inspect_enterprise_foundation`) reads
    read-only.

    All fields are optional; an absent ``enterprise`` section in the
    product config is fully valid (Step 1–7 configs continue to load
    unchanged) and just yields ``foundation_level="absent"``.

    Fields:

    - ``deployment_tier`` — one of :data:`DEPLOYMENT_TIERS`
      (``"dev"`` / ``"test"`` / ``"stage"`` / ``"prod-like"``).
      ``None`` means the operator has not declared a tier yet.
    - ``instance_id`` — operator-chosen string that uniquely names
      the running instance (e.g. ``"acme-stage-eu-west"``). Not
      validated for shape beyond "non-empty string"; the foundation
      inspector flags missing instance_id especially for
      ``deployment_tier="prod-like"``.
    - ``config_owner`` — operator-readable owner / contact for this
      product config (e.g. ``"infra@acme.local"``). Free-form string;
      the inspector flags absence on prod-like.
    - ``change_control_required`` — explicit operator declaration of
      whether a change-control discipline applies. The platform does
      not enforce a change-control workflow itself; this flag is
      surfaced verbatim so an external CI / approval pipeline can
      read it.
    - ``require_operator_identity`` — explicit operator declaration
      that an operator-identity must be attached to mutating
      operations. The platform does not yet **enforce** this (Step 8
      is foundation, not policy execution); the flag is surfaced so
      future enforcement can read it without changing the contract.
    - ``runbook_reference`` (optional, sixth field) — free-form
      string pointing at the operator's runbook URL / wiki page /
      ticket query. Surfaced as-is.
    """

    deployment_tier: str | None = None
    instance_id: str | None = None
    config_owner: str | None = None
    change_control_required: bool = False
    require_operator_identity: bool = False
    runbook_reference: str | None = None


@dataclass(frozen=True)
class DoctorFinding:
    """One finding from the prereqs doctor.

    ``severity`` is one of ``"ok"`` / ``"warning"`` / ``"error"``.
    ``confidence`` is one of ``"confirmed"`` (we directly observed
    the fact — file exists, executable resolves, module is importable)
    or ``"presumed"`` (heuristic — e.g. URL shape vs. real HTTP probe).
    Confirmed/presumed split mirrors the convention already used by
    Phase 4 intelligence-tools.
    """

    code: str
    severity: str
    confidence: str
    detail: str


@dataclass
class DoctorReport:
    """Outcome of a single prereqs doctor run.

    The report itself is always considered "ran successfully": doctor
    catches its own internal errors and converts them into findings.
    Whether the platform is *ready to run* is captured by
    ``error_count`` — any non-zero value means a blocking finding is
    present.
    """

    findings: list[DoctorFinding] = field(default_factory=list)
    error_count: int = 0
    warning_count: int = 0
    recommended_actions: list[str] = field(default_factory=list)


@dataclass
class BootstrapResult:
    """Outcome of a single bootstrap step (boundary-level helper).

    ``ok`` reflects whether bootstrap completed at all (config loaded
    and doctor ran). It is **not** "everything is healthy" — even an
    ``ok=True`` result may carry blocking findings inside ``doctor``,
    and the caller must inspect ``doctor.error_count`` to decide
    whether the product is actually ready to run.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    doctor: DoctorReport | None
    message: str


# ---------------------------------------------------------------------------
# Phase 5 / Step 3 — runtime orchestration models.
# ---------------------------------------------------------------------------

# Allowed values for ``RuntimeServiceState.status``. Listed here so
# tests, README and runtime helpers all share one source of truth.
RUNTIME_STATUSES: tuple[str, ...] = (
    "configured",  # known and ready to start, never started in this state
    "running",     # state file says running and PID is alive
    "stopped",     # explicitly stopped
    "stale",       # state file said running, but PID is dead
    "error",       # last start attempt failed
    "disabled",    # spec exists but enabled=False
    "missing",     # spec is absent or has no command (fail-closed)
)

# Phase 6 / Step 6 bumped this from 1 → 2 to surface the new
# per-service fields (restart_policy / restart_attempts /
# last_exit_code / stdout_log_path / stderr_log_path /
# last_started_at / last_stopped_at). Reader is backward-compatible:
# ``schema_version=1`` files are still accepted and the missing
# fields default to honest sentinels (``"never"`` for restart_policy,
# ``0`` for restart_attempts, ``None`` for the rest). Writer always
# emits version 2.
RUNTIME_STATE_SCHEMA_VERSION: int = 2
RUNTIME_STATE_READABLE_SCHEMA_VERSIONS: tuple[int, ...] = (1, 2)


@dataclass
class RuntimeServiceState:
    """Per-service runtime snapshot.

    ``configured`` is True iff a :class:`ProductServiceSpec` exists
    AND has a non-empty ``command``. ``enabled`` mirrors the spec's
    flag. ``status`` is one of :data:`RUNTIME_STATUSES`. ``pid`` is
    only meaningful for ``status="running"`` / ``"stale"``.

    ``env_override_keys`` lists the **keys** of env overrides the
    spec declares — values are intentionally not persisted in the
    state file (no risk of leaking secrets through the state file).

    Phase 6 / Step 6 fields:

    - ``restart_policy`` — mirror of the spec's policy
      (:data:`RESTART_POLICIES`); persisted so an operator reading
      the state file sees how the service is configured to react to
      stale PIDs.
    - ``restart_attempts`` — counter incremented every time the
      runtime layer **attempts** a restart-if-stale spawn for this
      service. Counts attempts, not successes; restart_succeeded /
      restart_failed information lands in findings.
    - ``last_exit_code`` — best-effort exit code of the last
      observed transition out of ``"running"``. Populated on
      Windows via ``GetExitCodeProcess`` when a stale PID is
      observed; left ``None`` on POSIX (we did not spawn the
      process as a child of the current orchestrator, so
      ``waitpid`` is not available — honestly degrade rather than
      pretend).
    - ``stdout_log_path`` / ``stderr_log_path`` — absolute paths of
      the log files used by the most recent spawn, or ``None`` if
      logging was disabled / not yet started. Tools and operators
      use these to find logs without re-deriving paths.
    - ``last_started_at`` — alias of the existing ``started_at``,
      kept for symmetry with ``last_stopped_at``. Both are ISO-8601
      UTC strings or ``None``. ``started_at`` is preserved as-is
      for backward compatibility; ``last_started_at`` is updated
      every time a spawn succeeds.
    - ``last_stopped_at`` — ISO-8601 UTC of the most recent
      observed stop / stale transition for this service.
    """

    name: str
    enabled: bool
    configured: bool
    status: str
    command: list[str] | None = None
    working_dir: str | None = None
    env_override_keys: list[str] = field(default_factory=list)
    pid: int | None = None
    started_at: str | None = None
    last_error: str | None = None
    restart_policy: str = "never"
    restart_attempts: int = 0
    last_exit_code: int | None = None
    stdout_log_path: str | None = None
    stderr_log_path: str | None = None
    last_started_at: str | None = None
    last_stopped_at: str | None = None


@dataclass
class RuntimeStateFile:
    """Persisted runtime state ( ``<work_dir>/.runtime/runtime-state.json`` ).

    The file is written atomically (write-then-rename) by
    :mod:`onec_platform.state`. ``schema_version`` is bumped if the
    on-disk format ever changes; readers reject unknown versions
    fail-closed.
    """

    schema_version: int
    product_name: str
    profile_name: str
    default_environment: str
    services: dict[str, RuntimeServiceState] = field(default_factory=dict)


@dataclass
class RuntimeOperationResult:
    """Outcome of ``start`` / ``stop`` / ``reload`` (boundary helper).

    ``ok`` reflects whether the orchestration step ran (config
    accepted, work_dir resolved, state file readable/writable). It is
    **not** "all services are now in the desired state" — individual
    per-service failures are captured as findings, and the caller
    must inspect ``services`` and ``findings`` to decide.

    ``services`` is the post-operation snapshot of every service
    that was visible to this operation (including disabled / missing
    ones, so that the report is complete).
    """

    ok: bool
    operation: str  # "start" / "stop" / "reload"
    product_name: str | None
    profile_name: str | None
    services: list[RuntimeServiceState]
    findings: list[DoctorFinding]
    message: str


@dataclass
class RuntimeStatusResult:
    """Outcome of ``get_product_runtime_status`` (boundary helper).

    Read-only snapshot. Lazily upgrades any state file row whose
    persisted ``status="running"`` no longer matches a live PID:
    such rows are reported as ``"stale"`` in this result, but the
    on-disk state file is **not** silently rewritten by status —
    only ``start`` / ``stop`` / ``reload`` mutate the on-disk file.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    services: list[RuntimeServiceState]
    findings: list[DoctorFinding]
    state_path: str | None
    message: str


# ---------------------------------------------------------------------------
# Phase 5 / Step 4 — environment doctor / health dashboard models.
# ---------------------------------------------------------------------------

# Allowed values for ``DashboardVerdict.overall_status`` — single source
# of truth for tests, README and the rule engine in
# :mod:`onec_platform.dashboard`.
DASHBOARD_OVERALL_STATUSES: tuple[str, ...] = (
    "healthy",   # all sections clean
    "degraded",  # warnings exist, but no blocking findings
    "blocked",   # at least one blocking finding
)


@dataclass
class DashboardSectionResult:
    """One section of the environment dashboard.

    Each section is the output of one underlying signal source —
    ``bootstrap`` / ``runtime`` / ``read_health`` /
    ``read_diagnosis`` / ``intelligence_runtime`` /
    ``intelligence_risk``. The aggregator never raises: a sub-tool
    that fails turns into ``ok=False`` for its section, with the
    reason captured in :attr:`message` and (when applicable) one
    error-level finding inside :attr:`confirmed_findings`.

    ``confirmed_findings`` and ``presumed_findings`` carry the
    confidence split per Phase 4 convention. ``payload`` keeps the
    raw response of the source (a :class:`mcp_common.ToolResult`
    payload, a :class:`BootstrapResult` projected into a dict, or a
    :class:`RuntimeStatusResult` projected into a dict) so the caller
    can drill in without re-running the sub-tool.
    """

    name: str
    ok: bool
    source: str
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    payload: dict = field(default_factory=dict)
    message: str = ""


@dataclass
class DashboardVerdict:
    """Top-level rule-based product verdict.

    Computed deterministically by :func:`onec_platform.dashboard._compute_verdict`
    from the per-section results. The ruleset is intentionally small
    and read-only; the README of the product layer documents every
    rule in plain language so an operator can cross-check the verdict
    by hand.
    """

    overall_status: str
    ready_for_workflows: bool
    blocking_issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)


@dataclass
class EnvironmentDashboardResult:
    """Full product-level health snapshot.

    ``ok=True`` means the dashboard ran end-to-end (config accepted,
    sections built — even if some sub-tools failed honestly inside
    their own section). ``ok=False`` is reserved for the case where
    even the product config could not be loaded — there is nothing
    to aggregate on top of.

    ``confirmed_findings`` / ``presumed_findings`` /
    ``recommended_actions`` / ``sources_used`` are aggregated across
    all sections, with each finding tagged by its originating
    section so that provenance is preserved.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    work_dir: str | None
    state_path: str | None
    sections: dict[str, DashboardSectionResult]
    verdict: DashboardVerdict | None
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    sources_used: list[str] = field(default_factory=list)
    message: str = ""


# ---------------------------------------------------------------------------
# Phase 5 / Step 5 — guided workflow layer models.
# ---------------------------------------------------------------------------

# Workflow names supported on Step 5. Single source of truth — the
# runner refuses anything not listed here, fail-closed.
WORKFLOW_NAMES: tuple[str, ...] = (
    "safe-add-attribute",
    "safe-add-module-method",
    "safe-add-form-attribute",
    "stand-health-check",
)

# Modes a workflow run can report. ``preview``: plan built, nothing
# executed. ``executed``: a mutating workflow attempted execution
# (success or failure visible via ``ok``). ``diagnostic``: read-only
# stand-health-check. ``blocked``: dashboard precondition failed for
# a mutating workflow. ``rejected``: product config could not even
# be loaded.
WORKFLOW_MODES: tuple[str, ...] = (
    "preview",
    "executed",
    "diagnostic",
    "blocked",
    "rejected",
)


@dataclass
class WorkflowStepResult:
    """One step of a guided workflow run.

    Each step is the outcome of one underlying call — a precondition
    check, an intelligence sub-tool, a write-tool, a verify-tool, or
    a post-write audit/rollback hint lookup. Steps are append-only:
    even when the workflow is honestly aborted (e.g. blocked by
    dashboard or by a write-tool failure), already-completed steps
    are preserved in :class:`WorkflowRunResult.steps` so the operator
    sees how far the workflow got.

    ``kind`` is one of:

    - ``"precondition"`` — dashboard / runtime / pre-flight gating;
    - ``"intelligence"`` — read-only intelligence sub-tool;
    - ``"preview"`` — plan-only marker, no real call beyond it;
    - ``"mutating"`` — actual write-side execution;
    - ``"verify"`` — post-write verification;
    - ``"diagnostic"`` — stand-health-check read-only step;
    - ``"audit"`` — last-write-operation / rollback-hint lookup.

    ``source`` is a provenance marker (e.g.
    ``"intelligence.suggest_metadata_patch_plan"``,
    ``"write.add_catalog_attribute"``).
    """

    name: str
    kind: str
    ok: bool
    source: str
    payload: dict = field(default_factory=dict)
    message: str = ""


@dataclass
class WorkflowPlan:
    """Operator-visible plan assembled from intelligence sub-tools.

    ``summary`` is a small list of human-readable bullets that
    describe what the workflow intends to do; the runner prints
    these so the operator can read them before passing
    ``confirm_execute=True``. ``suggested_tools`` and
    ``suggested_write_tools`` are bound to **real registered**
    public tool names — the runner programmatically refuses to add
    unknown names (see :func:`onec_platform.workflow._allow_only_real_tools`).
    """

    workflow_name: str
    target_kind: str | None = None
    target_name: str | None = None
    summary: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    impact_level: str | None = None
    risk_level: str | None = None


@dataclass
class WorkflowRunResult:
    """Outcome of a single guided workflow run (boundary-level helper).

    ``ok`` is the overall workflow verdict: did the run honestly
    complete its intended mode? See :data:`WORKFLOW_MODES` for
    individual semantics. ``execution_performed`` reflects whether
    the runner actually invoked any mutating write-tool — independent
    of ``ok`` (e.g. ``execution_performed=True, ok=False`` when the
    write-tool ran and rejected the input).

    Mutating-workflow extras (``write_results`` / ``verify_results``
    / ``last_write_operation`` / ``rollback_hint``) are populated
    only when ``mode == "executed"``; for preview / diagnostic /
    blocked / rejected they are empty / ``None``.
    """

    ok: bool
    workflow_name: str
    mode: str
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    ready_for_workflows: bool
    execution_performed: bool
    plan: WorkflowPlan | None
    steps: list[WorkflowStepResult] = field(default_factory=list)
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    write_results: list[dict] = field(default_factory=list)
    verify_results: list[dict] = field(default_factory=list)
    last_write_operation: dict | None = None
    rollback_hint: dict | None = None
    message: str = ""


# ---------------------------------------------------------------------------
# Phase 5 / Step 6 — rollback / recovery / audit UX models.
# ---------------------------------------------------------------------------

# Modes a rollback assistant run can report. ``preview``: plan built,
# nothing executed (default for confirm_execute=False). ``executed``:
# a supported automatic recovery path was attempted (success/failure
# visible via ``ok``). ``blocked``: confirm_execute=True but dashboard
# is not safe for execution. ``unsupported``: confirm_execute=True but
# this audit operation has no supported automatic recovery path —
# operator must use the snapshot hint manually. ``rejected``: invalid
# input / config rejected / operation_id not found.
RECOVERY_MODES: tuple[str, ...] = (
    "preview",
    "executed",
    "blocked",
    "unsupported",
    "rejected",
)


@dataclass
class OperationHistoryEntry:
    """One normalised audit entry visible to the operator.

    ``position`` is a 0-based line index in
    ``<dump_path>/.audit/audit.jsonl``. The audit JSONL has no
    timestamps, so position is the only stable monotonic ordering
    we can offer — it is sufficient for "list latest N" /
    "show me operation X" semantics.
    """

    position: int
    operation_id: str
    tool_name: str
    environment: str
    base_id: str
    status: str
    message: str
    raw_line: str = ""


@dataclass
class OperationHistorySummary:
    """Counts derived from a list of :class:`OperationHistoryEntry`."""

    total: int = 0
    ok_count: int = 0
    error_count: int = 0
    other_count: int = 0


@dataclass
class OperationHistoryResult:
    """Outcome of :func:`onec_platform.recovery.get_operation_history`.

    ``ok=True`` covers both "audit loaded with N entries" and "no
    audit file present yet" (a clean environment that has not yet
    seen any write is honest history-empty, not an error). ``ok=False``
    is reserved for invalid inputs or unreadable audit content.

    ``audit_path`` is always the resolved absolute path of where
    the audit JSONL would live, even when the file is absent.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    audit_path: str | None
    entries: list[OperationHistoryEntry]
    summary: OperationHistorySummary
    findings: list[DoctorFinding] = field(default_factory=list)
    message: str = ""


@dataclass
class OperationInspectResult:
    """Outcome of :func:`onec_platform.recovery.inspect_operation`.

    ``operation_found`` is the boolean source of truth — ``ok``
    only reflects whether the inspect step itself ran. A missing
    operation produces ``ok=False, operation_found=False`` so the
    caller can branch cleanly.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    operation_id: str
    operation_found: bool
    history_entry: OperationHistoryEntry | None
    rollback_hint: dict | None
    automatic_recovery_supported: bool
    operator_summary: list[str] = field(default_factory=list)
    findings: list[DoctorFinding] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class RollbackPlan:
    """Operator-visible plan assembled by the rollback assistant.

    The plan is always built (even on ``blocked`` / ``unsupported``
    modes); the assistant just refuses to execute it. Surface here
    explicitly carries the ``automatic_recovery_supported`` flag —
    Step 6 ships advisory-only, so this flag is False for every
    currently-known write-tool family.
    """

    operation_id: str
    tool_name: str | None
    automatic_recovery_supported: bool
    summary: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    suggested_backup_root: str | None = None
    suggested_dump_root: str | None = None


@dataclass
class RollbackAssistantResult:
    """Outcome of :func:`onec_platform.recovery.run_rollback_assistant`.

    ``mode`` ∈ :data:`RECOVERY_MODES`. ``execution_performed`` is
    ``True`` only when the assistant actually invoked a mutating
    write-tool / workflow runner (currently never on Step 6 — every
    confirm_execute=True path with a known tool resolves to
    ``unsupported`` because no automatic content-level rollback is
    safe to ship without public ``delete_*`` write-tools).
    """

    ok: bool
    mode: str
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    operation_id: str
    operation_found: bool
    execution_performed: bool
    plan: RollbackPlan | None
    history_entry: OperationHistoryEntry | None
    history_summary: OperationHistorySummary | None
    rollback_hint: dict | None
    dashboard_summary: dict | None
    steps: list[WorkflowStepResult] = field(default_factory=list)
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    write_results: list[dict] = field(default_factory=list)
    verify_results: list[dict] = field(default_factory=list)
    last_write_operation: dict | None = None
    message: str = ""


# ---------------------------------------------------------------------------
# Phase 5 / Step 7 — real-stand / 1cv8 binary integration models.
# ---------------------------------------------------------------------------

# Modes a real-stand smoke test run can report. ``preview``: plan
# built, no probe attempted. ``executed``: at least one honest probe
# step ran (filesystem stat, optionally a controlled subprocess).
# ``blocked``: confirm_execute=True but readiness gate failed.
# ``rejected``: invalid input / config rejected.
REAL_STAND_SMOKE_MODES: tuple[str, ...] = (
    "preview",
    "executed",
    "blocked",
    "rejected",
)


@dataclass
class RealStandReadinessResult:
    """Outcome of :func:`onec_platform.realstand.get_real_stand_readiness`.

    Read-only. ``ready_for_real_stand_smoke`` is the single-bit
    operator-facing verdict: True iff every blocking finding is
    absent. ``binary_present`` and ``binary_executable_like`` are
    fact-level confirmed signals (file existence, file-vs-dir).

    ``ok`` reflects whether the readiness step itself ran (it almost
    always does, even when readiness is False). ``ok=False`` is
    reserved for invalid inputs and unloadable configs.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    onec_binary_path: str | None
    binary_present: bool
    binary_executable_like: bool
    has_probe_args: bool
    ready_for_real_stand_smoke: bool
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class RealStandSmokeResult:
    """Outcome of :func:`onec_platform.realstand.run_real_stand_smoke_test`.

    ``mode`` ∈ :data:`REAL_STAND_SMOKE_MODES`.
    ``binary_invoked`` is True iff the smoke test actually started a
    subprocess (``onec_process_runner.run_process``). It can be False
    even in ``mode="executed"`` when the operator did not configure
    ``onec_binary_probe_args`` — the smoke test then ships only the
    metadata-level filesystem probe, which is still honestly
    "executed" (it observed real filesystem state).

    ``binary_exit_code`` / ``binary_stdout_excerpt`` /
    ``binary_stderr_excerpt`` are populated only when
    ``binary_invoked`` is True; excerpts are short, truncated
    strings — the assistant never streams arbitrary subprocess
    output back as a payload.
    """

    ok: bool
    mode: str
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    onec_binary_path: str | None
    ready_for_real_stand_smoke: bool
    execution_performed: bool
    binary_invoked: bool
    binary_exit_code: int | None
    binary_stdout_excerpt: str | None
    binary_stderr_excerpt: str | None
    plan_summary: list[str]
    steps: list[WorkflowStepResult] = field(default_factory=list)
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    message: str = ""


# ---------------------------------------------------------------------------
# Phase 6 / Step 3 — installer / setup fast path models.
# ---------------------------------------------------------------------------

# Modes the install fast path boundary can report. ``preview``: nothing
# was written to disk; the helper just showed what *would* happen.
# ``executed``: the helper actually wrote ``output_config_path`` and
# re-loaded it through the existing bootstrap entry point. ``rejected``:
# input is invalid (config rejected, target file already present without
# explicit override, etc.). The fast path is **not** an industrial
# installer — it is a small product-layer helper that reduces the setup
# ritual to "fill in a template + bootstrap".
INSTALL_MODES: tuple[str, ...] = (
    "preview",
    "executed",
    "rejected",
)


@dataclass
class ProductConfigTemplateResult:
    """Outcome of :func:`onec_platform.templates.build_product_config_template`.

    The template is returned as a JSON-serialisable ``dict``; the helper
    does **not** write to disk by itself. ``ok=True`` covers the case
    where the template was assembled honestly, even if the operator
    later decides not to write it.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    template: dict
    findings: list[DoctorFinding] = field(default_factory=list)
    message: str = ""


@dataclass
class ReleaseLayoutReport:
    """Outcome of :func:`onec_platform.installer.inspect_release_layout`.

    Honest, minimal layout check. ``ok=True`` means the inspection step
    *ran* (root path is a directory we could read); individual missing
    expected entries are surfaced as findings, not as ``ok=False``.
    ``ok=False`` is reserved for the case where the inspection itself
    cannot run — root path absent or not a directory.
    """

    ok: bool
    root_path: str
    is_directory: bool
    expected_entries: list[str]
    present_entries: list[str]
    missing_entries: list[str]
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class InstallFastPathResult:
    """Outcome of :func:`onec_platform.installer.run_install_fast_path`.

    ``mode`` ∈ :data:`INSTALL_MODES`. ``mode="preview"`` is the default
    (``confirm_write=False``) — nothing is written to disk. ``mode="executed"``
    is reached only with ``confirm_write=True`` and a free target path:
    the helper wrote ``output_config_path`` and re-loaded it through the
    existing :func:`onec_platform.bootstrap_product_from_json_file` entry
    point to confirm it is readable as a real product config.

    The fast path is deliberately small: it does **not** start runtime,
    does **not** mutate an infobase, does **not** invoke MCP write-tools.
    Its job is to cut the manual install ritual to: "fill in a template,
    pass it once with ``confirm_write=True``, then run the existing
    runtime/workflow surface as a separate step".
    """

    ok: bool
    mode: str
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    output_config_path: str | None
    config_written: bool
    layout_report: ReleaseLayoutReport | None
    bootstrap_pre: BootstrapResult | None
    bootstrap_post: BootstrapResult | None
    template_preview: dict | None
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    message: str = ""


# ---------------------------------------------------------------------------
# Phase 6 / Step 8 — enterprise foundation inspection result.
# ---------------------------------------------------------------------------


@dataclass
class EnterpriseFoundationResult:
    """Outcome of :func:`onec_platform.inspect_enterprise_foundation`.

    Read-only inspection: the boundary never spawns, never writes
    audit, never calls ``run_write_flow``. ``ok=True`` means the
    inspection itself ran (config loadable, environment resolvable);
    it does **not** mean the platform is enterprise-ready.

    The honest verdict is split between two fields so the operator
    cannot conflate them:

    - ``foundation_level`` ∈ :data:`FOUNDATION_LEVELS` —
      ``"absent"`` / ``"minimal"`` / ``"partial"`` / ``"strong"``.
      A small, deterministic rule set (see
      :mod:`onec_platform.enterprise`) maps observed signals to a
      level. ``"strong"`` does **not** mean "production-ready" —
      it means every Phase 6 foundation knob is set in a way that
      future enterprise track work can build on.
    - ``ready_for_enterprise_track`` — bool, true iff
      ``foundation_level == "strong"`` AND no blocking finding
      fired. Phase 6 / Step 8 deliberately does **not** export an
      ``enterprise_ready`` flag — only ``ready_for_enterprise_track``
      (next-step readiness, not deployment readiness).

    Field shape mirrors the existing dashboard / installer / recovery
    result shapes so operator UIs can render it uniformly:
    ``confirmed_findings`` for confirmed-confidence facts,
    ``presumed_findings`` for heuristic / observational hints,
    ``recommended_actions`` for short operator-readable next steps,
    ``suggested_tools`` / ``suggested_write_tools`` filtered through
    :func:`onec_platform.workflow._allow_only_real_tools` so only
    real registered names appear.
    """

    ok: bool
    product_name: str | None
    profile_name: str | None
    default_environment: str | None
    foundation_level: str
    ready_for_enterprise_track: bool
    enterprise_section_present: bool
    deployment_tier: str | None
    instance_id: str | None
    config_owner: str | None
    change_control_required: bool
    require_operator_identity: bool
    runbook_reference: str | None
    confirmed_findings: list[DoctorFinding] = field(default_factory=list)
    presumed_findings: list[DoctorFinding] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    suggested_tools: list[str] = field(default_factory=list)
    suggested_write_tools: list[str] = field(default_factory=list)
    message: str = ""
