"""Build a :class:`RuntimeContext` from an environment configuration."""

from onec_config import EnvironmentConfig
from onec_health import check_environment_health, summarize_health

from .models import RuntimeContext


def build_runtime_context(environment: EnvironmentConfig) -> RuntimeContext:
    """Collect environment health and return a :class:`RuntimeContext`."""
    results = check_environment_health(environment)
    codes = summarize_health(results)
    return RuntimeContext(
        environment=environment,
        health_results=results,
        health_codes=codes,
    )
