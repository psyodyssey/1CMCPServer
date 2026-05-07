"""Minimal rule-based troubleshooting over health-check status codes."""

from .models import TroubleshootingReport


def diagnose_from_health(statuses: list[str]) -> TroubleshootingReport:
    """Map a list of health status codes to a troubleshooting report."""
    if "gateway_down" in statuses:
        return TroubleshootingReport(
            problem_code="gateway_down",
            probable_cause="HTTP gateway is not running or not reachable.",
            recommended_action="Start the HTTP gateway and re-run health checks.",
        )
    if "dump_missing" in statuses:
        return TroubleshootingReport(
            problem_code="dump_missing",
            probable_cause="Configured dump path does not exist.",
            recommended_action="Check dump path configuration and regenerate dump if needed.",
        )
    if "index_lock" in statuses:
        return TroubleshootingReport(
            problem_code="index_lock",
            probable_cause="Search index may be locked by an orphan process.",
            recommended_action="Inspect orphan processes and clear index lock safely.",
        )
    return TroubleshootingReport(
        problem_code="unknown",
        probable_cause="Unknown problem.",
        recommended_action="Run extended diagnostics.",
    )
