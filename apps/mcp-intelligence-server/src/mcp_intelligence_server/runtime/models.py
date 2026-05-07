"""Runtime-level data models for mcp-intelligence-server.

Read-only by construction (Phase 4 guardrail). These models describe
a snapshot of an environment plus its health state and resolved dump
root. They carry no mutation semantics and are not ToolResult's —
they are an internal handle for intelligence helpers, similar to
``mcp_read_server.runtime.RuntimeContext``.
"""

from dataclasses import dataclass
from pathlib import Path

from onec_config import EnvironmentConfig
from onec_health import HealthCheckResult


@dataclass
class IntelligenceRuntimeContext:
    """Snapshot of an environment, its health state and dump root.

    ``dump_root`` is always populated (it is the resolved
    :class:`pathlib.Path` of ``environment.dump_path``); whether that
    path actually exists is reflected by ``health_codes`` (for example
    ``dump_missing``). This keeps the context constructible even for
    broken environments so diagnostics tools can still operate on it.
    """

    environment: EnvironmentConfig
    health_results: list[HealthCheckResult]
    health_codes: list[str]
    dump_root: Path
