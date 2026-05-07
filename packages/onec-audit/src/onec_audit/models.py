"""Data models for audit records."""

from dataclasses import dataclass, field


@dataclass
class AuditRecord:
    """A single structured audit entry.

    ``details`` (Phase 6 / Step 4) is an optional small dict carrying
    the structured artefacts that downstream rollback / inspect
    helpers need (e.g. ``relative_path`` of a single mutated file,
    ``dump_snapshot_path`` from the write-flow snapshot stage). It is
    free-shape on purpose — only string keys with JSON-serialisable
    values — so existing audit lines without it stay readable, and
    older readers ignore the new field. Old (pre-Step-4) audit lines
    deserialise as ``details=None`` and downstream code degrades
    honestly to "automatic recovery not supported for this entry".
    """

    operation_id: str
    tool_name: str
    environment: str
    base_id: str
    status: str
    message: str
    details: dict | None = None
