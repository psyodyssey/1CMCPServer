# Parallel Track Q — Windows Installer Path and setup.exe Delivery — Baseline Audit

Companion to
[track-q-windows-installer-path-and-setup-exe-delivery-plan.md](track-q-windows-installer-path-and-setup-exe-delivery-plan.md)
and
[track-q-windows-installer-path-and-setup-exe-delivery-step-map.md](track-q-windows-installer-path-and-setup-exe-delivery-step-map.md).

This document is the **Step 2** deliverable of Track Q.
It is **descriptive, not prescriptive**. No RFC 2119
language. No MUST / MUST NOT / SHOULD locks. Every
"decision" is recorded as a directional recommendation
to be either ratified or revised by the Step 3 normative
contract.

The audit lens is deliberately narrow: *what is the
shortest honest path from the current working server
core to `setup.exe` → install → launch → Claude-connect
on an ordinary Windows-user machine, given the Track Q
plan §4 central constraint that a pure-Python codebase
without preinstalled Python structurally requires a
bundled Python runtime inside the installer.*

This document does **not** survey the broader Windows
installer ecosystem. It does **not** rank installer
technologies for use cases Track Q has already rejected
(MDM / SCCM / Intune / Group Policy / Store
publication). It does **not** speculate about a "future
v2" Windows installer. Those framings are explicitly
out of scope per the step-map carry-through list.

---

## 1. Purpose / scope of this audit

You are reading this because Track Q / Step 1 (commit
`9b03edf`) declared a closure-worthy gap — *ordinary
Windows-user setup.exe experience* — and locked Q1–Q7
directional defaults in the plan. Step 2 is the
honesty checkpoint between Step 1's directional
defaults and Step 3's normative contract. Its purpose
is:

- to take inventory of every Windows-install-adjacent
  surface that already exists in the repo, with
  `file:line` anchors, so Step 3 cannot accidentally
  duplicate work or contradict existing recipes;
- to take inventory of what does **not** exist (no
  `.iss` file, no `.wxs` file, no `.nsi` file, no
  bundled CPython binary, no Windows-installer
  recipe, no Add/Remove Programs registration), so
  Step 3 knows exactly what new surface it is
  declaring;
- to classify the inventory into the four standard
  classes Tracks A–O have used (already-reusable /
  adjacent-but-insufficient / clearly-missing /
  explicitly-out-of-scope), so Step 3's file-surface
  cap is grounded;
- to audit honestly the only two structurally
  possible shapes under plan §4 (α bundled
  embeddable CPython vs β frozen executable
  bundling), so Step 3 picks one with evidence;
- to compare the candidate installer technologies
  (Inno Setup / WiX / NSIS / a handful of others)
  on the criteria that actually matter for the
  Track Q gap — *not* on general installer-
  ecosystem criteria;
- to record directional resolutions of Q1–Q6
  grounded in the inventory above, with Q7 left for
  Step 6 framing;
- to hand off a clean ≥10-item list of decisions
  the Step 3 contract is responsible for locking.

What this document is **not**:

- it is **not** a Step 3 contract — no normative
  language, no `MUST`, no "is locked";
- it is **not** an installer-technology survey for
  general Windows-developer audiences — its scope
  is bounded by the Track Q gap;
- it is **not** a comparison of Windows installer
  technologies on enterprise-deployment criteria —
  enterprise-deployment is hard out-of-scope per
  step-map carry-through list;
- it is **not** a recipe an operator can follow to
  produce setup.exe today — that recipe lives at
  Step 4 (under whichever path the Step 3 contract
  ends up locking) and does not exist yet;
- it is **not** authorisation to commit a `.iss`
  file or any installer-definition file — Step 2
  carry-through invariants forbid that surface;
- it is **not** authorisation to commit a binary —
  step-map invariant §1.30 forbids any
  bundled-runtime binary at any step.

The audit avoids one specific anti-pattern: it does
not claim that *cataloguing* the existing
install-adjacent paths plus *listing* installer
technologies *equals* "Windows install solved". It
explicitly does not. Step 2 produces an audit, not a
solution. Step 4 produces a narrow implementation
slice, not a "Windows install solved forever"
artefact. Track Q closure language is reserved for
Step 6.

---

## 2. Ordinary-Windows-user persona reality

The Track Q gap is anchored in a specific persona:
an *ordinary Windows user* who has been handed (a)
some kind of distributable produced by an operator
and (b) the expectation that they can install the
1C Agent Platform on their Windows 10 / 11 amd64
machine without becoming a Python operator
themselves.

What "ordinary Windows user" means, for this audit:

- has Windows 10 or Windows 11 on amd64;
- has a normal user account (administrative
  elevation possible but not assumed);
- does **not** have Python 3.11 (or any Python)
  installed;
- does **not** have `pip` available;
- does **not** have `git` installed;
- does **not** have a PowerShell developer
  workflow;
- has not configured `PATH` for any developer
  tooling;
- expects "download → double-click → Next /
  Install / Finish → it is installed → it appears
  in Start menu → it appears in Add/Remove
  Programs → I can uninstall it";
- does not expect to read a README to find out
  *which Python version* they should install
  first.

What "ordinary Windows user" does **not** mean:

- they are not an IT administrator deploying the
  platform across a fleet of machines (that is the
  enterprise deployment persona, hard out-of-scope
  per step-map);
- they are not a developer reading the source
  tree (Track O / `pip install -e .` is the
  developer surface);
- they are not an operator on a deployment host
  with a controlled environment (that is the
  Track M `pip install <WHEEL_PATH>` persona);
- they are not someone who is going to compile
  CPython themselves;
- they are not someone willing to install Python
  3.11 first as a prerequisite (if they were, the
  Track M path would already work for them — and
  the Track Q gap would not exist).

Current state, against this persona, by direct
inspection of the three install-adjacent paths
inventoried in §3:

| Persona ask                              | `scripts/release/install.ps1` | `pip install <WHEEL_PATH>` | `pip install -e .` |
|------------------------------------------|------------------------------|----------------------------|--------------------|
| Works without preinstalled Python?       | No                           | No                         | No                 |
| Works without `pip`?                     | No                           | No                         | No                 |
| Works without PowerShell familiarity?    | No                           | Borderline                 | No                 |
| Works without `git clone`?               | Yes (if release tree shipped)| Yes                        | No                 |
| Produces Start menu shortcut?            | No                           | No                         | No                 |
| Registers in Add/Remove Programs?        | No                           | No (pip is not registered) | No                 |
| Double-clickable from File Explorer?     | No                           | No                         | No                 |

Every cell that is not "Yes" represents a slice of
the Track Q gap. The audit does not claim that
solving every cell is in Track Q's scope; the
following sections drive at the narrowest honest
slice consistent with "double-click setup.exe →
Next/Install/Finish → it is installed".

---

## 3. Inventory: three existing install-adjacent paths

The repository contains exactly three paths that an
operator could honestly call "an install path",
each scoped to a different persona, each presupposing
preinstalled Python. None of them closes the Track Q
gap; none of them is wrong, either. They are
**orthogonal** to Track Q, not predecessors of
Track Q. The Step 3 contract will need to position
the new installer surface as a fourth orthogonal
boundary, not as a replacement of any of these.

### 3.1 Path I — `scripts/release/install.ps1` (Track B / Track I)

- **File:** `scripts/release/install.ps1`. Companion
  helper `scripts/release/_install_runner.py`.
- **Surface:** PowerShell wrapper that bootstraps
  `PYTHONPATH` via `scripts/dev/bootstrap_paths.ps1`
  and forwards to `onec_platform.run_install_fast_path_from_json_file`
  (implemented in
  `apps/platform/src/onec_platform/installer.py`,
  see `installer.py:_install_runner.py` reference at
  `scripts/release/install.ps1:32`).
- **Persona served:** operator who has the platform
  source tree on disk and needs to materialise a
  product-config JSON from operator-declared inputs.
- **What it does:** preview by default (writes
  nothing); on `-Confirm`, writes the materialised
  JSON product-config to the operator-chosen path
  and re-loads it to confirm readability. Defended
  in `scripts/release/install.ps1:1-26`.
- **What it does NOT do (verbatim from
  `scripts/release/install.ps1:9-11`):** "It does
  NOT introduce a new install ecosystem. No `.msi`,
  no `.deb`, no GUI wizard, no signed distribution."
- **Python prerequisite:** mandatory. The script
  calls `python $runner …` at
  `scripts/release/install.ps1:51`. Without
  preinstalled Python, the script fails immediately.
- **Persona for Track Q:** insufficient. Ordinary
  Windows user does not have Python; does not have
  PowerShell familiarity; does not have a product-
  config JSON authored by hand.

### 3.2 Path II — `pip install <WHEEL_PATH>` (Track M)

- **Recipe:** `docs/operators/packaging/distribution-boundary.md`
  (operator-facing recipe, 11 src-layout packages
  enumerated in `pyproject.toml:51-63`).
- **Surface:** standard Python packaging ecosystem.
  Build with `python -m build`; install with `pip
  install <WHEEL_PATH>`; uninstall with `pip
  uninstall 1c-agent-platform`; upgrade with `pip
  install --upgrade <NEW_WHEEL_PATH>`; verify with
  `mcp-read-server --help`.
- **Persona served:** operator on a deployment host
  they own, who already has CPython 3.11 + pip
  installed and is comfortable in a terminal.
- **What it does:** installs the platform as a
  `py3-none-any` wheel containing the eleven src-
  layout packages; places three console scripts on
  `PATH` (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`); is uninstallable via
  pip.
- **What it does NOT do (verbatim from
  `docs/operators/packaging/distribution-boundary.md:838-841`):**
  ""GUI installer" — denied. There is no "GUI
  installer" and no "wizard". The five lifecycle
  verbs are CLI-driven (`pip`, `python -m build`,
  `mcp-read-server --help`)."
- **Python prerequisite:** mandatory. The first
  step of the recipe is "create or activate a
  Python 3.11 environment with `pip` available".
- **Persona for Track Q:** insufficient. Ordinary
  Windows user does not have a Python 3.11
  environment; pip is not double-clickable; wheels
  are not File Explorer artefacts; Add/Remove
  Programs does not list pip-installed packages.

### 3.3 Path III — `pip install -e .` (Track O)

- **Recipe:** `docs/dev/editable-install-and-workspace-discovery.md`
  (contributor-facing recipe; first-class install
  verb locked at Track O Step 3 §5.1).
- **Surface:** PEP 660 editable install via
  hatchling's default; eleven src-layout packages
  resolved against `pyproject.toml:51-63` directly
  from the working tree.
- **Persona served:** contributor / developer
  editing the source tree, who already has
  Python 3.11 + pip + git installed and has
  cloned the repo.
- **Python prerequisite:** mandatory. The recipe
  opens with venv setup (Windows PowerShell + POSIX
  bash/zsh fenced examples) and `pip install -e .`.
- **Persona for Track Q:** insufficient. Ordinary
  Windows user is not a contributor; does not clone
  the repo; is not building from source.

### 3.4 Cross-cutting observations

All three paths are honest within their personas;
none is a broken installer Track Q replaces. All
three presuppose preinstalled Python — the "honest
gap" is the persona for whom no Python, no pip, no
git, no PowerShell familiarity exists. None
produces a setup.exe; the anchor denials in §4
articulate this as deliberate deferral, not failure.
The Step 3 contract will need to position setup.exe
as a **fourth orthogonal axis**, not a substitute
for any of the three above; each axis continues to
serve its own persona after Track Q closes.

---

## 4. Inventory: three anchor citations

Track Q / Step 1 named three anchor citations as the
grounded justification for the gap. Audit verifies
each anchor verbatim against repo state at HEAD.

### 4.1 Anchor — `scripts/release/install.ps1:9-11`

Verbatim:

> It does NOT introduce a new install ecosystem. No
> `.msi`, no `.deb`, no GUI wizard, no signed
> distribution.

**Audit verdict:** confirmed present at HEAD, byte-
identical to Track B / Step 3 commit, byte-identical
to Track I / Step 4 commit (Track I added 15 LOC
inside `installer.py:_config_to_dict` but did not
touch this comment block). This denial is the
strongest in-repo evidence that "GUI installer" /
"setup.exe" was deliberately deferred by prior
tracks, not forgotten. It also names exactly the
shape Track Q is delivering ("GUI wizard" → minimal
Inno-Setup-class wizard).

### 4.2 Anchor — `docs/operators/packaging/distribution-boundary.md:838-841`

Verbatim (within §13 Honest non-goals):

> **"GUI installer"** — denied. There is no "GUI
> installer" and no "wizard". The five lifecycle
> verbs are CLI-driven (`pip`, `python -m build`,
> `mcp-read-server --help`).

**Audit verdict:** confirmed present at HEAD, byte-
identical to Track M / Step 4 commit. The denial
sits inside §13, which the Track M Step 3 contract
authored as the *honest non-goals* list — explicitly
not a "future improvement backlog", explicitly a
"these shapes are out of scope of this recipe". This
anchor is the cleanest evidence that the wheel-based
distribution boundary deliberately stops short of
the GUI installer persona, and that closing the
GUI-installer gap is a *different track's* job.
That track is Track Q.

### 4.3 Anchor — `pyproject.toml:44-50` (Track M comment block)

Verbatim:

> Explicit non-goals (mirroring the recipe): no
> "PyPI publication", no "signed distribution", no
> "GUI installer", no "Chocolatey / Homebrew / apt
> / conda-forge / NuGet" support, no "enterprise-
> ready" packaging. The build toolchain (`build`)
> remains an operator-side prerequisite — NOT a
> project dependency. The install-fast-path
> (`scripts/release/install.ps1`) and the wheel are
> orthogonal-but-complementary axes; see the recipe.

**Audit verdict:** confirmed present at HEAD, byte-
identical since Track M / Step 4 closure commit
`00a8e1f`. This anchor is the most concise three-
way reconciliation of the existing three paths and
the implicit fourth (Track Q). The pyproject
comment block explicitly says wheel and `install.ps1`
are *orthogonal*, not redundant — and explicitly
says "GUI installer" is **non**-goal of Track M.
Track Q lives in the space those denials defined.

### 4.4 Cross-cutting observation

All three anchors **deny** the GUI installer shape
in identical wording ("GUI installer", "wizard").
None of them frames the denial as a hidden defect or
a planned-but-broken surface. The denial is honest
deferral. The audit's reading: Track Q is **not**
fixing a broken thing; Track Q is **closing a
deliberately deferred gap**. The Step 3 contract's
framing should follow that reading exactly (the
Track Q plan §1 already does so) — Track Q does
not "complete" or "finish" Track B / Track I /
Track M; it adds a fourth orthogonal axis.

---

## 5. Inventory: missing installer-technology files and bundled-runtime binaries

The audit verifies that **none** of the artefacts a
Step 4 implementation would produce exists at HEAD.
Step 4 invariants forbid committing any of these at
Steps 1 / 2 / 3, so this section confirms the
discipline is being preserved.

### 5.1 No installer-technology definition file in repo

Verified by direct repository inspection at HEAD:

- No `*.iss` file (Inno Setup).
- No `*.wxs` file (WiX Toolset).
- No `*.nsi` / `*.nsh` file (NSIS).
- No `installer.iss` / `setup.iss` / `installer.wxs`
  / `setup.wxs` / `setup.nsi` under any path.
- No `installers/` directory; no `installer/`
  directory; no `windows/` directory; no `dist/installer/`
  directory.
- No Squirrel.Windows config (`Squirrel.exe`
  references, `.releases` files).
- No Velopack config.
- No Briefcase config (`briefcase.toml`,
  `pyproject.toml` `[tool.briefcase]` block).
- No PyInstaller spec file (`*.spec`).
- No Nuitka build configuration.
- No `py2exe` / `cx_Freeze` configuration.
- No MSIX manifest (`AppxManifest.xml`).
- No Advanced Installer / InstallShield project
  file.

**Audit verdict:** confirmed. The Step 4 file
surface (under whichever PATH the Step 3 contract
locks) will be entirely new ground.

### 5.2 No bundled-runtime binary in repo

Verified by direct repository inspection at HEAD:

- No `python-3.11.*-embed-amd64.zip` anywhere.
- No `python.exe` / `pythonw.exe` / `python311.dll`
  / `python3.dll` committed.
- No `*.pyd` extension modules committed.
- No frozen `.exe` / `.dll` / `.cab` / `.msi` /
  `.7z` / `.zip` produced by Track B / Track I /
  Track M / Track O.
- No bundled CPython source distribution
  (`Python-3.11.*.tgz`) committed.
- No PyInstaller `dist/` containing platform-
  branded `.exe` files (`dist/` contains exactly
  the Track M wheel + sdist artefacts; nothing
  else).

**Audit verdict:** confirmed. The Step 4 build
helper (under whichever PATH the Step 3 contract
locks) will be expected to fetch the bundled
CPython at build time — *not* to read it from a
committed binary blob. Step-map invariant §1.30
explicitly forbids committing such a blob at any
Track Q step.

### 5.3 No Windows-installer recipe

Verified by direct inspection of `docs/operators/`:

- `docs/operators/deployment-boundary.md` exists
  (Track J).
- `docs/operators/observability.md` exists (Track N).
- `docs/operators/packaging/distribution-boundary.md`
  exists (Track M).
- `docs/operators/service/service-supervision.md`
  exists (Track L).
- `docs/operators/service/mcp-server.service`
  exists (Track L Linux systemd template).
- **`docs/operators/installer/` does not exist.**
- **`docs/operators/installer/windows-setup-exe.md`
  does not exist.**

**Audit verdict:** confirmed. The Step 4 operator-
facing recipe (the new path the Step 3 contract is
expected to lock) will create the `docs/operators/installer/`
sub-tree.

### 5.4 No HKCU Uninstall surface and no Start menu shortcut creator

There is **no** code, script, or installer-definition
in the repo that:

- writes to `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\<key>`;
- writes to `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\<key>`;
- creates a `.lnk` under
  `%APPDATA%\Microsoft\Windows\Start Menu\Programs\`;
- creates a `.lnk` under
  `%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\`;
- creates a desktop `.lnk`;
- modifies user `PATH`.

**Audit verdict:** confirmed. These are
*installer-side* concerns — the installer
technology (Inno Setup / WiX / NSIS) handles them
declaratively; the platform's Python code is *not*
expected to touch them. The Step 3 contract is
expected to lock the installer technology and the
declarative shape (Start menu shortcut: yes;
desktop shortcut: optional, recommended off by
default; `PATH` modification: no).

### 5.5 No Windows-runner CI job

`.github/workflows/dev-check.yml` runs only on
ubuntu-latest. Verified at HEAD:

- No Windows-runner job in `.github/workflows/`.
- No `windows-latest` reference in any workflow.
- No `release.yml` / `installer-build.yml` that
  produces setup.exe in CI.

**Audit verdict:** confirmed. Step-map invariant
§1.22 governs whether Step 4 may extend the
workflow with a Windows-runner installer-build
job; default expectation per the step-map is no
workflow change. This audit does not pre-decide
that question; it is recorded as a Step 3 handoff
item (§12).

---

## 6. Four-class classification

Standard Track classification (mirrors Track O /
Step 2's framing).

### 6.1 Already-reusable

Existing in-repo surfaces that the Step 4 installer
can rely on without modification:

- **Track M wheel build** (`pyproject.toml:34-63`).
  The eleven src-layout packages already build to
  `1c_agent_platform-<VERSION>-py3-none-any.whl`.
  The installer is built **on top of** this wheel
  (step-map invariant §1.24); the wheel itself is
  not modified.
- **Three `[project.scripts]` console entries**
  (`pyproject.toml:22-25`). The three entry points
  `mcp-read-server` / `mcp-write-server` /
  `mcp-intelligence-server` define exactly the
  binaries the bundled-Python launcher will invoke.
- **`onec_platform.run_install_fast_path_from_json_file`**
  (`apps/platform/src/onec_platform/installer.py`,
  650 LOC). The product-config materialisation
  helper that the installer's *post-install*
  optional first-run step (if Step 3 contract
  locks one) can call directly through the bundled
  Python.
- **`onec_platform.runtime`** (`runtime.py`, 1118
  LOC). The product-runtime orchestration boundary;
  the launcher's "start the configured MCP
  server" semantics route through this module.
- **`onec_platform.process_control`**
  (`process_control.py`, 258 LOC). Cross-platform
  liveness probe; survives in the installer-
  launched process exactly as it survives today.
- **`.python-version`** Python 3.11 pin. Defines
  the embeddable CPython version the build helper
  is expected to fetch.

### 6.2 Adjacent-but-insufficient

Existing surfaces that overlap the Track Q persona
but cannot serve it alone:

- **`scripts/release/install.ps1`** (Track B / I) —
  presupposes preinstalled Python; PowerShell-only;
  not double-clickable.
- **`pip install <WHEEL_PATH>`** (Track M) —
  presupposes preinstalled Python + pip; not
  registered in Add/Remove Programs; produces no
  Start menu shortcut.
- **`pip install -e .`** (Track O) — developer-
  only; presupposes git clone + Python + pip + venv.
- **`scripts/dev/launch.ps1`** — developer launch
  umbrella for the source tree; not an installer
  launcher; not invoked from any setup.exe.
- **`docs/operators/service/mcp-server.service`**
  (Track L) — Linux systemd template; wrong OS
  for the Track Q gap.
- **`docs/operators/deployment-boundary.md`**
  (Track J) — operator-controlled deployment-host
  recipe; assumes Python on deploy host;
  orthogonal to setup.exe persona.

### 6.3 Clearly-missing

Surfaces that must be invented (under whichever
PATH the Step 3 contract locks) to close the
Track Q gap:

- A **single `setup.exe` artefact** the ordinary
  Windows user double-clicks.
- An **installer-technology definition** (default
  expectation per plan §10: one `.iss` file
  ≤250 LOC) that declares the install steps
  declaratively.
- A **bundled CPython 3.11 embeddable
  distribution** acquired at build time from
  python.org and packed into setup.exe (default
  expectation per plan §4: `python-3.11.<x>-embed-amd64.zip`
  ~10 MB).
- An **install location**, default expectation
  `%LOCALAPPDATA%\Programs\1C Agent Platform\`
  (Inno Setup `{userpf}` semantics — per-user,
  no admin elevation).
- A **Start menu shortcut**, default expectation
  one shortcut named "1C Agent Platform" under
  `Start Menu\Programs\1C Agent Platform\`
  pointing at the launcher.
- A **launcher wrapper**, default expectation a
  small `.cmd` / `.bat` (or installer-generated
  `.lnk` directly) that invokes the bundled
  Python with the canonical MCP-server console-
  script entry.
- An **HKCU Uninstall registry entry** so the
  product appears in *Settings → Apps → Installed
  apps* / *Control Panel → Programs and Features*
  and is uninstallable through the standard
  Windows surface.
- An **operator-facing Windows-installer recipe**
  under `docs/operators/installer/windows-setup-exe.md`
  documenting build, install, uninstall, upgrade,
  verify on the ordinary-Windows-user persona.
- Optionally: a **PowerShell build helper** that
  fetches the python.org embeddable distribution
  at build time and produces a build directory the
  installer-compiler (e.g. `iscc.exe`) consumes.

### 6.4 Explicitly-out-of-scope

Hard out-of-scope per step-map carry-through list
(lines 183–239). Restated here for clarity, not
expanded:

- No Linux installer (`.deb`, `.rpm`, `.apk`,
  `.AppImage`, `.snap`, `.flatpak`).
- No macOS installer (`.dmg`, `.pkg`, `.app`,
  Homebrew cask, MacPorts, notarization).
- No `.msi` in broad form (WiX considered only if
  this audit surfaces a grounded MDM/SCCM/Intune
  operator need — §8.2 below records that it does
  **not**, so default = Inno Setup setup.exe).
- No Chocolatey / winget / Scoop / NuGet /
  Microsoft Store publication.
- No PyPI publication (Track M non-goal
  preserved).
- No code signing / Authenticode / EV cert /
  notarization / SBOM / SLSA / supply-chain
  attestation.
- No auto-update / OTA / delta-update.
- No GUI dashboard / browser UI / web admin
  panel.
- No service-supervision redesign (Track L
  preserved; installer does **not** register a
  Windows Service by default).
- No auth redesign (Track D / H preserved).
- No transport redesign (Track G / H preserved).
- No new MCP tools / registry change.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new entrypoint module.
- No new project dependencies.
- No new transports (WebSocket, SSE, gRPC, AMQP).
- No remote-dev / DX / IDE integrations (Track O
  preserved).
- No enterprise installer platform (Group Policy
  templates, SCCM packaging, Intune publishing).
- No containerisation.
- No cluster / HA.
- No "all Windows distributions supported" claim
  (default support matrix: Windows 10 + 11 amd64;
  Windows 7, Windows Server, ARM64, x86 not in
  default).
- No "one-click everything solved forever".
- No "enterprise-grade installer".
- No "production-ready desktop app".
- No "GUI config wizard" (the installer drops the
  platform on disk; product configuration is a
  separate operator step using existing surfaces).
- No "Windows service auto-magic by default".
- No test-suite program (Track P territory).
- No observability redesign (Track N preserved).
- No remote push / GitHub release publishing.

---

## 7. Option-space audit under plan §4 — shape α vs shape β

Plan §4 (lines 355–445) names the two structurally
possible shapes that satisfy "no preinstalled Python
on target machine". The audit's job here is to
evaluate each shape against grounded criteria — not
to lock one; the Step 3 contract will lock.

### 7.1 Shape α — bundled embeddable CPython inside setup.exe

**What it is.** The installer carries (or pulls at
install time from python.org) the
`python-3.11.<x>-embed-amd64.zip` distribution
(~10 MB; contains `python.exe`, the standard
library as a `.zip` blob, `python311.dll`, and a
minimal set of `.pyd` extension modules). The
installer extracts this to the install directory
alongside the platform wheel's contents. The
launcher invokes `<install_dir>\python\python.exe -m
mcp_read_server` (or whichever MCP entrypoint is the
default Claude-connect target).

**Pros (evidence-grounded):**

- Uses the **official python.org distribution** —
  same CPython 3.11 the wheel already targets
  (`pyproject.toml:9` `requires-python = ">=3.11"`,
  `.python-version` pin). No build-tool
  divergence; no compiler surface.
- **Smallest installed footprint** of the two
  shapes — roughly 10–15 MB total (10 MB
  embeddable CPython + ~1 MB combined for the
  eleven src-layout packages from `pyproject.toml:51-63`).
- **Smallest build-tool surface** — Step 4 build
  helper is a single PowerShell script that
  fetches a zip from python.org, extracts it
  alongside the wheel contents, and hands a
  directory to Inno Setup's compiler. No
  PyInstaller, no Nuitka, no Briefcase.
- **Trivially auditable.** The embeddable zip's
  contents are listed on python.org; the
  extraction is declarative.
- **Trivially reproducible.** Pinning a specific
  python.org embeddable filename (e.g.
  `python-3.11.9-embed-amd64.zip`) makes the build
  bit-identical across operators.
- **No re-bundling licence question.** The
  python.org embeddable distribution is shipped
  under the PSF licence; redistribution within an
  installer is explicitly permitted by PSF
  licence terms.

**Cons (evidence-grounded):**

- **Footprint is non-trivial** by application
  standards (~10 MB just for Python) — but this
  is the irreducible structural cost of the
  Track Q gap closure under the §4 constraint.
- **Embeddable distribution has limited
  default `pip` support** — the embeddable zip
  ships without `pip` by default. This is **not** a
  problem for Track Q (the installer is not
  expected to run pip post-install; the platform's
  Python sources are extracted alongside the
  embeddable runtime, not pip-installed into it).
- **Two-binary install** (the platform .py
  sources + the bundled python.exe) — the
  launcher script has to know to set
  `PYTHONPATH` (or use `python._pth`) to the
  platform install directory.
- **No native single-file `.exe`.** The user
  sees `python.exe` in the install directory.
  Subjectively this is fine — it is consistent
  with how Python desktop apps look on Windows
  — but it is not "looks like a native Windows
  app" in the Slack-style desktop-shell sense.

**Plan §4 directional lean:** α with python.org
embeddable distribution as the runtime, because β
(see below) multiplies surface area significantly.

### 7.2 Shape β — frozen executable distribution

**What it is.** A build-time tool (PyInstaller /
Nuitka / Briefcase / py2exe / cx_Freeze) consumes
the platform's Python sources and produces
standalone `.exe` files — one per console script,
or a single `.exe` whose argv selects which script
to run. CPython is statically embedded inside each
`.exe`. The installer ships those exes plus their
resource bundles.

**Pros (evidence-grounded):**

- **No `python.exe` visible to the user** — the
  installer drops `mcp-read-server.exe` and the
  user double-clicks it. Subjectively more "native
  Windows app" feeling.
- **Single-file (PyInstaller `--onefile`) is
  possible**, producing one `.exe` per console
  script.

**Cons (evidence-grounded):**

- **Multiplies the build surface** — Track Q
  step-map invariant §1.28 forbids new project
  dependencies, but a frozen-build pipeline
  realistically requires a build-time dependency
  on PyInstaller / Nuitka. The Step 3 contract
  would need to position this as an *operator-
  side prerequisite* (mirroring how Track M
  positions `python -m build`) — fine in
  principle, but expands the build-tooling
  surface meaningfully.
- **Footprint typically larger** (~30–80 MB per
  frozen `.exe` because each one re-embeds
  CPython + stdlib; multiple console scripts
  multiply this unless Step 3 locks a single-
  multiplexed-exe shape).
- **Less auditable.** The frozen `.exe` is an
  opaque blob produced by a third-party tool.
  Operators who want to verify "what's actually
  shipped" have a harder time than with the
  embeddable distribution.
- **Anti-virus heuristic risk.** PyInstaller-
  bundled exes are a known false-positive trigger
  for some Windows AV products; the embeddable
  distribution does not have this property.
- **Step 4 LOC budget pressure.** A PyInstaller
  `.spec` + a wrapping build helper is plausibly
  comparable in size to a `.iss` + a fetch-helper,
  but with substantially more pipeline glue.

**Plan §4 directional lean:** **rejected as
default**. Shape β is not eliminated — Step 3
contract may still pick it, given grounded reason
— but the default expectation locked in plan
§4 is shape α.

### 7.3 Audit recommendation

Audit evidence is consistent with plan §4 default
expectation. **Recommended direction for Step 3
contract: shape α (bundled python.org embeddable
CPython 3.11).** Pinning a specific filename
(`python-3.11.<x>-embed-amd64.zip`, with the `<x>`
pinned to a specific patch version) gives
reproducibility. Shape β remains available as a
fallback if Step 3 contract uncovers a grounded
reason — but audit found none.

---

## 8. Installer-technology comparison — Inno Setup vs WiX vs NSIS vs others

Audit scope: only technologies that could plausibly
produce a `setup.exe` matching the persona criteria
in §2. Technologies that produce `.msi` only
(MSIX, Microsoft Installer-only flows), or that are
update frameworks rather than installers (Squirrel,
Velopack), or that are commercial-only (Advanced
Installer, InstallShield) are not deep-compared.

The criteria audit uses:

- **C1 — produces a single setup.exe** the user
  double-clicks?
- **C2 — supports embedding files** (the
  embeddable CPython zip + the platform sources)
  declaratively?
- **C3 — supports per-user install** (HKCU
  Uninstall registration, no admin elevation
  required)?
- **C4 — supports Add/Remove Programs
  registration**?
- **C5 — supports Start menu shortcut creation**?
- **C6 — supports uninstall as a first-class verb**
  (the user can uninstall through the standard
  Windows surface)?
- **C7 — free and licensable for redistribution
  of the produced setup.exe**?
- **C8 — small build-tool surface** (a single
  compiler binary the operator runs; no large
  framework)?
- **C9 — actively maintained** (recent releases,
  bug-fix activity)?
- **C10 — no auto-update embedded** (Track Q
  hard out-of-scope: "no auto-update / OTA /
  delta-update")?
- **C11 — no Microsoft Store coupling** (Track Q
  hard out-of-scope: "no Microsoft Store
  publication")?

### 8.1 Inno Setup

- C1: yes — Inno Setup's compiler (`iscc.exe`)
  consumes a `.iss` script and produces a single
  `setup.exe`.
- C2: yes — declarative `[Files]` section.
- C3: yes — `PrivilegesRequired=lowest`,
  `DefaultDirName={userpf}\1C Agent Platform`,
  `UsedUserAreasWarning=no`.
- C4: yes — Inno Setup writes the HKCU/HKLM
  Uninstall key automatically; the product
  appears in *Settings → Apps* without manual
  registry code.
- C5: yes — `[Icons]` section.
- C6: yes — Inno Setup ships an uninstaller exe
  alongside setup.exe; uninstall is invoked from
  *Settings → Apps* through the standard Windows
  surface.
- C7: yes — free, modified BSD-style licence,
  redistribution of produced setup.exe
  unrestricted.
- C8: yes — `iscc.exe` is a single ~3 MB binary
  + a Pascal-script-flavoured DSL.
- C9: yes — actively maintained for 25+ years;
  recent releases.
- C10: yes — no embedded auto-updater.
- C11: yes — no Store coupling.

**Audit verdict:** all 11 criteria met. Plan §10
directional default (Inno Setup) is consistent with
audit evidence.

### 8.2 WiX Toolset

- C1: produces `.msi` natively; can wrap as
  `.exe` bootstrapper via Burn.
- C2: yes.
- C3: per-user `.msi` install is supported but
  requires careful `MSIINSTALLPERUSER` /
  `ALLUSERS` configuration; non-trivial.
- C4: yes (MSI auto-registers).
- C5: yes.
- C6: yes (MSI uninstall is native).
- C7: yes — MS-RL licence, free.
- C8: **no** — WiX's surface is substantially
  larger than Inno Setup (XML schemas, Heat /
  Candle / Light tool pipeline, .NET runtime
  dependency for the build host).
- C9: yes — actively maintained.
- C10: yes.
- C11: yes.

**Audit verdict:** WiX is overkill for the Track Q
persona. The MSI ecosystem strengths (MDM / SCCM /
Intune / Group Policy deployability) are explicitly
out-of-scope per step-map line 218. Without those
strengths, WiX is just a heavier Inno Setup.
**Rejected as default**; reconsidered only if Step 3
contract surfaces a grounded MDM / SCCM / Intune
need — and audit confirms no such need is present in
the gap framing of plan §1.

### 8.3 NSIS (Nullsoft Scriptable Install System)

- C1: yes.
- C2: yes.
- C3: yes (per-user install supported via
  `RequestExecutionLevel user`).
- C4: yes (manual registry write in the script).
- C5: yes.
- C6: yes (NSIS generates an uninstaller).
- C7: yes — zlib-style licence.
- C8: yes — single `makensis.exe` binary.
- C9: yes — actively maintained.
- C10: yes.
- C11: yes.

**Audit verdict:** NSIS is comparable to Inno Setup
on every criterion. The differentiators are
**subjective**: NSIS's scripting DSL is harder to
read than Inno Setup's; Inno Setup's defaults
(automatic HKCU Uninstall registration, default
icons, default UI strings) reduce the `.iss`
LOC budget more than NSIS's `.nsi` defaults
reduce the `.nsi` LOC budget. Plan §10 Step 4
LOC cap (≤250 LOC for the installer-definition
file) is more comfortably met by a `.iss` than by
a `.nsi`. **Not rejected, but not preferred over
Inno Setup as default.** Step 3 contract may pick
either; audit lean = Inno Setup.

### 8.4 Other technologies (brief, not deep-compared)

- **PyInstaller / Nuitka / Briefcase / py2exe**:
  these are shape β producers (§7.2), not
  installers in the §8 sense. They produce frozen
  executables, not a setup.exe wizard. To get a
  setup.exe over a frozen-exe pipeline, the
  operator still runs Inno Setup / WiX / NSIS on
  top. **Out of §8 scope by category** (they are
  evaluated in §7.2).
- **Squirrel.Windows / Velopack**: update-
  framework-first; embed auto-update by design.
  Track Q hard out-of-scope ("no auto-update / OTA
  / delta-update"). **Rejected by step-map
  invariant.**
- **MSIX**: Store-coupled; targets the modern
  Windows app model with sandboxing. Track Q
  hard out-of-scope ("no Microsoft Store
  publication"). **Rejected by step-map
  invariant.**
- **Advanced Installer / InstallShield**:
  commercial, paid, requires licensing of build
  tooling. Conflicts with Track Q's "no
  enterprise installer platform" out-of-scope
  framing and with the principle that build tools
  should not require commercial licensing. **Not
  considered.**
- **WiX Burn / dotNetInstaller bootstrapper**:
  evaluated only as wrappers around WiX; same
  reasoning as §8.2 applies — rejected as
  overkill for the Track Q persona.

### 8.5 Audit recommendation

Inno Setup is the directional default — audit
evidence consistent with plan §10. NSIS is the
nearest acceptable alternative. WiX and beyond are
rejected as overkill for the Track Q persona under
the step-map's hard out-of-scope list.

---

## 9. Expected installed footprint per option

Audit estimates only — the Step 3 contract is
expected to pin a supported footprint *range* (the
plan §4 indicative range is 10–15 MB).

| Combination                                                              | Estimated installed footprint | Notes                                                                                                  |
|--------------------------------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------------|
| Shape α (bundled embeddable) + Inno Setup setup.exe                      | ~10–15 MB                     | ~10 MB embeddable CPython + ~1 MB platform sources + Inno Setup runtime overhead (≤1 MB).              |
| Shape α + NSIS setup.exe                                                 | ~10–15 MB                     | Comparable to Inno Setup; NSIS stub is slightly smaller, embeddable CPython dominates total.           |
| Shape α + WiX (`.msi` via Burn)                                          | ~12–17 MB                     | Embeddable CPython dominates; MSI machinery adds ~1–2 MB.                                              |
| Shape β (PyInstaller `--onefile`, single multiplexed exe) + Inno Setup   | ~30–50 MB                     | Each PyInstaller exe re-embeds CPython; single multiplexed exe avoids tripling cost.                   |
| Shape β (PyInstaller, three console-script exes) + Inno Setup            | ~80–150 MB                    | Three exes × ~30 MB each + Inno Setup runtime overhead. Highest cost shape considered.                 |
| Shape β (Nuitka standalone) + Inno Setup                                 | ~40–80 MB                     | Nuitka's standalone mode produces a directory; bundle into Inno Setup; comparable to single-exe range. |

**Audit recommendation:** shape α + Inno Setup at
~10–15 MB is the smallest honest footprint. Step 3
contract is expected to pin this range as supported.

---

## 10. Seven Step 2 framing questions — directional answers

These are the seven framing questions the audit
lens deliberately bounded its scope to. Answers are
**directional**, not normative; Step 3 contract
locks the final wording.

### 10.1 What exactly should setup.exe install?

Directional answer: a **minimal honest payload** —
nothing more. Concretely:

- **Bundled CPython 3.11 embeddable distribution**
  (~10 MB, default expectation: pinned filename
  from python.org pulled at build time, **not**
  committed to git per step-map invariant §1.30).
- **Platform sources** — the eleven src-layout
  packages from `pyproject.toml:51-63` (~1 MB
  combined), extracted into the install directory
  in their importable layout. **Not the wheel
  itself** as a `.whl` — the installer is built
  on top of the wheel's contents, not pip-
  installed from it inside setup.exe.
- **A minimal launcher** — a `.cmd` (or installer-
  generated `.lnk` referencing the bundled
  `python.exe`) that invokes the canonical MCP-
  server console-script through the bundled
  Python.
- **Start menu shortcut** — one shortcut named
  "1C Agent Platform" under
  `Start Menu\Programs\1C Agent Platform\`
  pointing at the launcher.
- **HKCU Uninstall registry entry** — written
  declaratively by Inno Setup so the product
  appears in *Settings → Apps* with an uninstall
  action.

What setup.exe does **not** install:

- No 1C platform binaries (`1cv8.exe` etc).
  The 1C platform itself is operator-supplied;
  the agent platform integrates with whatever
  1C the operator has on their machine.
- No infobases / `.1cd` files / real credentials.
- No test suite (Track P territory).
- No `scripts/*` operator scripts — those are
  control-host artefacts, not end-user
  artefacts.
- No auto-updater.
- No GUI configuration wizard.
- No Windows Service registration by default.
- No `PATH` modification (the launcher invokes
  the bundled python by absolute path).

### 10.2 Can we honestly do without bundled Python?

Directional answer: **no, not honestly**, under
the Track Q persona. Plan §4 locks this
structurally:

- The platform is a pure-Python codebase.
- The persona is "no preinstalled Python on
  target machine".
- The two shapes that satisfy this honestly are
  α (bundled embeddable) and β (frozen exe);
  both shapes **include** Python in some form.

Specifically rejected as "honest alternatives":

- "Just bundle pip and let it install Python on
  demand." Pip itself requires Python; chain
  is circular.
- "Silent download of Python from python.org at
  install time." Either it does (which is α
  with the embeddable zip pulled at install
  rather than at build) or it doesn't (which
  fails persona acceptance).
- "Document Python 3.11 as a prerequisite." That
  is exactly the current state; the gap remains
  open.

Direction for Step 3: **bundled Python is the
structural cost** of the Track Q gap closure.
Pinning shape α with the python.org embeddable
distribution is the smallest honest
implementation of that cost.

### 10.3 Where should the installed server live?

Directional answer: **`%LOCALAPPDATA%\Programs\1C Agent Platform\`**
(Inno Setup `{userpf}` semantics, per-user install).

Why not `C:\Program Files\1C Agent Platform\`
(`{pf}`, per-machine):

- Per-machine install requires UAC elevation;
  the persona may not have admin rights;
  elevating expands the security boundary of the
  Track Q closure scope significantly.
- Per-user install registers the product under
  `HKCU\…\Uninstall\<key>` — visible to the
  installing user in *Settings → Apps* without
  admin elevation, uninstallable without admin.
- Per-user install does not modify shared
  system state.

The Step 3 contract may decide otherwise (e.g.
locking *per-machine* as default if the audited
persona is "shared workstation"); the audit
direction is **per-user** because the persona
description in §2 of this audit and plan §3 does
not name a shared-workstation use case.

### 10.4 How does the user launch the system after install?

Directional answer: **Start menu shortcut →
minimal launcher → bundled Python → canonical MCP-
server console script**, in that order.

Concrete shape (directional, not locked):

```
Start Menu / Programs / 1C Agent Platform /
  ↳ "1C Agent Platform" .lnk
      ↳ %LOCALAPPDATA%\Programs\1C Agent Platform\launch.cmd
          ↳ %LOCALAPPDATA%\Programs\1C Agent Platform\python\python.exe
              -m mcp_read_server   (or whichever entry Step 3 locks)
```

The launcher script's whole job is:

- to set `PYTHONPATH` (or use a `python._pth`
  file in the bundled-Python directory) so the
  bundled interpreter finds the eleven src-
  layout packages;
- to invoke `python.exe -m <module>` for the
  canonical console-script target;
- to keep the foreground process attached to a
  console window (stdio transport for Claude-
  connect).

What it does **not** do:

- No GUI shell.
- No control window with start/stop buttons.
- No tray icon.
- No background Windows Service registration.

The Step 3 contract may add an *optional* second
launcher variant (e.g. `mcp-write-server-launch.cmd`)
if Step 2 evidence warrants. Default expectation:
**one launcher, one Start menu shortcut**.

### 10.5 What is minimally required to choose a 1C base?

Directional answer: **setup.exe does not solve 1C
base selection.** The base-selection / product-
config-JSON-authoring concern is **separately**
addressed by the existing install-fast-path
(`onec_platform.run_install_fast_path_from_json_file`,
already present in `installer.py`, 650 LOC).

Track Q Step 4 closure does not require closing
the base-selection concern. Specifically:

- After setup.exe finishes, the user has the
  platform installed and a launcher in Start menu.
- The product-config JSON (path to `1cv8.exe`,
  path to infobase) is still produced via the
  existing install-fast-path workflow — exactly
  as today, through the bundled-Python launcher
  invoking the existing helper if Step 3
  contract chooses to wire a first-run prompt.
- Track Q does not invent a GUI config wizard
  (step-map hard out-of-scope, line 230).

Direction for Step 3 contract: lock that
setup.exe's responsibility ends at "platform on
disk + launcher + Start menu shortcut + Uninstall
registry". The base-selection / config-JSON
workflow remains an existing-surface operator
step, possibly orchestrated through the launcher
on first run if Step 3 explicitly authorises that
optional shape (default expectation: no — keep
setup.exe minimal).

### 10.6 Is a launcher / control window required for the first version?

Directional answer: **launcher yes, control
window no**.

- **A minimal launcher is required** to give the
  Start menu shortcut a target — without it,
  there is nothing for the user to double-click
  after install. The launcher is a single
  `.cmd` (or installer-generated `.lnk`); LOC
  budget under 30 lines.
- **A "control window" (GUI for start / stop /
  status) is not required** and is *out of
  scope*. Track Q hard out-of-scope list (step-
  map line 204) excludes GUI dashboards. A
  control window would expand scope
  significantly (Qt / .NET / Electron framework
  pull-in; new dependencies; new build surface
  — all forbidden by step-map invariants
  §1.28 and §1.30).

Direction for Step 3 contract: **lock launcher
required, control window forbidden**. A future
track may revisit the control-window concern;
Track Q deliberately does not.

### 10.7 Can the first MVP skip Windows Service?

Directional answer: **yes**.

Evidence:

- Track L is preserved byte-identical by step-map
  invariant §1.4. Track L's Linux systemd
  template is the only service-supervision
  surface in the repo; there is no Windows
  Service surface.
- `apps/platform/src/onec_platform/runtime.py:28-30`
  explicitly disclaims "daemon manager / service
  manager (no Windows Service / systemd unit
  registration on this step)" — this disclaim
  applies through Track Q (no production code
  change at any Track Q step).
- Track Q hard out-of-scope (step-map line 233)
  explicitly forbids "Windows service auto-magic
  by default".
- Claude-connect is **stdio-based** through the
  launcher process; the launcher running in
  foreground is sufficient.

Direction for Step 3 contract: lock "no Windows
Service registration by default; the installer
drops the platform on disk and creates a Start
menu shortcut; service-supervision (if any) is
a separate operator concern using existing
Windows tooling (`sc.exe`, Task Scheduler, NSSM)
explicitly out of Track Q closure scope". A
future track may add a Windows Service surface;
Track Q deliberately does not.

---

## 11. Q1–Q6 directional resolutions grounded in audit evidence

Mirroring the plan §12 directional defaults,
refined by §3–§10 audit evidence above.

### 11.1 Q1 — closure-gate scope

**Plan §12 direction:** closure-gate = ordinary
Windows user downloads single `setup.exe`, double-
clicks, sees Next/Install/Finish, gets Start menu
shortcut, can launch, can uninstall via standard
Windows surface.

**Audit refinement:** consistent with evidence. No
revision. The §2 persona reality, §6.3 clearly-
missing list, and §10 question-answers all align.
The Step 3 contract should add **one explicit
exclusion** the plan did not name: "does not
include 1C base selection / product-config-JSON
authoring; those remain existing-surface operator
steps". §10.5 surfaced this exclusion.

### 11.2 Q2 — installation story

**Plan §12 direction:** the installer is built **on
top of** the Track M wheel, not over it; wheel
artefact byte-identical (step-map invariant §1.24).

**Audit refinement:** consistent. §3.2 and §6.1
confirm. No revision.

### 11.3 Q3 — default artefact class

**Plan §12 direction:** single `setup.exe` (Inno
Setup default; WiX considered only on grounded
MDM/SCCM/Intune need).

**Audit refinement:** consistent. §8.5 confirms
Inno Setup direction. NSIS is the nearest
acceptable alternative; WiX rejected. Step 3
contract may pick either Inno Setup or NSIS; audit
direction = Inno Setup.

### 11.4 Q4 — bundled-runtime shape

**Plan §12 direction:** α (bundled embeddable
CPython 3.11 via python.org).

**Audit refinement:** consistent. §7.3 confirms.
Step 3 contract should pin a specific embeddable
filename (e.g. `python-3.11.<x>-embed-amd64.zip`)
to make builds reproducible. Audit does not name
a specific patch version — that is a Step 3
decision aligned with the current `.python-version`
pin.

### 11.5 Q5 — install location and uninstall surface

**Plan §12 direction:** per-user install
(`{userpf}`); HKCU Uninstall registration.

**Audit refinement:** consistent. §10.3 confirms.
Step 3 contract should explicitly lock "no UAC
elevation by default; no `PATH` modification".

### 11.6 Q6 — production code byte-identical

**Plan §12 direction:** zero production code
change across all six Track Q steps.

**Audit refinement:** consistent. Step-map
invariant §1.1 enumerates the byte-identical files
exhaustively; §6.1 confirms the existing
production code (the `installer.py` /
`runtime.py` / `process_control.py` /
`bootstrap.py` surfaces, plus the three console-
script entries) is *reused* by Track Q, not
modified. No revision.

### 11.7 Q7 — version-bump framing

**Plan §12 direction:** PATH B (recipe + `.iss` +
optional build helper) → PATCH default. PATH A
(docs-only) → NO-BUMP default. PATH C
(installer-definition-only, no recipe) →
rejected. MINOR available if the Step 3 contract
declares a new operator-visible surface (Add/Remove
Programs registration counts as one).

**Audit refinement:** directional only — Q7 is
framed at Step 6, not Step 3. Audit notes that
PATH B is the most likely path because PATH A
(docs without `.iss`) is unbuildable, mirroring
the Track M §6.1 "zero buildable wheel" anti-
pattern. Q7 framing recorded as **NO-BUMP /
PATCH / MINOR all live**, to be locked at
Step 6.

---

## 12. Step 3 handoff list

Items the Step 3 normative contract is responsible
for locking. ≥10 items per Step 2 deliverable
contract.

1. **Installer technology**: lock Inno Setup as
   default (audit direction §8.5). If NSIS is
   picked instead, the contract must record the
   grounded reason. WiX rejected.
2. **Bundled-runtime shape**: lock α (python.org
   embeddable CPython 3.11). Pin a specific
   embeddable filename / patch version against
   `.python-version`. Lock that the embeddable is
   fetched at build time, **not** committed to git.
3. **Install location**: lock per-user under
   `%LOCALAPPDATA%\Programs\1C Agent Platform\`
   (Inno Setup `{userpf}`). Lock "no UAC
   elevation by default" and "no `PATH`
   modification".
4. **Start menu shortcut**: lock single shortcut
   under `Start Menu\Programs\1C Agent Platform\`
   pointing at the launcher; lock that no desktop
   shortcut is created by default.
5. **Launcher shape**: lock the launcher
   (`.cmd` / `.lnk`) as required Step 4 artefact;
   lock LOC budget (audit suggests ≤30 LOC);
   lock that no control-window GUI is part of
   Step 4.
6. **Uninstall surface**: lock HKCU Uninstall
   registry registration through Inno Setup
   defaults; lock that *Settings → Apps* shows
   the product; lock that uninstall removes the
   install directory but **does not** touch
   operator-side artefacts (mirrors Track M
   §7.3 uninstall denial wording).
7. **Step 4 PATH**: lock PATH B (recipe +
   `.iss` + optional build helper). PATH A
   docs-only and PATH C definition-only both
   rejected by audit §11.7 reasoning.
8. **Step 4 file surface**: lock the new files
   exactly:
   (i) NEW `docs/operators/installer/windows-setup-exe.md` — operator recipe;
   (ii) NEW `installers/windows/setup.iss` (or whichever path the contract locks) — Inno Setup definition;
   (iii) OPTIONAL NEW `installers/windows/build-setup-exe.ps1` — build helper that fetches the embeddable CPython at build time and invokes `iscc.exe`.
   Lock LOC caps (audit suggests ≤1200 LOC for
   recipe, ≤250 LOC for `.iss`, ≤200 LOC for
   build helper).
9. **Forbidden-files surface for Step 4**:
   enumerate exhaustively what Step 4 MUST NOT
   touch. Must include at minimum: all of
   `apps/*/src/`, all of `packages/*/src/`,
   `pyproject.toml`, all of `scripts/*`,
   `SECURITY.md`, `docs/release-handoff.md`,
   `apps/platform/README.md`, `CHANGELOG.md`,
   manuals, existing operator recipes,
   `.python-version`, registry surfaces, CI
   workflow (default expectation; the contract
   may authorise a narrow Windows-runner job in
   `.github/workflows/dev-check.yml` only if it
   ships a grounded reason).
10. **No-binary invariant**: lock step-map
    §1.30 in normative form — Step 4 commits no
    `.zip`, `.exe`, `.dll`, `.pyd`, `.msi`,
    `.cab`, `.7z`, `.tar.*`, `.gz`, `.bz2`,
    `.xz`, or any other binary artefact.
11. **Supported installed footprint range**:
    lock 10–15 MB as audit-suggested supported
    range (§9). Step 3 contract may pick a
    slightly different range with grounded
    reason.
12. **Supported Windows matrix**: lock Windows
    10 + 11 amd64; explicitly deny Windows 7 /
    Windows Server / ARM64 / x86 (step-map
    line 224–226).
13. **Honest non-goals**: lock the §13-class
    denial list mirroring Track M's recipe §13.
    Must include at minimum: "no `.msi`", "no
    Chocolatey / winget / Scoop / NuGet / Store",
    "no code signing", "no auto-update", "no
    GUI dashboard", "no GUI config wizard", "no
    Windows Service auto-magic", "no enterprise
    installer", "no all-Windows-distributions
    claim", "no one-click-everything-solved
    claim".
14. **Relationship to existing four axes**: lock
    that the Track Q installer is a **fourth
    orthogonal axis** alongside Track B/I
    install-fast-path, Track M wheel install,
    and Track O editable install. None
    deprecates any other.
15. **Verification protocol**: lock the closure-
    gate scenario — ordinary Windows 10/11
    amd64 machine without preinstalled Python →
    download setup.exe → double-click → wizard
    completes → Start menu shortcut present →
    *Settings → Apps* shows entry → launcher
    starts → MCP server attached to stdio →
    Claude-connect successful → uninstall via
    Windows surface → install directory removed
    → *Settings → Apps* no longer shows entry.
    Lock the verification commands at the
    granularity Track K / Track N use.
16. **Q7 framing**: defer to Step 6 per Track
    M / Track L / Track O precedent. Step 3
    contract records NO-BUMP / PATCH / MINOR
    all live, with PATCH the audit-leaning
    default under PATH B.

---

— end of audit —
