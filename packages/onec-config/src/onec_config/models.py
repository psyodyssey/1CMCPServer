"""Data models for project configuration."""

from dataclasses import dataclass, field


@dataclass
class EnvironmentConfig:
    """Configuration of a single target environment (infobase).

    Phase 5 / Step 7 added two optional fields for the real-stand /
    1cv8 binary integration track. Both default to ``None`` so any
    previously-loaded config keeps working unchanged:

    - ``onec_binary_path`` — absolute filesystem path of the 1cv8
      executable for this environment. The product-layer real-stand
      readiness boundary checks file existence / file-vs-directory /
      basic shape; it does **not** assume any 1cv8-specific CLI
      grammar. ``None`` means the operator has not declared a binary
      yet — readiness will report this as a blocking finding when a
      smoke test is requested.
    - ``onec_binary_probe_args`` — operator-declared argv tail used
      by the controlled smoke probe. The smoke test runs
      ``[onec_binary_path] + onec_binary_probe_args`` through
      :mod:`onec_process_runner`. Operator owns the safety of these
      args; the platform does **not** invent a 1cv8-flag default,
      and the smoke test never opens a GUI / mutates an infobase
      without explicit operator configuration. ``None`` means the
      smoke test stays at a metadata-only probe (existence / shape).

    Phase 6 / Step 2 added one more optional field for the real
    ``DumpCfg`` execution path:

    - ``onec_dumpcfg_command_template`` — operator-declared **full
      argv template** for invoking 1cv8 to produce a dump snapshot.
      The platform does **not** invent 1cv8 CLI grammar: the
      operator writes the exact argv they want to be executed, with
      a small set of whitelisted placeholders that the write-tool
      substitutes safely (no shell). When this field is set
      together with ``onec_binary_path``,
      :func:`mcp_write_server.tools.create_dump_snapshot` switches
      to a binary-backed dispatch instead of the legacy stub. When
      either is missing, the tool keeps the legacy stub behaviour
      unchanged. Allowed placeholders are listed in
      ``mcp_write_server.tools._DUMPCFG_TEMPLATE_PLACEHOLDERS``;
      shell strings are not supported (argv list only).

    Parallel Track A / Step 2 added one more optional field for the
    real ``LoadCfg`` (apply config from files) execution path:

    - ``onec_applycfg_command_template`` — operator-declared **full
      argv template** for invoking 1cv8 to apply a configuration
      from a previously-dumped source tree
      (``LoadConfigFromFiles`` semantics). Same philosophy as
      ``onec_dumpcfg_command_template``: the platform does **not**
      invent 1cv8 CLI grammar — the operator writes the exact argv
      with a small set of whitelisted placeholders, and the
      write-tool substitutes them safely (no shell). When this
      field is set together with ``onec_binary_path``,
      :func:`mcp_write_server.tools.apply_config_from_files`
      switches to a binary-backed dispatch instead of the legacy
      stub-process apply. When either is missing, the tool keeps
      the legacy stub behaviour unchanged. Allowed placeholders are
      listed in
      ``mcp_write_server.tools._APPLYCFG_TEMPLATE_PLACEHOLDERS``;
      shell strings are not supported (argv list only).

    Parallel Track A / Step 3 added one more optional field for the
    real ``UpdateDBCfg`` (update database configuration) execution
    path:

    - ``onec_updatedb_command_template`` — operator-declared **full
      argv template** for invoking 1cv8 to update the database
      configuration after a successful apply
      (``UpdateDBCfg`` semantics). Same philosophy as the other two
      argv-template fields: the platform does **not** invent 1cv8
      CLI grammar — operator writes the exact argv with a small
      set of whitelisted placeholders, and the write-tool
      substitutes them safely (no shell). When this field is set
      together with ``onec_binary_path``,
      :func:`mcp_write_server.tools.update_database_configuration`
      switches to a binary-backed dispatch instead of the legacy
      stub-process update. When either is missing, the tool keeps
      the legacy stub behaviour unchanged. Allowed placeholders
      are listed in
      ``mcp_write_server.tools._UPDATEDB_TEMPLATE_PLACEHOLDERS``
      (a tighter subset than dumpcfg / applycfg — UpdateDBCfg
      does not need ``output_path`` or ``source_dump_path`` since
      it operates on the live infobase against the
      previously-applied config); shell strings are not supported
      (argv list only).
    """

    name: str
    base_id: str
    base_path: str
    publication_name: str
    http_base_url: str
    dump_path: str
    timeout_seconds: int | float
    allow_write: bool = False
    onec_binary_path: str | None = None
    onec_binary_probe_args: list[str] | None = None
    onec_dumpcfg_command_template: list[str] | None = None
    onec_applycfg_command_template: list[str] | None = None
    onec_updatedb_command_template: list[str] | None = None


@dataclass
class ProjectConfig:
    """Top-level configuration of the platform project."""

    environments: dict[str, EnvironmentConfig]
