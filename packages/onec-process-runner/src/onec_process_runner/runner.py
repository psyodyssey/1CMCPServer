"""Safe process runner built on top of :mod:`subprocess`.

The runner never uses ``shell=True`` and never spawns ``os.system``.
Timeouts are reported as a soft result (``completed=False``), while
start-time failures (missing binary, permission errors) surface as
``ProcessExecutionError`` from :mod:`mcp_common`.
"""

import subprocess

from mcp_common import ProcessExecutionError

from .models import ProcessRunRequest, ProcessRunResult


def run_process(request: ProcessRunRequest) -> ProcessRunResult:
    """Execute a process described by ``request`` and return the result."""
    try:
        completed_process = subprocess.run(
            request.command,
            cwd=request.cwd,
            timeout=request.timeout_seconds,
            capture_output=request.capture_output,
            text=request.text,
            env=request.env,
            input=request.input_text,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr_body = exc.stderr if isinstance(exc.stderr, str) else ""
        timeout_note = (
            f"\n[onec-process-runner] process timed out after "
            f"{request.timeout_seconds} seconds"
        )
        return ProcessRunResult(
            exit_code=-1,
            completed=False,
            stdout=stdout,
            stderr=stderr_body + timeout_note,
        )
    except FileNotFoundError as exc:
        raise ProcessExecutionError(
            f"Executable not found: {request.command[0] if request.command else '<empty>'}"
        ) from exc
    except OSError as exc:
        raise ProcessExecutionError(
            f"Failed to start process {request.command!r}: {exc}"
        ) from exc

    return ProcessRunResult(
        exit_code=completed_process.returncode,
        completed=True,
        stdout=completed_process.stdout or "",
        stderr=completed_process.stderr or "",
    )
