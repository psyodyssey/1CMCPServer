# Parallel Track Q — Windows Installer Path and setup.exe Delivery — Normative Contract

Companion to:

- [track-q-windows-installer-path-and-setup-exe-delivery-plan.md](track-q-windows-installer-path-and-setup-exe-delivery-plan.md) (Step 1)
- [track-q-windows-installer-path-and-setup-exe-delivery-step-map.md](track-q-windows-installer-path-and-setup-exe-delivery-step-map.md) (Step 1)
- [track-q-windows-installer-path-and-setup-exe-delivery-baseline-audit.md](track-q-windows-installer-path-and-setup-exe-delivery-baseline-audit.md) (Step 2)

This document is the **Step 3** deliverable of Track Q.
It is **prescriptive**. It uses RFC 2119 language —
**MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**,
**MAY**. Where it conflicts with Step 2 directional
defaults, this contract takes precedence; where it
conflicts with Step 1 plan defaults, this contract
takes precedence. Where it conflicts with the
step-map carry-through invariants, the step-map
invariants take precedence (the contract MUST NOT
weaken the step-map).

The contract closes the central product question of
Track Q: **the shortest honest human path from
`setup.exe` to "Claude can use the local server",
including configuration of one 1C base, end to end**.

The Step 2 audit §10.5 framing — "1C base selection
= not in Track Q scope" — is **explicitly
superseded**. Base selection / configuration of one
1C base **is** in Track Q scope. This is the
central product decision of Step 3 and the reason
this contract exists.

---

## §1. Purpose and scope of this contract

### §1.1 — What this contract locks

This contract pins, in normative form, every Track Q
decision that the Step 4 implementation slice will
operationalize. After this commit, Step 4 has no
remaining design questions; it has only execution
questions ("does the recipe match the contract",
"does the `.iss` match the contract", "does the
configurator script match the contract", "does the
build helper match the contract"). Step 5 has no
remaining design questions either; it has only
narrow-alignment questions ("does this README
sentence point at the new recipe", "does this
PROJECT-STATUS sentence describe Track Q closure
accurately"). Step 6 has only the final integration
pass plus the Q7 SemVer decision.

What this contract pins, enumerated:

1. The final Track Q closure-gate scenario (§5).
2. The exact installed files layout under
   `%LOCALAPPDATA%\Programs\1C Agent Platform\`
   (§6).
3. The installer wizard scope — what the Inno
   Setup wizard does and does NOT do (§7).
4. The first-run configurator — where one-base
   configuration happens, what the configurator
   surface is, what data it collects, how it
   writes the product-config, and how it ends
   (§8). This is the central new section.
5. The exact launch path the user follows after
   install (§9).
6. The uninstall boundary — what is removed and
   what is preserved (§10).
7. The honest non-goals — the denial list
   (§11).
8. The Step 4 PATH choice, file surface, LOC
   caps, and forbidden-files list (§12).
9. The Step 5 forbidden-files list (§13).
10. The Q7 framing for Step 6 (§14).

### §1.2 — What this contract does NOT do

This contract is a **document**. It does NOT:

- modify any production code (`apps/*/src/`,
  `packages/*/src/`) — the byte-identical
  invariant carried through every Track Q step
  remains in force;
- modify `pyproject.toml` — the byte-identical
  invariant remains in force;
- modify any file under `scripts/*` — the
  byte-identical invariant remains in force;
- commit any installer-definition file — Step 4
  ships the `.iss`; Step 3 only describes it;
- commit any binary artefact — step-map
  invariant §1.30 remains in force;
- ship any actual `setup.exe` — that is Step 4
  build output, never committed;
- open any new parallel track;
- weaken any of the 35 step-map carry-through
  invariants;
- introduce backward-incompatible language about
  Track P, Track O, Track M, or any earlier
  closed track.

### §1.3 — Reading guide

The contract has fourteen sections. Sections §1–§4
are framing. §5 is the closure-gate scenario.
§6–§10 are the locked product surfaces. §11 is the
denial list. §12–§14 are Step 4 / Step 5 / Step 6
boundaries. Sections do not depend on later
sections; the contract reads top-to-bottom without
forward references.

---

## §2. Normative language conventions

### §2.1 — RFC 2119 keywords

Where this contract uses **MUST**, **MUST NOT**,
**SHOULD**, **SHOULD NOT**, and **MAY**, those
keywords carry their RFC 2119 meanings.

- **MUST** = an absolute requirement. A Step 4
  implementation that violates a MUST is not a
  valid Track Q deliverable.
- **MUST NOT** = an absolute prohibition. A Step 4
  implementation that does the prohibited thing
  is not a valid Track Q deliverable.
- **SHOULD** = a strong recommendation; deviation
  requires a documented grounded reason inside
  the Step 4 commit message.
- **SHOULD NOT** = a strong prohibition with the
  same escape hatch.
- **MAY** = optional; either choice is
  contract-compatible.

### §2.2 — Scope of the keywords

RFC 2119 keywords apply to:

- the Step 4 file surface (§12);
- the Step 5 file surface (§13);
- the Step 6 closure conditions (§14);
- the closure-gate scenario at §5;
- the locked product surfaces in §6–§10.

They do **not** apply to the operator running the
build helper, the operator running Inno Setup's
compiler `iscc.exe`, or the ordinary Windows user
double-clicking setup.exe. Those are operator-side
actions, not contract obligations.

### §2.3 — Conflict resolution

Where this contract uses a normative keyword and
the step-map carries an invariant on the same
surface, the step-map invariant takes precedence.
Where this contract uses a normative keyword and
the Step 2 audit makes a directional
recommendation on the same surface, this contract
takes precedence (audits are directional;
contracts are normative).

---

## §3. Carry-through invariants (normative)

These restate the 35 step-map invariants in
normative form. The Step 4 implementation slice
**MUST** preserve every one.

### §3.1 — Production code

- All `apps/*/src/` modules **MUST** be byte-
  identical between Step 3 HEAD and Step 4 HEAD.
- All `packages/*/src/` modules **MUST** be byte-
  identical between Step 3 HEAD and Step 4 HEAD.
- In particular, `apps/platform/src/onec_platform/installer.py`
  **MUST** be byte-identical. The first-run
  configurator reuses
  `run_install_fast_path_from_json_file` through
  the bundled-Python `python.exe -c "…"` invocation
  exactly as it exists today; the Step 4 slice
  **MUST NOT** add a `[project.scripts]` entry for
  this helper, **MUST NOT** add a new public
  symbol to `installer.py`, and **MUST NOT**
  modify the helper's signature.

### §3.2 — Project metadata

- `pyproject.toml` **MUST** be byte-identical
  between Step 3 HEAD and the end of Step 4.
  Specifically: `version=0.5.2`, `[project]`,
  `[project.scripts]`, `[build-system]`,
  `[tool.ruff]`, `[tool.pytest.ini_options]`,
  `[tool.hatch.build.targets.wheel]` all byte-
  identical. Step 6 **MAY** modify `version` only
  per the Q7 outcome — never earlier.
- `.python-version` **MUST** be byte-identical at
  every Track Q step. The bundled-runtime patch
  version pinned by the Step 4 build helper
  **MUST** match the major-minor version in this
  file (the major-minor is `3.11`; the patch is a
  Step 4 build-helper decision).

### §3.3 — Operator-facing scripts

- All files under `scripts/*` **MUST** be byte-
  identical at every Track Q step (including
  Step 5 — the `scripts/release/README.md` MAY
  add at most one bullet pointing at the Step 4
  recipe; the three `.ps1` / `.py` files
  themselves remain byte-identical).
- `scripts/release/install.ps1` in particular
  **MUST** remain byte-identical; the Track Q
  installer is **orthogonal** to the Track B/I
  install-fast-path, not a replacement.

### §3.4 — Existing operator recipes

- `docs/operators/deployment-boundary.md` (Track J)
  **MUST** be byte-identical.
- `docs/operators/observability.md` (Track N)
  **MUST** be byte-identical.
- `docs/operators/packaging/distribution-boundary.md`
  (Track M) **MUST** be byte-identical.
- `docs/operators/service/service-supervision.md`
  (Track L) **MUST** be byte-identical.
- `docs/operators/service/mcp-server.service`
  (Track L) **MUST** be byte-identical.
- `docs/dev/editable-install-and-workspace-discovery.md`
  (Track O) **MUST** be byte-identical.

### §3.5 — Track Q architecture surface

- The Step 1 plan
  (`track-q-…-plan.md`) **MUST** be byte-identical
  at every step ≥ Step 1.
- The Step 1 step-map
  (`track-q-…-step-map.md`) **MUST** be byte-
  identical at every step ≥ Step 1.
- The Step 2 audit
  (`track-q-…-baseline-audit.md`) **MUST** be
  byte-identical at every step ≥ Step 2.
- This Step 3 contract
  (`track-q-…-contract.md`) **MUST** be byte-
  identical at every step ≥ Step 3.

### §3.6 — Track P preservation

- `docs/architecture/track-p-…-plan.md` and
  `docs/architecture/track-p-…-step-map.md`
  **MUST** be byte-identical at every Track Q
  step. Track Q **MUST NOT** touch Track P
  deliverables. Track P remains active at its own
  pace, decided by separate operator action.

### §3.7 — Registries

- The three MCP registries **MUST** carry counts
  `read = 15 / write = 25 / intelligence = 16` at
  every Track Q step. Step 4 **MUST NOT** add,
  remove, or rename any tool in any registry.
  `scripts/dev/selfcheck.py` **MUST** report
  `selfcheck_status = ok` at every step.

### §3.8 — CI workflow

- `.github/workflows/dev-check.yml` **MUST** be
  byte-identical at Steps 1 / 2 / 3 / 5. Step 4
  **MAY** extend the workflow with a Windows-
  runner installer-build job (≤ 30 lines of YAML
  addition) **only if** the Step 4 commit message
  surfaces a grounded reason; default expectation
  is no workflow change.

### §3.9 — Build artefacts

- The Track M wheel artefact contract
  (`1c_agent_platform-<VERSION>-py3-none-any.whl`)
  **MUST** remain byte-identical in shape. The
  Track Q installer is built **on top of** the
  wheel; it does not replace it.
- The Step 4 slice **MUST NOT** commit any binary
  artefact. Forbidden file extensions inside the
  Step 4 commit: `.zip`, `.exe`, `.dll`, `.pyd`,
  `.msi`, `.cab`, `.7z`, `.tar.*`, `.gz`, `.bz2`,
  `.xz`.

### §3.10 — Other surfaces

- `SECURITY.md`, `CHANGELOG.md`,
  `apps/platform/README.md`, all manuals,
  `docs/release-handoff.md` **MUST** be byte-
  identical at Steps 1 / 2 / 3 / 4. Step 5 **MAY**
  add narrow CLASS-1 updates per the step-map.
- `README.md` "Closed parallel tracks" list
  **MUST** be byte-identical at Steps 1 / 2 / 3 /
  4 / 5. Step 6 **MAY** extend it depending on
  Track P closure state.
- No `1cv8.exe` runs **MUST** occur in any Track Q
  step.
- No real credentials **MUST** appear in any
  committed text.
- No remote push **MUST** occur in any Track Q
  step.

### §3.11 — Closure-language discipline

- Steps 1–5 **MUST NOT** use closure language for
  Track Q itself ("Track Q closed", "Windows
  install solved forever", "enterprise installer
  ready"). Such phrases **MUST** appear only as
  explicit denials. Step 6 is the only step that
  may introduce closure language.

---

## §4. Q1–Q6 final answers (locked)

The Step 1 plan §12 named Q1–Q7 as directional
defaults; the Step 2 audit §11 confirmed Q1–Q6
were consistent with evidence and refined the
framing. This section locks Q1–Q6 normatively.
Q7 is framed for Step 6 in §14.

### §4.1 — Q1: closure-gate scope (LOCKED)

The Track Q closure-gate is the scenario in §5
below. It includes, as a non-optional component,
**configuration of one 1C base** through the
first-run configurator. The earlier Step 2 audit
§10.5 framing — "1C base selection = not in
Track Q scope" — is **superseded**. Closure-gate
scope **MUST** be exactly §5; nothing more,
nothing less.

### §4.2 — Q2: installation story (LOCKED)

The installer **MUST** be built **on top of** the
Track M wheel sources. The eleven src-layout
package paths from `pyproject.toml:51-63`
**MUST** be extracted into the install directory
in their importable layout. The wheel itself
**MUST NOT** be modified. The wheel build flow
remains the Track M responsibility.

### §4.3 — Q3: installer technology (LOCKED)

Step 4 **MUST** use Inno Setup as the installer
technology. The Step 4 file surface **MUST**
include exactly one `.iss` script under
`installers/windows/setup.iss`. WiX and NSIS
**MUST NOT** be used as the installer technology
in Step 4. Future tracks **MAY** revisit this
choice; Track Q **MUST NOT**.

### §4.4 — Q4: bundled-runtime shape (LOCKED)

Step 4 **MUST** use shape α (bundled python.org
embeddable CPython 3.11 distribution). Shape β
(frozen executables via PyInstaller / Nuitka /
Briefcase / py2exe / cx_Freeze) **MUST NOT** be
used. The exact embeddable filename **MUST** be
of the shape
`python-3.11.<x>-embed-amd64.zip` where `<x>` is
a specific patch version pinned by the Step 4
build helper. The patch version pinned **MUST**
match the major-minor declared in
`.python-version` (i.e., the major-minor
component **MUST** be `3.11`). The embeddable
zip **MUST** be fetched at build time by the
build helper, **MUST NOT** be committed to git,
**MUST NOT** appear in any Step 4 / Step 5 /
Step 6 commit as a binary blob.

### §4.5 — Q5: install location and uninstall surface (LOCKED)

#### §4.5.1 — Install location

Step 4 **MUST** lock the default install location
as `%LOCALAPPDATA%\Programs\1C Agent Platform\`
(Inno Setup `{userpf}\1C Agent Platform`,
per-user install). The Step 4 `.iss` **MUST**
declare `PrivilegesRequired=lowest` and
`DefaultDirName={userpf}\1C Agent Platform`. The
Step 4 `.iss` **MUST NOT** declare
`PrivilegesRequired=admin` and **MUST NOT**
declare `DefaultDirName={pf}\1C Agent Platform`.

#### §4.5.2 — `PATH` modification

The Step 4 `.iss` **MUST NOT** modify the user's
`PATH` environment variable. The Step 4 `.iss`
**MUST NOT** modify the machine's `PATH`
environment variable. All references to the
bundled `python.exe` **MUST** use absolute
paths.

#### §4.5.3 — Uninstall registration

The Step 4 `.iss` **MUST** register an
Add/Remove Programs entry under
`HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\<key>`
(Inno Setup default behaviour under
`PrivilegesRequired=lowest`). The Step 4 `.iss`
**MUST NOT** register under
`HKLM\…\Uninstall\<key>`. The uninstall
registry entry **MUST** make the product visible
under *Settings → Apps → Installed apps* / *Control
Panel → Programs and Features*.

### §4.6 — Q6: production code byte-identical (LOCKED)

Step 4 **MUST NOT** modify any file under
`apps/*/src/` or `packages/*/src/`. The first-
run configurator (§8) **MUST** reuse
`onec_platform.installer.run_install_fast_path_from_json_file`
through `python.exe -c "..."` invocation,
exactly as that function exists at Step 3 HEAD.
Step 4 **MUST NOT** add a new `[project.scripts]`
entry exposing this helper. Step 4 **MUST NOT**
introduce a new module or entrypoint to
`onec_platform`.

### §4.7 — Q-extra: MVP base type (LOCKED)

The Track Q MVP scope **MUST** support **only
file-based 1C infobases** (Russian: *файловая
база 1С*). The first-run configurator (§8), the
Inno Setup wizard (§7), and the closure-gate
scenario (§5) all **MUST** be locked to this
single base type.

Track Q **MUST NOT** support, at any step: TCP-
cluster server bases (Russian: *клиент-
серверная база 1С*; `Srvr="<host>";Ref="<ib>";`
connection strings); HTTP-published bases
(`publication_name` + `http_base_url` fields);
web-server-published bases via Apache / IIS /
nginx; any base type that requires presenting
a username + password at connect time; any
base type that requires a 1C cluster manager
(`rmngr.exe`) or agent (`ragent.exe`) on a
separate host. The full denial list with sub-
categories is enumerated in §11.

This denial is grounded in repo facts:

- `EnvironmentConfig`
  (`packages/onec-config/src/onec_config/models.py:93-105`)
  has **no** `username` / `password` /
  `server_name` / `cluster_name` fields.
  Adding them is a production code change
  forbidden by §3.1.
- Pushing credentials into the existing
  argv-template fields
  (`onec_dumpcfg_command_template` etc.) is the
  engineering JSON UX that Step 1 plan §1 and
  Step 2 audit §10.4 named as the path Track Q's
  tiny configurator is replacing; engineering
  JSON UX **MUST NOT** be the primary user-
  facing path.
- A two-mode configurator (file + server) is
  the first step toward a rich GUI config
  editor — §11 denies that shape.

Operators with server-based 1C infobases
retain the existing orthogonal engineering
path: `scripts/release/install.ps1` invoked
with operator-authored input-config JSON.
This path remains byte-identical through
Track Q per §3.3; Track Q does **not**
deprecate, modify, or shadow it. A future
track **MAY** extend the data model;
Track Q **MUST NOT** open scope onto server-
based bases at any of its six steps.

---

## §5. Closure-gate scenario (normative)

This section pins exactly what "Track Q closed"
means in operational terms. Step 6 verification
(§14) **MUST** demonstrate every step in this
scenario successfully. The scenario **MUST** be
demonstrable on a Windows 10 or Windows 11 amd64
machine that has **no** preinstalled Python,
**no** pip, **no** git, and a user account that
**MAY** be non-administrative.

### §5.1 — The end-to-end happy path

1. **Operator builds setup.exe** on a control
   host using the Step 4 build helper.
   - Build helper fetches the pinned embeddable
     CPython 3.11 zip from python.org.
   - Build helper assembles the build directory
     (extracted embeddable + the eleven
     src-layout packages from `pyproject.toml:51-63`
     + the first-run configurator script + the
     uninstaller stub references).
   - Build helper invokes `iscc.exe` on
     `installers/windows/setup.iss`.
   - Output: a single `setup.exe` artefact under
     the build helper's chosen output directory.
2. **Operator transfers setup.exe** to the
   ordinary Windows user (out-of-band; mechanism
   is operator-side; not Track Q's concern).
3. **Ordinary user downloads setup.exe**, places
   it under their `Downloads` folder, double-
   clicks it.
4. **Inno Setup wizard appears** with the
   default Inno Setup UI: Welcome → License (if
   any; SHOULD be omitted for MVP) → Select
   Destination Location (defaulting to
   `%LOCALAPPDATA%\Programs\1C Agent Platform\`)
   → Select Start Menu Folder (defaulting to
   "1C Agent Platform") → Ready to Install →
   Installing → Finish.
5. **User clicks through Next / Install /
   Finish** without making any base-related
   decisions inside the wizard.
6. **At the end of the wizard** the user **MAY**
   tick "Launch 1C Agent Platform" (default
   ticked); on Finish, the Start menu shortcut
   target is invoked.
7. **First-run configurator runs.**
   - Configurator detects no
     `%LOCALAPPDATA%\1C Agent Platform\config.json`.
   - Configurator displays welcome message in a
     console window or a Windows.Forms message
     box (Step 4 picks one; the contract locks
     "minimal, native Windows surface").
   - Configurator opens
     `System.Windows.Forms.OpenFileDialog`
     prompting "Select 1cv8 executable"; filter
     "1cv8 binaries|1cv8.exe;1cestart.exe".
   - User picks a `1cv8.exe` or `1cestart.exe`.
   - Configurator opens
     `System.Windows.Forms.FolderBrowserDialog`
     prompting "Select file-based 1C infobase
     folder (must contain a `.1cd` file)". Per
     §4.7, server-based bases are not accepted.
   - User picks a folder containing a `.1cd`.
   - Configurator synthesises an input-config
     JSON with the locked MVP defaults (§8.4).
   - Configurator invokes bundled `python.exe -c
     "…"` to call
     `run_install_fast_path_from_json_file`.
   - On success, configurator displays the Claude
     MCP config snippet (§8.5) and copies it to
     the clipboard.
   - User reads the snippet, closes the window.
8. **User opens Claude (Desktop or CLI)** and
   pastes the snippet into Claude's MCP config.
9. **Claude spawns the MCP server** as a stdio
   subprocess on its next session. The server
   reads `%LOCALAPPDATA%\1C Agent Platform\config.json`,
   binds to the configured 1C base, and responds
   to MCP requests.
10. **Claude executes one read-only tool** (e.g.
    `ping` or `get_metadata_tree`) against the
    configured 1C base. The tool returns a
    real response derived from the configured
    infobase.
11. **User opens Settings → Apps → Installed apps**
    and sees "1C Agent Platform" listed.
12. **User clicks "Uninstall"** in *Settings →
    Apps*. The Inno Setup uninstaller removes
    `%LOCALAPPDATA%\Programs\1C Agent Platform\`,
    removes the Start menu folder, removes the
    HKCU Uninstall registry key.
13. **`%LOCALAPPDATA%\1C Agent Platform\config.json`
    survives** the uninstall (operator-side state,
    per §10).
14. **Claude's MCP config snippet survives** the
    uninstall (Claude-side state, per §10).

### §5.2 — Variants explicitly NOT in closure-gate

The closure-gate **MUST NOT** require any of the
following to be demonstrated:

- multi-base configuration (more than one
  EnvironmentConfig declared);
- write-server connectivity (the closure-gate
  ends at one successful read-tool execution);
- intelligence-server connectivity;
- Windows Service registration;
- code-signed setup.exe;
- `.msi` artefact;
- silent install (no-UI install via command-line
  flags);
- enterprise-fleet deployment (Group Policy /
  SCCM / Intune);
- update from a previous Track Q setup.exe
  (upgrade-in-place is **MAY** scope for Step 4,
  see §7.4);
- `1cv8.exe` headless launch by the platform
  itself (the platform reads metadata; running
  the 1C binary is operator-side);
- offline install with no internet access at
  build time (the build helper requires internet
  to fetch embeddable CPython; this is operator-
  side, not Track Q-side).

---

## §6. Installed files layout (locked)

### §6.1 — Install directory tree

The Step 4 `.iss` **MUST** declare the install
directory as `%LOCALAPPDATA%\Programs\1C Agent Platform\`
and **MUST** populate it with exactly the
following tree (file names are normative; the
Pascal-script formatters Inno Setup uses
internally **MAY** vary case slightly per Windows
filesystem behaviour):

```
%LOCALAPPDATA%\Programs\1C Agent Platform\
├── python\                              (bundled embeddable CPython 3.11)
│   ├── python.exe
│   ├── pythonw.exe
│   ├── python311.dll
│   ├── python311.zip                    (stdlib zipped)
│   ├── python311._pth                   (path config; see §6.3)
│   ├── vcruntime140.dll                 (shipped inside the embeddable zip)
│   └── ...                              (other embeddable bits per python.org)
├── mcp_read_server\                     (from pyproject.toml:52)
├── mcp_write_server\                    (from pyproject.toml:53)
├── mcp_intelligence_server\             (from pyproject.toml:54)
├── onec_platform\                       (from pyproject.toml:55)
├── mcp_common\                          (from pyproject.toml:56)
├── onec_process_runner\                 (from pyproject.toml:57)
├── onec_policy_engine\                  (from pyproject.toml:58)
├── onec_audit\                          (from pyproject.toml:59)
├── onec_health\                         (from pyproject.toml:60)
├── onec_troubleshooting\                (from pyproject.toml:61)
├── onec_config\                         (from pyproject.toml:62)
├── first_run.ps1                        (configurator + launcher)
├── unins000.exe                         (auto-generated by Inno Setup)
└── unins000.dat                         (auto-generated by Inno Setup)
```

The Step 4 `.iss` **MUST NOT** populate the
install directory with any of:

- a `.whl` file (the wheel itself; the install
  layout extracts wheel contents, not the wheel);
- a `dist/` subdirectory;
- a `tests/` subdirectory;
- any `scripts/*` content;
- any `docs/*` content (the recipe is published
  in-repo, not on user disk);
- a `.git/` subdirectory;
- a `pyproject.toml`;
- a `CHANGELOG.md`;
- a `SECURITY.md`;
- a `README.md`;
- a `LICENSE` file (the Step 4 `.iss` **MAY**
  include a `LICENSE.txt` page in the wizard; if
  it does, the file **MUST** be embedded
  declaratively in the `.iss` `[Files]` section,
  not copied into the install directory).

### §6.2 — Operator-side state directory tree

The first-run configurator (§8) **MUST** create
and populate `%LOCALAPPDATA%\1C Agent Platform\`
(NOT the `\Programs\` subtree — this is a
separate user-data path) with the following:

```
%LOCALAPPDATA%\1C Agent Platform\
├── config.json                          (product-config materialised by fast-path)
└── .runtime\                            (lazily created when the MCP server runs)
    └── ...                              (Phase 5 runtime state files)
```

This directory **MUST NOT** be touched by the
Inno Setup `.iss` `[Files]` section. It is
created by the configurator on first run, and by
`onec_platform.runtime` on first server run.

### §6.3 — `python311._pth` shape

The bundled embeddable distribution carries a
`python311._pth` file that controls `sys.path`.
The Step 4 build helper **MUST** edit this file
(at build time, against the extracted embeddable
directory) so that the eleven src-layout package
directories under the install root are
discoverable. Specifically, after build helper
runs, `python311._pth` **MUST** contain:

```
python311.zip
.
..
..\mcp_read_server
..\mcp_write_server
..\mcp_intelligence_server
..\onec_platform
..\mcp_common
..\onec_process_runner
..\onec_policy_engine
..\onec_audit
..\onec_health
..\onec_troubleshooting
..\onec_config
```

Step 4 **MUST NOT** modify `python311._pth` at
install time from the `.iss`. Step 4 **MUST**
modify `python311._pth` at build time from the
build helper, before `iscc.exe` consumes the
prepared build directory.

The `import site` line of the default embeddable
`_pth` **MUST** remain commented out, consistent
with the embeddable distribution's intent. The
Step 4 build helper **MUST NOT** install pip
into the embeddable runtime; the first-run
configurator does not use pip.

### §6.4 — Shortcut surface

The Step 4 `.iss` **MUST** declare:

- one Start menu shortcut named "1C Agent Platform"
  under `Start Menu\Programs\1C Agent Platform\`,
  pointing at:
  `powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Normal -File "%LOCALAPPDATA%\Programs\1C Agent Platform\first_run.ps1"`
- one Start menu shortcut named "Uninstall 1C Agent Platform"
  under the same Start menu folder, pointing at
  `unins000.exe`.

The Step 4 `.iss` **MUST NOT** declare:

- a desktop shortcut by default (the `.iss` **MAY**
  expose a "Create desktop icon" checkbox in the
  wizard, **default unchecked**);
- a Quick Launch shortcut;
- a pin-to-taskbar action;
- a Windows Terminal profile registration;
- a context menu shell extension.

---

## §7. Installer wizard scope and constraints

### §7.1 — Wizard pages: locked set

The Step 4 `.iss` **MUST** use only the standard
Inno Setup wizard pages:

- Welcome
- Select Destination Location
- Select Start Menu Folder
- Ready to Install
- Installing
- Finish

The Step 4 `.iss` **MUST NOT** add custom Pascal-
script wizard pages. The Step 4 `.iss` **MUST
NOT** add a "1cv8 binary picker" wizard page.
The Step 4 `.iss` **MUST NOT** add an "infobase
folder picker" wizard page. The Step 4 `.iss`
**MUST NOT** add an "MCP server selection"
wizard page. Base configuration **MUST NOT**
happen inside the wizard; it happens in the
first-run configurator (§8). This is a deliberate
Step 3 design choice: Pascal scripting for
Windows.Forms dialogs is brittle, the bundled
CPython is only fully present after `[Files]`
install completes, and the existing fast-path
helper requires the bundled interpreter to run.

### §7.2 — Wizard text language

The wizard text **MUST** be in Russian (the
project's primary operator language) or in
English; the Step 4 `.iss` **MAY** declare
either. The Step 4 `.iss` **MUST NOT** declare
both languages with a language-selection page
(simplicity over completeness).

### §7.3 — Wizard appearance

The Step 4 `.iss` **MUST** use the default Inno
Setup wizard appearance. The Step 4 `.iss`
**MUST NOT** include a custom wizard image
(`WizardImageFile` / `WizardSmallImageFile`
overrides). The Step 4 `.iss` **MAY** declare a
small `SetupIconFile` if a project-licensed icon
is available; if not, the Inno Setup default icon
is acceptable.

### §7.4 — Upgrade-in-place

Upgrade-in-place handling is **MAY** scope for
Step 4. If the Step 4 `.iss` declares upgrade-
in-place, it **MUST** use Inno Setup's standard
`AppId={…}` GUID with `UninstallExistingPath`
semantics so a second run of setup.exe replaces
the prior install. The upgrade flow **MUST NOT**
touch `%LOCALAPPDATA%\1C Agent Platform\config.json`
(operator-side state). If the Step 4 `.iss` does
not declare upgrade-in-place, a second run of
setup.exe **MUST** prompt the user to uninstall
the previous version first; the contract permits
either behaviour.

### §7.5 — Silent install

Silent install (`/SILENT` / `/VERYSILENT`
command-line flags) is **MAY** scope for Step 4.
If declared, silent install **MUST** still
require the first-run configurator on first
launcher invocation (configuration is not part
of the wizard, and silent install cannot bypass
configuration). The Step 4 recipe **MAY**
document the silent-install command line if
operator distribution scripts need it.

### §7.6 — Anti-virus and SmartScreen

The Step 4 `.iss` **MUST NOT** attempt to bypass
Windows Defender SmartScreen reputation checks.
Step 4 **MUST NOT** declare code-signing
metadata (Authenticode / EV / `SignTool` calls).
The Step 4 recipe **MUST** acknowledge in honest-
non-goals that an unsigned setup.exe is the
expected delivery shape and that SmartScreen
**MAY** display a "Windows protected your PC"
warning on first run; operators distributing
setup.exe in adversarial environments are
responsible for their own signing chain
(operator-side, not Track Q-side).

---

## §8. First-run configurator (one-base configuration)

This is the central new section of the contract.
The first-run configurator is **the** Track Q
deliverable that closes the "configure one base"
gap. The Step 2 audit §10.5 framing is superseded
by this section.

### §8.1 — Purpose

The first-run configurator transforms the
ordinary-Windows-user persona's two natural
inputs — "where is my 1C executable" and "where
is my infobase" — into a complete product-config
JSON the MCP servers can consume. The
configurator **MUST** be the user-facing surface
through which one-base configuration happens.
The configurator **MUST NOT** be a "rich config
editor"; it **MUST** be the smallest possible
surface that solves the persona problem.

### §8.2 — File: `first_run.ps1`

The Step 4 file surface **MUST** include exactly
one PowerShell script at
`installers/windows/first_run.ps1`. The Step 4
`.iss` **MUST** install this script as
`%LOCALAPPDATA%\Programs\1C Agent Platform\first_run.ps1`.
The script **MUST** be invoked by the Start menu
shortcut "1C Agent Platform" (§6.4). The script
LOC budget **MUST** be ≤ 300 LOC.

### §8.3 — Surface technology

The configurator **MUST** use:

- **PowerShell 5.1 or later** as the host
  language (Windows 10 and 11 ship PowerShell
  5.1 by default; the script **MUST NOT**
  require PowerShell 7+ as a prerequisite).
- **`System.Windows.Forms.OpenFileDialog`** for
  the 1cv8 executable picker (loaded via
  `Add-Type -AssemblyName System.Windows.Forms`).
- **`System.Windows.Forms.FolderBrowserDialog`**
  for the infobase folder picker.
- **`System.Windows.Forms.MessageBox`** for the
  welcome / success / error message boxes.

The configurator **MUST NOT** use:

- tkinter (the embeddable CPython does not ship
  tcl/tk by default; pulling tcl/tk would
  multiply the installed footprint significantly
  and violate the "minimal honest payload"
  principle);
- a custom WPF / WinUI / Avalonia GUI;
- a browser-based UI;
- an Electron / Tauri / web-view shell;
- a tray icon;
- a `tkinter` / `wxPython` / `PyQt` Python GUI
  (no new Python dependencies; pyproject byte-
  identical).

### §8.4 — Inputs and synthesised product-config

The configurator **MUST** collect exactly two
user-visible inputs:

1. **1cv8 executable path.** Either a `1cv8.exe`
   or a `1cestart.exe`; the file dialog filter
   **MUST** allow both.
2. **File-based 1C infobase folder path.** A
   directory containing a `.1cd` file (the 1C
   file-mode infobase artefact). The folder
   picker **MUST** validate that the path
   exists, is a directory, and contains at
   least one `.1cd` file at its top level.
   Per §4.7, a folder with no `.1cd` **MUST**
   be rejected (§8.9), not silently accepted
   with a synthesised connection string.

The configurator **MUST** synthesise an
input-config JSON (the operator-declared JSON
the existing fast-path helper consumes) with
exactly these fields, using exactly these MVP
defaults:

```json
{
  "product_name": "1C Agent Platform",
  "profile_name": "default",
  "project": {
    "environments": {
      "main": {
        "name": "main",
        "base_id": "main",
        "base_path": "<USER_SELECTED_INFOBASE_PATH>",
        "publication_name": "",
        "http_base_url": "",
        "dump_path": "<%LOCALAPPDATA%>\\1C Agent Platform\\dumps",
        "timeout_seconds": 600,
        "allow_write": false,
        "onec_binary_path": "<USER_SELECTED_1CV8_PATH>"
      }
    }
  },
  "default_environment": "main",
  "servers": { ... },
  "bootstrap": { ... }
}
```

The `<servers>` and `<bootstrap>` defaults **MUST**
be the minimal shapes the existing
`load_product_config` accepts; Step 4 **MAY**
inline these from the existing test fixtures
in-repo (if any are present) but **MUST NOT**
modify production code to provide them.

Field rationale:

- `name = "main"` / `base_id = "main"` /
  `default_environment = "main"` — single
  environment named "main" is the MVP
  expectation; multi-base is out-of-scope.
- `publication_name = ""` and
  `http_base_url = ""` — MVP scope is file-
  based 1C infobase only per §4.7. HTTP
  publication bases, web-server-published
  bases, and TCP-cluster server bases are
  out of scope of Track Q and **MUST NOT**
  be supported by the Step 4 configurator.
  Operators with server-based bases retain
  the existing engineering path through
  `scripts/release/install.ps1` plus a
  hand-authored input JSON (orthogonal to
  Track Q; see §4.7).
- `dump_path = "%LOCALAPPDATA%\1C Agent Platform\dumps"`
  — under the user's writable state directory,
  not the install directory.
- `timeout_seconds = 600` — 10 minutes, a
  defensible default; Step 4 **MAY** pick a
  different value with a grounded reason in
  the commit message.
- `allow_write = false` — read-only MVP; the
  closure-gate scenario §5 ends at one
  successful read-tool execution; write
  toggles are an operator's later, manual
  edit of `config.json`, not Track Q's
  responsibility.

### §8.5 — Fast-path invocation

The configurator **MUST** invoke the existing
fast-path helper exactly once per first-run, via
a `python.exe -c "..."` invocation that:

1. imports `run_install_fast_path_from_json_file`
   from `onec_platform.installer`;
2. calls it with `path = "<temp_input.json>"`,
   `output_config_path = "%LOCALAPPDATA%\1C Agent Platform\config.json"`,
   `confirm_write = True`;
3. prints the returned `InstallFastPathResult`'s
   `mode` and `ok` fields to stdout for the
   PowerShell script to capture;
4. exits with status 0 if `ok=True`, non-zero
   otherwise.

The configurator **MUST** delete the temp input
JSON after the fast-path returns, regardless of
outcome. The temp JSON **MUST** be created under
`%TEMP%\1C Agent Platform first run\` with a
unique filename, and the directory **MUST** be
removed on success.

The configurator **MUST NOT** edit
`config.json` directly with raw `Set-Content` /
`Out-File` calls bypassing the fast-path helper.
The fast-path helper's validation is the single
source of truth for product-config shape.

### §8.6 — Claude MCP config snippet

On successful fast-path completion, the
configurator **MUST** display the following
snippet (with the resolved absolute path
substituted in place of the placeholder):

```json
{
  "mcpServers": {
    "1c-agent-platform-read": {
      "command": "C:\\Users\\<USER>\\AppData\\Local\\Programs\\1C Agent Platform\\python\\python.exe",
      "args": ["-m", "mcp_read_server"]
    }
  }
}
```

The configurator **MUST**:

- compute the absolute path to the bundled
  `python.exe` at runtime (do not hardcode the
  user name);
- escape backslashes correctly in the displayed
  JSON;
- show the snippet in a Windows.Forms message
  box, in a console-friendly text block, OR
  written to a file the user can open (Step 4
  picks one of the three; the contract permits
  any).

The configurator **SHOULD** copy the snippet to
the clipboard via `Set-Clipboard` so the user
can paste it directly into Claude's MCP config.

The configurator **MUST NOT**:

- offer to auto-edit Claude's MCP config file
  (Claude's config is operator-side; auto-edit
  expands scope and risks corrupting an
  existing config);
- depend on Claude being installed when the
  configurator runs;
- check for Claude's installation status;
- expose `mcp-write-server` or
  `mcp-intelligence-server` in the default
  snippet (MVP = read-only; write/intelligence
  servers are exposed only by a user manually
  editing their MCP config to add additional
  entries).

### §8.7 — Configurator end-of-life

The configurator **MUST** exit after displaying
the snippet (with success status) or after
displaying an error (with non-zero status). The
configurator **MUST NOT**:

- run the MCP server as a child process (the
  server runs only when Claude spawns it);
- daemonise itself;
- install a tray icon;
- install a scheduled task;
- modify any Windows service;
- modify `HKCU\Run` or `HKLM\Run` for autostart.

### §8.8 — Subsequent runs of the Start menu shortcut

When the user invokes the Start menu shortcut
after first run (i.e., `config.json` already
exists), the configurator **MUST**:

- display the existing `config.json` summary
  (the two configured paths) in a Windows.Forms
  message box;
- redisplay the Claude MCP config snippet
  (§8.6);
- offer two buttons: "OK" (closes) and
  "Reconfigure" (re-runs §8.4 with the existing
  paths prefilled as dialog defaults).

The configurator **MUST NOT** silently
overwrite an existing `config.json` on
subsequent runs; the user **MUST** explicitly
choose "Reconfigure".

### §8.9 — Errors

The configurator **MUST** handle the following
honestly with a Windows.Forms error message box
and exit non-zero:

- user cancels the 1cv8 picker dialog;
- user cancels the infobase folder dialog;
- selected 1cv8 path does not exist when the
  picker returns (race condition);
- selected infobase folder does not exist when
  the picker returns;
- selected infobase folder exists but contains
  no `.1cd` file at its top level (the folder
  is not a valid file-based 1C infobase per
  §4.7); the message box **MUST** say in spirit
  that no `.1cd` was found, that server-based
  bases are not supported in this version, and
  **MUST** point at the operator recipe for the
  existing engineering path for server-based
  bases;
- fast-path helper returns `ok=False` (the
  message box **MUST** include the helper's
  error finding verbatim);
- bundled `python.exe` is missing (catastrophic
  install corruption; the message box **MUST**
  suggest reinstalling).

The configurator **MUST NOT**:

- silently retry on cancellation;
- guess a 1cv8 path if the picker is cancelled;
- guess an infobase path if the folder picker
  is cancelled.

### §8.10 — Idempotence

Running the configurator on the same machine
with the same user twice (with "Reconfigure")
**MUST** produce a `config.json` byte-identical
to what the first run produced if the user's
inputs are byte-identical. The configurator
**MUST NOT** include timestamps, UUIDs, or
machine-specific identifiers in the generated
`config.json` beyond what the fast-path helper
itself generates (the existing helper's output
shape is preserved; Track Q adds no fields).

---

## §9. Launch path after install

### §9.1 — The single user-facing launch surface

After install, the **only** user-facing launch
surface is the Start menu shortcut declared in
§6.4. The Step 4 `.iss` **MUST NOT** declare
multiple launch shortcuts. The Step 4 `.iss`
**MUST NOT** install a tray icon. The Step 4
`.iss` **MUST NOT** install an autostart entry.

### §9.2 — What happens when the user clicks the shortcut

Clicking the "1C Agent Platform" Start menu
shortcut **MUST** invoke
`powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Normal -File "%LOCALAPPDATA%\Programs\1C Agent Platform\first_run.ps1"`
in a normal console window.

The PowerShell script's behaviour **MUST** be
defined in §8.

### §9.3 — How Claude reaches the MCP server

After the user completes first-run
configuration and pastes the Claude MCP config
snippet into Claude's MCP config:

- Claude **MUST** be responsible for spawning
  the MCP server subprocess (stdio-based, per
  the MCP protocol).
- The Step 4 `.iss` **MUST NOT** spawn the MCP
  server itself.
- The first-run configurator **MUST NOT** spawn
  the MCP server itself.
- The Step 4 deliverable **MUST NOT** include
  any "server lifecycle daemon" — the existence
  of `onec_platform.runtime` is an internal-to-
  the-platform process supervisor for
  declarative subprocesses, NOT a Claude-
  facing daemon.

### §9.4 — Server selection

The default Claude-connect target **MUST** be
`mcp_read_server` (read-only, registry size 15).

Track Q **MUST NOT** wire `mcp_write_server`
(registry size 25) or `mcp_intelligence_server`
(registry size 16) into the default Claude MCP
config snippet. Users who want write or
intelligence semantics **MUST** add additional
entries to their Claude MCP config manually,
using the same `python.exe` path and the
appropriate module name.

The Step 4 recipe (§12) **MUST** document the
write and intelligence module names so users
who need them know what to add. The recipe
**MUST** also document the safety implications
of enabling write (the `allow_write = false`
default in `config.json` is the gating
boundary).

---

## §10. Uninstall boundary

### §10.1 — Uninstall verb

The uninstall verb is exposed through:

- *Settings → Apps → Installed apps → 1C Agent Platform → Uninstall*;
- *Control Panel → Programs and Features → 1C Agent Platform → Uninstall*;
- the "Uninstall 1C Agent Platform" Start menu
  shortcut (§6.4).

All three surfaces **MUST** invoke
`%LOCALAPPDATA%\Programs\1C Agent Platform\unins000.exe`
(auto-generated by Inno Setup).

### §10.2 — What uninstall removes

The Inno Setup uninstaller **MUST** remove:

- the entire install directory
  `%LOCALAPPDATA%\Programs\1C Agent Platform\`
  including the bundled Python, the eleven
  src-layout packages, `first_run.ps1`, and
  `unins000.exe` itself (Inno Setup self-
  removal);
- the Start menu folder
  `Start Menu\Programs\1C Agent Platform\`
  including both shortcuts;
- the HKCU Uninstall registry key.

### §10.3 — What uninstall MUST preserve

The Inno Setup uninstaller **MUST NOT** remove:

- `%LOCALAPPDATA%\1C Agent Platform\config.json`
  (operator-side state; the user's configured
  paths to 1cv8 and infobase);
- `%LOCALAPPDATA%\1C Agent Platform\.runtime\`
  (operator-side state; persistent runtime
  state files);
- `%LOCALAPPDATA%\1C Agent Platform\dumps\`
  (operator-side state; previously created
  dumps);
- the user's Claude MCP config (Claude-side
  state, not under Inno Setup's purview);
- the 1C platform itself (`1cv8.exe`,
  `1cestart.exe`, the configured infobase);
- any registry keys not created by Inno Setup
  itself.

This boundary mirrors Track M §7.3 ("What
uninstall does NOT touch") and Track L's
preservation discipline. Operator-side state
survives the uninstall by design.

### §10.4 — Reinstall semantics

If the user uninstalls and later reinstalls
setup.exe:

- the install directory is re-populated;
- the Start menu folder is re-created;
- the HKCU Uninstall registry key is re-
  written;
- the first-run configurator detects the
  preserved `config.json` and behaves as
  §8.8 (subsequent run) — the user is NOT
  re-prompted for paths unless they choose
  "Reconfigure".

### §10.5 — User-initiated config wipe

A user who wants to "reset to factory" **MUST**
manually delete `%LOCALAPPDATA%\1C Agent Platform\config.json`.
Track Q **MUST NOT** ship a "reset" UI in the
configurator (overengineering); the user opens
File Explorer and deletes the file. The Step 4
recipe **MUST** document this path.

---

## §11. Honest non-goals (denial list)

This section is the §13-equivalent of Track M's
recipe — the normative denial list. The Step 4
recipe **MUST** include a non-goals section
mirroring this list verbatim or in operator-
friendly paraphrase. The Step 6 closure
**MUST** reference this list as the basis for
"what 'Track Q closed' does and does not
claim".

### §11.1 — Track Q does NOT close any of:

- "All Windows installer ecosystem solved" —
  denied. Track Q closes one narrow path:
  Inno Setup setup.exe on Windows 10/11 amd64
  for the ordinary-Windows-user persona.
- "Enterprise installer" — denied. No Group
  Policy templates, no SCCM packaging, no
  Intune publishing, no MSI ecosystem
  integration.
- "Code-signed distribution" — denied. setup.exe
  is unsigned; SmartScreen warnings on first run
  are expected.
- "PyPI publication" — denied. Track M non-goal
  preserved.
- "Auto-update / OTA / delta-update" — denied.
  No in-platform updater; a new setup.exe
  release is an operator-side rebuild + reship.
- "GUI dashboard / web admin panel" — denied.
  No dashboard.
- "Rich GUI config editor" — denied. The first-
  run configurator collects exactly two paths
  (§8.4) via native Windows file dialogs; it
  is not an editor.
- "Multi-base configuration" — denied. The MVP
  scope is exactly one 1C base
  (`default_environment = "main"`); operators
  who need multi-base **MUST** edit
  `config.json` manually with awareness of the
  product-config shape.
- "Server-based / client-server 1C infobase
  (клиент-серверная база)" — denied per §4.7.
  TCP-cluster bases (`Srvr="…";Ref="…"`),
  HTTP-published bases, web-server-published
  bases, and any base requiring username/
  password credentials at connect time are
  out of scope at every step. Grounding and
  alternative engineering path are in §4.7.
- "Write-server enabled by default" — denied.
  `allow_write = false`; the closure-gate
  scenario ends at one successful read-tool
  execution.
- "Windows Service / autostart" — denied. The
  installer **MUST NOT** register a Windows
  Service. Server lifecycle is owned by
  Claude's MCP client (stdio subprocess
  spawning).
- "Tray icon / background daemon" — denied. The
  configurator exits after first run.
- "Chocolatey / winget / Scoop / NuGet / Store
  publication" — denied. Track Q ships a
  standalone setup.exe; package-manager
  distribution is a future track's concern.
- "macOS installer / Linux installer" — denied.
  Windows 10/11 amd64 only.
- "ARM64 / x86 Windows support" — denied. amd64
  only.
- "Windows 7 / Windows Server support" — denied.
  Windows 10 + 11 amd64 only.
- "Silent install solves enterprise rollout" —
  denied. Silent install (§7.5) is a MAY
  feature; enterprise rollout is out-of-scope
  regardless.
- "Production-ready desktop app" — denied. The
  platform is a CLI MCP server bundle; the
  installer is the smallest honest delivery
  primitive for the ordinary-Windows-user
  persona.
- "Hostile-internet distribution" — denied.
  setup.exe is delivered out-of-band between
  the operator and the user; Track Q ships no
  hostile-internet update channel.
- "Test suite shipping" — denied. Track P
  territory.
- "Observability redesign" — denied. Track N
  preserved.
- "Service-supervision redesign" — denied.
  Track L preserved.
- "Auth redesign" — denied. Track D / Track H
  preserved.
- "Transport redesign" — denied. Track G /
  Track H preserved.
- "Registry change" — denied. read=15 /
  write=25 / intelligence=16 preserved.
- "New CLI flag on existing servers" — denied.
- "New `[project.scripts]` entries" — denied.
- "New project dependencies" — denied.
- "New entrypoint module" — denied.
- "Production code change" — denied. Zero
  changes to `apps/*/src/` or `packages/*/src/`
  across all six Track Q steps.

---

## §12. Step 4 PATH lock, file surface, LOC caps, forbidden-files list

### §12.1 — PATH lock

The Step 4 PATH is **PATH B** (operator recipe +
Inno Setup `.iss` + first-run configurator +
build helper). PATH A (docs-only, no `.iss`) is
**rejected** because docs alone cannot ship a
buildable setup.exe; the Track M §6.1
"buildable artefact" gate applies. PATH C
(installer-definition without recipe) is
**rejected** because an `.iss` without an
operator recipe is not honestly documentable.

### §12.2 — Step 4 file surface (locked)

The Step 4 commit **MUST** add exactly four new
files, no more, no fewer:

1. **`docs/operators/installer/windows-setup-exe.md`**
   — operator-facing recipe. 8–12 sections.
   ≤ 1200 LOC. Operator-friendly tone consistent
   with Track J / Track L / Track M / Track N
   recipes.
2. **`installers/windows/setup.iss`** — Inno
   Setup definition. ≤ 250 LOC. Pascal-script
   `[Code]` section limited to upgrade-in-place
   handling if §7.4 is exercised; no other
   Pascal scripting.
3. **`installers/windows/first_run.ps1`** —
   first-run configurator. ≤ 300 LOC. Surface
   strictly as §8.
4. **`installers/windows/build-setup-exe.ps1`**
   — build helper. ≤ 200 LOC. Fetches pinned
   embeddable CPython zip, prepares build
   directory, edits `python311._pth`, invokes
   `iscc.exe` against `setup.iss`.

Total Step 4 LOC cap = 1950.

### §12.3 — Step 4 forbidden-files list (locked)

The Step 4 commit **MUST NOT** modify or create:

- any file under `apps/*/src/`;
- any file under `packages/*/src/`;
- `pyproject.toml`;
- `.python-version`;
- any file under `scripts/*`;
- `SECURITY.md`;
- `CHANGELOG.md`;
- `README.md`;
- `PROJECT-STATUS.md`;
- `LICENSE`;
- `apps/platform/README.md`;
- any file under `docs/operators/deployment-boundary.md`,
  `docs/operators/observability.md`,
  `docs/operators/packaging/`,
  `docs/operators/service/`,
  `docs/dev/`;
- any file under `docs/architecture/track-{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p}-*.md`
  (Track Q's own architecture surface remains
  byte-identical to its current Step 3 state
  after Step 3 commits this contract);
- `docs/release-handoff.md`;
- any manual under `docs/`;
- `.github/workflows/dev-check.yml` (default;
  the only exception is the §3.8 narrow Windows-
  runner extension if Step 4 surfaces a
  grounded reason);
- any test file (no `tests/` directory creation;
  that is Track P territory);
- any binary file extension: `.zip`, `.exe`,
  `.dll`, `.pyd`, `.msi`, `.cab`, `.7z`,
  `.tar.*`, `.gz`, `.bz2`, `.xz`, `.ico` (the
  installer icon, if any, **MUST** be the Inno
  Setup default, not a committed `.ico`),
  `.bmp`, `.png`, `.jpg`, `.gif`, `.webp`.

### §12.4 — Step 4 commit-message expectations

The Step 4 commit message **MUST**:

- name the four added files explicitly;
- cite this contract by section number for each
  major decision;
- explicitly state "no production code change";
- explicitly state "no `pyproject.toml` change";
- explicitly state "no `scripts/*` change";
- explicitly state the registry invariant
  `read=15 / write=25 / intelligence=16`;
- explicitly state "no binary committed";
- explicitly state "no remote push";
- explicitly state "no `1cv8.exe` run".

### §12.5 — Step 4 verification

The Step 4 commit **MUST** be verifiable by:

- `git diff --stat HEAD~1` showing exactly four
  added files and zero modified files;
- `git diff --diff-filter=M HEAD~1` returning
  empty;
- `python scripts/dev/selfcheck.py` (with
  bootstrap_paths.ps1 sourced)
  → `selfcheck_status = ok`;
- `git ls-files` containing all four added
  paths.

Step 4 verification **MAY** also include a manual
"does iscc.exe produce setup.exe" run on the
operator's control host, but this is operator-
side and not a contract obligation; the in-repo
verification is `git diff` and `selfcheck.py`.

---

## §13. Step 5 forbidden-files list (locked)

Step 5 is the narrow docs/release alignment step.
The Step 5 commit **MUST**:

- add narrow CLASS-1 wording to `README.md`
  (Quickstart paragraph extension pointing at
  the Windows setup.exe path) and/or
  `PROJECT-STATUS.md` (Track Q closure
  narrative) — total CLASS-1 wording ≤ 50 LOC
  added across both files;
- **MAY** add ≤ 1 bullet to
  `docs/release-handoff.md` "Where to read
  deeper" section;
- **MAY** add ≤ 1 bullet to
  `scripts/release/README.md` pointing at the
  Step 4 recipe;
- **MAY** add a narrow cross-link in
  `docs/operator-manual.md`.

The Step 5 commit **MUST NOT**:

- modify any file under `apps/*/src/`;
- modify any file under `packages/*/src/`;
- modify `pyproject.toml`;
- modify any `.ps1` / `.py` script under
  `scripts/*` (the `scripts/release/README.md`
  is the only `scripts/*` file Step 5 **MAY**
  touch);
- modify any Track Q architecture document
  (plan / step-map / audit / contract — all
  four byte-identical at Step 5);
- modify any other Track's architecture
  document;
- modify any existing operator recipe;
- modify the Step 4 file surface (recipe /
  `.iss` / `first_run.ps1` / `build-setup-exe.ps1`);
- modify the Track O / Track M / Track L /
  Track J / Track N / Track P documents;
- modify any registry;
- modify any binary;
- introduce a new file outside the four-file
  Step 4 surface and the narrow Step 5
  CLASS-1 surface above;
- declare Track Q "closed" (closure language
  is reserved for Step 6 per §3.11).

---

## §14. Q7 framing for Step 6

### §14.1 — What Step 6 does

Step 6 is the final integration pass. It:

- verifies every §3 carry-through invariant
  holds end-to-end across the six Track Q
  commits;
- verifies the closure-gate scenario §5
  end-to-end (operator-side; the verification
  is documented in Step 6's commit message but
  cannot be executed by CI given the no-Windows-
  runner default of §3.8);
- updates `README.md` "Closed parallel tracks"
  list to add Track Q (or to an "out-of-order
  closure" subsection if Track P is still
  active);
- appends a Track Q closure entry to
  `CHANGELOG.md`;
- locks the Q7 SemVer decision;
- writes the closure narrative into
  `PROJECT-STATUS.md` "Статус" section.

### §14.2 — Q7 directional framing (not locked)

The Q7 decision is **deferred to Step 6**. This
section frames the three possible outcomes
without locking one.

#### §14.2.1 — Q7 = NO-BUMP

NO-BUMP would require Track Q to ship **no new
buildable artefact**. PATH B (§12.1) ships a
buildable `.iss` + a configurator + a build
helper; these are buildable artefacts even if
they are scripts rather than compiled binaries.
**NO-BUMP is therefore inconsistent with PATH B**
and SHOULD NOT be Step 6's outcome under the
locked PATH B. If Step 6 nonetheless picks
NO-BUMP, the commit message **MUST** surface a
grounded reason that explains how the new file
surface is not a buildable artefact.

#### §14.2.2 — Q7 = PATCH

PATCH would treat Track Q as a "narrow new
operator surface that does not change the
declared `[project.scripts]` / `[project.dependencies]`
/ public Python API of the platform". This is
the **most likely** Step 6 outcome and the audit-
leaning default per Step 2 §11.7. The Track I
PATCH precedent (`installer.py` +15 LOC defect
repair) and the Track M PATCH precedent
(`pyproject.toml` 11-element `packages` flip)
both involved narrow changes to the existing
declared surface; Track Q's situation differs
(no existing declared surface modified) but the
PATCH framing fits the SemVer §6
"backward-compatible additions of functionality
that do not modify public API" reading.

If Step 6 picks PATCH, the commit **MUST**
modify `pyproject.toml` to bump `version` from
`0.5.2` to `0.5.3` (or whichever PATCH version
is next at Step 6 time). This is the **only**
exception to the §3.2 byte-identical invariant,
and it applies **only** to the Step 6 commit,
**only** to the `version` line.

#### §14.2.3 — Q7 = MINOR

MINOR would treat Track Q as a "backward-
compatible declaration of a new operator-visible
surface". The Add/Remove Programs registration
(§4.5.3), the new operator recipe (§12.2 file
1), and the new build artefact class
(setup.exe) **could** be read as a new operator-
visible surface in the §11 SemVer sense. Step 6
**MAY** pick MINOR if it concludes that the
combined effect of these surfaces crosses the
"new operator-visible surface" threshold.

If Step 6 picks MINOR, the commit **MUST**
bump `pyproject.toml` `version` from `0.5.2` to
`0.6.0` (or whichever MINOR version is next at
Step 6 time).

### §14.3 — MAJOR is forbidden

Step 6 **MUST NOT** bump MAJOR. Track Q does
not break backward compatibility in any
declared surface. MAJOR would be inconsistent
with the §3 byte-identical invariants which
preserve every existing declared surface.

### §14.4 — Step 6 file surface (advance framing)

Step 6 **MUST** be a narrow integration commit.
Step 6 **MUST**:

- modify `README.md` to add Track Q to the
  closed-tracks list (or an out-of-order
  closure subsection);
- modify `PROJECT-STATUS.md` to write the
  closure narrative;
- modify `CHANGELOG.md` to append the closure
  entry;
- modify `pyproject.toml` `version` line **only
  if** Q7 = PATCH or MINOR.

Step 6 **MUST NOT** modify any other file. In
particular, Step 6 **MUST NOT** modify the
Step 4 file surface (`.iss` / `first_run.ps1`
/ `build-setup-exe.ps1` / recipe) — those are
locked at Step 4 commit. Step 6 **MUST NOT**
modify any production code. Step 6 **MUST NOT**
modify any other architecture document.

---

— end of contract —
