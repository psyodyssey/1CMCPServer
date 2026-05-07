"""onec_config — project configuration loader for 1C Agent Platform."""

from .loader import load_project_config
from .models import EnvironmentConfig, ProjectConfig

__all__ = [
    "EnvironmentConfig",
    "ProjectConfig",
    "load_project_config",
]
