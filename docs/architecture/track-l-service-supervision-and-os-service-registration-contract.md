# Parallel Track L — Service Supervision and OS Service Registration — Contract

**Status.** Normative contract document produced by Track L /
Step 3 at HEAD `d58c8d9` (Track L / Step 2 closure). This
document uses RFC 2119 MUST / MUST NOT / SHOULD / SHOULD
NOT / MAY language. It pins the final Step 4 PATH and locks
every Step 4 / Step 5 / Step 6 boundary that derives from
the Step 2 baseline audit. It is **not** an implementation;
Step 4 implements within this contract's surface caps.

**Companion documents.**

- [`track-l-service-supervision-and-os-service-registration-plan.md`](track-l-service-supervision-and-os-service-registration-plan.md)
  — Step 1 planning document (14 sections, Q1–Q7 directional
  defaults).
- [`track-l-service-supervision-and-os-service-registration-step-map.md`](track-l-service-supervision-and-os-service-registration-step-map.md)
  — Step 1 step-map (16 invariants, 18 categorical denials,
  6-step boundary).
- [`track-l-service-supervision-and-os-service-registration-baseline-audit.md`](track-l-service-supervision-and-os-service-registration-baseline-audit.md)
  — Step 2 descriptive baseline audit (9 sections, 10
  enumerated absences, 14 handoff items, Q1–Q6 directional
  resolutions).

---

## §1. Purpose / scope

### §1.1 What this contract is

A single prescriptive normative document that translates
the Step 2 audit's directional Q1–Q6 resolutions and 14
Step 3 handoff items into RFC 2119 MUST / MUST NOT / SHOULD
/ SHOULD NOT / MAY rules. The contract pins the final
Step 4 PATH, the final implementation-covered OS family,
the lifecycle-coverage minimum, the allowed Step 4 file
surface, the forbidden Step 4 file surface, the closure-
gate definition, the insufficient-evidence list, the
carry-forward invariants, and the verification protocol.
Step 4 implements **within** this contract's surface caps;
Step 5 / Step 6 operate within this contract's forbidden-
file lists.

### §1.2 What this contract is not

This contract is **not** an implementation. It does not
ship a unit file, a recipe, or a wrapper script. It does
not modify production code, `pyproject.toml`, or any
existing `scripts/*` file. It does not rewrite Step 1 plan
or Step 2 audit anchors. It does not move Track L into
README's Closed parallel tracks list — Track L remains
**active** through Step 5; closure narrative is Step 6
territory only.

### §1.3 RFC 2119 keyword usage

The key words **MUST**, **MUST NOT**, **REQUIRED**,
**SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**,
**RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

### §1.4 Track L scope reminder (binding)

In scope (carry-forward from plan §6, audit §1.3): planning,
audit, contract (this document), narrow implementation,
docs-alignment, and closure for service supervision plus
OS service registration of the three existing MCP server
surfaces; lifecycle vocabulary (start / stop / restart /
status / logs); preserving every Tracks G / H / I / J / K
invariant byte-identical.

Out of scope (carry-forward verbatim from plan §7, step-map
"Track L hard out-of-scope", audit §1.3): new MCP tools;
registry changes; transport redesign; auth redesign;
deployment-boundary redesign; packaging ecosystem;
enterprise identity stack; clustering / HA / load-
balancing / orchestration platforms; web UI; full
observability stack; `/healthz` endpoint; standalone
`apps/platform` daemon entrypoint; hot reload / zero-
downtime restart guarantee; automatic update / OTA / self-
upgrade; rollback / AST / multi-version 1С matrix
expansion; `1cv8` work; remote push. The phrases "service
supervision solved" / "production-ready service
supervision" / "all OS families supported" / "clustered
HA" / "zero-downtime restart" MUST appear in any Track L
deliverable only as explicit DENIALS.

---

## §2. Relationship to Step 1 plan and Step 2 audit

### §2.1 Step boundary

The six-step boundary established by the Step 1 step-map
is **binding**:

- Step 1 = planning (closed at `e713f8e`).
- Step 2 = descriptive baseline audit (closed at
  `d58c8d9`).
- Step 3 = normative contract (this document).
- Step 4 = the **only** step that MAY add an
  implementation or declarative-template artefact.
- Step 5 = docs / release / operator alignment (narrow
  CLASS-1).
- Step 6 = final integration pass and track closure
  with explicit Q7 SemVer decision.

### §2.2 Re-litigation rule

Step 3 **MUST NOT** reopen Step 2 audit findings unless
new contradictory repo evidence emerges. The contract is
permitted to **tighten** directional resolutions into
normative locks, to **narrow** Step 4 PATH selection from
multiple acceptable options to a single chosen option, and
to **add** Step-4-specific caps and forbidden-file lists
that did not appear in the audit. It is **not** permitted
to soften, reverse, or contradict any Step 2 conclusion.

### §2.3 Carried-forward Q1–Q6 audit resolutions

Step 2 audit §7 produced six directional resolutions.
This contract **MUST** preserve their direction:

- Q1 audit-directional: service supervision target =
  recipe + declarative template + five lifecycle verbs.
  → Locked normatively below in §4 / §5 / §6.
- Q2 audit-directional: systemd / Linux first, cross-OS
  prose for Windows + macOS.
  → Locked normatively below in §5.
- Q3 audit-directional: PATH B as default; PATH A and
  PATH C acceptable per Step 3 decision.
  → **Locked normatively below in §7 as PATH B.**
- Q4 audit-directional: all five lifecycle verbs
  mandatory.
  → Locked normatively below in §6.
- Q5 audit-directional: six insufficient-evidence
  categories.
  → Locked normatively below in §9.
- Q6 audit-directional: no production code change.
  → Locked normatively below in §8.

---

## §3. Inherited fixed decisions from Step 2

These observations from the Step 2 audit are **fixed
inputs** to this contract. The contract treats them as
load-bearing facts and does not re-prove them. Any
attempt to contradict them in Step 4 / Step 5 / Step 6 is
out-of-contract.

1. **`Type=simple`-compatible foreground-blocking shape.**
   The three MCP server `__main__.py` modules
   (`apps/mcp-read-server/src/mcp_read_server/__main__.py`,
   `apps/mcp-write-server/src/mcp_write_server/__main__.py`,
   `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`)
   are trivially-thin (~40 LOC each) and block the
   invoking process until the transport loop exits. Audit
   §3.1.

2. **`KeyboardInterrupt`-mediated graceful shutdown.**
   `packages/mcp-common/src/mcp_common/_stdio_transport.py:208`
   and
   `packages/mcp-common/src/mcp_common/_network_transport.py:618–624`
   handle `KeyboardInterrupt` gracefully. HTTP path uses
   `httpd.daemon_threads = True` at line 607, so in-flight
   requests are abandoned on shutdown by design — this is
   **explicit policy**, not a defect. Audit §3.1 / §3.3.

3. **No `signal.signal(SIGTERM, ...)` handler installed.**
   The only signal-related call in production code is
   `os.kill(pid, signal.SIGTERM)` inside
   `apps/platform/src/onec_platform/process_control.py:178`
   (POSIX `terminate_pid`), which is the supervisor
   **sending** SIGTERM, not the supervised process
   **handling** it. Audit §6.5.

4. **`apps/platform/src/onec_platform/runtime.py` is
   adjacent but orthogonal.** Phase 5 / Step 3 + Phase 6 /
   Step 6 in-process supervisor for operator-declared
   product-layer subprocesses (declared in
   `ProductConfig.runtime.services` with
   `restart_policy ∈ {"never", "restart-if-stale"}`). Its
   module docstring (lines 21–31) explicitly says "not a
   daemon manager / service manager (no Windows Service /
   systemd unit registration on this step)" and "does NOT
   start MCP transports inside the three servers". This
   contract **MUST** preserve `runtime.py` byte-identical
   and **MUST NOT** extend it. Audit §3.4 / §5.1.

5. **CLI surface already sufficient.** Each server accepts
   `--transport {stdio,http}`, `--config-path <path>`,
   `--log-level <level>`, plus for HTTP `--bind
   <HOST>:<PORT>` and `--auth-token-env <VARNAME>`.
   Sufficient for any reasonable systemd `ExecStart=`,
   launchd `ProgramArguments`, or Windows-service argv
   without adding a new flag. Audit §4.2.

6. **stderr-only diagnostic logging.** All three servers
   log to stderr (audit §4.3). OS service managers capture
   stderr to their respective stream destinations
   (journald / launchd `StandardErrorPath` / NSSM
   `AppStderr` / Windows Service framework). No Python-
   layer log-path configuration is required. Audit §4.3.

7. **Env-var-based auth token.** Track H Step 4 wired
   `--auth-token-env <VARNAME>`. The supervised path
   sources the token from operator-managed environment
   variables; no real credentials enter the repo. Audit
   §4.4.

8. **Operator-machine context is Windows-resident.**
   `examples/demo-infobase/infobase6.config.json` shows
   `C:/Users/user/Documents/InfoBase6`,
   `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`.
   Audit §7.2 acknowledges this but recommends systemd-
   first for **broadest industrial precedent**, not for
   the specific operator's primary OS. The contract honors
   the audit's recommendation in §5 below.

9. **Track J `docs/operators/deployment-boundary.md` is
   the topology sibling.** The recipe Step 4 ships under
   `docs/operators/service/` (see §8) is the **process-
   lifecycle sibling** of the deployment-boundary recipe.
   They are orthogonal axes that operators read together.
   Audit §3.5.

10. **Ten clearly missing pieces.** Audit §6 enumerated
    them; the contract treats each as a closure target
    rather than re-enumerating them here. The Step 4
    artefact MUST address at minimum: missing service-unit
    template; missing operator lifecycle-verb vocabulary;
    missing `EnvironmentFile=` discipline for token
    secrets in supervised context; missing `Restart=`
    policy guidance; missing `User=` / `Group=` / service-
    account discipline guidance.

---

## §4. Closure-gate contract

### §4.1 Definition of "honest Track L closure"

Track L closure (Step 6) **REQUIRES** all of the following
to be true at Step 6 commit:

1. **C1 — Recipe artefact.** Exactly one operator-facing
   recipe document MUST exist at the Step-4-locked path
   under `docs/operators/service/` (see §8.2).
2. **C2 — Declarative template artefact.** Exactly one
   declarative service-unit template MUST exist at the
   Step-4-locked path under `docs/operators/service/`
   (see §8.3).
3. **C3 — Lifecycle coverage.** All five lifecycle verbs
   (start, stop, restart, status, logs) MUST be documented
   end-to-end on the implementation-covered OS family
   (§5); MUST be at minimum referenced with vetted-
   external-reference prose for the other two OS families
   covered by the recipe.
4. **C4 — Implementation-covered OS family.** Exactly one
   OS family MUST be implementation-covered with both the
   recipe walkthrough and the declarative template (§5).
5. **C5 — Cross-OS prose.** The recipe MUST contain prose
   coverage for the other two OS families (Windows and
   macOS, in any order). Prose-only coverage MUST be
   honestly framed in the recipe — operators MUST be told
   which OS family is implementation-covered and which are
   prose-only.
6. **C6 — Placeholder discipline.** All examples in the
   recipe and template MUST use abstract placeholders only
   (`<USER>`, `<GROUP>`, `<HOST>`, `<PORT>`, `<UNIT_NAME>`,
   `<SERVICE_NAME>`, `<LOG_PATH>`, `<VARNAME>`,
   `<MCP_TOKEN_VARNAME>`, `<PYTHONPATH>`,
   `<WORKING_DIR>`). No real domains, ports, accounts,
   tokens, paths, or hostnames.
7. **C7 — Honest non-goals.** The recipe MUST contain
   explicit denial of "service supervision solved forever",
   "production-ready service supervision", "all OS
   families supported", "clustered HA", "zero-downtime
   restart", "hostile-network-ready service exposure",
   "automatic update / OTA", "enterprise-grade identity
   integration".
8. **C8 — Carry-forward invariants.** §10 invariants MUST
   all be observable as byte-identical in the Step 6
   commit's `git diff` against the relevant surfaces.
9. **C9 — Verify-release GREEN.** `verify-release.ps1`
   (and `-AllowDirtyTree` during the working pass)
   **MUST** be GREEN on all 8 checks at every Track L
   commit from Step 3 onward.
10. **C10 — Selfcheck OK.** Registries
    `read=15 / write=25 / intelligence=16` and
    `selfcheck_status=ok` MUST be confirmed at every
    Track L commit from Step 3 onward.

### §4.2 What does NOT count as closure-gate proof

The following MUST NOT, on its own, be accepted as Track L
closure-gate evidence (locked from audit §5 / §6 / §7.5):

- Launch instructions only (e.g., a paragraph in README).
- Release docs only (e.g., a bullet under "What is in this
  handoff").
- Generic deployment prose without an OS-facing recipe.
- Operator lore not committed to the repo.
- `docs/operators/deployment-boundary.md` standing in for
  a service-supervision recipe (orthogonal axis).
- Screenshots, video, or external-link-only artefacts.
- Extending `apps/platform/src/onec_platform/runtime.py`
  to also supervise the MCP servers in-process. This is
  **rejected** by plan §12.Q1 option C and contradicts
  `runtime.py:24` "does NOT start MCP transports inside
  the three servers". The supervision concern MUST stay
  **outside** the platform process tree, on the OS layer.
- A wrapper script that calls `python -m mcp_<server>`
  in the background without involving an OS-level service
  manager.
- A markdown checklist of "run these commands to start"
  without a declarative service-unit artefact.
- A unit file lacking either `[Unit]` / `[Service]` /
  `[Install]` (for systemd), or `<key>Label</key>` /
  `<key>ProgramArguments</key>` (for launchd), or NSSM
  `--AppStdout` / `--AppStderr` / `--AppExit` style
  configuration commitments (for Windows NSSM-based
  prose).

### §4.3 What service-registration proof Step 4 MUST commit

The Step 4 artefact MUST commit, in repo, **declarative**
service-unit content sufficient for the operator to:

- copy the template to the OS service manager's
  expected location (e.g., `/etc/systemd/system/`),
- substitute placeholders for their environment, and
- run the five lifecycle verbs in the recipe walkthrough.

The artefact MUST NOT depend on imperative shell scripts
that hide service-manager invocations from the operator.
The point of the declarative template is that the operator
sees and owns the service-manager configuration.

---

## §5. Implementation-covered OS family contract

### §5.1 Final pick — systemd / Linux

Step 4's implementation-covered OS family **MUST** be
**systemd on Linux**. The template artefact MUST be a
single `.service` unit file at the path locked in §8.3.
The recipe walkthrough MUST exercise the five lifecycle
verbs against this systemd unit.

### §5.2 Defence of the systemd-first pick

The contract makes this pick from these repo-grounded
facts (audit §7.2 + this section):

- **Broadest industrial precedent.** systemd is the
  default init system on every mainstream Linux
  distribution shipped since the mid-2010s (Debian /
  Ubuntu / Fedora / RHEL / SUSE / Arch). A single
  declarative unit file maps to a known operator
  vocabulary across all of them.
- **Cleanest declarative model.** `[Unit]`, `[Service]`,
  `[Install]` sections; `ExecStart=`, `Restart=`,
  `User=`, `Group=`, `EnvironmentFile=`, `KillSignal=`
  keys — each documented in `systemd.service(5)` /
  `systemd.exec(5)`. No imperative shell required for
  the template itself.
- **Well-known lifecycle vocabulary.** `systemctl start`,
  `systemctl stop`, `systemctl restart`, `systemctl
  status`, `journalctl -u <unit>` — five verbs, five
  one-line commands per the §6 contract.
- **Native foreground-blocking compatibility.** The
  three MCP server `__main__.py` modules' `Type=simple`-
  compatible shape needs no adaptation. `KillSignal=SIGINT`
  is a single-line override that re-routes service stop
  to the existing `KeyboardInterrupt` branch.

### §5.3 Cross-OS prose — Windows and macOS

The recipe MUST contain a Windows section AND a macOS
section, in any order. Each cross-OS section MUST:

- name a canonical service manager (Windows: NSSM, or
  pywin32-based service wrapper, or Windows Service
  Control Manager via `sc.exe` — the recipe MUST pick
  one and stick to it; default RECOMMENDED = NSSM
  because it avoids a Python dependency and avoids
  re-implementing `win32serviceutil`; macOS: `launchd`
  with a `~/Library/LaunchAgents/<label>.plist` for
  user-level or `/Library/LaunchDaemons/<label>.plist`
  for system-level — the recipe MUST pick one and stick
  to it);
- name the canonical declarative artefact shape (NSSM:
  `nssm install <SERVICE_NAME> ...` invocation
  documented in prose; launchd: a `.plist` shape
  documented inline or by reference);
- cover the same five lifecycle verbs in the cross-OS
  vocabulary (NSSM: `nssm start`, `nssm stop`,
  `nssm restart`, `sc query`, `--AppStdout` /
  `--AppStderr` log path; launchd: `launchctl bootstrap`
  / `launchctl bootout`, `launchctl kickstart -k`,
  `launchctl print`, `StandardErrorPath` / `StandardOutPath`);
- contain at most three external references (e.g., one
  per: NSSM documentation, systemd documentation,
  launchd documentation), each of which MUST be either
  an officially-maintained reference site or a well-
  established freely-available reference;
- contain explicit honest framing: "Windows / macOS
  prose-only coverage; closure-gate template is the
  systemd unit; operators on these platforms are
  expected to apply the prose to their service manager
  with operator-side validation".

### §5.4 Cross-OS template artefacts — forbidden in Step 4

Step 4 MUST NOT ship NSSM-install scripts, `.plist`
files, `.bat` wrappers, PowerShell `Install-Service`
wrappers, or any other declarative artefact for
Windows / macOS. The single Step 4 declarative artefact
is the systemd `.service` unit file. Cross-OS coverage
is prose-only.

Rationale: shipping a `.plist` or NSSM-install command
file would (a) widen the Step 4 file surface beyond
§8's ≤2-file cap, (b) commit the contract to a
specific Windows / macOS configuration we have not
validated end-to-end, (c) duplicate the abstract-
placeholder discipline twice more without
correspondingly stronger closure proof. Prose with
abstract placeholders is the narrowest honest cross-OS
coverage.

### §5.5 Future cross-OS implementation expansion is out of scope

A future track MAY ship Windows / macOS template
artefacts as part of a separate scope. Track L MUST NOT.

---

## §6. Lifecycle coverage contract

### §6.1 Five mandatory verbs

The recipe MUST cover all five lifecycle verbs end-to-end
on the implementation-covered OS family (§5.1):

1. **start** — operator command to take the MCP server
   from "not running" to "running and registered".
   systemd: `systemctl start <UNIT_NAME>` (and
   `systemctl enable <UNIT_NAME>` separately for boot
   persistence).
2. **stop** — operator command to take the MCP server
   from "running" to "not running" cleanly.
   systemd: `systemctl stop <UNIT_NAME>`.
3. **restart** — operator command to perform a
   stop-then-start cycle. systemd: `systemctl restart
   <UNIT_NAME>`.
4. **status** — operator command to read the current
   service state (active / inactive / failed; PID;
   last exit code; recent log lines). systemd:
   `systemctl status <UNIT_NAME>`.
5. **logs** — operator command to read the supervised
   process's stdout/stderr stream as captured by the OS
   service manager. systemd: `journalctl -u <UNIT_NAME>`
   (with examples for `-f` follow, `--since` time
   filter, and `-p err` priority filter).

### §6.2 Partial coverage rejection

Partial lifecycle coverage at Step 6 commit **MUST NOT**
be accepted as closure-gate evidence. If any one of the
five verbs is missing from the recipe's implementation-
covered-OS section, Step 6 MUST be re-opened.

### §6.3 Cross-OS lifecycle coverage

The Windows and macOS sections (§5.3) MUST each cover
the same five verbs in their respective OS vocabulary,
in the prose-only mode. Partial cross-OS coverage is
acceptable only if the missing verb has a clearly-
documented native-platform rationale (e.g., "Windows
NSSM provides start / stop / restart natively;
status-equivalent via `sc query` requires the operator
to know the service name they registered with"). Any
gap MUST be honestly named in the recipe section.

### §6.4 Verbs are documented procedurally, not aspirationally

Each verb MUST be presented as a concrete operator
command (or a small sequence of commands) plus the
expected operator-visible response. Aspirational
language ("operators can manage lifecycle via the
service manager") MUST NOT replace concrete command
examples.

### §6.5 What the verbs do NOT promise

The recipe MUST contain an explicit denial of:

- **No zero-downtime restart.** A supervised `restart`
  interrupts in-flight requests; client-side retry is
  the operator's concern. `daemon_threads = True` is
  explicit policy (§3 fact #2).
- **No automatic restart on graceful shutdown.**
  `Restart=on-failure` (recommended default in the
  template; see §6.6) restarts on non-zero exit, not on
  clean operator-initiated stop.
- **No hot reload.** A configuration change requires
  stop-then-start; the recipe MUST point this out.
- **No /healthz endpoint.** Track J §8 defer carried
  forward. Service "alive" is `systemctl status` or
  the corresponding cross-OS verb. Non-`/mcp` HTTP
  paths return 404 deterministically (Track H).

### §6.6 RECOMMENDED systemd `Restart=` defaults (non-binding)

The contract RECOMMENDS — but does **not** require — the
following systemd unit-file defaults. The template MAY
ship with these values or with the placeholders alongside;
Step 4 chooses.

- `Restart=on-failure` (not `Restart=always`, which
  would mask operator-initiated `systemctl stop`).
- `RestartSec=5s` (modest delay before respawn).
- `StartLimitBurst=5` over `StartLimitIntervalSec=600s`
  (rate-limit respawn loops; operator can override).
- `KillSignal=SIGINT` (re-route service stop to the
  existing `KeyboardInterrupt` graceful branch; §3
  fact #2).
- `KillMode=mixed` (send SIGINT to main process, SIGKILL
  to remaining group members after `TimeoutStopSec=`).
- `TimeoutStopSec=15s` (modest grace).

The recipe MUST document each of these values' effect.
The operator MAY override every one of them.

---

## §7. Final Step 4 PATH selection

### §7.1 Locked: PATH B

Step 4's PATH **MUST** be **PATH B** — docs + one
declarative template artefact. No code, no wrapper
script. Two new files, both under
`docs/operators/service/` (see §8).

### §7.2 PATH A explicitly rejected

PATH A (docs-only, no declarative template) is rejected.
Audit §4 closure-gate test ("zero systemd unit files
anywhere in the tree" at HEAD `d58c8d9`) cannot be closed
honestly by prose alone — prose describing a unit file
without committing the unit file leaves operators
inventing the file structure themselves, which
re-introduces the operator-machine-only-knowledge gap
Track L exists to close. Audit §7.3 leaned away from
PATH A; contract locks the rejection.

### §7.3 PATH C explicitly rejected

PATH C (docs + template + wrapper script under
`scripts/release/`) is rejected. Audit §3.2 shows that
the current install flow runs through
`scripts/release/install.ps1`, which is Windows-only and
unrelated to systemd registration. A sibling wrapper
script under `scripts/release/` would either (a) duplicate
the systemd `systemctl enable` step into PowerShell (POSIX
operators do not use PowerShell and would not run it), or
(b) require a separate `.sh` wrapper that itself becomes
a maintenance liability for marginal operator benefit
(`systemctl enable <UNIT>` is already a single command).
Audit §7.3 acknowledged PATH C as "acceptable if Step 3
authorizes it"; this contract chooses not to. The
declarative unit file with placeholders is the narrower,
more honest, more durable closure.

### §7.4 No code change defended again

Step 4 MUST NOT add a wrapper script under
`scripts/release/`, MUST NOT add any new helper under
`scripts/dev/`, MUST NOT modify any existing
`scripts/*` file, MUST NOT add a Python module, and MUST
NOT modify any file under `apps/*/src/` or
`packages/*/src/`. The only legitimate Step 4 output is
the two-file artefact described in §8.

### §7.5 PATH B file shape

PATH B is exactly two new files:

1. One operator-facing recipe document (§8.2).
2. One declarative systemd `.service` unit-file template
   with placeholders (§8.3).

Both files MUST be co-located under
`docs/operators/service/` (a new directory created by
Step 4). The directory MUST NOT receive any other Step 4
file.

---

## §8. Exact Step 4 implementation surface

### §8.1 File count cap

Step 4 MUST add **exactly two** new files and MUST NOT
modify any existing file. Step 4 MUST NOT create any
other new file under any other path. The forbidden-files
list in §8.4 is exhaustive.

### §8.2 Recipe file — exact path and required structure

The recipe file path **MUST** be:

```
docs/operators/service/service-supervision.md
```

The recipe file MUST contain at minimum:

- §1 Purpose.
- §2 Scope statement (which OS family is implementation-
  covered, which are prose-only; closure-gate target =
  systemd; cross-OS = Windows + macOS in prose).
- §3 Prerequisites (Python runtime, PYTHONPATH bootstrap
  reminder pointing at `scripts/dev/bootstrap_paths.ps1`
  for Windows or its POSIX equivalent operator-side
  pattern, env-var-based MCP token reminder pointing at
  Track H + Track J).
- §4 Service-account / permissions discipline (using
  `<USER>` / `<GROUP>` / `<WORKING_DIR>` placeholders;
  systemd `User=` / `Group=` defaults RECOMMENDED but
  not REQUIRED; cross-OS equivalents for Windows /
  macOS).
- §5 Install / register walkthrough on the closure-gate
  OS (systemd): copy template to `/etc/systemd/system/`;
  `systemctl daemon-reload`; `systemctl enable
  <UNIT_NAME>`; `systemctl start <UNIT_NAME>`; verify via
  `systemctl status <UNIT_NAME>`.
- §6 Uninstall / deregister walkthrough on the closure-
  gate OS (systemd): `systemctl stop <UNIT_NAME>`;
  `systemctl disable <UNIT_NAME>`; remove template;
  `systemctl daemon-reload`.
- §7 Full lifecycle-verb table per OS family — all five
  verbs (§6.1) for systemd; cross-OS equivalents for
  Windows / macOS per §5.3.
- §8 Troubleshooting bullets — at minimum: "service
  fails to start", "service starts but exits
  immediately", "service starts but HTTP transport binds
  fail" (cross-reference Track J recipe §3 / §4 / §5),
  "logs not appearing in journald" (cross-reference §6
  RECOMMENDED unit-file defaults).
- §9 Cross-references — to Track G `__main__.py`
  entrypoints, Track H bind / auth policy, Track J
  `deployment-boundary.md`, Track K smoke harness,
  `apps/platform/src/onec_platform/runtime.py` with
  explicit "this is **not** the supervisor; that is the
  systemd unit" framing.
- §10 Honest non-goals — explicit denial list from §6.5
  + §4.2 + audit §6 "ten clearly missing pieces that
  Track L does NOT close after Step 6".

The recipe file MUST be ≤ 1200 lines (soft cap; ≤ 1500
lines hard cap). All examples MUST use abstract
placeholders only (§4.1 C6).

### §8.3 Template file — exact path and required structure

The template file path **MUST** be:

```
docs/operators/service/mcp-server.service
```

The template MUST be a single systemd unit file with the
following minimal shape (commented inline to remain
operator-readable; line count ≤ 80 lines including
comments; placeholders only):

```ini
# Track L / Step 4 systemd unit template for the 1C Agent
# Platform MCP servers. Placeholders only. Operator
# substitutes per their environment; copy to
# /etc/systemd/system/<UNIT_NAME>.service.

[Unit]
Description=1C Agent Platform MCP server (<UNIT_NAME>)
Documentation=https://example.invalid/docs/track-l
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=<USER>
Group=<GROUP>
WorkingDirectory=<WORKING_DIR>
EnvironmentFile=<ENV_FILE_PATH>
ExecStart=<PYTHON_BIN> -m <MCP_SERVER_MODULE> \
    --transport <TRANSPORT> \
    --config-path <CONFIG_PATH> \
    --bind <HOST>:<PORT> \
    --auth-token-env <MCP_TOKEN_VARNAME>
Restart=on-failure
RestartSec=5s
StartLimitBurst=5
StartLimitIntervalSec=600s
KillSignal=SIGINT
KillMode=mixed
TimeoutStopSec=15s

[Install]
WantedBy=multi-user.target
```

The template MUST use placeholders only. No real paths,
no real users, no real ports, no real tokens, no real
hostnames. Per-placeholder semantics MUST be documented
in the recipe §4–§5 (§8.2). The template MUST NOT
import or reference any other file.

### §8.4 Forbidden file surface for Step 4 (exhaustive list)

Step 4 MUST NOT modify or create any file outside the
two listed in §8.2 / §8.3. The following list is
exhaustive — any file not listed here is **automatically
forbidden** for Step 4 by closure-of-scope discipline:

**Forbidden production code:**
- `apps/mcp-read-server/src/**`
- `apps/mcp-write-server/src/**`
- `apps/mcp-intelligence-server/src/**`
- `apps/platform/src/**`
  (specifically including `runtime.py`,
  `process_control.py`, `runtime_logs.py`,
  `models.py`, `state.py`, `installer.py`, `loader.py`).
- `packages/mcp-common/src/**`
  (specifically including `_stdio_transport.py`,
  `_network_transport.py`).
- All other `packages/*/src/**` files.

**Forbidden configuration / build:**
- `pyproject.toml`.
- `.python-version`.
- `.editorconfig`.
- `.github/**`.
- `.gitignore`.

**Forbidden existing scripts:**
- `scripts/dev/launch.ps1`.
- `scripts/dev/bootstrap_paths.ps1`.
- `scripts/dev/run_dev_check.ps1`.
- `scripts/dev/selfcheck.py`.
- `scripts/dev/mcp_client_smoke.py`.
- `scripts/dev/README.md`.
- `scripts/release/install.ps1`.
- `scripts/release/_install_runner.py`.
- `scripts/release/verify-release.ps1`.
- `scripts/release/README.md`.
- Any new file under `scripts/dev/` or
  `scripts/release/` — Step 4 PATH C is rejected.

**Forbidden Track / closure docs:**
- `README.md`.
- `PROJECT-STATUS.md`.
- `CHANGELOG.md`.
- `SECURITY.md`.
- `LICENSE`.
- `docs/release-handoff.md`.
- `apps/platform/README.md`.
- `docs/operator-manual.md`.
- `docs/administrator-manual.md`.
- `docs/developer-manual.md`.
- `docs/runbooks.md`.
- `docs/version-support-matrix.md`.

**Forbidden Track-precedent artefacts:**
- `docs/operators/deployment-boundary.md`
  (Track J / Step 4 artefact).
- `docs/runbooks/track-a-reference-stand-round-trip.md`.
- All `docs/architecture/track-{a,b,c,d,e,f,g,h,i,j,k}-*.md`
  files.
- Track L Step 1 / Step 2 docs (this contract included).

**Forbidden examples / demo data:**
- `examples/**` (no demo-infobase changes; no demo-dumps
  changes).

**Forbidden runtime / state:**
- Anything under `<work_dir>/.runtime/` (not in repo but
  named for completeness — Step 4 MUST NOT introduce
  any artefact that writes there).

**Forbidden new directories or files anywhere else.**
Any directory not named in §8.2 / §8.3 / `docs/operators/
service/` itself is forbidden. The new directory
`docs/operators/service/` may contain only the two
listed files; no `.gitkeep`, no `README.md`, no other
files.

### §8.5 LOC and dependency caps

- Recipe (§8.2): ≤ 1200 lines soft; ≤ 1500 lines hard.
- Template (§8.3): ≤ 80 lines including comments.
- Both files: stdlib-only mental model — no
  dependencies on external tools beyond the OS service
  manager itself (systemd, NSSM, launchd); no Python
  imports anywhere; no shell scripts.
- No new entries in `pyproject.toml`
  `[project.dependencies]` / `[project.optional-dependencies]` /
  `[project.scripts]`. (`pyproject.toml` is forbidden
  to Step 4 entirely — §8.4 — so this is enforced
  twice.)

---

## §9. Forbidden evidence / insufficient-evidence contract

### §9.1 Insufficient-on-its-own list (binding)

The following MUST NOT, individually or in any combination
short of meeting all of §4.1 C1–C10, count as Track L
closure-gate proof:

1. **"Just use `python -m mcp_<server>` in a terminal"** —
   current state at HEAD `d58c8d9`; whole reason Track L
   exists.
2. **Launch instructions only** — a paragraph in `README.md`
   or in `docs/operator-manual.md` describing how to run
   the server interactively.
3. **Release docs only** — a bullet in
   `docs/release-handoff.md` saying "to run as a service,
   write your own unit file".
4. **Generic deployment prose without OS-facing recipe** —
   abstract deployment prose that offloads the contract
   back to the operator.
5. **Operator lore not committed in repo** — knowledge
   that lives only in chat logs, screenshots, or
   operator-side notebooks.
6. **Extending `runtime.py` to also supervise MCP
   servers in-process** — explicitly forbidden by §3 fact
   #4 and audit §3.4. In-process supervision is not OS
   service registration; the platform process tree is
   not the OS service manager.
7. **Documentation of the deployment-boundary recipe
   only** — `docs/operators/deployment-boundary.md` is
   the network-exposure-axis sibling; it is orthogonal
   and insufficient on its own as a process-lifecycle
   recipe.
8. **A wrapper script that backgrounds `python -m
   mcp_<server>` without involving an OS service
   manager** — e.g., `nohup python -m ... &` in a
   sample script. This pattern does not survive reboots,
   does not produce a lifecycle vocabulary, and does
   not register with the OS service manager.
9. **Screenshots, videos, or external-link-only
   evidence** — any non-text artefact.
10. **A unit-file template without an operator recipe** —
    the template alone fails C1; the recipe walkthrough
    is what teaches the operator how to use the template
    end-to-end. Both files (§8.2 / §8.3) are required
    individually.
11. **A recipe without a template** — the recipe alone
    fails C2; without a declarative artefact in the
    repo, the operator re-invents the unit file.
12. **A `Type=oneshot` unit file** — `Type=oneshot` is
    for one-shot tasks; the MCP servers are long-lived
    foreground-blocking processes that require
    `Type=simple`.
13. **A unit file with `Type=forking` or
    `daemonize=true`** — explicitly rejected by plan
    §12.Q6 and inconsistent with the foreground-blocking
    runtime shape (§3 fact #1).
14. **A unit file lacking `[Unit]` / `[Service]` /
    `[Install]` sections** — incomplete systemd unit.
15. **Real credentials in the template or recipe** —
    forbidden by §4.1 C6 and by `verify-release.ps1`
    Check 7 (credential leak guard).

### §9.2 What MUST appear in the recipe as explicit denial

The recipe MUST contain explicit DENIAL of each of these
phrases / claims (each may appear in the recipe only as
a negation):

- "service supervision solved forever"
- "all OS families supported"
- "production-ready service supervision for hostile
  network exposure"
- "clustered HA"
- "zero-downtime restart"
- "automatic update / OTA"
- "enterprise-grade identity integration"
- "the platform now manages process supervision
  internally"
- "`/healthz` endpoint added"
- "any of the ten Step 2 missing pieces (§6) that Track L
  does NOT close" — Track L closes only the operator-
  facing recipe + systemd template + five lifecycle
  verbs; the broader pieces remain honest non-goals.

### §9.3 What MUST NOT appear in any Track L artefact

The following phrases MUST NOT appear in any Track L
artefact except as quoted explicit denials:

- "fully supervised"
- "production-grade service"
- "supported on all platforms"
- "supported in production"
- "hostile-network-ready"
- "enterprise-ready"

---

## §10. Carry-forward invariants / backward compatibility

Step 4 / Step 5 / Step 6 commits MUST preserve all of
these byte-identical:

### §10.1 Tracks G / H / I / J / K runtime invariants

- **Track G stdio runtime** —
  `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  byte-identical.
- **Track H HTTP runtime** —
  `packages/mcp-common/src/mcp_common/_network_transport.py`
  byte-identical. `/mcp` POST-only; 1 MiB body cap;
  bearer auth with failure-equivalence + redaction
  discipline; `WWW-Authenticate: Bearer realm="mcp"` on
  401; non-`/mcp` 404 deterministic.
- **Track I installer auth round-trip** —
  `apps/platform/src/onec_platform/installer.py`
  byte-identical. `_config_to_dict` emit branches
  unchanged.
- **Track J deployment-boundary recipe** —
  `docs/operators/deployment-boundary.md` byte-identical.
- **Track J carry-forward §13 / §6 / §7 / §8** — in-
  process TLS forbidden; mTLS forbidden; Forwarded
  headers MUST-NOT-consume; `/healthz` not shipped.
- **Track K diagnostic harness** —
  `scripts/dev/mcp_client_smoke.py` byte-identical.

### §10.2 Platform-layer invariants

- **`apps/platform/src/onec_platform/runtime.py`** —
  byte-identical. Track L MUST NOT extend it to also
  supervise MCP servers; that path is rejected by §3
  fact #4, audit §3.4, plan §12.Q1 option C, and §9.1
  item 6.
- **`apps/platform/src/onec_platform/process_control.py`** —
  byte-identical.
- **`apps/platform/src/onec_platform/runtime_logs.py`** —
  byte-identical.
- **`apps/platform/src/onec_platform/models.py`** —
  byte-identical (`ProductServiceSpec` /
  `RuntimeServiceState` / `RESTART_POLICIES` shape
  preserved).

### §10.3 Registry invariants

- `mcp-read-server` registry: 15 tools.
- `mcp-write-server` registry: 25 tools.
- `mcp-intelligence-server` registry: 16 tools.

`selfcheck status=ok` and the four-line registry summary
MUST be confirmed via `verify-release.ps1` at every Track
L commit from Step 3 onward.

### §10.4 SemVer invariants

- `pyproject.toml` `version="0.5.1"` MUST be preserved
  through Steps 3 / 4 / 5. Step 6 Q7 decision is the
  only step that MAY touch `pyproject.toml`, and only
  if Q7 = PATCH or MINOR is honestly defensible.
- Default Q7 expectation = NO-BUMP, per audit §7 + plan
  §12.Q7 + Track J + Track K precedent. This contract
  does **not** make Q7 binding at Step 3 — Step 6 does.
  But it does establish that PATH B + no production
  code change + no new public API = NO-BUMP by
  symmetry with Track J / Track K.

### §10.5 No new MCP tools, no registry change

- Step 4 / Step 5 / Step 6 MUST NOT add any new tool to
  any of the three MCP servers.
- Step 4 / Step 5 / Step 6 MUST NOT modify any tool
  registration in any of the three MCP servers.
- Step 4 / Step 5 / Step 6 MUST NOT modify
  `mcp_common/__init__.py` `__all__`.

### §10.6 No 1cv8.exe, no real credentials, no remote push

- No `1cv8.exe` runs at any step of Track L from Step 3
  onward.
- No real credentials in any committed file at any step.
  Placeholder vocabulary (§4.1 C6) is the only
  acceptable form.
- No remote push as part of any Track L commit. GitHub
  push remains an explicit operator action outside the
  track.

---

## §11. Verification contract for Step 4

### §11.1 Pre-commit verification (mandatory)

Before the Step 4 commit, the following MUST be
verified, in this order, with each result captured in
the Step 4 commit body:

**Scope checks (S1–S6):**
- **S1.** Exactly two new files under
  `docs/operators/service/` (the recipe at §8.2 and the
  template at §8.3). Verified by `git status --short`
  showing exactly two new files, no modified files.
- **S2.** No file in §8.4's forbidden list is modified.
  Verified by `git diff --name-only` returning only the
  two new file paths.
- **S3.** `git diff` against the explicit forbidden
  surfaces (production code, `pyproject.toml`,
  `scripts/`, README / PROJECT-STATUS / CHANGELOG /
  SECURITY / release-handoff / apps/platform/README /
  manuals / examples / Track-precedent architecture
  docs / Track L Step 1–3 docs) returns zero lines.
- **S4.** Recipe file LOC ≤ 1500 (hard cap, §8.5).
- **S5.** Template file LOC ≤ 80 (§8.5).
- **S6.** Recipe + template combined: no Python
  imports, no shell-script content, no
  `pyproject.toml` snippets, no `[project.scripts]`
  edits.

**Selfcheck checks (Z1–Z2):**
- **Z1.** `verify-release.ps1 -AllowDirtyTree`
  `selfcheck` line shows registries
  `read=15 / write=25 / intelligence=16` and
  `status=ok`.
- **Z2.** No registry drift since Track K closure
  (`0e40056`).

**Release-verify check (R1):**
- **R1.** `verify-release.ps1 -AllowDirtyTree` GREEN on
  all 8 checks pre-commit.

**Honesty checks (H1–H7):**
- **H1.** No `1cv8.exe` invocation in Step 4 work or
  commit message.
- **H2.** No real credentials in either Step 4 file or
  commit message. Placeholder discipline (§4.1 C6) is
  observable by grep: only `<USER>`, `<GROUP>`,
  `<HOST>`, `<PORT>`, `<UNIT_NAME>`, `<SERVICE_NAME>`,
  `<LOG_PATH>`, `<VARNAME>`, `<MCP_TOKEN_VARNAME>`,
  `<PYTHONPATH>`, `<WORKING_DIR>`, `<ENV_FILE_PATH>`,
  `<PYTHON_BIN>`, `<MCP_SERVER_MODULE>`,
  `<TRANSPORT>`, `<CONFIG_PATH>` appear as concrete
  example values.
- **H3.** No premature Track L closure language in
  Step 4 commit message. "Closed", "closure", "fully
  solved" appear only in references to **Step 4 itself
  being closed**, not Track L being closed (Step 6 is
  the closure step).
- **H4.** No false implementation claims. The recipe
  MUST NOT claim "production-ready service supervision",
  "all OS families supported", "clustered HA",
  "zero-downtime restart" except as explicit denials
  per §9.2.
- **H5.** No new MCP tools claimed; registries
  `15 / 25 / 16` unchanged.
- **H6.** No fake closure phrases. Per §9.3, the six
  forbidden phrases appear in the artefact only as
  quoted explicit denials.
- **H7.** No remote push performed by Step 4.

**Recipe / template coverage checks (C1–C10):**
- **C1.** Recipe section count ≥ 10 (§8.2).
- **C2.** Recipe contains all five lifecycle verbs in
  the implementation-covered-OS section (§6.1).
- **C3.** Recipe contains a Windows section per §5.3.
- **C4.** Recipe contains a macOS section per §5.3.
- **C5.** Recipe contains the §6.5 RECOMMENDED systemd
  defaults documented procedurally.
- **C6.** Recipe contains the §9.2 explicit-denial
  list with each phrase appearing as a negation.
- **C7.** Recipe contains §9 cross-references to
  Tracks G / H / I / J / K.
- **C8.** Template parses as valid systemd unit-file
  syntax (sections, key=value pairs, no malformed
  lines). Verified by visual inspection; optionally
  by `systemd-analyze verify` if a Linux environment is
  available. `systemd-analyze` is **not** required;
  visual inspection is sufficient.
- **C9.** Template uses placeholders exclusively.
  Grep for absolute paths (`/usr/`, `/etc/`, `/var/`,
  `C:\\`, `D:\\`, `/Library/`, etc.) returns zero
  non-comment hits.
- **C10.** Template `Type=simple` (matches §3 fact #1).

### §11.2 Post-commit verification (mandatory)

Step 4's commit MUST be followed by:

- **P1.** `verify-release.ps1` (clean tree) GREEN on
  all 8 checks.
- **P2.** Working tree clean (`git status` returns
  `nothing to commit, working tree clean`).
- **P3.** New commit count = HEAD pre-commit + 1.
- **P4.** Step 4 commit message subject = exactly
  `Track L / Step 4 — service supervision systemd template and recipe`
  (or other Step-4-canonical subject locked at Step 4
  drafting; this contract does not pre-lock the exact
  subject string, only the file surface and the
  verification protocol).

### §11.3 Step 5 verification carry-forward

Step 5 MUST satisfy:

- **V1.** Production code byte-identical to Step 4
  commit.
- **V2.** `pyproject.toml` byte-identical to Track K
  closure.
- **V3.** `scripts/*` byte-identical to Track K closure
  (no new wrapper script per PATH C rejection).
- **V4.** Step 4 deliverables byte-identical to Step 4
  commit.
- **V5.** Track K and earlier deliverables byte-
  identical.
- **V6.** `verify-release.ps1` GREEN.
- **V7.** Selfcheck OK; registries unchanged.

Step 5 MAY modify only:

- `README.md` Quickstart paragraph + Active parallel
  track section to reflect Steps 1–4 closed and Step 5
  active.
- `docs/release-handoff.md` — one bullet in "What is in
  this handoff" + one bullet in "Where to read deeper"
  pointing at the Step 4 recipe.
- `apps/platform/README.md` — only if Step 4 introduces
  a service-supervision boundary that the platform
  README's existing boundary inventory reasonably
  mentions; default expectation = no edit.
- `SECURITY.md` — only if Step 4 ships a service-
  account / permissions section that meaningfully
  intersects the existing security claim; default
  expectation = no edit.

Step 5 MUST NOT modify Track L closed-tracks list,
PROJECT-STATUS, CHANGELOG, or `pyproject.toml` —
those are Step 6 territory.

### §11.4 Step 6 verification carry-forward

Step 6 MUST satisfy:

- **W1.** Production code byte-identical.
- **W2.** `scripts/*` byte-identical.
- **W3.** Step 4 deliverables byte-identical (immutable
  Step 4 anchors).
- **W4.** Track L Step 1 / 2 / 3 deliverables byte-
  identical (immutable anchors).
- **W5.** `pyproject.toml` MAY be modified **only** if
  Q7 = PATCH or Q7 = MINOR is honestly defended in the
  Step 6 commit body. Q7 = NO-BUMP is the default
  expectation per §10.4 and audit §7.6; Step 6 chooses.
- **W6.** README / PROJECT-STATUS / CHANGELOG MAY be
  modified to reflect Track L closure (Closed parallel
  tracks list extended from одиннадцать to
  двенадцать; Track L detail (закрыт) section added;
  Track K Step 6 historical-edit annotation updated;
  CHANGELOG Track L subsection inserted).
- **W7.** `verify-release.ps1` GREEN pre-commit and
  post-commit.
- **W8.** Selfcheck OK; registries unchanged.

### §11.5 Forbidden verification proxies

The following MUST NOT be used as substitute proof for
any §11 check:

- Manual operator confirmation in chat.
- Screenshot of `systemctl status`.
- External video demo.
- "Worked on my machine" assertions in commit messages.
- Soft "should work" language without concrete `git
  diff` / `verify-release` / `selfcheck` output.

---

## §12. Honest non-goals

By Step 6 closure under this contract, Track L will
**NOT** have delivered any of the following. Each is an
explicit denial:

### §12.1 Supervisor / framework non-goals

- No in-repo Python supervisor framework.
- No `pywin32`-based service wrapper class.
- No `systemd` unit-generation Python module.
- No `launchctl` plist-generation Python module.
- No `nssm` install-script generator.
- No service-watcher daemon.
- No auto-restart-on-config-change watcher.
- No hot reload.
- No zero-downtime restart.

### §12.2 OS-family non-goals

- No Windows `.bat` / `.cmd` / `.ps1` install wrappers.
- No macOS `.plist` files in the repo.
- No `systemd-analyze verify` invocation as a release
  gate (visual inspection only; §11.1 C8).
- No multi-distro Linux compatibility matrix testing.
- No SystemV init scripts.
- No upstart configuration.
- No FreeBSD `rc.d` scripts.
- No NixOS module declarations.

### §12.3 Integration non-goals

- No `journald` log-format integration (the Python
  layer continues to log to stderr; journald captures
  it as text).
- No `Event Viewer` log-channel registration.
- No `syslog` integration.
- No `OpenTelemetry` integration.
- No `Prometheus` metrics endpoint.
- No `Jaeger` tracing.
- No `/healthz` / `/readyz` / `/livez` endpoint —
  Track J §8 defer carried forward.
- No `Systemd-readyz`-style notification protocol
  (no `sd_notify` / `Type=notify` socket).

### §12.4 Identity / auth non-goals

- No SSO / SAML / OIDC / SCIM / RBAC / ABAC /
  multi-tenant.
- No mTLS / client certificate authentication —
  Track H §13.3 carried forward.
- No in-process TLS — Track H §13.1 / Track J §5
  carried forward.
- No JWT / OAuth / refresh-token / session-cookie /
  per-tenant.
- No automatic token rotation.

### §12.5 Deployment / orchestration non-goals

- No `Kubernetes` manifests.
- No `Docker Compose` files.
- No `Nomad` job files.
- No `Consul` service registration.
- No `etcd` integration.
- No `Zookeeper` integration.
- No `HAProxy` configuration.
- No clustering / HA / load-balancing.
- No multi-instance coordination.

### §12.6 Packaging / distribution non-goals

- No `.msi` / `.deb` / `.rpm` / `.dmg` / `.pkg` /
  signed-binary distribution.
- No GUI installer / wizard.
- No `PyPI` publication.
- No wheel publication beyond the existing
  `[project.scripts]` declarations (which remain
  un-installable by Track C / Step 3 honest
  constraint).
- No `pip install`-from-source flow.

### §12.7 Other carry-over non-goals

- No web UI / dashboard frontend.
- No standalone `apps/platform` daemon entrypoint.
- No automatic update / OTA / self-upgrade mechanism.
- No rollback expansion / AST work / 1С matrix
  expansion.
- No `1cv8.exe` runs anywhere in Track L.
- No remote push.

---

## §13. Step 4 handoff note

This contract hands the following exact items to Step 4
for implementation. Step 4 MUST satisfy each item without
expansion:

1. **File count: exactly two.** Recipe at §8.2 path;
   template at §8.3 path. No other new files. No
   modified files. Verified by §11.1 S1.

2. **File location: `docs/operators/service/`.** New
   directory; co-located with Track J's `docs/operators/`.
   No other location.

3. **Recipe content: ≥ 10 sections per §8.2 structure.**
   Each section MUST be present.

4. **Recipe content: all five lifecycle verbs per
   §6.1.** Per OS family that the recipe covers.
   Implementation-covered OS family (systemd / Linux)
   MUST cover all five end-to-end. Cross-OS sections
   (Windows + macOS) MUST cover all five in prose per
   §5.3 / §6.3.

5. **Template content: ≤ 80 lines, systemd `.service`
   shape, `Type=simple`, placeholders only per §8.3.**

6. **Placeholder vocabulary fixed (§4.1 C6 + §11.1 H2).**
   Only these placeholders MAY appear: `<USER>`,
   `<GROUP>`, `<HOST>`, `<PORT>`, `<UNIT_NAME>`,
   `<SERVICE_NAME>`, `<LOG_PATH>`, `<VARNAME>`,
   `<MCP_TOKEN_VARNAME>`, `<PYTHONPATH>`,
   `<WORKING_DIR>`, `<ENV_FILE_PATH>`, `<PYTHON_BIN>`,
   `<MCP_SERVER_MODULE>`, `<TRANSPORT>`, `<CONFIG_PATH>`.
   Step 4 MAY introduce up to **two** additional
   placeholders if a clearly-named operator concept
   requires it (e.g., `<ENV_KEY_NAME>` for a per-token
   env-var) — each new placeholder MUST be motivated by
   the recipe text. No real values.

7. **RECOMMENDED systemd defaults per §6.6.** Template
   MAY ship with these defaults inline. Recipe MUST
   document each value's effect.

8. **Honest non-goals per §9.2 / §12.** Recipe MUST
   contain each denial as a negation. No false maturity
   claims.

9. **Cross-references per §8.2 §9.** Recipe MUST point
   at Tracks G / H / I / J / K artefacts; MUST
   distinguish `runtime.py` from the systemd unit; MUST
   explicitly cross-reference Track J recipe.

10. **Verification per §11.1.** All scope / selfcheck /
    release-verify / honesty / recipe-template coverage
    checks MUST PASS pre-commit. Each check's outcome
    MUST be captured in the Step 4 commit body.

11. **Commit message discipline.** Step 4 commit
    message body MUST include: §11.1 verification
    summary; Step 4 file count + paths; explicit
    "Track L still active" framing; no premature
    closure language; explicit denial that Step 4
    closes Track L (only Step 6 does).

12. **No production code change.** §10.1 / §10.2
    invariants byte-identical.

13. **No `pyproject.toml` change.** §10.4 first
    sentence.

14. **No `scripts/*` change.** §8.4 forbidden list.

15. **No README / PROJECT-STATUS / CHANGELOG change.**
    Those are Step 5 / Step 6 territory.

---

## §14. Honest summary

**This contract pins Step 4.** Two new files, both
under `docs/operators/service/`: an operator-facing
recipe and a systemd `.service` unit-file template.
PATH B locked. PATH A and PATH C explicitly rejected.
Cross-OS (Windows + macOS) prose-only coverage. Five
lifecycle verbs mandatory on the implementation-covered
OS family. RECOMMENDED systemd defaults documented but
operator-overridable.

**This contract does not pin Q7.** Step 6 chooses Q7;
the default expectation is NO-BUMP per §10.4, Track J
precedent, Track K precedent, and audit §7.6. Q7 = PATCH
considered only if Step 4 unexpectedly introduces a
defect-class fix (audit §7.6 found no such defect, so
this is not anticipated). Q7 = MINOR considered only if
Step 4 introduces a new CLI flag (rejected by §10.5 +
§3 fact #5). Q7 = MAJOR forbidden.

**This contract preserves every prior track invariant.**
§10 enumerates them; §8.4 enforces them via the
forbidden-file list; §11 verification catches drift.

**This contract makes Track L closable in the narrowest
honest way.** Two files in repo, five lifecycle verbs
documented, one OS family covered with declarative
template, two OS families covered in prose, every
prior-track surface untouched, every false-maturity
claim explicitly denied, no production code change, no
pyproject change, no scripts change, no registry
change, no `1cv8.exe` runs, no real credentials, no
remote push.

**Track L is active at Step 3.** Step 3 closes with this
contract. Step 4 is the next step and MAY be opened by
the operator in a separate session. Closure narrative
remains Step 6 territory.
