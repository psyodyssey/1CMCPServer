# Track K — Real MCP Client Integration Test Contract (Normative)

> **Status.** Track K / Step 3 — normative contract.
> Step 1 (commit `02783df`) opened the track with two
> planning documents and a narrow active-track flip in
> README / PROJECT-STATUS. Step 2 (commit `62069a5`)
> shipped a descriptive baseline audit with 14-item
> handoff list. This document — Step 3 — is the
> **normative** layer: it formalizes the closure-gate
> definition, pins the final Step 4 PATH, locks the
> Step 4 file surface, and locks the Step 4
> verification harness so that Track K cannot drift
> into adjacent territories (new MCP tools, registry
> change, transport redesign, auth-scheme change,
> deployment-boundary redesign, packaging ecosystem,
> service supervision, enterprise identity).
>
> Normative keywords (**MUST**, **MUST NOT**,
> **SHOULD**, **SHOULD NOT**, **MAY**) follow RFC 2119
> / RFC 8174 conventions. Where this document
> re-states a rule already pinned by an earlier track,
> it does so by **carry-forward** and **MUST NOT**
> weaken the original rule.

> **Authoritative version pin (read-time grounding).**
> `pyproject.toml` `version = 0.5.1` (preserved through
> Track J closure `dd86261`, Track K Step 1 opening
> `02783df`, and Track K Step 2 audit closure
> `62069a5`). Registry invariants `read = 15 / write =
> 25 / intelligence = 16` carried through into Track K
> Step 3. HEAD before this commit = `62069a5`.

---

## 1. Purpose / scope

### 1.1 — Why this contract exists

Track K's mandate (Step 1 plan §1, §5) is to close the
"no real MCP client integration proof" honest gap that
was carried forward through every prior MCP-transport-
track closure (Tracks G / H / I / J). Step 2's
descriptive audit established that:

- the runtime **internally** implements a plausible
  MCP interpretation (`initialize` /
  `notifications/initialized` / `ping` /
  `tools/list` / `tools/call` recognised in
  `_handle_request`; HTTP path enforces bearer auth
  with failure-equivalence + redaction discipline +
  `/mcp` POST-only + 1 MiB body cap; deterministic
  404 on non-`/mcp`; 405 + `Allow: POST` on wrong
  method; protocolVersion = `"2024-11-05"`);
- but **no externally-probed evidence** of this
  exists in the repo today: zero `tests/` directory;
  zero `test_*.py`; zero `*smoke*` Python; no
  MCP-client harness fragment anywhere.

This contract pins the rules that make Step 4
near-mechanical: it defines what counts as honest
proof, what file surface Step 4 may touch, and what
verification harness Step 4's commit must satisfy.

### 1.2 — What this contract does

- Carries forward Step 2 audit §4–§6 evidence
  byte-identical (no re-litigation).
- Promotes Step 2 directional Q1–Q6 resolutions
  into normative MUST / SHOULD / MAY rules.
- Pins **PATH B (narrow harness)** as the final
  Step 4 PATH (PATH A docs-only and PATH C hybrid
  rejected per §9 below).
- Locks Step 4 file surface to **exactly one new
  file at `scripts/dev/mcp_client_smoke.py`**, ≤300
  LOC stdlib-only soft cap, no new
  `[project.dependencies]`.
- Locks the closure-gate scenario:
  `initialize` + `tools/list` + at least one
  read-only `tools/call` exercised against
  `mcp-read-server` over **both** `--transport
  stdio` and `--transport http`, plus the HTTP
  401 failing-mode probe.
- Locks a 22-check Step 4 verification harness
  (§12).
- Forbids any maturity / hostile-network /
  enterprise / multi-tenant / "client integration
  solved" framing in Step 4 / Step 5 / Step 6
  deliverables.

### 1.3 — What this contract does NOT do

- **MUST NOT** rewrite any production code.
- **MUST NOT** add or change MCP tools.
- **MUST NOT** change registries (`read = 15 /
  write = 25 / intelligence = 16` invariant).
- **MUST NOT** change `pyproject.toml`.
- **MUST NOT** modify any existing file under
  `scripts/*`. Step 4 **MAY** add the single new
  harness file at `scripts/dev/mcp_client_smoke.py`
  but **MUST NOT** modify
  `scripts/dev/{bootstrap_paths.ps1,launch.ps1,run_dev_check.ps1,selfcheck.py,README.md}`
  or any file under `scripts/release/`.
- **MUST NOT** change `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/
  README.md`, `CHANGELOG.md`, `README.md`,
  `PROJECT-STATUS.md`, `examples/*`, manuals.
  Those are Step 5 / Step 6 alignment territory.
- **MUST NOT** rewrite Track K Step 1 plan or
  step-map, Track K Step 2 audit, or any Track A–J
  contract. Where this document references them,
  it does so by citation.
- **MUST NOT** redesign Track G stdio transport,
  Track H HTTP transport, Track H bearer auth,
  Track I installer auth round-trip, or Track J
  deployment-boundary contract. All carry-forward
  byte-identical.
- **MUST NOT** introduce in-process TLS, mTLS,
  JWT, OAuth, OIDC, SAML, SCIM, RBAC, ABAC,
  per-tool ACL, per-tenant isolation, rate
  limiting, WAF, IDS, DDoS protection, supervisor
  daemon / systemd unit / Windows Service / hot
  reload, web UI, observability stack, packaging
  ecosystem, standalone `apps/platform`
  entrypoint, `/healthz` / `/readyz` / `/livez`
  endpoint, multi-version 1С matrix expansion,
  rollback whitelist expansion, AST work, or any
  1cv8 work.
- **MUST NOT** make a SemVer decision. The bump
  (if any) is Step 6 / Q7 territory; default
  expectation per Step 1 plan §12 / Step 2 audit
  §8.6 is **NO-BUMP**.
- **MUST NOT** push to a remote.
- **MUST NOT** include any real credential, real
  hostname, real certificate, or real env-var
  value in any committed text.

---

## 2. Relationship to Step 1 plan and Step 2 audit

### 2.1 — Layer roles

| Step | Role | Output |
|---|---|---|
| Step 1 | Direction-setter | Plan + step-map; opens the track and pins scope/openness boundaries. |
| Step 2 | Descriptive baseline | Audit document; states what already exists, what is missing, and directional Q1–Q6 resolutions. |
| **Step 3 (this doc)** | **Normative layer** | **Contract; promotes Step 2 directional findings into MUST / SHOULD / MAY rules and pins Step 4 PATH.** |
| Step 4 | Implementation (per pinned PATH) | Per §9 / §10 below: **one new harness file** at `scripts/dev/mcp_client_smoke.py`. |
| Step 5 | Operator / docs / release alignment | Narrow CLASS-1 edits to point at the Step 4 harness. |
| Step 6 | Closure | Final integration pass; Q7 SemVer decision (default NO-BUMP); track closure narrative. |

### 2.2 — Re-litigation rule

This contract **MUST NOT** re-litigate Step 2 evidence
without new contradictory facts. Step 2's audit
methodology — full read of `selfcheck.py`,
`verify-release.ps1`, `_stdio_transport.py`,
`_network_transport.py`, three `__main__.py`,
`pyproject.toml`; whole-repo glob for `tests/`,
`test_*.py`, `*smoke*`, `examples/*`; classification
into the 4-class breakdown — produced the findings
this contract consumes. Step 3 drafting did not
surface contradictory evidence. Therefore Step 3
**MUST** consume Step 2 findings as load-bearing.

### 2.3 — Carried-forward invariants from earlier tracks

The following are **not** Track K's to change; this
contract preserves them by reference:

- **Track G / Step 4** — `_stdio_transport.py`
  runtime; line-delimited JSON-RPC 2.0 over
  stdin/stdout; trusted-local-subprocess threat
  model; no auth on stdio.
- **Track H / Step 4** — `_network_transport.py`
  runtime; HTTP/1.1 `/mcp` POST-only endpoint;
  bearer auth with failure-equivalence + redaction
  discipline; 1 MiB body cap; non-`/mcp` 404;
  non-POST 405; multi-`Authorization` 400; 415 on
  wrong Content-Type; 413 over-cap.
- **Track H / Step 3 contract §10** — `--bind`
  rules (no default, required-when-http,
  `socket.gethostbyname` validation); `--auth-token-env`
  rules; precedence (CLI wins, replace not merge).
- **Track H / Step 3 contract §13** — TLS posture
  (in-process TLS forbidden; reverse-proxy
  deployment model; mTLS out-of-scope).
- **Track I / Step 4** — `installer.py:_config_to_dict`
  auth round-trip preservation. Track K does not
  touch this.
- **Track J / Step 3 contract §6** —
  Forwarded-header MUST-NOT-consume policy
  (`X-Forwarded-*` / `Forwarded` / `X-Real-IP` /
  `True-Client-IP` / `CF-Connecting-IP`).
- **Track J / Step 3 contract §7** — per-scenario
  MUST/SHOULD/MAY matrix for deployment.
- **Track J / Step 3 contract §8** — `/healthz`
  defer.
- **`protocolVersion`** in `_handle_request`'s
  `initialize` arm = `"2024-11-05"`. Step 4 harness
  **MUST NOT** modify this; harness MAY observe
  and assert it.

---

## 3. Inherited fixed decisions from Step 2

The following Step 2 directional findings (audit §8)
are **promoted** in this contract from "directional"
to "normative". This section is the bridge from Step
2's descriptive language to Step 3's MUST/SHOULD/MAY
language.

### 3.1 — Q1 normative resolution (client class)

> The closure gate is **Class B** (minimum-viable
> real-client-compatible harness shipped as a single
> new file in the repo). Class A (third-party real
> client such as Claude Desktop / `mcp-cli` /
> equivalent) is **recommended-only** and **MUST NOT**
> be the closure gate. Class C (hybrid Class A +
> Class B) collapses to Class B for the closure-gate
> definition; any Class A demonstration is
> recommended-only operator-facing material that
> Step 5 / Step 6 **MAY** mention but **MUST NOT**
> require.

### 3.2 — Q2 normative resolution (transport coverage)

> Closure gate **MUST** exercise both
> `--transport stdio` and `--transport http`. Stdio is
> the default transport per Track G; HTTP exercises
> the bearer-auth + reverse-proxy-deployment surface
> per Track H / Track J. Skipping either leaves a
> material surface unverified.

### 3.3 — Q3 normative resolution (Step 4 PATH)

> Step 4 **MUST** be **PATH B (narrow harness)**.
> PATH A (docs-only) and PATH C (hybrid) are
> rejected by §9 below for the reasons given there.

### 3.4 — Q4 normative resolution (minimum scenario)

> The closure-gate scenario per server / per transport
> **MUST** include:
>
> 1. `initialize` request → assert `protocolVersion =
>    "2024-11-05"` and well-shaped `serverInfo` /
>    `capabilities`;
> 2. `tools/list` request → assert non-empty `tools`
>    array and well-shaped per-entry `name` /
>    `description` / `inputSchema`;
> 3. at least one read-only `tools/call` against a
>    tool registered by `mcp-read-server` →
>    assert `_serialize_tool_result`-shaped envelope
>    (`content` / `isError` keys present).
>
> The HTTP transport pass **MUST** additionally
> include the **failure-equivalence probe** per §7.4
> below.
>
> Multi-server coverage (`mcp-write-server` /
> `mcp-intelligence-server`) is **recommended-only**
> and **MUST NOT** be the closure gate. The harness
> **MAY** be parameterised per-server but **MUST NOT**
> fail closure if only `mcp-read-server` is
> exercised.

### 3.5 — Q5 normative resolution (insufficient evidence)

> The following **MUST NOT** be accepted as closure
> evidence on their own:
>
> - `selfcheck.py` output;
> - `verify-release.ps1` output;
> - in-process invocation of `_handle_request` with a
>   constructed dict;
> - reading the contract documents
>   (Track G / H / I / J / Track K Step 1 / Step 2 /
>   this contract);
> - operator-side demonstration (Claude Desktop /
>   `mcp-cli` / equivalent) that is **not** recorded
>   as a byte-replayable artefact in the closure
>   commit;
> - Track A / Track E reference-stand runbooks
>   (orthogonal — 1С-binary integration, not
>   MCP-client integration);
> - vague "it worked locally" / screenshot-only
>   narrative.

### 3.6 — Q6 normative resolution (production-code modification)

> Track K **MUST NOT** modify any existing production
> code (`apps/*/src/`, `packages/*/src/`,
> `installer.py`, `_stdio_transport.py`,
> `_network_transport.py`, `__main__.py`, etc.) at
> any step. Step 4 **MAY** add **exactly one** new
> file at the location pinned by §10.1.

### 3.7 — Q7 normative deferral (SemVer)

> Step 3 **MUST NOT** decide the SemVer bump. The
> bump (or no-bump) is Step 6 closure territory.
> Default expectation per Step 1 plan §12 / Step 2
> audit §8.6 = **NO-BUMP**. PATCH `0.5.1 → 0.5.2` is
> permitted **only** if Step 4 ships a defect-class
> fix observable by end-users — which a stand-alone
> diagnostic harness file is not. MINOR / MAJOR
> bumps are **forbidden** by track scope (§7 of Step
> 1 plan; §13 of this contract).

---

## 4. Closure-gate contract

### 4.1 — Definition

The closure gate for Track K is the production of a
**byte-replayable artefact in the repo** that
demonstrably exercises the platform's MCP method set
end-to-end against at least one running MCP server
process over both supported transports.

### 4.2 — Required form

The closure-gate artefact **MUST**:

- live as exactly one new file in the repo (per
  §10.1);
- be runnable on the operator's local machine after
  the documented PYTHONPATH bootstrap (Track C /
  Phase 0 baseline);
- launch the MCP server process(es) it exercises
  via `subprocess.Popen([sys.executable, "-m",
  mcp_<server>, ...])` (or equivalent stdlib
  invocation), without depending on third-party
  process supervisors;
- speak JSON-RPC 2.0 envelope shape over the wire
  (stdin/stdout for stdio path; HTTP/1.1 `POST
  /mcp` for HTTP path) using only stdlib
  facilities;
- assert response envelope shapes (per §7) and
  exit non-zero on any assertion failure;
- print operator-readable progress lines to
  `stdout` describing each step it performs;
- print a final summary line that includes the
  word `OK` on success or a clear failure
  description.

### 4.3 — Replayability requirement

The closure-gate artefact **MUST** be replayable from
the repo without operator-supplied configuration
beyond:

- a Python interpreter satisfying
  `pyproject.toml` `requires-python >= "3.11"`;
- the documented PYTHONPATH bootstrap
  (`scripts/dev/bootstrap_paths.ps1`);
- for the HTTP path **only**, an environment
  variable holding a synthetic bearer token (the
  harness **MUST** generate the token value
  itself at run time using `secrets.token_urlsafe`
  or equivalent stdlib API; the operator does **not**
  supply a real token).

The harness **MUST NOT** require a real reverse
proxy, real TLS certificate, real hostname, or real
1С infobase. The harness **MUST NOT** read any file
under `examples/demo-dumps/` or any 1С binary.

### 4.4 — Manual / screenshot artefacts insufficient

Manual demonstrations recorded as commit-message
prose, screenshots in `docs/`, or "tested locally"
assertions **MUST NOT** be accepted as closure
evidence. The closure gate is the runnable artefact
itself, not the narration around it. Step 5 /
Step 6 narrative **MAY** describe what the harness
does and **MAY** record an optional Class A
operator-side observation as recommended-only, but
the closure gate is the file.

---

## 5. Allowed client-class contract

### 5.1 — Class B as the closure gate

Per §3.1, Class B (minimum-viable harness) is the
closure gate. Step 4 **MUST** ship a Class B
harness.

### 5.2 — Class A as recommended-only

Step 4 **MAY** include in its commit-message body a
short paragraph describing how an operator could
optionally point a Class A real client (Claude
Desktop, `mcp-cli`, or equivalent) at one of the
servers and observe successful interoperation. Such
description is **recommended-only**, **MUST NOT** be
required for closure, and **MUST NOT** include any
real credential, real hostname, or real third-party
client URL beyond a generic mention of the tool name.

### 5.3 — Class C collapses to Class B

A "hybrid" Class C closure (running both Class B
harness and Class A operator demonstration) is
permitted but the closure-gate **definition** is
unchanged: only the Class B harness is what proves
Track K's gap closed. Class A observations are
narrative addenda.

---

## 6. Transport-coverage contract

### 6.1 — Both transports MUST be exercised

Per §3.2, the closure gate **MUST** exercise both
`--transport stdio` and `--transport http`. The
harness **MUST**:

- launch one server process under
  `--transport stdio` and complete the §3.4
  scenario against it;
- launch a separate server process under
  `--transport http --bind 127.0.0.1:<EPHEMERAL_PORT>
  --auth-token-env <SYNTHETIC_VARNAME>` and
  complete the §3.4 scenario against it;
- shut down each process cleanly before launching
  the next (no concurrent server processes are
  required; serial launch + clean shutdown is
  sufficient and simpler).

### 6.2 — Ephemeral port handling

For the HTTP path, the harness **MUST** select an
ephemeral port via stdlib `socket` facilities (e.g.,
`socket.socket().bind(("127.0.0.1", 0))` to
discover a free port; close the discovery socket;
pass the discovered port to the server). The
harness **MUST NOT** hardcode a port number; the
test must not collide with operator-side processes.

### 6.3 — Bind host MUST be loopback

The harness **MUST** bind the HTTP server to
`127.0.0.1` (loopback) only. Track J §7 scenario A
matches: local-only / development on the operator's
own machine. The harness **MUST NOT** bind to
`0.0.0.0`, public-routable IPs, or non-loopback
private IPs. No reverse proxy is exercised because
the harness lives on the same host as the server
(Track J §7 scenario A allows omitted reverse
proxy on loopback).

### 6.4 — Token MUST be synthetic and process-local

The HTTP harness **MUST**:

- generate a synthetic bearer token using
  `secrets.token_urlsafe(<N>)` (recommended N ≥ 32)
  at run time;
- export the token via `os.environ[<SYNTHETIC_VARNAME>] = <token>`
  before launching the server subprocess;
- pass `--auth-token-env <SYNTHETIC_VARNAME>` to
  the server subprocess;
- send the token in the harness's
  `Authorization: Bearer <token>` header for
  passing-mode probes;
- omit / mangle the header for the failure-mode
  probe (§7.4);
- **MUST NOT** print the token value to `stdout` /
  `stderr` / log file in any form (no value, no
  length, no prefix, no suffix, no hash, no
  fingerprint — same redaction discipline as the
  listener applies, observable at the harness
  level).

The synthetic variable **name** (e.g.,
`MCP_CLIENT_SMOKE_TOKEN`) is not a secret and may
appear in the harness source / commit message; the
**value** **MUST NEVER** be committed.

---

## 7. Minimum proof scenario contract

### 7.1 — Per-server / per-transport scenario

For each `(server, transport)` pair the harness
exercises (closure-gate minimum =
`(mcp-read-server, stdio)` + `(mcp-read-server,
http)`), the harness **MUST** perform the following
sequence and assert the listed shape constraints:

#### 7.1.1 — `initialize`

- Send a JSON-RPC 2.0 request with
  `"method": "initialize"` and a unique `id`
  (integer or string).
- Receive a response.
- Assert `result.protocolVersion == "2024-11-05"`.
- Assert `result.serverInfo.name` is a non-empty
  string.
- Assert `result.serverInfo.version` is a non-empty
  string.
- Assert `result.capabilities` is a JSON object
  containing a `tools` key.

#### 7.1.2 — `notifications/initialized` (optional)

- The harness **MAY** send a JSON-RPC 2.0
  notification with `"method":
  "notifications/initialized"` and no `id`.
- The harness **MUST NOT** assert any response (the
  server returns `None` per `_handle_request`;
  HTTP yields 204; stdio yields nothing).

#### 7.1.3 — `tools/list`

- Send a JSON-RPC 2.0 request with
  `"method": "tools/list"`.
- Receive a response.
- Assert `result.tools` is an array with length
  matching the registry expectation for that
  server (15 for read; 25 for write; 16 for
  intelligence) — the harness **MAY** assert
  `len(tools) >= 1` instead of the exact count
  to keep the harness loose to future registry
  bumps; the **stricter** equality assertion is
  **recommended-only**.
- For each entry, assert `name` is a non-empty
  string, `description` is a string,
  `inputSchema` is a JSON object.

#### 7.1.4 — `tools/call` (one read-only tool)

- Choose any one tool name returned by
  `tools/list` (the harness **MAY** prefer
  `health_summary` if present, but **MUST NOT**
  hardcode a specific tool name).
- Send a JSON-RPC 2.0 request with
  `"method": "tools/call"`,
  `"params": {"name": <chosen>, "arguments": {}}`.
- Receive a response.
- Assert `result.content` is an array with at
  least one entry; each entry has `type` and
  (for `type == "text"`) `text`.
- The `result.isError` flag **MAY** be either
  `true` or `false` — read-only tools may
  legitimately return `isError=True` for synthetic
  inputs, and that is well-shaped, not a
  failure of Track K's gate.

### 7.2 — Stdio framing

The harness's stdio code path **MUST**:

- write each request as a single line (one JSON
  envelope, no embedded newlines, terminated by
  `\n`) to the server's `stdin`;
- read responses as single lines from the server's
  `stdout` (one JSON envelope per line);
- route the server's `stderr` to a buffer or log
  file and **MUST NOT** confuse `stderr` content
  with `stdout` envelopes;
- flush after each write; close `stdin` to signal
  EOF when finished.

### 7.3 — HTTP framing

The harness's HTTP code path **MUST**:

- send each request as `POST /mcp` with
  `Content-Type: application/json` and
  `Authorization: Bearer <token>`;
- send body as a UTF-8-encoded JSON object (one
  envelope per request);
- accept response as `200 OK` with `Content-Type:
  application/json` and a JSON-object body, or
  `204 No Content` for notifications;
- assert no `Set-Cookie` header is present (the
  listener does not issue cookies);
- assert the response body fits the body-cap
  expectation if material to the assertion.

### 7.4 — Failure-equivalence probe (HTTP only)

After the §7.1 passing-mode scenario completes on
HTTP, the harness **MUST** send one additional
request with the `Authorization` header omitted.
Assertions:

- Response status code = `401 Unauthorized`.
- Response header `WWW-Authenticate` = `Bearer
  realm="mcp"` (case-insensitive header name; exact
  value match including the `realm="mcp"` part).
- Response body is JSON-shaped with
  `error.code == -32001` (the Track H Step 3
  contract `JSONRPC_AUTH_FAIL_CODE`).

The harness **MAY** additionally probe a malformed-
scheme variant, a wrong-token variant, or a
multi-`Authorization` 400 variant. These additional
probes are **recommended-only**.

### 7.5 — Server lifecycle

For each transport the harness:

- spawns the server process via
  `subprocess.Popen` with explicit `stdin` /
  `stdout` / `stderr` pipes (stdio path) or
  explicit CLI flags (HTTP path);
- waits for server startup before issuing the
  first request — for stdio, the server is ready
  as soon as the process is launched; for HTTP,
  the harness **SHOULD** poll the bind port via
  `socket.create_connection((host, port),
  timeout=<seconds>)` until success or a
  reasonable timeout (recommend ≤10 seconds);
- after the scenario completes, signals the
  server to exit cleanly (close stdin for stdio;
  send SIGTERM via `process.terminate()` for
  HTTP);
- waits for process exit with a timeout
  (`process.wait(timeout=<seconds>)`); on timeout,
  escalates to `process.kill()`.

The harness **MUST NOT** orphan server processes.
The harness **MUST** print operator-readable lines
indicating each lifecycle phase.

---

## 8. Insufficient-evidence contract

Per §3.5, the following are explicitly **MUST NOT**
be accepted as closure-gate evidence:

- **selfcheck.py output alone.** Bypasses
  transport; in-process callable invocation only.
- **verify-release.ps1 output alone.** Inherits
  selfcheck's limitation; adds repo-shape checks
  irrelevant to client integration.
- **In-process `_handle_request(req, ...)`
  invocation with a constructed dict.** Closer
  than selfcheck (exercises the switch) but still
  bypasses the wire and the transport-layer
  framing/auth.
- **Reading the contract documents.** Track G §6
  / §8, Track J §6 / §7, Track K Step 2 audit,
  this contract are normative or descriptive
  statements **about** what the runtime should do;
  they are not evidence that it **does**.
- **Operator-side demonstration without commit-
  recorded evidence.** Track-J-style "I ran
  Claude Desktop and it worked" with no commit
  artefact leaves the closure outside the repo.
- **Track A / Track E reference-stand runbooks.**
  Orthogonal — they prove 1С-binary integration,
  not MCP-client integration.
- **Screenshots or images committed in `docs/`.**
  Not byte-replayable; not assertable.
- **CI green elsewhere.** The project ships no
  CI / test suite; an external CI green narrative
  is outside the closure-gate framing.

Step 4 commit body **MUST NOT** rely on any of the
above as primary closure evidence. The closure gate
is exclusively the runnable harness file's
demonstrable execution.

---

## 9. Final Step 4 PATH selection and rationale

### 9.1 — Decision

**Step 4 MUST be PATH B (narrow harness).**

PATH A (docs-only) and PATH C (hybrid) are
**rejected**.

### 9.2 — Why PATH B

Step 2 audit §7 enumerated the missing proof
elements; every one of them is a runnable artefact,
not a documentation artefact. PATH A operationalizes
documentation; Track J Step 4 already shipped the
documentation that the deployment-boundary surface
needs. The Track K gap is specifically
*evidence-of-runtime-behaviour*, which prose
cannot supply. PATH B ships exactly the byte-
replayable artefact the gap calls for.

PATH B is achievable within track scope discipline:

- one new file (≤300 LOC stdlib-only soft cap);
- no modification to any existing file;
- no new `[project.dependencies]`;
- no registry change;
- no `pyproject.toml` change;
- no production-code modification;
- exercises existing surfaces only.

### 9.3 — Why not PATH A

PATH A (docs-only) would document an operator-side
procedure (Class A) but not produce a byte-
replayable closure artefact. Per §4.4 above, manual
demonstrations are insufficient for closure. PATH A
would leave the closure-gate evidence outside the
repo and dependent on third-party tooling
availability.

The Step 1 plan / Step 2 audit kept PATH A alive as
a planning option specifically so this Step 3
contract could reject it on the basis of evidence
rather than dogma. The evidence is now in: §4.4
plus §8 plus the Step 2 audit's repo-shape findings
(zero replayable smoke artefact today) make PATH A
the weaker honest closure, not the narrower
one.

### 9.4 — Why not PATH C

PATH C (hybrid: PATH B harness + PATH A operator-
facing demonstration document) inherits PATH B's
strength but adds a second deliverable file that
duplicates Step 5 territory. Step 5 is the
operator-facing alignment step; Track K Step 4
**MUST NOT** pre-empt it. Class A operator-side
recommendations belong in Step 5 alignment edits
(if any) or in Step 6 closure narrative, not in a
parallel Step 4 document.

PATH C is therefore rejected as scope creep
relative to PATH B without a corresponding
closure-strength benefit.

### 9.5 — Reversibility

Future tracks **MAY** revisit Class A integration
testing, multi-server matrix harness expansion,
multi-transport-with-real-reverse-proxy harness,
multi-protocol-version compatibility testing, or
similar. Those are separate-track decisions with
their own scope, plan, audit, contract,
implementation, alignment, and closure. Track K
**MUST NOT** preempt them.

---

## 10. Exact Step 4 implementation surface

### 10.1 — Allowed file surface for Step 4

Step 4 **MUST** ship exactly one new file:

- **`scripts/dev/mcp_client_smoke.py`** (default
  filename; this contract pins this exact path).

The contract pins this location rather than
`examples/mcp-client-smoke/run.py` because:

- the harness is operator-runnable diagnostic
  tooling (analogous in role to
  `scripts/dev/selfcheck.py`), not a worked-
  example artefact;
- placing it under `scripts/dev/` makes it
  discoverable next to existing dev wrappers;
- `examples/` has historically been reserved for
  demo-config / demo-dump artefacts (Track C +
  Track E precedent);
- one canonical location avoids Step 5 cross-link
  ambiguity.

### 10.2 — Forbidden file surface for Step 4

Step 4 **MUST NOT** modify or create any file other
than `scripts/dev/mcp_client_smoke.py`. Specifically
forbidden:

- any file under `apps/*/src/`,
  `packages/*/src/`;
- `pyproject.toml`;
- any existing file under `scripts/dev/` or
  `scripts/release/`;
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `README.md`, `PROJECT-STATUS.md`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`,
  `docs/operators/deployment-boundary.md`;
- any file under `examples/*` (existing
  artefacts byte-identical; no new file under
  `examples/` either, since §10.1 pins
  `scripts/dev/`);
- `docs/architecture/track-k-real-mcp-client-integration-test-{plan,step-map,baseline-audit}.md`,
  this contract — Track K Step 1 / 2 / 3
  deliverables immutable, cited only;
- any new MCP tool registration, registry
  modification, or `[project.scripts]` entry.

### 10.3 — Stdlib-only / no new dependency

The Step 4 harness **MUST** import only from the
Python standard library. Permitted modules
(non-exhaustive but illustrative):

- `argparse`, `json`, `os`, `sys`, `subprocess`,
  `socket`, `secrets`, `shlex`, `signal`, `time`,
  `typing`, `urllib.request`, `urllib.error`,
  `urllib.parse`, `email.message`, `pathlib`,
  `dataclasses`, `enum`.

The harness **MUST NOT**:

- add to `pyproject.toml` `[project.dependencies]`;
- import from `mcp` (the third-party MCP SDK), any
  HTTP client library other than stdlib, any
  test framework (pytest / unittest), or any
  third-party JSON library;
- import internal `mcp_common._stdio_transport` /
  `mcp_common._network_transport` (these are
  **server-side** internals, not client-side
  reusable APIs; importing them would couple the
  harness to internals it should not depend on).

The harness **MAY** import internal package names
**only** to read the registry expectation from
`mcp_read_server.list_tools()` / etc. — but this
is **discouraged**; the harness **SHOULD** assert
on response shape rather than on the import-time
list. The recommended approach is to issue
`tools/list` and assert `len(tools) >= 1` (per
§7.1.3) without importing any internal package.

### 10.4 — Required content of the Step 4 deliverable

The Step 4 file `scripts/dev/mcp_client_smoke.py`
**MUST** contain:

1. A module docstring explaining what the file does,
   that it is a Track K closure-gate artefact, and
   how to run it.
2. A `__main__` block invoking a `main()` function.
3. An `argparse` CLI with at minimum a
   `--server {read,write,intelligence}` flag
   (default `read`) and a
   `--transport {stdio,http,both}` flag (default
   `both`).
4. Functions implementing the §7.1 scenario for
   stdio (e.g., `run_stdio_scenario(...)`) and
   the §7.1 + §7.4 scenario for HTTP (e.g.,
   `run_http_scenario(...)`).
5. Assertions implemented as `assert <expr>,
   <message>` statements **or** as explicit
   `if not <expr>: raise SystemExit(<code>)`
   constructs. Either is acceptable; the harness
   **MUST** exit non-zero on any assertion
   failure.
6. Operator-readable progress prints (one line per
   phase).
7. A final summary print containing the literal
   string `OK` on success, or a clear failure
   description on failure.
8. Synthetic-bearer-token generation via
   `secrets.token_urlsafe(<N>)` for the HTTP path;
   environment variable export via `os.environ`;
   the variable **name** is harness-internal
   (e.g., `MCP_CLIENT_SMOKE_TOKEN` or similar) and
   **MUST NOT** collide with operator-likely env
   names.
9. Ephemeral port discovery for the HTTP path per
   §6.2.
10. Subprocess lifecycle management per §7.5 (clean
    shutdown; kill-on-timeout escalation; no orphan
    processes).

### 10.5 — Forbidden content of the Step 4 deliverable

The Step 4 file **MUST NOT** contain:

- any real bearer token, real env-var value, real
  hostname, real TLS certificate fragment, real
  internal IP, real DNS name — examples are
  abstract or omitted;
- any claim of enterprise-readiness / hostile-
  internet-readiness / multi-tenant-readiness /
  zero-trust-readiness / "client integration
  solved" / "interop fully proven" /
  "production-ready client compatibility";
- any forward-looking promise about features
  Track K does not ship (`/healthz`, in-process
  TLS, mTLS, additional MCP method support
  beyond the §7 scenario);
- any new MUST / MUST NOT rule the Step 4 author
  invents on their own. Step 4 is operationalization,
  not normative re-design. If a new rule needs to
  be pinned, the Step 4 author **MUST** stop and
  surface it as a Step 3 contract amendment, not
  ship it directly;
- any code that reads from or writes to a 1С
  infobase, runs `1cv8.exe`, or modifies any file
  outside the harness's own controlled subprocess
  pipes.

### 10.6 — Length and tone

Step 4 deliverable **SHOULD** be ≤ 300 lines (soft
cap; ≤ 400 if multi-server parameterisation
naturally pushes higher). Code **SHOULD** be
straightforward stdlib-Python; no metaprogramming,
no decorators-as-DSL, no fancy abstractions. The
harness is diagnostic tooling, not production
infrastructure.

---

## 11. Carry-forward invariants / backward compatibility

### 11.1 — Track G stdio baseline

`packages/mcp-common/src/mcp_common/_stdio_transport.py`
preserved byte-identical from Track G / Step 4
forward through Track K / Step 4 / Step 5 / Step 6.
Step 4 **MUST NOT** touch this file.

### 11.2 — Track H HTTP baseline

`packages/mcp-common/src/mcp_common/_network_transport.py`
preserved byte-identical from Track H / Step 4 /
Track J carry-forward through Track K. Step 4
**MUST NOT** touch this file.

### 11.3 — Track I installer baseline

`apps/platform/src/onec_platform/installer.py`
preserved byte-identical. Step 4 **MUST NOT** touch
this file.

### 11.4 — Track J deployment-boundary baseline

Track J §13 / §6 / §7 / §8 carried forward
unchanged: in-process TLS forbidden, mTLS forbidden,
Forwarded-header MUST-NOT-consume policy,
per-scenario MUST/SHOULD/MAY matrix preserved,
`/healthz` not shipped. The harness exercises
loopback only (Track J §7 scenario A) and does
**not** introduce any of the above.

### 11.5 — Registries

Registry counts **MUST** remain `read = 15 / write
= 25 / intelligence = 16` through Track K / Step 4
/ Step 5 / Step 6. Step 4 **MUST NOT** add or
remove any MCP tool. The selfcheck at every step
**MUST** confirm `selfcheck_status=ok` and the
three-count invariant.

### 11.6 — `pyproject.toml`

`pyproject.toml` **MUST** remain `version =
"0.5.1"` through Step 3 (this commit), Step 4,
Step 5. Step 6 **MAY** bump per Q7 default
(NO-BUMP) or PATCH `0.5.1 → 0.5.2` only if Step 4
ships a defect-class fix (which a stand-alone
diagnostic harness file is not). MINOR / MAJOR
bumps are forbidden by track scope.

### 11.7 — No secret-management / hostile-network claims

Track K at no step **MUST NOT** characterize the
platform as "secrets-managed", "vault-backed",
"KMS-integrated", "hostile-internet-ready",
"enterprise-ingress-ready", "zero-trust-ready",
"multi-tenant-ready", or similar. Track J §11.6
carry-forward.

### 11.8 — No new MCP tools / no registry change

Step 4 **MUST NOT** register a new MCP tool with any
of the three servers. Step 4 **MUST NOT** modify
any tool registration. The harness reads tool names
via `tools/list` at runtime and asserts on shape;
it does not introduce new tool registrations.

---

## 12. Verification contract for Step 4

Step 4's commit **MUST** demonstrate the following
at the time of commit:

### 12.1 — Scope checks

1. Working tree contains exactly one expected new
   file (`scripts/dev/mcp_client_smoke.py`).
2. No other file is modified.
3. Production code untouched (`apps/*/src/`,
   `packages/*/src/`).
4. `pyproject.toml` untouched (`version =
   "0.5.1"` preserved).
5. Existing files under `scripts/dev/` and
   `scripts/release/` byte-identical.
6. `SECURITY.md` / `docs/release-handoff.md` /
   `apps/platform/README.md` / `CHANGELOG.md` /
   `README.md` / `PROJECT-STATUS.md` / manuals /
   `docs/operators/deployment-boundary.md` /
   `examples/*` byte-identical.
7. Track K Step 1 / 2 / 3 architecture documents
   byte-identical.

### 12.2 — Registry / selfcheck checks

8. `selfcheck_status=ok`.
9. Registries `read = 15 / write = 25 /
   intelligence = 16` confirmed unchanged.

### 12.3 — Release-verify check

10. `verify-release.ps1 -AllowDirtyTree` GREEN on
    all eight checks (Repo layout / Release
    entrypoints / Important docs / Working tree
    (1 uncommitted accepted) / Git baseline /
    Selfcheck / Credential leak guard / Credential
    template hygiene).

### 12.4 — Honesty checks

11. No `1cv8.exe` runs in Step 4.
12. No real credentials in committed text (no
    real tokens, env-var values, hostnames,
    certificate fragments). Verified by manual
    review of the deliverable.
13. No premature Track-K closure language.
    Verified by grep on `Track K.*(закрыт треком|
    completed|shipped production|implemented in
    Step 4|merged|finalized|GA-ready|production-
    ready|enterprise-ready|deployment solved|
    hostile-network-ready|battle-tested|track
    closure|client integration solved|production-
    ready client compatibility|interop fully
    proven)` returning zero matches against the
    Step 4 deliverable.
14. No false implementation claims. The harness
    runs successfully against all three servers
    on both transports (or against the closure-
    gate minimum `mcp-read-server` on both
    transports, with multi-server coverage
    documented as recommended-only). Verified by
    Step 4 author running the harness and recording
    `OK` output evidence in the commit message.
15. No fake "client integration solved" / "interop
    fully proven already" / "production-ready
    client compatibility" framing.

### 12.5 — Harness-runnability checks (PATH B specific)

16. The harness **MUST** be runnable via
    `python scripts/dev/mcp_client_smoke.py
    --server read --transport both` (after
    `bootstrap_paths.ps1` PYTHONPATH setup).
17. The harness **MUST** exit `0` on a clean
    successful run.
18. The harness **MUST** exit non-zero on any
    assertion failure.
19. The harness's final summary line **MUST**
    include the literal string `OK` on success.
20. The harness **MUST NOT** orphan server
    processes (verified via the Step 4 author's
    local run; commit message records the
    observation).
21. The harness **MUST NOT** print the bearer
    token value at any verbosity level (verified
    via `grep` of harness output for the token
    value during Step 4 author's local run).
22. Step 4 commit message **MUST** include the
    raw final summary line from the harness's
    successful run as evidence (operator-readable;
    abstracted-placeholders-only).

### 12.6 — Verification verdict

If checks 1–22 are GREEN, Step 4 closes. If any
check fails, Step 4 **MUST NOT** be committed; the
author **MUST** fix the harness and re-verify.

---

## 13. Honest non-goals

This contract restates the Track K non-goals so
they are MUST-NOT-do for Step 4 / Step 5 / Step 6:

- **MUST NOT** introduce in-process TLS / HTTPS
  termination (Track H §13.1 / Track J §5 carry-
  forward).
- **MUST NOT** introduce mTLS / client certificate
  authentication (Track H §13.3 carry-forward).
- **MUST NOT** introduce JWT / OAuth 2.0 / OIDC /
  SAML / SCIM / federated identity.
- **MUST NOT** introduce RBAC / ABAC / per-tool
  ACL / per-tenant isolation / multi-tenant
  identity.
- **MUST NOT** introduce token rotation endpoint /
  refresh tokens / session cookies.
- **MUST NOT** introduce rate limiting / WAF / IDS
  / DDoS protection / anomaly detection.
- **MUST NOT** introduce supervisor daemon /
  systemd unit / Windows Service registration /
  launchd / hot reload / restart watcher /
  auto-update.
- **MUST NOT** introduce packaging ecosystem
  (`.msi` / `.deb` / signed distribution / GUI
  installer / wizard / PyPI publication / wheel
  publication beyond `[project.scripts]`).
- **MUST NOT** introduce web UI / dashboard
  frontend.
- **MUST NOT** introduce observability stack
  (OpenTelemetry / Jaeger / Prometheus /
  OpenMetrics / log aggregation / distributed
  tracing).
- **MUST NOT** introduce a standalone
  `apps/platform` entrypoint.
- **MUST NOT** introduce `/healthz` / `/readyz` /
  `/livez` endpoint (Track J §8 carry-forward).
- **MUST NOT** add new MCP tools or change
  registries.
- **MUST NOT** add to `pyproject.toml` outside
  Step 6 Q7 SemVer bump (default = NO-BUMP).
- **MUST NOT** run `1cv8.exe` (Track K operates
  on MCP client / transport layer; not on 1cv8
  binary surface).
- **MUST NOT** push to a remote (operator
  action; not part of any Track K step).
- **MUST NOT** commit real credentials or real
  hostnames in any deliverable.
- **MUST NOT** rewrite Track G / Track H /
  Track I / Track J contracts or runtime.
- **MUST NOT** redesign auth scheme, error
  envelopes, or HTTP method/path policy.
- **MUST NOT** expand multi-version 1С matrix /
  rollback whitelist / AST coverage in any
  Track K step.
- **MUST NOT** make any `1.0.0` / `production-
  ready` / `GA` claim.

---

## 14. Step 4 handoff note

### 14.1 — Step 4 opening ritual

When Step 4 opens, the author **MUST**:

1. Confirm clean working tree (HEAD = the Step 3
   commit).
2. Re-read this contract end-to-end. Step 4
   **MUST NOT** start drafting before this.
3. Confirm Step 1 plan / Step 2 audit / this
   contract are all citable (Step 4 deliverable
   references them; modifying them is forbidden).
4. Confirm the file path
   `scripts/dev/mcp_client_smoke.py` does **not**
   yet exist (Step 4 creates it fresh).

### 14.2 — Step 4 output ritual

When Step 4 commits:

1. Subject **MUST** be exactly:
   `Track K / Step 4 — narrow MCP client smoke harness`.
2. Body **MUST** include: why one new harness file
   is sufficient; exact file added; what was
   intentionally NOT touched; verification summary
   (per §12 — all 22 checks); explicit
   confirmation that no registries changed / no
   new MCP tools / no `1cv8.exe` / no remote
   push / no real credentials; PATH B pinned per
   this contract; harness's raw `OK` output as
   evidence of successful local run.
3. Step 5 (operator / docs / release alignment)
   is the next opening and **MUST NOT** be
   opened in the same commit.

### 14.3 — Step 4 verification harness

Step 4 author **MUST** run, at minimum:

```
git status --short
python scripts\dev\mcp_client_smoke.py --server read --transport both
.\scripts\release\verify-release.ps1 -AllowDirtyTree
```

…and the 22 checks listed in §12. If any fail,
Step 4 commit **MUST NOT** be created.

### 14.4 — What Step 4 does NOT do

- Does not edit Step 1 plan / Step 2 audit / this
  contract.
- Does not edit `SECURITY.md` /
  `docs/release-handoff.md` /
  `apps/platform/README.md` / manuals /
  `README.md` / `PROJECT-STATUS.md` /
  `CHANGELOG.md` (Step 5 territory).
- Does not bump SemVer (Step 6 territory).
- Does not run `1cv8.exe`.
- Does not push to a remote.
- Does not invent new normative rules.

### 14.5 — Step 5 / Step 6 preview

This contract pins enough to make Step 5
mechanical:

- Step 5 = narrow CLASS-1 alignment of operator-
  facing surfaces. At minimum: README.md
  Quickstart paragraph + Active parallel track
  section reflect Step 4 closed and Step 5
  active; `docs/release-handoff.md` "What is in
  this handoff" + "Where to read deeper" lists
  may add a one-bullet pointer to the harness.
  Whether to add a recipe-side cross-link from
  `docs/operators/deployment-boundary.md` is a
  Step 5 judgment call (likely no — the recipe is
  about deployment boundary, not about MCP
  client testing). PROJECT-STATUS.md / CHANGELOG
  / `pyproject.toml` / closed-tracks list NOT
  touched (Step 6 territory). Track K still
  framed as **active** in this commit.
- Step 6 = final integration pass; Q7 SemVer
  call (default NO-BUMP per §3.7 / §11.6);
  track-closure narrative; README.md Closed
  parallel tracks list extended десять →
  одиннадцать; PROJECT-STATUS.md header flipped
  to no-active-step; CHANGELOG.md Track K
  closure subsection (under existing 0.5.1
  if Q7=NO-BUMP, mirroring Track J pattern);
  no production code changes; eleventh post-
  phase parallel track closed.

---

## 15. Honest summary

This contract:

- Carries forward Track G §6 / §10 / §13, Track H
  §6 / §8 / §10 / §13, Track I §11.5, Track J §6
  / §7 / §8 byte-identical (no weakening).
- Promotes Step 2 audit's directional Q1–Q6
  resolutions to normative MUST / SHOULD / MAY
  rules.
- Pins **PATH B (narrow harness)** as the final
  Step 4 PATH on the basis that Track K's gap is
  specifically *evidence-of-runtime-behaviour*
  which prose cannot supply, and Step 4 can
  produce a byte-replayable runnable artefact in
  one new stdlib-only ≤300-LOC file without
  touching production code.
- Pins the §10.1 location
  (`scripts/dev/mcp_client_smoke.py`) as
  canonical.
- Pins the §7 minimum scenario as load-bearing
  closure-gate evidence: `initialize` +
  `tools/list` + one read-only `tools/call`
  against `mcp-read-server` over **both**
  transports + HTTP 401 failure-equivalence
  probe.
- Pins the §6.4 synthetic-token discipline as
  invariant: harness generates its own token via
  `secrets.token_urlsafe`; no operator-supplied
  real credential; no token value ever printed.
- Constrains Step 4's verification harness to 22
  concrete checks across scope, selfcheck,
  release-verify, honesty, and harness-
  runnability.
- Forbids any maturity / hostile-network /
  enterprise / multi-tenant / "client integration
  solved" framing in Step 4 / Step 5 / Step 6.
- Forbids SemVer pre-commit (Step 6 / Q7
  territory; default expectation = NO-BUMP).
- Forbids code changes outside the one new
  Step 4 harness file, registry changes, new MCP
  tools, `1cv8.exe` runs, real credentials, and
  remote push at every Track K step.

Step 3 is therefore closeable as a single
normative contract document, with **Track K /
Step 4 — narrow MCP client smoke harness (PATH B,
single new file at `scripts/dev/mcp_client_smoke.py`)**
as the next opening.
