"""Read-server tool implementations."""

import urllib.parse

from mcp_common import PlatformError
from onec_config import EnvironmentConfig
from onec_health import (
    check_dump_path_exists,
    check_http_gateway_available,
    check_search_index_available,
    summarize_health,
)
from onec_troubleshooting import diagnose_from_health

from .models import ToolResult
from .runtime import (
    build_runtime_context,
    fetch_json_from_environment,
    find_files_by_pattern,
    read_dump_file,
    read_text_file,
    resolve_dump_path,
)

_PREVIEW_RADIUS = 80

_WRITE_KEYWORDS = (
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
)


def ping() -> ToolResult:
    """Return a liveness marker for the read server."""
    return ToolResult(
        ok=True,
        tool_name="ping",
        message="mcp-read-server is alive.",
        payload={"status": "ok"},
    )


def health_summary(
    dump_path: str,
    gateway_available: bool = True,
    search_index_available: bool = True,
) -> ToolResult:
    """Aggregate health checks into a troubleshooting-aware summary."""
    results = [
        check_dump_path_exists(dump_path),
        check_http_gateway_available(gateway_available),
        check_search_index_available(search_index_available),
    ]
    codes = summarize_health(results)
    if codes == ["ok"]:
        return ToolResult(
            ok=True,
            tool_name="health_summary",
            message="All health checks passed.",
            payload={"health_codes": ["ok"], "troubleshooting": None},
        )
    report = diagnose_from_health(codes)
    return ToolResult(
        ok=False,
        tool_name="health_summary",
        message="Health issues detected.",
        payload={
            "health_codes": codes,
            "troubleshooting": {
                "problem_code": report.problem_code,
                "probable_cause": report.probable_cause,
                "recommended_action": report.recommended_action,
            },
        },
    )


def get_configuration_info(environment: EnvironmentConfig) -> ToolResult:
    """Read high-level configuration info from the live HTTP endpoint."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    try:
        data = fetch_json_from_environment(environment, "configuration")
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_configuration_info",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_configuration_info",
        message="Configuration info loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def get_metadata_tree(
    environment: EnvironmentConfig,
    filter_value: str | None = None,
) -> ToolResult:
    """Read metadata tree from the live HTTP endpoint, optionally filtered."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    if filter_value is None:
        relative_path = "metadata"
    else:
        relative_path = f"metadata?filter={urllib.parse.quote(filter_value)}"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_metadata_tree",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_metadata_tree",
        message="Metadata tree loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def get_metadata_object(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Read a single metadata object card by full name (e.g. ``Catalog.Items``)."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    relative_path = f"metadata/object?name={urllib.parse.quote(object_name)}"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_metadata_object",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_metadata_object",
        message="Metadata object loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def _snippet(text: str, hit_idx: int, query_len: int) -> str:
    """Return ``text`` around ``hit_idx`` padded by ``_PREVIEW_RADIUS`` on each side."""
    start = max(0, hit_idx - _PREVIEW_RADIUS)
    end = min(len(text), hit_idx + query_len + _PREVIEW_RADIUS)
    return text[start:end]


def read_module_code_from_dump(
    environment: EnvironmentConfig,
    relative_path: str,
) -> ToolResult:
    """Read a single dump file by path relative to the environment's dump root."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    try:
        text = read_dump_file(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="read_module_code_from_dump",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="read_module_code_from_dump",
        message="Dump file loaded successfully.",
        payload={
            "runtime": runtime_payload,
            "data": {"relative_path": relative_path, "text": text},
        },
    )


def search_code(environment: EnvironmentConfig, query: str) -> ToolResult:
    """Substring-search ``query`` across every ``*.bsl`` file of the dump."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    try:
        dump_root = resolve_dump_path(environment)
        bsl_files = find_files_by_pattern(dump_root, "*.bsl")
        matches: list[dict] = []
        for bsl_path in bsl_files:
            text = read_text_file(bsl_path)
            hit_idx = text.find(query)
            if hit_idx == -1:
                continue
            matches.append(
                {
                    "relative_path": str(bsl_path.relative_to(dump_root)),
                    "matched": True,
                    "preview": _snippet(text, hit_idx, len(query)),
                }
            )
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="search_code",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    if matches:
        message = "Code search completed successfully."
    else:
        message = "Code search completed: no matches found."
    return ToolResult(
        ok=True,
        tool_name="search_code",
        message=message,
        payload={
            "runtime": runtime_payload,
            "data": {"query": query, "matches": matches},
        },
    )


def validate_query(environment: EnvironmentConfig, query: str) -> ToolResult:
    """Validate a 1C query syntactically against the live endpoint."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    relative_path = f"query/validate?text={urllib.parse.quote(query)}"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="validate_query",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="validate_query",
        message="Query validation completed successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def execute_read_query(
    environment: EnvironmentConfig,
    query: str,
    row_limit: int = 100,
) -> ToolResult:
    """Execute a read-only 1C query against the live endpoint.

    Applies a temporary keyword-level guardrail: a query whose upper-cased
    text contains any of ``INSERT``, ``UPDATE``, ``DELETE``, ``DROP``,
    ``ALTER``, ``CREATE`` or ``TRUNCATE`` is refused before touching the
    live endpoint. This is a minimal stop-gap until a full policy layer
    lands.
    """
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}

    upper = query.upper()
    if any(keyword in upper for keyword in _WRITE_KEYWORDS):
        return ToolResult(
            ok=False,
            tool_name="execute_read_query",
            message="Only read-only queries are allowed.",
            payload={"runtime": runtime_payload},
        )

    relative_path = (
        f"query/execute?text={urllib.parse.quote(query)}&limit={row_limit}"
    )
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="execute_read_query",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="execute_read_query",
        message="Read query executed successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def get_event_log(
    environment: EnvironmentConfig,
    period_start: str | None = None,
    period_end: str | None = None,
    level: str | None = None,
    user: str | None = None,
) -> ToolResult:
    """Read the event log from the live HTTP endpoint with optional filters."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    params: list[tuple[str, str]] = []
    if period_start is not None:
        params.append(("start", period_start))
    if period_end is not None:
        params.append(("end", period_end))
    if level is not None:
        params.append(("level", level))
    if user is not None:
        params.append(("user", user))
    if params:
        query_string = "&".join(
            f"{key}={urllib.parse.quote(value)}" for key, value in params
        )
        relative_path = f"event-log?{query_string}"
    else:
        relative_path = "event-log"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_event_log",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_event_log",
        message="Event log loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def get_object_structure(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Read a metadata object's structure (attributes, tabular parts, forms, modules)."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    relative_path = f"object/structure?name={urllib.parse.quote(object_name)}"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_object_structure",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_object_structure",
        message="Object structure loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def get_form_structure(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str | None = None,
) -> ToolResult:
    """Read a form's structure (attributes, elements, handler bindings)."""
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    relative_path = f"form/structure?object={urllib.parse.quote(object_name)}"
    if form_name is not None:
        relative_path = f"{relative_path}&form={urllib.parse.quote(form_name)}"
    try:
        data = fetch_json_from_environment(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="get_form_structure",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="get_form_structure",
        message="Form structure loaded successfully.",
        payload={"runtime": runtime_payload, "data": data},
    )


def check_runtime_health(environment: EnvironmentConfig) -> ToolResult:
    """Aggregate health of the environment into a single diagnostics snapshot."""
    context = build_runtime_context(environment)
    codes = list(context.health_codes)
    runtime_payload = {"health_codes": codes}
    checks = [
        {
            "check_name": result.check_name,
            "status": result.status,
            "message": result.message,
        }
        for result in context.health_results
    ]
    env_payload = {
        "name": environment.name,
        "base_id": environment.base_id,
        "http_base_url": environment.http_base_url,
        "dump_path": environment.dump_path,
    }
    data_payload = {"environment": env_payload, "checks": checks}
    if codes == ["ok"]:
        return ToolResult(
            ok=True,
            tool_name="check_runtime_health",
            message="Runtime health check completed successfully.",
            payload={"runtime": runtime_payload, "data": data_payload},
        )
    return ToolResult(
        ok=False,
        tool_name="check_runtime_health",
        message="Runtime health issues detected.",
        payload={"runtime": runtime_payload, "data": data_payload},
    )


def diagnose_connectivity_issue(environment: EnvironmentConfig) -> ToolResult:
    """Translate current health codes into a human-readable troubleshooting report."""
    context = build_runtime_context(environment)
    codes = list(context.health_codes)
    runtime_payload = {"health_codes": codes}
    if codes == ["ok"]:
        return ToolResult(
            ok=True,
            tool_name="diagnose_connectivity_issue",
            message="No connectivity issues detected.",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "problem_code": None,
                    "probable_cause": None,
                    "recommended_action": None,
                },
            },
        )
    report = diagnose_from_health(codes)
    return ToolResult(
        ok=False,
        tool_name="diagnose_connectivity_issue",
        message="Connectivity issue diagnosis completed.",
        payload={
            "runtime": runtime_payload,
            "data": {
                "problem_code": report.problem_code,
                "probable_cause": report.probable_cause,
                "recommended_action": report.recommended_action,
            },
        },
    )


def search_metadata(environment: EnvironmentConfig, query: str) -> ToolResult:
    """Substring-search ``query`` across every ``*.xml`` file of the dump.

    A file matches if the query is found in its file name or in its text
    content. ``preview`` is populated when the content matches; for
    name-only matches it is an empty string.
    """
    context = build_runtime_context(environment)
    runtime_payload = {"health_codes": list(context.health_codes)}
    try:
        dump_root = resolve_dump_path(environment)
        xml_files = find_files_by_pattern(dump_root, "*.xml")
        matches: list[dict] = []
        for xml_path in xml_files:
            file_name = xml_path.name
            name_hit = query in file_name
            text = read_text_file(xml_path)
            hit_idx = text.find(query)
            if not name_hit and hit_idx == -1:
                continue
            preview = _snippet(text, hit_idx, len(query)) if hit_idx != -1 else ""
            matches.append(
                {
                    "relative_path": str(xml_path.relative_to(dump_root)),
                    "file_name": file_name,
                    "preview": preview,
                }
            )
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="search_metadata",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )
    if matches:
        message = "Metadata search completed successfully."
    else:
        message = "Metadata search completed: no matches found."
    return ToolResult(
        ok=True,
        tool_name="search_metadata",
        message=message,
        payload={
            "runtime": runtime_payload,
            "data": {"query": query, "matches": matches},
        },
    )
