# Parallel Track L — Service Supervision and OS Service Registration — Baseline Audit

**Status.** Descriptive baseline audit produced by Track L /
Step 2 at HEAD `e713f8e` (Track L / Step 1 closure). This
document is **not** a contract. It does **not** use RFC 2119
MUST / MUST NOT / SHOULD / MAY language. All "decisions"
appear here as directional resolutions grounded in repo
evidence, intended for Step 3 contract consumption. Step 3
locks; Step 2 observes.

**Companion documents.**

- [`track-l-service-supervision-and-os-service-registration-plan.md`](track-l-service-supervision-and-os-service-registration-plan.md)
  — Step 1 planning document with 14 sections including
  Q1–Q7 directional defaults.
- [`track-l-service-supervision-and-os-service-registration-step-map.md`](track-l-service-supervision-and-os-service-registration-step-map.md)
  — Step 1 step-map document with 16 track invariants and
  18 categorical out-of-scope denials.

---

## §1. Purpose / scope

### §1.1 What this audit is

A single descriptive read-only inventory of every repo
surface that is either (a) part of the current launch /
run / lifecycle story for the three MCP servers
(`mcp-read-server`, `mcp-write-server`,
`mcp-intelligence-server`), or (b) part of an
**adjacent** supervision-like layer that already exists in
the repo. The audit grounds Step 3's contract decisions in
repo facts at HEAD `e713f8e`, not in wishful thinking.

### §1.2 What this audit is not

Not a Step 3 contract. Not a Step 4 implementation. Not
a closure narrative. Not a rewrite of Track L Step 1
planning docs. Not a normative MUST-language document.
Not an attempt to commit pre-emptively to PATH A / PATH B /
PATH C — those are Step 3 contract territory.

### §1.3 Track L scope reminder (from Step 1 plan §6 / §7)

In scope: planning / audit / contract / narrow
implementation / docs-alignment / closure for service
supervision + OS service registration of the three
existing MCP server surfaces; lifecycle vocabulary
(start / stop / restart / status / logs); preserving
Track G / H / I / J / K invariants byte-identical.

Out of scope: new MCP tools; registry changes; transport
redesign; auth redesign; deployment-boundary redesign;
packaging ecosystem; enterprise identity stack; clustering /
HA / load-balancing / orchestration platforms; web UI;
full observability stack; `/healthz` endpoint; standalone
`apps/platform` daemon entrypoint; hot reload / zero-
downtime restart; automatic update / OTA; rollback / AST /
multi-version 1С matrix expansion; `1cv8` work; remote
push. The phrases "service supervision solved" /
"production-ready service supervision" / "all OS families
supported" / "clustered HA" / "zero-downtime restart" may
appear in Track L docs only as explicit denials.

---

## §2. Method / evidence sources

The audit observes the repo at HEAD `e713f8e` via these
mechanisms only — no `1cv8.exe`, no real-network probe,
no remote push, no production code change:

- **Whole-repo grep** (ripgrep via the Grep tool, case-
  insensitive) for the supervision-vocabulary terms:
  `systemd`, `launchd`, `Restart=`, `sc.exe`, `nssm`,
  `New-Service`, `pywin32`, `supervisor`, `supervisord`,
  `daemon`, `daemonize`, `PIDFile`, `pidfile`,
  `--background`, `--fork`, `--daemonize`, `journald`,
  `Event Viewer`, `service-unit`, `service_unit`.
  Coverage: every `.py`, `.md`, `.ps1`, `.toml`, `.json`,
  `.sh` tracked file.
- **Targeted Python signal-handling grep** for `SIGTERM`,
  `SIGINT`, `SIGHUP`, `signal.signal`, `KeyboardInterrupt`,
  `atexit`, `shutdown`, `graceful` across `**/*.py`.
- **Targeted reads** of the three MCP server `__main__.py`
  modules, `packages/mcp-common/src/mcp_common/
  _stdio_transport.py`, `packages/mcp-common/src/
  mcp_common/_network_transport.py`,
  `apps/platform/src/onec_platform/process_control.py`,
  `apps/platform/src/onec_platform/runtime.py`,
  `apps/platform/src/onec_platform/models.py`,
  `scripts/dev/launch.ps1`, `scripts/release/install.ps1`,
  `docs/operator-manual.md` head section.
- **Directory listings** of `scripts/dev/` (6 files) and
  `scripts/release/` (4 files) for surface inventory.
- **`verify-release.ps1`** GREEN on 8 checks at HEAD =
  baseline-state guarantee that registries are `15 / 25 /
  16` and `selfcheck status=ok`.

No file was modified during the evidence-gathering pass.
All commands were read-only.

---

## §3. Current service-supervision baseline

### §3.1 The three MCP server entrypoints

All three follow the same trivially-thin shape, observed
verbatim in `apps/mcp-read-server/src/mcp_read_server/
__main__.py`, `apps/mcp-write-server/src/
mcp_write_server/__main__.py`, and
`apps/mcp-intelligence-server/src/mcp_intelligence_server/
__main__.py`:

```python
from mcp_common._network_transport import run_main_http
from .server import get_tool, list_tools

SERVER_NAME = "mcp-<role>-server"
SERVER_VERSION = "0.4.0"


def main() -> int:
    return run_main_http(
        prog="python -m mcp_<role>_server",
        description="...",
        server_name=SERVER_NAME,
        server_version=SERVER_VERSION,
        list_tools_fn=list_tools,
        get_tool_fn=get_tool,
    )


if __name__ == "__main__":
    raise SystemExit(main())
```

Each `main()` blocks until the transport loop returns,
which happens only on:

- **stdio path** — `EOF on stdin` (graceful) or
  `KeyboardInterrupt` (Ctrl-C / SIGINT).
  Reference: `packages/mcp-common/src/mcp_common/
  _stdio_transport.py:208–212`.
- **HTTP path** — `KeyboardInterrupt` (Ctrl-C / SIGINT)
  inside the `serve_forever()` call.
  Reference: `packages/mcp-common/src/mcp_common/
  _network_transport.py:616–624`.

There is no `signal.signal(SIGTERM, ...)` handler installed
anywhere in `_stdio_transport.py` or `_network_transport.py`.
On POSIX, Python's default SIGTERM disposition is to exit
immediately, which terminates `serve_forever()` without
running the `try/except/finally` graceful-shutdown path.
On Windows, there is no SIGTERM equivalent; the canonical
stop signal is `SERVICE_CONTROL_STOP` (pywin32-mediated)
or `Ctrl-C` emulation (via `GenerateConsoleCtrlEvent`,
which `nssm` does by default). Both Windows paths
re-enter the `KeyboardInterrupt` branch.

The HTTP path uses `httpd.daemon_threads = True`
(`_network_transport.py:606–607`), which means in-flight
requests are abandoned on shutdown regardless of which
path is taken. The audit observes no inherent advantage to
adding a SIGTERM handler on POSIX given this design —
in-flight requests are abandoned either way.

### §3.2 `python -m mcp_<server>` and `[project.scripts]`

`pyproject.toml` declares three console scripts:

```toml
[project.scripts]
mcp-read-server = "mcp_read_server.__main__:main"
mcp-write-server = "mcp_write_server.__main__:main"
mcp-intelligence-server = "mcp_intelligence_server.__main__:main"
```

Reference: `pyproject.toml:22–25`. Because
`[tool.hatch.build.targets.wheel] packages = []` is
intentionally empty (Track C / Step 3 honest constraint),
these console scripts are not currently installable via
`pip install` — they exist as targets that a future
packaging track could activate. Today, operators run the
servers via `python -m mcp_<role>_server`, which requires
the project's 11-src-path PYTHONPATH to be bootstrapped
first (`scripts/dev/bootstrap_paths.ps1` or the harness's
equivalent path-prepend logic).

The audit observes this as a Step 4 implementation
consideration: a systemd unit's `ExecStart=` line would
need either (a) a wrapper that bootstraps PYTHONPATH
before calling `python -m`, or (b) absolute PYTHONPATH
export inside the unit file's `Environment=` line. Both
are normal patterns; neither requires production code
change.

### §3.3 Operator launch helpers

**`scripts/dev/launch.ps1`** — operator umbrella wrapper.
Read verbatim: it explicitly **does NOT start the MCP
servers** ("Launching the servers from this wrapper is a
deliberate scope choice that this umbrella does NOT
take", `launch.ps1:26–28`). Its commands are `selfcheck`,
`repl`, `run`, `help`. Foreground-only by definition; it
delegates to `python` interactively. Useful for dev
work; uninvolved in the service-supervision question.

**`scripts/release/install.ps1`** — install fast-path
wrapper (Track B / Step 3, extended by Track I / Step 4
for `auth.tokens` round-trip integrity). Materialises a
`ProductConfig` JSON from the operator's source config and
emits follow-up `python -m mcp_<server> --transport ...`
invocation strings. Reference: `scripts/release/
install.ps1` (2501 bytes). It **does not** register the
materialised config as a service, **does not** create a
systemd unit, **does not** invoke `sc.exe`, **does not**
ship with a service-control wrapper around the resulting
command lines.

**`scripts/dev/mcp_client_smoke.py`** (Track K / Step 4
artefact) — stdlib-only client-side harness that spawns
its own MCP server subprocesses, exercises
`initialize` / `tools/list` / one read-only `tools/call`
plus an HTTP 401 probe, then tears them down via
`close-stdin → terminate → wait(5s) → kill` escalation.
Useful as a smoke proof of the transport surfaces; not a
supervisor; never persistent across reboots.

**`scripts/dev/selfcheck.py`** — stdlib import-and-count
probe. Confirms registries `15 / 25 / 16` and importability
of the three MCP packages. Not a supervisor.

**`scripts/dev/run_dev_check.ps1` /
`scripts/dev/bootstrap_paths.ps1`** — PYTHONPATH
bootstrap and selfcheck launcher. Not supervisors.

**`scripts/release/verify-release.ps1`** — 8-check
release-side gate. Not a supervisor.

### §3.4 Adjacent product-layer in-process supervisor (Phase 5 / Step 3 + Phase 6 / Step 6)

This is the most important "looks similar but is not the
same thing" finding of the audit. Read carefully.

**What exists.** `apps/platform/src/onec_platform/
runtime.py` (Phase 5 / Step 3, extended Phase 6 / Step 6)
implements a thin **in-process** supervisor over
`ProductConfig.runtime.services` — operator-declared
**subprocesses**. Boundary helpers:

- `start_product_runtime_from_json_file(<path>)` →
  services up.
- `stop_product_runtime_from_json_file(<path>)` →
  services down.
- `get_product_runtime_status_from_json_file(<path>)` →
  per-service status with `pid`, `started_at`,
  `restart_attempts`, `last_exit_code`,
  `stdout_log_path`, `stderr_log_path`, etc.
- `reload_product_runtime_from_json_file(<path>)` →
  controlled stop-then-start (explicitly not a hot
  reload, per `runtime.py:18–19`).

Underlying primitives in `process_control.py`:

- `spawn_service(command, working_dir, env_overrides,
  stdout_handle, stderr_handle)` —
  `subprocess.Popen` with `stdin=DEVNULL`,
  `start_new_session=True` (POSIX) / `CREATE_NEW_PROCESS_GROUP`
  (Windows), per-service stdout/stderr file handles
  optional, no `shell=True`.
- `is_pid_alive(pid)` — POSIX uses `os.kill(pid, 0)`;
  Windows uses `OpenProcess + WaitForSingleObject` via
  ctypes.
- `terminate_pid(pid)` — POSIX `os.kill(pid, SIGTERM)`;
  Windows `OpenProcess(PROCESS_TERMINATE) +
  TerminateProcess`.
- `get_pid_exit_code(pid)` — Windows only via
  `GetExitCodeProcess`; POSIX honestly returns `None`
  (the orchestrator did not `fork`-spawn the child of
  the current process; it reads PIDs from
  `runtime-state.json` after restarts).

Per-service spec / state in `models.py`:

- `ProductServiceSpec.restart_policy ∈ {"never",
  "restart-if-stale"}`, default `"never"`. Reference:
  `models.py:64–73`, `models.py:127`.
- `RESTART_POLICIES = ("never", "restart-if-stale")`.
- `RuntimeServiceState` carries `restart_policy`,
  `restart_attempts`, `last_exit_code`,
  `stdout_log_path`, `stderr_log_path`,
  `last_started_at`, `last_stopped_at`.

Persistent state in `state.py` (`runtime-state.json`
under `<work_dir>/.runtime/`, schema version 2 with
backward-compat reader; survives orchestrator restart).

Log rotation in `runtime_logs.py` (single-generation
rotate-if-exceeds-size, per Phase 6 / Step 6 narrow
contract).

**What this is.** Verbatim from `runtime.py:11–19`: "a
thin supervisor over operator-declared subprocesses; a
persistent on-disk state file under
`<work_dir>/.runtime/` so `status` survives orchestrator
restarts; a cross-platform liveness probe; a contract
that `reload` is a controlled stop-then-start, not a hot
reload."

**What this is not** — verbatim from `runtime.py:21–31`:
"it does **not** start MCP transports inside the three
servers — those still live as in-process modules; it
does **not** introduce write effects from inside the
product layer; it is **not** a daemon manager / service
manager (no Windows Service / systemd unit registration
on this step); it is **not** a per-service health
probe."

And verbatim from `docs/operator-manual.md`
(grep `head_limit=20`, lines 191–197): "No production-
grade process supervisor (no Windows Service / ...). No
background watcher / auto-restart daemon. The
`restart-if-stale` policy triggers only on next
stop-then-start."

And verbatim from `process_control.py:168–169`: "Callers
that want POSIX exit codes need a real supervisor — out
of scope for Step 6."

**What this means for Track L.** The platform already
has, since Phase 5 / Step 3 and extended by Phase 6 /
Step 6, an **in-process narrow supervisor** for
operator-declared **product-layer subprocesses**. These
subprocesses are **not** the three MCP servers — the MCP
servers run as in-process modules invoked separately by
`python -m mcp_<server>`. The Phase 6 layer is for
sidecar workers (e.g., 1С-binary-adjacent processes the
operator declares in `runtime.services`). Track L closes
a **different and orthogonal** gap: turning the
foreground-blocking MCP server entrypoints into
**OS-supervised long-lived services** wrapped by
`systemd` / `launchd` / Windows Service Control Manager
**outside** the platform process tree.

This is a crisp distinction that Step 3 contract must
preserve verbatim:

- Phase 6 `runtime.py` = in-process supervisor for
  operator-declared **product-layer subprocesses**.
- Track L = **external OS service supervisor** wrapping
  the foreground-blocking MCP server entrypoints.

Track L MUST NOT extend `runtime.py` to "also supervise
the MCP servers" — that would be the rejected code-level
supervisor path (plan §12.Q1 option C) and would
contradict `runtime.py:24` "it does **not** start MCP
transports inside the three servers". Track L MUST keep
the supervision concern **outside** the platform process
tree, on the OS layer.

### §3.5 Deployment-boundary recipe (Track J / Step 4)

`docs/operators/deployment-boundary.md` (691 lines, 10
sections) covers the network-side deployment posture:
which bind-host scenarios are supported, how the
operator-owned reverse proxy terminates TLS, why
`X-Forwarded-*` headers are MUST-NOT-consume, why
`/healthz` is deferred. It does **not** cover the
**process-supervision** posture: how the MCP server
process behind the reverse proxy stays alive across
reboots, how it restarts on failure, how its logs are
surfaced. Track L is the symmetric document on the
process-lifecycle dimension that the deployment-
boundary recipe is on the network-exposure dimension.

### §3.6 Client-side replay (Track K / Step 4)

`scripts/dev/mcp_client_smoke.py` is a Track K artefact;
not in Track L scope. The audit notes it only to
distinguish "operator-runnable diagnostic harness that
spawns and tears down its own server subprocess for one-
shot proof" from "OS-level supervisor that keeps the
server alive across reboots". They are different things.

---

## §4. Existing reusable surfaces

These are repo surfaces Track L can legitimately rely on,
without modifying them:

### §4.1 Trivially-thin foreground entrypoints

Three `__main__.py` modules, each ~40 lines (`__main__.py:1–43`
for read-server, symmetric for write- and intelligence-).
They follow the `Type=simple`-compatible shape: the
process blocks the foreground until it exits, and exits
cleanly on `KeyboardInterrupt` / EOF. This is exactly
the shape `systemd` `Type=simple` expects, what `launchd`
`KeepAlive=true` `RunAtLoad=true` expects, and what
`nssm` / `pywin32` Windows wrappers can host. **No
production code change needed** to make these supervisable.

### §4.2 CLI surface

Per `_network_transport.py` and `_stdio_transport.py`
argument parsers, each server accepts (Track G / H
exposes these uniformly across all three servers):

- `--transport {stdio,http}` (Track G default = `stdio`,
  Track H opt-in = `http`).
- `--config-path <path>` (Track G).
- `--log-level <level>` (Track G; default `INFO`).
- `--bind <HOST>:<PORT>` (Track H, HTTP only).
- `--auth-token-env <VARNAME>` (Track H, HTTP only).

A systemd `ExecStart=` line can use any combination of
these. No new CLI flag required.

### §4.3 Logging to stderr

All three servers log diagnostic output to stderr (per
`__main__.py:13` and the `logging` module's default
basicConfig). `systemd` captures stderr to its journal
automatically; `launchd` captures it to `StandardErrorPath=`;
`nssm` redirects it to `--AppStderr <path>`; Windows
Service Control Manager via pywin32 captures it via the
service framework. The audit observes that **no log-path
configuration is required at the Python layer** — Track L
can rely on the OS service manager's stream capture.

### §4.4 Environment-variable-based auth token

Track H requires the HTTP transport's bearer token to be
sourced from an environment variable via
`--auth-token-env <VARNAME>` (or `ProductConfig.auth.tokens`
with `${ENV:NAME}` placeholders). Track L's unit-file
template can declare `Environment=` (systemd) /
`EnvironmentFile=` (systemd recommended for secrets) /
`EnvironmentVariables=` (launchd) entries pointing at
operator-managed env-vars; the operator's secret manager
populates them. No Track L credentials in repo — placeholder
discipline preserved.

### §4.5 Foreground signal handling

Both transports already handle `KeyboardInterrupt`
gracefully (`_stdio_transport.py:208`, `_network_transport.py:618`).
On Windows, NSSM's `AppStopMethodConsole` sends `Ctrl-C`
which lands in this branch. On POSIX, `systemd`'s
`KillSignal=SIGINT` override (single line in the unit
file) re-routes service stop to the same branch. **No
production code change needed** to enable graceful
shutdown across both OS families.

### §4.6 Cross-platform process primitives in `process_control.py`

Although `runtime.py` is **not** the supervisor Track L
is producing, the cross-platform helpers in
`process_control.py` (`is_pid_alive`, `terminate_pid`,
ctypes-based Windows handle management) are precedent
that the repo handles platform-specific process lifecycle
correctly. Track L does **not** need to import or extend
these — they live in the product layer for the product-
layer in-process supervisor — but they are evidence that
the cross-OS posture in this repo is mature enough to
support Track L's documentation discipline.

---

## §5. Adjacent but insufficient surfaces

These surfaces address something related to service
supervision but are not, on their own, sufficient closure
of the Track L gap:

### §5.1 `runtime.py` in-process supervisor

Insufficient because: scoped to operator-declared
**product-layer subprocesses** (not the three MCP
servers); explicitly **not** a service manager (no
systemd / launchd / Windows Service registration); not a
background watcher (`restart-if-stale` triggers only on
next stop-then-start); not a per-service health probe.
Track L cannot piggyback on `runtime.py` to make the MCP
servers OS-supervised — extending it would be code-level
supervisor scope-creep that the plan §12.Q1 explicitly
rejected.

### §5.2 `install.ps1` install fast-path

Insufficient because: materialises config, prints
follow-up `python -m` commands. Does not register a
service. Does not produce a unit file. Does not write
`sc.exe create` invocations. Track L could **optionally**
ship a sibling install-side wrapper under
`scripts/release/` (PATH C in plan §12.Q3), but that is
an addition, not a re-use of `install.ps1`.

### §5.3 Track J `deployment-boundary.md` recipe

Insufficient because: orthogonal axis (network exposure
posture vs process lifecycle posture). Track L is the
process-lifecycle sibling document on the same shelf,
not a subset of the deployment-boundary recipe.

### §5.4 Track K `mcp_client_smoke.py` harness

Insufficient because: one-shot client-side smoke that
spawns its own server subprocess and tears it down.
Track L's supervised server runs across reboots, with
external lifecycle verbs; harness's lifecycle is
"spawn for the duration of the test". Different
problem.

### §5.5 `launch.ps1` umbrella wrapper

Insufficient because: foreground dev convenience;
explicitly does not start MCP servers. Track L cannot
adopt `launch.ps1` even as a launcher for the
supervised path, because the supervised path runs under
the OS service manager, not under a PowerShell session.

### §5.6 `[project.scripts]` console entries

Insufficient because: declared, but not currently
installable (the empty wheel-packages list per Track C /
Step 3 honest constraint). Operators today invoke
`python -m mcp_<server>`, not `mcp-read-server` /
`mcp-write-server` / `mcp-intelligence-server`
directly. Track L's recipe can use **either** form in
its unit file `ExecStart=`; both work today via the
PYTHONPATH-bootstrap path, but neither is exposed via
a wheel install. This is a packaging concern, not a
supervision concern — Track L does not address it.

### §5.7 Operator / administrator / developer manuals

Currently describe one-shot interactive workflows
(`python -m mcp_<server> --transport ...`); do not
contain a `systemctl start mcp-read-server` /
`launchctl bootstrap` / `nssm install` style recipe.
Insufficient on their own; Track L's Step 4 recipe is
the addition that closes the gap.

---

## §6. Clearly missing pieces

Each of the following is verifiably absent at HEAD
`e713f8e`:

1. **Zero `systemd` unit files** anywhere in the tree.
   Whole-repo grep for `[Unit]`, `[Service]`,
   `[Install]`, `ExecStart=`, `Restart=`, `KillSignal=`,
   `EnvironmentFile=`, `WantedBy=` returns zero
   `.service` files and zero embedded unit-file
   snippets in `.md` files. The only matches are this
   audit (in §6 / §7 reference text) and the Track L
   Step 1 plan / step-map (which mention the
   vocabulary as terms to introduce, not as recipe
   content).

2. **Zero `launchd` plists**. Whole-repo grep for
   `<key>Label</key>`, `<key>ProgramArguments</key>`,
   `<key>RunAtLoad</key>`, `<key>KeepAlive</key>`,
   `.plist` returns zero files.

3. **Zero Windows Service registration helpers**.
   Whole-repo grep for `New-Service`, `sc.exe create`,
   `Set-Service`, `Restart-Service`, `nssm install`,
   `pywin32`, `win32serviceutil`, `ServiceManager`,
   `SERVICE_CONTROL_STOP` returns zero matches (no
   pywin32 dependency declared, no Windows Service
   wrapper class in `apps/*/src/` or `packages/*/src/`).

4. **Zero `pidfile` / `PIDFile` / `--background` /
   `--fork` / `--daemonize` plumbing** in any Python
   module or PowerShell script. The audit confirms by
   grep that these terms appear only in honest-non-goals
   prose in Track G / H / J / K closure docs, never as
   feature surfaces.

5. **Zero `signal.signal(SIGTERM, ...)` handler**.
   The only signal-related call in production code is
   `os.kill(pid, signal.SIGTERM)` inside
   `process_control.terminate_pid` (POSIX branch) — that
   is the supervisor **sending** SIGTERM, not the
   supervised process **handling** it.

6. **Zero documented stop / start / restart / status /
   logs operator vocabulary** for the MCP servers as
   long-lived services. Existing manuals describe how
   to launch the server interactively; none describe
   how to manage it as a unit.

7. **Zero `journald`, `Event Viewer`, `Application Log`
   integration mention**. Track L Step 4 recipe will
   need to address where logs land on each OS family;
   today this is implicit (stderr → caller's terminal).

8. **Zero `EnvironmentFile=` / `EnvironmentVariables=`
   recipe** for managing `MCP_TOKEN`-class secrets in
   the supervised context. Track H Step 4 already wired
   `--auth-token-env <VARNAME>`, so the runtime is
   ready; the missing piece is operator-facing guidance
   on how to inject that variable into the supervised
   process's environment securely.

9. **Zero `Restart=on-failure` / `RestartSec=` /
   `StartLimitBurst=` / `StartLimitIntervalSec=`
   policy guidance**. Operators currently have no
   suggested defaults.

10. **Zero `User=` / `Group=` (systemd) / `RunAsUser`
    (launchd) / service-account (Windows) discipline
    documented**. Operators currently have no
    documented "what user account should the MCP server
    run under" guidance.

---

## §7. Directional Q1–Q6 resolutions

These are **directional**, evidence-grounded
recommendations for Step 3 contract consumption. They
are not normative; they preserve Step 4 PATH openness
where evidence stays mixed.

### §7.1 Q1 — what counts as "service supervision" for this repo?

**Evidence summary.** §3.4 shows the platform already
defers "real supervisor" to "out of scope for Step 6";
§3.1 shows the three MCP server entrypoints are already
shaped for `Type=simple`-style OS supervision; §6 shows
zero unit-files / plists / service-control helpers in
repo today.

**Directional resolution.** Track L's "service
supervision" target is at minimum (a) **one documented
operator-facing recipe per supported OS family** plus
(b) **one declarative service-unit template per
implementation-covered OS family**, demonstrating
register / start / stop / restart / status / logs.
Broader code-level supervisor (custom daemon wrapper,
pywin32 service class, etc.) is rejected by both the
plan §12.Q1 option C ban and by the runtime.py
"not a daemon manager / service manager" precedent.

This matches **plan §12.Q1 option A** (documented
template + operator workflow) and accommodates **option
B** (PATH C wrapper script) only if Step 3 contract
authorizes it.

### §7.2 Q2 — primary implementation OS family?

**Evidence summary.** §3.2 / §3.3 / §3.4 do not lean
strongly toward one OS family; the operator-machine
context observed in
`examples/demo-infobase/infobase6.config.json` is
Windows-resident (`C:/Users/user/Documents/InfoBase6`,
`C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`),
suggesting Windows is realistic for at least one
operator. However, the broadest industrial precedent
for declarative service supervision is **systemd**:
single-file `[Unit] / [Service] / [Install]` shape,
mature `systemctl status / start / stop / restart`
vocabulary, well-known `journalctl -u <unit>` logs
discovery, well-documented `Restart=on-failure` policy
language, and the strongest stability across Linux
distributions over 10+ years.

**Directional resolution.** Implementation-covered
closure-gate target = **systemd / Linux first**.
Cross-OS prose covering Windows (via NSSM or pywin32
patterns) and macOS (launchd) MUST appear in the same
Step 4 recipe, with the honest framing "implementation
verified on Linux/systemd; Windows and macOS guidance
is prose-only with vetted external references".
Windows-first remains acceptable if Step 3 contract
chooses to pivot — the operator-machine context
argument is non-trivial — but the audit's directional
recommendation is systemd-first.

This matches **plan §12.Q2 option (A) with cross-OS
prose** as the default.

### §7.3 Q3 — likely Step 4 PATH?

**Evidence summary.** §3.1 / §3.2 show that the
foreground-blocking entrypoint shape is **already
correct** for `Type=simple` supervision — there is
nothing for Track L to fix in the runtime. §6 shows the
gap is purely operator-facing: missing template + missing
recipe. §3.4 establishes that scope-creep into in-repo
code-level supervisor would conflict with `runtime.py:24`
"it does **not** start MCP transports inside the three
servers".

**Directional resolution.** Step 4 PATH = **PATH B
(docs + one declarative template artefact)** is the
honest narrowest path. PATH A (docs-only) is
acceptable-as-fallback if Step 3 contract decides a
template is too prescriptive (e.g., distro-specific
paths in a unit file lock prematurely). PATH C (docs +
template + wrapper script under `scripts/release/`) is
acceptable if Step 3 decides the install-side
ergonomics warrant a thin wrapper around
`systemctl enable` / `nssm install` (with placeholders
only; no real credentials; under the plan §8 LOC cap of
≤ 150 LOC stdlib-only).

Evidence does **not** uniquely lock to one of these
three; the audit leans toward PATH B by symmetry with
Track J / Step 4 (one operator recipe + one set of
declarative snippets) and Track K / Step 4 (one
operator-runnable artefact, no production code change).
Step 3 contract decides.

### §7.4 Q4 — which lifecycle verbs are truly mandatory for closure?

**Evidence summary.** §6.6 shows all five verbs (start,
stop, restart, status, logs) are absent. The cost of
adding each is one line per OS family in the recipe;
the operator benefit of each is straightforwardly
"one less thing to invent". §3.1 shows the runtime
already supports the implicit shape for each verb (start
= invoke entrypoint, stop = `KeyboardInterrupt` /
SIGTERM equivalent, restart = stop-then-start, status =
PID liveness probe, logs = stderr capture). No
verb-specific runtime gap exists.

**Directional resolution.** All five verbs
**mandatory for closure**. Partial coverage rejected.
Evidence is one-sided: there is no concrete cost to
covering all five, and the closure narrative is
incomplete without any one of them. This matches plan
§12.Q5 default.

### §7.5 Q5 — what is definitely insufficient as closure proof?

**Evidence summary.** §5.1 through §5.7 enumerate the
adjacent-but-insufficient surfaces; §6 enumerates what
is missing.

**Directional resolution.** Definitively insufficient on
its own as Track L closure proof:

- **"Just use `python -m mcp_<server>` in a terminal"**
  — that is the current state and the whole reason
  Track L exists.
- **Launch instructions only** (e.g., a paragraph in
  README saying "to run as a service, write your own
  unit file") — operator pain remains.
- **Release docs only** (e.g., a `docs/release-handoff.md`
  bullet) — same as above.
- **Generic deployment prose without OS-facing recipe**
  — e.g., "deploy behind a process supervisor of your
  choice"; offloads the contract back to the operator.
- **Manual operator lore not committed in repo** — does
  not survive the operator-machine context.
- **Extending `runtime.py` to also supervise MCP
  servers in-process** — violates `runtime.py:24` and
  the plan §12.Q1 option C rejection; in-process
  supervision is not OS service registration.

### §7.6 Q6 — does Track L likely require production code at all?

**Evidence summary.** §3.1 shows `Type=simple`-compatible
foreground-blocking entrypoints. §3.3 shows graceful
shutdown via `KeyboardInterrupt` (handled by both
transports). §4.1–§4.5 show that PYTHONPATH bootstrap,
log-stream capture, env-var-based auth, and signal
routing all have viable Step 4 recipes that do **not**
require Python-side code change.

**Directional resolution. NO production code change.**
The existing foreground-blocking shape is exactly the
right shape for `Type=simple` systemd / launchd /
pywin32 / nssm. Adding `signal.signal(SIGTERM, ...)`
explicitly on POSIX is debatable but defensible-as-not-
needed because (a) Python's default SIGTERM disposition
+ daemon-threads HTTP mode + `KillSignal=SIGINT`
systemd override yield the same shutdown semantics, and
(b) the in-flight-request abandonment posture is
explicit policy (`daemon_threads = True`), not a
defect. Adding `--pidfile` is unnecessary because
`systemd`'s `MainPID=` tracking handles `Type=simple`
processes natively. This matches plan §12.Q6 option (A).

If Step 2 audit had revealed a concrete defect in the
foreground-blocking shape (e.g., `KeyboardInterrupt` not
firing reliably under specific signal-handling
conditions), the audit would directionally recommend
narrow option (B) — but Step 2 found no such defect.

---

## §8. Step 3 handoff note

These items the audit hands off to Step 3 contract for
normative locking. They are **not** decided here; Step 3
locks them.

1. **Track L "service supervision" target definition.**
   Audit-directional = recipe + declarative template +
   five lifecycle verbs documented. Step 3 to lock the
   exact text.

2. **Implementation-covered OS family.** Audit-
   directional = systemd / Linux first, with cross-OS
   prose for Windows / macOS in the same recipe.
   Step 3 to lock final pick and the cross-OS prose
   discipline.

3. **Step 4 PATH selection.** Audit-directional = PATH B
   (docs + one declarative template). Step 3 may pin
   PATH A or PATH C if it has a defensible reason from
   audit evidence; default = PATH B.

4. **Step 4 file surface cap.** Audit-directional = ≤ 2
   new files for PATH B (one recipe + one template);
   ≤ 3 new files for PATH C (recipe + template +
   wrapper script). Step 3 to lock final cap.

5. **Step 4 LOC cap for any code-bearing artefact.**
   Audit-directional = ≤ 150 LOC stdlib-only, no new
   dependencies (matching plan §8 default). Step 3 to
   lock.

6. **Step 4 file locations.** Audit-directional =
   `docs/operators/service/` for the recipe (co-located
   with Track J's `docs/operators/deployment-boundary.md`);
   `docs/operators/service/<filename>.service` for the
   systemd unit-file template. If PATH C is chosen,
   wrapper script under `scripts/release/`. Step 3 to
   lock final paths.

7. **Lifecycle-verb coverage.** Audit-directional = all
   five (start / stop / restart / status / logs)
   mandatory; partial coverage rejected. Step 3 to
   lock.

8. **Production code modification.** Audit-directional =
   none. Step 3 to lock this as a forbidden surface
   for Step 4.

9. **Placeholder discipline.** Audit-directional = the
   same placeholder vocabulary used by Track J recipe
   plus service-specific tokens (`<USER>`, `<GROUP>`,
   `<HOST>`, `<PORT>`, `<UNIT_NAME>`, `<SERVICE_NAME>`,
   `<LOG_PATH>`, `<VARNAME>`, `<MCP_TOKEN_VARNAME>`).
   Step 3 to lock final list.

10. **Forbidden file surfaces for Step 4.** Audit-
    directional: production code, `pyproject.toml`,
    `scripts/dev/*` (existing files), `SECURITY.md`,
    `docs/release-handoff.md`, `apps/platform/README.md`,
    `CHANGELOG.md`, `README.md`, `PROJECT-STATUS.md`,
    `examples/*`, `docs/operators/deployment-boundary.md`,
    `scripts/dev/mcp_client_smoke.py`, all Track L
    Step 1/2/3 deliverables (frozen anchors). Step 3
    to lock final list.

11. **Verification protocol for Step 4.** Audit-
    directional: scope checks (new-file count ≤ cap,
    forbidden surfaces byte-identical), selfcheck
    (registries `15 / 25 / 16`, status=ok), release-
    verify (8-check `verify-release.ps1 -AllowDirtyTree`
    GREEN), honesty (no `1cv8.exe`, no real
    credentials, no premature closure language, no
    false implementation claims, no fake "service
    supervision solved" framing), doc-consistency (all
    five lifecycle verbs covered, cross-OS prose
    present if Step 3 locks systemd-first), template-
    correctness (unit-file template parses cleanly under
    `systemd-analyze verify` semantics — Step 3 may
    require this or treat it as recommendation-only).
    Step 3 to lock the exact count.

12. **Honest non-goals carry-forward.** Audit-
    directional: full list verbatim from plan §7
    plus the additional non-goals revealed by §6:
    no `journald` integration shipping; no `Event
    Viewer` integration shipping; no `User=` / `Group=`
    enforcement (recipe documents recommended values,
    operator chooses); no `RestartPolicy` defaults
    chosen as policy — recipe documents standard
    values, operator chooses. Step 3 to lock.

13. **Q7 framing for Step 6.** Audit-directional =
    NO-BUMP if Step 4 = PATH A or PATH B (Track J /
    Track K precedent); PATCH only if Step 4 = PATH C
    with honest defect-class framing (default not the
    case); MINOR / MAJOR forbidden. Step 6 locks.

14. **Carry-forward invariants from Tracks G / H / I /
    J / K.** Audit-directional: identical to plan §11
    table — Track G stdio runtime byte-identical;
    Track H HTTP runtime byte-identical; Track I
    installer round-trip byte-identical; Track J §13 /
    §6 / §7 / §8 carry-forward unchanged (in-process
    TLS forbidden, mTLS forbidden, Forwarded headers
    MUST-NOT-consume, `/healthz` not shipped);
    Track K diagnostic harness byte-identical.
    `runtime.py` Phase 5 / Phase 6 in-process
    supervisor for product-layer subprocesses byte-
    identical (Track L does **not** extend it).
    Registries `15 / 25 / 16`. `pyproject.toml`
    `version=0.5.1` until Step 6 Q7.
    Step 3 to lock.

---

## §9. Honest summary

**The gap is real.** §6's ten enumerated absences are
each independently verifiable in the repo at HEAD
`e713f8e`. No `systemd` unit file, no `launchd` plist,
no Windows Service helper, no PID-file plumbing, no
custom SIGTERM handler, no documented lifecycle
vocabulary for the MCP servers as long-lived services.
Existing launch surfaces (`launch.ps1`, `install.ps1`,
the three `__main__.py` entrypoints) are insufficient
on their own and do not address the gap; they were
never designed to.

**The fix is narrow.** §7.6 establishes that no
production code change is required. §4.1–§4.5 establish
that the foreground-blocking entrypoint shape is
already correct for OS-level supervision. §6.1–§6.6
establish that the missing pieces are operator-facing
documentation and at most one declarative template.

**The risk of scope-creep is real.** §3.4 establishes
that an in-repo in-process supervisor already exists
(`runtime.py`); extending it to "also supervise the MCP
servers" is the rejected code-level supervisor path
and would contradict `runtime.py:24`. Track L MUST
keep supervision concern **outside** the platform
process tree, on the OS layer.

**The audit does not commit Step 3.** Step 3 locks the
final PATH (A / B / C), the final OS family, the
final file surfaces, the final LOC cap, the
verification protocol, and the Q7 framing for Step 6.
This audit recommends directionally; it does not
decide normatively. Step 4 PATH openness is preserved
exactly because audit evidence narrows directionally
without uniquely locking.

**No "service supervision solved" claim.** Track L's
closure target is one OS-family implementation slice +
cross-OS prose + five lifecycle verbs documented +
honest denial of "production-ready service supervision",
"all OS families supported", "clustered HA", "zero-
downtime restart" claims. The same honest-non-goals
discipline that closed Track J and Track K applies
here.

**Active state at the end of Step 2.** Track L /
Step 2 closed (this audit). Track L still **active**.
Next step = Track L / Step 3 (normative contract).
Step 3 not opened in this commit.
