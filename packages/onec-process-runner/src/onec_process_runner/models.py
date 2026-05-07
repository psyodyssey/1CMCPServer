"""Request/response contracts for running external processes."""

from dataclasses import dataclass


@dataclass
class ProcessRunRequest:
    """Description of a single process invocation."""

    command: list[str]
    cwd: str | None = None
    timeout_seconds: int | float | None = None
    capture_output: bool = True
    text: bool = True
    env: dict[str, str] | None = None
    input_text: str | None = None


@dataclass
class ProcessRunResult:
    """Outcome of a single process invocation."""

    exit_code: int
    completed: bool
    stdout: str
    stderr: str
