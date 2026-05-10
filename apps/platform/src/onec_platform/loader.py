"""Loader for the product config (Phase 5 / Step 2).

Two entry points:

- :func:`load_product_config` — dict → :class:`ProductConfig`. Pure
  structural validation, no I/O. Mirrors the style of
  :func:`onec_config.load_project_config`.
- :func:`load_product_config_from_json_file` — JSON file → dict →
  :class:`ProductConfig`. Adds the file-read step and JSON-parse
  step on top.

Both functions raise :class:`ValueError` on bad input. The
boundary-level :mod:`onec_platform.bootstrap` helpers wrap these
errors into a :class:`BootstrapResult` so user-facing callers never
see an exception.
"""

import json
import re
from pathlib import Path

from onec_config import load_project_config

from .models import (
    DEFAULT_LOG_MAX_BYTES,
    DEPLOYMENT_TIERS,
    EnterpriseFoundationSettings,
    ProductAuthSettings,
    ProductBootstrapSettings,
    ProductConfig,
    ProductRuntimeSettings,
    ProductServerToggles,
    ProductServiceSpec,
    RESTART_POLICIES,
)

# Track H / Step 4 — env-substitution form for auth.tokens entries.
# Byte-identical to Track D pattern in
# apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py.
_AUTH_ENV_TOKEN_RE = re.compile(r"^\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}$")

_REQUIRED_TOP_LEVEL: tuple[str, ...] = (
    "product_name",
    "profile_name",
    "project",
    "default_environment",
)


def load_product_config(data: dict) -> ProductConfig:
    """Convert a dict into :class:`ProductConfig` with full validation.

    Validation contract (fail-closed via :class:`ValueError`):

    - the root must be a dict;
    - all keys in :data:`_REQUIRED_TOP_LEVEL` must be present;
    - ``product_name`` / ``profile_name`` / ``default_environment``
      must be non-empty strings;
    - ``project`` must be a dict in the shape accepted by
      :func:`onec_config.load_project_config` (delegated);
    - ``default_environment`` must be a key of
      ``project.environments``;
    - ``servers`` (optional) must be a dict if present, with bool
      values ``read`` / ``write`` / ``intelligence``;
    - ``bootstrap`` (optional) must be a dict if present, with
      string ``work_dir`` (or absent) and bool ``require_*`` flags.
    """
    if not isinstance(data, dict):
        raise ValueError("Product config root must be a dict.")

    for key in _REQUIRED_TOP_LEVEL:
        if key not in data:
            raise ValueError(
                f"Product config is missing required key '{key}'."
            )

    product_name = data["product_name"]
    if not isinstance(product_name, str) or not product_name:
        raise ValueError("'product_name' must be a non-empty string.")

    profile_name = data["profile_name"]
    if not isinstance(profile_name, str) or not profile_name:
        raise ValueError("'profile_name' must be a non-empty string.")

    default_environment = data["default_environment"]
    if not isinstance(default_environment, str) or not default_environment:
        raise ValueError("'default_environment' must be a non-empty string.")

    project_data = data["project"]
    if not isinstance(project_data, dict):
        raise ValueError(
            "'project' must be a dict in the shape accepted by "
            "onec_config.load_project_config."
        )
    project = load_project_config(project_data)

    if default_environment not in project.environments:
        raise ValueError(
            f"'default_environment' = {default_environment!r} is not "
            f"present in project.environments. Known environments: "
            f"{sorted(project.environments)}."
        )

    servers_raw = data.get("servers")
    if servers_raw is None:
        servers = ProductServerToggles()
    elif not isinstance(servers_raw, dict):
        raise ValueError("'servers' must be a dict if present.")
    else:
        servers = ProductServerToggles(
            read=bool(servers_raw.get("read", True)),
            write=bool(servers_raw.get("write", True)),
            intelligence=bool(servers_raw.get("intelligence", True)),
        )

    bootstrap_raw = data.get("bootstrap")
    if bootstrap_raw is None:
        bootstrap = ProductBootstrapSettings()
    elif not isinstance(bootstrap_raw, dict):
        raise ValueError("'bootstrap' must be a dict if present.")
    else:
        work_dir = bootstrap_raw.get("work_dir")
        if work_dir is not None and not isinstance(work_dir, str):
            raise ValueError(
                "'bootstrap.work_dir' must be a string if present."
            )
        bootstrap = ProductBootstrapSettings(
            work_dir=work_dir,
            require_dump_path=bool(
                bootstrap_raw.get("require_dump_path", True)
            ),
            require_base_path=bool(
                bootstrap_raw.get("require_base_path", True)
            ),
            require_python=bool(
                bootstrap_raw.get("require_python", True)
            ),
        )

    runtime = _parse_runtime(data.get("runtime"))
    enterprise = _parse_enterprise(data.get("enterprise"))
    auth = _parse_auth(data.get("auth"))

    return ProductConfig(
        product_name=product_name,
        profile_name=profile_name,
        project=project,
        default_environment=default_environment,
        servers=servers,
        bootstrap=bootstrap,
        runtime=runtime,
        enterprise=enterprise,
        auth=auth,
    )


def _parse_runtime(runtime_raw: object) -> ProductRuntimeSettings:
    """Parse the optional ``runtime`` section of a product config.

    Validation contract (fail-closed via :class:`ValueError`):

    - missing section → empty :class:`ProductRuntimeSettings` (Step 2
      backward compatibility);
    - present section must be a dict;
    - ``services`` (optional) must be a dict if present, with string
      keys and dict values;
    - each per-service entry is parsed by :func:`_parse_service_spec`.
    """
    if runtime_raw is None:
        return ProductRuntimeSettings()
    if not isinstance(runtime_raw, dict):
        raise ValueError("'runtime' must be a dict if present.")

    services_raw = runtime_raw.get("services")
    if services_raw is None:
        return ProductRuntimeSettings()
    if not isinstance(services_raw, dict):
        raise ValueError(
            "'runtime.services' must be a dict if present."
        )

    services: dict[str, ProductServiceSpec] = {}
    for name, spec_raw in services_raw.items():
        if not isinstance(name, str) or not name:
            raise ValueError(
                "Each key under 'runtime.services' must be a non-empty string."
            )
        if not isinstance(spec_raw, dict):
            raise ValueError(
                f"'runtime.services.{name}' must be a dict."
            )
        services[name] = _parse_service_spec(name, spec_raw)
    return ProductRuntimeSettings(services=services)


def _parse_service_spec(name: str, spec_raw: dict) -> ProductServiceSpec:
    """Parse one service spec under ``runtime.services``.

    Step 3 fields:

    - ``enabled`` (optional, default ``True``) — must be bool-ish.
    - ``command`` (optional, default ``None``) — must be a list of
      strings if present, with at least one entry. Shell strings are
      not supported on purpose; argument lists keep quoting safe.
    - ``working_dir`` (optional, default ``None``) — must be a string
      if present.
    - ``env_overrides`` (optional, default ``{}``) — must be a dict
      of string→string if present.

    Step 6 fields (all optional, all backward-compatible — Step 3
    configs continue to load unchanged):

    - ``restart_policy`` (optional, default ``"never"``) — must be
      one of :data:`RESTART_POLICIES` if present. Strict whitelist.
    - ``logs_enabled`` (optional, default ``True``) — must be a
      ``bool`` (not bool-ish; a malformed shape like a string
      ``"true"`` is rejected fail-closed).
    - ``log_max_bytes`` (optional, default
      :data:`DEFAULT_LOG_MAX_BYTES`) — must be a positive int.
      Booleans are explicitly rejected here even though
      ``isinstance(True, int)`` is True in Python — operators
      passing ``log_max_bytes: true`` is almost certainly a typo,
      not a 1-byte log threshold.
    """
    enabled = bool(spec_raw.get("enabled", True))

    command_raw = spec_raw.get("command")
    if command_raw is None:
        command: list[str] | None = None
    elif not isinstance(command_raw, list) or not command_raw:
        raise ValueError(
            f"'runtime.services.{name}.command' must be a non-empty list "
            f"of strings if present."
        )
    else:
        for item in command_raw:
            if not isinstance(item, str):
                raise ValueError(
                    f"'runtime.services.{name}.command' must contain only "
                    f"strings; got {type(item).__name__}."
                )
        command = list(command_raw)

    working_dir = spec_raw.get("working_dir")
    if working_dir is not None and not isinstance(working_dir, str):
        raise ValueError(
            f"'runtime.services.{name}.working_dir' must be a string "
            f"if present."
        )

    env_raw = spec_raw.get("env_overrides")
    if env_raw is None:
        env_overrides: dict[str, str] = {}
    elif not isinstance(env_raw, dict):
        raise ValueError(
            f"'runtime.services.{name}.env_overrides' must be a dict "
            f"of string→string if present."
        )
    else:
        env_overrides = {}
        for key, value in env_raw.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError(
                    f"'runtime.services.{name}.env_overrides' entries "
                    f"must be string→string; got "
                    f"{type(key).__name__}→{type(value).__name__}."
                )
            env_overrides[key] = value

    restart_policy_raw = spec_raw.get("restart_policy")
    if restart_policy_raw is None:
        restart_policy = "never"
    elif not isinstance(restart_policy_raw, str):
        raise ValueError(
            f"'runtime.services.{name}.restart_policy' must be a string "
            f"if present (one of {sorted(RESTART_POLICIES)})."
        )
    elif restart_policy_raw not in RESTART_POLICIES:
        raise ValueError(
            f"'runtime.services.{name}.restart_policy' must be one of "
            f"{sorted(RESTART_POLICIES)}; got {restart_policy_raw!r}."
        )
    else:
        restart_policy = restart_policy_raw

    logs_enabled_raw = spec_raw.get("logs_enabled")
    if logs_enabled_raw is None:
        logs_enabled = True
    elif not isinstance(logs_enabled_raw, bool):
        raise ValueError(
            f"'runtime.services.{name}.logs_enabled' must be a bool if "
            f"present; got {type(logs_enabled_raw).__name__}."
        )
    else:
        logs_enabled = logs_enabled_raw

    log_max_bytes_raw = spec_raw.get("log_max_bytes")
    if log_max_bytes_raw is None:
        log_max_bytes = DEFAULT_LOG_MAX_BYTES
    elif isinstance(log_max_bytes_raw, bool) or not isinstance(
        log_max_bytes_raw, int
    ):
        # bool subclasses int in Python — reject explicitly so that
        # ``log_max_bytes: true`` does not silently mean "1 byte".
        raise ValueError(
            f"'runtime.services.{name}.log_max_bytes' must be a positive "
            f"int if present; got {type(log_max_bytes_raw).__name__}."
        )
    elif log_max_bytes_raw <= 0:
        raise ValueError(
            f"'runtime.services.{name}.log_max_bytes' must be > 0; got "
            f"{log_max_bytes_raw}."
        )
    else:
        log_max_bytes = log_max_bytes_raw

    return ProductServiceSpec(
        name=name,
        enabled=enabled,
        command=command,
        working_dir=working_dir,
        env_overrides=env_overrides,
        restart_policy=restart_policy,
        logs_enabled=logs_enabled,
        log_max_bytes=log_max_bytes,
    )


def _parse_enterprise(
    enterprise_raw: object,
) -> EnterpriseFoundationSettings:
    """Parse the optional ``enterprise`` section (Phase 6 / Step 8).

    Validation contract (fail-closed via :class:`ValueError`):

    - missing section → empty :class:`EnterpriseFoundationSettings`
      (Step 1–7 backward compatibility);
    - present section must be a dict;
    - ``deployment_tier`` (optional, default ``None``) — string
      whitelisted by :data:`DEPLOYMENT_TIERS` if present;
    - ``instance_id`` (optional) — non-empty string if present;
    - ``config_owner`` (optional) — non-empty string if present;
    - ``change_control_required`` (optional, default ``False``) —
      strict ``bool`` (no bool-ish coercion);
    - ``require_operator_identity`` (optional, default ``False``) —
      strict ``bool``;
    - ``runbook_reference`` (optional) — non-empty string if present.

    No additional keys are accepted; any unknown key is rejected
    fail-closed so a typo (``deplyoment_tier``) never silently
    becomes the default value.
    """
    if enterprise_raw is None:
        return EnterpriseFoundationSettings()
    if not isinstance(enterprise_raw, dict):
        raise ValueError("'enterprise' must be a dict if present.")

    allowed_keys = {
        "deployment_tier",
        "instance_id",
        "config_owner",
        "change_control_required",
        "require_operator_identity",
        "runbook_reference",
    }
    unknown = set(enterprise_raw) - allowed_keys
    if unknown:
        raise ValueError(
            f"'enterprise' contains unknown keys: {sorted(unknown)}. "
            f"Allowed keys: {sorted(allowed_keys)}."
        )

    tier_raw = enterprise_raw.get("deployment_tier")
    if tier_raw is None:
        deployment_tier: str | None = None
    elif not isinstance(tier_raw, str):
        raise ValueError(
            "'enterprise.deployment_tier' must be a string if present "
            f"(one of {sorted(DEPLOYMENT_TIERS)})."
        )
    elif tier_raw not in DEPLOYMENT_TIERS:
        raise ValueError(
            f"'enterprise.deployment_tier' must be one of "
            f"{sorted(DEPLOYMENT_TIERS)}; got {tier_raw!r}."
        )
    else:
        deployment_tier = tier_raw

    def _opt_non_empty_str(name: str, value: object) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"'enterprise.{name}' must be a non-empty string if present."
            )
        return value

    instance_id = _opt_non_empty_str(
        "instance_id", enterprise_raw.get("instance_id")
    )
    config_owner = _opt_non_empty_str(
        "config_owner", enterprise_raw.get("config_owner")
    )
    runbook_reference = _opt_non_empty_str(
        "runbook_reference", enterprise_raw.get("runbook_reference")
    )

    def _strict_bool(name: str, value: object, *, default: bool) -> bool:
        if value is None:
            return default
        if not isinstance(value, bool):
            raise ValueError(
                f"'enterprise.{name}' must be a bool if present; got "
                f"{type(value).__name__}."
            )
        return value

    change_control_required = _strict_bool(
        "change_control_required",
        enterprise_raw.get("change_control_required"),
        default=False,
    )
    require_operator_identity = _strict_bool(
        "require_operator_identity",
        enterprise_raw.get("require_operator_identity"),
        default=False,
    )

    return EnterpriseFoundationSettings(
        deployment_tier=deployment_tier,
        instance_id=instance_id,
        config_owner=config_owner,
        change_control_required=change_control_required,
        require_operator_identity=require_operator_identity,
        runbook_reference=runbook_reference,
    )


def _parse_auth(auth_raw: object) -> ProductAuthSettings:
    """Parse the optional ``auth`` section (Track H / Step 4).

    Validation contract (fail-closed via :class:`ValueError`):

    - missing section → empty :class:`ProductAuthSettings` (Phase 1–6
      and Track A–G backward compatibility);
    - present section must be a dict with at most one key, ``tokens``;
    - ``tokens`` (optional, default ``[]``) must be a list of strings
      if present;
    - each entry MUST match the env-substitution form
      ``${ENV:NAME}`` per :data:`_AUTH_ENV_TOKEN_RE`. Literal
      cleartext tokens are rejected fail-closed; empty strings and
      partial / mixed forms (``${ENV:`` without closing brace, or
      bare ``${`` prefix) are rejected fail-closed.

    See ``docs/architecture/track-h-network-transport-and-auth-contract.md``
    §9 for the full normative contract.
    """
    if auth_raw is None:
        return ProductAuthSettings()
    if not isinstance(auth_raw, dict):
        raise ValueError("'auth' must be a dict if present.")

    allowed_keys = {"tokens"}
    unknown = set(auth_raw) - allowed_keys
    if unknown:
        raise ValueError(
            f"'auth' contains unknown keys: {sorted(unknown)}. "
            f"Allowed keys: {sorted(allowed_keys)}."
        )

    tokens_raw = auth_raw.get("tokens")
    if tokens_raw is None:
        return ProductAuthSettings()
    if not isinstance(tokens_raw, list):
        raise ValueError(
            "'auth.tokens' must be a list of strings if present."
        )

    tokens: list[str] = []
    for index, entry in enumerate(tokens_raw):
        if not isinstance(entry, str):
            raise ValueError(
                f"'auth.tokens[{index}]' must be a string; got "
                f"{type(entry).__name__}."
            )
        if not _AUTH_ENV_TOKEN_RE.match(entry):
            # Do not echo the offending value -- it could be a
            # literal cleartext token. Operator gets the index and
            # the required form only.
            raise ValueError(
                f"'auth.tokens[{index}]' must match the env-"
                f"substitution form '${{ENV:NAME}}'. Literal "
                f"cleartext tokens are not accepted."
            )
        tokens.append(entry)
    return ProductAuthSettings(tokens=tokens)


def load_product_config_from_json_file(path: str | Path) -> ProductConfig:
    """Read a JSON file from disk and parse it as a :class:`ProductConfig`.

    All file-system / JSON parsing errors are converted into
    :class:`ValueError` so callers have a single error type to handle.
    Structural errors from :func:`load_product_config` propagate
    unchanged.
    """
    p = Path(path)
    if not p.exists():
        raise ValueError(f"Product config file not found: {p}")
    if not p.is_file():
        raise ValueError(f"Product config path is not a regular file: {p}")
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(
            f"Failed to read product config file {p}: {exc}"
        ) from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Product config file is not valid JSON ({p}): {exc}"
        ) from exc
    return load_product_config(data)
