"""Loader that converts a plain dict into a ProjectConfig dataclass.

The loader performs structural validation only. It does not read files,
environment variables, or any external sources — those will be layered
on top of this function later.
"""

from .models import EnvironmentConfig, ProjectConfig

_REQUIRED_ENV_FIELDS = (
    "name",
    "base_id",
    "base_path",
    "publication_name",
    "http_base_url",
    "dump_path",
    "timeout_seconds",
)


def load_project_config(data: dict) -> ProjectConfig:
    """Convert a dict-shaped config into a :class:`ProjectConfig` dataclass.

    Raises:
        ValueError: when ``environments`` key is missing, when it is empty,
            or when any environment is missing a required field.
    """
    if "environments" not in data:
        raise ValueError("Config is missing required key 'environments'.")

    raw_environments = data["environments"]
    if not raw_environments:
        raise ValueError("Config section 'environments' must not be empty.")

    environments: dict[str, EnvironmentConfig] = {}
    for env_key, env_data in raw_environments.items():
        for field in _REQUIRED_ENV_FIELDS:
            if field not in env_data:
                raise ValueError(
                    f"Environment '{env_key}' is missing required field '{field}'."
                )

        binary_path = env_data.get("onec_binary_path")
        if binary_path is not None and not isinstance(binary_path, str):
            raise ValueError(
                f"Environment '{env_key}': 'onec_binary_path' must be a "
                "string if present."
            )

        probe_args = env_data.get("onec_binary_probe_args")
        if probe_args is not None:
            if not isinstance(probe_args, list):
                raise ValueError(
                    f"Environment '{env_key}': 'onec_binary_probe_args' must "
                    "be a list of strings if present."
                )
            for entry in probe_args:
                if not isinstance(entry, str):
                    raise ValueError(
                        f"Environment '{env_key}': 'onec_binary_probe_args' "
                        "must contain only strings; got "
                        f"{type(entry).__name__}."
                    )
            probe_args = list(probe_args)

        dumpcfg_template = env_data.get("onec_dumpcfg_command_template")
        if dumpcfg_template is not None:
            if not isinstance(dumpcfg_template, list):
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_dumpcfg_command_template' must be a list of "
                    "strings if present."
                )
            if not dumpcfg_template:
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_dumpcfg_command_template' must not be empty if "
                    "present."
                )
            for entry in dumpcfg_template:
                if not isinstance(entry, str):
                    raise ValueError(
                        f"Environment '{env_key}': "
                        "'onec_dumpcfg_command_template' must contain only "
                        f"strings; got {type(entry).__name__}."
                    )
            dumpcfg_template = list(dumpcfg_template)

        applycfg_template = env_data.get("onec_applycfg_command_template")
        if applycfg_template is not None:
            if not isinstance(applycfg_template, list):
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_applycfg_command_template' must be a list of "
                    "strings if present."
                )
            if not applycfg_template:
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_applycfg_command_template' must not be empty if "
                    "present."
                )
            for entry in applycfg_template:
                if not isinstance(entry, str):
                    raise ValueError(
                        f"Environment '{env_key}': "
                        "'onec_applycfg_command_template' must contain only "
                        f"strings; got {type(entry).__name__}."
                    )
            applycfg_template = list(applycfg_template)

        updatedb_template = env_data.get("onec_updatedb_command_template")
        if updatedb_template is not None:
            if not isinstance(updatedb_template, list):
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_updatedb_command_template' must be a list of "
                    "strings if present."
                )
            if not updatedb_template:
                raise ValueError(
                    f"Environment '{env_key}': "
                    "'onec_updatedb_command_template' must not be empty if "
                    "present."
                )
            for entry in updatedb_template:
                if not isinstance(entry, str):
                    raise ValueError(
                        f"Environment '{env_key}': "
                        "'onec_updatedb_command_template' must contain only "
                        f"strings; got {type(entry).__name__}."
                    )
            updatedb_template = list(updatedb_template)

        environments[env_key] = EnvironmentConfig(
            name=env_data["name"],
            base_id=env_data["base_id"],
            base_path=env_data["base_path"],
            publication_name=env_data["publication_name"],
            http_base_url=env_data["http_base_url"],
            dump_path=env_data["dump_path"],
            timeout_seconds=env_data["timeout_seconds"],
            allow_write=env_data.get("allow_write", False),
            onec_binary_path=binary_path,
            onec_binary_probe_args=probe_args,
            onec_dumpcfg_command_template=dumpcfg_template,
            onec_applycfg_command_template=applycfg_template,
            onec_updatedb_command_template=updatedb_template,
        )

    return ProjectConfig(environments=environments)
