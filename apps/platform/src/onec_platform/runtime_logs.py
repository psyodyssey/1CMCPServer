"""Per-service runtime log helpers (Phase 6 / Step 6).

Narrow stdlib-only path for routing a service's ``stdout`` /
``stderr`` to log files under
``<work_dir>/.runtime/logs/<service>.{out,err}.log``, with a
single-generation rotate-if-exceeds-size shim.

This module is intentionally tiny:

- it does **not** ship a real logging framework;
- it does **not** know about journald / Windows Service / log
  aggregation;
- it does **not** stream / multiplex / tail;
- it does **not** retain more than one rotated generation
  (``.1`` is the only suffix; an older ``.1`` is overwritten on
  the next rotation, by design).

The runtime boundary
(:mod:`onec_platform.runtime`) is the only caller. Failures
during log preparation surface as ``OSError`` and are turned
into structured findings + fail-closed status by the caller.
"""

from __future__ import annotations

import os
from pathlib import Path

from .state import runtime_dir

_LOGS_DIR_NAME: str = "logs"
_OUT_SUFFIX: str = ".out.log"
_ERR_SUFFIX: str = ".err.log"
_ROTATED_SUFFIX: str = ".1"


def logs_dir(work_dir: str | Path) -> Path:
    """Return the platform-owned ``<work_dir>/.runtime/logs`` path.

    Does not create the directory; that is :func:`prepare_log_dir`'s
    job.
    """
    return runtime_dir(work_dir) / _LOGS_DIR_NAME


def get_log_paths(work_dir: str | Path, service_name: str) -> tuple[Path, Path]:
    """Return ``(stdout_path, stderr_path)`` for a given service.

    Pure path arithmetic — no filesystem side effects.
    """
    base = logs_dir(work_dir)
    return (
        base / f"{service_name}{_OUT_SUFFIX}",
        base / f"{service_name}{_ERR_SUFFIX}",
    )


def prepare_log_dir(work_dir: str | Path) -> Path:
    """Ensure the ``<work_dir>/.runtime/logs`` directory exists.

    The platform-owned ``.runtime`` parent is created if missing
    (the existing :mod:`onec_platform.state` does the same on
    state writes; we mirror that behaviour here so logging is
    self-contained). The caller's ``work_dir`` itself is **not**
    created — that is the operator's territory.

    Raises ``OSError`` on any filesystem problem (missing
    ``work_dir``, permission denied, …). The runtime boundary
    catches this and turns it into a structured finding; the
    service start fails closed rather than silently degrading to
    DEVNULL.
    """
    wd = Path(work_dir)
    if not wd.is_dir():
        raise OSError(
            f"work_dir does not exist or is not a directory: {wd}"
        )
    target = logs_dir(wd)
    target.mkdir(parents=True, exist_ok=True)
    return target


def rotate_log_if_oversized(path: Path, max_bytes: int) -> bool:
    """Rotate ``path`` to ``path.1`` if it is larger than ``max_bytes``.

    One generation only — an older ``path.1`` is overwritten via
    ``os.replace`` (atomic where the OS supports it). Returns
    ``True`` when a rotation actually happened, ``False`` when
    nothing was rotated (file missing, file at-or-below the
    threshold, or ``max_bytes`` non-positive).

    ``OSError`` from ``stat`` / ``replace`` propagates so the
    runtime boundary can fail-closed.
    """
    if max_bytes <= 0:
        return False
    if not path.exists():
        return False
    try:
        size = path.stat().st_size
    except OSError:
        # Stat failed — treat as "nothing to rotate" but let the
        # caller observe the OSError itself if it stat'd directly.
        # Here we re-raise so the boundary can decide.
        raise
    if size <= max_bytes:
        return False
    rotated = path.with_name(path.name + _ROTATED_SUFFIX)
    os.replace(path, rotated)
    return True


def open_log_handles(
    stdout_path: Path, stderr_path: Path
):
    """Open ``stdout_path`` / ``stderr_path`` in append-binary mode.

    Returns the pair ``(stdout_handle, stderr_handle)`` ready to be
    passed to :func:`onec_platform.process_control.spawn_service`.

    Append-binary mode is deliberate:
    - append, so a fresh process does not clobber whatever the
      previous run wrote to the same file (rotation is the
      explicit bound — Step 6 keeps one rotated generation);
    - binary, so the child's encoding does not matter — the file
      stores raw bytes.

    The caller is responsible for closing both handles **after**
    the spawn has returned. The handles must outlive the spawn
    call but can be closed immediately afterwards: the OS-level
    file descriptor is duplicated into the child by Popen, so the
    parent's handle can be released without affecting the child.

    Raises ``OSError`` on any open failure; the runtime boundary
    converts that into a fail-closed finding for the service.
    """
    stdout_handle = open(stdout_path, "ab", buffering=0)
    try:
        stderr_handle = open(stderr_path, "ab", buffering=0)
    except OSError:
        stdout_handle.close()
        raise
    return stdout_handle, stderr_handle
