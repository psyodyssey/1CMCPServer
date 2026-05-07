"""Low-level dump filesystem adapter for the mcp-read-server runtime.

This module stays below the tool layer: it knows how to resolve a dump
root, read UTF-8 text files and list files by pattern, but does not
interpret them or know about specific read tools.
"""

from pathlib import Path

from mcp_common import PlatformError
from onec_config import EnvironmentConfig


def resolve_dump_path(environment: EnvironmentConfig) -> Path:
    """Return the environment's dump root as a :class:`pathlib.Path`."""
    return Path(environment.dump_path)


def read_text_file(path: Path) -> str:
    """Read a text file as UTF-8, replacing decoding errors."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError as exc:
        raise PlatformError(f"Dump file not found: {path}.") from exc
    except OSError as exc:
        raise PlatformError(f"Failed to read dump file {path}: {exc}.") from exc


def find_files_by_pattern(root: Path, pattern: str) -> list[Path]:
    """Return sorted ``rglob(pattern)`` matches under ``root``."""
    if not root.exists():
        raise PlatformError(f"Dump root does not exist: {root}.")
    try:
        return sorted(root.rglob(pattern))
    except OSError as exc:
        raise PlatformError(
            f"Failed to scan {root} for {pattern}: {exc}."
        ) from exc


def read_dump_file(environment: EnvironmentConfig, relative_path: str) -> str:
    """Read a dump file by ``relative_path`` inside the environment's dump root."""
    dump_root = resolve_dump_path(environment)
    target = dump_root / relative_path
    return read_text_file(target)
