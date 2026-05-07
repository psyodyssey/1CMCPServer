"""Environment doctor / health dashboard (Phase 5 / Step 4).

Single product-level aggregation boundary that builds one read-only
snapshot of platform health from the signals that already exist
elsewhere in the project. **No new diagnostic logic is invented
here** — the dashboard is a careful aggregator over:

- Step 2 product bootstrap (:func:`bootstrap_product`);
- Step 3 runtime orchestration (:func:`get_product_runtime_status`);
- read-server diagnostics
  (:func:`mcp_read_server.tools.check_runtime_health`,
  :func:`mcp_read_server.tools.diagnose_connectivity_issue`);
- intelligence-server diagnostics
  (:func:`mcp_intelligence_server.tools.analyze_runtime_issue`,
  :func:`mcp_intelligence_server.tools.summarize_configuration_risk`).

What the dashboard is NOT:

- it does **not** introduce new MCP tools or change any registry;
- it does **not** start servers, mutate runtime state, or write to
  the infobase — :func:`build_environment_dashboard` is strictly
  read-only;
- it does **not** import :mod:`onec_policy_engine` and does not
  participate in write-policy decisions;
- it is **not** Step 5 guided workflows — it produces a snapshot
  that workflows can read; it does not run them.

Failure model:

- Boundary helpers (:func:`build_environment_dashboard`,
  :func:`build_environment_dashboard_from_json_file`) **never raise**.
- A single sub-tool failure inside one section degrades that
  section's :attr:`DashboardSectionResult.ok` to ``False`` with a
  honest ``message`` and (where applicable) one error finding;
  the dashboard as a whole still returns ``ok=True``.
- Only an unloadable product config produces a fully ``ok=False``
  dashboard — there is nothing to aggregate on top of.

Verdict:

- :class:`DashboardVerdict.overall_status` is one of ``healthy`` /
  ``degraded`` / ``blocked``, computed by :func:`_compute_verdict`
  with a deterministic, hand-written ruleset (no ML, no
  classification model). The product README documents every rule
  in plain language.
- :class:`DashboardVerdict.ready_for_workflows` is ``True`` only
  when ``overall_status == "healthy"`` — Step 5 workflows then
  treat that as the green-light precondition.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from onec_config import EnvironmentConfig

# Cross-app imports (allowed direction: product → read, product → intelligence).
from mcp_intelligence_server.tools import (
    analyze_runtime_issue,
    summarize_configuration_risk,
)
from mcp_read_server.tools import (
    check_runtime_health,
    diagnose_connectivity_issue,
)

from .bootstrap import bootstrap_product
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    BootstrapResult,
    DASHBOARD_OVERALL_STATUSES,
    DashboardSectionResult,
    DashboardVerdict,
    DoctorFinding,
    EnvironmentDashboardResult,
    ProductConfig,
    RuntimeStatusResult,
)
from .runtime import get_product_runtime_status
from .state import state_file_path


# ---------------------------------------------------------------------------
# Section / source identifiers — kept here as a single source of truth.
# ---------------------------------------------------------------------------

SECTION_BOOTSTRAP: str = "bootstrap"
SECTION_RUNTIME: str = "runtime"
SECTION_READ_HEALTH: str = "read_health"
SECTION_READ_DIAGNOSIS: str = "read_diagnosis"
SECTION_INTELLIGENCE_RUNTIME: str = "intelligence_runtime"
SECTION_INTELLIGENCE_RISK: str = "intelligence_risk"

_SECTION_SOURCES: dict[str, str] = {
    SECTION_BOOTSTRAP: "platform.bootstrap_product",
    SECTION_RUNTIME: "platform.get_product_runtime_status",
    SECTION_READ_HEALTH: "read.check_runtime_health",
    SECTION_READ_DIAGNOSIS: "read.diagnose_connectivity_issue",
    SECTION_INTELLIGENCE_RUNTIME: "intelligence.analyze_runtime_issue",
    SECTION_INTELLIGENCE_RISK: "intelligence.summarize_configuration_risk",
}


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
# Config resolution.
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


def _resolve_environment(
    config: ProductConfig,
) -> EnvironmentConfig | None:
    """Return the default :class:`EnvironmentConfig` or ``None`` if unknown.

    The loader already validates that ``default_environment`` exists in
    ``project.environments``; this helper is defensive.
    """
    return config.project.environments.get(config.default_environment)


# ---------------------------------------------------------------------------
# Section: bootstrap.
# ---------------------------------------------------------------------------


def _bootstrap_payload(result: BootstrapResult) -> dict:
    """Project a :class:`BootstrapResult` into a JSON-friendly dict.

    Used as the section's ``payload`` so the operator can drill into
    the raw bootstrap response without re-running it.
    """
    payload: dict[str, Any] = {
        "ok": result.ok,
        "product_name": result.product_name,
        "profile_name": result.profile_name,
        "default_environment": result.default_environment,
        "message": result.message,
    }
    if result.doctor is not None:
        payload["doctor"] = asdict(result.doctor)
    return payload


def _section_bootstrap(config: ProductConfig) -> DashboardSectionResult:
    """Run :func:`bootstrap_product` against the dataclass and project results."""
    try:
        boot = bootstrap_product(_dictify_config(config))
    except Exception as exc:  # noqa: BLE001 — boundary, never propagate
        return DashboardSectionResult(
            name=SECTION_BOOTSTRAP,
            ok=False,
            source=_SECTION_SOURCES[SECTION_BOOTSTRAP],
            confirmed_findings=[
                _err(
                    "bootstrap_section_unexpected_error",
                    f"bootstrap_product raised: {exc}",
                )
            ],
            payload={},
            message=f"Bootstrap section failed: {exc}",
        )

    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    if not boot.ok:
        confirmed.append(
            _err(
                "bootstrap_rejected",
                boot.message or "Bootstrap could not run.",
            )
        )
        return DashboardSectionResult(
            name=SECTION_BOOTSTRAP,
            ok=False,
            source=_SECTION_SOURCES[SECTION_BOOTSTRAP],
            confirmed_findings=confirmed,
            presumed_findings=presumed,
            recommended_actions=actions,
            payload=_bootstrap_payload(boot),
            message=boot.message,
        )

    if boot.doctor is not None:
        for finding in boot.doctor.findings:
            target = confirmed if finding.confidence == "confirmed" else presumed
            target.append(finding)
        actions = list(boot.doctor.recommended_actions)

    return DashboardSectionResult(
        name=SECTION_BOOTSTRAP,
        ok=True,
        source=_SECTION_SOURCES[SECTION_BOOTSTRAP],
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        payload=_bootstrap_payload(boot),
        message=boot.message,
    )


# ---------------------------------------------------------------------------
# Section: runtime.
# ---------------------------------------------------------------------------


def _runtime_payload(result: RuntimeStatusResult) -> dict:
    return {
        "ok": result.ok,
        "product_name": result.product_name,
        "profile_name": result.profile_name,
        "state_path": result.state_path,
        "services": [asdict(s) for s in result.services],
        "findings": [asdict(f) for f in result.findings],
        "message": result.message,
    }


def _section_runtime(config: ProductConfig) -> DashboardSectionResult:
    """Run :func:`get_product_runtime_status` and project to a section."""
    try:
        status = get_product_runtime_status(config)
    except Exception as exc:  # noqa: BLE001
        return DashboardSectionResult(
            name=SECTION_RUNTIME,
            ok=False,
            source=_SECTION_SOURCES[SECTION_RUNTIME],
            confirmed_findings=[
                _err(
                    "runtime_section_unexpected_error",
                    f"get_product_runtime_status raised: {exc}",
                )
            ],
            payload={},
            message=f"Runtime section failed: {exc}",
        )

    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    # Runtime sub-tool itself splits findings via the ``confidence`` field
    # — we keep that split.
    for finding in status.findings:
        target = confirmed if finding.confidence == "confirmed" else presumed
        target.append(finding)

    # Project per-service status as confirmed informational findings so the
    # operator gets a flat, scannable view at the dashboard level.
    for svc in status.services:
        severity = _runtime_severity_for(svc.status)
        confirmed.append(
            DoctorFinding(
                code=f"runtime_service_state:{svc.name}",
                severity=severity,
                confidence="confirmed",
                detail=(
                    f"{svc.name}: status={svc.status} pid={svc.pid} "
                    f"enabled={svc.enabled} configured={svc.configured}"
                ),
            )
        )

    return DashboardSectionResult(
        name=SECTION_RUNTIME,
        ok=status.ok,
        source=_SECTION_SOURCES[SECTION_RUNTIME],
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        payload=_runtime_payload(status),
        message=status.message,
    )


def _runtime_severity_for(status: str) -> str:
    """Map a runtime ``status`` to a finding severity for dashboard view."""
    if status == "running":
        return "ok"
    if status in ("disabled",):
        return "ok"  # disabled by configuration is not a problem in itself
    if status == "stopped":
        return "ok"  # stopped is not blocking; verdict will use service shape
    if status in ("missing", "error"):
        return "error"
    if status == "stale":
        return "warning"
    return "ok"  # "configured" is fine — service has not been started yet


# ---------------------------------------------------------------------------
# Section: read-side health.
# ---------------------------------------------------------------------------


def _section_read_health(
    config: ProductConfig,
) -> DashboardSectionResult:
    env = _resolve_environment(config)
    if env is None:
        return DashboardSectionResult(
            name=SECTION_READ_HEALTH,
            ok=False,
            source=_SECTION_SOURCES[SECTION_READ_HEALTH],
            confirmed_findings=[
                _err(
                    "default_environment_missing",
                    f"Default environment {config.default_environment!r} is "
                    "not present in project.environments.",
                )
            ],
            message="Default environment cannot be resolved.",
        )

    try:
        result = check_runtime_health(env)
    except Exception as exc:  # noqa: BLE001
        return DashboardSectionResult(
            name=SECTION_READ_HEALTH,
            ok=False,
            source=_SECTION_SOURCES[SECTION_READ_HEALTH],
            confirmed_findings=[
                _err(
                    "read_health_unexpected_error",
                    f"check_runtime_health raised: {exc}",
                )
            ],
            message=f"Read-side health check raised: {exc}",
        )

    payload = result.payload if isinstance(result.payload, dict) else {}
    health_codes = (
        list(payload.get("runtime", {}).get("health_codes", []))
        if isinstance(payload.get("runtime"), dict)
        else []
    )
    checks = (
        payload.get("data", {}).get("checks", [])
        if isinstance(payload.get("data"), dict)
        else []
    )

    confirmed: list[DoctorFinding] = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        check_name = str(check.get("check_name", "unknown"))
        status = str(check.get("status", "unknown"))
        message = str(check.get("message", ""))
        severity = "ok" if status == "ok" else "error" if status == "error" else "warning"
        confirmed.append(
            DoctorFinding(
                code=f"read_health_check:{check_name}",
                severity=severity,
                confidence="confirmed",
                detail=message,
            )
        )

    # Surface the aggregated health_codes once so verdict rules have a flat
    # signal to look at.
    confirmed.append(
        DoctorFinding(
            code="read_health_codes",
            severity="ok" if health_codes == ["ok"] else "warning",
            confidence="confirmed",
            detail=f"runtime.health_codes = {health_codes}",
        )
    )

    return DashboardSectionResult(
        name=SECTION_READ_HEALTH,
        ok=result.ok,
        source=_SECTION_SOURCES[SECTION_READ_HEALTH],
        confirmed_findings=confirmed,
        presumed_findings=[],
        recommended_actions=[],
        payload=payload,
        message=result.message,
    )


# ---------------------------------------------------------------------------
# Section: read-side connectivity diagnosis.
# ---------------------------------------------------------------------------


def _section_read_diagnosis(
    config: ProductConfig,
) -> DashboardSectionResult:
    env = _resolve_environment(config)
    if env is None:
        return DashboardSectionResult(
            name=SECTION_READ_DIAGNOSIS,
            ok=False,
            source=_SECTION_SOURCES[SECTION_READ_DIAGNOSIS],
            confirmed_findings=[
                _err(
                    "default_environment_missing",
                    f"Default environment {config.default_environment!r} is "
                    "not present in project.environments.",
                )
            ],
            message="Default environment cannot be resolved.",
        )

    try:
        result = diagnose_connectivity_issue(env)
    except Exception as exc:  # noqa: BLE001
        return DashboardSectionResult(
            name=SECTION_READ_DIAGNOSIS,
            ok=False,
            source=_SECTION_SOURCES[SECTION_READ_DIAGNOSIS],
            confirmed_findings=[
                _err(
                    "read_diagnosis_unexpected_error",
                    f"diagnose_connectivity_issue raised: {exc}",
                )
            ],
            message=f"Connectivity diagnosis raised: {exc}",
        )

    payload = result.payload if isinstance(result.payload, dict) else {}
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    problem_code = data.get("problem_code")
    probable_cause = data.get("probable_cause") or ""
    recommended_action = data.get("recommended_action") or ""

    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    if problem_code:
        presumed.append(
            DoctorFinding(
                code=f"connectivity_diagnosis:{problem_code}",
                severity="warning",
                confidence="presumed",
                detail=probable_cause,
            )
        )
        if recommended_action:
            actions.append(recommended_action)

    return DashboardSectionResult(
        name=SECTION_READ_DIAGNOSIS,
        ok=True,
        source=_SECTION_SOURCES[SECTION_READ_DIAGNOSIS],
        confirmed_findings=[],
        presumed_findings=presumed,
        recommended_actions=actions,
        payload=payload,
        message=result.message,
    )


# ---------------------------------------------------------------------------
# Section: intelligence runtime aggregation.
# ---------------------------------------------------------------------------


def _section_intelligence_runtime(
    config: ProductConfig,
) -> DashboardSectionResult:
    env = _resolve_environment(config)
    if env is None:
        return DashboardSectionResult(
            name=SECTION_INTELLIGENCE_RUNTIME,
            ok=False,
            source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RUNTIME],
            confirmed_findings=[
                _err(
                    "default_environment_missing",
                    f"Default environment {config.default_environment!r} is "
                    "not present in project.environments.",
                )
            ],
            message="Default environment cannot be resolved.",
        )

    try:
        result = analyze_runtime_issue(env)
    except Exception as exc:  # noqa: BLE001
        return DashboardSectionResult(
            name=SECTION_INTELLIGENCE_RUNTIME,
            ok=False,
            source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RUNTIME],
            confirmed_findings=[
                _err(
                    "intelligence_runtime_unexpected_error",
                    f"analyze_runtime_issue raised: {exc}",
                )
            ],
            message=f"Intelligence runtime analysis raised: {exc}",
        )

    payload = result.payload if isinstance(result.payload, dict) else {}
    confirmed_raw = payload.get("confirmed_findings") or []
    presumed_raw = payload.get("presumed_findings") or []
    recommended = payload.get("recommended_checks") or []

    confirmed = [_normalise_finding(item, "confirmed") for item in confirmed_raw]
    presumed = [_normalise_finding(item, "presumed") for item in presumed_raw]

    return DashboardSectionResult(
        name=SECTION_INTELLIGENCE_RUNTIME,
        ok=result.ok,
        source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RUNTIME],
        confirmed_findings=[f for f in confirmed if f is not None],
        presumed_findings=[f for f in presumed if f is not None],
        recommended_actions=[str(item) for item in recommended],
        payload=payload,
        message=result.message,
    )


# ---------------------------------------------------------------------------
# Section: intelligence risk summary.
# ---------------------------------------------------------------------------


def _section_intelligence_risk(
    config: ProductConfig,
) -> DashboardSectionResult:
    env = _resolve_environment(config)
    if env is None:
        return DashboardSectionResult(
            name=SECTION_INTELLIGENCE_RISK,
            ok=False,
            source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RISK],
            confirmed_findings=[
                _err(
                    "default_environment_missing",
                    f"Default environment {config.default_environment!r} is "
                    "not present in project.environments.",
                )
            ],
            message="Default environment cannot be resolved.",
        )

    try:
        result = summarize_configuration_risk(env)
    except Exception as exc:  # noqa: BLE001
        return DashboardSectionResult(
            name=SECTION_INTELLIGENCE_RISK,
            ok=False,
            source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RISK],
            confirmed_findings=[
                _err(
                    "intelligence_risk_unexpected_error",
                    f"summarize_configuration_risk raised: {exc}",
                )
            ],
            message=f"Intelligence risk summary raised: {exc}",
        )

    payload = result.payload if isinstance(result.payload, dict) else {}
    risk_level = str(payload.get("risk_level", "unknown"))
    severity = (
        "error" if risk_level == "high"
        else "warning" if risk_level == "medium"
        else "ok"
    )
    presumed_raw = payload.get("presumed_findings") or []

    presumed: list[DoctorFinding] = [
        DoctorFinding(
            code=f"intelligence_risk_level:{risk_level}",
            severity=severity,
            confidence="presumed",
            detail=f"Risk level reported as {risk_level!r}.",
        )
    ]
    for item in presumed_raw:
        finding = _normalise_finding(item, "presumed")
        if finding is not None:
            presumed.append(finding)

    return DashboardSectionResult(
        name=SECTION_INTELLIGENCE_RISK,
        ok=result.ok,
        source=_SECTION_SOURCES[SECTION_INTELLIGENCE_RISK],
        confirmed_findings=[],
        presumed_findings=presumed,
        recommended_actions=[
            str(item) for item in (payload.get("recommended_checks") or [])
        ],
        payload=payload,
        message=result.message,
    )


# ---------------------------------------------------------------------------
# Helpers — normalise foreign findings, dictify config.
# ---------------------------------------------------------------------------


def _normalise_finding(item: Any, confidence: str) -> DoctorFinding | None:
    """Turn an intelligence-tool finding (free-shaped dict) into a
    :class:`DoctorFinding`.

    Intelligence-tools produce findings as dicts with various shapes
    (``code`` / ``pattern`` / ``problem_code`` / etc.). This helper
    normalises the most common keys; unknown shapes fall back to a
    string representation so nothing is silently dropped.
    """
    if not isinstance(item, dict):
        return DoctorFinding(
            code="intelligence_finding",
            severity="warning",
            confidence=confidence,
            detail=str(item),
        )
    code = str(
        item.get("code")
        or item.get("pattern")
        or item.get("problem_code")
        or "intelligence_finding"
    )
    detail = str(
        item.get("detail")
        or item.get("probable_cause")
        or item.get("hint")
        or item.get("recommended_action")
        or item.get("category")
        or ""
    )
    severity = str(item.get("severity") or ("error" if confidence == "confirmed" else "warning"))
    if severity not in ("ok", "warning", "error"):
        severity = "warning"
    return DoctorFinding(
        code=code, severity=severity, confidence=confidence, detail=detail
    )


def _dictify_config(config: ProductConfig) -> dict:
    """Reduce a :class:`ProductConfig` to the dict shape expected by
    :func:`bootstrap_product` / :func:`load_product_config`.

    Avoids re-entering the loader for already-validated config — we
    just hand it the already-parsed shape. Field names mirror the
    JSON contract documented in the product layer README.
    """
    envs: dict = {}
    for key, env in config.project.environments.items():
        envs[key] = {
            "name": env.name,
            "base_id": env.base_id,
            "base_path": env.base_path,
            "publication_name": env.publication_name,
            "http_base_url": env.http_base_url,
            "dump_path": env.dump_path,
            "timeout_seconds": env.timeout_seconds,
            "allow_write": env.allow_write,
        }
    runtime_services: dict[str, dict] = {}
    for name, spec in config.runtime.services.items():
        runtime_services[name] = {
            "enabled": spec.enabled,
            "command": list(spec.command) if spec.command else None,
            "working_dir": spec.working_dir,
            "env_overrides": dict(spec.env_overrides),
        }
    return {
        "product_name": config.product_name,
        "profile_name": config.profile_name,
        "default_environment": config.default_environment,
        "project": {"environments": envs},
        "servers": {
            "read": config.servers.read,
            "write": config.servers.write,
            "intelligence": config.servers.intelligence,
        },
        "bootstrap": {
            "work_dir": config.bootstrap.work_dir,
            "require_dump_path": config.bootstrap.require_dump_path,
            "require_base_path": config.bootstrap.require_base_path,
            "require_python": config.bootstrap.require_python,
        },
        "runtime": {"services": runtime_services},
    }


# ---------------------------------------------------------------------------
# Verdict.
# ---------------------------------------------------------------------------


def _required_runtime_services(config: ProductConfig) -> list[str]:
    """Return service names that count as 'required' for verdict rules.

    A runtime service is required iff its spec has ``enabled=True`` and
    has a non-empty command (i.e. it is "configured" in the
    Step 3 sense). Disabled services do not block the verdict;
    services with no command are surfaced via their own ``missing``
    finding but are not implicitly required either.
    """
    out: list[str] = []
    for name, spec in config.runtime.services.items():
        if spec.enabled and spec.command:
            out.append(name)
    return out


def _runtime_service_status_map(
    runtime_section: DashboardSectionResult,
) -> dict[str, str]:
    """Pull a name→status map from the runtime section's payload."""
    services_raw = runtime_section.payload.get("services") or []
    out: dict[str, str] = {}
    if not isinstance(services_raw, list):
        return out
    for raw in services_raw:
        if isinstance(raw, dict):
            name = raw.get("name")
            status = raw.get("status")
            if isinstance(name, str) and isinstance(status, str):
                out[name] = status
    return out


def _read_health_codes(
    read_health_section: DashboardSectionResult,
) -> list[str]:
    """Pull health_codes from the read_health section's payload."""
    runtime_block = read_health_section.payload.get("runtime")
    if isinstance(runtime_block, dict):
        codes = runtime_block.get("health_codes")
        if isinstance(codes, list):
            return [str(c) for c in codes]
    return []


def _intel_risk_level(risk_section: DashboardSectionResult) -> str:
    payload = risk_section.payload
    return str(payload.get("risk_level", "unknown")) if isinstance(payload, dict) else "unknown"


def _compute_verdict(
    config: ProductConfig,
    sections: dict[str, DashboardSectionResult],
) -> DashboardVerdict:
    """Apply a fixed, deterministic ruleset over the sections.

    Plain-language rules (also documented in the product README):

    - **blocked** if:
      - bootstrap section is ``ok=False``;
      - bootstrap doctor reports any error finding (severity=error);
      - runtime section is ``ok=False`` (e.g. work_dir invalid);
      - any required runtime service is in ``missing`` or ``error``;
      - read-side health codes contain ``dump_missing`` or
        ``gateway_down``.
    - **degraded** if (and not blocked):
      - any runtime service is ``stale``;
      - read-side health codes contain anything other than ``ok``;
      - bootstrap doctor has any warning;
      - intelligence risk level is ``medium`` or ``high``;
      - runtime contract is empty (Step 2 product-config without
        ``runtime`` section);
      - any section returned ``ok=False`` for a reason other than the
        ones already classified blocked.
    - **healthy** otherwise.

    ``ready_for_workflows`` is ``True`` iff ``overall_status == "healthy"``.
    """
    blocking: list[str] = []
    warnings: list[str] = []
    rationale: list[str] = []

    bootstrap = sections[SECTION_BOOTSTRAP]
    runtime = sections[SECTION_RUNTIME]
    read_health = sections[SECTION_READ_HEALTH]
    read_diagnosis = sections[SECTION_READ_DIAGNOSIS]
    intel_runtime = sections[SECTION_INTELLIGENCE_RUNTIME]
    intel_risk = sections[SECTION_INTELLIGENCE_RISK]

    # --- BLOCKING rules ----------------------------------------------------
    if not bootstrap.ok:
        blocking.append("bootstrap_section_failed")
        rationale.append(
            f"bootstrap section is ok=False ({bootstrap.message!r})."
        )
    bootstrap_errors = [
        f for f in bootstrap.confirmed_findings if f.severity == "error"
    ] + [
        f for f in bootstrap.presumed_findings if f.severity == "error"
    ]
    if bootstrap_errors:
        for f in bootstrap_errors:
            blocking.append(f"bootstrap_error:{f.code}")
        rationale.append(
            f"bootstrap doctor reported {len(bootstrap_errors)} blocking finding(s)."
        )

    if not runtime.ok:
        blocking.append("runtime_section_failed")
        rationale.append(
            f"runtime section is ok=False ({runtime.message!r})."
        )
    runtime_status_map = _runtime_service_status_map(runtime)
    required = _required_runtime_services(config)
    for svc_name in required:
        status = runtime_status_map.get(svc_name)
        if status in ("missing", "error"):
            blocking.append(f"runtime_required_service_{status}:{svc_name}")
            rationale.append(
                f"required service {svc_name!r} is {status}."
            )

    health_codes = _read_health_codes(read_health)
    for code in health_codes:
        if code in ("dump_missing", "gateway_down"):
            blocking.append(f"read_health_code:{code}")
            rationale.append(
                f"read-side health reports blocking code {code!r}."
            )

    # --- DEGRADED rules ----------------------------------------------------
    for svc_name, status in runtime_status_map.items():
        if status == "stale":
            warnings.append(f"runtime_service_stale:{svc_name}")
            rationale.append(
                f"runtime service {svc_name!r} is stale (PID gone)."
            )

    non_ok_codes = [c for c in health_codes if c != "ok"]
    extra_health_codes = [
        c for c in non_ok_codes if c not in ("dump_missing", "gateway_down")
    ]
    for code in extra_health_codes:
        warnings.append(f"read_health_code:{code}")
        rationale.append(
            f"read-side health reports non-ok code {code!r}."
        )

    if bootstrap.ok and not bootstrap_errors:
        bootstrap_warnings = [
            f
            for f in bootstrap.confirmed_findings + bootstrap.presumed_findings
            if f.severity == "warning"
        ]
        if bootstrap_warnings:
            warnings.append("bootstrap_warnings")
            rationale.append(
                f"bootstrap doctor reports {len(bootstrap_warnings)} warning(s)."
            )

    risk_level = _intel_risk_level(intel_risk)
    if risk_level in ("medium", "high"):
        warnings.append(f"intelligence_risk_level:{risk_level}")
        rationale.append(
            f"intelligence risk_level is {risk_level!r}."
        )

    if not config.runtime.services:
        warnings.append("runtime_contract_empty")
        rationale.append(
            "product config has no runtime.services entries."
        )

    for section_name in (
        SECTION_READ_DIAGNOSIS,
        SECTION_INTELLIGENCE_RUNTIME,
        SECTION_INTELLIGENCE_RISK,
    ):
        section = sections[section_name]
        if not section.ok:
            warnings.append(f"section_failed:{section_name}")
            rationale.append(
                f"section {section_name!r} returned ok=False."
            )

    # connectivity diagnosis with a non-null problem_code is also a warning
    diag_payload = read_diagnosis.payload
    if isinstance(diag_payload, dict):
        diag_data = diag_payload.get("data") if isinstance(diag_payload.get("data"), dict) else {}
        problem_code = diag_data.get("problem_code")
        if problem_code:
            tag = f"connectivity_problem:{problem_code}"
            if tag not in warnings:
                warnings.append(tag)
                rationale.append(
                    f"connectivity diagnosis reports problem_code={problem_code!r}."
                )

    # silence intel_runtime — its findings overlap with read_health and
    # bootstrap; we already account for the underlying signals above. We
    # do not double-count it for the verdict, but it stays in the per-section
    # report for the operator.
    _ = intel_runtime  # explicitly unused in verdict, kept in sections.

    if blocking:
        overall = "blocked"
    elif warnings:
        overall = "degraded"
    else:
        overall = "healthy"
    assert overall in DASHBOARD_OVERALL_STATUSES  # belt and suspenders

    return DashboardVerdict(
        overall_status=overall,
        ready_for_workflows=(overall == "healthy"),
        blocking_issues=blocking,
        warnings=warnings,
        rationale=rationale,
    )


# ---------------------------------------------------------------------------
# Aggregation helpers.
# ---------------------------------------------------------------------------


def _tagged(finding: DoctorFinding, section_name: str) -> DoctorFinding:
    """Return a copy of ``finding`` with the section tag prepended to ``code``."""
    return DoctorFinding(
        code=f"{section_name}/{finding.code}",
        severity=finding.severity,
        confidence=finding.confidence,
        detail=finding.detail,
    )


def _aggregate_findings(
    sections: dict[str, DashboardSectionResult],
    bucket: str,
) -> list[DoctorFinding]:
    out: list[DoctorFinding] = []
    for name, section in sections.items():
        source = (
            section.confirmed_findings
            if bucket == "confirmed"
            else section.presumed_findings
        )
        for finding in source:
            out.append(_tagged(finding, name))
    return out


def _aggregate_actions(
    sections: dict[str, DashboardSectionResult],
) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for section in sections.values():
        for action in section.recommended_actions:
            if action and action not in seen:
                seen.add(action)
                out.append(action)
    return out


def _resolve_state_path(config: ProductConfig) -> str | None:
    """Return the runtime state path if work_dir is set; else None."""
    if not config.bootstrap.work_dir:
        return None
    try:
        return str(state_file_path(config.bootstrap.work_dir))
    except Exception:  # noqa: BLE001 — best-effort path discovery
        return None


# ---------------------------------------------------------------------------
# Public boundary helpers.
# ---------------------------------------------------------------------------


def _dashboard_rejected(reason: str) -> EnvironmentDashboardResult:
    return EnvironmentDashboardResult(
        ok=False,
        product_name=None,
        profile_name=None,
        default_environment=None,
        work_dir=None,
        state_path=None,
        sections={},
        verdict=None,
        confirmed_findings=[
            _err("config_rejected", reason)
        ],
        presumed_findings=[],
        recommended_actions=[],
        sources_used=[],
        message=reason,
    )


def build_environment_dashboard(
    data: dict | ProductConfig,
) -> EnvironmentDashboardResult:
    """Aggregate platform / read / intelligence signals into one snapshot.

    Read-only. Never raises. Returns ``ok=False`` only when the product
    config itself cannot be loaded.
    """
    config, err = _resolve_config(data)
    if config is None:
        return _dashboard_rejected(err or "Unknown configuration error.")

    sections: dict[str, DashboardSectionResult] = {
        SECTION_BOOTSTRAP: _section_bootstrap(config),
        SECTION_RUNTIME: _section_runtime(config),
        SECTION_READ_HEALTH: _section_read_health(config),
        SECTION_READ_DIAGNOSIS: _section_read_diagnosis(config),
        SECTION_INTELLIGENCE_RUNTIME: _section_intelligence_runtime(config),
        SECTION_INTELLIGENCE_RISK: _section_intelligence_risk(config),
    }
    verdict = _compute_verdict(config, sections)
    confirmed = _aggregate_findings(sections, "confirmed")
    presumed = _aggregate_findings(sections, "presumed")
    actions = _aggregate_actions(sections)
    sources = sorted({section.source for section in sections.values()})

    state_path: str | None = None
    runtime_payload = sections[SECTION_RUNTIME].payload
    if isinstance(runtime_payload, dict):
        sp = runtime_payload.get("state_path")
        if isinstance(sp, str):
            state_path = sp
    if state_path is None:
        state_path = _resolve_state_path(config)

    message = (
        f"Dashboard built. overall_status={verdict.overall_status}; "
        f"ready_for_workflows={verdict.ready_for_workflows}."
    )

    return EnvironmentDashboardResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        work_dir=config.bootstrap.work_dir,
        state_path=state_path,
        sections=sections,
        verdict=verdict,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        sources_used=sources,
        message=message,
    )


def build_environment_dashboard_from_json_file(
    path: str | Path,
) -> EnvironmentDashboardResult:
    """Like :func:`build_environment_dashboard`, but reads a JSON product
    config from disk first. Never raises."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _dashboard_rejected(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _dashboard_rejected(
            f"Product config could not be loaded: {exc}"
        )
    return build_environment_dashboard(config)
