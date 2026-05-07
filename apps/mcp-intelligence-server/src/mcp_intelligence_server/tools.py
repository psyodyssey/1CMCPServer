"""Intelligence-server tool implementations.

Phase 4 / Step 4 — first wave of public intelligence-tools, group A
(dependency / reference analysis).
Phase 4 / Step 5 — diagnostics / troubleshooting tools, group C
(``analyze_runtime_issue``, ``analyze_event_log_patterns``,
``diagnose_broken_form_binding``,
``diagnose_missing_method_or_attribute``).
Phase 4 / Step 6 — impact / recommendation tools, groups B and D
(``estimate_change_impact``, ``find_affected_forms``,
``find_affected_modules``, ``suggest_safe_change_order``,
``suggest_fix_for_issue``, ``suggest_metadata_patch_plan``,
``summarize_configuration_risk``, ``prepare_intelligence_report``).

All tools here are strictly read-only: they never mutate state, never
call ``run_write_flow``, never emit audit records and never import
:mod:`onec_policy_engine`.

Each tool returns a :class:`ToolResult`. Exceptions from the runtime
helpers and cross-app calls (missing dump root, unreadable file,
unreachable endpoint) are caught and turned into ``ok=False`` results
or surfaced as findings — they do not propagate out of the tool layer.

Payloads consistently separate ``confirmed`` data (direct substring
or XML-structural evidence from a specific file; explicit health
codes; method existence verdicts from a readable module text) from
``presumed`` data (heuristic inferences such as probable root cause
or why something is missing). This keeps the intelligence contract
honest: callers can tell which items are facts vs. hints.

Failure style across the module is unified:

- ``ok=True`` — tool completed its analysis (findings may be empty).
- ``ok=False`` — tool could not complete its analysis (invalid input,
  an unavoidable dependency returned an error, dump/module inaccessible
  where required).
"""

from __future__ import annotations

import re
from collections import Counter

from mcp_common import PlatformError
from mcp_read_server.tools import (
    check_runtime_health as read_check_runtime_health,
    diagnose_connectivity_issue as read_diagnose_connectivity_issue,
    get_event_log as read_get_event_log,
    get_form_structure as read_get_form_structure,
)
from mcp_write_server.runtime.metadata_ops import module_contains_method
from onec_config import EnvironmentConfig

from .models import ToolResult
from .runtime import (
    IntelligenceRuntimeContext,
    ReferenceMatch,
    add_edge,
    add_node,
    build_runtime_context,
    empty_graph,
    find_references,
    list_bsl_files,
    list_xml_files,
    read_utf8_text,
)

# Known 1C metadata-type prefixes that precede a dotted object reference
# in either XML cards (<Type>, <Reference>, ...) or BSL code.  Both
# Cyrillic and English forms are accepted at MVP level — this is a
# substring heuristic, not a parser.
_KNOWN_PREFIXES: tuple[str, ...] = (
    "Справочник.",
    "Справочники.",
    "Документ.",
    "Документы.",
    "Перечисление.",
    "Перечисления.",
    "РегистрСведений.",
    "РегистрыСведений.",
    "РегистрНакопления.",
    "РегистрыНакопления.",
    "ПланВидовХарактеристик.",
    "ПланыВидовХарактеристик.",
    "ПланСчетов.",
    "ПланыСчетов.",
    "ОбщийМодуль.",
    "ОбщиеМодули.",
    "Отчёт.",
    "Отчёты.",
    "Обработка.",
    "Обработки.",
    "Catalog.",
    "Document.",
    "Enum.",
    "InformationRegister.",
    "AccumulationRegister.",
    "ChartOfCharacteristicTypes.",
    "ChartOfAccounts.",
    "CommonModule.",
    "Report.",
    "DataProcessor.",
)

_IDENTIFIER_CONT = r"[A-Za-zА-Яа-яЁё0-9_]+"


def ping() -> ToolResult:
    """Return a liveness marker for the intelligence server."""
    return ToolResult(
        ok=True,
        tool_name="ping",
        message="mcp-intelligence-server is alive.",
        payload={"status": "ok"},
    )


# ---------------------------------------------------------------------------
# Internal helpers (not public tools).
# ---------------------------------------------------------------------------


def _runtime_payload(context: IntelligenceRuntimeContext) -> dict:
    return {"health_codes": list(context.health_codes)}


def _match_to_dict(match: ReferenceMatch) -> dict:
    return {
        "relative_path": match.relative_path,
        "source": match.source,
        "line_number": match.line_number,
        "preview": match.preview,
    }


def _simple_name(object_name: str) -> str:
    """Return the tail of a dotted name (``Catalog.Foo`` → ``Foo``)."""
    if "." in object_name:
        return object_name.rsplit(".", 1)[1]
    return object_name


def _extract_prefixed_references(text: str) -> set[str]:
    """Find ``<KnownPrefix><Identifier>`` tokens in ``text``.

    Returns a set of full dotted names (e.g. ``"Справочник.Secondary"``).
    The heuristic is a substring/regex match — it does not parse XML or
    BSL. That is intentional for Phase 4 MVP.
    """
    hits: set[str] = set()
    for prefix in _KNOWN_PREFIXES:
        pattern = re.escape(prefix) + _IDENTIFIER_CONT
        for token in re.findall(pattern, text):
            hits.add(token)
    return hits


def _fail(
    tool_name: str,
    message: str,
    context: IntelligenceRuntimeContext | None = None,
) -> ToolResult:
    payload: dict = {}
    if context is not None:
        payload["runtime"] = _runtime_payload(context)
    return ToolResult(
        ok=False,
        tool_name=tool_name,
        message=message,
        payload=payload,
    )


# ---------------------------------------------------------------------------
# Public intelligence tools — group A.
# ---------------------------------------------------------------------------


def find_references_to_object(
    environment: EnvironmentConfig,
    object_name: str,
    max_matches: int | None = None,
) -> ToolResult:
    """Find substring references to ``object_name`` across dump XML and BSL.

    Read-only substring scan. Every match is a confirmed substring
    occurrence in a concrete file; interpretation of *why* the name
    appears (declaration vs. call vs. comment) is deliberately left to
    the caller / to more specialised tools.

    Returns ``ok=False`` if the dump root is unreachable or ``object_name``
    is empty. Returns ``ok=True`` with an empty ``confirmed_matches``
    list when the dump is reachable but the name does not occur — an
    empty-but-valid search is a valid outcome.
    """
    tool_name = "find_references_to_object"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    try:
        matches = find_references(
            context.dump_root, object_name, max_matches=max_matches
        )
    except (PlatformError, ValueError, OSError) as exc:
        return _fail(tool_name, f"Reference scan failed: {exc}", context)

    dump_xml_used = any(m.source == "xml" for m in matches)
    dump_bsl_used = any(m.source == "bsl" for m in matches)

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Found {len(matches)} reference(s) to '{object_name}'."
            if matches
            else f"No references to '{object_name}' found in dump."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "object_name": object_name,
            "total_matches": len(matches),
            "confirmed_matches": [_match_to_dict(m) for m in matches],
            "confirmed_sources": sorted(
                {m.relative_path for m in matches}
            ),
            "sources_used": {
                "dump_xml": dump_xml_used,
                "dump_bsl": dump_bsl_used,
            },
            "max_matches_applied": max_matches is not None
            and len(matches) == max_matches,
        },
    )


def find_module_method_usages(
    environment: EnvironmentConfig,
    method_name: str,
    max_matches: int | None = None,
) -> ToolResult:
    """Find occurrences of ``method_name`` in dump BSL sources.

    Scans ``*.bsl`` files only. Each confirmed substring match is
    additionally classified, on a *presumed* basis, as one of:

    - ``"declaration"`` — the line looks like a ``Процедура`` /
      ``Функция`` / ``Procedure`` / ``Function`` declaration of the
      method.
    - ``"usage"`` — any other substring occurrence of the name (could
      be a call site, a comment, or a string literal — the tool does
      not disambiguate further).

    The split is heuristic and is surfaced in the payload under
    ``presumed_declarations`` / ``presumed_usages``. Callers that only
    need raw ground truth look at ``confirmed_matches``.
    """
    tool_name = "find_module_method_usages"
    if not method_name:
        return _fail(tool_name, "method_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    try:
        matches = find_references(
            context.dump_root,
            method_name,
            extensions=("bsl",),
            max_matches=max_matches,
        )
    except (PlatformError, ValueError, OSError) as exc:
        return _fail(tool_name, f"Method usage scan failed: {exc}", context)

    decl_pattern = re.compile(
        r"^\s*(?:Процедура|Функция|Procedure|Function)\s+"
        + re.escape(method_name)
        + r"\s*\(",
    )
    declarations: list[dict] = []
    usages: list[dict] = []
    confirmed: list[dict] = []
    for match in matches:
        record = _match_to_dict(match)
        confirmed.append(record)
        if decl_pattern.search(match.preview):
            declarations.append(record)
        else:
            usages.append(record)

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Found {len(matches)} occurrence(s) of method '{method_name}'."
            if matches
            else f"No occurrences of method '{method_name}' found in BSL dump."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "method_name": method_name,
            "total_matches": len(matches),
            "confirmed_matches": confirmed,
            "presumed_declarations": declarations,
            "presumed_usages": usages,
            "sources_used": {"dump_bsl": bool(matches)},
            "max_matches_applied": max_matches is not None
            and len(matches) == max_matches,
        },
    )


def analyze_object_dependencies(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Enumerate objects/modules the given object references.

    Locates the object's own XML card (``*.xml`` whose stem equals the
    simple object name) and its own BSL module(s) (any ``*.bsl`` whose
    path contains the simple object name as a segment). Extracts known
    ``<MetadataType>.<Identifier>`` tokens from each.

    Split in the payload:

    - ``confirmed_dependencies`` — tokens extracted from the object's
      own XML card. XML structure carries high signal (a ``<Type>`` or
      ``<Reference>`` tag is a deliberate reference), so these are
      treated as confirmed.
    - ``presumed_dependencies`` — tokens extracted from the object's
      own BSL sources. BSL substrings may also appear in comments or
      string literals, so these are surfaced as heuristic inferences.

    Self-references (the object referencing itself) are excluded.
    Returns ``ok=False`` if the dump root is unreachable or the object
    cannot be located anywhere in the dump (no XML, no BSL).
    """
    tool_name = "analyze_object_dependencies"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    simple = _simple_name(object_name)

    try:
        all_xml = list_xml_files(context.dump_root)
        all_bsl = list_bsl_files(context.dump_root)
    except (PlatformError, OSError) as exc:
        return _fail(
            tool_name, f"Dump scan failed: {exc}", context
        )

    xml_cards = [p for p in all_xml if p.stem == simple]
    bsl_modules = [p for p in all_bsl if simple in p.parts]

    if not xml_cards and not bsl_modules:
        return _fail(
            tool_name,
            f"Object '{object_name}' not found in dump (no XML card, no BSL module).",
            context,
        )

    dump_root = context.dump_root
    confirmed_sources = sorted(
        p.relative_to(dump_root).as_posix() for p in xml_cards
    )
    presumed_sources = sorted(
        p.relative_to(dump_root).as_posix() for p in bsl_modules
    )

    self_tokens = {f"{prefix}{simple}" for prefix in _KNOWN_PREFIXES}

    graph = empty_graph()
    add_node(graph, object_name, kind="root")

    confirmed_deps: list[dict] = []
    for xml_path in xml_cards:
        rel = xml_path.relative_to(dump_root).as_posix()
        try:
            text = read_utf8_text(xml_path)
        except (PlatformError, OSError) as exc:
            return _fail(
                tool_name,
                f"Failed to read XML card {rel}: {exc}",
                context,
            )
        for token in sorted(_extract_prefixed_references(text)):
            if token in self_tokens:
                continue
            confirmed_deps.append({"name": token, "source": rel})
            add_node(graph, token, kind="dependency")
            add_edge(graph, object_name, token, kind="xml_reference")

    presumed_deps: list[dict] = []
    for bsl_path in bsl_modules:
        rel = bsl_path.relative_to(dump_root).as_posix()
        try:
            text = read_utf8_text(bsl_path)
        except (PlatformError, OSError) as exc:
            return _fail(
                tool_name,
                f"Failed to read BSL module {rel}: {exc}",
                context,
            )
        for token in sorted(_extract_prefixed_references(text)):
            if token in self_tokens:
                continue
            presumed_deps.append({"name": token, "source": rel})
            add_node(graph, token, kind="dependency")
            add_edge(graph, object_name, token, kind="bsl_reference")

    graph_payload = {
        "nodes": [
            {"name": n.name, "kind": n.kind} for n in graph.nodes
        ],
        "edges": [
            {"from": e.from_node, "to": e.to_node, "kind": e.kind}
            for e in graph.edges
        ],
        "adjacency": {k: list(v) for k, v in graph.adjacency.items()},
    }

    total_deps = len(confirmed_deps) + len(presumed_deps)
    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Analyzed '{object_name}': "
            f"{len(confirmed_deps)} confirmed, "
            f"{len(presumed_deps)} presumed dependencies."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "object_name": object_name,
            "simple_name": simple,
            "confirmed_sources": confirmed_sources,
            "presumed_sources": presumed_sources,
            "confirmed_dependencies": confirmed_deps,
            "presumed_dependencies": presumed_deps,
            "total_dependencies": total_deps,
            "graph": graph_payload,
        },
    )


# ---------------------------------------------------------------------------
# Public intelligence tools — group C (diagnostics / troubleshooting).
# ---------------------------------------------------------------------------


_HEALTH_CODE_HINTS: dict[str, str] = {
    "gateway_down": (
        "HTTP gateway is unreachable — verify the publication and "
        "Apache/IIS process; restart the site if it is dead."
    ),
    "dump_missing": (
        "Configured dump_path does not exist — re-run configuration "
        "dump or correct the environment config."
    ),
    "index_lock": (
        "Dump path exists but has no readable BSL files — index is "
        "empty or locked; re-generate the dump."
    ),
}


def analyze_runtime_issue(environment: EnvironmentConfig) -> ToolResult:
    """Aggregate read-server diagnostics into one intelligence answer.

    High-level aggregator on top of existing read-server diagnostic
    tools (``check_runtime_health``, ``diagnose_connectivity_issue``)
    and the intelligence runtime context. Never calls write-flow, never
    probes the environment in any new way — it only collects,
    classifies and explains what the read-side already knows.

    Payload splits:

    - ``confirmed_findings`` — explicit, code-backed issues
      (every non-``ok`` entry from ``runtime.health_codes`` becomes
      one finding with its own deterministic hint).
    - ``presumed_findings`` — the output of
      ``diagnose_connectivity_issue`` (a rule-based interpretation,
      hence presumed).
    - ``health_checks`` — the raw per-check snapshot from
      ``check_runtime_health``, so the caller can audit evidence.
    - ``recommended_checks`` — short next-step suggestions derived
      from the findings.

    ``ok=True`` whenever analysis completed (even when it reports
    several issues). ``ok=False`` only if the tool could not complete
    at all.
    """
    tool_name = "analyze_runtime_issue"
    if environment is None:
        return _fail(tool_name, "environment is missing.")

    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)

    try:
        health_result = read_check_runtime_health(environment)
        connectivity_result = read_diagnose_connectivity_issue(environment)
    except Exception as exc:  # noqa: BLE001 — never leak to caller
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=f"Underlying diagnostics tool raised: {exc}",
            payload={"runtime": runtime_payload},
        )

    health_checks = (
        health_result.payload.get("data", {}).get("checks", [])
        if isinstance(health_result.payload, dict)
        else []
    )

    confirmed_findings: list[dict] = []
    for code in context.health_codes:
        if code == "ok":
            continue
        confirmed_findings.append(
            {
                "code": code,
                "category": "health",
                "hint": _HEALTH_CODE_HINTS.get(
                    code, "See health_checks for evidence."
                ),
                "source": "read.check_runtime_health",
            }
        )

    presumed_findings: list[dict] = []
    conn_data = (
        connectivity_result.payload.get("data")
        if isinstance(connectivity_result.payload, dict)
        else None
    )
    if (
        isinstance(conn_data, dict)
        and conn_data.get("problem_code") is not None
    ):
        presumed_findings.append(
            {
                "problem_code": conn_data.get("problem_code"),
                "probable_cause": conn_data.get("probable_cause"),
                "recommended_action": conn_data.get("recommended_action"),
                "source": "read.diagnose_connectivity_issue",
            }
        )

    recommended_checks: list[str] = []
    for finding in confirmed_findings:
        code = finding["code"]
        if code == "gateway_down":
            recommended_checks.append(
                "Verify HTTP gateway availability via read.check_runtime_health."
            )
        elif code == "dump_missing":
            recommended_checks.append(
                "Re-run configuration dump; then re-check dump_path."
            )
        elif code == "index_lock":
            recommended_checks.append(
                "Re-generate dump to ensure BSL files are present and readable."
            )
    if not recommended_checks:
        recommended_checks.append(
            "No actionable recommendations: health snapshot is clean."
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Analyzed runtime: {len(confirmed_findings)} confirmed, "
            f"{len(presumed_findings)} presumed finding(s)."
        ),
        payload={
            "runtime": runtime_payload,
            "health_checks": health_checks,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": recommended_checks,
            "sources_used": [
                "read.check_runtime_health",
                "read.diagnose_connectivity_issue",
            ],
        },
    )


def _extract_event_entries(data: object) -> list[dict]:
    """Return a best-effort list-of-dicts of event-log entries.

    The live endpoint's shape is not strictly fixed at Phase 4 MVP.
    We accept a few reasonable shapes: ``{"entries": [...]}``,
    ``{"events": [...]}``, or just a raw list. Non-dict entries are
    silently skipped — surfacing weird shapes is the read-server's
    job, not ours.
    """
    if isinstance(data, list):
        candidates = data
    elif isinstance(data, dict):
        for key in ("entries", "events", "items", "records"):
            value = data.get(key)
            if isinstance(value, list):
                candidates = value
                break
        else:
            candidates = []
    else:
        candidates = []
    return [item for item in candidates if isinstance(item, dict)]


def _top_n(counter: Counter, n: int = 5) -> list[dict]:
    return [
        {"value": value, "count": count}
        for value, count in counter.most_common(n)
    ]


def analyze_event_log_patterns(
    environment: EnvironmentConfig,
    period_start: str | None = None,
    period_end: str | None = None,
    level: str | None = None,
    user: str | None = None,
) -> ToolResult:
    """Aggregate event-log entries into simple patterns.

    Delegates to read-server's ``get_event_log`` (which itself hits the
    live HTTP endpoint through :mod:`urllib`). Filters are passed
    through verbatim. If the read-server returned ``ok=False`` —
    because the endpoint is unreachable or the response is malformed —
    this tool fails-closed with the same message.

    On a successful fetch, entries are grouped by ``level``, ``user``
    and ``event`` using :class:`collections.Counter`. No ML, no
    clustering: counting repeated field values is already useful and
    honest. An empty log produces ``ok=True`` with empty findings.
    """
    tool_name = "analyze_event_log_patterns"
    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)
    filters = {
        "period_start": period_start,
        "period_end": period_end,
        "level": level,
        "user": user,
    }

    try:
        log_result = read_get_event_log(
            environment, period_start, period_end, level, user
        )
    except Exception as exc:  # noqa: BLE001
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=f"Underlying get_event_log raised: {exc}",
            payload={"runtime": runtime_payload, "filters": filters},
        )

    if not log_result.ok:
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=f"read.get_event_log failed: {log_result.message}",
            payload={
                "runtime": runtime_payload,
                "filters": filters,
                "sources_used": ["read.get_event_log"],
            },
        )

    data = (
        log_result.payload.get("data")
        if isinstance(log_result.payload, dict)
        else None
    )
    entries = _extract_event_entries(data)

    level_counts: Counter = Counter()
    user_counts: Counter = Counter()
    event_counts: Counter = Counter()
    error_samples: list[dict] = []
    for entry in entries:
        lvl = entry.get("level")
        usr = entry.get("user")
        evt = entry.get("event") or entry.get("message")
        if isinstance(lvl, str) and lvl:
            level_counts[lvl] += 1
        if isinstance(usr, str) and usr:
            user_counts[usr] += 1
        if isinstance(evt, str) and evt:
            event_counts[evt] += 1
        if isinstance(lvl, str) and lvl.lower() in ("error", "critical"):
            if len(error_samples) < 5:
                error_samples.append(
                    {
                        "level": lvl,
                        "user": usr,
                        "event": evt,
                        "timestamp": entry.get("timestamp"),
                    }
                )

    confirmed_findings = {
        "total_entries": len(entries),
        "top_levels": _top_n(level_counts),
        "top_users": _top_n(user_counts),
        "top_events": _top_n(event_counts),
        "error_samples": error_samples,
    }
    presumed_findings: list[dict] = []
    error_total = sum(
        count
        for value, count in level_counts.items()
        if value.lower() in ("error", "critical")
    )
    if error_total >= 2 and entries:
        presumed_findings.append(
            {
                "pattern": "error_spike",
                "error_entries": error_total,
                "probable_cause": (
                    "Multiple error-level entries in the selected window — "
                    "inspect the top event names and users for the dominant cause."
                ),
                "source": "analyze_event_log_patterns heuristic",
            }
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Analyzed {len(entries)} event-log entries "
            f"({error_total} error-level)."
        ),
        payload={
            "runtime": runtime_payload,
            "filters": filters,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": (
                [
                    "Cross-check the top error event against "
                    "diagnose_missing_method_or_attribute or "
                    "analyze_runtime_issue."
                ]
                if presumed_findings
                else []
            ),
            "sources_used": ["read.get_event_log"],
        },
    )


def diagnose_broken_form_binding(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str | None = None,
) -> ToolResult:
    """Diagnose typical breakages of a form's handler bindings.

    Fetches the form's structure via read-server's
    ``get_form_structure`` (live HTTP) and, when a module relative
    path is present in the returned data, resolves the module text
    from the dump. For each declared handler in the form, checks
    — via the pure read-only helper
    ``mcp_write_server.runtime.metadata_ops.module_contains_method``
    — whether the bound method is actually declared.

    Expected shape of the form payload (best-effort):
    ``{"elements": [...], "handlers": [{"event": str,
    "handler_method": str}], "module_relative_path": str}``.

    Confirmed findings: form absent, form has no elements / handlers,
    handler method missing in module. Presumed findings: probable
    root-cause narrative for each confirmed symptom.
    """
    tool_name = "diagnose_broken_form_binding"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)

    try:
        form_result = read_get_form_structure(environment, object_name, form_name)
    except Exception as exc:  # noqa: BLE001
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=f"Underlying get_form_structure raised: {exc}",
            payload={"runtime": runtime_payload},
        )

    if not form_result.ok:
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=f"read.get_form_structure failed: {form_result.message}",
            payload={
                "runtime": runtime_payload,
                "object_name": object_name,
                "form_name": form_name,
                "sources_used": ["read.get_form_structure"],
            },
        )

    form_data = (
        form_result.payload.get("data")
        if isinstance(form_result.payload, dict)
        else None
    )
    if not isinstance(form_data, dict):
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message="get_form_structure returned no usable data.",
            payload={
                "runtime": runtime_payload,
                "object_name": object_name,
                "form_name": form_name,
                "sources_used": ["read.get_form_structure"],
            },
        )

    elements = form_data.get("elements") or []
    handlers = form_data.get("handlers") or []
    module_relative_path = form_data.get("module_relative_path")

    confirmed_findings: list[dict] = []
    presumed_findings: list[dict] = []
    recommended_checks: list[str] = []
    sources_used: list[str] = ["read.get_form_structure"]

    if not elements:
        confirmed_findings.append(
            {
                "code": "form_has_no_elements",
                "form_name": form_data.get("form_name") or form_name,
                "source": "read.get_form_structure",
            }
        )
    if not handlers:
        confirmed_findings.append(
            {
                "code": "form_has_no_handlers",
                "form_name": form_data.get("form_name") or form_name,
                "source": "read.get_form_structure",
            }
        )

    module_text: str | None = None
    module_read_error: str | None = None
    if module_relative_path and handlers:
        module_path = context.dump_root / module_relative_path
        if not module_path.exists():
            module_read_error = (
                f"Module not found in dump: {module_relative_path}"
            )
            recommended_checks.append(
                "Re-generate the dump to include the form's module file."
            )
        else:
            try:
                module_text = read_utf8_text(module_path)
                sources_used.append("dump_scanner.read_utf8_text")
            except (PlatformError, OSError) as exc:
                module_read_error = (
                    f"Failed to read module {module_relative_path}: {exc}"
                )

    if module_text is not None:
        sources_used.append(
            "write_runtime.metadata_ops.module_contains_method"
        )
        for handler in handlers:
            if not isinstance(handler, dict):
                continue
            method_name = handler.get("handler_method") or handler.get("method")
            event = handler.get("event")
            if not method_name:
                continue
            if not module_contains_method(module_text, method_name):
                confirmed_findings.append(
                    {
                        "code": "handler_method_missing",
                        "event": event,
                        "method_name": method_name,
                        "module_relative_path": module_relative_path,
                        "source": "write_runtime.metadata_ops.module_contains_method",
                    }
                )
                presumed_findings.append(
                    {
                        "pattern": "handler_method_missing",
                        "event": event,
                        "method_name": method_name,
                        "probable_cause": (
                            f"Form handler '{event}' binds to method "
                            f"'{method_name}' that is not declared in "
                            f"{module_relative_path}. The method may have "
                            "been renamed, removed, or never added."
                        ),
                        "source": "diagnose_broken_form_binding heuristic",
                    }
                )
    elif module_read_error is not None:
        confirmed_findings.append(
            {
                "code": "module_not_readable",
                "module_relative_path": module_relative_path,
                "detail": module_read_error,
                "source": "dump_scanner.read_utf8_text",
            }
        )
        presumed_findings.append(
            {
                "pattern": "module_not_readable",
                "probable_cause": (
                    "Form references a module that cannot be read from the "
                    "current dump. Handler bindings cannot be verified."
                ),
                "source": "diagnose_broken_form_binding heuristic",
            }
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Diagnosed form binding for '{object_name}'"
            f"{' / ' + form_name if form_name else ''}: "
            f"{len(confirmed_findings)} confirmed, "
            f"{len(presumed_findings)} presumed finding(s)."
        ),
        payload={
            "runtime": runtime_payload,
            "object_name": object_name,
            "form_name": form_name,
            "module_relative_path": module_relative_path,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": recommended_checks,
            "sources_used": sources_used,
        },
    )


_ATTRIBUTE_TAG_PATTERNS: tuple[str, ...] = (
    r"<Attribute\s+[^>]*name\s*=\s*[\"']{name}[\"']",
    r"<Attribute\b[^>]*>\s*<Name>\s*{name}\s*</Name>",
)


def _xml_declares_attribute(xml_text: str, attribute_name: str) -> bool:
    name = re.escape(attribute_name)
    for template in _ATTRIBUTE_TAG_PATTERNS:
        pattern = re.compile(template.format(name=name))
        if pattern.search(xml_text):
            return True
    return False


def diagnose_missing_method_or_attribute(
    environment: EnvironmentConfig,
    *,
    object_name: str | None = None,
    module_relative_path: str | None = None,
    method_name: str | None = None,
    attribute_name: str | None = None,
) -> ToolResult:
    """Explain why a specific method or attribute is missing (or confirm it is present).

    Two modes, combinable:

    - **Method mode** — ``module_relative_path`` + ``method_name``
      must both be provided. The module text is read from the dump
      and scanned with
      ``mcp_write_server.runtime.metadata_ops.module_contains_method``.
    - **Attribute mode** — ``object_name`` + ``attribute_name`` must
      both be provided. The XML card for ``object_name`` is located
      under the dump root (stem match on the simple name) and
      scanned with a known-structure regex over common ``<Attribute>``
      patterns.

    At least one complete mode must be supplied; otherwise the tool
    returns ``ok=False`` with ``invalid_input``.

    Confirmed findings are binary verdicts anchored to a concrete file
    (``method_exists``, ``method_missing``, ``module_file_missing``,
    ``attribute_exists``, ``attribute_missing``, ``xml_card_missing``).
    Presumed findings supply a short probable-cause narrative for each
    *missing* verdict.
    """
    tool_name = "diagnose_missing_method_or_attribute"
    method_mode = bool(module_relative_path) and bool(method_name)
    attribute_mode = bool(object_name) and bool(attribute_name)
    if not (method_mode or attribute_mode):
        return _fail(
            tool_name,
            "Provide either (module_relative_path + method_name) "
            "or (object_name + attribute_name), or both.",
        )

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    runtime_payload = _runtime_payload(context)
    confirmed_findings: list[dict] = []
    presumed_findings: list[dict] = []
    sources_used: list[str] = []
    recommended_checks: list[str] = []

    if method_mode:
        module_path = context.dump_root / module_relative_path
        if not module_path.exists():
            confirmed_findings.append(
                {
                    "code": "module_file_missing",
                    "module_relative_path": module_relative_path,
                    "source": "dump_scanner",
                }
            )
            presumed_findings.append(
                {
                    "pattern": "module_file_missing",
                    "probable_cause": (
                        f"Module file '{module_relative_path}' is absent "
                        "from the current dump; the method cannot exist "
                        "without its module."
                    ),
                    "source": "diagnose_missing_method_or_attribute heuristic",
                }
            )
            recommended_checks.append(
                "Re-generate the dump or verify module_relative_path."
            )
        else:
            try:
                module_text = read_utf8_text(module_path)
                sources_used.append("dump_scanner.read_utf8_text")
            except (PlatformError, OSError) as exc:
                return _fail(
                    tool_name,
                    f"Failed to read module '{module_relative_path}': {exc}",
                    context,
                )
            sources_used.append(
                "write_runtime.metadata_ops.module_contains_method"
            )
            if module_contains_method(module_text, method_name):
                confirmed_findings.append(
                    {
                        "code": "method_exists",
                        "method_name": method_name,
                        "module_relative_path": module_relative_path,
                        "source": "write_runtime.metadata_ops.module_contains_method",
                    }
                )
            else:
                confirmed_findings.append(
                    {
                        "code": "method_missing",
                        "method_name": method_name,
                        "module_relative_path": module_relative_path,
                        "source": "write_runtime.metadata_ops.module_contains_method",
                    }
                )
                presumed_findings.append(
                    {
                        "pattern": "method_missing",
                        "probable_cause": (
                            f"Method '{method_name}' is not declared in "
                            f"{module_relative_path}; the module is "
                            "readable, so the method was never added or "
                            "has been renamed/removed."
                        ),
                        "source": "diagnose_missing_method_or_attribute heuristic",
                    }
                )

    if attribute_mode:
        simple = _simple_name(object_name)
        try:
            xml_cards = [
                p for p in list_xml_files(context.dump_root) if p.stem == simple
            ]
        except (PlatformError, OSError) as exc:
            return _fail(
                tool_name,
                f"Failed to scan dump for XML cards: {exc}",
                context,
            )
        if not xml_cards:
            confirmed_findings.append(
                {
                    "code": "xml_card_missing",
                    "object_name": object_name,
                    "source": "dump_scanner.list_xml_files",
                }
            )
            presumed_findings.append(
                {
                    "pattern": "xml_card_missing",
                    "probable_cause": (
                        f"No XML card found for '{object_name}' under "
                        f"{context.dump_root}; the object may not exist "
                        "in this dump."
                    ),
                    "source": "diagnose_missing_method_or_attribute heuristic",
                }
            )
            recommended_checks.append(
                "Check object_name spelling and re-generate the dump."
            )
        else:
            sources_used.append("dump_scanner.list_xml_files")
            xml_card = xml_cards[0]
            rel = xml_card.relative_to(context.dump_root).as_posix()
            try:
                xml_text = read_utf8_text(xml_card)
            except (PlatformError, OSError) as exc:
                return _fail(
                    tool_name,
                    f"Failed to read XML card '{rel}': {exc}",
                    context,
                )
            sources_used.append(f"dump_xml:{rel}")
            if _xml_declares_attribute(xml_text, attribute_name):
                confirmed_findings.append(
                    {
                        "code": "attribute_exists",
                        "object_name": object_name,
                        "attribute_name": attribute_name,
                        "xml_card": rel,
                        "source": "dump_xml",
                    }
                )
            else:
                confirmed_findings.append(
                    {
                        "code": "attribute_missing",
                        "object_name": object_name,
                        "attribute_name": attribute_name,
                        "xml_card": rel,
                        "source": "dump_xml",
                    }
                )
                presumed_findings.append(
                    {
                        "pattern": "attribute_missing",
                        "probable_cause": (
                            f"Attribute '{attribute_name}' is not declared "
                            f"in the XML card {rel}; the attribute may have "
                            "been planned but never created, or the dump is "
                            "stale."
                        ),
                        "source": "diagnose_missing_method_or_attribute heuristic",
                    }
                )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Diagnosed: {len(confirmed_findings)} confirmed, "
            f"{len(presumed_findings)} presumed finding(s)."
        ),
        payload={
            "runtime": runtime_payload,
            "inputs": {
                "object_name": object_name,
                "module_relative_path": module_relative_path,
                "method_name": method_name,
                "attribute_name": attribute_name,
            },
            "mode": {
                "method_mode": method_mode,
                "attribute_mode": attribute_mode,
            },
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": recommended_checks,
            "sources_used": sources_used,
        },
    )


# ---------------------------------------------------------------------------
# Public intelligence tools — group B (impact / affected scope).
# ---------------------------------------------------------------------------


def _impact_level(reference_count: int) -> str:
    if reference_count > 20:
        return "high"
    if reference_count > 5:
        return "medium"
    if reference_count > 0:
        return "low"
    return "none"


def _is_form_path(relative_path: str, source: str) -> bool:
    """Heuristic: does this dump path look like a form artefact?

    Very intentionally a rough check. 1C's dump layout usually places
    forms under a ``Forms/`` segment or names form-related files with
    ``Form`` in the stem. Both Cyrillic and Latin conventions exist in
    the wild, so we accept either.
    """
    low = relative_path.lower()
    parts = relative_path.replace("\\", "/").split("/")
    if any(part.lower() == "forms" for part in parts):
        return True
    if "/forms/" in "/" + low + "/":
        return True
    stem = parts[-1].rsplit(".", 1)[0]
    if "form" in stem.lower() or "форма" in stem.lower():
        return True
    return False


def estimate_change_impact(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Compact estimate of how far a change to ``object_name`` could reach.

    Composes intelligence runtime + substring reference scan:

    - counts total substring matches and splits them between ``*.xml``
      and ``*.bsl``;
    - locates the object's own XML card and BSL modules (same heuristic
      as :func:`analyze_object_dependencies`);
    - derives an ``impact_level`` band — ``none`` / ``low`` / ``medium`` /
      ``high`` — from the total reference count. The band is a
      deterministic threshold, not a judgment call.

    The reference count is a confirmed fact (substring hit in a concrete
    file, line number known). The impact band is a presumed inference
    (substring ≠ real behavioural usage, and the thresholds are arbitrary
    MVP cutoffs). The payload surfaces both separately.
    """
    tool_name = "estimate_change_impact"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    runtime_payload = _runtime_payload(context)
    dump_root = context.dump_root

    try:
        matches = find_references(dump_root, object_name)
        all_xml = list_xml_files(dump_root)
        all_bsl = list_bsl_files(dump_root)
    except (PlatformError, ValueError, OSError) as exc:
        return _fail(tool_name, f"Impact scan failed: {exc}", context)

    simple = _simple_name(object_name)
    own_xml = [p for p in all_xml if p.stem == simple]
    own_bsl = [p for p in all_bsl if simple in p.parts]

    xml_hits = [m for m in matches if m.source == "xml"]
    bsl_hits = [m for m in matches if m.source == "bsl"]
    sources_referenced = sorted({m.relative_path for m in matches})
    level = _impact_level(len(matches))

    confirmed_findings = {
        "reference_count": len(matches),
        "xml_references": len(xml_hits),
        "bsl_references": len(bsl_hits),
        "own_xml_cards": [
            p.relative_to(dump_root).as_posix() for p in own_xml
        ],
        "own_bsl_modules": [
            p.relative_to(dump_root).as_posix() for p in own_bsl
        ],
        "simple_name": simple,
        "referenced_paths": sources_referenced,
    }
    presumed_findings = [
        {
            "pattern": "impact_estimate",
            "impact_level": level,
            "probable_cause": (
                f"Substring-based reference count = {len(matches)}; "
                "band is a deterministic threshold, real behavioural "
                "impact may differ."
            ),
            "source": "estimate_change_impact heuristic",
        }
    ]
    if bsl_hits:
        presumed_findings.append(
            {
                "pattern": "module_impact_possible",
                "probable_cause": (
                    f"{len(bsl_hits)} BSL reference(s) suggest code "
                    "paths may depend on the object."
                ),
                "source": "estimate_change_impact heuristic",
            }
        )
    if any(_is_form_path(rel, "xml") or _is_form_path(rel, "bsl") for rel in sources_referenced):
        presumed_findings.append(
            {
                "pattern": "form_impact_possible",
                "probable_cause": (
                    "One or more references live under a form-like path; "
                    "attached forms could need re-verification."
                ),
                "source": "estimate_change_impact heuristic",
            }
        )

    recommended_checks: list[str] = []
    if level in ("medium", "high"):
        recommended_checks.append(
            "Review affected forms and modules before applying the change."
        )
    if bsl_hits:
        recommended_checks.append(
            "Scan BSL modules via find_module_method_usages for the "
            "relevant method names."
        )
    if not matches:
        recommended_checks.append(
            "No references found: re-check object_name spelling or "
            "confirm the object exists in this dump."
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Impact estimate for '{object_name}': "
            f"{len(matches)} reference(s), level={level}."
        ),
        payload={
            "runtime": runtime_payload,
            "object_name": object_name,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": recommended_checks,
            "suggested_tools": [
                "find_references_to_object",
                "analyze_object_dependencies",
                "find_affected_forms",
                "find_affected_modules",
            ],
            "sources_used": [
                "runtime.reference_finder.find_references",
                "runtime.dump_scanner.list_xml_files",
                "runtime.dump_scanner.list_bsl_files",
            ],
        },
    )


def find_affected_forms(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """List dump paths that look like forms referencing ``object_name``.

    Uses :func:`find_references` and partitions the matches by a path
    heuristic:

    - **confirmed_findings** — matches whose relative path contains a
      ``Forms/`` segment or whose file stem contains ``"form"`` /
      ``"форма"``. Those are structurally form artefacts in the dump.
    - **presumed_findings** — everything else. The reference exists in
      a file that is not obviously a form but might still describe
      form-related behaviour; surfaced as weak signals, not facts.

    No live HTTP is used. The heuristic is intentionally rough (MVP
    substring / path inspection) — a real form-binding query belongs to
    :func:`diagnose_broken_form_binding`.
    """
    tool_name = "find_affected_forms"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    try:
        matches = find_references(context.dump_root, object_name)
    except (PlatformError, ValueError, OSError) as exc:
        return _fail(tool_name, f"Form scan failed: {exc}", context)

    confirmed: list[dict] = []
    presumed: list[dict] = []
    for match in matches:
        record = _match_to_dict(match)
        if _is_form_path(match.relative_path, match.source):
            confirmed.append(record)
        else:
            presumed.append(
                {
                    "pattern": "weak_form_signal",
                    **record,
                    "probable_cause": (
                        "Object referenced in a non-form artefact; could "
                        "still describe form behaviour (e.g. metadata XML "
                        "that links forms)."
                    ),
                }
            )

    recommended_checks: list[str] = []
    if confirmed:
        recommended_checks.append(
            "Call diagnose_broken_form_binding for each confirmed form path."
        )
    if not confirmed and presumed:
        recommended_checks.append(
            "No structural form paths hit; re-check by reading the "
            "suspicious files directly."
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Affected forms for '{object_name}': "
            f"{len(confirmed)} confirmed, {len(presumed)} presumed."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "object_name": object_name,
            "confirmed_findings": confirmed,
            "presumed_findings": presumed,
            "recommended_checks": recommended_checks,
            "suggested_tools": [
                "diagnose_broken_form_binding",
                "find_references_to_object",
            ],
            "sources_used": [
                "runtime.reference_finder.find_references",
            ],
        },
    )


def find_affected_modules(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """List BSL modules and metadata files referencing ``object_name``.

    Confirmed = ``*.bsl`` matches (every ``.bsl`` file is by definition a
    module). Presumed = ``*.xml`` matches — XML may describe
    module-level linkage indirectly (``<CommonModule>`` tags, handler
    bindings, ...), but a substring hit there is not a code-level fact.

    The payload separates the two buckets and groups confirmed matches
    by module relative path so callers can see per-module hit counts
    at a glance.
    """
    tool_name = "find_affected_modules"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    try:
        matches = find_references(context.dump_root, object_name)
    except (PlatformError, ValueError, OSError) as exc:
        return _fail(tool_name, f"Module scan failed: {exc}", context)

    confirmed: list[dict] = []
    per_module: Counter = Counter()
    presumed: list[dict] = []
    for match in matches:
        record = _match_to_dict(match)
        if match.source == "bsl":
            confirmed.append(record)
            per_module[match.relative_path] += 1
        else:
            presumed.append(
                {
                    "pattern": "module_signal_via_xml",
                    **record,
                    "probable_cause": (
                        "Object referenced in XML metadata; a module "
                        "linkage (e.g. <CommonModule>, form-binding) "
                        "may exist but is not proven by this match alone."
                    ),
                }
            )

    module_summary = [
        {"module_relative_path": path, "match_count": count}
        for path, count in per_module.most_common()
    ]

    recommended_checks: list[str] = []
    if module_summary:
        recommended_checks.append(
            "Run find_module_method_usages per module to inspect actual calls."
        )
    if not confirmed and presumed:
        recommended_checks.append(
            "Only XML signals found; open these files manually before planning code changes."
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Affected modules for '{object_name}': "
            f"{len(module_summary)} distinct module(s), "
            f"{len(confirmed)} BSL match(es), {len(presumed)} XML signal(s)."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "object_name": object_name,
            "confirmed_findings": confirmed,
            "module_summary": module_summary,
            "presumed_findings": presumed,
            "recommended_checks": recommended_checks,
            "suggested_tools": [
                "find_module_method_usages",
                "find_references_to_object",
            ],
            "sources_used": [
                "runtime.reference_finder.find_references",
            ],
        },
    )


def suggest_safe_change_order(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Recommend a safe ordered sequence of steps around changing an object.

    Pure recommendation: the tool itself executes nothing, applies
    nothing, and has no side effects. It reuses the already-computed
    dependency picture (``analyze_object_dependencies``) when available;
    when the object is not in the dump the sequence is still emitted,
    clearly annotated as generic.

    The suggested sequence refers **only** to real public tools that
    already exist — read-server tools, write-server Phase 2/3 tools, and
    intelligence tools Step 4/5. No invented tool names.
    """
    tool_name = "suggest_safe_change_order"
    if not object_name:
        return _fail(tool_name, "object_name is empty.")

    context = build_runtime_context(environment)
    if not context.dump_root.exists():
        return _fail(
            tool_name,
            f"Dump root does not exist: {context.dump_root}.",
            context,
        )

    # Delegate to the already-registered public tool for dependency facts.
    deps_result = analyze_object_dependencies(environment, object_name)
    deps_payload = (
        deps_result.payload
        if isinstance(deps_result.payload, dict)
        else {}
    )
    confirmed_deps = deps_payload.get("confirmed_dependencies", []) or []
    presumed_deps = deps_payload.get("presumed_dependencies", []) or []

    impact_result = estimate_change_impact(environment, object_name)
    impact_payload = (
        impact_result.payload
        if isinstance(impact_result.payload, dict)
        else {}
    )
    impact_level = "unknown"
    for item in impact_payload.get("presumed_findings", []) or []:
        if isinstance(item, dict) and item.get("pattern") == "impact_estimate":
            impact_level = item.get("impact_level", "unknown")
            break

    object_found = deps_result.ok

    recommended_sequence: list[dict] = [
        {
            "step": 1,
            "description": (
                "Read current object structure to confirm baseline "
                "(attributes, forms, modules)."
            ),
            "suggested_tools": ["get_object_structure"],
        },
        {
            "step": 2,
            "description": (
                "Run reference / dependency analysis to understand "
                "downstream impact."
            ),
            "suggested_tools": [
                "analyze_object_dependencies",
                "find_references_to_object",
                "estimate_change_impact",
                "find_affected_forms",
                "find_affected_modules",
            ],
        },
        {
            "step": 3,
            "description": (
                "Take backup and dump snapshots through write-server "
                "preflight helpers."
            ),
            "suggested_write_tools": [
                "check_write_preconditions",
                "create_backup_snapshot",
                "create_dump_snapshot",
            ],
        },
        {
            "step": 4,
            "description": (
                "Apply metadata-level change through an appropriate "
                "Phase 3 write-tool (caller picks the specific one)."
            ),
            "suggested_write_tools": [
                "create_catalog",
                "add_catalog_attribute",
                "add_document_attribute",
                "create_managed_form",
                "add_form_element",
                "append_module_method",
                "replace_module_method_body",
            ],
        },
        {
            "step": 5,
            "description": (
                "Verify the change landed via read-server and write-server "
                "verification tools."
            ),
            "suggested_tools": ["get_object_structure", "get_form_structure"],
            "suggested_write_tools": [
                "verify_metadata_change",
                "verify_attribute_exists",
                "verify_module_contains",
                "verify_object_exists",
                "diff_dump_fragment",
            ],
        },
        {
            "step": 6,
            "description": (
                "On failure, retrieve audit trail and rollback hint."
            ),
            "suggested_write_tools": [
                "describe_last_write_operation",
                "prepare_rollback_hint",
            ],
        },
    ]

    confirmed_findings = {
        "object_found_in_dump": object_found,
        "confirmed_dependency_count": len(confirmed_deps),
        "presumed_dependency_count": len(presumed_deps),
        "impact_level": impact_level,
    }
    presumed_findings: list[dict] = []
    if object_found and (confirmed_deps or presumed_deps):
        presumed_findings.append(
            {
                "pattern": "cascade_risk",
                "probable_cause": (
                    "Object references other metadata; changing it may "
                    "cascade to dependents."
                ),
                "source": "suggest_safe_change_order heuristic",
            }
        )
    if not object_found:
        presumed_findings.append(
            {
                "pattern": "object_not_in_dump",
                "probable_cause": (
                    "Object not located in the current dump; sequence is "
                    "emitted as a generic template."
                ),
                "source": "suggest_safe_change_order heuristic",
            }
        )
    if impact_level == "high":
        presumed_findings.append(
            {
                "pattern": "high_blast_radius",
                "probable_cause": (
                    "Reference count is high; consider splitting the "
                    "change into smaller steps."
                ),
                "source": "suggest_safe_change_order heuristic",
            }
        )

    recommended_checks = [
        "Do not skip step 3 (snapshots) — write-flow refuses mutating operations without them.",
        "Re-run verification tools after every mutating step, not only at the end.",
    ]

    suggested_tools = sorted(
        {
            tool
            for step in recommended_sequence
            for tool in step.get("suggested_tools", [])
        }
    )
    suggested_write_tools = sorted(
        {
            tool
            for step in recommended_sequence
            for tool in step.get("suggested_write_tools", [])
        }
    )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Safe change order for '{object_name}': "
            f"{len(recommended_sequence)} step(s), impact={impact_level}."
        ),
        payload={
            "runtime": _runtime_payload(context),
            "object_name": object_name,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_sequence": recommended_sequence,
            "recommended_checks": recommended_checks,
            "suggested_tools": suggested_tools,
            "suggested_write_tools": suggested_write_tools,
            "sources_used": [
                "intelligence.analyze_object_dependencies",
                "intelligence.estimate_change_impact",
            ],
        },
    )


# ---------------------------------------------------------------------------
# Public intelligence tools — group D (recommendations / planning).
# ---------------------------------------------------------------------------


# Rule-based mapping from a known issue_code to structured guidance.
# ``suggested_write_tools`` lists must only contain names of public
# write-server tools that actually exist in ``REGISTERED_TOOLS``.
_ISSUE_FIX_RULES: dict[str, dict] = {
    "gateway_down": {
        "probable_cause": "HTTP gateway of the infobase is unreachable.",
        "steps": [
            "Check that the 1C publication is running.",
            "Verify the web-server (Apache/IIS) process.",
            "Re-run read.check_runtime_health after restart.",
        ],
        "suggested_tools": [
            "check_runtime_health",
            "diagnose_connectivity_issue",
            "analyze_runtime_issue",
        ],
        "suggested_write_tools": [],
    },
    "dump_missing": {
        "probable_cause": "Configured dump_path does not exist on disk.",
        "steps": [
            "Verify environment.dump_path is correct.",
            "Re-generate the dump manually.",
            "Re-run analyze_runtime_issue.",
        ],
        "suggested_tools": [
            "analyze_runtime_issue",
            "summarize_configuration_risk",
        ],
        "suggested_write_tools": ["create_dump_snapshot"],
    },
    "index_lock": {
        "probable_cause": (
            "Dump directory exists but contains no readable BSL files; "
            "the dump may be empty or locked."
        ),
        "steps": [
            "Re-generate the dump.",
            "Check filesystem permissions on dump_path.",
        ],
        "suggested_tools": [
            "analyze_runtime_issue",
        ],
        "suggested_write_tools": ["create_dump_snapshot"],
    },
    "form_has_no_elements": {
        "probable_cause": (
            "Form exists but carries no UI elements; the form may have "
            "been created but never populated."
        ),
        "steps": [
            "Review the form in the configurator / dump XML.",
            "Add required elements via add_form_element.",
        ],
        "suggested_tools": ["diagnose_broken_form_binding", "get_form_structure"],
        "suggested_write_tools": ["add_form_element"],
    },
    "form_has_no_handlers": {
        "probable_cause": (
            "Form has no handler bindings; either not needed or the "
            "bindings were never wired up."
        ),
        "steps": [
            "Confirm whether the form is expected to have handlers.",
            "If yes — add the bindings in the form definition and "
            "declare corresponding methods via append_module_method.",
        ],
        "suggested_tools": ["diagnose_broken_form_binding", "get_form_structure"],
        "suggested_write_tools": ["append_module_method"],
    },
    "handler_method_missing": {
        "probable_cause": (
            "Form handler references a method that is not declared in "
            "the bound module."
        ),
        "steps": [
            "Decide whether the form binding is stale (remove it) or "
            "the method must be added.",
            "If adding: append the method to the module.",
            "Re-verify.",
        ],
        "suggested_tools": [
            "diagnose_broken_form_binding",
            "diagnose_missing_method_or_attribute",
            "find_module_method_usages",
        ],
        "suggested_write_tools": [
            "append_module_method",
            "verify_module_contains",
        ],
    },
    "method_missing": {
        "probable_cause": (
            "Method is not declared in the referenced module, but the "
            "module file itself is readable."
        ),
        "steps": [
            "Add the method via append_module_method.",
            "Verify via verify_module_contains.",
        ],
        "suggested_tools": [
            "diagnose_missing_method_or_attribute",
            "find_module_method_usages",
        ],
        "suggested_write_tools": [
            "append_module_method",
            "verify_module_contains",
        ],
    },
    "module_file_missing": {
        "probable_cause": (
            "Module file is absent from the dump. No method can exist "
            "without its module."
        ),
        "steps": [
            "Confirm the module_relative_path.",
            "If the module is needed — create the surrounding object "
            "or common module and re-generate the dump.",
        ],
        "suggested_tools": [
            "diagnose_missing_method_or_attribute",
            "summarize_configuration_risk",
        ],
        "suggested_write_tools": ["create_common_module"],
    },
    "attribute_missing": {
        "probable_cause": (
            "Attribute is not declared in the object's XML card."
        ),
        "steps": [
            "Pick the correct write-tool (add_catalog_attribute for "
            "catalogs, add_document_attribute for documents).",
            "Verify via verify_attribute_exists.",
        ],
        "suggested_tools": ["diagnose_missing_method_or_attribute"],
        "suggested_write_tools": [
            "add_catalog_attribute",
            "add_document_attribute",
            "verify_attribute_exists",
        ],
    },
    "xml_card_missing": {
        "probable_cause": (
            "No XML card is present for the object under the current "
            "dump root."
        ),
        "steps": [
            "Confirm object_name spelling and dump freshness.",
            "If the object must exist — create it (e.g. create_catalog) "
            "and re-generate the dump.",
        ],
        "suggested_tools": [
            "analyze_object_dependencies",
            "summarize_configuration_risk",
        ],
        "suggested_write_tools": [
            "create_catalog",
            "create_common_module",
            "verify_object_exists",
        ],
    },
    "error_spike": {
        "probable_cause": (
            "Multiple error/critical entries in the event log indicate "
            "a repeating failure; inspect the dominant event."
        ),
        "steps": [
            "Re-run analyze_event_log_patterns and inspect top_events.",
            "Trace the top error toward a specific object/method.",
            "Use diagnose_* tools to classify the root cause.",
        ],
        "suggested_tools": [
            "analyze_event_log_patterns",
            "diagnose_missing_method_or_attribute",
            "diagnose_broken_form_binding",
            "analyze_runtime_issue",
        ],
        "suggested_write_tools": [],
    },
}


def suggest_fix_for_issue(
    environment: EnvironmentConfig,
    issue_code: str,
    context_data: dict | None = None,
) -> ToolResult:
    """Map a known ``issue_code`` to a structured fix recommendation.

    Purely rule-based — no ML, no probing, no live calls. Looks
    ``issue_code`` up in a fixed table of recipes. Each recipe yields
    a probable cause (presumed), a short ordered list of steps
    (recommended_checks), and a set of ``suggested_tools`` /
    ``suggested_write_tools`` that reference existing public tools only.

    ``context_data`` is passed through verbatim in the payload (so the
    caller can correlate the response to the issue they came from) but
    is not interpreted — the MVP does not parametrise recipes by
    context.

    Unknown ``issue_code`` — fail-closed with ``ok=False`` and a
    message listing the known codes.
    """
    tool_name = "suggest_fix_for_issue"
    if not issue_code:
        return _fail(tool_name, "issue_code is empty.")

    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)
    rule = _ISSUE_FIX_RULES.get(issue_code)
    if rule is None:
        return ToolResult(
            ok=False,
            tool_name=tool_name,
            message=(
                f"Unknown issue_code '{issue_code}'. "
                f"Known codes: {sorted(_ISSUE_FIX_RULES)}."
            ),
            payload={
                "runtime": runtime_payload,
                "issue_code": issue_code,
                "known_issue_codes": sorted(_ISSUE_FIX_RULES),
            },
        )

    confirmed_findings = {
        "issue_code": issue_code,
        "context_data": context_data or {},
    }
    presumed_findings = [
        {
            "pattern": "issue_fix_recipe",
            "probable_cause": rule["probable_cause"],
            "source": "suggest_fix_for_issue rule table",
        }
    ]

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Fix recipe for '{issue_code}': "
            f"{len(rule['steps'])} step(s), "
            f"{len(rule['suggested_write_tools'])} write-tool(s) suggested."
        ),
        payload={
            "runtime": runtime_payload,
            "issue_code": issue_code,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": list(rule["steps"]),
            "suggested_tools": list(rule["suggested_tools"]),
            "suggested_write_tools": list(rule["suggested_write_tools"]),
            "sources_used": ["suggest_fix_for_issue rule table"],
        },
    )


# ``target_kind`` → ordered recipe of write-tools. Each string in
# ``suggested_write_tools`` must be a real, registered public write-
# server tool.  Kinds that current Phase 2/3 write-server cannot
# address are listed with an empty recipe + a honest note.
_PATCH_PLAN_RECIPES: dict[str, dict] = {
    "catalog": {
        "description": "Create a new catalog object.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "create_catalog",
            "update_database_configuration",
            "verify_object_exists",
        ],
    },
    "common_module": {
        "description": "Create a new common module.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "create_common_module",
            "update_database_configuration",
            "verify_module_contains",
        ],
    },
    "catalog_attribute": {
        "description": "Add an attribute to an existing catalog.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "add_catalog_attribute",
            "update_database_configuration",
            "verify_attribute_exists",
        ],
    },
    "document_attribute": {
        "description": "Add an attribute to an existing document.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "add_document_attribute",
            "update_database_configuration",
            "verify_attribute_exists",
        ],
    },
    "managed_form": {
        "description": "Create a managed form on an existing object.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "create_managed_form",
            "verify_metadata_change",
        ],
    },
    "form_element": {
        "description": "Add an element to an existing managed form.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "add_form_element",
            "verify_metadata_change",
        ],
    },
    "module_method": {
        "description": "Append a method to an existing module.",
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "append_module_method",
            "verify_module_contains",
        ],
    },
    "module_method_body": {
        "description": (
            "Replace the body of an existing module method "
            "(requires confirm_replace=True on the write call)."
        ),
        "suggested_write_tools": [
            "check_write_preconditions",
            "create_backup_snapshot",
            "create_dump_snapshot",
            "replace_module_method_body",
            "verify_metadata_change",
        ],
    },
}


# Known targets that Phase 2/3 public write-server does NOT cover. The
# plan tool honestly surfaces these as unsupported instead of inventing
# nonexistent tools.
_PATCH_PLAN_UNSUPPORTED: dict[str, str] = {
    "document": (
        "No create_document public write-tool exists in Phase 2/3; "
        "only add_document_attribute is available."
    ),
    "information_register": (
        "No create_information_register public write-tool exists in "
        "Phase 2/3."
    ),
    "role": "No create_role public write-tool exists in Phase 2/3.",
    "report": "No create_report public write-tool exists in Phase 2/3.",
    "data_processor": (
        "No create_data_processor public write-tool exists in Phase 2/3."
    ),
}


_DELETION_KEYWORDS: tuple[str, ...] = (
    "delete", "remove", "drop", "удалить", "удалять", "убрать",
)


def suggest_metadata_patch_plan(
    environment: EnvironmentConfig,
    target_kind: str,
    target_name: str,
    change_goal: str,
) -> ToolResult:
    """Emit a safe, ordered plan of **existing** write-tools to reach a goal.

    Inputs:

    - ``target_kind`` — one of the kinds keyed in
      :data:`_PATCH_PLAN_RECIPES` (``catalog``, ``common_module``,
      ``catalog_attribute``, ``document_attribute``, ``managed_form``,
      ``form_element``, ``module_method``, ``module_method_body``).
    - ``target_name`` — the object or module identifier.
    - ``change_goal`` — freeform text describing intent (e.g. "create",
      "add attribute", "rename"). Inspected only for deletion
      keywords; otherwise surfaced verbatim.

    The plan lists only tools that already exist in Phase 2/3's
    write-server. If the requested kind is known-but-unsupported (e.g.
    ``document`` which has no ``create_document`` tool), or if the goal
    contains a deletion keyword (no ``delete_*`` tools exist yet), the
    tool returns ``ok=True`` with an honest ``presumed_findings`` entry
    saying so and an empty ``suggested_write_tools`` list.

    Never emits invented tool names.
    """
    tool_name = "suggest_metadata_patch_plan"
    if not target_kind:
        return _fail(tool_name, "target_kind is empty.")
    if not target_name:
        return _fail(tool_name, "target_name is empty.")
    if change_goal is None:
        return _fail(tool_name, "change_goal is None.")

    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)
    kind_normalised = target_kind.strip().lower().replace("-", "_")
    goal_lower = change_goal.lower()
    deletion_request = any(k in goal_lower for k in _DELETION_KEYWORDS)

    recipe = _PATCH_PLAN_RECIPES.get(kind_normalised)
    unsupported_note = _PATCH_PLAN_UNSUPPORTED.get(kind_normalised)

    confirmed_findings: dict = {
        "target_kind": target_kind,
        "normalised_kind": kind_normalised,
        "target_name": target_name,
        "change_goal": change_goal,
        "supported": recipe is not None and not deletion_request,
    }
    presumed_findings: list[dict] = []
    recommended_sequence: list[dict] = []
    suggested_write_tools: list[str] = []
    suggested_tools: list[str] = [
        "analyze_object_dependencies",
        "estimate_change_impact",
        "suggest_safe_change_order",
    ]

    if deletion_request:
        presumed_findings.append(
            {
                "pattern": "deletion_not_supported",
                "probable_cause": (
                    "change_goal requests a deletion, but current Phase 2/3 "
                    "public write-server exposes no delete_* tools."
                ),
                "source": "suggest_metadata_patch_plan rule",
            }
        )
    elif unsupported_note is not None:
        presumed_findings.append(
            {
                "pattern": "kind_unsupported",
                "probable_cause": unsupported_note,
                "source": "suggest_metadata_patch_plan rule",
            }
        )
    elif recipe is None:
        presumed_findings.append(
            {
                "pattern": "unknown_kind",
                "probable_cause": (
                    f"target_kind '{target_kind}' is not among the known "
                    f"kinds: {sorted(_PATCH_PLAN_RECIPES)}."
                ),
                "source": "suggest_metadata_patch_plan rule",
            }
        )
    else:
        suggested_write_tools = list(recipe["suggested_write_tools"])
        for idx, tool in enumerate(suggested_write_tools, start=1):
            recommended_sequence.append(
                {
                    "step": idx,
                    "write_tool": tool,
                    "description": _step_description(tool),
                }
            )

    message_head = (
        f"Patch plan for {kind_normalised} '{target_name}'"
    )
    if recommended_sequence:
        message = (
            f"{message_head}: {len(recommended_sequence)} write-tool step(s) "
            f"based on existing Phase 2/3 tools."
        )
    else:
        message = (
            f"{message_head}: no applicable public write-tool recipe — "
            "see presumed_findings for the reason."
        )

    recommended_checks: list[str] = []
    if recipe and not deletion_request:
        recommended_checks.append(
            "Re-run suggest_safe_change_order after picking the target "
            "for a dependency-aware ordering."
        )
    if not recommended_sequence:
        recommended_checks.append(
            "No automated path available; this change must be performed "
            "outside the platform's current write-tool surface."
        )

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=message,
        payload={
            "runtime": runtime_payload,
            "target_kind": target_kind,
            "target_name": target_name,
            "change_goal": change_goal,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_sequence": recommended_sequence,
            "recommended_checks": recommended_checks,
            "suggested_tools": suggested_tools,
            "suggested_write_tools": suggested_write_tools,
            "sources_used": ["suggest_metadata_patch_plan rule table"],
        },
    )


_WRITE_TOOL_DESCRIPTIONS: dict[str, str] = {
    "check_write_preconditions": "Validate preflight conditions before any mutation.",
    "create_backup_snapshot": "Snapshot the infobase-side backup state.",
    "create_dump_snapshot": "Snapshot the dump-side state.",
    "apply_config_from_files": "Apply configuration changes from files.",
    "update_module_code": "Update BSL module code.",
    "create_common_module": "Create a new common module object.",
    "verify_module_contains": "Verify a method is present in a module.",
    "verify_object_exists": "Verify an object exists in the configuration.",
    "verify_metadata_change": "Verify a metadata shape change landed.",
    "update_database_configuration": "Re-apply configuration to the database.",
    "add_catalog_attribute": "Add an attribute to a catalog.",
    "write_audit_record": "Write an audit record (called internally by write-flow).",
    "describe_last_write_operation": "Describe the last write operation from audit.",
    "prepare_rollback_hint": "Prepare a rollback hint for a past write operation.",
    "create_catalog": "Create a new catalog object.",
    "add_document_attribute": "Add an attribute to a document.",
    "verify_attribute_exists": "Verify an attribute exists on an object.",
    "diff_dump_fragment": "Diff a specific dump fragment against the previous snapshot.",
    "create_managed_form": "Create a managed form on an existing object.",
    "add_form_element": "Add an element to a managed form.",
    "append_module_method": "Append a new method to an existing module.",
    "replace_module_method_body": "Replace the body of an existing module method (requires confirm_replace=True).",
}


def _step_description(write_tool: str) -> str:
    return _WRITE_TOOL_DESCRIPTIONS.get(write_tool, "See write-server docs.")


def summarize_configuration_risk(
    environment: EnvironmentConfig,
    object_name: str | None = None,
) -> ToolResult:
    """Short rule-based risk summary for the environment or for one object.

    Two modes:

    - **Global** (``object_name is None``) — risk driven by
      ``runtime.health_codes``: ``dump_missing`` → high,
      ``gateway_down`` or ``index_lock`` → medium, otherwise low.
    - **Per-object** — runtime signals + ``find_references_to_object``
      reference count. ``dump_missing`` still dominates. Otherwise:
      > 20 references → medium, > 5 → low, 0 references → low with a
      ``object_not_referenced`` presumed signal.

    The risk band is a deterministic rule; the thresholds and the
    reasoning live in ``presumed_findings``.
    """
    tool_name = "summarize_configuration_risk"
    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)

    health_codes = list(context.health_codes)
    confirmed_findings: dict = {
        "health_codes": health_codes,
        "object_name": object_name,
    }

    reference_count: int | None = None
    ref_error: str | None = None
    if object_name:
        if context.dump_root.exists():
            try:
                reference_count = len(
                    find_references(context.dump_root, object_name)
                )
                confirmed_findings["reference_count"] = reference_count
            except (PlatformError, ValueError, OSError) as exc:
                ref_error = f"reference scan failed: {exc}"
        else:
            ref_error = f"dump root missing: {context.dump_root}"

    if "dump_missing" in health_codes:
        risk_level = "high"
        reasoning = (
            "Dump is missing — most intelligence tools cannot produce "
            "reliable output until the dump is regenerated."
        )
    elif "gateway_down" in health_codes or "index_lock" in health_codes:
        risk_level = "medium"
        reasoning = (
            "Runtime health has non-critical issues; live-facing tools "
            "will degrade gracefully but some analyses will be blind."
        )
    elif object_name:
        if reference_count is None:
            risk_level = "medium"
            reasoning = (
                "Per-object analysis requested, but reference count "
                "could not be computed; treat as medium risk until "
                "resolved."
            )
        elif reference_count > 20:
            risk_level = "medium"
            reasoning = (
                f"Object '{object_name}' has {reference_count} references; "
                "a change here has wide blast radius."
            )
        elif reference_count == 0:
            risk_level = "low"
            reasoning = (
                f"No references to '{object_name}' found — either the "
                "object is isolated or misspelled; risk is low but worth "
                "confirming."
            )
        else:
            risk_level = "low"
            reasoning = (
                f"Object '{object_name}' has {reference_count} reference(s); "
                "limited blast radius."
            )
    else:
        risk_level = "low"
        reasoning = "No health issues and no per-object context."

    presumed_findings: list[dict] = [
        {
            "pattern": "risk_summary",
            "risk_level": risk_level,
            "reasoning": reasoning,
            "source": "summarize_configuration_risk rule",
        }
    ]
    if ref_error is not None:
        presumed_findings.append(
            {
                "pattern": "reference_scan_error",
                "probable_cause": ref_error,
                "source": "summarize_configuration_risk rule",
            }
        )
    if object_name and reference_count == 0:
        presumed_findings.append(
            {
                "pattern": "object_not_referenced",
                "probable_cause": (
                    "Object has zero references in the scanned dump."
                ),
                "source": "summarize_configuration_risk rule",
            }
        )

    recommended_checks: list[str] = []
    if "dump_missing" in health_codes:
        recommended_checks.append("Re-generate the dump; re-run health checks.")
    if "gateway_down" in health_codes:
        recommended_checks.append(
            "Restart the publication and re-run analyze_runtime_issue."
        )
    if object_name and reference_count and reference_count > 20:
        recommended_checks.append(
            "Run estimate_change_impact and suggest_safe_change_order "
            "before touching the object."
        )
    if not recommended_checks:
        recommended_checks.append("No immediate follow-up recommended.")

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=(
            f"Risk summary"
            f"{f' for {object_name!r}' if object_name else ''}: "
            f"{risk_level}."
        ),
        payload={
            "runtime": runtime_payload,
            "object_name": object_name,
            "risk_level": risk_level,
            "confirmed_findings": confirmed_findings,
            "presumed_findings": presumed_findings,
            "recommended_checks": recommended_checks,
            "suggested_tools": (
                [
                    "analyze_runtime_issue",
                    "estimate_change_impact",
                    "analyze_object_dependencies",
                ]
                if object_name
                else ["analyze_runtime_issue"]
            ),
            "sources_used": ["runtime.build_runtime_context"]
            + (["runtime.reference_finder.find_references"] if reference_count is not None else []),
        },
    )


# Whitelist of tool names ``prepare_intelligence_report`` is allowed to
# orchestrate.  The callable is resolved at call time via
# ``globals()`` to avoid forward-reference problems; names here must
# correspond to public intelligence-tool functions defined in this
# module.
_REPORT_KNOWN_TOOLS: dict[str, str] = {
    "analyze_runtime_issue": "no_subject",
    "analyze_event_log_patterns": "no_subject",
    "analyze_object_dependencies": "subject_as_object_name",
    "find_references_to_object": "subject_as_object_name",
    "find_module_method_usages": "subject_as_method_name",
    "estimate_change_impact": "subject_as_object_name",
    "find_affected_forms": "subject_as_object_name",
    "find_affected_modules": "subject_as_object_name",
    "summarize_configuration_risk": "subject_as_object_name_optional",
}

_REPORT_DEFAULT_INCLUDE: tuple[str, ...] = (
    "analyze_runtime_issue",
    "analyze_object_dependencies",
    "estimate_change_impact",
    "summarize_configuration_risk",
)


def _invoke_report_tool(
    name: str, environment: EnvironmentConfig, subject: str
) -> ToolResult:
    mode = _REPORT_KNOWN_TOOLS[name]
    fn = globals()[name]
    if mode == "no_subject":
        return fn(environment)
    if mode == "subject_as_method_name":
        return fn(environment, subject)
    # subject_as_object_name and subject_as_object_name_optional both
    # accept subject as positional/object_name here.
    return fn(environment, subject)


def prepare_intelligence_report(
    environment: EnvironmentConfig,
    subject: str,
    include_tools: list[str] | None = None,
) -> ToolResult:
    """Orchestrate a compact, read-only intelligence report on a subject.

    Invokes a whitelisted subset of other intelligence-tools defined in
    this module. Never writes anything to disk, never creates temp
    files, never calls write-flow.

    Inputs:

    - ``subject`` — non-empty string; used as ``object_name`` or
      ``method_name`` by the sub-tools that need one.
    - ``include_tools`` — optional list of tool names to include. If
      omitted, a small sensible default set is used. Names not in the
      orchestrator whitelist are surfaced in
      ``skipped_unknown_tools`` rather than silently dropped.

    The payload aggregates each sub-tool's result under ``sections``
    and flattens their ``confirmed_findings`` / ``presumed_findings`` /
    ``recommended_checks`` / ``suggested_tools`` for convenience, always
    tagged with the originating tool name so the caller can trace
    provenance.
    """
    tool_name = "prepare_intelligence_report"
    if not subject:
        return _fail(tool_name, "subject is empty.")

    context = build_runtime_context(environment)
    runtime_payload = _runtime_payload(context)

    if include_tools is None:
        requested = list(_REPORT_DEFAULT_INCLUDE)
    else:
        requested = list(include_tools)

    included: list[str] = []
    skipped: list[str] = []
    for name in requested:
        if name in _REPORT_KNOWN_TOOLS:
            included.append(name)
        else:
            skipped.append(name)

    sections: dict[str, dict] = {}
    aggregate_confirmed: list[dict] = []
    aggregate_presumed: list[dict] = []
    aggregate_checks: list[dict] = []
    aggregate_suggested: set[str] = set()

    for name in included:
        try:
            result = _invoke_report_tool(name, environment, subject)
        except Exception as exc:  # noqa: BLE001 — never leak to caller
            sections[name] = {
                "ok": False,
                "message": f"Orchestration raised: {exc}",
                "payload": {},
            }
            continue
        sections[name] = {
            "ok": result.ok,
            "message": result.message,
            "payload": result.payload,
        }
        payload = result.payload if isinstance(result.payload, dict) else {}
        cf = payload.get("confirmed_findings")
        if isinstance(cf, list):
            for item in cf:
                aggregate_confirmed.append({"tool": name, "item": item})
        elif isinstance(cf, dict):
            aggregate_confirmed.append({"tool": name, "item": cf})
        pf = payload.get("presumed_findings")
        if isinstance(pf, list):
            for item in pf:
                aggregate_presumed.append({"tool": name, "item": item})
        checks = payload.get("recommended_checks")
        if isinstance(checks, list):
            for item in checks:
                aggregate_checks.append({"tool": name, "check": item})
        suggested = payload.get("suggested_tools")
        if isinstance(suggested, list):
            for item in suggested:
                if isinstance(item, str):
                    aggregate_suggested.add(item)

    message = (
        f"Intelligence report for '{subject}': "
        f"{len(included)} section(s)"
    )
    if skipped:
        message += f", {len(skipped)} unknown tool(s) skipped"

    return ToolResult(
        ok=True,
        tool_name=tool_name,
        message=message,
        payload={
            "runtime": runtime_payload,
            "subject": subject,
            "included_tools": included,
            "skipped_unknown_tools": skipped,
            "sections": sections,
            "confirmed_findings": aggregate_confirmed,
            "presumed_findings": aggregate_presumed,
            "recommended_checks": aggregate_checks,
            "suggested_tools": sorted(aggregate_suggested),
            "sources_used": [f"intelligence.{n}" for n in included],
        },
    )
