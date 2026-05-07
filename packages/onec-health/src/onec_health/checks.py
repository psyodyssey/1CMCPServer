"""Built-in health checks for live infobase / dump / gateway.

All checks are non-throwing: they always return a :class:`HealthCheckResult`
and never propagate network or filesystem exceptions to the caller.
Legacy boolean inputs are preserved for compatibility with the existing
skeleton selfcheck.
"""

import urllib.error
import urllib.request
from pathlib import Path

from onec_config import EnvironmentConfig

from .models import HealthCheckResult


def check_dump_path_exists(path: str) -> HealthCheckResult:
    """Check whether the configured dump path exists on disk."""
    if Path(path).exists():
        return HealthCheckResult(
            status="ok",
            check_name="dump_path_exists",
            message=f"Dump path exists: {path}",
        )
    return HealthCheckResult(
        status="error",
        check_name="dump_path_exists",
        message=f"Dump path does not exist: {path}",
    )


def check_http_gateway_available(
    target: str | bool,
    timeout_seconds: int | float | None = None,
) -> HealthCheckResult:
    """Check HTTP gateway availability.

    ``target`` can be either a boolean (legacy stub mode, preserved for
    the skeleton selfcheck) or a URL string. In URL mode the function
    performs a real HTTP GET through :mod:`urllib.request`, treating
    2xx/3xx responses as ``ok`` and everything else as ``error``.
    """
    if isinstance(target, bool):
        if target:
            return HealthCheckResult(
                status="ok",
                check_name="http_gateway",
                message="HTTP gateway is reported as available.",
            )
        return HealthCheckResult(
            status="error",
            check_name="http_gateway",
            message="HTTP gateway is reported as unavailable.",
        )

    url = target
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            status_code = response.status
    except urllib.error.HTTPError as exc:
        return HealthCheckResult(
            status="error",
            check_name="http_gateway",
            message=f"HTTP gateway returned error for {url}: HTTP {exc.code}.",
        )
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        return HealthCheckResult(
            status="error",
            check_name="http_gateway",
            message=f"HTTP gateway check failed for {url}: {exc}.",
        )

    if 200 <= status_code < 400:
        return HealthCheckResult(
            status="ok",
            check_name="http_gateway",
            message=f"HTTP gateway is reachable: {url} (HTTP {status_code}).",
        )
    return HealthCheckResult(
        status="error",
        check_name="http_gateway",
        message=f"HTTP gateway returned unexpected status for {url}: HTTP {status_code}.",
    )


def check_search_index_available(target: str | bool) -> HealthCheckResult:
    """Check search-index availability backed by a dump directory.

    ``target`` can be either a boolean (legacy stub mode, preserved for
    the skeleton selfcheck) or a dump directory path string. In path
    mode the function returns ``ok`` when the directory exists and
    contains at least one ``.bsl`` file (searched recursively).
    """
    if isinstance(target, bool):
        if target:
            return HealthCheckResult(
                status="ok",
                check_name="search_index",
                message="Search index is reported as available.",
            )
        return HealthCheckResult(
            status="error",
            check_name="search_index",
            message="Search index is reported as unavailable.",
        )

    dump_dir = Path(target)
    if not dump_dir.is_dir():
        return HealthCheckResult(
            status="error",
            check_name="search_index",
            message=f"Dump path missing or not a directory: {target}.",
        )
    try:
        first_bsl = next(dump_dir.rglob("*.bsl"), None)
    except OSError as exc:
        return HealthCheckResult(
            status="error",
            check_name="search_index",
            message=f"Failed to scan dump path {target}: {exc}.",
        )
    if first_bsl is not None:
        return HealthCheckResult(
            status="ok",
            check_name="search_index",
            message=f"Dump path contains BSL sources: {target}.",
        )
    return HealthCheckResult(
        status="error",
        check_name="search_index",
        message=f"Dump path exists but no BSL files found: {target}.",
    )


def check_environment_health(
    environment: EnvironmentConfig,
) -> list[HealthCheckResult]:
    """Run the three basic health checks for a given environment.

    Returns a list of three :class:`HealthCheckResult` in a stable order:
    dump path existence, HTTP gateway reachability, dump-backed search
    index availability.
    """
    return [
        check_dump_path_exists(environment.dump_path),
        check_http_gateway_available(
            environment.http_base_url, environment.timeout_seconds
        ),
        check_search_index_available(environment.dump_path),
    ]
