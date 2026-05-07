"""Data models used by the policy engine."""

from dataclasses import dataclass


@dataclass
class PolicyDecision:
    """Result of a write-policy / preflight check."""

    allowed: bool
    reason: str
    reason_code: str
    require_snapshots: bool


@dataclass
class WriteIntent:
    """Description of a single write-side operation being considered."""

    operation_name: str
    target: str | None = None
