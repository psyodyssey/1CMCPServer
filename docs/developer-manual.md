# Developer Manual — 1C Agent Platform

Practical guide for the **developer** extending the platform. Not a
walk-through of every file: the per-app READMEs and `apps/platform/README.md`
remain the canonical reference. This manual is "where to put the
next thing without breaking the safety invariants".

Audience assumption: comfortable with Python, dataclasses, and the
existing read/write/intelligence/platform split.

---

## Architectural map (one screen)

```
                                  +-----------------------------+
                                  |         operator            |
                                  +-----------------------------+
                                                |
                                                v
+---------------------------+      +-----------------------------+
|  apps/platform/           |      |    docs/                    |
|  src/onec_platform        |      |  operator-manual.md         |
|                           |      |  administrator-manual.md    |
|  bootstrap / installer    |      |  developer-manual.md        |
|  doctor / dashboard       |      |  runbooks.md                |
|  workflow / recovery      |      |  tools-spec/* api/* …       |
|  realstand / runtime      |      +-----------------------------+
|                           |
|  state / process_control  |
|  runtime_logs / loader    |
|  models / templates       |
+---------------------------+
        |        |        |
        v        v        v
+---------+ +---------+ +-----------------+
|  read   | | write   | |  intelligence   |
|  15     | | 25      | |  16             |
|  tools  | | tools   | |  tools          |
+---------+ +---------+ +-----------------+
        |        |        |
        +--------+--------+
                 |
                 v
        +-----------------+
        |  packages/      |
        |  mcp-common,    |
        |  onec-config,   |
        |  onec-audit,    |
        |  onec-health,   |
        |  onec-policy-engine,
        |  onec-process-runner,
        |  onec-troubleshooting
        +-----------------+
```

Information flows top → bottom. Mutating effects flow only through
write-server's `run_write_flow` discipline. Read-side and
intelligence-side never mutate.

---

## Where to put the next capability

| You want to add… | Right home | Reason |
|---|---|---|
| A **new metadata read** (e.g. list-some-catalogs-by-pattern) | `apps/mcp-read-server/src/mcp_read_server/tools.py` | Read-side, no side effects, no policy engine. |
| A **new mutating metadata write** (e.g. add-some-element) | `apps/mcp-write-server/src/mcp_write_server/tools.py` + `runtime/metadata_ops.py` | Must route through `run_write_flow`. Internal helpers in `metadata_ops.py`. |
| A **new metadata verify check** | Either a private helper in `tools.py` plus a new `kind=` branch in `verify_metadata_change`, **or** a new top-level `verify_*` public tool. Prefer the dispatcher branch when the contract is "verify a thing exists / has a property" — it keeps public surface narrow. |
| A **new analytical read** (intelligence) | `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py` | Must be read-only by construction. No `onec_policy_engine` import. |
| A **new product-layer boundary** (operator-facing) | `apps/platform/src/onec_platform/<area>.py` | Boundary helpers never raise; produce structured results. |
| A **new safety contract / guardrail** | Per-package model file + a private check inside the boundary that needs it. Avoid creating a new package for one rule. |

When in doubt, the rule is: **the layer that mutates state is the
layer that owns the policy decision around it.** Read and
intelligence never decide write policy.

---

## Safety invariants you cannot break

1. **`run_write_flow` is the only path to a mutating effect.** Every
   public mutating write-tool routes through it. The product layer
   never opens files in a dump and writes to them directly. Step 4
   rollback uses a public write-tool (`restore_dump_file_from_snapshot`)
   precisely so it inherits the same discipline.

2. **`onec_policy_engine` is imported only by the write-server and
   `onec-config`.** It is **not** imported by:
   - `apps/platform/src/**`,
   - `apps/mcp-intelligence-server/src/**`,
   - `apps/mcp-read-server/src/**`.
   The integration check programmatically verifies this; a CI
   that ever flags an import there is correct, the import is
   wrong.

3. **The intelligence server is read-only by construction.** It
   never calls `run_write_flow`, never writes audit, never opens
   a dump for write. The contract is enforced by absence of the
   policy-engine import.

4. **No silent fallbacks.** If a precondition fails, the boundary
   returns `ok=False` with an honest reason. There is no "if X
   doesn't work, try Y instead" hidden in the runtime.

5. **No `shell=True` anywhere.** All subprocess invocations use
   argv lists. This includes `onec_dumpcfg_command_template`,
   `onec_binary_probe_args`, and `runtime.services[*].command`.

6. **Atomic writes.** Persisted files (`runtime-state.json`,
   product config, attribute XML, restore target) all use
   `*.tmp` + `os.replace` — readers never see a partial state.

7. **Boundary helpers never raise.** The contract is `ok=False`
   plus a finding. `try/except` at the boundary translates every
   exception into a structured result; only the failure path
   inside the boundary itself uses raises.

When you add a new boundary, the integration check at
`C:/Users/user/AppData/Local/Temp/phase6_step7_check.py` is the
template for proving these properties.

---

## Phase 6 slice map (what each step actually shipped)

| Step | What changed | Key files |
|---|---|---|
| **1** | Planning | `docs/architecture/phase-6-*.md` |
| **2** | `create_dump_snapshot` got a binary-backed branch (operator-declared `onec_dumpcfg_command_template`); stub stays as backward-compat default. | `apps/mcp-write-server/.../tools.py`, `onec-config/models.py` |
| **3** | Install fast path: declarative template + atomic JSON write + round-trip bootstrap. | `apps/platform/.../installer.py`, `templates.py` |
| **4** | First executable rollback for `add_catalog_attribute` / `add_document_attribute` only. New write-tool `restore_dump_file_from_snapshot` (registry +1 → 24). Audit `details` dict added (back-compat: omitted when None). | `apps/mcp-write-server/.../tools.py`, `runtime/flow.py`; `onec-audit/models.py`; `onec_platform/recovery.py` |
| **5** | First structural XML edit: `add_form_attribute` (registry +1 → 25). Six DOM-style helpers in `metadata_ops.py`. New `verify_metadata_change(kind="form_attribute_exists")`. | `apps/mcp-write-server/.../tools.py`, `runtime/metadata_ops.py` |
| **6** | Runtime hardening: per-service log files + 1-generation rotation, `restart_policy ∈ {"never","restart-if-stale"}` (boundary-only), `RuntimeServiceState` enriched, schema bumped 1→2 (back-compat read). | `onec_platform/runtime.py`, `runtime_logs.py`, `process_control.py`, `state.py`, `models.py`, `loader.py` |
| **7** | Validation + standalone docs. **No code changes.** | `docs/operator-manual.md`, `administrator-manual.md`, `developer-manual.md`, `runbooks.md` |

Phase 6 narrowed scope on every step rather than fanning out — that
is the deliberate discipline. Each step ships exactly one new slice
and explicitly leaves N follow-ups for parallel tracks.

---

## How to write a manual-check script

The pattern across `phase6_step{2..7}_check.py`:

```
# 1. Import path bootstrap.
ROOT = Path(r"C:\Tools\1c-agent-platform")
for sub in [...]:                          # all src trees
    sys.path.insert(0, str(ROOT / sub))

# 2. Tempdir for synthetic state.
workdir_root = Path(tempfile.mkdtemp(prefix="stepN_check_"))

# 3. Local HTTPServer for the gateway, only when scenarios need a
#    healthy dashboard.
gateway = _Gateway(); base_url = gateway.start()

# 4. Per-case workdir; never reuse the root for multiple cases.
work = workdir_root / "case-x"; work.mkdir()

# 5. Real subprocesses where they matter — but never the real 1cv8
#    binary; use sys.executable as a stand-in.

# 6. Discipline asserts: registry counts, suggested-tool whitelist,
#    zero policy-engine imports.
```

Three pitfalls to avoid:
- **Multi-line `python -c` payloads on Windows** — command-line
  quoting can mangle them. Materialise the script as a file and
  pass the path. (Step 6's manual check learnt this the hard way.)
- **Reading log files after `stop`** — the child gets a hard
  TerminateProcess on Windows. Read while the child is still
  running, or use `flush()` + a small sleep before stop.
- **`cp1251` console encoding** — Russian-Windows consoles cannot
  print `→` / `✓` / `…`. Use ASCII alternatives in `print()`.

---

## How not to dilute `run_write_flow`

`run_write_flow` is the choke-point. Every change that touches
mutating discipline goes through it. The signature is stable:

```
run_write_flow(
    environment, intent,
    *, label,
    operation_callable: Callable[[ctx], dict],
    verify_callable: Callable[[ctx, op_payload], dict],
) -> ToolResult
```

Rules of thumb:
- The `operation_callable` should **only** mutate. Validation
  belongs upstream (in the public tool). Snapshot creation and
  audit happen in the flow itself; do not reimplement them.
- The `verify_callable` should re-read the file and confirm the
  invariant the operator cares about. Substring presence is a
  weak verify; structural presence (DOM check, byte-equality)
  is strong.
- `intent.operation_name` must be in
  `_MUTATING_OPERATIONS` or `_METADATA_MUTATING_OPERATIONS` of
  `onec_policy_engine`. Otherwise the policy engine fail-closes
  with `unknown_intent`.
- Audit `details` (Step 4+) is a small JSON-serialisable dict
  carrying `operation_name`, `rollback_supported`,
  `backup_snapshot_path`, `dump_snapshot_path`, `relative_path`.
  The flow populates it automatically.
- The product-layer recovery code reads `details` to decide
  whether automatic rollback is supported (`tool_name` in the
  Step 4 whitelist **and** `details` carry both
  `dump_snapshot_path` and `relative_path`).

If your new tool needs to do something `run_write_flow` cannot
express, **stop and propose a flow extension** — do not bypass
the flow.

---

## Where to start when reviewing a PR

1. Did `read=15` / `write=N` / `intelligence=16` move? If yes,
   was it announced in the step brief?
2. Are there any `import onec_policy_engine` lines under
   `apps/platform/src` or `apps/mcp-intelligence-server/src`?
3. Does any new mutating tool route through `run_write_flow`?
4. Does the new boundary helper return a structured result on
   every code path, or is there a `raise` that escapes?
5. Are any preconditions short-circuited with `# TODO` or
   `_silent_fallback_`? Both are red flags.
6. Was the manual check updated alongside the code? A code change
   without a matching `phase{N}_step{M}_check.py` revision is a
   half-shipped change.

The README of the changed app or package should answer "what
does this look like to an operator and to a developer". If a PR
adds a behaviour the README does not describe, the README is
the bug.
