"""File-based read-only adapter for environments without an HTTP gateway.

The MVP install path (``first_run.ps1``) produces an environment with
``http_base_url=""`` — a pure file-based 1C infobase observed through
the 1cv8 binary. The HTTP-backed read tools cannot work in that mode
because there is no published HTTP gateway to fetch JSON from.

This module fills the gap with three small pieces:

- :func:`ensure_dump_populated` — lazy "dump on first read" bootstrap.
  When the configured ``dump_path`` is empty and the environment has a
  valid ``onec_binary_path``, invokes ``1cv8 DESIGNER /DumpConfigToFiles``
  through :mod:`onec_process_runner`. No new dependency: the runner is
  already shipped in the platform wheel.
- :func:`read_configuration_info_from_dump` /
  :func:`read_metadata_tree_from_dump` /
  :func:`read_metadata_object_from_dump` — minimal dump-tree readers
  that mirror the JSON shape the HTTP tools historically returned, so
  the boundary at ``tools.py`` is a one-line ``if http_base_url == ""``
  branch and not a parallel implementation.

What this module is NOT:

- it does **not** invoke a write operation against the infobase;
  ``DumpConfigToFiles`` reads from ``.1CD`` and writes only to
  ``dump_path``;
- it does **not** introduce HTTP publication / Apache / webinst;
- it does **not** require operator-supplied argv templates — the
  argv used here is the documented read-only invocation for file-based
  infobases. Operators who need an exotic argv keep the write-side
  ``onec_dumpcfg_command_template`` knob untouched.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from mcp_common import PlatformError, ProcessExecutionError
from onec_config import EnvironmentConfig
from onec_process_runner import ProcessRunRequest, run_process

# Generous default: a real ``DumpConfigToFiles`` on a small demo base
# completes in ~30 s; on a large enterprise configuration it can take
# several minutes. The environment's own ``timeout_seconds`` is the
# cap and falls back to ten minutes if the operator did not configure
# anything sensible.
_DEFAULT_DUMP_TIMEOUT_SECONDS: int = 600

# Marker files we treat as "dump is populated enough that read tools
# can return useful data". The top-level ``Configuration.xml`` is the
# canonical root descriptor every successful ``DumpConfigToFiles``
# produces; presence of any ``*.xml`` in the dump root is the loose
# fallback for partially-populated trees written by older 1C versions.
_DUMP_ROOT_DESCRIPTOR: str = "Configuration.xml"

# DESIGNER credential env vars. Matches the write-side ``${ENV:NAME}``
# convention so operators that already configure write-side credentials
# do not need a second mechanism for read-side dumps. Omitted when the
# infobase has no users (default for a fresh file-based base).
_ONEC_USER_ENV_VAR: str = "ONEC_USER"
_ONEC_PASSWORD_ENV_VAR: str = "ONEC_PASSWORD"


def _is_file_based_infobase(base_path: str) -> bool:
    """Return True iff ``base_path`` looks like a file-based 1C infobase."""
    folder = Path(base_path)
    if not folder.is_dir():
        return False
    try:
        return any(folder.glob("*.1[cC][dD]"))
    except OSError:
        return False


def _dump_is_populated(dump_path: str) -> bool:
    """Return True iff the dump tree already contains a real config dump."""
    root = Path(dump_path)
    if not root.is_dir():
        return False
    if (root / _DUMP_ROOT_DESCRIPTOR).is_file():
        return True
    try:
        return next(root.rglob("*.xml"), None) is not None
    except OSError:
        return False


def _build_dumpcfg_command(
    onec_binary_path: str,
    base_path: str,
    dump_path: str,
    out_log_path: str,
) -> list[str]:
    """Return the argv for a read-only ``DumpConfigToFiles`` invocation.

    Mirrors the audited, working argv recorded in
    ``examples/demo-dumps/_snapshots/.../dump-meta.json``: separate
    ``/F <base_path>`` tokens, optional ``/N``/``/P`` for infobases
    with users (read from ``ONEC_USER`` / ``ONEC_PASSWORD``), an
    explicit ``/Out <log>`` because DESIGNER refuses to start headless
    without one, and ``/DisableStartupMessages`` to suppress the
    "Configuration is being modified" splash.
    """
    command: list[str] = [
        onec_binary_path,
        "DESIGNER",
        "/F",
        base_path,
    ]
    username = os.environ.get(_ONEC_USER_ENV_VAR)
    if username:
        command += ["/N", username]
        password = os.environ.get(_ONEC_PASSWORD_ENV_VAR, "")
        command += ["/P", password]
    command += [
        "/DumpConfigToFiles",
        dump_path,
        "/Out",
        out_log_path,
        "/DisableStartupMessages",
    ]
    return command


def _read_designer_log_tail(out_log_path: Path) -> str:
    """Return the last non-empty line of the DESIGNER /Out log file.

    DESIGNER writes the log in the platform's native encoding (UTF-16
    with BOM on modern Windows builds, CP1251 on older ones). We try
    UTF-16 first, fall back to CP1251 with ``errors='replace'``. Empty
    or unreadable logs return an empty string; callers compose their
    own error message.
    """
    if not out_log_path.is_file():
        return ""
    try:
        raw = out_log_path.read_bytes()
    except OSError:
        return ""
    if not raw:
        return ""
    text: str
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16", errors="replace")
    else:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp1251", errors="replace")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def ensure_dump_populated(environment: EnvironmentConfig) -> Path:
    """Make sure ``environment.dump_path`` has a usable config dump.

    Returns the dump root as a :class:`pathlib.Path` on success. Raises
    :class:`PlatformError` with an operator-readable message on any
    failure (missing binary, locked infobase, non-zero exit, timeout).
    """
    dump_root = Path(environment.dump_path)
    if _dump_is_populated(environment.dump_path):
        return dump_root

    binary = environment.onec_binary_path
    if not binary:
        raise PlatformError(
            "Dump is empty and no 1cv8 binary is configured for this "
            "environment. Set 'onec_binary_path' in the product config "
            "(or run first_run.ps1 again) and retry."
        )
    if not Path(binary).is_file():
        raise PlatformError(
            f"Configured 1cv8 binary does not exist: {binary}."
        )
    if not _is_file_based_infobase(environment.base_path):
        raise PlatformError(
            "Configured base_path is not a file-based 1C infobase "
            f"(no .1CD file at the top level): {environment.base_path}."
        )

    dump_root.mkdir(parents=True, exist_ok=True)
    timeout_seconds = (
        environment.timeout_seconds
        if environment.timeout_seconds and environment.timeout_seconds > 0
        else _DEFAULT_DUMP_TIMEOUT_SECONDS
    )
    log_handle, log_name = tempfile.mkstemp(
        prefix="dumpcfg-1c-out-", suffix=".log"
    )
    os.close(log_handle)
    out_log_path = Path(log_name)
    command = _build_dumpcfg_command(
        binary,
        environment.base_path,
        environment.dump_path,
        str(out_log_path),
    )
    try:
        try:
            result = run_process(
                ProcessRunRequest(
                    command=command, timeout_seconds=timeout_seconds
                )
            )
        except ProcessExecutionError as exc:
            raise PlatformError(
                f"Failed to start 1cv8 DESIGNER for dump bootstrap: {exc}."
            ) from exc
        if not result.completed:
            raise PlatformError(
                "1cv8 DESIGNER did not finish within "
                f"{timeout_seconds}s while dumping configuration to "
                f"{environment.dump_path}. Close any open DESIGNER "
                "session for this infobase and retry."
            )
        if result.exit_code != 0:
            log_tail = _read_designer_log_tail(out_log_path)
            stderr_tail = (
                (result.stderr or "").strip().splitlines()[-1:] or [""]
            )[0]
            tail = log_tail or stderr_tail
            hint = ""
            if not os.environ.get(_ONEC_USER_ENV_VAR):
                hint = (
                    " If the infobase has users, set the "
                    f"{_ONEC_USER_ENV_VAR}/{_ONEC_PASSWORD_ENV_VAR} "
                    "environment variables and retry."
                )
            raise PlatformError(
                f"1cv8 DESIGNER returned exit code {result.exit_code} "
                f"while dumping configuration. Tail: {tail!r}.{hint}"
            )
        if not _dump_is_populated(environment.dump_path):
            log_tail = _read_designer_log_tail(out_log_path)
            raise PlatformError(
                "1cv8 DESIGNER exited cleanly but produced no XML "
                f"output at {environment.dump_path}. Log tail: "
                f"{log_tail!r}."
            )
    finally:
        try:
            out_log_path.unlink()
        except OSError:
            pass
    return dump_root


def read_configuration_info_from_dump(environment: EnvironmentConfig) -> dict:
    """Return a small dict describing the dumped configuration root.

    Mirrors the shape returned by the HTTP ``configuration`` endpoint
    just enough for an MCP client to confirm the read path is alive.
    Full XML parsing is intentionally avoided — operators who need
    structured fields can call :func:`read_metadata_object_from_dump`.
    """
    dump_root = ensure_dump_populated(environment)
    descriptor = dump_root / _DUMP_ROOT_DESCRIPTOR
    file_count = sum(1 for _ in dump_root.rglob("*.xml"))
    if descriptor.is_file():
        try:
            text = descriptor.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise PlatformError(
                f"Failed to read configuration descriptor {descriptor}: {exc}."
            ) from exc
        return {
            "source": "dump",
            "dump_path": str(dump_root),
            "descriptor_path": str(descriptor),
            "descriptor_xml": text,
            "xml_file_count": file_count,
        }
    return {
        "source": "dump",
        "dump_path": str(dump_root),
        "descriptor_path": None,
        "descriptor_xml": None,
        "xml_file_count": file_count,
    }


def read_metadata_tree_from_dump(
    environment: EnvironmentConfig, filter_value: str | None = None
) -> dict:
    """Walk the dump tree and group object descriptors by kind.

    Each immediate sub-directory of the dump root is treated as one
    metadata kind (``Catalogs``, ``Documents``, ``CommonModules``…).
    Children of the kind directory ending in ``.xml`` are reported as
    object names. ``filter_value``, when given, is matched
    case-insensitive as a substring against either the kind or the
    object name.
    """
    dump_root = ensure_dump_populated(environment)
    needle = filter_value.lower() if filter_value else None
    object_types: dict[str, list[str]] = {}
    try:
        kind_dirs = sorted(p for p in dump_root.iterdir() if p.is_dir())
    except OSError as exc:
        raise PlatformError(
            f"Failed to enumerate dump root {dump_root}: {exc}."
        ) from exc
    for kind_dir in kind_dirs:
        kind = kind_dir.name
        names: list[str] = []
        try:
            for entry in sorted(kind_dir.iterdir()):
                if entry.is_file() and entry.suffix.lower() == ".xml":
                    names.append(entry.stem)
                elif entry.is_dir():
                    descriptor = entry.with_suffix(".xml")
                    if descriptor.is_file():
                        names.append(entry.name)
        except OSError:
            continue
        if needle is not None:
            kind_match = needle in kind.lower()
            names = [n for n in names if kind_match or needle in n.lower()]
            if not names and not kind_match:
                continue
        if names:
            object_types[kind] = names
    return {
        "source": "dump",
        "dump_path": str(dump_root),
        "filter": filter_value,
        "object_types": object_types,
    }


def _split_object_name(object_name: str) -> tuple[str, str]:
    if "." not in object_name:
        raise PlatformError(
            "Metadata object name must be 'Kind.Name' (e.g. 'Catalog.Items'). "
            f"Got {object_name!r}."
        )
    kind, _, simple = object_name.partition(".")
    if not kind or not simple:
        raise PlatformError(
            "Metadata object name must be 'Kind.Name' with non-empty parts. "
            f"Got {object_name!r}."
        )
    return kind, simple


def _candidate_descriptor_paths(
    dump_root: Path, kind: str, simple_name: str
) -> list[Path]:
    """Return possible dump-tree locations of an object descriptor.

    DumpConfigToFiles uses the plural form of the kind as the
    directory name (``Catalog`` -> ``Catalogs``). We try the plural
    form first and fall back to the literal kind for kinds whose
    plural is irregular.
    """
    plural = kind + "s"
    return [
        dump_root / plural / f"{simple_name}.xml",
        dump_root / kind / f"{simple_name}.xml",
    ]


def read_metadata_object_from_dump(
    environment: EnvironmentConfig, object_name: str
) -> dict:
    """Read one metadata object's XML descriptor from the dump tree."""
    dump_root = ensure_dump_populated(environment)
    kind, simple_name = _split_object_name(object_name)
    candidates = _candidate_descriptor_paths(dump_root, kind, simple_name)
    descriptor: Path | None = next(
        (path for path in candidates if path.is_file()), None
    )
    if descriptor is None:
        try:
            descriptor = next(
                (
                    p
                    for p in dump_root.rglob(f"{simple_name}.xml")
                    if p.parent.name.lower().rstrip("s") == kind.lower()
                ),
                None,
            )
        except OSError:
            descriptor = None
    if descriptor is None:
        raise PlatformError(
            f"Metadata object {object_name!r} not found in dump "
            f"{dump_root}. Looked at: "
            f"{[str(c) for c in candidates]}."
        )
    try:
        text = descriptor.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise PlatformError(
            f"Failed to read metadata descriptor {descriptor}: {exc}."
        ) from exc
    return {
        "source": "dump",
        "dump_path": str(dump_root),
        "object_name": object_name,
        "descriptor_path": str(descriptor),
        "descriptor_xml": text,
    }
