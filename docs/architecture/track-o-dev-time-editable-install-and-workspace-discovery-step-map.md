# Parallel Track O — Dev-Time Editable Install and Workspace Discovery — Step Map

Companion to
[track-o-dev-time-editable-install-and-workspace-discovery-plan.md](track-o-dev-time-editable-install-and-workspace-discovery-plan.md).
This document defines the six steps of Track O in the
standard format used by Tracks A–N (Goal / What changes /
What does NOT change / Result), plus the track invariants
block, the hard out-of-scope block, and the Step 6 Q7
framing.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track O invariants

These invariants must hold at every step. They are
verifiable from repo state (grep / `git diff` /
`selfcheck.py` / `verify-release.ps1`) at every commit:

1. **Tracks A–N production code byte-identical.**
   `apps/*/src/`, `packages/*/src/`, in particular
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py`,
   `apps/platform/src/onec_platform/runtime.py`,
   `apps/platform/src/onec_platform/process_control.py`,
   `apps/platform/src/onec_platform/runtime_logs.py`,
   `apps/platform/src/onec_platform/models.py` not
   modified by any Track O step. Track O is a dev-time
   boundary track; it does not modify runtime.
2. **Track K diagnostic harness byte-identical.**
   `scripts/dev/mcp_client_smoke.py` not modified at any
   step.
3. **Track J operator recipe byte-identical.**
   `docs/operators/deployment-boundary.md` not modified
   at any step.
4. **Track L operator recipe + systemd template byte-
   identical.** `docs/operators/service/service-supervision.md`
   and `docs/operators/service/mcp-server.service` not
   modified at any step.
5. **Track M operator recipe + wheel-build flip byte-
   identical.** `docs/operators/packaging/distribution-boundary.md`
   not modified at any step. `pyproject.toml`
   `[tool.hatch.build.targets.wheel] packages = [...]`
   11-element array byte-identical.
6. **Track N operator recipe byte-identical.**
   `docs/operators/observability.md` not modified at
   any step.
7. **`pyproject.toml`** byte-identical at Steps 1 / 2 /
   3 / 5. Step 4 MAY modify `pyproject.toml` only if
   Step 3 contract explicitly authorises PATH B and
   names the exact change under the locked LOC cap;
   default expectation: no change. Step 6 MAY further
   modify `pyproject.toml` `version` only if Q7 = PATCH;
   default expectation Q7 = NO-BUMP if Step 4 PATH A.
8. **Registries `read = 15 / write = 25 / intelligence
   = 16`** unchanged across all six steps.
   `selfcheck.py` `status=ok` at every step.
9. **`scripts/dev/selfcheck.py`** byte-identical at
   every step.
10. **`scripts/dev/mcp_client_smoke.py`** byte-
    identical at every step.
11. **`scripts/dev/launch.ps1`,
    `scripts/dev/bootstrap_paths.ps1`,
    `scripts/dev/run_dev_check.ps1`** byte-identical at
    Steps 1 / 2 / 3 / 5 / 6. Step 4 MAY add a new
    sibling file (e.g., `bootstrap_paths.sh` cross-OS
    sibling) only if Step 3 contract explicitly
    authorises PATH B under the Step 4 file-surface
    cap. Default expectation: no new file.
12. **`scripts/dev/README.md`** byte-identical at Steps
    1 / 2 / 3 / 4. Step 5 MAY add narrow CLASS-1
    updates (e.g., replace the line "editable install и
    workspace discovery всё ещё out of scope" with a
    pointer at the new recipe). Default expectation:
    one targeted line replacement, no broader
    rewriting.
13. **`scripts/release/*`** byte-identical at every
    step (`install.ps1`, `verify-release.ps1`,
    `_install_runner.py`, `README.md`).
14. **`SECURITY.md`** byte-identical at every step
    (Track O does not change the security claim).
15. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow CLASS-1
    updates if the "What is in this handoff" / "Where
    to read deeper" lists develop direct factual drift
    after Step 4. Default expectation Step 5 edit: at
    most one new bullet pointing at the Step 4 recipe.
16. **`apps/platform/README.md`** byte-identical at
    every step (Track O does not change the platform-
    layer boundary inventory).
17. **`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    CLASS-1 cross-link in `docs/developer-manual.md`
    only if it develops direct factual drift; default
    expectation: at most one new bullet.
18. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a Track O closure
    entry.
19. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still ends
    at Track N, 14 entries). Only Step 6 extends it
    to 15 entries (A through O).
20. **No new MCP tools** at any step.
21. **No new CLI flag** on any existing MCP server
    entrypoint at any step.
22. **No new `[project.scripts]` console entries.**
23. **No new project dependencies.** Step 4 must not
    add to `[project.dependencies]` or
    `[project.optional-dependencies]`.
24. **No new entrypoint module** in any `apps/*/src/`
    package.
25. **`1c_agent_platform-<VERSION>-py3-none-any.whl`
    artefact class byte-identical** (Track M closure
    state).
26. **CI workflow `.github/workflows/dev-check.yml`**
    byte-identical at Steps 1 / 2 / 3 / 5 / 6. Step 4
    MAY extend the CI workflow only if Step 3 contract
    explicitly authorises PATH B with an editable-
    install verification step under the locked LOC cap.
    Default expectation: no CI change.
27. **`.python-version`** byte-identical at every step
    (Python 3.11 pin preserved).
28. **No `1cv8.exe` runs** at any step.
29. **No real credentials** in any committed text.
30. **No remote push** at any step.
31. **No premature closure language.** Phrases that
    frame Track O as "закрыт" / "closed" / "fully
    solved" / "developer workflow solved forever" /
    "all IDE integrations supported" / "all package
    managers supported for dev install" /
    "containerised dev environment shipped" /
    "remote-dev shipped" / "enterprise developer
    experience" may appear in Steps 1–5 only as
    explicit DENIALS. Only Step 6 introduces closure
    language for Track O itself.

---

## Track O hard out-of-scope (carry through every step)

These categories must not be addressed by Track O at any
step. Each is named explicitly to prevent silent
expansion:

- No new transport family (no WebSocket, no SSE, no
  TCP, no Unix-socket, no named-pipe).
- No auth-scheme redesign.
- No deployment-boundary redesign (Track J invariants
  preserved).
- No service-supervision redesign (Track L invariants
  preserved).
- No packaging redesign (Track M invariants preserved).
- No observability redesign (Track N invariants
  preserved).
- No containerised dev environment — no Dockerfile,
  no `docker-compose.yml`, no `.devcontainer/` bundle.
- No IDE-specific integration — no VSCode `.vscode/`,
  no JetBrains `.idea/`, no Cursor / Zed / Sublime /
  Vim project files.
- No remote-dev workflow — no Codespaces, no GitPod,
  no Coder template.
- No multi-Python-version matrix — Python 3.11 pin
  preserved.
- No formatter / linter / test-runner policy redesign.
  Existing `[tool.ruff]` and `[tool.pytest.ini_options]`
  configuration is operator-side discretion; Track O
  does not mandate or extend it.
- No alternative build-backend evaluation. Hatchling
  remains the build backend.
- No enterprise identity stack.
- No clustering / HA / orchestration platforms.
- No web UI / dashboard frontend.
- No `/healthz` / `/readyz` / `/livez` endpoint
  (Track J §6 defer preserved).
- No new MCP tools / registry change.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new project dependencies.
- No new entrypoint module.
- No `1cv8.exe` runs.
- No remote push.
- No rollback / AST / multi-version 1С matrix
  expansion.
- No installable-from-git-URL story (Q2 (B)
  rejection).
- No "developer workflow solved forever" / "all IDE
  integrations supported" / "all package managers
  supported for dev install" / "containerised dev
  environment shipped" / "remote-dev shipped" /
  "enterprise developer experience" / "production-
  ready DX" / "DX matrix complete" claim.

---

## Step 1 — planning dev-time editable install and workspace discovery

**Goal.** Open Track O formally with a single planning
document and a single step-map document, plus the
narrative flip on README.md and PROJECT-STATUS.md
required to mark Track O as the active parallel track.
Establish the Q1–Q7 directional defaults without locking
final answers.

**What changes.**
- NEW: `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement
  grounded in the explicit `scripts/dev/README.md:5-11`
  out-of-scope sentence; in-scope / out-of-scope;
  guardrails; acceptance criteria; relationship table
  to Tracks G/H/I/J/K/L/M/N; step trajectory).
- NEW: `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-step-map.md`
  (this document — six steps + 31 track invariants
  block + hard out-of-scope carry-through list).
- MODIFIED: `README.md` — Quickstart paragraph
  appended with Track O active-planning wording;
  "Active parallel track" section reopened describing
  Track O at Step 1 planning-only; Closed parallel
  tracks list **unchanged** (still 14 entries A–N).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "Активного шага нет" to "Track O / Step 1 active
  planning"; Track N closure block preserved byte-
  identical beneath; one new per-step section
  "Parallel Track O / Step 1 — planning dev-time
  editable install and workspace discovery (завершён)"
  inserted in the canonical location.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`).
- `pyproject.toml` (`version=0.5.2` preserved;
  wheel-build packages array preserved).
- `scripts/*` — all existing files byte-identical
  (selfcheck.py, verify-release.ps1, install.ps1,
  _install_runner.py, launch.ps1, bootstrap_paths.ps1,
  run_dev_check.ps1, mcp_client_smoke.py,
  scripts/dev/README.md, scripts/release/README.md).
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, manuals (`docs/operator-
  manual.md` / `docs/administrator-manual.md` /
  `docs/developer-manual.md`),
  `docs/operators/deployment-boundary.md` (Track J),
  `docs/operators/service/*` (Track L),
  `docs/operators/packaging/distribution-boundary.md`
  (Track M), `docs/operators/observability.md`
  (Track N), `CHANGELOG.md` — byte-identical.
- All Tracks A–N architecture docs — byte-identical.
- CI workflow `.github/workflows/dev-check.yml` —
  byte-identical.
- Registries `read=15 / write=25 / intelligence=16`.
- README Closed parallel tracks list (still 14
  entries A–N).
- `.python-version` — Python 3.11 pin preserved.
- No `1cv8.exe` runs.
- No real credentials.
- No remote push.
- No Step 2 opening.

**Result.** Track O is formally open at Step 1. The
plan document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file)
fixes the six-step boundary. Contributor can read the
plan and step-map and know exactly what Track O will
and will not do. README and PROJECT-STATUS reflect the
active-track flip. No code change anywhere; no
`pyproject.toml` change; registry invariant carried
through; selfcheck green; `verify-release.ps1` green
on 8 checks.

---

## Step 2 — baseline audit of current dev-time state

**Goal.** Produce a single descriptive (not
prescriptive) audit document inventorying the current
state of dev-time editable install / workspace
discovery / bootstrap surfaces in the repo; classify
the inventory into the standard 4-class breakdown
(already-reusable / adjacent-but-insufficient /
clearly-missing / explicitly-out-of-scope); produce
Q1–Q6 directional resolutions grounded in evidence;
produce a handoff list for Step 3 contract consumption.

**What changes.**
- NEW: `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-baseline-audit.md`
  — single descriptive audit document. Default
  expectation = 8–12 sections, ≤ 1500 lines. Sections
  must cover: inventory of `scripts/dev/*`
  (bootstrap_paths.ps1, launch.ps1,
  run_dev_check.ps1, selfcheck.py, mcp_client_smoke.py,
  README.md); inventory of `pyproject.toml` developer-
  facing surface ([build-system], [project],
  [project.scripts], [tool.hatch.build.targets.wheel],
  [tool.ruff], [tool.pytest.ini_options]); inventory
  of `.python-version`; inventory of CI workflow;
  inventory of developer-facing prose in
  `docs/developer-manual.md`; whole-repo grep for
  dev-vocabulary patterns (`pip install -e`,
  `editable`, `PEP 660`, `bootstrap`, `workspace`,
  `monorepo`, `PYTHONPATH`, `develop`, `develop-
  mode`, `setup.py develop`); inventory of
  `scripts/dev/README.md:5-11` explicit out-of-scope
  sentence; 4-class breakdown; Q1–Q6 directional
  resolutions; Step 3 handoff list (≥ 10 items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`, manuals.
- All existing operator recipes (Track J / L / M / N).
- README and PROJECT-STATUS — Step 2 is the audit
  step.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 2 produces a single descriptive audit
document. No prescriptive language; no MUST / MUST
NOT / SHOULD lock. All "decisions" stay as
directional recommendations to be locked by Step 3
contract.

---

## Step 3 — dev-time editable install / workspace discovery contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY language. Lock Q1–Q7 final
answers (Q7 deferred to Step 6 but framed). Lock Step
4 PATH (A docs-only / B docs + narrow declarative
slice / C docs + bootstrap helper). Lock Step 4 file-
surface cap (default ≤ 3 touched files). Lock Step 4
LOC cap for any code-bearing artefact (default ≤ 200
LOC stdlib-only, no new dependencies). Lock Step 4
forbidden-files list. Lock Step 5 forbidden-files
list. Lock the closure-gate scenario.

**What changes.**
- NEW: `docs/architecture/track-o-dev-time-editable-install-and-workspace-discovery-contract.md`
  — single normative contract document with RFC 2119
  language. Default expectation = 10–14 sections,
  ≤ 1700 lines.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`, manuals.
- All existing operator recipes (Track J / L / M / N).
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 3 closes with the prescriptive
contract in place. Step 4 has a closure-gate
scenario, a file surface, a LOC cap, a forbidden-files
list, and a verification protocol — all locked.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by
shipping the locked Step 4 artefact(s) under the
locked path and cap. Default expectation under PATH A
= one contributor-facing recipe (likely at
`docs/dev/editable-install-and-workspace-discovery.md`
or `docs/contributors/dev-workflow.md` per Step 3
contract path lock). PATH B / PATH C only if Step 3
contract explicitly authorises them and names the
exact file(s).

**What changes (default expectation, PATH A).**
- NEW: contributor-facing dev-time-boundary recipe
  under `docs/dev/` (or whichever path Step 3
  contract locks). Default expectation = 6–12
  sections, ≤ 1000 lines. Sections cover: purpose;
  scope statement (what dev-time boundary ships,
  what does NOT ship); supported dev workflow
  (clone + bootstrap or editable install — Step 3
  contract pins which is first-class); supported
  tooling preconditions (Python 3.11, pip, optional
  editable-install support); workspace discovery
  (which paths are dev-time PYTHONPATH entries,
  reference to wheel-build packages array
  symmetry); cross-OS posture; relationship to
  Track M deploy-time recipe (orthogonal,
  complementary); honest non-goals enumeration;
  contributor-side verification (selfcheck +
  optional smoke).

**What changes (alternative, PATH B — if Step 3
contract authorises).**
- NEW: contributor-facing dev-time-boundary recipe
  (as above).
- MODIFIED: at most one of
  - `pyproject.toml` (narrow declarative addition —
    e.g., a comment block formalising editable-
    install posture, or a `[tool.hatch.build.targets.
    wheel.hooks.*]` editable hint if Step 3 contract
    locks it);
  - `scripts/dev/` (e.g., a new
    `bootstrap_paths.sh` cross-OS sibling; ≤ 100
    LOC stdlib-shell).

**What changes (alternative, PATH C — if Step 3
contract authorises).**
- NEW: contributor-facing dev-time-boundary recipe
  (as above).
- NEW: a single dev-onboarding helper script under
  `scripts/dev/` (≤ 150 LOC stdlib-only or stdlib-
  shell), wrapping install + selfcheck for new
  contributors.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`)
  byte-identical at all four PATH variants.
- `pyproject.toml` `version`; `[project]` metadata;
  `[project.scripts]` entries (locked); `[project.
  dependencies]` (empty); `[tool.hatch.build.targets.
  wheel] packages` array (Track M / Step 4 lock
  preserved).
- All existing operator recipes (Track J / L / M / N)
  byte-identical.
- `scripts/release/*` byte-identical.
- `scripts/dev/selfcheck.py`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/dev/launch.ps1`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/run_dev_check.ps1` byte-identical
  (PATH B may add a new sibling file but does not
  modify existing files).
- `scripts/dev/README.md` byte-identical at Step 4
  (Step 5 may update).
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  README.md, PROJECT-STATUS.md — Step 4 is the
  implementation step; closure-doc updates belong
  to Step 5 / Step 6.
- Track O Step 1 / Step 2 / Step 3 docs byte-
  identical.
- All Tracks A–N architecture docs byte-identical.
- CI workflow `.github/workflows/dev-check.yml`
  byte-identical (unless Step 3 contract explicitly
  authorises a PATH B editable-install
  verification CI step, which is not the default
  expectation).
- `.python-version` byte-identical (Python 3.11 pin
  preserved).
- Registries.
- No new MCP tools.
- No new CLI flag.
- No new dependencies.
- No new entrypoint module.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Step 4 ships the locked artefact(s).
Track O's dev-time boundary is now contributor-
readable end-to-end. Production code byte-identical to
Track N closure state (default PATH A) OR narrowly
modified under the locked LOC cap (PATH B/C).
Registry invariant carried through. `selfcheck.py`
green. `verify-release.ps1` green on 8 checks.

---

## Step 5 — docs / operator / release alignment

**Goal.** Bring narrow CLASS-1 alignment edits to
README / PROJECT-STATUS / possibly
`docs/release-handoff.md` / possibly
`docs/developer-manual.md` / possibly
`scripts/dev/README.md` so that contributor- and
operator-facing narrative reflects the Step 4
reality without introducing new code, new declared
surface, or new dependencies. Step 5 is a docs-only
step.

**What changes.**
- POSSIBLY MODIFIED: `README.md` — narrow CLASS-1
  wording updates only (e.g., Quickstart paragraph
  hint that Track O dev-time recipe exists; "Active
  parallel track" section updated to reflect Step 5
  progress). Closed parallel tracks list
  **unchanged** (still 14 entries A–N).
- POSSIBLY MODIFIED: `PROJECT-STATUS.md` — one new
  per-step section "Parallel Track O / Step 5 —
  docs / operator / release alignment (завершён)"
  inserted in the canonical location.
- POSSIBLY MODIFIED: `docs/release-handoff.md` — at
  most one new bullet pointing at the Step 4 recipe
  in the "Where to read deeper" list.
- POSSIBLY MODIFIED: `docs/developer-manual.md` —
  at most one new cross-link if the developer-
  manual content develops direct factual drift from
  Step 4 recipe content.
- POSSIBLY MODIFIED: `scripts/dev/README.md` — at
  most one targeted line replacement of the
  "editable install и workspace discovery всё ещё
  out of scope" sentence with a pointer at the new
  recipe.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/dev/*.ps1` / `scripts/dev/*.py` (only
  `scripts/dev/README.md` may be narrowly updated).
- `SECURITY.md` byte-identical.
- All existing operator recipes (Track J / L / M / N)
  byte-identical.
- `docs/operators/observability.md` (Track N) byte-
  identical.
- Track O Step 4 recipe byte-identical (Step 4
  deliverable immutable).
- All Tracks A–N architecture docs byte-identical.
- Track O Step 1 / Step 2 / Step 3 / Step 4 docs
  byte-identical.
- `CHANGELOG.md` byte-identical.
- README Closed parallel tracks list (still 14
  entries A–N).
- Registries.
- CI workflow byte-identical.
- `.python-version` byte-identical.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Contributor- and operator-facing
narrative aligned with post-Step-4 reality. No code
change. No new declared surface. Track O still **not**
closed (Step 6 remaining).

---

## Step 6 — final integration pass and track closure

**Goal.** Land the final integration pass that
explicitly closes Track O. Update README Closed
parallel tracks list from 14 entries to 15 (A through
O). Add Track O closure narrative to PROJECT-STATUS.
Append Track O closure entry to CHANGELOG.md. Lock Q7
(NO-BUMP if Step 4 = PATH A; PATCH if Step 4 = PATH
B/C with an honest defect-class declarative repair
closing the explicit `scripts/dev/README.md:5-11`
out-of-scope sentence). Carry every Tracks A–N
invariant byte-identical.

**Q7 framing for closure step:**

- **NO-BUMP** (default expectation under PATH A):
  Track O closes under existing `0.5.2` without
  `pyproject.toml [project] version` change. Mirrors
  Track J / Track K / Track L / Track N NO-BUMP
  precedents. PATH A is pure docs-only contributor-
  facing recipe; no production code, no
  pyproject.toml, no scripts logic, no new declared
  surface — Q7 = NO-BUMP is the only honest outcome.
- **PATCH `0.5.2 → 0.5.3`** (acceptable only if Step
  4 = PATH B with a narrow declarative defect-class
  repair, e.g., a `pyproject.toml` comment block
  formalising editable-install posture or a
  `scripts/dev/bootstrap_paths.sh` cross-OS sibling
  that closes the `scripts/dev/README.md:5-11`
  out-of-scope sentence). Mirrors Track I PATCH
  (`installer.py:_config_to_dict` +15 LOC) and Track
  M PATCH (`pyproject.toml` packages flip +7 LOC)
  defect-class declarative-repair precedents.
- **MINOR** explicitly prohibited by guardrails §21
  (no new CLI flag on existing servers), §22 (no
  new `[project.scripts]` entry), §23 (no new
  dependencies); no new declared external capability
  warrants MINOR.
- **MAJOR** forbidden by track scope.

**What changes.**
- MODIFIED: `README.md` — Closed parallel tracks
  list extended from 14 to 15 entries (Track O added
  at the bottom); "Active parallel track" section
  flipped back to "Активного parallel track'а
  сейчас нет"; Quickstart paragraph updated to
  reflect Track O closure; "Track O detail
  (закрыт)" section added above "Track N detail
  (закрыт)" (mirror of existing Tracks A–N detail
  sections in length and shape).
- MODIFIED: `PROJECT-STATUS.md` — header flipped
  from "Track O / Step <previous>" to "Активного
  шага нет"; Track O closure narrative added
  beneath top-of-status; six per-step sections for
  Track O finalised.
- MODIFIED: `CHANGELOG.md` — one Track O closure
  entry appended (mirror of Track A–N closure
  entries in shape); under existing `0.5.2`
  section if Q7 = NO-BUMP (with explicit "closed
  under existing 0.5.2, no further bump" framing
  mirroring Track J/K/L/N precedent under 0.5.1
  and 0.5.2); under a new `0.5.3` section if Q7 =
  PATCH.
- POSSIBLY MODIFIED: `pyproject.toml` — `version`
  bumped from `0.5.2` to `0.5.3` only if Q7 =
  PATCH; other fields byte-identical.

**What does NOT change.**
- All production code (`apps/*/src/`,
  `packages/*/src/`) byte-identical to Step 4
  state.
- `scripts/*` byte-identical to Step 4 state.
- `SECURITY.md` byte-identical.
- All existing operator recipes (Track J / L / M / N)
  byte-identical.
- Track O Step 4 recipe byte-identical.
- All Tracks A–N architecture docs byte-identical.
- Track O Step 1 / Step 2 / Step 3 / Step 4 / Step 5
  docs byte-identical.
- `docs/release-handoff.md` byte-identical to Step 5
  state.
- `apps/platform/README.md` byte-identical to Step 5
  state.
- Manuals byte-identical to Step 5 state.
- CI workflow byte-identical to Step 4 state.
- `.python-version` byte-identical.
- Registries.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Track O closed. Fifteen post-phase
parallel tracks (A through O) closed sequentially.
README Closed parallel tracks list updated. Q7
locked. Contributor- and operator-facing narrative
reflects Track O closure. Selfcheck green; verify-
release.ps1 green on 8 checks; no real credentials;
no `1cv8.exe`; no remote push.
