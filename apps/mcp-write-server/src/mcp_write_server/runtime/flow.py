"""Single-pipeline helper for write-server operations.

Provides the "preflight → snapshot → operation → verify → audit"
pipeline through which every write-tool of group B is expected to go.
Group B tools are not implemented here — this is the infrastructure
they will build upon.
"""

import uuid
from dataclasses import dataclass
from typing import Callable

from mcp_common import HealthCheckError, PolicyDeniedError
from onec_audit import AuditRecord, append_record
from onec_config import EnvironmentConfig
from onec_policy_engine import WriteIntent

from ..models import ToolResult
from .context import build_runtime_context
from .guards import require_write_preconditions
from .models import WriteRuntimeContext


@dataclass
class WriteFlowArtifacts:
    """Artifacts collected during a single ``run_write_flow`` invocation."""

    backup_snapshot_path: str | None
    dump_snapshot_path: str | None
    audit_path: str | None
    operation_payload: dict | None
    verify_payload: dict | None


OperationCallable = Callable[[WriteRuntimeContext], dict]
VerifyCallable = Callable[[WriteRuntimeContext, dict], dict]


def _runtime_payload(context: WriteRuntimeContext) -> dict:
    """Build the ``runtime`` sub-dict used in every ``ToolResult`` here."""
    return {
        "health_codes": list(context.health_codes),
        "policy": {
            "allowed": context.policy_decision.allowed,
            "reason_code": context.policy_decision.reason_code,
            "require_snapshots": context.policy_decision.require_snapshots,
        },
    }


def _extract_snapshot_path(tool_result: ToolResult) -> str | None:
    """Pull ``payload.data.snapshot_path`` from a snapshot-tool result if present."""
    payload = tool_result.payload or {}
    data = payload.get("data") or {}
    value = data.get("snapshot_path")
    return value if isinstance(value, str) else None


def _append_audit(
    context: WriteRuntimeContext,
    operation_id: str,
    status: str,
    message: str,
    *,
    details: dict | None = None,
) -> str | None:
    """Append an audit record; on I/O failure return ``None`` instead of raising.

    ``tool_name`` is taken from ``context.intent.operation_name`` so that
    audit records are traceable to the exact public tool that initiated
    the flow (e.g. ``update_module_code``), not the generic flow helper.

    ``details`` (Phase 6 / Step 4) is an optional small dict with
    structured artefacts that downstream rollback / inspect helpers
    need: ``backup_snapshot_path`` / ``dump_snapshot_path`` /
    ``relative_path`` / ``operation_name`` /
    ``rollback_supported``. It is free-shape and JSON-serialisable.
    Pre-Step-4 audit lines have no ``details`` key; readers that
    encounter an old line just see ``details=None`` and degrade
    honestly to "automatic recovery not supported for this entry".
    """
    record = AuditRecord(
        operation_id=operation_id,
        tool_name=context.intent.operation_name,
        environment=context.environment.name,
        base_id=context.environment.base_id,
        status=status,
        message=message,
        details=details,
    )
    try:
        return append_record(context.audit_dir, record)
    except OSError:
        return None


# Phase 6 / Step 4 — small whitelist used to mark audit details with
# ``rollback_supported=True`` for the operations the recovery
# assistant can actually execute against. Single source of truth lives
# in :mod:`onec_platform.recovery`; this helper-side mirror exists
# only so the audit row carries a stable hint and downstream code
# does not have to re-derive it. Keep the two in sync by hand for
# now (Step 4 ships exactly two entries).
_ROLLBACK_SUPPORTED_OPERATIONS: frozenset[str] = frozenset(
    {
        "add_catalog_attribute",
        "add_document_attribute",
    }
)


_RELATIVE_PATH_KEYS: tuple[str, ...] = (
    "catalog_relative_path",
    "document_relative_path",
    "module_relative_path",
    "relative_path",
)


def _extract_relative_path(operation_payload: dict) -> str | None:
    """Best-effort lookup of the single mutated file inside a write-flow
    operation payload.

    The known mutating tools record the relative path under one of a
    handful of keys (``catalog_relative_path``,
    ``document_relative_path``, ``module_relative_path``,
    ``relative_path``). Anything else returns ``None`` and the audit
    row simply omits the field — recovery degrades honestly to
    advisory-only.
    """
    for key in _RELATIVE_PATH_KEYS:
        value = operation_payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def run_write_flow(
    environment: EnvironmentConfig,
    intent: WriteIntent,
    *,
    label: str,
    operation_callable: OperationCallable,
    verify_callable: VerifyCallable,
) -> ToolResult:
    """Run preflight → snapshot → operation → verify → audit for one write op.

    Never raises: every failure path returns a ``ToolResult(ok=False, ...)``
    with a ``stage`` marker in ``payload.data`` and whatever artefacts
    (snapshot paths, operation_id, audit_path) were produced before the
    failure.
    """
    # Lazy import to break circular dependency with `.tools`
    # (tools.py imports from .runtime; .runtime.flow reuses snapshot tools).
    from ..tools import create_backup_snapshot, create_dump_snapshot

    context = build_runtime_context(environment, intent)
    runtime_payload = _runtime_payload(context)

    # Step 2 — preflight
    try:
        require_write_preconditions(context)
    except (PolicyDeniedError, HealthCheckError) as exc:
        return ToolResult(
            ok=False,
            tool_name="run_write_flow",
            message=str(exc),
            payload={
                "runtime": runtime_payload,
                "data": {"stage": "preflight"},
            },
        )

    # Step 3 — snapshots (if policy requires)
    backup_snapshot_path: str | None = None
    dump_snapshot_path: str | None = None

    if context.policy_decision.require_snapshots:
        backup_result = create_backup_snapshot(environment, label)
        if not backup_result.ok:
            return ToolResult(
                ok=False,
                tool_name="run_write_flow",
                message=backup_result.message,
                payload={
                    "runtime": runtime_payload,
                    "data": {
                        "stage": "backup_snapshot",
                        "backup_snapshot_path": _extract_snapshot_path(
                            backup_result
                        ),
                    },
                },
            )
        backup_snapshot_path = _extract_snapshot_path(backup_result)

        dump_result = create_dump_snapshot(environment, label)
        if not dump_result.ok:
            return ToolResult(
                ok=False,
                tool_name="run_write_flow",
                message=dump_result.message,
                payload={
                    "runtime": runtime_payload,
                    "data": {
                        "stage": "dump_snapshot",
                        "backup_snapshot_path": backup_snapshot_path,
                        "dump_snapshot_path": _extract_snapshot_path(
                            dump_result
                        ),
                    },
                },
            )
        dump_snapshot_path = _extract_snapshot_path(dump_result)

    operation_id = str(uuid.uuid4())

    # Step 4 — operation
    try:
        operation_payload = operation_callable(context)
    except Exception as exc:  # noqa: BLE001 — tool boundary, must not raise
        audit_path = _append_audit(
            context,
            operation_id,
            "error",
            f"Write operation failed: {exc}",
        )
        return ToolResult(
            ok=False,
            tool_name="run_write_flow",
            message=f"Write operation failed: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "stage": "operation",
                    "operation_id": operation_id,
                    "backup_snapshot_path": backup_snapshot_path,
                    "dump_snapshot_path": dump_snapshot_path,
                    "audit_path": audit_path,
                },
            },
        )

    # Step 5 — verify
    try:
        verify_payload = verify_callable(context, operation_payload)
    except Exception as exc:  # noqa: BLE001 — tool boundary, must not raise
        audit_path = _append_audit(
            context,
            operation_id,
            "error",
            f"Write verify failed: {exc}",
        )
        return ToolResult(
            ok=False,
            tool_name="run_write_flow",
            message=f"Write verify failed: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "stage": "verify",
                    "operation_id": operation_id,
                    "backup_snapshot_path": backup_snapshot_path,
                    "dump_snapshot_path": dump_snapshot_path,
                    "audit_path": audit_path,
                    "operation_payload": operation_payload,
                },
            },
        )

    # Step 6 — audit success
    operation_name = context.intent.operation_name
    relative_path = (
        _extract_relative_path(operation_payload)
        if isinstance(operation_payload, dict)
        else None
    )
    success_details: dict = {
        "operation_name": operation_name,
        "rollback_supported": operation_name in _ROLLBACK_SUPPORTED_OPERATIONS,
    }
    if backup_snapshot_path is not None:
        success_details["backup_snapshot_path"] = backup_snapshot_path
    if dump_snapshot_path is not None:
        success_details["dump_snapshot_path"] = dump_snapshot_path
    if relative_path is not None:
        success_details["relative_path"] = relative_path
    audit_path = _append_audit(
        context,
        operation_id,
        "ok",
        "Write flow completed successfully.",
        details=success_details,
    )

    # Step 7 — final success ToolResult
    return ToolResult(
        ok=True,
        tool_name="run_write_flow",
        message="Write flow completed successfully.",
        payload={
            "runtime": runtime_payload,
            "data": {
                "stage": "completed",
                "operation_id": operation_id,
                "backup_snapshot_path": backup_snapshot_path,
                "dump_snapshot_path": dump_snapshot_path,
                "audit_path": audit_path,
                "operation_payload": operation_payload,
                "verify_payload": verify_payload,
            },
        },
    )
