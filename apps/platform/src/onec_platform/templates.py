"""Declarative product-config template generator (Phase 6 / Step 3).

A tiny, honest helper: given a few mandatory fields (product name,
profile name, default environment, base / dump / publication URL),
returns a JSON-serialisable ``dict`` that matches the **current
contract** of :class:`onec_config.ProjectConfig` /
:class:`onec_config.EnvironmentConfig` and the product-layer wrapping
(server toggles, bootstrap settings, optional runtime contract,
optional binary-related fields).

Honesty constraints:

- The template is built strictly on top of fields that already exist
  in the loader contract today. No magic "future" fields.
- The template is returned as a dict; nothing is written to disk by
  this module. File-system side effects belong to
  :mod:`onec_platform.installer`.
- Internal validation raises :class:`ValueError` fail-closed; the
  installer boundary catches that and converts it into an honest
  ``ok=False`` :class:`ProductConfigTemplateResult`.
- No defaults are silently invented for security-relevant fields
  (e.g. ``allow_write`` defaults to ``False``, matching the existing
  ``EnvironmentConfig`` default — this is preserved here, not invented).
"""

from __future__ import annotations

from typing import Any

from .models import DEPLOYMENT_TIERS, DoctorFinding, ProductConfigTemplateResult


# ---------------------------------------------------------------------------
# Validation helpers.
# ---------------------------------------------------------------------------


def _require_non_empty_str(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name!r} must be a non-empty string.")
    return value


def _require_int_or_float(name: str, value: Any) -> int | float:
    if isinstance(value, bool):
        raise ValueError(f"{name!r} must be a number, not a bool.")
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name!r} must be an int or a float.")
    return value


def _validate_optional_str_list(name: str, value: Any) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list) or not value:
        raise ValueError(
            f"{name!r} must be a non-empty list of strings if present."
        )
    for entry in value:
        if not isinstance(entry, str):
            raise ValueError(
                f"{name!r} must contain only strings; got {type(entry).__name__}."
            )
    return list(value)


def _validate_optional_str(name: str, value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name!r} must be a string or None.")
    return value


# ---------------------------------------------------------------------------
# Public boundary.
# ---------------------------------------------------------------------------


def build_product_config_template(
    *,
    product_name: str,
    profile_name: str,
    default_environment: str,
    base_path: str,
    dump_path: str,
    http_base_url: str,
    publication_name: str | None = None,
    base_id: str | None = None,
    timeout_seconds: int | float = 30,
    allow_write: bool = False,
    work_dir: str | None = None,
    enable_read: bool = True,
    enable_write: bool = True,
    enable_intelligence: bool = True,
    runtime_services: dict[str, dict] | None = None,
    onec_binary_path: str | None = None,
    onec_binary_probe_args: list[str] | None = None,
    onec_dumpcfg_command_template: list[str] | None = None,
    enterprise_deployment_tier: str | None = None,
    enterprise_instance_id: str | None = None,
    enterprise_config_owner: str | None = None,
    enterprise_change_control_required: bool | None = None,
    enterprise_require_operator_identity: bool | None = None,
    enterprise_runbook_reference: str | None = None,
) -> ProductConfigTemplateResult:
    """Assemble a JSON-serialisable product-config template.

    Boundary helper: **never raises**. Internal validation issues are
    converted into ``ok=False`` results with one error finding; happy
    paths return the template under :attr:`ProductConfigTemplateResult.template`.

    Optional binary-related fields are emitted only when set — absent
    fields are simply omitted, matching the loader's contract that
    they are optional.
    """
    findings: list[DoctorFinding] = []

    try:
        product_name = _require_non_empty_str("product_name", product_name)
        profile_name = _require_non_empty_str("profile_name", profile_name)
        default_environment = _require_non_empty_str(
            "default_environment", default_environment
        )
        base_path = _require_non_empty_str("base_path", base_path)
        dump_path = _require_non_empty_str("dump_path", dump_path)
        http_base_url = _require_non_empty_str("http_base_url", http_base_url)
        if publication_name is None:
            publication_name = profile_name
        else:
            publication_name = _require_non_empty_str(
                "publication_name", publication_name
            )
        if base_id is None:
            base_id = default_environment
        else:
            base_id = _require_non_empty_str("base_id", base_id)
        timeout_seconds = _require_int_or_float("timeout_seconds", timeout_seconds)
        if not isinstance(allow_write, bool):
            raise ValueError("'allow_write' must be a bool.")
        work_dir = _validate_optional_str("work_dir", work_dir)
        if not isinstance(enable_read, bool):
            raise ValueError("'enable_read' must be a bool.")
        if not isinstance(enable_write, bool):
            raise ValueError("'enable_write' must be a bool.")
        if not isinstance(enable_intelligence, bool):
            raise ValueError("'enable_intelligence' must be a bool.")
        onec_binary_path = _validate_optional_str(
            "onec_binary_path", onec_binary_path
        )
        onec_binary_probe_args = _validate_optional_str_list(
            "onec_binary_probe_args", onec_binary_probe_args
        )
        onec_dumpcfg_command_template = _validate_optional_str_list(
            "onec_dumpcfg_command_template", onec_dumpcfg_command_template
        )

        # Phase 6 / Step 8 — optional enterprise-foundation knobs.
        # Each is independently optional; the template emits an
        # ``enterprise`` block only when at least one of them is
        # supplied. This keeps Step 1–7 templates byte-identical when
        # the operator does not care about enterprise foundation.
        if enterprise_deployment_tier is not None:
            if not isinstance(enterprise_deployment_tier, str):
                raise ValueError(
                    "'enterprise_deployment_tier' must be a string if provided."
                )
            if enterprise_deployment_tier not in DEPLOYMENT_TIERS:
                raise ValueError(
                    f"'enterprise_deployment_tier' must be one of "
                    f"{sorted(DEPLOYMENT_TIERS)}; got "
                    f"{enterprise_deployment_tier!r}."
                )
        enterprise_instance_id = _validate_optional_str(
            "enterprise_instance_id", enterprise_instance_id
        )
        if (
            enterprise_instance_id is not None
            and not enterprise_instance_id.strip()
        ):
            raise ValueError(
                "'enterprise_instance_id' must be non-empty if provided."
            )
        enterprise_config_owner = _validate_optional_str(
            "enterprise_config_owner", enterprise_config_owner
        )
        if (
            enterprise_config_owner is not None
            and not enterprise_config_owner.strip()
        ):
            raise ValueError(
                "'enterprise_config_owner' must be non-empty if provided."
            )
        enterprise_runbook_reference = _validate_optional_str(
            "enterprise_runbook_reference", enterprise_runbook_reference
        )
        if (
            enterprise_runbook_reference is not None
            and not enterprise_runbook_reference.strip()
        ):
            raise ValueError(
                "'enterprise_runbook_reference' must be non-empty if provided."
            )
        if (
            enterprise_change_control_required is not None
            and not isinstance(enterprise_change_control_required, bool)
        ):
            raise ValueError(
                "'enterprise_change_control_required' must be a bool if provided."
            )
        if (
            enterprise_require_operator_identity is not None
            and not isinstance(enterprise_require_operator_identity, bool)
        ):
            raise ValueError(
                "'enterprise_require_operator_identity' must be a bool if provided."
            )

        if runtime_services is not None:
            if not isinstance(runtime_services, dict):
                raise ValueError("'runtime_services' must be a dict if provided.")
            for svc_name, spec in runtime_services.items():
                if not isinstance(svc_name, str) or not svc_name:
                    raise ValueError(
                        "'runtime_services' keys must be non-empty strings."
                    )
                if not isinstance(spec, dict):
                    raise ValueError(
                        f"'runtime_services[{svc_name!r}]' must be a dict."
                    )
                if "enabled" in spec and not isinstance(spec["enabled"], bool):
                    raise ValueError(
                        f"'runtime_services[{svc_name!r}].enabled' must be bool."
                    )
                if "command" in spec and spec["command"] is not None:
                    cmd = spec["command"]
                    if not isinstance(cmd, list) or not cmd:
                        raise ValueError(
                            f"'runtime_services[{svc_name!r}].command' must be a "
                            "non-empty list of strings if present."
                        )
                    for entry in cmd:
                        if not isinstance(entry, str):
                            raise ValueError(
                                f"'runtime_services[{svc_name!r}].command' must "
                                "contain only strings."
                            )
    except ValueError as exc:
        return ProductConfigTemplateResult(
            ok=False,
            product_name=None,
            profile_name=None,
            default_environment=None,
            template={},
            findings=[
                DoctorFinding(
                    code="template_input_rejected",
                    severity="error",
                    confidence="confirmed",
                    detail=str(exc),
                )
            ],
            message=str(exc),
        )

    env_block: dict[str, Any] = {
        "name": profile_name,
        "base_id": base_id,
        "base_path": base_path,
        "publication_name": publication_name,
        "http_base_url": http_base_url,
        "dump_path": dump_path,
        "timeout_seconds": timeout_seconds,
        "allow_write": allow_write,
    }
    if onec_binary_path is not None:
        env_block["onec_binary_path"] = onec_binary_path
    if onec_binary_probe_args is not None:
        env_block["onec_binary_probe_args"] = list(onec_binary_probe_args)
    if onec_dumpcfg_command_template is not None:
        env_block["onec_dumpcfg_command_template"] = list(
            onec_dumpcfg_command_template
        )

    template: dict[str, Any] = {
        "product_name": product_name,
        "profile_name": profile_name,
        "default_environment": default_environment,
        "project": {"environments": {default_environment: env_block}},
        "servers": {
            "read": enable_read,
            "write": enable_write,
            "intelligence": enable_intelligence,
        },
        "bootstrap": {
            "work_dir": work_dir,
            "require_dump_path": True,
            "require_base_path": True,
            "require_python": True,
        },
    }
    if runtime_services is not None:
        template["runtime"] = {
            "services": {name: dict(spec) for name, spec in runtime_services.items()}
        }

    enterprise_block: dict[str, Any] = {}
    if enterprise_deployment_tier is not None:
        enterprise_block["deployment_tier"] = enterprise_deployment_tier
    if enterprise_instance_id is not None:
        enterprise_block["instance_id"] = enterprise_instance_id
    if enterprise_config_owner is not None:
        enterprise_block["config_owner"] = enterprise_config_owner
    if enterprise_change_control_required is not None:
        enterprise_block["change_control_required"] = (
            enterprise_change_control_required
        )
    if enterprise_require_operator_identity is not None:
        enterprise_block["require_operator_identity"] = (
            enterprise_require_operator_identity
        )
    if enterprise_runbook_reference is not None:
        enterprise_block["runbook_reference"] = enterprise_runbook_reference
    if enterprise_block:
        template["enterprise"] = enterprise_block

    if work_dir is None:
        findings.append(
            DoctorFinding(
                code="template_work_dir_absent",
                severity="warning",
                confidence="presumed",
                detail=(
                    "bootstrap.work_dir is unset in the generated template; "
                    "set it before running runtime orchestration / rollback / "
                    "dashboard helpers."
                ),
            )
        )
    if onec_binary_path is None or onec_dumpcfg_command_template is None:
        findings.append(
            DoctorFinding(
                code="template_binary_backed_inactive",
                severity="warning",
                confidence="presumed",
                detail=(
                    "Binary-backed dump path is not configured "
                    "(onec_binary_path or onec_dumpcfg_command_template "
                    "missing); create_dump_snapshot will use the legacy "
                    "stub mode until both are set."
                ),
            )
        )

    return ProductConfigTemplateResult(
        ok=True,
        product_name=product_name,
        profile_name=profile_name,
        default_environment=default_environment,
        template=template,
        findings=findings,
        message="Product-config template assembled.",
    )


__all__ = ["build_product_config_template"]
