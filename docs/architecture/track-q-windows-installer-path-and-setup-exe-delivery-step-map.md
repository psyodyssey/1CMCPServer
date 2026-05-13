# Parallel Track Q — Windows Installer Path and setup.exe Delivery — Step Map

Companion to
[track-q-windows-installer-path-and-setup-exe-delivery-plan.md](track-q-windows-installer-path-and-setup-exe-delivery-plan.md).
This document defines the six steps of Track Q in the
standard format used by Tracks A–P (Goal / What changes /
What does NOT change / Result), plus the track invariants
block, the hard out-of-scope block, and the Step 6 Q7
framing.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track Q invariants

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
   modified by any Track Q step. Default expectation:
   zero production code change across all six Track Q
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
8. **Track P / Step 1 planning surface byte-
   identical.**
   `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-plan.md`
   and
   `docs/architecture/track-p-test-suite-shipping-and-verification-boundary-step-map.md`
   not modified by any Track Q step. Track Q does not
   touch Track P deliverables; Track P remains active
   at its own pace, decided by separate operator
   action.
9. **`pyproject.toml`** byte-identical at Steps 1 / 2
   / 3 / 4 / 5. Step 6 MAY modify `pyproject.toml`
   `version` only if Q7 = PATCH or MINOR; default
   expectation Q7 framing only with the version-bump
   decision deferred to Step 6. `[project]`,
   `[project.scripts]`, `[tool.ruff]`,
   `[tool.pytest.ini_options]`,
   `[tool.hatch.build.targets.wheel]`,
   `[build-system]` blocks remain byte-identical
   across all six steps.
10. **Registries `read = 15 / write = 25 / intelligence
    = 16`** unchanged across all six steps.
    `selfcheck.py` `status=ok` at every step.
11. **`scripts/dev/selfcheck.py`** byte-identical at
    every step.
12. **`scripts/dev/launch.ps1`** byte-identical at
    every step. Track Q does not modify the launch
    umbrella; the Windows-installer launch surface is
    a Start menu shortcut owned by the installer-
    technology runtime (Inno Setup default), not by
    `launch.ps1`.
13. **`scripts/dev/bootstrap_paths.ps1`,
    `scripts/dev/run_dev_check.ps1`** byte-identical
    at every step.
14. **`scripts/release/install.ps1`,
    `scripts/release/verify-release.ps1`,
    `scripts/release/_install_runner.py`,
    `scripts/release/README.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    pointer to the Step 4 recipe in
    `scripts/release/README.md` only (≤ 1 new
    bullet); the three script files remain byte-
    identical at every step.
15. **`scripts/dev/README.md`** byte-identical at
    every step.
16. **`SECURITY.md`** byte-identical at every step.
17. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    CLASS-1 updates (≤ 1 new bullet).
18. **`apps/platform/README.md`** byte-identical at
    every step.
19. **`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    cross-link in `docs/operator-manual.md` only.
20. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still 15
    entries A–O). Step 6 may extend the list
    depending on whether Track P closure has
    occurred independently by that point. If Track
    P is still active at Step 6 of Track Q, Track
    Q's closure narrative goes into a "Closed
    parallel tracks (out-of-order closure)"
    subsection rather than extending the main list
    arbitrarily.
21. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a Track Q closure
    entry.
22. **`.github/workflows/dev-check.yml`** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5. Step 4
    MAY extend the workflow file only if Step 3
    contract explicitly authorises a Windows-runner
    installer-build job (≤ 30 lines of YAML
    addition); default expectation under PATH A / B
    is no workflow change.
23. **`.python-version`** byte-identical at every
    step (Python 3.11 pin preserved as the
    bundled-runtime target — the installer bundles
    a CPython interpreter whose version is governed
    by this pin).
24. **`1c_agent_platform-<VERSION>-py3-none-any.whl`
    artefact class byte-identical** (Track M closure
    state). The Track Q installer is built **on top
    of** the wheel, not over it; the wheel artefact
    contract is unchanged.
25. **No new MCP tools** at any step.
26. **No new CLI flag** on any existing MCP server
    entrypoint at any step.
27. **No new `[project.scripts]` console entries.**
28. **No new project dependencies in
    `[project.dependencies]` nor in
    `[project.optional-dependencies]`.** Track Q
    does not add Python dependencies; the bundled
    Python runtime is an out-of-band installer-side
    artefact, not a `pip`-resolved dependency.
29. **No new entrypoint module.**
30. **No bundled-runtime binary committed to git.**
    The python.org embeddable distribution (or any
    equivalent CPython binary) is acquired at build
    time by the build helper, not committed as a
    binary blob to the repository. The Step 4 file
    surface MUST NOT include any `.zip`, `.exe`,
    `.dll`, `.pyd`, `.msi`, `.cab`, `.7z`, `.tar.*`,
    `.gz`, `.bz2`, `.xz`, or other binary artefact.
31. **No `1cv8.exe` runs** at any step.
32. **No outbound network at runtime.** The build-
    time fetch of the python.org embeddable
    distribution (if any) is build-time operator-
    triggered behaviour, documented in the recipe.
    No production code path performs outbound HTTP.
33. **No real credentials** in any committed text.
34. **No remote push** at any step. Operator-side
    GitHub release publishing is not part of any
    Track Q step.
35. **No premature closure language.** Phrases that
    frame Track Q as "закрыт" / "closed" / "fully
    solved" / "Windows install solved forever" /
    "enterprise-grade installer" / "production-
    ready desktop app" / "all Windows distributions
    supported" / "one-click everything solved
    forever" / "GUI config wizard" / "Windows
    service auto-magic by default" may appear in
    Steps 1–5 only as explicit DENIALS. Only Step 6
    introduces closure language for Track Q itself.

---

## Track Q hard out-of-scope (carry through every step)

These categories must not be addressed by Track Q at
any step. Each is named explicitly to prevent silent
expansion:

- No Linux installer (`.deb`, `.rpm`, `.apk`,
  `.AppImage`, `.snap`, `.flatpak`).
- No macOS installer (`.dmg`, `.pkg`, `.app`,
  Homebrew cask, MacPorts, notarization).
- No `.msi` ecosystem in broad form (WiX considered
  only if Step 2 audit surfaces a grounded MDM /
  SCCM / Intune operator need; default = Inno Setup
  producing setup.exe).
- No Chocolatey / winget / Scoop / NuGet / Microsoft
  Store publication.
- No PyPI publication (Track M non-goal preserved).
- No code signing / Authenticode / EV cert /
  notarization / SBOM / SLSA / supply-chain
  attestation.
- No auto-update / OTA / delta-update.
- No GUI dashboard / browser UI / web admin panel.
- No service supervision redesign (Track L
  preserved; installer does not register a Windows
  Service by default).
- No auth redesign (Track D / H preserved).
- No transport redesign (Track G / H preserved).
- No new MCP tools / registry change.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new entrypoint module.
- No new project dependencies (runtime or optional).
- No new transports (WebSocket, SSE, gRPC, AMQP).
- No remote-dev / DX / IDE integrations (Track O
  preserved).
- No enterprise installer platform (Group Policy
  templates, SCCM packaging, Intune publishing).
- No containerisation (Dockerfile, OCI image,
  Podman, container runtime).
- No cluster / HA.
- No "all Windows distributions supported" claim
  (default support matrix: Windows 10 + 11 amd64;
  Windows 7, Windows Server, ARM64, x86 not in
  default).
- No "one-click everything solved forever" claim.
- No "enterprise-grade installer" claim.
- No "production-ready desktop app" claim.
- No "GUI config wizard" claim (installer drops the
  platform on disk; product configuration is a
  separate operator step using existing surfaces).
- No "Windows service auto-magic by default" claim
  (Track L recipe preserved; the installer does not
  silently register a Windows Service).
- No test-suite program (Track P territory).
- No observability redesign (Track N preserved).
- No remote push / GitHub release publishing.
- No new parallel track opened in the same Step.

---

## Step 1 — planning Windows installer path

**Goal.** Open Track Q formally with a single planning
document and a single step-map document, plus the
narrative flip on README.md and PROJECT-STATUS.md
required to mark Track Q as the second active parallel
track (alongside Track P at its own Step 1).
Establish the Q1–Q7 directional defaults without
locking final answers. Make the central honest
constraint (bundled Python runtime is structurally
required) explicit and prominent.

**What changes.**
- NEW: `docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement grounded
  in `scripts/release/install.ps1:1-11` +
  `docs/operators/packaging/distribution-boundary.md
  §7` + `pyproject.toml` Track M comment block
  anchors; central honest constraint about bundled
  Python runtime called out as §4 not as a footnote;
  in-scope / out-of-scope; guardrails; acceptance
  criteria; relationship table to Tracks M/L/O/P;
  step trajectory).
- NEW: `docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-step-map.md`
  (this document — six steps + 35 track invariants
  block + hard out-of-scope carry-through list +
  Step 6 Q7 framing).
- MODIFIED: `README.md` — Quickstart paragraph
  appended with Track Q active-planning wording
  alongside the existing Track P active-planning
  wording; "Active parallel track" section extended
  to enumerate Track P and Track Q both at Step 1
  planning-only (the section pluralises to "Active
  parallel tracks" because there are now two);
  Closed parallel tracks list **unchanged** (still
  15 entries A–O).
- MODIFIED: `PROJECT-STATUS.md` — header narrative
  extended to describe Track Q / Step 1 alongside
  the existing Track P / Step 1 description; new
  per-step section "Parallel Track Q / Step 1 —
  planning Windows installer path and setup.exe
  delivery (завершён)" inserted in the canonical
  location, structurally mirroring the existing
  Track P / Step 1 section.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`).
- `pyproject.toml` (`version=0.5.2` preserved; all
  blocks byte-identical).
- `scripts/*` — every existing file byte-identical
  (including `scripts/release/install.ps1` whose
  umbrella comment is the anchor we cite, but which
  itself is not modified).
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, manuals,
  `docs/operators/*` (Tracks J/L/M/N recipes),
  `docs/dev/editable-install-and-workspace-discovery.md`
  (Track O recipe), `CHANGELOG.md` — byte-identical.
- Track P / Step 1 planning surface
  (`docs/architecture/track-p-*`) — byte-identical.
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
- No additional parallel track opened in this Step.
- No bundled-runtime binary committed.
- No installer-definition file committed.

**Result.** Track Q is formally open at Step 1. The
plan document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file)
fixes the six-step boundary. Contributor and
operator can read the plan and step-map and know
exactly what Track Q will and will not do. README
and PROJECT-STATUS reflect the second active-track
flip. Track P remains untouched. No code change
anywhere; no `pyproject.toml` change; registry
invariant carried through; selfcheck green;
`verify-release.ps1` green on 8 checks.

---

## Step 2 — baseline audit of current Windows install reality

**Goal.** Produce a single descriptive (not
prescriptive) audit document inventorying the
current state of Windows-install-relevant surfaces
in the repo (the three install-adjacent paths +
their Python prerequisite + the three anchor
citations in `scripts/release/install.ps1`,
`docs/operators/packaging/distribution-boundary.md`,
`pyproject.toml` Track M comment block + the
ordinary-Windows-user persona reality);
classify the inventory into the standard 4-class
breakdown (already-reusable / adjacent-but-
insufficient / clearly-missing / explicitly-out-
of-scope); inventory honest options under §4
constraint (α bundled embeddable vs β frozen
executable); compare candidate installer
technologies (Inno Setup vs WiX vs NSIS vs
others); produce Q1–Q6 directional resolutions
grounded in evidence; produce a handoff list for
Step 3 contract consumption.

**What changes.**
- NEW: `docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-baseline-audit.md`
  — single descriptive audit document. Default
  expectation = 8–12 sections, ≤ 1500 lines.
  Sections must cover: ordinary-Windows-user
  persona reality; inventory of three existing
  install-adjacent paths
  (`scripts/release/install.ps1`,
  `pip install <WHEEL_PATH>`, `pip install -e .`)
  with Python prerequisite explicit for each;
  inventory of three anchor citations
  (`scripts/release/install.ps1:1-11`,
  `docs/operators/packaging/distribution-
  boundary.md §7`, `pyproject.toml` Track M
  comment block); inventory of repository for
  installer-technology definition files
  (verifying none exist); inventory of repository
  for any bundled-runtime binaries (verifying
  none exist); option-space audit of §4 shape α
  vs shape β; technology-choice audit of Inno
  Setup vs WiX vs NSIS vs others with grounded
  per-option pro/con; expected installed
  footprint per technology; Q1–Q6 directional
  resolutions; Step 3 handoff list (≥ 10 items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  manuals, existing operator recipes (Track J/L/M/N),
  Track O dev recipe.
- Track P / Step 1 planning surface.
- README and PROJECT-STATUS — Step 2 is the audit
  step.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.
- No bundled-runtime binary committed.
- No installer-definition file committed.

**Result.** Step 2 produces a single descriptive
audit document. No prescriptive language; no MUST /
MUST NOT / SHOULD lock. All "decisions" stay as
directional recommendations to be locked by Step 3
contract.

---

## Step 3 — Windows installer path and setup.exe delivery contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY language. Lock Q1–Q6
final answers (Q7 deferred to Step 6 but framed).
Lock the installer technology choice (default
expectation: Inno Setup). Lock the bundled-runtime
shape (default expectation: python.org embeddable
CPython 3.11). Lock the install directory default.
Lock the launch surface default. Lock the
uninstall verb. Lock the supported installed
footprint range. Lock the Step 4 PATH (A docs-
only / B docs + narrow `.iss` + optional build
helper / C docs + standalone non-product helper).
Lock the Step 4 file-surface cap (default ≤ 3
touched files). Lock the Step 4 LOC caps (≤ 250
LOC for `.iss`; ≤ 1200 LOC for recipe). Lock the
Step 4 forbidden-files list. Lock the Step 5
forbidden-files list. Lock the closure-gate
scenario.

**What changes.**
- NEW: `docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-contract.md`
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
- Track P / Step 1 planning surface.
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update.
- Registries.
- CI workflow.
- `.python-version`.
- No 1cv8.exe runs.
- No remote push.
- No bundled-runtime binary committed.
- No installer-definition file committed.

**Result.** Step 3 closes with the prescriptive
contract in place. Step 4 has a closure-gate
scenario, a file surface, LOC caps, a forbidden-
files list, and a verification protocol — all
locked.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by
shipping the locked Step 4 artefact(s) under the
locked path and cap. Default expectation (per
Step 1 plan Q3 directional default) = PATH B
(operator recipe + one Inno Setup `.iss` script
+ optionally one PowerShell build helper). PATH A
(docs-only) acceptable fallback if Step 2/3 audit
reveals that committing a `.iss` expands scope.
PATH C (standalone helper without the `.iss`)
rejected by default.

**What changes (default expectation, PATH B).**
- NEW: operator-facing Windows-installer recipe
  under `docs/operators/installer/windows-setup-exe.md`
  (or whichever path Step 3 contract locks).
  Default expectation = 8–12 sections, ≤ 1200 lines.
  Sections must cover: scope and audience
  (ordinary Windows user without Python/pip/Git);
  bundled-runtime fact stated up front;
  acquisition of the python.org embeddable CPython
  3.11 distribution at build time; structure of
  the install directory (default
  `%LOCALAPPDATA%\Programs\1c-agent-platform\`);
  what the installer does (extracts wheel
  contents + embedded runtime + creates Start menu
  shortcut + registers uninstall entry under
  HKCU\Software\Microsoft\Windows\CurrentVersion\
  Uninstall\\<GUID>); how to launch the platform
  after install (Start menu shortcut opens a
  PowerShell window in install directory; manual
  config materialisation remains a separate
  step using existing scripts/release/install.ps1
  invoked through the bundled runtime); uninstall
  verb (Settings → Apps → Installed apps →
  Uninstall); honest non-goals (no signing, no
  auto-update, no GUI config wizard, no service
  registration, no MDM, no enterprise platform);
  cross-references to Track M packaging recipe
  and Track L service-supervision recipe (with
  explicit note that the installer does **not**
  perform service registration).
- NEW: `installer/windows/<NAME>.iss` Inno Setup
  script — one declarative file, default
  expectation ≤ 250 LOC. No bundled-runtime
  binary committed; the script references the
  expected runtime path at build time, pulled by
  the optional build helper.
- POSSIBLY NEW: `installer/windows/build-setup-exe.ps1`
  — optional PowerShell build helper that pulls
  the python.org embeddable distribution, copies
  the Track M wheel contents into the staging
  directory, invokes Inno Setup compiler, emits
  setup.exe under `dist/installer/`. Default
  expectation ≤ 200 LOC. Only included if Step 3
  contract authorises the optional helper.

**What changes (alternative, PATH A — if Step 3
contract authorises).**
- NEW: operator-facing Windows-installer recipe
  only. The recipe walks an operator through
  producing setup.exe out-of-tree; no `.iss`
  committed.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`)
  byte-identical at all PATH variants.
- `pyproject.toml` byte-identical (no version
  bump at Step 4; Q7 is Step 6 territory).
- All existing operator recipes (Track J/L/M/N)
  byte-identical.
- Track O dev recipe byte-identical.
- Track P / Step 1 planning surface byte-identical.
- `scripts/dev/selfcheck.py`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/dev/launch.ps1`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/run_dev_check.ps1`,
  `scripts/dev/README.md` byte-identical at Step 4.
- `scripts/release/install.ps1`,
  `scripts/release/verify-release.ps1`,
  `scripts/release/_install_runner.py`,
  `scripts/release/README.md` byte-identical at
  Step 4.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  README.md, PROJECT-STATUS.md — Step 4 is the
  implementation step; closure-doc updates belong
  to Step 5 / Step 6.
- Track Q Step 1 / Step 2 / Step 3 docs byte-
  identical.
- All Tracks A–O architecture docs byte-identical.
- CI workflow `.github/workflows/dev-check.yml`
  byte-identical (unless Step 3 contract explicitly
  authorises a Windows-runner installer-build job).
- `.python-version` byte-identical.
- Registries.
- No new MCP tools.
- No new CLI flag.
- No new `[project.scripts]` console entries.
- No new entrypoint module.
- No new project dependencies (runtime or
  optional).
- No bundled-runtime binary committed.
- No `1cv8.exe` runs.
- No outbound network in any committed production
  code.
- No remote push.

**Result.** Step 4 ships the locked artefact(s).
Track Q's Windows-installer boundary is now
operator-readable end-to-end. Production code
byte-identical to Track O closure state. Registry
invariant carried through. `selfcheck.py` green.
`verify-release.ps1` green on 8 checks.

---

## Step 5 — docs / operator / release alignment

**Goal.** Bring narrow CLASS-1 alignment edits to
README / PROJECT-STATUS / possibly
`docs/release-handoff.md` / possibly
`docs/operator-manual.md` / possibly
`scripts/release/README.md` so that operator-facing
narrative reflects the Step 4 reality without
introducing new code, new declared surface, or new
dependencies. Step 5 is a docs-only step.

**What changes.**
- POSSIBLY MODIFIED: `README.md` — narrow CLASS-1
  wording updates only. Closed parallel tracks
  list **unchanged** (still 15 entries A–O).
- POSSIBLY MODIFIED: `PROJECT-STATUS.md` — one new
  per-step section "Parallel Track Q / Step 5 —
  docs / operator / release alignment (завершён)".
- POSSIBLY MODIFIED: `docs/release-handoff.md` —
  at most one new bullet pointing at the Step 4
  recipe.
- POSSIBLY MODIFIED: `docs/operator-manual.md` —
  at most one new cross-link if its prose
  develops factual drift.
- POSSIBLY MODIFIED: `scripts/release/README.md`
  — at most one new pointer.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- `scripts/dev/selfcheck.py`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/dev/launch.ps1`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/run_dev_check.ps1`,
  `scripts/dev/README.md` byte-identical.
- `scripts/release/install.ps1`,
  `scripts/release/verify-release.ps1`,
  `scripts/release/_install_runner.py` byte-
  identical.
- `SECURITY.md` byte-identical.
- All existing operator recipes (Track J/L/M/N)
  byte-identical.
- Track O dev recipe byte-identical.
- Track P / Step 1 planning surface byte-identical.
- Track Q Step 4 recipe + (if PATH B) `.iss` +
  optional build helper byte-identical (Step 4
  deliverable immutable).
- All Tracks A–O architecture docs byte-identical.
- Track Q Step 1 / Step 2 / Step 3 / Step 4 docs
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
- No bundled-runtime binary committed.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Operator-facing narrative aligned with
post-Step-4 reality. No code change beyond Step 4.
No new declared surface. Track Q still **not**
closed (Step 6 remaining).

---

## Step 6 — final integration pass and track closure

**Goal.** Land the final integration pass that
explicitly closes Track Q. Update README Closed
parallel tracks list (or add a "Closed parallel
tracks (out-of-order closure)" subsection,
depending on whether Track P has independently
closed by this point). Add Track Q closure
narrative to PROJECT-STATUS. Append Track Q
closure entry to CHANGELOG.md. Lock Q7 (NO-BUMP /
PATCH / MINOR per §12 framing in the plan).
Carry every Tracks A–O invariant and Track P
state byte-identical.

**Q7 framing for closure step:**

- **NO-BUMP** (defensible under PATH A): Track Q
  closes under existing `0.5.2` without
  `pyproject.toml [project] version` change.
  Mirrors Track J / Track K / Track L / Track N /
  Track O NO-BUMP precedents. PATH A is pure
  docs-only operator-facing recipe; no
  production code, no `pyproject.toml`, no
  `scripts/*` logic, no new declared surface —
  Q7 = NO-BUMP is one honest outcome.
- **PATCH `0.5.2 → 0.5.3`** (or next-PATCH after
  Track P, if Track P consumed PATCH first;
  defensible under PATH B framed as defect-
  class delivery-channel repair): Track Q
  closes with a PATCH bump if Step 4 = PATH B
  materialises the deferred "no GUI installer"
  non-goal anchor in Track M's recipe and
  `pyproject.toml` comment block. Mirrors
  Track I PATCH (`installer.py:_config_to_dict`
  defect-class round-trip fix making the
  declared `auth.tokens` round-trip actually
  preserved) and Track M PATCH
  (`pyproject.toml` packages flip defect-class
  repair making the declared
  `[project.scripts]` console entries actually
  installable). Track Q PATH B framed under
  this precedent closes the long-standing
  deferred GUI-installer surface — declared-as-
  non-goal-but-deferred → declared-and-shipped-
  out-of-band-with-honest-boundary = PATCH
  territory.
- **MINOR `0.5.2 → 0.6.0`** (or next-MINOR
  after Track P; defensible under PATH B
  framed as new operator-visible delivery
  capability): Track Q closes with a MINOR
  bump if Step 4 = PATH B is framed as
  introducing a **new operator-visible delivery
  channel** — the ordinary Windows user
  without Python on the box is a genuinely new
  audience and a delivery channel that
  ordinary product consumers could not use
  before. Mirror of Track H MINOR precedent
  (introduction of the HTTP network transport
  as a new operator-visible delivery
  capability).
- **MAJOR** forbidden by track scope.

**What changes.**
- MODIFIED: `README.md` — Closed parallel tracks
  list updated (extended to 16 or 17 entries, or
  with a new "out-of-order closure" subsection,
  depending on whether Track P has independently
  closed by this point); "Active parallel tracks"
  section updated to reflect Track Q closure (and
  Track P state, untouched); Quickstart paragraph
  updated to reflect Track Q closure; "Track Q
  detail (закрыт)" section added (mirror of
  existing Tracks A–O detail sections in length
  and shape).
- MODIFIED: `PROJECT-STATUS.md` — header narrative
  updated to reflect Track Q closure (and Track
  P state, untouched); Track Q closure narrative
  added; six per-step sections for Track Q
  finalised.
- MODIFIED: `CHANGELOG.md` — Track Q closure
  entry appended. If Q7 = NO-BUMP, appended as a
  sub-section under existing `0.5.2` heading. If
  Q7 = PATCH, created as a new top-level
  `## 0.5.3` heading (or whichever next PATCH is
  honest at that point) with grounded PATCH-bump
  justification. If Q7 = MINOR, created as a new
  top-level `## 0.6.0` heading (or whichever
  next MINOR is honest) with grounded MINOR-bump
  justification.
- POSSIBLY MODIFIED: `pyproject.toml` — `version`
  bumped only if Q7 = PATCH or MINOR; other
  fields byte-identical.

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
- Track P / Step 1 planning surface byte-identical
  (Track Q does not retro-modify Track P even at
  closure).
- Track Q Step 4 recipe + (if PATH B) `.iss` +
  optional build helper byte-identical.
- All Tracks A–O architecture docs byte-identical.
- Track Q Step 1 / Step 2 / Step 3 / Step 4 /
  Step 5 docs byte-identical.
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
- No bundled-runtime binary committed.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Track Q closed. Sixteen or seventeen
post-phase parallel tracks (A through P/Q,
depending on whether Track P has independently
closed by this point) listed in closure narrative.
README Closed parallel tracks structure updated.
Q7 locked. Operator-facing narrative reflects
Track Q closure (Windows setup.exe path is now a
first-class operator-discoverable surface).
Selfcheck green; verify-release.ps1 green on 8
checks; no real credentials; no `1cv8.exe`; no
remote push; central honest constraint (bundled
Python runtime ~10 MB embedded into the
installer) preserved in the closure narrative.
