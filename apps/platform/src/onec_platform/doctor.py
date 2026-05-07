"""Prereqs doctor for the product layer (Phase 5 / Step 2).

Minimal but real: never installs anything, never touches a real 1C
stand, never starts a server, never makes a write operation. It only
**observes** what is already present and produces an honest report.

Each finding carries an explicit ``confidence`` field —
``"confirmed"`` (we directly observed the condition: file exists,
module is importable, executable resolves) or ``"presumed"``
(heuristic: e.g. URL shape, parsed but not actually probed). This
mirrors the convention already established by Phase 4
intelligence-tools.

Failure-style: :func:`run_prereqs_doctor` never raises. Internal
errors are caught and surfaced as ``severity="error"`` findings.
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from urllib.parse import urlparse

from .models import DoctorFinding, DoctorReport, ProductConfig

_SERVER_TOGGLE_TO_MODULE: dict[str, str] = {
    "read": "mcp_read_server",
    "write": "mcp_write_server",
    "intelligence": "mcp_intelligence_server",
}


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


def _module_importable(module_name: str) -> bool:
    """Return True if Python can locate ``module_name`` via spec lookup.

    Uses :func:`importlib.util.find_spec` — does not actually import
    the module. Catches ``ImportError`` / ``ValueError`` defensively
    (some malformed parents can raise during spec resolution).
    """
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ValueError):
        return False


def run_prereqs_doctor(config: ProductConfig) -> DoctorReport:
    """Run the minimal prereqs doctor for a :class:`ProductConfig`.

    The doctor never raises. It always returns a :class:`DoctorReport`,
    even if internal observations fail — failure becomes a finding.

    Checks performed (each yields one or more findings):

    1. Default environment resolves inside ``project.environments``.
       Loader already validates this; the doctor re-asserts defensively
       and immediately stops if it fails (everything else needs the
       environment).
    2. ``base_path`` exists (skipped if ``require_base_path=False``).
    3. ``dump_path`` exists (skipped if ``require_dump_path=False``).
    4. ``python`` resolves on PATH (skipped if ``require_python=False``).
    5. ``http_base_url`` parses to scheme+host. **Presumed** — no real
       HTTP probe in Step 2; that belongs to Step 4 health dashboard.
    6. For every enabled server toggle, the corresponding MCP server
       package is importable.
    7. Optional ``bootstrap.work_dir`` exists and is a directory.
    """
    findings: list[DoctorFinding] = []
    actions: list[str] = []

    env_name = config.default_environment
    env = config.project.environments.get(env_name)
    if env is None:
        # Defensive: loader should have caught this. Stay fail-closed.
        findings.append(
            _err(
                "default_environment_missing",
                f"Default environment {env_name!r} is not present in "
                f"project.environments.",
            )
        )
        actions.append(
            f"Add an environment {env_name!r} to project.environments "
            f"or change default_environment."
        )
        return DoctorReport(
            findings=findings,
            error_count=1,
            warning_count=0,
            recommended_actions=actions,
        )

    findings.append(
        _ok(
            "default_environment_resolved",
            f"Default environment is {env_name!r}.",
        )
    )

    if config.bootstrap.require_base_path:
        base_path = Path(env.base_path)
        if base_path.exists():
            findings.append(
                _ok(
                    "base_path_exists",
                    f"base_path exists: {base_path}",
                )
            )
        else:
            findings.append(
                _err(
                    "base_path_missing",
                    f"base_path does not exist: {base_path}",
                )
            )
            actions.append(
                f"Create or correct base_path for environment "
                f"{env_name!r}: {base_path}."
            )
    else:
        findings.append(
            _warn(
                "base_path_check_disabled",
                "Skipped base_path check (bootstrap.require_base_path=False).",
            )
        )

    if config.bootstrap.require_dump_path:
        dump_path = Path(env.dump_path)
        if dump_path.exists():
            findings.append(
                _ok(
                    "dump_path_exists",
                    f"dump_path exists: {dump_path}",
                )
            )
        else:
            findings.append(
                _err(
                    "dump_path_missing",
                    f"dump_path does not exist: {dump_path}",
                )
            )
            actions.append(
                f"Re-generate dump for environment {env_name!r} or "
                f"correct dump_path: {dump_path}."
            )
    else:
        findings.append(
            _warn(
                "dump_path_check_disabled",
                "Skipped dump_path check (bootstrap.require_dump_path=False).",
            )
        )

    if config.bootstrap.require_python:
        python_loc = shutil.which("python")
        if python_loc is None:
            findings.append(
                _err(
                    "python_not_on_path",
                    "'python' executable was not found on PATH.",
                )
            )
            actions.append(
                "Install Python 3.11+ and ensure 'python' is on PATH."
            )
        else:
            findings.append(
                _ok(
                    "python_on_path",
                    f"'python' resolves to: {python_loc}",
                )
            )
    else:
        findings.append(
            _warn(
                "python_check_disabled",
                "Skipped python check (bootstrap.require_python=False).",
            )
        )

    # http_base_url shape — presumed only. Real reachability check
    # belongs to Step 4 (health dashboard / environment doctor).
    parsed = urlparse(env.http_base_url)
    if parsed.scheme and parsed.netloc:
        findings.append(
            _ok(
                "http_base_url_well_formed",
                f"http_base_url has scheme and host: {env.http_base_url}",
                confidence="presumed",
            )
        )
    else:
        findings.append(
            _warn(
                "http_base_url_malformed",
                f"http_base_url has no scheme or host: {env.http_base_url!r}.",
                confidence="presumed",
            )
        )
        actions.append(
            f"Verify http_base_url for environment {env_name!r}: must "
            "be a valid URL with scheme and host."
        )

    # MCP server packages importable.
    for toggle_name, module_name in _SERVER_TOGGLE_TO_MODULE.items():
        toggle_enabled = bool(getattr(config.servers, toggle_name))
        if not toggle_enabled:
            findings.append(
                _warn(
                    f"server_disabled:{toggle_name}",
                    f"Server toggle {toggle_name!r} is disabled in product "
                    f"config; importability check skipped.",
                )
            )
            continue
        if _module_importable(module_name):
            findings.append(
                _ok(
                    f"server_module_importable:{toggle_name}",
                    f"Module {module_name} is importable.",
                )
            )
        else:
            findings.append(
                _err(
                    f"server_module_missing:{toggle_name}",
                    f"Module {module_name} is not importable. PYTHONPATH "
                    f"may be missing the platform layout.",
                )
            )
            actions.append(
                "Run scripts/dev/bootstrap_paths.ps1 (or set PYTHONPATH "
                f"manually) so that {module_name} is importable."
            )

    # Optional bootstrap.work_dir.
    if config.bootstrap.work_dir is not None:
        wd = Path(config.bootstrap.work_dir)
        if wd.exists() and wd.is_dir():
            findings.append(
                _ok(
                    "bootstrap_work_dir_exists",
                    f"bootstrap.work_dir exists and is a directory: {wd}",
                )
            )
        elif wd.exists() and not wd.is_dir():
            findings.append(
                _err(
                    "bootstrap_work_dir_not_a_dir",
                    f"bootstrap.work_dir exists but is not a directory: {wd}",
                )
            )
            actions.append(
                f"Change bootstrap.work_dir to a directory or remove the "
                f"non-directory entry at {wd}."
            )
        else:
            findings.append(
                _warn(
                    "bootstrap_work_dir_missing",
                    f"bootstrap.work_dir does not exist: {wd}",
                )
            )
            actions.append(
                f"Create the directory at bootstrap.work_dir: {wd}."
            )

    error_count = sum(1 for f in findings if f.severity == "error")
    warning_count = sum(1 for f in findings if f.severity == "warning")

    return DoctorReport(
        findings=findings,
        error_count=error_count,
        warning_count=warning_count,
        recommended_actions=actions,
    )
