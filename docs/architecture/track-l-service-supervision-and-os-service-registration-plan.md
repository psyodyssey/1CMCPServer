# Parallel Track L — Service Supervision and OS Service Registration — Plan

**Track status at the time of this document:** Parallel Track L
opened as the twelfth post-phase parallel track after Track K
closure (commit `0e40056`). Step 1 — planning only;
documentation-only. No production code change. No
`pyproject.toml` change. No `scripts/*` change. No registry
change. No `1cv8.exe` runs.

**Track L positioning relative to Tracks A–K.**
Tracks A–K closed sequentially as eleven post-phase parallel
tracks (A real-write-path, B productization, C packaging,
D credentials hardening, E version-matrix scaffolding, F
rollback expansion, G stdio transport + CLI, H HTTP transport
+ bearer auth, I installer auth round-trip integrity, J TLS
and reverse-proxy deployment boundary, K real MCP client
integration test). After Track K closure the platform has:

- a stdio MCP transport (Track G);
- a narrow HTTP `/mcp` endpoint with static bearer auth
  (Track H);
- `ProductConfig.auth.tokens` with `${ENV:NAME}` env-
  substitution and `--auth-token-env` CLI override
  (Tracks D + H);
- an install fast-path with auth round-trip integrity
  (Track I);
- an operator-facing deployment-boundary recipe
  (Track J);
- a real MCP client smoke harness at
  `scripts/dev/mcp_client_smoke.py` (Track K).

What it still does **not** have is a first-class
"runs as a long-lived supervised service" story.

---

## §1. Purpose — why this track exists

Track L exists to convert the current honest gap

> "the product can be **run**, but it is not yet a formal
> **OS-managed long-lived supervised service**"

into a disciplined six-step closure track using the same
shape as Tracks A–K (planning → audit → contract → narrow
implementation → docs alignment → final integration pass).

Every prior MCP-transport-track closure (Tracks G / H / I /
J / K) and the Phase-6 closure narrative explicitly flagged
**service supervision / OS service registration** as an
honest non-goal, deferred to a future parallel track. Track L
is that parallel track. It does **not** widen the deferral
into a packaging or enterprise track; it is intentionally the
narrowest honest answer to the supervision gap.

The track is not justified by a defect — there is no broken
behaviour. It is justified by an **operator-ergonomics gap**:
without a service story, an operator who wants to keep an
MCP server running across reboots must hand-roll one (cron,
nohup, ad-hoc `Task Scheduler`, manual `systemd` unit, etc.)
or keep a terminal open. That is acceptable for a developer
machine but is the obvious next pragmatic maturity layer.

---

## §2. Current post-Track-K baseline

The relevant baseline for Track L (as of `0e40056`):

### §2.1 Launch surfaces that already exist

- **`scripts/release/install.ps1`** — operator install
  fast-path; materialises a `ProductConfig` JSON and prints
  follow-up `python -m mcp_<server> --transport ...`
  invocation strings. Confirmed in `scripts/release/`.
- **`scripts/dev/launch.ps1`** — operator-facing local
  launcher that bootstraps PYTHONPATH and runs one of the
  three MCP server entrypoints in the foreground.
- **`python -m mcp_read_server`**, **`python -m
  mcp_write_server`**, **`python -m
  mcp_intelligence_server`** — three canonical `__main__:main`
  entrypoints from Track G, declared as console scripts in
  `pyproject.toml` `[project.scripts]`. They run in the
  foreground of the invoking shell.
- **`--transport stdio`** — line-delimited JSON-RPC 2.0
  over stdin/stdout. Process lifetime is bound to the
  parent invocation; ends when the parent disconnects.
- **`--transport http --bind <HOST>:<PORT>
  --auth-token-env <VAR>`** — `_serve_http` blocks the
  invoking shell on a `ThreadingHTTPServer` until the
  process is killed.
- **`scripts/dev/mcp_client_smoke.py`** — Track K narrow
  diagnostic harness; spawns and tears down its own
  subprocess.

### §2.2 What is **not** in the repo today

- No `systemd` unit file.
- No `launchd` plist.
- No Windows Service registration (`sc.exe create`,
  `New-Service`, `nssm`, native `pywin32`-based service
  wrapper).
- No supervisor wrapper (`supervisord`, `runit`,
  `s6-overlay`, `daemon-tools`).
- No documented restart / status / logs operator story for
  any of the three servers as a long-lived process.
- No `Restart=` / `RestartSec=` / `RestartPolicy` shape in
  any repo file (grep confirms).
- No PID-file handling, no `/var/run/...`, no Windows event-
  log integration.
- No `--daemon` / `--background` / `--fork` CLI flag.
- No graceful-shutdown hook beyond default Python
  `SIGINT` / `KeyboardInterrupt` handling in the
  `ThreadingHTTPServer` loop.

### §2.3 What Track L therefore must close

A first-class "supervision story": guidance the operator can
follow to keep an MCP server running across reboots, with a
known restart policy, a known stop / start / status verb
set, and known log location, **without** asking them to
invent the wrapper themselves.

The track must close that gap **honestly**: it does not
promise "production-ready service supervision", it does not
promise "zero-downtime restart", it does not promise
"clustered HA". It promises **one** documented and
optionally template-backed path per chosen OS family,
preserving every Track G / H / I / J / K invariant byte-
identical.

---

## §3. Honest gap statement

Three observations, each independently verifiable in the
repo at `0e40056`:

1. **No unit / plist / service-control artefact ships in the
   repo.** Whole-repo grep for `systemd`, `launchd`,
   `Restart=`, `nssm`, `New-Service`, `sc.exe create`,
   `RestartPolicy`, `daemon`, `supervisor` returns zero
   matches across `apps/*/src/`, `packages/*/src/`,
   `scripts/*`, `docs/*` other than incidental occurrences
   in this plan and existing honest-non-goals lists.
2. **No formal lifecycle vocabulary in the docs.** Existing
   operator-manual / administrator-manual / runbooks
   describe one-shot or interactive workflows. None of them
   say "to stop the read-server cleanly, do X; to inspect
   its current state, do Y; to view its logs, look at Z".
3. **No process-supervision contract exists.** Track G
   plan / step-map and Track H plan / step-map both list
   "service supervision / hot reload / restart watcher /
   auto-update" in their out-of-scope blocks; Track J Step 3
   contract §13 carries that forward; Track K Step 1 plan
   §7 again denies it. The deferral is consistent and
   honest, which is exactly why a dedicated narrow track is
   now the cleanest way to close it.

The gap is real. It is not papered over by `scripts/dev/
launch.ps1` (foreground only, dev convenience) nor by
`scripts/release/install.ps1` (materialises config; does
not register a service).

---

## §4. Why this gap is real and not already solved

Each of the following candidate "we already have this"
arguments is rejected from repo evidence:

- **"`launch.ps1` is enough."** It runs in the foreground
  of the invoking PowerShell session. Closing the shell
  closes the server. No reboot survival. No restart
  policy. No formal stop verb. Only viable for interactive
  development.
- **"`install.ps1` is enough."** It writes a materialised
  config and prints follow-up commands. It does not start
  a service. It does not register a service. It does not
  define a service lifecycle.
- **"`python -m mcp_<server>` is enough."** That is the
  in-process entry point. It blocks the foreground; it
  has no supervision shell around it. It is the **process**
  the supervision track wraps, not a supervisor.
- **"Track J's reverse-proxy recipe is enough."** Track J
  formalises bind-host policy and TLS termination at an
  operator-owned reverse proxy. It explicitly does **not**
  address the question of how the MCP server process
  behind the proxy stays alive across reboots, restarts
  on failure, or surfaces lifecycle state.
- **"Operators can write their own unit file."** True but
  evades the gap. The same logic would have rejected
  Track J's recipe ("operators can write their own nginx
  config") and Track K's harness ("operators can write
  their own smoke test"). Track L's purpose is to bring
  one supervised path in-repo, with the same level of
  honest scope discipline.

---

## §5. Goal of the track

By Step 6 closure, Track L must have delivered:

1. A single normative service-supervision contract
   (Step 3) that pins the closure-gate scope, the OS-family
   target, the lifecycle vocabulary, and the file surface
   for Step 4.
2. Either a single operator-facing service-supervision
   recipe **or** a single template artefact (unit file
   skeleton, service-registration script, or similar)
   **or** a hybrid — depending on Step 3 Q3 lock; Step 4
   is the only step that may add a code-or-config-template
   artefact.
3. Honest closure narrative in README / PROJECT-STATUS /
   CHANGELOG that documents which OS family was covered,
   which lifecycle verbs are first-class, and explicitly
   denies the broader claims Track L does **not** make.
4. Preserved byte-identical runtime: Track G stdio path,
   Track H HTTP path, Track I installer round-trip,
   Track J reverse-proxy posture, Track K harness — **all**
   unchanged.

---

## §6. What is in scope

- Planning, audit, contract, narrow implementation, docs-
  alignment, and closure for service supervision and OS
  service registration of the already-existing three MCP
  server surfaces (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`).
- Defining what "supervised service" means concretely for
  this repo (process supervisor + restart policy + stop /
  start / status / logs vocabulary, **not** orchestration
  / clustering / observability).
- Defining whether Step 4 targets **one OS family first**
  (Linux / systemd, or Windows / SCM, or macOS / launchd)
  or ships cross-OS guidance with **one** implementation
  slice plus prose for the others.
- Defining service-lifecycle expectations: start / stop /
  restart / status / logs. Whether all five are mandatory
  for closure or whether a subset is sufficient — Q5 of
  the contract.
- Preserving compatibility with all Tracks G / H / I /
  J / K invariants.

## §7. What is out of scope

The following are intentionally **not** Track L scope.
Each is denied explicitly to prevent silent expansion:

- **No new MCP tools.** Registry invariant `read = 15 /
  write = 25 / intelligence = 16` must carry through all
  six Track L steps.
- **No registry changes** of any kind.
- **No transport redesign.** Track G stdio + Track H HTTP
  preserved byte-identical.
- **No auth redesign.** Track H static bearer + Track I
  round-trip integrity + Track D `${ENV:NAME}` substitution
  preserved byte-identical.
- **No deployment-boundary redesign.** Track J reverse-
  proxy / TLS-termination model preserved byte-identical;
  Forwarded-header MUST-NOT-consume invariant carried
  forward.
- **No packaging ecosystem.** No `.msi`, no `.deb`, no
  signed-binary distribution, no GUI installer, no wizard,
  no PyPI publication, no wheel publication beyond
  existing `[project.scripts]` declarations. Track C
  wheel-build empty constraint preserved.
- **No enterprise identity stack.** No SSO, no SAML, no
  OIDC, no SCIM, no RBAC, no ABAC, no per-tenant
  isolation, no multi-tenant, no federated identity.
- **No clustering / HA / load-balancing / orchestration
  platforms.** No Kubernetes manifests, no Docker Compose
  with replicas, no Nomad, no Consul, no etcd.
- **No web UI / dashboard frontend.**
- **No full observability stack.** No OpenTelemetry, no
  Jaeger, no Prometheus exporter, no OpenMetrics endpoint,
  no log-aggregation forwarder, no distributed tracing.
  Track L may scope "where to look for logs" but does
  **not** ship integration.
- **No rollback expansion / AST work / 1C matrix
  expansion.** Track F / Track A / Track E remain
  orthogonal.
- **No `1cv8.exe` runs.** Track L operates on process
  supervision, not on 1C binary surface.
- **No remote push.** GitHub push remains an explicit
  operator action.
- **No hot reload / zero-downtime restart.** A supervised
  restart that interrupts in-flight requests is sufficient.
- **No automatic-update mechanism.** Operator-driven
  upgrade only.
- **No claim of "production-grade service supervision"
  for hostile-network exposure.** Track J §13 trusted-
  internal-network posture carries forward unchanged.

---

## §8. Guardrails

Each guardrail is verifiable on the post-Step-1 commit and
must remain verifiable through Step 6:

1. **Tracks A–K invariants byte-identical.** `apps/*/src/`,
   `packages/*/src/`, `_stdio_transport.py`,
   `_network_transport.py`, `installer.py`,
   `scripts/dev/mcp_client_smoke.py`, `docs/operators/
   deployment-boundary.md` not touched by Steps 1–3 or
   Step 5 / Step 6; Step 4 may add at most one new file
   (and possibly modify one operator-facing doc only if
   the Step 3 contract pins that and it is the narrowest
   honest closure path — but the default expectation is
   that Step 4 adds files only).
2. **Registries invariant.** `selfcheck.py` registries
   `read=15 / write=25 / intelligence=16` must remain
   confirmed green at every step.
3. **No new MCP tools** at any step.
4. **`pyproject.toml`** untouched through Step 5; Step 6
   may bump `version` only if Q7 lands on PATCH or MINOR.
   Default Q7 expectation = NO-BUMP (see §12.Q7).
5. **No real credentials** in any committed file. All
   examples must use abstract placeholders
   (`<USER>`, `<HOST>`, `<PORT>`, `<UNIT_NAME>`,
   `<SERVICE_NAME>`, `<LOG_PATH>`, `<VARNAME>`).
6. **No `1cv8.exe` runs** at any step.
7. **No remote push** at any step.
8. **No premature closure language.** Steps 1–5 may not
   describe Track L as "закрыт" / "closed". Only Step 6
   may do so.
9. **No false implementation claims.** Step 1 plan must
   present Q1–Q7 as **defaults** and **recommendations**,
   not as decided answers.
10. **No "service supervision solved" / "production-ready
    service" / "all OS families supported" framing.** Such
    phrases may appear in Track L docs only as explicit
    denials.
11. **No standalone `apps/platform` entrypoint** added by
    Track L (carry-over of Track G / H / I / J / K
    out-of-scope).
12. **No `/healthz` endpoint** added by Track L (carry-
    over of Track J §8 defer).
13. **Step 4 file-surface cap.** Step 3 contract MUST pin
    a maximum number of new files (default expectation =
    ≤ 2 new files; e.g., one unit-file template plus one
    operator-facing recipe doc). Step 3 contract MUST also
    pin a maximum LOC cap for any code-bearing artefact
    (default expectation = ≤ 150 LOC stdlib-only, no new
    dependencies). Step 3 may tighten these defaults.

---

## §9. Acceptance criteria for eventual closure

By Step 6 commit:

1. Track L has shipped **at most one new architecture
   plan-doc, one new step-map doc, one new baseline-audit
   doc, one new normative contract doc, and (Step 4) at
   most two new artefacts** — under Step 3 contract caps.
2. Production code (`apps/*/src/`, `packages/*/src/`)
   byte-identical to the Track K closure state
   (`0e40056`).
3. `pyproject.toml` `version` either unchanged (`0.5.1`,
   Q7 = NO-BUMP) or bumped per Q7 rule.
4. Registries `read=15 / write=25 / intelligence=16`
   carried through unchanged.
5. README / PROJECT-STATUS / CHANGELOG closure narrative
   present and honest: explicit denial of "production-
   ready service" / "all OS families supported" /
   "clustered HA" / "zero-downtime restart" claims;
   explicit statement of which OS family Step 4
   implemented; explicit statement of which lifecycle
   verbs Step 4 covered; explicit Q7 reasoning.
6. `verify-release.ps1` GREEN on 8 checks at every step.
7. `selfcheck.py` `status=ok` at every step.
8. No real credentials anywhere in committed text.
9. No `1cv8.exe` runs anywhere in the track.
10. No remote push performed automatically by any step.
11. Track L moved into README's "Closed parallel tracks"
    list, growing it from eleven to twelve closed tracks
    (A / B / C / D / E / F / G / H / I / J / K / L).

---

## §10. Honest constraints after closure

These constraints remain after Track L closure (they are
**not** removed by Track L — they remain honest non-goals
of the platform):

- **No "production-ready service supervision for hostile-
  network exposure" claim.** Track J trusted-internal-
  network posture preserved.
- **No automatic update / OTA upgrade.** Operator-driven
  upgrade only.
- **No clustering / HA / multi-instance coordination.**
  Single-host single-process model preserved.
- **No web UI / dashboard for service control.** Lifecycle
  verbs are CLI-only on the operator's machine, mediated
  by the OS service manager.
- **No standalone `apps/platform` daemon entrypoint.**
- **No zero-downtime restart.** Supervised restart may
  interrupt in-flight requests; client-side retry is the
  operator's concern.
- **No full observability stack.** Track L documents
  where the OS service manager writes logs; integration
  with log-aggregation / metrics / tracing is out of
  scope.
- **No `/healthz` endpoint.** Track J §8 defer preserved.
- **No enterprise identity stack.**
- **No multi-version 1С matrix expansion** (Track E
  follow-up).
- **No rollback / AST work** (Track F / Track A
  follow-ups).
- **No new MCP tools / registry change** (registry
  invariant `15 / 25 / 16` preserved).
- **No `1cv8.exe` runs.** Track L is orthogonal to the
  1C binary surface.

---

## §11. Relationship to Tracks G / H / I / J / K

| Aspect | Track G | Track H | Track I | Track J | Track K | Track L (this) |
| --- | --- | --- | --- | --- | --- | --- |
| Surface | stdio transport + CLI | HTTP `/mcp` + bearer auth | installer auth round-trip | TLS / reverse-proxy boundary | real MCP client smoke proof | service supervision / OS service registration |
| Code touched? | YES (3 `__main__.py` + 245-LOC `_stdio_transport.py` + `[project.scripts]`) | YES (549-LOC `_network_transport.py` + auth wiring) | YES (+15 LOC in `installer.py`) | NO (docs-only) | NO (one new diagnostic file under `scripts/dev/`) | **TBD by Step 3 contract** (default expectation: 0 production code lines; may add one or two operator-facing artefacts) |
| New transport? | YES | YES | NO | NO | NO | NO |
| New endpoint? | NO | YES (`/mcp`) | NO | NO | NO | NO |
| New CLI flag? | YES (`--transport`, `--config-path`, `--log-level`) | YES (`--bind`, `--auth-token-env`) | NO | NO | NO | **TBD** (default = NO; no new CLI flag on existing server entrypoints) |
| Registry change? | NO | NO | NO | NO | NO | NO |
| SemVer outcome | MINOR (0.3.0 → 0.4.0) | MINOR (0.4.0 → 0.5.0) | PATCH (0.5.0 → 0.5.1) | NO-BUMP (under 0.5.1) | NO-BUMP (under 0.5.1) | **TBD** (default = NO-BUMP; see §12.Q7) |

Track L inherits all preceding tracks' invariants and adds
none that conflict with them.

---

## §12. Open questions Q1–Q7 with default recommendations

These are **defaults and directional recommendations**, not
decided answers. Step 2 audit may move them; Step 3
contract locks them.

### Q1 — what exactly counts as "service supervision" for closure?

**Options.**
- **(A)** Minimum: one documented unit-file (or equivalent)
  template + a documented operator workflow for register /
  start / stop / restart / status / logs.
- **(B)** Broader: option A **plus** a thin wrapper script
  (e.g., `scripts/release/register-service.ps1` or
  `scripts/release/install-systemd-unit.sh`) that performs
  the install / register step idempotently.
- **(C)** Full: a code-level supervisor (daemon shim,
  pywin32 service class, etc.) inside the repo.

**Default recommendation.** **(A)** as closure gate; **(B)**
optional in Step 4 if it stays narrow under the §8 file-
surface cap. **(C)** explicitly rejected by §7 out-of-scope.

### Q2 — which OS family does Step 4 implement first?

**Options.**
- **(A)** Linux / systemd first (most reproducible; widest
  industrial precedent; cleanest unit-file vocabulary).
- **(B)** Windows / Service Control Manager first (matches
  the operator machine context observed in
  `examples/demo-infobase/infobase6.config.json` —
  Windows-resident).
- **(C)** macOS / launchd first (least industrial; least
  appropriate as the closure-gate target).
- **(D)** Cross-OS: docs covering all three with a single
  implementation slice on whichever Step 3 contract picks.

**Default recommendation.** **(A) systemd first** as the
closure-gate target (broadest precedent; cleanest
declarative unit-file model). **(D) cross-OS docs +
systemd implementation slice** as the contract default;
**(B)** acceptable if Step 2 audit reveals that the
operator-machine context makes Windows the only
realistic real-world target — but cross-OS prose covering
Windows / macOS must still appear in Step 4 docs even if
the implementation slice is Linux-only. **(C)** never the
primary target.

### Q3 — docs-only vs template/config-based vs wrapper-assisted

**Options.**
- **(A)** PATH A — docs only. One operator-facing recipe
  enumerating the unit-file shape, install steps, lifecycle
  verbs.
- **(B)** PATH B — docs + one template artefact (unit
  file under `docs/operators/` or `examples/service/`)
  that operator pastes / copies, with placeholders only.
- **(C)** PATH C — docs + template + thin wrapper script
  under `scripts/release/`.

**Default recommendation.** **(B) PATH B** as default
closure path: one operator-facing recipe (e.g.,
`docs/operators/service-supervision.md`) + one template
artefact (e.g., `examples/service/mcp-server.service` or
`docs/operators/service/mcp-server.service`). PATH C is
acceptable if the wrapper script stays under the Step 3
LOC cap (default ≤ 150 LOC stdlib-only) and avoids new
dependencies. PATH A acceptable as fallback if Step 2
audit reveals a strong reason to keep Step 4 entirely
prose-only.

### Q4 — where do template / config artefacts live?

**Options.**
- **(A)** `docs/operators/service/` — co-located with the
  Track J `docs/operators/deployment-boundary.md` recipe.
- **(B)** `examples/service/` — co-located with
  `examples/demo-infobase/` / `examples/demo-dumps/`.
- **(C)** `scripts/release/` — co-located with
  `install.ps1`.

**Default recommendation.** **(A)** for unit-file
templates and recipe docs (operator-readable artefacts);
**(C)** for any wrapper script (operator-runnable
artefact, by Track C precedent). `examples/service/`
rejected by default — it would mix declarative service
config with the in-repo demo-infobase artefacts, which
have a different purpose.

### Q5 — are restart / status / logs expectations mandatory for closure?

**Options.**
- **(A)** All five lifecycle verbs (start / stop / restart /
  status / logs) mandatory for closure.
- **(B)** Only start / stop mandatory; restart / status /
  logs documented but not closure-blocking.
- **(C)** Only start documented; everything else recommended.

**Default recommendation.** **(A) all five mandatory** for
closure. The cost is low (each verb is a one-line `systemctl`
/ `sc.exe` / `launchctl` command on the target OS family)
and the operator benefit is large. Step 3 contract should
lock this.

### Q6 — does Track L need production code modification?

**Options.**
- **(A)** NO. All three MCP server entrypoints already
  block in the foreground until `KeyboardInterrupt` /
  process termination; that is the correct shape for a
  process the OS service manager owns.
- **(B)** YES, narrow — e.g., a `--pidfile` flag, a
  graceful-shutdown signal handler beyond `SIGINT`, an
  optional structured-startup-message line on stdout that
  service-managers can match.
- **(C)** YES, broader — e.g., refactor to background
  / daemonise.

**Default recommendation.** **(A) NO** — the existing
foreground-blocking shape is **the correct shape** for a
`systemd` `Type=simple` unit, a Windows `SCM`-managed
service via `nssm`-style wrapping, or a `launchd` plist.
`Type=forking` / `daemonize=true` are explicitly rejected
because they trade implementation simplicity for a
historically buggier supervision contract. **(B)** is
acceptable only if Step 2 audit reveals a concrete defect
in the foreground-blocking shape; default expectation =
no defect, no code change. **(C)** explicitly rejected by
§7.

### Q7 — what SemVer bump does Track L justify?

**Options.**
- **(A)** NO-BUMP. Track L closes under existing `0.5.1`
  if Step 4 = PATH A (docs-only) or PATH B (docs +
  declarative template, no code change). This mirrors
  Track J and Track K closure precedent (both NO-BUMP).
- **(B)** PATCH `0.5.1 → 0.5.2`. Track L closes with a
  PATCH bump only if Step 4 = PATH C and the wrapper
  script is honestly framed as a defect-class fix
  (default: not the case; nothing is broken).
- **(C)** MINOR `0.5.1 → 0.6.0`. Track L closes with a
  MINOR bump only if Step 4 ships net-new external
  capability for ordinary product consumers — e.g., a new
  `--pidfile` flag on the server entrypoints, or a new
  CLI subcommand under `[project.scripts]`. The default
  expectation rejects this — Track L's intent is to add
  no new external capability, only documented supervision
  guidance.
- **(D)** MAJOR. Explicitly rejected by track scope (no
  backward-incompatible change is contemplated).

**Default recommendation.** **(A) NO-BUMP** as the
strongly preferred Step 6 Q7 outcome. PATCH considered
only if Step 4 introduces a wrapper script under
`scripts/release/` and operator framing makes "defect-
class" honest; MINOR considered only if Step 4 introduces
a new CLI flag on existing server entrypoints. Track L
plan §8 guardrails are designed to keep Step 4 at PATH B
default, which yields NO-BUMP by symmetry with Track J /
Track K.

---

## §13. Step trajectory preview

| Step | Kind | Default file surface | Default scope cap |
| --- | --- | --- | --- |
| Step 1 (this) | planning | 2 new docs + README + PROJECT-STATUS | docs-only |
| Step 2 | descriptive baseline audit | 1 new doc under `docs/architecture/track-l-*-baseline-audit.md` | docs-only |
| Step 3 | normative contract | 1 new doc under `docs/architecture/track-l-*-contract.md` | docs-only |
| Step 4 | narrow implementation (PATH A / B / C) | ≤ 2 new files under `docs/operators/service/` (and optionally `scripts/release/`); production code untouched; pyproject untouched | one OS family implementation slice; cross-OS prose may appear |
| Step 5 | docs / operator / release alignment | narrow CLASS-1 only: README, possibly `docs/release-handoff.md`, possibly `apps/platform/README.md`; NO production code; NO pyproject | scope locked by Step 3 contract |
| Step 6 | final integration pass and track closure | README + PROJECT-STATUS + CHANGELOG; optionally `pyproject.toml` if Q7 = PATCH or MINOR | NO production code; Q7 decision explicit |

---

## §14. Honest summary

**What Track L will do.** Convert the "no formal service-
supervision story" gap into one disciplined operator-facing
recipe (and at most one accompanying template artefact),
preserving every Tracks A–K invariant byte-identical.

**What Track L will not do.** It will not introduce a
custom daemon, will not promise production-grade
supervision for hostile-network exposure, will not promise
cross-OS parity at the same level of rigour for the closure-
gate target, will not add a packaging ecosystem, will not
introduce new MCP tools, will not change registries, will
not run `1cv8.exe`, will not push to GitHub automatically.

**Why this is the next right narrow track.** Every prior
post-phase track left "service supervision" in its honest-
non-goals list. Track L closes that bucket the same way
Track J closed "deployment boundary" and Track K closed
"real MCP client integration test": one document and at
most one operator-facing artefact, with explicit denial of
the broader claims a less disciplined version of the same
track would make.

**Default Q7 outcome.** NO-BUMP, closing under existing
`0.5.1` (matching Track J and Track K precedent). Q7 lock
is Step 6 territory.
