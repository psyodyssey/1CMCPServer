"""Fail-fast guards for write-side operations."""

from mcp_common import HealthCheckError, PolicyDeniedError

from .models import WriteRuntimeContext


def require_write_preconditions(context: WriteRuntimeContext) -> None:
    """Raise if the write-side preconditions of ``context`` are not met.

    Policy is checked first: a deny results in :class:`PolicyDeniedError`
    before any health interpretation. Then unhealthy runtime
    (``health_codes != ["ok"]``) raises :class:`HealthCheckError`.
    On success the function returns ``None``.
    """
    if not context.policy_decision.allowed:
        raise PolicyDeniedError(context.policy_decision.reason)
    if context.health_codes != ["ok"]:
        raise HealthCheckError(
            f"Write preconditions failed due to unhealthy runtime: "
            f"{context.health_codes}"
        )
