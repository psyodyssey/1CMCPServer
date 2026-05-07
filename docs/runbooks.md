# Runbooks — 1C Agent Platform

Short "when X, do Y" recipes. Each runbook is a fixed shape:
**Symptom**, **Cause**, **Diagnose**, **Fix**, **Confirm**. They are
deliberately compact — for narrative context see
`docs/operator-manual.md` / `docs/administrator-manual.md`.

The pre-existing runbook at `docs/runbooks/local-dev-check.md`
remains as-is; the recipes below complement, not replace it.

---

## RB-1 — Bootstrap doctor red

**Symptom.** `bootstrap_product(...)` returns
`ok=False, message="Product config rejected: ..."` **or**
`ok=True` but `doctor.error_count > 0`.

**Cause.** Product config either fails structural validation in
the loader or passes loader but fails one of the doctor's prereq
checks (`work_dir` missing, `dump_path` missing, Python interpreter
not found on PATH, etc.).

**Diagnose.**
1. Read the `message` field. The loader is specific:
   - `"... is missing required key 'X'"` → fill in `X`;
   - `"'runtime.services.<svc>.command' must be a non-empty list..."` → fix shape;
   - `"'runtime.services.<svc>.restart_policy' must be one of [...]'"` → use the whitelist.
2. If the message says doctor errored, look at `boot.doctor.findings`
   for entries with `severity="error"`.

**Fix.** Edit the JSON config (or the dict, if calling
programmatically) and re-run `bootstrap_product`. The doctor
reports paths that are absolute and concrete; copy them into your
shell to confirm.

**Confirm.** `bootstrap_product(...)` returns
`ok=True, doctor.error_count == 0`. Then call
`build_environment_dashboard` once — it should be at least
`degraded` (and `healthy` if you set up runtime services).

---

## RB-2 — Runtime stale PID

**Symptom.** `get_product_runtime_status` returns one or more
services with `status="stale"` and a `runtime_pid_stale:<svc>`
finding.

**Cause.** The persisted state file says the service was running
under PID *N*, but the OS no longer knows that PID. Process
crashed, was killed externally, or the host rebooted between
`start` and `status`.

**Diagnose.**
1. Inspect the service's stderr log:
   `<work_dir>/.runtime/logs/<svc>.err.log`. Look for the last
   exception / non-zero exit message.
2. On Windows, the stale finding includes `last_exit_code=N`
   when available. POSIX honest-degrades to "exit code
   unavailable on this platform".
3. Confirm the spec is still well-formed:
   `runtime.services.<svc>.command` is a non-empty argv list.

**Fix.** Two options.
- **Manual:** call `start_product_runtime(...)` (or
  `reload_product_runtime`) to spawn a fresh process. The new
  PID is persisted; `last_started_at` is stamped fresh.
- **Operator-declared auto-recovery:** set
  `restart_policy: "restart-if-stale"` on the service. From the
  next boundary call (`start` / `reload` / `status`) onward, a
  stale PID triggers exactly one fresh spawn; findings
  `runtime_restart_attempted:<svc>` then either
  `runtime_restart_succeeded:<svc>` or
  `runtime_restart_failed:<svc>` will appear.

**Confirm.** `get_product_runtime_status` shows
`status="running"`, a fresh `pid`, and `last_started_at`
updated. `runtime_pid_stale:<svc>` finding is gone.

**Caveat.** `restart-if-stale` fires only on a boundary call. It
is **not** a background watcher; if you need OS-level
supervision, pair the service with a Windows Service / systemd
unit (out of Phase 6 scope).

---

## RB-3 — Workflow blocked

**Symptom.** `run_guided_workflow(..., confirm_execute=True)`
returns `mode="blocked"` and `execution_performed=False`. The
preview is still populated, but no write happened.

**Cause.** The dashboard verdict for the resolved environment is
not `healthy`. `ready_for_workflows` is `False`. The blocking
gate refuses to run a mutating workflow under a degraded /
blocked dashboard, by design.

**Diagnose.**
1. Run `build_environment_dashboard(...)`.
2. Read `verdict.blocking_issues` and `verdict.warnings`.
3. Top blockers, in observed frequency:
   - `read_health_code:dump_missing` — `environment.dump_path`
     does not exist.
   - `read_health_code:gateway_down` — HTTP gateway at
     `environment.http_base_url` does not respond. Check whether
     the gateway is supposed to be running for this environment
     and start it.
   - `bootstrap_section_failed` — config / doctor problems;
     follow RB-1.
   - `runtime_required_service_missing:<svc>` — a service marked
     `enabled=True` has no `command`; either set the command or
     mark it disabled.

**Fix.** Address each blocker one at a time. Re-run
`build_environment_dashboard` after each fix. The warning
`runtime_contract_empty` (no `runtime.services` declared at all)
is a degraded — add at least one enabled service spec.

**Confirm.** Dashboard returns `overall_status="healthy"` and
`ready_for_workflows=True`. Re-run the workflow with
`confirm_execute=True`; it should reach `mode="executed"`.

---

## RB-4 — Reading a rollback preview / executed / unsupported

**Symptom.** Operator just ran a mutating workflow, has the
`operation_id`, and wants to know what rollback options exist.

**Diagnose.** Always start with **preview**:

```
res = run_rollback_assistant(cfg, operation_id=<id>)
res.plan.automatic_recovery_supported  # True or False
res.rollback_hint                      # backup / dump roots
```

Three honest outcomes when you re-run with
`confirm_execute=True`:

- **`mode="executed"`, `ok=True`** — the rollback succeeded:
  `restore_dump_file_from_snapshot` returned `ok=True`, and the
  mandatory post-rollback verify (`diff_dump_fragment`) reports
  `data.changed=False`. Both signals are required for `ok=True`.
- **`mode="unsupported"`, `ok=True`** — the operation's
  `tool_name` is **not** in the Step 4 automatic-recovery
  whitelist, **or** its audit row is pre-Step-4 and lacks the
  structured `details` field. The product layer honestly
  refuses to fake an automatic rollback. Manual path: use
  `rollback_hint.suggested_backup_root` /
  `suggested_dump_root` (or your own snapshots) to restore the
  file by hand. The platform does not do the copy for you.
- **`mode="blocked"`, `ok=False`** — the dashboard was not
  healthy at the moment of the call. Resolve dashboard issues
  (RB-3) and re-run.

**Step 4 whitelist (current):** `add_catalog_attribute` and
`add_document_attribute` only. Everything else stays
advisory-only until a future step extends the whitelist. The
whitelist is not magic — these two were chosen because their
mutation is fully described by **one** XML file, and the inverse
is exactly "copy the snapshot version of that file back".

**Confirm.** When `mode="executed", ok=True`, the live dump file
byte-equals the pre-add baseline. The integration check at
`phase6_step7_check.py` re-parses the catalog XML to prove this
structurally — copy that pattern when you need a similar proof.

---

## RB-5 — Real-stand smoke failed

**Symptom.** `run_real_stand_smoke_test(..., confirm_execute=True)`
returned with one of:
- `mode="blocked"` — readiness gate refused.
- `mode="executed"`, `binary_invoked=True`, `binary_exit_code != 0` —
  the binary actually ran and returned a non-zero exit.

**Cause depends on which.**
- `mode="blocked"` — `get_real_stand_readiness` already explained
  why. Common: `onec_binary_path` missing / not a regular file /
  no execute bits on POSIX, or dashboard not healthy.
- `mode="executed"` with non-zero exit — the binary itself
  rejected the probe args. The platform does not invent probe
  args; whatever you put into `onec_binary_probe_args` was
  invoked literally.

**Diagnose.**
- For blocked: read `readiness.recommended_actions`. Each
  finding is paired with one specific action.
- For non-zero exit: read
  `smoke.binary_stdout_excerpt` and
  `smoke.binary_stderr_excerpt` (each capped at 1024 chars).
  These are the first surface to look at; full logs are
  operator territory.

**Fix.**
- Blocked: address each `recommended_actions` entry.
- Non-zero exit: change `onec_binary_probe_args` so the binary
  accepts the probe. Smoke probe args are normally a metadata-
  only invocation (`-version` / `-Q` / equivalent) — **not** a
  full `DESIGNER /CHECKMODULE` run.

**Confirm.** `mode="executed", binary_invoked=True,
binary_exit_code=0`. This is a one-time smoke; it is **not** a
substitute for your own end-to-end testing against a real
infobase.

---

## RB-6 — Malformed audit log lines

**Symptom.** `get_operation_history(...)` returns `ok=True` but
the `findings` list contains entries like
`audit_line_invalid_json:<index>` or
`audit_line_missing_fields:<index>`. The history is shorter than
expected.

**Cause.** A line in `<dump_path>/.audit/audit.jsonl` is not a
well-formed `AuditRecord` JSON dict, or is missing required
string fields. This typically happens when an external tool
(or a hand-edit) appended a line that the platform did not
generate. The platform's own writer never produces malformed
lines.

**Diagnose.**
1. Open the audit file: `<dump_path>/.audit/audit.jsonl`.
2. Walk to the line index from the finding code. Compare against
   a well-formed line above or below — required keys are
   `operation_id`, `tool_name`, `environment`, `base_id`,
   `status`, `message` (all strings).
3. Confirm the file is JSON-Lines (one record per line, no
   leading whitespace, no trailing comma).

**Fix.** The audit file is **append-only by contract**. Two safe
options:
- **Leave the malformed line in place.** The history boundary
  surfaces a finding but does not crash; `inspect_operation` on
  any other `operation_id` still works. This is the
  recommended response when the malformed line is harmless
  (e.g. corrupted single byte from a crashed external writer).
- **Rotate the audit file manually.** Stop product runtime,
  rename `.audit/audit.jsonl` to `.audit/audit.jsonl.<date>`,
  let the platform recreate a fresh file on the next mutating
  call. Old `operation_id`s become unreadable to the platform —
  do this only when the operator no longer needs old history.

**Do not** edit lines in place. The audit file shape is
JSON-Lines append-only; in-place edits are explicitly
out-of-contract and may shift line indices that other tools
depend on.

**Confirm.** `get_operation_history(...).findings` no longer
contains the offending `audit_line_*:<index>` entry; the entries
list shows the recovered history.
