"""Shared exception hierarchy for the platform."""


class PlatformError(Exception):
    """Base exception for all 1C Agent Platform errors."""


class PolicyDeniedError(PlatformError):
    """Raised when an operation is denied by the policy engine."""


class ProcessExecutionError(PlatformError):
    """Raised when running an external process fails."""


class HealthCheckError(PlatformError):
    """Raised when a health check fails."""
