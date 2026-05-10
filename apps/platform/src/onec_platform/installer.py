"""Install / setup fast path (Phase 6 / Step 3).

Two boundary helpers, both fail-closed and never-raising at the
boundary:

- :func:`inspect_release_layout` — read-only check that a directory
  has the shape of a 1C Agent Platform release / source checkout.
- :func:`run_install_fast_path` — preview by default; on
  ``confirm_write=True`` materialises a JSON product-config at the
  operator-chosen path and re-loads it through the existing
  :func:`bootstrap_product_from_json_file` to confirm it is readable.

What this module is, very precisely:

- a small product-layer helper that **reduces** the manual install
  ritual (read sources → guess product-config layout → write JSON →
  bootstrap_doctor) to **one boundary call**;
- it does not start MCP servers, it does not invoke any
  ``mcp_write_server`` tool, it does not touch an infobase, it does
  not use shell;
- it only writes the operator-declared JSON config to disk when the
  operator passed ``confirm_write=True`` and the target path is free
  (no silent overwrite);
- there is no GUI installer, no MSI, no .deb, no packaging
  ecosystem — those belong to a parallel track that is explicitly
  out of Phase 6 / Step 3 scope.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .bootstrap import (
    bootstrap_product,
    bootstrap_product_from_json_file,
)
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import (
    BootstrapResult,
    DEFAULT_LOG_MAX_BYTES,
    DoctorFinding,
    INSTALL_MODES,
    InstallFastPathResult,
    ProductConfig,
    ReleaseLayoutReport,
)


# ---------------------------------------------------------------------------
# Constants — single source of truth for the Step 3 release layout.
# ---------------------------------------------------------------------------

# Top-level entries the helper expects in a release / source checkout.
# Honest minimum: every monorepo-style snapshot of this project carries
# these exactly, and nothing else is implied. The helper does **not**
# walk subtrees or guess content — it only checks presence at the root.
_EXPECTED_RELEASE_ENTRIES: tuple[str, ...] = (
    "apps",
    "packages",
    "docs",
    "README.md",
    "PROJECT-STATUS.md",
)


# ---------------------------------------------------------------------------
# Finding factories.
# ---------------------------------------------------------------------------


def _ok(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="ok", confidence=confidence, detail=detail
    )


def _warn(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="warning", confidence=confidence, detail=detail
    )


def _err(code: str, detail: str, *, confidence: str = "confirmed") -> DoctorFinding:
    return DoctorFinding(
        code=code, severity="error", confidence=confidence, detail=detail
    )


# ---------------------------------------------------------------------------
# Boundary: inspect_release_layout.
# ---------------------------------------------------------------------------


def inspect_release_layout(root_path: str | Path) -> ReleaseLayoutReport:
    """Honest read-only inspection of a release / source layout.

    ``ok=True`` means the inspection step itself ran (root path is a
    directory that we could read). Missing expected entries appear as
    findings — they are honest signals, not boundary failures.
    ``ok=False`` is reserved for "root path is absent / not a
    directory" — there is nothing to inspect.

    The inspection does **not** open any file inside the directory;
    it only checks top-level entries. No content guessing.
    """
    p = Path(root_path)
    if not p.exists():
        return ReleaseLayoutReport(
            ok=False,
            root_path=str(p),
            is_directory=False,
            expected_entries=list(_EXPECTED_RELEASE_ENTRIES),
            present_entries=[],
            missing_entries=list(_EXPECTED_RELEASE_ENTRIES),
            confirmed_findings=[
                _err(
                    "release_root_missing",
                    f"Release root path does not exist: {p}",
                )
            ],
            recommended_actions=[
                f"Verify the release root path: {p}.",
            ],
            message=f"Release root path does not exist: {p}",
        )
    if not p.is_dir():
        return ReleaseLayoutReport(
            ok=False,
            root_path=str(p),
            is_directory=False,
            expected_entries=list(_EXPECTED_RELEASE_ENTRIES),
            present_entries=[],
            missing_entries=list(_EXPECTED_RELEASE_ENTRIES),
            confirmed_findings=[
                _err(
                    "release_root_not_directory",
                    f"Release root path is not a directory: {p}",
                )
            ],
            recommended_actions=[
                f"Pass a directory path, not a file: {p}.",
            ],
            message=f"Release root path is not a directory: {p}",
        )

    confirmed: list[DoctorFinding] = [
        _ok(
            "release_root_resolved",
            f"Release root path is a directory: {p}",
        )
    ]
    presumed: list[DoctorFinding] = []
    actions: list[str] = []
    present: list[str] = []
    missing: list[str] = []

    for name in _EXPECTED_RELEASE_ENTRIES:
        entry = p / name
        if entry.exists():
            present.append(name)
            confirmed.append(
                _ok(
                    f"release_entry_present:{name}",
                    f"Expected entry present: {name}",
                )
            )
        else:
            missing.append(name)
            confirmed.append(
                _warn(
                    f"release_entry_missing:{name}",
                    f"Expected entry not found at root: {name}",
                )
            )
            actions.append(
                f"If this is a release / source checkout, ensure "
                f"{name!r} is present at the root."
            )

    if missing:
        message = (
            f"Layout inspection completed: {len(present)} expected entries "
            f"present, {len(missing)} missing."
        )
    else:
        message = "Layout inspection completed: all expected entries present."

    return ReleaseLayoutReport(
        ok=True,
        root_path=str(p),
        is_directory=True,
        expected_entries=list(_EXPECTED_RELEASE_ENTRIES),
        present_entries=present,
        missing_entries=missing,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        message=message,
    )


# ---------------------------------------------------------------------------
# Internal helpers for run_install_fast_path.
# ---------------------------------------------------------------------------


def _resolve_input_config(
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
        "Input must be a dict or a pre-loaded ProductConfig "
        f"(got {type(data).__name__})."
    )


def _config_to_dict(config: ProductConfig) -> dict:
    """Project a :class:`ProductConfig` into its JSON-serialisable shape.

    Mirrors the dict layout that
    :func:`onec_platform.loader.load_product_config` reads back. Only
    fields known to the loader are emitted; nothing speculative.
    """
    envs: dict[str, dict] = {}
    for key, env in config.project.environments.items():
        env_block: dict[str, Any] = {
            "name": env.name,
            "base_id": env.base_id,
            "base_path": env.base_path,
            "publication_name": env.publication_name,
            "http_base_url": env.http_base_url,
            "dump_path": env.dump_path,
            "timeout_seconds": env.timeout_seconds,
            "allow_write": env.allow_write,
        }
        if env.onec_binary_path is not None:
            env_block["onec_binary_path"] = env.onec_binary_path
        if env.onec_binary_probe_args is not None:
            env_block["onec_binary_probe_args"] = list(env.onec_binary_probe_args)
        if env.onec_dumpcfg_command_template is not None:
            env_block["onec_dumpcfg_command_template"] = list(
                env.onec_dumpcfg_command_template
            )
        envs[key] = env_block

    runtime_services: dict[str, dict] = {}
    for name, spec in config.runtime.services.items():
        svc: dict[str, Any] = {
            "enabled": spec.enabled,
            "command": list(spec.command) if spec.command else None,
            "working_dir": spec.working_dir,
            "env_overrides": dict(spec.env_overrides),
        }
        # Phase 6 / Step 6 service-level fields. Emit each one only
        # when it deviates from the dataclass default so Step 1–5
        # configs round-trip byte-identical.
        if spec.restart_policy != "never":
            svc["restart_policy"] = spec.restart_policy
        if spec.logs_enabled is not True:
            svc["logs_enabled"] = spec.logs_enabled
        if spec.log_max_bytes != DEFAULT_LOG_MAX_BYTES:
            svc["log_max_bytes"] = spec.log_max_bytes
        runtime_services[name] = svc

    out: dict = {
        "product_name": config.product_name,
        "profile_name": config.profile_name,
        "default_environment": config.default_environment,
        "project": {"environments": envs},
        "servers": {
            "read": config.servers.read,
            "write": config.servers.write,
            "intelligence": config.servers.intelligence,
        },
        "bootstrap": {
            "work_dir": config.bootstrap.work_dir,
            "require_dump_path": config.bootstrap.require_dump_path,
            "require_base_path": config.bootstrap.require_base_path,
            "require_python": config.bootstrap.require_python,
        },
        "runtime": {"services": runtime_services},
    }

    # Phase 6 / Step 8 — preserve the operator's enterprise-foundation
    # block through the install fast path round-trip. Emit only the
    # fields that diverge from the empty default so Step 1–7 configs
    # without an enterprise block remain byte-identical (no implicit
    # ``"enterprise": {...defaults...}`` injection).
    enterprise_block: dict[str, Any] = {}
    e = config.enterprise
    if e.deployment_tier is not None:
        enterprise_block["deployment_tier"] = e.deployment_tier
    if e.instance_id is not None:
        enterprise_block["instance_id"] = e.instance_id
    if e.config_owner is not None:
        enterprise_block["config_owner"] = e.config_owner
    if e.change_control_required:
        enterprise_block["change_control_required"] = True
    if e.require_operator_identity:
        enterprise_block["require_operator_identity"] = True
    if e.runbook_reference is not None:
        enterprise_block["runbook_reference"] = e.runbook_reference
    if enterprise_block:
        out["enterprise"] = enterprise_block

    # Track I / Step 4 — preserve the operator's auth.tokens
    # declarations through the install fast path round-trip. Emit
    # only when the token list is non-empty so pre-Track-H configs
    # without an auth block remain byte-identical (no implicit
    # ``"auth": {}`` injection). Token strings are round-tripped
    # raw as configuration data; ``${ENV:NAME}`` env-substitution
    # form is preserved character-by-character. Resolution remains
    # the runtime boundary in
    # ``packages/mcp-common/src/mcp_common/_network_transport.py``.
    auth_block: dict[str, Any] = {}
    if config.auth.tokens:
        auth_block["tokens"] = list(config.auth.tokens)
    if auth_block:
        out["auth"] = auth_block

    return out


def _rejected(message: str) -> InstallFastPathResult:
    return InstallFastPathResult(
        ok=False,
        mode="rejected",
        product_name=None,
        profile_name=None,
        default_environment=None,
        output_config_path=None,
        config_written=False,
        layout_report=None,
        bootstrap_pre=None,
        bootstrap_post=None,
        template_preview=None,
        confirmed_findings=[_err("install_rejected", message)],
        presumed_findings=[],
        recommended_actions=[],
        message=message,
    )


def _write_product_config_template(
    template: dict, output_path: Path
) -> tuple[bool, str | None]:
    """Atomically write ``template`` as JSON to ``output_path``.

    Internal helper. Creates the parent directory if it does not yet
    exist (this is part of the "reduce ritual" goal — operator should
    not have to ``mkdir`` the parent themselves). Returns ``(True,
    None)`` on success, ``(False, error_message)`` on failure. Does
    not raise.
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return False, f"Failed to create parent directory: {exc}"
    try:
        text = json.dumps(template, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as exc:
        return False, f"Failed to serialise product config to JSON: {exc}"
    tmp_path = output_path.with_name(output_path.name + ".tmp")
    try:
        tmp_path.write_text(text, encoding="utf-8")
        tmp_path.replace(output_path)
    except OSError as exc:
        # Best-effort cleanup of the temp file.
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except OSError:
            pass
        return False, f"Failed to write product config: {exc}"
    return True, None


# ---------------------------------------------------------------------------
# Boundary: run_install_fast_path.
# ---------------------------------------------------------------------------


def run_install_fast_path(
    data: dict | ProductConfig,
    *,
    output_config_path: str | Path,
    confirm_write: bool = False,
) -> InstallFastPathResult:
    """Reduce the manual install ritual to one boundary call.

    Steps:

    1. Resolve / validate the input product config (uses the existing
       :func:`load_product_config` contract).
    2. Inspect the release layout at the project root inferred from
       ``output_config_path``'s nearest existing ancestor — purely
       informational; missing entries do not block the helper.
    3. Run :func:`bootstrap_product` against the input config
       (pre-write bootstrap).
    4. Project the loaded config into a JSON-serialisable template
       (re-using :func:`_config_to_dict`).
    5. If ``confirm_write=False``: stop here, ``mode="preview"``, no
       file is written. The template is returned under
       :attr:`template_preview` for the operator to inspect.
    6. If ``confirm_write=True``: refuse to overwrite an existing
       target (``mode="rejected"``); otherwise write the JSON, then
       re-load it through :func:`bootstrap_product_from_json_file` to
       confirm round-trip readability (post-write bootstrap).

    This helper **never** runs MCP servers, **never** invokes write-
    tools, **never** touches an infobase. It is a thin product-layer
    fast path; a real industrial installer is out of scope.
    """
    output_path = Path(output_config_path)
    confirmed: list[DoctorFinding] = []
    presumed: list[DoctorFinding] = []
    actions: list[str] = []

    config, err = _resolve_input_config(data)
    if config is None:
        return _rejected(err or "Unknown configuration error.")

    layout = inspect_release_layout(_infer_layout_root(output_path))
    if layout.missing_entries:
        presumed.append(
            _warn(
                "install_layout_partial",
                f"Release layout inspection at {layout.root_path!r} found "
                f"{len(layout.missing_entries)} missing top-level "
                f"entries: {layout.missing_entries}.",
                confidence="presumed",
            )
        )

    bootstrap_pre = bootstrap_product(_config_to_dict(config))
    confirmed.append(
        _ok(
            "install_bootstrap_pre_ran",
            f"Pre-write bootstrap_product completed: {bootstrap_pre.message}",
        )
    )

    template_preview = _config_to_dict(config)

    if not confirm_write:
        actions.append(
            "Re-run with confirm_write=True to materialise the product "
            f"config at {output_path}."
        )
        return InstallFastPathResult(
            ok=True,
            mode="preview",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            output_config_path=str(output_path),
            config_written=False,
            layout_report=layout,
            bootstrap_pre=bootstrap_pre,
            bootstrap_post=None,
            template_preview=template_preview,
            confirmed_findings=confirmed,
            presumed_findings=presumed,
            recommended_actions=actions,
            message=(
                "Install fast path preview built. No file written. Pass "
                "confirm_write=True to materialise the product config."
            ),
        )

    if output_path.exists():
        # Refuse to overwrite silently — Step 3 ships honest install
        # discipline, not "magic re-install". Operator can resolve by
        # picking a fresh path or removing the existing file.
        return InstallFastPathResult(
            ok=False,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            output_config_path=str(output_path),
            config_written=False,
            layout_report=layout,
            bootstrap_pre=bootstrap_pre,
            bootstrap_post=None,
            template_preview=template_preview,
            confirmed_findings=confirmed
            + [
                _err(
                    "output_config_path_exists",
                    f"Refusing to overwrite existing file: {output_path}.",
                )
            ],
            presumed_findings=presumed,
            recommended_actions=[
                "Pick a different output_config_path, or remove the "
                "existing file manually before re-running."
            ],
            message=(
                f"Refusing to overwrite existing file: {output_path}. "
                "No silent overwrite from the install fast path."
            ),
        )

    written, write_err = _write_product_config_template(
        template_preview, output_path
    )
    if not written:
        return InstallFastPathResult(
            ok=False,
            mode="rejected",
            product_name=config.product_name,
            profile_name=config.profile_name,
            default_environment=config.default_environment,
            output_config_path=str(output_path),
            config_written=False,
            layout_report=layout,
            bootstrap_pre=bootstrap_pre,
            bootstrap_post=None,
            template_preview=template_preview,
            confirmed_findings=confirmed
            + [_err("config_write_failed", write_err or "Unknown error.")],
            presumed_findings=presumed,
            recommended_actions=actions,
            message=write_err or "Failed to write product config.",
        )

    confirmed.append(
        _ok(
            "config_written",
            f"Product config written to: {output_path}",
        )
    )

    bootstrap_post = bootstrap_product_from_json_file(output_path)
    if not bootstrap_post.ok:
        confirmed.append(
            _err(
                "bootstrap_post_failed",
                f"Re-loading the freshly-written config failed: "
                f"{bootstrap_post.message}",
            )
        )
    else:
        confirmed.append(
            _ok(
                "bootstrap_post_ok",
                "Re-loaded the freshly-written config through "
                "bootstrap_product_from_json_file successfully.",
            )
        )

    actions.append(
        "Run the existing runtime / dashboard / workflow boundaries "
        "(start_product_runtime, build_environment_dashboard, etc.) "
        "as separate, explicit steps. The install fast path does NOT "
        "start servers."
    )

    return InstallFastPathResult(
        ok=bool(bootstrap_post.ok),
        mode="executed",
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        output_config_path=str(output_path),
        config_written=True,
        layout_report=layout,
        bootstrap_pre=bootstrap_pre,
        bootstrap_post=bootstrap_post,
        template_preview=template_preview,
        confirmed_findings=confirmed,
        presumed_findings=presumed,
        recommended_actions=actions,
        message=(
            "Install fast path executed: config written and re-loaded "
            "through bootstrap_product_from_json_file. Runtime / workflow "
            "/ real-stand boundaries are NOT started by this helper — "
            "operator runs them explicitly as the next step."
        ),
    )


def run_install_fast_path_from_json_file(
    path: str | Path,
    *,
    output_config_path: str | Path,
    confirm_write: bool = False,
) -> InstallFastPathResult:
    """Like :func:`run_install_fast_path`, but read product config from JSON.

    Boundary helper. Never raises. Missing / malformed JSON ends up as
    ``mode="rejected", ok=False`` with an honest error finding.
    """
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _rejected(f"Product config rejected: {exc}")
    except Exception as exc:  # noqa: BLE001 — boundary, never propagate
        return _rejected(f"Product config could not be loaded: {exc}")
    return run_install_fast_path(
        config,
        output_config_path=output_config_path,
        confirm_write=confirm_write,
    )


# ---------------------------------------------------------------------------
# Layout-root inference helper.
# ---------------------------------------------------------------------------


def _infer_layout_root(output_path: Path) -> Path:
    """Pick the closest existing ancestor of ``output_path`` for layout
    inspection.

    The fast path tolerates the operator pointing
    ``output_config_path`` at a brand-new directory: the layout
    inspector is fed the closest existing ancestor instead, so it
    has *something* honest to report on. If even the cwd does not
    exist (extremely unlikely), the helper falls back to the path
    itself and the inspector reports it honestly.
    """
    candidate = output_path.parent if output_path.parent != output_path else output_path
    while True:
        if candidate.exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            return output_path
        candidate = parent


__all__ = [
    "INSTALL_MODES",
    "inspect_release_layout",
    "run_install_fast_path",
    "run_install_fast_path_from_json_file",
]
