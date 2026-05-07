"""Runtime orchestration boundary (Phase 5 / Step 3).

Single product-level entry point for ``start`` / ``stop`` /
``status`` / ``reload`` of the long-lived processes declared in
``ProductConfig.runtime``. The product layer **does not** invent
MCP transport for read / write / intelligence — it manages whatever
argv-list commands the operator declared in product-config. If a
service has no command, orchestration fails closed for that service
without guessing.

What this module is, very precisely:

- a thin supervisor over operator-declared subprocesses;
- a persistent on-disk state file under ``<work_dir>/.runtime/`` so
  ``status`` survives orchestrator restarts;
- a cross-platform liveness probe (POSIX: ``os.kill(pid, 0)``;
  Windows: ``WaitForSingleObject`` via ctypes);
- a contract that ``reload`` is a controlled stop-then-start, not
  a hot reload.

What this module is NOT:

- it does **not** start MCP transports inside the three servers —
  those still live as in-process modules;
- it does **not** introduce write effects from inside the product
  layer — :mod:`onec_platform` does not import
  :mod:`onec_policy_engine` and does not call ``run_write_flow``;
- it is **not** a daemon manager / service manager (no Windows
  Service / systemd unit registration on this step);
- it is **not** a per-service health probe (Step 4 belongs to the
  health dashboard).

All boundary helpers (:func:`start_product_runtime`,
:func:`stop_product_runtime`, :func:`get_product_runtime_status`,
:func:`reload_product_runtime`) **never raise** — every error is
captured as a finding inside the structured result.
"""

from __future__ import annotations

import os
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    DoctorFinding,
    ProductConfig,
    ProductServiceSpec,
    RUNTIME_STATE_SCHEMA_VERSION,
    RuntimeOperationResult,
    RuntimeServiceState,
    RuntimeStateFile,
    RuntimeStatusResult,
)
from .process_control import (
    get_pid_exit_code,
    is_pid_alive,
    spawn_service,
    terminate_pid,
)
from .runtime_logs import (
    get_log_paths,
    open_log_handles,
    prepare_log_dir,
    rotate_log_if_oversized,
)
from .state import read_state, state_file_path, write_state


# ---------------------------------------------------------------------------
# Finding factories.
# ---------------------------------------------------------------------------


def _ok(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="ok", confidence=confidence, detail=detail
    )


def _warn(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="warning", confidence=confidence, detail=detail
    )


def _err(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="error", confidence=confidence, detail=detail
    )


# ---------------------------------------------------------------------------
# Pre-flight: config + work_dir.
# ---------------------------------------------------------------------------


def _resolve_config(data: dict | ProductConfig) -> tuple[ProductConfig | None, str | None]:
    """Resolve a ``ProductConfig`` from an input dict or pass-through.

    Returns ``(config, error_message)`` — exactly one is non-None.
    """
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


def _resolve_work_dir(config: ProductConfig) -> tuple[Path | None, DoctorFinding | None]:
    """Confirm ``bootstrap.work_dir`` is set and refers to an existing dir.

    Returns ``(path, finding)`` — exactly one is non-None.
    """
    work_dir = config.bootstrap.work_dir
    if work_dir is None:
        return None, _err(
            "work_dir_not_configured",
            "bootstrap.work_dir is required for runtime orchestration "
            "but is not set in the product config.",
        )
    p = Path(work_dir)
    if not p.exists():
        return None, _err(
            "work_dir_missing",
            f"bootstrap.work_dir does not exist: {p}",
        )
    if not p.is_dir():
        return None, _err(
            "work_dir_not_a_dir",
            f"bootstrap.work_dir exists but is not a directory: {p}",
        )
    return p, None


# ---------------------------------------------------------------------------
# Service-state derivation.
# ---------------------------------------------------------------------------


def _service_state_from_spec(spec: ProductServiceSpec) -> RuntimeServiceState:
    """Build an initial :class:`RuntimeServiceState` from a config spec."""
    configured = bool(spec.command)
    if not spec.enabled:
        status = "disabled"
    elif not configured:
        status = "missing"
    else:
        status = "configured"
    return RuntimeServiceState(
        name=spec.name,
        enabled=spec.enabled,
        configured=configured,
        status=status,
        command=list(spec.command) if spec.command else None,
        working_dir=spec.working_dir,
        env_override_keys=sorted(spec.env_overrides.keys()),
        pid=None,
        started_at=None,
        last_error=None,
        # Step 6 — spec-driven shape is authoritative for the
        # restart policy; numeric counters / log paths / timestamps
        # come from persisted state via the merge below.
        restart_policy=spec.restart_policy,
        restart_attempts=0,
        last_exit_code=None,
        stdout_log_path=None,
        stderr_log_path=None,
        last_started_at=None,
        last_stopped_at=None,
    )


def _merge_persisted_into_spec_state(
    spec_state: RuntimeServiceState,
    persisted: RuntimeServiceState | None,
) -> RuntimeServiceState:
    """Overlay persisted runtime info on top of a spec-derived state.

    Spec-derived shape (``enabled`` / ``configured`` / ``command`` /
    ``working_dir`` / ``env_override_keys`` / ``restart_policy``) is
    authoritative — it reflects the *current* product config.
    Persisted fields (``status`` / ``pid`` / ``started_at`` /
    ``last_error`` / Step 6 counters / log paths / timestamps /
    last_exit_code) are overlaid only when the persisted entry is
    consistent with the current spec (same enabled+configured
    shape).
    """
    if persisted is None:
        return spec_state
    # If the spec says disabled or missing, persisted runtime info is
    # not interesting — surface the spec verdict and drop stale PID.
    if spec_state.status in ("disabled", "missing"):
        return spec_state
    return replace(
        spec_state,
        status=persisted.status,
        pid=persisted.pid,
        started_at=persisted.started_at,
        last_error=persisted.last_error,
        # Step 6 — keep historical counters and log paths from the
        # persisted state, but the policy is taken from the *current*
        # config (spec_state), not from the historical persisted row.
        restart_attempts=persisted.restart_attempts,
        last_exit_code=persisted.last_exit_code,
        stdout_log_path=persisted.stdout_log_path,
        stderr_log_path=persisted.stderr_log_path,
        last_started_at=persisted.last_started_at or persisted.started_at,
        last_stopped_at=persisted.last_stopped_at,
    )


def _materialize_services(
    config: ProductConfig, persisted: RuntimeStateFile | None
) -> dict[str, RuntimeServiceState]:
    """Compose the full service map from the current spec + persisted state."""
    out: dict[str, RuntimeServiceState] = {}
    persisted_services = persisted.services if persisted is not None else {}
    for name, spec in config.runtime.services.items():
        spec_state = _service_state_from_spec(spec)
        out[name] = _merge_persisted_into_spec_state(
            spec_state, persisted_services.get(name)
        )
    return out


def _refresh_running_against_pid(
    services: dict[str, RuntimeServiceState],
) -> list[DoctorFinding]:
    """For any service whose persisted status='running', verify PID liveness.

    Mutates ``services`` in place. Returns informational findings for
    transitions (e.g. "running -> stale" when PID is dead). Phase 6 /
    Step 6: best-effort capture of ``last_exit_code`` (Windows only —
    POSIX returns ``None`` honestly because we did not spawn the PID
    as a child of this process) and stamp ``last_stopped_at``.
    """
    findings: list[DoctorFinding] = []
    for name, svc in list(services.items()):
        if svc.status != "running" or svc.pid is None:
            continue
        if is_pid_alive(svc.pid):
            continue
        exit_code = get_pid_exit_code(svc.pid)
        services[name] = replace(
            svc,
            status="stale",
            last_error=(
                svc.last_error
                or f"PID {svc.pid} from runtime state is not alive."
            ),
            last_exit_code=exit_code,
            last_stopped_at=_now_iso(),
        )
        if exit_code is not None:
            findings.append(
                _warn(
                    f"runtime_pid_stale:{name}",
                    f"Service {name!r} state was 'running' with pid={svc.pid} "
                    f"but the process is not alive (last_exit_code="
                    f"{exit_code}); reporting as 'stale'.",
                )
            )
        else:
            findings.append(
                _warn(
                    f"runtime_pid_stale:{name}",
                    f"Service {name!r} state was 'running' with pid={svc.pid} "
                    "but the process is not alive (exit code unavailable on "
                    "this platform); reporting as 'stale'.",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Filtering by ``only=``.
# ---------------------------------------------------------------------------


def _resolve_only_filter(
    only: Iterable[str] | None,
    services: dict[str, RuntimeServiceState],
) -> tuple[set[str] | None, list[DoctorFinding]]:
    """Validate and apply an ``only=`` whitelist of service names.

    Unknown names yield warning findings but do not abort the
    operation; the operation just operates on the intersection.
    """
    if only is None:
        return None, []
    requested = {str(name) for name in only}
    findings: list[DoctorFinding] = []
    for name in sorted(requested):
        if name not in services:
            findings.append(
                _warn(
                    f"only_filter_unknown:{name}",
                    f"only=… contains service {name!r} which is not "
                    "declared in runtime.services; skipped.",
                )
            )
    return requested, findings


def _selected(
    only: set[str] | None, name: str
) -> bool:
    return only is None or name in only


# ---------------------------------------------------------------------------
# Persistence helpers.
# ---------------------------------------------------------------------------


def _build_state_file(
    config: ProductConfig, services: dict[str, RuntimeServiceState]
) -> RuntimeStateFile:
    return RuntimeStateFile(
        schema_version=RUNTIME_STATE_SCHEMA_VERSION,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        services=services,
    )


def _load_persisted_or_finding(
    work_dir: Path,
) -> tuple[RuntimeStateFile | None, DoctorFinding | None]:
    """Load persisted state; convert :class:`ValueError` into a finding.

    A missing state file is fine: returns ``(None, None)``.
    """
    try:
        return read_state(work_dir), None
    except ValueError as exc:
        return None, _err(
            "runtime_state_unreadable",
            f"Failed to read runtime state: {exc}",
        )


def _persist_or_finding(
    work_dir: Path, state: RuntimeStateFile
) -> DoctorFinding | None:
    try:
        write_state(work_dir, state)
        return None
    except (ValueError, OSError) as exc:
        return _err(
            "runtime_state_unwritable",
            f"Failed to write runtime state: {exc}",
        )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Internal start/stop primitives.
# ---------------------------------------------------------------------------


def _prepare_logs_for_spawn(
    spec: ProductServiceSpec,
    work_dir: Path,
) -> tuple[
    object | None,  # stdout_handle
    object | None,  # stderr_handle
    str | None,  # stdout_path
    str | None,  # stderr_path
    bool,  # rotation_happened
    DoctorFinding | None,  # log_dir_failed finding (if any)
]:
    """Open per-service log handles, rotating if oversized.

    Phase 6 / Step 6 helper. When ``spec.logs_enabled`` is False,
    returns ``(None, None, None, None, False, None)`` and the
    caller routes the spawn to ``DEVNULL`` (legacy behaviour).
    When True, prepares ``<work_dir>/.runtime/logs/`` and opens
    binary-append handles for ``stdout`` / ``stderr``.

    On any filesystem failure (log dir cannot be created, log
    file cannot be opened, rotation cannot rename), returns a
    finding with ``code="runtime_log_dir_failed:<name>"`` /
    ``"runtime_log_open_failed:<name>"`` / etc., and **None**
    handles. The caller (``_start_one``) treats this as
    fail-closed for the start of that specific service — no
    silent fallback to ``DEVNULL``.
    """
    if not spec.logs_enabled:
        return (None, None, None, None, False, None)

    try:
        prepare_log_dir(work_dir)
    except OSError as exc:
        return (
            None,
            None,
            None,
            None,
            False,
            _err(
                f"runtime_log_dir_failed:{spec.name}",
                f"Failed to prepare log directory for service "
                f"{spec.name!r}: {exc}",
            ),
        )

    stdout_path, stderr_path = get_log_paths(work_dir, spec.name)

    rotation_happened = False
    try:
        out_rotated = rotate_log_if_oversized(stdout_path, spec.log_max_bytes)
        err_rotated = rotate_log_if_oversized(stderr_path, spec.log_max_bytes)
        rotation_happened = bool(out_rotated or err_rotated)
    except OSError as exc:
        return (
            None,
            None,
            str(stdout_path),
            str(stderr_path),
            False,
            _err(
                f"runtime_log_rotate_failed:{spec.name}",
                f"Failed to rotate logs for service {spec.name!r}: {exc}",
            ),
        )

    try:
        stdout_handle, stderr_handle = open_log_handles(
            stdout_path, stderr_path
        )
    except OSError as exc:
        return (
            None,
            None,
            str(stdout_path),
            str(stderr_path),
            rotation_happened,
            _err(
                f"runtime_log_open_failed:{spec.name}",
                f"Failed to open log files for service {spec.name!r}: {exc}",
            ),
        )

    return (
        stdout_handle,
        stderr_handle,
        str(stdout_path),
        str(stderr_path),
        rotation_happened,
        None,
    )


def _start_one(
    spec: ProductServiceSpec,
    current: RuntimeServiceState,
    work_dir: Path,
) -> tuple[RuntimeServiceState, list[DoctorFinding]]:
    """Try to start one service. Returns the new state and findings.

    Phase 6 / Step 6: returns a *list* of findings (was a single
    finding in Step 3) so log-rotation / log-dir issues can be
    surfaced alongside the start outcome.
    """
    findings: list[DoctorFinding] = []

    if not spec.enabled:
        return (
            replace(current, status="disabled"),
            [
                _warn(
                    f"runtime_skip_disabled:{spec.name}",
                    f"Service {spec.name!r} is disabled; not starting.",
                )
            ],
        )
    if not spec.command:
        return (
            replace(current, status="missing"),
            [
                _err(
                    f"runtime_command_missing:{spec.name}",
                    f"Service {spec.name!r} has no runtime command; "
                    "fail-closed (no silent default executable).",
                )
            ],
        )

    # Already-running detection: trust persisted state but verify PID.
    if current.status == "running" and current.pid is not None:
        if is_pid_alive(current.pid):
            return (
                current,
                [
                    _ok(
                        f"runtime_already_running:{spec.name}",
                        f"Service {spec.name!r} is already running "
                        f"(pid={current.pid}); start is idempotent.",
                    )
                ],
            )

    (
        stdout_handle,
        stderr_handle,
        stdout_path,
        stderr_path,
        rotation_happened,
        log_finding,
    ) = _prepare_logs_for_spawn(spec, work_dir)
    if log_finding is not None:
        # Fail-closed for this service: log open failed and we
        # explicitly refuse to silently route stdio to DEVNULL.
        findings.append(log_finding)
        return (
            replace(
                current,
                status="error",
                pid=None,
                started_at=None,
                last_error=log_finding.detail,
                stdout_log_path=stdout_path,
                stderr_log_path=stderr_path,
            ),
            findings,
        )

    if rotation_happened:
        findings.append(
            _ok(
                f"runtime_log_rotated:{spec.name}",
                f"Rotated log file(s) for {spec.name!r} above "
                f"log_max_bytes={spec.log_max_bytes}.",
            )
        )

    if spec.logs_enabled:
        findings.append(
            _ok(
                f"runtime_log_paths:{spec.name}",
                f"Service {spec.name!r} log paths: "
                f"stdout={stdout_path}, stderr={stderr_path}.",
            )
        )

    try:
        process = spawn_service(
            list(spec.command),
            working_dir=spec.working_dir,
            env_overrides=spec.env_overrides,
            stdout_handle=stdout_handle,
            stderr_handle=stderr_handle,
        )
    except (OSError, ValueError) as exc:
        # Close any opened log handles so we do not leak them.
        if stdout_handle is not None:
            try:
                stdout_handle.close()
            except OSError:
                pass
        if stderr_handle is not None:
            try:
                stderr_handle.close()
            except OSError:
                pass
        findings.append(
            _err(
                f"runtime_start_failed:{spec.name}",
                f"Failed to spawn {spec.name!r}: {exc}",
            )
        )
        return (
            replace(
                current,
                status="error",
                pid=None,
                started_at=None,
                last_error=str(exc),
                stdout_log_path=stdout_path,
                stderr_log_path=stderr_path,
            ),
            findings,
        )

    # Spawn succeeded — close our copies of the log handles. The
    # OS-level fds are already duplicated into the child by
    # subprocess.Popen, so the child keeps writing happily after the
    # parent's handles are released.
    if stdout_handle is not None:
        try:
            stdout_handle.close()
        except OSError:
            pass
    if stderr_handle is not None:
        try:
            stderr_handle.close()
        except OSError:
            pass

    now = _now_iso()
    findings.append(
        _ok(
            f"runtime_started:{spec.name}",
            f"Service {spec.name!r} started (pid={process.pid}).",
        )
    )
    return (
        replace(
            current,
            status="running",
            pid=process.pid,
            started_at=now,
            last_error=None,
            stdout_log_path=stdout_path,
            stderr_log_path=stderr_path,
            last_started_at=now,
        ),
        findings,
    )


def _stop_one(
    current: RuntimeServiceState,
) -> tuple[RuntimeServiceState, DoctorFinding]:
    """Try to stop one service. Returns the new state and a finding."""
    if current.status not in ("running", "stale"):
        return (
            current,
            _ok(
                f"runtime_already_stopped:{current.name}",
                f"Service {current.name!r} is not running "
                f"(status={current.status!r}); nothing to stop.",
            ),
        )
    now = _now_iso()
    if current.pid is None:
        return (
            replace(
                current,
                status="stopped",
                pid=None,
                started_at=None,
                last_stopped_at=now,
            ),
            _warn(
                f"runtime_stopped_no_pid:{current.name}",
                f"Service {current.name!r} state had no PID; marked stopped.",
            ),
        )
    if not is_pid_alive(current.pid):
        return (
            replace(
                current,
                status="stopped",
                pid=None,
                started_at=None,
                last_stopped_at=now,
            ),
            _ok(
                f"runtime_pid_already_gone:{current.name}",
                f"Service {current.name!r} pid={current.pid} was already "
                "gone; state cleaned up.",
            ),
        )
    ok = terminate_pid(current.pid)
    if ok:
        return (
            replace(
                current,
                status="stopped",
                pid=None,
                started_at=None,
                last_stopped_at=now,
            ),
            _ok(
                f"runtime_stopped:{current.name}",
                f"Service {current.name!r} stopped (was pid={current.pid}).",
            ),
        )
    return (
        replace(current, status="error", last_error=(
            f"terminate_pid({current.pid}) returned False; process may "
            "still be running."
        )),
        _err(
            f"runtime_stop_failed:{current.name}",
            f"Failed to stop service {current.name!r} (pid={current.pid}).",
        ),
    )


def _apply_restart_if_stale(
    config: ProductConfig,
    services: dict[str, RuntimeServiceState],
    work_dir: Path,
) -> list[DoctorFinding]:
    """Restart services whose status is ``stale`` and policy is
    ``restart-if-stale``.

    Phase 6 / Step 6 — only fires on a boundary call (status / start
    / reload). There is no background watcher / timer / supervisor
    daemon. Mutates ``services`` in place. Returns findings:
    ``runtime_restart_attempted:<name>`` always when the policy
    fired, plus ``runtime_restart_succeeded:<name>`` /
    ``runtime_restart_failed:<name>`` reflecting the outcome.

    A service whose policy is ``"never"`` is intentionally left in
    ``"stale"`` — the existing ``runtime_pid_stale:<name>`` finding
    from :func:`_refresh_running_against_pid` is the operator's
    cue.
    """
    findings: list[DoctorFinding] = []
    for name, svc in list(services.items()):
        if svc.status != "stale":
            continue
        spec = config.runtime.services.get(name)
        if spec is None:
            continue
        if spec.restart_policy != "restart-if-stale":
            continue

        # Bump the attempt counter regardless of outcome — that is
        # what "attempts" means.
        attempt_count = svc.restart_attempts + 1
        services[name] = replace(svc, restart_attempts=attempt_count)
        findings.append(
            _warn(
                f"runtime_restart_attempted:{name}",
                f"Service {name!r} is stale and restart_policy="
                f"'restart-if-stale'; attempting restart "
                f"(attempt #{attempt_count}).",
            )
        )

        new_state, start_findings = _start_one(
            spec, services[name], work_dir
        )
        services[name] = new_state
        findings.extend(start_findings)
        if new_state.status == "running":
            findings.append(
                _ok(
                    f"runtime_restart_succeeded:{name}",
                    f"Service {name!r} successfully restarted "
                    f"(pid={new_state.pid}, attempt #{attempt_count}).",
                )
            )
        else:
            findings.append(
                _err(
                    f"runtime_restart_failed:{name}",
                    f"Service {name!r} restart attempt #{attempt_count} "
                    f"did not result in 'running'; status="
                    f"{new_state.status!r}.",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Public boundary helpers.
# ---------------------------------------------------------------------------


def get_product_runtime_status(
    data: dict | ProductConfig,
) -> RuntimeStatusResult:
    """Return a snapshot of runtime state for ``data``.

    Read-only: never spawns / terminates / writes state. If a
    persisted ``status="running"`` entry references a dead PID, the
    return value reports it as ``"stale"``, but the on-disk file is
    not silently rewritten — that's the job of ``start`` / ``stop``
    / ``reload``.
    """
    config, err = _resolve_config(data)
    if config is None:
        return RuntimeStatusResult(
            ok=False,
            product_name=None,
            profile_name=None,
            services=[],
            findings=[_err("config_rejected", err or "Unknown error.")],
            state_path=None,
            message=err or "Product config rejected.",
        )

    findings: list[DoctorFinding] = []

    work_dir, wd_finding = _resolve_work_dir(config)
    if work_dir is None:
        findings.append(wd_finding)  # type: ignore[arg-type]
        return RuntimeStatusResult(
            ok=False,
            product_name=config.product_name,
            profile_name=config.profile_name,
            services=[],
            findings=findings,
            state_path=None,
            message=wd_finding.detail if wd_finding else "work_dir invalid.",
        )

    persisted, persisted_finding = _load_persisted_or_finding(work_dir)
    if persisted_finding is not None:
        findings.append(persisted_finding)

    if not config.runtime.services:
        findings.append(
            _warn(
                "runtime_contract_empty",
                "Product config has no runtime.services entries; "
                "nothing to manage.",
            )
        )

    services_map = _materialize_services(config, persisted)
    findings.extend(_refresh_running_against_pid(services_map))

    # Phase 6 / Step 6 — restart-if-stale fires on this boundary call
    # too (status), not only on start/reload. The whole point of the
    # policy is "every time the operator calls into the runtime
    # boundary, recover from a stale PID". This is *not* a background
    # supervisor: nothing fires unless the operator calls in.
    restart_findings = _apply_restart_if_stale(
        config, services_map, work_dir
    )
    findings.extend(restart_findings)

    # If any restart attempt happened, persist the updated state so
    # the new PID and counters survive — otherwise status is purely
    # read-only and we keep the file untouched.
    if restart_findings:
        persist_finding = _persist_or_finding(
            work_dir, _build_state_file(config, services_map)
        )
        if persist_finding is not None:
            findings.append(persist_finding)

    services_list = sorted(services_map.values(), key=lambda s: s.name)
    state_path = str(state_file_path(work_dir))
    summary = _summarize_statuses(services_list)
    return RuntimeStatusResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        services=services_list,
        findings=findings,
        state_path=state_path,
        message=f"Runtime status: {summary}.",
    )


def start_product_runtime(
    data: dict | ProductConfig,
    *,
    only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Start all enabled+configured services not already running.

    Idempotent: a service that the persisted state lists as
    ``running`` and whose PID is alive is left untouched. Services
    that are disabled or have no command are surfaced as findings,
    not started.
    """
    return _run_operation("start", data, only=only)


def stop_product_runtime(
    data: dict | ProductConfig,
    *,
    only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Stop services that the persisted state lists as running/stale."""
    return _run_operation("stop", data, only=only)


def reload_product_runtime(
    data: dict | ProductConfig,
    *,
    only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Controlled restart: stop, then start.

    **Not** a hot reload. The MVP semantics in Phase 5 / Step 3 are
    a deliberate stop-then-start pass: each in-scope service is
    asked to stop (best-effort), then asked to start. A single
    :class:`RuntimeOperationResult` is returned with combined
    findings from both phases so the operator sees what happened.
    """
    return _run_operation("reload", data, only=only)


# ---------------------------------------------------------------------------
# JSON-file convenience wrappers.
# ---------------------------------------------------------------------------


def _from_json_file(path: str | Path) -> tuple[ProductConfig | None, str | None]:
    try:
        return load_product_config_from_json_file(path), None
    except (ValueError, TypeError) as exc:
        return None, f"Product config rejected: {exc}"


def get_product_runtime_status_from_json_file(
    path: str | Path,
) -> RuntimeStatusResult:
    """Like :func:`get_product_runtime_status`, but loads config from JSON."""
    config, err = _from_json_file(path)
    if config is None:
        return RuntimeStatusResult(
            ok=False,
            product_name=None,
            profile_name=None,
            services=[],
            findings=[_err("config_rejected", err or "Unknown error.")],
            state_path=None,
            message=err or "Product config rejected.",
        )
    return get_product_runtime_status(config)


def start_product_runtime_from_json_file(
    path: str | Path, *, only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Like :func:`start_product_runtime`, but loads config from JSON."""
    config, err = _from_json_file(path)
    if config is None:
        return _rejected("start", err or "Unknown error.")
    return start_product_runtime(config, only=only)


def stop_product_runtime_from_json_file(
    path: str | Path, *, only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Like :func:`stop_product_runtime`, but loads config from JSON."""
    config, err = _from_json_file(path)
    if config is None:
        return _rejected("stop", err or "Unknown error.")
    return stop_product_runtime(config, only=only)


def reload_product_runtime_from_json_file(
    path: str | Path, *, only: Iterable[str] | None = None,
) -> RuntimeOperationResult:
    """Like :func:`reload_product_runtime`, but loads config from JSON."""
    config, err = _from_json_file(path)
    if config is None:
        return _rejected("reload", err or "Unknown error.")
    return reload_product_runtime(config, only=only)


# ---------------------------------------------------------------------------
# Internal operation runner shared by start/stop/reload.
# ---------------------------------------------------------------------------


def _rejected(operation: str, message: str) -> RuntimeOperationResult:
    return RuntimeOperationResult(
        ok=False,
        operation=operation,
        product_name=None,
        profile_name=None,
        services=[],
        findings=[_err("config_rejected", message)],
        message=message,
    )


def _run_operation(
    operation: str,
    data: dict | ProductConfig,
    *,
    only: Iterable[str] | None,
) -> RuntimeOperationResult:
    """Backbone of :func:`start_product_runtime` / ``stop`` / ``reload``."""
    config, err = _resolve_config(data)
    if config is None:
        return _rejected(operation, err or "Unknown error.")

    findings: list[DoctorFinding] = []
    work_dir, wd_finding = _resolve_work_dir(config)
    if work_dir is None:
        findings.append(wd_finding)  # type: ignore[arg-type]
        return RuntimeOperationResult(
            ok=False,
            operation=operation,
            product_name=config.product_name,
            profile_name=config.profile_name,
            services=[],
            findings=findings,
            message=(
                wd_finding.detail
                if wd_finding is not None
                else "work_dir invalid."
            ),
        )

    persisted, persisted_finding = _load_persisted_or_finding(work_dir)
    if persisted_finding is not None:
        findings.append(persisted_finding)

    if not config.runtime.services:
        findings.append(
            _warn(
                "runtime_contract_empty",
                "Product config has no runtime.services entries; "
                "nothing to do.",
            )
        )
        # Honest degradation: ok=True (the operation ran), but
        # services list is empty.
        return RuntimeOperationResult(
            ok=True,
            operation=operation,
            product_name=config.product_name,
            profile_name=config.profile_name,
            services=[],
            findings=findings,
            message=(
                f"{operation}: no runtime contract; nothing to "
                f"{operation}."
            ),
        )

    services_map = _materialize_services(config, persisted)
    findings.extend(_refresh_running_against_pid(services_map))

    only_set, only_findings = _resolve_only_filter(only, services_map)
    findings.extend(only_findings)

    if operation in ("stop", "reload"):
        for name, svc in list(services_map.items()):
            if not _selected(only_set, name):
                continue
            new_state, finding = _stop_one(svc)
            services_map[name] = new_state
            findings.append(finding)

    if operation in ("start", "reload"):
        for name, spec in config.runtime.services.items():
            if not _selected(only_set, name):
                continue
            new_state, start_findings = _start_one(
                spec, services_map[name], work_dir
            )
            services_map[name] = new_state
            findings.extend(start_findings)

    # Phase 6 / Step 6 — restart-if-stale also fires on start /
    # reload boundary calls. ``stop`` deliberately does not trigger
    # restart-if-stale: the operator just asked for a stop, and
    # auto-resurrecting the service after that would surprise them.
    if operation in ("start", "reload"):
        findings.extend(
            _apply_restart_if_stale(config, services_map, work_dir)
        )

    persist_finding = _persist_or_finding(
        work_dir, _build_state_file(config, services_map)
    )
    if persist_finding is not None:
        findings.append(persist_finding)
        # Operation logically ran but state is now inconsistent;
        # surface that honestly via a non-ok result.
        return RuntimeOperationResult(
            ok=False,
            operation=operation,
            product_name=config.product_name,
            profile_name=config.profile_name,
            services=sorted(services_map.values(), key=lambda s: s.name),
            findings=findings,
            message=(
                f"{operation} completed in memory but persisted state "
                "could not be written; see findings."
            ),
        )

    services_list = sorted(services_map.values(), key=lambda s: s.name)
    summary = _summarize_statuses(services_list)
    return RuntimeOperationResult(
        ok=True,
        operation=operation,
        product_name=config.product_name,
        profile_name=config.profile_name,
        services=services_list,
        findings=findings,
        message=f"{operation} done. Status: {summary}.",
    )


def _summarize_statuses(services: list[RuntimeServiceState]) -> str:
    if not services:
        return "no services"
    counts: dict[str, int] = {}
    for svc in services:
        counts[svc.status] = counts.get(svc.status, 0) + 1
    return ", ".join(
        f"{status}={count}" for status, count in sorted(counts.items())
    )
