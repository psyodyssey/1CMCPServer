"""Substring / reference finder over ``*.xml`` and ``*.bsl`` dump files.

Minimal Phase 4 helper that will back future public intelligence
tools such as ``find_references_to_object``,
``find_module_method_usages`` and ``analyze_object_dependencies``.
Returns plain dataclass records, not ``ToolResult`` — public-tool
payload shaping belongs to Step 4+, not here.

Read-only by construction. No caching, no disk writes.
"""

from dataclasses import dataclass
from pathlib import Path

from .dump_scanner import list_files_by_extensions, read_utf8_text

_PREVIEW_MAX_LENGTH = 160
_DEFAULT_EXTENSIONS: tuple[str, ...] = ("xml", "bsl")


@dataclass(frozen=True)
class ReferenceMatch:
    """One substring match inside a dump file.

    ``relative_path`` is POSIX-style (forward slashes) and relative to
    the dump root supplied to :func:`find_references`. ``source``
    mirrors the file extension (``"xml"`` or ``"bsl"``). ``line_number``
    is 1-based. ``preview`` is the full matching line, stripped and
    truncated to a short length so calling code can log it directly.
    """

    relative_path: str
    source: str
    line_number: int
    preview: str


def _truncate_preview(line: str) -> str:
    stripped = line.strip()
    if len(stripped) <= _PREVIEW_MAX_LENGTH:
        return stripped
    return stripped[: _PREVIEW_MAX_LENGTH - 3] + "..."


def find_references(
    dump_root: Path,
    needle: str,
    *,
    extensions: tuple[str, ...] | None = None,
    max_matches: int | None = None,
) -> list[ReferenceMatch]:
    """Find substring occurrences of ``needle`` across dump files.

    Search is case-sensitive substring. ``extensions`` defaults to
    ``("xml", "bsl")``. If ``max_matches`` is set, the scan stops
    early once that many matches are collected — useful for intelligence
    tools that only want to prove existence or gather a small sample.
    Empty ``needle`` is not allowed (fail-closed via ``ValueError``).
    """
    if not needle:
        raise ValueError("find_references requires a non-empty needle.")
    exts = extensions if extensions is not None else _DEFAULT_EXTENSIONS

    matches: list[ReferenceMatch] = []
    for path in list_files_by_extensions(dump_root, exts):
        text = read_utf8_text(path)
        ext = path.suffix.lstrip(".").lower() or "unknown"
        rel = path.relative_to(dump_root).as_posix()
        for line_idx, line in enumerate(text.splitlines(), start=1):
            if needle in line:
                matches.append(
                    ReferenceMatch(
                        relative_path=rel,
                        source=ext,
                        line_number=line_idx,
                        preview=_truncate_preview(line),
                    )
                )
                if max_matches is not None and len(matches) >= max_matches:
                    return matches
    return matches


def count_references(
    dump_root: Path,
    needle: str,
    *,
    extensions: tuple[str, ...] | None = None,
) -> int:
    """Return the number of substring matches for ``needle`` across dump."""
    return len(find_references(dump_root, needle, extensions=extensions))
