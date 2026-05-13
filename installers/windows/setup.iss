; ============================================================================
; setup.iss - 1C Agent Platform Windows installer definition
; Track Q / Step 4. PATH B per contract sec.12.1.
; Companion recipe: docs/operators/installer/windows-setup-exe.md
;
; This file is consumed by the Inno Setup 6 compiler (iscc.exe) after the
; build helper (installers/windows/build-setup-exe.ps1) has assembled the
; build directory layout described below.
;
; Expected build inputs at compile time:
;   build/python/                - embeddable CPython 3.11 fetched at build
;                                  time (NOT committed to git); python311._pth
;                                  rewritten by the build helper per contract
;                                  sec.6.3 to expose the eleven src-layout
;                                  packages.
;   build/packages/<eleven dirs> - the eleven src-layout package directories
;                                  copied verbatim from apps/*/src/* and
;                                  packages/*/src/* per pyproject.toml:51-63.
;   build/first_run.ps1          - copied verbatim from
;                                  installers/windows/first_run.ps1.
;
; Output: a single 1c-agent-platform-setup.exe under -OutputDir (defaults to
; <repo>/dist/installer/ via the build helper).
;
; Scope discipline anchors:
;   sec.4.5  per-user install at %LOCALAPPDATA%\Programs\1C Agent Platform\,
;            no admin elevation, HKCU Uninstall registration auto by Inno.
;   sec.6.1  exact installed files layout.
;   sec.6.4  one Start menu shortcut + one Uninstall shortcut.
;   sec.7.1  standard wizard pages only; no custom Pascal-script pages.
;   sec.7.3  default Inno Setup wizard appearance.
;   sec.9.1  single user-facing launch surface.
;   sec.10.3 uninstall preserves %LOCALAPPDATA%\1C Agent Platform\ state.
; ============================================================================

#define MyAppName "1C Agent Platform"
#define MyAppVersion "0.5.3"
#define MyAppPublisher "1C Agent Platform Team"
#define MyAppDirName "1C Agent Platform"
#define BuildRoot ".\..\..\build"

[Setup]
; A stable AppId GUID is required for clean upgrade-in-place semantics
; (Inno Setup uses it to identify previously installed versions).
AppId={{B7D4F2E9-5A6C-4B8F-9E1A-3D2C8F5A7B14}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
UninstallDisplayName={#MyAppName}

; Per-user install per contract sec.4.5.1: DefaultDirName={userpf}\..., never
; {pf}\... . PrivilegesRequired=lowest, never =admin.
DefaultDirName={userpf}\{#MyAppDirName}
DefaultGroupName={#MyAppDirName}
DisableProgramGroupPage=yes
DisableWelcomePage=no
DisableReadyPage=no
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=

; Per contract sec.4.5.2: no PATH modification, ever. (Inno Setup does NOT
; modify PATH unless we ask via [Registry]/[Tasks]/[Code]; we ask for none.)

OutputBaseFilename=1c-agent-platform-setup
OutputDir={#BuildRoot}\..\dist\installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

; Logging is informational and operator-side only; it does NOT write to any
; tracked path.
SetupLogging=yes

[Languages]
; Single language per contract sec.7.2 (no language-selection page).
Name: "en"; MessagesFile: "compiler:Default.isl"

[Files]
; -- Bundled embeddable CPython 3.11 (per contract sec.4.4 / sec.6.1 / sec.6.3)
Source: "{#BuildRoot}\python\*"; DestDir: "{app}\python"; \
    Flags: recursesubdirs createallsubdirs ignoreversion

; -- The eleven src-layout packages (per contract sec.4.2 / sec.6.1; mirrors
;    pyproject.toml [tool.hatch.build.targets.wheel] packages array).
Source: "{#BuildRoot}\packages\mcp_read_server\*"; DestDir: "{app}\mcp_read_server"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\mcp_write_server\*"; DestDir: "{app}\mcp_write_server"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\mcp_intelligence_server\*"; DestDir: "{app}\mcp_intelligence_server"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_platform\*"; DestDir: "{app}\onec_platform"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\mcp_common\*"; DestDir: "{app}\mcp_common"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_process_runner\*"; DestDir: "{app}\onec_process_runner"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_policy_engine\*"; DestDir: "{app}\onec_policy_engine"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_audit\*"; DestDir: "{app}\onec_audit"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_health\*"; DestDir: "{app}\onec_health"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_troubleshooting\*"; DestDir: "{app}\onec_troubleshooting"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#BuildRoot}\packages\onec_config\*"; DestDir: "{app}\onec_config"; \
    Flags: recursesubdirs createallsubdirs ignoreversion

; -- First-run configurator (per contract sec.8 / sec.9.2)
Source: "{#BuildRoot}\first_run.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; -- One Start menu shortcut pointing at first_run.ps1 (per sec.6.4 / sec.9.1
;    / sec.9.2). The shortcut target is powershell.exe with the exact argv
;    locked by sec.9.2: -ExecutionPolicy Bypass -NoProfile -WindowStyle
;    Normal -File <abs path to first_run.ps1>.
Name: "{group}\{#MyAppName}"; \
    Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -NoProfile -WindowStyle Normal -File ""{app}\first_run.ps1"""; \
    WorkingDir: "{app}"; \
    Comment: "Configure and connect Claude to one file-based 1C infobase"

; -- Standard Inno Setup uninstaller shortcut (per sec.6.4).
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; \
    Comment: "Uninstall {#MyAppName}"

; -- No desktop shortcut by default per sec.6.4.
; -- No Quick Launch / taskbar pin / context menu extension (all forbidden by
;    sec.6.4).

[Run]
; -- Optional "Launch on Finish" tick on the wizard Finish page. The user MAY
;    untick this; either way the Start menu shortcut is the canonical surface.
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -NoProfile -WindowStyle Normal -File ""{app}\first_run.ps1"""; \
    Description: "Launch {#MyAppName}"; \
    WorkingDir: "{app}"; \
    Flags: postinstall nowait skipifsilent unchecked

; -- No silent post-install steps (no MCP-server spawn, no service install, no
;    autostart registration, no tray icon registration). Everything below is
;    deliberately empty.

[UninstallDelete]
; -- Explicit removal of {app}\ on uninstall. The default Inno Setup tracking
;    of `Source: dir\*` + `recursesubdirs` does not reliably remove every file
;    under {app}\<module>\ — see Step 4 acceptance / Step 4 correction pass.
;    The Inno Setup self-delete mechanism handles unins000.exe correctly.
;    %LOCALAPPDATA%\1C Agent Platform\ (config.json, .runtime\, dumps\) is on
;    a separate path; this directive does not touch it. User state survives
;    uninstall per contract sec.10.3.
Type: filesandordirs; Name: "{app}"

[UninstallRun]
; -- Deliberately empty. No external uninstall hooks; Inno Setup uses the
;    auto-generated unins000.exe entirely.

[Registry]
; -- Deliberately empty. The HKCU Uninstall registry entry is written
;    automatically by Inno Setup under PrivilegesRequired=lowest (per contract
;    sec.4.5.3). No HKLM writes (forbidden by sec.4.5.3). No PATH writes.
;    No HKCU\Run / HKLM\Run autostart writes (forbidden by sec.8.7).
