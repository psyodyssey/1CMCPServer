"""Data models for health-check results."""

from dataclasses import dataclass


@dataclass
class HealthCheckResult:
    """Outcome of a single health check."""

    status: str
    check_name: str
    message: str
