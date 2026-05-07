"""Enterprise foundation inspector (Phase 6 / Step 8).

Single read-only product-layer boundary that gives the operator an
honest verdict on whether the **foundation** for a future enterprise
track is in place. This is **not** an enterprise readiness verdict
and **not** a policy/RBAC engine.

What this module is, very precisely:

- a thin **read-only** doctor over the existing product config plus
  filesystem checks for the standalone manuals/runbooks shipped in
  Step 7;
- a deterministic, hand-written rule-set that maps observed signals
  to one of four foundation levels: ``"absent"``, ``"minimal"``,
  ``"partial"``, ``"strong"``;
- a deliberately humble surface: the boolean
  ``ready_for_enterprise_track`` is true only when every section
  scores cleanly **and** ``foundation_level == "strong"``.

What this module is NOT:

- it does **not** introduce new MCP tools or change any registry;
- it does **not** mutate the audit log, the dump, or the infobase;
- it does **not** import :mod:`onec_policy_engine` and never makes
  policy decisions of its own;
- it does **not** probe a 1cv8 binary — that lives in
  :mod:`onec_platform.realstand`. This module checks for the
  *contract* (paths declared, template placeholders shaped); it
  does **not** spawn anything.

Failure model:

- :func:`inspect_enterprise_foundation` and
  :func:`inspect_enterprise_foundation_from_json_file` **never raise**.
- ``ok=True`` covers every honest run (config loadable, environment
  resolvable). ``ok=False`` is reserved for invalid inputs and
  unloadable configs.
- ``foundation_level`` and ``ready_for_enterprise_track`` are the
  honest verdict; do not collapse them into a single boolean.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import mcp_intelligence_server as _mis
import mcp_read_server as _mrs
import mcp_write_server as _mws

from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    DEPLOYMENT_TIERS,
    DoctorFinding,
    EnterpriseFoundationResult,
    FOUNDATION_LEVELS,
    ProductConfig,
)
from .workflow import _allow_only_real_tools


# Repository docs the inspector expects to find. Phase 6 / Step 7
# materialised these. The platform is happy if they are absent
# (operators may legitimately strip docs from a deployment), but it
# scores the foundation as weaker.
_EXPECTED_DOCS: tuple[str, ...] = (
    "docs/operator-manual.md",
    "docs/administrator-manual.md",
    "docs/developer-manual.md",
    "docs/runbooks.md",
)


# Production-marker substrings. Mirrors the discipline already used
# by ``onec_policy_engine`` (without importing it from here): a
# config that calls itself ``prod`` / ``production`` in any visible
# field is held to the prod-like checklist regardless of
# ``deployment_tier`` declaration.
_PRODUCTION_MARKERS: tuple[str, ...] = ("prod", "production")


# ---------------------------------------------------------------------------
# Finding factories.
# ---------------------------------------------------------------------------


def _ok(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="ok", confidence=confidence, detail=detail)


def _warn(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="warning", confidence=confidence, detail=detail)


def _err(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="error", confidence=confidence, detail=detail)


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------


def _resolve_config(
    data: dict | ProductConfig,
) -> tuple[ProductConfig | None, str | None]:
    if isinstance(data, ProductConfig):
        return data, None
    if isinstance(data, dict):
        try:
            return load_product_config(data), None
        except (ValueError, TypeError) as exc:
            return None, f"Product config rejected: {exc}"
    return None, (
        "Product config must be a dict or a pre-loaded ProductConfig "
        f"(got {type(data).__name__})."
    )


def _is_prod_like(config: ProductConfig) -> bool:
    """Return True iff this config looks production-bound.

    Prod-like means **either** ``enterprise.deployment_tier ==
    'prod-like'`` **or** any visible identity field
    (`profile_name`, default-environment fields) contains a
    production marker. This intentionally over-detects: we would
    rather hold a dev-misnamed-as-prod config to the prod checklist
    than under-warn on a real prod config.
    """
    enterprise = config.enterprise
    if enterprise.deployment_tier == "prod-like":
        return True
    fields_to_scan: list[str | None] = [
        config.profile_name,
        config.default_environment,
    ]
    env = config.project.environments.get(config.default_environment)
    if env is not None:
        fields_to_scan.extend(
            [env.name, env.base_id, env.publication_name, env.http_base_url]
        )
    for value in fields_to_scan:
        if not value:
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in _PRODUCTION_MARKERS):
            return True
    return False


def _repo_root_from_config(config: ProductConfig) -> Path | None:
    """Best-effort path to the repository root for docs lookup.

    The runtime work_dir is operator-chosen and typically *not* the
    repository root, so we walk up from the running module's path
    until a parent contains an ``apps`` directory + a top-level
    ``docs`` directory. Returns ``None`` if no such ancestor is
    found within a reasonable depth — the inspector then degrades
    honestly and emits one warning instead of guessing.
    """
    here = Path(__file__).resolve()
    for ancestor in here.parents:
        if (ancestor / "apps").is_dir() and (ancestor / "docs").is_dir():
            return ancestor
    return None


# ---------------------------------------------------------------------------
# Section A — identity / config discipline.
# ---------------------------------------------------------------------------


def _check_identity(
    config: ProductConfig,
    *,
    prod_like: bool,
) -> tuple[list[DoctorFinding], list[DoctorFinding], list[str], int]:
    """Return (confirmed, presumed, actions, score) for section A."""
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    score = 0  # 0..3 — higher is stronger
    e = config.enterprise

    if e.deployment_tier is None:
        confirmed.append(
            _warn(
                "foundation_deployment_tier_missing",
                "enterprise.deployment_tier is not declared. The "
                f"foundation inspector cannot honestly score the "
                "config without a tier; declare one of "
                f"{sorted(DEPLOYMENT_TIERS)}.",
            )
        )
        actions.append(
            "Set enterprise.deployment_tier in the product config to "
            f"one of {sorted(DEPLOYMENT_TIERS)}."
        )
    else:
        confirmed.append(
            _ok(
                "foundation_deployment_tier_declared",
                f"enterprise.deployment_tier = {e.deployment_tier!r}.",
            )
        )
        score += 1

    if e.instance_id is None:
        if prod_like:
            confirmed.append(
                _err(
                    "foundation_instance_id_missing_on_prod",
                    "enterprise.instance_id is required for prod-like "
                    "configs but is not set.",
                )
            )
            actions.append(
                "Set enterprise.instance_id (e.g. 'acme-stage-eu-west') "
                "for any prod-like config."
            )
        else:
            confirmed.append(
                _warn(
                    "foundation_instance_id_missing",
                    "enterprise.instance_id is not declared. Useful for "
                    "future audit / rollout correlation; not strictly "
                    "blocking for non-prod tiers.",
                )
            )
    else:
        confirmed.append(
            _ok(
                "foundation_instance_id_declared",
                f"enterprise.instance_id = {e.instance_id!r}.",
            )
        )
        score += 1

    if e.config_owner is None:
        if prod_like:
            confirmed.append(
                _err(
                    "foundation_config_owner_missing_on_prod",
                    "enterprise.config_owner is required for prod-like "
                    "configs but is not set.",
                )
            )
            actions.append(
                "Set enterprise.config_owner to an operator-readable "
                "owner / contact (e.g. 'infra@acme.local')."
            )
        else:
            confirmed.append(
                _warn(
                    "foundation_config_owner_missing",
                    "enterprise.config_owner is not declared.",
                )
            )
    else:
        confirmed.append(
            _ok(
                "foundation_config_owner_declared",
                f"enterprise.config_owner = {e.config_owner!r}.",
            )
        )
        score += 1

    confirmed.append(
        _ok(
            "foundation_change_control_declared",
            f"enterprise.change_control_required = "
            f"{e.change_control_required}. (Surfaced verbatim — the "
            "platform does not enforce a change-control workflow itself.)",
        )
    )
    confirmed.append(
        _ok(
            "foundation_operator_identity_declared",
            f"enterprise.require_operator_identity = "
            f"{e.require_operator_identity}. (Foundation flag only — "
            "no enforcement on this step.)",
        )
    )
    if e.runbook_reference is not None:
        presumed.append(
            _ok(
                "foundation_runbook_reference_present",
                f"enterprise.runbook_reference = {e.runbook_reference!r}.",
                confidence="presumed",
            )
        )

    return confirmed, presumed, actions, score


# ---------------------------------------------------------------------------
# Section B — operability foundation.
# ---------------------------------------------------------------------------


def _check_operability(
    config: ProductConfig,
) -> tuple[list[DoctorFinding], list[DoctorFinding], list[str], int]:
    """Return (confirmed, presumed, actions, score) for section B."""
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    score = 0  # 0..3

    work_dir = config.bootstrap.work_dir
    if not work_dir:
        confirmed.append(
            _err(
                "foundation_work_dir_missing",
                "bootstrap.work_dir is not configured; runtime "
                "orchestration / dashboards / logs cannot work.",
            )
        )
        actions.append(
            "Set bootstrap.work_dir to an existing operator-owned "
            "directory."
        )
    else:
        confirmed.append(
            _ok(
                "foundation_work_dir_declared",
                f"bootstrap.work_dir = {work_dir!r}.",
            )
        )
        score += 1

    services = config.runtime.services
    if not services:
        confirmed.append(
            _warn(
                "foundation_runtime_services_empty",
                "runtime.services is empty. The platform manages "
                "whatever long-lived processes the operator declares; "
                "an empty contract makes start/stop/dashboard verdicts "
                "degraded.",
            )
        )
        actions.append(
            "Declare at least one runtime.services entry "
            "(read / write / intelligence)."
        )
    else:
        confirmed.append(
            _ok(
                "foundation_runtime_services_declared",
                f"runtime.services has {len(services)} entry/entries.",
            )
        )
        score += 1

    enabled_services = [s for s in services.values() if s.enabled]
    bad_log_services: list[str] = []
    bad_policy_services: list[str] = []
    for svc in enabled_services:
        if not svc.logs_enabled:
            bad_log_services.append(svc.name)
        if svc.restart_policy not in (
            "never",
            "restart-if-stale",
        ):
            # Loader already whitelisted; defensive only.
            bad_policy_services.append(svc.name)
    if enabled_services and not bad_log_services:
        confirmed.append(
            _ok(
                "foundation_logs_enabled_for_all_enabled_services",
                f"All {len(enabled_services)} enabled service(s) have "
                "logs_enabled=True.",
            )
        )
        score += 1
    elif bad_log_services:
        confirmed.append(
            _warn(
                "foundation_logs_disabled_on_enabled_services",
                "Enabled services with logs_enabled=False: "
                f"{sorted(bad_log_services)}. The foundation expects "
                "every enabled service to capture stdout/stderr.",
            )
        )
        actions.append(
            "Set logs_enabled=True (or omit the field — default is True) "
            f"for: {sorted(bad_log_services)}."
        )

    if bad_policy_services:
        confirmed.append(
            _err(
                "foundation_restart_policy_not_in_whitelist",
                f"Services with non-whitelist restart_policy: "
                f"{sorted(bad_policy_services)}.",
            )
        )

    return confirmed, presumed, actions, score


# ---------------------------------------------------------------------------
# Section C — traceability / recovery foundation.
# ---------------------------------------------------------------------------


_RECOVERY_PLATFORM_FUNCTIONS = (
    "get_operation_history",
    "inspect_operation",
    "run_rollback_assistant",
)


def _check_traceability() -> tuple[
    list[DoctorFinding], list[DoctorFinding], list[str], int
]:
    """Return (confirmed, presumed, actions, score) for section C."""
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    score = 0  # 0..2

    repo_root = _repo_root_from_config_unbound()
    if repo_root is None:
        presumed.append(
            _warn(
                "foundation_repo_root_unresolved",
                "Could not resolve the repository root from the "
                "running module path; the inspector skipped the "
                "manuals / runbooks check. This is honest "
                "degrade — not a blocker.",
                confidence="presumed",
            )
        )
    else:
        missing_docs: list[str] = []
        present_docs: list[str] = []
        for rel in _EXPECTED_DOCS:
            target = repo_root / rel
            if target.is_file():
                present_docs.append(rel)
            else:
                missing_docs.append(rel)
        if missing_docs:
            confirmed.append(
                _warn(
                    "foundation_manuals_missing",
                    "Standalone manuals/runbooks missing: "
                    f"{missing_docs}. Step 7 shipped the four "
                    "documents; an operator distribution that strips "
                    "them weakens the traceability foundation.",
                )
            )
            actions.append(
                "Restore the missing files under docs/: "
                f"{missing_docs}."
            )
        else:
            confirmed.append(
                _ok(
                    "foundation_manuals_present",
                    "All four standalone manuals/runbooks are present "
                    "in docs/.",
                )
            )
            score += 1
        if present_docs:
            presumed.append(
                _ok(
                    "foundation_manuals_inventory",
                    f"Found docs ({len(present_docs)}): {present_docs}.",
                    confidence="presumed",
                )
            )

    # Recovery surface — we verify the boundary names are actually
    # exposed by the ``onec_platform`` package (real callables on the
    # public surface), without invoking them. This matches the
    # operator's mental model: "the recovery boundaries are
    # available" === "the operator can import and call them".
    import onec_platform as _op_pkg
    missing_recovery = [
        name for name in _RECOVERY_PLATFORM_FUNCTIONS
        if not callable(getattr(_op_pkg, name, None))
    ]
    if missing_recovery:
        confirmed.append(
            _err(
                "foundation_recovery_surface_incomplete",
                f"Recovery boundary names missing from onec_platform "
                f"public surface: {missing_recovery}.",
            )
        )
    else:
        confirmed.append(
            _ok(
                "foundation_recovery_surface_present",
                "Recovery boundaries declared: "
                f"{list(_RECOVERY_PLATFORM_FUNCTIONS)}.",
            )
        )
        score += 1

    presumed.append(
        _ok(
            "foundation_automatic_rollback_narrow",
            "Automatic rollback whitelist is intentionally narrow "
            "(Phase 6 / Step 4 ships only add_catalog_attribute and "
            "add_document_attribute). This is an honest constraint, "
            "not a foundation gap.",
            confidence="presumed",
        )
    )

    return confirmed, presumed, actions, score


def _repo_root_from_config_unbound() -> Path | None:
    """Module-level shim — same logic as :func:`_repo_root_from_config`
    but does not require a config (we use it from section C, which
    inspects the repository, not the per-config state).
    """
    here = Path(__file__).resolve()
    for ancestor in here.parents:
        if (ancestor / "apps").is_dir() and (ancestor / "docs").is_dir():
            return ancestor
    return None


# ---------------------------------------------------------------------------
# Section D — real-stand / binary foundation.
# ---------------------------------------------------------------------------


def _check_real_stand_contract(
    config: ProductConfig,
    *,
    prod_like: bool,
) -> tuple[list[DoctorFinding], list[DoctorFinding], list[str], int]:
    """Return (confirmed, presumed, actions, score) for section D.

    Pure contract inspection — we look at *declared* fields. We do
    **not** invoke any binary here (that is real-stand smoke's job).

    After Track A / Steps 2–4 the real write-path contract is no
    longer dumpcfg-only. The three binary-backed write tools
    (``create_dump_snapshot`` / ``apply_config_from_files`` /
    ``update_database_configuration``) all share the same honest
    dual-mode shape, so this section honestly accounts for the full
    contract: ``onec_binary_path`` plus three command templates,
    score 0..4.
    """
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    score = 0  # 0..4

    env = config.project.environments.get(config.default_environment)
    if env is None:
        confirmed.append(
            _err(
                "foundation_default_environment_missing",
                f"Default environment {config.default_environment!r} "
                "is not present in project.environments.",
            )
        )
        return confirmed, presumed, actions, score

    has_binary = bool(env.onec_binary_path)
    has_dumpcfg = bool(env.onec_dumpcfg_command_template)
    has_applycfg = bool(env.onec_applycfg_command_template)
    has_updatedb = bool(env.onec_updatedb_command_template)
    if has_binary:
        confirmed.append(
            _ok(
                "foundation_onec_binary_path_declared",
                f"environment.onec_binary_path = {env.onec_binary_path!r}.",
            )
        )
        score += 1
    elif prod_like:
        confirmed.append(
            _err(
                "foundation_onec_binary_path_missing_on_prod",
                "environment.onec_binary_path is not declared. "
                "Required for prod-like configs to enable smoke / "
                "binary-backed dump.",
            )
        )
        actions.append(
            "Set environment.onec_binary_path to the absolute path of "
            "the 1cv8 executable for this environment."
        )
    else:
        confirmed.append(
            _warn(
                "foundation_onec_binary_path_missing",
                "environment.onec_binary_path is not declared.",
            )
        )

    if has_dumpcfg:
        confirmed.append(
            _ok(
                "foundation_onec_dumpcfg_template_declared",
                "environment.onec_dumpcfg_command_template is declared "
                f"({len(env.onec_dumpcfg_command_template)} arg(s)).",
            )
        )
        score += 1
    elif prod_like:
        confirmed.append(
            _err(
                "foundation_onec_dumpcfg_template_missing_on_prod",
                "environment.onec_dumpcfg_command_template is not "
                "declared. Required for prod-like configs to enable "
                "real DumpCfg.",
            )
        )
        actions.append(
            "Set environment.onec_dumpcfg_command_template to the "
            "operator-declared argv template (placeholders: "
            "{binary_path}, {output_path}, {base_path}, {base_id}, "
            "{publication_name}, {http_base_url})."
        )
    else:
        presumed.append(
            _warn(
                "foundation_onec_dumpcfg_template_missing",
                "environment.onec_dumpcfg_command_template is not "
                "declared; create_dump_snapshot will use stub mode.",
                confidence="presumed",
            )
        )

    if has_applycfg:
        confirmed.append(
            _ok(
                "foundation_onec_applycfg_template_declared",
                "environment.onec_applycfg_command_template is declared "
                f"({len(env.onec_applycfg_command_template)} arg(s)).",
            )
        )
        score += 1
    elif prod_like:
        confirmed.append(
            _err(
                "foundation_onec_applycfg_template_missing_on_prod",
                "environment.onec_applycfg_command_template is not "
                "declared. Required for prod-like configs to enable "
                "real LoadCfg / apply_config_from_files.",
            )
        )
        actions.append(
            "Set environment.onec_applycfg_command_template to the "
            "operator-declared argv template (placeholders: "
            "{binary_path}, {input_path}, {base_path}, {base_id}, "
            "{publication_name}, {http_base_url})."
        )
    else:
        presumed.append(
            _warn(
                "foundation_onec_applycfg_template_missing",
                "environment.onec_applycfg_command_template is not "
                "declared; apply_config_from_files will use stub mode.",
                confidence="presumed",
            )
        )

    if has_updatedb:
        confirmed.append(
            _ok(
                "foundation_onec_updatedb_template_declared",
                "environment.onec_updatedb_command_template is declared "
                f"({len(env.onec_updatedb_command_template)} arg(s)).",
            )
        )
        score += 1
    elif prod_like:
        confirmed.append(
            _err(
                "foundation_onec_updatedb_template_missing_on_prod",
                "environment.onec_updatedb_command_template is not "
                "declared. Required for prod-like configs to enable "
                "real UpdateDBCfg / update_database_configuration.",
            )
        )
        actions.append(
            "Set environment.onec_updatedb_command_template to the "
            "operator-declared argv template (placeholders: "
            "{binary_path}, {base_path}, {base_id}, "
            "{publication_name}, {http_base_url})."
        )
    else:
        presumed.append(
            _warn(
                "foundation_onec_updatedb_template_missing",
                "environment.onec_updatedb_command_template is not "
                "declared; update_database_configuration will use stub "
                "mode.",
                confidence="presumed",
            )
        )

    full_real_write = (
        has_binary and has_dumpcfg and has_applycfg and has_updatedb
    )
    if full_real_write:
        presumed.append(
            _ok(
                "foundation_real_write_path_contract_complete",
                "Full real write-path contract is declared "
                "(onec_binary_path + dumpcfg + applycfg + updatedb "
                "templates). All three binary-backed write tools "
                "(create_dump_snapshot, apply_config_from_files, "
                "update_database_configuration) will run in honest "
                "binary-backed mode at runtime; the actual run still "
                "lives behind run_write_flow / write-server tools.",
                confidence="presumed",
            )
        )
    elif has_binary and has_dumpcfg:
        presumed.append(
            _ok(
                "foundation_real_stand_smoke_contract_available",
                "Real-stand smoke contract is available "
                "(onec_binary_path + dumpcfg template set), but the "
                "full write contract (apply / updatedb templates) is "
                "not yet complete. The actual smoke run is "
                "run_real_stand_smoke_test's job, not this inspector's.",
                confidence="presumed",
            )
        )

    return confirmed, presumed, actions, score


# ---------------------------------------------------------------------------
# Verdict.
# ---------------------------------------------------------------------------


_SECTION_MAX_SCORE = {
    "identity": 3,    # tier + instance + owner
    "operability": 3, # work_dir + services + logs_enabled cleanly
    "traceability": 2,  # docs + recovery surface
    "binary": 4,      # binary_path + dumpcfg + applycfg + updatedb templates
}


def _classify_foundation_level(
    enterprise_present: bool,
    section_scores: dict[str, int],
    blocking_errors: int,
) -> str:
    if not enterprise_present:
        return "absent"
    if blocking_errors > 0:
        # Errors mean a section actively fails; the rest of the
        # signal is irrelevant for the high tier.
        return "minimal"
    total = sum(section_scores.values())
    max_total = sum(_SECTION_MAX_SCORE.values())
    if total >= max_total:
        return "strong"
    # "partial" requires at least the identity + operability core
    if (
        section_scores.get("identity", 0) >= 2
        and section_scores.get("operability", 0) >= 2
    ):
        return "partial"
    return "minimal"


# ---------------------------------------------------------------------------
# Public boundary.
# ---------------------------------------------------------------------------


def _rejected(
    message: str,
    *,
    product_name: str | None = None,
    profile_name: str | None = None,
    default_environment: str | None = None,
) -> EnterpriseFoundationResult:
    return EnterpriseFoundationResult(
        ok=False,
        product_name=product_name,
        profile_name=profile_name,
        default_environment=default_environment,
        foundation_level="absent",
        ready_for_enterprise_track=False,
        enterprise_section_present=False,
        deployment_tier=None,
        instance_id=None,
        config_owner=None,
        change_control_required=False,
        require_operator_identity=False,
        runbook_reference=None,
        confirmed_findings=[_err("foundation_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        message=message,
    )


def _enterprise_section_present(config: ProductConfig) -> bool:
    """Detect whether the operator declared *any* enterprise data.

    The dataclass always exists (the loader supplies a default empty
    instance for backward compat); we treat it as "present" iff at
    least one field is non-default.
    """
    e = config.enterprise
    return bool(
        e.deployment_tier
        or e.instance_id
        or e.config_owner
        or e.change_control_required
        or e.require_operator_identity
        or e.runbook_reference
    )


def inspect_enterprise_foundation(
    data: dict | ProductConfig,
) -> EnterpriseFoundationResult:
    """Run the read-only enterprise-foundation doctor (Phase 6 / Step 8).

    Returns an :class:`EnterpriseFoundationResult` that reports
    foundation level + readiness for the next-step enterprise track.
    Never raises. Read-only: does not spawn, does not mutate audit,
    does not call ``run_write_flow``, does not start/stop runtime.

    Section D (real-stand / binary foundation) honestly reflects the
    full real write-path contract introduced by Track A / Steps 2–4:
    the binary path plus three command templates (dumpcfg, applycfg,
    updatedb). Score range is 0..4 and a "strong" foundation requires
    all four declared on prod-like configs.
    """
    config, err = _resolve_config(data)
    if config is None:
        return _rejected(err or "Unknown configuration error.")

    enterprise_present = _enterprise_section_present(config)
    prod_like = _is_prod_like(config)

    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    confirmed.append(
        _ok(
            "foundation_enterprise_section_present"
            if enterprise_present
            else "foundation_enterprise_section_absent",
            (
                "Enterprise section is declared."
                if enterprise_present
                else "Enterprise section is not declared (Step 1–7 "
                "compatible config). The foundation level is reported "
                "as 'absent'."
            ),
        )
    )
    if prod_like:
        presumed.append(
            _ok(
                "foundation_prod_like_detected",
                "Configuration looks prod-like (deployment_tier or "
                "identity fields contain a production marker). "
                "Holding it to the prod-like checklist.",
                confidence="presumed",
            )
        )

    section_scores: dict[str, int] = {}
    blocking_errors = 0

    a_conf, a_pres, a_act, a_score = _check_identity(config, prod_like=prod_like)
    confirmed.extend(a_conf)
    presumed.extend(a_pres)
    actions.extend(a_act)
    section_scores["identity"] = a_score
    blocking_errors += sum(1 for f in a_conf if f.severity == "error")

    b_conf, b_pres, b_act, b_score = _check_operability(config)
    confirmed.extend(b_conf)
    presumed.extend(b_pres)
    actions.extend(b_act)
    section_scores["operability"] = b_score
    blocking_errors += sum(1 for f in b_conf if f.severity == "error")

    c_conf, c_pres, c_act, c_score = _check_traceability()
    confirmed.extend(c_conf)
    presumed.extend(c_pres)
    actions.extend(c_act)
    section_scores["traceability"] = c_score
    blocking_errors += sum(1 for f in c_conf if f.severity == "error")

    d_conf, d_pres, d_act, d_score = _check_real_stand_contract(
        config, prod_like=prod_like
    )
    confirmed.extend(d_conf)
    presumed.extend(d_pres)
    actions.extend(d_act)
    section_scores["binary"] = d_score
    blocking_errors += sum(1 for f in d_conf if f.severity == "error")

    foundation_level = _classify_foundation_level(
        enterprise_present, section_scores, blocking_errors
    )
    ready_for_enterprise_track = (
        foundation_level == "strong" and blocking_errors == 0
    )

    suggested_tools = _allow_only_real_tools(
        [
            "build_environment_dashboard",
            "get_product_runtime_status",
            "get_real_stand_readiness",
            "get_operation_history",
            "inspect_operation",
        ]
    )
    suggested_write_tools = _allow_only_real_tools(
        [
            "describe_last_write_operation",
            "prepare_rollback_hint",
        ]
    )

    score_summary = ", ".join(
        f"{name}={value}/{_SECTION_MAX_SCORE[name]}"
        for name, value in section_scores.items()
    )
    message = (
        f"Enterprise foundation: level={foundation_level!r}, "
        f"ready_for_enterprise_track={ready_for_enterprise_track}, "
        f"sections=({score_summary}), errors={blocking_errors}."
    )

    return EnterpriseFoundationResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        foundation_level=foundation_level,
        ready_for_enterprise_track=ready_for_enterprise_track,
        enterprise_section_present=enterprise_present,
        deployment_tier=config.enterprise.deployment_tier,
        instance_id=config.enterprise.instance_id,
        config_owner=config.enterprise.config_owner,
        change_control_required=config.enterprise.change_control_required,
        require_operator_identity=config.enterprise.require_operator_identity,
        runbook_reference=config.enterprise.runbook_reference,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        message=message,
    )


def inspect_enterprise_foundation_from_json_file(
    path: str | Path,
) -> EnterpriseFoundationResult:
    """Like :func:`inspect_enterprise_foundation`, but loads config from JSON."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001 — boundary, never propagate
        return _rejected(f"Product config could not be loaded: {exc}")
    return inspect_enterprise_foundation(config)


# Defensive sanity check — the verdict map must reference real
# foundation levels. Ten lines of code; no excuse for a typo.
assert all(
    level in FOUNDATION_LEVELS
    for level in ("absent", "minimal", "partial", "strong")
)
# Reference the imported MCP modules so pyflakes / linters do not
# complain. The import is needed because :func:`_allow_only_real_tools`
# pulls live registries from these modules transitively, but the
# assertion below makes the intent visible at the bottom of the file.
assert all(callable(getattr(m, "list_tools", None)) for m in (_mrs, _mws, _mis))


__all__ = [
    "inspect_enterprise_foundation",
    "inspect_enterprise_foundation_from_json_file",
]
