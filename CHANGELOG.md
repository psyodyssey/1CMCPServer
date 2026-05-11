# Changelog

All notable changes to **1C Agent Platform** are documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and the project adheres to [Semantic Versioning](https://semver.org/) starting
from `0.1.0`.

## 0.5.1 — Parallel Track I (PATCH bump), Parallel Track J (docs-only closure under 0.5.1, no further bump), Parallel Track K (diagnostic-tooling-only closure under 0.5.1, no further bump), and Parallel Track L (docs + declarative-template closure under 0.5.1, no further bump)

Version 0.5.1 closes four parallel post-phase tracks. The
`0.5.0 → 0.5.1` PATCH bump itself was made by **Parallel
Track I** (defect-class installer round-trip integrity fix).
**Parallel Track J** (TLS and Reverse-Proxy Deployment
Boundary) subsequently closed under the same `0.5.1` version
without further bump (**Q7 = NO-BUMP**), because Track J was
an intentionally documentation-only deployment-boundary
formalization track with zero production code changes, zero
new public API surface, zero new CLI flag or MCP tool, zero
registry change, and zero observable runtime behaviour
change. **Parallel Track K** (Real MCP Client Integration
Test) then closed under the same `0.5.1` version without
further bump (**Q7 = NO-BUMP**), because Track K was an
intentionally diagnostic-tooling-only track: zero production
code changes, zero defect-class fix, one new operator-
runnable harness file under `scripts/dev/` (symmetric to
the existing `scripts/dev/selfcheck.py`) without
`[project.scripts]` exposure or other public API surface,
zero new MCP tool, zero registry change, and zero observable
runtime behaviour change for ordinary product consumers.
**Parallel Track L** (Service Supervision and OS Service
Registration) then closed under the same `0.5.1` version
without further bump (**Q7 = NO-BUMP**), because Track L was
an intentionally docs-and-declarative-template-only track:
zero production code changes, zero defect-class fix, two
new operator-facing files under a new `docs/operators/service/`
directory (a single operator recipe at `service-supervision.md`
and a single declarative `Type=simple` systemd unit-file
template at `mcp-server.service`, both placeholder-only),
zero new CLI flag, zero new MCP tool, zero
`[project.scripts]` exposure, zero registry change, and
zero observable runtime behaviour change for ordinary
product consumers. Each track has its own subsection below;
all four close under the single `0.5.1` release line.

After Tracks I, J, K and L close, the registry invariant
remains `read = 15 / write = 25 / intelligence = 16`, the
HTTP transport runtime is byte-identical to its Track H /
Step 4 shape (with the Track I defect fix layered on top),
the stdio transport runtime is byte-identical to its Track G
/ Step 4 shape, the platform-layer in-process supervisor
`apps/platform/src/onec_platform/runtime.py` remains byte-
identical and is **not** a service manager (it continues to
supervise only operator-declared product-layer subprocesses
from `ProductConfig.runtime.services`, **not** the MCP
servers themselves), and `pyproject.toml` `version` stays at
`0.5.1`. Active parallel track = none.

### Parallel Track L — Service Supervision and OS Service Registration (NO-BUMP closure under 0.5.1)

Track L is the twelfth post-phase parallel track. It closes
under existing `0.5.1` without further version bump. Track L
closed the next honest operational gap — the lack of a
first-class supervised OS-service story for the three MCP
server entrypoints — by shipping a single operator-facing
recipe at `docs/operators/service/service-supervision.md`
(972 lines, 15 top-level sections) and a single declarative
systemd unit-file template at
`docs/operators/service/mcp-server.service` (76 lines
including comments, `Type=simple`, placeholders only,
RECOMMENDED defaults inline). The recipe covers all five
lifecycle verbs (`start` / `stop` / `restart` / `status` /
`logs`) end-to-end against systemd on Linux as the
implementation-covered closure-gate OS family, plus prose-
only notes for Windows (NSSM) and macOS (launchd). The
runtime that Track L wraps is byte-identical to the post-
Track-K runtime; Track L added no code under `apps/*/src/`
or `packages/*/src/`, no new endpoint, no new flag, no new
MCP tool, no registry change. Track L's closure-gate target
covers **one OS family implementation slice plus cross-OS
prose**; it is **not** a claim that every OS is supported,
that supervision is solved forever, or that clustered HA
and zero-downtime restart are now in scope.

The **Q7 = NO-BUMP** decision is grounded in repo facts:

- **Zero production code change** across all six Track L
  steps. `apps/*/src/`, `packages/*/src/`,
  `_network_transport.py`, `_stdio_transport.py`,
  `installer.py`, `runtime.py`, `process_control.py`,
  `runtime_logs.py`, `models.py` byte-identical to the
  Track K closure state (`0e40056`).
- **Zero defect-class fix.** Step 2 audit explicitly
  established that the foreground-blocking shape of the
  three MCP server `__main__.py` modules is already
  `Type=simple`-compatible; the existing `KeyboardInterrupt`
  graceful-shutdown path in `_stdio_transport.py:208` and
  `_network_transport.py:618-624` together with
  `daemon_threads = True` at `:606-607` provides the
  graceful-shutdown semantics the systemd template's
  `KillSignal=SIGINT` override expects. Track L added
  operator-facing documentation and a declarative template
  for that existing behaviour, not a fix for any broken
  behaviour, silent failure, or operator workaround.
- **Zero new external capability for ordinary product
  consumers.** Both Step 4 deliverables live under
  `docs/operators/service/`, symmetric to Track J's
  `docs/operators/deployment-boundary.md`. They are **not**
  declared in `[project.scripts]`; they are **not**
  importable as Python modules; they are **not** part of
  the install fast path; pip-installing the project does
  not expose them. Pre-Track-L operators could already
  write equivalent unit-file content using stock systemd
  documentation; Track L formalises that content under a
  contract-locked file in repo rather than introducing a
  new capability.
- **Zero new public API surface.** No new public types,
  functions, imports, `__all__` exports,
  `[project.scripts]` entries, `ProductConfig` schema
  fields, CLI flags on existing servers, or HTTP
  endpoints. `mcp_common/__init__.py` `__all__`
  byte-identical to Track K closure state.
- **`runtime.py` byte-identical and NOT extended.** The
  Phase-5/Step-3 + Phase-6/Step-6 in-process supervisor for
  operator-declared product-layer subprocesses remains
  byte-identical. Track L Step 3 contract §3 fact #4 +
  §9.1 item 6 + §10.2 explicitly forbade extending
  `runtime.py` into a service manager; the supervision
  concern stays **outside** the platform process tree, on
  the OS layer. Recipe §4.3 explains the distinction in
  operator-facing prose.
- **SemVer §6 / Keep-a-Changelog.** PATCH is for backward-
  compatible bug fixes; Track L fixed no bug. PATCH
  inertia is rejected by the Q7 default-bias rule.
- **Track I PATCH precedent does not transfer.** Track I
  had `+15 / -0 LOC` of production code AND a previously-
  broken silent-data-loss round-trip; Track L has neither
  (zero production LOC; nothing was previously broken).
- **Track J NO-BUMP precedent applies directly.** Track J
  closed under `0.5.1` without bump after shipping one
  operator-facing artefact (deployment-boundary recipe)
  plus four architecture documents. Track L follows the
  same pattern with one operator-facing recipe + one
  declarative template + four architecture documents.
- **Track K NO-BUMP precedent applies directly.** Track K
  closed under `0.5.1` without bump after shipping one
  operator-runnable diagnostic artefact (smoke harness)
  plus four architecture documents. Track L matches that
  shape; the artefact is a recipe + declarative template
  rather than a Python harness, but the surface profile
  (docs-and-one-static-artefact, no `[project.scripts]`,
  no public API) is identical.
- **Track A / B / C / E precedent applies.** Those docs-
  heavy tracks also closed without separate version entries
  in this `CHANGELOG.md`.
- **Step 1 plan §12.Q7 and Step 3 contract §10.4 / §14**
  explicitly authorize NO-BUMP if Step 4 does not ship a
  defect-class fix observable by end users and does not
  introduce a new CLI flag. Both conditions hold.

#### Per-step outcomes (Track L)

- **Step 1 (planning service supervision and OS service
  registration)** — two planning documents under
  `docs/architecture/track-l-service-supervision-and-os-service-registration-{plan,step-map}.md`
  (plan + step-map; plan has 14 sections including 18
  out-of-scope denials and 13 guardrails; step-map has 16
  track invariants and 18 categorical out-of-scope denials)
  plus narrative updates to README.md / PROJECT-STATUS.md
  to open the track. Step 4 PATH explicitly preserved as
  open between PATH A docs-only, PATH B docs + one
  declarative template, and PATH C docs + template + thin
  wrapper script. Q1–Q7 directional defaults framed only
  (no fake certainty). No production code; no registry
  change; no SemVer bump. Commit `e713f8e`.
- **Step 2 (service supervision baseline audit)** — one
  new descriptive documentation-only document
  (`docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`,
  966 lines, 9 sections). Inventoried existing launch
  surfaces (three foreground-blocking `__main__.py`
  modules; `scripts/dev/launch.ps1` foreground-only dev
  wrapper; `scripts/release/install.ps1` materialise-but-
  not-register install fast-path); inventoried
  supervision-adjacent surfaces via whole-repo grep for
  `systemd` / `launchd` / `Restart=` / `sc.exe` / `nssm` /
  `pywin32` / `supervisor` / `daemon` / `pidfile` /
  `--background` / `--fork` / `--daemonize` patterns;
  inventoried signal-handling shape in
  `_stdio_transport.py:208` and `_network_transport.py:618-624`;
  produced 4-class breakdown (already-reusable / adjacent-
  but-insufficient / clearly-missing / explicitly-out-of-
  scope) with critical finding that
  `apps/platform/src/onec_platform/runtime.py` is
  adjacent-but-orthogonal (in-process supervisor for
  product-layer subprocesses, not for the MCP servers
  themselves; module docstring lines 21–31 explicitly
  excludes "Windows Service / systemd unit registration");
  enumerated 10 clearly missing pieces (zero systemd
  units / zero launchd plists / zero Windows Service
  helpers / zero pidfile plumbing / zero
  `signal.signal(SIGTERM, ...)` handler / zero documented
  operator lifecycle vocabulary / zero journald-Event-
  Viewer integration / zero `EnvironmentFile=` recipe /
  zero `Restart=` policy guidance / zero `User=` /
  `Group=` discipline); resolved Q1–Q6 directionally with
  PATH B + systemd-first + all-five-verbs-mandatory + no-
  production-code-change defaults; produced 14-item
  Step 3 handoff list. Commit `d58c8d9`.
- **Step 3 (service supervision contract)** — one new
  prescriptive normative document
  (`docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`,
  1401 lines, 14 sections, RFC 2119 MUST / MUST NOT /
  SHOULD / SHOULD NOT / MAY language). Pinned **PATH B
  (docs + one declarative template)** for Step 4 (PATH A
  docs-only and PATH C docs + template + wrapper script
  both explicitly rejected with repo-grounded defence);
  pinned systemd / Linux as implementation-covered
  closure-gate OS family with mandatory cross-OS prose
  coverage for Windows + macOS; pinned cross-OS template
  artefacts forbidden in Step 4; pinned all five lifecycle
  verbs (start / stop / restart / status / logs)
  mandatory for closure; pinned no production code change;
  pinned `runtime.py` byte-identical NOT extended; pinned
  exact Step 4 file surface (exactly two new files at
  `docs/operators/service/service-supervision.md` and
  `docs/operators/service/mcp-server.service`; recipe
  ≤1200 soft / ≤1500 hard LOC; template ≤80 LOC including
  comments); pinned exhaustive forbidden file surface for
  Step 4; pinned closure-gate contract C1–C10 (recipe +
  template + 5 verbs + 1 OS implementation + cross-OS
  prose + placeholder discipline + honest non-goals +
  carry-forward invariants + verify-release GREEN +
  selfcheck OK); pinned 15-item insufficient-evidence
  list; pinned 11 forbidden maturity-claim phrases that
  may appear only as quoted denials; pinned 22-check
  Step 4 verification protocol plus Step 5 / Step 6
  carry-forward checks. Carry-forward of Track G stdio +
  Track H HTTP + Track I installer round-trip + Track J
  deployment boundary + Track K diagnostic harness
  preserved byte-identical. Commit `76342a5`.
- **Step 4 (service supervision recipe and systemd
  template, PATH B)** — two new files under a new
  `docs/operators/service/` directory:
  [`docs/operators/service/service-supervision.md`](../docs/operators/service/service-supervision.md)
  (972 lines, well under contract §8.5 ≤1200 soft / ≤1500
  hard caps; 15 top-level sections covering purpose with
  explicit denial list, supported closure target locking
  Linux/systemd implementation + Windows/macOS prose-only,
  preconditions, service model with `Type=simple` defence
  and `runtime.py` non-extension explanation and signal
  handling, all five lifecycle verbs end-to-end against
  systemd in §5–§9, environment / token configuration
  with full placeholder vocabulary table and Track H /
  Track D cross-references, reverse-proxy / TLS boundary
  reminder carrying forward Track H / Track J invariants,
  cross-OS notes for Windows NSSM and macOS launchd as
  prose-only with explicit gap-naming, honest non-goals
  across seven subcategories plus eleven forbidden
  maturity-claim phrases each as explicit denials, cross-
  references to Tracks G/H/I/J/K and production code
  anchors, honest summary) and
  [`docs/operators/service/mcp-server.service`](../docs/operators/service/mcp-server.service)
  (76 lines including comments, within contract §8.5
  ≤80-line hard cap; declarative `Type=simple` systemd
  unit-file template with `[Unit]` / `[Service]` /
  `[Install]` sections; placeholders exclusive
  (`<USER>`, `<GROUP>`, `<WORKING_DIR>`, `<ENV_FILE_PATH>`,
  `<PYTHONPATH>`, `<PYTHON_BIN>`, `<MCP_SERVER_MODULE>`,
  `<TRANSPORT>`, `<CONFIG_PATH>`, `<HOST>`, `<PORT>`,
  `<MCP_TOKEN_VARNAME>`); RECOMMENDED defaults inline
  (`Restart=on-failure`, `RestartSec=5s`,
  `StartLimitBurst=5`, `StartLimitIntervalSec=600s`,
  `KillSignal=SIGINT` to re-route service stop to the
  existing `KeyboardInterrupt` graceful path,
  `KillMode=mixed`, `TimeoutStopSec=15s`)). Zero
  modified files; zero production code change; zero
  `pyproject` change; no new dependencies; the 22-check
  Step 3 §11.1 verification protocol passed all checks
  pre-commit. Commit `efb4ea1`.
- **Step 5 (operator docs and service-supervision
  alignment)** — narrow CLASS-1 docs-alignment. Two files
  modified, zero new files: `README.md` (Quickstart
  paragraph + Active parallel track section refreshed to
  reflect Steps 1–4 closed and Step 5 active — Track L
  still framed as **active**; closed-tracks list and
  Track L detail section deferred to Step 6) and
  `docs/release-handoff.md` (six narrow CLASS-1 edits:
  new bullet in "What is in this handoff" pointing at
  the Track L recipe and template, rewrite of the stale
  "supervisor daemon / systemd unit / Windows Service
  registration / hot reload" line in "What is NOT in
  this handoff", rewrite of two stale "Known limitations"
  bullets to reflect the now-shipped recipe with explicit
  honest framing, new bullet in "Where to read deeper"
  pointing at the recipe). `SECURITY.md`,
  `apps/platform/README.md`, `scripts/dev/README.md`,
  manuals deliberately untouched per Step 3 contract
  §11.3 V defaults (no security-claim change; no
  factual drift introduced). PROJECT-STATUS.md /
  CHANGELOG.md / `pyproject.toml` / closed-tracks list
  deliberately untouched (Step 6 territory). Commit
  `82345b4`.
- **Step 6 (final integration pass and Track L
  closure)** — closure-only commit. README move of
  Track L into Closed parallel tracks list (одиннадцать
  → двенадцать); Active parallel track section
  compressed back to "no active track" wording with
  recommended-only candidates list; new "Track L detail
  (закрыт)" section added above "Track K detail
  (закрыт)"; Quickstart paragraph flipped from active →
  no-active-track wording. PROJECT-STATUS.md header
  rewritten from "Track L / Step 1 in progress" to
  "no active step + Track L fully closed" with `closed`
  status block; historical-edit annotation at the tail
  of Track K Step 6 section updated to reflect Track L
  full closure; per-step closure sections for Track L
  Step 2 / Step 3 / Step 4 / Step 5 / Step 6 inserted
  between Step 1 section and `## Phase 6 закрыта`.
  CHANGELOG.md (this document) — `## 0.5.1` heading
  restructured to embrace four tracks (Track I PATCH
  bump, Track J / K / L NO-BUMP closures); this Track L
  subsection inserted above the existing Track K
  subsection. `pyproject.toml` **NOT** touched (Q7 =
  NO-BUMP). `SECURITY.md`, `docs/release-handoff.md`
  (Step 5 already aligned), `apps/platform/README.md`,
  `docs/operators/deployment-boundary.md`,
  `docs/operators/service/service-supervision.md`
  (Step 4 deliverable, immutable),
  `docs/operators/service/mcp-server.service` (Step 4
  deliverable, immutable), Track L Step 1–4
  architecture docs, `scripts/*`, `examples/*`, manuals,
  production code (`apps/*/src/`, `packages/*/src/`) —
  all byte-identical to their Step 5 closure state.

#### Honest constraints carried forward (Track L)

These are **not new** with Track L — they are properties of
the post-Track-K baseline that Track L documents but does
not change:

- **stdio baseline preserved.** `--transport stdio` remains
  the trusted-local-subprocess channel from Track G /
  Step 4. No auth, no network listener, no bind. Track L
  did not touch `_stdio_transport.py`.
- **HTTP baseline preserved.** `--transport http` remains
  the single `/mcp` POST endpoint from Track H / Step 4
  with bearer auth, 1 MiB body cap, failure-equivalent
  401, complete redaction discipline, plain HTTP/1.1 (no
  in-process TLS), no consumption of forwarded headers.
  Track L did not touch `_network_transport.py`.
- **Installer auth round-trip preserved.** Track I /
  Step 4 emit branch in `installer.py:_config_to_dict`
  preserved byte-identical. Track L did not touch
  `installer.py`.
- **Deployment boundary preserved.** Track J Step 4
  recipe at `docs/operators/deployment-boundary.md`
  preserved byte-identical. Reverse proxy still
  terminates TLS; forwarded headers still not consumed;
  `/healthz` still not shipped. Track L's recipe at
  `docs/operators/service/service-supervision.md`
  cross-references the deployment-boundary recipe (§11)
  as the **orthogonal network-exposure axis sibling**
  but does not modify it.
- **Diagnostic harness preserved.** Track K Step 4
  harness at `scripts/dev/mcp_client_smoke.py` preserved
  byte-identical. Track L did not touch it.
- **Platform-layer in-process supervisor preserved.**
  `apps/platform/src/onec_platform/runtime.py` byte-
  identical. The recipe explicitly distinguishes it from
  the Track L systemd unit in §4.3 — `runtime.py`
  continues to supervise only operator-declared product-
  layer subprocesses (those in `ProductConfig.runtime.services`),
  not the MCP servers themselves.
- **Registries `read = 15 / write = 25 / intelligence =
  16`** carried through unchanged across all six Track L
  steps. Selfcheck `selfcheck_status=ok` confirmed at
  every step.
- **Closure-gate target framing.** Implementation-covered
  OS family = systemd / Linux. Cross-OS coverage =
  prose-only for Windows (NSSM) and macOS (launchd).
  Broader matrices (Windows Service / launchd template
  artefacts / clustered HA / zero-downtime restart) are
  **explicitly out of scope** of Track L and remain
  recommended-only.

#### What Track L explicitly does NOT do

For absolute clarity (carry-forward from Step 1 plan §7,
Step 3 contract §12, recipe §13):

- No new transport family — no WebSocket / SSE / TCP /
  Unix-socket / named-pipe transport.
- No auth-scheme redesign — no JWT / OAuth 2.0 / OIDC /
  SAML / SCIM / federated identity; no RBAC / ABAC /
  per-tool ACL / per-tenant isolation / multi-tenant; no
  token rotation endpoint / refresh tokens / session
  cookies; no in-process TLS / mTLS (Track H §13.1 / §13.3
  carry-forward).
- No deployment-boundary redesign — Track J §13 / §6 /
  §7 / §8 carry-forward unchanged.
- No in-repo Python supervisor framework / daemon class /
  pywin32 service wrapper.
- No `runtime.py` extension into a service manager.
- No auto-restart-on-config-change watcher.
- No hot reload — config changes require `systemctl
  restart`.
- No zero-downtime restart — in-flight requests are
  abandoned on stop (Track H `daemon_threads=True`
  policy).
- No Windows `.bat` / `.cmd` / `.ps1` install wrappers in
  the repo.
- No macOS `.plist` artefacts in the repo.
- No SystemV init / upstart / FreeBSD `rc.d` / NixOS
  module declarations.
- No multi-distro Linux compatibility matrix.
- No journald structured-log integration beyond stderr
  capture.
- No Windows Event Viewer log-channel registration.
- No syslog / `rsyslog` / `syslog-ng` forwarding.
- No OpenTelemetry / Jaeger / Prometheus / OpenMetrics /
  log-aggregation integration.
- No `/healthz` / `/readyz` / `/livez` endpoint — Track J
  §8 defer carried forward.
- No `sd_notify` / `Type=notify` readiness protocol.
- No SSO / SAML / OIDC / SCIM / RBAC / ABAC / multi-
  tenant.
- No Kubernetes manifests, Docker Compose files, Nomad
  job files, Consul / etcd / Zookeeper integration.
- No clustering / HA / load-balancing / multi-instance
  coordination.
- No `.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` / signed-
  binary distribution.
- No GUI installer / wizard.
- No PyPI publication; no wheel publication beyond
  existing `[project.scripts]` declarations.
- No web UI / dashboard frontend.
- No standalone `apps/platform` daemon entrypoint.
- No automatic update / OTA / self-upgrade mechanism.
- No rollback expansion / AST work / 1С matrix expansion.
- No new MCP tools or registry change.
- No `1cv8.exe` runs at any step.
- No real credentials — synthetic placeholder vocabulary
  only.
- No "service supervision solved forever" / "all OS
  families supported" / "production-ready service
  supervision" / "supported on all platforms" /
  "supported in production" / "hostile-network-ready" /
  "enterprise-ready service supervision" / "fully
  supervised" / "production-grade service" / "clustered
  HA" / "zero-downtime restart" claim. The recipe and
  template explicitly enumerate each of these phrases as
  forbidden except as quoted denials.
- No remote push (operator action; not part of any
  Track L step).

#### Active parallel track after Track L closure

None. Twelve post-phase parallel tracks (A / B / C / D /
E / F / G / H / I / J / K / L) closed sequentially.
Phase 7 as a linear phase is not planned. Opening of any
next parallel track is a separate operator decision.
Recommended-only candidates (not auto-opened): TLS-in-
process / mTLS expansion as a separate enterprise-grade
identity track; full packaging ecosystem track (`.msi` /
`.deb` / signed distribution / GUI installer / wizard /
PyPI wheel publication); multi-version 1С matrix
expansion (post-Track-E follow-up); full rollback / AST
work (post-Track-F / post-Track-A follow-ups); full
observability stack track (OpenTelemetry / Prometheus /
log aggregation); web UI / dashboard frontend track;
in-repo daemon framework / pywin32 service wrapper /
launchd plist artefacts as a separate track.

### Parallel Track K — Real MCP Client Integration Test (NO-BUMP closure under 0.5.1)

Track K is the eleventh post-phase parallel track. It closes
under existing `0.5.1` without further version bump. Track K
closed one of the project's last remaining honest gaps —
the lack of real MCP-client-facing end-to-end proof for the
already-existing stdio / HTTP transport surfaces — by
shipping a single stdlib-only operator-runnable diagnostic
harness file at `scripts/dev/mcp_client_smoke.py` (341 LOC),
plus four planning / audit / contract architecture documents
under `docs/architecture/`. The runtime that Track K probes
externally is byte-identical to the post-Track-J runtime;
Track K added no new code under `apps/*/src/` or
`packages/*/src/`, no new endpoint, no new flag, no new MCP
tool, no registry change. Track K's harness exercises the
narrow closure-gate scenario only (`initialize` +
`tools/list` + one read-only `tools/call` against
`mcp-read-server` over both stdio and HTTP transports, plus
an HTTP missing-`Authorization` failure-equivalence probe);
it is **not** a claim that every MCP client is supported,
or that interoperability is solved forever, or that client
compatibility is production-ready.

The **Q7 = NO-BUMP** decision is grounded in repo facts:

- **Zero production code change** across all six Track K
  steps. `apps/*/src/`, `packages/*/src/`,
  `_network_transport.py`, `_stdio_transport.py`,
  `installer.py` byte-identical to the Track J closure
  state (`dd86261`).
- **Zero defect-class fix.** Step 2 audit explicitly
  established that the runtime is internally consistent
  with a plausible MCP interpretation (`_handle_request`
  recognises `initialize` / `tools/list` / `tools/call`
  with correct envelope shapes; `protocolVersion =
  "2024-11-05"`; HTTP path enforces bearer auth +
  failure-equivalence + redaction + `/mcp` POST-only +
  1 MiB body cap). Track K added externally-replayable
  proof of that existing behaviour, not a fix for any
  broken behaviour, silent failure, or operator
  workaround.
- **Zero new external capability for ordinary product
  consumers.** The harness `scripts/dev/mcp_client_smoke.py`
  lives under `scripts/dev/`, in the same category as the
  existing `scripts/dev/selfcheck.py` and the existing
  `scripts/dev/launch.ps1`. It is **not** declared in
  `[project.scripts]`; it is **not** importable as a
  public module from `mcp_common` or any other package;
  it is **not** part of the install fast path; pip-
  installing the project (when a future packaging track
  enables that) does not expose it. Pre-Track-K
  operators already could write equivalent diagnostic
  scripts using only stdlib; Track K formalises that
  capability under a contract-locked file rather than
  introducing a new capability.
- **Zero new public API surface.** No new public types,
  functions, imports, `__all__` exports,
  `[project.scripts]` entries, `ProductConfig` schema
  fields, CLI flags on existing servers, or HTTP
  endpoints. `mcp_common/__init__.py` `__all__`
  byte-identical to Track J closure state.
- **SemVer §6 / Keep-a-Changelog.** PATCH is for
  backward-compatible bug fixes; Track K fixed no bug.
  PATCH inertia is rejected by the prompt's Q7 default-
  bias rule.
- **Track I PATCH precedent does not transfer.** Track I
  had `+15 / -0 LOC` of production code AND a previously-
  broken silent-data-loss round-trip; Track K has neither
  (zero production LOC; nothing was previously broken).
- **Track J NO-BUMP precedent applies directly.** Track
  J also closed under `0.5.1` without bump after shipping
  one operator-facing artefact
  (`docs/operators/deployment-boundary.md`) plus four
  architecture documents. Track K follows the same
  pattern, with one operator-runnable diagnostic artefact
  (`scripts/dev/mcp_client_smoke.py`) plus four
  architecture documents.
- **Track A / B / C / E precedent applies.** Those
  docs-heavy tracks also closed without separate version
  entries in this `CHANGELOG.md`.
- **Step 1 plan §12 Q7 and Step 3 contract §3.Q7 /
  §11.5** explicitly authorize NO-BUMP if Step 4 does
  not ship a defect-class fix observable by end users.
  Step 4 shipped an operator-runnable diagnostic
  harness, not a defect fix. Both conditions hold.

#### Per-step outcomes (Track K)

- **Step 1 (planning real MCP client integration test)** —
  two planning documents under
  `docs/architecture/track-k-real-mcp-client-integration-test-{plan,step-map}.md`
  (plan + step-map) plus narrative updates to README.md /
  PROJECT-STATUS.md to open the track. Q1–Q7 directional
  defaults only (no fake certainty). Step 4 PATH
  explicitly preserved as open between PATH A docs-only,
  PATH B narrow ≤300 LOC harness, and PATH C hybrid.
  No production code; no registry change; no SemVer
  bump. Commit `02783df`.
- **Step 2 (client integration baseline audit)** — one
  new descriptive documentation-only document
  (`docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md`,
  1076 lines, 10 sections). Inventoried existing client-
  integration approximations (`selfcheck.py`,
  `verify-release.ps1`, in-process `_handle_request`
  switch); inventoried what real-MCP-client end-to-end
  proof would require; produced 4-class breakdown
  (already-covered / adjacent-but-insufficient /
  clearly-missing / out-of-scope); resolved Q1–Q6
  directionally (Q1 = Class B closure gate; Q2 = stdio
  + HTTP; Q3 = narrowing toward PATH B; Q4 = mandatory
  closure scenario locked; Q5 = insufficient-on-its-own
  list; Q6 = no production code modification needed);
  produced 14-item Step 3 handoff list. Commit
  `62069a5`.
- **Step 3 (client integration contract)** — one new
  prescriptive normative document
  (`docs/architecture/track-k-real-mcp-client-integration-test-contract.md`,
  1302 lines, 15 sections, RFC 2119 MUST / MUST NOT /
  SHOULD / SHOULD NOT / MAY language). Pinned **PATH B
  (narrow harness)** for Step 4 (PATH A docs-only and
  PATH C hybrid explicitly rejected); pinned closure-
  gate scenario (`initialize` + `tools/list` + one
  read-only `tools/call` against `mcp-read-server`
  over both transports + HTTP 401 failing-mode probe);
  pinned synthetic-token discipline
  (`secrets.token_urlsafe(N≥32)`; token value MUST
  NEVER be printed); pinned Step 4 file surface (exactly
  one new file at canonical pinned location
  `scripts/dev/mcp_client_smoke.py`); pinned ≤300 LOC
  stdlib-only soft cap / ≤400 LOC stdlib-only hard cap;
  pinned 22-check Step 4 verification harness; pinned
  forbidden file surface for Step 4 / Step 5 / Step 6;
  carry-forward of Track G / Track H §10 / §13 / Track
  I / Track J §13 / §6 / §7 / §8 preserved byte-
  identical. Commit `ead4a0e`.
- **Step 4 (narrow MCP client smoke harness, PATH B)** —
  one new stdlib-only harness file at
  [`scripts/dev/mcp_client_smoke.py`](../scripts/dev/mcp_client_smoke.py)
  (341 LOC, under the contract §10.6 ≤400 hard cap).
  Zero modified files; zero production code changes;
  zero `pyproject` changes; no new dependencies. CLI:
  `--server {read,write,intelligence}` default `read`;
  `--transport {stdio,http,both}` default `both`.
  Builds its own PYTHONPATH (mirrors
  `bootstrap_paths.ps1`'s 11 src paths) so it works
  even without operator pre-bootstrap. For each
  `(server, transport)` pair: `initialize` →
  `tools/list` → one read-only `tools/call`, with
  per-method envelope-shape assertions; HTTP also
  exercises a missing-`Authorization` 401 +
  `WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
  `-32001` probe. Synthetic token via
  `secrets.token_urlsafe(32)` at run time, exported via
  `os.environ["MCP_CLIENT_SMOKE_TOKEN"]` and passed to
  the server subprocess via `--auth-token-env`; token
  value never appears in source, output, or commit
  message. Subprocess lifecycle: stderr → DEVNULL;
  ephemeral port via `socket.bind(("127.0.0.1", 0))`;
  port readiness poll with 10s timeout; cleanup
  close-stdin → `proc.terminate()` → `wait(5s)` →
  escalate to `proc.kill()`. Verification run results
  captured in the Step 4 commit body: primary
  closure-gate `--server read --transport both` → exit 0,
  raw final line `OK (server=read transport=both)`;
  spot-check `--server write --transport stdio` → `OK`;
  spot-check `--server intelligence --transport http` →
  `OK`. Commit `979eced`.
- **Step 5 (operator docs and client-integration
  alignment)** — narrow CLASS-1 docs-alignment. Three
  files modified, zero new files: `README.md`
  Quickstart paragraph + Active parallel track section
  refreshed to reflect Steps 1–4 closed and Step 5
  active (Track K still framed as **active** in this
  commit; closed-tracks list and Track K detail section
  deferred to Step 6); `docs/release-handoff.md`
  "What is in this handoff" + "Where to read deeper"
  lists — one bullet each pointing at the new harness
  with diagnostic-tooling framing; `scripts/dev/README.md`
  "Содержимое" section — added `mcp_client_smoke.py`
  alongside the existing four dev scripts. The phrases
  "client integration solved" / "production-ready
  client compatibility" / "all clients supported" /
  "interop fully proven" appear in touched docs only
  as explicit DENIALS (honest-non-goals framing).
  PROJECT-STATUS.md / CHANGELOG.md / `pyproject.toml` /
  closed-tracks list deliberately untouched (Step 6
  territory). Commit `ef9c6c7`.
- **Step 6 (final integration pass and Track K
  closure)** — closure-only commit. README move of
  Track K into Closed parallel tracks list (десять →
  одиннадцать); Active parallel track section
  compressed back to "no active track" wording; new
  "Track K detail (закрыт)" section added above
  "Track J detail (закрыт)"; Quickstart paragraph
  flipped from active → no-active-track wording.
  PROJECT-STATUS.md header rewritten from "Track K /
  Step 1 in progress" to "no active step + Track K
  fully closed" with `closed` status block;
  historical-edit annotation at the tail of the
  Track J Step 6 section updated; per-step closure
  sections for Step 2 / Step 3 / Step 4 / Step 5 /
  Step 6 inserted. CHANGELOG.md (this document) —
  `0.5.1` heading restructured to embrace three
  tracks (Track I PATCH bump, Track J NO-BUMP
  closure, Track K NO-BUMP closure). `pyproject.toml`
  **NOT** touched (Q7 = NO-BUMP). `SECURITY.md`,
  `docs/release-handoff.md` (Step 5 already aligned),
  `scripts/dev/README.md` (Step 5 already aligned),
  `scripts/dev/mcp_client_smoke.py` (Step 4 deliverable
  immutable), `apps/platform/README.md`,
  `docs/operators/deployment-boundary.md`, Track K
  Step 1–4 architecture docs, production code,
  `apps/*/src/`, `packages/*/src/`, остальные
  `scripts/*`, `examples/*`, manuals — all
  byte-identical to their Step 5 closure state.

#### Honest constraints carried forward (Track K)

These are **not new** with Track K — they are properties
of the post-Track-J baseline that Track K probes externally
but does not change:

- **stdio baseline preserved.** `--transport stdio`
  remains the trusted-local-subprocess channel from
  Track G / Step 4. No auth, no network listener, no
  bind. Track K did not touch `_stdio_transport.py`.
- **HTTP baseline preserved.** `--transport http`
  remains the single `/mcp` POST endpoint from
  Track H / Step 4 with bearer auth, 1 MiB body cap,
  failure-equivalent 401, complete redaction
  discipline, plain HTTP/1.1 (no in-process TLS),
  no consumption of forwarded headers. Track K did
  not touch `_network_transport.py`.
- **Installer auth round-trip preserved.** Track I /
  Step 4 emit branch in `installer.py:_config_to_dict`
  preserved byte-identical. Track K did not touch
  `installer.py`.
- **Deployment boundary preserved.** Track J Step 4
  recipe at `docs/operators/deployment-boundary.md`
  preserved byte-identical. Reverse proxy still
  terminates TLS; forwarded headers still not
  consumed; `/healthz` still not shipped. Track K did
  not touch `docs/operators/deployment-boundary.md`.
- **Registries `read = 15 / write = 25 /
  intelligence = 16`** carried through unchanged
  across all six Track K steps. Selfcheck
  `selfcheck_status=ok` confirmed at every step.
- **Harness target framing.** Closure-gate target =
  `mcp-read-server` over both transports; other
  servers (`mcp-write-server`, `mcp-intelligence-server`)
  were spot-checked (one transport each) but are
  recommended-only verification surfaces, not
  acceptance gates. This is documented in the Step 3
  contract §7 and re-asserted in the harness commit
  body.

#### What Track K explicitly does NOT do

For absolute clarity (carry-forward from Step 1 plan §7,
Step 3 contract §13, and Step 4 commit body honest
constraints):

- No new transport family — no WebSocket / SSE / TCP /
  Unix-socket / named-pipe transport.
- No in-process TLS / HTTPS termination — Track H §13.1
  forbid carried forward through Track J §5.
- No mTLS / client certificate authentication — Track H
  §13.3 carried forward.
- No auth-scheme redesign — no JWT / OAuth 2.0 / OIDC /
  SAML / SCIM / federated identity; no RBAC / ABAC /
  per-tool ACL / per-tenant isolation / multi-tenant;
  no token rotation endpoint / refresh tokens /
  session cookies.
- No deployment-boundary redesign — Track J §13 / §6 /
  §7 / §8 carry-forward unchanged.
- No rate limiting / WAF / IDS / DDoS protection /
  anomaly detection in the listener.
- No service supervisor / systemd unit / Windows
  Service registration / launchd / hot reload /
  restart watcher / auto-update.
- No packaging ecosystem (`.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI
  publication / wheel publication beyond
  `[project.scripts]`).
- No web UI / dashboard frontend.
- No observability stack (OpenTelemetry / Jaeger /
  Prometheus / OpenMetrics / log aggregation /
  distributed tracing).
- No standalone `apps/platform` entrypoint.
- No `/healthz` / `/readyz` / `/livez` endpoint.
- No new MCP tools or registry change.
- No multi-version 1С matrix expansion.
- No rollback / AST work.
- No 1cv8 work — Track K operates at the MCP client /
  transport layer, not at the 1cv8 binary surface;
  there were zero `1cv8.exe` runs in any Track K
  step.
- No real credentials — synthetic bearer token only,
  generated at run time via
  `secrets.token_urlsafe(32)`, never printed.
- No "client integration solved forever" / "all
  clients supported" / "production-ready client
  compatibility" / "interop fully proven" claim. The
  harness gate exercises only the narrow closure-gate
  scenario against one primary server over two
  transports plus two spot-checks; broader matrices
  (third-party real MCP clients like Claude Desktop,
  all servers / all mutating tools / all permutations,
  hostile-internet posture, enterprise-grade identity
  matrix) are recommended-only and remain explicitly
  out of scope.
- No deployment / packaging / enterprise-ready /
  hostile-network-ready posture claim. Track J
  trusted-internal-network-behind-operator-reverse-
  proxy model carries forward unchanged.
- No remote push (operator action; not part of any
  Track K step).

#### Active parallel track after Track K closure

None. Eleven post-phase parallel tracks (A / B / C /
D / E / F / G / H / I / J / K) closed sequentially.
Phase 7 as a linear phase is not planned. Opening of
any next parallel track is a separate operator
decision. Recommended-only candidates (not auto-
opened): TLS-in-process / mTLS expansion as a
separate enterprise-grade identity track; service
supervision / packaging ecosystem track; multi-
version 1С matrix expansion (post-Track-E follow-up);
full rollback / AST work (post-Track-F / post-
Track-A follow-ups); observability stack track; web
UI / dashboard frontend track.

### Parallel Track J — TLS and Reverse-Proxy Deployment Boundary (NO-BUMP closure under 0.5.1)

Track J is the tenth post-phase parallel track. It closes
under existing `0.5.1` without further version bump. Track J
formalized the "trusted-internal-network HTTP MCP listener
fronted by an operator-owned reverse proxy that terminates
TLS" deployment shape (already a general-policy statement in
Track H Step 3 contract §13) into a single operator-facing
single-source-of-truth deployment-boundary recipe. The
runtime that Track J describes is byte-identical to the
post-Track-I runtime; Track J added no new code, no new
endpoint, no new flag, no new MCP tool, no registry change.

The **Q7 = NO-BUMP** decision is grounded in repo facts:

- **Zero production code change** across all six Track J
  steps. `apps/*/src/`, `packages/*/src/`,
  `_network_transport.py`, `_stdio_transport.py`,
  `installer.py` byte-identical to the Track I closure
  state (`d408dd2`).
- **Zero defect-class fix.** Step 2 audit explicitly
  established that the runtime already enforced the
  deployment-boundary invariants Track J formalizes
  (bind validation, fail-closed startup, `/mcp` POST-only,
  bearer auth with failure-equivalence + redaction
  discipline, deterministic 404 on non-`/mcp`, zero
  consumption of `X-Forwarded-*` / `Forwarded` /
  `X-Real-IP` / `client_ip` / `peer_ip` for access-control
  purposes, no in-process TLS code path). There was no
  broken behaviour, silent failure, or operator workaround
  at any point.
- **Zero new external capability.** No new `/healthz`
  endpoint, no `--bind` runtime warning, no new CLI flag,
  no new MCP tool, no new auth scheme, no new transport.
  Step 3 contract pinned PATH A specifically to avoid
  net-new capability that would force the SemVer question
  into MINOR territory.
- **Zero new public API surface.** No new public types,
  functions, imports, `__all__` exports, `[project.scripts]`
  entries, or config schema fields.
- **SemVer §6 / Keep-a-Changelog.** PATCH is for
  backward-compatible bug fixes; Track J fixed no bug.
  PATCH inertia is rejected by the prompt's Q7 default-bias
  rule.
- **Track I PATCH precedent does not transfer.** Track I
  had `+15 / -0 LOC` of production code AND a previously-
  broken silent-data-loss round-trip; Track J has neither.
- **Track A / B / C / E precedent applies.** Those
  docs-heavy tracks also closed without separate version
  entries in this `CHANGELOG.md`.
- **Step 1 plan §14 and Step 3 contract §3.7 / §11.5**
  explicitly authorize NO-BUMP if Step 6 is closure-doc
  alignment with no version-relevant change. Both
  conditions hold.

#### Per-step outcomes (Track J)

- **Step 1 (planning TLS and reverse-proxy deployment
  boundary)** — two planning documents under
  `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-{plan,step-map}.md`
  (plan + step-map) plus narrative updates to README.md /
  PROJECT-STATUS.md to open the track. Step 4 PATH
  explicitly preserved as open between PATH A docs-only,
  PATH B narrow ≤15 LOC code, and PATH C hybrid. No
  production code; no registry change; no SemVer bump.
  Commit `e203e43`.
- **Step 2 (deployment-boundary baseline audit)** — one
  new descriptive documentation-only document
  (`docs/architecture/track-j-deployment-boundary-baseline-audit.md`,
  980 lines, 10 sections). Inventoried existing
  TLS / reverse-proxy / bind-host text in Track H
  contract / SECURITY / release-handoff /
  apps/platform/README / scripts; inventoried
  `_network_transport.py` runtime behaviour; produced
  4-class breakdown (already-formalized at general-
  policy level / partially-documented scattered /
  clearly-missing / explicitly-out-of-scope); resolved
  Q1–Q6 directionally (Q1 = reverse-proxy-first hybrid
  with in-process TLS deferred; Q2 directional default
  = PATH A docs-only; Q3 = trusted internal network
  behind operator-owned reverse proxy; Q4 = surfaces
  enumerated for three scenarios; Q5 = `/healthz`
  defer; Q6 = Track J probably needs no production
  code); produced 14-item Step 3 handoff list. Commit
  `344129c`.
- **Step 3 (deployment-boundary contract)** — one new
  prescriptive normative document
  (`docs/architecture/track-j-deployment-boundary-contract.md`,
  1150 lines, 15 sections, RFC 2119 MUST / MUST NOT /
  SHOULD / SHOULD NOT / MAY language). Pinned **PATH A
  docs-only** for Step 4 (PATH B / PATH C explicitly
  rejected); pinned per-scenario MUST/SHOULD/MAY
  matrix for three deployment scenarios (loopback /
  trusted private subnet / public-facing-through-
  reverse-proxy); pinned Forwarded-header MUST-NOT-
  consume policy for `X-Forwarded-For` /
  `X-Forwarded-Proto` / `X-Forwarded-Host` /
  `X-Forwarded-Port` / `X-Forwarded-Server` /
  `X-Real-IP` / `Forwarded` / `True-Client-IP` /
  `CF-Connecting-IP`; pinned `/healthz` defer; pinned
  Step 4 file surface (one new file under `docs/`
  default `docs/operators/deployment-boundary.md`);
  pinned 18-check Step 4 verification harness;
  pinned forbidden file surface for Step 4 / Step 5 /
  Step 6; carry-forward of Track H §10 / §13 + Track G
  stdio + Track I installer round-trip preserved
  byte-identical. Commit `4e04771`.
- **Step 4 (operator-facing deployment-boundary
  recipe, PATH A docs-only)** — one new operator-
  facing recipe document
  ([`docs/operators/deployment-boundary.md`](operators/deployment-boundary.md),
  691 lines, 10 sections; well under contract §10.5
  ≤1500-line soft cap). Sections: purpose,
  threat-model summary, per-scenario deployment
  matrix (byte-identical to contract §7.1),
  per-scenario walkthroughs (A local-only / B
  trusted private subnet with B1 proxy-fronted and
  B2 proxy-omitted variants / C public-facing-
  through-reverse-proxy), Forwarded-header policy
  with full nine-header list, `/healthz` non-
  shipping with rationale and strict-2xx-only-prober
  workarounds, two abstract reverse-proxy snippets
  (nginx + Caddy) plus an explicit deferral note for
  the third under contract §10.3 ≤3 cap, eight
  operator decision-point Q&A, cross-references,
  honest non-goals. Created new `docs/operators/`
  directory. No production code change. All examples
  use abstract placeholders (`<PUBLIC_HOSTNAME>`,
  `<CERT_PATH>`, `<KEY_PATH>`, `<LISTENER_PORT>`,
  `<VARNAME>`); zero real domains, certificates,
  ports, env-var values. Commit `5c793c1`.
- **Step 5 (operator docs and deployment-boundary
  alignment)** — narrow CLASS-1 docs-alignment.
  Three files modified, zero new files: `README.md`
  Quickstart paragraph + Active parallel track
  section refreshed to reflect Steps 1–4 closed and
  Step 5 active (Track J still framed as **active**
  in this commit; closed-tracks list and Track J
  detail section deferred to Step 6); `SECURITY.md`
  "Threat model for HTTP" bullet — single-sentence
  cross-link to the new recipe; `docs/release-handoff.md`
  "What is in this handoff" + "Where to read deeper"
  lists — one bullet each pointing at the recipe
  with required-reading framing. PROJECT-STATUS.md /
  CHANGELOG.md / `pyproject.toml` / closed-tracks
  list deliberately untouched (Step 6 territory).
  Commit `19e8923`.
- **Step 6 (final integration pass and Track J
  closure)** — closure-only commit. README move of
  Track J into Closed parallel tracks list (девять →
  десять); Active parallel track section compressed
  back to "no active track" wording; new "Track J
  detail (закрыт)" section added above "Track I
  detail (закрыт)"; Quickstart paragraph flipped
  from active → no-active-track wording.
  PROJECT-STATUS.md header rewritten from "Track J /
  Step 1 in progress" to "no active step + Track J
  fully closed" with `closed` status block;
  historical-edit annotation updated; per-step
  closure sections for Step 2 / Step 3 / Step 4 /
  Step 5 / Step 6 inserted. CHANGELOG.md (this
  document) — `0.5.1` heading restructured to
  embrace both Track I (PATCH bump) and Track J
  (NO-BUMP closure) subsections. `pyproject.toml`
  **NOT** touched (Q7 = NO-BUMP). `SECURITY.md`,
  `docs/release-handoff.md`,
  `apps/platform/README.md`,
  `docs/operators/deployment-boundary.md`, Track J
  Step 1–4 architecture docs, production code,
  `scripts/*`, `examples/*`, manuals — all
  byte-identical to their Step 5 closure state.

#### Honest constraints carried forward (Track J)

These are **not new** with Track J — they are properties
of the post-Track-H / post-Track-I baseline that Track J
documents but does not change:

- **stdio baseline preserved.** `--transport stdio`
  remains the trusted-local-subprocess channel from
  Track G / Step 4. No auth, no network listener, no
  bind. Track J did not touch
  `_stdio_transport.py`.
- **HTTP baseline preserved.** `--transport http`
  remains the single `/mcp` POST endpoint from
  Track H / Step 4 with bearer auth, 1 MiB body cap,
  failure-equivalent 401, complete redaction
  discipline, plain HTTP/1.1 (no in-process TLS),
  no consumption of forwarded headers. Track J did
  not touch `_network_transport.py`.
- **Reverse proxy terminates TLS.** Operator-owned;
  the listener never speaks TLS itself.
- **Forwarded headers not consumed.** The listener
  does not consume `X-Forwarded-*` / `Forwarded` /
  `X-Real-IP` / `True-Client-IP` / `CF-Connecting-IP`
  for any access-control / trust / allow-listing /
  identity / audit / routing decision. Track J Step 3
  contract §6 pinned this as a MUST-NOT.
- **`/healthz` not shipped.** Non-`/mcp` paths
  return deterministic `404 Not Found` without
  requiring auth — sufficient for connectivity-class
  load-balancer probes. Strict-2xx-only probers must
  reconfigure to accept 4xx as alive or use a proxy-
  synthesised 2xx. Track J does not promise a future
  `/healthz`.
- **Public-routable bind without fronting TLS proxy
  is NOT SUPPORTED.** Documented in the recipe as a
  prose risk; deliberately not a runtime warning
  (PATH A scope discipline; PATH B/C rejected by
  contract §9).
- **Registries `read = 15 / write = 25 /
  intelligence = 16`** carried through unchanged
  across all six Track J steps. Selfcheck
  `selfcheck_status=ok` confirmed at every step.

#### What Track J explicitly does NOT do

For absolute clarity (carry-forward from Step 3 contract
§13 and Step 4 recipe §10):

- No in-process TLS / HTTPS termination — Track H §13.1
  forbid carried forward.
- No mTLS / client certificate authentication — Track H
  §13.3 carried forward.
- No JWT / OAuth 2.0 / OIDC / SAML / SCIM / federated
  identity.
- No RBAC / ABAC / per-tool ACL / per-tenant isolation
  / multi-tenant.
- No token rotation endpoint / refresh tokens / session
  cookies.
- No rate limiting / WAF / IDS / DDoS protection /
  anomaly detection in the listener.
- No service supervisor / systemd unit / Windows
  Service registration / launchd / hot reload /
  restart watcher / auto-update.
- No packaging ecosystem (`.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI
  publication / wheel publication beyond
  `[project.scripts]`).
- No web UI / dashboard frontend.
- No observability stack (OpenTelemetry / Jaeger /
  Prometheus / OpenMetrics / log aggregation /
  distributed tracing).
- No standalone `apps/platform` entrypoint.
- No `/healthz` / `/readyz` / `/livez` endpoint.
- No `0.0.0.0` runtime warning.
- No new MCP tools or registry change.
- No multi-version 1С matrix expansion.
- No rollback / AST work.
- No 1cv8 work.
- No remote push (operator action; not part of any
  Track J step).

#### Active parallel track after Track J closure

None at the time of Track J Step 6 commit. **Historical
update at Track K Step 6:** the first of the
recommended-next-track candidates ("real MCP client
integration test track") was subsequently opened as
Track K and fully closed under the same `0.5.1`
version line (see the Track K subsection above for
the full per-step narrative and Q7 = NO-BUMP
reasoning). **Historical update at Track L Step 6:**
"service supervision / packaging ecosystem track"
from the same recommended-list was then partially
selected as the next opened track — opened as
Track L (Service Supervision and OS Service
Registration) and fully closed under the same
`0.5.1` version line (see the Track L subsection
above for the full per-step narrative and Q7 = NO-BUMP
reasoning). After Track L closure, twelve post-phase
parallel tracks (A / B / C / D / E / F / G / H / I /
J / K / L) closed sequentially. Phase 7 as a linear
phase is not planned. Opening of any next parallel
track is a separate operator decision.

### Parallel Track I — Installer Auth Round-Trip Integrity (PATCH bump 0.5.0 → 0.5.1)

This patch release closes **Parallel Track I — Installer Auth
Round-Trip Integrity**, the ninth post-phase parallel track.
Track I is a defect-class round-trip integrity fix, not a
feature delta. It restores the missing emit branch for the
`auth` section in
`apps/platform/src/onec_platform/installer.py:_config_to_dict`
that was deferred during Track H / Step 4 (per Track H Step 3
contract §11.5 forbidden-files list). After Track I, install
fast-path materialization round-trip preserves the operator's
`auth.tokens` declarations byte-identical to the source list;
raw `${ENV:NAME}` strings remain raw configuration data; env
resolution remains the runtime boundary in
`_network_transport._resolve_env_token`, not install time.

The version bump `0.5.0` → `0.5.1` (Q6 resolved PATCH, NOT
MINOR) reflects the honest framing of Track I as a defect-
class fix:

- Step 4 commit (`d047a6d`) changed `+15 / -0` LOC in a
  single function (`installer.py:_config_to_dict`), symmetric
  to the existing Phase 6 / Step 8 `enterprise_block` emit-
  only-when-divergent pattern that has been in
  `_config_to_dict` since Phase 6.
- **No new public API surface.** `ProductAuthSettings` and
  `ProductConfig.auth` already existed in version `0.5.0`
  (Track H / Step 4); Track I added zero new public types,
  zero new functions, zero new module imports, zero new CLI
  flags, zero new MCP tools, zero changes to
  `mcp_common/__init__.py` `__all__`, zero changes to
  `[project.scripts]`.
- **No new runtime capability for end users.** Operators
  using `--transport http` already had two correct paths
  pre-Track-I: declare `auth.tokens` in source config (works
  unless they round-trip through install fast-path), or use
  `--auth-token-env` CLI override. Track I closed a silent
  data-loss bug in install fast-path materialization that
  operators worked around. There is no net-new capability;
  there is a previously-broken round-trip that now works.
- **SemVer prior precedent comparison.** Track D
  `0.1.0 → 0.2.0` (env-substitution + verify-release Check 8
  — added 50+ LOC of new credential-resolution logic + new
  release-side check). Track F `0.2.0 → 0.3.0` (rollback
  whitelist 2 → 6 — meaningful runtime-reachable recovery for
  4 new tool families). Track G `0.3.0 → 0.4.0` (3 new
  `__main__.py` + 245-LOC `_stdio_transport.py` + new
  `[project.scripts]` block — net-new runnable surface).
  Track H `0.4.0 → 0.5.0` (549-LOC `_network_transport.py`
  + new HTTP/`/mcp` endpoint + bearer auth + new CLI flags —
  net-new transport family). Each of D/F/G/H added a
  recognizable new external capability and warranted MINOR.
  **Track I does not** — it restores integrity of a flow
  that should have always preserved this section.
- **Per Keep-a-Changelog conventions and SemVer §6**, "Bug
  fixes" → PATCH. Track I plan §10 Q6 explicitly framed
  PATCH `0.5.1` as the alternative path "only if Step 4 diff
  truly tiny and framing honest as defect-fix"; both
  conditions are met.

### Per-step outcomes

- **Step 1 (planning installer auth round-trip integrity)** —
  two planning documents under `docs/architecture/track-i-*`
  (plan + step-map). 7 open questions Q1–Q7 with default
  recommendations. No code changes. Commit `cb79597`.
- **Step 2 (installer round-trip baseline audit)** — one new
  descriptive documentation-only document
  (`track-i-installer-auth-round-trip-baseline-audit.md`,
  889 lines, 12 sections). Per-section `_config_to_dict`
  inventory (9 logical sections) + 4-class breakdown (CLASS
  1 already round-trip-safe = 8 sections; CLASS 2 partially
  preserved = empty; CLASS 3 currently dropped = only
  `auth`; CLASS 4 explicitly out-of-scope = 11 items) +
  read-only evidence (file/line refs + diff `ProductConfig`
  dataclass fields vs `_config_to_dict` emit branches +
  precedent for emit-only-when-divergent pattern). Resolved
  Q1 (`installer.py` only — verified by Phase 6/Step 6
  service-level + Phase 6/Step 8 enterprise single-file
  precedents), Q2 (5 preservation rules with file/line
  evidence anchors), Q3 (11 forbidden sub-rules with Track H
  contract + observed-evidence anchors). Commit `e7d9973`.
- **Step 3 (auth round-trip preservation contract)** — one
  new prescriptive normative document
  (`track-i-installer-auth-round-trip-contract.md`, 843
  lines) using RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (118 normative keyword usages: 78
  MUST, 32 MUST NOT, 4 SHOULD, 3 MAY, 1 SHALL). 11 sections
  pinning round-trip integrity definition, exact emit-branch
  placement (after `enterprise_block` attach at l.314, before
  `return out`), exact accumulator-and-conditional-attach
  shape, list-copying discipline, raw `${ENV:NAME}` byte-
  identical preservation, no env-resolution-at-install-time
  rule, exact Step 4 allowed/forbidden file surfaces,
  verification protocol (6 positive checks + 6 negative
  checks + 4 insufficient-verification exclusions + no-real-
  MCP-client-gate carry-over), 15 honest non-goals each
  followed by "No ..." denial clauses, 8-precondition +
  11-prohibition Step 4 handoff note. Commit `525c611`.
- **Step 4 (narrow installer auth round-trip
  implementation)** — the only step with production code
  change. One file modified, +15 / -0 LOC. Additive emit
  branch in `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  between existing `enterprise_block` attach (l.314) and
  `return out`:
  ```python
  auth_block: dict[str, Any] = {}
  if config.auth.tokens:
      auth_block["tokens"] = list(config.auth.tokens)
  if auth_block:
      out["auth"] = auth_block
  ```
  Comment block describes Track I provenance + raw
  `${ENV:NAME}` preservation rule + resolution boundary in
  `_network_transport.py`. No new imports (`Any` already
  imported); no edits to existing 8 emit branches; no helper
  extraction; no refactor; no cleanup churn. Verification:
  14/14 PASS through one-off ephemeral
  `.tmp_track_i_smoke.py` smoke harness (deleted pre-commit)
  covering multi-token round-trip with order, single-token
  round-trip, empty/default no-injection across 3 cases,
  pre-Track-H reload defaults to empty, token order
  positionally preserved, raw `${ENV:NAME}` byte-for-byte
  preserved without populating `os.environ`, no env
  resolution at install time (probe value never appears in
  projected JSON), literal cleartext rejected fail-closed by
  `loader._parse_auth` upstream, end-to-end install fast-
  path executed-mode real-IO round-trip preserves
  `auth.tokens` element-wise. Commit `d047a6d`.
- **Step 5 (operator docs and installer auth alignment)** —
  three docs aligned with the actual Step 4 fix state
  (+185 / -84 lines): `SECURITY.md` (single bullet "Known
  limitation in install fast path round-trip" replaced with
  "Install fast path auth round-trip preserved (Track I /
  Step 4)" + pointer to release-handoff.md for full carry-
  forward); `docs/release-handoff.md` (two locations:
  "What is NOT in this handoff" bullet + "Known limitations"
  pointer); `README.md` (Quickstart paragraph + "Active
  parallel track" section enumerating Steps 1-4 closure
  summary). Drift inventory classified 8 candidates:
  3 CLASS-1 (touched), 3 CLASS-2 (apps/platform/README.md +
  scripts/dev/launch.ps1 + scripts/dev/README.md —
  qualitatively still accurate, no gap mention; verified by
  grep), 2 CLASS-3 (PROJECT-STATUS.md + CHANGELOG.md —
  closure narrative territory, deferred to Step 6). Commit
  `2e9e0b8`.
- **Step 6 (final integration pass and Track I closure)** —
  this closure: `pyproject.toml` version bumped `0.5.0` →
  `0.5.1` (Q6 = PATCH); `README.md`, `PROJECT-STATUS.md`,
  and `CHANGELOG.md` aligned with Track I closed status.
  Read-only final integration check green: linear Step 1 → 6
  history, all Step 1–5 deliverables present on disk,
  registries without drift, `verify-release.ps1` GREEN on 8
  checks, no real credentials anywhere in the six Track I
  commits, no 1cv8.exe runs at any Track I step.

### Actual install fast-path round-trip surface after Track I closure

```powershell
# Operator declares config with auth section
.\scripts\release\install.ps1 `
    -ConfigPath input.config.json `
    -OutputConfigPath out.config.json `
    -Confirm
# Materialised out.config.json now contains
# "auth": {"tokens": ["${ENV:MCP_TOKEN}"]}
# byte-identical to source (raw env-substitution form
# preserved as configuration data; no env resolution
# at install time)
```

Materialised config can then be loaded directly by
`python -m mcp_<server> --transport http --bind <H>:<P>
--config-path out.config.json`; Track H startup gate
accepts the token source without requiring operators to
re-add the section by hand or pass `--auth-token-env`.

### Registry invariant carried through Track I

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track I.

### Honest constraints update under Track I closure

- **Install fast-path auth round-trip preserved.** Operator
  `auth.tokens` declarations now survive
  `scripts/release/install.ps1 ... -Confirm` materialization
  byte-identical to the source list; raw `${ENV:NAME}`
  strings remain raw configuration data (no env resolution
  at install time); pre-Track-H configs without an `auth`
  section round-trip byte-identical (no implicit
  `"auth": {}` injection).
- **No full installer ecosystem.** No `.msi` / `.deb` /
  signed binary distribution / GUI installer / wizard /
  PyPI publication / wheel publication beyond existing
  `[project.scripts]` declarations. Track C wheel-build
  empty constraint preserved.
- **No secret storage / vault / KMS / OS keychain
  integration.** Operator-managed `${ENV:NAME}` path
  remains the only documented secret discipline (Track D
  carry-over).
- **No env-var resolution at install time.** This is a
  design invariant, not a gap. Resolution lives in
  `packages/mcp-common/src/mcp_common/_network_transport.py:_resolve_env_token`
  at server startup, called by Track H
  `_resolve_token_sources` boundary.
- **No Track H auth model changes.** Bearer / case-
  insensitive scheme / constant-time compare via
  `hmac.compare_digest` / failure-equivalence rule / fail-
  closed startup gate / complete redaction discipline all
  preserved byte-identical.
- **No new transport / network / TLS / mTLS / OAuth / JWT
  / OIDC / SAML / SCIM / RBAC / multi-tenant / sessions /
  rate limiting / token rotation / refresh tokens.**
- **No supervisor daemon / systemd unit / Windows Service
  registration / `launchd` plist / hot reload / restart
  watcher / auto-update / orchestration templates / HA /
  clustering / load balancing.**
- **No web UI / dashboard frontend.**
- **No standalone `apps/platform` entrypoint** (carry-over
  out-of-scope from Tracks G/H).
- **No new MCP tools.** Registry counts unchanged
  (`read=15 / write=25 / intelligence=16`).
- **No 1cv8.exe runs at any Track I step.** Track I
  operates at the install/materialization layer; the 1cv8
  binary surface is not engaged.
- **No real MCP client integration test as a closure
  gate.** Recommended but not blocking (Track G/H precedent
  carry-over).
- **No deployment / packaging / enterprise-ready /
  hostile-network-ready posture claim.** Track H trusted-
  network-behind-operator-reverse-proxy model carries
  forward unchanged.
- **All other 0.5.0 honest constraints carry forward
  unchanged.**
- **All earlier 0.4.0 / 0.3.0 / 0.2.0 / 0.1.0 honest
  constraints carry forward unchanged.**

### Active work

None. No parallel track is currently open after Track I
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.5.0 — Parallel Track H — Network-Grade MCP Transport and Authentication Boundary

This release closes **Parallel Track H — Network-Grade MCP
Transport and Authentication Boundary**, the eighth post-
phase parallel track. Track H shipped the **second maturity
layer** on top of Track G: a single HTTP/1.1 `/mcp` endpoint
with static bearer authentication, additive over the existing
local stdio transport. The same `list_tools()` /
`get_tool(name)` boundary serves both transports; the
existing `--transport stdio` path is preserved byte-
identically. **No new MCP tools.** **No changes to tool
registries, `mcp_common` public API, audit row `details`
shape, or `run_write_flow` discipline.** Six steps plus one
Step 2 follow-up; production code was touched in only one
step (Step 4) and only on the explicit allowed surfaces.

The version bump `0.4.0` → `0.5.0` (Q7 resolved YES) reflects
that Track H / Step 4 shipped a real production code change
with observable runtime capability delta:
`python -m mcp_<server> --transport http --bind ...
--auth-token-env ...` now actually starts an HTTP/1.1
listener with bearer authentication, whereas before Track H
the existing `_stdio_transport._build_arg_parser` had
`ALLOWED_TRANSPORTS=("stdio",)` and rejected `http` at
argparse level. This is backward-compatible new functionality
classifying as a classic MINOR bump per SemVer (existing
`--transport stdio` byte-identical via delegation to
`_stdio_transport._serve_stdio`; `mcp_common/__init__.py`
`__all__` byte-identical; `_stdio_transport.py` byte-
identical; `[project.scripts]` byte-identical; registries
`15/25/16` invariant; audit `details` shape preserved; new
`ProductConfig.auth` is an optional field with
`default_factory=ProductAuthSettings`, so pre-Track-H
configs continue to load unchanged).

### Per-step outcomes

- **Step 1 (planning network-grade MCP transport and
  authentication boundary)** — two planning documents under
  `docs/architecture/track-h-*` (plan + step-map). 7 open
  questions Q1–Q7. No code changes. Commit `563b27b`.
- **Step 2 (transport / auth baseline audit)** — one new
  descriptive documentation-only document
  (`track-h-transport-and-auth-baseline-audit.md`,
  1085 lines, 11 sections). Per-server / per-package /
  per-pyproject inventory + 4-class breakdown (11 reusable
  / 8 adjacent / 11 missing / 12 out-of-scope) + read-only
  evidence (zero hits across 8 grep categories: HTTP server
  libs, SSE, WebSocket, TCP, TLS, auth, sessions, rate-
  limit). Resolved Q1 (HTTP-based MCP transport), Q2
  (exactly one transport family), Q3 (static bearer token
  via `Authorization` header, constant-time compare, fail-
  closed), Q4 (`ProductConfig.auth.tokens` + Track D
  `${ENV:NAME}` pattern + `--auth-token-env` CLI override).
  Commit `3c74564`.
- **Step 2 follow-up (credential leak guard self-reference
  fix)** — narrow one-file fix removing four literal
  credential-leak-guard pattern strings from the audit doc
  that started self-matching against `verify-release.ps1`
  Check 7 once the file became tracked (the same self-
  reference hazard the script already handles for itself
  and its README via the `$excludes` list). Paraphrased
  without weakening the audit's meaning; touching
  `scripts/release/verify-release.ps1` deliberately
  avoided. Commit `0628f4c`.
- **Step 3 (network transport / auth contract)** — one new
  prescriptive normative document
  (`track-h-network-transport-and-auth-contract.md`, 1650
  lines) using RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (293 normative keyword usages: 199
  MUST, 74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL). 18
  sections pinning the exact transport family, framing,
  endpoint, MCP method coverage, JSON-RPC ↔ HTTP boundary
  (per-failure-mode HTTP status + envelope shape pinned),
  concurrency, auth contract (`Authorization: <case-
  insensitive-Bearer> <token>`, `hmac.compare_digest`,
  failure-equivalence rule, complete redaction discipline,
  exhaustive forbidden auth-shape list), config schema, CLI
  surface, integration boundary, backward compatibility,
  TLS posture (in-process TLS forbidden; operator-reverse-
  proxy responsibility), `pyproject.toml` posture, exact
  Step 4 implementation surface (allowed/forbidden file
  lists), verification protocol. Commit `2e76061`.
- **Step 4 (narrow HTTP transport and bearer auth boundary)**
  — the only step with production code change.
  Implementation PATH A. Five files changed (+877 / -35,
  1 new + 4 modified):
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    — new, 549 LOC; underscore-prefixed internal helper,
    NOT exported from `mcp_common.__init__`; pure stdlib
    (`http.server.ThreadingHTTPServer`, `hmac`, `os`, `re`,
    `json`, `argparse`, `logging`, `sys`, `email.message`).
    Implements the `/mcp` POST handler (GET → 405+
    `Allow:POST`; non-`/mcp` → 404; wrong Content-Type →
    415+`-32600`; body > 1 MiB → 413+`-32600`; multiple
    Authorization headers → 400+`-32600`; case-insensitive
    Bearer scheme; constant-time token compare; failure-
    equivalence 401+`WWW-Authenticate: Bearer realm="mcp"`+
    JSON-RPC `-32001` for missing/empty/malformed/invalid
    tokens; notifications → 204; complete token-redaction
    discipline) and a unified `run_main_http(...)` that
    handles both `--transport stdio` and `--transport http`
    via a single argparser (stdio path delegates to
    existing `_stdio_transport._serve_stdio` byte-
    identically).
  - Three `__main__.py` (modified) — switched import
    `_stdio_transport.run_main` → `_network_transport.run_main_http`;
    `SERVER_VERSION` bumped 0.3.0→0.4.0; module docstrings
    describe both transports; `main() -> int` signature
    preserved.
  - `apps/platform/src/onec_platform/models.py` (modified)
    — added `ProductAuthSettings` dataclass with
    `tokens: list[str]` + `auth: ProductAuthSettings`
    field on `ProductConfig` with `default_factory`.
  - `apps/platform/src/onec_platform/loader.py` (modified)
    — added `_AUTH_ENV_TOKEN_RE` regex byte-identical to
    Track D pattern; added `_parse_auth(auth_raw)` with
    unknown-keys reject, list-of-strings validation,
    env-substitution regex enforce per entry, literal
    cleartext fail-closed at config-load time. Wired into
    `load_product_config`. Commit `5814041`.
- **Step 5 (operator docs and security alignment)** — six
  docs aligned with the actual Step 4 surface (+410 / -173
  lines): `README.md` Quickstart + "Что Quickstart не
  обещает" + full rewrite of "Active parallel track"
  section enumerating Steps 1–4 closure summary;
  `SECURITY.md` "Local stdio MCP transport only" bullet
  replaced with structured per-transport block (stdio
  threat model + http threat model) plus exhaustive
  still-NOT list and the installer auth-round-trip gap;
  `docs/release-handoff.md` four locations updated;
  `apps/platform/README.md` four locations updated;
  `scripts/dev/launch.ps1` header comment + Show-Usage
  help text point operators at both transports;
  `scripts/dev/README.md` `launch.ps1` parenthetical
  rewritten. `PROJECT-STATUS.md` and `CHANGELOG.md`
  deliberately not touched (closure territory). Commit
  `407a2f2`.
- **Step 6 (final integration pass and Track H closure)** —
  this closure: `pyproject.toml` version bumped 0.4.0 →
  0.5.0 (Q7 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track H closed status. Read-
  only final integration check green: linear Step 1 → 6
  history, all Step 1–5 deliverables present on disk,
  registries without drift, `verify-release.ps1` GREEN on
  8 checks, no real credentials anywhere in the seven
  Track H commits, no 1cv8.exe runs at any Track H step.

### Actual launch surface after Track H closure

```
python -m mcp_read_server --transport stdio --help
python -m mcp_read_server --transport http \
    --bind 127.0.0.1:8765 --auth-token-env MCP_TOKEN --help
```

(and analogously for `mcp_write_server` and
`mcp_intelligence_server`). The CLI flag set is identical
across all three servers: `--help`, `--config-path`,
`--transport {stdio,http}`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`, `--bind <HOST>:<PORT>`,
`--auth-token-env <VARNAME>`. `--bind` and a token source
(either `--auth-token-env <VARNAME>` or non-empty
`auth.tokens` in product config) are required when
`--transport http`; both are silently ignored when
`--transport stdio`.

The HTTP `/mcp` endpoint accepts only POST with
`Content-Type: application/json` and a single JSON-RPC
2.0 message per body up to 1 MiB. The `Authorization`
header is required (`<case-insensitive-Bearer> <token>`);
missing, empty, malformed, mismatched, or duplicate
header all map to a deterministic shape (401 +
`WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
`-32001` envelope, except multiple-Authorization which
maps to 400+`-32600`). Token validation is constant-time
via `hmac.compare_digest`. Token values, lengths, prefixes,
suffixes, hashes, and fingerprints never appear in stderr
logs, response bodies, error messages, or audit `details`.

Tool dispatch goes through the existing `server.py`
boundary (`list_tools()` / `get_tool(name)`); the
`run_write_flow` discipline for write tools and the
read-only-by-construction discipline of the intelligence
server are preserved unchanged on both transports.

### Registry invariant carried through Track H

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track H.

### Honest constraints update under Track H closure

- **Local trusted-stdio + trusted-network HTTP+bearer
  baseline only.** Threat model = local trusted stdio
  boundary for `--transport stdio`, trusted-network
  deployment behind operator-owned reverse proxy for
  `--transport http`. The platform does not claim
  production readiness for adversarial-internet
  deployment.
- **No in-process TLS / HTTPS termination.** Operator
  is responsible for TLS termination at the reverse
  proxy layer; the Track H listener binds plain HTTP/1.1
  and SHOULD be bound to a loopback or private interface.
- **No mTLS / client certificate authentication.**
- **No JWT / OAuth 2.0 / OIDC / SAML / SCIM**, no token
  introspection / refresh / rotation endpoints, no
  session cookies.
- **No RBAC / ABAC / per-token permissioning / per-tool
  ACL / per-tenant isolation / multi-tenant policy
  engine.** Single-tier auth: a valid token grants access
  to the full tool registry.
- **No rate limiting / quotas / throttling.**
- **No WebSocket / Server-Sent Events / TCP / Unix-socket
  / named-pipe transports.**
- **No supervisor daemon / systemd unit / Windows Service
  registration / `launchd` plist / hot reload / restart
  watcher.** Each server is a single-shot process; the
  operator (or the existing `apps/platform/runtime.py`
  boundary, which Track H did not extend) is responsible
  for lifecycle.
- **No web UI / dashboard frontend.**
- **No standalone `apps/platform` entrypoint** (Q6
  carry-over from Track G).
- **No packaging ecosystem beyond `[project.scripts]`
  declarations.** No `.msi` / `.deb` / GUI installer /
  signed binary distribution / PyPI / wheel publication.
  Track C wheel-build empty constraint preserved.
- **No new MCP tools.** Registry counts unchanged.
- **No 1cv8.exe runs at any Track H step.** Track H
  operates at the process / transport / auth layer; the
  1cv8 binary surface is not engaged.
- **Known install fast path round-trip limitation.**
  `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  does not yet emit the new `auth` section, so a config
  round-tripped through `scripts/release/install.ps1
  ... -Confirm` silently loses its `auth.tokens`
  declarations. Operators using `--transport http`
  against a round-tripped config get a clean fail-
  closed startup ("`--transport http requires
  --auth-token-env or auth.tokens in product config`")
  and can either re-add the section by hand or use
  `--auth-token-env <VARNAME>` to bypass the config.
  Future post-Track-H fix to `_config_to_dict` is
  analogous to the Phase 6 / Step 9 service-level +
  enterprise round-trip fix.
- **No real MCP client integration test as a closure
  gate.** Real client testing (Claude Desktop, MCP CLI
  launching the server) is recommended but not blocking
  (Track G precedent carry-over).
- **All other 0.4.0 honest constraints carry forward
  unchanged** (local stdio baseline; rollback whitelist
  6 of 25 mutating registry tools; no `delete_*` family;
  no multi-file restore; no DB schema rollback; no AST
  semantic inversion; no transactional rollback).
- **All earlier 0.3.0 / 0.2.0 / 0.1.0 honest constraints
  carry forward unchanged** (DESIGNER credentials via
  `${ENV:NAME}` substitution; 8th hygiene check in
  `verify-release.ps1`; no installer ecosystem; no full
  enterprise super-set; no full AST parser; no full
  rollback / delete coverage).

### Active work

None. No parallel track is currently open after Track H
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.4.0 — Parallel Track G — Production-Grade MCP Transport and CLI

This release closes **Parallel Track G — Production-Grade MCP
Transport and CLI**, the seventh post-phase parallel track.
Track G shipped the **first production-grade operational
layer** for the three MCP servers: canonical `__main__.py`
entrypoints (`mcp_read_server` / `mcp_write_server` /
`mcp_intelligence_server`), a minimum-viable line-delimited
stdio JSON-RPC 2.0 transport (stdlib-only, no third-party
SDK), a minimal CLI surface (`--help`, `--config-path`,
`--transport`, `--log-level`), and `[project.scripts]`
console entries in `pyproject.toml`. **No new MCP tools.**
**No changes to tool registries, `mcp_common` public API,
audit row `details` shape, or `run_write_flow` discipline.**
Six steps total; production code was touched in only one
step (Step 4); all other steps were
documentation/status/version-only.

The version bump `0.3.0` → `0.4.0` (Q7 resolved YES) reflects
that Track G / Step 4 shipped a real production code change
with observable runtime capability delta:
`python -m mcp_read_server` (and the two siblings) now
actually start a stdio JSON-RPC server, whereas before
Track G the modules were not runnable as scripts at all.
This is backward-compatible new functionality classifying as
a classic MINOR bump per SemVer (existing `list_tools()` /
`get_tool(name)` API preserved byte-identical; the new helper
`mcp_common._stdio_transport` is underscore-prefixed and is
NOT exported from `mcp_common.__init__`, so the public API
surface of `mcp_common` is preserved byte-identical).

### Per-step outcomes

- **Step 1 (planning production-grade MCP transport and CLI)** —
  two planning documents under `docs/architecture/track-g-*`
  (plan + step-map). 7 open questions Q1–Q7. No code
  changes. Commit `7a39454`.
- **Step 2 (transport baseline audit)** — one new
  descriptive documentation-only document
  (`track-g-transport-baseline-audit.md`, 587 lines). Per-
  server inventory of the current state with a 4-class
  breakdown (already useful baseline / adjacent insufficient
  / clearly missing / out-of-scope). Critical findings:
  zero declared runtime dependencies in `pyproject.toml`,
  zero MCP SDK imports anywhere in repo, all three MCP
  server packages identical in structure and lacking
  `__main__.py`. **Q1 resolved** (stdio only). **Q2
  resolved** (custom stdlib only, no new pyproject deps).
  **Q6 resolved** (`apps/platform` standalone entrypoint
  out-of-scope). Commit `6f3ad73`.
- **Step 3 (runtime CLI / entrypoint contract)** — one new
  prescriptive normative document
  (`track-g-runtime-cli-entrypoint-contract.md`, 879 lines)
  using RFC 2119-style MUST / MUST NOT / SHALL / SHOULD /
  MAY wording (85 normative keyword usages). 15 sections
  pinning down the exact `__main__.py` shape, exact CLI
  surface, exact transport scope (stdio JSON-RPC 2.0 only,
  forbidden libraries, stdout/stderr discipline,
  minimum-viable MCP method set), server binding /
  dispatch contract via existing `list_tools()` /
  `get_tool(name)` boundary, no-auth / no-supervisor
  posture, exact `[project.scripts]` block content,
  backward compatibility statement, exact Step 4
  implementation surface (allowed files + forbidden
  surfaces + scope creep markers), verification protocol.
  Commit `8bb3883`.
- **Step 4 (narrow stdio transport and CLI entrypoints)** —
  the only step with production code change. Implementation
  PATH B (3 entrypoints + pyproject scripts + 1 private
  `mcp_common` helper); PATH A pure inline rejected because
  each `__main__.py` would have carried ~140 LOC of
  identical argparse / JSON-RPC framing / dispatch logic
  (~280 LOC of pure copy-paste across 3 servers),
  qualifying as "duplication otherwise unreasonable" under
  Step 3 contract §12.1.4. Five files changed (+361
  lines):
  - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
    — new, 245 LOC; underscore-prefixed internal helper,
    NOT exported from `mcp_common.__init__`; pure stdlib
    (`argparse`, `json`, `logging`, `inspect`, `sys`);
    implements line-delimited JSON-RPC 2.0 loop, the four
    required CLI flags, handlers for `initialize` /
    `ping` / `tools/list` / `tools/call` /
    `notifications/initialized` /
    `notifications/cancelled`, `ToolResult` → MCP
    envelope serialization (`content` +
    `structuredContent` + `isError`), top-of-`run_main`
    exception boundary; `sys.stdout` reserved for
    JSON-RPC envelopes, all diagnostic output routed to
    `sys.stderr` via `logging`.
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`,
    `apps/mcp-write-server/src/mcp_write_server/__main__.py`,
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    — new, ~30 LOC each; each defines `main() -> int`
    that calls `run_main` with the package's existing
    `list_tools` / `get_tool` boundary and a per-server
    name + version. No `__init__.py` edits, no
    `server.py` edits, no `tools.py` / `models.py` /
    `runtime/` / `apps/platform/` touches.
  - `pyproject.toml` — `[project.scripts]` block added
    with exactly three console entries (`mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`). No
    new dependencies; the
    `[tool.hatch.build.targets.wheel] packages = []`
    block (Track C / Step 3 honest constraint) is
    preserved unchanged. Commit `370c5a8`.
- **Step 5 (operator docs and transport alignment)** —
  six docs aligned with the actual Step 4 surface
  (+229 / -81 lines): `README.md` Quickstart paragraph +
  "Что Quickstart не обещает" + full rewrite of "Active
  parallel track" section enumerating closed Steps 1–4
  with artifacts and the actual launch surface;
  `SECURITY.md` "No production-grade MCP transport yet"
  bullet replaced with "Local stdio MCP transport only"
  block (explicit threat model, explicit still-NOT list);
  `docs/release-handoff.md` new "What is in this
  handoff" bullet for the three `python -m` entrypoints,
  reworded "What is NOT in this handoff", launch-section
  parenthetical fix, "Known limitations" alignment;
  `apps/platform/README.md` four "transport / `__main__`
  / CLI does not exist" locations rewritten under the
  Step 4 baseline while preserving network / auth /
  supervisor out-of-scope; `scripts/dev/launch.ps1`
  header comment + `Show-Usage` help text point operators
  at `python -m <server> --help`; `scripts/dev/README.md`
  two operator-facing parentheticals + CI workflow note
  aligned. `PROJECT-STATUS.md` and `CHANGELOG.md`
  deliberately not touched (closure territory). Commit
  `5890ba5`.
- **Step 6 (final integration pass and Track G closure)** —
  this closure: `pyproject.toml` version bumped 0.3.0 →
  0.4.0 (Q7 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track G closed status. Read-
  only final integration check green: linear Step 1 → 6
  history, all Step 1–5 deliverables present on disk,
  registries without drift, `verify-release.ps1` GREEN on
  8 checks, no real credentials anywhere in the six
  Track G commits, no 1cv8.exe runs at any Track G step.

### Actual launch surface after Track G closure

```
python -m mcp_read_server --help
python -m mcp_write_server --help
python -m mcp_intelligence_server --help
```

Each server starts a line-delimited stdio JSON-RPC 2.0 loop
with handlers for `initialize`, `ping`, `tools/list`,
`tools/call`, `notifications/initialized`, and
`notifications/cancelled`. `sys.stdout` is reserved for
JSON-RPC envelopes; diagnostic output (logs) is routed to
`sys.stderr`. Tool dispatch goes through the existing
`server.py` boundary (`list_tools()` / `get_tool(name)`); the
`run_write_flow` discipline for write tools and the read-
only-by-construction discipline of the intelligence server
are preserved unchanged. CLI flags: `--help`, `--config-path
<path>`, `--transport stdio`, `--log-level
{DEBUG,INFO,WARNING,ERROR}`. The same three names are also
declared as `[project.scripts]` console entries in
`pyproject.toml`; the wheel build remains empty
(`[tool.hatch.build.targets.wheel] packages = []`), so these
console entries become installable binaries only when a
future packaging track ships an actual wheel — meanwhile the
documented invocation is `python -m <server>`.

### Registry invariant carried through Track G

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track G.

### Honest constraints update under Track G closure

- **Local trusted-stdio transport only.** No HTTP, no
  WebSocket, no SSE, no TCP, no Unix domain socket, no
  named pipe / Windows IPC. Network exposure remains
  out-of-scope; threat model = local trusted stdio
  boundary (operator-owned process). A future post-
  Track-G network transport track is the right place
  for any of those.
- **No authentication / authorisation.** No token / Bearer
  / JWT / API key validation; no mutual TLS; no OAuth /
  OpenID Connect / SAML; no RBAC / ABAC; no multi-tenant
  isolation; no rate limiting. The platform does not
  claim production readiness for adversarial network
  deployment.
- **No supervisor / service registration.** No systemd
  unit, no Windows Service, no `launchd` plist, no Docker
  / Kubernetes deployment configuration, no
  `supervisor` / `runit` / `s6` recipes, no automatic
  restart watcher, no log aggregation
  (`journald` / `syslog` / ELK), no distributed tracing
  / observability stack.
- **No hot reload, no background config watcher.** Each
  server is a single-shot process; lifecycle is the
  operator's responsibility (or the existing
  `apps/platform/runtime.py` boundary, which Track G did
  not extend).
- **No web UI / dashboard frontend.**
- **No standalone `apps/platform` entrypoint** (Q6
  explicit out-of-scope; Track G ships entrypoints for
  the three MCP servers only, not for `onec_platform`).
- **No packaging ecosystem beyond `[project.scripts]`
  declarations.** No `.msi` / `.deb` / GUI installer /
  signed binary distribution / PyPI / wheel publication.
  Track C wheel-build empty constraint is preserved.
- **No new MCP tools.** Registry counts unchanged
  (`read=15 / write=25 / intelligence=16`).
- **No 1cv8.exe runs at any Track G step.** Track G
  operates at the process / transport layer; the 1cv8
  binary surface is not engaged.
- **No real MCP client integration test as a closure
  gate.** Real client testing (Claude Desktop, MCP CLI
  launching the server) requires operator infrastructure
  and is recommended but not blocking.
- **All other 0.3.0 honest constraints carry forward
  unchanged** (rollback whitelist 6 of 25 mutating
  registry tools, no public `delete_*`, no multi-file
  restore, no DB schema rollback, no AST semantic
  inversion, no transactional rollback).
- **All earlier 0.2.0 / 0.1.0 honest constraints carry
  forward unchanged** (DESIGNER credentials via
  `${ENV:NAME}` substitution; 8th hygiene check in
  `verify-release.ps1`; no installer ecosystem; no full
  enterprise super-set; no full AST parser; no full
  rollback / delete coverage).

### Active work

None. No parallel track is currently open after Track G
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.3.0 — Parallel Track F — Rollback Whitelist Expansion

This release closes **Parallel Track F — Rollback Whitelist
Expansion**, the sixth post-phase parallel track. Track F
narrowly extended the existing `_AUTOMATIC_RECOVERY_SUPPORTED`
whitelist (and its mirror `_ROLLBACK_SUPPORTED_OPERATIONS` in
the write-server runtime) from 2 to 6 entries, strictly inside
the existing snapshot-restore-based rollback model. **No new
MCP tools.** **No changes to recovery API, audit row details
shape, or registries.** Six steps total; production code was
touched in only one step (Step 4) and only in two files
(`recovery.py` + `flow.py`); all other steps were
documentation-only.

The version bump `0.2.0` → `0.3.0` (Q5 resolved YES) reflects
that Track F / Step 4 shipped a real production code change
with observable runtime behaviour delta:
`automatic_recovery_supported=True` is now runtime-reachable
for 4 additional tool families through `run_rollback_assistant`.
This is backward-compatible new functionality classifying as a
classic MINOR bump per SemVer.

### Per-step outcomes

- **Step 1 (planning rollback whitelist expansion)** — two
  planning documents under `docs/architecture/track-f-*` (plan
  + step-map). 10 acceptance criteria; 7 open questions Q1–Q7.
  No code changes. Commit `351278b`.
- **Step 2 (rollback baseline audit and candidate selection)** —
  one new descriptive documentation-only document
  (`track-f-rollback-baseline-audit.md`, 637 lines). Manual
  code review of full mcp-write-server registry (25 tools)
  with per-tool tier breakdown: **Tier 4** (already, 2 tools);
  **Tier 1** (strong candidates, 4 tools — `add_form_attribute`,
  `add_form_element`, `append_module_method`,
  `replace_module_method_body` — verified payload-key match
  against `flow.py:_RELATIVE_PATH_KEYS`); **Tier 2** (deferred,
  1 tool — `update_module_code` payload key naming mismatch);
  **Tier 3** (categorically excluded, 5 tools — `create_*`
  family + `apply_config_from_files` +
  `update_database_configuration` with per-criterion violation
  citation). Q2 resolved: Step 4 target set fixed at the four
  Tier 1 tools. Critical finding documented: whitelist lives in
  TWO mirror frozensets that must stay synchronized
  (`recovery.py:_AUTOMATIC_RECOVERY_SUPPORTED` +
  `flow.py:_ROLLBACK_SUPPORTED_OPERATIONS`). Commit `e9725b2`.
- **Step 3 (rollback eligibility contract)** — one new
  prescriptive normative document
  (`track-f-rollback-eligibility-contract.md`, 633 lines)
  using RFC 2119-style MUST / MUST NOT / SHALL / MAY wording
  (64 normative keyword usages). Six eligibility criteria
  4.A–4.F (payload shape, restore semantics, verification,
  sync discipline, non-expansion, implementation surface);
  9 categorical exclusions; exact Step 4 implementation
  boundary with per-tool sanity check anchors and escape
  clause; backward compatibility statement. Q3 (no
  `restore_dump_file_from_snapshot` API change) and Q4 (no
  audit `details` shape change) resolved YES. Commit
  `45ad2b2`.
- **Step 4 (narrow rollback whitelist expansion)** — the only
  step with production code change. Two-file narrow expansion
  2 → 6 entries: `apps/platform/src/onec_platform/recovery.py`
  `_AUTOMATIC_RECOVERY_SUPPORTED` extended; mirror
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
  `_ROLLBACK_SUPPORTED_OPERATIONS` extended with identical
  6-entry content; minor sync-comment wording update in
  `flow.py:97-103` (allowed per Step 3 contract Section 6.3.1).
  Per-tool sanity check anchors cited in commit message with
  `tools.py` line numbers (3512-3520 / 2680-2687 / 2833-2838 /
  2994-2999) and payload keys for each. No changes to
  `tools.py`, `_RELATIVE_PATH_KEYS`, `_extract_relative_path`,
  audit `details` shape, public API signatures, or registries.
  Diff: 2 files, +17 / -7. Commit `cd95627`.
- **Step 5 (operator docs and rollback coverage alignment)** —
  eight point-edits across three operator-facing docs
  realigning wording with the actual post-Step-4 state:
  `apps/platform/README.md` (5 edits in RECOVERY_MODES /
  «Почему пуст» / «Что не делает» / Phase 6 historical /
  «Что Phase 6 / Step 4 НЕ делал» sections + new «Track F /
  Step 4 — расширение whitelist до 6 tools» subsection),
  `README.md` (2 edits: Quickstart Track F open + Track A
  detail honest constraints bullet), `docs/release-handoff.md`
  (1 edit: Known limitations rollback bullet). Unified support
  statement now consistent across the three modified docs:
  whitelist 2 → 6, broader but still narrow, no blanket
  reversibility claim. SECURITY.md untouched (qualitative
  «small, deliberate set» wording remains accurate). Commit
  `60f1761`.
- **Step 6 (final integration pass and Track F closure)** —
  this closure: `pyproject.toml` version bumped 0.2.0 → 0.3.0
  (Q5 = YES); `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track F closed status. Read-only
  final integration check green: linear Step 1 → 6 history,
  all Step 1–5 deliverables present on disk, identical 6-entry
  sets in both mirror frozensets verified, registries without
  drift, `verify-release.ps1` GREEN on 8 checks, no real
  credentials anywhere in the six Track F commits, no
  1cv8.exe runs at any Track F step.

### Final whitelist after Track F closure

Both `_AUTOMATIC_RECOVERY_SUPPORTED` (in `recovery.py`) and
`_ROLLBACK_SUPPORTED_OPERATIONS` (mirror in `flow.py`) contain
exactly six identical entries:

```
add_catalog_attribute        # already (Phase 6 / Step 4)
add_document_attribute       # already (Phase 6 / Step 4)
add_form_attribute           # added (Track F / Step 4)
add_form_element             # added (Track F / Step 4)
append_module_method         # added (Track F / Step 4)
replace_module_method_body   # added (Track F / Step 4)
```

Coverage: 6 of 25 mutating registry tools = 24% mutating
surface. 19 mutating tools remain manual snapshot-restore
territory by design (Tier 3 categorical exclusions:
`create_*` family — inverse = delete with no public `delete_*`
semantics; `apply_config_from_files` — multi-file impact;
`update_database_configuration` — DB schema migration;
multi-file ops in general).

### Registry invariant carried through Track F

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track F.

### Honest constraints update under Track F closure

- **No universal rollback.** Whitelist remains a narrow
  6-entry list; everything outside falls back to manual
  snapshot-restore via operator-side discipline.
- **No public `delete_*` write-tools.** Semantics of deletion
  in 1С remains undecided; Track F deliberately did not
  introduce them. `create_*` family inverse semantics
  therefore stays unimplemented (Tier 3 categorical
  exclusion).
- **No multi-file restore.** `restore_dump_file_from_snapshot`
  remains the exclusive single-file mutating mechanism for
  rollback.
- **No DB schema rollback.** `update_database_configuration`
  inverse remains operator-side external-DB-backup territory.
- **No AST semantic inversion.** File-byte-restore only; no
  BSL / XML semantic understanding for inverse computation.
- **No transactional rollback.** Multi-step chains
  (apply + updatedb sequence) have no atomic rollback.
- **All other 0.2.0 honest constraints carry forward
  unchanged** (DESIGNER credentials via `${ENV:NAME}`
  substitution; 8th hygiene check in `verify-release.ps1`).
- **All 0.1.0 honest constraints carry forward unchanged**
  (no production-grade MCP transport, no installer ecosystem,
  no full enterprise super-set, no hot reload, no full AST
  parser, no full rollback / delete coverage — Track F
  expanded coverage but not to full).

### Active work

None. No parallel track is currently open after Track F
closure. Phase 7 as a linear phase is not planned. Opening
the next parallel track is an explicit operator decision.

## 0.2.0 — Parallel Track D — Operator Credentials Hardening

This release closes **Parallel Track D — Operator Credentials
Hardening**, the fourth post-phase parallel track. Track D made the
operator credentials path less brittle by introducing a documented
`${ENV:NAME}` substitution form for argv elements inside
`onec_*_command_template`, render-time fail-closed semantics on
missing or malformed env tokens, password-position redaction in
`command_preview` and audit excerpts, operator-facing docs migrated
to the env-substitution default with literal cleartext kept as a
legacy fallback, and a narrow credential-template-hygiene heuristic
in `scripts/release/verify-release.ps1`. This is **not** an
enterprise security platform: no vault, no KMS, no SSO/RBAC, no OS
keychain, no encrypted-at-rest secrets file format. Six steps
total; production code was touched only at one boundary file
(`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`)
and one release-side script (`scripts/release/verify-release.ps1`);
all other steps were documentation-only or aligned existing
operator-facing docs.

### Per-step outcomes

- **Step 1 (planning operator credentials hardening)** — two
  planning documents under `docs/architecture/track-d-*` (plan +
  step-map). No code changes.
- **Step 2 (credentials-flow audit and contract)** — two new
  documentation-only documents under `docs/architecture/`:
  `track-d-credentials-flow-audit.md` (where `/P "<password>"` is
  surfaced today, which payload fields see rendered argv, what
  "out-of-band" meant before Track D), and
  `track-d-credentials-contract.md` (formal contract for the
  `${ENV:NAME}` substitution syntax, render-time resolution
  order, fail-closed semantics, redaction discipline, backward
  compatibility with literal cleartext templates). No code
  changes.
- **Step 3 (env substitution and preview redaction)** —
  implementation in
  `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`:
  `_resolve_env_token(...)` resolves the full-element token
  `${ENV:NAME}` from the process environment at render time
  (after structural placeholder substitution); fail-closed on
  missing, empty, or partial / mixed forms (`ok=False`,
  `command_preview=None`, no subprocess started);
  `_redact_password_args(...)` replaces the argv element
  following `/P` or `/Pwd` (case-insensitive) with the sentinel
  `<redacted>` in `command_preview` and trimmed payload
  excerpts. The actual subprocess argv stays unredacted because
  the binary must authenticate. Literal cleartext templates
  remain supported as a legacy fallback. Registry invariant
  preserved: `read=15 / write=25 / intelligence=16`.
- **Step 4 (operator docs and migration alignment)** —
  operator-facing documentation migrated to the `${ENV:NAME}`
  form as the recommended default, with literal cleartext kept
  as a clearly marked legacy fallback. Three documents aligned:
  `docs/runbooks/track-a-reference-stand-round-trip.md` (product
  config example, env-substitution callout, failure mode F2
  extended to env-token failures, credentials-in-logs note
  updated), `SECURITY.md` (Honest constraints block rewritten
  under env-substitution), `docs/release-handoff.md` (Known
  limitations DESIGNER credentials bullet rewritten). No code
  changes.
- **Step 5 (release verify credential hygiene heuristic)** —
  eighth release-facing check **Credential template hygiene**
  added to `scripts/release/verify-release.ps1`. The check
  scans tracked `*.config.json` files (via `git ls-files`) for
  argv elements immediately following `"/P"` or `"/Pwd"`
  (case-insensitive) inside command-template arrays. Documented
  safe forms (`"${ENV:NAME}"`, `"<password>"`) pass; literal
  cleartext values emit `WARN` (not `FAIL`), naming file and
  line; empty values are not flagged. WARN does not change
  exit-code semantics, so legacy templates do not block the
  receive-side flow. `scripts/release/README.md` and
  `docs/release-handoff.md` updated to describe the eighth
  check and its narrow heuristic-not-DLP scope.
- **Step 6 (final integration pass and Track D closure)** —
  this closure: `pyproject.toml` version bumped 0.1.0 → 0.2.0;
  `README.md`, `PROJECT-STATUS.md`, and `CHANGELOG.md` aligned
  with Track D closed status. Read-only final integration
  check green: linear Step 1 → 6 history, all Step 1–5
  deliverables present on disk, registries `read=15 / write=25
  / intelligence=16` without drift, `verify-release.ps1` GREEN
  with eight checks, no real credentials anywhere in the
  diffs of the six Track D commits.

### Registry invariant carried into 0.2.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track D.

### Honest constraints update

- DESIGNER credentials remain operator-managed. The new
  **recommended path** is the `${ENV:NAME}` substitution form
  resolved at render time. Literal cleartext templates remain
  supported as a legacy fallback. The platform still does
  **not** ship a secrets manager, vault, KMS, OS keychain
  integration, or encrypted-at-rest secrets file format —
  operators feed env vars from their own secrets infrastructure
  if they need that.
- Check 8 is a narrow heuristic over tracked `*.config.json`
  files, not a full DLP scan. It does not parse 1С template
  semantics, does not scan runbooks or other documentation,
  and emits `WARN` (not `FAIL`).
- All other 0.1.0 honest constraints carry forward unchanged
  (single-version 1С smoke evidence on `8.3.27.1859`, no
  production-grade MCP transport, no installer ecosystem,
  no full enterprise super-set, no hot reload, no full AST
  parser, no full rollback / delete coverage).

### Parallel Track E follow-up — Multi-Version 1C Smoke Matrix (closure under 0.2.0)

After Track D closure, **Parallel Track E — Multi-Version 1C
Smoke Matrix** was opened as the fifth post-phase parallel
track and closed within the same `0.2.0` release line as a
documentation / scaffolding follow-up, **without** a minor
version bump (Q5 resolved: NO bump). Track E shipped no
functional delta — production code untouched throughout the
track, registries `read=15 / write=25 / intelligence=16`
without drift, no new MCP tools, no `1cv8.exe` runs at any
step. Six steps total.

#### Per-step outcomes

- **Step 1 (planning multi-version 1C smoke matrix)** — two
  planning documents under `docs/architecture/track-e-*` (plan
  + step-map). No code changes. Commit `1b233ce`.
- **Step 2 (current evidence audit and smoke scenario freeze)** —
  two new documentation-only documents:
  `track-e-current-evidence-audit.md` (descriptive — what is
  proven on reference `8.3.27.1859`, physical artifacts on
  disk, what is not yet evidenced, why single-version is
  insufficient; strict separation proven / inferred /
  not-yet-run / operator-supplied future inputs) and
  `track-e-smoke-scenario.md` (prescriptive **frozen** —
  scenario name `frozen-smoke-v1`, cut-down
  `create_dump_snapshot` via `/DumpConfigToFiles` only,
  principle-based version selection criteria,
  12-column matrix shape, PASS / FAIL / NOT RUN semantics,
  required evidence fields, Step 4 execution boundary).
  Commit `630f837`.
- **Step 3 (matrix scaffolding and operator runbook)** — two
  new operator-facing documents:
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`
  (operator runbook for running `frozen-smoke-v1` on an
  operator-supplied 1С version) and
  `docs/version-support-matrix.md` (top-level evidence
  table with frozen 12-column shape; reference Row 1 for
  `8.3.27.1859` filled copy-only from existing Track A /
  Step 6 evidence, scenario field explicitly marked as
  `stronger-than-frozen-smoke-v1`; no fabricated additional
  rows). No `1cv8.exe` run. Commit `7c08cae`.
- **Step 4 (operator-driven smoke execution and matrix update)** —
  closed via **PATH B (honest operator-supplied gap)**. No
  `1cv8.exe` runs were executed; no additional evidence rows
  were added. Operator-side inventory found only the `8.3.27`
  minor family installed locally (builds `1859/x64` reference
  + `1936/x86` same-family disqualified per Step 2 §2.2);
  no `8.3.<other minor>` family was available; ENV-substitution
  credentials were not set in the work session. Per Track E
  plan Q4 + step-map Step 4, this is honest closure, not
  track failure. `docs/version-support-matrix.md` gained a
  closure note subsection enumerating the actual operator-side
  inventory and an explicit list of what Step 4 deliberately
  did not do (no run on same-family x86 build, no rerun of
  reference, no scenario expansion, no matrix contract
  changes, no fabricated rows, no real credentials).
  Commit `f962d78`.
- **Step 5 (support statement and docs alignment)** — five
  point-edits across three operator-facing docs to align
  wording with the actual Step 4 PATH B outcome: `SECURITY.md`
  (single-version evidence bullet renamed to "Single-version
  1С evidence (with multi-version scaffolding)" with pointer
  to matrix doc + Track E PATH B context + "no blanket
  multi-version support claim"), `docs/release-handoff.md`
  ("No multi-version 1С smoke matrix" Known limitations
  bullet rewritten as "Multi-version 1С smoke matrix —
  scaffolding only" with pointers and PATH B context;
  Single-version coverage bullet extended with matrix-doc
  pointer), `README.md` (Quickstart paragraph rewritten to
  remove stale "planning-only, Step 1" and broad
  "matrix из нескольких 1С версий" implication; "Куда идти
  дальше" navigation enriched with Track E runbook + matrix
  doc + Track E architecture mentions). Unified support
  statement now consistent across all three docs. Commit
  `78d5956`.
- **Step 6 (final integration pass and Track E closure)** —
  this closure: `README.md`, `PROJECT-STATUS.md`, and
  `CHANGELOG.md` aligned with Track E closed status. No
  `pyproject.toml` change (Q5 = NO; Track E without
  functional delta does not warrant a minor bump). Read-only
  final integration check green: linear Step 1 → 6 history,
  all Step 1–5 deliverables present on disk, registries
  without drift, `verify-release.ps1` GREEN on 8 checks, no
  real credentials anywhere in the six Track E commits.

#### Registry invariant carried through Track E

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track E.

#### Honest constraints update under Track E closure

- **Reference single-version evidence remains
  single-version.** Track E shipped scaffolding (frozen
  scenario + operator runbook + matrix-table doc) but did
  not extend the actual evidence breadth. The reference
  row in `docs/version-support-matrix.md` covers
  `8.3.27.1859` only; no additional version evidence rows
  were added.
- **No blanket multi-version support claim.** The platform
  remains multi-version-friendly architecturally (operator
  selects the binary path), but evidence-level claims are
  bounded by the reference row and the honest
  operator-supplied gap notation in the matrix doc.
- **`docs/version-support-matrix.md` is the single source
  of truth** for the actual evidence level. Post-closure
  additional evidence rows can be added through
  documentation-only updates against the matrix doc by
  following
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`,
  without re-opening Track E.
- All other 0.2.0 honest constraints (DESIGNER credentials
  remain operator-managed via `${ENV:NAME}` substitution;
  Check 8 is a narrow heuristic, not full DLP) carry
  forward unchanged.
- All 0.1.0 honest constraints (no production-grade MCP
  transport, no installer ecosystem, no full enterprise
  super-set, no hot reload, no full AST parser, no full
  rollback / delete coverage) also carry forward
  unchanged.

### Active work (at the end of 0.2.0)

At the end of the 0.2.0 release line: Track E was opened and
closed within 0.2.0 as a documentation / scaffolding follow-up
without a minor version bump (Q5 = NO; no functional delta).
**Parallel Track F — Rollback Whitelist Expansion** was opened
afterwards and closed in 0.3.0 with a minor bump (Q5 = YES;
real production code change with functional delta — see
0.3.0 release notes above). Phase 7 as a linear phase remains
not planned. Opening the next parallel track is an explicit
operator decision.

## 0.1.0 — initial public snapshot

The first publicly trackable snapshot of the project. The version
matches `pyproject.toml`.

### Closed before 0.1.0

- **Phases 1–6** — read MVP, write MVP, metadata changes, intelligence
  layer, product layer, industrialization & completion track.
  See `PROJECT-STATUS.md` for per-phase detail.
- **Parallel Track A — Full Real 1cv8-backed Write Path** — closed on
  Step 7. Real binary-backed write path
  (`/DumpConfigToFiles` / `/LoadConfigFromFiles` / `/UpdateDBCfg`) is
  proven on a reference stand. See
  `docs/runbooks/track-a-reference-stand-round-trip.md`.
- **Parallel Track B — Productization & Delivery Polish** — closed on
  Step 6 (final integration pass and Track B closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-b-*`.
  - Step 2 (repo hygiene + legal layer) — `git init` on `main`,
    extended `.gitignore`, this `CHANGELOG.md`, `LICENSE`
    (Apache-2.0, full standard text), `SECURITY.md`, first
    meaningful commit.
  - Step 3 (operator-discoverable install fast path) — thin
    PowerShell wrapper `scripts/release/install.ps1` over the
    existing `run_install_fast_path` helper, plus
    `_install_runner.py` and `scripts/release/README.md`.
  - Step 4 (operator/dev local launch umbrella) —
    `scripts/dev/launch.ps1` with `selfcheck` / `repl` / `run` /
    `help` subcommands; updated `scripts/dev/README.md`.
  - Step 5 (root README quickstart and docs polish) — top-level
    `## Quickstart` block in this README with install / check /
    launch commands and a deeper-docs map.
  - Step 6 (final integration pass and Track B closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track B closed status.
- **Parallel Track C — Packaging & Installer Delivery** — closed on
  Step 6 (final integration pass and Track C closure). Six steps
  total; production code untouched throughout the track. Per-step
  outcomes:
  - Step 1 (planning) — two planning documents under
    `docs/architecture/track-c-*`.
  - Step 2 (release-facing verify path and layout polish) —
    `scripts/release/verify-release.ps1` as a read-only
    pre-handoff sanity check; updated `scripts/release/README.md`
    for the three-entrypoint surface (`install` / `verify` /
    `launch`).
  - Step 3 (packaging-facing install flow honest review) —
    inline block comment in `pyproject.toml` documenting why
    `[tool.hatch.build.targets.wheel] packages = []` is an
    intentional no-op (multi-app monorepo shape; install via
    `scripts/release/install.ps1`, not `pip install`); short
    "Packaging story" section in `scripts/release/README.md`.
  - Step 4 (release handoff documentation) — new
    `docs/release-handoff.md` for the receive-side operator:
    what you received, system prerequisites, reproducible
    install sequence, verify sequence, honest known
    limitations table.
  - Step 5 (integration and handoff polish) — minimal pointer
    to `docs/release-handoff.md` from the Quickstart "Куда
    идти дальше" navigation in this README.
  - Step 6 (final integration pass and Track C closure) — this
    closure: README + PROJECT-STATUS + CHANGELOG aligned with
    Track C closed status.

### Registry invariant carried into 0.1.0

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

No MCP surface drift through Track A, Track B, or Track C.

### Honest constraints carried into 0.1.0

- DESIGNER credentials remain operator-managed and out-of-band; never
  stored in repository.
- Multi-version 1С smoke matrix not yet exercised — single-version
  evidence on `8.3.27.1859`.
- No production-grade MCP transport, no installer ecosystem
  (`.msi` / `.deb` / GUI wizard / signed distribution), no web-UI,
  no full enterprise super-set (SSO/RBAC, multi-tenant, secrets vault
  as a service, federated audit storage, policy-as-code DSL,
  multi-instance HA).
- No hot reload, no OS-level service supervision, no full AST parser,
  no full rollback/delete coverage.

These are honest constraints, not hidden gaps.

### Active work (at the time of 0.1.0)

None. No parallel track was open at the time of the 0.1.0 release.
**Parallel Track D — Operator Credentials Hardening** was opened
afterwards and closed in 0.2.0; see the 0.2.0 release notes above.
