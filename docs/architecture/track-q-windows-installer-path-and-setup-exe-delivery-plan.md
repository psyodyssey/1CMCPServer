# Parallel Track Q — Windows Installer Path and setup.exe Delivery — Plan

**Track status at the time of this document.** Parallel
Track Q opens as the seventeenth post-phase parallel
track, alongside Parallel Track P — Test Suite Shipping
and Verification Boundary (currently at Step 1 planning
only, commit `d6f1936`). Step 1 of Track Q —
**planning only**; documentation-only. No production
code change. No `pyproject.toml` change. No
`scripts/*` change. No registry change. No `1cv8.exe`
runs. No remote push. No Track P deliverable touched.

**Track Q positioning relative to Tracks A–P.** Sixteen
post-phase parallel tracks have opened sequentially in
the order A real-write-path, B productization,
C packaging, D credentials hardening, E version-matrix
scaffolding, F rollback expansion, G stdio transport +
CLI, H HTTP transport + bearer auth, I installer auth
round-trip integrity, J TLS and reverse-proxy
deployment boundary, K real MCP client integration
test, L service supervision and OS service
registration, M packaging ecosystem and distribution
boundary, N observability and diagnostics boundary,
O dev-time editable install and workspace discovery,
P test suite shipping and verification boundary
(opened, currently at Step 1 planning only). After
Tracks A–O closure and Track P / Step 1 opening, the
platform has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer
  auth (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip
  integrity, invoked through
  `scripts/release/install.ps1` (Track I);
- an operator-facing deployment-boundary recipe
  (Track J);
- a real MCP client smoke harness (Track K);
- an operator-facing service-supervision recipe and a
  declarative systemd unit-file template (Track L);
- a single buildable pure-Python wheel
  (`1c_agent_platform-0.5.2-py3-none-any.whl`) and an
  operator-facing distribution-boundary recipe
  (Track M);
- an operator-facing observability/diagnostics recipe
  with FC1–FC7 first-class signals and a triage
  recipe (Track N);
- a contributor-facing dev-time editable install /
  workspace discovery recipe with first-class
  `pip install -e .` and recommended-only
  `bootstrap_paths.ps1` (Track O);
- a Track P planning surface (plan + step-map) for a
  future shipped automated test suite (Track P, in
  progress, not closed).

What it still does **not** have — and what no prior
track addressed — is a **Windows setup.exe install
path** for an ordinary Windows end user who does not
have Python, pip, or Git installed on the box.

That gap is the **only** subject of Track Q.

---

## §1. Purpose — why this track exists

Track Q exists to convert the current honest gap

> "The platform has a wheel/pip distribution boundary
> (Track M) and an install fast-path PowerShell
> wrapper (Track B / Track I) — but both presuppose
> that the operator already has Python 3.11, pip, and
> (for `pip install` from a Git source) Git installed
> on the Windows machine. An ordinary Windows end
> user who has only Windows and a downloaded
> `setup.exe` cannot today install this platform by
> double-clicking that one file. No `setup.exe` exists
> in the repository, in `dist/`, or in any release
> artefact. No bundled-runtime installer artefact
> exists. The wheel/pip path is a **packaging path**
> (correct, working, Track M shipped) — it is **not**
> a Windows installer path."

into a disciplined six-step closure track using the
same shape as Tracks A–P (planning → audit → contract
→ narrow implementation → docs alignment → final
integration pass).

The gap is **not** a defect in Track M. Track M
correctly framed itself as packaging/distribution
boundary (`py3-none-any` pure-Python wheel,
operator-side `pip install <WHEEL_PATH>` lifecycle).
Track M's recipe at
`docs/operators/packaging/distribution-boundary.md`
explicitly lists "no GUI installer" in its non-goals
(§7) and explicitly defers any installer-experience
question. Track Q is the **dedicated narrow track**
that takes that deferred question and gives it a
six-step shape — without expanding it into anything
broader than one honest Windows installer path.

The recommended-next-track candidates list in
`PROJECT-STATUS.md` (see the closure block at
roughly line 16920) explicitly named "broader
packaging ecosystem track (`.msi` / `.deb` / `.rpm`
/ `.dmg` / `.pkg` / signed distribution chain /
PyPI publication / multi-package-manager
publication)" among the recommended candidates.
Track Q is **not** that broader candidate. Track Q
narrows that candidate sharply: **Windows only,
setup.exe only, one technology choice, no
`.msi`/`.deb`/`.rpm`/`.dmg`/`.pkg`/`.snap`/`.flatpak`
ecosystem, no PyPI publication, no signing, no
multi-package-manager matrix**. The broader
candidate remains available as a separate future
track; Track Q does not absorb it.

---

## §2. Current post-Tracks-A–O baseline relevant to Track Q

The relevant baseline for Track Q (as of `d6f1936`,
the Track P / Step 1 planning commit, which itself
did not touch any installer-relevant surface):

### §2.1 What an ordinary Windows user actually has today

An ordinary Windows end user, after a fresh Windows 11
install, has by default:

- Windows + PowerShell 5.1.
- No Python.
- No pip.
- No Git.
- No Visual Studio build tools.
- No `1cv8.exe` (unless they install the 1С platform
  separately).

The README "Системные требования" block
(`README.md:468-473` after the Track P / Step 1
edit) declares as prerequisites:

- Windows + PowerShell 5.1 / 7+;
- Python 3.11 (`.python-version` pin);
- optional `1cv8.exe` for real binary-backed write
  path.

For the "ordinary Windows user" persona, two of
those three prerequisites (Python 3.11; Git, used by
many install flows) are **not present by default**.

### §2.2 What the platform ships for installation today

Three distinct install-adjacent surfaces exist in the
repo, all of which presuppose Python being already
installed:

- **`scripts/release/install.ps1`** (Track B / Step 3
  + Track I round-trip integrity). A "thin scripts-
  only wrapper" — its umbrella comment at lines 1–11
  is verbatim explicit: "It does NOT introduce a new
  install ecosystem. No `.msi`, no `.deb`, no GUI
  wizard, no signed distribution." It bootstraps
  `PYTHONPATH` via `scripts/dev/bootstrap_paths.ps1`
  and forwards to a Python helper
  (`scripts/release/_install_runner.py`). It requires
  Python 3.11 to already be on `PATH`.
- **`pip install <WHEEL_PATH>`** (Track M / Step 4).
  The buildable `1c_agent_platform-0.5.2-py3-none-any.whl`
  wheel is installed by an operator via `pip
  install`. The wheel install verb is the operator-
  facing lifecycle verb pinned by Track M / Step 3
  contract §6.3. It requires Python 3.11 + pip
  already on `PATH`.
- **`pip install -e .`** (Track O / Step 4). The
  contributor-facing editable install verb. Also
  requires Python 3.11 + pip + a git clone of the
  repo. Strictly a developer-facing path.

None of these three is a Windows installer in the
double-click `setup.exe` sense. All three start from
the assumption that a working Python toolchain
already exists on the machine.

### §2.3 What the platform does NOT ship for installation

- **No `setup.exe`.** The string `setup.exe` does
  not appear in any committed source file, recipe,
  or release artefact. The `dist/` directory at
  HEAD `d6f1936` contains only the wheel (and, by
  the Track M recipe's instructions, optionally a
  sdist) produced by `python -m build`.
- **No bundled Python runtime artefact.** Neither
  `python-embed-*.zip` from python.org's
  embeddable distribution, nor any other bundled
  CPython binary, is present in the repository or
  produced by any committed build script.
- **No installer-technology definition file.** No
  Inno Setup `.iss`, no WiX `.wxs`, no NSIS `.nsi`,
  no Advanced Installer `.aip`, no MSIX manifest,
  no InstallShield project file, no Visual Studio
  setup project — none of these exist anywhere in
  the repository.
- **No GitHub Releases setup.exe asset.** GitHub
  Releases publishing is, per repeated explicit
  non-goal denials in Tracks B/C/M, an operator
  action and not part of any track.
- **No Authenticode signing pipeline.** Code
  signing was never in any prior track's scope and
  is explicitly excluded from Track Q (see §7).
- **No Windows Add/Remove Programs registry
  entry.** Pip-installed wheels do not register
  themselves under
  `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall`
  or its `HKCU` / `WOW6432Node` siblings — that
  registry surface is owned by Windows installer
  technologies, not by pip.
- **No `Programs and Features` / `Settings → Apps`
  uninstall entry.** Same reason as above.

### §2.4 Explicit anchors that point at this gap

Three anchor citations make the gap independently
verifiable at HEAD `d6f1936`:

- **`scripts/release/install.ps1:1-11`** — umbrella
  comment block stating "No `.msi`, no `.deb`, no
  GUI wizard, no signed distribution."
- **`docs/operators/packaging/distribution-boundary.md`
  §7 non-goals** (Track M recipe, committed in
  `31313db`) — verbatim names "no GUI installer"
  among the non-goals.
- **`pyproject.toml`** lines 44–50 (Track M comment
  block inside the `[tool.hatch.build.targets.wheel]`
  block) — verbatim "no GUI installer", "no
  Chocolatey / Homebrew / apt / conda-forge /
  NuGet", "no enterprise-ready packaging".

These three anchors are not contradictions;
they are honest **deferrals**. Track Q closes the
deferral with a narrow shape — without violating
any non-goal Track M committed to (Track M's "no
GUI installer" non-goal is **inside Track M's
scope**; Track Q is a separate track that opens its
own scope where this non-goal does not apply).

### §2.5 What Track Q therefore must close

A first-class **Windows setup.exe install path** for
an ordinary Windows end user who is not assumed to
have Python, pip, or Git installed, where the user
experience is:

1. Download `setup.exe`.
2. Double-click.
3. Click **Next** → **Install** → **Finish**.
4. The platform is installed.
5. Uninstall is reachable through the standard
   Windows Add/Remove Programs surface (or its
   modern Settings → Apps equivalent).

with guidance and at most one narrow installer-
definition slice (e.g., one `.iss` file for Inno
Setup), plus a recipe documenting the boundary,
**without** silently expanding into Linux/macOS
installers, broader package-manager publication,
code signing, auto-update, GUI dashboards,
configuration wizards, service-supervision auto-
magic, or enterprise installer platforms.

The track must close the gap **honestly**: it does
not promise "Windows install solved forever",
does not promise "enterprise-grade installer",
does not promise "production-ready desktop app",
does not promise "all Windows distributions
supported", does not promise "one-click everything
solved forever", does not promise "GUI config
wizard", does not promise "Windows service auto-
magic by default". It promises **one** documented
Windows installer boundary plus (at Step 4) a
narrow implementation slice that, in combination
with a bundled Python runtime, lets an ordinary
Windows user reach a Next/Install/Finish flow
exactly once, with uninstall as a first-class part
of the supported boundary.

---

## §3. Honest gap statement

Six observations, each independently verifiable in
the repo at `d6f1936`:

1. **No `setup.exe` exists.** Filesystem check on
   `dist/`, `release/`, repo root, `scripts/*`,
   `docs/*` confirms no `*.exe` artefact named
   `setup.exe` (or any analogous installer
   binary) is shipped or built by any committed
   script.
2. **No installer-technology definition file
   exists.** No `*.iss`, no `*.wxs`, no `*.nsi`,
   no `*.aip`, no `Package.appxmanifest`, no
   `setup.bdsproj`, no Visual Studio setup
   project file exists anywhere in the
   repository.
3. **No bundled Python runtime exists.** Neither
   `python-3.11.*-embed-*.zip` nor any other
   embeddable / portable CPython distribution is
   committed to the repository or pulled by any
   committed build script. The honest Windows-
   installer-without-preinstalled-Python path
   **structurally requires** such a runtime to be
   present somehow — see §4 below.
4. **All three existing install-adjacent surfaces
   presuppose Python.** `scripts/release/
   install.ps1`, `pip install <WHEEL_PATH>`, and
   `pip install -e .` all require an already-
   installed Python 3.11 toolchain. None reaches
   an ordinary Windows user who lacks Python.
5. **Repo anchors explicitly defer the GUI/
   installer question.** Three anchor citations
   (`scripts/release/install.ps1:1-11`,
   `docs/operators/packaging/distribution-boundary.md
   §7`, `pyproject.toml` Track M comment block)
   verbatim name "no GUI installer" / "no `.msi`"
   among the explicit non-goals of prior tracks.
   Those non-goals were honest deferrals, not
   permanent closures.
6. **The recommended-next-track candidates list
   names this territory.**
   `PROJECT-STATUS.md` (closure block roughly at
   line 16920) names "broader packaging ecosystem
   track (`.msi` / `.deb` / `.rpm` / `.dmg` /
   `.pkg` / signed distribution chain / PyPI
   publication / multi-package-manager
   publication)" among the recommended-next-track
   candidates. Track Q narrows that candidate to
   Windows-setup.exe-only and opens it.

The gap is real. It is not closed by Track M's
wheel (different audience: operator with Python
already on the box, not ordinary end user). It is
not closed by Track B's `install.ps1` (same
audience constraint). It is not closed by Track O's
`pip install -e .` (developer-facing). It is not
closed by the recommendation lists in PROJECT-
STATUS (recommendations are not shipped
installers).

---

## §4. Central honest constraint — bundled Python runtime

This section is deliberately prominent, not a
footnote. It states the structural truth that the
remaining sections of this plan, the Step 2 audit,
the Step 3 contract, and the Step 4 implementation
must all respect.

**The platform is a pure-Python codebase.** Track M
ships `py3-none-any` wheel, declaring three console
scripts (`mcp-read-server`, `mcp-write-server`,
`mcp-intelligence-server`) implemented in Python
3.11+ source under eleven src-layout packages. At
runtime, the platform requires a CPython 3.11
interpreter and the standard library. There is no
ahead-of-time compilation step, no PyInstaller-
style executable bundling, no Nuitka compilation,
no MyPyC AOT — none of those is in scope of any
prior track or of Track Q.

Therefore, an **honest Windows installer path that
does not require preinstalled Python** has exactly
two structurally possible shapes:

- **(α) Bundled Python runtime inside the
  installer.** The `setup.exe` itself contains (or
  downloads at install time) an embeddable CPython
  distribution — the standard supported option is
  `python-3.11.<x>-embed-amd64.zip` from
  python.org's official downloads page (a ~10 MB
  zip containing `python.exe`, the standard
  library as a `.zip`, `pythonXY.dll`, and a
  minimal set of `.pyd` modules). The installer
  extracts this into the install directory
  alongside the platform's wheel contents and
  arranges for the three console scripts to be
  invoked through the bundled interpreter.
- **(β) Frozen executable distribution.** The
  installer contains pre-built executables produced
  by PyInstaller, Nuitka, Briefcase, py2exe, or a
  similar tool. The three console scripts become
  standalone `.exe` files at build time; the
  installer ships those exes plus their resource
  bundles.

There is **no** structurally honest third option
that satisfies "no preinstalled Python on the
target machine". Specifically, the following are
**not** honest options:

- "Just `pip install` it from inside the
  installer." Pip itself requires Python; the chain
  is circular if Python is not already present.
- "The installer auto-downloads Python silently
  from python.org." Either it does (which is
  option α with `embed.zip` pulled at install time
  instead of at build time), or it doesn't and the
  user sees a Python prerequisite — which fails
  the gap acceptance.
- "The user can install Python first." That is
  exactly the current state and exactly the
  acceptance failure.

The Step 2 baseline audit must inventory both
shapes (α) and (β) honestly. The Step 3 contract
must lock one of them (default expectation: α with
the python.org embeddable distribution as the
runtime, because β multiplies the surface area
significantly with PyInstaller / Nuitka tooling
that is not currently in the repo). Track Q's
narrow Step 4 implementation default expectation
is shape (α) bundled-embeddable.

Track Q **must call this constraint out loudly**
in every closure-facing document. Not as a
footnote, not as a small warning, not as a
parenthetical. It is the **central design
constraint** of the entire track. A Windows
installer that requires preinstalled Python is not
the deliverable Track Q is closing; a Windows
installer that bundles a Python runtime is.

This constraint also defines a **non-trivial
installed footprint**. Embeddable CPython adds
roughly 10 MB; the eleven src-layout packages add
roughly under 1 MB combined; total footprint
roughly 10–15 MB. That is not "tiny", but it is
honest, and it is the minimum cost of the gap
closure. Step 3 contract should pin this expected
range as the supported installed footprint cap.

---

## §5. Goal of the track

By Step 6 closure, Track Q must have delivered:

1. A single normative Windows-installer-path-and-
   setup.exe-delivery contract (Step 3) that pins
   the closure-gate scope, the installer-technology
   choice (default expectation: Inno Setup;
   alternatives considered only if Step 2 audit
   surfaces a grounded reason), the bundled Python
   runtime shape (default expectation: python.org
   embeddable distribution α), the install
   directory default, the launch surface, the
   uninstall verb, the supported installed
   footprint, the file surface for Step 4, and the
   verification protocol.
2. Either a single operator-facing Windows-
   installer recipe (PATH A docs-only) **or** that
   recipe plus a narrow installer-technology
   definition slice (PATH B docs + one `.iss` or
   equivalent) **or** that recipe plus a narrow
   non-product build helper (PATH C) — depending
   on Step 3 contract Q3 lock. Step 4 is the only
   step that may add files beyond docs.
3. Honest closure narrative in README / PROJECT-
   STATUS / CHANGELOG that documents what Windows
   installer boundary Track Q settled, what it
   explicitly did NOT solve, and what remains out
   of scope (Linux/macOS installers, broader
   package-manager publication, code signing,
   auto-update, GUI dashboard, configuration
   wizard, enterprise installer platform,
   containerised distribution, cluster/HA, "one-
   click everything solved forever",
   "enterprise-grade installer", "production-ready
   desktop app").
4. Preserved byte-identical runtime and existing
   verification surfaces: Track G stdio path,
   Track H HTTP path, Track I installer round-trip,
   Track J reverse-proxy posture, Track K
   diagnostic harness, Track L service-supervision
   recipe + systemd template, Track M
   distribution-boundary recipe + wheel-build flip,
   Track N observability recipe, Track O dev-time
   recipe, Track P Step 1 planning deliverables —
   all unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation,
  docs-alignment, and closure for a single Windows
  setup.exe install path.
- Defining what counts as a "supported Windows
  installer experience" concretely for this repo
  at the current maturity level (download
  setup.exe → Next/Install/Finish → installed →
  uninstall via Add/Remove Programs).
- Defining whether Step 4 targets:
  - **PATH A** — installer-boundary docs only
    (operator-facing recipe describing the Inno
    Setup `.iss` template, the python.org
    embeddable runtime acquisition step, the
    expected installed footprint, the install
    directory default, the uninstall behaviour;
    no installer-definition file committed; the
    operator may follow the recipe to produce
    setup.exe out-of-tree);
  - **PATH B** — recipe + a narrow installer-
    technology definition file (one `.iss` Inno
    Setup script committed under
    `installer/windows/` or equivalent locked
    path, ≤ a Step-3-locked LOC cap; no bundled
    Python runtime binary committed to git —
    the build script pulls the embeddable
    distribution from python.org during build,
    not at clone time; no production code
    change);
  - **PATH C** — recipe + a narrow non-product
    helper (e.g., a build script that produces
    the installer-definition file from a
    template, or a CI workflow extension that
    builds setup.exe on a Windows runner).
- Defining the installer technology choice (default
  expectation: Inno Setup, because it is the
  simplest free Windows installer technology with
  honest uninstall registry support and a long
  reliability track record; WiX/MSI considered if
  Step 2 surfaces a grounded reason; NSIS / Advanced
  Installer / InstallShield / MSIX not default).
- Defining the bundled Python runtime shape (default
  expectation: python.org embeddable distribution,
  pulled by the build script — not committed binary).
- Defining the install directory default (default
  expectation: `%LOCALAPPDATA%\Programs\1c-agent-
  platform\` for per-user install; `Program Files\
  1c-agent-platform\` not default at Step 1).
- Defining the launch surface (default expectation:
  Start menu shortcut to a launcher that opens a
  PowerShell window in the install directory; no
  GUI app; no system-tray icon).
- Defining the uninstall verb (default expectation:
  registers under
  `HKCU\Software\Microsoft\Windows\CurrentVersion\
  Uninstall\<GUID>` so that the standard Windows
  "Settings → Apps → Installed apps" surface lists
  the platform and offers an Uninstall button).
- Defining how the installer relates to the
  existing wheel/pip path (default expectation:
  orthogonal but complementary — the wheel
  remains the canonical packaging artefact;
  setup.exe is one specific delivery channel
  built **on top of** the wheel, not a
  replacement for it).
- Preserving compatibility with all Tracks G / H /
  I / J / K / L / M / N / O invariants and the
  Track P / Step 1 planning surface.

## §7. What is out of scope

The following are intentionally **not** Track Q
scope. Each is denied explicitly to prevent silent
expansion. Track Q must not silently grow into any
of these even if technically adjacent:

- **No Linux installer.** No `.deb`, no `.rpm`, no
  `.apk`, no `.AppImage`, no `.snap`, no
  `.flatpak`, no Linux post-install hooks.
- **No macOS installer.** No `.dmg`, no `.pkg`,
  no `.app`, no Homebrew cask, no MacPorts, no
  notarization.
- **No `.msi` ecosystem in broad form.** Track Q
  defaults to Inno Setup producing setup.exe;
  WiX-produced `.msi` is considered only if
  Step 2 audit surfaces a grounded reason and
  Step 3 contract authorises it. The track does
  not commit to "MSI distribution channel" as a
  general claim.
- **No package manager publication.** No
  Chocolatey package, no winget manifest, no
  Scoop bucket, no NuGet package, no Microsoft
  Store / MSIX in store sense. Operators may
  hand-publish anywhere; Track Q does not.
- **No PyPI publication.** Wheel publication to
  PyPI / TestPyPI remains operator decision, not
  track work (Track M non-goal preserved).
- **No code signing / Authenticode / EV cert /
  notarization / SBOM / SLSA.** The shipped
  setup.exe is unsigned by default. Operators
  who need signing arrange it separately. SBOM /
  SLSA / supply-chain attestation are explicit
  non-goals.
- **No auto-update / OTA / delta-update.** The
  installer does not check for new versions, does
  not phone home, does not download patches.
  Operator triggers re-install manually by
  running a newer setup.exe.
- **No GUI dashboard.** The platform has no
  frontend; the installer does not ship one.
- **No browser UI / web admin panel.** Same as
  above.
- **No service supervision redesign.** Track L
  recipe + systemd template byte-identical. The
  installer does NOT register a Windows Service
  by default (default expectation: per-user
  install, manual launch through Start menu
  shortcut; Windows Service registration is an
  out-of-band operator decision, not Track Q
  scope).
- **No auth redesign.** Tracks D / H preserved
  byte-identical. The installer does not
  fabricate tokens, does not store credentials,
  does not change the auth surface.
- **No transport redesign.** Tracks G / H
  preserved byte-identical. The installer does
  not change stdio or HTTP transport surfaces.
- **No new MCP tools.** Registry invariant
  `read=15 / write=25 / intelligence=16` must
  carry through all six Track Q steps.
- **No registry changes** (MCP registry, not
  Windows registry — the latter is in scope only
  for the Add/Remove Programs uninstall entry).
- **No new CLI flag on existing servers.** The
  Track G / H flag surface (`--transport`,
  `--config-path`, `--log-level`, `--bind`,
  `--auth-token-env`) is locked.
- **No new entrypoint module.**
- **No new `[project.scripts]` console entries.**
- **No new transports.** No WebSocket transport,
  no SSE transport, no gRPC, no AMQP.
- **No remote-dev / DX / IDE integrations.**
  Track O preserved byte-identical.
- **No enterprise installer platform / MDM
  integration.** No Group Policy templates, no
  SCCM packaging, no Intune publishing.
- **No containerisation.** No Dockerfile, no
  OCI image, no Podman build, no container
  runtime.
- **No cluster / HA.** Single-machine install
  only.
- **No "all Windows distributions supported"
  claim.** Default expectation: Windows 10 and
  Windows 11 amd64. Windows 7, Windows Server,
  ARM64, x86 not in default support matrix.
- **No "one-click everything solved forever"
  claim.**
- **No "enterprise-grade installer" claim.**
- **No "production-ready desktop app" claim.**
- **No "GUI config wizard" claim.** The
  installer does not collect configuration —
  default expectation is that the installer
  drops the platform on disk; product
  configuration remains a separate operator
  step using existing `scripts/release/
  install.ps1` or equivalent.
- **No "Windows service auto-magic by default"
  claim.** Track L recipe preserved; the
  installer does not silently register a Windows
  Service.
- **No test-suite program.** Track P territory,
  byte-identical.
- **No observability redesign.** Track N
  recipe + FC1–FC7 signals byte-identical.
- **No remote push.** GitHub push remains
  operator decision.
- **No new track opened in parallel with Track Q
  at Step 1.** Track Q opens exactly one new
  parallel track.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1
commit and must remain verifiable through Step 6:

1. **Tracks A–O closed-state invariants byte-
   identical.** `apps/*/src/`, `packages/*/src/`,
   `docs/operators/deployment-boundary.md`,
   `docs/operators/service/service-supervision.md`,
   `docs/operators/service/mcp-server.service`,
   `docs/operators/packaging/distribution-boundary.md`,
   `docs/operators/observability.md`,
   `docs/dev/editable-install-and-workspace-discovery.md`
   not touched by any Track Q step.
2. **Track P planning deliverables byte-identical.**
   `docs/architecture/track-p-test-suite-shipping-
   and-verification-boundary-plan.md` and
   `docs/architecture/track-p-test-suite-shipping-
   and-verification-boundary-step-map.md` not
   touched by any Track Q step.
3. **`pyproject.toml`** byte-identical at Steps 1 /
   2 / 3 / 4 / 5. Track Q does **not** modify
   `pyproject.toml` at Step 4 by default; the
   wheel-build block and `[project.scripts]`
   entries are Track M deliverables and Track Q is
   built **on top of** them, not over them. Step 6
   MAY modify `pyproject.toml` `version` only if
   Q7 = PATCH or MINOR; default expectation Q7
   framing only, with the version-bump decision
   deferred to Step 6.
4. **Registries invariant.** `selfcheck.py`
   registries `read=15 / write=25 / intelligence=16`
   must remain confirmed green at every step.
5. **No new MCP tools** at any step.
6. **No new CLI flag on existing servers.** The
   Track G / H flag surface (`--transport`,
   `--config-path`, `--log-level`, `--bind`,
   `--auth-token-env`) is locked.
7. **No new entrypoint module.**
8. **`scripts/dev/selfcheck.py`** byte-identical at
   every step.
9. **`scripts/dev/mcp_client_smoke.py`** byte-
   identical at every step.
10. **`scripts/release/install.ps1`,
    `scripts/release/verify-release.ps1`,
    `scripts/release/_install_runner.py`,
    `scripts/dev/launch.ps1`,
    `scripts/dev/bootstrap_paths.ps1`,
    `scripts/dev/run_dev_check.ps1`** byte-identical
    at every step. Track Q does **not** modify any
    existing `scripts/*` file; if Step 4 PATH B/C
    requires a build helper, it is a new file under
    `installer/` or equivalent locked path, not a
    modification of any existing script.
11. **`SECURITY.md`** byte-identical at every step.
12. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    CLASS-1 pointer to the Step 4 recipe; default
    expectation: ≤ 1 new bullet.
13. **`apps/platform/README.md`** byte-identical at
    every step.
14. **`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    cross-link in `docs/operator-manual.md` only.
15. **`scripts/dev/README.md`,
    `scripts/release/README.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add a narrow
    pointer in `scripts/release/README.md` only.
16. **README.md "Closed parallel tracks" list**
    byte-identical at Steps 1 / 2 / 3 / 4 / 5
    (still 15 entries A–O). Only Step 6 extends
    it (potentially to 17 entries A–O + P + Q,
    only after Track P closes independently;
    Track Q closure does **not** extend the list
    if Track P is still active — Track Q is
    listed separately under "active parallel
    tracks" closure language).
17. **`CHANGELOG.md`** byte-identical at Steps 1 /
    2 / 3 / 4 / 5. Only Step 6 appends a Track Q
    closure entry.
18. **`.github/workflows/dev-check.yml`** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5. Step 4
    MAY extend the workflow file only if Step 3
    contract explicitly authorises a Windows-
    runner installer-build job (PATH C); default
    expectation under PATH A/B: no workflow
    change.
19. **`.python-version`** byte-identical at every
    step (Python 3.11 pin preserved as the
    bundled-runtime target).
20. **`1c_agent_platform-0.5.2-py3-none-any.whl`
    artefact class byte-identical** (Track M
    closure state). Track Q's installer is built
    **on top of** this wheel — it does not
    replace it.
21. **No bundled-runtime binary committed to
    git.** The python.org embeddable distribution
    (or any equivalent) is acquired by the build
    script at build time, not committed as a
    binary to the repository. The Step 4 file
    surface MUST NOT include any `.zip`, `.exe`,
    `.dll`, `.pyd`, or other binary artefact.
22. **No `1cv8.exe` runs** at any step.
23. **No real credentials** in any committed file.
24. **No premature closure language.** Steps 1–5
    may not describe Track Q as "закрыт" /
    "closed".
25. **No false implementation claims.** Step 1
    plan must present Q1–Q7 as **defaults** and
    **recommendations**, not as decided answers.
26. **Step 4 file-surface cap.** Step 3 contract
    MUST pin a maximum number of touched files
    (default expectation: ≤ 3 — at most one
    recipe doc + at most one installer-definition
    file + at most one narrow build-helper
    script). Step 3 may tighten.
27. **Step 4 LOC cap for installer-definition
    file.** Default expectation: ≤ 250 LOC for
    the `.iss` (Inno Setup script). Step 3 may
    tighten.
28. **Step 4 LOC cap for recipe doc.** Default
    expectation: ≤ 1200 LOC for the operator-
    facing recipe at
    `docs/operators/installer/windows-setup-exe.md`
    or equivalent locked path. Step 3 may
    tighten.
29. **Installed footprint cap.** Step 3 contract
    must pin the expected installed footprint
    range. Default expectation: 10–15 MB.
30. **Uninstall path part of the supported
    boundary.** The installer MUST produce an
    uninstall path that is reachable through the
    standard Windows Add/Remove Programs surface
    or its modern equivalent. Step 3 contract
    must lock this.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track Q has shipped **at most one new
   architecture plan-doc, one new step-map doc,
   one new baseline-audit doc, one new normative
   contract doc, and (Step 4) at most three new
   files or surgical modifications** under
   Step 3 contract caps.
2. Production code (`apps/*/src/`,
   `packages/*/src/`) byte-identical to Track O
   closure state (`720ac54`).
3. `pyproject.toml` `version` either unchanged
   (`0.5.2`, Q7 = NO-BUMP) or bumped per Q7
   rule; the wheel-build block and
   `[project.scripts]` entries byte-identical.
4. Registries `read=15 / write=25 /
   intelligence=16` carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure
   narrative present and honest: explicit
   denial of "Windows install solved forever",
   "enterprise-grade installer", "production-
   ready desktop app", "all Windows
   distributions supported", "one-click
   everything solved forever", "GUI config
   wizard", "Windows service auto-magic by
   default" claims; explicit statement of which
   Windows installer boundary Track Q settled;
   explicit Q7 reasoning.
6. `verify-release.ps1` GREEN on 8 checks at
   every step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed
   text.
9. No `1cv8.exe` runs anywhere in the track.
10. No outbound-network calls in any committed
    code (the build-time fetch of the python.org
    embeddable distribution, if any, is operator-
    triggered build-time behaviour, not runtime
    behaviour, and is documented in the recipe;
    it does not appear in any production code
    path).
11. No remote push performed automatically by any
    step.
12. Track Q either added to README's "Closed
    parallel tracks" list (only if Track P has
    independently closed by Step 6 of Track Q —
    not assumed) or noted separately in a
    "Closed parallel tracks (out-of-order
    closure)" subsection. Default expectation:
    Track Q runs in parallel with Track P; final
    closure-list shape is a Step 6 decision.

---

## §10. Honest constraints after closure

These constraints remain after Track Q closure:

- **No "production-ready Windows installer
  platform" claim.** Track Q's closure-gate
  covers one narrow Windows-setup.exe-delivery
  slice; broader installer platforms remain
  recommended-only.
- **Bundled-runtime footprint cost.** The honest
  installed footprint is roughly 10–15 MB
  (~10 MB embeddable CPython + ~1 MB platform
  packages + small installer overhead). That is
  the structural cost of the gap closure; no
  reduction is promised.
- **Unsigned setup.exe by default.** Operators
  who need Authenticode signing arrange it
  separately. SmartScreen warnings on first run
  are expected and documented as honest
  baseline behaviour.
- **No auto-update.** Re-install is operator-
  triggered.
- **Single-user, single-machine install.** No
  multi-user / per-machine / MDM / cluster /
  HA capabilities.
- **No GUI configuration step in the installer.**
  Product configuration remains a separate
  operator action using existing surfaces.
- **No new MCP tools / registry change.**
- **No `1cv8.exe` runs.**

---

## §11. Relationship to Tracks G / H / I / J / K / L / M / N / O / P

| Aspect | Track M (packaging) | Track L (service) | Track O (dev-time) | Track P (test suite) | Track Q (this — Windows installer) |
| --- | --- | --- | --- | --- | --- |
| Audience | Operator with Python on the box | Operator with systemd/launchd familiarity | Contributor editing the repo | Contributor verifying behaviour | **Ordinary Windows end user without Python/pip/Git** |
| Primary artefact | `1c_agent_platform-*.whl` | `docs/operators/service/service-supervision.md` + systemd template | `docs/dev/editable-install-and-workspace-discovery.md` | TBD by Track P Step 3 contract | TBD by Track Q Step 3 contract; default expectation = operator recipe + one `.iss` Inno Setup script |
| Install verb | `pip install <WHEEL_PATH>` | n/a | `pip install -e .` | n/a | **Double-click `setup.exe` → Next → Install → Finish** |
| Uninstall verb | `pip uninstall 1c-agent-platform` | systemctl disable/remove | n/a | n/a | **Add/Remove Programs → Uninstall** |
| Bundled runtime? | NO (assumes Python on box) | NO (assumes Python on box) | NO (assumes Python on box) | NO | **YES — embeddable CPython 3.11 (default expectation, structural requirement)** |
| Cross-OS | py3-none-any (any OS with Python 3.11) | Linux primary + others prose | Windows primary + POSIX via editable install | TBD; default cross-OS neutral | **Windows only** |
| Code touched? | NO production code | NO production code | NO production code | TBD by Track P Step 3 contract | **NO production code** (Step 3 contract may explicitly forbid) |
| New transport / endpoint / flag? | NO | NO | NO | NO | NO |
| Registry change (MCP)? | NO | NO | NO | NO | NO |
| Windows-registry uninstall entry? | NO | NO | NO | NO | **YES — under HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\\<GUID>** |
| SemVer outcome | PATCH (Track M closure) | NO-BUMP | NO-BUMP | TBD | **TBD (directional framing only; not locked at Step 1)** |

Track Q inherits all preceding tracks' invariants and
adds none that conflict with them. Track Q is
specifically **complementary to Track M**: Track M's
wheel is the foundation; Track Q wraps it inside a
Windows-native installer experience. Track Q does
**not** make the wheel obsolete — operators with
Python on the box continue to use the wheel path
without change.

---

## §12. Open questions Q1–Q7 with directional defaults

These are **defaults / directional recommendations**,
not decided answers. Step 2 audit may move them;
Step 3 contract locks them. Q7 is intentionally
left as directional framing only — its lock point
is Step 6.

### Q1 — what counts as "Windows installer path shipped" for closure?

**Options.**
- **(A)** Operator-facing recipe only: a single
  recipe document at
  `docs/operators/installer/windows-setup-exe.md`
  (or equivalent locked path) that walks an
  operator through producing setup.exe out-of-
  tree using Inno Setup, with explicit guidance
  on bundling the python.org embeddable
  distribution, structuring the install
  directory, registering the uninstall entry,
  and creating the Start menu shortcut. No
  installer-definition file committed.
- **(B)** Recipe **plus** a narrow installer-
  technology definition file — one Inno Setup
  `.iss` script committed under
  `installer/windows/` (or equivalent Step-3-
  locked path), ≤ 250 LOC. No bundled-runtime
  binary committed to git. No production code
  change.
- **(C)** Recipe **plus** a narrow non-product
  helper (e.g., a PowerShell build script
  `installer/windows/build-setup-exe.ps1` that
  pulls the python.org embeddable distribution,
  invokes Inno Setup, and emits setup.exe in
  `dist/installer/`).

**Default recommendation.** **(B) recipe +
narrow installer-definition slice** as the most
likely outcome, because committing a single
`.iss` makes the installer reproducible across
operators and across time (mirror of Track M /
Step 4 closing the `packages = []` aspirational
declaration: declaring-but-not-shipping is the
gap, declaring-AND-shipping closes it). **(A)**
acceptable fallback if Step 2 audit reveals that
the Inno Setup `.iss` surface is large enough to
expand scope beyond Track Q's narrow boundary.
**(C)** acceptable as an additive complement to
(B) if Step 3 contract authorises both, but
rejected as a standalone (a build script without
the installer-definition it consumes is hollow).

### Q2 — installer technology default

**Options.**
- **(A) Inno Setup** — free, open-source,
  long reliability track record, single `.iss`
  declarative script, native uninstall registry
  support, mature on Windows 10/11.
- **(B) WiX Toolset / .msi** — Microsoft-aligned,
  declarative XML (`.wxs`), produces `.msi`
  rather than `.exe`. Heavier ramp; explicitly
  considered only if Step 2 audit surfaces a
  grounded reason (e.g., MDM/SCCM/Intune
  compatibility a stated operator need).
- **(C) NSIS** — free, scriptable, longer
  surface area than Inno Setup, less obvious
  uninstall registry semantics. Considered if
  Step 2 surfaces a specific need.
- **(D) Advanced Installer** — commercial,
  feature-rich. Rejected by default (Track Q
  prefers free tooling).
- **(E) InstallShield** — commercial, enterprise-
  oriented. Rejected by default (out of scope).
- **(F) MSIX** — Microsoft's modern packaging
  format with Store distribution. Rejected by
  default (Track Q does not ship to the Store).

**Default recommendation.** **(A) Inno Setup**
as the baseline choice. Inno Setup is the
simplest honest Windows installer technology
that meets all Track Q acceptance criteria
(Next/Install/Finish flow, Windows registry
uninstall entry, no preinstalled prerequisites,
free tooling, single declarative file).
**(B) WiX** considered only if Step 2 surfaces
a grounded MDM/SCCM/Intune operator need.
**(C)–(F)** rejected by default and require
Step 2 audit + Step 3 contract authorisation.
**Step 1 does not lock the technology choice;**
Step 3 contract is the lock point.

### Q3 — likely honest Step 4 path?

**Options.**
- **PATH A** — operator recipe only.
- **PATH B** — operator recipe + one `.iss`
  Inno Setup script + (optionally) one narrow
  build-helper script.
- **PATH C** — operator recipe + non-product
  build helper standalone (without the `.iss`).

**Default recommendation.** **PATH B is the most
likely outcome**, with PATH A held in reserve if
Step 2 audit reveals that committing a `.iss`
expands scope beyond Track Q's narrow boundary.
PATH C rejected as standalone (without the
installer-definition file the build helper has
nothing to consume). **Do not lock Step 4 PATH
at Step 1**; Step 3 contract is the lock point.

### Q4 — install experience prerequisite stance

**Locked default recommendation (directional, not
yet contract-binding).** The install experience
**MUST NOT** require any of the following to be
preinstalled on the target Windows machine:

- Python (any version);
- pip;
- Git;
- Visual Studio Build Tools / MSVC;
- Windows SDK;
- Any C/C++ runtime beyond what Windows 10/11
  ships by default;
- Any third-party package manager (Chocolatey,
  winget, Scoop, NuGet).

The honest implication, restated from §4 above:
the installer MUST bundle (or download at install
time) a Python runtime. Default expectation:
python.org embeddable CPython 3.11 distribution,
pulled at build time by the build helper, not
committed as binary to git.

Step 2 audit must verify this constraint
honestly and inventory the trade-offs between
build-time bundling vs install-time download
(both are honest options; both are forms of
shape α from §4).

### Q5 — uninstall path stance

**Locked default recommendation (directional, not
yet contract-binding).** Uninstall is a
**first-class part of the supported boundary**.
The installer MUST register an uninstall entry
under

```
HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\<GUID>
```

(or the per-machine `HKLM` equivalent if the
operator chooses a per-machine install) so that
the platform appears in the standard Windows
"Settings → Apps → Installed apps" surface and
offers an Uninstall button. Inno Setup handles
this registry surface natively. The uninstall
verb is documented in the recipe and verified by
the Step 4 / Step 5 closure-gate scenario.

### Q6 — does Track Q require production code changes?

**Default recommendation.** **No.** The installer
packages the existing wheel contents plus a
bundled Python runtime. The platform's behaviour
when invoked through the bundled runtime is
**identical** to its behaviour when invoked
through an operator-installed Python — there is
no codepath that needs to know which runtime is
hosting it. Step 2 audit must verify this
honestly, but the default expectation is that no
`apps/*/src/` or `packages/*/src/` change is
warranted. Step 3 contract is expected to
explicitly forbid production code changes at
Step 4.

### Q7 — SemVer expectation

**Options.**
- **(A) NO-BUMP.** Track Q closes under existing
  `0.5.2` if Step 4 = PATH A docs-only.
  Mirrors Track J / Track K / Track L / Track N /
  Track O NO-BUMP precedents.
- **(B) PATCH `0.5.2 → 0.5.3`** (or, if Track P
  consumed PATCH first, the next-PATCH after
  that). Track Q closes with a PATCH bump if
  Step 4 = PATH B and the change is honestly
  framed as defect-class delivery-channel
  repair closing the long-standing "no GUI
  installer" deferral in Track M's recipe and
  `pyproject.toml` comment block. Mirror of
  Track I / Track M PATCH precedents.
- **(C) MINOR `0.5.2 → 0.6.0`** (or next-MINOR
  after Track P). Track Q closes with a MINOR
  bump if Step 4 = PATH B + the new Windows-
  setup.exe delivery channel is honestly framed
  as a **new operator-visible delivery
  capability**, since "ordinary Windows user
  install without Python on the box" is a
  genuinely new audience and a new delivery
  channel that ordinary product consumers can
  use that they could not use before. Mirror of
  Track H minor-bump precedent (introduction of
  the network transport as a new operator-
  visible capability).
- **(D) MAJOR.** Explicitly rejected by track
  scope.

**Default recommendation (directional only).**
**(A) NO-BUMP** if Step 4 PATH A; **(B) PATCH**
defensible if Step 4 PATH B is framed as defect-
class delivery-channel repair; **(C) MINOR**
defensible if Step 4 PATH B is framed as a new
operator-visible delivery capability. Track Q
plan explicitly **does not lock** this answer.
Step 1 captures all three as live possibilities;
Step 3 contract may narrow them; Step 6 closure
locks. The user has been explicit that Q7 should
remain directional framing only at Step 1.

---

## §13. Six-step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-q-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-q-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 3 new files or surgical modifications (default under PATH B = one operator recipe `docs/operators/installer/windows-setup-exe.md` + one Inno Setup `.iss` script under `installer/windows/` + optionally one build-helper script `installer/windows/build-setup-exe.ps1`) | locked by Step 3 contract |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `docs/operator-manual.md`, possibly `scripts/release/README.md`; NO production code; NO existing `scripts/*` script body change | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` version field if Q7 = PATCH or MINOR | NO production code; Q7 decision explicit |

---

## §14. Honest summary

**What Track Q will do.** Convert the "no honest
Windows setup.exe install path for an ordinary
Windows user without Python/pip/Git" gap into one
operator-facing Windows-installer recipe (and, if
Step 3 contract pins PATH B, a narrow Inno Setup
`.iss` script plus optionally one narrow build-
helper script that pulls the python.org
embeddable CPython 3.11 distribution at build
time), preserving every Tracks A–O invariant and
the Track P / Step 1 planning surface byte-
identical.

**What Track Q will not do.** It will not
introduce a broader installer ecosystem (no
Linux/macOS installers, no broad `.msi`/`.deb`/
`.rpm`/`.dmg`/`.pkg`/`.snap`/`.flatpak`
ecosystem, no PyPI publication, no package-
manager matrix, no code signing, no auto-update,
no GUI dashboard, no browser UI, no service
supervision redesign, no auth redesign, no
transport redesign, no new MCP tools, no
registry changes, no new CLI flags, no new
`[project.scripts]` entries, no remote-dev / DX /
IDE integrations, no enterprise installer
platform, no containerisation, no cluster/HA);
will not run `1cv8.exe`; will not push to
GitHub automatically.

**Central honest constraint.** Because the
platform is a pure-Python codebase and the
acceptance criterion is "install experience MUST
NOT require preinstalled Python/pip/Git", the
installer **structurally must bundle a Python
runtime**. The default expectation is the
python.org embeddable CPython 3.11 distribution,
pulled at build time by the build helper. No
honest setup.exe path exists without this. The
installed footprint cost is roughly 10–15 MB and
is the structural cost of the gap closure.

**Why this is the next right narrow track.** The
recommended-next-track candidates list in
PROJECT-STATUS explicitly names broader
installer-ecosystem work; Track M's recipe and
the `pyproject.toml` comment block explicitly
defer the "GUI installer" question; the
`scripts/release/install.ps1` umbrella comment
explicitly says "no `.msi`, no `.deb`, no GUI
wizard". Three independently verifiable repo
anchors say "this gap exists and is deferred to
a future track". Track Q is that future track,
narrowed to Windows-setup.exe-only — the same
disciplined narrowing Track M applied to the
"broader packaging ecosystem" recommendation
when it chose `py3-none-any` wheel only without
PyPI publication.

**Default Q7 outcome.** **NO-BUMP** if Step 4
PATH A (docs-only); **PATCH** defensible if Step 4
PATH B framed as defect-class delivery-channel
repair; **MINOR** defensible if Step 4 PATH B
framed as new operator-visible delivery
capability. Q7 lock is Step 6 territory; Step 1
captures all three as live possibilities and
locks none.

**What Step 1 explicitly does not do.** It does
not open Step 2; it does not pick the installer
technology (default expectation Inno Setup is
directional, not contract-binding); it does not
commit any installer-definition file; it does not
commit any binary artefact; it does not change
production code; it does not change
`pyproject.toml`; it does not change any
`scripts/*` file; it does not modify Track P
planning surface; it does not extend the README
Closed parallel tracks list; it does not run
`1cv8.exe`; it does not push to a GitHub remote.
