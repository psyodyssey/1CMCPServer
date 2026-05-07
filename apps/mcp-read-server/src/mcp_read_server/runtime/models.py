"""Runtime-level data models for mcp-read-server."""

from dataclasses import dataclass

from onec_config import EnvironmentConfig
from onec_health import HealthCheckResult


@dataclass
class RuntimeContext:
    """Snapshot of an environment plus its health state for a tool call."""

    environment: EnvironmentConfig
    health_results: list[HealthCheckResult]
    health_codes: list[str]
