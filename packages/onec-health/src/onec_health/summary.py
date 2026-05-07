"""Summarization of health-check results into status codes."""

from .models import HealthCheckResult


def summarize_health(results: list[HealthCheckResult]) -> list[str]:
    """Reduce health results to a list of problem codes for troubleshooting."""
    codes: list[str] = []
    for result in results:
        if result.check_name == "dump_path_exists" and result.status == "error":
            codes.append("dump_missing")
        elif result.check_name == "http_gateway" and result.status == "error":
            codes.append("gateway_down")
        elif result.check_name == "search_index" and result.status == "error":
            codes.append("index_lock")
    if not codes:
        return ["ok"]
    return codes
