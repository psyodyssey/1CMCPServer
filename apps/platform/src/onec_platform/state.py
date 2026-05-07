"""Persisted runtime state file (Phase 5 / Step 3, extended Step 6).

Layout::

    <work_dir>/.runtime/runtime-state.json

The ``.runtime/`` directory is owned by the platform — it is
auto-created on first state write. The parent ``work_dir`` is the
operator's territory and must already exist; the runtime layer
**never** creates ``work_dir`` itself.

Writes are atomic: contents go to a temporary sibling file, fsync,
then ``os.replace`` over the final path. Writes always emit the
**current** :data:`RUNTIME_STATE_SCHEMA_VERSION` (Phase 6 / Step 6
bumped this to 2).

Readers accept any schema in
:data:`RUNTIME_STATE_READABLE_SCHEMA_VERSIONS`. Schema 1 files
(pre-Step-6) are honestly upgraded in memory: missing fields default
to ``"never"`` / ``0`` / ``None`` so the operator sees a complete
shape without a confusing crash. Truly unknown schema versions are
rejected fail-closed by raising :class:`ValueError` — callers in
:mod:`onec_platform.runtime` catch this and turn it into a
structured finding.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path

from .models import (
    RUNTIME_STATE_READABLE_SCHEMA_VERSIONS,
    RUNTIME_STATE_SCHEMA_VERSION,
    RuntimeServiceState,
    RuntimeStateFile,
)

_RUNTIME_DIR_NAME: str = ".runtime"
_STATE_FILE_NAME: str = "runtime-state.json"


def runtime_dir(work_dir: str | Path) -> Path:
    """Return the platform-owned ``<work_dir>/.runtime`` directory path.

    Does not create it; that's the responsibility of writers.
    """
    return Path(work_dir) / _RUNTIME_DIR_NAME


def state_file_path(work_dir: str | Path) -> Path:
    """Return the absolute path of the persisted state file."""
    return runtime_dir(work_dir) / _STATE_FILE_NAME


def read_state(work_dir: str | Path) -> RuntimeStateFile | None:
    """Load and return the persisted state, or ``None`` if absent.

    Raises :class:`ValueError` for malformed JSON, wrong schema
    version, or structurally invalid content. The runtime boundary
    catches these and turns them into a finding.
    """
    path = state_file_path(work_dir)
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(
            f"Runtime state path is not a regular file: {path}"
        )
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(
            f"Failed to read runtime state {path}: {exc}"
        ) from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Runtime state file is not valid JSON ({path}): {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(
            f"Runtime state root must be a dict (got {type(data).__name__})."
        )

    schema_version = data.get("schema_version")
    if schema_version not in RUNTIME_STATE_READABLE_SCHEMA_VERSIONS:
        raise ValueError(
            f"Unsupported runtime state schema_version "
            f"{schema_version!r}; readable versions: "
            f"{list(RUNTIME_STATE_READABLE_SCHEMA_VERSIONS)}."
        )

    services_raw = data.get("services") or {}
    if not isinstance(services_raw, dict):
        raise ValueError(
            "'services' in runtime state must be a dict."
        )

    services: dict[str, RuntimeServiceState] = {}
    for name, raw in services_raw.items():
        if not isinstance(raw, dict):
            raise ValueError(
                f"Runtime state entry for service {name!r} must be a dict."
            )
        services[name] = RuntimeServiceState(
            name=raw.get("name", name),
            enabled=bool(raw.get("enabled", True)),
            configured=bool(raw.get("configured", False)),
            status=str(raw.get("status", "configured")),
            command=raw.get("command"),
            working_dir=raw.get("working_dir"),
            env_override_keys=list(raw.get("env_override_keys") or []),
            pid=raw.get("pid"),
            started_at=raw.get("started_at"),
            last_error=raw.get("last_error"),
            # Step 6 fields — schema=1 files do not have them, so
            # default to honest sentinels rather than crash.
            restart_policy=str(raw.get("restart_policy", "never")),
            restart_attempts=int(raw.get("restart_attempts", 0) or 0),
            last_exit_code=raw.get("last_exit_code"),
            stdout_log_path=raw.get("stdout_log_path"),
            stderr_log_path=raw.get("stderr_log_path"),
            last_started_at=raw.get("last_started_at")
            or raw.get("started_at"),
            last_stopped_at=raw.get("last_stopped_at"),
        )

    return RuntimeStateFile(
        # Always normalise to the current schema in memory; the writer
        # below also always emits the current schema. Old on-disk
        # files are upgraded on first write after a Step 6 boundary
        # call.
        schema_version=RUNTIME_STATE_SCHEMA_VERSION,
        product_name=str(data.get("product_name", "")),
        profile_name=str(data.get("profile_name", "")),
        default_environment=str(data.get("default_environment", "")),
        services=services,
    )


def write_state(work_dir: str | Path, state: RuntimeStateFile) -> Path:
    """Atomically persist ``state`` to ``<work_dir>/.runtime/runtime-state.json``.

    The platform-owned ``.runtime`` directory is created if missing.
    The parent ``work_dir`` is **not** created here — the operator
    is expected to provide an existing directory. Returns the
    absolute path of the written file.
    """
    wd = Path(work_dir)
    if not wd.is_dir():
        raise ValueError(
            f"work_dir does not exist or is not a directory: {wd}"
        )
    rt_dir = runtime_dir(wd)
    rt_dir.mkdir(parents=True, exist_ok=True)
    target = state_file_path(wd)

    payload = {
        "schema_version": RUNTIME_STATE_SCHEMA_VERSION,
        "product_name": state.product_name,
        "profile_name": state.profile_name,
        "default_environment": state.default_environment,
        "services": {
            name: asdict(svc) for name, svc in state.services.items()
        },
    }

    fd, tmp_path = tempfile.mkstemp(
        prefix="runtime-state-",
        suffix=".json.tmp",
        dir=str(rt_dir),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
    except Exception:
        # Best-effort cleanup of the temp file on failure.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return target
