# Operator-Facing Windows Installer Recipe — `setup.exe`

> **Audience.** Operators building, distributing, installing,
> uninstalling, or upgrading the 1C Agent Platform as a Windows
> `setup.exe` for an *ordinary Windows user* persona — a person
> on Windows 10 or Windows 11 amd64 who does **not** have
> Python, `pip`, or `git` installed and is **not** going to install
> them.
>
> **What this document is.** A practical operator recipe for the
> narrow, honestly supported Windows installer boundary of the
> 1C Agent Platform. The normative source-of-truth for every
> claim below is the Track Q Step 3 contract
> (`docs/architecture/track-q-windows-installer-path-and-setup-exe-delivery-contract.md`).
> This recipe operationalizes that contract for the four
> lifecycle verbs operators care about: **build**, **install**,
> **uninstall**, **upgrade**, and **verify**.
>
> **What this document is NOT.** It is not a claim that
> "Windows installation is solved forever". It is not an
> enterprise rollout playbook. It is not a code-signing manual.
> It is not a GUI dashboard recipe. It does not document
> support for server-based / client-server 1C infobases — see
> §9 for the existing engineering path for those. The full
> denial list is in §11.

---

## 1. Purpose and scope

You are reading this because you have built or received the
1C Agent Platform source tree and you need to produce a single
`setup.exe` that an ordinary Windows user can double-click
to install, run once to configure a single file-based 1C
infobase, and connect Claude to as a local stdio MCP server —
without ever installing Python themselves.

This document answers, in order:

- what the `setup.exe` artefact installs and where (§2);
- what tooling you (the operator) need on the build host (§3);
- how to build the `setup.exe` (§4);
- how to distribute the `setup.exe` to the end user (§5);
- what the end user sees on install (§6);
- how to verify a working install (§7);
- how to uninstall (§8);
- how to upgrade (§9);
- what to do for server-based 1C infobases (§10 — the
  existing engineering path, unchanged by Track Q);
- cross-references to other operator recipes (§11);
- honest non-goals — what this recipe deliberately does
  **not** cover (§12).

### 1.1 What this is for

- One place to look when an operator asks "how do I produce
  a Windows installer for a 1C Agent Platform release?".
- One place to look when an operator asks "what exactly
  does the installer drop on the end user's machine?".
- One place to look when an operator asks "what does the
  end user see, and how do they get Claude to talk to the
  installed server?".
- One place to look when an operator asks "how do I
  uninstall this cleanly?".

### 1.2 What this is NOT for

- A general Windows installer tutorial. We use Inno Setup
  with a single `.iss` file under
  `installers/windows/setup.iss`; we do not survey the
  installer ecosystem.
- A code-signing recipe. The `setup.exe` we ship is
  unsigned. Windows Defender SmartScreen will show a
  "Windows protected your PC" warning on first run on a
  fresh machine. Operators who distribute in adversarial
  environments need to establish their own signing chain
  out of band — that work is not in scope.
- A multi-base configuration recipe. The Track Q MVP
  scope is exactly one 1C base
  (`default_environment = "main"`). Operators with multi-
  base needs edit `config.json` manually after first run.
- A server-based 1C infobase recipe. See §10.
- A Windows Service / autostart recipe. The installer
  does **not** register a Windows Service. The MCP server
  is spawned on demand by Claude's MCP client.

---

## 2. What the installer produces and installs

### 2.1 Installer artefact

The build produces exactly one artefact:

```
dist/installer/1c-agent-platform-setup.exe
```

The artefact is a standard Inno Setup self-extracting
`setup.exe`. It is unsigned. It is built for Windows 10 + 11
amd64. There is **no** `.msi` produced; there is **no**
`.zip` portable distribution; there is **no** per-architecture
or per-Windows-version matrix.

### 2.2 Installed file layout

On the end-user machine, after `setup.exe` finishes, the
following layout exists under `%LOCALAPPDATA%\Programs\1C Agent Platform\`
(per-user install, no admin elevation, contract §6.1):

```
%LOCALAPPDATA%\Programs\1C Agent Platform\
├── python\                            (bundled embeddable CPython 3.11)
│   ├── python.exe
│   ├── pythonw.exe
│   ├── python311.dll
│   ├── python311.zip                  (stdlib, zipped)
│   ├── python311._pth                 (rewritten at build time per §6.3)
│   ├── vcruntime140.dll
│   └── (other embeddable files from python.org)
├── mcp_read_server\                   (the eleven src-layout
├── mcp_write_server\                   packages copied verbatim
├── mcp_intelligence_server\            from apps/*/src/ and
├── onec_platform\                      packages/*/src/, per
├── mcp_common\                         pyproject.toml:51-63)
├── onec_process_runner\
├── onec_policy_engine\
├── onec_audit\
├── onec_health\
├── onec_troubleshooting\
├── onec_config\
├── first_run.ps1                      (configurator + launcher target)
├── unins000.exe                       (Inno Setup uninstaller)
└── unins000.dat                       (uninstall log)
```

Start menu entries:

```
Start Menu\Programs\1C Agent Platform\
├── 1C Agent Platform.lnk              → first_run.ps1 (via powershell.exe)
└── Uninstall 1C Agent Platform.lnk    → unins000.exe
```

Registry entries:

- `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{B7D4F2E9-5A6C-4B8F-9E1A-3D2C8F5A7B14}_is1`
  (auto-written by Inno Setup under `PrivilegesRequired=lowest`;
  this is what makes the product appear in *Settings → Apps*).

Operator-side state, created lazily by `first_run.ps1` and
the runtime, under `%LOCALAPPDATA%\1C Agent Platform\`
(NOT the `Programs\...` subtree — this is a separate
writable path):

```
%LOCALAPPDATA%\1C Agent Platform\
├── config.json        (product-config; written by first_run.ps1
│                       through the existing fast-path helper)
├── .runtime\          (created lazily when an MCP server runs)
└── dumps\             (created lazily for DumpCfg targets)
```

The installer itself does **not** create
`%LOCALAPPDATA%\1C Agent Platform\` — `first_run.ps1` does,
on first run.

---

## 3. Prerequisites on the build host

You (the operator) need exactly two things on the build host:

1. **Windows 10 or Windows 11 amd64.** Cross-platform builds
   are not supported. Linux + Wine is not supported.
2. **Inno Setup 6**, installed from
   `https://jrsoftware.org/isdl.php`. The build helper
   searches the standard `Program Files` locations; if
   yours is unusual, pass `-IsccPath <full path to ISCC.exe>`.
3. **Windows PowerShell 5.1+** (ships with every Windows 10
   and 11 machine; nothing to install).
4. **Internet access** at build time, to fetch the python.org
   embeddable distribution. The build helper downloads
   `python-3.11.<x>-embed-amd64.zip` directly from
   `https://www.python.org/ftp/python/`. There is **no**
   mirror; offline builds are not supported in Track Q
   scope.

That is the entire prerequisite list. You do **not** need:

- Python on the build host (the build helper fetches it).
- `pip` on the build host.
- `git` on the build host (though you almost certainly used
  it to obtain the source tree).
- Any IDE.
- Any code-signing certificate.
- Any AV exemption (Inno Setup output sometimes triggers
  Windows Defender heuristic checks; treat that as
  operator-side, out of Track Q scope).

---

## 4. Build verb

### 4.1 Default invocation

From the project root, in a Windows PowerShell session:

```powershell
pwsh installers\windows\build-setup-exe.ps1
```

(Or `powershell.exe` if you are on PowerShell 5.1.)

The build helper:

1. resolves `iscc.exe` (Inno Setup compiler);
2. fetches the python.org embeddable CPython 3.11 zip into
   `build\python.zip`, extracts to `build\python\`, deletes
   the zip;
3. rewrites `build\python\python311._pth` so the eleven
   src-layout packages will be importable from the
   installed location (per contract §6.3);
4. copies the eleven src-layout packages from
   `apps/*/src/<module>` and `packages/*/src/<module>` into
   `build\packages\<module>\`, stripping `__pycache__` and
   `.pyc` files;
5. copies `installers\windows\first_run.ps1` into
   `build\first_run.ps1`;
6. invokes `iscc.exe /O<output_dir> installers\windows\setup.iss`;
7. prints the location of the produced `setup.exe`.

Default output: `dist\installer\1c-agent-platform-setup.exe`.

Both `build\` and `dist\` are gitignored. Do **not** commit
either directory — the embeddable Python zip is treated as
a build-time fetch artefact, never a tracked binary.

### 4.2 Parameters

| Parameter             | Default                                                                  | When to override                                              |
|-----------------------|--------------------------------------------------------------------------|---------------------------------------------------------------|
| `-PythonEmbedVersion` | `3.11.9`                                                                 | When pinning a different patch within Python 3.11.            |
| `-PythonEmbedUrl`     | computed from version                                                    | When mirroring python.org behind a corporate proxy.           |
| `-IsccPath`           | searches `Program Files [(x86)]\Inno Setup 6\ISCC.exe`                   | When `ISCC.exe` is in an unusual location.                    |
| `-OutputDir`          | `<repo>\dist\installer`                                                  | When writing setup.exe elsewhere.                             |
| `-SkipFetch`          | off                                                                      | When iterating on `setup.iss` and reusing the existing embed. |

`.python-version` pins the major-minor (currently `3.11`);
the patch you choose with `-PythonEmbedVersion` must remain
inside `3.11.x` to satisfy contract §3.2. Bumping the
patch is operator-side and does **not** require a
project version bump.

### 4.3 Expected build duration and footprint

- First clean build with embedded fetch:
  approximately 30–90 seconds depending on network. The
  embeddable zip is roughly 10 MB.
- `-SkipFetch` build:
  approximately 5–15 seconds (just copy packages + run
  iscc.exe).
- Output `setup.exe` size:
  approximately 10–15 MB compressed (`Compression=lzma2`).
- Installed footprint on the end user's machine after
  install: approximately 10–15 MB (contract §9 supported
  range).

### 4.4 What the build helper does NOT do

- It does **not** modify any production code.
- It does **not** modify `pyproject.toml`.
- It does **not** modify `scripts/*`.
- It does **not** modify `.python-version`.
- It does **not** modify any registry on the build host.
- It does **not** install Python on the build host.
- It does **not** install `pip` on the build host.
- It does **not** commit anything to git.
- It does **not** push anything to a remote.
- It does **not** sign the produced `setup.exe`.

---

## 5. Distribute verb

The `setup.exe` artefact is delivered out of band between
you (the operator) and the end user. Examples of acceptable
delivery channels:

- direct download from your internal release server;
- internal file share;
- USB drive;
- corporate distribution system (your own MDM / SCCM /
  Intune flow — Track Q does not opinionate on this);
- an email attachment if your size budget allows.

Track Q does **not** ship a delivery channel. There is **no**
auto-update mechanism. A new release is a fresh `setup.exe`
the operator distributes again.

### 5.1 SmartScreen on first download

On a fresh Windows machine the first time the user runs an
unsigned `setup.exe` downloaded from the internet, Windows
Defender SmartScreen displays:

> **Windows protected your PC**
> Microsoft Defender SmartScreen prevented an unrecognized
> app from starting. Running this app might put your PC at
> risk.
>
> [More info]

The user clicks "More info" then "Run anyway". This is
expected behaviour for an unsigned installer; it is **not**
a Track Q bug. If your audience is unwilling to click
through SmartScreen, sign the produced `setup.exe` with
your own certificate before distribution (out of scope of
this recipe).

---

## 6. Install verb (end user view)

### 6.1 The user double-clicks `setup.exe`

The Inno Setup wizard opens with the standard pages:

1. **Welcome** — "Welcome to the 1C Agent Platform Setup
   Wizard". User clicks Next.
2. **Select Destination Location** — default
   `%LOCALAPPDATA%\Programs\1C Agent Platform`. User
   accepts default (recommended) or picks another folder.
   No admin elevation requested.
3. **Ready to Install** — summary screen. User clicks
   Install.
4. **Installing** — file copy progress.
5. **Finish** — "Setup has finished installing 1C Agent
   Platform on your computer". A "Launch 1C Agent
   Platform" checkbox is present, **unchecked** by default
   (the user can tick it to run `first_run.ps1` right
   away, or leave it and use the Start menu shortcut).

The wizard does **not** prompt for a 1C base, a 1cv8 path,
credentials, or anything else. All configuration happens
afterwards in `first_run.ps1` (§6.2).

### 6.2 First run of `first_run.ps1`

When the user clicks the Start menu entry "1C Agent
Platform" (or the wizard's "Launch on Finish" checkbox if
they ticked it), a PowerShell console window opens briefly
while Windows Forms initialises, then the configurator
runs:

1. **Welcome message** — Windows.Forms.MessageBox saying
   the user will be asked for two paths.
2. **1cv8 executable picker** — `OpenFileDialog` with
   filter `1cv8.exe;1cestart.exe`. User selects their
   1cv8 binary. (Typically
   `C:\Program Files\1cv8\<version>\bin\1cv8.exe`.)
3. **File-based infobase folder picker** —
   `FolderBrowserDialog`. User selects a folder containing
   a `.1cd` file at the top level. The configurator
   validates this; folders without a `.1cd` are rejected
   with an honest error message pointing the user at this
   recipe's §10.
4. **Fast-path invocation** — the configurator synthesises
   an input-config JSON with locked MVP defaults
   (one environment named `main`, `allow_write=false`,
   `dump_path=%LOCALAPPDATA%\1C Agent Platform\dumps`,
   `work_dir=%LOCALAPPDATA%\1C Agent Platform\.runtime`,
   `servers.read=true`, others false), writes it to a
   temp file, and invokes the bundled `python.exe` with
   a short `-c` snippet that calls the existing
   `onec_platform.installer.run_install_fast_path_from_json_file`.
   On success, `config.json` is written under
   `%LOCALAPPDATA%\1C Agent Platform\`.
5. **Claude MCP snippet** — Windows.Forms.MessageBox
   displaying the exact JSON snippet to paste into
   Claude's MCP config:

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

   The snippet is also copied to the clipboard via
   `Set-Clipboard`. The actual `<USER>` segment is
   resolved at runtime from the install location.

6. **User closes the dialog.** The configurator exits.
   No MCP server is left running. The system is
   configured and idle, waiting for Claude to spawn
   the read server on demand.

### 6.3 Subsequent runs of the Start menu shortcut

If the user clicks "1C Agent Platform" again later (with
`config.json` already present), the configurator shows
an *existing configuration* summary (the two paths) and
offers two buttons:

- **OK** — redisplays the Claude MCP snippet + clipboard
  copy. Useful after a Windows reinstall, when the user
  needs the snippet again.
- **Cancel (Reconfigure)** — re-runs the picker flow,
  pre-filling the dialogs with the current paths.

### 6.4 What the end user does NOT do

The end user does **not**:

- install Python;
- install `pip`;
- install `git`;
- clone the repository;
- edit any JSON manually as the primary path;
- start the MCP server themselves (Claude spawns it);
- run any command-line invocation;
- configure a Windows Service;
- configure autostart;
- install a tray application;
- deal with multi-base configuration.

---

## 7. Verify verb

Verification at three levels.

### 7.1 Build-side verification

After running `build-setup-exe.ps1`:

- `dist\installer\1c-agent-platform-setup.exe` exists and
  is non-empty;
- `build\python\python.exe` exists;
- `build\python\python311._pth` contains the eleven
  `..\<module>` entries;
- `build\packages\` contains eleven subdirectories named
  exactly as the modules in `pyproject.toml:51-63`.

### 7.2 Install-side verification (operator-side smoke test)

After the user installs:

- *Settings → Apps → Installed apps* lists "1C Agent
  Platform";
- *Start Menu → 1C Agent Platform* lists two shortcuts
  ("1C Agent Platform" + "Uninstall 1C Agent Platform");
- `%LOCALAPPDATA%\Programs\1C Agent Platform\python\python.exe`
  exists;
- the eleven module directories exist under
  `%LOCALAPPDATA%\Programs\1C Agent Platform\`.

### 7.3 Configuration-side verification

After `first_run.ps1` finishes a fresh configuration:

- `%LOCALAPPDATA%\1C Agent Platform\config.json` exists
  and is non-empty JSON;
- Opening Claude with the pasted MCP snippet succeeds
  and Claude can call read tools (e.g. `ping`,
  `get_metadata_tree`) against the configured 1C base.

### 7.4 Honest non-verification

This recipe does **not** include a self-test command that
spawns the MCP server in the foreground. The MCP server
runs only when Claude spawns it. If you want to verify
the bundled Python can start the read server in isolation,
run from a PowerShell window:

```powershell
& "$env:LOCALAPPDATA\Programs\1C Agent Platform\python\python.exe" -m mcp_read_server --help
```

You should see the read server's help text.

---

## 8. Uninstall verb

### 8.1 How the user uninstalls

Any of:

- *Settings → Apps → Installed apps → 1C Agent Platform → Uninstall*;
- *Control Panel → Programs and Features → 1C Agent Platform → Uninstall*;
- *Start Menu → 1C Agent Platform → Uninstall 1C Agent Platform*.

All three surfaces invoke
`%LOCALAPPDATA%\Programs\1C Agent Platform\unins000.exe`.

### 8.2 What uninstall removes

- The entire install directory
  `%LOCALAPPDATA%\Programs\1C Agent Platform\` (bundled
  Python, the eleven src-layout packages, `first_run.ps1`,
  the uninstaller itself).
- The Start menu folder
  `Start Menu\Programs\1C Agent Platform\` and both
  shortcuts.
- The HKCU Uninstall registry key.

### 8.3 What uninstall PRESERVES (deliberate, contract §10.3)

- `%LOCALAPPDATA%\1C Agent Platform\config.json` —
  operator-side state (the user's configured paths).
- `%LOCALAPPDATA%\1C Agent Platform\.runtime\` —
  runtime state files.
- `%LOCALAPPDATA%\1C Agent Platform\dumps\` —
  previously created dump artefacts.
- Claude's MCP config — Claude-side state.
- The 1C platform itself (`1cv8.exe`, `1cestart.exe`).
- The end user's 1C infobase.

A user who wants a true "reset to factory" deletes
`%LOCALAPPDATA%\1C Agent Platform\config.json` manually
through File Explorer.

---

## 9. Upgrade verb

To upgrade an existing install:

1. Operator builds a new `setup.exe` from the new source
   tree (§4).
2. Operator distributes the new `setup.exe` to the end
   user (§5).
3. End user double-clicks the new `setup.exe`.
4. Inno Setup detects the existing install via the stable
   `AppId` GUID and offers to replace it.
5. New files replace old files under
   `%LOCALAPPDATA%\Programs\1C Agent Platform\`.
6. `%LOCALAPPDATA%\1C Agent Platform\config.json` survives
   the upgrade (operator-side state, contract §10.3).
7. On next launch of the Start menu shortcut,
   `first_run.ps1` detects the preserved `config.json`
   and offers the existing-configuration view (§6.3),
   not a fresh prompt.

There is **no** auto-update. There is **no** in-platform
"check for updates" surface. Releases are operator-pushed.

---

## 10. Server-based 1C infobases — the existing engineering path

The Track Q MVP supports **only file-based 1C infobases**
(контракт §4.7). If your end user runs a server-based /
client-server 1C base (Russian: *клиент-серверная база
1С*) — a base that requires presenting a username and
password to a 1C server cluster — the installer is **not**
the path for them.

That path remains the existing engineering surface,
unchanged by Track Q:

- `scripts/release/install.ps1` invoked with a
  hand-authored input-config JSON that contains the
  appropriate `base_path` connection string
  (`Srvr="<host>";Ref="<infobase_name>";`), an
  operator-authored `onec_binary_path`, and operator-
  authored argv templates for the write-tool flows that
  need them.
- The resulting `config.json` lives wherever the operator
  chooses; the MCP servers read it through the same
  loader that `first_run.ps1` writes to in the file-base
  path.

This path is documented at:

- `scripts/release/README.md`
- `docs/operators/deployment-boundary.md` (Track J)
- `docs/operators/packaging/distribution-boundary.md`
  (Track M, for `pip install <WHEEL_PATH>` shape)

A future track **may** extend the data model to add
credential fields and revisit server-based base support
in a non-engineering UX. That track is **not** Track Q.

---

## 11. Cross-references

| Track   | Recipe                                                   | Relationship to this recipe                                                                                  |
|---------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Track B | `scripts/release/README.md`                              | Install-fast-path wrapper. Used by the existing engineering path for server-based bases (§10).               |
| Track J | `docs/operators/deployment-boundary.md`                  | Deployment-host operator recipe. Orthogonal: assumes Python on deploy host.                                  |
| Track L | `docs/operators/service/service-supervision.md`          | Linux systemd template. Wrong OS for this recipe. The Windows installer does **not** register a service.    |
| Track M | `docs/operators/packaging/distribution-boundary.md`      | Wheel-based pip-install path. Orthogonal: requires preinstalled Python.                                      |
| Track N | `docs/operators/observability.md`                        | Observability recipe. Orthogonal to install path.                                                            |
| Track O | `docs/dev/editable-install-and-workspace-discovery.md`   | Dev-time editable install. Developer-only persona. Not for ordinary Windows users.                           |
| Track Q | `docs/architecture/track-q-...-contract.md` (normative)  | The contract this recipe operationalizes.                                                                    |

---

## 12. Honest non-goals (denial list)

This recipe deliberately does **not** address any of the
following. Phrasings mirror contract §11 verbatim where
possible.

- **"All Windows installer ecosystems solved"** — denied.
  Track Q closes one narrow path: Inno Setup `setup.exe`
  on Windows 10/11 amd64 for the ordinary-user persona.
- **"Enterprise installer"** — denied. No Group Policy
  templates, no SCCM packaging, no Intune publishing, no
  `.msi` ecosystem integration.
- **"Code-signed distribution"** — denied. `setup.exe` is
  unsigned; SmartScreen warnings are expected.
- **"PyPI publication"** — denied (Track M non-goal
  preserved).
- **"Auto-update / OTA / delta-update"** — denied. No
  in-platform updater; releases are operator-pushed.
- **"GUI dashboard / web admin panel"** — denied.
- **"Rich GUI config editor"** — denied. The configurator
  collects exactly two paths.
- **"Multi-base configuration"** — denied. MVP is one
  base (`default_environment="main"`); multi-base needs
  a manual `config.json` edit with awareness of the
  product-config shape.
- **"Server-based / client-server 1C infobase"** —
  denied (contract §4.7). See §10 for the existing
  engineering path.
- **"Write-server enabled by default"** — denied.
  `allow_write=false`; the closure-gate scenario ends at
  one successful read-tool execution.
- **"Windows Service / autostart"** — denied. No
  service registration. Claude spawns the MCP server on
  demand as a stdio subprocess.
- **"Tray icon / background daemon"** — denied. The
  configurator exits after run.
- **"Chocolatey / winget / Scoop / NuGet / Microsoft
  Store"** — denied.
- **"macOS / Linux installer"** — denied.
- **"ARM64 / x86 Windows"** — denied. amd64 only.
- **"Windows 7 / Windows Server"** — denied. Windows
  10 + 11 amd64 only.
- **"Silent install solves enterprise rollout"** — silent
  install is supported by Inno Setup defaults
  (`/SILENT` / `/VERYSILENT`), but enterprise rollout is
  out of Track Q scope regardless. Silent install still
  requires a subsequent first-run configurator
  invocation (configuration is **not** part of the
  wizard).
- **"Production-ready desktop app"** — denied. The
  platform is a CLI MCP server bundle; the installer is
  the smallest honest delivery primitive for the
  ordinary-Windows-user persona.
- **"Hostile-internet distribution"** — denied.
- **"Track Q completes Track B / Track I / Track M"** —
  denied. Track Q is a fourth orthogonal axis alongside
  those three. Each axis continues to serve its own
  persona.

— end of recipe —
