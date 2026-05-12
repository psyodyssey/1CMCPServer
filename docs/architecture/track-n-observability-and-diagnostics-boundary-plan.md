# Parallel Track N — Observability and Diagnostics Boundary — Plan

**Track status at the time of this document.** Parallel
Track N opens as the fourteenth post-phase parallel track
after Track M closure (commit `a3bdc48`). Step 1 — planning
only; documentation-only. No production code change. No
`pyproject.toml` change. No `scripts/*` change. No registry
change. No `1cv8.exe` runs. No remote push.

**Track N positioning relative to Tracks A–M.** Tracks A–M
closed sequentially as thirteen post-phase parallel tracks
(A real-write-path, B productization, C packaging, D
credentials hardening, E version-matrix scaffolding, F
rollback expansion, G stdio transport + CLI, H HTTP
transport + bearer auth, I installer auth round-trip
integrity, J TLS and reverse-proxy deployment boundary, K
real MCP client integration test, L service supervision and
OS service registration, M packaging ecosystem and
distribution boundary). After Track M closure the platform
has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer auth
  (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip integrity
  (Track I);
- an operator-facing deployment-boundary recipe at
  `docs/operators/deployment-boundary.md` (Track J);
- a real MCP client smoke harness at
  `scripts/dev/mcp_client_smoke.py` (Track K);
- an operator-facing service-supervision recipe at
  `docs/operators/service/service-supervision.md` plus a
  declarative systemd unit-file template at
  `docs/operators/service/mcp-server.service` (Track L);
- a single buildable pure-Python wheel
  (`1c_agent_platform-0.5.2-py3-none-any.whl`) plus an
  operator-facing distribution-boundary recipe at
  `docs/operators/packaging/distribution-boundary.md`
  (Track M).

What it still does **not** have is a first-class
"how-this-product-is-observed" story.

---

## §1. Purpose — why this track exists

Track N exists to convert the current honest gap

> "the platform **runs**, can be **authenticated**,
> **installed**, **deployed**, **supervised**, **packaged**
> and **verified**, but it does not yet have a formal
> **observability / diagnostics boundary** an operator can
> read end-to-end"

into a disciplined six-step closure track using the same
shape as Tracks A–M (planning → audit → contract → narrow
implementation → docs alignment → final integration pass).

Every prior post-phase track left "full observability
stack" in its honest-non-goals list. Track J / Step 3
contract §13 enumerated "full observability stack" as
forbidden carry-through; Track L / Step 6 closure repeated
"не full observability stack"; Track M / Step 6 closure
repeated the same denial. Each track was right to deny it
within its own scope. Track N is the dedicated narrow
track that finally answers the operator-facing question

> "When this product misbehaves in operation, what
> diagnostic surface am I supposed to consult, and where
> is the supported boundary between today's stderr /
> journald / process-state signals and a hypothetical
> future full observability stack?"

The track is **not** justified by a defect — there is no
broken behaviour. It is justified by an **operator-
diagnostics-ergonomics gap**: today's diagnostic surface
exists ad-hoc (stderr from each MCP server process, exit
codes from `selfcheck.py` and `verify-release.ps1`,
auth-failure 401 responses from the HTTP transport, the
real MCP client smoke harness output) but no document
tells an operator which of those signals are first-class,
which are recommended-only, and what they do NOT add up to.

---

## §2. Current post-Track-M baseline

The relevant baseline for Track N (as of `a3bdc48`):

### §2.1 Diagnostic surfaces that exist today

- **stderr from each MCP server process** — stdio and HTTP
  transports both surface startup banners, config-load
  errors, auth-config errors, and per-request errors via
  the standard stderr stream. Track G / Step 4 wired the
  stdio transport to emit a single startup line ("ready"
  shape); Track H / Step 4 added the HTTP listener startup
  banner including `--bind <HOST>:<PORT>`.
- **exit codes** — `python -m mcp_<server>` exits with
  non-zero on config-load failure, auth-config failure
  (e.g., `--auth-token-env VAR` pointing at an unset env
  var, when `--transport http`), and on `KeyboardInterrupt`
  / `SIGINT` (graceful shutdown path Track L unit template
  routes through `KillSignal=SIGINT`).
- **`scripts/dev/selfcheck.py`** — emits a single-line
  status (`selfcheck_status=ok`) plus a structured summary
  block (`read=15 / write=25 / intelligence=16`,
  `imports_ok=true`). The umbrella `scripts/dev/launch.ps1
  selfcheck` wraps it.
- **`scripts/release/verify-release.ps1`** — 8-check
  release-side gate. Prints per-check PASS/FAIL lines and
  exits non-zero on any failure.
- **`scripts/dev/mcp_client_smoke.py`** (Track K) — stdlib-
  only 341-LOC stand-alone harness that exercises
  `initialize` + `tools/list` + read-only `tools/call`
  round-trip plus an HTTP missing-`Authorization` probe;
  prints structured progress lines and exits non-zero on
  any assertion failure.
- **HTTP transport auth-failure responses** — Track H /
  Step 4 wired the HTTP `/mcp` endpoint to return
  `401 Unauthorized` with `WWW-Authenticate: Bearer
  realm="mcp"` and JSON-RPC error `-32001` on
  missing/empty/malformed/invalid bearer; the failure shape
  itself is a diagnostic surface (visible in reverse-proxy
  access logs and in client-side error messages).
- **install fast-path output** — `scripts/release/
  install.ps1` prints `command_preview` lines (password-
  position redacted per Track D) and exits non-zero on
  config-load or write failure.
- **Track L systemd integration** — `Type=simple` +
  `Restart=on-failure` + `KillSignal=SIGINT` means
  `systemctl status mcp-server` and `journalctl -u
  mcp-server` are the recommended operator-side observation
  surface on Linux/systemd hosts; cross-OS prose covers
  Windows NSSM (`nssm status`) and macOS launchd
  (`launchctl print`) at recipe level.

### §2.2 What is **not** in the repo today

- **No single document tells operators which of the §2.1
  surfaces are first-class.** There is no
  `docs/operators/observability.md` or
  `docs/operators/diagnostics.md`.
- **No documented triage recipe** for "the MCP server
  exited non-zero" / "the MCP server is up but returns
  401 to every request" / "selfcheck failed" / "wheel
  install succeeded but `mcp-read-server --help` is not on
  PATH". Each of these is recoverable today but the path
  is not in one place.
- **No documented relationship between stderr and journald
  on Track L systemd hosts.** Track L recipe says
  `journalctl -u mcp-server` shows logs; it does not
  state which lines are first-class diagnostic signals
  vs. incidental output.
- **No log-shape contract.** There is no statement of
  format (free-text, key=value, JSON-lines, structured),
  no statement of severity levels (`INFO` / `WARN` /
  `ERROR`), no statement of which fields (if any) are
  guaranteed to appear.
- **No diagnostic-artefact contract for failure triage.**
  There is no `--diagnostic-bundle` flag, no `selfcheck
  --json` mode, no operator-readable failure-fingerprint
  output.
- **No statement of what observability the product does
  NOT ship.** Track J / Track L / Track M each denied
  "full observability stack" in their own scope; no
  central document collects those denials.
- **No machine-readable health signal.** No `/healthz`,
  no `/readyz`, no `/livez`, no exit-code-as-health
  table; Track J / Step 3 contract §8 explicitly deferred
  `/healthz`.
- **No metrics surface.** No Prometheus exposition, no
  OpenMetrics endpoint, no statsd / dogstatsd surface;
  no metric counters / gauges / histograms anywhere in
  code.
- **No tracing surface.** No OpenTelemetry instrumentation,
  no `X-Request-ID` propagation guarantee, no
  per-request correlation id.

### §2.3 What Track N therefore must close

A first-class "observability / diagnostics boundary": a
single operator-facing recipe (or contract document) that
enumerates the §2.1 surfaces, classifies which are
first-class supported diagnostic signals vs. recommended-
only vs. out-of-scope, and states what the product does
NOT promise. Optionally — and only if Step 3 contract
explicitly authorises it — one narrow code-bearing slice
that materially improves a single diagnostic surface (the
default candidate, per Q2 defaults below, is a
`selfcheck --json` mode or equivalent structured-output
narrow slice; PATH A docs-only remains the fallback).

The track must close that gap **honestly**: it does not
promise "observability solved forever", does not promise
"full OpenTelemetry instrumentation", does not promise
"Prometheus / Grafana platform", does not promise
"distributed tracing", does not promise "SIEM integration",
does not promise "alerting / paging / on-call story". It
promises **one** documented observability/diagnostics
boundary plus (optionally, depending on Step 3 contract
PATH selection) at most one narrow diagnostic artefact,
preserving every Track G / H / I / J / K / L / M invariant
byte-identical.

---

## §3. Honest gap statement

Five observations, each independently verifiable in the
repo at `a3bdc48`:

1. **No central observability document.** Whole-repo glob
   for `docs/operators/observability*`,
   `docs/operators/diagnostics*`,
   `docs/operators/logging*`, `docs/operators/triage*`
   returns zero files. The single source of operator
   guidance under `docs/operators/` after Track M
   closure is the deployment-boundary recipe (Track J),
   the service-supervision recipe (Track L), and the
   distribution-boundary recipe (Track M) — none of
   which take "observe operational behaviour" as their
   primary axis.
2. **No log-shape contract.** Whole-repo grep for
   `logging.basicConfig`, `getLogger`, `INFO`, `WARN`,
   `ERROR`, `DEBUG`, `--log-level` (existing CLI flag,
   added Track G) returns scattered usages with no
   declared format. The `--log-level` flag exists on
   each MCP server entrypoint but no document tells
   operators what each level produces or which level
   is the supported default for production operation.
3. **No documented triage recipe.** Whole-repo grep for
   `triage`, `troubleshoot`, `failure mode`, `exit
   code`, `non-zero exit` returns scattered references
   in `apps/platform/README.md` (the troubleshooting
   sub-section is product-layer scoped, not operator-
   layer scoped) and in Track K / Track L recipe text
   (each within its own narrow scope). No single
   document collects "the MCP server exited X — what
   to do" / "the MCP server returns 401 — what to
   check" / "selfcheck failed — what to inspect" as
   first-class operator content.
4. **No machine-readable health signal documented.**
   The product has no `/healthz`, no exit-code-as-
   health table, no `selfcheck --json` mode, no
   structured failure fingerprint. The `--help` and
   `-V` / `--version` flags (where present) are
   diagnostic-adjacent but not first-class health
   signals.
5. **No central non-goals document.** Track J / Track L /
   Track M each contain "не full observability stack"
   in their per-track non-goals. No single document
   collects the "what observability we do NOT ship"
   discipline as an operator-facing contract.

The gap is real. It is not papered over by Track L
recipe's `journalctl -u mcp-server` reference (which
states the command, not the signal vocabulary), nor by
Track K's `mcp_client_smoke.py` harness (which exercises
the transport surface, not operator-facing triage), nor
by `selfcheck.py` (which checks registry counts, not
runtime operability).

---

## §4. Why this gap is real and not already solved

Each of the following candidate "we already have this"
arguments is rejected from repo evidence:

- **"`selfcheck.py` IS the diagnostic surface."**
  `selfcheck.py` checks build-time invariants (registry
  counts match expectations, imports succeed). It is a
  pre-flight gate, not a runtime triage tool. It cannot
  diagnose "the HTTP listener is bound to the wrong
  interface", "auth token resolves to an empty value",
  "the upstream reverse proxy is forwarding the wrong
  Host header", "the systemd unit is restarting in a
  loop". Different layer.
- **"`verify-release.ps1` IS the diagnostic surface."**
  Same response — it is a release-side gate, not a
  runtime triage tool. Eight checks; none of them
  cover runtime operability.
- **"`mcp_client_smoke.py` (Track K) IS the diagnostic
  surface."** Track K / Step 6 closure explicitly framed
  the harness as a **developer / operator diagnostic
  file under `scripts/dev/`**, parallel to `selfcheck.py`,
  not a runtime capability. It exercises the transport;
  it does not triage failures end-to-end. Different
  layer.
- **"stderr / journald IS the observability surface."**
  Operationally true — but the stderr emission today is
  ad-hoc (different shapes from different code paths,
  no severity classification, no structured fields, no
  guarantee what is INFO-class vs. ERROR-class). Reading
  stderr without a contract is not first-class
  observability; it is luck.
- **"Track L recipe already covers this on systemd."**
  Track L recipe mentions `journalctl -u mcp-server` as
  the command. It does not enumerate what diagnostic
  signals operators should look for in that output. The
  recipe is a service-supervision recipe, not an
  observability recipe.
- **"Operators write their own observability."** True
  but evades the gap. The same logic would have rejected
  Track J's deployment-boundary recipe ("operators can
  write their own nginx config") or Track L's recipe
  ("operators can write their own systemd unit"). Track
  N's purpose is to define **one** supported
  observability/diagnostics boundary in-repo so operators
  do not need to invent it.
- **"Track J / Track L / Track M already deny full
  observability."** True — and each was right to do so
  within its own scope. None of them positively defines
  what the supported diagnostic surface IS; they only
  deny what it is NOT. Denials without a positive
  contract are insufficient.

---

## §5. Goal of the track

By Step 6 closure, Track N must have delivered:

1. A single normative observability / diagnostics
   contract (Step 3) that pins the closure-gate scope,
   the supported diagnostic surface (or explicit "no
   artefact — diagnostics boundary documented only"),
   the file surface for Step 4, and the verification
   protocol.
2. Either a single operator-facing observability /
   diagnostics recipe **or** a single narrow code-
   bearing diagnostic artefact (e.g., `selfcheck
   --json` mode) **or** a hybrid — depending on Step 3
   Q2 / Q3 lock. Step 4 is the only step that may add
   code beyond docs.
3. Honest closure narrative in README / PROJECT-STATUS /
   CHANGELOG that documents what observability /
   diagnostics boundary Track N settled, what it
   explicitly did NOT solve, and what remains operator-
   supplied (e.g., metrics platform / tracing platform /
   alerting / on-call rotation).
4. Preserved byte-identical runtime and existing
   artefacts: Track G stdio path, Track H HTTP path,
   Track I installer round-trip, Track J reverse-proxy
   posture, Track K diagnostic harness, Track L service-
   supervision recipe + systemd template, Track M
   distribution-boundary recipe + wheel-build flip — all
   unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation, docs-
  alignment, and closure for observability and
  diagnostics boundary of the existing platform.
- Defining what counts as a "supported operator-visible
  diagnostic surface" concretely for this repo (which of
  the §2.1 surfaces are first-class, which are
  recommended-only, which are out-of-scope).
- Defining a log-shape boundary at the level the project
  honestly supports today (e.g., "stderr free-text plus
  exit codes per documented table"); narrower than a
  structured-logging redesign.
- Defining a triage recipe ("the MCP server exited X" /
  "the MCP server returns 401" / "selfcheck failed")
  that points operators at existing signals without
  inventing new ones.
- Defining whether Step 4 targets:
  - **PATH A** — observability/diagnostics docs only (no
    code change; recipe formalises today's signals with
    explicit non-goals);
  - **PATH B** — docs + one narrow code-bearing
    diagnostic artefact (default candidate: `selfcheck
    --json` mode or equivalent structured-output narrow
    slice ≤ 200 LOC stdlib-only);
  - **PATH C** — docs + one narrow log-shape contract
    code slice (e.g., a single canonical startup-banner
    line shape applied symmetric across the three MCP
    servers).
- Defining whether observability stays cross-OS neutral
  or names one primary implementation-covered observation
  target (Linux/systemd/journald is the default candidate,
  symmetric to Track L's primary OS-family).
- Defining how observability relates to current
  transport / auth / installer / deployment / service /
  packaging truths (cross-references only; no redesign).
- Preserving compatibility with all Tracks G / H / I /
  J / K / L / M invariants.

## §7. What is out of scope

The following are intentionally **not** Track N scope.
Each is denied explicitly to prevent silent expansion:

- **No new MCP tools.** Registry invariant `read = 15 /
  write = 25 / intelligence = 16` must carry through all
  six Track N steps.
- **No registry changes** of any kind.
- **No transport redesign.** Track G stdio + Track H HTTP
  preserved byte-identical.
- **No auth redesign.** Track H static bearer + Track I
  round-trip integrity + Track D `${ENV:NAME}`
  substitution preserved byte-identical.
- **No deployment-boundary redesign.** Track J reverse-
  proxy / TLS-termination model preserved byte-identical.
- **No service-supervision redesign.** Track L recipe +
  systemd template preserved byte-identical.
- **No packaging redesign.** Track M wheel-build flip +
  recipe preserved byte-identical. No new
  `[project.scripts]` entry. No new dependency.
- **No new transport family.** No WebSocket, no SSE, no
  Unix-socket, no named-pipe.
- **No full OpenTelemetry program.** No OTel SDK
  dependency, no OTel collector configuration, no
  per-request span emission, no trace context
  propagation guarantee, no `traceparent` header
  vocabulary added to the HTTP transport.
- **No Prometheus / OpenMetrics rollout.** No
  `/metrics` endpoint, no Prometheus exporter, no
  histogram / counter / gauge surface, no
  `prometheus_client` dependency.
- **No Grafana / Tempo / Loki / Jaeger platform.** No
  dashboards bundled in-repo, no datasource
  configuration, no panel JSON.
- **No SIEM / SOC integration.** No Splunk forwarder,
  no Elastic ingestion config, no SOAR runbook
  scaffolding.
- **No distributed tracing.** No request-id propagation
  across systems, no trace assembly, no service map.
- **No alerting / paging / on-call workflows.** No
  PagerDuty / Opsgenie / Slack / email alert rule
  bundled in-repo.
- **No web UI / dashboard frontend** bound to the
  observability story.
- **No `/healthz` / `/readyz` / `/livez` endpoint.**
  Track J / Step 3 contract §8 defer preserved.
- **No log-aggregation forwarder.** No
  `vector` / `fluentd` / `fluent-bit` / `rsyslog` /
  `journal-remote` configuration bundled in-repo.
- **No structured-logging library rollout.** No
  `structlog` / `loguru` / `python-json-logger`
  dependency.
- **No log-level redesign of `--log-level`.** The flag
  exists since Track G; Track N may document its
  semantics, but MUST NOT redefine its accepted values,
  default, or behaviour.
- **No new CLI flag on existing servers.** No new
  `--log-format`, `--log-output`, `--diagnostic-bundle`,
  `--healthcheck`, or sibling flag added by Track N.
  The Track G / H flag surface is locked.
- **No new entrypoint module.** No new `__main__.py` in
  any `apps/*/src/` package.
- **No new dependencies.** Step 4 must not add to
  `[project.dependencies]` or
  `[project.optional-dependencies]`. The existing
  stdlib-only orientation of `mcp_common` and the three
  servers is preserved.
- **No enterprise identity stack** bound to the
  observability story.
- **No rollback expansion / AST work / 1С matrix
  expansion.**
- **No `1cv8.exe` runs.**
- **No remote push.** GitHub push remains operator
  decision.
- **No "observability solved forever" / "production-
  ready observability" / "full OTel instrumentation" /
  "Prometheus platform shipped" / "distributed tracing
  ready" / "SIEM-ready" / "enterprise-ready
  observability" claim.** Such phrases may appear in
  Track N docs only as explicit denials.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1 commit
and must remain verifiable through Step 6:

1. **Tracks A–M invariants byte-identical.** `apps/*/src/`,
   `packages/*/src/`, in particular
   `packages/mcp-common/src/mcp_common/_stdio_transport.py`,
   `packages/mcp-common/src/mcp_common/_network_transport.py`,
   `apps/platform/src/onec_platform/installer.py`,
   `apps/platform/src/onec_platform/runtime.py`,
   `apps/platform/src/onec_platform/process_control.py`,
   `apps/platform/src/onec_platform/runtime_logs.py`,
   `apps/platform/src/onec_platform/models.py`,
   `scripts/dev/mcp_client_smoke.py`,
   `docs/operators/deployment-boundary.md`,
   `docs/operators/service/service-supervision.md`,
   `docs/operators/service/mcp-server.service`,
   `docs/operators/packaging/distribution-boundary.md`
   not touched by Steps 1 / 2 / 3 / 5 / 6. Step 4 may
   modify production code **only** if Step 3 contract
   explicitly authorises PATH B with code surface and
   names the exact file under the locked LOC cap.
2. **`pyproject.toml`** byte-identical at Steps 1 / 2 /
   3 / 4 / 5. Step 6 MAY further modify
   `pyproject.toml` `version` only if Q7 = PATCH or
   MINOR; default expectation Q7 = NO-BUMP if Step 4
   PATH A; Q7 = PATCH considered only if Step 4 ships
   a code-bearing diagnostic artefact (PATH B / C)
   that closes an honestly defect-class diagnostic
   gap.
3. **Registries invariant.** `selfcheck.py` registries
   `read=15 / write=25 / intelligence=16` must remain
   confirmed green at every step.
4. **No new MCP tools** at any step.
5. **No new CLI flag on existing servers.** No new
   `--log-format`, `--log-output`, `--diagnostic-
   bundle`, `--healthcheck`, or sibling flag added by
   Track N; the existing flag surface
   (`--transport`, `--config-path`, `--log-level`,
   `--bind`, `--auth-token-env`) is locked.
6. **No new entrypoint module.** No new `__main__.py`
   in any `apps/*/src/` package.
7. **No new dependencies.** Step 4 must not add to
   `[project.dependencies]` or
   `[project.optional-dependencies]`. The existing
   stdlib-only orientation of `mcp_common` and the
   three servers is preserved.
8. **`scripts/release/install.ps1`**,
   **`scripts/release/verify-release.ps1`**,
   **`scripts/release/_install_runner.py`**,
   **`scripts/dev/bootstrap_paths.ps1`**,
   **`scripts/dev/launch.ps1`**,
   **`scripts/dev/run_dev_check.ps1`**,
   **`scripts/dev/README.md`** byte-identical at Steps
   1 / 2 / 3 / 5 / 6. Step 4 MAY modify
   `scripts/dev/selfcheck.py` **only** if Step 3
   contract explicitly authorises PATH B with a
   structured-output mode under the locked LOC cap.
   Default expectation: no `scripts/*` modification.
9. **`scripts/release/README.md`** byte-identical at
   every step.
10. **`SECURITY.md`** byte-identical at every step
    (Track N does not change the security claim).
11. **`docs/release-handoff.md`** byte-identical at
    Steps 1 / 2 / 3 / 4. Step 5 MAY add narrow
    CLASS-1 updates if the "What is in this handoff" /
    "What is NOT in this handoff" / "Where to read
    deeper" lists develop direct factual drift after
    Step 4. Most likely Step 5 edit: a new bullet
    pointing at the Step 4 recipe and (if Step 4 ships
    `selfcheck --json` PATH B) a rewrite of the
    existing "selfcheck output" reference if any.
12. **`apps/platform/README.md`** byte-identical at
    every step (Track N does not change the platform-
    layer boundary inventory).
13. **README.md "Closed parallel tracks" list** byte-
    identical at Steps 1 / 2 / 3 / 4 / 5 (still ends
    at Track M, thirteen entries). Only Step 6 extends
    it to fourteen entries (A through N).
14. **`1c_agent_platform-<VERSION>-py3-none-any.whl`
    artefact class** byte-identical (Track M closure
    state). Step 4 PATH B / C may modify code, which
    transitively changes the wheel's contained bytes,
    but the **artefact class** (one pure-Python wheel,
    `py3-none-any` platform tag, 11 src-layout
    packages, three `[project.scripts]` console
    entries) is locked.
15. **No `1cv8.exe` runs** at any step.
16. **No remote push** at any step.
17. **No real credentials** in any committed file. All
    examples must use abstract placeholders.
18. **No premature closure language.** Steps 1–5 may
    not describe Track N as "закрыт" / "closed".
19. **No false implementation claims.** Step 1 plan
    must present Q1–Q7 as **defaults** and
    **recommendations**, not as decided answers.
20. **No "observability solved forever" / "production-
    ready observability" / "full OTel instrumentation"
    / "Prometheus platform shipped" / "distributed
    tracing ready" / "SIEM-ready" / "enterprise-ready
    observability" framing** except as explicit
    denials.
21. **Step 4 file-surface cap.** Step 3 contract MUST
    pin a maximum number of touched files (default
    expectation: ≤ 3 — at most one recipe doc + at
    most one narrow code-bearing slice + at most one
    accompanying file). Step 3 may tighten.
22. **Step 4 LOC cap for any code-bearing artefact.**
    Default expectation: ≤ 200 LOC stdlib-only, no
    new dependencies. Step 3 may tighten.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track N has shipped **at most one new architecture
   plan-doc, one new step-map doc, one new baseline-
   audit doc, one new normative contract doc, and
   (Step 4) at most three new files or surgical
   modifications** under Step 3 contract caps.
2. Production code (`apps/*/src/`, `packages/*/src/`)
   byte-identical to the Track M closure state
   (`a3bdc48`), UNLESS Step 3 contract explicitly
   authorises a single narrow code-bearing diagnostic
   artefact under PATH B / C and names the file under
   the locked LOC cap.
3. `pyproject.toml` `version` either unchanged
   (`0.5.2`, Q7 = NO-BUMP) or bumped per Q7 rule.
   Other `pyproject.toml` fields byte-identical.
4. Registries `read=15 / write=25 / intelligence=16`
   carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure
   narrative present and honest: explicit denial of
   "observability solved forever", "production-ready
   observability", "full OTel instrumentation",
   "Prometheus platform shipped", "distributed tracing
   ready", "SIEM-ready", "enterprise-ready
   observability" claims; explicit statement of which
   diagnostic surface Track N settled on; explicit Q7
   reasoning.
6. `verify-release.ps1` GREEN on 8 checks at every
   step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed text.
9. No `1cv8.exe` runs anywhere in the track.
10. No remote push performed automatically by any
    step.
11. Track N moved into README's "Closed parallel
    tracks" list, growing it from thirteen to
    fourteen closed tracks (A / B / C / D / E / F /
    G / H / I / J / K / L / M / N).

---

## §10. Honest constraints after closure

These constraints remain after Track N closure:

- **No "production-ready observability" claim.** Track
  N's closure-gate covers one narrow diagnostic-boundary
  slice; broader matrices recommended-only.
- **No metrics platform.** No Prometheus / OpenMetrics
  endpoint, no histogram / counter / gauge surface.
- **No distributed tracing.** No OTel SDK, no span
  emission, no trace context propagation guarantee.
- **No alerting / paging / on-call story.**
- **No SIEM / SOC integration.**
- **No log-aggregation forwarder bundled in-repo.**
- **No structured-logging library dependency.**
- **No `/healthz` / `/readyz` / `/livez` endpoint**
  (Track J §8 defer preserved).
- **No new MCP tools / registry change.**
- **No `1cv8.exe` runs.**

---

## §11. Relationship to Tracks G / H / I / J / K / L / M

| Aspect | Track G | Track H | Track I | Track J | Track K | Track L | Track M | Track N (this) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Surface | stdio transport + CLI | HTTP `/mcp` + bearer auth | installer auth round-trip | TLS / reverse-proxy boundary | real MCP client smoke proof | service supervision / OS service registration | packaging ecosystem / distribution boundary | observability / diagnostics boundary |
| Code touched? | YES (3 `__main__.py` + 245-LOC `_stdio_transport.py` + `[project.scripts]`) | YES (549-LOC `_network_transport.py` + auth wiring) | YES (+15 LOC in `installer.py`) | NO (docs-only) | NO (one new diagnostic file under `scripts/dev/`) | NO (two new files under `docs/operators/service/`) | NO production code (single narrow `pyproject.toml` flip + one operator recipe) | **TBD by Step 3 contract** (default expectation: ≤ 3 files; possibly one operator recipe + at most one narrow diagnostic slice ≤ 200 LOC stdlib-only) |
| New transport? | YES | YES | NO | NO | NO | NO | NO | NO |
| New endpoint? | NO | YES | NO | NO | NO | NO | NO | NO (Q-N-out invariant) |
| New CLI flag? | YES | YES | NO | NO | NO | NO | NO | NO (Q5 invariant) |
| Registry change? | NO | NO | NO | NO | NO | NO | NO | NO |
| SemVer outcome | MINOR (0.3.0 → 0.4.0) | MINOR (0.4.0 → 0.5.0) | PATCH (0.5.0 → 0.5.1) | NO-BUMP | NO-BUMP | NO-BUMP | PATCH (0.5.1 → 0.5.2) | **TBD** (default = NO-BUMP if PATH A; PATCH considered only if Step 4 = PATH B/C with honest defect-class diagnostic-surface improvement; see §12.Q7) |

Track N inherits all preceding tracks' invariants and
adds none that conflict with them.

---

## §12. Open questions Q1–Q7 with default recommendations

These are **defaults and directional recommendations**,
not decided answers. Step 2 audit may move them; Step 3
contract locks them.

### Q1 — what exactly counts as "observability/diagnostics" for closure?

**Options.**
- **(A)** Documented diagnostics-boundary recipe only —
  formalise today's stderr / exit-code / selfcheck /
  verify-release / smoke-harness signals as the
  supported diagnostic surface with explicit non-goals;
  no code change.
- **(B)** Documented diagnostics boundary **plus** one
  narrow code-bearing diagnostic artefact — e.g., a
  `selfcheck --json` mode or equivalent structured-
  output narrow slice that materialises an existing
  signal into a machine-readable shape, plus an
  operator recipe.
- **(C)** Documented diagnostics boundary **plus** one
  narrow log-shape contract code slice — e.g., a single
  canonical startup-banner line shape applied symmetric
  across the three MCP servers, plus an operator
  recipe.

**Default recommendation.** **(A) docs-only** as the
narrowest honest closure. Option **(B)** acceptable if
Step 2 audit confirms `selfcheck.py` structured output
is the cheapest single artefact that materially closes
the "no machine-readable health signal" honest gap
without expanding scope into a metrics / tracing
platform. **(C)** acceptable only if Step 2 audit
reveals a stderr-shape inconsistency across the three
MCP servers that operators cannot work around via prose
recipe alone. The default leans **conservative** because
Track N's risk is silent expansion into a full
observability stack; docs-only minimises that risk.

### Q2 — does the track cover diagnostic artefact only, or triage story too?

**Options.**
- **(A)** Diagnostic artefact only — Step 4 ships at
  most one narrow diagnostic slice (or none, per Q1
  PATH A), the operator-facing triage story remains
  scattered across Tracks J / K / L recipes.
- **(B)** Diagnostic artefact + triage story — Step 4
  ships (at most one narrow artefact and) a documented
  operator triage recipe that walks through 3–5
  canonical failure modes end-to-end ("MCP server
  exits non-zero on startup" / "HTTP transport returns
  401 to every request" / "selfcheck fails" / "wheel
  install succeeded but console entry not on PATH" /
  "systemd unit restart-loops").
- **(C)** Triage story only — Step 4 ships only the
  recipe (no code-bearing artefact), corresponds to
  PATH A from Q1.

**Default recommendation.** **(B) triage story
included** as the operator-facing closure target. A
diagnostic artefact without a triage recipe is operator-
hostile (operators do not know when to consult which
signal). The recipe MUST cover at minimum 3 canonical
failure modes end-to-end — even if (per Q1 PATH A) no
code-bearing artefact is shipped, the recipe alone
qualifies as Track N closure.

### Q3 — what artefact class does Step 4 produce (if any)?

**Options.**
- **(A)** No artefact — PATH A from Q1; one operator-
  facing recipe only.
- **(B)** One narrow code-bearing structured-output
  slice — e.g., `selfcheck.py` gains a `--json` mode
  that emits the existing summary as a JSON-lines
  record; ≤ 200 LOC stdlib-only.
- **(C)** One narrow log-shape contract code slice —
  e.g., a single canonical startup-banner line shape
  helper in `mcp_common` applied symmetric across the
  three MCP servers; ≤ 200 LOC stdlib-only.
- **(D)** One narrow diagnostic-bundle helper — e.g., a
  stand-alone script under `scripts/dev/` that
  collects exit codes, last-N stderr lines, selfcheck
  output, verify-release output into a single
  operator-readable text bundle; ≤ 200 LOC stdlib-
  only.

**Default recommendation.** **(A) no artefact** as the
narrowest closure path. **(B)** considered acceptable
fallback if Step 2 audit reveals strong evidence that
`selfcheck.py` structured output is the cheapest single
artefact that materially closes the "no machine-readable
health signal" honest gap. **(C)** rejected by default
because canonical log-shape requires touching all three
MCP server entrypoints, expanding the code surface
beyond Track N's narrow scope. **(D)** rejected by
default because a diagnostic-bundle script duplicates
the already-existing Track K smoke harness and Track L
journalctl recipe surface without clear additive value.
The default leans **toward (A)** because the diagnostic
surface mostly EXISTS today — what's missing is a
document that NAMES which signals are first-class.

### Q4 — cross-OS neutral or one primary observation OS?

**Options.**
- **(A)** Cross-OS neutral — recipe describes signals
  that work wherever Python 3.11 + stdio / HTTP /
  process-exit-code are supported (i.e., everywhere);
  no OS-specific implementation-coverage.
- **(B)** Linux/systemd/journald primary — recipe walks
  systemd/journald end-to-end (mirror of Track L
  closure target), cross-OS prose only for Windows
  (NSSM, Event Viewer) and macOS (launchd,
  Console.app).
- **(C)** Windows first — recipe walks Windows-side
  diagnostic surface end-to-end (Event Viewer, Task
  Manager process state, PowerShell `Get-EventLog`),
  cross-OS prose only for Linux/macOS.

**Default recommendation.** **(B) Linux/systemd/
journald primary** as the implementation-covered
observation target, symmetric to Track L's primary OS-
family. Track L recipe pins `journalctl -u
mcp-server` as the recommended supervisor-side
observation command; Track N recipe SHOULD extend that
into a documented signal vocabulary on the same OS-
family. **(A)** acceptable as alternative if Step 2
audit reveals that Linux-specific framing leaks into
the recipe more than 30% (rough heuristic). **(C)**
rejected by default because Track L pinned Linux
primary; Track N consistency benefits from the same
choice.

### Q5 — should current selfcheck / verify-release / client smoke belong inside the supported diagnostics surface?

**Options.**
- **(A)** YES — Track N recipe explicitly classifies
  `selfcheck.py` (pre-flight gate), `verify-
  release.ps1` (release-side gate), and `mcp_client_
  smoke.py` (transport smoke harness) as first-class
  diagnostic surfaces, each with named role.
- **(B)** PARTIALLY — Track N recipe classifies
  `selfcheck.py` and `verify-release.ps1` as first-
  class; `mcp_client_smoke.py` recommended-only
  because Track K closure framed it as
  developer/operator diagnostic file, not a runtime
  capability.
- **(C)** NO — Track N recipe treats those three
  surfaces as pre-existing, out-of-scope of the
  diagnostics boundary; the boundary is defined only
  around runtime signals (stderr / exit codes /
  systemd-or-equivalent status).

**Default recommendation.** **(A) all three first-
class**, with their existing scope respected. Each is
already operator-runnable and already produces stable
output; the recipe formalises what each signals (pre-
flight invariants, release-side invariants, transport-
boundary round-trip) and when to consult each during
triage. This costs zero code and zero new
infrastructure.

### Q6 — does Track N likely justify NO-BUMP / PATCH / MINOR?

**Options.**
- **(A)** NO-BUMP. Track N closes under existing
  `0.5.2` if Step 4 = PATH A (docs-only) and no
  production code / `pyproject.toml` changes happen.
  Mirrors Track J / Track K / Track L closure
  precedent.
- **(B)** PATCH `0.5.2 → 0.5.3`. Track N closes with a
  PATCH bump if Step 4 = PATH B/C with a code-bearing
  diagnostic artefact AND the resulting artefact is
  honestly framed as a defect-class repair of an
  existing diagnostic-surface gap (e.g., `selfcheck`
  was machine-readable-adjacent but not actually
  machine-readable; adding `--json` closes that
  long-standing defect-class gap). Mirrors Track I /
  Track M PATCH precedents.
- **(C)** MINOR `0.5.2 → 0.6.0`. Track N closes with a
  MINOR bump only if Step 4 ships net-new external
  capability for ordinary product consumers — e.g., a
  newly-exposed `/healthz` endpoint operators can
  hit. This is **explicitly rejected** by §7 (no
  `/healthz` / `/readyz` / `/livez`) and by §8.5 (no
  new CLI flag on existing servers).

**Default recommendation.** **(A) NO-BUMP** if Step 4
PATH A. **(B) PATCH** acceptable only if Step 4 PATH
B/C closes a clearly defect-class diagnostic-surface
gap. **(C) MINOR** explicitly rejected by track scope
(guardrails §8.5, §8.6, §8.7). The default leans
**NO-BUMP** because the most likely Step 4 outcome,
under §6 / Q1 / Q3 defaults, is docs-only.

### Q7 — how do we avoid silent expansion into a full observability platform?

**Options.**
- **(A)** Explicit denial discipline in every track
  doc — plan + step-map + audit + contract + recipe +
  README + PROJECT-STATUS + CHANGELOG each enumerate
  the forbidden categories (OTel / Prometheus /
  Grafana / Tempo / Loki / Jaeger / SIEM /
  distributed tracing / alerting / on-call); Step 6
  closure block enumerates them again as carry-
  forward non-goals.
- **(B)** File-surface cap + LOC cap discipline —
  Step 3 contract MUST pin ≤ 3 files for Step 4 and
  ≤ 200 LOC stdlib-only for any code-bearing artefact;
  no new dependency; no new entrypoint module; no new
  CLI flag.
- **(C)** Both (A) + (B) combined.

**Default recommendation.** **(C) both combined.** The
risk that Track N silently expands into a full
observability stack is the central risk of this track
— every adjacent track had the same risk and managed
it via denial discipline + numeric caps. Track N
applies the same playbook: explicit denial of every
forbidden category at every step, plus numeric caps
on Step 4 surface. Q7 is the most important question
of the track; the default recommendation locks both
disciplines simultaneously.

---

## §13. Step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-n-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-n-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 3 new files or surgical modifications (default expectation under Q1 (A) = one operator recipe under `docs/operators/observability/` or similar; default expectation under Q1 (B/C) = one operator recipe + at most one ≤ 200 LOC stdlib-only code slice + at most one accompanying file) | locked by Step 3 contract |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `apps/platform/README.md`, possibly `scripts/release/README.md`; NO production code | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` if Q6 = PATCH | NO production code beyond Step 4; Q6 decision explicit |

---

## §14. Honest summary

**What Track N will do.** Convert the "no first-class
observability / diagnostics boundary" gap into one
operator-facing observability / diagnostics recipe
(and, if Step 3 contract pins PATH B/C, one narrow
≤ 200 LOC stdlib-only code-bearing diagnostic slice
that materialises an existing signal into a machine-
readable shape or pins a canonical log-shape across the
three MCP servers), preserving every Tracks A–M
invariant byte-identical.

**What Track N will not do.** It will not introduce a
broader observability platform (no full OTel
instrumentation, no Prometheus / OpenMetrics endpoint,
no Grafana / Tempo / Loki / Jaeger dashboards, no
SIEM / SOC integration, no distributed tracing, no
alerting / paging / on-call rotation, no `/healthz` /
`/readyz` / `/livez` endpoint, no log-aggregation
forwarder, no structured-logging library dependency),
will not add new MCP tools, will not change registries,
will not run `1cv8.exe`, will not push to GitHub
automatically.

**Why this is the next right narrow track.** Every
prior post-phase track left "full observability stack"
in its honest-non-goals list, and Track J / Track L /
Track M each repeated the denial. None of them
positively defined what the supported diagnostic
surface IS — they only denied what it is NOT. Track N
closes that long-standing constraint the same way
Track L closed "service supervision" and Track M
closed "packaging boundary": one document and at most
one narrow declarative or code-bearing slice, with
explicit denial of the broader claims a less
disciplined version of the same track would make.

**Default Q6 outcome.** **NO-BUMP** if Step 4 PATH A
(docs-only); **PATCH** considered only if Step 4
PATH B/C ships a code-bearing diagnostic artefact that
honestly closes a defect-class diagnostic-surface gap.
Q6 lock is Step 6 territory.
