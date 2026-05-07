# Administrator Manual — 1C Agent Platform

Practical guide for the **administrator** — the person who decides
what goes into the product config, where the work directory lives,
and what the operator's runtime services actually run. Distinct from
the operator manual: an administrator owns config, the operator
owns daily operations.

Audience assumption: comfortable with paths, processes, and JSON
config; not necessarily a Python developer.

---

## Product config — what you actually need to fill in

A product config is a JSON document loadable by
`load_product_config`. Top-level required keys:

| Key | Type | Purpose |
|---|---|---|
| `product_name` | non-empty string | Operator-readable name. |
| `profile_name` | non-empty string | Free-form. Convention: `local-dev` / `staging` / `prod-readonly`. |
| `default_environment` | non-empty string | Must match a key in `project.environments`. |
| `project` | dict | Wrapped `onec_config.ProjectConfig` shape. |

Optional but recommended top-level keys:

| Key | Type | Purpose |
|---|---|---|
| `servers` | dict of bools | Toggles for `read` / `write` / `intelligence`. Default all `True`. |
| `bootstrap` | dict | `work_dir` (string), and three `require_*` flags (default `True`). |
| `runtime` | dict | The runtime services contract. See below. |

A bare-minimum config that loads:

```json
{
  "product_name": "1C Agent Platform",
  "profile_name": "local-dev",
  "default_environment": "local-dev",
  "project": {
    "environments": {
      "local-dev": {
        "name": "Local Dev",
        "base_id": "local-dev",
        "base_path": "C:/onec/infobase",
        "publication_name": "local-dev",
        "http_base_url": "http://127.0.0.1:8080/local-dev",
        "dump_path": "C:/onec/dump",
        "timeout_seconds": 5,
        "allow_write": true
      }
    }
  },
  "bootstrap": {"work_dir": "C:/onec/work"},
  "runtime": {
    "services": {
      "demo": {
        "name": "demo",
        "command": ["python", "-c", "import time; time.sleep(3600)"]
      }
    }
  }
}
```

Things to know:
- `default_environment` must be a key under
  `project.environments`. Otherwise `bootstrap_product` rejects
  the config with a clear message.
- `bootstrap.work_dir` must already exist on disk before any
  runtime call. The platform **never** creates `work_dir` itself —
  that is administrator territory.
- `allow_write: false` **disables** every mutating write-tool for
  this environment via the policy engine. Use this for read-only
  / staging configs.
- A name containing `prod` or `production` (in `name`, `base_id`,
  `publication_name`, or `http_base_url`) is **always** treated as
  production by the policy engine and writes are blocked
  regardless of `allow_write`.

---

## Runtime services — `runtime.services`

A **service** is one operator-declared long-lived subprocess. The
product runtime starts it on `start_product_runtime`, watches its
PID via the persisted state file, and stops it on
`stop_product_runtime`.

Per-service spec keys (all optional except as noted):

| Key | Type | Default | Notes |
|---|---|---|---|
| `name` | string | required by convention | Echo of the dict key. |
| `enabled` | bool | `true` | A disabled service is reported `status="disabled"` and never started. |
| `command` | non-empty list of strings | `null` | Argv list. **No shell strings.** Without `command` the service is reported `status="missing"`. |
| `working_dir` | string | `null` | cwd of the child process; `null` inherits parent. |
| `env_overrides` | dict<str,str> | `{}` | Merged on top of `os.environ`. |
| `restart_policy` | one of `"never"` / `"restart-if-stale"` | `"never"` | See below. |
| `logs_enabled` | bool | `true` | When `false`, `stdout`/`stderr` go to `DEVNULL` (legacy Step 3). |
| `log_max_bytes` | positive int | `1048576` (1 MiB) | Rotate threshold. **Booleans are rejected** — see why under loader notes. |

Loader notes (fail-closed for any bad shape):
- `restart_policy` must be exactly one of the two whitelist
  strings. `"always"`, `"on-failure"`, etc. are **rejected**.
- `logs_enabled` must be a **strict** `bool`. Strings like
  `"true"` are rejected to avoid silent truthiness traps.
- `log_max_bytes` must be a positive int. `bool` is explicitly
  rejected (Python's `bool ⊂ int`, so `log_max_bytes: true`
  would otherwise mean "1 byte"). Strings like `"1k"` are
  rejected.

---

## Restart policy — what it actually does

Only two values matter. Both fire **only on a boundary call**
(`start` / `reload` / `status`); there is no background watcher,
no timer, no daemon.

- `"never"` (default) — a stale PID stays stale. The dashboard
  surfaces `runtime_pid_stale:<svc>`. Operator decides whether to
  re-`start`.
- `"restart-if-stale"` — when a boundary call observes a stale
  PID, the runtime layer increments `restart_attempts` and tries
  one fresh spawn through the same `_start_one` path (logs +
  rotation + verify). Findings: `runtime_restart_attempted:<svc>`,
  then `runtime_restart_succeeded:<svc>` or
  `runtime_restart_failed:<svc>`. There is no exponential
  backoff and no max-attempts cap — every boundary call that
  sees stale will try once, regardless of history.

What `restart-if-stale` is **not**:
- not a process supervisor;
- not a watch-and-restart daemon;
- not a crash-loop manager;
- not a way to "keep the platform running"; if you need that,
  you need a real OS-level supervisor (Windows Service / systemd
  unit), which is out of Phase 6 scope.

---

## Where state and logs live

Everything platform-owned is under `<work_dir>/.runtime/`:

```
<work_dir>/
└── .runtime/
    ├── runtime-state.json         persisted state (atomic write)
    └── logs/
        ├── <svc>.out.log          current stdout
        ├── <svc>.out.log.1        previous stdout (rotation backup)
        ├── <svc>.err.log
        └── <svc>.err.log.1
```

- `runtime-state.json` schema_version is **2** (Phase 6 / Step 6).
  The reader still accepts version-1 files honestly: missing
  Step 6 fields default to sentinels (`"never"` / `0` / `None`)
  and the in-memory shape is normalised. Writers always emit
  version 2.
- The `.audit/audit.jsonl` file lives under
  `<environment.dump_path>/.audit/`, **not** under `work_dir`.
  That is by design: audit follows the dump it describes.

Per-environment `.audit/audit.jsonl`:
- Append-only JSONL.
- Each line is one `AuditRecord`.
- Step 4+ rows carry an optional `details` dict with
  `operation_name`, `rollback_supported`, and snapshot/path
  pointers. Pre-Step-4 rows omit the key — that omission is
  byte-identical to the old format.

---

## 1cv8 binary integration — what the optional fields really mean

These three optional environment-level fields enable real-1cv8
hooks. They are mutually independent in the loader, but
operationally they pair up:

| Field | Type | Purpose |
|---|---|---|
| `onec_binary_path` | absolute file path | Used by `get_real_stand_readiness` (file existence / shape) and as `{binary_path}` in `onec_dumpcfg_command_template`. |
| `onec_binary_probe_args` | list<str> | Argv tail for the smoke test's controlled subprocess invocation. |
| `onec_dumpcfg_command_template` | non-empty list<str> | Full argv template for `create_dump_snapshot`'s binary-backed mode. Whitelist placeholders only. |

Allowed placeholders inside `onec_dumpcfg_command_template`:
`{binary_path}`, `{output_path}`, `{base_path}`, `{base_id}`,
`{publication_name}`, `{http_base_url}`. Anything else fails
fail-closed at render time.

When **only one of** `onec_binary_path` /
`onec_dumpcfg_command_template` is set, `create_dump_snapshot`
falls back to its legacy stub mode (marker file + `dump-meta.json`).
This is the only config-time fallback in the system. Once an
operator declared the binary-backed contract by setting **both**,
runtime failures stay honest failures (non-zero exit propagates;
no silent retry under stub mode).

`onec_binary_probe_args` is independent: when missing, the smoke
test runs metadata-level checks only (`binary_invoked=False`).
Setting it turns on a controlled subprocess invocation against
the binary.

---

## Common failures and the right response

| Symptom | First thing to check |
|---|---|
| `bootstrap_product.ok=False, message="Product config rejected: ..."` | Read the `message`; the loader is specific. Common: missing `default_environment` key in `project.environments`, malformed `runtime.services.<svc>.command`. |
| `runtime_contract_empty` warning | Your config has no `runtime.services` entries (or all are `enabled=False`). The dashboard verdict goes `degraded` and mutating workflows refuse. Add at least one enabled service. |
| `runtime_pid_stale:<svc>` repeatedly | The service died after a previous start. Check `<work_dir>/.runtime/logs/<svc>.err.log`. If you intend the service to auto-recover, set `restart_policy: "restart-if-stale"`. |
| `runtime_log_dir_failed:<svc>` | `<work_dir>/.runtime/logs/` could not be created (typically permission, or a regular file is sitting there with that name). The service goes `status="error"`; nothing is written; **no silent fallback to DEVNULL**. |
| `runtime_log_rotated:<svc>` | Informational. The previous log exceeded `log_max_bytes` and was rotated to `<file>.1`. Old `.1` was overwritten. If you need long-term retention, run your own archiving job. |
| Smoke test `mode='blocked'` | `get_real_stand_readiness.recommended_actions` is the next step. Typical fix: set `onec_binary_path` to an existing executable file. |
| Smoke test `binary_exit_code != 0` | The binary actually ran and returned non-zero. Read `binary_stdout_excerpt` / `binary_stderr_excerpt` (1024 chars cap each). Probe args are **operator territory** — the platform does not invent them. |
| `automatic_recovery_supported=False` for an `add_catalog_attribute` row | The audit row is pre-Step-4 (no `details`) or one of the structured fields is missing. Use the `rollback_hint.*_root` paths for a manual restore. |

---

## What you should not expect from this version

- The platform does **not** start MCP transports for the three
  servers. They live as in-process modules. Productions usage
  requires you to wire transport yourself (out of Phase 6 scope).
- The platform does **not** ship installers (`.msi` / `.deb` /
  signed binaries). `run_install_fast_path` materialises a JSON
  config, nothing more.
- The platform does **not** ship hot reload, log aggregation,
  multi-generation rotation, or any form of secrets vault. If
  you need these, treat them as parallel tracks after Phase 6.
- The rollback assistant supports automatic execution **only**
  for two write-tools (`add_catalog_attribute`,
  `add_document_attribute`). Anything else is advisory-only.
- `apply_config_from_files` and `update_database_configuration`
  remain **stub-backed** in Phase 2. They have not been replaced
  by real `1cv8 LoadConfigFromFiles` / `UpdateDBCfg` invocations
  in Phase 6.

When the platform refuses to do something, that is the point.
The honest refusal is part of the contract.
