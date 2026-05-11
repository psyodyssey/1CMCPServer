# Service Supervision and OS Service Registration

> **Track L / Step 4 operator-facing recipe.** Companion to the
> declarative systemd template at
> [`mcp-server.service`](mcp-server.service). Both files together
> ship the Track L narrow closure: one operator-runnable systemd
> recipe for the three 1C Agent Platform MCP servers, plus prose
> notes for Windows and macOS. See
> [`docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`](../../architecture/track-l-service-supervision-and-os-service-registration-contract.md)
> for the normative Step 3 contract this implementation satisfies.

---

## §1. Purpose

### §1.1 What this document is

A practical, operator-runnable recipe for taking the three existing
MCP server entrypoints (`mcp-read-server`, `mcp-write-server`,
`mcp-intelligence-server`) from "I can run them in a terminal" to
"they run as long-lived OS-supervised services that survive
reboots, log to the OS log facility, and respond to a standard
lifecycle vocabulary (`start` / `stop` / `restart` / `status` /
`logs`)".

The recipe is structured around one **implementation-covered**
operating-system family — Linux with `systemd` — plus **prose-
only** notes for Windows and macOS. The two artefacts that ship
with Track L are:

1. This recipe (`docs/operators/service/service-supervision.md`).
2. A declarative systemd unit-file template
   ([`mcp-server.service`](mcp-server.service)).

Both files use placeholders exclusively. No real credentials, no
real paths, no real hostnames.

### §1.2 What this document is **not**

This document does **not** claim:

- "service supervision solved forever";
- "all OS families supported";
- "production-ready service supervision for hostile-network
  exposure";
- "clustered HA";
- "zero-downtime restart";
- "automatic update / OTA";
- "enterprise-grade identity integration";
- "the platform now manages process supervision internally".

Each of these phrases appears here **only as an explicit denial**.
Track L closes one narrow gap: documented operator-facing recipe
plus one declarative systemd template plus five lifecycle verbs on
one OS family with cross-OS prose for the other two. Broader
ambitions remain honest non-goals (see §13).

---

## §2. Supported closure target

### §2.1 Implementation-covered OS family — Linux / systemd

This recipe is implementation-covered for **systemd on Linux**.
The companion template `mcp-server.service` ships in repo; the
five lifecycle verbs are documented end-to-end against
`systemctl` and `journalctl` in §5–§9.

### §2.2 Cross-OS coverage — prose only

Windows and macOS coverage is **prose-only** (see §12). No
`.plist`, no NSSM install script, no PowerShell wrapper, no
`.bat` ships with Track L. Operators on those platforms are
expected to apply the prose to their service manager with
operator-side validation.

### §2.3 Why this is the current honest boundary

Track L Step 2 baseline audit and Step 3 contract grounded this
choice in repo facts:

- The three MCP server `__main__.py` modules are
  `Type=simple`-compatible foreground-blocking processes (no
  Python-side code change required).
- systemd has the broadest industrial precedent and the
  cleanest declarative unit-file model.
- Cross-OS template artefacts would require maintaining
  configurations we have not validated end-to-end; cross-OS
  prose with abstract placeholders is the narrowest honest
  coverage.
- The platform-layer in-process supervisor at
  `apps/platform/src/onec_platform/runtime.py` is **not** the
  supervisor this recipe builds; that module explicitly says
  (lines 21–31) it does not register OS services and does not
  start MCP transports inside the three servers. Track L keeps
  process supervision **outside** the platform process tree, on
  the OS layer.

---

## §3. Preconditions

Before following any walkthrough in this document, the operator
**must** have:

1. **A working Track G / H install of the project.** The three
   modules `mcp_read_server`, `mcp_write_server`, and
   `mcp_intelligence_server` import cleanly, and
   `python -m mcp_read_server --help` prints a usage message on
   the host where the service will run.
2. **PYTHONPATH bootstrap understanding.** The project source
   spreads across 11 paths under `apps/*/src/` and
   `packages/*/src/`. Either:
   - export an explicit `PYTHONPATH=<colon-joined paths>` in the
     environment of the supervised process (the systemd template
     does this via its `Environment=PYTHONPATH=<PYTHONPATH>`
     line), or
   - install the project into a virtualenv (a future packaging
     track may make this routine — Track C wheel-build is
     intentionally empty today).
3. **A materialised product config.** Run
   `scripts/release/install.ps1` once on a control host to
   materialise a `ProductConfig` JSON, or hand-author one. The
   path to this JSON becomes `<CONFIG_PATH>` in the systemd
   template's `ExecStart=` line.
4. **An MCP bearer token for HTTP transport (only if using
   `--transport http`).** Per Track H, the token MUST come from
   an environment variable named `<MCP_TOKEN_VARNAME>`. Per
   Track J §6, the listener is fronted by an operator-owned
   reverse proxy that terminates TLS; nothing in this recipe
   changes that.
5. **A dedicated unprivileged OS account** (`<USER>` /
   `<GROUP>`) that will own the supervised process. The
   recipe never instructs the operator to run as `root`. The
   account must have read access to the working directory and
   the env-file path, plus write access to whatever the
   product config declares as `bootstrap.work_dir`.

---

## §4. Service model

### §4.1 What the service actually runs

A single MCP server process. The supervised command is one of:

- `<PYTHON_BIN> -m mcp_read_server --transport <TRANSPORT> ...`
- `<PYTHON_BIN> -m mcp_write_server --transport <TRANSPORT> ...`
- `<PYTHON_BIN> -m mcp_intelligence_server --transport <TRANSPORT> ...`

The operator runs one systemd unit per MCP server they want
supervised. A typical deployment supervises all three (one
read-only, one mutating, one intelligence) as three separate
units with three different `<UNIT_NAME>` values.

### §4.2 Why `Type=simple` is correct

The MCP server entrypoints block the invoking process until the
transport loop exits — either on `EOF on stdin` (stdio), on a
graceful `KeyboardInterrupt`, or on a fatal error. systemd's
`Type=simple` expects exactly this shape: the configured
`ExecStart=` runs in the foreground and systemd considers the
service "started" as soon as the process is forked, "stopped"
when it exits.

`Type=forking` is **wrong** — the MCP runtime does not fork or
double-fork to background itself.

`Type=notify` is **wrong** — the runtime does not call
`sd_notify`; no `READY=1` socket protocol is implemented (and
the contract §12.3 explicitly excludes it).

`Type=oneshot` is **wrong** — the MCP runtime is long-lived,
not a one-shot task.

### §4.3 Why `runtime.py` is **not** part of this Track L closure

The repo already contains
`apps/platform/src/onec_platform/runtime.py`, an in-process
**product-layer** supervisor that orchestrates operator-declared
**sidecar subprocesses** (those declared in
`ProductConfig.runtime.services` with
`restart_policy ∈ {"never", "restart-if-stale"}`). It is a
different layer:

- `runtime.py` supervises subprocesses **inside** the platform
  process tree (e.g., 1C-binary-adjacent workers).
- Track L's recipe supervises the MCP server processes
  themselves **outside** the platform process tree, on the
  systemd / launchd / NSSM layer.

Extending `runtime.py` to also supervise the three MCP servers
is **explicitly rejected** by the Track L contract (§3 fact #4,
§9.1 item 6) and would contradict `runtime.py`'s own module
docstring (lines 21–31: "not a daemon manager / service manager
(no Windows Service / systemd unit registration on this step)";
"does NOT start MCP transports inside the three servers"). The
two layers stay orthogonal.

### §4.4 Signal handling — what the supervised process does on stop

Both transports already handle `KeyboardInterrupt` gracefully:

- `packages/mcp-common/src/mcp_common/_stdio_transport.py:208`
  catches `KeyboardInterrupt` and exits cleanly.
- `packages/mcp-common/src/mcp_common/_network_transport.py:618`
  catches `KeyboardInterrupt`, runs `httpd.shutdown()` and
  `httpd.server_close()` in `finally`, returns 0.

systemd's default service-stop signal is `SIGTERM`, which by
Python's default disposition exits immediately without running
those handlers. The template at
[`mcp-server.service`](mcp-server.service) sets
`KillSignal=SIGINT` to re-route service stop to the existing
`KeyboardInterrupt` branch. This avoids any Python-side code
change.

In-flight HTTP requests are abandoned on shutdown — the runtime
sets `httpd.daemon_threads = True` deliberately. This is
**explicit policy**, not a defect; do not expect zero-downtime
restart (see §6.5).

---

## §5. Start

The five lifecycle verbs in §5–§9 cover the **implementation-
covered** OS family (systemd on Linux). Cross-OS equivalents are
in §12.

### §5.1 One-time install per unit

```sh
# 1. Copy the placeholder template from the repo to the system
#    unit directory under a chosen <UNIT_NAME>, e.g. mcp-read.
sudo cp <REPO_ROOT>/docs/operators/service/mcp-server.service \
    /etc/systemd/system/<UNIT_NAME>.service

# 2. Edit the new file. Substitute every <PLACEHOLDER>. See §3
#    for required preconditions and §10 for env-var / token
#    discipline. NEVER leave placeholders in the final file.
sudo editor /etc/systemd/system/<UNIT_NAME>.service

# 3. Reload systemd so it picks up the new unit.
sudo systemctl daemon-reload

# 4. Enable the unit so it auto-starts on boot.
sudo systemctl enable <UNIT_NAME>.service
```

### §5.2 Start the service

```sh
sudo systemctl start <UNIT_NAME>.service
```

Expected operator-visible result: the command returns within a
few seconds with no output. The service moves from `inactive`
to `active (running)`. Verify with `systemctl status` (§8).

### §5.3 Start one MCP server per unit

The recipe is **single-server-per-unit**. To supervise all
three MCP servers, install three units with three different
`<UNIT_NAME>` values (e.g., `mcp-read`, `mcp-write`,
`mcp-intelligence`), each with its own `<MCP_SERVER_MODULE>`
in `ExecStart=`. Do **not** wrap multiple servers in a single
unit — that defeats the lifecycle verbs (e.g., you cannot
restart only the read-server without restarting the others).

---

## §6. Stop

### §6.1 Operator-initiated stop

```sh
sudo systemctl stop <UNIT_NAME>.service
```

Expected operator-visible result: the command returns within
`TimeoutStopSec` (default 15s in the template). The service
moves from `active (running)` to `inactive (dead)`. The
runtime's `KeyboardInterrupt` handler runs (because the
template sets `KillSignal=SIGINT`), the HTTP server (if any)
calls `httpd.shutdown()` and `httpd.server_close()`, and the
process exits 0.

### §6.2 Auto-stop on graceful exit

The supervised process may exit on its own (e.g., stdio EOF on
stdin). systemd marks the unit `inactive (dead)` and does
**not** respawn — `Restart=on-failure` in the template
respawns only on **non-zero** exit codes.

### §6.3 Clean-stop semantics

`systemctl stop` is the canonical operator command. It is
**not** the same as `pkill` / `kill -9`:

- `systemctl stop` sends `KillSignal` (SIGINT in the template).
- After `TimeoutStopSec` (15s default), systemd escalates to
  `SIGKILL` via `KillMode=mixed`. This is the unconditional
  fallback; in practice the MCP runtime exits long before it.

### §6.4 In-flight request abandonment

In-flight HTTP requests are abandoned on stop. This is
`httpd.daemon_threads = True` policy from Track H Step 4
(`_network_transport.py:606–607`). Client-side retry is the
operator's concern.

### §6.5 What stop does **not** promise

- **No zero-downtime restart.** A stop interrupts in-flight
  requests as above.
- **No drain.** systemd does not gate `systemctl stop` on
  in-flight HTTP completion.
- **No clustering / HA failover.** A single-host single-process
  model is preserved.

---

## §7. Restart

```sh
sudo systemctl restart <UNIT_NAME>.service
```

`systemctl restart` is equivalent to `systemctl stop` followed
by `systemctl start` — a clean stop-then-start, **not** a hot
reload. The runtime imports config at startup; any config-file
change requires a restart to take effect.

### §7.1 Restart on failure

If the supervised process exits with a non-zero status, systemd
respawns it automatically after `RestartSec` (5s default in the
template), subject to the rate limit `StartLimitBurst` per
`StartLimitIntervalSec`. The defaults in the template
(5 restarts per 600 seconds) are conservative and operator-
overridable.

### §7.2 Operator-initiated restart does **not** count against rate limit

`systemctl restart` is an explicit operator action, not a
failure event. systemd's rate limiter only counts non-zero
exit respawns. The operator may restart freely.

### §7.3 Restart and configuration changes

A configuration change (a new `<CONFIG_PATH>` JSON, a new
`<MCP_TOKEN_VARNAME>` env-var value, a new `--bind` host or
port) requires `systemctl restart` to take effect. The
runtime does **not** support hot reload (Track L contract
§6.5 / §12.1).

---

## §8. Status

### §8.1 Short status

```sh
systemctl status <UNIT_NAME>.service
```

Expected output (abbreviated):

- `Active: active (running) since <TIMESTAMP>; <DURATION> ago`
- `Main PID: <PID> (python)`
- Recent log lines (last ~10) from the unit's journal.

If the service is failing, look for:

- `Active: failed (Result: exit-code) since <TIMESTAMP>` —
  the supervised process exited non-zero; the unit hit
  `StartLimitBurst` before recovering. Use §9 to read logs.
- `Active: inactive (dead)` — the unit is stopped (either by
  operator or because the supervised process exited 0).

### §8.2 Boot-time enablement check

```sh
systemctl is-enabled <UNIT_NAME>.service
```

Returns `enabled` (will auto-start on boot — set up in §5.1),
`disabled` (will not auto-start), or `static` /
`indirect` / etc. for unusual cases.

### §8.3 Process-level inspection

```sh
systemctl show <UNIT_NAME>.service --property=MainPID,ExecMainStartTimestamp,Result
```

Gives machine-readable status fields (PID, last-start
timestamp, last result code). Useful for shell scripts that
need to check service state without parsing prose.

### §8.4 What status does **not** promise

- **No /healthz probe.** Per Track J §8, the runtime does
  **not** ship a `/healthz` endpoint. `systemctl status`
  reports OS-supervised process liveness, not application-
  layer readiness. Non-`/mcp` HTTP paths return 404
  deterministically (Track H).
- **No per-tool health surface.** Track L does not extend the
  in-process `runtime.py` health-dashboard layer; that is a
  separate concern.

---

## §9. Logs

### §9.1 Follow logs live

```sh
journalctl -u <UNIT_NAME>.service -f
```

`-f` follows in real time. systemd captures the supervised
process's `stdout` and `stderr` to the journal automatically —
no Python-side log-path configuration is required. The MCP
runtime already logs its diagnostic output to `stderr` (see
each `__main__.py` and the `logging.basicConfig` default).

### §9.2 Read recent logs

```sh
journalctl -u <UNIT_NAME>.service --since "1 hour ago"
```

`--since` accepts standard time expressions (`"yesterday"`,
`"2 hours ago"`, `"2026-05-11 12:00"`). Combine with
`--until` for a time window.

### §9.3 Filter by priority

```sh
journalctl -u <UNIT_NAME>.service -p err
```

`-p err` shows only `ERR`-or-worse priority lines. The MCP
runtime logs `WARNING` / `ERROR` for credential / auth /
config issues; `INFO` for startup / shutdown events; `DEBUG`
for transport-level detail when `--log-level DEBUG` is in
`ExecStart=`.

### §9.4 Log persistence and rotation

journald defaults persist logs across reboots when
`/var/log/journal/` exists. Operators who require classic
text-file logs may add `SyslogIdentifier=<UNIT_NAME>` to the
unit and forward to `rsyslog` / `syslog-ng` — that is **out
of Track L scope**; consult `systemd-journald(8)` for
distribution-specific guidance.

### §9.5 What logs do **not** include

- **No full observability stack integration.** Track L does
  not integrate OpenTelemetry / Jaeger / Prometheus / log
  aggregation forwarders. See §13.
- **No structured JSON-line format.** The runtime logs prose
  via `logging.basicConfig`. A future track may add structured
  logging; Track L does not.
- **No secret values.** Track H Step 4 redaction discipline
  carries forward — bearer tokens never appear in logs.

---

## §10. Environment / token configuration

### §10.1 The `EnvironmentFile=` discipline

The systemd template sources operator-managed environment
variables via:

```ini
EnvironmentFile=<ENV_FILE_PATH>
```

`<ENV_FILE_PATH>` is a file readable **only by `<USER>`**
(mode `0600` recommended). It **never** lives in the repo. It
**never** contains a literal cleartext bearer token in a
committed file. Example shape (placeholders only):

```text
# <ENV_FILE_PATH> — read by systemd at unit start; never commit.
<MCP_TOKEN_VARNAME>=<SECRET_TOKEN_VALUE>
PYTHONUNBUFFERED=1
```

`<SECRET_TOKEN_VALUE>` is supplied by the operator's secret
manager (vault, KMS, OS keychain, etc.). Track L does **not**
ship a secret manager; the env-file is the boundary at which
the operator's secret manager hands off to the supervised
process.

### §10.2 Relationship to Track H / Track D

Track H Step 4 wired `--auth-token-env <VARNAME>` into the
MCP server CLI. The systemd template's `ExecStart=` line
passes `--auth-token-env <MCP_TOKEN_VARNAME>` to the
supervised process. The token resolution happens in
`_network_transport._resolve_env_token` at server startup —
unchanged by Track L.

Track D Step 4 added the `${ENV:NAME}` substitution path
inside `ProductConfig.auth.tokens`. If the operator declares
tokens in product config rather than via `--auth-token-env`,
the systemd template's `EnvironmentFile=` still applies —
the runtime resolves `${ENV:NAME}` against the supervised
process's environment, which `EnvironmentFile=` populates.

### §10.3 Placeholder discipline

Both this recipe and the template use placeholders only.
The full set:

| Placeholder | Operator-supplied meaning |
| --- | --- |
| `<USER>` | Unprivileged OS user that owns the process. |
| `<GROUP>` | Primary group for `<USER>`. |
| `<UNIT_NAME>` | systemd unit name (e.g., `mcp-read`). |
| `<SERVICE_NAME>` | NSSM service name / launchd Label (cross-OS). |
| `<REPO_ROOT>` | Absolute filesystem path to the project root. |
| `<WORKING_DIR>` | Working directory of the supervised process. |
| `<PYTHON_BIN>` | Absolute path to a Python 3.11+ interpreter. |
| `<PYTHONPATH>` | Colon-joined 11-src-path PYTHONPATH (or venv site-packages). |
| `<MCP_SERVER_MODULE>` | `mcp_read_server` / `mcp_write_server` / `mcp_intelligence_server`. |
| `<TRANSPORT>` | `stdio` or `http`. |
| `<CONFIG_PATH>` | Path to materialised product config JSON. |
| `<HOST>` | Bind host for HTTP transport. |
| `<PORT>` | Bind port for HTTP transport. |
| `<MCP_TOKEN_VARNAME>` | Env-var name holding the bearer token. |
| `<ENV_FILE_PATH>` | Path to env-file (mode 0600). |
| `<LOG_PATH>` | (cross-OS only) operator-chosen log file path. |
| `<VARNAME>` | (cross-OS only) generic env-var placeholder. |

No real values appear anywhere in this recipe or the template.
The credential-leak guard in `scripts/release/verify-release.ps1`
catches accidental literal secrets.

### §10.4 stdio transport notes

For `<TRANSPORT>=stdio` the unit's `ExecStart=` MUST drop the
`--bind <HOST>:<PORT>` and `--auth-token-env
<MCP_TOKEN_VARNAME>` arguments. stdio is a trusted local
subprocess channel (Track G); there is no network listener
and no auth. Running stdio MCP servers under systemd is
unusual — the typical use of stdio is in-process spawning by
an MCP client. Track L supports it for completeness but the
most common production shape is HTTP behind a reverse proxy.

---

## §11. Reverse proxy / TLS boundary reminder

This recipe does **not** redesign the deployment boundary.
Carry-forward truths from Tracks H and J apply unchanged:

- **In-process TLS forbidden.** The MCP server listens on
  plain HTTP/1.1. Track H §13.1 invariant; Track J §5
  carry-forward.
- **mTLS forbidden.** Track H §13.3 carry-forward.
- **Reverse proxy terminates TLS.** Operator-owned reverse
  proxy (nginx / Caddy / etc.) fronts the listener for any
  network exposure beyond `127.0.0.1`. See Track J's
  [`deployment-boundary.md`](../deployment-boundary.md)
  recipe for the full per-scenario matrix and abstract
  reverse-proxy snippets.
- **`X-Forwarded-*` headers MUST NOT be consumed.** Track J
  §6 invariant; the listener ignores them for any access-
  control, trust, identity, audit, or routing decision.
- **`/healthz` not shipped.** Track J §8 defer. Non-`/mcp`
  paths return 404 deterministically. For load-balancer
  probes that require 2xx, the operator's reverse proxy
  synthesises a 2xx; see deployment-boundary recipe §6.

This recipe answers **process supervision**; Track J's
recipe answers **network exposure**. Both are required for a
full deployment story; neither subsumes the other.

---

## §12. Cross-OS notes (prose only)

These sections describe how to apply the recipe's principles
on Windows and macOS. They are **prose only** — no `.plist`,
no NSSM install script, no PowerShell wrapper ships with
Track L. Operators on these platforms validate the
configuration end-to-end on their own.

### §12.1 Windows notes

**Service manager.** The recommended tool is NSSM (the
Non-Sucking Service Manager), a small open-source executable
that wraps an arbitrary command line into a Windows Service.
NSSM avoids a Python `pywin32` dependency and avoids
re-implementing `win32serviceutil`.

**Why NSSM rather than native pywin32.** The `pywin32` route
requires importing `win32serviceutil` and subclassing
`win32serviceutil.ServiceFramework` — that is a Python-side
code change Track L explicitly excludes (contract §10.1 /
§12.1). NSSM keeps the supervised command identical to the
systemd shape (`python -m mcp_<role>_server ...`) and routes
service control through the operating system's Service
Control Manager.

**Install (prose, one MCP server per service):**

1. Download NSSM and place `nssm.exe` somewhere on `PATH`
   (e.g., `C:\Tools\nssm\nssm.exe`).
2. Run `nssm install <SERVICE_NAME>` in an elevated
   PowerShell or `cmd` session. The NSSM GUI opens.
3. **Application tab:** set `Path` to `<PYTHON_BIN>`,
   `Startup directory` to `<WORKING_DIR>`, and `Arguments` to
   `-m <MCP_SERVER_MODULE> --transport <TRANSPORT> --config-path <CONFIG_PATH> --bind <HOST>:<PORT> --auth-token-env <MCP_TOKEN_VARNAME>`.
4. **Details tab:** set `Display name` and `Description` to
   match `<SERVICE_NAME>`.
5. **Log on tab:** set the service account to an unprivileged
   `<USER>`, or `Local Service` for a system-managed identity.
   Do **not** run as `LocalSystem`.
6. **Process tab:** check `Console window` only for
   troubleshooting; uncheck for production.
7. **I/O tab:** set `Output (stdout)` to `<LOG_PATH>\stdout.log`
   and `Error (stderr)` to `<LOG_PATH>\stderr.log`. NSSM
   handles rotation if you configure it on the **File rotation**
   tab.
8. **Environment tab:** add `<MCP_TOKEN_VARNAME>=<TOKEN_VALUE>`
   and `PYTHONPATH=<PYTHONPATH>`. Do **not** check this file
   into version control; the NSSM service config is stored in
   the Windows registry by NSSM, not in the operator's repo.
9. Click `Install service`. Confirm `Service installed
   successfully` dialog.

**Lifecycle verbs (Windows):**

- **start** — `nssm start <SERVICE_NAME>`, equivalent to
  `sc start <SERVICE_NAME>`.
- **stop** — `nssm stop <SERVICE_NAME>`, equivalent to
  `sc stop <SERVICE_NAME>`. NSSM by default sends a
  `Ctrl-C`-equivalent event via the
  `AppStopMethodConsole` parameter, which lands in the
  `KeyboardInterrupt` branch of the MCP runtime.
- **restart** — `nssm restart <SERVICE_NAME>`.
- **status** — `sc query <SERVICE_NAME>` or
  `Get-Service <SERVICE_NAME>` in PowerShell.
- **logs** — read `<LOG_PATH>\stdout.log` and
  `<LOG_PATH>\stderr.log`; or use Windows Event Viewer if
  NSSM event-log forwarding is configured.

**Cross-OS gaps honestly named:**

- Track L does **not** ship an NSSM install script. The
  operator runs `nssm install` interactively (or scripts it
  themselves) — that script is not part of Track L scope.
- Track L does **not** validate the NSSM configuration end-
  to-end; the prose describes a known-good pattern but the
  operator owns operator-side validation.
- `Get-Service` does **not** show the unit's recent log lines
  the way `systemctl status` does. The operator combines
  `Get-Service` with reading the log files for the full
  status picture.

### §12.2 macOS notes

**Service manager.** The native option is `launchd` with a
`.plist` configuration file in either:

- `~/Library/LaunchAgents/<LABEL>.plist` — user-level
  service (runs only when the user is logged in).
- `/Library/LaunchDaemons/<LABEL>.plist` — system-level
  service (runs at boot regardless of login). Requires
  `root` to install.

Choose the system-level path (`LaunchDaemons`) for the
deployment shape Track L addresses (long-lived service
across reboots).

**Plist shape (prose, do not commit a `.plist` to the repo):**

```xml
<!-- /Library/LaunchDaemons/<LABEL>.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string><LABEL></string>
    <key>ProgramArguments</key>
    <array>
        <string><PYTHON_BIN></string>
        <string>-m</string>
        <string><MCP_SERVER_MODULE></string>
        <string>--transport</string>
        <string><TRANSPORT></string>
        <string>--config-path</string>
        <string><CONFIG_PATH></string>
        <string>--bind</string>
        <string><HOST>:<PORT></string>
        <string>--auth-token-env</string>
        <string><MCP_TOKEN_VARNAME></string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string><PYTHONPATH></string>
        <key><MCP_TOKEN_VARNAME></key>
        <string><TOKEN_VALUE></string>
    </dict>
    <key>WorkingDirectory</key>
    <string><WORKING_DIR></string>
    <key>UserName</key>
    <string><USER></string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string><LOG_PATH>/stdout.log</string>
    <key>StandardErrorPath</key>
    <string><LOG_PATH>/stderr.log</string>
</dict>
</plist>
```

`KeepAlive` with `SuccessfulExit=false` matches systemd's
`Restart=on-failure`: respawn only on non-zero exit, not
on operator-initiated stop.

**Lifecycle verbs (macOS):**

- **start** —
  `sudo launchctl bootstrap system /Library/LaunchDaemons/<LABEL>.plist`.
  Once bootstrapped the plist auto-starts at boot
  (`RunAtLoad=true`).
- **stop** — `sudo launchctl bootout system /Library/LaunchDaemons/<LABEL>.plist`.
- **restart** — `sudo launchctl kickstart -k system/<LABEL>`.
- **status** — `sudo launchctl print system/<LABEL>`.
- **logs** — read `<LOG_PATH>/stdout.log` and
  `<LOG_PATH>/stderr.log`; or `log show --predicate
  'subsystem == "<LABEL>"' --info` if the operator
  configures `os_log` forwarding (which Track L does **not**
  do).

**Cross-OS gaps honestly named:**

- Track L does **not** ship a `.plist` file. The XML shape
  above is operator-adapted, not committed.
- Track L does **not** validate the launchd configuration
  end-to-end.
- `launchctl print` output is verbose and not as
  operator-friendly as `systemctl status`; the operator
  combines `launchctl print` with the log files.
- macOS Gatekeeper / SIP / notarisation concerns are
  **out of Track L scope**.

### §12.3 Reference documentation

External references (linked here as prose for operator
guidance, not endorsed beyond their published documentation):

- systemd: `man systemd.unit`, `man systemd.service`,
  `man systemd.exec`, `man systemctl`, `man journalctl` —
  available on every systemd-using Linux host.
- NSSM: <https://nssm.cc/> — official NSSM project page;
  refer to current NSSM documentation for parameter names.
- launchd: Apple's `man launchd`, `man launchd.plist`,
  `man launchctl` — available on every macOS host.

Track L does **not** mirror or embed external documentation;
the references above are pointers for cross-OS operator
adaptation.

---

## §13. Honest non-goals

By Step 6 closure Track L will **not** have delivered any of
the following. Each appears here as an explicit denial:

### §13.1 Supervisor / framework non-goals

- No in-repo Python supervisor framework, daemon class, or
  `pywin32` service wrapper.
- No `runtime.py` extension into a service manager —
  `apps/platform/src/onec_platform/runtime.py` remains
  byte-identical and continues to supervise only operator-
  declared product-layer subprocesses, **not** the MCP
  servers themselves.
- No auto-restart-on-config-change watcher.
- No hot reload — config changes require `systemctl
  restart`.
- No zero-downtime restart — in-flight requests are
  abandoned on stop (Track H `daemon_threads=True`
  policy).

### §13.2 OS-family non-goals

- No Windows `.bat` / `.cmd` / `.ps1` install wrappers in
  the repo.
- No macOS `.plist` artefacts in the repo.
- No SystemV init / upstart / FreeBSD `rc.d` / NixOS
  module declarations.
- No multi-distro Linux compatibility matrix.

### §13.3 Integration non-goals

- No journald structured-log integration beyond stderr
  capture.
- No Windows Event Viewer log-channel registration.
- No syslog / `rsyslog` / `syslog-ng` forwarding shipped.
- No OpenTelemetry / Jaeger / Prometheus / OpenMetrics /
  log-aggregation integration.
- No `/healthz` / `/readyz` / `/livez` endpoint — Track J
  §8 defer carried forward.
- No `sd_notify` / `Type=notify` readiness protocol.

### §13.4 Identity / auth non-goals

- No SSO / SAML / OIDC / SCIM / RBAC / ABAC / multi-tenant.
- No mTLS / in-process TLS — Track H §13 carry-forward.
- No JWT / OAuth / refresh-token / session-cookie / per-
  tenant identity.
- No automatic token rotation.

### §13.5 Deployment / orchestration non-goals

- No Kubernetes manifests, Docker Compose files, Nomad job
  files, Consul / etcd / Zookeeper integration.
- No clustering / HA / load-balancing / multi-instance
  coordination.

### §13.6 Packaging / distribution non-goals

- No `.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` / signed-
  binary distribution.
- No GUI installer / wizard.
- No PyPI publication; no wheel publication beyond existing
  `[project.scripts]` declarations (which remain un-
  installable by Track C / Step 3 honest constraint).

### §13.7 Other carry-over non-goals

- No web UI / dashboard frontend.
- No standalone `apps/platform` daemon entrypoint.
- No automatic update / OTA / self-upgrade.
- No rollback expansion / AST work / 1C matrix expansion.
- No `1cv8.exe` runs anywhere in Track L.
- No new MCP tools — registries `read=15 / write=25 /
  intelligence=16` invariant carried through.
- No registry change.
- No remote push.

### §13.8 Forbidden maturity-claim phrases

The following phrases MUST NOT appear in any Track L
artefact except as quoted explicit denials:

- "service supervision solved forever"
- "production-ready service supervision"
- "all OS families supported"
- "supported on all platforms"
- "supported in production"
- "hostile-network-ready"
- "enterprise-ready service supervision"
- "fully supervised"
- "production-grade service"
- "clustered HA"
- "zero-downtime restart"

---

## §14. Cross-references

### §14.1 Track L architecture docs (frozen anchors)

- [`docs/architecture/track-l-service-supervision-and-os-service-registration-plan.md`](../../architecture/track-l-service-supervision-and-os-service-registration-plan.md)
  — Step 1 planning document (14 sections, Q1–Q7 directional
  defaults, in-scope / out-of-scope, guardrails, acceptance
  criteria, relationship-to-G/H/I/J/K table).
- [`docs/architecture/track-l-service-supervision-and-os-service-registration-step-map.md`](../../architecture/track-l-service-supervision-and-os-service-registration-step-map.md)
  — Step 1 step-map (16 track invariants, 18 categorical
  out-of-scope denials, six-step boundary).
- [`docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`](../../architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md)
  — Step 2 descriptive baseline audit (10 enumerated
  absences, Q1–Q6 directional resolutions, 14 Step 3
  handoff items).
- [`docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`](../../architecture/track-l-service-supervision-and-os-service-registration-contract.md)
  — Step 3 normative contract (RFC 2119 language, PATH B
  locked at §7.1, exhaustive forbidden file surface,
  verification protocol).

### §14.2 Track J deployment-boundary recipe

- [`docs/operators/deployment-boundary.md`](../deployment-boundary.md)
  — Network-side companion recipe. Reverse-proxy posture,
  TLS termination, bind-host policy, Forwarded-header
  MUST-NOT-consume rule. Read together with this document
  for a full operator deployment story.

### §14.3 Production code anchors (do not modify in Track L)

- `apps/mcp-read-server/src/mcp_read_server/__main__.py`
  — read-server `Type=simple`-compatible entrypoint
  (~40 LOC).
- `apps/mcp-write-server/src/mcp_write_server/__main__.py`
  — symmetric for write-server.
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
  — symmetric for intelligence-server.
- `packages/mcp-common/src/mcp_common/_stdio_transport.py:208`
  — `KeyboardInterrupt` graceful-shutdown path (stdio).
- `packages/mcp-common/src/mcp_common/_network_transport.py:618–624`
  — `KeyboardInterrupt` graceful-shutdown path (HTTP),
  with `daemon_threads=True` at `:606–607`.
- `apps/platform/src/onec_platform/runtime.py` — in-
  process supervisor for **product-layer** subprocesses,
  **not** for MCP servers. Module docstring lines 21–31
  explicit denial. Preserved byte-identical by Track L.

### §14.4 Release / install adjacencies

- [`scripts/release/install.ps1`](../../../scripts/release/install.ps1)
  — install fast-path materialises product config JSON;
  prints follow-up commands. Materialised JSON path =
  `<CONFIG_PATH>` in the systemd template's `ExecStart=`
  line. Track L does **not** modify this script.
- [`scripts/dev/launch.ps1`](../../../scripts/dev/launch.ps1)
  — operator umbrella wrapper. Explicitly does not start
  MCP servers; foreground-only dev convenience. Unrelated
  to Track L's supervised path.
- [`scripts/dev/mcp_client_smoke.py`](../../../scripts/dev/mcp_client_smoke.py)
  — Track K Step 4 client-side replay harness. Spawns its
  own server subprocess for one-shot proof; not a
  supervisor.

---

## §15. Honest summary

Track L / Step 4 ships exactly two files: this recipe and
the companion systemd unit-file template at
[`mcp-server.service`](mcp-server.service). Together they
take an operator from "I can run an MCP server in a
terminal" to "the MCP server is supervised by systemd,
survives reboots, responds to start / stop / restart / status
/ logs, and logs to journald" — on Linux. Windows and macOS
operators apply the §12 prose to NSSM and launchd with
operator-side validation.

The recipe does **not** redesign transports, auth,
deployment boundary, or the in-process product-layer
supervisor. It does **not** add a new CLI flag, a new MCP
tool, a new endpoint, or a new dependency. It does **not**
claim production-grade supervision, zero-downtime restart,
clustered HA, or all-OS-families support. Each of those
appears here only as an explicit denial.

The two-file slice is the narrowest honest closure of the
Step 1 plan's gap statement, locked by the Step 3 contract,
verified by Step 4's commit. Track L remains active through
Step 5 (narrow CLASS-1 docs alignment) and Step 6 (final
integration pass and Q7 SemVer decision; default
NO-BUMP).
