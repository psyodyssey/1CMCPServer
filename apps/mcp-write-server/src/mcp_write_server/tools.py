"""Write-server tool implementations."""

import difflib
import json
import re
import shutil
import string
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

from mcp_common import HealthCheckError, PlatformError, PolicyDeniedError
from mcp_read_server.runtime import (
    fetch_json_from_environment,
    find_files_by_pattern,
    read_dump_file,
    read_text_file,
    resolve_dump_path,
)
from onec_audit import AuditRecord, append_record, read_last_record
from onec_config import EnvironmentConfig
from onec_policy_engine import WriteIntent
from onec_process_runner import ProcessRunRequest, run_process

from .models import ToolResult
from .runtime import (
    build_runtime_context,
    require_write_preconditions,
    run_write_flow,
)
from .runtime.binary_dispatch import (
    BINARY_DEFAULT_TIMEOUT_SECONDS,
    binary_backed_payload_fields,
    binary_backed_render_failure_fields,
    binary_backed_start_failure_fields,
    excerpt as _excerpt,
    is_binary_subprocess_successful,
    render_command_template,
    stub_honest_mode_fields,
)
from .runtime.dump_ops import run_stub_apply_process
from .runtime.metadata_ops import (
    add_attribute_to_form_attributes_block,
    append_method_to_module,
    build_attribute_fragment,
    build_form_fragment,
    build_module_method_fragment,
    find_form_element,
    form_has_attribute,
    get_or_create_form_attributes_block,
    insert_fragment_into_named_block,
    module_contains_method,
    parse_xml_file,
    patch_text_file,
    patch_xml_file,
    write_xml_file,
)

_SAFE_LABEL_CHARS = frozenset(string.ascii_letters + string.digits + "-_")
_MODULE_NAME_RE = re.compile(r"\w+")
_ALLOWED_ATTR_TYPES = frozenset({"String", "Number", "Date"})

# Tool-specific placeholder whitelists for the three binary-backed
# write-tools. After Parallel Track A / Step 4 the *mechanics*
# (excerpt cap, default timeout, render engine, payload field
# assembly) are unified in :mod:`runtime.binary_dispatch`; the
# whitelists below are deliberately **not** unified — each tool
# has its own intentional placeholder surface, and that intent
# stays explicit at the call site.

# Phase 6 / Step 2 — whitelist of placeholders that
# ``onec_dumpcfg_command_template`` may reference.
_DUMPCFG_TEMPLATE_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "binary_path",
        "output_path",
        "base_path",
        "base_id",
        "publication_name",
        "http_base_url",
    }
)

# Parallel Track A / Step 2 — whitelist of placeholders that
# ``onec_applycfg_command_template`` may reference. Mirrors the
# DumpCfg whitelist with one substitution: ``{output_path}`` →
# ``{source_dump_path}`` (apply reads the dump, dumpcfg writes it).
_APPLYCFG_TEMPLATE_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "binary_path",
        "source_dump_path",
        "base_path",
        "base_id",
        "publication_name",
        "http_base_url",
    }
)

# Parallel Track A / Step 3 — whitelist of placeholders that
# ``onec_updatedb_command_template`` may reference. UpdateDBCfg
# operates on the live infobase against the previously-applied
# config; it does not need ``output_path`` (nothing is dumped) or
# ``source_dump_path`` (nothing is read from a source tree). The
# whitelist is therefore a tighter subset than dumpcfg / applycfg.
_UPDATEDB_TEMPLATE_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "binary_path",
        "base_path",
        "base_id",
        "publication_name",
        "http_base_url",
    }
)


def ping() -> ToolResult:
    """Return a liveness marker for the write server."""
    return ToolResult(
        ok=True,
        tool_name="ping",
        message="mcp-write-server is alive.",
        payload={"status": "ok"},
    )


def _safe_snapshot_label(label: str) -> str:
    """Sanitize ``label`` for use in a snapshot directory name."""
    sanitized = "".join(c if c in _SAFE_LABEL_CHARS else "_" for c in label)
    return sanitized if sanitized else "snapshot"


def _runtime_payload(context) -> dict:
    """Build the ``runtime`` sub-dict for tool payloads."""
    return {
        "health_codes": list(context.health_codes),
        "policy": {
            "allowed": context.policy_decision.allowed,
            "reason_code": context.policy_decision.reason_code,
            "require_snapshots": context.policy_decision.require_snapshots,
        },
    }


def _with_tool_name(result: ToolResult, tool_name: str) -> ToolResult:
    """Return a copy of ``result`` with ``tool_name`` replaced."""
    return ToolResult(
        ok=result.ok,
        tool_name=tool_name,
        message=result.message,
        payload=result.payload,
    )


def check_write_preconditions(
    environment: EnvironmentConfig,
    intent: WriteIntent,
) -> ToolResult:
    """Verify that write-side preconditions hold for ``intent`` on ``environment``."""
    context = build_runtime_context(environment, intent)
    runtime_payload = _runtime_payload(context)
    data_payload = {"audit_dir": context.audit_dir}
    try:
        require_write_preconditions(context)
    except (PolicyDeniedError, HealthCheckError) as exc:
        return ToolResult(
            ok=False,
            tool_name="check_write_preconditions",
            message=str(exc),
            payload={"runtime": runtime_payload, "data": data_payload},
        )
    return ToolResult(
        ok=True,
        tool_name="check_write_preconditions",
        message="Write preconditions satisfied.",
        payload={"runtime": runtime_payload, "data": data_payload},
    )


def create_backup_snapshot(
    environment: EnvironmentConfig,
    label: str,
) -> ToolResult:
    """Create a filesystem snapshot of ``environment.base_path`` via ``shutil.copytree``."""
    intent = WriteIntent("create_backup_snapshot", label)
    context = build_runtime_context(environment, intent)
    runtime_payload = _runtime_payload(context)
    try:
        require_write_preconditions(context)
    except (PolicyDeniedError, HealthCheckError) as exc:
        return ToolResult(
            ok=False,
            tool_name="create_backup_snapshot",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )

    base_path = Path(environment.base_path)
    snapshots_root = base_path.parent / "_snapshots"
    safe_label = _safe_snapshot_label(label)
    target_dir = snapshots_root / f"backup-{environment.base_id}-{safe_label}"

    if target_dir.exists():
        return ToolResult(
            ok=False,
            tool_name="create_backup_snapshot",
            message="Backup snapshot already exists.",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "backup",
                    "snapshot_path": str(target_dir),
                },
            },
        )

    try:
        snapshots_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(base_path, target_dir)
    except (OSError, shutil.Error) as exc:
        return ToolResult(
            ok=False,
            tool_name="create_backup_snapshot",
            message=f"Failed to create backup snapshot: {exc}",
            payload={"runtime": runtime_payload},
        )

    return ToolResult(
        ok=True,
        tool_name="create_backup_snapshot",
        message="Backup snapshot created successfully.",
        payload={
            "runtime": runtime_payload,
            "data": {
                "snapshot_type": "backup",
                "snapshot_path": str(target_dir),
            },
        },
    )


def _render_dumpcfg_command(
    template: list[str],
    *,
    environment: EnvironmentConfig,
    binary_path: str,
    output_path: str,
) -> list[str]:
    """Render an operator-declared dumpcfg argv template.

    Thin tool-specific wrapper around the shared
    :func:`runtime.binary_dispatch.render_command_template`
    (Track A / Step 4). Builds the dumpcfg-specific
    ``substitutions`` dict; the rest — per-item substitution
    discipline, fail-closed on unknown placeholder, error message
    naming the config field — lives in the shared helper.
    """
    return render_command_template(
        template,
        substitutions={
            "binary_path": binary_path,
            "output_path": output_path,
            "base_path": environment.base_path,
            "base_id": environment.base_id,
            "publication_name": environment.publication_name,
            "http_base_url": environment.http_base_url,
        },
        allowed_placeholders=_DUMPCFG_TEMPLATE_PLACEHOLDERS,
        template_field_name="onec_dumpcfg_command_template",
    )


def _create_dump_snapshot_stub(
    environment: EnvironmentConfig,
    label: str,
    runtime_payload: dict,
    target_dir: Path,
    snapshots_root: Path,
) -> ToolResult:
    """Original Phase 2 / Step 5 stub-backed dump snapshot path.

    Backward compatibility for any environment that does not declare
    both ``onec_binary_path`` and ``onec_dumpcfg_command_template``.
    Stub side-effects (``dump-created.txt`` marker file +
    ``dump-meta.json``) are unchanged.

    Track A / Step 4 — payload discipline unification: every branch
    of this stub now emits the same six honest-mode fields as
    :func:`apply_config_from_files` and
    :func:`update_database_configuration` stub branches via
    :func:`stub_honest_mode_fields`. Stub-mode-only fields
    (``mode='stub'`` / ``binary_invoked=False`` / explicit ``None``
    for the binary-backed-only fields) sit alongside the
    dump-snapshot-specific extras (``snapshot_type`` /
    ``snapshot_path``).
    """
    python_exe = shutil.which("python")
    if python_exe is None:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message="Python interpreter not found in PATH for dump snapshot stub.",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    **stub_honest_mode_fields(),
                },
            },
        )

    try:
        snapshots_root.mkdir(parents=True, exist_ok=True)
        target_dir.mkdir()
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=f"Failed to prepare dump snapshot directory: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    **stub_honest_mode_fields(),
                },
            },
        )

    marker_path = target_dir / "dump-created.txt"
    process_result = run_process(
        ProcessRunRequest(
            command=[
                python_exe,
                "-c",
                "import sys; open(sys.argv[1], 'w', encoding='utf-8').write('ok')",
                str(marker_path),
            ],
            timeout_seconds=10,
        )
    )
    if not process_result.completed or process_result.exit_code != 0:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message="Dump snapshot process failed.",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    "snapshot_path": str(target_dir),
                    "completed": process_result.completed,
                    "stderr": process_result.stderr,
                    **stub_honest_mode_fields(),
                },
            },
        )

    meta = {
        "base_id": environment.base_id,
        "label": label,
        "source_dump_path": environment.dump_path,
    }
    try:
        (target_dir / "dump-meta.json").write_text(
            json.dumps(meta, ensure_ascii=False), encoding="utf-8"
        )
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=f"Failed to write dump meta: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    "snapshot_path": str(target_dir),
                    **stub_honest_mode_fields(),
                },
            },
        )

    return ToolResult(
        ok=True,
        tool_name="create_dump_snapshot",
        message="Dump snapshot created successfully.",
        payload={
            "runtime": runtime_payload,
            "data": {
                "snapshot_type": "dump",
                "snapshot_path": str(target_dir),
                **stub_honest_mode_fields(),
            },
        },
    )


def _create_dump_snapshot_binary_backed(
    environment: EnvironmentConfig,
    label: str,
    runtime_payload: dict,
    target_dir: Path,
    snapshots_root: Path,
) -> ToolResult:
    """Phase 6 / Step 2 binary-backed dump snapshot path.

    Activated when both ``environment.onec_binary_path`` and
    ``environment.onec_dumpcfg_command_template`` are set. Renders
    the operator-declared argv template with whitelisted
    placeholders, runs the subprocess via
    :func:`onec_process_runner.run_process`, and reports the result.

    Track A / Step 4 — payload discipline unification: every branch
    now emits the same six honest-mode fields as
    :func:`apply_config_from_files` /
    :func:`update_database_configuration` binary-backed branches
    via :func:`binary_backed_render_failure_fields` /
    :func:`binary_backed_start_failure_fields` /
    :func:`binary_backed_payload_fields`. Tool-specific extras
    (``snapshot_type`` / ``snapshot_path``) sit alongside.

    There is **no** silent fallback to the stub branch from here:
    once the operator declared a binary-backed contract, a runtime
    failure stays a real failure. Fallback only happens at the
    dispatch level — when one of the two config fields is missing.
    """
    binary_path = environment.onec_binary_path
    template = environment.onec_dumpcfg_command_template
    # Defensive: dispatch already checked these, but the inner helper
    # must not assume.
    if not binary_path or not template:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=(
                "Internal: binary-backed branch entered without both "
                "onec_binary_path and onec_dumpcfg_command_template set."
            ),
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    **binary_backed_render_failure_fields(),
                },
            },
        )

    try:
        snapshots_root.mkdir(parents=True, exist_ok=True)
        target_dir.mkdir()
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=f"Failed to prepare dump snapshot directory: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    **binary_backed_render_failure_fields(),
                },
            },
        )

    try:
        command = _render_dumpcfg_command(
            template,
            environment=environment,
            binary_path=binary_path,
            output_path=str(target_dir),
        )
    except ValueError as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=str(exc),
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    "snapshot_path": str(target_dir),
                    **binary_backed_render_failure_fields(),
                },
            },
        )

    try:
        process_result = run_process(
            ProcessRunRequest(
                command=command,
                timeout_seconds=BINARY_DEFAULT_TIMEOUT_SECONDS,
                capture_output=True,
                text=True,
            )
        )
    except PlatformError as exc:
        # ProcessExecutionError is a PlatformError; missing binary etc.
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=f"Failed to start dumpcfg subprocess: {exc}",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    "snapshot_path": str(target_dir),
                    **binary_backed_start_failure_fields(command),
                },
            },
        )

    binary_data = {
        "snapshot_type": "dump",
        "snapshot_path": str(target_dir),
        **binary_backed_payload_fields(command, process_result),
    }

    if not is_binary_subprocess_successful(binary_data):
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=(
                f"dumpcfg subprocess failed (exit_code="
                f"{process_result.exit_code}, "
                f"completed={process_result.completed})."
            ),
            payload={"runtime": runtime_payload, "data": binary_data},
        )

    meta = {
        "base_id": environment.base_id,
        "label": label,
        "source_dump_path": environment.dump_path,
        "mode": "binary-backed",
        "command_preview": list(command),
    }
    try:
        (target_dir / "dump-meta.json").write_text(
            json.dumps(meta, ensure_ascii=False), encoding="utf-8"
        )
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=f"Failed to write dump meta: {exc}",
            payload={"runtime": runtime_payload, "data": binary_data},
        )

    return ToolResult(
        ok=True,
        tool_name="create_dump_snapshot",
        message="Dump snapshot created successfully (binary-backed).",
        payload={"runtime": runtime_payload, "data": binary_data},
    )


def create_dump_snapshot(
    environment: EnvironmentConfig,
    label: str,
) -> ToolResult:
    """Create a dump snapshot directory.

    Two modes, dispatched on environment configuration:

    - **stub** (Phase 2 / Step 5 default) — used when at least one of
      ``environment.onec_binary_path`` /
      ``environment.onec_dumpcfg_command_template`` is missing.
      Identical to the legacy behaviour: marker file + dump-meta.json,
      exercised through ``onec-process-runner`` + preflight + snapshot
      path. ``payload.data.mode = "stub"``,
      ``payload.data.binary_invoked = False``.
    - **binary-backed** (Phase 6 / Step 2) — used when **both** fields
      are set. Renders the operator-declared argv template with a
      whitelisted set of placeholders
      (:data:`_DUMPCFG_TEMPLATE_PLACEHOLDERS`), runs the subprocess
      via :func:`onec_process_runner.run_process` with a fixed
      :data:`_DUMPCFG_DEFAULT_TIMEOUT_SECONDS` cap, and reports the
      outcome. ``payload.data.mode = "binary-backed"``;
      ``binary_invoked``, ``exit_code``, ``command_preview``,
      ``stdout_excerpt``, ``stderr_excerpt`` all populated.

    There is **no** silent fallback from binary-backed to stub on
    runtime failure — once the operator declared a binary-backed
    contract, a non-zero exit stays an honest failure. Fallback only
    applies when the contract itself is incomplete (one of the two
    fields is unset).

    External contract preserved: ``ToolResult`` shape is unchanged;
    callers reading ``payload.data.snapshot_path`` keep working in
    both modes.
    """
    intent = WriteIntent("create_dump_snapshot", label)
    context = build_runtime_context(environment, intent)
    runtime_payload = _runtime_payload(context)
    try:
        require_write_preconditions(context)
    except (PolicyDeniedError, HealthCheckError) as exc:
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message=str(exc),
            payload={"runtime": runtime_payload},
        )

    dump_path = Path(environment.dump_path)
    snapshots_root = dump_path.parent / "_snapshots"
    safe_label = _safe_snapshot_label(label)
    target_dir = snapshots_root / f"dump-{environment.base_id}-{safe_label}"

    if target_dir.exists():
        return ToolResult(
            ok=False,
            tool_name="create_dump_snapshot",
            message="Dump snapshot already exists.",
            payload={
                "runtime": runtime_payload,
                "data": {
                    "snapshot_type": "dump",
                    "snapshot_path": str(target_dir),
                },
            },
        )

    if environment.onec_binary_path and environment.onec_dumpcfg_command_template:
        return _create_dump_snapshot_binary_backed(
            environment,
            label,
            runtime_payload,
            target_dir,
            snapshots_root,
        )
    return _create_dump_snapshot_stub(
        environment,
        label,
        runtime_payload,
        target_dir,
        snapshots_root,
    )


def _render_applycfg_command(
    template: list[str],
    *,
    environment: EnvironmentConfig,
    binary_path: str,
    source_dump_path: str,
) -> list[str]:
    """Render an operator-declared apply argv template.

    Thin tool-specific wrapper around the shared
    :func:`runtime.binary_dispatch.render_command_template`
    (Track A / Step 4). Builds the apply-specific
    ``substitutions`` dict; the rest — per-item substitution
    discipline, fail-closed on unknown placeholder, error message
    naming the config field — lives in the shared helper.
    """
    return render_command_template(
        template,
        substitutions={
            "binary_path": binary_path,
            "source_dump_path": source_dump_path,
            "base_path": environment.base_path,
            "base_id": environment.base_id,
            "publication_name": environment.publication_name,
            "http_base_url": environment.http_base_url,
        },
        allowed_placeholders=_APPLYCFG_TEMPLATE_PLACEHOLDERS,
        template_field_name="onec_applycfg_command_template",
    )


def _build_apply_stub_callables(source_dump_path: str):
    """Return ``(operation, verify)`` callables for the legacy stub
    apply branch.

    Phase 2 / Step 7 behaviour preserved verbatim: stub-process apply
    writes ``apply-stub.txt`` + ``apply-meta.json`` inside
    ``source_dump_path``. Verify confirms the marker exists.

    Track A / Step 4 — payload discipline: the unified six
    honest-mode fields (``mode='stub'``, ``binary_invoked=False``,
    explicit ``None`` for the binary-backed-only fields) come from
    :func:`stub_honest_mode_fields`, so this helper and the
    update-db / dump-snapshot stub branches now share one source
    of truth for the stub-mode shape.
    """

    def operation(ctx):
        # ``run_stub_apply_process`` already returns the stub
        # operation payload (``mode="stub-process-apply"``,
        # ``source_dump_path``, ``marker_path``). Spread it first,
        # then overlay the unified honest-mode fields so the
        # Track A / Step 4 mode value (``"stub"``) wins.
        stub_payload = run_stub_apply_process(source_dump_path)
        return {
            **stub_payload,
            **stub_honest_mode_fields(),
        }

    def verify(ctx, operation_payload):
        marker_path = Path(operation_payload["marker_path"])
        if not marker_path.exists():
            raise AssertionError(f"Stub apply marker missing: {marker_path}")
        return {
            "verified": True,
            "mode": operation_payload["mode"],
            "marker_exists": True,
        }

    return operation, verify


def _build_apply_binary_backed_callables(
    command: list[str],
    source_dump_path: str,
):
    """Return ``(operation, verify)`` callables for the binary-backed
    apply branch.

    Track A / Step 4 — payload discipline unification: operation
    builds its dict via :func:`binary_backed_payload_fields` (the
    shared helper that produces the unified six honest-mode fields
    plus the ``completed`` flag) merged with the apply-specific
    ``source_dump_path`` extra. Verify uses
    :func:`is_binary_subprocess_successful` for the success check
    so the same predicate applies to all three binary-backed
    write-tools.

    Operator-facing semantics unchanged: operator-declared argv
    runs through :func:`onec_process_runner.run_process` with a
    fixed :data:`BINARY_DEFAULT_TIMEOUT_SECONDS` cap; runtime
    failure (non-zero exit / non-completed / unstartable
    subprocess) stays an honest failure with no silent stub
    fallback.
    """

    def operation(ctx):
        try:
            process_result = run_process(
                ProcessRunRequest(
                    command=command,
                    timeout_seconds=BINARY_DEFAULT_TIMEOUT_SECONDS,
                    capture_output=True,
                    text=True,
                )
            )
        except PlatformError as exc:
            # Subprocess could not be started (binary missing, etc).
            # Re-raise so run_write_flow turns this into a
            # stage='operation' failure. ``binary_invoked`` is
            # honestly False here because no PID was ever produced.
            raise RuntimeError(
                f"Failed to start applycfg subprocess: {exc}"
            ) from exc
        return {
            "applied": (
                process_result.completed and process_result.exit_code == 0
            ),
            "source_dump_path": source_dump_path,
            **binary_backed_payload_fields(command, process_result),
        }

    def verify(ctx, operation_payload):
        if not is_binary_subprocess_successful(operation_payload):
            raise AssertionError(
                "applycfg subprocess failed: exit_code="
                f"{operation_payload.get('exit_code')}, completed="
                f"{operation_payload.get('completed')}"
            )
        return {
            "verified": True,
            "mode": operation_payload["mode"],
            "binary_invoked": operation_payload["binary_invoked"],
            "exit_code": operation_payload["exit_code"],
        }

    return operation, verify


def apply_config_from_files(
    environment: EnvironmentConfig,
    source_dump_path: str,
    label: str = "apply-config",
) -> ToolResult:
    """Apply a configuration from ``source_dump_path`` via the write-flow pipeline.

    Two modes, dispatched on environment configuration; the public
    contract (``ToolResult`` shape, ``run_write_flow`` discipline,
    audit, snapshots) is identical between them. Mirror of
    :func:`create_dump_snapshot`'s dual-mode dispatcher (Phase 6 /
    Step 2):

    - **stub** (Phase 2 / Step 7 default; backward-compat) — used
      when at least one of ``environment.onec_binary_path`` /
      ``environment.onec_applycfg_command_template`` is missing.
      Identical to the legacy stub-process apply: writes
      ``apply-stub.txt`` + ``apply-meta.json`` inside
      ``source_dump_path`` through ``onec_process_runner``.
      ``operation_payload.mode = "stub"``,
      ``operation_payload.binary_invoked = False``.
    - **binary-backed** (Parallel Track A / Step 2) — used when
      **both** fields are set. Renders the operator-declared argv
      template with a whitelisted set of placeholders
      (:data:`_APPLYCFG_TEMPLATE_PLACEHOLDERS`), runs the subprocess
      via :func:`onec_process_runner.run_process` with a fixed
      :data:`_APPLYCFG_DEFAULT_TIMEOUT_SECONDS` cap, and reports
      the outcome.
      ``operation_payload.mode = "binary-backed"``,
      ``operation_payload.binary_invoked`` is ``True`` once a PID
      was produced (``False`` only when the subprocess could not be
      started or the unknown-placeholder pre-flight rejected the
      call before spawning anything).

    There is **no** silent fallback from binary-backed to stub on
    runtime failure. Once the operator declares the binary-backed
    contract by setting both fields, a non-zero exit / non-completed
    subprocess / unstartable binary stays an honest failure
    (``ok=False`` with the binary-backed payload preserved).
    Fallback only happens at **dispatch** time — when the contract
    is incomplete (one or both fields missing).

    External contract preserved: ``ToolResult`` shape is unchanged;
    callers reading ``payload.data.operation_payload`` keep working
    in both modes; the Track A / Step 2 mode marker fields are
    additive, never replacing legacy fields.
    """
    binary_path = environment.onec_binary_path
    applycfg_template = environment.onec_applycfg_command_template
    use_binary_backed = bool(binary_path) and bool(applycfg_template)

    intent = WriteIntent("apply_config_from_files", source_dump_path)

    if use_binary_backed:
        # Render the argv template up-front. Unknown-placeholder /
        # malformed-template fail-closed BEFORE the flow starts so
        # we never take snapshots / write audit rows for a call
        # that cannot even spawn. ``binary_invoked`` is honestly
        # False because no PID was produced.
        try:
            command = _render_applycfg_command(
                applycfg_template,
                environment=environment,
                binary_path=binary_path,
                source_dump_path=source_dump_path,
            )
        except ValueError as exc:
            return ToolResult(
                ok=False,
                tool_name="apply_config_from_files",
                message=str(exc),
                payload={
                    "data": {
                        "source_dump_path": source_dump_path,
                        **binary_backed_render_failure_fields(),
                    }
                },
            )
        operation, verify = _build_apply_binary_backed_callables(
            command, source_dump_path
        )
    else:
        operation, verify = _build_apply_stub_callables(source_dump_path)

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "apply_config_from_files")


def update_module_code(
    environment: EnvironmentConfig,
    module_relative_path: str,
    new_text: str,
    label: str = "update-module-code",
) -> ToolResult:
    """Overwrite the contents of a module file inside the environment's dump root."""
    if not new_text or not new_text.strip():
        return ToolResult(
            ok=False,
            tool_name="update_module_code",
            message="new_text must be a non-empty, non-whitespace string.",
            payload={"data": {"target": module_relative_path}},
        )

    intent = WriteIntent("update_module_code", module_relative_path)

    def operation(ctx):
        target = Path(ctx.environment.dump_path) / module_relative_path
        if not target.is_file():
            raise FileNotFoundError(
                f"Module not found in dump: {module_relative_path}"
            )
        target.write_text(new_text, encoding="utf-8")
        return {
            "changed": True,
            "target": module_relative_path,
            "text_length": len(new_text),
        }

    def verify(ctx, operation_payload):
        target = Path(ctx.environment.dump_path) / module_relative_path
        actual = target.read_text(encoding="utf-8")
        if actual != new_text:
            raise AssertionError(
                f"Module content does not match expected text for {module_relative_path}."
            )
        return {
            "verified": True,
            "target": module_relative_path,
            "text_length": len(new_text),
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "update_module_code")


def create_common_module(
    environment: EnvironmentConfig,
    module_name: str,
    initial_text: str = "",
    label: str = "create-common-module",
) -> ToolResult:
    """Create a new ``CommonModules/<module_name>/Ext/Module.bsl`` in the dump tree."""
    if not module_name or not _MODULE_NAME_RE.fullmatch(module_name):
        return ToolResult(
            ok=False,
            tool_name="create_common_module",
            message=(
                f"Invalid module_name: {module_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={"data": {"module_name": module_name}},
        )

    intent = WriteIntent("create_common_module", module_name)
    module_relative_path = f"CommonModules/{module_name}/Ext/Module.bsl"
    expected_text = initial_text if initial_text else f"// {module_name}\n"

    def _resolve_target(ctx):
        return (
            Path(ctx.environment.dump_path)
            / "CommonModules"
            / module_name
            / "Ext"
            / "Module.bsl"
        )

    def operation(ctx):
        target = _resolve_target(ctx)
        if target.exists():
            raise FileExistsError(
                f"Common module already exists: {module_relative_path}"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(expected_text, encoding="utf-8")
        return {
            "created": True,
            "module_name": module_name,
            "module_relative_path": module_relative_path,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Common module file missing after create: {target}"
            )
        actual = target.read_text(encoding="utf-8")
        if actual != expected_text:
            raise AssertionError(
                f"Common module text does not match expected for {module_relative_path}."
            )
        return {
            "verified": True,
            "module_name": module_name,
            "module_relative_path": module_relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "create_common_module")


def verify_module_contains(
    environment: EnvironmentConfig,
    module_relative_path: str,
    expected_substring: str,
) -> ToolResult:
    """Verify that ``module_relative_path`` inside the dump contains ``expected_substring``."""
    if not expected_substring or not expected_substring.strip():
        return ToolResult(
            ok=False,
            tool_name="verify_module_contains",
            message="expected_substring must be a non-empty, non-whitespace string.",
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "expected_substring": expected_substring,
                }
            },
        )
    try:
        text = read_dump_file(environment, module_relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="verify_module_contains",
            message=str(exc),
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "expected_substring": expected_substring,
                    "contains": False,
                }
            },
        )
    contains = expected_substring in text
    if contains:
        return ToolResult(
            ok=True,
            tool_name="verify_module_contains",
            message="Module verification succeeded.",
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "expected_substring": expected_substring,
                    "contains": True,
                }
            },
        )
    return ToolResult(
        ok=False,
        tool_name="verify_module_contains",
        message="Expected substring was not found in module.",
        payload={
            "data": {
                "module_relative_path": module_relative_path,
                "expected_substring": expected_substring,
                "contains": False,
            }
        },
    )


def verify_object_exists(
    environment: EnvironmentConfig,
    object_name: str,
) -> ToolResult:
    """Cross-check that ``object_name`` exists on both live endpoint and dump."""
    # Live side
    live_exists = False
    live_error: str | None = None
    try:
        fetch_json_from_environment(
            environment,
            f"metadata/object?name={urllib.parse.quote(object_name)}",
        )
        live_exists = True
    except PlatformError as exc:
        live_error = str(exc)

    # Dump side — substring search across *.xml files
    dump_match_count = 0
    dump_error: str | None = None
    try:
        dump_root = resolve_dump_path(environment)
        xml_files = find_files_by_pattern(dump_root, "*.xml")
        for xml_path in xml_files:
            text = read_text_file(xml_path)
            if object_name in text:
                dump_match_count += 1
    except PlatformError as exc:
        dump_error = str(exc)

    dump_exists = dump_match_count > 0

    data = {
        "object_name": object_name,
        "live_exists": live_exists,
        "dump_exists": dump_exists,
        "dump_match_count": dump_match_count,
    }
    if live_error is not None:
        data["live_error"] = live_error
    if dump_error is not None:
        data["dump_error"] = dump_error

    if live_exists and dump_exists:
        return ToolResult(
            ok=True,
            tool_name="verify_object_exists",
            message="Object exists in both live and dump sources.",
            payload={"data": data},
        )
    return ToolResult(
        ok=False,
        tool_name="verify_object_exists",
        message="Object was not confirmed in both live and dump sources.",
        payload={"data": data},
    )


def verify_metadata_change(
    environment: EnvironmentConfig,
    expectation: dict,
) -> ToolResult:
    """Facade over the minimal expectation contract.

    Supported kinds:
    - ``object_exists`` with ``object_name``;
    - ``module_contains`` with ``module_relative_path`` and
      ``expected_substring``;
    - ``attribute_exists`` with ``object_name`` and ``attribute_name``;
    - ``form_exists`` with ``object_name`` and ``form_name``;
    - ``method_exists`` with ``module_relative_path`` and
      ``method_name``;
    - ``form_attribute_exists`` (Phase 6 / Step 5) with
      ``object_name``, ``form_name`` and ``attribute_name`` —
      structural check via ``ElementTree``: confirms the named
      attribute exists inside the named form's own
      ``<Attributes>`` block (not the object-level one).
    """
    if not isinstance(expectation, dict) or "kind" not in expectation:
        return ToolResult(
            ok=False,
            tool_name="verify_metadata_change",
            message="expectation must be a dict with a 'kind' field.",
            payload={"data": {"expectation": expectation}},
        )

    kind = expectation["kind"]

    if kind == "object_exists":
        object_name = expectation.get("object_name")
        if not object_name:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message="expectation.object_name is required for kind='object_exists'.",
                payload={"data": {"verification_kind": kind}},
            )
        inner = verify_object_exists(environment, object_name)
    elif kind == "module_contains":
        module_relative_path = expectation.get("module_relative_path")
        expected_substring = expectation.get("expected_substring")
        if not module_relative_path or expected_substring is None:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message=(
                    "expectation.module_relative_path and "
                    "expectation.expected_substring are required for "
                    "kind='module_contains'."
                ),
                payload={"data": {"verification_kind": kind}},
            )
        inner = verify_module_contains(
            environment, module_relative_path, expected_substring
        )
    elif kind == "attribute_exists":
        object_name = expectation.get("object_name")
        attribute_name = expectation.get("attribute_name")
        if not object_name or not attribute_name:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message=(
                    "expectation.object_name and expectation.attribute_name "
                    "are required for kind='attribute_exists'."
                ),
                payload={"data": {"verification_kind": kind}},
            )
        inner = verify_attribute_exists(
            environment, object_name, attribute_name
        )
    elif kind == "form_exists":
        object_name = expectation.get("object_name")
        form_name = expectation.get("form_name")
        if not object_name or not form_name:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message=(
                    "expectation.object_name and expectation.form_name "
                    "are required for kind='form_exists'."
                ),
                payload={"data": {"verification_kind": kind}},
            )
        inner = _verify_form_exists_internal(
            environment, object_name, form_name
        )
    elif kind == "method_exists":
        module_relative_path = expectation.get("module_relative_path")
        method_name = expectation.get("method_name")
        if not module_relative_path or not method_name:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message=(
                    "expectation.module_relative_path and "
                    "expectation.method_name are required for "
                    "kind='method_exists'."
                ),
                payload={"data": {"verification_kind": kind}},
            )
        inner = _verify_method_exists_internal(
            environment, module_relative_path, method_name
        )
    elif kind == "form_attribute_exists":
        object_name = expectation.get("object_name")
        form_name = expectation.get("form_name")
        attribute_name = expectation.get("attribute_name")
        if not object_name or not form_name or not attribute_name:
            return ToolResult(
                ok=False,
                tool_name="verify_metadata_change",
                message=(
                    "expectation.object_name, expectation.form_name and "
                    "expectation.attribute_name are required for "
                    "kind='form_attribute_exists'."
                ),
                payload={"data": {"verification_kind": kind}},
            )
        inner = _verify_form_attribute_exists_internal(
            environment, object_name, form_name, attribute_name
        )
    else:
        return ToolResult(
            ok=False,
            tool_name="verify_metadata_change",
            message=f"Unknown metadata verification kind: {kind!r}.",
            payload={"data": {"verification_kind": kind}},
        )

    payload = dict(inner.payload or {})
    data = dict(payload.get("data") or {})
    data["verification_kind"] = kind
    payload["data"] = data
    return ToolResult(
        ok=inner.ok,
        tool_name="verify_metadata_change",
        message=inner.message,
        payload=payload,
    )


def _render_updatedb_command(
    template: list[str],
    *,
    environment: EnvironmentConfig,
    binary_path: str,
) -> list[str]:
    """Render an operator-declared update-db argv template.

    Thin tool-specific wrapper around the shared
    :func:`runtime.binary_dispatch.render_command_template`
    (Track A / Step 4). Builds the update-db-specific
    ``substitutions`` dict (tighter than dumpcfg / applycfg —
    no ``output_path`` / ``source_dump_path``); the rest — per-item
    substitution discipline, fail-closed on unknown placeholder,
    error message naming the config field — lives in the shared
    helper.
    """
    return render_command_template(
        template,
        substitutions={
            "binary_path": binary_path,
            "base_path": environment.base_path,
            "base_id": environment.base_id,
            "publication_name": environment.publication_name,
            "http_base_url": environment.http_base_url,
        },
        allowed_placeholders=_UPDATEDB_TEMPLATE_PLACEHOLDERS,
        template_field_name="onec_updatedb_command_template",
    )


def _build_updatedb_stub_callables():
    """Return ``(operation, verify)`` callables for the legacy stub
    update-db branch.

    Phase 2 / Step 9 side-effects preserved verbatim:
    ``.update-db-stub.txt`` + ``.update-db-meta.json`` inside
    ``environment.dump_path`` through
    :func:`onec_process_runner.run_process`. Track A / Step 4 —
    payload discipline: the unified six honest-mode fields come
    from :func:`stub_honest_mode_fields`. Legacy meta-file
    ``mode: "stub-update-db"`` value still lives on disk
    (backward-compat for any external reader); the in-payload
    ``mode`` field is now the unified ``"stub"``.
    """

    def operation(ctx):
        python_exe = shutil.which("python")
        if python_exe is None:
            raise FileNotFoundError(
                "Python interpreter not found in PATH for update-db stub."
            )
        dump_root = Path(ctx.environment.dump_path)
        marker_path = dump_root / ".update-db-stub.txt"
        meta_path = dump_root / ".update-db-meta.json"

        process_result = run_process(
            ProcessRunRequest(
                command=[
                    python_exe,
                    "-c",
                    "import sys; open(sys.argv[1], 'w', encoding='utf-8').write('updated')",
                    str(marker_path),
                ],
                timeout_seconds=10,
            )
        )
        if not process_result.completed or process_result.exit_code != 0:
            raise RuntimeError(
                f"Stub update-db process failed: completed={process_result.completed} "
                f"exit_code={process_result.exit_code} stderr={process_result.stderr!r}"
            )
        meta = {
            "mode": "stub-update-db",
            "base_id": ctx.environment.base_id,
        }
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False), encoding="utf-8"
        )
        return {
            "updated": True,
            "marker_path": str(marker_path),
            **stub_honest_mode_fields(),
        }

    def verify(ctx, operation_payload):
        dump_root = Path(ctx.environment.dump_path)
        marker_path = dump_root / ".update-db-stub.txt"
        meta_path = dump_root / ".update-db-meta.json"
        if not marker_path.exists():
            raise AssertionError(f"Update-db marker missing: {marker_path}")
        if not meta_path.exists():
            raise AssertionError(f"Update-db meta missing: {meta_path}")
        return {
            "verified": True,
            "mode": operation_payload["mode"],
            "marker_exists": True,
            "meta_exists": True,
        }

    return operation, verify


def _build_updatedb_binary_backed_callables(command: list[str]):
    """Return ``(operation, verify)`` callables for the binary-backed
    update-db branch.

    Track A / Step 4 — payload discipline unification: operation
    builds its dict via :func:`binary_backed_payload_fields` (the
    shared helper that produces the unified six honest-mode fields
    plus the ``completed`` flag). Verify uses
    :func:`is_binary_subprocess_successful` for the success check
    so the same predicate applies to all three binary-backed
    write-tools.

    Operator-facing semantics unchanged: operator-declared argv
    runs through :func:`onec_process_runner.run_process` with a
    fixed :data:`BINARY_DEFAULT_TIMEOUT_SECONDS` cap; runtime
    failure (non-zero exit / non-completed / unstartable
    subprocess) stays an honest failure with no silent stub
    fallback.
    """

    def operation(ctx):
        try:
            process_result = run_process(
                ProcessRunRequest(
                    command=command,
                    timeout_seconds=BINARY_DEFAULT_TIMEOUT_SECONDS,
                    capture_output=True,
                    text=True,
                )
            )
        except PlatformError as exc:
            # Subprocess could not be started (binary missing, etc).
            # Re-raise so run_write_flow turns this into a
            # stage='operation' failure. ``binary_invoked`` is
            # honestly False here because no PID was ever produced.
            raise RuntimeError(
                f"Failed to start updatedb subprocess: {exc}"
            ) from exc
        return {
            "updated": (
                process_result.completed and process_result.exit_code == 0
            ),
            **binary_backed_payload_fields(command, process_result),
        }

    def verify(ctx, operation_payload):
        if not is_binary_subprocess_successful(operation_payload):
            raise AssertionError(
                "updatedb subprocess failed: exit_code="
                f"{operation_payload.get('exit_code')}, completed="
                f"{operation_payload.get('completed')}"
            )
        return {
            "verified": True,
            "mode": operation_payload["mode"],
            "binary_invoked": operation_payload["binary_invoked"],
            "exit_code": operation_payload["exit_code"],
        }

    return operation, verify


def update_database_configuration(
    environment: EnvironmentConfig,
    label: str = "update-database-configuration",
) -> ToolResult:
    """Trigger a database configuration update via the write-flow pipeline.

    Two modes, dispatched on environment configuration; the public
    contract (``ToolResult`` shape, ``run_write_flow`` discipline,
    audit, snapshots) is identical between them. Mirror of
    :func:`apply_config_from_files`'s dual-mode dispatcher
    (Parallel Track A / Step 2) and of
    :func:`create_dump_snapshot`'s dual-mode dispatcher
    (Phase 6 / Step 2):

    - **stub** (Phase 2 / Step 9 default; backward-compat) — used
      when at least one of ``environment.onec_binary_path`` /
      ``environment.onec_updatedb_command_template`` is missing.
      Identical to the legacy stub-process update: writes
      ``.update-db-stub.txt`` + ``.update-db-meta.json`` inside
      ``environment.dump_path`` through ``onec_process_runner``.
      ``operation_payload.mode = "stub"``,
      ``operation_payload.binary_invoked = False``.
    - **binary-backed** (Parallel Track A / Step 3) — used when
      **both** fields are set. Renders the operator-declared argv
      template with a whitelisted set of placeholders
      (:data:`_UPDATEDB_TEMPLATE_PLACEHOLDERS`), runs the
      subprocess via :func:`onec_process_runner.run_process` with
      a fixed :data:`_UPDATEDB_DEFAULT_TIMEOUT_SECONDS` cap, and
      reports the outcome.
      ``operation_payload.mode = "binary-backed"``,
      ``operation_payload.binary_invoked`` is ``True`` once a PID
      was produced (``False`` only when the subprocess could not
      be started or the unknown-placeholder pre-flight rejected
      the call before spawning anything).

    There is **no** silent fallback from binary-backed to stub on
    runtime failure. Once the operator declares the binary-backed
    contract by setting both fields, a non-zero exit / non-completed
    subprocess / unstartable binary stays an honest failure
    (``ok=False`` with the binary-backed payload preserved).
    Fallback only happens at **dispatch** time — when the contract
    is incomplete (one or both fields missing).

    Final unification of the binary-backed payload contract across
    ``create_dump_snapshot`` / ``apply_config_from_files`` /
    ``update_database_configuration`` lands in Track A / Step 4;
    Step 3 simply lifts update-db onto the same shape that Step 2
    and Phase 6 / Step 2 already use.
    """
    binary_path = environment.onec_binary_path
    updatedb_template = environment.onec_updatedb_command_template
    use_binary_backed = bool(binary_path) and bool(updatedb_template)

    intent = WriteIntent("update_database_configuration", environment.base_id)

    if use_binary_backed:
        # Render the argv template up-front. Unknown-placeholder /
        # malformed-template fail-closed BEFORE the flow starts so
        # we never take snapshots / write audit rows for a call
        # that cannot even spawn. ``binary_invoked`` is honestly
        # False because no PID was produced.
        try:
            command = _render_updatedb_command(
                updatedb_template,
                environment=environment,
                binary_path=binary_path,
            )
        except ValueError as exc:
            return ToolResult(
                ok=False,
                tool_name="update_database_configuration",
                message=str(exc),
                payload={
                    "data": {
                        **binary_backed_render_failure_fields(),
                    }
                },
            )
        operation, verify = _build_updatedb_binary_backed_callables(command)
    else:
        operation, verify = _build_updatedb_stub_callables()

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "update_database_configuration")


def add_catalog_attribute(
    environment: EnvironmentConfig,
    catalog_name: str,
    attribute_spec: dict,
    label: str = "add-catalog-attribute",
) -> ToolResult:
    """Add a new attribute to a catalog XML card via a pragmatic text patch.

    MVP-level: not a full 1C XML schema DOM editor. The new attribute is
    inserted as a small XML fragment before the document's last closing
    tag. Accepted types whitelist: ``String``, ``Number``, ``Date``.
    """
    if not catalog_name or not isinstance(catalog_name, str) or not catalog_name.strip():
        return ToolResult(
            ok=False,
            tool_name="add_catalog_attribute",
            message="catalog_name must be a non-empty string.",
            payload={"data": {"catalog_name": catalog_name}},
        )
    if not isinstance(attribute_spec, dict):
        return ToolResult(
            ok=False,
            tool_name="add_catalog_attribute",
            message="attribute_spec must be a dict.",
            payload={"data": {"catalog_name": catalog_name}},
        )
    attr_name = attribute_spec.get("name")
    attr_type = attribute_spec.get("type")
    synonym = attribute_spec.get("synonym")

    if (
        not attr_name
        or not isinstance(attr_name, str)
        or attr_name != attr_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_catalog_attribute",
            message=(
                "attribute_spec.name must be a non-empty string without "
                "leading/trailing whitespace."
            ),
            payload={
                "data": {
                    "catalog_name": catalog_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )
    if not attr_type or attr_type not in _ALLOWED_ATTR_TYPES:
        return ToolResult(
            ok=False,
            tool_name="add_catalog_attribute",
            message=(
                f"attribute_spec.type must be one of "
                f"{sorted(_ALLOWED_ATTR_TYPES)}."
            ),
            payload={
                "data": {
                    "catalog_name": catalog_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )

    intent = WriteIntent("add_catalog_attribute", catalog_name)
    catalog_relative_path = f"Catalogs/{catalog_name}.xml"
    fragment = build_attribute_fragment(attr_name, attr_type, synonym)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / "Catalogs" / f"{catalog_name}.xml"

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Catalog XML not found in dump: {catalog_relative_path}"
            )

        def _patcher(xml_text: str) -> str:
            if attr_name in xml_text:
                raise FileExistsError(
                    f"Attribute {attr_name!r} already referenced in "
                    f"{catalog_relative_path}."
                )
            return insert_fragment_into_named_block(
                xml_text, "Attributes", fragment
            )

        patch_xml_file(target, _patcher)
        return {
            "changed": True,
            "catalog_name": catalog_name,
            "attribute_name": attr_name,
            "catalog_relative_path": catalog_relative_path,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Catalog XML missing after add: {catalog_relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if attr_name not in text:
            raise AssertionError(
                f"Attribute name {attr_name!r} not found in "
                f"{catalog_relative_path}."
            )
        if attr_type not in text:
            raise AssertionError(
                f"Attribute type {attr_type!r} not found in "
                f"{catalog_relative_path}."
            )
        return {
            "verified": True,
            "catalog_name": catalog_name,
            "attribute_name": attr_name,
            "catalog_relative_path": catalog_relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "add_catalog_attribute")


def write_audit_record(
    environment: EnvironmentConfig,
    record: dict,
) -> ToolResult:
    """Append a single audit record to the environment's audit store."""
    if not isinstance(record, dict):
        return ToolResult(
            ok=False,
            tool_name="write_audit_record",
            message="record must be a dict.",
            payload={"data": {}},
        )
    required = ("operation_id", "tool_name", "status", "message")
    missing = [
        key
        for key in required
        if not record.get(key) or not isinstance(record.get(key), str)
    ]
    if missing:
        return ToolResult(
            ok=False,
            tool_name="write_audit_record",
            message=f"record is missing required string fields: {missing}",
            payload={"data": {}},
        )

    audit_dir = str(Path(environment.dump_path) / ".audit")
    audit_record = AuditRecord(
        operation_id=record["operation_id"],
        tool_name=record["tool_name"],
        environment=environment.name,
        base_id=environment.base_id,
        status=record["status"],
        message=record["message"],
    )
    try:
        audit_path = append_record(audit_dir, audit_record)
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="write_audit_record",
            message=f"Failed to write audit record: {exc}",
            payload={
                "data": {"operation_id": record["operation_id"]}
            },
        )
    return ToolResult(
        ok=True,
        tool_name="write_audit_record",
        message="Audit record written successfully.",
        payload={
            "data": {
                "audit_path": audit_path,
                "operation_id": record["operation_id"],
                "status": record["status"],
            }
        },
    )


def describe_last_write_operation(
    environment: EnvironmentConfig,
) -> ToolResult:
    """Return the most recent :class:`AuditRecord` for the environment."""
    audit_dir = str(Path(environment.dump_path) / ".audit")
    try:
        last = read_last_record(audit_dir)
    except (OSError, ValueError) as exc:
        return ToolResult(
            ok=False,
            tool_name="describe_last_write_operation",
            message=f"Failed to read audit store: {exc}",
            payload={"data": {}},
        )
    if last is None:
        return ToolResult(
            ok=False,
            tool_name="describe_last_write_operation",
            message="No audit records found.",
            payload={"data": {}},
        )
    return ToolResult(
        ok=True,
        tool_name="describe_last_write_operation",
        message="Last write operation loaded successfully.",
        payload={
            "data": {
                "operation_id": last.operation_id,
                "tool_name": last.tool_name,
                "environment": last.environment,
                "base_id": last.base_id,
                "status": last.status,
                "message": last.message,
            }
        },
    )


def prepare_rollback_hint(
    environment: EnvironmentConfig,
    operation_id: str,
) -> ToolResult:
    """Prepare a human-readable rollback hint for a given ``operation_id``.

    MVP-level: does NOT execute a rollback. Scans the audit log for the
    target ``operation_id`` and returns suggested snapshot roots plus a
    short hint telling the operator what to do next.
    """
    audit_file = Path(environment.dump_path) / ".audit" / "audit.jsonl"
    if not audit_file.is_file():
        return ToolResult(
            ok=False,
            tool_name="prepare_rollback_hint",
            message="No audit log found for environment.",
            payload={"data": {"operation_id": operation_id}},
        )
    try:
        raw_lines = audit_file.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return ToolResult(
            ok=False,
            tool_name="prepare_rollback_hint",
            message=f"Failed to read audit log: {exc}",
            payload={"data": {"operation_id": operation_id}},
        )

    found = None
    for line in reversed(raw_lines):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if record.get("operation_id") == operation_id:
            found = record
            break

    if found is None:
        return ToolResult(
            ok=False,
            tool_name="prepare_rollback_hint",
            message="Operation was not found in audit log.",
            payload={"data": {"operation_id": operation_id}},
        )

    suggested_backup_root = str(
        Path(environment.base_path).parent / "_snapshots"
    )
    suggested_dump_root = str(
        Path(environment.dump_path).parent / "_snapshots"
    )
    hint_text = (
        "Locate the backup/dump snapshot created around this operation "
        "and use it as the rollback source for a future apply/update step."
    )

    return ToolResult(
        ok=True,
        tool_name="prepare_rollback_hint",
        message="Rollback hint prepared.",
        payload={
            "data": {
                "operation_id": operation_id,
                "audit_status": found.get("status"),
                "suggested_backup_root": suggested_backup_root,
                "suggested_dump_root": suggested_dump_root,
                "hint_text": hint_text,
            }
        },
    )


def create_catalog(
    environment: EnvironmentConfig,
    catalog_name: str,
    spec: dict,
    label: str = "create-catalog",
) -> ToolResult:
    """Create a new catalog stub XML card under ``Catalogs/<catalog_name>.xml``.

    MVP-level: writes a minimal ``<MetaData>`` stub with ``<Name>``,
    an optional ``<Synonym>``, and an empty ``<Attributes></Attributes>``
    block ready for subsequent ``add_catalog_attribute`` calls. Not a
    full 1C configuration card.
    """
    if (
        not catalog_name
        or not isinstance(catalog_name, str)
        or not _MODULE_NAME_RE.fullmatch(catalog_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="create_catalog",
            message=(
                f"Invalid catalog_name: {catalog_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={"data": {"catalog_name": catalog_name}},
        )
    if not isinstance(spec, dict):
        return ToolResult(
            ok=False,
            tool_name="create_catalog",
            message="spec must be a dict.",
            payload={"data": {"catalog_name": catalog_name}},
        )
    synonym = spec.get("synonym")
    if synonym is not None and not isinstance(synonym, str):
        return ToolResult(
            ok=False,
            tool_name="create_catalog",
            message="spec.synonym must be a string or None.",
            payload={"data": {"catalog_name": catalog_name}},
        )

    intent = WriteIntent("create_catalog", catalog_name)
    catalog_relative_path = f"Catalogs/{catalog_name}.xml"
    # Stub includes empty <Attributes></Attributes> and <Forms></Forms> blocks
    # so that subsequent add_catalog_attribute / create_managed_form calls
    # have deterministic insertion points (Phase 3 composability).
    if synonym:
        stub_xml = (
            f"<MetaData>"
            f"<Name>{catalog_name}</Name>"
            f"<Synonym>{synonym}</Synonym>"
            f"<Attributes></Attributes>"
            f"<Forms></Forms>"
            f"</MetaData>"
        )
    else:
        stub_xml = (
            f"<MetaData>"
            f"<Name>{catalog_name}</Name>"
            f"<Attributes></Attributes>"
            f"<Forms></Forms>"
            f"</MetaData>"
        )

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / "Catalogs" / f"{catalog_name}.xml"

    def operation(ctx):
        target = _resolve_target(ctx)
        if target.exists():
            raise FileExistsError(
                f"Catalog XML already exists: {catalog_relative_path}"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stub_xml, encoding="utf-8")
        return {
            "created": True,
            "catalog_name": catalog_name,
            "catalog_relative_path": catalog_relative_path,
            "has_synonym": synonym is not None,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Catalog XML missing after create: {catalog_relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if f"<Name>{catalog_name}</Name>" not in text:
            raise AssertionError(
                f"Catalog XML does not contain expected <Name> for "
                f"{catalog_name}."
            )
        if synonym and f"<Synonym>{synonym}</Synonym>" not in text:
            raise AssertionError(
                f"Catalog XML does not contain expected <Synonym> for "
                f"{catalog_name}."
            )
        return {
            "verified": True,
            "catalog_name": catalog_name,
            "catalog_relative_path": catalog_relative_path,
            "has_synonym": synonym is not None,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "create_catalog")


def add_document_attribute(
    environment: EnvironmentConfig,
    document_name: str,
    attribute_spec: dict,
    label: str = "add-document-attribute",
) -> ToolResult:
    """Add a new attribute to a document XML card via the metadata helper layer.

    Inserts the fragment produced by ``build_attribute_fragment`` inside
    the document's ``<Attributes>...</Attributes>`` block using
    ``insert_fragment_into_named_block``. If the document XML does not
    contain a paired ``<Attributes>`` block the operation fails
    fail-closed — no ``rfind("</")`` fallback.
    """
    if (
        not document_name
        or not isinstance(document_name, str)
        or not document_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_document_attribute",
            message="document_name must be a non-empty string.",
            payload={"data": {"document_name": document_name}},
        )
    if not isinstance(attribute_spec, dict):
        return ToolResult(
            ok=False,
            tool_name="add_document_attribute",
            message="attribute_spec must be a dict.",
            payload={"data": {"document_name": document_name}},
        )
    attr_name = attribute_spec.get("name")
    attr_type = attribute_spec.get("type")
    synonym = attribute_spec.get("synonym")

    if (
        not attr_name
        or not isinstance(attr_name, str)
        or attr_name != attr_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_document_attribute",
            message=(
                "attribute_spec.name must be a non-empty string without "
                "leading/trailing whitespace."
            ),
            payload={
                "data": {
                    "document_name": document_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )
    if not attr_type or attr_type not in _ALLOWED_ATTR_TYPES:
        return ToolResult(
            ok=False,
            tool_name="add_document_attribute",
            message=(
                f"attribute_spec.type must be one of "
                f"{sorted(_ALLOWED_ATTR_TYPES)}."
            ),
            payload={
                "data": {
                    "document_name": document_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )

    intent = WriteIntent("add_document_attribute", document_name)
    document_relative_path = f"Documents/{document_name}.xml"
    fragment = build_attribute_fragment(attr_name, attr_type, synonym)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / "Documents" / f"{document_name}.xml"

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Document XML not found in dump: {document_relative_path}"
            )

        def _patcher(xml_text: str) -> str:
            if attr_name in xml_text:
                raise FileExistsError(
                    f"Attribute {attr_name!r} already referenced in "
                    f"{document_relative_path}."
                )
            return insert_fragment_into_named_block(
                xml_text, "Attributes", fragment
            )

        patch_xml_file(target, _patcher)
        return {
            "changed": True,
            "document_name": document_name,
            "attribute_name": attr_name,
            "document_relative_path": document_relative_path,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Document XML missing after add: {document_relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if attr_name not in text:
            raise AssertionError(
                f"Attribute name {attr_name!r} not found in "
                f"{document_relative_path}."
            )
        if attr_type not in text:
            raise AssertionError(
                f"Attribute type {attr_type!r} not found in "
                f"{document_relative_path}."
            )
        if synonym and synonym not in text:
            raise AssertionError(
                f"Attribute synonym {synonym!r} not found in "
                f"{document_relative_path}."
            )
        return {
            "verified": True,
            "document_name": document_name,
            "attribute_name": attr_name,
            "document_relative_path": document_relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "add_document_attribute")


_OBJECT_NAME_PREFIXES = (
    ("Справочник.", "Catalogs"),
    ("Документ.", "Documents"),
)

_DIFF_PREVIEW_MAX_LINES = 40


def _resolve_object_xml_path(object_name: str) -> str | None:
    """Return the dump-relative XML path for ``object_name`` or None.

    Supported prefixes (MVP):
    - ``Справочник.<name>`` → ``Catalogs/<name>.xml``
    - ``Документ.<name>``  → ``Documents/<name>.xml``
    """
    if not isinstance(object_name, str):
        return None
    for prefix, folder in _OBJECT_NAME_PREFIXES:
        if object_name.startswith(prefix):
            tail = object_name[len(prefix):]
            if not tail:
                return None
            return f"{folder}/{tail}.xml"
    return None


def verify_attribute_exists(
    environment: EnvironmentConfig,
    object_name: str,
    attribute_name: str,
) -> ToolResult:
    """Verify that ``attribute_name`` is present in the object's dump XML card.

    MVP-level: dump-only substring check. Resolves ``object_name`` via
    ``_resolve_object_xml_path`` (``Справочник.<name>`` →
    ``Catalogs/<name>.xml``; ``Документ.<name>`` → ``Documents/<name>.xml``).
    Unsupported prefix or missing file → ``ok=False`` with a concrete
    reason; PlatformError from the dump adapter is wrapped, not raised.
    """
    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="verify_attribute_exists",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "attribute_name": attribute_name,
                    "exists": False,
                }
            },
        )

    try:
        text = read_dump_file(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="verify_attribute_exists",
            message=str(exc),
            payload={
                "data": {
                    "object_name": object_name,
                    "attribute_name": attribute_name,
                    "relative_path": relative_path,
                    "exists": False,
                }
            },
        )

    exists = attribute_name in text
    return ToolResult(
        ok=exists,
        tool_name="verify_attribute_exists",
        message=(
            "Attribute exists in dump XML."
            if exists
            else "Attribute not found in dump XML."
        ),
        payload={
            "data": {
                "object_name": object_name,
                "attribute_name": attribute_name,
                "relative_path": relative_path,
                "exists": exists,
            }
        },
    )


def _verify_form_exists_internal(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str,
) -> ToolResult:
    """Internal helper for ``verify_metadata_change(kind='form_exists')``.

    Dump-level substring check: resolves the object's XML card and
    looks for ``form_name`` as a plain substring. ``tool_name`` on
    the returned ToolResult is internal; the dispatcher rewraps it
    to ``"verify_metadata_change"``.
    """
    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_exists_internal",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "exists": False,
                }
            },
        )
    try:
        text = read_dump_file(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_exists_internal",
            message=str(exc),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "relative_path": relative_path,
                    "exists": False,
                }
            },
        )
    exists = form_name in text
    return ToolResult(
        ok=exists,
        tool_name="_verify_form_exists_internal",
        message=(
            "Form name found in object XML."
            if exists
            else "Form name not found in object XML."
        ),
        payload={
            "data": {
                "object_name": object_name,
                "form_name": form_name,
                "relative_path": relative_path,
                "exists": exists,
            }
        },
    )


def _verify_method_exists_internal(
    environment: EnvironmentConfig,
    module_relative_path: str,
    method_name: str,
) -> ToolResult:
    """Internal helper for ``verify_metadata_change(kind='method_exists')``.

    Uses :func:`module_contains_method` from the metadata helper layer
    (lenient BSL method-declaration regex). ``tool_name`` is internal;
    the dispatcher rewraps it.
    """
    try:
        text = read_dump_file(environment, module_relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="_verify_method_exists_internal",
            message=str(exc),
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_name": method_name,
                    "exists": False,
                }
            },
        )
    exists = module_contains_method(text, method_name)
    return ToolResult(
        ok=exists,
        tool_name="_verify_method_exists_internal",
        message=(
            "Method declaration found in module."
            if exists
            else "Method declaration not found in module."
        ),
        payload={
            "data": {
                "module_relative_path": module_relative_path,
                "method_name": method_name,
                "exists": exists,
            }
        },
    )


def diff_dump_fragment(
    environment: EnvironmentConfig,
    relative_path: str,
    baseline: str,
) -> ToolResult:
    """Return a read-only diff of a dump file against ``baseline``.

    - ``ok=True`` whenever the file was read, regardless of whether the
      content matches the baseline. A difference is information, not
      an error.
    - ``ok=False`` only if the file is unreadable (missing /
      ``PlatformError`` from the dump adapter).
    - ``diff_preview`` is a compact unified diff (first
      ``_DIFF_PREVIEW_MAX_LINES`` lines with a truncation marker if
      the diff is larger); empty string when ``changed=False``.
    """
    try:
        current_text = read_dump_file(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="diff_dump_fragment",
            message=str(exc),
            payload={
                "data": {
                    "relative_path": relative_path,
                    "changed": False,
                    "current_text_length": 0,
                    "baseline_length": len(baseline),
                    "diff_preview": "",
                }
            },
        )

    changed = current_text != baseline
    if not changed:
        diff_preview = ""
    else:
        diff_lines = list(
            difflib.unified_diff(
                baseline.splitlines(),
                current_text.splitlines(),
                fromfile="baseline",
                tofile="current",
                lineterm="",
                n=3,
            )
        )
        if len(diff_lines) > _DIFF_PREVIEW_MAX_LINES:
            diff_preview = (
                "\n".join(diff_lines[:_DIFF_PREVIEW_MAX_LINES])
                + "\n... (diff truncated)"
            )
        else:
            diff_preview = "\n".join(diff_lines)

    return ToolResult(
        ok=True,
        tool_name="diff_dump_fragment",
        message=(
            "Dump fragment matches baseline."
            if not changed
            else "Dump fragment differs from baseline."
        ),
        payload={
            "data": {
                "relative_path": relative_path,
                "changed": changed,
                "current_text_length": len(current_text),
                "baseline_length": len(baseline),
                "diff_preview": diff_preview,
            }
        },
    )


# ---------------------------------------------------------------------------
# Phase 3 / Step 6 — form / module level metadata tools
# ---------------------------------------------------------------------------


def _build_form_element_fragment(
    name: str,
    element_type: str,
    title: str | None = None,
) -> str:
    """Build a minimal ``<Element>`` XML fragment for a form."""
    if title:
        return (
            f'<Element name="{name}">'
            f"<Type>{element_type}</Type>"
            f"<Title>{title}</Title>"
            f"</Element>"
        )
    return (
        f'<Element name="{name}">'
        f"<Type>{element_type}</Type>"
        f"</Element>"
    )


def _find_form_block_bounds(
    xml_text: str, form_name: str
) -> tuple[int, int] | None:
    """Return ``(start, end)`` of ``<Form name="form_name">...</Form>`` or None.

    Matches the form by the literal opening tag ``<Form name="form_name">``;
    the nearest ``</Form>`` after that opening is taken as the closing bound.
    Returns None if either boundary is not found.
    """
    opening = f'<Form name="{form_name}">'
    start = xml_text.find(opening)
    if start == -1:
        return None
    close = xml_text.find("</Form>", start)
    if close == -1:
        return None
    return (start, close + len("</Form>"))


_BSL_SIGNATURE_RE_TEMPLATE = (
    r"(?P<keyword>Процедура|Функция|Procedure|Function)"
    r"\s+{name}\s*\([^)]*\)"
    r"(?:\s+(?:Экспорт|Export))?"
    r"\s*(?:\r\n|\n|\r)"
)

_BSL_END_PROCEDURE_RE = re.compile(
    r"\b(?:КонецПроцедуры|EndProcedure)\b", re.IGNORECASE
)
_BSL_END_FUNCTION_RE = re.compile(
    r"\b(?:КонецФункции|EndFunction)\b", re.IGNORECASE
)


def create_managed_form(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str,
    label: str = "create-managed-form",
) -> ToolResult:
    """Insert a managed form stub into an object's ``<Forms>`` XML block.

    MVP-level: works on dump XML only. Uses
    :func:`insert_fragment_into_named_block` to place
    :func:`build_form_fragment` inside the object's ``<Forms>`` block.
    Fails fail-closed if the object XML has no paired ``<Forms>`` block
    or if ``form_name`` is already referenced in the card.
    """
    if (
        not object_name
        or not isinstance(object_name, str)
        or not object_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="create_managed_form",
            message="object_name must be a non-empty string.",
            payload={"data": {"object_name": object_name}},
        )
    if (
        not form_name
        or not isinstance(form_name, str)
        or not _MODULE_NAME_RE.fullmatch(form_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="create_managed_form",
            message=(
                f"Invalid form_name: {form_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={"data": {"object_name": object_name, "form_name": form_name}},
        )

    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="create_managed_form",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={"data": {"object_name": object_name, "form_name": form_name}},
        )

    intent = WriteIntent("create_managed_form", form_name)
    fragment = build_form_fragment(form_name)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / relative_path

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Object XML not found in dump: {relative_path}"
            )

        def _patcher(xml_text: str) -> str:
            if f'<Form name="{form_name}">' in xml_text:
                raise FileExistsError(
                    f"Form {form_name!r} already exists in {relative_path}."
                )
            return insert_fragment_into_named_block(
                xml_text, "Forms", fragment
            )

        patch_xml_file(target, _patcher)
        return {
            "changed": True,
            "object_name": object_name,
            "form_name": form_name,
            "relative_path": relative_path,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Object XML missing after form create: {relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if f'<Form name="{form_name}">' not in text:
            raise AssertionError(
                f"Form {form_name!r} was not inserted into {relative_path}."
            )
        return {
            "verified": True,
            "object_name": object_name,
            "form_name": form_name,
            "relative_path": relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "create_managed_form")


def add_form_element(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str,
    element_spec: dict,
    label: str = "add-form-element",
) -> ToolResult:
    """Add an element into the targeted form's ``<Elements>`` block.

    Pragmatic structural patch: locates the specific
    ``<Form name="form_name">...</Form>`` block via
    :func:`_find_form_block_bounds`, looks for its ``<Elements>`` child
    block, and inserts the new element fragment before that block's
    closing tag. Fails fail-closed if the form or its ``<Elements>``
    block cannot be unambiguously located, or if an element with the
    same ``name`` is already present in the form.
    """
    if (
        not object_name
        or not isinstance(object_name, str)
        or not object_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message="object_name must be a non-empty string.",
            payload={"data": {"object_name": object_name}},
        )
    if (
        not form_name
        or not isinstance(form_name, str)
        or not _MODULE_NAME_RE.fullmatch(form_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message=(
                f"Invalid form_name: {form_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={"data": {"object_name": object_name, "form_name": form_name}},
        )
    if not isinstance(element_spec, dict):
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message="element_spec must be a dict.",
            payload={"data": {"object_name": object_name, "form_name": form_name}},
        )

    element_name = element_spec.get("name")
    element_type = element_spec.get("type")
    title = element_spec.get("title")

    if (
        not element_name
        or not isinstance(element_name, str)
        or element_name != element_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message=(
                "element_spec.name must be a non-empty string without "
                "leading/trailing whitespace."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "element_spec": element_spec,
                }
            },
        )
    if not element_type or not isinstance(element_type, str) or not element_type.strip():
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message="element_spec.type must be a non-empty string.",
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "element_spec": element_spec,
                }
            },
        )

    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="add_form_element",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={"data": {"object_name": object_name, "form_name": form_name}},
        )

    intent = WriteIntent("add_form_element", element_name)
    fragment = _build_form_element_fragment(element_name, element_type, title)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / relative_path

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Object XML not found in dump: {relative_path}"
            )

        def _patcher(xml_text: str) -> str:
            bounds = _find_form_block_bounds(xml_text, form_name)
            if bounds is None:
                raise ValueError(
                    f'Form <Form name="{form_name}"> not found in '
                    f"{relative_path}."
                )
            form_start, form_end = bounds
            form_block = xml_text[form_start:form_end]

            collision_marker = f'<Element name="{element_name}">'
            if collision_marker in form_block:
                raise FileExistsError(
                    f"Element {element_name!r} already present in form "
                    f"{form_name!r}."
                )

            # Elements block inside this specific form
            elements_close_rel = form_block.find("</Elements>")
            if elements_close_rel == -1:
                raise ValueError(
                    f"Form {form_name!r} has no <Elements> block for insertion."
                )
            if "<Elements>" not in form_block and "<Elements " not in form_block:
                raise ValueError(
                    f"Form {form_name!r} <Elements> block has no opening tag."
                )

            insertion_point = form_start + elements_close_rel
            return xml_text[:insertion_point] + fragment + xml_text[insertion_point:]

        patch_xml_file(target, _patcher)
        return {
            "changed": True,
            "object_name": object_name,
            "form_name": form_name,
            "element_name": element_name,
            "element_type": element_type,
            "relative_path": relative_path,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Object XML missing after form element add: {relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        bounds = _find_form_block_bounds(text, form_name)
        if bounds is None:
            raise AssertionError(
                f"Form {form_name!r} not found after add_form_element."
            )
        form_block = text[bounds[0]:bounds[1]]
        marker = f'<Element name="{element_name}">'
        if marker not in form_block:
            raise AssertionError(
                f"Element {element_name!r} not found in form {form_name!r}."
            )
        if element_type not in form_block:
            raise AssertionError(
                f"Element type {element_type!r} not found in form {form_name!r}."
            )
        return {
            "verified": True,
            "object_name": object_name,
            "form_name": form_name,
            "element_name": element_name,
            "element_type": element_type,
            "relative_path": relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "add_form_element")


def append_module_method(
    environment: EnvironmentConfig,
    module_relative_path: str,
    method_spec: dict,
    label: str = "append-module-method",
) -> ToolResult:
    """Append a new BSL ``Процедура`` method to a dump module file.

    Uses :func:`build_module_method_fragment` +
    :func:`append_method_to_module` +
    :func:`module_contains_method` from the metadata helper layer.
    Fails fail-closed if the target module is missing, if the method
    is already declared, or if ``method_spec.body`` is empty/whitespace.
    """
    if (
        not module_relative_path
        or not isinstance(module_relative_path, str)
        or not module_relative_path.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="append_module_method",
            message="module_relative_path must be a non-empty string.",
            payload={"data": {"module_relative_path": module_relative_path}},
        )
    if not isinstance(method_spec, dict):
        return ToolResult(
            ok=False,
            tool_name="append_module_method",
            message="method_spec must be a dict.",
            payload={"data": {"module_relative_path": module_relative_path}},
        )
    method_name = method_spec.get("name")
    body = method_spec.get("body")
    export = method_spec.get("export", False)

    if (
        not method_name
        or not isinstance(method_name, str)
        or not _MODULE_NAME_RE.fullmatch(method_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="append_module_method",
            message=(
                f"Invalid method_spec.name: {method_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_spec": method_spec,
                }
            },
        )
    if not isinstance(body, str) or not body or not body.strip():
        return ToolResult(
            ok=False,
            tool_name="append_module_method",
            message="method_spec.body must be a non-empty, non-whitespace string.",
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_spec": method_spec,
                }
            },
        )
    if not isinstance(export, bool):
        return ToolResult(
            ok=False,
            tool_name="append_module_method",
            message="method_spec.export must be a bool if provided.",
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_spec": method_spec,
                }
            },
        )

    intent = WriteIntent("append_module_method", method_name)
    fragment = build_module_method_fragment(method_name, body, export=export)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / module_relative_path

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Module not found in dump: {module_relative_path}"
            )

        def _patcher(text: str) -> str:
            if module_contains_method(text, method_name):
                raise FileExistsError(
                    f"Method {method_name!r} already declared in "
                    f"{module_relative_path}."
                )
            return append_method_to_module(text, fragment)

        patch_text_file(target, _patcher)
        return {
            "changed": True,
            "module_relative_path": module_relative_path,
            "method_name": method_name,
            "export": export,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Module missing after append_module_method: "
                f"{module_relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if not module_contains_method(text, method_name):
            raise AssertionError(
                f"Method {method_name!r} not detected after append in "
                f"{module_relative_path}."
            )
        return {
            "verified": True,
            "module_relative_path": module_relative_path,
            "method_name": method_name,
            "export": export,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "append_module_method")


def replace_module_method_body(
    environment: EnvironmentConfig,
    module_relative_path: str,
    method_name: str,
    new_body: str,
    *,
    confirm_replace: bool = False,
    label: str = "replace-module-method-body",
) -> ToolResult:
    """Replace the body of an existing BSL method, preserving its signature.

    **Deliberately dangerous.** Requires explicit ``confirm_replace=True``;
    otherwise the tool rejects the request before entering the write flow.
    Uses a signature regex to locate exactly one method by name, then the
    matching ``КонецПроцедуры`` / ``КонецФункции`` (or English
    equivalents) to bound the body. If the structure cannot be resolved
    unambiguously, the operation fails fail-closed without touching the
    file.
    """
    if not confirm_replace:
        return ToolResult(
            ok=False,
            tool_name="replace_module_method_body",
            message=(
                "replace_module_method_body requires explicit "
                "confirm_replace=True."
            ),
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_name": method_name,
                    "confirm_replace": confirm_replace,
                }
            },
        )
    if (
        not module_relative_path
        or not isinstance(module_relative_path, str)
        or not module_relative_path.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="replace_module_method_body",
            message="module_relative_path must be a non-empty string.",
            payload={"data": {"module_relative_path": module_relative_path}},
        )
    if (
        not method_name
        or not isinstance(method_name, str)
        or not _MODULE_NAME_RE.fullmatch(method_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="replace_module_method_body",
            message=(
                f"Invalid method_name: {method_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_name": method_name,
                }
            },
        )
    if not isinstance(new_body, str) or not new_body or not new_body.strip():
        return ToolResult(
            ok=False,
            tool_name="replace_module_method_body",
            message="new_body must be a non-empty, non-whitespace string.",
            payload={
                "data": {
                    "module_relative_path": module_relative_path,
                    "method_name": method_name,
                }
            },
        )

    intent = WriteIntent("replace_module_method_body", method_name)
    signature_re = re.compile(
        _BSL_SIGNATURE_RE_TEMPLATE.format(name=re.escape(method_name)),
        re.IGNORECASE,
    )

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / module_relative_path

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Module not found in dump: {module_relative_path}"
            )

        def _patcher(text: str) -> str:
            if not module_contains_method(text, method_name):
                raise FileNotFoundError(
                    f"Method {method_name!r} not found in "
                    f"{module_relative_path}."
                )
            sig_match = signature_re.search(text)
            if sig_match is None:
                raise ValueError(
                    f"Method signature for {method_name!r} could not be "
                    f"parsed unambiguously in {module_relative_path}."
                )
            keyword = sig_match.group("keyword").lower()
            if keyword in ("процедура", "procedure"):
                end_re = _BSL_END_PROCEDURE_RE
            else:
                end_re = _BSL_END_FUNCTION_RE
            end_match = end_re.search(text, sig_match.end())
            if end_match is None:
                raise ValueError(
                    f"End keyword for method {method_name!r} not found "
                    f"after its signature in {module_relative_path}."
                )
            body_start = sig_match.end()
            body_end = end_match.start()
            normalized_body = new_body if new_body.endswith("\n") else new_body + "\n"
            return text[:body_start] + normalized_body + text[body_end:]

        patch_text_file(target, _patcher)
        return {
            "changed": True,
            "module_relative_path": module_relative_path,
            "method_name": method_name,
            "new_body_length": len(new_body),
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Module missing after replace_module_method_body: "
                f"{module_relative_path}"
            )
        text = target.read_text(encoding="utf-8")
        if not module_contains_method(text, method_name):
            raise AssertionError(
                f"Method {method_name!r} disappeared after body replace."
            )
        if new_body not in text:
            raise AssertionError(
                f"New body not present in {module_relative_path} after replace."
            )
        return {
            "verified": True,
            "module_relative_path": module_relative_path,
            "method_name": method_name,
            "new_body_length": len(new_body),
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "replace_module_method_body")


# ---------------------------------------------------------------------------
# Phase 6 / Step 4 — single-file restore from snapshot.
# ---------------------------------------------------------------------------


def restore_dump_file_from_snapshot(
    environment: EnvironmentConfig,
    relative_path: str,
    snapshot_file_path: str,
    label: str = "restore-dump-file",
) -> ToolResult:
    """Restore a single dump file from a snapshot back into the live dump.

    Phase 6 / Step 4 — narrowest possible rollback primitive: copy ONE
    operator-named file from a snapshot tree back over its live
    counterpart inside ``environment.dump_path``. Whole-tree restore
    is **out of scope** of this tool.

    Contract:

    - Mutating; goes through :func:`run_write_flow` with full
      preflight + snapshot + operation + verify + audit discipline.
    - ``relative_path`` must resolve to a path **inside**
      ``environment.dump_path`` (no escape via absolute paths or
      ``..`` segments). Rejects fail-closed.
    - ``snapshot_file_path`` must point at an existing regular file.
      Missing or non-regular path → fail-closed.
    - Parent directories of the live target are created on demand
      (one operation, scoped to the dump tree). No unrelated
      directories are touched.
    - In-flow ``verify`` confirms byte-equality between the live
      target and the snapshot file after the copy.
    """
    if (
        not relative_path
        or not isinstance(relative_path, str)
        or not relative_path.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="restore_dump_file_from_snapshot",
            message="relative_path must be a non-empty string.",
            payload={"data": {"relative_path": relative_path}},
        )
    if (
        not snapshot_file_path
        or not isinstance(snapshot_file_path, str)
        or not snapshot_file_path.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="restore_dump_file_from_snapshot",
            message="snapshot_file_path must be a non-empty string.",
            payload={
                "data": {
                    "relative_path": relative_path,
                    "snapshot_file_path": snapshot_file_path,
                }
            },
        )

    snapshot_path = Path(snapshot_file_path)
    if not snapshot_path.exists():
        return ToolResult(
            ok=False,
            tool_name="restore_dump_file_from_snapshot",
            message=f"snapshot_file_path does not exist: {snapshot_path}",
            payload={
                "data": {
                    "relative_path": relative_path,
                    "snapshot_file_path": str(snapshot_path),
                }
            },
        )
    if not snapshot_path.is_file():
        return ToolResult(
            ok=False,
            tool_name="restore_dump_file_from_snapshot",
            message=f"snapshot_file_path is not a regular file: {snapshot_path}",
            payload={
                "data": {
                    "relative_path": relative_path,
                    "snapshot_file_path": str(snapshot_path),
                }
            },
        )

    dump_root = Path(environment.dump_path).resolve()
    rel = relative_path.replace("\\", "/")
    if rel.startswith("/") or ".." in Path(rel).parts:
        return ToolResult(
            ok=False,
            tool_name="restore_dump_file_from_snapshot",
            message=(
                "relative_path must be a relative path inside dump_path; "
                "absolute paths and '..' segments are not allowed."
            ),
            payload={
                "data": {
                    "relative_path": relative_path,
                    "snapshot_file_path": str(snapshot_path),
                }
            },
        )

    intent = WriteIntent("restore_dump_file_from_snapshot", relative_path)

    def operation(ctx):
        live_root = Path(ctx.environment.dump_path).resolve()
        target = (live_root / rel).resolve()
        # Containment check: target must really be inside dump_path.
        try:
            target.relative_to(live_root)
        except ValueError as exc:
            raise PermissionError(
                f"Restore target escapes dump_path: {target}"
            ) from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        snapshot_bytes = snapshot_path.read_bytes()
        # Atomic write through tmp + replace, identical pattern to the
        # rest of the write surface.
        tmp = target.with_name(target.name + ".restore.tmp")
        tmp.write_bytes(snapshot_bytes)
        tmp.replace(target)
        return {
            "changed": True,
            "relative_path": rel,
            "snapshot_file_path": str(snapshot_path),
            "restored_bytes": len(snapshot_bytes),
        }

    def verify(ctx, operation_payload):
        live_root = Path(ctx.environment.dump_path).resolve()
        target = (live_root / rel).resolve()
        if not target.is_file():
            raise AssertionError(
                f"Restore target missing after copy: {target}"
            )
        live_bytes = target.read_bytes()
        snapshot_bytes = snapshot_path.read_bytes()
        if live_bytes != snapshot_bytes:
            raise AssertionError(
                "Live dump file does not match snapshot baseline after "
                f"restore: {target}"
            )
        return {
            "verified": True,
            "relative_path": rel,
            "snapshot_file_path": str(snapshot_path),
            "byte_equal": True,
            "byte_count": len(live_bytes),
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "restore_dump_file_from_snapshot")


def _verify_form_attribute_exists_internal(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str,
    attribute_name: str,
) -> ToolResult:
    """Internal helper for ``verify_metadata_change(kind='form_attribute_exists')``.

    Read-only DOM-style check: resolves the object's XML card, parses
    it via ``parse_xml_file``, looks up the ``<Form name=form_name>``
    via :func:`find_form_element`, and checks the form's own
    ``<Attributes>`` block via :func:`form_has_attribute`. The
    ``tool_name`` on the returned :class:`ToolResult` is internal —
    the dispatcher in :func:`verify_metadata_change` rewraps it.

    Reads the dump through :func:`read_dump_file` (consistent with
    :func:`_verify_form_exists_internal`) so the check goes through
    the existing dump adapter rather than touching the filesystem
    directly. ``PlatformError`` from the adapter and
    ``ET.ParseError`` from a malformed card both translate into
    ``ok=False`` with a concrete message — no crash.
    """
    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_attribute_exists_internal",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_name": attribute_name,
                    "exists": False,
                }
            },
        )
    try:
        text = read_dump_file(environment, relative_path)
    except PlatformError as exc:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_attribute_exists_internal",
            message=str(exc),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_name": attribute_name,
                    "relative_path": relative_path,
                    "exists": False,
                }
            },
        )

    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_attribute_exists_internal",
            message=f"Object XML is not well-formed: {exc}",
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_name": attribute_name,
                    "relative_path": relative_path,
                    "exists": False,
                }
            },
        )

    form = find_form_element(root, form_name)
    if form is None:
        return ToolResult(
            ok=False,
            tool_name="_verify_form_attribute_exists_internal",
            message=(
                f"Form {form_name!r} not found in {relative_path}."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_name": attribute_name,
                    "relative_path": relative_path,
                    "exists": False,
                }
            },
        )

    exists = form_has_attribute(form, attribute_name)
    return ToolResult(
        ok=exists,
        tool_name="_verify_form_attribute_exists_internal",
        message=(
            "Form attribute exists in dump XML."
            if exists
            else "Form attribute not found in dump XML."
        ),
        payload={
            "data": {
                "object_name": object_name,
                "form_name": form_name,
                "attribute_name": attribute_name,
                "relative_path": relative_path,
                "exists": exists,
            }
        },
    )


def add_form_attribute(
    environment: EnvironmentConfig,
    object_name: str,
    form_name: str,
    attribute_spec: dict,
    label: str = "add-form-attribute",
) -> ToolResult:
    """Add a new attribute to a managed form's ``<Attributes>`` block.

    Phase 6 / Step 5 — first true structural XML edit slice. Unlike
    :func:`add_catalog_attribute` and :func:`add_document_attribute`
    (which use the long-standing substring helper
    :func:`insert_fragment_into_named_block`), this tool parses the
    object's XML card with ``xml.etree.ElementTree``, locates the
    target ``<Form name="form_name">`` element via
    :func:`find_form_element`, structurally creates an
    ``<Attributes>`` child if it is missing
    (:func:`get_or_create_form_attributes_block`), checks duplicates
    by attribute ``name`` attribute (not text substring) via
    :func:`form_has_attribute`, and appends a new
    ``<Attribute name="...">`` element via
    :func:`add_attribute_to_form_attributes_block`. The tree is then
    written back via :func:`write_xml_file` (UTF-8 + XML declaration,
    empty containers stay open).

    Routed strictly through :func:`run_write_flow` (preflight +
    snapshots + operation + verify + audit). Pre-flow validation
    rejects bad inputs before the flow even starts; failures during
    the flow surface via the standard ``stage`` markers (``operation``
    / ``verify`` / etc.) without any back-door write channel.

    Contract:

    - ``object_name`` must use a supported prefix
      (``Справочник.<name>`` or ``Документ.<name>``); otherwise
      ``ok=False`` pre-flow.
    - ``form_name`` must match the existing module-name discipline
      (``\\w+``); otherwise ``ok=False`` pre-flow.
    - ``attribute_spec`` must be a dict with non-empty
      whitespace-stripped ``name``, ``type`` ∈
      :data:`_ALLOWED_ATTR_TYPES` (``String`` / ``Number`` /
      ``Date``), and an optional ``synonym``.
    - The target form must exist in the card; otherwise the operation
      fails fail-closed at the ``operation`` stage (no rfind / no
      substring fallback).
    - If the form has no ``<Attributes>`` block yet, the tool
      structurally **creates** it; the tool does not require the
      block to be pre-present.
    - If an ``<Attribute name="attr_name">`` element is already
      present inside the form's own ``<Attributes>``, the tool fails
      fail-closed (``operation`` stage) without modifying the file.
    - In-flow ``verify`` re-parses the card and confirms the new
      attribute is present inside the same form via
      :func:`form_has_attribute`. Substring presence in the file
      text is **not** sufficient — the check is structural.

    Limitations honestly documented:

    - No XML namespace handling. 1С production cards typically carry
      ``xmlns="http://v8.1c.ru/8.3/MDClasses"``; namespaced cards
      are out of scope for this Step 5 slice and would need explicit
      namespace plumbing.
    - ``ElementTree`` does not preserve original whitespace /
      pretty-print exactly; the file may be re-serialized in a
      slightly different but equivalent form.
    - ``add_catalog_attribute`` / ``add_document_attribute``
      (object-level Attributes) are **not** rewritten on this step;
      they keep their existing substring-based path. Step 5 ships
      the structural-edit slice point-wise, not as a sweep.
    """
    if (
        not object_name
        or not isinstance(object_name, str)
        or not object_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message="object_name must be a non-empty string.",
            payload={"data": {"object_name": object_name}},
        )
    if (
        not form_name
        or not isinstance(form_name, str)
        or not _MODULE_NAME_RE.fullmatch(form_name)
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message=(
                f"Invalid form_name: {form_name!r}. "
                "Allowed: Latin/Cyrillic letters, digits, underscore; "
                "non-empty; no spaces."
            ),
            payload={
                "data": {"object_name": object_name, "form_name": form_name}
            },
        )
    if not isinstance(attribute_spec, dict):
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message="attribute_spec must be a dict.",
            payload={
                "data": {"object_name": object_name, "form_name": form_name}
            },
        )
    attr_name = attribute_spec.get("name")
    attr_type = attribute_spec.get("type")
    synonym = attribute_spec.get("synonym")
    if (
        not attr_name
        or not isinstance(attr_name, str)
        or attr_name != attr_name.strip()
    ):
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message=(
                "attribute_spec.name must be a non-empty string without "
                "leading/trailing whitespace."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )
    if not attr_type or attr_type not in _ALLOWED_ATTR_TYPES:
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message=(
                f"attribute_spec.type must be one of "
                f"{sorted(_ALLOWED_ATTR_TYPES)}."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )

    relative_path = _resolve_object_xml_path(object_name)
    if relative_path is None:
        return ToolResult(
            ok=False,
            tool_name="add_form_attribute",
            message=(
                f"Unsupported object_name prefix: {object_name!r}. "
                "Expected 'Справочник.<name>' or 'Документ.<name>'."
            ),
            payload={
                "data": {
                    "object_name": object_name,
                    "form_name": form_name,
                    "attribute_spec": attribute_spec,
                }
            },
        )

    intent = WriteIntent("add_form_attribute", form_name)

    def _resolve_target(ctx):
        return Path(ctx.environment.dump_path) / relative_path

    def operation(ctx):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise FileNotFoundError(
                f"Object XML not found in dump: {relative_path}"
            )

        tree = parse_xml_file(target)
        root = tree.getroot()

        form = find_form_element(root, form_name)
        if form is None:
            raise ValueError(
                f"Form {form_name!r} not found in {relative_path}."
            )

        if form_has_attribute(form, attr_name):
            raise FileExistsError(
                f"Attribute {attr_name!r} already exists in form "
                f"{form_name!r} of {relative_path}."
            )

        attributes_block_pre_existing = form.find("Attributes") is not None
        attrs_block = get_or_create_form_attributes_block(form)
        add_attribute_to_form_attributes_block(
            attrs_block, attr_name, attr_type, synonym
        )
        write_xml_file(target, tree)

        return {
            "changed": True,
            "object_name": object_name,
            "form_name": form_name,
            "attribute_name": attr_name,
            "attribute_type": attr_type,
            "relative_path": relative_path,
            "attributes_block_created": not attributes_block_pre_existing,
        }

    def verify(ctx, operation_payload):
        target = _resolve_target(ctx)
        if not target.is_file():
            raise AssertionError(
                f"Object XML missing after add_form_attribute: {relative_path}"
            )
        tree = parse_xml_file(target)
        root = tree.getroot()
        form = find_form_element(root, form_name)
        if form is None:
            raise AssertionError(
                f"Form {form_name!r} disappeared after add_form_attribute: "
                f"{relative_path}."
            )
        if not form_has_attribute(form, attr_name):
            raise AssertionError(
                f"Attribute {attr_name!r} not present in form {form_name!r} "
                f"after add_form_attribute: {relative_path}."
            )
        return {
            "verified": True,
            "object_name": object_name,
            "form_name": form_name,
            "attribute_name": attr_name,
            "attribute_type": attr_type,
            "relative_path": relative_path,
        }

    result = run_write_flow(
        environment,
        intent,
        label=label,
        operation_callable=operation,
        verify_callable=verify,
    )
    return _with_tool_name(result, "add_form_attribute")
