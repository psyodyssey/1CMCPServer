"""Internal runtime adapters for mcp-read-server.

Stays below the tool layer: knows how to talk to the live HTTP endpoint
and to the dump directory of an environment, but does not know about
any specific read tool.
"""

from .context import build_runtime_context
from .dump_adapter import (
    find_files_by_pattern,
    read_dump_file,
    read_text_file,
    resolve_dump_path,
)
from .live_adapter import fetch_json, fetch_json_from_environment
from .models import RuntimeContext

__all__ = [
    "RuntimeContext",
    "build_runtime_context",
    "fetch_json",
    "fetch_json_from_environment",
    "resolve_dump_path",
    "read_text_file",
    "find_files_by_pattern",
    "read_dump_file",
]
