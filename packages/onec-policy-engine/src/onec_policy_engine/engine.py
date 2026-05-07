"""Policy / preflight engine for write operations in the 1C Agent Platform.

Two invocation modes are supported:

- **New mode** — ``check_write_allowed(environment: EnvironmentConfig,
  intent: WriteIntent)`` — full policy / preflight decision against a
  structured environment and a described write intent.
- **Legacy mode** — ``check_write_allowed(environment_name: str,
  allow_write: bool)`` — preserved strictly for the existing skeleton
  selfcheck in ``scripts/dev/selfcheck.py``. Will be removed once the
  selfcheck migrates to the new form.

Four categories of ``operation_name`` are recognised in new mode:

1. **Phase 2 mutating** (``_MUTATING_OPERATIONS``) — the original
   write-tools of Write MVP. ``reason_code="allowed_mutating"``.
2. **Phase 2 non-mutating support** (``_NON_MUTATING_SUPPORT_OPERATIONS``)
   — preflight, snapshots, verify, audit helpers of Write MVP.
   ``reason_code="allowed_non_mutating"``.
3. **Phase 3 metadata mutating** (``_METADATA_MUTATING_OPERATIONS``) —
   metadata-oriented write operations planned in Phase 3
   (create_catalog, add_document_attribute, append_module_method, …).
   ``reason_code="allowed_metadata_mutating"``.
4. **Phase 3 metadata support / verification**
   (``_METADATA_SUPPORT_OPERATIONS``) — read-only verification and
   diagnostics for metadata changes (verify_attribute_exists,
   diff_dump_fragment, …). ``reason_code="allowed_metadata_support"``.

Anything else is refused as ``unknown_intent`` (fail-closed).

**Phase 4 / Intelligence operations are *not* routed through this
engine.** ``mcp-intelligence-server`` tools are read-only by
construction (Phase 4 guardrail): they never mutate state, never
call ``run_write_flow``, never write an audit record. Their
contract is enforced by the absence of any import of this engine
from the intelligence package, mirroring the existing pattern of
``mcp-read-server``. This keeps the write-policy surface narrow and
conceptually consistent: ``check_write_allowed`` decides **write**
operations, not read ones. As a side effect the ``unknown_intent``
branch below acts as a free safety net — any intelligence
operation name that ever leaks into a write-side ``WriteIntent`` is
rejected fail-closed.
See ``apps/mcp-intelligence-server/README.md`` for the mirror
statement on the intelligence side.
"""

from onec_config import EnvironmentConfig

from .models import PolicyDecision, WriteIntent

_MUTATING_OPERATIONS = frozenset(
    {
        "apply_config_from_files",
        "update_database_configuration",
        "create_common_module",
        "update_module_code",
        "add_catalog_attribute",
        # Phase 6 / Step 4 — single-file restore from snapshot.
        # Mutating: writes a single dump file. Inherits the same
        # require_snapshots / preflight / verify / audit discipline
        # as every other mutating operation.
        "restore_dump_file_from_snapshot",
    }
)

_NON_MUTATING_SUPPORT_OPERATIONS = frozenset(
    {
        "check_write_preconditions",
        "create_backup_snapshot",
        "create_dump_snapshot",
        "verify_metadata_change",
        "verify_module_contains",
        "verify_object_exists",
        "write_audit_record",
        "describe_last_write_operation",
        "prepare_rollback_hint",
    }
)

_METADATA_MUTATING_OPERATIONS = frozenset(
    {
        "create_catalog",
        "create_document",
        "create_information_register",
        "create_common_module_from_template",
        "create_role",
        "add_document_attribute",
        "add_tabular_section",
        "add_form_attribute",
        "change_attribute_type",
        "create_managed_form",
        "add_form_element",
        "bind_form_handler",
        "append_module_method",
        "replace_module_method_body",
    }
)

_METADATA_SUPPORT_OPERATIONS = frozenset(
    {
        "verify_attribute_exists",
        "verify_form_exists",
        "verify_module_method_exists",
        "verify_metadata_shape",
        "diff_dump_fragment",
    }
)

_PRODUCTION_MARKERS = ("prod", "production")

_PRODUCTION_BLOCKED_REASON = (
    "Write operations are forbidden for production-like environments by default."
)
_WRITE_NOT_ALLOWED_REASON = "Write operations require allow_write=True."


def _contains_production_marker(*fields: str) -> bool:
    """Return True if any non-empty field contains a production marker."""
    for value in fields:
        if not value:
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in _PRODUCTION_MARKERS):
            return True
    return False


def check_write_allowed(environment, intent=None) -> PolicyDecision:
    """Decide whether a write-side operation is allowed.

    See module docstring for supported invocation modes and categories.
    """
    if isinstance(environment, str) and isinstance(intent, bool):
        return _legacy_check(environment, intent)
    return _new_check(environment, intent)


def _legacy_check(environment_name: str, allow_write: bool) -> PolicyDecision:
    if _contains_production_marker(environment_name):
        return PolicyDecision(
            allowed=False,
            reason=_PRODUCTION_BLOCKED_REASON,
            reason_code="production_blocked",
            require_snapshots=False,
        )
    if not allow_write:
        return PolicyDecision(
            allowed=False,
            reason=_WRITE_NOT_ALLOWED_REASON,
            reason_code="write_not_allowed",
            require_snapshots=False,
        )
    return PolicyDecision(
        allowed=True,
        reason="Legacy write check allowed.",
        reason_code="allowed_legacy",
        require_snapshots=True,
    )


def _new_check(
    environment: EnvironmentConfig, intent: WriteIntent
) -> PolicyDecision:
    if _contains_production_marker(
        environment.name,
        environment.base_id,
        environment.publication_name,
        environment.http_base_url,
    ):
        return PolicyDecision(
            allowed=False,
            reason=_PRODUCTION_BLOCKED_REASON,
            reason_code="production_blocked",
            require_snapshots=False,
        )
    if not environment.allow_write:
        return PolicyDecision(
            allowed=False,
            reason=_WRITE_NOT_ALLOWED_REASON,
            reason_code="write_not_allowed",
            require_snapshots=False,
        )
    if intent.operation_name in _MUTATING_OPERATIONS:
        return PolicyDecision(
            allowed=True,
            reason="Mutating write operation allowed; snapshots are required.",
            reason_code="allowed_mutating",
            require_snapshots=True,
        )
    if intent.operation_name in _NON_MUTATING_SUPPORT_OPERATIONS:
        return PolicyDecision(
            allowed=True,
            reason="Non-mutating write-side support operation allowed.",
            reason_code="allowed_non_mutating",
            require_snapshots=False,
        )
    if intent.operation_name in _METADATA_MUTATING_OPERATIONS:
        return PolicyDecision(
            allowed=True,
            reason=(
                "Metadata mutating operation allowed; "
                "snapshots are required."
            ),
            reason_code="allowed_metadata_mutating",
            require_snapshots=True,
        )
    if intent.operation_name in _METADATA_SUPPORT_OPERATIONS:
        return PolicyDecision(
            allowed=True,
            reason="Metadata verification/support operation allowed.",
            reason_code="allowed_metadata_support",
            require_snapshots=False,
        )
    return PolicyDecision(
        allowed=False,
        reason=f"Unknown write intent: {intent.operation_name}",
        reason_code="unknown_intent",
        require_snapshots=False,
    )
