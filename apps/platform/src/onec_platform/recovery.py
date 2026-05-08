"""Rollback / recovery / audit UX (Phase 5 / Step 6).

Single product-level orchestration boundary that gives the operator
three things over an environment's existing audit JSONL:

- :func:`get_operation_history` — operator-visible list of past
  write operations from ``<dump_path>/.audit/audit.jsonl``;
- :func:`inspect_operation` — focus on one ``operation_id``,
  attaching its rollback hint and a short operator summary;
- :func:`run_rollback_assistant` — preview / advisory mode with an
  honest ``confirm_execute=True`` gate.

What this module is, very precisely:

- a thin UX over the audit JSONL plus the already-existing
  :func:`mcp_write_server.tools.prepare_rollback_hint`
  / :func:`mcp_write_server.tools.describe_last_write_operation`
  surface, with a narrow Phase 6 / Step 4 executed-rollback path on
  top of it;
- a deliberately-honest assistant: the executed-rollback branch
  always goes through public write-tools
  (:func:`mcp_write_server.tools.restore_dump_file_from_snapshot`
  and :func:`mcp_write_server.tools.diff_dump_fragment`), so the
  policy / preflight / snapshot / verify / audit discipline of
  ``run_write_flow`` applies to rollbacks just like to forward
  writes. There is no back-door filesystem write from the product
  layer.

What this module is NOT:

- it does **not** introduce new MCP tools or change any registry;
- it does **not** mutate the audit log directly, the dump
  directly, or the infobase (any mutation goes through public
  write-tools);
- it does **not** import :mod:`onec_policy_engine` and never makes
  policy decisions of its own;
- it is **not** a Step 7 real-stand / 1cv8 integration track.

Failure model:

- :func:`get_operation_history`, :func:`inspect_operation`,
  :func:`run_rollback_assistant`, and their ``_from_json_file``
  variants **never raise**.
- ``ok=True`` covers the honest happy paths (history loaded,
  operation inspected, preview built, supported recovery executed
  and verified). Phase 6 / Step 4 ships the first non-empty
  whitelist — see :data:`_AUTOMATIC_RECOVERY_SUPPORTED`.
- ``ok=False`` is reserved for invalid inputs, missing operation,
  unreadable audit, or attempted execution that ran and failed
  (including post-rollback verify mismatch).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from onec_config import EnvironmentConfig

# Cross-app imports go forward only: product → write.
# Phase 6 / Step 4 adds two more write-server entries used by the
# executed-rollback branch: ``restore_dump_file_from_snapshot`` (the
# new mutating restore tool that goes through ``run_write_flow``) and
# ``diff_dump_fragment`` (read-only verify). Both are real public
# tools registered in the write-server registry; product layer never
# touches the dump filesystem directly.
from mcp_write_server.tools import (
    describe_last_write_operation,
    diff_dump_fragment,
    prepare_rollback_hint,
    restore_dump_file_from_snapshot,
)

from .dashboard import build_environment_dashboard
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    DoctorFinding,
    EnvironmentDashboardResult,
    OperationHistoryEntry,
    OperationHistoryResult,
    OperationHistorySummary,
    OperationInspectResult,
    ProductConfig,
    RECOVERY_MODES,
    RollbackAssistantResult,
    RollbackPlan,
    WorkflowStepResult,
)

# Re-use the live-registry tool-name discipline established in Step 5.
# Importing the private helper keeps a single source of truth — if a
# new tool is added to a registry, both workflow and recovery surfaces
# pick it up without duplication.
from .workflow import _allow_only_real_tools


# ---------------------------------------------------------------------------
# Honest-recovery whitelist.
# ---------------------------------------------------------------------------

# Tool families for which Phase 6 / Step 4 ships an automatic
# content-level rollback path. The Step 4 slice is intentionally
# narrow: only single-file XML-card metadata mutations whose live
# target is captured by the write-flow's ``dump_snapshot_path`` and
# whose ``operation_payload`` records a single ``relative_path``.
#
# When this whitelist is hit at ``confirm_execute=True`` time, the
# assistant runs :func:`mcp_write_server.tools.restore_dump_file_from_snapshot`
# (a real mutating write-tool registered in the write-server registry,
# routed through ``run_write_flow`` like every other mutation) and
# then post-rollback verifies via :func:`diff_dump_fragment`. There
# is **no** product-layer back-door write channel — the recovery
# branch lives entirely on top of public write surfaces.
#
# Adding more tool families here in the future requires that:
# (a) their ``operation_payload`` carries a single ``relative_path``,
# (b) they are reasonably restorable by overwriting that one file,
# (c) their inverse semantics are honestly captured by snapshot
#     restore (not e.g. ``delete_module`` whose snapshot still
#     contains the dependent code that referenced it).
_AUTOMATIC_RECOVERY_SUPPORTED: frozenset[str] = frozenset(
    {
        "add_catalog_attribute",
        "add_document_attribute",
        "add_form_attribute",
        "add_form_element",
        "append_module_method",
        "replace_module_method_body",
    }
)


# Tool families the assistant has *informational* knowledge of, even
# though it cannot auto-execute their rollback. Used to print honest
# "snapshot-restore is the manual path forward" hints in the plan
# summary. Anything here must be a real registered write-tool name
# (validated programmatically by the manual check).
_KNOWN_WRITE_TOOL_FAMILIES: frozenset[str] = frozenset(
    {
        "add_catalog_attribute",
        "add_document_attribute",
        "append_module_method",
        "create_catalog",
        "create_common_module",
        "create_managed_form",
        "add_form_element",
        "update_module_code",
        "replace_module_method_body",
        "apply_config_from_files",
        "update_database_configuration",
    }
)


# ---------------------------------------------------------------------------
# Finding factories.
# ---------------------------------------------------------------------------


def _ok(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="ok", confidence=confidence, detail=detail)


def _warn(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="warning", confidence=confidence, detail=detail)


def _err(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(code=code, severity="error", confidence=confidence, detail=detail)


# ---------------------------------------------------------------------------
# Config / environment resolution.
# ---------------------------------------------------------------------------


def _resolve_config(
    data: dict | ProductConfig,
) -> tuple[ProductConfig | None, str | None]:
    if isinstance(data, ProductConfig):
        return data, None
    if isinstance(data, dict):
        try:
            return load_product_config(data), None
        except (ValueError, TypeError) as exc:
            return None, f"Product config rejected: {exc}"
    return None, (
        "Product config must be a dict or a pre-loaded ProductConfig "
        f"(got {type(data).__name__})."
    )


def _resolve_environment(
    config: ProductConfig,
) -> EnvironmentConfig | None:
    return config.project.environments.get(config.default_environment)


# ---------------------------------------------------------------------------
# Audit-log reading.
# ---------------------------------------------------------------------------


def _audit_path(env: EnvironmentConfig) -> Path:
    """Return the canonical audit file path for an environment."""
    return Path(env.dump_path) / ".audit" / "audit.jsonl"


_REQUIRED_RECORD_FIELDS: tuple[str, ...] = (
    "operation_id",
    "tool_name",
    "environment",
    "base_id",
    "status",
    "message",
)


def _read_audit_lines(audit_file: Path) -> tuple[list[str], DoctorFinding | None]:
    """Read the raw audit JSONL lines.

    Returns ``(lines, finding)`` where ``finding`` is non-None only
    on a hard read error. A missing file is **not** an error — it
    yields ``([], None)``: a clean environment with no writes yet
    is a valid honest history-empty state.
    """
    if not audit_file.exists():
        return [], None
    if not audit_file.is_file():
        return [], _err(
            "audit_path_not_a_file",
            f"Audit path exists but is not a regular file: {audit_file}",
        )
    try:
        text = audit_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [], _err(
            "audit_unreadable",
            f"Failed to read audit log {audit_file}: {exc}",
        )
    return text.splitlines(), None


def _entry_details(entry: OperationHistoryEntry) -> dict | None:
    """Extract structured ``details`` from an audit entry's raw line.

    Backward-compatible reader: pre-Phase-6/Step-4 audit lines do not
    carry a ``details`` key, so this returns ``None`` for them, and
    downstream code degrades to "automatic recovery not supported for
    this entry". Returns ``None`` for any malformed shape rather than
    raising — the parent caller already passed JSON validation by
    constructing the entry, but ``details`` is free-shape and we
    treat anything weird as "no usable structured data".
    """
    raw = entry.raw_line
    if not raw:
        return None
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(decoded, dict):
        return None
    details = decoded.get("details")
    return details if isinstance(details, dict) else None


def _details_indicate_rollback_supported(
    entry: OperationHistoryEntry, details: dict | None
) -> bool:
    """Decide whether automatic rollback is supported for an audit entry.

    Three conditions must hold simultaneously:
    - the audit entry's ``tool_name`` is in
      :data:`_AUTOMATIC_RECOVERY_SUPPORTED`;
    - structured ``details`` are present (i.e. the audit row was
      written by the Step 4-aware write-flow);
    - ``details`` carry the two artefacts the executed branch needs:
      ``dump_snapshot_path`` and ``relative_path``.

    If any of the three is missing, the assistant degrades honestly
    to advisory-only — no fake supported flag.
    """
    if entry.tool_name not in _AUTOMATIC_RECOVERY_SUPPORTED:
        return False
    if not details:
        return False
    snapshot = details.get("dump_snapshot_path")
    relative = details.get("relative_path")
    return (
        isinstance(snapshot, str)
        and bool(snapshot)
        and isinstance(relative, str)
        and bool(relative)
    )


def _parse_audit_lines(
    lines: list[str],
) -> tuple[list[OperationHistoryEntry], list[DoctorFinding]]:
    """Parse raw lines into entries; collect findings for malformed lines.

    Empty lines are skipped silently (audit may legitimately end with
    a trailing newline). Malformed JSON or missing required fields
    yield warning findings but do not abort the load — the operator
    sees the rest of the history plus an honest finding for each
    skipped line.
    """
    entries: list[OperationHistoryEntry] = []
    findings: list[DoctorFinding] = []
    position = 0
    for raw_idx, raw in enumerate(lines):
        stripped = raw.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            findings.append(
                _warn(
                    f"audit_line_invalid_json:{raw_idx}",
                    f"Skipped non-JSON audit line at index {raw_idx}.",
                )
            )
            continue
        if not isinstance(payload, dict):
            findings.append(
                _warn(
                    f"audit_line_not_a_dict:{raw_idx}",
                    f"Skipped non-dict audit line at index {raw_idx}.",
                )
            )
            continue
        missing = [f for f in _REQUIRED_RECORD_FIELDS if not isinstance(payload.get(f), str)]
        if missing:
            findings.append(
                _warn(
                    f"audit_line_missing_fields:{raw_idx}",
                    f"Skipped audit line at index {raw_idx}; missing/non-string "
                    f"fields: {missing}.",
                )
            )
            continue
        entries.append(
            OperationHistoryEntry(
                position=position,
                operation_id=payload["operation_id"],
                tool_name=payload["tool_name"],
                environment=payload["environment"],
                base_id=payload["base_id"],
                status=payload["status"],
                message=payload["message"],
                raw_line=stripped,
            )
        )
        position += 1
    return entries, findings


def _summarize(entries: list[OperationHistoryEntry]) -> OperationHistorySummary:
    summary = OperationHistorySummary(total=len(entries))
    for entry in entries:
        if entry.status == "ok":
            summary.ok_count += 1
        elif entry.status == "error":
            summary.error_count += 1
        else:
            summary.other_count += 1
    return summary


def _filter_entries(
    entries: list[OperationHistoryEntry],
    *,
    only_status: str | None,
    limit: int | None,
) -> list[OperationHistoryEntry]:
    if only_status is not None:
        entries = [e for e in entries if e.status == only_status]
    if limit is not None and limit >= 0:
        entries = entries[-limit:] if limit > 0 else []
    return entries


# ---------------------------------------------------------------------------
# Boundary: operation history viewer.
# ---------------------------------------------------------------------------


def _rejected_history(
    message: str,
    *,
    product_name: str | None = None,
    profile_name: str | None = None,
    default_env: str | None = None,
) -> OperationHistoryResult:
    return OperationHistoryResult(
        ok=False,
        product_name=product_name,
        profile_name=profile_name,
        default_environment=default_env,
        audit_path=None,
        entries=[],
        summary=OperationHistorySummary(),
        findings=[_err("history_rejected", message)],
        message=message,
    )


def get_operation_history(
    data: dict | ProductConfig,
    *,
    limit: int | None = None,
    only_status: str | None = None,
) -> OperationHistoryResult:
    """Return the operator-visible audit history for the default environment.

    Read-only. Never raises. ``ok=True`` covers both "history with N
    entries" and "no audit file present yet". ``ok=False`` is only
    used for invalid inputs (bad config, unresolved environment,
    invalid filter values).
    """
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            return _rejected_history(
                f"limit must be a non-negative int if provided; got {limit!r}."
            )
    if only_status is not None and not isinstance(only_status, str):
        return _rejected_history(
            f"only_status must be a string if provided; got {type(only_status).__name__}."
        )

    config, err = _resolve_config(data)
    if config is None:
        return _rejected_history(err or "Unknown configuration error.")

    env = _resolve_environment(config)
    if env is None:
        return _rejected_history(
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments.",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_env=config.default_environment,
        )

    audit_file = _audit_path(env)
    lines, read_finding = _read_audit_lines(audit_file)
    findings: list[DoctorFinding] = []
    if read_finding is not None:
        findings.append(read_finding)
        return OperationHistoryResult(
            ok=False,
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            audit_path=str(audit_file),
            entries=[],
            summary=OperationHistorySummary(),
            findings=findings,
            message=read_finding.detail,
        )

    parsed, parse_findings = _parse_audit_lines(lines)
    findings.extend(parse_findings)

    filtered = _filter_entries(parsed, only_status=only_status, limit=limit)
    summary = _summarize(filtered)

    if not parsed:
        message = "Audit log is empty or absent — no operations to show."
    else:
        message = (
            f"Loaded {summary.total} operation(s) "
            f"(ok={summary.ok_count}, error={summary.error_count}, "
            f"other={summary.other_count})."
        )

    return OperationHistoryResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        audit_path=str(audit_file),
        entries=filtered,
        summary=summary,
        findings=findings,
        message=message,
    )


def get_operation_history_from_json_file(
    path: str | Path,
    *,
    limit: int | None = None,
    only_status: str | None = None,
) -> OperationHistoryResult:
    """Like :func:`get_operation_history`, but reads the product config
    from a JSON file. Never raises."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_history(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_history(f"Product config could not be loaded: {exc}")
    return get_operation_history(config, limit=limit, only_status=only_status)


# ---------------------------------------------------------------------------
# Boundary: inspect a single operation.
# ---------------------------------------------------------------------------


def _find_entry(
    entries: list[OperationHistoryEntry], operation_id: str
) -> OperationHistoryEntry | None:
    for entry in entries:
        if entry.operation_id == operation_id:
            return entry
    return None


def _rollback_hint_payload(env: EnvironmentConfig, operation_id: str) -> dict | None:
    """Best-effort fetch of the rollback hint dict for an operation_id.

    Reuses the existing read-only :func:`prepare_rollback_hint`
    write-server tool. Returns the ``data`` sub-dict on success, or
    ``None`` if the helper failed for any reason — the caller decides
    whether that is fatal.
    """
    try:
        result = prepare_rollback_hint(env, operation_id)
    except Exception:  # noqa: BLE001 — boundary, never propagate
        return None
    if not result.ok:
        return None
    payload = result.payload if isinstance(result.payload, dict) else {}
    data = payload.get("data") if isinstance(payload.get("data"), dict) else None
    return dict(data) if isinstance(data, dict) else None


def _operator_summary_for_entry(
    entry: OperationHistoryEntry,
    *,
    automatic_supported: bool,
    rollback_hint: dict | None,
) -> list[str]:
    summary: list[str] = [
        f"Operation: {entry.tool_name} (operation_id={entry.operation_id}).",
        f"Status: {entry.status}.",
    ]
    if entry.message:
        summary.append(f"Message: {entry.message}")
    if automatic_supported:
        summary.append(
            "Automatic recovery: SUPPORTED — assistant can re-attempt the "
            "inverse step under operator confirmation."
        )
    else:
        summary.append(
            "Automatic recovery: NOT SUPPORTED on Step 6. The honest path is "
            "manual snapshot-restore from the rollback hint below."
        )
    if rollback_hint is not None:
        backup = rollback_hint.get("suggested_backup_root")
        dump = rollback_hint.get("suggested_dump_root")
        if backup:
            summary.append(f"Suggested backup snapshot root: {backup}")
        if dump:
            summary.append(f"Suggested dump snapshot root: {dump}")
    return summary


def _rejected_inspect(
    operation_id: str,
    message: str,
    *,
    config: ProductConfig | None = None,
    operation_found: bool = False,
) -> OperationInspectResult:
    return OperationInspectResult(
        ok=False,
        product_name=(config.product_name if config is not None else None),
        profile_name=(config.profile_name if config is not None else None),
        default_environment=(config.default_environment if config is not None else None),
        operation_id=operation_id,
        operation_found=operation_found,
        history_entry=None,
        rollback_hint=None,
        automatic_recovery_supported=False,
        operator_summary=[],
        findings=[_err("inspect_rejected", message)],
        suggested_tools=[],
        suggested_write_tools=[],
        message=message,
    )


def inspect_operation(
    data: dict | ProductConfig,
    *,
    operation_id: str,
) -> OperationInspectResult:
    """Focus on one ``operation_id`` and return a rich operator view.

    Read-only. Never raises. Returns ``ok=False, operation_found=False``
    when the operation is missing — the caller branches on
    ``operation_found`` rather than parsing the message.
    """
    if not isinstance(operation_id, str) or not operation_id.strip():
        return _rejected_inspect(
            str(operation_id) if operation_id is not None else "",
            "operation_id must be a non-empty string.",
        )

    config, err = _resolve_config(data)
    if config is None:
        return _rejected_inspect(
            operation_id, err or "Unknown configuration error."
        )

    env = _resolve_environment(config)
    if env is None:
        return _rejected_inspect(
            operation_id,
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments.",
            config=config,
        )

    audit_file = _audit_path(env)
    lines, read_finding = _read_audit_lines(audit_file)
    findings: list[DoctorFinding] = []
    if read_finding is not None:
        findings.append(read_finding)
        return OperationInspectResult(
            ok=False,
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            operation_id=operation_id,
            operation_found=False,
            history_entry=None,
            rollback_hint=None,
            automatic_recovery_supported=False,
            operator_summary=[],
            findings=findings,
            suggested_tools=[],
            suggested_write_tools=[],
            message=read_finding.detail,
        )
    parsed, parse_findings = _parse_audit_lines(lines)
    findings.extend(parse_findings)

    entry = _find_entry(parsed, operation_id)
    if entry is None:
        return OperationInspectResult(
            ok=False,
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            operation_id=operation_id,
            operation_found=False,
            history_entry=None,
            rollback_hint=None,
            automatic_recovery_supported=False,
            operator_summary=[],
            findings=findings + [
                _err(
                    "operation_not_found",
                    f"operation_id={operation_id!r} not found in audit log.",
                )
            ],
            suggested_tools=[],
            suggested_write_tools=[],
            message=f"operation_id={operation_id!r} not found in audit log.",
        )

    rollback_hint = _rollback_hint_payload(env, operation_id)
    details = _entry_details(entry)
    automatic_supported = _details_indicate_rollback_supported(entry, details)
    operator_summary = _operator_summary_for_entry(
        entry,
        automatic_supported=automatic_supported,
        rollback_hint=rollback_hint,
    )
    if details is not None:
        rel = details.get("relative_path")
        snap = details.get("dump_snapshot_path")
        if isinstance(rel, str) and rel:
            operator_summary.append(f"Audit relative_path: {rel}")
        if isinstance(snap, str) and snap:
            operator_summary.append(f"Audit dump_snapshot_path: {snap}")

    base_tools = [
        "describe_last_write_operation",
        "prepare_rollback_hint",
        "build_environment_dashboard",
        "get_product_runtime_status",
    ]
    base_write_tools = [
        "describe_last_write_operation",
        "prepare_rollback_hint",
    ]
    if automatic_supported:
        # Only when the entry can really be auto-recovered do we
        # advertise the executed-rollback tools as suggested. Keeps
        # the tool-name discipline honest for pre-Step-4 audit lines.
        base_write_tools.extend(
            ["restore_dump_file_from_snapshot", "diff_dump_fragment"]
        )
        base_tools.append("diff_dump_fragment")
    suggested_tools = _allow_only_real_tools(base_tools)
    suggested_write_tools = _allow_only_real_tools(base_write_tools)

    return OperationInspectResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        operation_id=operation_id,
        operation_found=True,
        history_entry=entry,
        rollback_hint=rollback_hint,
        automatic_recovery_supported=automatic_supported,
        operator_summary=operator_summary,
        findings=findings,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        message=(
            f"Operation {operation_id!r} ({entry.tool_name}) inspected; "
            f"automatic_recovery_supported={automatic_supported}."
        ),
    )


def inspect_operation_from_json_file(
    path: str | Path,
    *,
    operation_id: str,
) -> OperationInspectResult:
    """Like :func:`inspect_operation`, but reads product config from JSON."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_inspect(operation_id, f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_inspect(
            operation_id, f"Product config could not be loaded: {exc}"
        )
    return inspect_operation(config, operation_id=operation_id)


# ---------------------------------------------------------------------------
# Boundary: rollback / recovery assistant.
# ---------------------------------------------------------------------------


def _step_from_tool_result(
    name: str,
    kind: str,
    source: str,
    result: Any,
) -> WorkflowStepResult:
    payload = result.payload if isinstance(getattr(result, "payload", None), dict) else {}
    return WorkflowStepResult(
        name=name,
        kind=kind,
        ok=bool(getattr(result, "ok", False)),
        source=source,
        payload=payload,
        message=str(getattr(result, "message", "")),
    )


def _tool_result_dict(result: Any) -> dict:
    """Flatten a ``ToolResult`` to the dict shape used by ``write_results``.

    Mirrors :func:`onec_platform.workflow._tool_result_dict` — kept local
    to avoid coupling recovery to another private helper in workflow.
    """
    return {
        "ok": bool(getattr(result, "ok", False)),
        "tool_name": str(getattr(result, "tool_name", "")),
        "message": str(getattr(result, "message", "")),
        "payload": (
            result.payload
            if isinstance(getattr(result, "payload", None), dict)
            else {}
        ),
    }


def _diff_indicates_match(diff_result: Any) -> bool:
    """Return True iff a ``diff_dump_fragment`` result reports no diff.

    Phase 6 / Step 4 post-rollback verify success criterion. We require
    both ``ok=True`` (the file was readable) AND ``data.changed=False``
    (live target byte-equals the baseline). Any other shape is treated
    as a verify failure — the assistant degrades the executed-rollback
    result to ``ok=False`` rather than silently claim success.
    """
    if not bool(getattr(diff_result, "ok", False)):
        return False
    payload = diff_result.payload if isinstance(getattr(diff_result, "payload", None), dict) else {}
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return False
    changed = data.get("changed")
    return changed is False


def _build_dashboard_summary(
    dash: EnvironmentDashboardResult,
) -> dict:
    return {
        "ok": dash.ok,
        "verdict": (asdict(dash.verdict) if dash.verdict is not None else None),
        "sources_used": list(dash.sources_used),
        "message": dash.message,
    }


def _build_rollback_plan(
    entry: OperationHistoryEntry,
    rollback_hint: dict | None,
    details: dict | None = None,
) -> RollbackPlan:
    """Assemble an operator-visible rollback plan.

    On Phase 6 / Step 4 ``automatic_recovery_supported`` is True iff
    the entry's ``tool_name`` is in
    :data:`_AUTOMATIC_RECOVERY_SUPPORTED` AND the audit row carries
    structured ``details`` with both ``dump_snapshot_path`` and
    ``relative_path``. Pre-Step-4 audit lines (no ``details``) keep
    falling into advisory-only.
    """
    automatic = _details_indicate_rollback_supported(entry, details)
    backup_root = (
        rollback_hint.get("suggested_backup_root")
        if isinstance(rollback_hint, dict)
        else None
    )
    dump_root = (
        rollback_hint.get("suggested_dump_root")
        if isinstance(rollback_hint, dict)
        else None
    )
    summary: list[str] = [
        f"Target operation: {entry.tool_name} (operation_id={entry.operation_id}).",
        f"Audit status: {entry.status}.",
    ]
    if automatic:
        rel = (details or {}).get("relative_path")
        snap = (details or {}).get("dump_snapshot_path")
        summary.append(
            "Automatic recovery: SUPPORTED (Phase 6 / Step 4). Executing "
            "with confirm_execute=True will call the public write-tool "
            "restore_dump_file_from_snapshot — single-file restore "
            "through run_write_flow (preflight + snapshot + verify + "
            "audit), then post-rollback verify via diff_dump_fragment."
        )
        if isinstance(rel, str) and rel:
            summary.append(f"relative_path to restore: {rel}")
        if isinstance(snap, str) and snap:
            summary.append(f"snapshot root for restore: {snap}")
    else:
        if entry.tool_name in _AUTOMATIC_RECOVERY_SUPPORTED:
            summary.append(
                "Automatic recovery: NOT SUPPORTED for this audit entry. "
                "The tool family is whitelisted, but the audit row lacks "
                "structured details (dump_snapshot_path / relative_path) "
                "needed for executed rollback. This typically means the "
                "row was written before Phase 6 / Step 4 added structured "
                "audit details. Use the snapshot hints below for a "
                "manual restore."
            )
        else:
            summary.append(
                "Automatic recovery: NOT SUPPORTED for this tool family "
                "on Phase 6 / Step 4. The Step 4 slice ships executed "
                "rollback only for add_catalog_attribute and "
                "add_document_attribute. Other classes remain advisory-"
                "only — the product layer never back-doors the dump."
            )
        if entry.tool_name in _KNOWN_WRITE_TOOL_FAMILIES:
            summary.append(
                "Recommended manual path: use the snapshot roots below "
                "to copy back the pre-operation state. The product layer "
                "does not perform the copy itself for unsupported families."
            )
    if backup_root:
        summary.append(f"Suggested backup snapshot root: {backup_root}")
    if dump_root:
        summary.append(f"Suggested dump snapshot root: {dump_root}")

    base_tools = [
        "describe_last_write_operation",
        "prepare_rollback_hint",
        "build_environment_dashboard",
        "get_product_runtime_status",
    ]
    base_write_tools = [
        "describe_last_write_operation",
        "prepare_rollback_hint",
    ]
    if automatic:
        base_write_tools.extend(
            ["restore_dump_file_from_snapshot", "diff_dump_fragment"]
        )
        base_tools.append("diff_dump_fragment")
    suggested_tools = _allow_only_real_tools(base_tools)
    suggested_write_tools = _allow_only_real_tools(base_write_tools)
    return RollbackPlan(
        operation_id=entry.operation_id,
        tool_name=entry.tool_name,
        automatic_recovery_supported=automatic,
        summary=summary,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        suggested_backup_root=backup_root,
        suggested_dump_root=dump_root,
    )


def _rejected_assistant(
    operation_id: str,
    message: str,
    *,
    config: ProductConfig | None = None,
) -> RollbackAssistantResult:
    return RollbackAssistantResult(
        ok=False,
        mode="rejected",
        product_name=(config.product_name if config is not None else None),
        profile_name=(config.profile_name if config is not None else None),
        default_environment=(config.default_environment if config is not None else None),
        operation_id=operation_id,
        operation_found=False,
        execution_performed=False,
        plan=None,
        history_entry=None,
        history_summary=None,
        rollback_hint=None,
        dashboard_summary=None,
        steps=[],
        confirmed_findings=[_err("rollback_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        message=message,
    )


def run_rollback_assistant(
    data: dict | ProductConfig,
    *,
    operation_id: str,
    confirm_execute: bool = False,
) -> RollbackAssistantResult:
    """Build a rollback / recovery preview for ``operation_id``.

    Boundary helper. **Never raises.** ``mode`` is one of
    :data:`RECOVERY_MODES`:

    - ``preview`` — preview built, ``confirm_execute=False``;
    - ``executed`` — Phase 6 / Step 4 automatic recovery ran
      (whitelisted tool family + audit details present + healthy
      dashboard). Sets ``execution_performed=True``. ``ok=True`` when
      both the public restore tool returned ``ok=True`` AND the
      mandatory post-rollback verify via ``diff_dump_fragment``
      reported ``changed=False``; ``ok=False`` if either step
      failed. The actual restore goes through
      ``restore_dump_file_from_snapshot`` — i.e. through the same
      ``run_write_flow`` discipline as every other write — so the
      rollback itself is preflighted, snapshotted, verified, and
      audited;
    - ``blocked`` — ``confirm_execute=True`` requested but the
      dashboard is not in ``ready_for_workflows`` state; preview is
      still built;
    - ``unsupported`` — ``confirm_execute=True`` requested and the
      dashboard is healthy, but the audit operation has no automatic
      recovery path on Phase 6 / Step 4 (tool family outside the
      whitelist, or whitelisted tool with audit row missing structured
      details); assistant honestly says so without writing anything;
    - ``rejected`` — invalid input, missing operation, unreadable
      audit, or unloadable product config.
    """
    if not isinstance(operation_id, str) or not operation_id.strip():
        return _rejected_assistant(
            str(operation_id) if operation_id is not None else "",
            "operation_id must be a non-empty string.",
        )

    config, err = _resolve_config(data)
    if config is None:
        return _rejected_assistant(operation_id, err or "Unknown configuration error.")

    env = _resolve_environment(config)
    if env is None:
        return _rejected_assistant(
            operation_id,
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments.",
            config=config,
        )

    steps: list[WorkflowStepResult] = []
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    # 1. Dashboard (always built, even on degraded — preview is allowed).
    dash = build_environment_dashboard(config)
    steps.append(
        WorkflowStepResult(
            name="precondition_dashboard",
            kind="precondition",
            ok=dash.ok,
            source="platform.build_environment_dashboard",
            payload=_build_dashboard_summary(dash),
            message=dash.message,
        )
    )
    ready = bool(dash.verdict and dash.verdict.ready_for_workflows)

    # 2. History.
    audit_file = _audit_path(env)
    lines, read_finding = _read_audit_lines(audit_file)
    if read_finding is not None:
        return RollbackAssistantResult(
            ok=False,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            operation_id=operation_id,
            operation_found=False,
            execution_performed=False,
            plan=None,
            history_entry=None,
            history_summary=None,
            rollback_hint=None,
            dashboard_summary=_build_dashboard_summary(dash),
            steps=steps,
            confirmed_findings=[read_finding],
            presumed_findings=[],
            recommended_actions=[],
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            message=read_finding.detail,
        )
    parsed, parse_findings = _parse_audit_lines(lines)
    presumed.extend(parse_findings)
    summary = _summarize(parsed)
    steps.append(
        WorkflowStepResult(
            name="audit_history",
            kind="audit",
            ok=True,
            source="platform.recovery._read_audit_lines",
            payload={
                "audit_path": str(audit_file),
                "summary": asdict(summary),
                "entry_count": len(parsed),
            },
            message=(
                f"Audit history loaded ({summary.total} entries)."
                if parsed
                else "Audit history is empty."
            ),
        )
    )

    # 3. Find the operation.
    entry = _find_entry(parsed, operation_id)
    if entry is None:
        return RollbackAssistantResult(
            ok=False,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            operation_id=operation_id,
            operation_found=False,
            execution_performed=False,
            plan=None,
            history_entry=None,
            history_summary=summary,
            rollback_hint=None,
            dashboard_summary=_build_dashboard_summary(dash),
            steps=steps,
            confirmed_findings=confirmed
            + [
                _err(
                    "operation_not_found",
                    f"operation_id={operation_id!r} not found in audit log.",
                )
            ],
            presumed_findings=presumed,
            recommended_actions=actions,
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            message=f"operation_id={operation_id!r} not found in audit log.",
        )

    # 4. Rollback hint via the existing read-only write-server tool.
    hint_call = prepare_rollback_hint(env, operation_id)
    steps.append(
        _step_from_tool_result(
            "audit_prepare_rollback_hint",
            "audit",
            "write.prepare_rollback_hint",
            hint_call,
        )
    )
    rollback_hint: dict | None = None
    if hint_call.ok and isinstance(hint_call.payload, dict):
        data_block = hint_call.payload.get("data")
        if isinstance(data_block, dict):
            rollback_hint = dict(data_block)

    # 5. last_write_operation surface (read-only).
    last_call = describe_last_write_operation(env)
    steps.append(
        _step_from_tool_result(
            "audit_describe_last_write_operation",
            "audit",
            "write.describe_last_write_operation",
            last_call,
        )
    )
    last_write_operation: dict | None = None
    if last_call.ok and isinstance(last_call.payload, dict):
        data_block = last_call.payload.get("data")
        if isinstance(data_block, dict):
            last_write_operation = dict(data_block)

    # 6. Plan.
    details = _entry_details(entry)
    plan = _build_rollback_plan(entry, rollback_hint, details)

    # 7. Mode resolution.
    automatic_supported = plan.automatic_recovery_supported
    write_results: list[dict] = []
    verify_results: list[dict] = []

    if not confirm_execute:
        mode = "preview"
        ok = True
        message = (
            f"Rollback preview built for operation_id={operation_id!r}. "
            f"automatic_recovery_supported={automatic_supported}. "
            "Pass confirm_execute=True to (attempt to) execute."
        )
        execution_performed = False
    elif not ready:
        # Preview is still built; execution refused while environment
        # is not workflow-ready.
        mode = "blocked"
        ok = False
        message = (
            "Rollback execution blocked: dashboard.ready_for_workflows "
            "is False. Preview is preserved; resolve dashboard issues "
            "before re-running with confirm_execute=True."
        )
        execution_performed = False
    elif not automatic_supported:
        # Honest unsupported result. We do NOT pretend to execute
        # something that does not exist. Tool families outside the
        # Phase 6 / Step 4 whitelist (or whitelisted families whose
        # audit row pre-dates Step 4 and lacks structured details)
        # land here.
        mode = "unsupported"
        ok = True  # the assistant ran honestly; nothing was attempted.
        message = (
            f"Automatic recovery for tool {entry.tool_name!r} is not "
            "supported for this audit entry on Phase 6 / Step 4. Use "
            "the snapshot roots in rollback_hint to perform a manual "
            "restore. The product layer does not perform the copy "
            "itself for unsupported entries."
        )
        execution_performed = False
    else:
        # Phase 6 / Step 4 — real executed rollback for the narrow
        # whitelist (add_catalog_attribute / add_document_attribute).
        # Routed exclusively through public write-tools: no back-door
        # filesystem write from the product layer.
        rel_path = (details or {}).get("relative_path")
        snap_root = (details or {}).get("dump_snapshot_path")
        # Defensive: _details_indicate_rollback_supported guarantees
        # both fields are non-empty strings, but re-validate so a
        # type-confused payload cannot crash the assistant.
        if not isinstance(rel_path, str) or not rel_path:
            mode = "unsupported"
            ok = True
            execution_performed = False
            message = (
                "Automatic recovery aborted: relative_path missing from "
                "audit details after whitelist check. This indicates a "
                "malformed audit row; manual snapshot-restore remains "
                "available via rollback_hint."
            )
        elif not isinstance(snap_root, str) or not snap_root:
            mode = "unsupported"
            ok = True
            execution_performed = False
            message = (
                "Automatic recovery aborted: dump_snapshot_path missing "
                "from audit details after whitelist check. Manual "
                "snapshot-restore remains available via rollback_hint."
            )
        else:
            snapshot_file_path = Path(snap_root) / rel_path
            if not snapshot_file_path.is_file():
                mode = "executed"
                ok = False
                execution_performed = False
                presumed.append(
                    _err(
                        "rollback_snapshot_file_missing",
                        "Snapshot file referenced by audit details is not "
                        f"present on disk: {snapshot_file_path}",
                    )
                )
                message = (
                    "Rollback execution aborted before write: snapshot "
                    f"file {snapshot_file_path} is missing. The "
                    "underlying snapshot tree may have been cleaned up "
                    "or moved. Manual restore is no longer possible "
                    "from this audit entry."
                )
            else:
                # Step a — snapshot baseline text is read once up front
                # so post-rollback verify compares against a stable copy
                # even if the snapshot tree changes mid-flight.
                try:
                    baseline_text = snapshot_file_path.read_text(encoding="utf-8")
                except OSError as exc:
                    mode = "executed"
                    ok = False
                    execution_performed = False
                    presumed.append(
                        _err(
                            "rollback_snapshot_unreadable",
                            f"Snapshot file unreadable: {exc}",
                        )
                    )
                    message = (
                        "Rollback execution aborted before write: snapshot "
                        f"file {snapshot_file_path} could not be read "
                        f"({exc}). No write was attempted."
                    )
                else:
                    rollback_label = f"rollback-{operation_id[:8]}"
                    # Step b — restore via public write-tool (run_write_flow).
                    restore_call = restore_dump_file_from_snapshot(
                        env,
                        rel_path,
                        str(snapshot_file_path),
                        label=rollback_label,
                    )
                    steps.append(
                        _step_from_tool_result(
                            "rollback_restore_dump_file",
                            "mutating",
                            "write.restore_dump_file_from_snapshot",
                            restore_call,
                        )
                    )
                    write_results.append(_tool_result_dict(restore_call))

                    # Step c — refresh last_write_operation so the caller
                    # sees the audit row produced by the restore itself
                    # (the original entry is still preserved in
                    # ``history_entry``).
                    refreshed_last = describe_last_write_operation(env)
                    steps.append(
                        _step_from_tool_result(
                            "rollback_describe_last_write_operation",
                            "audit",
                            "write.describe_last_write_operation",
                            refreshed_last,
                        )
                    )
                    if refreshed_last.ok and isinstance(
                        refreshed_last.payload, dict
                    ):
                        refreshed_data = refreshed_last.payload.get("data")
                        if isinstance(refreshed_data, dict):
                            last_write_operation = dict(refreshed_data)

                    # Step d — mandatory post-rollback verify via the
                    # existing read-only diff_dump_fragment tool.
                    diff_call = diff_dump_fragment(env, rel_path, baseline_text)
                    steps.append(
                        _step_from_tool_result(
                            "rollback_verify_diff_dump_fragment",
                            "verify",
                            "write.diff_dump_fragment",
                            diff_call,
                        )
                    )
                    verify_results.append(_tool_result_dict(diff_call))

                    restore_ok = bool(getattr(restore_call, "ok", False))
                    diff_match = _diff_indicates_match(diff_call)

                    mode = "executed"
                    execution_performed = True
                    if restore_ok and diff_match:
                        ok = True
                        message = (
                            f"Automatic rollback executed for "
                            f"operation_id={operation_id!r} "
                            f"(tool={entry.tool_name!r}, "
                            f"relative_path={rel_path!r}). "
                            "Post-rollback verify confirms the live "
                            "target byte-matches the snapshot baseline."
                        )
                    elif not restore_ok:
                        ok = False
                        message = (
                            "Automatic rollback FAILED at restore step: "
                            f"{getattr(restore_call, 'message', '')}. "
                            "See write_results for the full ToolResult; "
                            "verify_results may be empty if verify was "
                            "still attempted."
                        )
                    else:
                        ok = False
                        message = (
                            "Automatic rollback verify FAILED: "
                            "diff_dump_fragment did not report "
                            "changed=False after restore. The live "
                            "target may differ from the snapshot "
                            "baseline; see verify_results for the diff."
                        )

    return RollbackAssistantResult(
        ok=ok,
        mode=mode,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        operation_id=operation_id,
        operation_found=True,
        execution_performed=execution_performed,
        plan=plan,
        history_entry=entry,
        history_summary=summary,
        rollback_hint=rollback_hint,
        dashboard_summary=_build_dashboard_summary(dash),
        steps=steps,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=plan.suggested_tools,
        suggested_write_tools=plan.suggested_write_tools,
        write_results=write_results,
        verify_results=verify_results,
        last_write_operation=last_write_operation,
        message=message,
    )


def run_rollback_assistant_from_json_file(
    path: str | Path,
    *,
    operation_id: str,
    confirm_execute: bool = False,
) -> RollbackAssistantResult:
    """Like :func:`run_rollback_assistant`, but reads product config from JSON."""
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_assistant(operation_id, f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_assistant(
            operation_id, f"Product config could not be loaded: {exc}"
        )
    return run_rollback_assistant(
        config, operation_id=operation_id, confirm_execute=confirm_execute
    )


# ---------------------------------------------------------------------------
# Public surface listing — convenience for callers introspecting the module.
# ---------------------------------------------------------------------------


__all__ = [
    "RECOVERY_MODES",
    "get_operation_history",
    "get_operation_history_from_json_file",
    "inspect_operation",
    "inspect_operation_from_json_file",
    "run_rollback_assistant",
    "run_rollback_assistant_from_json_file",
]
