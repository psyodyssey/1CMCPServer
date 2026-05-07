"""onec_process_runner — runner for 1C processes used by the platform."""

from .models import ProcessRunRequest, ProcessRunResult
from .runner import run_process

__all__ = [
    "ProcessRunRequest",
    "ProcessRunResult",
    "run_process",
]
