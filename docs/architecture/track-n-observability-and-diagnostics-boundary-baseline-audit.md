# Parallel Track N — Observability and Diagnostics Boundary — Baseline Audit

**Step status.** Parallel Track N / Step 2 — descriptive
baseline audit. Companion to
[track-n-observability-and-diagnostics-boundary-plan.md](track-n-observability-and-diagnostics-boundary-plan.md)
and
[track-n-observability-and-diagnostics-boundary-step-map.md](track-n-observability-and-diagnostics-boundary-step-map.md).

This document is **descriptive**, not normative. It
inventories what observability/diagnostics surfaces
already exist at HEAD `efb4e5c` (project version
`0.5.2`), classifies them, and produces **directional**
Q1–Q6 resolutions grounded in the repo evidence below.
It does **not** use RFC 2119 MUST / MUST NOT / SHOULD /
SHOULD NOT language; that vocabulary is reserved for the
Step 3 normative contract.

The audit explicitly does **not** decide Step 4 path
dogmatically. The intent is to give Step 3 a credible
evidence base, not to pre-empt Step 3.

---

## §1. Purpose / scope

### §1.1 What this document is

A single descriptive audit covering:

- Operator-visible diagnostics surfaces actually present
  in the repo at `efb4e5c`.
- Verification / diagnostic helper surfaces (selfcheck,
  verify-release, MCP client smoke harness, install
  fast-path runner, dev-check CI workflow).
- Observability-adjacent documentation under
  `docs/operators/` and elsewhere.
- The honest gap between "there are some signals" and
  "there is a supported observability/diagnostics
  boundary".
- Directional Q1–Q6 resolutions to hand off into Step 3.

### §1.2 What this document is **not**

- Not a contract. No MUST / MUST NOT / SHOULD.
- Not a Step 4 implementation decision.
- Not a forecast of every possible future observability
  surface. Out-of-scope categories (full OpenTelemetry /
  Prometheus / Grafana / Tempo / Loki / Jaeger / SIEM /
  distributed tracing / alerting / on-call /
  `/healthz` / log-aggregation forwarder / structured-
  logging library) are named only for boundary
  hygiene, not analysed for feasibility.
- Not a rewrite or amendment of Step 1 planning docs.
  Step 1 plan + step-map remain the planning anchors;
  this audit complements them with repo evidence.

### §1.3 What the audit explicitly preserves

- Tracks A–M closure invariants byte-identical
  (verifiable via `git diff a3bdc48 -- apps/ packages/
  scripts/`, etc.).
- Registry invariant `read=15 / write=25 /
  intelligence=16` (verifiable via `python
  scripts/dev/selfcheck.py`).
- No production code change.
- No `pyproject.toml`, `scripts/*`, `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `CHANGELOG.md`, `README.md`, `PROJECT-STATUS.md` edit
  in this step.

---

## §2. Method / evidence sources

The audit is grounded in direct repo inspection at
`efb4e5c`. Specifically:

- **Transport modules read directly.**
  `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  and `packages/mcp-common/src/mcp_common/_network_transport.py`
  inspected for `logging`, `sys.stderr`, `print`,
  `SystemExit`, `sys.exit`, status-code emission, and
  shutdown-path messages.
- **Three MCP server entrypoints inspected.**
  `apps/mcp-read-server/src/mcp_read_server/__main__.py`,
  `apps/mcp-write-server/src/mcp_write_server/__main__.py`,
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
  — each delegates to `mcp_common` `run_main` / `run_main_http`.
- **Helper scripts read directly.**
  `scripts/dev/selfcheck.py`,
  `scripts/release/verify-release.ps1`,
  `scripts/dev/mcp_client_smoke.py`,
  `scripts/release/install.ps1`,
  `scripts/release/_install_runner.py`.
- **Operator docs read directly.**
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/service-supervision.md`,
  `docs/operators/service/mcp-server.service`,
  `docs/operators/packaging/distribution-boundary.md`.
- **Health / troubleshooting packages enumerated.**
  `packages/onec-health/src/onec_health/`,
  `packages/onec-troubleshooting/src/onec_troubleshooting/`.
- **CI workflow inspected.**
  `.github/workflows/dev-check.yml`.
- **Whole-repo grep on observability vocabulary** —
  `opentelemetry|otel|prometheus|openmetrics|grafana|tempo|loki|jaeger|siem|distributed.tracing|/healthz|/readyz|/livez|log.aggreg|forwarder|alerting`
  plus `observ|monitor|triage|troubleshoot|diagnost|health|metric|tracing|stderr|journal`.

Citations below give file paths plus line numbers so
Step 3 can verify directly.

---

## §3. Current observability/diagnostics baseline

### §3.1 stderr emission via Python `logging`

Both transport modules wire the same `logging`
boundary:

- `_stdio_transport.py:62-68` — `_configure_logging()`
  calls `logging.basicConfig(stream=sys.stderr,
  level=getattr(logging, level_name),
  format="%(asctime)s %(levelname)s %(name)s:
  %(message)s")` and returns `logging.getLogger(server_name)`.
- `--log-level` flag declared at
  `_stdio_transport.py:53-58` with `choices =
  ALLOWED_LOG_LEVELS = ("DEBUG", "INFO", "WARNING",
  "ERROR")`, default `"INFO"`, help `"Diagnostic log
  level. Logs are written to stderr."`.
- The unified `run_main_http()` at
  `_network_transport.py:632-704` also calls
  `_configure_logging(args.log_level, server_name)`
  (line 662) — same boundary, same format.

This is the only structured signal abstraction in the
runtime today. Everything else (stderr, exit codes,
HTTP responses) is conveyed through this same `logging`
pipe or through explicit `print(..., file=sys.stderr)`
in startup failures.

### §3.2 Startup banners

- **stdio.** `_stdio_transport.py:181`:
  `logger.info("Starting %s stdio transport (JSON-RPC
  2.0).", server_name)`.
- **HTTP.** `_network_transport.py:609-615`:
  `logger.info("Starting %s HTTP transport (JSON-RPC
  2.0) on %s:%s with %d valid token(s).",
  server_name, actual_host, actual_port,
  len(valid_tokens))`.

Both banners are emitted at `INFO` level **after** a
successful socket bind / stream open. They are the
canonical "the server is up" signal an operator gets
today.

### §3.3 Process exit codes

Repo evidence:

| Scenario | Exit Code | Citation |
| --- | --- | --- |
| Clean Ctrl-C / SIGINT (stdio) | 0 | `_stdio_transport.py:208-210` |
| EOF on stdin (stdio) | 0 | `_stdio_transport.py:211-212` |
| Clean Ctrl-C / SIGINT (HTTP) | 0 | `_network_transport.py:618-620` |
| Bad config-path / argparse startup failure | 2 | `_network_transport.py:165-170` (`_fail()`) |
| `--transport http` without `--bind` | 2 | `_network_transport.py:686-687` |
| Auth-config missing / unresolved env var | 2 | `_network_transport.py` via `_resolve_token_sources` + `_fail()` |
| Bind error (port in use) | 2 | `_network_transport.py:603-605` |
| Unhandled exception (stdio) | 1 | `_stdio_transport.py:242-244` |
| Unhandled exception (HTTP) | 1 | `_network_transport.py:701-703` |

`0` = clean exit; `1` = unhandled exception logged via
`logger.exception("Fatal error in %s entrypoint", …)`;
`2` = startup-time operator-readable failure routed
through `_fail()` (single line on stderr, no traceback).
This three-bucket convention is **factually present in
the code** but is **not currently documented** in any
operator-facing recipe.

### §3.4 Shutdown messages

- `_stdio_transport.py:208-212` —
  `"Interrupted (KeyboardInterrupt); exiting cleanly."` /
  `"EOF on stdin; exiting cleanly."`, both `INFO`.
- `_network_transport.py:618-620` —
  `"Interrupted (KeyboardInterrupt); shutting down HTTP
  server."`, `INFO`.

These are the canonical "the server stopped on purpose"
signals.

### §3.5 HTTP transport diagnostic surface

`_network_transport.py` returns identical 401
envelopes for every auth-failure mode (per Track H /
Step 3 §8.4 failure-equivalence). Repo evidence:

| Condition | HTTP Status | Headers | JSON-RPC Code / Message | Citation |
| --- | --- | --- | --- | --- |
| Missing / empty / wrong-scheme / wrong-token Authorization | 401 | `WWW-Authenticate: Bearer realm="mcp"` | `-32001 / "Unauthorized"` | `_network_transport.py:496-504` + `:519-541` |
| Multiple Authorization headers | 400 | — | `-32600 / "Invalid Request"` | `_network_transport.py:364-373` |
| Body > 1 MiB | 413 | — | `-32600 / "Invalid Request"` | `_network_transport.py:392-399` |
| Non-`application/json` Content-Type | 415 | — | `-32600 / "Invalid Request"` | `_network_transport.py:354-363` |
| Bad JSON body | 400 | — | `-32700 / "Parse error"` | `_network_transport.py:405-412` |
| Bad JSON-RPC envelope | 400 | — | `-32600 / "Invalid Request"` | `_network_transport.py:423-432` |

Every request goes through the handler's
`log_message()` override at
`_network_transport.py:314-328`, which routes the
default Python `http.server` access-log line into
`logger.info("http %s - %s", ...)`. So `INFO` already
includes per-request access lines on the HTTP path —
this is a non-trivial observability fact today.

Constant-time token comparison via
`hmac.compare_digest()` at
`_network_transport.py:538-540` ensures tokens never
appear in logs in any failure path.

### §3.6 Install fast-path output

- `scripts/release/_install_runner.py:57-78` prints a
  block of `ok / mode / product_name / profile_name /
  default_environment / output_config_path /
  config_written` fields (one per line), then optional
  `confirmed findings`, `presumed findings`,
  `recommended actions` sub-blocks with per-finding
  `[severity] code: detail` shape.
- Exit codes (`_install_runner.py:80-84`):
  `0` = ok in `preview` / `executed` mode;
  `2` = mode is `rejected` (operator-blocking finding);
  `3` = other failure.
- `install.ps1` delegates to `_install_runner.py`; no
  redaction layer is needed because tokens are never
  printed (passwords inside `command_preview` are
  redacted at Track D's `installer.py` layer before
  ever reaching the runner — see Track D / Step 4
  closure for that anchor).

### §3.7 selfcheck output

`scripts/dev/selfcheck.py` is short and concrete.
Output is **exactly eleven** key=value lines printed in
order (`selfcheck.py:95-105`):

```
imports_ok = true
read_server_tools = [...]
write_server_tools = [...]
intelligence_server_tools = [...]
production_write_allowed = false
local_dev_write_allowed = false
diagnosis_example = gateway_down
config_envs = [...]
health_summary_ok = false
health_summary_problem = gateway_down
selfcheck_status = ok
```

Exit code = `0` on success; the script's docstring
(`selfcheck.py:1-5`) is explicit: **"No try/except: if
anything is wired incorrectly, we want a loud, honest
failure."** There is no `--json` mode; the format is
parseable key=value text only.

### §3.8 verify-release output

`scripts/release/verify-release.ps1` runs **exactly 8
named checks** in order (`verify-release.ps1:82-267`):

1. `"Repo layout (root files)"` (line 90)
2. `"Release entrypoints"` (line 102)
3. `"Important docs"` (line 114)
4. `"Working tree"` (line 134 / 138 / 140)
5. `"Git baseline"` (line 154 / 156)
6. `"Selfcheck"` (line 163 / 179 / 181)
7. `"Credential leak guard"` (line 213 / 215)
8. `"Credential template hygiene"` (line 264 / 266)

Summary block at `verify-release.ps1:271-292` prints
each check as `"  [PASS|FAIL|SKIP|WARN] {name} -
{detail}"` and exits `0` if no FAIL, `2` if any FAIL.

### §3.9 mcp_client_smoke output

`scripts/dev/mcp_client_smoke.py` (Track K artefact,
341 LOC stdlib-only). Output is structured progress
lines per transport per server, terminating in either
`OK (server=<S> transport=<T>)` (exit 0) or `FAIL: …`
(exit 1). Concretely:

```
[stdio] launching python -m <module> --transport stdio
  [<server>/stdio] initialize ...
  [<server>/stdio] tools/list ...
  [<server>/stdio] tools/call name='<tool>' (synthetic empty args) ...
  [<server>/stdio] envelope shape OK
[stdio] shutdown clean

[http] launching python -m <module> --transport http --bind 127.0.0.1:<port> --auth-token-env <VARNAME>
  [<server>/http] initialize ...
  [<server>/http] tools/list ...
  [<server>/http] tools/call ...
  [<server>/http] envelope shape OK
[http] missing-Authorization probe ...
[http] missing-Authorization probe OK (401 + WWW-Authenticate + -32001)
[http] shutdown clean

OK (server=<server> transport=<transport>)
```

Track K / Step 6 closure explicitly classified the
harness as a **diagnostic file under `scripts/dev/`**,
parallel to `selfcheck.py`, not a runtime capability.
It exercises `initialize` + `tools/list` + read-only
`tools/call` + one HTTP missing-`Authorization` probe.

### §3.10 onec-health and onec-troubleshooting packages

- `packages/onec-health/src/onec_health/__init__.py:1-19`
  exports: `HealthCheckResult`, `check_dump_path_exists`,
  `check_http_gateway_available`,
  `check_search_index_available`,
  `check_environment_health`, `summarize_health`.
- `packages/onec-troubleshooting/src/onec_troubleshooting/`
  exports: `diagnose_from_health`, `TroubleshootingReport`.
- These packages are exercised in
  `selfcheck.py:22-29, 44-65` to produce the
  `health_summary_*` and `diagnosis_example` lines.
- `health_summary` is exposed as a registered tool on
  `mcp-read-server` (visible in the selfcheck output's
  `read_server_tools` list). It is **not** an HTTP
  endpoint, **not** exposed under `/healthz` (the
  platform deliberately does not ship `/healthz`, per
  Track J / §6 of `deployment-boundary.md`).

### §3.11 Existing operator-doc observability mentions

#### §3.11.1 `docs/operators/service/service-supervision.md` — Track L

Track L has the **most observability-adjacent content
in the repo today** because systemd inherently wraps
stderr → journald. Section titles relevant to Track N:

- §8 Status (`service-supervision.md:360-413`).
- §8.3 Process-level inspection.
- §8.4 What status does **not** promise.
- §9 Logs (lines 415-470) — the central anchor.
  - §9.1 Follow logs live: `journalctl -u
    <UNIT_NAME>.service -f`.
  - §9.2 Read recent logs: `journalctl --since`.
  - §9.3 Filter by priority: `journalctl -p err`.
    Notable verbatim quote at lines 445-449: **"The
    MCP runtime logs `WARNING` / `ERROR` for credential
    / auth / config issues; `INFO` for startup /
    shutdown events; `DEBUG` for transport-level
    detail when `--log-level DEBUG` is in
    `ExecStart=`."**
  - §9.4 Log persistence and rotation (out-of-scope
    note pointing at `systemd-journald(8)`).
  - §9.5 What logs do **not** include (verbatim at
    lines 460-469): **"No full observability stack
    integration. Track L does not integrate
    OpenTelemetry / Jaeger / Prometheus / log
    aggregation forwarders. See §13."** plus **"No
    structured JSON-line format. The runtime logs
    prose via `logging.basicConfig`. A future track
    may add structured logging; Track L does not."**

Track L / §9 is therefore **already a partial signal-
vocabulary statement** for the systemd-supervised
path. It pins (a) the level-to-event mapping
(`WARNING/ERROR` for cred/auth/config, `INFO` for
startup/shutdown, `DEBUG` for transport detail), (b)
the journald-as-supported-observation-surface stance,
and (c) the "future track may add structured logging"
clause. Track N's recipe can build on §9 rather than
inventing a parallel vocabulary.

#### §3.11.2 `docs/operators/deployment-boundary.md` — Track J

Track J's relevant content:

- §6 `/healthz` non-shipping (lines 354-382). Verbatim
  at line 379-382: **"This document does **not**
  promise a future `/healthz` endpoint. That is not a
  Track J commitment, and the project may never ship
  one."** Section explains workarounds: probe any non-
  `/mcp` URL for deterministic 404 (no auth required),
  or have the reverse proxy synthesise 2xx for strict
  health probers.
- §10 honest non-goals (line 666 onward): **"No
  observability stack (OpenTelemetry, Jaeger,
  Prometheus, OpenMetrics, log aggregation,
  distributed tracing). Diagnostic logs go to
  stderr; whatever your platform does with stderr is
  up to you."**
- Line 153: **"Not multi-tenant. Not load-balanced.
  Not observed."** (intro-level scope statement).

So Track J's existing position is: no `/healthz`, no
observability stack, stderr is the boundary. Track N
does not contradict this; it formalises what "stderr is
the boundary" actually means in operator-actionable
terms.

#### §3.11.3 `docs/operators/packaging/distribution-boundary.md` — Track M

No primary observability content. Two incidental hits
on `monitor` / `observation` vocabulary — neither is
load-bearing for Track N.

#### §3.11.4 systemd unit template `mcp-server.service`

`docs/operators/service/mcp-server.service`:

- `KillSignal=SIGINT` + `KillMode=mixed` +
  `TimeoutStopSec=15s` — graceful-shutdown
  configuration that routes `systemctl stop` into the
  existing `KeyboardInterrupt` clean-exit path.
- `Documentation=file://<REPO_ROOT>/docs/operators/service/service-supervision.md`
  — operator-discoverable cross-reference.

The unit template itself is silent on log facility
(systemd journald is the implicit default for
`Type=simple`); the `service-supervision.md` §9 prose
documents that fact explicitly.

### §3.12 CI workflow

`.github/workflows/dev-check.yml` (entire file is 25
lines). On `push` and `pull_request`, runs on
`windows-latest`:

1. Checkout (actions/checkout@v4).
2. Set up Python 3.11.
3. `. .\scripts\dev\bootstrap_paths.ps1; python
   .\scripts\dev\selfcheck.py`.

The CI thus exercises **only the selfcheck pre-flight
gate**. It does not start any MCP server, does not run
verify-release.ps1, does not run mcp_client_smoke.py,
does not touch real infobases. The CI signal is binary
"selfcheck PASS / FAIL"; selfcheck's eleven key=value
lines flow to CI logs, which means an operator
debugging a CI failure already has a precedent for
reading those exact eleven lines.

### §3.13 Whole-repo grep on observability vocabulary

Counts at `efb4e5c` (rough, post-Step-1):

- `opentelemetry` / `otel` / `prometheus` / `openmetrics`
  / `grafana` / `tempo` / `loki` / `jaeger` / `siem` /
  `distributed.tracing` — **zero hits** in
  production code; non-zero hits exist only in
  docs/architecture (Track N plan / step-map / prior
  tracks' non-goals lists; all denial-style).
- `/healthz` / `/readyz` / `/livez` — **zero hits** in
  production code; non-zero in `deployment-boundary.md`
  §6 (non-shipping) and in track architecture docs as
  carry-through denials.
- `monitor` / `observ` / `metric` / `tracing` — non-
  zero in docs but always in denial / out-of-scope /
  prose contexts; **zero metric-emitting code**.
- `troubleshoot` / `diagnost` / `health` — non-zero in
  package names (`onec-health`,
  `onec-troubleshooting`), in `health_summary` tool,
  in `service-supervision.md` §9, in
  `selfcheck.py:22-29`. These are the only positive
  observability-vocabulary hits in production code.

---

## §4. Existing reusable surfaces

The audit groups what is **already in the repo and
honestly reusable** for a Track N closure:

### §4.1 Python `logging.basicConfig` as the canonical sink

- One canonical sink in the runtime
  (`_configure_logging` at `_stdio_transport.py:62-68`,
  shared between stdio + HTTP entrypoints via
  `run_main_http` at `_network_transport.py:662`).
- Four declared levels (`DEBUG/INFO/WARNING/ERROR`)
  documented inline at `_stdio_transport.py:53-58`.
- Format string is consistent across both transports:
  `"%(asctime)s %(levelname)s %(name)s: %(message)s"`.

This is the single most reusable observability surface
in the repo today. Track L's `service-supervision.md`
§9.3 already pins level-to-event mapping; Track N can
inherit it.

### §4.2 Three-bucket exit-code convention

`0 / 1 / 2` factually present in code (§3.3 table) but
not yet documented. Reusable directly — Track N's
recipe can promote this de-facto convention into an
operator-facing table without any code change.

### §4.3 Failure-equivalence on HTTP auth (Track H §8.4)

Identical 401 + `WWW-Authenticate: Bearer realm="mcp"` +
JSON-RPC `-32001 / "Unauthorized"` for every auth-failure
mode (`_network_transport.py:496-504, 519-541`). This is
a stable, contract-locked diagnostic surface usable
verbatim in a triage recipe.

### §4.4 Per-request HTTP access logs at `INFO`

`_network_transport.py:314-328` already routes every
HTTP request through `logger.info("http %s - %s", ...)`.
An operator running with `--log-level INFO` already has
per-request access lines without any code change.

### §4.5 onec-health + onec-troubleshooting packages

Already-implemented health and troubleshooting
libraries (`packages/onec-health/`,
`packages/onec-troubleshooting/`). `health_summary` is
exposed as a read-server MCP tool (visible in
selfcheck's `read_server_tools` list). These are
existing library surfaces that a Track N recipe can
reference as "first-class health helpers from inside
the MCP tool surface".

### §4.6 selfcheck + verify-release as named gates

Both produce stable structured-text output (§3.7,
§3.8). Track N can cite each by name and role:
`selfcheck.py` = pre-flight import + registry gate;
`verify-release.ps1` = release-side 8-check gate. No
code change needed to classify them.

### §4.7 mcp_client_smoke.py as named transport-boundary probe

Track K closure already classified this harness as a
diagnostic file. Track N can adopt the classification
without modifying the harness.

### §4.8 Track L §9 prose as partial signal vocabulary

`service-supervision.md` §9.3 already pins the level-
to-event mapping for the systemd-supervised path.
Reusable verbatim as the systemd-side signal
vocabulary in Track N's recipe.

### §4.9 Track J §6 + §10 deployment-side denials

`deployment-boundary.md` §6 (`/healthz` non-shipping)
and §10 (no observability stack) already pin what the
deployment boundary does **not** promise. Track N's
recipe inherits these denials verbatim.

---

## §5. Adjacent but insufficient surfaces

These exist but do not, on their own, close the Step 1
gap:

### §5.1 stderr alone

Without a document that names which lines are first-
class and what each level means in the runtime,
operators reading stderr are reading luck, not
contract. Track L §9.3 partially closes this for the
systemd path; nothing closes it cross-OS.

### §5.2 selfcheck alone

`selfcheck.py` is a **pre-flight gate**: imports +
registry counts + library smoke. It cannot diagnose
"the HTTP listener is bound to the wrong interface" /
"auth token resolves to an empty value" / "the
upstream reverse proxy is forwarding the wrong Host
header" / "the systemd unit is restart-looping". It
runs before the server starts; runtime triage is
outside its scope.

### §5.3 verify-release alone

`verify-release.ps1` is a **release-side gate**: 8
checks on repo layout, working tree, git baseline,
selfcheck, credential hygiene. Same response — it
cannot diagnose runtime operability.

### §5.4 mcp_client_smoke.py alone

The harness is a **transport-boundary smoke**: it
exercises `initialize` + `tools/list` + read-only
`tools/call` + 401 probe against one server
(`mcp-read-server`) on each transport. It cannot
diagnose post-startup failure modes (e.g., reverse-
proxy forwarding errors, env-var resolution mistakes
at runtime, in-flight request timeout patterns). Track
K / Step 6 explicitly framed it as a diagnostic
file, not a triage harness.

### §5.5 service-supervision.md alone

Track L §9 covers the journald-supervised path well.
It does not cover:
- Windows NSSM / Event Viewer (Track L §12.1 is prose-
  only and points outward).
- macOS launchd / Console.app (Track L §12.2 prose-
  only).
- Non-supervised execution (operator running
  `python -m mcp_<server>` manually without systemd /
  NSSM / launchd wrapper).
- Failure-mode triage outside the systemd journal
  (e.g., what to do when `systemctl status` says
  "active (running)" but every client request returns
  401 — the journal helps but is not a triage recipe).

### §5.6 deployment-boundary.md alone

Track J §6 / §10 enumerate denials only. They do not
positively describe the supported diagnostic surface.

### §5.7 install fast-path output alone

`_install_runner.py` prints structured fields +
findings, but this is **install-time** output. It does
not help with **runtime** triage.

### §5.8 ad-hoc lore

Reading the code is currently the only way to know
what each stderr line means, what each exit code
implies, and what each HTTP response code surfaces.
This is reasonable for repo-savvy developers and
hostile to operators who treat the platform as a
deployed binary.

---

## §6. Clearly missing pieces

Items that **do not exist anywhere at `efb4e5c`** and
would have to be created (or deliberately denied as
out-of-scope) for Track N closure:

### §6.1 Cross-OS supported-signal vocabulary

Track L §9.3 pins a level-to-event mapping for
systemd/journald. Nothing similar exists for Windows
(NSSM / Event Viewer) or macOS (launchd / Console.app)
or for non-supervised execution.

### §6.2 Operator-facing triage recipe

No file in the repo enumerates canonical failure modes
end-to-end. Track N / Step 1 plan §6 names this as an
in-scope item (Q2 default = (B) triage story
included).

### §6.3 First-class vs recommended-only classification

No file states which of stderr / exit codes /
`selfcheck.py` / `verify-release.ps1` /
`mcp_client_smoke.py` / HTTP responses are **first-
class supported** diagnostic surfaces vs.
**recommended-only** developer/operator tools.

### §6.4 Authoritative non-goals enumeration

Denials exist scattered across Track J §10, Track L
§9.5 / §13, Track M §13 / §14, Track N plan §7.
Nothing collects them into a single observability-
specific non-goals statement.

### §6.5 Machine-readable health signal

No `/healthz`, no exit-code-as-health table, no
`selfcheck --json` mode, no diagnostic-fingerprint
output. (Track J §6 deferred `/healthz` deliberately;
that defer is preserved through Track N — see Step 1
plan §7 and step-map invariant.)

### §6.6 Log-shape contract

The runtime's existing log shape is `"%(asctime)s
%(levelname)s %(name)s: %(message)s"` per
`_stdio_transport.py:66`. No document pins this as
contract; a future code change could alter it without
violating any current commitment.

### §6.7 Cross-reference index from runtime → recipes

Each operator-facing recipe (Track J / Track L /
Track M) cross-references the others but none
cross-references the runtime's stderr / exit-code
behaviour as a first-class operator signal.

### §6.8 What is not missing

For honesty: a metrics surface, distributed tracing,
alerting/paging/on-call workflows, log-aggregation
forwarder, structured-logging library — are **not
missing** because **they are not in scope**. They are
out-of-scope per Step 1 plan §7 and step-map hard
out-of-scope list.

---

## §7. Directional Q1–Q6 resolutions

Per Step 1 plan §12, these are **defaults / directional
recommendations grounded in repo evidence**, not
decided answers. Step 3 contract locks final answers.

### §7.1 Q1 — what counts as "observability/diagnostics" for closure?

**Step 1 default.** PATH A docs-only.
**Audit-grounded recommendation.** **PATH A docs-
only** holds, with a slightly higher confidence
because of §4.8 (Track L §9 prose already pins
systemd-side signal vocabulary) and §3.13 (zero
runtime evidence of any metrics / tracing / OTel /
Prometheus surface). The honest gap is naming + cross-
OS extension, not signal generation.

**PATH B** considered acceptable fallback **only** if
Step 3 audit reveals strong evidence that
`selfcheck --json` materially closes the §6.5
machine-readable-health-signal gap and does so within
a ≤ 50 LOC stdlib-only addition. Repo evidence is
mixed on this: selfcheck's existing eleven key=value
lines are already easily parseable by any
`while read line` loop; the marginal value of `--json`
is real but small. No urgent driver.

**PATH C** rejected by audit — touching all three MCP
server entrypoints (Step 1 step-map §Step 4 PATH C
default file surface) expands the code surface for
marginal observability gain when the runtime already
has a consistent log format string.

### §7.2 Q2 — primary supported diagnostics surface?

**Step 1 default.** Linux/systemd/journald primary;
cross-OS prose for Windows / macOS / non-supervised.
**Audit-grounded recommendation.** **Confirmed.**
Track L §9 is the existing anchor; Track N's recipe
extends it. Windows (NSSM / Event Viewer) and macOS
(launchd / Console.app) get prose-only sections plus
the non-supervised path (operator running
`python -m mcp_<server>` directly) gets a brief
"what stderr looks like and where it goes" pointer.

Non-systemd hosts read the same `--log-level
INFO|DEBUG` output via whatever their supervisor (or
terminal) routes stderr to; the runtime contract is
identical.

### §7.3 Q3 — likely honest Step 4 path?

**Step 1 default.** PATH A docs-only.
**Audit-grounded recommendation.** **PATH A docs-
only as primary**, with the following honest
caveats:
- Evidence is **strongly** in favour of PATH A. Every
  observability signal Track N needs to formalise
  already exists in some form (logging.basicConfig,
  exit codes, HTTP 401 envelope, selfcheck output,
  smoke harness output, install runner output,
  systemd journal integration, onec-health package).
  What is missing is a **document**, not a signal.
- PATH B remains a non-zero-probability fallback if
  Step 3 contract decides selfcheck `--json` mode is
  the cheapest single artefact that closes §6.5. Repo
  evidence suggests this is operator-preference-
  driven, not gap-driven.
- PATH C remains the lowest-probability option per
  §7.1.

### §7.4 Q4 — what is definitely mandatory for closure?

**Audit-grounded recommendation.** The following are
**mandatory** (in the sense of "without these the
gap is not closed"):

1. **A supported signals list.** Naming which of §3.1
   stderr / §3.3 exit codes / §3.5 HTTP responses /
   §3.7 selfcheck / §3.8 verify-release / §3.9
   mcp_client_smoke are **first-class supported
   diagnostic surfaces** and which are **recommended-
   only**.
2. **An operator triage recipe.** 3–5 canonical
   failure modes end-to-end, citing concrete signals
   (e.g., "the server exited with code `2` immediately
   on startup → consult last stderr line; possible
   causes A/B/C with check commands").
3. **An exit-code-meaning table.** Promoting the de
   facto `0/1/2` convention (§3.3) to documentation.
4. **A log-level-to-event-class mapping.** Either
   inheriting Track L §9.3 verbatim or stating a
   superset.
5. **An authoritative non-goals enumeration.**
   Collecting Track J §10 + Track L §9.5 + Track L
   §13 + Track M §13 denials into one observability-
   focused list.
6. **A `/healthz` non-shipping cross-reference.**
   Pointing operators at Track J §6 rather than
   restating its content.

**Recommended-only** (good to have, not mandatory):
- A `selfcheck --json` mode (only if PATH B / PATH C
  is selected at Step 3).
- A "supported log-shape format string" pin (a
  description without a contract MUST).
- A short "stderr lines you can ignore" / "stderr
  lines that always indicate trouble" pair of
  examples.

### §7.5 Q5 — what is definitely insufficient as closure proof?

The audit explicitly rejects each of the following as
sufficient on its own:

- "There are logs somewhere" — `service-supervision.md`
  §9.1 already cites this in essence; alone it does
  not enumerate signal classes or triage paths.
- `selfcheck.py` alone — pre-flight gate only (§5.2).
- `verify-release.ps1` alone — release-side gate only
  (§5.3).
- `mcp_client_smoke.py` alone — transport-boundary
  smoke only (§5.4).
- `service-supervision.md` §9 alone — covers
  systemd/journald but not Windows / macOS / non-
  supervised (§5.5).
- `deployment-boundary.md` §6 / §10 alone — denials-
  only, no positive surface (§5.6).
- Ad-hoc repo lore — operator-hostile (§5.8).

Closure requires **a single document that integrates
the above signals into a positive operator-facing
contract**, plus the recipe / triage / non-goals
content named in §7.4.

### §7.6 Q6 — does Track N likely require production code at all?

**Step 1 default.** NO-BUMP if PATH A; PATCH only if
honest defect-class diagnostic-surface repair under
PATH B/C.
**Audit-grounded recommendation.** **The gap is
solvable without touching production code.** All §3
surfaces exist; §6 missing pieces are documents and
classifications, not code. Therefore:
- **Probability Track N PATH = A:** high.
- **Probability Track N PATH = B:** low — small
  marginal value of `selfcheck --json` not gap-
  closing.
- **Probability Track N PATH = C:** very low — log-
  shape contract requires touching all three MCP
  server entrypoints for negligible operator gain.

Conclusion: **the gap looks solvable without touching
production code.** Step 3 may still pin PATH B / C
if operator value justifies, but the audit does not
identify a driver.

---

## §8. Step 3 handoff note

Items the Step 3 contract will need to lock based on
this audit (a non-exhaustive list, ≥ 10 items):

1. **Q1 / Q3 final answer** — PATH A docs-only vs.
   PATH B with `selfcheck --json` vs. PATH C log-
   shape contract. Audit recommends PATH A.
2. **Q2 final answer** — Linux/systemd/journald
   primary OS-family for implementation-covered
   prose, with Windows + macOS + non-supervised
   prose-only sections. Audit recommends as-is.
3. **Step 4 file-surface cap.** Default
   expectation: ≤ 3 files under PATH A (one operator
   recipe + at most one accompanying file, if any).
   Step 3 may tighten to exactly 1 file.
4. **Step 4 LOC cap.** Default ≤ 200 LOC stdlib-only.
   Under PATH A this is effectively `0 LOC`; under
   PATH B (selfcheck `--json`) ≤ 50 LOC expected;
   under PATH C ≤ 100 LOC stdlib-only across helper
   + three entrypoint call-sites.
5. **Mandatory recipe sections** — supported signals
   list / triage recipe (3–5 failure modes) / exit-
   code table / log-level-to-event mapping / non-
   goals enumeration / `/healthz` cross-reference
   (audit §7.4 items 1–6).
6. **Recipe path.** Default: `docs/operators/
   observability/` (new directory) + a single
   primary file. Step 3 may relocate to
   `docs/operators/observability.md` (no
   subdirectory) for symmetry with
   `docs/operators/deployment-boundary.md`.
7. **Authoritative non-goals carry-through.**
   Reproduce Track J §10 + Track L §9.5/§13 + Track M
   §13 denial language verbatim or by reference.
8. **Signal vocabulary alignment with Track L §9.3.**
   The level-to-event mapping (`WARNING/ERROR` for
   cred/auth/config, `INFO` for startup/shutdown,
   `DEBUG` for transport detail) is the existing
   anchor; the contract should not invent a parallel
   vocabulary.
9. **Failure-equivalence on HTTP auth carry-through.**
   Track H §8.4 identical-401 discipline must be
   preserved verbatim in the triage recipe; no new
   distinguishing characteristics.
10. **`/healthz` non-shipping carry-through.**
    Track J §6 verbatim or by reference; Track N
    does not change this commitment.
11. **`selfcheck.py` output discipline.** Eleven
    key=value lines (§3.7) — PATH A: byte-identical;
    PATH B: identical default + new optional
    `--json` mode with same field semantics.
12. **`verify-release.ps1` check inventory.** 8 named
    checks (§3.8) — byte-identical; the contract may
    reference but does not modify.
13. **Q6 SemVer outcome.** Default NO-BUMP under
    PATH A; PATCH considered only under PATH B / C
    with honest defect-class framing.
14. **Step 4 forbidden-files list.** Production code
    under `apps/*/src/` and `packages/*/src/` (other
    than `selfcheck.py` if PATH B) byte-identical;
    Track L / Track J / Track M recipes byte-
    identical; `pyproject.toml` byte-identical;
    `mcp_client_smoke.py` byte-identical.

---

## §9. Honest summary

**Gap as it actually stands at `efb4e5c`.** The
platform has consistent stderr emission via
`logging.basicConfig`, a three-bucket exit-code
convention, a stable HTTP failure-response envelope
with auth-failure-equivalence, three named helper
tools (`selfcheck.py`, `verify-release.ps1`,
`mcp_client_smoke.py`), an install-time output shape
with structured findings, two library packages
(`onec-health`, `onec-troubleshooting`), and one
operator recipe (Track L §9) that already pins
level-to-event mapping for the systemd-supervised
path. What is missing is **one document that
integrates the above into a positive operator-facing
contract** — not a metric pipeline, not a tracing
stack, not an alerting platform, not a `/healthz`
endpoint.

**Why one descriptive audit file is sufficient.** The
gap is integration-and-naming, not signal-generation.
Every surface this audit names is already in the
repo. The Step 3 contract will pin which of them are
first-class vs. recommended-only and what the closure
gate is; Step 4 will ship the operator recipe (and,
under PATH B/C, an optional narrow code slice).
Step 2's job is exactly to give Step 3 a credible
evidence base — that is now done.

**Track N likely closure shape.** Highest-probability
trajectory: Step 3 contract pins PATH A docs-only;
Step 4 ships a single operator recipe at
`docs/operators/observability/observability-and-diagnostics.md`
(or analogue path) integrating §3 / §4 / §7 content
into operator-readable form; Step 5 adds narrow
CLASS-1 alignment edits to README + PROJECT-STATUS
and possibly one `docs/release-handoff.md` cross-link;
Step 6 closes Track N with NO-BUMP, fourteen post-
phase parallel tracks (A through N) closed
sequentially.

**Track N likely does not require production code.**
Audit identifies no driver for code change. Step 3
may still pin PATH B (`selfcheck --json`) if operator
preference justifies; under that path the bump
likely lands at PATCH (`0.5.2 → 0.5.3`) mirroring
Track I / Track M precedent. Audit does not see
gap-driven justification for PATH B at this stage;
operator-preference-driven justification remains a
Step 3 decision.

**Out-of-scope reaffirmed.** No full OpenTelemetry,
no Prometheus/Grafana/Tempo/Loki/Jaeger, no
SIEM/SOC, no distributed tracing, no alerting/paging/
on-call, no `/healthz` endpoint, no log-aggregation
forwarder, no structured-logging library dependency,
no new MCP tools, no registry change, no
transport/auth/deployment/service/packaging redesign,
no 1cv8 work, no remote push.

**No premature closure language.** Track N is
**active**, currently at the boundary between
Step 2 (this commit) and Step 3 (next operator
decision). Phrases like "observability solved
forever" / "production-ready observability" / "full
OTel instrumentation" / "Prometheus platform
shipped" / "distributed tracing ready" / "SIEM-
ready" / "enterprise-ready observability" /
"alerting solved" / "all signals covered" appear in
this audit **only as denials**.

**Canonical next step.** Parallel Track N / Step 3 —
normative contract (RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY) locking Q1–Q6 final
answers plus Step 4 file/LOC caps and forbidden-files
list. Opening Step 3 is a separate operator decision;
not auto-opened.
