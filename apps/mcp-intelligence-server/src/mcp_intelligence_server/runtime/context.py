"""Build an :class:`IntelligenceRuntimeContext` from an environment.

Read-only. Does not import :mod:`onec_policy_engine` and does not
write anything to disk. Mirrors
``mcp_read_server.runtime.build_runtime_context`` but returns the
intelligence-specific context dataclass which additionally carries a
resolved ``dump_root``.
"""

from pathlib import Path

from onec_config import EnvironmentConfig
from onec_health import check_environment_health, summarize_health

from .models import IntelligenceRuntimeContext


def build_runtime_context(
    environment: EnvironmentConfig,
) -> IntelligenceRuntimeContext:
    """Collect environment health and return an intelligence runtime context."""
    results = check_environment_health(environment)
    codes = summarize_health(results)
    return IntelligenceRuntimeContext(
        environment=environment,
        health_results=results,
        health_codes=codes,
        dump_root=Path(environment.dump_path),
    )
