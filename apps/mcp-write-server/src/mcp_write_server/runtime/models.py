"""Write-server runtime data models."""

from dataclasses import dataclass

from onec_config import EnvironmentConfig
from onec_health import HealthCheckResult
from onec_policy_engine import PolicyDecision, WriteIntent


@dataclass
class WriteRuntimeContext:
    """Snapshot of environment + write-side preflight state for one tool call."""

    environment: EnvironmentConfig
    intent: WriteIntent
    health_results: list[HealthCheckResult]
    health_codes: list[str]
    policy_decision: PolicyDecision
    audit_dir: str
