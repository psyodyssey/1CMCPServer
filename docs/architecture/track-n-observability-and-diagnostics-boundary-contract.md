# Parallel Track N — Observability and Diagnostics Boundary — Contract

**Step status.** Parallel Track N / Step 3 — normative
contract. Companion to
[track-n-observability-and-diagnostics-boundary-plan.md](track-n-observability-and-diagnostics-boundary-plan.md)
(Step 1 planning, Q1–Q7 directional defaults) and
[track-n-observability-and-diagnostics-boundary-baseline-audit.md](track-n-observability-and-diagnostics-boundary-baseline-audit.md)
(Step 2 descriptive baseline, Q1–Q6 directional
resolutions grounded in repo evidence at HEAD
`d4183ca`, project version `0.5.2`).

This document is **normative**. It translates Step 2
evidence into RFC 2119 MUST / MUST NOT / SHOULD /
SHOULD NOT / MAY rules that lock Step 4 PATH, Step 4
file surface, the supported diagnostics boundary, and
the verification protocol. After this commit there is
no remaining design freedom for Step 4 beyond what this
contract explicitly authorises.

The contract MUST NOT widen Track N into a full
observability platform, metrics stack, tracing program,
SIEM/SOC integration, alerting/on-call system, or
dashboard frontend. Each forbidden category is named in
§9 / §12.

---

## §1. Purpose / scope

### §1.1 What this contract is

A single normative document that:

- Locks the final answers to Q1 / Q2 / Q3 / Q4 / Q5
  from Step 1 plan §12 and Step 2 audit §7.
- Pins the **Step 4 PATH** to a single named option.
- Defines the **closure-gate scope** in terms of
  concrete, testable artefacts.
- Defines the **supported diagnostics surface** in
  terms of existing signals (no new signal classes
  introduced by Track N).
- Defines the **Step 4 file surface** (exact allowed
  paths, file counts, LOC caps, forbidden-files list).
- Defines the **verification protocol** Step 4 must
  satisfy pre-commit and post-commit.
- Carries forward every Tracks A–M invariant byte-
  identical.

### §1.2 What this contract is not

- Not an implementation. No production code, no
  recipe content, no `pyproject.toml` change, no
  `scripts/*` change.
- Not an audit. Step 2 already produced the
  descriptive baseline at
  `docs/architecture/track-n-observability-and-diagnostics-boundary-baseline-audit.md`;
  this contract MUST NOT re-litigate Step 2 evidence
  except where a new contradictory fact appears.
- Not a Step 5 alignment doc. CLASS-1 alignment of
  README / PROJECT-STATUS / `docs/release-handoff.md`
  / `apps/platform/README.md` is Step 5 territory and
  is locked separately.
- Not a Step 6 closure document. Q6 (SemVer outcome)
  is **framed** here but **locked** at Step 6.

### §1.3 RFC 2119 keyword usage

Throughout this document:

- **MUST** / **MUST NOT** / **REQUIRED** /
  **SHALL** / **SHALL NOT** — absolute requirements
  whose violation invalidates a Step 4 commit.
- **SHOULD** / **SHOULD NOT** / **RECOMMENDED** —
  default behaviour; deviation MUST be justified
  inline in the affected commit message.
- **MAY** / **OPTIONAL** — operator-level discretion;
  no justification required.

Keywords appear in **bold** when they carry RFC 2119
weight; lowercase usage in prose has its ordinary
English meaning.

### §1.4 Track N scope reminder (binding)

This contract MUST keep Track N narrow. Specifically,
the contract MUST NOT authorise, encourage, or
indirectly enable any of:

- A full OpenTelemetry program (SDK / collector /
  span emission / `traceparent` propagation).
- Any Prometheus / OpenMetrics / `/metrics` endpoint /
  exporter / `prometheus_client` dependency.
- Any Grafana / Tempo / Loki / Jaeger / Mimir / Cortex
  / VictoriaMetrics platform.
- Any SIEM / SOC integration (Splunk forwarder /
  Elastic ingestion / SOAR runbook scaffolding).
- Distributed tracing across systems.
- Alerting / paging / on-call workflows (PagerDuty /
  Opsgenie / Slack alerts / email alerts).
- `/healthz` / `/readyz` / `/livez` HTTP endpoints
  (Track J §6 defer preserved).
- Log-aggregation forwarders bundled in-repo
  (`vector` / `fluentd` / `fluent-bit` / `rsyslog`
  config / `journal-remote`).
- Structured-logging library dependencies
  (`structlog` / `loguru` / `python-json-logger`).
- Web UI / dashboard frontend.
- Transport redesign (Track G stdio + Track H HTTP
  preserved byte-identical).
- Auth redesign (Track H bearer + Track D
  `${ENV:NAME}` + Track I round-trip preserved byte-
  identical).
- Deployment-boundary redesign (Track J preserved
  byte-identical).
- Service-supervision redesign (Track L preserved
  byte-identical).
- Packaging redesign (Track M preserved byte-
  identical, including the 11-element `[tool.hatch.
  build.targets.wheel] packages` array).
- New MCP tools or registry change (`read=15 /
  write=25 / intelligence=16` invariant carried
  through).
- New CLI flags on existing servers (Track G/H flag
  surface locked).
- New `[project.scripts]` console entries.
- New dependencies in `[project.dependencies]` or
  `[project.optional-dependencies]`.
- New entrypoint module in any `apps/*/src/`
  package.
- `1cv8.exe` runs.
- Remote push (operator decision; never automated).
- Any maturity claim of the form "observability
  solved forever" / "production-ready observability"
  / "full OTel instrumentation" / "Prometheus
  platform shipped" / "distributed tracing ready" /
  "SIEM-ready" / "enterprise-ready observability" /
  "alerting solved" / "all signals covered".

---

## §2. Relationship to Step 1 plan and Step 2 audit

### §2.1 Step boundary

This contract sits between Step 2 (descriptive audit)
and Step 4 (narrow implementation slice). The six-step
shape is fixed by Step 1 step-map:

| Step | Kind | Status at this commit |
| --- | --- | --- |
| Step 1 | planning | closed (commit `efb4e5c`) |
| Step 2 | descriptive baseline audit | closed (commit `d4183ca`) |
| Step 3 | normative contract | **this commit** |
| Step 4 | narrow implementation slice | upcoming |
| Step 5 | docs / operator / release alignment | future |
| Step 6 | final integration pass + Q6 lock | future |

### §2.2 Re-litigation rule

This contract MUST NOT silently amend Step 2 findings
without naming the contradiction. If, during Step 4
authoring, a Step 2 fact is contradicted by repo
evidence, the Step 4 commit MUST cite this contract
§2.2 and explicitly call out the contradiction in its
commit message before proceeding. Re-opening Step 2 is
a separate process.

### §2.3 Inherited Step 2 audit resolutions

Step 2 §7 produced six directional resolutions. This
contract converts them into normative answers.

**Q1 — what counts as "observability/diagnostics" for
closure?**
Audit recommendation: PATH A docs-only primary.
**Contract LOCK (§4 / §6 / §7).** Closure is **one
operator-facing diagnostics-boundary recipe** plus the
named supported-signals classification it embeds; no
new signal generation, no new code-bearing artefact.

**Q2 — primary supported diagnostics surface?**
Audit recommendation: Linux/systemd/journald primary;
cross-OS prose for Windows / macOS / non-supervised.
**Contract LOCK (§5).** Linux + systemd + journald
is the implementation-covered primary OS-family;
Windows (NSSM / Event Viewer) + macOS (launchd /
Console.app) + non-supervised execution receive
prose-only sections in the recipe.

**Q3 — likely honest Step 4 path?**
Audit recommendation: PATH A docs-only primary.
**Contract LOCK (§7.1).** Step 4 PATH = **PATH A
docs-only**. PATH B (selfcheck `--json` slice) and
PATH C (log-shape contract slice) are explicitly
rejected in §7.2 / §7.3.

**Q4 — what is definitely mandatory for closure?**
Audit recommendation: six mandatory items.
**Contract LOCK (§4.1 / §6).** Six mandatory recipe
elements pinned: supported signals list, triage
recipe (≥ 3 canonical failure modes end-to-end),
exit-code-meaning table, log-level-to-event mapping,
authoritative non-goals enumeration, `/healthz` non-
shipping cross-reference.

**Q5 — what is definitely insufficient as closure
proof?**
Audit recommendation: each existing surface
individually insufficient.
**Contract LOCK (§9).** Each named source on its own
is normatively insufficient; only the integration
document closes the gap.

**Q6 — does Track N require production code?**
Audit recommendation: likely no.
**Contract LOCK (§10).** No production code change
under PATH A. Q6 SemVer outcome framed (§13.5) but
locked at Step 6.

---

## §3. Inherited fixed decisions from Step 2

The following decisions are inherited from Step 2 §3 /
§4 evidence and MUST NOT be revisited by this contract
or by Step 4 without new contradictory evidence.

### §3.1 Existing diagnostic surfaces preserved byte-identical

Step 2 §3 enumerated the existing surfaces. Each MUST
be preserved byte-identical through Step 4:

1. **Python `logging` boundary** at
   `packages/mcp-common/src/mcp_common/_stdio_transport.py:62-68`
   (`_configure_logging()`, format string
   `"%(asctime)s %(levelname)s %(name)s: %(message)s"`).
2. **`--log-level` flag** declared at
   `_stdio_transport.py:53-58` (choices DEBUG / INFO /
   WARNING / ERROR; default INFO).
3. **stdio startup banner** at
   `_stdio_transport.py:181` (`logger.info("Starting %s
   stdio transport (JSON-RPC 2.0).", server_name)`).
4. **HTTP startup banner** at
   `_network_transport.py:609-615` (`logger.info(
   "Starting %s HTTP transport (JSON-RPC 2.0) on
   %s:%s with %d valid token(s).", ...)`).
5. **Shutdown messages** at
   `_stdio_transport.py:208-212` and
   `_network_transport.py:618-620`.
6. **Three-bucket exit codes** (0 / 1 / 2) as
   exhaustively enumerated in Step 2 §3.3.
7. **HTTP response envelope table** as exhaustively
   enumerated in Step 2 §3.5 (auth-failure 401 +
   `WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
   `-32001` "Unauthorized"; 400/413/415/400/400 for
   the non-auth failure modes; per Track H §8.4
   failure-equivalence on auth).
8. **Per-request HTTP access logs** at
   `_network_transport.py:314-328` via
   `log_message()` override routing to
   `logger.info("http %s - %s", ...)`.
9. **`scripts/dev/selfcheck.py`** exact 11 key=value
   line output (`selfcheck.py:95-105`).
10. **`scripts/release/verify-release.ps1`** 8 named
    checks (`verify-release.ps1:90-267`).
11. **`scripts/dev/mcp_client_smoke.py`** structured
    progress output.
12. **`scripts/release/_install_runner.py:57-78`**
    structured findings output and exit codes
    (`_install_runner.py:80-84`).
13. **`packages/onec-health/`** library exports
    (`HealthCheckResult`, `check_dump_path_exists`,
    `check_http_gateway_available`,
    `check_search_index_available`,
    `check_environment_health`, `summarize_health`);
    `health_summary` exposed as a read-server MCP
    tool.
14. **`packages/onec-troubleshooting/`** library
    exports (`diagnose_from_health`,
    `TroubleshootingReport`).
15. **Track L `service-supervision.md` §9** signal
    vocabulary (`WARNING/ERROR` for credential / auth
    / config issues; `INFO` for startup / shutdown;
    `DEBUG` for transport-level detail when
    `--log-level DEBUG`).
16. **Track J `deployment-boundary.md` §6 / §10**
    deployment-side denials (no `/healthz`, no
    observability stack, stderr is the boundary).
17. **`.github/workflows/dev-check.yml`** running
    `selfcheck.py` only.

### §3.2 Existing gap statement preserved

Step 2 §3 / §6 established the gap as **integration
and naming**, not signal generation. This contract
MUST NOT introduce new signal-generation surfaces.

### §3.3 Existing reusable surfaces preserved

Step 2 §4 enumerated 9 reusable surfaces. All MUST
be preserved byte-identical through Step 4.

---

## §4. Closure-gate contract

### §4.1 Definition of "honest Track N closure"

Track N closes honestly **iff** all of the following
hold at the Step 6 commit:

C1. **Single operator-facing observability /
    diagnostics recipe** committed at the path locked
    in §8.2.
C2. The recipe **MUST** contain a **supported signals
    list** classifying each diagnostic surface from
    §3.1 as one of:
    - **first-class supported**,
    - **recommended-only**,
    - **out-of-scope** (carry-forward denial).
C3. The recipe **MUST** contain an **exit-code-
    meaning table** promoting the de-facto 0 / 1 / 2
    convention from `_stdio_transport.py:208-212,
    242-244` and `_network_transport.py:603-605,
    618-624, 701-703` to operator-readable form.
C4. The recipe **MUST** contain a **log-level-to-
    event mapping** that EITHER (a) inherits Track L
    `service-supervision.md` §9.3 verbatim by quote
    or by explicit reference, OR (b) states a
    superset that does not contradict §9.3.
C5. The recipe **MUST** contain a **triage recipe**
    of **at least three** canonical failure modes
    end-to-end. Each failure mode entry MUST cite
    concrete signals from §3.1 (e.g., "the server
    exited with code `2` immediately on startup
    → consult the last stderr line; possible causes
    A / B / C with check commands").
C6. The recipe **MUST** contain an **authoritative
    non-goals enumeration** collecting Track J §10 +
    Track L §9.5 + Track L §13 + Track M §13
    denials into one observability-specific list
    (verbatim quotes or explicit references both
    acceptable).
C7. The recipe **MUST** contain a **`/healthz` non-
    shipping cross-reference** pointing operators
    at Track J `deployment-boundary.md` §6 rather
    than restating its content.
C8. The recipe **MUST** contain **at least one
    explicit cross-reference each** to: Track J
    `deployment-boundary.md`, Track L
    `service-supervision.md`, Track M
    `distribution-boundary.md`, `scripts/dev/selfcheck.py`,
    `scripts/release/verify-release.ps1`,
    `scripts/dev/mcp_client_smoke.py`,
    `scripts/release/install.ps1`.
C9. The recipe **MUST** contain a **cross-OS
    posture** section: Linux/systemd/journald
    primary (implementation-covered prose) plus
    Windows (NSSM / Event Viewer) and macOS
    (launchd / Console.app) and non-supervised
    execution (operator running `python -m
    mcp_<server>` directly) as prose-only sections.
C10. README / PROJECT-STATUS / CHANGELOG closure
     narrative (Step 5 + Step 6) MUST honestly
     describe what was settled and MUST explicitly
     deny each forbidden-claim phrase from §1.4.
C11. Tracks A–M production code byte-identical to
     Track M closure state (`a3bdc48`).
C12. Registries `read=15 / write=25 /
     intelligence=16` unchanged.
C13. `verify-release.ps1` GREEN on 8 checks at each
     of Step 3 / 4 / 5 / 6 commits (pre- and post-).
C14. `selfcheck.py` `status=ok` at each step.
C15. No real credentials in any committed file.
C16. No `1cv8.exe` runs.
C17. No remote push performed by the track.

### §4.2 What does NOT count as closure-gate proof

The following claims, however true individually, are
**NOT** sufficient closure-gate proof:

- "There are logs somewhere" (sufficient prose, not
  sufficient closure proof).
- `selfcheck.py` PASS alone (pre-flight gate;
  Step 2 §5.2).
- `verify-release.ps1` GREEN alone (release-side
  gate; Step 2 §5.3).
- `mcp_client_smoke.py` PASS alone (transport-
  boundary smoke; Step 2 §5.4).
- `install.ps1` / `_install_runner.py` output alone
  (install-time only; Step 2 §5.7).
- Track L `service-supervision.md` §9 alone
  (systemd-supervised only; Step 2 §5.5).
- Track J `deployment-boundary.md` §6 / §10 alone
  (denials only, no positive surface; Step 2 §5.6).
- Track M `distribution-boundary.md` alone (no
  primary observability content; Step 2 §3.11.3).
- Ad-hoc operator lore (Step 2 §5.8).
- Screenshots of running terminals or browser
  windows.
- Generic statements about future observability
  intent.
- Verbal commitments outside the recipe file.

### §4.3 What Step 4 MUST commit

Step 4 MUST commit exactly the file set defined in
§8 and MUST NOT commit anything else. Specifically:

- Exactly one new operator recipe file at the path
  locked in §8.2.
- Zero modifications to any file enumerated in §8.5
  (forbidden file surface).
- No new dependencies.
- No new scripts.
- No new MCP tools.
- No registry change.

---

## §5. Primary supported diagnostics surface contract

### §5.1 Locked primary surface

The primary supported diagnostics surface for Track N
is:

> **stderr emission via Python `logging.basicConfig`
> at the `--log-level INFO|WARNING|ERROR|DEBUG`
> boundary, plus process exit codes, plus HTTP
> response envelopes for the HTTP transport, plus the
> existing named helper gates (`selfcheck.py`,
> `verify-release.ps1`, `mcp_client_smoke.py`,
> `install.ps1` / `_install_runner.py`), plus the
> systemd/journald boundary on Linux hosts that
> deploy via Track L.**

### §5.2 Primary OS-family

Linux + systemd + journald is the
implementation-covered primary OS-family for Track N
recipe prose. This is **inherited** from Track L
`service-supervision.md` §2.1; Track N does not
duplicate the systemd unit template, does not change
the `KillSignal=SIGINT` boundary, and does not redefine
the level-to-event mapping in `service-supervision.md`
§9.3.

### §5.3 Cross-OS coverage

The Track N recipe **MUST** include prose-only
sections for:

- **Windows** — NSSM service-wrapper service-recovery
  pane + Windows Event Viewer (Application log; the
  Track L §12.1 cross-reference is sufficient).
- **macOS** — launchd `launchctl print` plus
  `Console.app` System Reports; the Track L §12.2
  cross-reference is sufficient.
- **Non-supervised execution** — operator running
  `python -m mcp_<server>` directly: stderr arrives
  on whatever terminal / parent process / log file
  the operator chose to redirect it to; no platform-
  provided rotation, persistence, or filter.

Cross-OS sections **MUST NOT** claim implementation-
covered parity with the Linux/systemd path.

### §5.4 No new signal classes

Track N **MUST NOT** add any new signal class. The
existing signal classes are:

- Python `logging` log records at
  DEBUG/INFO/WARNING/ERROR.
- Process exit codes (0 / 1 / 2).
- HTTP response status codes + headers + JSON-RPC
  envelope.
- Helper-script structured-text output (selfcheck /
  verify-release / mcp_client_smoke / install
  runner).
- systemd journal records (inherited from §3.1.15;
  no new fields, no structured-JSON-line format).

A future track MAY add structured logging; Track N
does not (Track L §9.5 carry-forward).

### §5.5 No metric / tracing / alerting surface

Track N **MUST NOT** introduce:

- Histogram, counter, gauge, summary metric.
- Span emission or trace context propagation.
- Alert rule, threshold, paging hook.
- Notification channel binding.
- Dashboard configuration.

Any of the above belongs to a separate future track
or to operator-side tooling outside the Track N
boundary.

---

## §6. Observability / diagnostics boundary contract

### §6.1 What the boundary is

The Track N boundary is:

- **A single in-repo operator recipe** at the path
  locked in §8.2.
- **Six mandatory content elements** (C2–C7 from
  §4.1).
- **Cross-references** to the seven anchors in C8.
- **Cross-OS posture** (C9).
- **Explicit denial of forbidden categories** from
  §1.4.

### §6.2 What the boundary is NOT

The Track N boundary is **NOT**:

- A guarantee of operator-side observability
  outcomes (operators retain full discretion over
  how they consume logs / exit codes / responses).
- A guarantee of a stable log-line text format —
  log strings may evolve between project versions;
  the recipe pins **categories** of events (level-
  to-event mapping) rather than literal strings.
- A claim that every operationally relevant signal
  is enumerated. Operators MAY observe additional
  signals (e.g., systemd `MainPID` state,
  reverse-proxy access logs); the recipe enumerates
  the **first-class** subset.
- A claim of cross-OS implementation-covered parity.
- A health-endpoint, alerting story, metric pipe,
  or tracing infrastructure.

### §6.3 First-class vs recommended-only vs out-of-scope

The recipe **MUST** classify each surface from §3.1
as one of three categories. The default classification
(which the recipe MAY adjust if it justifies the
adjustment inline) is:

**First-class supported diagnostic surfaces:**
- Python `logging` stderr emission at
  `--log-level INFO` (recipe quotes Track L §9.3
  level-to-event mapping verbatim or by reference).
- Process exit codes 0 / 1 / 2.
- HTTP response envelope (status + headers +
  JSON-RPC `-32xxx` code).
- `scripts/dev/selfcheck.py` 11-key=value output.
- `scripts/release/verify-release.ps1` 8-check
  summary.
- `scripts/release/install.ps1` / `_install_runner.py`
  structured findings.
- systemd `journalctl -u <UNIT>.service` (Linux
  hosts deployed via Track L).

**Recommended-only diagnostic surfaces:**
- `scripts/dev/mcp_client_smoke.py` transport-
  boundary smoke (Track K classification preserved).
- `--log-level DEBUG` transport-detail traces
  (operationally noisy; not for steady-state
  operation).
- `health_summary` MCP tool on `mcp-read-server`
  (callable via any MCP client; operator-side
  invocation is operator's choice).
- per-request HTTP access lines at `INFO` (existing
  surface; useful but not a triage primitive).

**Out-of-scope (forbidden by Track N):**
- Everything in §1.4's forbidden list.

### §6.4 Log-level-to-event mapping

The recipe **MUST** state the level-to-event mapping.
The locked mapping (inherited from Track L
`service-supervision.md` §9.3) is:

- **DEBUG** — transport-level detail (per-request
  HTTP access lines, JSON-RPC envelope details,
  initialisation traces). Used when `--log-level
  DEBUG` is passed; NOT recommended for steady-
  state operation.
- **INFO** — startup banner, shutdown messages,
  successful config-load events, per-request HTTP
  access lines. Default level.
- **WARNING** — recoverable issues, degraded paths,
  resolved-but-suspicious config (Track L §9.3
  "credential / auth / config issues" overlaps with
  WARNING and ERROR depending on severity).
- **ERROR** — failure-equivalent conditions:
  unresolved env-var for `--auth-token-env`, bind
  failure (`_network_transport.py:603-605`),
  unhandled exception (`logger.exception` paths at
  `_stdio_transport.py:242-244` and
  `_network_transport.py:701-703,682-683`),
  HTTP request handler exceptions.

### §6.5 Exit-code-meaning table

The recipe **MUST** include a table covering:

| Code | Meaning | Where |
| --- | --- | --- |
| 0 | Clean exit (operator-initiated stop, EOF on stdin, graceful Ctrl-C / SIGINT). | `_stdio_transport.py:208-212`, `_network_transport.py:618-624` |
| 1 | Unhandled exception caught at the entrypoint boundary; full traceback logged via `logger.exception("Fatal error in %s entrypoint", ...)`. | `_stdio_transport.py:242-244`, `_network_transport.py:701-703,682-683` |
| 2 | Startup-time operator-readable failure (bad config path, missing required flag like `--bind` for HTTP transport, unresolved `--auth-token-env`, bind error). Single-line stderr message via `_fail()`; no traceback. | `_network_transport.py:165-170,603-605,686-687`; argparse `parser.parse_args()` defaults |

The recipe MAY add explanatory prose around the
table; it MUST NOT introduce additional exit-code
buckets.

### §6.6 Triage recipe scope

The triage recipe **MUST** cover at least the
following three canonical failure modes (the recipe
MAY add more, up to ≤ 5 total for §8 file-size
discipline):

T1. **"The server exited with code `2` immediately
    on startup."** Operator action: read the last
    line on stderr; expected causes include
    bad-config-path, missing `--bind` for HTTP
    transport, unresolved env-var for
    `--auth-token-env`, port-in-use bind failure.
    Each cause MUST cite the line in
    `_network_transport.py` where the failure
    originates.
T2. **"The HTTP transport returns 401 to every
    request."** Operator action: per Track H §8.4
    failure-equivalence, check (a) presence of
    `Authorization` header in the client request,
    (b) literal Bearer scheme match, (c) token
    value present in `ProductConfig.auth.tokens` or
    via `--auth-token-env`, (d) constant-time
    comparison succeeded (i.e., the configured
    token MUST equal the presented one byte-for-
    byte). Recipe MUST point operators at Track H
    contract §8 and Track I installer round-trip
    integrity.
T3. **"`selfcheck.py` failed."** Operator action:
    read the last lines on stderr (the Python
    traceback Python emits when an import fails);
    fix the broken import / dependency boundary.
    Recipe MUST state that `selfcheck.py` is a
    pre-flight gate and a `selfcheck.py` FAIL does
    not necessarily indicate a runtime issue —
    only an import/registry-integrity issue.

The triage recipe MAY add:

T4 (optional). "`mcp_client_smoke.py` reports a
   transport failure." Pointer to Track K
   classification + checks.
T5 (optional). "The systemd unit is restart-
   looping." Pointer to Track L §7 + journalctl
   filter.

The triage recipe MUST NOT cover:
- Performance / capacity / scaling triage
  (out of scope).
- Distributed-system failure modes spanning
  multiple hosts (out of scope).
- Vendor-specific cloud-platform triage (out of
  scope).

### §6.7 Non-goals enumeration scope

The recipe **MUST** include an explicit non-goals
section. The non-goals enumeration MUST cover at
minimum:

- Full OpenTelemetry program.
- Prometheus / OpenMetrics / `/metrics` endpoint.
- Grafana / Tempo / Loki / Jaeger / Mimir / Cortex /
  VictoriaMetrics platform.
- SIEM / SOC integration.
- Distributed tracing.
- Alerting / paging / on-call workflows.
- `/healthz` / `/readyz` / `/livez` endpoints.
- Log-aggregation forwarder configuration.
- Structured-logging library dependency.
- Web UI / dashboard frontend.
- New MCP tools.
- New CLI flag on existing servers.
- New `[project.scripts]` entries.
- New dependencies.

For each item, the recipe MAY either restate the
denial verbatim or cite the existing anchor (Track J
§10, Track L §9.5, Track L §13, Track M §13).

### §6.8 Relationship to existing operator recipes

The recipe **MUST** explicitly position itself as
orthogonal-but-complementary to:

- **Track J `deployment-boundary.md`** — deployment-
  boundary, reverse-proxy, TLS termination, threat
  model, `/healthz` non-shipping. Recipe MUST cross-
  reference §6 and §10.
- **Track L `service-supervision.md`** — service
  supervision, lifecycle verbs, log facility on
  systemd hosts. Recipe MUST cross-reference §9 and
  §13.
- **Track M `distribution-boundary.md`** — packaging
  boundary, wheel build, install lifecycle verbs.
  Recipe MUST cross-reference where install-time
  diagnostics live.

The recipe MUST NOT duplicate content from these
recipes; cross-references are sufficient.

---

## §7. Final Step 4 PATH selection

### §7.1 Locked: PATH A docs-only

**Step 4 PATH = PATH A docs-only.**

Step 4 SHALL produce exactly one new operator-facing
recipe under the path locked in §8.2 and SHALL NOT
modify any production code, `pyproject.toml`,
`scripts/*`, or any existing operator recipe.

### §7.2 PATH B explicitly rejected

PATH B (docs + one narrow code-bearing slice, e.g.,
`selfcheck.py` gains a `--json` mode) is explicitly
rejected by this contract. Justification grounded in
Step 2 evidence:

- Step 2 §4.6 / §7.4 / §7.6 / §9 establish that
  `selfcheck.py` output is **already operator-
  parseable** as 11 key=value lines (line-oriented,
  trivial to read with `awk` / `grep` / `while
  read`).
- No Step 2 evidence identifies an operator who is
  blocked by the absence of a structured-output
  mode.
- Adding `--json` mode would require touching
  `scripts/dev/selfcheck.py` (currently 110 LOC,
  byte-identical since Track G); that touch is
  defensible only as defect-class repair, and no
  defect class is present (the script does what its
  docstring promises).
- The Step 2 audit §7.6 explicitly states
  "production code change likely not required".
- PATH B trades complexity for marginal value when
  the gap is integration-and-naming.

PATH B remains theoretically available for a future
track; this Track N closes under PATH A.

### §7.3 PATH C explicitly rejected

PATH C (docs + one narrow log-shape contract slice,
e.g., a canonical startup-banner helper in
`mcp_common` applied symmetric across the three MCP
server entrypoints) is explicitly rejected by this
contract. Justification:

- The existing log format string at
  `_stdio_transport.py:66`
  (`"%(asctime)s %(levelname)s %(name)s: %(message)s"`)
  is **already symmetric** across both transports;
  there is no inconsistency to repair.
- The existing startup banners at
  `_stdio_transport.py:181` and
  `_network_transport.py:609-615` are short,
  operator-readable, and well-formed.
- A helper in `mcp_common` would require modifying
  all three MCP server entrypoints (`apps/*/src/*/
  __main__.py`), expanding the touched-files surface
  for negligible operator gain.
- The Step 2 audit §7.1 / §7.6 explicitly classifies
  PATH C as "very low probability".

PATH C remains theoretically available for a future
track; this Track N closes under PATH A.

### §7.4 PATH D considered and rejected

A late-arriving "PATH D" (diagnostic-bundle helper
script under `scripts/dev/` that collects last-N
stderr lines + exit code + selfcheck output + verify-
release output into a single operator-readable
bundle) was considered and rejected:

- Step 2 §3.13 / §6.5 establishes that no operator
  workflow currently consumes such a bundle.
- The functionality of "look at recent stderr +
  recent selfcheck + recent verify-release" already
  exists out-of-band (operators run each gate
  separately and read its output).
- The bundle would duplicate the existing surfaces
  rather than integrate them.
- Track K `mcp_client_smoke.py` precedent does not
  generalise: the smoke harness exercises a specific
  transport-boundary scenario, not a heterogenous
  signal-collection workflow.

### §7.5 PATH A defended

PATH A is the narrowest honest closure path because:

- The gap is **integration and naming**, not
  signal generation (Step 2 §3 / §6).
- Every signal Track N needs to formalise **already
  exists** (Step 2 §3.1–§3.13).
- Production code change is **likely not required**
  (Step 2 §7.6).
- Tracks J / L / M closed comparable gaps under
  docs-only patterns (Track J = PATH A; Track L =
  PATH B but only because Track L shipped one
  declarative template file; Track M = PATH B with
  the narrowest possible `pyproject.toml` flip).
- Track J / Step 6 closure precedent established the
  `Q7 = NO-BUMP` outcome for a comparable docs-only
  boundary closure; this contract §13.5 frames the
  same expectation for Track N Q6.

---

## §8. Exact Step 4 implementation surface

### §8.1 File count cap

Step 4 **MUST** add **exactly one** new file and
**MUST** modify **exactly zero** files. Total Step 4
touched-files count = 1 (add).

If Step 4 authoring encounters a situation that
appears to require touching more than one file, the
authoring MUST STOP and surface the conflict
explicitly rather than silently expand scope.

### §8.2 Recipe path — canonical location

The new recipe **MUST** be created at exactly:

```
docs/operators/observability.md
```

Rationale: Step 2 §8 item 6 proposed either
`docs/operators/observability/` (subdirectory) or
`docs/operators/observability.md` (single file). The
contract picks the **single-file** form for
symmetry with `docs/operators/deployment-boundary.md`
(Track J): both are operator-recipe single-file
artefacts at the top level of `docs/operators/`. A
subdirectory is only warranted if multiple peer files
ship, which Track N MUST NOT do.

### §8.3 Recipe required content shape

The new file **MUST** be structured as a recipe (not
a contract, not an audit). Recommended top-level
sections (the recipe MAY rename / reorder; section
content is normative per §4.1 / §6):

- §1 Purpose / scope (what this recipe is and is not).
- §2 Supported diagnostic surfaces (the first-class
  list per §6.3).
- §3 Log-level-to-event mapping (per §6.4; quote or
  reference Track L §9.3).
- §4 Exit-code-meaning table (per §6.5).
- §5 HTTP response envelopes (per §3.1.7 / Track H
  §8.4 carry-forward, summary table).
- §6 Triage recipe (≥ 3 canonical failure modes per
  §6.6).
- §7 Cross-OS posture (per §5.3, prose-only outside
  Linux/systemd).
- §8 Relationship to existing recipes (per §6.8,
  Track J / L / M cross-references).
- §9 Honest non-goals (per §6.7).
- §10 Verification (operator-side: how to confirm
  each first-class signal is readable on their
  host).
- §11 Cross-references (file list pointing back to
  §3.1 anchors).

### §8.4 Recipe size cap

- **Hard cap: ≤ 1200 lines** (the longest existing
  comparable recipe, Track M
  `distribution-boundary.md`, is 912 lines).
- **Soft cap: ≤ 1000 lines** (RECOMMENDED).
- LOC cap is on operator-facing prose. The recipe
  MUST NOT contain executable code beyond literal
  command-line examples in fenced code blocks. Code
  examples MUST use abstract placeholders
  (`<UNIT_NAME>` / `<PORT>` / `<TOKEN_ENV_VAR>`)
  rather than real values.

### §8.5 Forbidden file surface for Step 4 (exhaustive list)

Step 4 **MUST NOT** create, modify, delete, or
rename any file in this exhaustive list:

**Production code (byte-identical):**
- `apps/mcp-read-server/src/mcp_read_server/**`
- `apps/mcp-write-server/src/mcp_write_server/**`
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/**`
- `apps/platform/src/onec_platform/**`
- `packages/mcp-common/src/mcp_common/**`
- `packages/onec-process-runner/src/onec_process_runner/**`
- `packages/onec-policy-engine/src/onec_policy_engine/**`
- `packages/onec-audit/src/onec_audit/**`
- `packages/onec-health/src/onec_health/**`
- `packages/onec-troubleshooting/src/onec_troubleshooting/**`
- `packages/onec-config/src/onec_config/**`

**Project configuration (byte-identical):**
- `pyproject.toml`
- `.python-version`
- `.gitignore`
- `LICENSE`

**Existing scripts (byte-identical):**
- `scripts/dev/selfcheck.py`
- `scripts/dev/mcp_client_smoke.py`
- `scripts/dev/launch.ps1`
- `scripts/dev/bootstrap_paths.ps1`
- `scripts/dev/run_dev_check.ps1`
- `scripts/dev/README.md`
- `scripts/release/install.ps1`
- `scripts/release/verify-release.ps1`
- `scripts/release/_install_runner.py`
- `scripts/release/README.md`

**Existing operator recipes (byte-identical):**
- `docs/operators/deployment-boundary.md`
- `docs/operators/service/service-supervision.md`
- `docs/operators/service/mcp-server.service`
- `docs/operators/packaging/distribution-boundary.md`

**Existing status / handoff docs (byte-identical;
those listed here are Step-5 / Step-6 territory):**
- `README.md`
- `PROJECT-STATUS.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `docs/release-handoff.md`
- `apps/platform/README.md`
- `docs/operator-manual.md`
- `docs/administrator-manual.md`
- `docs/developer-manual.md`
- `docs/runbooks.md`
- `docs/runbooks/**`

**Tests / data (byte-identical):**
- `tests/**` (if present)
- `examples/**`
- `dist/**`

**Track N step docs (byte-identical):**
- `docs/architecture/track-n-observability-and-diagnostics-boundary-plan.md`
- `docs/architecture/track-n-observability-and-diagnostics-boundary-step-map.md`
- `docs/architecture/track-n-observability-and-diagnostics-boundary-baseline-audit.md`
- this file (`docs/architecture/track-n-observability-and-diagnostics-boundary-contract.md`)

**All Tracks A–M architecture docs (byte-identical):**
- `docs/architecture/track-a-*.md`
- `docs/architecture/track-b-*.md`
- `docs/architecture/track-c-*.md`
- `docs/architecture/track-d-*.md`
- `docs/architecture/track-e-*.md`
- `docs/architecture/track-f-*.md`
- `docs/architecture/track-g-*.md`
- `docs/architecture/track-h-*.md`
- `docs/architecture/track-i-*.md`
- `docs/architecture/track-j-*.md`
- `docs/architecture/track-k-*.md`
- `docs/architecture/track-l-*.md`
- `docs/architecture/track-m-*.md`
- `docs/architecture/phase-*.md`

**CI workflow (byte-identical):**
- `.github/workflows/dev-check.yml`
- `.github/**` (any other file present)

If Step 4 touches any path on this list, the commit
MUST be rejected.

### §8.6 LOC and dependency caps

- **LOC cap (Step 4):** the new recipe MAY be up to
  the soft / hard caps in §8.4. No other LOC accrues
  because no other file changes.
- **Net code LOC change (Step 4):** **0**.
- **New `[project.dependencies]` entries:** 0.
- **New `[project.optional-dependencies]` entries:** 0.
- **New `[project.scripts]` entries:** 0.
- **New entrypoint modules:** 0.

### §8.7 What Step 4 MAY do beyond §8.1–§8.6

- Step 4 MAY use Markdown features (tables, fenced
  code blocks, headings, lists, blockquotes) in the
  recipe.
- Step 4 MAY include short fenced shell snippets
  (`bash`, `pwsh`) with abstract placeholders.
- Step 4 MAY quote prose verbatim from Track L §9.3
  / Track J §6 / §10 / Track M §13 / other anchor
  docs.
- Step 4 MAY reference selfcheck / verify-release /
  smoke harness output by name and shape (no need
  to literally invoke the scripts during authoring).
- Step 4 MAY include a "Cross-references" tail
  section pointing back at the seven anchors in C8.

---

## §9. Forbidden evidence / insufficient-evidence contract

### §9.1 Insufficient-on-its-own list (binding)

The following claims, presented as standalone closure
proof, MUST be rejected by any Step 4 review:

1. **"There are logs somewhere."** — Step 2 §5.1.
2. **"Selfcheck passes."** — pre-flight gate only;
   does not exercise any runtime transport.
   Step 2 §5.2.
3. **"Verify-release is GREEN."** — release-side
   gate only; does not exercise transport, auth, or
   runtime triage. Step 2 §5.3.
4. **"`mcp_client_smoke.py` passes."** — transport-
   boundary smoke only; Track K classification
   preserved. Step 2 §5.4.
5. **"`service-supervision.md` already covers logs."**
   — covers systemd path only; no Windows, no
   macOS, no non-supervised, no positive signal
   classification, no triage. Step 2 §5.5.
6. **"`deployment-boundary.md` already covers
   observability."** — denials only, no positive
   surface. Step 2 §5.6.
7. **"Install fast-path output is enough."** —
   install-time only; no runtime triage. Step 2 §5.7.
8. **"Ad-hoc operator lore is enough."** — operator-
   hostile, code-savvy-only. Step 2 §5.8.
9. **"Screenshots of running terminals."** — non-
   text, non-reproducible.
10. **"Generic statements about future observability
    intent."** — aspiration, not commitment.

### §9.2 What MUST appear in the recipe as explicit denial

The recipe **MUST** explicitly deny each of the
following claims (verbatim quote acceptable; explicit
restatement acceptable; bare reference is NOT
sufficient for these specific phrases):

- "Observability solved forever."
- "Production-ready observability."
- "Full OpenTelemetry instrumentation."
- "Prometheus platform shipped."
- "Distributed tracing ready."
- "SIEM-ready."
- "Enterprise-ready observability."
- "Alerting solved."
- "All signals covered."

The recipe MUST collect these as a single "forbidden
maturity claims" sub-section under §9 of the recipe
(per §8.3 suggested structure) or in functionally
equivalent location.

### §9.3 What MUST NOT appear in any Track N artefact

- Real credentials of any kind (no tokens, no
  passwords, no private keys, no bearer strings).
- Real customer / operator host names, IP addresses,
  reverse-proxy domain names.
- Vendor-specific cloud-platform references (AWS /
  GCP / Azure / Yandex / etc. service names) as
  required-tools claims; vendor names MAY appear
  only as out-of-scope examples.
- Forward-looking commitments to ship `/healthz`,
  metrics endpoints, or any of §1.4 forbidden
  categories.
- "Soon" / "in the next release" / "tracked for
  future work" framing applied to forbidden
  categories.
- Premature closure language for Track N itself
  before Step 6 (e.g., "Track N is closed"
  appearing in Step 3 / 4 / 5 artefacts).

---

## §10. Carry-forward invariants / backward compatibility

### §10.1 Tracks A–M runtime invariants

The following files MUST remain byte-identical to
their state at Track M closure commit `a3bdc48`:

- All files enumerated in §8.5 "Production code".
- `pyproject.toml` (`version=0.5.2` preserved;
  `[tool.hatch.build.targets.wheel] packages`
  11-element array preserved).
- All files enumerated in §8.5 "Existing scripts".
- All files enumerated in §8.5 "Existing operator
  recipes".

### §10.2 Track G / H invariants (transport + auth)

Preserved verbatim:

- stdio transport behaviour at
  `_stdio_transport.py:175-212`.
- HTTP transport behaviour at
  `_network_transport.py:300-704`.
- `--transport stdio|http`, `--config-path`,
  `--log-level DEBUG|INFO|WARNING|ERROR`, `--bind
  HOST:PORT`, `--auth-token-env VARNAME` flag
  surface.
- Failure-equivalence on auth (Track H §8.4): every
  auth-failure mode → identical 401 +
  `WWW-Authenticate: Bearer realm="mcp"` +
  JSON-RPC `-32001 / "Unauthorized"`.
- `ProductConfig.auth.tokens` `${ENV:NAME}`
  resolution at runtime boundary.

### §10.3 Track I invariants (installer round-trip)

Preserved verbatim:

- `installer.py:_config_to_dict` emit branch for
  `auth.tokens`.
- Install-time `${ENV:NAME}` round-trip integrity.

### §10.4 Track J invariants (deployment-boundary)

Preserved verbatim:

- `deployment-boundary.md` §6 `/healthz` non-shipping
  defer.
- `deployment-boundary.md` §10 deployment-side
  observability denials.
- TLS / mTLS forbidden in-process.
- Forwarded-header MUST-NOT-consume policy.
- Three deployment scenarios (loopback / private
  subnet / public-facing-through-reverse-proxy).

### §10.5 Track K invariants (smoke harness)

Preserved verbatim:

- `scripts/dev/mcp_client_smoke.py` 341 LOC
  byte-identical.
- Classification as diagnostic file (not runtime
  capability) per Track K §6.

### §10.6 Track L invariants (service supervision)

Preserved verbatim:

- `service-supervision.md` and `mcp-server.service`
  byte-identical.
- `Type=simple` + `Restart=on-failure` +
  `KillSignal=SIGINT` unit-template defaults.
- `runtime.py` is NOT a service manager (Track L
  §4.3).
- §9.3 level-to-event mapping (Track N inherits
  verbatim or by reference).

### §10.7 Track M invariants (packaging / distribution)

Preserved verbatim:

- `distribution-boundary.md` byte-identical.
- `pyproject.toml [tool.hatch.build.targets.wheel]
  packages` 11-element array byte-identical.
- One buildable pure-Python wheel
  (`1c_agent_platform-0.5.2-py3-none-any.whl`)
  artefact class preserved.
- Three `[project.scripts]` console entries
  (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`) byte-identical.

### §10.8 Registry invariant

`scripts/dev/selfcheck.py` MUST report
`registries read=15 / write=25 / intelligence=16`
unchanged at every Track N step.

### §10.9 No new MCP tools

The MCP tool surface is locked to the existing
56-tool inventory (15 + 25 + 16). No tool MAY be
added, removed, or renamed by Track N.

### §10.10 No 1cv8.exe, no real credentials, no remote push

Track N MUST NOT run `1cv8.exe`. Track N MUST NOT
commit real credentials. Track N MUST NOT execute
`git push` to any remote.

---

## §11. Verification contract for Step 4

### §11.1 Pre-commit verification (mandatory)

Before staging the Step 4 commit, the authoring
agent / operator **MUST** run all of:

V1. `git status` shows exactly one new file at the
    path locked in §8.2 (no modified files, no
    deleted files, no renamed files).
V2. `git diff --stat` confirms zero changes to any
    file enumerated in §8.5.
V3. `python scripts/dev/selfcheck.py` exits 0 and
    output line `selfcheck_status = ok` appears.
V4. The output includes `registries read=15 /
    write=25 / intelligence=16` equivalent
    information (parsed from `read_server_tools` /
    `write_server_tools` / `intelligence_server_tools`
    list lengths).
V5. `scripts/release/verify-release.ps1
    -AllowDirtyTree` exits 0 and all 8 named checks
    show `[PASS]` / `[WARN]` (no `[FAIL]`).
V6. Grep over the new file confirms it contains all
    six C2–C7 mandatory elements (per §4.1):
    supported signals list (C2), exit-code-meaning
    table (C3), log-level-to-event mapping (C4),
    triage recipe with ≥ 3 failure modes (C5),
    non-goals enumeration (C6), `/healthz` non-
    shipping cross-reference (C7).
V7. The new file contains at least the seven
    explicit cross-references named in C8.
V8. The new file contains the cross-OS posture
    section per C9.
V9. The new file contains all explicit denial
    phrases per §9.2.
V10. The new file MUST NOT contain real credentials
     (the existing `verify-release.ps1` Credential
     leak guard check covers this; cross-check
     should still apply).
V11. The new file MUST NOT contain premature
     closure language for Track N itself.
V12. The new file MUST NOT contain any of the
     forbidden maturity claims from §9.2 except as
     explicit denials.

### §11.2 Post-commit verification (mandatory)

After the Step 4 commit lands, **MUST** run:

P1. `git status` shows clean working tree.
P2. `git log -1` shows the new commit as the HEAD.
P3. `scripts/release/verify-release.ps1` (no
    `-AllowDirtyTree`) exits 0 and all 8 checks
    PASS on clean tree.
P4. `python scripts/dev/selfcheck.py` exits 0.

### §11.3 Step 5 verification carry-forward

Step 5 alignment commits MUST preserve V1–V12 and
P1–P4 except where Step 5 modifies the specifically
authorised CLASS-1 alignment files (README,
PROJECT-STATUS, possibly `docs/release-handoff.md`,
possibly `apps/platform/README.md`).

### §11.4 Step 6 verification carry-forward

Step 6 closure commit MUST preserve V1–V12 and
P1–P4 except where Step 6 modifies README,
PROJECT-STATUS, CHANGELOG, and (only if Q6 = PATCH)
`pyproject.toml [project] version`. Q6 lock at Step
6 MUST defend one of:
- **NO-BUMP** (default per §13.5 expectation): if
  Step 4 PATH A closed without code change. Mirrors
  Track J / Track K / Track L closure precedents.
- **PATCH** (`0.5.2 → 0.5.3`): explicitly
  prohibited under PATH A because no code change
  occurs.
- **MINOR**: explicitly prohibited by §1.4 (no new
  CLI flag, no new declared surface).
- **MAJOR**: explicitly prohibited by track scope.

Under PATH A, Step 6 Q6 outcome MUST be NO-BUMP.

### §11.5 Forbidden verification proxies

The following do NOT substitute for V1–V12 / P1–P4:

- "I ran the recipe in my head" — not a verification.
- "The recipe looks complete" — not a verification.
- "Step 2 audit said this would work" — Step 2 is
  evidence, not closure proof.
- "The forbidden-files list is mostly intact" — V2
  requires zero modifications, not "mostly intact".

---

## §12. Honest non-goals

### §12.1 Observability platform non-goals

Track N **MUST NOT** introduce:

- An OpenTelemetry SDK dependency or
  instrumentation.
- An OTel collector configuration.
- A `traceparent` / `tracestate` header propagation
  policy.
- A span emission contract.
- A trace ID / request ID propagation contract.
- A trace context sampling policy.

### §12.2 Metrics platform non-goals

Track N **MUST NOT** introduce:

- A `/metrics` HTTP endpoint.
- A `prometheus_client` (or any metrics-library)
  dependency.
- A counter / gauge / histogram / summary metric.
- A push-gateway client.
- A `StatsD` / `DogStatsD` socket emitter.

### §12.3 Dashboard / visualisation non-goals

Track N **MUST NOT** introduce:

- A Grafana dashboard JSON.
- A Tempo / Loki / Jaeger / Mimir / Cortex /
  VictoriaMetrics datasource configuration.
- A Kibana visualisation.
- A custom in-repo dashboard frontend.
- A web UI of any kind.

### §12.4 Alerting / paging / on-call non-goals

Track N **MUST NOT** introduce:

- A PagerDuty integration.
- An Opsgenie integration.
- A Slack alert / webhook configuration.
- An email alert configuration.
- An alerting threshold or rule.

### §12.5 Log-aggregation / SIEM non-goals

Track N **MUST NOT** introduce:

- A `vector` / `fluentd` / `fluent-bit` / `rsyslog`
  / `journal-remote` configuration.
- A Splunk forwarder.
- An Elastic ingestion configuration.
- A SOAR runbook scaffolding.
- A SIEM normalisation pipeline.

### §12.6 Health-endpoint non-goals

Track N **MUST NOT** ship:

- `/healthz`, `/readyz`, `/livez` HTTP endpoint
  (Track J §6 defer preserved).
- A `--healthcheck` CLI subcommand.
- A `health_summary` HTTP endpoint (the existing
  `health_summary` MCP tool on `mcp-read-server`
  remains accessible via MCP only).

### §12.7 Logging-library / format non-goals

Track N **MUST NOT** introduce:

- A `structlog` / `loguru` / `python-json-logger`
  dependency.
- A structured-JSON-line log format.
- A log-field schema or canonical key set.
- A log rotation / persistence policy beyond what
  the OS log facility provides.

### §12.8 Other carry-over non-goals

Track N **MUST NOT** introduce:

- A new MCP tool, new transport, new auth scheme,
  new deployment posture, new service-supervision
  pattern, new packaging format, new entrypoint
  module, new CLI flag, new `[project.scripts]`
  entry, new dependency, new env-var convention.
- A `1cv8.exe` invocation.
- A real-credential commit.
- A remote push.
- A rollback / AST / multi-version 1С matrix
  expansion.

---

## §13. Step 4 handoff note

### §13.1 Allowed Step 4 commit shape

Step 4 commit message subject **MUST** be:

```
Track N / Step 4 — observability and diagnostics recipe
```

(or a close functional equivalent that names the recipe).

Commit body **MUST** cite this contract §§4 / 6 / 8 /
9 / 11 for closure-gate, recipe content, file
surface, denials, and verification respectively.

### §13.2 Allowed Step 4 file change set

Single addition at `docs/operators/observability.md`
(per §8.2). Nothing else.

### §13.3 Recipe authorship guidance (non-normative)

(This subsection is descriptive / advisory, NOT
normative. It is included to make Step 4 authoring
easier without expanding contract scope.)

The recipe SHOULD:

- Open with a one-paragraph "what this is and is
  not" statement, mirroring §1.1 / §1.2 of this
  contract.
- Use tables for the supported-signals
  classification, exit-code meanings, and HTTP
  response shapes.
- Use fenced shell snippets (`bash`, `pwsh`) for
  literal command examples.
- Use abstract placeholders (`<UNIT_NAME>`,
  `<PORT>`, `<TOKEN_ENV_VAR>`, `<SERVER>`) in all
  examples.
- Use Markdown blockquotes for verbatim quotes
  from Track L §9.3 / Track J §6 / Track M §13 to
  make inheritance visible.
- Cross-link back to anchor file paths (e.g.,
  `[docs/operators/deployment-boundary.md
  §6](../operators/deployment-boundary.md#6-healthz-non-shipping)`).

### §13.4 Step 5 handoff expectations

After Step 4, Step 5 (docs / operator / release
alignment) MAY:

- Add at most one narrow bullet to
  `docs/release-handoff.md` pointing at the new
  recipe in the "Where to read deeper" list.
- Add a "Active parallel track: Track N at Step 5"
  / Step 4 transition note in
  `PROJECT-STATUS.md`.
- Add a CLASS-1 Quickstart-paragraph cross-reference
  in `README.md` to the new recipe.
- Modify `apps/platform/README.md` only if its
  troubleshooting prose develops direct factual
  drift from the new recipe content.

Step 5 MUST NOT modify any file in §8.5 except for
the four CLASS-1 alignment files just named.

### §13.5 Step 6 Q6 framing (lock at Step 6)

Under PATH A docs-only, Q6 default expectation =
**NO-BUMP**. Track N closes under existing `0.5.2`
without `pyproject.toml [project] version` change.
Mirrors Track J / Track K / Track L NO-BUMP
precedents:

- Track J — docs-only deployment-boundary recipe →
  Q7 = NO-BUMP.
- Track K — single new diagnostic file under
  `scripts/dev/` → Q7 = NO-BUMP (artefact is
  developer tool, not consumer-visible capability).
- Track L — docs + one declarative systemd unit
  template → Q7 = NO-BUMP (template is operator
  copy-template, not bundled production code).

Track N under PATH A is more like Track J than
Track L: pure docs, no declarative template flip.
Hence the default Q6 framing is NO-BUMP.

Q6 lock is at Step 6; this contract pins the
expectation, not the final lock.

### §13.6 Track N closure target after Step 6

After Track N closure:

- README "Closed parallel tracks" list grows from
  13 entries to 14 (A through N).
- PROJECT-STATUS shows "Активного шага нет" again
  until an operator opens a future track.
- CHANGELOG appends a Track N closure line.
- Fourteen post-phase parallel tracks (A–N) closed
  sequentially.

### §13.7 Forbidden Step 4 / 5 / 6 actions (recap)

Even though §8.5 and §10 are exhaustive, the most-
common Step 4 / 5 / 6 mistakes are explicitly named
here:

- ❌ Adding a `selfcheck.py --json` mode.
  (PATH B; rejected by §7.2.)
- ❌ Adding a canonical startup-banner helper.
  (PATH C; rejected by §7.3.)
- ❌ Touching `_network_transport.py` or
  `_stdio_transport.py`.
  (§10.2; rejected.)
- ❌ Adding `/healthz` "for completeness".
  (§12.6; rejected; Track J §6 defer preserved.)
- ❌ Adding `prometheus_client` "since we're
  documenting metrics anyway".
  (§12.2; rejected.)
- ❌ Bundling a Grafana dashboard JSON
  "as a recommendation".
  (§12.3; rejected.)
- ❌ Touching Track L's
  `service-supervision.md` to "centralise log
  guidance".
  (§10.6 / §8.5; rejected.)
- ❌ Adding a forward-looking sentence
  "Track P will add OTel".
  (§9.3; rejected.)

---

## §14. Honest summary

**What this contract does.** Locks the final
answers to Step 1 plan Q1–Q5 (Q6 framed for Step 6
lock) using repo evidence from Step 2 audit. Pins
Step 4 PATH = PATH A docs-only. Pins the exact
single-file Step 4 deliverable at
`docs/operators/observability.md`. Pins six
mandatory recipe content elements (C2–C7 of §4.1).
Pins the exhaustive forbidden-file surface for Step
4 (§8.5). Pins the verification protocol (§11).
Preserves every Tracks A–M invariant byte-identical
(§10).

**What this contract does not do.** Does not
implement the recipe (Step 4 territory). Does not
align README / PROJECT-STATUS / CHANGELOG (Step 5 /
Step 6 territory). Does not lock Q6 SemVer outcome
(Step 6 territory; framed as NO-BUMP per §13.5).
Does not authorise any of the forbidden categories
in §1.4 / §12.

**Why one normative file is sufficient.** Step 2
established that the gap is integration-and-naming.
Step 3 contracts the integration shape and the
naming discipline in a single document; Step 4
ships the recipe; Step 5 / Step 6 close. Tracks J /
L / M each closed under similar single-contract-
file Step 3 patterns; Track N follows the
established pattern.

**Step 4 is unambiguously specified.** Path:
`docs/operators/observability.md`. Content:
operator-facing diagnostics recipe with six
mandatory elements (C2–C7), seven mandatory cross-
references (C8), cross-OS posture section (C9), and
all explicit denials from §9.2. Cap: ≤ 1200 lines
hard, ≤ 1000 lines RECOMMENDED. Forbidden surface:
exhaustively enumerated in §8.5. Verification:
V1–V12 pre-commit, P1–P4 post-commit.

**No premature closure.** Track N is **active**.
Step 1 / Step 2 / Step 3 are closed; Step 4 / 5 / 6
remain. Phrases enumerated in §9.2 appear in this
contract only as DENIALS or as the verbatim list of
forbidden maturity claims that the recipe must
itself deny.

**Canonical next step.** Parallel Track N / Step 4 —
narrow PATH A implementation: ship
`docs/operators/observability.md` per §4 / §6 / §8.
Opening Step 4 is a separate operator decision; not
auto-opened.
