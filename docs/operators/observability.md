# Observability and Diagnostics — Operator Recipe

> **What this is.** A single operator-facing recipe
> that names which diagnostic signals 1C Agent Platform
> supports today, what each signal means, and how to
> use them when something is wrong.
>
> **What this is not.** A full observability platform.
> Not a metrics pipeline. Not a tracing system. Not an
> alerting rotation. Not a health-endpoint
> implementation. Not a SIEM integration. Not a
> commitment to ship any of those in a future release.
> See §9 for the complete non-goals list.

---

## §1. Purpose / scope

### §1.1 What this recipe covers

This document tells an operator who has installed and
deployed the platform (per the recipes cross-referenced
in §8 / §11):

- Which on-host signals are **first-class supported**
  (you can rely on them; we test them).
- Which signals are **recommended-only** (useful, but
  classified at narrower scope by a prior track).
- Which signals are **out-of-scope** (deliberately not
  shipped by the project at this maturity level).
- A short level-to-event mapping for `--log-level`
  values.
- A table of process exit-code meanings.
- A summary of the HTTP transport's response envelope.
- A triage recipe for three canonical failure modes
  (plus two optional follow-ups).
- The cross-OS posture (Linux/systemd primary;
  Windows / macOS / non-supervised prose-only).
- How this recipe relates to the deployment-boundary,
  service-supervision, and packaging recipes.
- An authoritative non-goals enumeration.
- How an operator can verify each first-class signal
  is readable on their host.

### §1.2 What this recipe does not cover

This recipe is **not** any of:

- A guarantee that every operationally-relevant event
  produces a structured signal. Operators MAY observe
  additional signals (e.g., systemd `MainPID` state,
  reverse-proxy access logs) — the platform names a
  **first-class** subset, not an exhaustive list.
- A guarantee that log-line text strings are stable
  between project versions. The recipe pins **event
  categories** (per §3 level-to-event mapping), not
  literal substrings. Tools that grep on literal
  message text may break on minor version bumps.
- A `/healthz` endpoint or any HTTP health probe. See
  §6 for the carry-forward of that non-shipping
  position from the deployment-boundary recipe.
- A metric pipeline, tracing context, or alert rule.
  See §9 for the full denial list.

### §1.3 Forbidden maturity claims — explicit denials

The platform does **not** claim, and this recipe MUST
NOT be cited as evidence of, any of the following:

- ❌ **"Observability solved forever."** The recipe
  closes one narrow integration gap; future
  operational realities may surface additional
  observability needs that fall outside this
  recipe's scope.
- ❌ **"Production-ready observability."** This
  recipe describes the supported diagnostic surface
  at the current project maturity. It does not
  describe a production-ready observability stack.
- ❌ **"Full OpenTelemetry instrumentation."** No
  OpenTelemetry SDK is bundled. No span emission. No
  trace context propagation. No OTel collector
  configuration.
- ❌ **"Prometheus platform shipped."** No `/metrics`
  endpoint. No exporter. No `prometheus_client`
  dependency.
- ❌ **"Distributed tracing ready."** No
  cross-system request-id propagation. No trace
  assembly. No service map.
- ❌ **"SIEM-ready."** No Splunk forwarder. No
  Elastic ingestion configuration. No SOAR runbook
  scaffolding bundled.
- ❌ **"Enterprise-ready observability."** This
  recipe is operator-scale, not enterprise-platform
  scale.
- ❌ **"Alerting solved."** No alert rules, no
  paging integrations, no on-call workflow shipped.
- ❌ **"All signals covered."** The first-class list
  in §2 is narrow on purpose. Many operationally
  interesting questions ("how many requests/sec
  does this server handle in the last 5 minutes?",
  "what is the p95 tool-call latency?") do not have
  a first-class answer today.

---

## §2. Supported diagnostic surfaces

### §2.1 First-class signals

These signals are **first-class supported**. Operators
can rely on them being present, in the documented
shape, on hosts that follow the supported deployment /
service-supervision recipes.

| # | Signal | What it tells you | Authoritative source |
| - | --- | --- | --- |
| FC1 | **stderr emission via Python `logging`** at `--log-level INFO` (default) | Startup banner; per-request HTTP access lines; shutdown messages; warnings / errors at credential / auth / config layer; unhandled exceptions. | `packages/mcp-common/src/mcp_common/_stdio_transport.py:62-68,181,208-212`, `packages/mcp-common/src/mcp_common/_network_transport.py:314-328,609-615,618-624,701-703` |
| FC2 | **Process exit code (0 / 1 / 2)** | Clean exit vs unhandled exception vs operator-readable startup failure. See §4. | Same files; per-exit-code citations in §4 |
| FC3 | **HTTP response envelope** on the `/mcp` endpoint | Auth-failure 401 + `WWW-Authenticate` + JSON-RPC `-32001`; transport-level errors (400 / 413 / 415) with JSON-RPC `-32xxx` body. See §5. | `packages/mcp-common/src/mcp_common/_network_transport.py:354-541` |
| FC4 | **`scripts/dev/selfcheck.py`** key=value output | Pre-flight gate. Confirms imports succeed and tool registries match expected counts (`read=15 / write=25 / intelligence=16`). | `scripts/dev/selfcheck.py:95-105` |
| FC5 | **`scripts/release/verify-release.ps1`** 8-check summary | Release-side gate. Confirms repo layout / release entrypoints / important docs / working tree / git baseline / selfcheck / credential leak guard / credential template hygiene. | `scripts/release/verify-release.ps1:90-267` |
| FC6 | **`scripts/release/install.ps1`** + **`scripts/release/_install_runner.py`** structured findings | Install-time. Confirms config materialisation; per-finding `[severity] code: detail` lines; exit-code-meaning per `_install_runner.py:80-84`. | `scripts/release/_install_runner.py:57-84` |
| FC7 | **systemd `journalctl -u <UNIT>.service`** on Linux hosts deployed via the service-supervision recipe | Captured stdout / stderr persisted by the journal; filterable by priority and time window. | `docs/operators/service/service-supervision.md` §9 |

If any of FC1–FC7 is missing from your operator
environment, your deployment has drifted from a
supported recipe. The fix is to re-align with the
deployment-boundary / service-supervision / packaging
recipes (see §8); not to invent a substitute signal.

### §2.2 Recommended-only signals

These signals are **useful and present**, but are
classified at narrower scope by an earlier track or
exist as developer/operator tooling rather than
runtime capabilities. Use them when relevant; do not
rely on them as the sole basis for an operational
decision.

| # | Signal | Status | Notes |
| - | --- | --- | --- |
| R1 | **`scripts/dev/mcp_client_smoke.py`** transport-boundary smoke | Developer/operator diagnostic file under `scripts/dev/`. | Track K classified the harness as parallel to `selfcheck.py`, **not** a runtime capability. It exercises `initialize` + `tools/list` + a synthetic read-only `tools/call` + one HTTP missing-`Authorization` probe; it does not exercise post-startup runtime failure modes. |
| R2 | **`--log-level DEBUG`** transport-detail traces | Operationally noisy; not recommended for steady-state operation. | Use only when you have a specific question that `INFO`-level cannot answer. Restart with `INFO` once the question is resolved. |
| R3 | **`health_summary` MCP tool** on `mcp-read-server` | Callable via any MCP client. | Returns a structured summary of `onec-health` library checks. This is **not** an HTTP health endpoint. Calling it is the operator's choice. |
| R4 | **Per-request HTTP access lines at `INFO`** (`_network_transport.py:314-328`) | Already present; useful for traffic awareness. | Not a triage primitive — use FC1 + FC3 for actual failure diagnosis. |

### §2.3 Out-of-scope signals (carry-forward denials)

The following are deliberately **not shipped**.
Operators who require them must source them externally
or wait for a future, separately-justified track.

- No OpenTelemetry program (no SDK dependency, no
  collector configuration, no span emission, no
  `traceparent` propagation).
- No Prometheus / OpenMetrics surface (no
  `/metrics` endpoint, no exporter, no
  `prometheus_client` dependency).
- No Grafana / Tempo / Loki / Jaeger / Mimir /
  Cortex / VictoriaMetrics platform bundled.
- No SIEM / SOC integration.
- No distributed tracing.
- No alerting / paging / on-call workflow.
- No `/healthz` / `/readyz` / `/livez` HTTP endpoint
  (§6 carry-forward).
- No log-aggregation forwarder
  (`vector` / `fluentd` / `fluent-bit` / `rsyslog` /
  `journal-remote`) bundled.
- No structured-logging library dependency
  (`structlog` / `loguru` / `python-json-logger`).
- No web UI / dashboard frontend.

This list is reiterated at §9 with the same
authoritative anchors. It is repeated here so
operators reading the surface inventory understand at
the same place what is shipped and what is not.

---

## §3. Log levels and what each one means

### §3.1 Inherited mapping (from service-supervision §9.3)

The service-supervision recipe pins the level-to-event
mapping for the systemd-supervised path. This recipe
inherits that mapping verbatim and extends it to all
supported deployment shapes (systemd / NSSM / launchd /
non-supervised):

> "The MCP runtime logs `WARNING` / `ERROR` for
> credential / auth / config issues; `INFO` for
> startup / shutdown events; `DEBUG` for transport-
> level detail when `--log-level DEBUG` is in
> `ExecStart=`."
>
> — `docs/operators/service/service-supervision.md` §9.3

### §3.2 Operator-readable level table

| Level | Event categories | Default? | Notes |
| --- | --- | --- | --- |
| **DEBUG** | Per-request transport details; JSON-RPC envelope traces; initialisation step-by-step. | No | Operationally noisy. Use ad-hoc for a specific question; revert to `INFO` once resolved. See R2 in §2.2. |
| **INFO** | Startup banners ("Starting `<server>` stdio transport (JSON-RPC 2.0)." / "Starting `<server>` HTTP transport (JSON-RPC 2.0) on `<host>`:`<port>` with N valid token(s)."); shutdown messages ("Interrupted (KeyboardInterrupt); …"); per-request HTTP access lines; successful config-load events. | **Yes** (default for `--log-level`). | Recommended for steady-state operation on systemd / NSSM / launchd. |
| **WARNING** | Recoverable issues; resolved-but-suspicious config; degraded paths. | No | Less common; signals an unusual state worth checking. |
| **ERROR** | Failure-equivalent: unresolved env-var for `--auth-token-env`; bind failure (`_network_transport.py:603-605`); unhandled exception at the entrypoint boundary (`logger.exception("Fatal error in <server> entrypoint", ...)`); HTTP request handler exceptions. | No | If you see `ERROR` lines, something needs attention. |

### §3.3 Log-line shape

The runtime emits log lines in this format
(`_stdio_transport.py:62-68` and inherited by the HTTP
transport via `_network_transport.py:662`):

```
%(asctime)s %(levelname)s %(name)s: %(message)s
```

This format **may change between project versions** as
the project evolves. Do not parse against literal
substrings. Parse against the **level field** and the
**event category** (per §3.2) instead. Tools that grep
on literal message text are not supported.

### §3.4 No structured JSON-line format

The runtime logs prose via `logging.basicConfig`. A
future track **may** add structured logging; this
recipe does **not**. (See service-supervision §9.5
for the original anchor; this recipe carries it
forward.)

---

## §4. Process exit codes — operator-readable meanings

### §4.1 Exit-code table

| Code | Meaning | Where it originates | What to do |
| ---- | --- | --- | --- |
| **0** | Clean exit. Operator-initiated stop (Ctrl-C / SIGINT on a foreground process; `systemctl stop` on a supervised unit); EOF on stdin for the stdio transport. | `_stdio_transport.py:208-212`, `_network_transport.py:618-624` | Nothing — the server stopped on purpose. |
| **1** | Unhandled exception caught at the entrypoint boundary. A full Python traceback is logged via `logger.exception("Fatal error in <server> entrypoint", ...)` immediately before exit. | `_stdio_transport.py:242-244`, `_network_transport.py:701-703`, `_network_transport.py:682-683` | Read the traceback in stderr / journal. If the cause is operator-side (e.g., missing PYTHONPATH entry), fix and retry; if it is a defect, file with the traceback attached. |
| **2** | Startup-time operator-readable failure. A single-line message on stderr (no traceback) precedes exit. Common causes: bad `--config-path`; missing `--bind` when `--transport http`; unresolved `--auth-token-env` env var; port-in-use bind failure. | `_network_transport.py:165-170` (`_fail()`), `_network_transport.py:603-605` (bind), `_network_transport.py:686-687` (`--bind` gate); argparse defaults for unknown flags. | Read the **last line** on stderr. The line is operator-readable by construction — no Python traceback. Match against the cause; fix the offending CLI flag / env var / port / config-path. |

### §4.2 Exit codes are stable; semantics are not extended

The three-bucket convention (0 / 1 / 2) is documented
here for the first time but has been the de-facto
behaviour since the transport modules existed. Track N
does not extend the table — there are no exit codes
3+ shipped by the runtime as of this writing. If you
observe an unexpected non-zero exit code, treat it as
a defect-class condition and surface it; do not
invent a new bucket meaning.

---

## §5. HTTP transport — response envelope

This section summarises the HTTP `/mcp` endpoint
behaviour from `_network_transport.py:354-541` for
quick triage reference. It is **not** a redefinition
of any prior contract; the deployment-boundary recipe
and the Track H transport contract remain
authoritative.

### §5.1 Auth-failure envelope (failure-equivalence)

All authorisation-failure modes — missing
`Authorization` header, empty value, wrong scheme
(non-`Bearer`), token that does not match a configured
token — produce **identical** responses by design:

- HTTP status: `401 Unauthorized`.
- `WWW-Authenticate: Bearer realm="mcp"`.
- Content-Type: `application/json`.
- Body: JSON-RPC error envelope with
  `code = -32001` and `message = "Unauthorized"`.

This is the Track H §8.4 failure-equivalence
discipline. It is intentional and exists to prevent
information-leakage about which specific aspect of
authentication failed.

For triage, see T2 in §7.

### §5.2 Other failure envelopes

| Condition | HTTP Status | Headers | JSON-RPC | Source |
| --- | --- | --- | --- | --- |
| Multiple `Authorization` headers | 400 | — | `-32600 / "Invalid Request"` | `_network_transport.py:364-373` |
| Body > 1 MiB | 413 | — | `-32600 / "Invalid Request"` | `_network_transport.py:392-399` |
| Content-Type not `application/json` | 415 | — | `-32600 / "Invalid Request"` | `_network_transport.py:354-363` |
| Body is not valid JSON | 400 | — | `-32700 / "Parse error"` | `_network_transport.py:405-412` |
| Body is JSON but not a valid JSON-RPC 2.0 envelope | 400 | — | `-32600 / "Invalid Request"` | `_network_transport.py:423-432` |

The deployment-boundary recipe §6 explains that a
probe directed at any **non-`/mcp` URL** returns
`404 Not Found` with body `Not Found\n` and **does not
require auth**. That behaviour is the supported answer
to "I need a TCP-connectable + HTTP-known-status load
balancer probe"; see §6 below.

---

## §6. `/healthz` non-shipping — carry-forward

The platform **does not** ship a `/healthz`,
`/readyz`, or `/livez` HTTP endpoint. This is not a
Track N decision; it is a Track J decision that Track
N carries forward unchanged.

> "This document does **not** promise a future
> `/healthz` endpoint. That is not a Track J
> commitment, and the project may never ship one.
> Plan around the current behaviour, not around an
> aspirational endpoint."
>
> — `docs/operators/deployment-boundary.md` §6

For an operator who needs a TCP-connectable health
probe **today**, the deployment-boundary recipe §6
gives two workable patterns:

1. **Point your probe at any non-`/mcp` URL.** The
   listener returns deterministic
   `404 Not Found` (`text/plain; charset=utf-8`,
   body `"Not Found\n"`) without requiring
   authentication. Configure the probe to treat 404
   as alive.
2. **Have the reverse proxy synthesise a 2xx.**
   nginx: `location /healthz { return 200; }`.
   Caddy / Apache equivalents are similarly short.

Track N does not extend or contradict either pattern.
Neither does it imply that a `/healthz` endpoint will
ship in a future release.

For first-class **process-state** signals (the
question a `/healthz` probe is actually trying to
answer for a supervised process), use FC2 (exit codes)
+ FC7 (`systemctl status` + `journalctl -u`) instead.

---

## §7. Triage recipe

Three canonical failure modes are covered end-to-end.
Two optional follow-ups are sketched briefly. The
triage recipe MUST NOT be read as exhaustive — for
failure modes outside this list, surface as a defect
or open a future operator-facing recipe.

### §7.1 T1 — The server exited with code 2 immediately on startup

**What you see first.**

- Process exited within a fraction of a second of
  start.
- Exit code = `2` (read via `$LASTEXITCODE` in
  PowerShell; `echo $?` in bash; **MainPID** in
  `systemctl status <UNIT>` shows the failed exit
  status as `code=exited, status=2/INVALIDARGUMENT`
  or similar).
- A **single line** appears on stderr (no Python
  traceback). The line is operator-readable by
  construction (per `_fail()` at
  `_network_transport.py:165-170`).

**Where to look next.**

- The last line on stderr. On systemd:
  `journalctl -u <UNIT>.service -n 20`. On a
  foreground run: the terminal scrollback.
- The CLI flags actually passed (compare to
  `ExecStart=` on the systemd unit; or to the
  scripted invocation on Windows / macOS).
- The environment variables resolved at start
  (verify the `EnvironmentFile=` referenced by the
  unit; on a foreground run, your shell's `env`).

**Match against the most common causes.**

| Last-stderr-line pattern | Cause | Fix |
| --- | --- | --- |
| `bad --config-path` / `cannot read product config from <path>` | Configured config-path does not exist or is unreadable. | Confirm the path on disk; confirm the supervisor user can read it (`ls -l` on Linux; ACLs on Windows). |
| `--transport http requires --bind HOST:PORT` | HTTP transport requested without a `--bind` value. | Add `--bind <HOST>:<PORT>` to the invocation (`_network_transport.py:686-687`). |
| `--auth-token-env <VAR> not set in environment` or `auth.tokens has 0 valid entries after env-substitution` | The bearer-token env var is unset, empty, or resolves to an empty value at startup. | Confirm the env var is set in the supervisor's environment (`EnvironmentFile=` for systemd; service envblock on NSSM; `EnvironmentVariables` on launchd). See the service-supervision recipe §10. |
| `Failed to bind <host>:<port>: …` | Port already in use, or operator lacks bind privilege on a privileged port. | `ss -ltn \| grep <port>` on Linux to find the holder; switch the platform to a free non-privileged port if appropriate. |

**Authoritative helper surface.**

- FC7 (`journalctl -u <UNIT>`) on Linux/systemd.
- FC1 (stderr) on any host.

**What T1 does NOT prove.**

- T1 does not confirm that the server's HTTP
  transport, once it does come up, will accept your
  client. For that, see T2.
- T1 does not confirm correctness of routing through
  any reverse proxy or load balancer. For that, see
  the deployment-boundary recipe (§8).

### §7.2 T2 — The HTTP transport returns 401 to every request

**What you see first.**

- Every authenticated request to `/mcp` produces
  `HTTP 401`, `WWW-Authenticate: Bearer
  realm="mcp"`, body
  `{"jsonrpc":"2.0","id":null,"error":{"code":-32001,"message":"Unauthorized"}}`.
- Per §5.1 failure-equivalence, the 401 is the same
  for every auth-failure mode — you cannot
  distinguish missing-header from wrong-scheme from
  wrong-token by inspecting the response alone.

**Where to look next.**

This is the deliberate path: cannot triage from the
response side; must triage from the server-side and
the client-side independently.

1. **Server-side: confirm a token is configured.**
   On startup, FC1 / FC7 contain the line:

   ```
   <name> HTTP transport (JSON-RPC 2.0) on <host>:<port> with N valid token(s).
   ```

   If `N = 0`, the server has no usable token. Check:
   - The `ProductConfig.auth.tokens` map (the file
     pointed at by `--config-path`, after
     `${ENV:NAME}` substitution). See the install
     fast-path artefact (FC6) for the materialised
     config.
   - The `--auth-token-env <VARNAME>` CLI flag, and
     the env-var it points at. The env-var MUST be
     set **and non-empty** in the supervisor's
     environment.

2. **Client-side: confirm the request actually
   carries a Bearer header.**
   - Header name: `Authorization`. **Exactly one**
     such header (multiple `Authorization` headers
     produce a different response — `400` with
     JSON-RPC `-32600`, see §5.2).
   - Header value: `Bearer <token>` (scheme name is
     case-insensitive; the token bytes are
     compared constant-time via
     `hmac.compare_digest`).
3. **Compare bytes.** The configured token and the
   presented token must be byte-for-byte equal. A
   trailing newline or surrounding whitespace in
   either source is a frequent cause.

**Authoritative helper surface.**

- FC3 (HTTP response envelope) — for confirming
  failure-equivalence behaviour.
- FC1 / FC7 — for the startup banner's `N valid
  token(s)` count.
- R1 (`scripts/dev/mcp_client_smoke.py`) — the
  smoke harness's missing-`Authorization` probe
  exercises exactly the 401 / `WWW-Authenticate`
  pair, providing a known-good baseline to compare
  against your own client request.

**What T2 does NOT prove.**

- T2 does not prove the transport's routing through a
  reverse proxy is correct. A reverse proxy may
  strip the `Authorization` header if misconfigured;
  the deployment-boundary recipe §7 covers
  `Forwarded-*` / `X-Forwarded-*` MUST-NOT-consume
  policy and reverse-proxy header forwarding.
- T2 is not a defect in the platform's 401 logic if
  N = 0 valid tokens is what the operator
  configured. That is correct behaviour by design;
  fix the configuration, not the runtime.

### §7.3 T3 — `selfcheck.py` failed

**What you see first.**

- `python scripts/dev/selfcheck.py` exits non-zero.
- No `selfcheck_status = ok` line printed on
  stdout.
- A Python traceback appears on stderr (the
  script's docstring explicitly states: "**No
  try/except: if anything is wired incorrectly, we
  want a loud, honest failure.**").

**Where to look next.**

1. **Read the traceback's last frame.** It names
   the import or attribute that failed.
2. **Check PYTHONPATH.** `selfcheck.py` is
   designed to be run after sourcing
   `scripts/dev/bootstrap_paths.ps1` (or
   equivalent). If you ran it without first
   bootstrapping the path, the `ModuleNotFoundError`
   names the package you need on PYTHONPATH.
3. **Check installed `1c-agent-platform` wheel.**
   If you installed via `pip install
   <WHEEL_PATH>` (Track M packaging recipe), the
   wheel installs every package referenced by
   `selfcheck.py`. A `ModuleNotFoundError` after a
   successful `pip install` is a defect signal —
   surface it with the traceback attached.
4. **Check the tool-registry counts** in the
   output (if the script got past imports and
   failed at registry assertions). The counts are
   `read=15 / write=25 / intelligence=16`; any
   other value is a defect-class condition.

**Authoritative helper surface.**

- FC4 (`selfcheck.py` output). The 11 key=value
  lines on `stdout`; Python traceback on `stderr`.

**What T3 does NOT prove.**

- `selfcheck.py` is a **pre-flight gate**: imports
  succeed; library smoke succeeds; registry counts
  match. A `selfcheck.py` PASS does **not** prove
  that the runtime will start, that any transport
  will bind, that auth tokens are usable, or that
  any 1С infobase is reachable. Conversely, a
  `selfcheck.py` FAIL does not necessarily indicate
  a runtime issue — only an import / registry-
  integrity issue. T1 / T2 still apply to runtime
  triage.

### §7.4 T4 (optional) — `mcp_client_smoke.py` reports a transport failure

`scripts/dev/mcp_client_smoke.py` is classified as a
diagnostic file (R1 in §2.2). It exercises
`initialize` → `tools/list` → a read-only
`tools/call` round-trip plus one HTTP missing-
`Authorization` probe on both transports against
`mcp-read-server`.

A FAIL line from the harness will name the failing
step and transport:

```
FAIL: <server>/<transport> <step>: <reason>
```

Match the step against the recipe:

- `<step> = initialize` → the server probably did not
  start (T1).
- `<step> = tools/list` → server is up but the
  registry surface is misbehaving (T3 territory).
- `<step> = tools/call` → server is up and listing
  tools but a synthetic empty-args call failed.
  Investigate the specific tool referenced in the
  reason.
- `<step> = missing-Authorization probe` → the HTTP
  transport is not returning the documented 401
  envelope. Either the auth wiring is broken (T2),
  or a reverse-proxy is rewriting the response
  before it reaches the harness.

### §7.5 T5 (optional) — systemd unit restart-looping

The service-supervision recipe pins
`Restart=on-failure` and a default `StartLimit`
window. If your unit restart-loops, the unit will
eventually enter the `failed` state and stop
restarting.

```sh
systemctl status <UNIT_NAME>.service
journalctl -u <UNIT_NAME>.service --since "10 minutes ago"
```

The journal will contain N copies of the relevant
startup-failure stderr line (per T1 patterns) plus
the systemd `Failed to start` / `Start request
repeated too quickly` annotations. Fix the
underlying T1 cause; do not raise the restart
threshold to mask it.

See service-supervision recipe §7 for the restart
behaviour contract.

---

## §8. Relationship to existing recipes

This recipe is **orthogonal-and-complementary** to
the three established operator recipes. It does not
duplicate their content; it integrates the
diagnostic-surface view across them.

### §8.1 Deployment-boundary recipe — `docs/operators/deployment-boundary.md`

Authoritative for: TLS / reverse-proxy posture, three
deployment scenarios (loopback / private subnet /
public-facing-through-reverse-proxy), Forwarded-header
MUST-NOT-consume policy, `/healthz` non-shipping
(§6), deployment-side observability denials (§10).

Cross-references:

- §6 of deployment-boundary is the authoritative
  source for the `/healthz` non-shipping carry-
  forward; this recipe §6 quotes and points to it.
- §10 of deployment-boundary's denial list is one
  of the three anchors aggregated in §9 of this
  recipe.

### §8.2 Service-supervision recipe — `docs/operators/service/service-supervision.md`

Authoritative for: cross-OS supervisor wiring
(Type=simple systemd unit + NSSM / launchd prose),
lifecycle verbs (`start` / `stop` / `restart` /
`status` / `logs`), log-level-to-event mapping for
the systemd path (§9.3), log persistence + rotation
guidance, "no full observability stack" denial
(§9.5), and the service-supervision-specific
honest-non-goals (§13).

Cross-references:

- §9.3 of service-supervision is the **inheritance
  anchor** for the level-to-event mapping. This
  recipe §3.1 quotes it verbatim.
- §9.5 ("No full observability stack integration")
  is one of the three anchors aggregated in §9 of
  this recipe.
- The systemd unit template at
  `docs/operators/service/mcp-server.service`
  routes `systemctl stop` → `KillSignal=SIGINT` →
  the existing `KeyboardInterrupt` clean-exit path
  (FC2 exit code 0).

### §8.3 Packaging recipe — `docs/operators/packaging/distribution-boundary.md`

Authoritative for: build / install / uninstall /
upgrade / verify lifecycle verbs over a single
buildable pure-Python wheel; the 11-package wheel
contents; cross-OS wheel install posture.

Cross-references:

- The §13 honest non-goals list of packaging
  contributes to this recipe's §9 aggregate.
- Install-time **diagnostics live** in the recipe-
  documented install-fast-path output (FC6); this
  recipe references that output rather than
  duplicating it.

### §8.4 `scripts/dev/selfcheck.py`

The selfcheck script is the pre-flight gate. This
recipe references it at FC4, T3, and §10.

### §8.5 `scripts/release/verify-release.ps1`

The verify-release gate is the release-side
8-check gate. This recipe references it at FC5 and
§10. The Selfcheck check inside verify-release is
the same FC4 surface, run from a release-validation
context.

### §8.6 `scripts/dev/mcp_client_smoke.py`

The smoke harness is the transport-boundary smoke
(Track K). This recipe references it at R1 and
T4. The harness's `OK (server=<server>
transport=<transport>)` final line is the canonical
PASS signal; any `FAIL: …` line is the canonical
FAIL signal.

### §8.7 `scripts/release/install.ps1` and the install fast-path

The install fast-path is the operator-facing
config-materialiser. This recipe references it at
FC6 and T2 (where the materialised
`ProductConfig.auth.tokens` is the on-disk source of
truth for "which tokens does this server actually
accept").

---

## §9. Authoritative non-goals

This recipe does **not** provide, ship, or promise to
ship any of the following. The denials below
aggregate Track J `deployment-boundary.md` §10,
Track L `service-supervision.md` §9.5 / §13, and
Track M `distribution-boundary.md` §13 into one
observability-specific list.

### §9.1 Observability platform — not shipped

- No OpenTelemetry SDK dependency.
- No OTel collector configuration.
- No `traceparent` / `tracestate` header propagation.
- No span emission contract.
- No trace ID propagation contract.

### §9.2 Metrics platform — not shipped

- No `/metrics` HTTP endpoint.
- No `prometheus_client` (or any metrics library)
  dependency.
- No counter / gauge / histogram / summary metric.
- No StatsD / DogStatsD socket emitter.

### §9.3 Dashboards — not shipped

- No Grafana dashboard JSON.
- No Tempo / Loki / Jaeger / Mimir / Cortex /
  VictoriaMetrics datasource configuration.
- No Kibana visualisation.
- No custom in-repo dashboard frontend.
- No web UI of any kind.

### §9.4 Alerting / paging / on-call — not shipped

- No PagerDuty integration.
- No Opsgenie integration.
- No Slack webhook / email alert configuration.
- No alerting threshold or rule.
- No on-call rotation scaffolding.

### §9.5 Log-aggregation / SIEM — not shipped

- No `vector` / `fluentd` / `fluent-bit` / `rsyslog`
  / `journal-remote` configuration bundled.
- No Splunk forwarder.
- No Elastic ingestion configuration.
- No SOAR runbook scaffolding.
- No SIEM normalisation pipeline.

### §9.6 Health endpoints — not shipped

- No `/healthz`, `/readyz`, `/livez` HTTP endpoint
  (per §6 carry-forward from
  `docs/operators/deployment-boundary.md` §6).
- No `--healthcheck` CLI subcommand.
- The existing `health_summary` MCP tool on
  `mcp-read-server` is accessible **via MCP only**;
  it is not an HTTP endpoint.

### §9.7 Logging-library / format — not shipped

- No `structlog` / `loguru` / `python-json-logger`
  dependency.
- No structured-JSON-line log format.
- No log-field schema or canonical key set.
- No log rotation / persistence policy beyond what
  the OS log facility provides.

### §9.8 Forbidden maturity claims (recap)

This recipe MUST NOT be cited as evidence of any of
the following — see §1.3 for the explicit denials:

- "Observability solved forever."
- "Production-ready observability."
- "Full OpenTelemetry instrumentation."
- "Prometheus platform shipped."
- "Distributed tracing ready."
- "SIEM-ready."
- "Enterprise-ready observability."
- "Alerting solved."
- "All signals covered."

### §9.9 Other carry-over non-goals

- No transport / auth / deployment / service /
  packaging redesign (Tracks G / H / I / J / L / M
  carry-forward unchanged).
- No new MCP tools (registry invariant
  `read=15 / write=25 / intelligence=16` preserved).
- No new CLI flag on existing servers (Tracks G / H
  flag surface locked).
- No new `[project.scripts]` console entries.
- No new project dependencies.
- No new entrypoint module.
- No `1cv8.exe` integration changes.
- No rollback / AST / multi-version 1С matrix
  expansion.

---

## §10. Cross-OS posture

### §10.1 Linux + systemd + journald — primary (implementation-covered)

If you have followed the service-supervision recipe
to install systemd units, you have all of FC1 / FC2 /
FC3 / FC4 / FC5 / FC6 / FC7 available end-to-end.
Use:

```sh
systemctl status <UNIT_NAME>.service
journalctl -u <UNIT_NAME>.service -f         # live tail
journalctl -u <UNIT_NAME>.service --since "1 hour ago"
journalctl -u <UNIT_NAME>.service -p err     # ERROR+ only
```

The service-supervision recipe §9 is authoritative
for the systemd-supervised observation surface;
Track N's recipe does not duplicate its detail.

### §10.2 Windows — prose-only

On Windows, the supported supervisor pattern is NSSM
(see service-supervision §12.1). FC1 / FC2 / FC3 /
FC4 / FC5 / FC6 are all available; FC7 is replaced
by NSSM's redirected `stdout` / `stderr` log files
or the Windows Event Viewer Application log, per
NSSM configuration.

This recipe **does not** test or maintain a Windows-
specific observation procedure beyond pointing at
NSSM's documented behaviour. Track N does not claim
implementation-covered parity with the
Linux/systemd path.

### §10.3 macOS — prose-only

On macOS, the supported supervisor pattern is
launchd (see service-supervision §12.2). FC1 /
FC2 / FC3 / FC4 / FC5 / FC6 are all available; FC7
is replaced by launchd's redirected `StandardOutPath`
/ `StandardErrorPath` and/or `Console.app` System
Reports.

This recipe **does not** test or maintain a macOS-
specific observation procedure beyond pointing at
launchd's documented behaviour. Track N does not
claim implementation-covered parity with the
Linux/systemd path.

### §10.4 Non-supervised execution — prose-only

If you are running the platform directly from a
terminal via `python -m mcp_<server> --transport
<...>` (without systemd / NSSM / launchd), then:

- FC1 (stderr) lands on the terminal. There is no
  built-in rotation or persistence — that is the
  shell's / terminal's responsibility.
- FC2 (exit code) is readable via `$?` / `$LASTEXITCODE`.
- FC3 (HTTP envelope) works identically.
- FC4 / FC5 / FC6 are all callable manually.
- FC7 is not applicable (no journal / Event Viewer
  / Console.app coupling unless you redirect
  stderr yourself).

Non-supervised execution is acceptable for
development and for short-running operator tasks; it
is **not** a recommended steady-state production
posture. Use the service-supervision recipe instead.

---

## §11. Operator-side verification — how to confirm each first-class signal works

This section gives short, copy-pasteable steps to
prove that each first-class signal is readable on
your host. Run these once at deployment time, then
again whenever you change supervisor / proxy / host
configuration.

### §11.1 FC1 (stderr) and FC2 (exit code)

Foreground sanity-check (any OS):

```pwsh
# Windows PowerShell
python -m mcp_read_server --transport stdio --log-level INFO
# Stop with Ctrl-C. Expected: clean shutdown, exit code 0.
$LASTEXITCODE   # → 0
```

```sh
# Linux / macOS
python -m mcp_read_server --transport stdio --log-level INFO
# Stop with Ctrl-C. Expected: clean shutdown.
echo $?         # → 0
```

You should see the startup-banner INFO line (per
§3.2) and, on shutdown, the
"Interrupted (KeyboardInterrupt); exiting cleanly."
line.

### §11.2 FC3 (HTTP envelope) — auth-failure shape

With a configured HTTP transport (per the
deployment-boundary recipe), the missing-auth probe
is one curl:

```sh
curl -i -X POST http://<HOST>:<PORT>/mcp \
     -H 'Content-Type: application/json' \
     --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

Expected: `HTTP/1.1 401 Unauthorized`,
`WWW-Authenticate: Bearer realm="mcp"`,
JSON-RPC body with `code = -32001` /
`message = "Unauthorized"`. (See §5.1.)

### §11.3 FC4 (`selfcheck.py`)

```pwsh
. .\scripts\dev\bootstrap_paths.ps1
python .\scripts\dev\selfcheck.py
```

Expected: `selfcheck_status = ok` as the last line
on stdout; exit code 0.

### §11.4 FC5 (`verify-release.ps1`)

```pwsh
.\scripts\release\verify-release.ps1
```

Expected: `Release verify: GREEN (all checks passed
or skipped)`; exit code 0. Eight `[PASS]` (or some
`[SKIP]` / `[WARN]`) check lines in the summary.

### §11.5 FC6 (install fast-path)

```pwsh
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json
```

(Preview mode by default; add `-Confirm` to actually
write.) Expected: structured `ok / mode /
product_name / …` block, optionally followed by
`confirmed findings` / `presumed findings` /
`recommended actions`. Exit code 0 in normal
preview / executed paths.

### §11.6 FC7 (`journalctl -u`)

On a systemd host with installed units:

```sh
journalctl -u <UNIT_NAME>.service -n 50 --no-pager
```

Expected: the startup-banner INFO line plus
subsequent INFO / DEBUG / WARNING / ERROR lines per
§3.

### §11.7 R1 (`mcp_client_smoke.py`) — optional

```pwsh
python .\scripts\dev\mcp_client_smoke.py `
    --server mcp-read-server `
    --transport stdio
```

Expected final line:
`OK (server=mcp-read-server transport=stdio)`.

For the HTTP transport, set the bearer token in an
env var first, then:

```pwsh
$env:MCP_SMOKE_TOKEN = '<TOKEN_VALUE>'
python .\scripts\dev\mcp_client_smoke.py `
    --server mcp-read-server `
    --transport http
```

Use a token value you generated yourself for the
smoke run; never put real production tokens into
ad-hoc shell variables.

---

## §12. Honest summary

This recipe gives an operator a single document to
read when something is wrong, plus a single document
to cite when classifying which signals the platform
supports and which it does not. The integration scope
is narrow on purpose:

- **What you can rely on:** seven first-class signals
  (FC1–FC7) covering stderr emission, exit codes,
  HTTP envelope, two pre-flight / release gates, one
  install-time output, and the systemd journal.
- **What you can use carefully:** four recommended-
  only signals (R1–R4) — the transport smoke harness,
  `--log-level DEBUG`, the `health_summary` MCP
  tool, and per-request HTTP access lines.
- **What is not shipped:** the entire forbidden
  surface enumerated in §1.3 + §2.3 + §9 — no full
  observability stack, no metrics platform, no
  dashboards, no alerting, no SIEM, no health
  endpoints, no structured-logging library, no
  `/healthz`.
- **The cross-OS posture is honest:** Linux/systemd/
  journald is the implementation-covered primary
  path; Windows / macOS / non-supervised execution
  are prose-only and do **not** claim parity.
- **The triage recipe is bounded:** three canonical
  failure modes (T1 startup-code-2; T2 universal
  401; T3 selfcheck FAIL) plus two optional follow-
  ups (T4 smoke FAIL; T5 systemd restart-loop). For
  anything else, surface as a defect or open a
  future operator-facing recipe.
- **No maturity is claimed beyond what is shipped.**
  Every forbidden maturity claim from §1.3 / §9.8
  appears in this recipe **only as an explicit
  denial**.

This is the entire Track N observability /
diagnostics boundary. Future tracks may extend it;
this recipe does not promise they will.

---

## §13. Cross-reference index

- `packages/mcp-common/src/mcp_common/_stdio_transport.py:53-58,62-68,181,208-212,242-244` — stdio transport logging boundary, `--log-level`, startup banner, shutdown messages, fatal-error handling.
- `packages/mcp-common/src/mcp_common/_network_transport.py:165-170,314-328,354-541,603-605,609-615,618-624,662,686-687,701-703` — HTTP transport `_fail()` path, access-log routing, response envelope shapes, bind failure, startup banner, shutdown messages, logging config, `--bind` startup gate, fatal-error handling.
- `scripts/dev/selfcheck.py:95-105` — selfcheck 11 key=value output (FC4).
- `scripts/release/verify-release.ps1:90-267` — verify-release 8-check gate (FC5).
- `scripts/dev/mcp_client_smoke.py` — transport-boundary smoke (R1).
- `scripts/release/_install_runner.py:57-84` — install fast-path output + exit codes (FC6).
- `scripts/release/install.ps1` — install fast-path entrypoint (FC6).
- `docs/operators/deployment-boundary.md` — Track J: TLS / reverse-proxy / `/healthz` non-shipping / deployment denials. §6 (carry-forward in this recipe §6); §10 (anchor for §9).
- `docs/operators/service/service-supervision.md` — Track L: supervisor wiring, lifecycle verbs, log facility. §9 (anchor for §3.1 level-to-event mapping); §9.5 (anchor for §9).
- `docs/operators/service/mcp-server.service` — Track L: systemd unit template; `KillSignal=SIGINT` graceful-shutdown wiring.
- `docs/operators/packaging/distribution-boundary.md` — Track M: build / install / uninstall / upgrade / verify lifecycle verbs over the wheel artefact. §13 (anchor for §9).
- `packages/onec-health/src/onec_health/__init__.py` — `HealthCheckResult` / `check_*` / `summarize_health` library exports (R3).
- `packages/onec-troubleshooting/src/onec_troubleshooting/__init__.py` — `diagnose_from_health` / `TroubleshootingReport` library exports.
