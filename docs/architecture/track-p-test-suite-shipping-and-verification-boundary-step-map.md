# Parallel Track P — Test Suite Shipping and Verification Boundary — Step Map

Companion to
[track-p-test-suite-shipping-and-verification-boundary-plan.md](track-p-test-suite-shipping-and-verification-boundary-plan.md).
This document defines the six steps of Track P in the
standard format used by Tracks A–O (Goal / What changes /
What does NOT change / Result), plus the track invariants
block, the hard out-of-scope block, and the Step 6 Q7
framing.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track P invariants

These invariants must hold at every step. They are
verifiable from repo state (grep / `git diff` /
`selfcheck.py` / `verify-release.ps1`) at every commit:

1. **Tracks A–O production code byte-identical.**
   `apps/*/src/`, `packages/*/src/`, in particular
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py`,
   `apps/platform/src/onec_platform/runtime.py`,
   `apps/platform/src/onec_platform/process_control.py`,
   `apps/platform/src/onec_platform/runtime_logs.py`,
   `apps/platform/src/onec_platform/models.py` not
   modified by Steps 1 / 2 / 3 / 5 / 6. Step 4 MAY
   modify production code only if Step 3 contract
   explicitly authorises a narrow code change for
   testability and names the exact file under the
   locked LOC cap. Default expectation: zero
   production code change across all six Track P
   steps.
2. **Track K diagnostic harness byte-identical.**
   `scripts/dev/mcp_client_smoke.py` not modified at
   any step.
3. **Track J operator recipe byte-identical.**
   `docs/operators/deployment-boundary.md` not
   modified at any step.
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
7. **Track O contributor recipe byte-identical.**
   `docs/dev/editable-install-and-workspace-discovery.md`
   not modified at any step.
8. **`pyproject.toml`** byte-identical at Steps 1 / 2
   / 3 / 5. Step 4 MAY modify `pyproject.toml` only
   if Step 3 contract explicitly authorises PATH B/C
   with a narrow `[project.optional-dependencies]
   test = ["pytest"]` (or equivalent) block addition;
   the `[project]`, `[project.scripts]`,
   `[tool.ruff]`, `[tool.pytest.ini_options]`,
   `[tool.hatch.build.targets.wheel]` blocks remain
   byte-identical. Step 6 MAY further modify
   `pyproject.toml` `version` only if Q7 = PATCH;
   default expectation Q7 = NO-BUMP if Step 4 PATH A;
   Q7 = PATCH most likely if Step 4 PATH B.
9. **Registries `read = 15 / write = 25 / intelligence
   = 16`** unchanged across all six steps.
   `selfcheck.py` `status=ok` at every step.
10. **`scripts/dev/selfcheck.py`** byte-identical at
    every step.
11. **`scripts/dev/launch.ps1`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY narrowly replace
    the two "no test suite yet" / "no pytest yet"
    prose sentences (lines 28 + 86 verbatim
    references) with a pointer at the new Track P
    recipe; no logic change. Default expectation
    Step 5 edit: ≤ 5 lines of prose touched.
12. **`scripts/dev/bootstrap_paths.ps1`,
    `scripts/dev/run_dev_check.ps1`** byte-identical
    at every step.
13. **`scripts/release/install.ps1`,
    `scripts/release/verify-release.ps1`,
    `scripts/release/_install_runner.py`,
    `scripts/release/README.md`** byte-identical at
    every step.
14. **`scripts/dev/README.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    pointer.
15. **`SECURITY.md`** byte-identical at every step.
16. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    CLASS-1 updates.
17. **`apps/platform/README.md`** byte-identical at
    every step.
18. **`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    cross-link in `docs/developer-manual.md` only.
19. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still 15
    entries A–O). Only Step 6 extends it to 16
    entries.
20. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a Track P closure
    entry.
21. **`.github/workflows/dev-check.yml`** byte-
    identical at Steps 1 / 2 / 3 / 5 / 6. Step 4
    MAY extend the workflow file only if Step 3
    contract explicitly authorises PATH B/C with a
    pytest-invocation step (≤ 5 lines of YAML
    addition).
22. **`.python-version`** byte-identical at every
    step (Python 3.11 pin preserved).
23. **No new MCP tools** at any step.
24. **No new CLI flag** on any existing MCP server
    entrypoint at any step.
25. **No new `[project.scripts]` console entries.**
26. **No new project dependencies in
    `[project.dependencies]`.** Step 4 MAY add to
    `[project.optional-dependencies]` only if Step 3
    contract authorises PATH B/C; default expectation
    a single `test = ["pytest"]` (or equivalent
    narrow) block.
27. **No new entrypoint module.**
28. **`1c_agent_platform-<VERSION>-py3-none-any.whl`
    artefact class byte-identical** (Track M closure
    state).
29. **No `1cv8.exe` runs** at any step. Tests MUST
    NOT invoke `1cv8.exe`.
30. **No outbound network** in any committed test.
    In-process / stdlib / localhost only.
31. **No real credentials** in any committed text.
32. **No remote push** at any step.
33. **No premature closure language.** Phrases that
    frame Track P as "закрыт" / "closed" / "fully
    solved" / "testing solved forever" / "full QA
    stack shipped" / "complete confidence matrix" /
    "production-grade certification" / "enterprise
    test infrastructure" / "100% coverage achieved" /
    "all behaviours covered" may appear in Steps 1–5
    only as explicit DENIALS. Only Step 6 introduces
    closure language for Track P itself.

---

## Track P hard out-of-scope (carry through every step)

These categories must not be addressed by Track P at any
step. Each is named explicitly to prevent silent
expansion:

- No performance benchmarking (no `pytest-benchmark`,
  no `timeit` regression).
- No load testing (no `locust`, no `wrk`, no JMeter).
- No stress testing.
- No fuzzing (no `hypothesis`, no `atheris`).
- No browser / UI tests (no Selenium, no Playwright,
  no Cypress).
- No web dashboard testing.
- No real `1cv8.exe` execution.
- No external SaaS / live-network integration.
- No multi-Python-version matrix.
- No containerised CI lab.
- No snapshot / golden approval framework.
- No mutation testing.
- No coverage-gate absolutism.
- No rewriting verification philosophy of selfcheck /
  verify-release / smoke harness — three existing
  gates remain byte-identical.
- No transport / auth / deployment / service /
  packaging / observability / dev-time recipe
  redesign.
- No new MCP tools / registry change.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new entrypoint module.
- No `1cv8.exe` runs.
- No remote push.
- No "testing solved forever" / "full QA stack
  shipped" / "complete confidence matrix" /
  "production-grade certification" / "enterprise test
  infrastructure" / "100% coverage achieved" / "all
  behaviours covered" claim.

---

## Step 1 — planning test suite shipping and verification boundary

**Goal.** Open Track P formally with a single planning
document and a single step-map document, plus the
narrative flip on README.md and PROJECT-STATUS.md
required to mark Track P as the active parallel track.
Establish the Q1–Q7 directional defaults without
locking final answers.

**What changes.**
- NEW: `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement grounded
  in `pyproject.toml:31-32` + `scripts/dev/launch.ps1`
  "no test suite yet" anchors; in-scope / out-of-
  scope; guardrails; acceptance criteria;
  relationship table to Tracks K/N/O; step
  trajectory).
- NEW: `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-step-map.md`
  (this document — six steps + 33 track invariants
  block + hard out-of-scope carry-through list +
  Step 6 Q7 framing).
- MODIFIED: `README.md` — Quickstart paragraph
  appended with Track P active-planning wording;
  "Active parallel track" section reopened
  describing Track P at Step 1 planning-only; Closed
  parallel tracks list **unchanged** (still 15
  entries A–O).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "Активного шага нет" to "Track P / Step 1 active
  planning"; Track O closure block preserved byte-
  identical beneath; one new per-step section
  "Parallel Track P / Step 1 — planning test suite
  shipping and verification boundary (завершён)"
  inserted in the canonical location.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`).
- `pyproject.toml` (`version=0.5.2` preserved;
  packages array, `[tool.pytest.ini_options]`,
  `[tool.ruff]`, `[project.scripts]`,
  `[project.dependencies]` all byte-identical).
- `scripts/*` — all existing files byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, manuals,
  `docs/operators/*` (Tracks J/L/M/N recipes),
  `docs/dev/editable-install-and-workspace-discovery.md`
  (Track O recipe), `CHANGELOG.md` — byte-identical.
- All Tracks A–O architecture docs — byte-identical.
- CI workflow `.github/workflows/dev-check.yml` —
  byte-identical.
- Registries `read=15 / write=25 / intelligence=16`.
- README Closed parallel tracks list (still 15
  entries A–O).
- `.python-version` — Python 3.11 pin preserved.
- No `1cv8.exe` runs.
- No real credentials.
- No remote push.
- No Step 2 opening.

**Result.** Track P is formally open at Step 1. The
plan document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file)
fixes the six-step boundary. Contributor can read the
plan and step-map and know exactly what Track P will
and will not do. README and PROJECT-STATUS reflect
the active-track flip. No code change anywhere; no
`pyproject.toml` change; registry invariant carried
through; selfcheck green; `verify-release.ps1` green
on 8 checks.

---

## Step 2 — baseline audit of current verification state

**Goal.** Produce a single descriptive (not
prescriptive) audit document inventorying the current
state of verification surfaces in the repo (the three
existing gates + the aspirational `testpaths`
declaration + the two `launch.ps1` hand-off-marker
anchors); classify the inventory into the standard
4-class breakdown (already-reusable / adjacent-but-
insufficient / clearly-missing / explicitly-out-of-
scope); produce Q1–Q6 directional resolutions
grounded in evidence; produce a handoff list for
Step 3 contract consumption.

**What changes.**
- NEW: `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-baseline-audit.md`
  — single descriptive audit document. Default
  expectation = 8–12 sections, ≤ 1500 lines.
  Sections must cover: inventory of `selfcheck.py`
  (output shape, exit codes, what it asserts);
  inventory of `verify-release.ps1` (8 named checks,
  PASS/FAIL/SKIP/WARN format, exit codes);
  inventory of `mcp_client_smoke.py` (the one
  round-trip scenario per server per transport);
  inventory of `_install_runner.py` (structured
  findings output); inventory of CI workflow (only
  selfcheck invocation); inventory of
  `pyproject.toml` test-related blocks
  (`[tool.pytest.ini_options]` aspirational
  declaration; absent `[project.optional-
  dependencies]`); inventory of
  `scripts/dev/launch.ps1` "no test suite yet"
  anchors; inventory of `tests/` directory non-
  existence; whole-repo grep for test-vocabulary
  patterns (`pytest`, `test_`, `_test.py`,
  `conftest`, `tox`, `nox`, `unittest`,
  `coverage`, `cov`, `assert`); 4-class breakdown;
  Q1–Q6 directional resolutions; Step 3 handoff
  list (≥ 10 items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  manuals, existing operator recipes (Track J/L/M/N),
  Track O dev recipe.
- README and PROJECT-STATUS — Step 2 is the audit
  step.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 2 produces a single descriptive
audit document. No prescriptive language; no MUST /
MUST NOT / SHOULD lock. All "decisions" stay as
directional recommendations to be locked by Step 3
contract.

---

## Step 3 — test suite shipping and verification boundary contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY language. Lock Q1–Q7 final
answers (Q7 deferred to Step 6 but framed). Lock
Step 4 PATH (A docs-only / B docs + narrow tests
slice / C docs + non-production helper). Lock Step 4
file-surface cap (default ≤ 4 touched files). Lock
Step 4 LOC cap for any tests slice (default ≤ 300
LOC stdlib + pytest only). Lock Step 4 forbidden-
files list. Lock Step 5 forbidden-files list. Lock
the closure-gate scenario.

**What changes.**
- NEW: `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-contract.md`
  — single normative contract document with RFC 2119
  language. Default expectation = 10–14 sections,
  ≤ 1700 lines.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  manuals, existing operator recipes (Track J/L/M/N),
  Track O dev recipe.
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 3 closes with the prescriptive
contract in place. Step 4 has a closure-gate
scenario, a file surface, a LOC cap, a forbidden-
files list, and a verification protocol — all
locked.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by
shipping the locked Step 4 artefact(s) under the
locked path and cap. Default expectation (per Step
1 plan Q3 directional default) = PATH B (recipe +
narrow `tests/` slice + narrow pyproject dev-extra
declaration). PATH A (docs-only) acceptable
fallback if Step 2/3 audit reveals materialising
even a narrow tests slice expands scope. PATH C
(non-production helper alone) rejected by default.

**What changes (default expectation, PATH B).**
- NEW: contributor-facing test-suite-boundary
  recipe under `docs/dev/` (e.g.,
  `docs/dev/test-suite-and-verification.md` or
  whichever path Step 3 contract locks). Default
  expectation = 6–10 sections, ≤ 800 lines.
- NEW: `tests/__init__.py` — empty marker file or
  short module docstring; no executable logic.
- NEW: `tests/test_*.py` — one narrow test file
  (≤ 300 LOC) exercising already-existing
  behaviour on pure-function / pure-class boundary.
- MODIFIED: `pyproject.toml` — narrow addition of
  `[project.optional-dependencies]` block with
  `test = ["pytest"]` (or equivalent narrow
  declaration). All other `pyproject.toml` blocks
  byte-identical.

**What changes (alternative, PATH A — if Step 3
contract authorises).**
- NEW: contributor-facing test-suite-boundary recipe
  only.
- `pyproject.toml` `[tool.pytest.ini_options]`
  `testpaths = ["tests"]` either left as-is with
  prose pointing at the recipe, or honestly removed
  by Step 4 (TBD by contract).

**What changes (alternative, PATH C — if Step 3
contract authorises).**
- NEW: contributor-facing recipe.
- NEW: `tests/conftest.py` — non-production helper
  for shared fixtures only; no actual tests.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`)
  byte-identical at all PATH variants.
- `pyproject.toml` `version`; `[project]` metadata;
  `[project.scripts]` entries; `[project.dependencies]`
  (empty); `[tool.hatch.build.targets.wheel] packages`
  array (Track M / Step 4 lock preserved);
  `[tool.ruff]`; `[tool.pytest.ini_options]
  testpaths` (preserved at PATH B/C; possibly
  honestly removed at PATH A).
- All existing operator recipes (Track J/L/M/N) byte-
  identical.
- Track O dev recipe byte-identical.
- `scripts/dev/selfcheck.py`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/dev/launch.ps1`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/run_dev_check.ps1`,
  `scripts/dev/README.md` byte-identical at Step 4.
- `scripts/release/*` byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  README.md, PROJECT-STATUS.md — Step 4 is the
  implementation step; closure-doc updates belong
  to Step 5 / Step 6.
- Track P Step 1 / Step 2 / Step 3 docs byte-
  identical.
- All Tracks A–O architecture docs byte-identical.
- CI workflow `.github/workflows/dev-check.yml`
  byte-identical (unless Step 3 contract explicitly
  authorises PATH B/C extension with a pytest-
  invocation step).
- `.python-version` byte-identical.
- Registries.
- No new MCP tools.
- No new CLI flag.
- No new `[project.scripts]` console entries.
- No new entrypoint module.
- No new `[project.dependencies]` entries (only
  `[project.optional-dependencies]` MAY be added at
  PATH B/C).
- No `1cv8.exe` runs.
- No outbound network in any committed test.
- No remote push.

**Result.** Step 4 ships the locked artefact(s).
Track P's test-suite boundary is now contributor-
readable end-to-end. Production code byte-identical
to Track O closure state. Registry invariant carried
through. `selfcheck.py` green. `verify-release.ps1`
green on 8 checks.

---

## Step 5 — docs / operator / release alignment

**Goal.** Bring narrow CLASS-1 alignment edits to
README / PROJECT-STATUS / possibly
`docs/release-handoff.md` / possibly
`docs/developer-manual.md` / possibly
`scripts/dev/launch.ps1` "no pytest yet" prose
narrow replacement / possibly `scripts/dev/README.md`
so that contributor- and operator-facing narrative
reflects the Step 4 reality without introducing new
code, new declared surface, or new dependencies.
Step 5 is a docs-only step.

**What changes.**
- POSSIBLY MODIFIED: `README.md` — narrow CLASS-1
  wording updates only. Closed parallel tracks list
  **unchanged** (still 15 entries A–O).
- POSSIBLY MODIFIED: `PROJECT-STATUS.md` — one new
  per-step section "Parallel Track P / Step 5 —
  docs / operator / release alignment (завершён)".
- POSSIBLY MODIFIED: `docs/release-handoff.md` —
  at most one new bullet pointing at the Step 4
  recipe.
- POSSIBLY MODIFIED: `docs/developer-manual.md` —
  at most one new cross-link if its prose develops
  factual drift.
- POSSIBLY MODIFIED: `scripts/dev/launch.ps1` —
  narrow line-replacement of the two "no test
  suite yet" / "no pytest yet" prose sentences
  (lines 28 + 86) with a pointer at the Step 4
  recipe; no logic change.
- POSSIBLY MODIFIED: `scripts/dev/README.md` — at
  most one new pointer.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- `scripts/dev/selfcheck.py`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/run_dev_check.ps1` byte-identical.
- `scripts/release/*` byte-identical.
- `SECURITY.md` byte-identical.
- All existing operator recipes (Track J/L/M/N) byte-
  identical.
- Track O dev recipe byte-identical.
- Track P Step 4 recipe byte-identical (Step 4
  deliverable immutable).
- All Tracks A–O architecture docs byte-identical.
- Track P Step 1 / Step 2 / Step 3 / Step 4 docs
  byte-identical.
- `CHANGELOG.md` byte-identical.
- README Closed parallel tracks list (still 15
  entries A–O).
- Registries.
- CI workflow byte-identical (unless Step 4
  extended it).
- `.python-version` byte-identical.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Contributor- and operator-facing
narrative aligned with post-Step-4 reality. No code
change beyond Step 4. No new declared surface.
Track P still **not** closed (Step 6 remaining).

---

## Step 6 — final integration pass and track closure

**Goal.** Land the final integration pass that
explicitly closes Track P. Update README Closed
parallel tracks list from 15 entries to 16 (A
through P). Add Track P closure narrative to
PROJECT-STATUS. Append Track P closure entry to
CHANGELOG.md. Lock Q7 (NO-BUMP if Step 4 = PATH A;
PATCH if Step 4 = PATH B with honest defect-class
declarative repair closing the long-standing
aspirational `[tool.pytest.ini_options]
testpaths = ["tests"]` declaration). Carry every
Tracks A–O invariant byte-identical.

**Q7 framing for closure step:**

- **NO-BUMP** (default expectation under PATH A):
  Track P closes under existing `0.5.2` without
  `pyproject.toml [project] version` change.
  Mirrors Track J / Track K / Track L / Track N /
  Track O NO-BUMP precedents. PATH A is pure docs-
  only contributor-facing recipe; no production
  code, no `pyproject.toml`, no `scripts/*` logic,
  no new declared surface — Q7 = NO-BUMP is the
  only honest outcome.
- **PATCH `0.5.2 → 0.5.3`** (most likely outcome
  under PATH B): Track P closes with a PATCH bump
  if Step 4 = PATH B materialises the aspirational
  `[tool.pytest.ini_options] testpaths = ["tests"]`
  declaration (committing `tests/__init__.py` +
  one `test_*.py` slice + adding `[project.optional-
  dependencies] test = ["pytest"]` block).
  Mirrors Track I PATCH (`installer.py:_config_to_dict`
  +15 LOC defect-class round-trip fix making the
  declared `auth.tokens` round-trip actually
  preserved) and Track M PATCH (`pyproject.toml`
  packages flip +7 LOC defect-class repair making
  the declared `[project.scripts]` console
  entries actually installable). Track P PATH B
  closes the long-standing aspirational
  `testpaths = ["tests"]` declaration via
  materialisation — declared-but-empty surface →
  declared-and-shipped = PATCH territory.
- **MINOR** explicitly prohibited by guardrails (no
  new CLI flag, no new declared external
  capability, no new `[project.scripts]` entry, no
  new runtime dependency).
- **MAJOR** forbidden by track scope.

**What changes.**
- MODIFIED: `README.md` — Closed parallel tracks
  list extended from 15 to 16 entries (Track P
  added at the bottom); "Active parallel track"
  section flipped back to "Активного parallel
  track'а сейчас нет"; Quickstart paragraph updated
  to reflect Track P closure; "Track P detail
  (закрыт)" section added above "Track O detail
  (закрыт)" (mirror of existing Tracks A–O detail
  sections in length and shape).
- MODIFIED: `PROJECT-STATUS.md` — header flipped
  from "Track P / Step <previous>" to "Активного
  шага нет"; Track P closure narrative added
  beneath top-of-status; six per-step sections for
  Track P finalised.
- MODIFIED: `CHANGELOG.md` — Track P closure entry
  appended. If Q7 = NO-BUMP, appended as a sub-
  section under existing `0.5.2` heading
  (mirroring Track N / Track O closure under same
  release line). If Q7 = PATCH, created as a new
  top-level `## 0.5.3` heading with grounded
  PATCH-bump justification.
- POSSIBLY MODIFIED: `pyproject.toml` — `version`
  bumped from `0.5.2` to `0.5.3` only if Q7 =
  PATCH; other fields byte-identical.

**What does NOT change.**
- All production code (`apps/*/src/`,
  `packages/*/src/`) byte-identical to Step 4
  state.
- `scripts/*` byte-identical to Step 4 / Step 5
  state.
- `SECURITY.md` byte-identical.
- All existing operator recipes (Track J/L/M/N)
  byte-identical.
- Track O dev recipe byte-identical.
- Track P Step 4 recipe + (if PATH B) `tests/`
  slice byte-identical.
- All Tracks A–O architecture docs byte-identical.
- Track P Step 1 / Step 2 / Step 3 / Step 4 / Step 5
  docs byte-identical.
- `docs/release-handoff.md` byte-identical to
  Step 5 state.
- `apps/platform/README.md` byte-identical to
  Step 5 state.
- Manuals byte-identical to Step 5 state.
- CI workflow byte-identical to Step 4 state.
- `.python-version` byte-identical.
- Registries.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new runtime dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Track P closed. Sixteen post-phase
parallel tracks (A through P) closed sequentially.
README Closed parallel tracks list updated. Q7
locked. Contributor- and operator-facing narrative
reflects Track P closure. Selfcheck green; verify-
release.ps1 green on 8 checks; no real credentials;
no `1cv8.exe`; no remote push.
