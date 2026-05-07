"""Guided workflow layer (Phase 5 / Step 5).

Single product-level orchestration boundary that walks an operator
through three honest end-to-end scenarios on top of the existing
read / write / intelligence surfaces:

- ``safe-add-attribute`` — preview plan → confirm → real
  ``add_catalog_attribute`` / ``add_document_attribute`` →
  ``verify_attribute_exists`` → ``describe_last_write_operation`` /
  ``prepare_rollback_hint``;
- ``safe-add-module-method`` — preview plan → confirm → real
  ``append_module_method`` → ``verify_module_contains`` →
  ``describe_last_write_operation`` / ``prepare_rollback_hint``;
- ``stand-health-check`` — read-only diagnostic over the dashboard
  + ``analyze_runtime_issue`` + ``summarize_configuration_risk``.

What this module is NOT:

- it does **not** introduce new MCP tools or modify any registry;
- it does **not** invent its own write path — every mutating step
  goes through the real public write-tool, which itself wraps
  ``run_write_flow`` (preflight → snapshot → operation → verify →
  audit). No bypass of write-side safety guarantees;
- it does **not** import :mod:`onec_policy_engine` and never makes
  policy decisions of its own — the write-tool's own preflight
  enforces ``allow_write`` and health gates;
- it does **not** silent-apply: a mutating workflow with
  ``confirm_execute=False`` always stops at the preview boundary;
- it is **not** Step 6 rollback / recovery UX — it merely surfaces
  the existing ``describe_last_write_operation`` /
  ``prepare_rollback_hint`` outputs so Step 6 can build on them.

Failure model:

- :func:`run_guided_workflow` and
  :func:`run_guided_workflow_from_json_file` **never raise**.
- ``ok=True`` covers three honest outcomes:
  successful preview, successful diagnostic, successful execution.
- ``ok=False`` covers four honest outcomes: rejected config,
  unknown workflow name, dashboard-blocked mutating workflow,
  failed mutating execution. Already-built plan and intelligence
  steps are preserved on the result so the operator can see how
  far the workflow got.

Tool-name discipline:

- Both ``WorkflowPlan.suggested_tools`` and
  ``WorkflowPlan.suggested_write_tools`` only contain names that
  exist in one of the live registries
  (:func:`mcp_read_server.list_tools`,
  :func:`mcp_write_server.list_tools`,
  :func:`mcp_intelligence_server.list_tools`) plus a fixed
  whitelist of platform-layer boundary helpers
  (:data:`_KNOWN_PLATFORM_FUNCTIONS`). Unknown names are dropped
  and not silently surfaced.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from onec_config import EnvironmentConfig

# Cross-app imports: product → read, product → intelligence,
# product → write. All registered public surfaces only; no private
# runtime imports beyond the explicitly published Python functions.
import mcp_intelligence_server as _mis
import mcp_read_server as _mrs
import mcp_write_server as _mws
from mcp_intelligence_server.tools import (
    analyze_runtime_issue,
    estimate_change_impact,
    find_affected_modules,
    suggest_metadata_patch_plan,
    suggest_safe_change_order,
    summarize_configuration_risk,
)
from mcp_write_server.tools import (
    add_catalog_attribute,
    add_document_attribute,
    add_form_attribute,
    append_module_method,
    describe_last_write_operation,
    prepare_rollback_hint,
    verify_attribute_exists,
    verify_metadata_change,
    verify_module_contains,
)

from .dashboard import build_environment_dashboard
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    DoctorFinding,
    EnvironmentDashboardResult,
    ProductConfig,
    WORKFLOW_MODES,
    WORKFLOW_NAMES,
    WorkflowPlan,
    WorkflowRunResult,
    WorkflowStepResult,
)

# ---------------------------------------------------------------------------
# Real-tool-name whitelist plumbing.
# ---------------------------------------------------------------------------

# Platform-layer boundary helpers that callers may legitimately see
# named in ``suggested_tools``. Kept tight on purpose.
_KNOWN_PLATFORM_FUNCTIONS: frozenset[str] = frozenset(
    {
        "bootstrap_product",
        "bootstrap_product_from_json_file",
        "build_environment_dashboard",
        "build_environment_dashboard_from_json_file",
        "get_product_runtime_status",
        "start_product_runtime",
        "stop_product_runtime",
        "reload_product_runtime",
        "run_guided_workflow",
        "run_guided_workflow_from_json_file",
    }
)


def _allowed_tool_names() -> set[str]:
    """Return the live union of registered public tool names.

    Computed at call time (not at import time) so that a server
    registry change in the same process is observed honestly. Adds
    the small fixed :data:`_KNOWN_PLATFORM_FUNCTIONS` whitelist.
    """
    return (
        set(_mrs.list_tools())
        | set(_mws.list_tools())
        | set(_mis.list_tools())
        | set(_KNOWN_PLATFORM_FUNCTIONS)
    )


def _allow_only_real_tools(names: list[str]) -> list[str]:
    """Filter ``names`` down to those that actually exist on the platform.

    Preserves order and drops duplicates. The runner never includes
    an unknown name in :attr:`WorkflowPlan.suggested_tools` /
    :attr:`WorkflowPlan.suggested_write_tools` — anything that is not
    a real public tool is silently dropped (and would also be caught
    by the manual-check assertions). This keeps the operator-visible
    plan honest.
    """
    allowed = _allowed_tool_names()
    seen: set[str] = set()
    out: list[str] = []
    for raw in names:
        if not isinstance(raw, str):
            continue
        if raw in seen or raw not in allowed:
            continue
        seen.add(raw)
        out.append(raw)
    return out


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
# Result-building helpers.
# ---------------------------------------------------------------------------


def _rejected_result(workflow_name: str, message: str) -> WorkflowRunResult:
    return WorkflowRunResult(
        ok=False,
        workflow_name=workflow_name,
        mode="rejected",
        product_name=None,
        profile_name=None,
        default_environment=None,
        ready_for_workflows=False,
        execution_performed=False,
        plan=None,
        steps=[],
        confirmed_findings=[_err("config_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        rollback_hint=None,
        message=message,
    )


def _unknown_workflow_result(workflow_name: str) -> WorkflowRunResult:
    return WorkflowRunResult(
        ok=False,
        workflow_name=workflow_name,
        mode="rejected",
        product_name=None,
        profile_name=None,
        default_environment=None,
        ready_for_workflows=False,
        execution_performed=False,
        plan=None,
        steps=[],
        confirmed_findings=[
            _err(
                "workflow_unknown",
                f"Unknown workflow {workflow_name!r}. "
                f"Known workflows: {sorted(WORKFLOW_NAMES)}.",
            )
        ],
        presumed_findings=[],
        recommended_actions=[],
        suggested_tools=[],
        suggested_write_tools=[],
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        rollback_hint=None,
        message=(
            f"Unknown workflow {workflow_name!r}. "
            f"Known workflows: {sorted(WORKFLOW_NAMES)}."
        ),
    )


# ---------------------------------------------------------------------------
# Step builders for foreign ToolResults.
# ---------------------------------------------------------------------------


def _step_from_tool_result(
    name: str,
    kind: str,
    source: str,
    result: Any,
) -> WorkflowStepResult:
    """Wrap an ``mcp_common.ToolResult`` into a :class:`WorkflowStepResult`.

    Robust against unexpected payload shapes — anything that is not a
    dict ends up as an empty payload.
    """
    payload = result.payload if isinstance(getattr(result, "payload", None), dict) else {}
    return WorkflowStepResult(
        name=name,
        kind=kind,
        ok=bool(getattr(result, "ok", False)),
        source=source,
        payload=payload,
        message=str(getattr(result, "message", "")),
    )


# ---------------------------------------------------------------------------
# Dashboard precondition.
# ---------------------------------------------------------------------------


def _build_dashboard_step(
    config: ProductConfig,
) -> tuple[EnvironmentDashboardResult, WorkflowStepResult]:
    """Build the dashboard once and project it into a step result."""
    dash = build_environment_dashboard(config)
    payload = {
        "ok": dash.ok,
        "verdict": (asdict(dash.verdict) if dash.verdict is not None else None),
        "sources_used": list(dash.sources_used),
        "sections": {
            name: {
                "ok": section.ok,
                "source": section.source,
                "message": section.message,
            }
            for name, section in dash.sections.items()
        },
        "message": dash.message,
    }
    step = WorkflowStepResult(
        name="precondition_dashboard",
        kind="precondition",
        ok=dash.ok,
        source="platform.build_environment_dashboard",
        payload=payload,
        message=dash.message,
    )
    return dash, step


# ---------------------------------------------------------------------------
# Plan extraction helpers.
# ---------------------------------------------------------------------------


def _impact_level_from(payload: dict) -> str | None:
    presumed = payload.get("presumed_findings") if isinstance(payload, dict) else None
    if not isinstance(presumed, list):
        return None
    for item in presumed:
        if isinstance(item, dict) and item.get("pattern") == "impact_estimate":
            level = item.get("impact_level")
            if isinstance(level, str):
                return level
    return None


def _risk_level_from(payload: dict) -> str | None:
    if isinstance(payload, dict):
        level = payload.get("risk_level")
        if isinstance(level, str):
            return level
    return None


# ---------------------------------------------------------------------------
# safe-add-attribute.
# ---------------------------------------------------------------------------


_VALID_ATTRIBUTE_KINDS: frozenset[str] = frozenset({"catalog", "document"})


def _validate_attribute_params(params: dict) -> str | None:
    target_kind = params.get("target_kind")
    if target_kind not in _VALID_ATTRIBUTE_KINDS:
        return (
            f"params.target_kind must be one of {sorted(_VALID_ATTRIBUTE_KINDS)}; "
            f"got {target_kind!r}."
        )
    object_name = params.get("object_name")
    if not isinstance(object_name, str) or not object_name.strip():
        return "params.object_name must be a non-empty string."
    attribute_spec = params.get("attribute_spec")
    if not isinstance(attribute_spec, dict):
        return "params.attribute_spec must be a dict."
    if not isinstance(attribute_spec.get("name"), str) or not attribute_spec["name"]:
        return "params.attribute_spec.name must be a non-empty string."
    if not isinstance(attribute_spec.get("type"), str) or not attribute_spec["type"]:
        return "params.attribute_spec.type must be a non-empty string."
    return None


def _full_object_name(target_kind: str, name: str) -> str:
    """Build a Cyrillic full-object name accepted by verify_attribute_exists."""
    if target_kind == "catalog":
        return f"Справочник.{name}"
    if target_kind == "document":
        return f"Документ.{name}"
    return name


def _patch_kind_for_attribute(target_kind: str) -> str:
    return "catalog_attribute" if target_kind == "catalog" else "document_attribute"


def _run_safe_add_attribute(
    config: ProductConfig,
    env: EnvironmentConfig,
    params: dict,
    confirm_execute: bool,
) -> WorkflowRunResult:
    workflow_name = "safe-add-attribute"
    steps: list[WorkflowStepResult] = []

    # 0. Param validation.
    err = _validate_attribute_params(params)
    if err is not None:
        return WorkflowRunResult(
            ok=False,
            workflow_name=workflow_name,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            ready_for_workflows=False,
            execution_performed=False,
            plan=None,
            steps=steps,
            confirmed_findings=[_err("workflow_params_invalid", err)],
            presumed_findings=[],
            recommended_actions=[],
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            rollback_hint=None,
            message=err,
        )

    target_kind = params["target_kind"]
    object_name = params["object_name"]
    attribute_spec = params["attribute_spec"]
    full_object = _full_object_name(target_kind, object_name)

    # 1. Dashboard precondition.
    dash, dashboard_step = _build_dashboard_step(config)
    steps.append(dashboard_step)
    ready = bool(dash.verdict and dash.verdict.ready_for_workflows)
    if not ready:
        return _blocked_result(
            workflow_name, config, dash, steps,
            reason="Mutating workflow blocked: dashboard.ready_for_workflows is False.",
        )

    # 2. Intelligence steps — collect signals for the plan.
    impact = estimate_change_impact(env, object_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_estimate_change_impact",
            "intelligence",
            "intelligence.estimate_change_impact",
            impact,
        )
    )
    safe_order = suggest_safe_change_order(env, object_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_suggest_safe_change_order",
            "intelligence",
            "intelligence.suggest_safe_change_order",
            safe_order,
        )
    )
    patch_kind = _patch_kind_for_attribute(target_kind)
    plan_tool = suggest_metadata_patch_plan(
        env,
        target_kind=patch_kind,
        target_name=object_name,
        change_goal=f"add attribute {attribute_spec['name']!r} to {target_kind} {object_name!r}",
    )
    steps.append(
        _step_from_tool_result(
            "intelligence_suggest_metadata_patch_plan",
            "intelligence",
            "intelligence.suggest_metadata_patch_plan",
            plan_tool,
        )
    )
    risk = summarize_configuration_risk(env, object_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_summarize_configuration_risk",
            "intelligence",
            "intelligence.summarize_configuration_risk",
            risk,
        )
    )

    # 3. Operator-visible plan.
    impact_level = _impact_level_from(impact.payload if isinstance(impact.payload, dict) else {})
    risk_level = _risk_level_from(risk.payload if isinstance(risk.payload, dict) else {})

    plan_summary: list[str] = [
        f"Workflow: {workflow_name}",
        f"Target: {target_kind} {object_name!r}",
        f"Add attribute {attribute_spec['name']!r} (type={attribute_spec.get('type')!r}).",
        (
            f"Estimated impact: {impact_level or 'unknown'} "
            f"(see intelligence.estimate_change_impact)."
        ),
        f"Risk level: {risk_level or 'unknown'} (see intelligence.summarize_configuration_risk).",
        (
            "Mutating step will go through write-server's run_write_flow: "
            "preflight -> backup snapshot -> dump snapshot -> operation -> "
            "verify -> audit. The product layer does not bypass this."
        ),
    ]
    write_tool_name = (
        "add_catalog_attribute" if target_kind == "catalog" else "add_document_attribute"
    )
    plan = WorkflowPlan(
        workflow_name=workflow_name,
        target_kind=target_kind,
        target_name=object_name,
        summary=plan_summary,
        suggested_tools=_allow_only_real_tools(
            [
                "estimate_change_impact",
                "suggest_safe_change_order",
                "suggest_metadata_patch_plan",
                "summarize_configuration_risk",
                "verify_attribute_exists",
                "build_environment_dashboard",
            ]
        ),
        suggested_write_tools=_allow_only_real_tools(
            [
                write_tool_name,
                "verify_attribute_exists",
                "describe_last_write_operation",
                "prepare_rollback_hint",
            ]
        ),
        impact_level=impact_level,
        risk_level=risk_level,
    )

    # 4. Confirm gate.
    if not confirm_execute:
        return _preview_result(workflow_name, config, ready, plan, steps)

    # 5. Execute mutating step (real write-tool).
    write_call = (
        add_catalog_attribute(env, object_name, attribute_spec)
        if target_kind == "catalog"
        else add_document_attribute(env, object_name, attribute_spec)
    )
    write_step = _step_from_tool_result(
        f"execute_{write_tool_name}",
        "mutating",
        f"write.{write_tool_name}",
        write_call,
    )
    steps.append(write_step)
    write_results = [_tool_result_dict(write_call)]

    # 6. Verify (only if write step ran cleanly OR just attempt and report).
    verify_step: WorkflowStepResult | None = None
    verify_results: list[dict] = []
    if write_step.ok:
        verify_call = verify_attribute_exists(env, full_object, attribute_spec["name"])
        verify_step = _step_from_tool_result(
            "verify_attribute_exists",
            "verify",
            "write.verify_attribute_exists",
            verify_call,
        )
        steps.append(verify_step)
        verify_results.append(_tool_result_dict(verify_call))

    # 7. Audit / rollback hint.
    last_op_dict, rollback_dict = _collect_audit_artifacts(env, steps)

    overall_ok = write_step.ok and (verify_step is None or verify_step.ok)
    return _executed_result(
        workflow_name,
        config,
        plan,
        steps,
        ready=True,
        ok=overall_ok,
        write_results=write_results,
        verify_results=verify_results,
        last_write_operation=last_op_dict,
        rollback_hint=rollback_dict,
    )


# ---------------------------------------------------------------------------
# safe-add-form-attribute (Phase 6 / Step 9 — minimal addition for the
# final integration pass).
#
# Why this exists: Phase 6 / Step 5 added the public mutating
# write-tool ``add_form_attribute`` (the first true structural XML
# edit slice) but did not wrap it in a guided workflow. The Step 9
# integration brief explicitly asks for a connected
# ``run_guided_workflow`` chain that internally exercises
# ``add_form_attribute``. This is the smallest honest addition that
# closes that gap: a thin guided wrapper that mirrors the existing
# ``safe-add-attribute`` discipline (preview → confirm → real
# write-tool through ``run_write_flow`` → verify → audit + rollback
# hint surface).
#
# It does NOT add a new MCP tool. It does NOT bypass run_write_flow.
# Like its siblings, it is a thin product-layer guide on top of an
# already-public write-tool.
# ---------------------------------------------------------------------------


def _validate_form_attribute_params(params: dict) -> str | None:
    object_name = params.get("object_name")
    if not isinstance(object_name, str) or not object_name.strip():
        return "params.object_name must be a non-empty string."
    form_name = params.get("form_name")
    if not isinstance(form_name, str) or not form_name.strip():
        return "params.form_name must be a non-empty string."
    attribute_spec = params.get("attribute_spec")
    if not isinstance(attribute_spec, dict):
        return "params.attribute_spec must be a dict."
    if not isinstance(attribute_spec.get("name"), str) or not attribute_spec["name"]:
        return "params.attribute_spec.name must be a non-empty string."
    if not isinstance(attribute_spec.get("type"), str) or not attribute_spec["type"]:
        return "params.attribute_spec.type must be a non-empty string."
    return None


def _run_safe_add_form_attribute(
    config: ProductConfig,
    env: EnvironmentConfig,
    params: dict,
    confirm_execute: bool,
) -> WorkflowRunResult:
    workflow_name = "safe-add-form-attribute"
    steps: list[WorkflowStepResult] = []

    err = _validate_form_attribute_params(params)
    if err is not None:
        return WorkflowRunResult(
            ok=False,
            workflow_name=workflow_name,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            ready_for_workflows=False,
            execution_performed=False,
            plan=None,
            steps=steps,
            confirmed_findings=[_err("workflow_params_invalid", err)],
            presumed_findings=[],
            recommended_actions=[],
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            rollback_hint=None,
            message=err,
        )

    object_name = params["object_name"]
    form_name = params["form_name"]
    attribute_spec = params["attribute_spec"]

    # 1. Dashboard precondition.
    dash, dashboard_step = _build_dashboard_step(config)
    steps.append(dashboard_step)
    ready = bool(dash.verdict and dash.verdict.ready_for_workflows)
    if not ready:
        return _blocked_result(
            workflow_name, config, dash, steps,
            reason=(
                "Mutating workflow blocked: dashboard.ready_for_workflows is False."
            ),
        )

    # 2. Intelligence signals — same set as safe-add-attribute, since
    # form-level attributes share the same risk/impact heuristics
    # surface from the operator's point of view.
    impact = estimate_change_impact(env, object_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_estimate_change_impact",
            "intelligence",
            "intelligence.estimate_change_impact",
            impact,
        )
    )
    risk = summarize_configuration_risk(env, object_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_summarize_configuration_risk",
            "intelligence",
            "intelligence.summarize_configuration_risk",
            risk,
        )
    )

    impact_level = _impact_level_from(
        impact.payload if isinstance(impact.payload, dict) else {}
    )
    risk_level = _risk_level_from(
        risk.payload if isinstance(risk.payload, dict) else {}
    )

    plan_summary: list[str] = [
        f"Workflow: {workflow_name}",
        f"Target form: {form_name!r} on object {object_name!r}",
        f"Add attribute {attribute_spec['name']!r} (type={attribute_spec.get('type')!r}).",
        (
            f"Estimated impact: {impact_level or 'unknown'} "
            "(see intelligence.estimate_change_impact)."
        ),
        (
            f"Risk level: {risk_level or 'unknown'} "
            "(see intelligence.summarize_configuration_risk)."
        ),
        (
            "Mutating step uses add_form_attribute, the structural "
            "ElementTree-based XML edit slice (Phase 6 / Step 5). It "
            "goes through write-server's run_write_flow: preflight -> "
            "backup snapshot -> dump snapshot -> operation -> verify "
            "-> audit. The product layer does not bypass this."
        ),
        (
            "Note: automatic recovery whitelist (Phase 6 / Step 4) "
            "currently covers add_catalog_attribute and "
            "add_document_attribute only — add_form_attribute is "
            "advisory-only. The rollback assistant will say so honestly."
        ),
    ]
    plan = WorkflowPlan(
        workflow_name=workflow_name,
        target_kind="form_attribute",
        target_name=f"{object_name}::{form_name}",
        summary=plan_summary,
        suggested_tools=_allow_only_real_tools(
            [
                "estimate_change_impact",
                "summarize_configuration_risk",
                "verify_metadata_change",
                "build_environment_dashboard",
            ]
        ),
        suggested_write_tools=_allow_only_real_tools(
            [
                "add_form_attribute",
                "verify_metadata_change",
                "describe_last_write_operation",
                "prepare_rollback_hint",
            ]
        ),
        impact_level=impact_level,
        risk_level=risk_level,
    )

    # 3. Confirm gate.
    if not confirm_execute:
        return _preview_result(workflow_name, config, ready, plan, steps)

    # 4. Execute mutating step (real write-tool).
    write_call = add_form_attribute(env, object_name, form_name, attribute_spec)
    write_step = _step_from_tool_result(
        "execute_add_form_attribute",
        "mutating",
        "write.add_form_attribute",
        write_call,
    )
    steps.append(write_step)
    write_results = [_tool_result_dict(write_call)]

    # 5. Verify (only when the write step actually ran cleanly).
    verify_step: WorkflowStepResult | None = None
    verify_results: list[dict] = []
    if write_step.ok:
        verify_call = verify_metadata_change(
            env,
            {
                "kind": "form_attribute_exists",
                "object_name": object_name,
                "form_name": form_name,
                "attribute_name": attribute_spec["name"],
            },
        )
        verify_step = _step_from_tool_result(
            "verify_form_attribute_exists",
            "verify",
            "write.verify_metadata_change",
            verify_call,
        )
        steps.append(verify_step)
        verify_results.append(_tool_result_dict(verify_call))

    # 6. Audit / rollback hint surface (read-only).
    last_op_dict, rollback_dict = _collect_audit_artifacts(env, steps)

    overall_ok = write_step.ok and (verify_step is None or verify_step.ok)
    return _executed_result(
        workflow_name,
        config,
        plan,
        steps,
        ready=True,
        ok=overall_ok,
        write_results=write_results,
        verify_results=verify_results,
        last_write_operation=last_op_dict,
        rollback_hint=rollback_dict,
    )


# ---------------------------------------------------------------------------
# safe-add-module-method.
# ---------------------------------------------------------------------------


def _validate_module_method_params(params: dict) -> str | None:
    mrp = params.get("module_relative_path")
    if not isinstance(mrp, str) or not mrp.strip():
        return "params.module_relative_path must be a non-empty string."
    method_spec = params.get("method_spec")
    if not isinstance(method_spec, dict):
        return "params.method_spec must be a dict."
    if not isinstance(method_spec.get("name"), str) or not method_spec["name"]:
        return "params.method_spec.name must be a non-empty string."
    body = method_spec.get("body")
    if not isinstance(body, str) or not body.strip():
        return "params.method_spec.body must be a non-empty, non-whitespace string."
    return None


def _run_safe_add_module_method(
    config: ProductConfig,
    env: EnvironmentConfig,
    params: dict,
    confirm_execute: bool,
) -> WorkflowRunResult:
    workflow_name = "safe-add-module-method"
    steps: list[WorkflowStepResult] = []

    err = _validate_module_method_params(params)
    if err is not None:
        return WorkflowRunResult(
            ok=False,
            workflow_name=workflow_name,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            ready_for_workflows=False,
            execution_performed=False,
            plan=None,
            steps=steps,
            confirmed_findings=[_err("workflow_params_invalid", err)],
            presumed_findings=[],
            recommended_actions=[],
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            rollback_hint=None,
            message=err,
        )

    module_relative_path = params["module_relative_path"]
    method_spec = params["method_spec"]
    method_name = method_spec["name"]

    # 1. Dashboard precondition.
    dash, dashboard_step = _build_dashboard_step(config)
    steps.append(dashboard_step)
    ready = bool(dash.verdict and dash.verdict.ready_for_workflows)
    if not ready:
        return _blocked_result(
            workflow_name, config, dash, steps,
            reason="Mutating workflow blocked: dashboard.ready_for_workflows is False.",
        )

    # 2. Intelligence steps.
    impact = estimate_change_impact(env, method_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_estimate_change_impact",
            "intelligence",
            "intelligence.estimate_change_impact",
            impact,
        )
    )
    affected_modules = find_affected_modules(env, method_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_find_affected_modules",
            "intelligence",
            "intelligence.find_affected_modules",
            affected_modules,
        )
    )
    safe_order = suggest_safe_change_order(env, method_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_suggest_safe_change_order",
            "intelligence",
            "intelligence.suggest_safe_change_order",
            safe_order,
        )
    )
    plan_tool = suggest_metadata_patch_plan(
        env,
        target_kind="module_method",
        target_name=method_name,
        change_goal=f"append method {method_name!r} to {module_relative_path}",
    )
    steps.append(
        _step_from_tool_result(
            "intelligence_suggest_metadata_patch_plan",
            "intelligence",
            "intelligence.suggest_metadata_patch_plan",
            plan_tool,
        )
    )
    risk = summarize_configuration_risk(env, method_name)
    steps.append(
        _step_from_tool_result(
            "intelligence_summarize_configuration_risk",
            "intelligence",
            "intelligence.summarize_configuration_risk",
            risk,
        )
    )

    impact_level = _impact_level_from(impact.payload if isinstance(impact.payload, dict) else {})
    risk_level = _risk_level_from(risk.payload if isinstance(risk.payload, dict) else {})
    plan_summary: list[str] = [
        f"Workflow: {workflow_name}",
        f"Target module: {module_relative_path}",
        f"Append method {method_name!r} (export={method_spec.get('export', False)}).",
        f"Estimated impact (using method name as needle): {impact_level or 'unknown'}.",
        f"Risk level: {risk_level or 'unknown'}.",
        (
            "Mutating step will go through write-server's run_write_flow: "
            "preflight -> backup snapshot -> dump snapshot -> operation -> "
            "verify -> audit."
        ),
    ]
    plan = WorkflowPlan(
        workflow_name=workflow_name,
        target_kind="module_method",
        target_name=method_name,
        summary=plan_summary,
        suggested_tools=_allow_only_real_tools(
            [
                "estimate_change_impact",
                "find_affected_modules",
                "suggest_safe_change_order",
                "suggest_metadata_patch_plan",
                "summarize_configuration_risk",
                "verify_module_contains",
                "build_environment_dashboard",
            ]
        ),
        suggested_write_tools=_allow_only_real_tools(
            [
                "append_module_method",
                "verify_module_contains",
                "describe_last_write_operation",
                "prepare_rollback_hint",
            ]
        ),
        impact_level=impact_level,
        risk_level=risk_level,
    )

    if not confirm_execute:
        return _preview_result(workflow_name, config, ready, plan, steps)

    write_call = append_module_method(env, module_relative_path, method_spec)
    write_step = _step_from_tool_result(
        "execute_append_module_method",
        "mutating",
        "write.append_module_method",
        write_call,
    )
    steps.append(write_step)
    write_results = [_tool_result_dict(write_call)]

    verify_step: WorkflowStepResult | None = None
    verify_results: list[dict] = []
    if write_step.ok:
        verify_call = verify_module_contains(env, module_relative_path, method_name)
        verify_step = _step_from_tool_result(
            "verify_module_contains",
            "verify",
            "write.verify_module_contains",
            verify_call,
        )
        steps.append(verify_step)
        verify_results.append(_tool_result_dict(verify_call))

    last_op_dict, rollback_dict = _collect_audit_artifacts(env, steps)

    overall_ok = write_step.ok and (verify_step is None or verify_step.ok)
    return _executed_result(
        workflow_name,
        config,
        plan,
        steps,
        ready=True,
        ok=overall_ok,
        write_results=write_results,
        verify_results=verify_results,
        last_write_operation=last_op_dict,
        rollback_hint=rollback_dict,
    )


# ---------------------------------------------------------------------------
# stand-health-check (read-only diagnostic).
# ---------------------------------------------------------------------------


def _run_stand_health_check(
    config: ProductConfig,
    env: EnvironmentConfig,
    params: dict,
    confirm_execute: bool,
) -> WorkflowRunResult:
    workflow_name = "stand-health-check"
    if confirm_execute:
        # Honest pass-through: read-only workflow ignores confirm_execute,
        # but we surface it so the operator sees they're in diagnostic mode.
        pass
    steps: list[WorkflowStepResult] = []

    dash, dashboard_step = _build_dashboard_step(config)
    steps.append(dashboard_step)

    runtime_call = analyze_runtime_issue(env)
    steps.append(
        _step_from_tool_result(
            "intelligence_analyze_runtime_issue",
            "diagnostic",
            "intelligence.analyze_runtime_issue",
            runtime_call,
        )
    )

    risk_call = summarize_configuration_risk(env)
    steps.append(
        _step_from_tool_result(
            "intelligence_summarize_configuration_risk",
            "diagnostic",
            "intelligence.summarize_configuration_risk",
            risk_call,
        )
    )

    risk_level = _risk_level_from(risk_call.payload if isinstance(risk_call.payload, dict) else {})
    overall_status = (
        dash.verdict.overall_status if dash.verdict is not None else "unknown"
    )

    plan_summary = [
        f"Workflow: {workflow_name} (read-only).",
        f"Dashboard verdict: overall_status={overall_status}.",
        f"Configuration risk level: {risk_level or 'unknown'}.",
        "No mutating steps. Operator can run this even on degraded environments.",
    ]
    plan = WorkflowPlan(
        workflow_name=workflow_name,
        target_kind=None,
        target_name=None,
        summary=plan_summary,
        suggested_tools=_allow_only_real_tools(
            [
                "build_environment_dashboard",
                "analyze_runtime_issue",
                "summarize_configuration_risk",
                "check_runtime_health",
                "diagnose_connectivity_issue",
                "get_product_runtime_status",
            ]
        ),
        suggested_write_tools=[],
        impact_level=None,
        risk_level=risk_level,
    )

    confirmed, presumed, actions = _aggregate_step_findings(steps, dash)
    suggested_tools, suggested_write_tools = _aggregate_suggested(plan)

    overall_ok = dash.ok  # diagnostic ran iff the dashboard ran
    ready = bool(dash.verdict and dash.verdict.ready_for_workflows)

    return WorkflowRunResult(
        ok=overall_ok,
        workflow_name=workflow_name,
        mode="diagnostic",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        ready_for_workflows=ready,
        execution_performed=False,
        plan=plan,
        steps=steps,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        rollback_hint=None,
        message=(
            f"stand-health-check diagnostic complete. overall_status={overall_status}, "
            f"risk_level={risk_level or 'unknown'}."
        ),
    )


# ---------------------------------------------------------------------------
# Result aggregation helpers.
# ---------------------------------------------------------------------------


def _aggregate_step_findings(
    steps: list[WorkflowStepResult],
    dash: EnvironmentDashboardResult | None,
) -> tuple[list[DoctorFinding], list[DoctorFinding], list[str]]:
    """Aggregate confirmed/presumed/actions across step payloads + dashboard.

    Each finding is tagged with the originating step name for
    traceability — same provenance discipline as the dashboard.
    """
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    seen_actions: set[str] = set()

    if dash is not None:
        for f in dash.confirmed_findings:
            confirmed.append(_tag(f, f"dashboard/{f.code}"))
        for f in dash.presumed_findings:
            presumed.append(_tag(f, f"dashboard/{f.code}"))
        for action in dash.recommended_actions:
            if action and action not in seen_actions:
                seen_actions.add(action)
                actions.append(action)

    for step in steps:
        payload = step.payload if isinstance(step.payload, dict) else {}
        # Most read/intelligence ToolResults expose confirmed_findings /
        # presumed_findings / recommended_checks / recommended_actions.
        cf = payload.get("confirmed_findings")
        if isinstance(cf, list):
            for item in cf:
                f = _normalise_finding(item, "confirmed", step.name)
                if f is not None:
                    confirmed.append(f)
        pf = payload.get("presumed_findings")
        if isinstance(pf, list):
            for item in pf:
                f = _normalise_finding(item, "presumed", step.name)
                if f is not None:
                    presumed.append(f)
        for key in ("recommended_actions", "recommended_checks"):
            value = payload.get(key)
            if isinstance(value, list):
                for action in value:
                    if isinstance(action, str) and action and action not in seen_actions:
                        seen_actions.add(action)
                        actions.append(action)

    return confirmed, presumed, actions


def _aggregate_suggested(plan: WorkflowPlan) -> tuple[list[str], list[str]]:
    """Funnel suggested-tool lists from the plan through the real-name filter
    once more (defensive)."""
    return (
        _allow_only_real_tools(plan.suggested_tools),
        _allow_only_real_tools(plan.suggested_write_tools),
    )


def _tag(finding: DoctorFinding, new_code: str) -> DoctorFinding:
    return DoctorFinding(
        code=new_code,
        severity=finding.severity,
        confidence=finding.confidence,
        detail=finding.detail,
    )


def _normalise_finding(
    item: Any, confidence: str, step_name: str
) -> DoctorFinding | None:
    """Turn a foreign ToolResult finding (free-shape dict) into a tagged
    :class:`DoctorFinding`."""
    if not isinstance(item, dict):
        return DoctorFinding(
            code=f"{step_name}/intelligence_finding",
            severity="warning",
            confidence=confidence,
            detail=str(item),
        )
    code_raw = (
        item.get("code")
        or item.get("pattern")
        or item.get("problem_code")
        or "intelligence_finding"
    )
    detail = str(
        item.get("detail")
        or item.get("probable_cause")
        or item.get("hint")
        or item.get("recommended_action")
        or item.get("category")
        or ""
    )
    severity = item.get("severity") or (
        "error" if confidence == "confirmed" else "warning"
    )
    if severity not in ("ok", "warning", "error"):
        severity = "warning"
    return DoctorFinding(
        code=f"{step_name}/{code_raw}",
        severity=severity,
        confidence=confidence,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Mutating helpers — audit, rollback, dictify.
# ---------------------------------------------------------------------------


def _tool_result_dict(result: Any) -> dict:
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


def _operation_id_from(result_dict: dict) -> str | None:
    payload = result_dict.get("payload")
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not isinstance(data, dict):
        return None
    op_id = data.get("operation_id")
    return op_id if isinstance(op_id, str) else None


def _collect_audit_artifacts(
    env: EnvironmentConfig,
    steps: list[WorkflowStepResult],
) -> tuple[dict | None, dict | None]:
    """Best-effort post-write lookup of last operation + rollback hint.

    Both tools are read-only and never mutate audit state. Failures
    here are surfaced as step results but do not flip the overall
    workflow ``ok`` — the mutating step + verify step are
    authoritative.
    """
    last_call = describe_last_write_operation(env)
    last_step = _step_from_tool_result(
        "audit_describe_last_write_operation",
        "audit",
        "write.describe_last_write_operation",
        last_call,
    )
    steps.append(last_step)
    last_op_dict: dict | None = None
    if last_call.ok and isinstance(last_call.payload, dict):
        data = last_call.payload.get("data")
        if isinstance(data, dict):
            last_op_dict = dict(data)

    rollback_dict: dict | None = None
    if last_op_dict is not None:
        op_id = last_op_dict.get("operation_id")
        if isinstance(op_id, str) and op_id:
            rb_call = prepare_rollback_hint(env, op_id)
            rb_step = _step_from_tool_result(
                "audit_prepare_rollback_hint",
                "audit",
                "write.prepare_rollback_hint",
                rb_call,
            )
            steps.append(rb_step)
            if rb_call.ok and isinstance(rb_call.payload, dict):
                data = rb_call.payload.get("data")
                if isinstance(data, dict):
                    rollback_dict = dict(data)
    return last_op_dict, rollback_dict


# ---------------------------------------------------------------------------
# Result assembly: preview / blocked / executed.
# ---------------------------------------------------------------------------


def _preview_result(
    workflow_name: str,
    config: ProductConfig,
    ready: bool,
    plan: WorkflowPlan,
    steps: list[WorkflowStepResult],
) -> WorkflowRunResult:
    confirmed, presumed, actions = _aggregate_step_findings(steps, None)
    suggested_tools, suggested_write_tools = _aggregate_suggested(plan)
    return WorkflowRunResult(
        ok=True,
        workflow_name=workflow_name,
        mode="preview",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        ready_for_workflows=ready,
        execution_performed=False,
        plan=plan,
        steps=steps,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        rollback_hint=None,
        message=(
            f"{workflow_name}: preview built. Pass confirm_execute=True "
            "to actually execute the plan."
        ),
    )


def _blocked_result(
    workflow_name: str,
    config: ProductConfig,
    dash: EnvironmentDashboardResult,
    steps: list[WorkflowStepResult],
    *,
    reason: str,
) -> WorkflowRunResult:
    confirmed, presumed, actions = _aggregate_step_findings(steps, dash)
    return WorkflowRunResult(
        ok=False,
        workflow_name=workflow_name,
        mode="blocked",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        ready_for_workflows=False,
        execution_performed=False,
        plan=None,
        steps=steps,
        confirmed_findings=confirmed
        + [_err("workflow_blocked_by_dashboard", reason)],
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=[],
        suggested_write_tools=[],
        write_results=[],
        verify_results=[],
        last_write_operation=None,
        rollback_hint=None,
        message=reason,
    )


def _executed_result(
    workflow_name: str,
    config: ProductConfig,
    plan: WorkflowPlan,
    steps: list[WorkflowStepResult],
    *,
    ready: bool,
    ok: bool,
    write_results: list[dict],
    verify_results: list[dict],
    last_write_operation: dict | None,
    rollback_hint: dict | None,
) -> WorkflowRunResult:
    confirmed, presumed, actions = _aggregate_step_findings(steps, None)
    suggested_tools, suggested_write_tools = _aggregate_suggested(plan)
    if ok:
        message = f"{workflow_name}: executed successfully."
    else:
        message = (
            f"{workflow_name}: execution attempted but reported failures; "
            "see write_results / verify_results / steps."
        )
    return WorkflowRunResult(
        ok=ok,
        workflow_name=workflow_name,
        mode="executed",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        ready_for_workflows=ready,
        execution_performed=True,
        plan=plan,
        steps=steps,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        suggested_tools=suggested_tools,
        suggested_write_tools=suggested_write_tools,
        write_results=write_results,
        verify_results=verify_results,
        last_write_operation=last_write_operation,
        rollback_hint=rollback_hint,
        message=message,
    )


# ---------------------------------------------------------------------------
# Public boundary helpers.
# ---------------------------------------------------------------------------


_WORKFLOW_RUNNERS = {
    "safe-add-attribute": _run_safe_add_attribute,
    "safe-add-module-method": _run_safe_add_module_method,
    "safe-add-form-attribute": _run_safe_add_form_attribute,
    "stand-health-check": _run_stand_health_check,
}


def run_guided_workflow(
    data: dict | ProductConfig,
    *,
    workflow_name: str,
    params: dict | None = None,
    confirm_execute: bool = False,
) -> WorkflowRunResult:
    """Run one guided workflow against a product config.

    Boundary-level. **Never raises.** Returns a structured
    :class:`WorkflowRunResult` whose ``mode`` is one of
    :data:`WORKFLOW_MODES`. Mutating workflows refuse to execute
    when ``confirm_execute`` is false (preview mode) or when the
    Step 4 dashboard is not in ``ready_for_workflows`` state
    (blocked mode).
    """
    if workflow_name not in _WORKFLOW_RUNNERS:
        return _unknown_workflow_result(workflow_name)

    config, err = _resolve_config(data)
    if config is None:
        return _rejected_result(workflow_name, err or "Unknown configuration error.")

    env = _resolve_environment(config)
    if env is None:
        return _rejected_result(
            workflow_name,
            f"Default environment {config.default_environment!r} is not "
            "present in project.environments.",
        )

    runner = _WORKFLOW_RUNNERS[workflow_name]
    actual_params = params if isinstance(params, dict) else {}
    try:
        return runner(config, env, actual_params, confirm_execute)
    except Exception as exc:  # noqa: BLE001 — boundary, must not propagate
        return WorkflowRunResult(
            ok=False,
            workflow_name=workflow_name,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            ready_for_workflows=False,
            execution_performed=False,
            plan=None,
            steps=[],
            confirmed_findings=[
                _err(
                    "workflow_unexpected_error",
                    f"Workflow runner raised: {exc}",
                )
            ],
            presumed_findings=[],
            recommended_actions=[],
            suggested_tools=[],
            suggested_write_tools=[],
            write_results=[],
            verify_results=[],
            last_write_operation=None,
            rollback_hint=None,
            message=f"Workflow runner raised: {exc}",
        )


def run_guided_workflow_from_json_file(
    path: str | Path,
    *,
    workflow_name: str,
    params: dict | None = None,
    confirm_execute: bool = False,
) -> WorkflowRunResult:
    """Like :func:`run_guided_workflow`, but loads product config from a JSON file.

    Never raises. JSON / file-system errors become an ``ok=False``
    result with ``mode="rejected"``.
    """
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected_result(workflow_name, f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _rejected_result(
            workflow_name,
            f"Product config could not be loaded: {exc}",
        )
    return run_guided_workflow(
        config,
        workflow_name=workflow_name,
        params=params,
        confirm_execute=confirm_execute,
    )


# Re-export the shared mode/name constants under workflow.py too — some
# callers prefer to discover them via the module that owns the runner.
__all__ = [
    "WORKFLOW_NAMES",
    "WORKFLOW_MODES",
    "run_guided_workflow",
    "run_guided_workflow_from_json_file",
]
