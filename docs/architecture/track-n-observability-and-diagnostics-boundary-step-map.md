# Parallel Track N — Observability and Diagnostics Boundary — Step Map

Companion to
[track-n-observability-and-diagnostics-boundary-plan.md](track-n-observability-and-diagnostics-boundary-plan.md).
This document defines the six steps of Track N in the
standard format used by Tracks A–M (Goal / What changes /
What does NOT change / Result), plus the track invariants
block and the hard out-of-scope block.

Companion plan locks the directional Q1–Q7 defaults; this
step-map locks the per-step boundary so each step ships
narrowly and verifiably.

---

## Track N invariants

These invariants must hold at every step. They are
verifiable from repo state (grep / `git diff` /
`selfcheck.py` / `verify-release.ps1`) at every commit:

1. **Tracks A–M production code byte-identical.**
   `apps/*/src/`, `packages/*/src/`, in particular
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py`,
   `apps/platform/src/onec_platform/runtime.py`,
   `apps/platform/src/onec_platform/process_control.py`,
   `apps/platform/src/onec_platform/runtime_logs.py`,
   `apps/platform/src/onec_platform/models.py` not
   modified by Steps 1 / 2 / 3 / 5 / 6. Step 4 MAY
   modify production code only if Step 3 contract
   explicitly authorises PATH B / PATH C with code
   surface and names the exact file(s) under the locked
   LOC cap. Default expectation: zero production code
   change across all six Track N steps.
2. **Track K diagnostic harness byte-identical.**
   `scripts/dev/mcp_client_smoke.py` not modified at any
   step.
3. **Track J operator recipe byte-identical.**
   `docs/operators/deployment-boundary.md` not modified
   at any step.
4. **Track L operator recipe + systemd template byte-
   identical.** `docs/operators/service/service-supervision.md`
   and `docs/operators/service/mcp-server.service` not
   modified at any step.
5. **Track M operator recipe + wheel-build flip byte-
   identical.** `docs/operators/packaging/distribution-boundary.md`
   not modified at any step. `pyproject.toml`
   `[tool.hatch.build.targets.wheel] packages = [...]`
   array byte-identical (11 src-layout package paths
   from Track M / Step 4 preserved).
6. **`pyproject.toml`** byte-identical at Steps 1 / 2 /
   3 / 4 / 5. Step 6 MAY further modify `pyproject.toml`
   `version` only if Q6 = PATCH; default expectation
   Q6 = NO-BUMP (Track N closes under existing `0.5.2`).
7. **Registries `read = 15 / write = 25 / intelligence =
   16`** unchanged across all six steps. `selfcheck.py`
   `status=ok` at every step.
8. **`scripts/dev/selfcheck.py`** byte-identical at
   Steps 1 / 2 / 3 / 5 / 6. Step 4 MAY modify
   `selfcheck.py` only if Step 3 contract explicitly
   authorises PATH B (structured-output narrow slice)
   under the locked LOC cap. Default expectation:
   `selfcheck.py` byte-identical at every step.
9. **`scripts/release/install.ps1`**,
   **`scripts/release/verify-release.ps1`**,
   **`scripts/release/_install_runner.py`**,
   **`scripts/dev/bootstrap_paths.ps1`**,
   **`scripts/dev/launch.ps1`**,
   **`scripts/dev/run_dev_check.ps1`**,
   **`scripts/dev/README.md`** byte-identical at every
   step.
10. **`scripts/release/README.md`** byte-identical at
    every step.
11. **`SECURITY.md`** byte-identical at every step
    (Track N does not change the security claim).
12. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow CLASS-1
    updates if the "What is in this handoff" / "What
    is NOT in this handoff" / "Where to read deeper"
    lists develop direct factual drift after Step 4.
    Default expectation Step 5 edit: at most one new
    bullet pointing at the Step 4 recipe.
13. **`apps/platform/README.md`** byte-identical at
    every step (Track N does not change the platform-
    layer boundary inventory).
14. **`CHANGELOG.md`** byte-identical at Steps 1 / 2 /
    3 / 4 / 5. Only Step 6 appends a closure-line for
    Track N.
15. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still ends
    at Track M, thirteen entries). Only Step 6 extends
    it to fourteen entries (A through N).
16. **No new MCP tools** at any step.
17. **No new CLI flag** on any existing MCP server
    entrypoint at any step. The Track G / Track H flag
    surface (`--transport`, `--config-path`,
    `--log-level`, `--bind`, `--auth-token-env`) is
    locked.
18. **No new `[project.scripts]` console entries.** The
    three existing entries (`mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`) are
    locked.
19. **No new dependencies.** Step 4 must not add to
    `[project.dependencies]` or
    `[project.optional-dependencies]`. The stdlib-only
    orientation of `mcp_common` and the three servers
    is preserved.
20. **No new entrypoint module.** No new `__main__.py`
    in any `apps/*/src/` package.
21. **`1c_agent_platform-<VERSION>-py3-none-any.whl`
    artefact class byte-identical** (Track M closure
    state). Step 4 PATH B / C may change wheel-
    contained bytes if it modifies in-wheel code, but
    the **artefact class** (one pure-Python wheel,
    `py3-none-any` platform tag, 11 src-layout
    packages, three `[project.scripts]` console
    entries) is locked.
22. **No `1cv8.exe` runs** at any step.
23. **No real credentials** in any committed text.
24. **No remote push** at any step.
25. **No premature closure language.** Phrases that
    frame Track N as "закрыт" / "closed" / "fully
    solved" / "observability solved forever" /
    "production-ready observability" / "full OTel
    instrumentation" / "Prometheus platform shipped" /
    "distributed tracing ready" / "SIEM-ready" /
    "enterprise-ready observability" may appear in
    Steps 1–5 only as explicit DENIALS. Only Step 6
    introduces closure language for Track N itself.

---

## Track N hard out-of-scope (carry through every step)

These categories must not be addressed by Track N at any
step. Each is named explicitly to prevent silent
expansion:

- No new transport family (no WebSocket, no SSE, no
  TCP, no Unix-socket, no named-pipe).
- No auth-scheme redesign (no JWT, no OAuth, no OIDC,
  no SAML, no SCIM, no RBAC, no ABAC, no per-tool ACL,
  no per-tenant isolation, no multi-tenant).
- No deployment-boundary redesign (Track J invariants
  preserved).
- No service-supervision redesign (Track L invariants
  preserved).
- No packaging redesign (Track M invariants preserved).
- No full OpenTelemetry program — no OTel SDK
  dependency, no OTel collector configuration, no
  per-request span emission, no trace context
  propagation guarantee, no `traceparent` header
  vocabulary added to the HTTP transport.
- No Prometheus / OpenMetrics rollout — no `/metrics`
  endpoint, no Prometheus exporter, no histogram /
  counter / gauge surface, no `prometheus_client`
  dependency.
- No Grafana / Tempo / Loki / Jaeger platform — no
  dashboards bundled in-repo, no datasource
  configuration, no panel JSON.
- No SIEM / SOC integration — no Splunk forwarder, no
  Elastic ingestion config, no SOAR runbook
  scaffolding.
- No distributed tracing — no request-id propagation
  across systems, no trace assembly, no service map.
- No alerting / paging / on-call workflows — no
  PagerDuty / Opsgenie / Slack / email alert rule
  bundled in-repo.
- No `/healthz` / `/readyz` / `/livez` endpoint
  (Track J §8 defer preserved).
- No log-aggregation forwarder — no
  `vector` / `fluentd` / `fluent-bit` / `rsyslog` /
  `journal-remote` configuration bundled in-repo.
- No structured-logging library rollout — no
  `structlog` / `loguru` / `python-json-logger`
  dependency.
- No log-level redesign — the existing `--log-level`
  flag (Track G) is locked; Track N may document its
  semantics but MUST NOT redefine accepted values,
  default, or behaviour.
- No web UI / dashboard frontend.
- No enterprise identity stack.
- No clustering / HA / orchestration platforms.
- No standalone `apps/platform` daemon entrypoint.
- No new MCP tools / registry change.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new dependencies.
- No new entrypoint module.
- No `1cv8.exe` runs.
- No remote push.
- No rollback expansion / AST work / 1С matrix
  expansion.
- No "observability solved forever" / "production-
  ready observability" / "full OTel instrumentation" /
  "Prometheus platform shipped" / "distributed tracing
  ready" / "SIEM-ready" / "enterprise-ready
  observability" / "alerting solved" claim.

---

## Step 1 — planning observability and diagnostics boundary

**Goal.** Open Track N formally with a single planning
document and a single step-map document, plus the
narrative flip on README.md and PROJECT-STATUS.md
required to mark Track N as the active parallel track.
Establish the Q1–Q7 directional defaults without locking
final answers.

**What changes.**
- NEW: `docs/architecture/track-n-observability-and-diagnostics-boundary-plan.md`
  (14-section planning document; Q1–Q7 directional
  recommendations only; honest gap statement; in-scope /
  out-of-scope; guardrails; acceptance criteria;
  relationship table to Tracks G/H/I/J/K/L/M; step
  trajectory).
- NEW: `docs/architecture/track-n-observability-and-diagnostics-boundary-step-map.md`
  (this document — six steps + track invariants block +
  hard out-of-scope block).
- MODIFIED: `README.md` — Quickstart paragraph appended
  with Track N active-planning wording; "Active
  parallel track" section reopened describing Track N
  at Step 1 planning-only; Closed parallel tracks list
  **unchanged** (Track N not moved there yet).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "Активного шага нет" to "Track N / Step 1 active
  planning"; Track M closure block preserved beneath
  byte-identical; one new per-step section "Parallel
  Track N / Step 1 — planning observability and
  diagnostics boundary (завершён)" inserted between
  the existing top-of-status block and the Track M
  closure narrative (or in the canonical equivalent
  location, mirroring prior tracks' per-step section
  placement).

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`, `runtime.py`, `process_control.py`,
  `runtime_logs.py`, `models.py`).
- `pyproject.toml` (`version=0.5.2` preserved; wheel-
  build `packages = [...]` 11-element array
  preserved).
- `scripts/*` — all existing files byte-identical
  (including `selfcheck.py`, `verify-release.ps1`,
  `install.ps1`, `_install_runner.py`, `launch.ps1`,
  `bootstrap_paths.ps1`, `run_dev_check.ps1`).
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/service-supervision.md`,
  `docs/operators/service/mcp-server.service`,
  `docs/operators/packaging/distribution-boundary.md`,
  `CHANGELOG.md` — byte-identical.
- All Tracks A–M architecture docs — byte-identical.
- Registries `read=15 / write=25 / intelligence=16`.
- README Closed parallel tracks list (still ends at
  Track M, thirteen entries).
- No `1cv8.exe` runs.
- No real credentials.
- No remote push.
- No Step 2 opening.

**Result.** Track N is formally open at Step 1. The
plan document fixes Q1–Q7 as defaults / directional
recommendations. The step-map document (this file)
fixes the six-step boundary. Operator can read the plan
and step-map and know exactly what Track N will and
will not do. README and PROJECT-STATUS reflect the
active-track flip. No code change anywhere; no
`pyproject` change; registry invariant carried through;
selfcheck green; `verify-release.ps1` green on 8
checks.

---

## Step 2 — baseline audit of current observability / diagnostics state

**Goal.** Produce a single descriptive (not
prescriptive) audit document inventorying the current
state of observability / diagnostics surfaces in the
repo; classify the inventory into the standard 4-class
breakdown (already-reusable / adjacent-but-insufficient
/ clearly-missing / explicitly-out-of-scope); produce
Q1–Q5 directional resolutions grounded in evidence;
produce a handoff list for Step 3 contract
consumption.

**What changes.**
- NEW: `docs/architecture/track-n-observability-and-diagnostics-boundary-baseline-audit.md`
  — single descriptive audit document. Default
  expectation = 8–12 sections, ≤ 1500 lines. Sections
  must cover: inventory of stderr emission across the
  three MCP server entrypoints (which startup banner
  lines are emitted, where in code, with what shape);
  inventory of exit-code paths (`SystemExit` /
  `KeyboardInterrupt` / unhandled-exception /
  config-load-failure / auth-config-failure); inventory
  of `selfcheck.py` output shape (single-line status +
  structured summary block); inventory of
  `verify-release.ps1` output shape (8 per-check
  PASS/FAIL lines); inventory of `mcp_client_
  smoke.py` output shape (structured progress lines);
  inventory of HTTP transport auth-failure responses
  (Track H 401 + `WWW-Authenticate: Bearer realm="mcp"`
  + JSON-RPC `-32001`); inventory of install
  fast-path output shape (`command_preview` +
  password-position redaction per Track D); inventory
  of Track L systemd integration observation surface
  (`systemctl status` / `journalctl -u`); whole-repo
  grep for observability-vocabulary terms (`log`,
  `logging`, `INFO`, `WARN`, `ERROR`, `DEBUG`,
  `--log-level`, `selfcheck`, `verify`, `triage`,
  `troubleshoot`, `diagnostic`, `health`,
  `monitoring`, `metrics`, `tracing`, `prometheus`,
  `otel`, `opentelemetry`, `jaeger`, `tempo`, `loki`,
  `grafana`, `siem`); 4-class breakdown; Q1–Q5
  directional resolutions; Step 3 handoff list (≥ 10
  items).

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`,
  `docs/operators/packaging/distribution-boundary.md`.
- README and PROJECT-STATUS — Step 2 is the audit
  step.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 2 produces a single descriptive audit
document. No prescriptive language; no MUST / MUST
NOT / SHOULD lock. All "decisions" stay as directional
recommendations to be locked by Step 3 contract.

---

## Step 3 — observability / diagnostics contract

**Goal.** Produce a single normative (prescriptive)
contract document using RFC 2119 MUST / MUST NOT /
SHOULD / SHOULD NOT / MAY language. Lock Q1–Q6 final
answers (Q6 deferred to Step 6 but framed). Lock Step 4
PATH (A docs-only / B docs + narrow structured-output
slice / C docs + narrow log-shape contract code
slice). Lock Step 4 file-surface cap (default ≤ 3
touched files). Lock Step 4 LOC cap for any code-
bearing artefact (default ≤ 200 LOC stdlib-only, no
new dependencies). Lock Step 4 forbidden-files list.
Lock Step 5 forbidden-files list. Lock the closure-
gate scenario (diagnostic surface boundary, triage
recipe coverage, machine-readable signal — if any).

**What changes.**
- NEW: `docs/architecture/track-n-observability-and-diagnostics-boundary-contract.md`
  — single normative contract document with RFC 2119
  language. Default expectation = 10–15 sections,
  ≤ 1700 lines.

**What does NOT change.**
- All production code.
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`,
  `docs/operators/packaging/distribution-boundary.md`.
- README / PROJECT-STATUS narrative beyond at most a
  single CLASS-1 wording update.
- Registries.
- No 1cv8.exe runs.
- No remote push.

**Result.** Step 3 closes with the prescriptive
contract in place. Step 4 has a closure-gate scenario,
a file surface, a LOC cap, a forbidden-files list, and
a verification protocol — all locked.

---

## Step 4 — narrow implementation slice

**Goal.** Operationalize the Step 3 contract by
shipping the locked Step 4 artefact(s) under the
locked path and cap. Default expectation = PATH A (one
operator-facing recipe under `docs/operators/
observability/` or whichever path Step 3 contract
locks; no code change) **if** Step 2 audit confirms
PATH A is sufficient to close the §3 gap. PATH B
(docs + one narrow structured-output slice ≤ 200 LOC
stdlib-only) or PATH C (docs + one narrow log-shape
contract slice ≤ 200 LOC stdlib-only) only if Step 3
contract explicitly authorises them and names the
exact file(s).

**What changes (default expectation, PATH A).**
- NEW: operator-facing observability / diagnostics
  recipe under `docs/operators/observability/` (or
  whichever path Step 3 contract locks). Default
  expectation = 6–14 sections, ≤ 1200 lines.
  Sections cover: purpose; scope statement (what
  diagnostic surface ships, what does NOT ship);
  first-class diagnostic surface enumeration (stderr
  emission with shape per server, exit codes with
  meaning table, `selfcheck.py` status output,
  `verify-release.ps1` 8-check output, HTTP transport
  auth-failure response shape, install fast-path
  output with redaction, Track L systemd integration
  observation commands); recommended-only surface
  enumeration (e.g., `mcp_client_smoke.py` as Track K
  closure-defined diagnostic file); triage recipe
  (3–5 canonical failure modes end-to-end); cross-OS
  posture (Linux/systemd/journald primary,
  Windows/macOS cross-OS prose); honest non-goals
  enumeration (full OTel / Prometheus / Grafana /
  Tempo / Loki / Jaeger / SIEM / distributed tracing /
  alerting / on-call / `/healthz` / log-aggregation
  forwarder / structured-logging library); cross-
  references to Tracks G/H/I/J/K/L/M.

**What changes (alternative, PATH B — if Step 3
contract authorises).**
- NEW: operator-facing observability / diagnostics
  recipe (as above).
- MODIFIED: `scripts/dev/selfcheck.py` — narrow
  structured-output slice (e.g., `--json` mode) that
  emits the existing status + summary in a single
  JSON-lines record. Default expectation: ≤ 50 LOC
  net addition, stdlib-only (`json` module), no
  redesign of the existing default text output.

**What changes (alternative, PATH C — if Step 3
contract authorises).**
- NEW: operator-facing observability / diagnostics
  recipe (as above).
- MODIFIED: `packages/mcp-common/src/mcp_common/`
  (single helper module or function added; ≤ 100 LOC
  stdlib-only) implementing the canonical startup-
  banner line shape.
- MODIFIED: `apps/mcp-read-server/src/mcp_read_server/
  __main__.py`,
  `apps/mcp-write-server/src/mcp_write_server/
  __main__.py`,
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/
  __main__.py` — each MCP server entrypoint calls the
  new helper to emit the canonical startup-banner
  line. Default expectation: ≤ 5 LOC net change per
  entrypoint.

**What does NOT change.**
- Production code (`apps/*/src/`, `packages/*/src/`,
  `_stdio_transport.py`, `_network_transport.py`,
  `installer.py`, `runtime.py`, `process_control.py`,
  `runtime_logs.py`, `models.py`) — UNLESS Step 3
  contract PATH B/C explicitly authorises a named
  file.
- `pyproject.toml` (`version=0.5.2` preserved; wheel-
  build `packages = [...]` array preserved).
- `scripts/dev/mcp_client_smoke.py` byte-identical.
- `scripts/release/install.ps1`,
  `scripts/release/verify-release.ps1`,
  `scripts/release/_install_runner.py`,
  `scripts/dev/bootstrap_paths.ps1`,
  `scripts/dev/launch.ps1`,
  `scripts/dev/run_dev_check.ps1` byte-identical.
- `docs/operators/deployment-boundary.md` byte-
  identical.
- `docs/operators/service/service-supervision.md` and
  `docs/operators/service/mcp-server.service` byte-
  identical.
- `docs/operators/packaging/distribution-boundary.md`
  byte-identical.
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `README.md`, `PROJECT-STATUS.md` — Step 4 is the
  implementation step; closure-doc updates belong to
  Step 5 / Step 6.
- Track N Step 1 / Step 2 / Step 3 docs byte-
  identical.
- Registries.
- No new MCP tools.
- No new CLI flag on existing servers.
- No new `[project.scripts]` console entries.
- No new dependencies.
- No new entrypoint module.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Step 4 ships the locked artefact(s). Track
N's diagnostic surface boundary is now operator-readable
end-to-end. Production code byte-identical to Track M
closure state (default PATH A) OR narrowly modified
under the locked LOC cap (PATH B/C). Registry
invariant carried through. `selfcheck.py` green.
`verify-release.ps1` green on 8 checks.

---

## Step 5 — docs / operator / release alignment

**Goal.** Bring narrow CLASS-1 alignment edits to
README / PROJECT-STATUS / possibly
`docs/release-handoff.md` / possibly
`apps/platform/README.md` so that operator-facing
narrative reflects the Step 4 reality without
introducing new code, new declared surface, or new
dependencies. Step 5 is a docs-only step.

**What changes.**
- POSSIBLY MODIFIED: `README.md` — narrow CLASS-1
  wording updates only (e.g., Quickstart paragraph
  hint that Track N observability/diagnostics recipe
  exists; "Active parallel track" section updated to
  reflect Step 5 progress). Closed parallel tracks
  list **unchanged**.
- POSSIBLY MODIFIED: `PROJECT-STATUS.md` — one new
  per-step section "Parallel Track N / Step 5 — docs /
  operator / release alignment (завершён)" inserted
  in the canonical location.
- POSSIBLY MODIFIED: `docs/release-handoff.md` — at
  most one new bullet pointing at the Step 4 recipe in
  the "Where to read deeper" list; rewrite of any
  pre-existing "no observability story" sentence if
  one exists.
- POSSIBLY MODIFIED: `apps/platform/README.md` — at
  most one new cross-link if the platform-layer
  troubleshooting prose develops direct factual drift
  from Step 4 recipe content.

**What does NOT change.**
- All production code (`apps/*/src/`,
  `packages/*/src/`).
- `pyproject.toml`.
- All `scripts/*` files.
- `SECURITY.md` byte-identical.
- `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`,
  `docs/operators/packaging/distribution-boundary.md`,
  Track N Step 4 recipe — byte-identical.
- All Tracks A–M architecture docs — byte-identical.
- Track N Step 1 / Step 2 / Step 3 / Step 4 docs
  byte-identical.
- `CHANGELOG.md` byte-identical.
- README Closed parallel tracks list (still ends at
  Track M).
- Registries.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Operator-facing narrative aligned with
post-Step-4 reality. No code change. No new declared
surface. Track N still **not** closed (Step 6
remaining).

---

## Step 6 — final integration pass and track closure

**Goal.** Land the final integration pass that
explicitly closes Track N. Update README Closed
parallel tracks list from 13 entries to 14 (A through
N). Add Track N closure narrative to PROJECT-STATUS.
Append Track N closure line to CHANGELOG.md. Lock Q6
(NO-BUMP if Step 4 = PATH A; PATCH if Step 4 = PATH
B/C and the artefact closes a clearly defect-class
diagnostic-surface gap). Carry every Tracks A–M
invariant byte-identical.

**What changes.**
- MODIFIED: `README.md` — Closed parallel tracks list
  extended from 13 to 14 entries (Track N added at
  the bottom); "Active parallel track" section flipped
  back to "no active track" wording; Quickstart
  paragraph updated to reflect Track N closure;
  "Track N detail (закрыт)" section added (mirror of
  existing Tracks A–M detail sections in length and
  shape).
- MODIFIED: `PROJECT-STATUS.md` — header flipped from
  "Track N / Step <previous>" to "Активного шага
  нет"; Track N closure narrative added beneath top-
  of-status; six per-step sections for Track N
  finalised.
- MODIFIED: `CHANGELOG.md` — one Track N closure
  line appended (mirror of Track A–M closure lines in
  shape); version bumped per Q6 lock.
- POSSIBLY MODIFIED: `pyproject.toml` — `version`
  bumped only if Q6 = PATCH (`0.5.2 → 0.5.3`); other
  fields byte-identical.

**What does NOT change.**
- All production code (`apps/*/src/`,
  `packages/*/src/`) — byte-identical to Step 4
  state (which, under default PATH A, is byte-
  identical to Track M closure state).
- All `scripts/*` files — byte-identical to Step 4
  state.
- `SECURITY.md` byte-identical.
- `docs/operators/deployment-boundary.md`,
  `docs/operators/service/*`,
  `docs/operators/packaging/distribution-boundary.md`,
  Track N Step 4 recipe — byte-identical.
- All Tracks A–M architecture docs — byte-identical.
- Track N Step 1 / Step 2 / Step 3 / Step 4 / Step 5
  docs byte-identical.
- `docs/release-handoff.md` byte-identical to Step 5
  state.
- `apps/platform/README.md` byte-identical to Step 5
  state.
- Registries.
- No new MCP tools / registry change.
- No new CLI flag / new declared surface.
- No new dependencies.
- No `1cv8.exe` runs.
- No remote push.

**Result.** Track N closed. Fourteen post-phase
parallel tracks (A through N) closed sequentially.
README Closed parallel tracks list updated. Q6 locked.
Operator-facing narrative reflects Track N closure.
Selfcheck green; verify-release.ps1 green on 8 checks;
no real credentials; no `1cv8.exe`; no remote push.
