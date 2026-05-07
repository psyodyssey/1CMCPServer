"""Cross-platform process control primitives (Phase 5 / Step 3, extended Step 6).

Tiny stdlib-only helpers for the runtime layer. Concerns:

- :func:`is_pid_alive` — given a PID we did not spawn ourselves
  (we only kept the PID in the on-disk state file), tell whether
  the OS still knows about a running process under that ID.
- :func:`get_pid_exit_code` — best-effort lookup of the exit code
  of a recently-terminated PID (Windows only; POSIX returns
  ``None`` because we did not spawn the child of the current
  process).
- :func:`terminate_pid` — best-effort polite termination of a
  PID we did not spawn ourselves.
- :func:`spawn_service` — spawn a long-lived service from a
  declarative argv list. By default detaches stdio to
  ``DEVNULL`` (legacy Step 3 behaviour); on Step 6 the runtime
  layer can pass real file handles for ``stdout`` and ``stderr``
  via the ``stdout_handle`` / ``stderr_handle`` parameters and
  the helper attaches them to the child.

POSIX uses :func:`os.kill` with sig=0 / SIGTERM. Windows uses
``ctypes`` to call ``OpenProcess`` + ``WaitForSingleObject`` /
``TerminateProcess`` / ``GetExitCodeProcess`` — :func:`os.kill`
on Windows is **not** a liveness probe (sig=0 still ends up
calling ``TerminateProcess`` in some Python builds), so we
deliberately avoid it there.

These helpers never raise on the happy path of "process is dead /
unreachable / permission denied". Failures are returned as bool/None
so the orchestration boundary can shape them into honest findings.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import IO

_IS_WINDOWS: bool = sys.platform == "win32"


# ---------------------------------------------------------------------------
# Liveness probe.
# ---------------------------------------------------------------------------


if _IS_WINDOWS:  # pragma: no cover - branched by platform
    import ctypes  # noqa: I001

    _SYNCHRONIZE = 0x00100000
    _PROCESS_TERMINATE = 0x0001
    _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _WAIT_TIMEOUT = 0x00000102
    _STILL_ACTIVE = 259  # exit code while process is still running

    def _open_process(pid: int, access: int) -> int:
        kernel32 = ctypes.windll.kernel32
        kernel32.OpenProcess.restype = ctypes.c_void_p
        handle = kernel32.OpenProcess(access, False, pid)
        return int(handle) if handle else 0

    def is_pid_alive(pid: int) -> bool:
        """Return ``True`` iff ``pid`` is currently a live process.

        Uses ``OpenProcess(SYNCHRONIZE)`` + ``WaitForSingleObject(0)``:
        live process is in the *not-signaled* state and the wait
        returns ``WAIT_TIMEOUT``; a dead process is signaled and the
        wait returns ``WAIT_OBJECT_0``. Any error opening the handle
        is treated as "not alive".
        """
        if pid <= 0:
            return False
        kernel32 = ctypes.windll.kernel32
        handle = _open_process(pid, _SYNCHRONIZE)
        if not handle:
            return False
        try:
            result = kernel32.WaitForSingleObject(
                ctypes.c_void_p(handle), 0
            )
            return int(result) == _WAIT_TIMEOUT
        finally:
            kernel32.CloseHandle(ctypes.c_void_p(handle))

    def get_pid_exit_code(pid: int) -> int | None:
        """Return the exit code of ``pid``, or ``None`` if unavailable.

        Phase 6 / Step 6 best-effort helper. Uses
        ``OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)`` +
        ``GetExitCodeProcess``. The handle is openable for some time
        after process exit, so this works for "freshly stale" PIDs.
        Returns ``None`` if the handle cannot be opened, the call
        fails, or the process is still running (``STILL_ACTIVE``).
        Never raises.
        """
        if pid <= 0:
            return None
        kernel32 = ctypes.windll.kernel32
        handle = _open_process(pid, _PROCESS_QUERY_LIMITED_INFORMATION)
        if not handle:
            return None
        try:
            exit_code = ctypes.c_ulong(0)
            ok = kernel32.GetExitCodeProcess(
                ctypes.c_void_p(handle), ctypes.byref(exit_code)
            )
            if not ok:
                return None
            value = int(exit_code.value)
            if value == _STILL_ACTIVE:
                return None
            return value
        finally:
            kernel32.CloseHandle(ctypes.c_void_p(handle))

    def terminate_pid(pid: int) -> bool:
        """Best-effort terminate the given PID. Returns ``True`` on
        success or if the process was already gone."""
        if pid <= 0:
            return False
        kernel32 = ctypes.windll.kernel32
        handle = _open_process(pid, _PROCESS_TERMINATE)
        if not handle:
            # Either we cannot open it, or it does not exist anymore.
            # The contract is "best-effort"; report success only when
            # we know the process is gone, otherwise False.
            return not is_pid_alive(pid)
        try:
            ok = bool(
                kernel32.TerminateProcess(ctypes.c_void_p(handle), 1)
            )
        finally:
            kernel32.CloseHandle(ctypes.c_void_p(handle))
        return ok

else:  # POSIX

    import signal

    def is_pid_alive(pid: int) -> bool:
        """Return ``True`` iff ``pid`` is currently a live process.

        Uses ``os.kill(pid, 0)`` — a no-op signal that raises
        ``ProcessLookupError`` for dead PIDs and returns silently
        for live ones. ``PermissionError`` means the process exists
        but we may not signal it, which we still report as alive.
        """
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    def get_pid_exit_code(pid: int) -> int | None:
        """Return the exit code of ``pid`` if known, else ``None``.

        On POSIX the orchestrator did not spawn this PID as a child
        of the current process (the runtime layer reads PIDs from
        ``runtime-state.json`` after restarts), so ``waitpid`` is
        not available here. Honest degrade: always returns ``None``
        on POSIX rather than fabricating an exit code. Callers that
        want POSIX exit codes need a real supervisor — out of scope
        for Step 6.
        """
        return None

    def terminate_pid(pid: int) -> bool:
        """Best-effort SIGTERM the given PID."""
        if pid <= 0:
            return False
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            return True  # already gone
        except PermissionError:
            return False
        return True


# ---------------------------------------------------------------------------
# Spawn helper.
# ---------------------------------------------------------------------------


def spawn_service(
    command: list[str],
    *,
    working_dir: str | None,
    env_overrides: dict[str, str] | None,
    stdout_handle: IO[bytes] | int | None = None,
    stderr_handle: IO[bytes] | int | None = None,
) -> subprocess.Popen:
    """Spawn a long-lived service subprocess.

    - ``command`` is an argv list (no shell). Caller is responsible
      for resolving the executable on PATH.
    - ``working_dir`` is the cwd of the child process; ``None`` means
      inherit from the parent.
    - ``env_overrides`` is merged on top of ``os.environ``; ``None``
      means inherit unchanged.
    - ``stdout_handle`` / ``stderr_handle`` (Phase 6 / Step 6) accept
      an open file object, an OS-level file descriptor (``int``), or
      ``None``. ``None`` keeps the legacy Step 3 behaviour for that
      stream — ``DEVNULL``. When a handle is supplied the child's
      stream is attached to it, which lets the runtime layer route
      ``stdout`` / ``stderr`` to per-service log files. The caller
      owns the handle's lifecycle; this helper does not close it.
    - ``stdin`` is always ``DEVNULL``: long-lived product services
      do not read from the orchestrator's stdin.
    - On POSIX, ``start_new_session=True`` so a Ctrl-C in the parent
      shell does not propagate to the child. On Windows, the
      equivalent flag is ``CREATE_NEW_PROCESS_GROUP``.
    - ``shell`` is **never** used. The argv list goes through
      ``subprocess.Popen`` directly.

    Raises ``OSError`` if the executable cannot be found / cannot be
    started. The caller (:mod:`onec_platform.runtime`) catches that
    and turns it into a structured finding; this helper is internal.
    """
    if not command:
        raise ValueError("spawn_service requires a non-empty command list.")
    if working_dir is not None:
        if not Path(working_dir).is_dir():
            raise OSError(
                f"working_dir does not exist or is not a directory: "
                f"{working_dir}"
            )

    env: dict[str, str] | None
    if env_overrides:
        env = dict(os.environ)
        env.update(env_overrides)
    else:
        env = None

    stdout = stdout_handle if stdout_handle is not None else subprocess.DEVNULL
    stderr = stderr_handle if stderr_handle is not None else subprocess.DEVNULL

    kwargs: dict = {
        "cwd": working_dir,
        "env": env,
        "stdin": subprocess.DEVNULL,
        "stdout": stdout,
        "stderr": stderr,
        "close_fds": True,
    }
    if _IS_WINDOWS:
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True

    return subprocess.Popen(command, **kwargs)
