"""Real-stand / 1cv8 binary integration track (Phase 5 / Step 7).

Two boundary helpers, both read-only by default:

- :func:`get_real_stand_readiness` — observes whether a given product
  config is honestly ready for the controlled smoke test (binary path
  declared, file present, base/dump paths exist, dashboard verdict
  not blocked, etc.);
- :func:`run_real_stand_smoke_test` — preview by default; on
  ``confirm_execute=True`` runs a **controlled probe** of the
  configured binary through :mod:`onec_process_runner`. There is no
  per-tool 1cv8 CLI knowledge baked in — the operator declares the
  probe argv via ``onec_binary_probe_args``; if absent, the smoke
  test stays at metadata-level filesystem checks (existence, file
  vs. directory). Either way, no infobase is mutated and no MCP
  write-tool is invoked.

What this module is, very precisely:

- a thin **product-layer** observer over the binary integration
  contract introduced in :mod:`onec_config` Step 7
  (``EnvironmentConfig.onec_binary_path`` /
  ``EnvironmentConfig.onec_binary_probe_args``);
- a single safe boundary that runs a real subprocess when (and only
  when) the operator has explicitly configured a probe argv. The
  subprocess is run through :func:`onec_process_runner.run_process`,
  which never uses ``shell=True`` and supports timeouts.

What this module is NOT:

- it does **not** introduce new MCP tools or change any registry;
- it does **not** itself rewrite the three binary-backed write tools
  (``create_dump_snapshot`` / ``apply_config_from_files`` /
  ``update_database_configuration``). Their honest dual-mode contract
  was delivered separately by Parallel Track A / Steps 2–4 inside
  ``mcp-write-server``; this module only observes the readiness
  surface and runs the bounded smoke probe;
- it does **not** chain dump → apply → updatedb on the real binary —
  a multi-step round-trip is Track A / Step 6, not this surface;
- it does **not** guess 1cv8-specific CLI flags. The operator owns
  what gets passed to the binary;
- it does **not** open a 1С GUI, mutate an infobase, or talk to a
  real stand from inside the smoke test;
- it does **not** import :mod:`onec_policy_engine`.

Failure model:

- :func:`get_real_stand_readiness`,
  :func:`run_real_stand_smoke_test`, and their ``_from_json_file``
  variants **never raise**.
- ``ok=True`` covers honest happy paths (readiness reported,
  preview built, probe completed). ``ok=False`` is reserved for
  invalid input, unloadable config, and failed probe execution
  inside ``mode="executed"``.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import asdict
from pathlib import Path

from mcp_common import ProcessExecutionError
from onec_config import EnvironmentConfig
from onec_process_runner import ProcessRunRequest, run_process

from .dashboard import build_environment_dashboard
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    DoctorFinding,
    EnvironmentDashboardResult,
    ProductConfig,
    REAL_STAND_SMOKE_MODES,
    RealStandReadinessResult,
    RealStandSmokeResult,
    WorkflowStepResult,
)
from .workflow import _allow_only_real_tools


# ---------------------------------------------------------------------------
# Constants — single source of truth for the Step 7 contract.
# ---------------------------------------------------------------------------

# Maximum length of stdout / stderr excerpts surfaced in the smoke
# result. The assistant never streams arbitrary subprocess output
# upstream — operators read full logs from their own observability.
_PROBE_OUTPUT_EXCERPT_LIMIT: int = 1024

# Default timeout for a single binary probe invocation. Honest cap:
# we do not let an operator-declared probe argv hold the assistant
# indefinitely.
_PROBE_DEFAULT_TIMEOUT_SECONDS: int = 30


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
# Config / environment resolution.
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


def _resolve_environment(config: ProductConfig) -> EnvironmentConfig | None:
    return config.project.environments.get(config.default_environment)


# ---------------------------------------------------------------------------
# Binary-shape inspection.
# ---------------------------------------------------------------------------


def _inspect_binary(
    binary_path: str | None,
) -> tuple[bool, bool, list[DoctorFinding], list[str]]:
    """Inspect the configured binary path without invoking it.

    Returns ``(present, executable_like, findings, recommended_actions)``.

    ``present`` is True iff the path exists. ``executable_like`` is
    True iff the path exists, points at a regular file, and (on
    POSIX) has at least one executable bit. On Windows the
    executable-bit notion is meaningless — we accept the
    ``.exe`` / ``.bat`` / ``.cmd`` suffix or simply trust the
    operator's choice for files without suffix (no silent
    rejection).
    """
    findings: list[DoctorFinding] = []
    actions: list[str] = []

    if not binary_path:
        findings.append(
            _err(
                "binary_path_not_configured",
                "Environment.onec_binary_path is not set; real-stand smoke "
                "is not configured.",
            )
        )
        actions.append(
            "Set 'onec_binary_path' in the default environment to an absolute "
            "path of the 1cv8 executable."
        )
        return False, False, findings, actions

    p = Path(binary_path)
    if not p.exists():
        findings.append(
            _err(
                "binary_path_missing",
                f"onec_binary_path does not exist on disk: {p}",
            )
        )
        actions.append(
            f"Verify that the 1cv8 binary is installed at {p}, or correct "
            "onec_binary_path."
        )
        return False, False, findings, actions

    if p.is_dir():
        findings.append(
            _err(
                "binary_path_is_directory",
                f"onec_binary_path points at a directory, not a file: {p}",
            )
        )
        actions.append(
            f"Set onec_binary_path to a regular file (e.g. 1cv8.exe), not the "
            "containing directory."
        )
        return True, False, findings, actions

    if not p.is_file():
        findings.append(
            _err(
                "binary_path_not_a_regular_file",
                f"onec_binary_path is neither file nor directory: {p}",
            )
        )
        actions.append(
            f"Replace onec_binary_path with a regular file path: {p}"
        )
        return True, False, findings, actions

    # On POSIX, check at least one executable bit. On Windows, treat
    # any regular file as executable-like (the OS does not expose
    # POSIX bits) — operator owns the choice of binary.
    executable_like: bool
    if os.name == "nt":
        executable_like = True
    else:
        try:
            executable_like = bool(p.stat().st_mode & 0o111)
        except OSError:
            executable_like = False
        if not executable_like:
            findings.append(
                _warn(
                    "binary_path_not_executable",
                    f"onec_binary_path is a regular file but has no executable "
                    f"bits set: {p}",
                )
            )
            actions.append(
                f"Set executable permission on the binary (e.g. chmod +x {p})."
            )

    findings.append(
        _ok(
            "binary_path_exists",
            f"onec_binary_path exists and is a regular file: {p}",
        )
    )
    return True, executable_like, findings, actions


# ---------------------------------------------------------------------------
# Boundary: get_real_stand_readiness.
# ---------------------------------------------------------------------------


def _suggested_tools_for_real_stand() -> list[str]:
    return _allow_only_real_tools(
        [
            "build_environment_dashboard",
            "bootstrap_product",
            "get_product_runtime_status",
            "check_runtime_health",
            "diagnose_connectivity_issue",
            "describe_last_write_operation",
            "prepare_rollback_hint",
        ]
    )


def _suggested_write_tools_for_real_stand() -> list[str]:
    # We deliberately surface *only* read-side / audit-side write
    # surfaces here. Step 7 does not ask the operator to call
    # mutating write-tools — those belong to guided workflows.
    return _allow_only_real_tools(
        [
            "describe_last_write_operation",
            "prepare_rollback_hint",
        ]
    )


def _rejected_readiness(message: str) -> RealStandReadinessResult:
    return RealStandReadinessResult(
        ok=False,
        product_name=None,
        profile_name=None,
        default_environment=None,
        onec_binary_path=None,
        binary_present=False,
        binary_executable_like=False,
        has_probe_args=False,
        ready_for_real_stand_smoke=False,
        confirmed_findings=[_err("readiness_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        message=message,
    )


def get_real_stand_readiness(
    data: dict | ProductConfig,
) -> RealStandReadinessResult:
    """Return an honest read-only readiness verdict for the smoke test.

    Never raises. ``ok=True`` covers any case where the readiness
    step itself ran — even when ``ready_for_real_stand_smoke`` is
    False. ``ok=False`` is reserved for invalid inputs / unloadable
    config.
    """
    config, err = _resolve_config(data)
    if config is None:
        return _rejected_readiness(err or "Unknown configuration error.")

    env = _resolve_environment(config)
    if env is None:
        return _rejected_readiness(
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments."
        )

    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    # 1. Binary inspection (filesystem-level only).
    present, executable_like, binary_findings, binary_actions = _inspect_binary(
        env.onec_binary_path
    )
    confirmed.extend(binary_findings)
    actions.extend(binary_actions)

    # 2. Probe args presence — informational, not blocking.
    has_probe_args = bool(env.onec_binary_probe_args)
    if has_probe_args:
        confirmed.append(
            _ok(
                "binary_probe_args_configured",
                f"onec_binary_probe_args has {len(env.onec_binary_probe_args)} "
                "argument(s); smoke test execute mode will run a controlled "
                "subprocess.",
            )
        )
    else:
        presumed.append(
            _warn(
                "binary_probe_args_absent",
                "onec_binary_probe_args is not set; smoke test execute mode "
                "will only perform metadata-level filesystem probes (no "
                "subprocess will be started).",
            )
        )

    # 3. base_path / dump_path / work_dir consistency. We rely on
    #    the dashboard for richer signals but also surface the
    #    binary-track-specific check in plain language here.
    base_path = Path(env.base_path)
    dump_path = Path(env.dump_path)
    if not base_path.exists():
        confirmed.append(
            _err(
                "base_path_missing",
                f"base_path does not exist: {base_path}",
            )
        )
        actions.append(
            f"Create or correct base_path for the default environment: {base_path}"
        )
    else:
        confirmed.append(
            _ok("base_path_exists", f"base_path exists: {base_path}")
        )
    if not dump_path.exists():
        confirmed.append(
            _err(
                "dump_path_missing",
                f"dump_path does not exist: {dump_path}",
            )
        )
        actions.append(
            f"Re-generate dump or correct dump_path: {dump_path}"
        )
    else:
        confirmed.append(
            _ok("dump_path_exists", f"dump_path exists: {dump_path}")
        )

    # 4. Dashboard summary as a presumed signal — the smoke test is a
    #    real-stand action, so it borrows the same precondition idea
    #    as Step 5 mutating workflows: dashboard verdict drives
    #    blocking. We do NOT recompute health here; that's dashboard's
    #    job.
    dash = build_environment_dashboard(config)
    if dash.verdict is not None:
        if dash.verdict.overall_status == "blocked":
            confirmed.append(
                _err(
                    "dashboard_blocked",
                    "Step 4 dashboard verdict is 'blocked'; real-stand smoke "
                    f"test is not ready. Reasons: {dash.verdict.blocking_issues}.",
                )
            )
            actions.append(
                "Resolve dashboard blocking issues before running the "
                "real-stand smoke test (see build_environment_dashboard)."
            )
        elif dash.verdict.overall_status == "degraded":
            presumed.append(
                _warn(
                    "dashboard_degraded",
                    "Step 4 dashboard verdict is 'degraded'; smoke test will "
                    "still build a preview, but execute mode will be blocked "
                    f"until dashboard is healthy. Warnings: {dash.verdict.warnings}.",
                )
            )
        else:
            confirmed.append(
                _ok(
                    "dashboard_healthy",
                    "Step 4 dashboard verdict is 'healthy'.",
                )
            )

    # 5. Final verdict.
    error_count = sum(1 for f in confirmed if f.severity == "error")
    ready = (
        present
        and (executable_like or os.name == "nt")
        and base_path.exists()
        and dump_path.exists()
        and (dash.verdict is None or dash.verdict.overall_status != "blocked")
        and error_count == 0
    )

    suggested_tools = _suggested_tools_for_real_stand()
    suggested_write_tools = _suggested_write_tools_for_real_stand()

    if ready:
        message = (
            "Real-stand readiness OK. "
            f"binary_invocable={'yes' if has_probe_args else 'metadata-only'}; "
            "smoke test is allowed."
        )
    else:
        message = (
            f"Real-stand readiness NOT met ({error_count} blocking finding(s)). "
            "Smoke test execution is not allowed; preview is still available."
        )

    return RealStandReadinessResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        onec_binary_path=env.onec_binary_path,
        binary_present=present,
        binary_executable_like=executable_like,
        has_probe_args=has_probe_args,
        ready_for_real_stand_smoke=ready,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        message=message,
    )


def get_real_stand_readiness_from_json_file(
    path: str | Path,
) -> RealStandReadinessResult:
    """Like :func:`get_real_stand_readiness`, but reads product config from JSON."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_readiness(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_readiness(
            f"Product config could not be loaded: {exc}"
        )
    return get_real_stand_readiness(config)


# ---------------------------------------------------------------------------
# Boundary: run_real_stand_smoke_test.
# ---------------------------------------------------------------------------


def _excerpt(text: str | None) -> str | None:
    if text is None:
        return None
    if len(text) <= _PROBE_OUTPUT_EXCERPT_LIMIT:
        return text
    return text[: _PROBE_OUTPUT_EXCERPT_LIMIT] + "...[truncated]"


def _step(
    name: str,
    kind: str,
    source: str,
    *,
    ok: bool,
    payload: dict | None = None,
    message: str = "",
) -> WorkflowStepResult:
    return WorkflowStepResult(
        name=name,
        kind=kind,
        ok=ok,
        source=source,
        payload=payload or {},
        message=message,
    )


def _build_plan_summary(
    env: EnvironmentConfig,
    readiness: RealStandReadinessResult,
) -> list[str]:
    has_args = bool(env.onec_binary_probe_args)
    summary: list[str] = [
        "Workflow: real-stand binary smoke test (Phase 5 / Step 7).",
        f"onec_binary_path: {env.onec_binary_path!r}",
    ]
    if has_args:
        summary.append(
            "onec_binary_probe_args: configured "
            f"({len(env.onec_binary_probe_args)} argument(s))."
        )
        summary.append(
            "Execute mode will: (1) re-run filesystem readiness checks, "
            "(2) start a controlled subprocess via onec_process_runner with "
            "the operator-declared argv, (3) capture exit code and short "
            "stdout/stderr excerpts. The infobase is NOT mutated and no "
            "MCP write-tool is invoked."
        )
    else:
        summary.append(
            "onec_binary_probe_args: not set; execute mode will only "
            "perform metadata-level filesystem probes (no subprocess)."
        )
    summary.append(
        "After Track A / Steps 2–4 the three binary-backed write tools "
        "(create_dump_snapshot / apply_config_from_files / "
        "update_database_configuration) all share an honest dual-mode "
        "contract: stub branch when the per-tool command template is "
        "not declared, real binary-backed branch via the unified "
        "internal binary_dispatch helper when it is."
    )
    summary.append(
        "This boundary itself is still a bounded probe of real-stand "
        "readiness — it does NOT chain dump → apply → updatedb on the "
        "real binary. A multi-step round-trip is Track A / Step 6, not "
        "this surface. The infobase is not mutated and no MCP "
        "write-tool is invoked from here."
    )
    summary.append(
        f"Real-stand readiness: {'READY' if readiness.ready_for_real_stand_smoke else 'NOT READY'}."
    )
    return summary


def _rejected_smoke(message: str) -> RealStandSmokeResult:
    return RealStandSmokeResult(
        ok=False,
        mode="rejected",
        product_name=None,
        profile_name=None,
        default_environment=None,
        onec_binary_path=None,
        ready_for_real_stand_smoke=False,
        execution_performed=False,
        binary_invoked=False,
        binary_exit_code=None,
        binary_stdout_excerpt=None,
        binary_stderr_excerpt=None,
        plan_summary=[],
        steps=[],
        confirmed_findings=[_err("smoke_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        message=message,
    )


def _readiness_to_step(readiness: RealStandReadinessResult) -> WorkflowStepResult:
    return _step(
        "precondition_real_stand_readiness",
        "precondition",
        "platform.get_real_stand_readiness",
        ok=readiness.ok,
        payload={
            "ready_for_real_stand_smoke": readiness.ready_for_real_stand_smoke,
            "binary_present": readiness.binary_present,
            "binary_executable_like": readiness.binary_executable_like,
            "has_probe_args": readiness.has_probe_args,
            "onec_binary_path": readiness.onec_binary_path,
            "message": readiness.message,
        },
        message=readiness.message,
    )


def _dashboard_step(dash: EnvironmentDashboardResult) -> WorkflowStepResult:
    return _step(
        "precondition_dashboard",
        "precondition",
        "platform.build_environment_dashboard",
        ok=dash.ok,
        payload={
            "verdict": (
                asdict(dash.verdict) if dash.verdict is not None else None
            ),
            "sources_used": list(dash.sources_used),
            "message": dash.message,
        },
        message=dash.message,
    )


def run_real_stand_smoke_test(
    data: dict | ProductConfig,
    *,
    confirm_execute: bool = False,
) -> RealStandSmokeResult:
    """Run a controlled real-stand smoke test.

    Boundary helper. **Never raises.** ``mode`` ∈
    :data:`REAL_STAND_SMOKE_MODES`:

    - ``preview`` — ``confirm_execute=False`` (default); plan
      built, no probe attempted.
    - ``executed`` — ``confirm_execute=True`` and readiness met;
      runs metadata-level probe always, plus a controlled subprocess
      invocation iff ``onec_binary_probe_args`` is configured.
    - ``blocked`` — ``confirm_execute=True`` but readiness gate
      failed (binary missing, dashboard blocked, etc.); preview is
      still preserved.
    - ``rejected`` — invalid input or unloadable config.
    """
    config, err = _resolve_config(data)
    if config is None:
        return _rejected_smoke(err or "Unknown configuration error.")

    env = _resolve_environment(config)
    if env is None:
        return _rejected_smoke(
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments."
        )

    readiness = get_real_stand_readiness(config)
    dash = build_environment_dashboard(config)

    steps: list[WorkflowStepResult] = [
        _dashboard_step(dash),
        _readiness_to_step(readiness),
    ]
    confirmed: list[DoctorFinding] = list(readiness.confirmed_findings)
    presumed: list[DoctorFinding] = list(readiness.presumed_findings)
    actions: list[str] = list(readiness.recommended_actions)
    plan_summary = _build_plan_summary(env, readiness)
    suggested_tools = _suggested_tools_for_real_stand()
    suggested_write_tools = _suggested_write_tools_for_real_stand()

    if not confirm_execute:
        return RealStandSmokeResult(
            ok=True,
            mode="preview",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            onec_binary_path=env.onec_binary_path,
            ready_for_real_stand_smoke=readiness.ready_for_real_stand_smoke,
            execution_performed=False,
            binary_invoked=False,
            binary_exit_code=None,
            binary_stdout_excerpt=None,
            binary_stderr_excerpt=None,
            plan_summary=plan_summary,
            steps=steps,
            confirmed_findings=confirmed,
            presumed_findings=presumed,
            recommended_actions=actions,
            suggested_tools=suggested_tools,
            suggested_write_tools=suggested_write_tools,
            message=(
                "Real-stand smoke preview built. Pass confirm_execute=True "
                "to run the controlled probe."
            ),
        )

    if not readiness.ready_for_real_stand_smoke:
        return RealStandSmokeResult(
            ok=False,
            mode="blocked",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            onec_binary_path=env.onec_binary_path,
            ready_for_real_stand_smoke=False,
            execution_performed=False,
            binary_invoked=False,
            binary_exit_code=None,
            binary_stdout_excerpt=None,
            binary_stderr_excerpt=None,
            plan_summary=plan_summary,
            steps=steps,
            confirmed_findings=confirmed,
            presumed_findings=presumed,
            recommended_actions=actions,
            suggested_tools=suggested_tools,
            suggested_write_tools=suggested_write_tools,
            message=(
                "Real-stand smoke test blocked: readiness gate failed. "
                "Resolve recommended actions and re-run."
            ),
        )

    # 3. Filesystem probe (always part of executed mode).
    p = Path(env.onec_binary_path) if env.onec_binary_path else None
    fs_payload: dict
    if p is not None and p.is_file():
        try:
            stat = p.stat()
            fs_payload = {
                "path": str(p),
                "size_bytes": int(stat.st_size),
                "mtime_unix": int(stat.st_mtime),
                "is_file": True,
            }
            steps.append(
                _step(
                    "filesystem_probe",
                    "executed",
                    "platform.realstand._inspect_binary",
                    ok=True,
                    payload=fs_payload,
                    message=(
                        f"Filesystem probe ok: size={stat.st_size} bytes, "
                        f"path={p}."
                    ),
                )
            )
        except OSError as exc:
            steps.append(
                _step(
                    "filesystem_probe",
                    "executed",
                    "platform.realstand._inspect_binary",
                    ok=False,
                    payload={"path": str(p), "error": str(exc)},
                    message=f"Filesystem probe failed: {exc}",
                )
            )
            confirmed.append(
                _err(
                    "filesystem_probe_failed",
                    f"Failed to stat onec_binary_path: {exc}",
                )
            )
    else:
        # readiness should have caught this; defensive belt-and-braces.
        steps.append(
            _step(
                "filesystem_probe",
                "executed",
                "platform.realstand._inspect_binary",
                ok=False,
                payload={"path": str(p) if p is not None else None},
                message="Filesystem probe skipped: binary path is missing or not a file.",
            )
        )
        confirmed.append(
            _err(
                "filesystem_probe_skipped",
                "Filesystem probe could not run; binary is missing or not a file.",
            )
        )

    # 4. Subprocess probe (only when probe args are configured).
    binary_invoked = False
    binary_exit_code: int | None = None
    binary_stdout: str | None = None
    binary_stderr: str | None = None
    has_args = bool(env.onec_binary_probe_args)
    if has_args and p is not None and p.is_file():
        cmd = [str(p), *env.onec_binary_probe_args]
        try:
            run_result = run_process(
                ProcessRunRequest(
                    command=cmd,
                    timeout_seconds=_PROBE_DEFAULT_TIMEOUT_SECONDS,
                    capture_output=True,
                    text=True,
                )
            )
        except ProcessExecutionError as exc:
            steps.append(
                _step(
                    "binary_probe",
                    "executed",
                    "platform.realstand.run_process",
                    ok=False,
                    payload={"command": cmd, "error": str(exc)},
                    message=f"Binary probe failed to start: {exc}",
                )
            )
            confirmed.append(
                _err(
                    "binary_probe_start_failed",
                    f"Failed to start onec_binary_path probe: {exc}",
                )
            )
        else:
            binary_invoked = True
            binary_exit_code = run_result.exit_code
            binary_stdout = _excerpt(run_result.stdout)
            binary_stderr = _excerpt(run_result.stderr)
            probe_ok = run_result.completed and run_result.exit_code == 0
            steps.append(
                _step(
                    "binary_probe",
                    "executed",
                    "platform.realstand.run_process",
                    ok=probe_ok,
                    payload={
                        "command": cmd,
                        "completed": run_result.completed,
                        "exit_code": run_result.exit_code,
                        "stdout_excerpt": binary_stdout,
                        "stderr_excerpt": binary_stderr,
                    },
                    message=(
                        f"Binary probe completed ok (exit={run_result.exit_code})."
                        if probe_ok
                        else (
                            f"Binary probe finished with exit_code="
                            f"{run_result.exit_code}; "
                            f"completed={run_result.completed}."
                        )
                    ),
                )
            )
            if not probe_ok:
                confirmed.append(
                    _err(
                        "binary_probe_nonzero",
                        f"Binary probe returned exit_code="
                        f"{run_result.exit_code}; "
                        f"completed={run_result.completed}.",
                    )
                )
    elif has_args:
        # has_args is True but the binary is missing/not a file; readiness
        # should have already caught this, but keep the step honest.
        steps.append(
            _step(
                "binary_probe",
                "executed",
                "platform.realstand.run_process",
                ok=False,
                payload={"command": list(env.onec_binary_probe_args)},
                message="Binary probe skipped: binary path is missing or not a file.",
            )
        )

    overall_ok = all(s.ok for s in steps if s.kind == "executed")
    if has_args and not binary_invoked:
        # We expected a subprocess but did not invoke one; honest
        # downgrade.
        overall_ok = False
    message = (
        "Real-stand smoke test executed."
        if overall_ok
        else "Real-stand smoke test ran but reported failures; see steps and findings."
    )
    return RealStandSmokeResult(
        ok=overall_ok,
        mode="executed",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        onec_binary_path=env.onec_binary_path,
        ready_for_real_stand_smoke=True,
        execution_performed=True,
        binary_invoked=binary_invoked,
        binary_exit_code=binary_exit_code,
        binary_stdout_excerpt=binary_stdout,
        binary_stderr_excerpt=binary_stderr,
        plan_summary=plan_summary,
        steps=steps,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        message=message,
    )


def run_real_stand_smoke_test_from_json_file(
    path: str | Path,
    *,
    confirm_execute: bool = False,
) -> RealStandSmokeResult:
    """Like :func:`run_real_stand_smoke_test`, but reads config from JSON."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_smoke(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_smoke(f"Product config could not be loaded: {exc}")
    return run_real_stand_smoke_test(config, confirm_execute=confirm_execute)


__all__ = [
    "REAL_STAND_SMOKE_MODES",
    "get_real_stand_readiness",
    "get_real_stand_readiness_from_json_file",
    "run_real_stand_smoke_test",
    "run_real_stand_smoke_test_from_json_file",
]
