"""Build a :class:`WriteRuntimeContext` for a prospective write operation."""

from pathlib import Path

from onec_config import EnvironmentConfig
from onec_health import check_environment_health, summarize_health
from onec_policy_engine import WriteIntent, check_write_allowed

from .models import WriteRuntimeContext


def build_runtime_context(
    environment: EnvironmentConfig,
    intent: WriteIntent,
) -> WriteRuntimeContext:
    """Collect environment health, policy decision and audit_dir into a context.

    Does not write anything to disk and does not touch the network beyond
    what the health checks themselves do. ``audit_dir`` is derived from
    ``environment.dump_path`` as ``<dump_path>/.audit`` until
    ``onec-config`` grows a dedicated field.
    """
    results = check_environment_health(environment)
    codes = summarize_health(results)
    decision = check_write_allowed(environment, intent)
    audit_dir = str(Path(environment.dump_path) / ".audit")
    return WriteRuntimeContext(
        environment=environment,
        intent=intent,
        health_results=results,
        health_codes=codes,
        policy_decision=decision,
        audit_dir=audit_dir,
    )
