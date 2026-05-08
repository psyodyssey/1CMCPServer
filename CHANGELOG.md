# Changelog

All notable changes to **1C Agent Platform** are documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and the project adheres to [Semantic Versioning](https://semver.org/) starting
from `0.1.0`.

## 0.2.0 — Parallel Track D — Operator Credentials Hardening

This release closes **Parallel Track D — Operator Credentials
Hardening**, the fourth post-phase parallel track. Track D made the
operator credentials path less brittle by introducing a documented
`${ENV:NAME}` substitution form for argv elements inside
`onec_*_command_template`, render-time fail-closed semantics on
missing or malformed env tokens, password-position redaction in
`command_preview` and audit excerpts, operator-facing docs migrated
to the env-substitution default with literal cleartext kept as a
legacy fallback, and a narrow credential-template-hygiene heuristic
in `scripts/release/verify-release.ps1`. This is **not** an
enterprise security platform: no vault, no KMS, no SSO/RBAC, no OS
keychain, no encrypted-at-rest secrets file format. Six steps
total; production code was touched only at one boundary file
(`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`)
and one release-side script (`scripts/release/verify-release.ps1`);
all other steps were documentation-only or aligned existing
operator-facing docs.

### Per-step outcomes

- **Step 1 (planning operator credentials hardening)** — two
  planning documents under `docs/architecture/track-d-*` (plan +
  step-map). No code changes.
- **Step 2 (credentials-flow audit and contract)** — two new
  documentation-only documents under `docs/architecture/`:
  `track-d-credentials-flow-audit.md` (where `/P "<password>"` is
  surfaced today, which payload fields see rendered argv, what
  "out-of-band" meant before Track D), and
  `track-d-credentials-contract.md` (formal contract for the
  `${ENV:NAME}` substitution syntax, render-time resolution
  order, fail-closed semantics, redaction discipline, backward
  compatibility with literal cleartext templates). No code
  changes.
- **Step 3 (env substitution and preview redaction)** —
  implementation in
  `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`:
  `_resolve_env_token(...)` resolves the full-element token
  `${ENV:NAME}` from the process environment at render time
  (after structural placeholder substitution); fail-closed on
  missing, empty, or partial / mixed forms (`ok=False`,
  `command_preview=None`, no subprocess started);
  `_redact_password_args(...)` replaces the argv element
  following `/P` or `/Pwd` (case-insensitive) with the sentinel
  `<redacted>` in `command_preview` and trimmed payload
  excerpts. The actual subprocess argv stays unredacted because
  the binary must authenticate. Literal cleartext templates
  remain supported as a legacy fallback. Registry invariant
  preserved: `read=15 / write=25 / intelligence=16`.
- **Step 4 (operator docs and migration alignment)** —
  operator-facing documentation migrated to the `${ENV:NAME}`
  form as the recommended default, with literal cleartext kept
  as a clearly marked legacy fallback. Three documents aligned:
  `docs/runbooks/track-a-reference-stand-round-trip.md` (product
  config example, env-substitution callout, failure mode F2
  extended to env-token failures, credentials-in-logs note
  updated), `SECURITY.md` (Honest constraints block rewritten
  under env-substitution), `docs/release-handoff.md` (Known
  limitations DESIGNER credentials bullet rewritten). No code
  changes.
- **Step 5 (release verify credential hygiene heuristic)** —
  eighth release-facing check **Credential template hygiene**
  added to `scripts/release/verify-release.ps1`. The check
  scans tracked `*.config.json` files (via `git ls-files`) for
  argv elements immediately following `"/P"` or `"/Pwd"`
  (case-insensitive) inside command-template arrays. Documented
  safe forms (`"${ENV:NAME}"`, `"<password>"`) pass; literal
  cleartext values emit `WARN` (not `FAIL`), naming file and
  line; empty values are not flagged. WARN does not change
  exit-code semantics, so legacy templates do not block the
  receive-side flow. `scripts/release/README.md` and
  `docs/release-handoff.md` updated to describe the eighth
  check and its narrow heuristic-not-DLP scope.
- **Step 6 (final integration pass and Track D closure)** —
  this closure: `pyproject.toml` version bumped 0.1.0 → 0.2.0;
  `README.md`, `PROJECT-STATUS.md`, and `CHANGELOG.md` aligned
  with Track D closed status. Read-only final integration
  check green: linear Step 1 → 6 history, all Step 1–5
  deliverables present on disk, registries `read=15 / write=25
  / intelligence=16` without drift, `verify-release.ps1` GREEN
  with eight checks, no real credentials anywhere in the
  diffs of the six Track D commits.

### Registry invariant carried into 0.2.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track D.

### Honest constraints update

- DESIGNER credentials remain operator-managed. The new
  **recommended path** is the `${ENV:NAME}` substitution form
  resolved at render time. Literal cleartext templates remain
  supported as a legacy fallback. The platform still does
  **not** ship a secrets manager, vault, KMS, OS keychain
  integration, or encrypted-at-rest secrets file format —
  operators feed env vars from their own secrets infrastructure
  if they need that.
- Check 8 is a narrow heuristic over tracked `*.config.json`
  files, not a full DLP scan. It does not parse 1С template
  semantics, does not scan runbooks or other documentation,
  and emits `WARN` (not `FAIL`).
- All other 0.1.0 honest constraints carry forward unchanged
  (single-version 1С smoke evidence on `8.3.27.1859`, no
  production-grade MCP transport, no installer ecosystem,
  no full enterprise super-set, no hot reload, no full AST
  parser, no full rollback / delete coverage).

### Parallel Track E follow-up — Multi-Version 1C Smoke Matrix (closure under 0.2.0)

After Track D closure, **Parallel Track E — Multi-Version 1C
Smoke Matrix** was opened as the fifth post-phase parallel
track and closed within the same `0.2.0` release line as a
documentation / scaffolding follow-up, **without** a minor
version bump (Q5 resolved: NO bump). Track E shipped no
functional delta — production code untouched throughout the
track, registries `read=15 / write=25 / intelligence=16`
without drift, no new MCP tools, no `1cv8.exe` runs at any
step. Six steps total.

#### Per-step outcomes

- **Step 1 (planning multi-version 1C smoke matrix)** — two
  planning documents under `docs/architecture/track-e-*` (plan
  + step-map). No code changes. Commit `1b233ce`.
- **Step 2 (current evidence audit and smoke scenario freeze)** —
  two new documentation-only documents:
  `track-e-current-evidence-audit.md` (descriptive — what is
  proven on reference `8.3.27.1859`, physical artifacts on
  disk, what is not yet evidenced, why single-version is
  insufficient; strict separation proven / inferred /
  not-yet-run / operator-supplied future inputs) and
  `track-e-smoke-scenario.md` (prescriptive **frozen** —
  scenario name `frozen-smoke-v1`, cut-down
  `create_dump_snapshot` via `/DumpConfigToFiles` only,
  principle-based version selection criteria,
  12-column matrix shape, PASS / FAIL / NOT RUN semantics,
  required evidence fields, Step 4 execution boundary).
  Commit `630f837`.
- **Step 3 (matrix scaffolding and operator runbook)** — two
  new operator-facing documents:
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`
  (operator runbook for running `frozen-smoke-v1` on an
  operator-supplied 1С version) and
  `docs/version-support-matrix.md` (top-level evidence
  table with frozen 12-column shape; reference Row 1 for
  `8.3.27.1859` filled copy-only from existing Track A /
  Step 6 evidence, scenario field explicitly marked as
  `stronger-than-frozen-smoke-v1`; no fabricated additional
  rows). No `1cv8.exe` run. Commit `7c08cae`.
- **Step 4 (operator-driven smoke execution and matrix update)** —
  closed via **PATH B (honest operator-supplied gap)**. No
  `1cv8.exe` runs were executed; no additional evidence rows
  were added. Operator-side inventory found only the `8.3.27`
  minor family installed locally (builds `1859/x64` reference
  + `1936/x86` same-family disqualified per Step 2 §2.2);
  no `8.3.<other minor>` family was available; ENV-substitution
  credentials were not set in the work session. Per Track E
  plan Q4 + step-map Step 4, this is honest closure, not
  track failure. `docs/version-support-matrix.md` gained a
  closure note subsection enumerating the actual operator-side
  inventory and an explicit list of what Step 4 deliberately
  did not do (no run on same-family x86 build, no rerun of
  reference, no scenario expansion, no matrix contract
  changes, no fabricated rows, no real credentials).
  Commit `f962d78`.
- **Step 5 (support statement and docs alignment)** — five
  point-edits across three operator-facing docs to align
  wording with the actual Step 4 PATH B outcome: `SECURITY.md`
  (single-version evidence bullet renamed to "Single-version
  1С evidence (with multi-version scaffolding)" with pointer
  to matrix doc + Track E PATH B context + "no blanket
  multi-version support claim"), `docs/release-handoff.md`
  ("No multi-version 1С smoke matrix" Known limitations
  bullet rewritten as "Multi-version 1С smoke matrix —
  scaffolding only" with pointers and PATH B context;
  Single-version coverage bullet extended with matrix-doc
  pointer), `README.md` (Quickstart paragraph rewritten to
  remove stale "planning-only, Step 1" and broad
  "matrix из нескольких 1С версий" implication; "Куда идти
  дальше" navigation enriched with Track E runbook + matrix
  doc + Track E architecture mentions). Unified support
  statement now consistent across all three docs. Commit
  `78d5956`.
- **Step 6 (final integration pass and Track E closure)** —
  this closure: `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track E closed status. No
  `pyproject.toml` change (Q5 = NO; Track E without
  functional delta does not warrant a minor bump). Read-only
  final integration check green: linear Step 1 → 6 history,
  all Step 1–5 deliverables present on disk, registries
  without drift, `verify-release.ps1` GREEN on 8 checks, no
  real credentials anywhere in the six Track E commits.

#### Registry invariant carried through Track E

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track E.

#### Honest constraints update under Track E closure

- **Reference single-version evidence remains
  single-version.** Track E shipped scaffolding (frozen
  scenario + operator runbook + matrix-table doc) but did
  not extend the actual evidence breadth. The reference
  row in `docs/version-support-matrix.md` covers
  `8.3.27.1859` only; no additional version evidence rows
  were added.
- **No blanket multi-version support claim.** The platform
  remains multi-version-friendly architecturally (operator
  selects the binary path), but evidence-level claims are
  bounded by the reference row and the honest
  operator-supplied gap notation in the matrix doc.
- **`docs/version-support-matrix.md` is the single source
  of truth** for the actual evidence level. Post-closure
  additional evidence rows can be added through
  documentation-only updates against the matrix doc by
  following
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`,
  without re-opening Track E.
- All other 0.2.0 honest constraints (DESIGNER credentials
  remain operator-managed via `${ENV:NAME}` substitution;
  Check 8 is a narrow heuristic, not full DLP) carry
  forward unchanged.
- All 0.1.0 honest constraints (no production-grade MCP
  transport, no installer ecosystem, no full enterprise
  super-set, no hot reload, no full AST parser, no full
  rollback / delete coverage) also carry forward
  unchanged.

### Active work

None. No parallel track is currently open after Track E
closure. Track E was opened and closed within the `0.2.0`
release line as a documentation / scaffolding follow-up,
without a minor version bump (Q5 = NO; no functional delta).
Phase 7 as a linear phase is not planned. Opening the next
parallel track is an explicit operator decision.

## 0.1.0 — initial public snapshot

The first publicly trackable snapshot of the project. The version
matches `pyproject.toml`.

### Closed before 0.1.0

- **Phases 1–6** — read MVP, write MVP, metadata changes, intelligence
  layer, product layer, industrialization & completion track.
  See `PROJECT-STATUS.md` for per-phase detail.
- **Parallel Track A — Full Real 1cv8-backed Write Path** — closed on
  Step 7. Real binary-backed write path
  (`/DumpConfigToFiles` / `/LoadConfigFromFiles` / `/UpdateDBCfg`) is
  proven on a reference stand. See
  `docs/runbooks/track-a-reference-stand-round-trip.md`.
- **Parallel Track B — Productization & Delivery Polish** — closed on
  Step 6 (final integration pass and Track B closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-b-*`.
  - Step 2 (repo hygiene + legal layer) — `git init` on `main`,
    extended `.gitignore`, this `CHANGELOG.md`, `LICENSE`
    (Apache-2.0, full standard text), `SECURITY.md`, first
    meaningful commit.
  - Step 3 (operator-discoverable install fast path) — thin
    PowerShell wrapper `scripts/release/install.ps1` over the
    existing `run_install_fast_path` helper, plus
    `_install_runner.py` and `scripts/release/README.md`.
  - Step 4 (operator/dev local launch umbrella) —
    `scripts/dev/launch.ps1` with `selfcheck` / `repl` / `run` /
    `help` subcommands; updated `scripts/dev/README.md`.
  - Step 5 (root README quickstart and docs polish) — top-level
    `## Quickstart` block in this README with install / check /
    launch commands and a deeper-docs map.
  - Step 6 (final integration pass and Track B closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track B closed status.
- **Parallel Track C — Packaging & Installer Delivery** — closed on
  Step 6 (final integration pass and Track C closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-c-*`.
  - Step 2 (release-facing verify path and layout polish) —
    `scripts/release/verify-release.ps1` as a read-only
    pre-handoff sanity check; updated `scripts/release/README.md`
    for the three-entrypoint surface (`install` / `verify` /
    `launch`).
  - Step 3 (packaging-facing install flow honest review) —
    inline block comment in `pyproject.toml` documenting why
    `[tool.hatch.build.targets.wheel] packages = []` is an
    intentional no-op (multi-app monorepo shape; install via
    `scripts/release/install.ps1`, not `pip install`); short
    "Packaging story" section in `scripts/release/README.md`.
  - Step 4 (release handoff documentation) — new
    `docs/release-handoff.md` for the receive-side operator:
    what you received, system prerequisites, reproducible
    install sequence, verify sequence, honest known
    limitations table.
  - Step 5 (integration and handoff polish) — minimal pointer
    to `docs/release-handoff.md` from the Quickstart "Куда
    идти дальше" navigation in this README.
  - Step 6 (final integration pass and Track C closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track C closed status.

### Registry invariant carried into 0.1.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track A, Track B, or Track C.

### Honest constraints carried into 0.1.0

- DESIGNER credentials remain operator-managed and out-of-band; never
  stored in repository.
- Multi-version 1С smoke matrix not yet exercised — single-version
  evidence on `8.3.27.1859`.
- No production-grade MCP transport, no installer ecosystem
  (`.msi` / `.deb` / GUI wizard / signed distribution), no web-UI,
  no full enterprise super-set (SSO/RBAC, multi-tenant, secrets vault
  as a service, federated audit storage, policy-as-code DSL,
  multi-instance HA).
- No hot reload, no OS-level service supervision, no full AST parser,
  no full rollback/delete coverage.

These are honest constraints, not hidden gaps.

### Active work (at the time of 0.1.0)

None. No parallel track was open at the time of the 0.1.0 release.
**Parallel Track D — Operator Credentials Hardening** was opened
afterwards and closed in 0.2.0; see the 0.2.0 release notes above.
