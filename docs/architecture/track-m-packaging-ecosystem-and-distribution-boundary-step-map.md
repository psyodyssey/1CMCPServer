# Parallel Track M — Packaging Ecosystem and Distribution Boundary — Step Map

Companion to
[track-m-packaging-ecosystem-and-distribution-boundary-plan.md](track-m-packaging-ecosystem-and-distribution-boundary-plan.md).
This document defines the six steps of Track M in the
standard format used by Tracks A–L (Goal / What changes /
What does NOT change / Result), plus the track invariants
block and the hard out-of-scope block.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track M invariants

These invariants must hold at every step. They are
verifiable from repo state (grep / `git diff` /
`selfcheck.py` / `verify-release.ps1`) at every commit:

1. **Tracks A–L production code byte-identical.**
   `apps/*/src/`, `packages/*/src/`, in particular
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py`,
   `apps/platform/src/onec_platform/runtime.py`,
   `apps/platform/src/onec_platform/process_control.py`,
   `apps/platform/src/onec_platform/runtime_logs.py`,
   `apps/platform/src/onec_platform/models.py` not modified
   by any Track M step. Track M is a packaging /
   distribution track; it does not modify production
   runtime.
2. **Track K diagnostic harness byte-identical.**
   `scripts/dev/mcp_client_smoke.py` not modified at any
   step.
3. **Track J operator recipe byte-identical.**
   `docs/operators/deployment-boundary.md` not modified at
   any step.
4. **Track L operator recipe + systemd template byte-
   identical.** `docs/operators/service/service-supervision.md`
   and `docs/operators/service/mcp-server.service` not
   modified at any step.
5. **`pyproject.toml`** byte-identical at Steps 1 / 2 / 3 /
   5. Step 4 MAY modify `pyproject.toml` only if Step 3
   contract explicitly authorises PATH B (declarative
   build-configuration change); the default-expectation
   change is a single narrow flip of
   `[tool.hatch.build.targets.wheel] packages = []` to a
   populated list plus an accompanying update to the
   24-line comment block. Step 6 MAY further modify
   `pyproject.toml` `version` only if Q7 = PATCH or MINOR;
   default expectation Q7 = NO-BUMP if Step 4 PATH A;
   Q7 = PATCH most likely if Step 4 PATH B.
6. **Registries `read = 15 / write = 25 / intelligence =
   16`** unchanged across all six steps. `selfcheck.py`
   `status=ok` at every step.
7. **`scripts/dev/selfcheck.py`** byte-identical at every
   step.
8. **`scripts/release/install.ps1`**,
   **`scripts/release/verify-release.ps1`**,
   **`scripts/release/_install_runner.py`**,
   **`scripts/dev/bootstrap_paths.ps1`**,
   **`scripts/dev/launch.ps1`**,
   **`scripts/dev/run_dev_check.ps1`**,
   **`scripts/dev/README.md`** byte-identical at Steps
   1 / 2 / 3 / 5 / 6. Step 4 MAY add a new sibling file
   under `scripts/release/` only if Step 3 contract
   explicitly authorises it under the Step 4 file-surface
   cap. Default expectation: no new script.
9. **`scripts/release/README.md`** byte-identical at Steps
   1 / 2 / 3 / 4. Step 5 MAY add at most one narrow
   cross-link bullet if Step 4 ships an artefact that
   meaningfully interacts with the install / verify-release
   surface; default expectation = no edit.
10. **`SECURITY.md`** byte-identical at every step (Track M
    does not change the security claim).
11. **`docs/release-handoff.md`** byte-identical at Steps
    1 / 2 / 3 / 4. Step 5 MAY add narrow CLASS-1 updates
    if the "What is in this handoff" / "What is NOT in
    this handoff" / "Where to read deeper" lists develop
    direct factual drift after Step 4. Most likely Step 5
    edit: a new bullet pointing at the Step 4 recipe and a
    rewrite of the existing "No wheel-based install" line
    in "What is NOT in this handoff" if Step 4 = PATH B
    ships a buildable wheel.
12. **`apps/platform/README.md`** byte-identical at every
    step (Track M does not change the platform-layer
    boundary inventory).
13. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still ends at
    Track L, twelve entries). Only Step 6 extends it to
    thirteen entries (A through M).
14. **No new MCP tools** at any step.
15. **No new CLI flag** on any existing MCP server
    entrypoint at any step. The Track G / Track H flag
    surface (`--transport`, `--config-path`,
    `--log-level`, `--bind`, `--auth-token-env`) is locked.
16. **No new `[project.scripts]` console entries.** The
    three existing entries (`mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`) are
    locked. Step 4 PATH B may make them **actually
    installable** by flipping the wheel-build to non-
    empty, but the entries themselves are not modified.
17. **No new dependencies.** Step 4 must not add to
    `[project.dependencies]` or
    `[project.optional-dependencies]`. The stdlib-only
    orientation of `mcp_common` and the three servers
    is preserved.
18. **No `1cv8.exe` runs** at any step.
19. **No real credentials** in any committed text.
20. **No remote push** at any step.
21. **No premature closure language.** Phrases that frame
    Track M as "закрыт" / "closed" / "fully solved" /
    "packaging solved forever" / "PyPI release ready" /
    "signed binary distribution" / "all package managers
    supported" / "production-ready packaging" /
    "enterprise-ready packaging" may appear in Steps 1–5
    only as explicit DENIALS. Only Step 6 introduces
    closure language for Track M itself.

---

## Track M hard out-of-scope (carry through every step)

These categories must not be addressed by Track M at any
step. Each is named explicitly to prevent silent expansion:

- No new transport family.
- No auth-scheme redesign (no JWT, no OAuth, no OIDC, no
  SAML, no SCIM, no RBAC, no ABAC, no per-tool ACL, no
  per-tenant isolation, no multi-tenant).
- No deployment-boundary redesign (Track J invariants
  preserved).
- No service-supervision redesign (Track L invariants
  preserved).
- No multiple-package-manager publication — no PyPI, no
  Chocolatey, no Homebrew, no apt repository, no rpm
  repository, no conda-forge, no NuGet — even if Step 4
  ships a single wheel.
- No OS-native package formats — no `.msi`, no `.deb`, no
  `.rpm`, no `.dmg`, no `.pkg`, no `.apk`, no `.snap`,
  no `.flatpak`.
- No signed distribution chain — no signing keys, no
  `cosign` / `sigstore` / Authenticode / Notarisation /
  SBOM / SLSA attestation.
- No GUI installer / wizard / setup.exe.
- No enterprise identity stack.
- No clustering / HA / load balancing / orchestration
  platforms (no Kubernetes, no Compose-with-replicas, no
  Nomad, no Consul, no etcd, no Zookeeper).
- No web UI / dashboard frontend.
- No full observability stack (no OpenTelemetry, no
  Jaeger, no Prometheus exporter, no OpenMetrics endpoint,
  no log-aggregation forwarder, no distributed tracing).
- No `/healthz` / `/readyz` / `/livez` endpoint (Track J
  §8 defer preserved).
- No standalone `apps/platform` daemon entrypoint.
- No hot reload / zero-downtime restart guarantee.
- No automatic-update / OTA / self-upgrade mechanism.
- No rollback expansion / AST work / 1С matrix expansion.
- No new MCP tools / registry change.
- No `1cv8.exe` runs.
- No remote push.
- No "packaging solved forever" / "PyPI release ready" /
  "signed binary distribution" / "all package managers
  supported" / "production-ready packaging" / "enterprise-
  ready packaging" / "hostile-internet distribution
  ready" claim.

---

## Step 1 — planning packaging ecosystem and distribution boundary

**Goal.** Open Track M formally with a single planning
document and a single step-map document, plus the narrative
flip on README.md and PROJECT-STATUS.md required to mark
Track M as the active parallel track. Establish the Q1–Q7
directional defaults without locking final answers.

**What changes.**
- NEW: `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement; in-scope /
  out-of-scope; guardrails; acceptance criteria;
  relationship table to Tracks G/H/I/J/K/L; step
  trajectory).
- NEW: `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-step-map.md`
  (this document — six steps + track invariants block +
  hard out-of-scope block).
- MODIFIED: `README.md` — Quickstart paragraph appended
  with Track M active wording; "Active parallel track"
  section reopened describing Track M at Step 1
  planning-only; Closed parallel tracks list **unchanged**
  (Track M not moved there yet).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "no active step" to "Track M / Step 1 active planning";
  Track L closure block preserved beneath byte-identical;
  one new per-step section "Parallel Track M / Step 1 —
  planning packaging ecosystem and distribution boundary
  (завершён)" inserted between the Track L Step 6
  section and `## Phase 6 закрыта`.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`, `runtime.py`, `process_control.py`).
- `pyproject.toml` (`version=0.5.1` preserved; wheel-
  build empty preserved).
- `scripts/*` — all existing files byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/service-supervision.md`,
  `docs/operators/service/mcp-server.service`,
  `CHANGELOG.md` — byte-identical.
- All Tracks A–L architecture docs — byte-identical.
- Registries `read=15 / write=25 / intelligence=16`.
- README Closed parallel tracks list (still ends at
  Track L).
- No `1cv8.exe` runs.
- No real credentials.
- No remote push.
- No Step 2 opening.

**Result.** Track M is formally open at Step 1. The plan
document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file) fixes
the six-step boundary. Operator can read the plan and
step-map and know exactly what Track M will and will not
do. README and PROJECT-STATUS reflect the active-track
flip. No code change anywhere; no `pyproject` change;
registry invariant carried through; selfcheck green;
`verify-release.ps1` green on 8 checks.

---

## Step 2 — baseline audit of current packaging / distribution state

**Goal.** Produce a single descriptive (not prescriptive)
audit document inventorying the current state of
packaging / build / distribution surfaces in the repo;
classify the inventory into the standard 4-class breakdown
(already-reusable / adjacent-but-insufficient / clearly-
missing / explicitly-out-of-scope); produce Q1–Q6
directional resolutions grounded in evidence; produce a
handoff list for Step 3 contract consumption.

**What changes.**
- NEW: `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-baseline-audit.md`
  — single descriptive audit document. Default expectation
  = 8–12 sections, ≤ 1500 lines. Sections must cover:
  inventory of `pyproject.toml` declared surface
  (`[project]` metadata, `[project.scripts]` console
  entries declared but un-installable, the empty wheel-
  build setting and its Track C / Step 3 honest-constraint
  comment block); inventory of `scripts/release/`
  artefacts (`install.ps1` config materialiser,
  `verify-release.ps1` 8-check gate, `_install_runner.py`
  helper, `README.md` "no install ecosystem" framing);
  inventory of release-handoff prose ("What is NOT in this
  handoff" enumeration of every absent packaging artefact);
  inventory of operator-facing docs that mention
  packaging non-goals (Track J recipe, Track K harness
  notes, Track L recipe); whole-repo grep for
  packaging-vocabulary terms (`wheel`, `sdist`, `dist/`,
  `release/`, `MANIFEST.in`, `setup.py`, `setup.cfg`,
  `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`, `signing`,
  `PyPI`, `Chocolatey`, `Homebrew`, `apt-get`, `conda-
  forge`, `cosign`, `sigstore`, `SBOM`); 4-class
  breakdown; Q1–Q6 directional resolutions; Step 3
  handoff list (≥ 10 items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`.
- README and PROJECT-STATUS — Step 2 is the audit step.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 2 produces a single descriptive audit
document. No prescriptive language; no MUST / MUST NOT /
SHOULD lock. All "decisions" stay as directional
recommendations to be locked by Step 3 contract.

---

## Step 3 — packaging / distribution contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT / SHOULD /
SHOULD NOT / MAY language. Lock Q1–Q7 final answers (Q7
deferred to Step 6 but framed). Lock Step 4 PATH (A docs-
only / B docs + narrow `pyproject.toml` flip / C docs +
operator-bundle artefact). Lock Step 4 file-surface cap
(default ≤ 3 touched files). Lock Step 4 LOC cap for any
code-bearing artefact (default ≤ 200 LOC stdlib-only,
no new dependencies). Lock Step 4 forbidden-files list.
Lock Step 5 forbidden-files list. Lock the closure-gate
scenario (artefact class, distribution boundary, install
recipe verbs).

**What changes.**
- NEW: `docs/architecture/track-m-packaging-ecosystem-and-distribution-boundary-contract.md`
  — single normative contract document with RFC 2119
  language. Default expectation = 10–15 sections, ≤ 1700
  lines.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`.
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 3 closes with the prescriptive contract
in place. Step 4 has a closure-gate scenario, a file
surface, a LOC cap, a forbidden-files list, and a
verification protocol — all locked.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by shipping
the locked Step 4 artefact(s) under the locked path and
cap. Default expectation = PATH B (one operator-facing
recipe + one narrow `pyproject.toml` flip making the
wheel-build non-empty) **if** Step 2 audit confirms PATH
B is feasible without ecosystem expansion. PATH A or
PATH C only if Step 3 contract explicitly authorises
them.

**What changes (default expectation, PATH B).**
- NEW: operator-facing distribution-boundary recipe under
  `docs/operators/packaging/` (or whichever path Step 3
  contract locks). Default expectation = 6–10 sections,
  ≤ 800 lines. Sections cover: purpose; scope statement
  (what artefact ships, what does NOT ship); the wheel-
  build flip itself (operator command `python -m build`
  produces a `.whl` under `dist/`); the install recipe
  (`pip install <wheel>`); the cross-OS neutral framing;
  cross-references to Tracks G / H / I / J / K / L;
  honest non-goals enumeration.
- MODIFIED: `pyproject.toml` — single narrow change:
  `[tool.hatch.build.targets.wheel] packages = []` →
  `packages = ["<path1>", "<path2>", ...]` populated
  with the project's eleven src-layout paths (or
  whichever subset Step 3 contract locks). The 24-line
  honest-constraint comment block above the change MUST
  be updated to reflect the new reality (the wheel build
  now produces a usable artefact); the change MUST NOT
  add any other `pyproject.toml` field (no
  `[project.urls]`, no classifiers, no keywords, no
  `MANIFEST.in`).
- POSSIBLY NEW: one accompanying file (e.g., short
  validation script or release-side note under
  `scripts/release/`) only if Step 3 contract explicitly
  authorises it under the file-surface cap.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`, `runtime.py`, `process_control.py`,
  `runtime_logs.py`, `models.py`).
- `pyproject.toml` `version`, `[project]` metadata
  (other than the wheel `packages` flip), `[project.scripts]`
  entries, `[tool.ruff]`, `[tool.pytest.ini_options]`
  (other than the deliberate narrow change in §8 above).
- Existing `scripts/dev/*`, `scripts/release/*`
  byte-identical (Step 4 may add **new** sibling files
  only if Step 3 contract pins PATH C or PATH B with
  helper script; existing files in those directories are
  not modified).
- `scripts/dev/mcp_client_smoke.py` byte-identical.
- `docs/operators/deployment-boundary.md` byte-identical.
- `docs/operators/service/service-supervision.md` and
  `docs/operators/service/mcp-server.service` byte-
  identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `README.md`, `PROJECT-STATUS.md` — Step 4 is the
  implementation step; closure-doc updates belong to
  Step 5 / Step 6.
- Track M Step 1 / Step 2 / Step 3 docs byte-identical.
- Registries.
- No new MCP tools.
- No 1cv8.exe runs.
- No real credentials.
- No remote push.

**Result.** Step 4 ships the locked Step 3 artefact(s).
Operator can follow the recipe end-to-end without further
repo modifications and end up with a working install of
the platform from a single buildable artefact (PATH B) or
with a documented distribution boundary (PATH A) or with
a copied operator bundle (PATH C).

---

## Step 5 — docs / operator / release alignment

**Goal.** Narrow CLASS-1 docs-alignment only. Update the
operator / security / release-facing docs that have direct
factual drift after Step 4. No Track M closure narrative;
Track M remains framed as **active** through Step 5
(closure narrative is Step 6 territory).

**What changes (default expectation, CLASS 1 only).**
- MODIFIED: `README.md` — Quickstart paragraph + "Active
  parallel track" section refreshed to reflect Steps 1–4
  closed and Step 5 active.
- POSSIBLY MODIFIED: `docs/release-handoff.md` — only if
  Step 4 = PATH B (wheel becomes buildable) and the
  existing "No wheel-based install" line in "What is NOT
  in this handoff" develops direct factual drift; if
  drift, rewrite that line + add one bullet in "What is
  in this handoff" pointing at the Step 4 recipe + add
  one bullet in "Where to read deeper".
- POSSIBLY MODIFIED: `scripts/release/README.md` — only
  if Step 4 introduces a release-side surface that the
  existing "Neither introduces a new install ecosystem"
  framing develops drift; default expectation = no edit
  (a narrow wheel-build flip does not invalidate the
  "no install ecosystem" claim per Step 3 contract).
- POSSIBLY MODIFIED: `apps/platform/README.md` — only
  if Step 4 introduces a packaging boundary that the
  platform README's existing inventory mentions; default
  expectation = no edit.

**What does NOT change.**
- Production code.
- `pyproject.toml`.
- `scripts/*` beyond `scripts/release/README.md` (and
  only if drift).
- `PROJECT-STATUS.md`, `CHANGELOG.md`, README Closed
  parallel tracks list / Track M detail (закрыт)
  section, `pyproject.toml` `version` — all Step 6
  territory.
- Track M Step 1 / Step 2 / Step 3 / Step 4 deliverables
  byte-identical.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 5 closes with operator-facing docs in
sync with the Step 4 artefact(s). CLASS-3 (closure-
narrative) edits are explicitly **not** done at Step 5.

---

## Step 6 — final integration pass and track closure

**Goal.** Honest closure of Track M. Q7 decision recorded
explicitly. Active tracks remaining = none afterwards.
Twelve post-phase parallel tracks become thirteen (A
through M).

**What changes.**
- MODIFIED: `README.md` — Quickstart paragraph flipped
  from active → no-active-track wording; "Active parallel
  track" section compressed back to "no active track";
  new "Track M detail (закрыт)" section added above
  "Track L detail (закрыт)"; Closed parallel tracks list
  extended from двенадцать → тринадцать with Track M
  entry.
- MODIFIED: `PROJECT-STATUS.md` — header rewritten from
  "Track M / Step 1 active planning" to "no active step
  + Track M fully closed"; new `closed` status block for
  Track M with six commit hashes; per-step closure
  sections for Track M Step 2 / Step 3 / Step 4 / Step 5 /
  Step 6 inserted; historical-edit annotation on the tail
  of the Track L Step 6 section updated to reflect
  Track M closure.
- MODIFIED: `CHANGELOG.md` — Track M subsection
  inserted. If Q7 = NO-BUMP: subsection under existing
  `## 0.5.1` heading. If Q7 = PATCH: new top-level
  `## 0.5.2 — Parallel Track M — Packaging Ecosystem and
  Distribution Boundary` heading. If Q7 = MINOR: new
  top-level `## 0.6.0 — Parallel Track M — Packaging
  Ecosystem and Distribution Boundary` heading (default
  expectation rejects MINOR per Q7 framing in plan §12).
- POSSIBLY MODIFIED: `pyproject.toml` — `version`
  bumped only if Q7 = PATCH (`0.5.1 → 0.5.2`) or MINOR
  (`0.5.1 → 0.6.0`); not touched if Q7 = NO-BUMP.

**What does NOT change.**
- Production code.
- All `scripts/*` files (no Step-4 wrapper script
  modification at Step 6; Step-4 deliverables immutable).
- Track M Step 1 / Step 2 / Step 3 / Step 4 / Step 5
  deliverables byte-identical.
- `SECURITY.md` (Step 5 didn't touch; Step 6 doesn't
  either).
- `docs/release-handoff.md` (Step 5 already aligned if
  it needed it; Step 6 does not re-touch).
- `apps/platform/README.md` (Step 5 already aligned if
  it needed it; Step 6 does not re-touch).
- `docs/operators/deployment-boundary.md`,
  `docs/operators/service/service-supervision.md`,
  `docs/operators/service/mcp-server.service` byte-
  identical (Track J / Track L artefacts, not in
  Track M scope at any step).
- Registries `read=15 / write=25 / intelligence=16`.
- No new MCP tools.
- No 1cv8.exe runs.
- No real credentials.
- No remote push.

**Result.** Track M closed. Thirteen post-phase parallel
tracks closed sequentially (A / B / C / D / E / F / G / H /
I / J / K / L / M). Phase 7 as a linear phase still not
planned. Q7 outcome recorded explicitly with defended
reasoning. Active parallel track = none.

---

## Q7 framing for Step 6

The Q7 decision is locked at Step 6 only. Defaults from
the plan §12.Q7:

- **NO-BUMP default** if Step 4 = PATH A (docs-only,
  `pyproject.toml` byte-identical). Mirrors Track J /
  Track K / Track L closure precedent.
- **PATCH considered** as the most likely outcome if
  Step 4 = PATH B (declarative `[tool.hatch.build.targets.wheel]
  packages` flip closing the Track C / Step 3 long-
  standing honest constraint about the empty wheel
  build). This is a legitimate defect-class repair
  framing — Track C explicitly left a 24-line comment
  block citing this exact future moment.
- **MINOR considered** only if Step 4 introduces net-new
  external capability for ordinary product consumers
  beyond making the existing `[project.scripts]`
  declarations functional. Default expectation rejects
  MINOR per the "no new CLI flag" Q4 / step-map
  invariant #15.
- **MAJOR forbidden** by track scope.

Step 6 must defend its Q7 choice with concrete repo facts
(diff stat, byte-identical inventories, public API
inventory, SemVer §6 / §7 applicability), not by inertia.

---

## Closure summary

By Step 6 commit:

- Thirteen post-phase parallel tracks (A through M)
  closed.
- Track M closed with an explicit Q7 decision.
- Production code byte-identical to Track L closure
  state (`e21e185`).
- Registries unchanged.
- At most one operator-facing recipe + at most one
  narrow `pyproject.toml` flip + at most one
  accompanying file (default PATH B).
- README / PROJECT-STATUS / CHANGELOG updated honestly,
  with explicit denial of "packaging solved forever" /
  "PyPI release ready" / "signed binary distribution" /
  "all package managers supported" / "production-ready
  packaging" / "enterprise-ready packaging" claims.
- `verify-release.ps1` GREEN on 8 checks at every step.
- `selfcheck.py` `status=ok` at every step.
- No new MCP tools / registry drift / `1cv8.exe` runs /
  real credentials / remote push at any step.
