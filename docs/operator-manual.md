# Operator Manual — 1C Agent Platform

Practical guide for the **operator** of the platform — the person who
installs, starts, watches, and recovers a working installation. Not a
reference for every public tool: that lives in the per-app READMEs and
in `docs/tools-spec/`. This manual focuses on the boundary helpers an
operator actually invokes during a normal day.

Audience assumption: comfortable with a terminal, comfortable with
JSON, no need to read source code to operate the platform.

---

## What the platform is, in one paragraph

The 1C Agent Platform is a controlled wrapper around a 1С:Enterprise
infobase that exposes three MCP servers (read / write / intelligence)
and a thin **product layer** (`onec_platform`) that orchestrates
install, runtime, dashboards, workflows, rollback, and a real-stand
smoke test. Mutating operations on a 1С infobase always go through the
write-server's `run_write_flow` discipline (preflight → snapshot →
operation → verify → audit). The product layer **never** writes to a
1С dump directly — it only calls public write-tools.

Phase 6 status: registries are read=15, write=25, intelligence=16.
None of these change between operator releases unless explicitly
announced.

---

## Short path: install → bootstrap → run

```
1. Operator fills in a minimal product config dict.
2. run_install_fast_path(...,confirm_write=True) → JSON on disk.
3. start_product_runtime_from_json_file(<path>)        → services up.
4. get_product_runtime_status_from_json_file(<path>)   → confirm PIDs.
5. build_environment_dashboard_from_json_file(<path>)  → must be 'healthy'.
6. (optional) run_guided_workflow_from_json_file(...)  → real change.
7. (optional) get_operation_history_from_json_file(...) → audit.
8. stop_product_runtime_from_json_file(<path>)         → services down.
```

That is the full operator loop. Everything else is recovery, verify,
or smoke-test.

### Fast-path details

`run_install_fast_path` has two modes:
- `preview` (default): builds the JSON template in memory, runs
  `bootstrap_product` once for shape validation, **does not write**.
- `executed`: writes the JSON atomically (`*.tmp` + `os.replace`),
  refuses to overwrite an existing file, then re-loads it via
  `bootstrap_product_from_json_file` to confirm round-trip readability.
  `bootstrap_post.ok` tells you the file is readable.

If install fails, you get `mode='rejected'` and a concrete reason. No
silent overwrite; no half-written config.

---

## Status words and what they mean

The operator sees a small fixed vocabulary across boundaries.

### Dashboard verdict (`build_environment_dashboard`)
- **`healthy`** — every section reported `ok` and no blocking
  rule fired. `ready_for_workflows = True`. Mutating workflows can
  proceed.
- **`degraded`** — at least one **warning** rule fired, but no
  **blocking** rule. `ready_for_workflows = False`. Read-only
  surfaces (history, inspect, preview) still work; mutating
  workflows refuse to start. Common cause: `runtime_contract_empty`
  on a config with no `runtime.services`.
- **`blocked`** — at least one blocking rule fired (bootstrap
  failed, gateway down, dump path missing, required service
  missing/error). `ready_for_workflows = False`.

### Workflow / rollback / smoke modes
- **`preview`** — the boundary built the plan and stopped before
  any mutating effect. Default for `confirm_execute=False`.
- **`executed`** — the boundary actually ran the mutating step.
  `ok=True` only if the step + verify both succeeded.
- **`blocked`** — `confirm_execute=True` was requested but the
  preflight gate refused (dashboard not ready, readiness gate
  failed). The preview is preserved; nothing was written.
- **`unsupported`** — `confirm_execute=True` was requested but the
  product layer honestly does not support automatic execution for
  this case (rollback assistant only supports a tiny whitelist;
  see below). No write; no fake success.
- **`rejected`** — invalid input / unloadable config. Boundary
  never raises.

If you see anything else, it is a bug.

---

## Mutating workflows — the safe shape

The platform ships three guided workflows:
- `safe-add-attribute` — adds an attribute to a Catalog or Document
  XML card.
- `safe-add-module-method` — appends a method to a CommonModule's
  module file.
- `stand-health-check` — diagnostic; never mutates anything.

For every mutating workflow:

1. Always run with `confirm_execute=False` first. The result's
   `plan.summary` shows what will happen and which write-tool will
   be called.
2. Read `plan.suggested_tools` / `plan.suggested_write_tools` —
   these are validated against the live registries; only real names
   appear there.
3. Re-run with `confirm_execute=True` only after you have read the
   preview.
4. After execution, capture `result.last_write_operation.operation_id` —
   you will need it for inspect / rollback.

Common confused-state recoveries:
- If `mode='blocked'` came back, your dashboard was not healthy.
  Run `build_environment_dashboard` and address `blocking_issues` /
  `warnings` first.
- If `mode='rejected'` came back, the params you passed were
  malformed. The `message` and findings explain exactly why.

---

## Reading a rollback preview

`run_rollback_assistant(..., operation_id=<id>)` is the single
operator-facing rollback boundary. Run **without** `confirm_execute`
first. The result contains:
- `plan.automatic_recovery_supported` — is automatic rollback
  possible at all? **Phase 6 / Step 4** ships this for **only two
  tools**: `add_catalog_attribute` and `add_document_attribute`.
  Everything else returns `False` here.
- `plan.summary` — operator-readable text describing what would
  happen.
- `rollback_hint` — pointers to the `backup_snapshot_path` /
  `dump_snapshot_path` that recovery would use.
- `suggested_write_tools` — only `restore_dump_file_from_snapshot` /
  `diff_dump_fragment` show up when `automatic_recovery_supported`
  is `True`.

If `automatic_recovery_supported=True`, re-running with
`confirm_execute=True` performs the rollback through the public
`restore_dump_file_from_snapshot` write-tool (so it inherits the
full write-flow discipline) and then runs a mandatory post-rollback
verify via `diff_dump_fragment`. Success requires both the restore
and the verify to come back clean (`changed=False`).

If `automatic_recovery_supported=False`, you have two honest
options:
1. Use `rollback_hint.suggested_backup_root` /
   `suggested_dump_root` to perform a manual snapshot restore
   yourself (operator territory). The product layer does not do
   the copy for you.
2. Wait for a future step that extends the whitelist.

There is no third option. The product layer **does not** ship a
back-door write channel just to claim "rollback works".

---

## Real-stand smoke test

`run_real_stand_smoke_test` exists to confirm — once — that the
installation can talk to the configured 1cv8 binary. Two modes:
- `preview`: plan-only.
- `executed`: runs a metadata-level filesystem probe and, if
  `onec_binary_probe_args` is configured, a controlled subprocess
  invocation of the binary.

Honest signals:
- `binary_invoked=True` + `binary_exit_code=0` — probe ran clean.
- `binary_invoked=True` + `binary_exit_code != 0` — probe ran but
  the binary returned an error. No silent fallback to "ok".
- `mode='blocked'` — readiness gate failed (binary missing /
  unreadable / dashboard not healthy). Fix the readiness issue
  first.

This is a **smoke test**, not a CI matrix. It does not replace your
own validation against a real 1С infobase.

---

## Honest Phase 6 limitations

What the platform deliberately **does not** ship in Phase 6:
- No production-grade process supervisor (no Windows Service /
  systemd unit registration).
- No background watcher / auto-restart daemon. The `restart-if-stale`
  policy fires only when an operator calls `start` / `reload` /
  `status`.
- No hot reload — `reload_product_runtime` is a controlled
  stop-then-start.
- No web UI / dashboard frontend.
- No log aggregation / forwarding. Logs live locally under
  `<work_dir>/.runtime/logs/`.
- No multi-generation log rotation. The shim keeps one `.1`
  backup; older backups are overwritten.
- No automatic rollback for tools outside the two-entry whitelist.
- No `delete_*` write-tools at all.
- No XML namespace handling in `add_form_attribute`. Tests and
  Phase 3 / 5 fixtures use un-namespaced cards; production cards
  with `xmlns="..."` are out of scope.

When you hit one of these, the operator-visible response is a
finding (`runtime_contract_empty`, `automatic_recovery_supported=False`,
etc.) — not a crash, not a silent fall-through.

---

## Where to look next

- `docs/administrator-manual.md` — config keys, runtime services,
  binary integration, where state and logs live.
- `docs/runbooks.md` — short "when X, do Y" recipes for common
  red signals.
- `docs/developer-manual.md` — architecture map and how to extend
  the platform safely.
- `apps/platform/README.md` — full Phase 5 + Phase 6 product-layer
  surface in one place.
