"""Thin dump-filesystem helpers for intelligence-side analysis.

Reuses low-level primitives from ``mcp_read_server.runtime`` (allowed
cross-app direction: ``intelligence → read``). The wrappers exist so
intelligence helpers have a small, intelligence-flavoured API
(``list_xml_files`` / ``list_bsl_files`` / ``read_utf8_text``) instead
of calling the generic read-server primitives directly everywhere.

Read-only by construction. No file is written, nothing is cached.
"""

from pathlib import Path

from mcp_read_server.runtime import (
    find_files_by_pattern,
    read_text_file,
)


def list_xml_files(dump_root: Path) -> list[Path]:
    """Return sorted list of ``*.xml`` files recursively under ``dump_root``."""
    return find_files_by_pattern(dump_root, "*.xml")


def list_bsl_files(dump_root: Path) -> list[Path]:
    """Return sorted list of ``*.bsl`` files recursively under ``dump_root``."""
    return find_files_by_pattern(dump_root, "*.bsl")


def read_utf8_text(path: Path) -> str:
    """Read a dump file as UTF-8 text, replacing decoding errors."""
    return read_text_file(path)


def list_files_by_extensions(
    dump_root: Path, extensions: tuple[str, ...]
) -> list[Path]:
    """Return sorted list of files matching any of the given extensions.

    ``extensions`` contains bare names without a leading dot, e.g.
    ``("xml", "bsl")``. Order of the resulting list is stable: sorted
    across all extensions together.
    """
    collected: list[Path] = []
    for ext in extensions:
        collected.extend(find_files_by_pattern(dump_root, f"*.{ext}"))
    return sorted(collected)
