"""Audit record formatting and append-only JSONL store."""

import json
from dataclasses import asdict
from pathlib import Path

from .models import AuditRecord

_AUDIT_FILE_NAME = "audit.jsonl"


def format_audit_record(record: AuditRecord) -> str:
    """Serialize an audit record to a canonical single-line JSON string.

    ``details`` is omitted from the JSON when it is ``None`` so that
    audit lines produced before Phase 6 / Step 4 stay byte-identical:
    older lines never carried this key, and freshly-emitted lines
    without structured details should not start carrying ``"details":
    null``. When ``details`` is a dict (even empty), it is preserved.
    """
    payload = asdict(record)
    if payload.get("details") is None:
        payload.pop("details", None)
    return json.dumps(payload, ensure_ascii=False)


def append_record(audit_dir: str, record: AuditRecord) -> str:
    """Append ``record`` as one JSON line to ``<audit_dir>/audit.jsonl``.

    Creates ``audit_dir`` if it does not exist. Returns the string path
    to the audit file. File-system errors propagate as :class:`OSError`.
    """
    directory = Path(audit_dir)
    directory.mkdir(parents=True, exist_ok=True)
    audit_path = directory / _AUDIT_FILE_NAME
    line = format_audit_record(record)
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.write("\n")
    return str(audit_path)


def read_last_record(audit_dir: str) -> AuditRecord | None:
    """Return the most recent :class:`AuditRecord` from the audit file.

    Returns ``None`` if ``<audit_dir>/audit.jsonl`` does not exist or
    contains no non-empty lines. Empty lines are skipped.

    Raises:
        ValueError: when the last non-empty line is not valid JSON or
            does not match the :class:`AuditRecord` shape.
        OSError: when the audit file exists but cannot be read.
    """
    audit_path = Path(audit_dir) / _AUDIT_FILE_NAME
    if not audit_path.exists():
        return None
    with audit_path.open("r", encoding="utf-8") as handle:
        lines = [line.strip() for line in handle if line.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        payload = json.loads(last)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Last audit line in {audit_path} is not valid JSON: {exc}"
        ) from exc
    try:
        return AuditRecord(**payload)
    except TypeError as exc:
        raise ValueError(
            f"Last audit line in {audit_path} does not match AuditRecord shape: {exc}"
        ) from exc
