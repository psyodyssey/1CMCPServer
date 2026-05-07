"""Internal runtime for mcp-write-server.

Gathers the per-call write context (environment, health, policy decision,
audit directory), provides a fail-fast preconditions guard, and the
single ``preflight → snapshot → operation → verify → audit`` pipeline
used by future write-tools of group B.
"""

from .context import build_runtime_context
from .flow import WriteFlowArtifacts, run_write_flow
from .guards import require_write_preconditions
from .models import WriteRuntimeContext

__all__ = [
    "WriteRuntimeContext",
    "build_runtime_context",
    "require_write_preconditions",
    "WriteFlowArtifacts",
    "run_write_flow",
]
