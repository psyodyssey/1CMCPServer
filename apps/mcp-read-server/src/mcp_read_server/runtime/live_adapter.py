"""Low-level live HTTP adapter for the mcp-read-server runtime.

This module stays below the tool layer: it knows how to perform a JSON
GET against an environment's published HTTP endpoint but knows nothing
about specific tool names or payload shapes.
"""

import json
import urllib.error
import urllib.request

from mcp_common import PlatformError
from onec_config import EnvironmentConfig


def fetch_json(url: str, timeout_seconds: int | float) -> dict:
    """HTTP GET the given URL and return the decoded JSON object."""
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            raw_body = response.read()
    except urllib.error.HTTPError as exc:
        raise PlatformError(
            f"HTTP error while fetching {url}: HTTP {exc.code}."
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        raise PlatformError(f"Failed to fetch {url}: {exc}.") from exc

    try:
        text_body = raw_body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PlatformError(
            f"Response from {url} is not valid UTF-8: {exc}."
        ) from exc

    try:
        payload = json.loads(text_body)
    except json.JSONDecodeError as exc:
        raise PlatformError(
            f"Response from {url} is not valid JSON: {exc}."
        ) from exc

    if not isinstance(payload, dict):
        raise PlatformError(
            f"Response from {url} is JSON but not an object "
            f"(got {type(payload).__name__})."
        )
    return payload


def fetch_json_from_environment(
    environment: EnvironmentConfig, relative_path: str
) -> dict:
    """Fetch JSON from ``<http_base_url>/<relative_path>`` on ``environment``."""
    base = environment.http_base_url.rstrip("/")
    suffix = relative_path.lstrip("/")
    url = f"{base}/{suffix}" if suffix else base
    return fetch_json(url, environment.timeout_seconds)
