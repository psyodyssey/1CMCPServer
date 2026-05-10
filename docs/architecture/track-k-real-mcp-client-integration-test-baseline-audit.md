# Track K — Real MCP Client Integration Test (Baseline Audit)

> **Status.** Track K / Step 2 — descriptive baseline
> audit (docs-only). This document **describes** the
> client-integration approximations that already exist
> in the repository as of HEAD `02783df` (Track K /
> Step 1 closed). It does NOT add normative MUST /
> MUST NOT language; that is reserved for Step 3
> (contract). It does NOT change production code. It
> does NOT pre-commit Step 4 to docs-only or to a
> code/harness path — Step 4 PATH A / PATH B / PATH C
> openness is preserved per the Step 1 plan / step-map.

> **Authoritative version pin (read-time grounding).**
> `pyproject.toml` `version = 0.5.1` (preserved through
> Track J closure `dd86261` and Track K Step 1 opening
> `02783df`). Registry invariants `read = 15 / write =
> 25 / intelligence = 16` carried through into Track K
> Step 2.

---

## 1. Purpose / scope

### 1.1 — Why this audit exists

Track K / Step 1 (commit `02783df`) opened the eleventh
post-phase parallel track to close the "no real MCP
client integration proof" honest gap that was
explicitly carried forward through every prior
MCP-transport-track closure (Tracks G / H / I / J).
Step 1 was deliberately planning-only: two architecture
documents (plan + step-map) plus a narrow README /
PROJECT-STATUS active-track flip. Step 2 — this
document — is a descriptive audit of what the
repository already contains by way of "client
integration proof" approximations, what those
approximations actually demonstrate, and what a real
MCP-client end-to-end proof would minimally require.

The Step 1 plan §12 declared Q1–Q7 directional
defaults *based on planning intuition*. Step 2's job
is to either **confirm** those defaults from observed
repo evidence or **adjust** them where the evidence
contradicts the planning view. Step 2 does not produce
normative rules; it produces a 4-class breakdown
(already-covered / adjacent-but-insufficient /
clearly-missing / explicitly-out-of-scope) and a
Step 3 handoff list.

### 1.2 — What this audit must answer

Per Step 1 plan §13 and Step 1 step-map Step 2 row,
this audit must directionally resolve:

- **Q1** — what should count as "real MCP client" for
  Track K?
- **Q2** — is stdio-only proof enough, or should HTTP
  also be included?
- **Q3** — is the likely honest Step 4 path PATH A /
  PATH B / PATH C?
- **Q4** — what is the minimum meaningful end-to-end
  scenario (initialize / tools/list / tools/call;
  one transport vs both; auth vs non-auth)?
- **Q5** — what is definitely insufficient as closure
  proof?
- **Q6** — does Track K likely require any production
  code at all?

### 1.3 — Hard scope limits

This audit:

- **Does NOT** rewrite Track K Step 1 plan or step-map.
  Their statements stand. Where this audit narrows a
  Step 1 directional default, the narrowing is
  explicitly tagged as a Step 2 finding for Step 3 to
  consume, not a normative re-decision.
- **Does NOT** propose Step 4 implementation.
- **Does NOT** propose any code change.
- **Does NOT** propose any pyproject / scripts /
  SECURITY / release-handoff / apps-platform README /
  CHANGELOG / README / PROJECT-STATUS / manuals edit.
  Those remain Step 5 / Step 6 territory and Track K
  Step 2 commits exactly one new file.
- **Does NOT** invent a new gap. The gap audit-
  described here is the same gap Track K Step 1
  formalized; this document quantifies it from
  observed evidence.
- **Does NOT** claim the platform speaks MCP
  correctly end-to-end, nor that it does not — it
  describes what is currently observable.

---

## 2. Method / evidence sources

### 2.1 — Files inspected

Read top-to-bottom or section-grepped:

- `scripts/dev/selfcheck.py` (full read).
- `scripts/release/verify-release.ps1` (header section
  + check definitions).
- `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  (full re-grounding from Track J Step 2 audit).
- `packages/mcp-common/src/mcp_common/_network_transport.py`
  (full re-grounding from Track J Step 2 audit).
- `apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/__main__.py`
  (entrypoint shape from Track J Step 2).
- `pyproject.toml` (version + `[project.scripts]` +
  `[tool.pytest.ini_options]` + `[tool.hatch.build.targets.wheel]`).
- `examples/*` (glob).
- `tests/*` (glob).
- `**/test_*.py` (glob).
- `**/*smoke*` (glob).

### 2.2 — Repo-shape findings (raw)

- **Zero `tests/` directory.** `pyproject.toml` declares
  `[tool.pytest.ini_options] testpaths = ["tests"]`
  but the directory does not exist. `pytest` would
  collect zero tests today.
- **Zero `test_*.py` files anywhere in the repo.**
- **Zero `*smoke*` Python files.** The four `*smoke*`
  matches are Track E architecture/runbook
  documentation (1С infobase smoke matrix —
  orthogonal to MCP client smoke).
- **`examples/` contains 1С demo dumps and a
  product-config JSON** (`infobase6.config.json`).
  No MCP-client harness, no transport-exercising
  script.
- **`scripts/dev/`** contains: `bootstrap_paths.ps1`,
  `launch.ps1`, `run_dev_check.ps1`, `selfcheck.py`,
  `README.md`. No MCP-client harness.
- **`scripts/release/`** contains: `install.ps1`,
  `install_helper.ps1`, `verify-release.ps1`,
  `README.md`. No MCP-client harness.
- **`docs/operators/`** (Track J / Step 4 deliverable
  location) contains `deployment-boundary.md`. No
  MCP-client demonstration document yet.

### 2.3 — Out-of-bounds for Step 2

- No real MCP client (Claude Desktop / `mcp-cli` /
  equivalent) was downloaded or executed for this
  audit.
- No live `python -m mcp_<server>` process was
  started for this audit.
- No `1cv8.exe` runs (Track K operates on MCP
  client / transport layer, not on 1cv8 binary
  surface).
- No real bearer token / hostname / certificate /
  internal IP referenced anywhere; the audit text
  uses abstract placeholders or omits examples.

---

## 3. Current client-integration baseline

This section describes what externally-meaningful
runtime surfaces currently exist, from the perspective
of a hypothetical real MCP client trying to talk to
the platform.

### 3.1 — The two transport surfaces a client could hit

#### 3.1.1 — `--transport stdio` (Track G / Step 4)

- Server entrypoint: any of
  `python -m mcp_read_server` /
  `python -m mcp_write_server` /
  `python -m mcp_intelligence_server` (or the three
  `[project.scripts]` console entries
  `mcp-read-server` / `mcp-write-server` /
  `mcp-intelligence-server` if installed).
- CLI flags: `--config-path`,
  `--transport stdio` (default), `--log-level`.
  `--bind` and `--auth-token-env` are silently
  ignored on stdio path (Track H Step 3 contract
  §10.3 / §10.4).
- Wire format: line-delimited JSON-RPC 2.0 over
  stdin/stdout. `_serve_stdio` reads `sys.stdin`
  line-by-line, parses each line as a JSON object,
  dispatches via `_handle_request`, writes the
  response (or none for notifications) back as one
  line on `sys.stdout`. EOF / Ctrl-C exits cleanly
  with code 0.
- Auth: none. Threat model = trusted local
  subprocess.
- Diagnostic logs: `sys.stderr` only, structured by
  `_configure_logging`.

#### 3.1.2 — `--transport http` (Track H / Step 4 +
Track I / Step 4 installer round-trip preservation
+ Track J / Step 3 deployment-boundary contract)

- Server entrypoint: same three modules + flags
  `--transport http --bind <HOST>:<PORT>
  --auth-token-env <VARNAME>` (or `auth.tokens` in
  product config).
- Wire format: HTTP/1.1 plain (no in-process TLS).
  Single endpoint `POST /mcp`, `Content-Type:
  application/json`, `Authorization: Bearer
  <token>`, body = one JSON-RPC 2.0 envelope, body
  size ≤ 1 MiB. Other paths → `404 Not Found`.
  Other methods on `/mcp` → `405 Method Not
  Allowed` + `Allow: POST`. Failure-equivalent
  401 + `WWW-Authenticate: Bearer realm="mcp"` for
  any auth failure (missing / empty / malformed /
  wrong-scheme / mismatched token). Multi-
  `Authorization` → 400.
- Threat model = trusted internal network behind
  operator-owned reverse proxy that terminates TLS
  (Track J §4 / §5 / §7).
- Diagnostic logs: `sys.stderr` (`address_string()`
  records the TCP peer's connect address — i.e.
  the reverse proxy when fronted, never the
  original client; Forwarded headers not
  consumed).

### 3.2 — The MCP method set the servers respond to

Both transports dispatch through the same
`_handle_request` switch (`_stdio_transport.py`
lines 112–171). Methods recognised:

- `initialize` — returns `{"protocolVersion":
  "2024-11-05", "capabilities": {"tools":
  {"listChanged": False}}, "serverInfo": {"name":
  <server>, "version": <ver>}}`.
- `notifications/initialized` /
  `initialized` /
  `notifications/cancelled` — no response (returns
  `None`; HTTP path replies 204; stdio path emits
  nothing).
- `ping` — returns `{}`.
- `tools/list` — returns
  `{"tools": [{"name": str, "description": str,
  "inputSchema": {"type": "object"}}, ...]}` —
  one entry per registered tool (15 / 25 / 16
  depending on server). Note: `inputSchema` is the
  trivial `{"type": "object"}`; per-tool argument
  schema is **not** advertised.
- `tools/call` — looks up the tool callable,
  invokes `tool(**arguments)`, serializes the
  result via `_serialize_tool_result`. Errors
  (unknown tool / non-dict args / bad-arg
  TypeError / arbitrary Exception) map to
  `_make_error` envelopes with codes -32601 /
  -32602 / -32603.
- Anything else → `_make_error(req_id, -32601,
  "Method not found: <method>")` for requests;
  notifications silently dropped.

### 3.3 — What an external MCP client encounters

A hypothetical real MCP client connecting to one of
the three servers will:

1. Open the wire — exec the subprocess (stdio) or
   open a TCP connection through the reverse proxy
   (HTTP).
2. Send `initialize` — get the platform's
   `protocolVersion` / `capabilities` /
   `serverInfo`.
3. Optionally send `notifications/initialized` —
   no response.
4. Call `tools/list` — get the per-server tool
   inventory (15 / 25 / 16 names with trivial
   `inputSchema`).
5. Call `tools/call` with `name` + `arguments` —
   get a result envelope shaped by
   `_serialize_tool_result`. For most read tools
   the underlying callable returns a `ToolResult`
   dataclass instance; the serializer wraps it in
   `{"content": [{"type": "text", "text": <msg>}],
   "isError": <bool>, "structuredContent": <payload>}`.

### 3.4 — Honest baseline summary

The runtime is **internally consistent** with a
plausible interpretation of the MCP specification:
it speaks JSON-RPC 2.0 envelope shape, recognises
the standard initialize / tools/list / tools/call
method set, distinguishes notifications from
requests by `id` presence, applies bearer auth on
HTTP, and returns well-shaped error envelopes for
known failure modes. Whether this consistency
actually interoperates with **any** real MCP client
is the question Track K exists to answer.

---

## 4. Existing approximations of "client integration proof"

This section inventories every artefact in the repo
that approximates "client integration proof", and
states what each one actually demonstrates and what
it does not.

### 4.1 — `scripts/dev/selfcheck.py`

**What it does.** Imports the three server packages
and a handful of platform packages. Calls
`read_ping()`, `write_ping()`,
`intelligence_ping()` (in-process Python function
calls — **not** MCP `ping` requests). Calls
`read_list_tools()`, `write_list_tools()`,
`intelligence_list_tools()` (in-process Python
function calls — **not** MCP `tools/list` requests).
Calls `health_summary(...)`,
`check_write_allowed(...)`, etc. Prints
`imports_ok = true`, the three registry tool lists,
and `selfcheck_status = ok`.

**What it actually demonstrates.**

- Every internal package imports cleanly under
  PYTHONPATH bootstrap.
- The three `list_tools()` callables return the
  expected 15 / 25 / 16 tool name lists.
- A handful of platform-layer callables return the
  expected shapes for synthetic inputs.
- The Python interpreter and the source layout are
  consistent.

**What it does NOT demonstrate.**

- Does not start `_serve_stdio` or `_serve_http`.
- Does not speak JSON-RPC 2.0 over **any** wire.
- Does not send `initialize` / `tools/list` /
  `tools/call` as protocol messages — it bypasses
  `_handle_request` entirely.
- Does not exercise the `__main__.py` entrypoints.
- Does not exercise the CLI argument parser
  (`--transport`, `--bind`, `--auth-token-env`,
  `--config-path`).
- Does not exercise bearer auth.
- Does not exercise the HTTP transport at all.
- Does not exercise the stdio transport at all.

**Classification.** Adjacent-but-insufficient. It
proves the source tree is internally consistent;
it does **not** prove the MCP protocol surface.

### 4.2 — `scripts/release/verify-release.ps1`

**What it does.** Eight read-only checks: repo
layout (7 root files), release entrypoints (7
scripts), important docs (11 docs), working tree
clean (or `-AllowDirtyTree`), git baseline
(`branch == main`, history non-empty), selfcheck
(runs `selfcheck.py` and asserts the registry
output), credential leak guard (`git grep` for PEM
private-key headers + AWS secret-access-key
markers), credential template hygiene (scans
`*.config.json` for `/P` / `/Pwd` argv elements
in 1С command templates).

**What it actually demonstrates.** Pre-handoff
release sanity: the repo as-shipped looks ready
to be handed off to another operator; selfcheck
runs cleanly; no obvious credential leaks; layout
matches expectations.

**What it does NOT demonstrate.**

- Does not start the MCP servers.
- Does not speak MCP protocol.
- Does not exercise either transport.
- Does not exercise auth.
- Check 6 (selfcheck) is the **same** approximation
  as §4.1 — it inherits §4.1's limitations.

**Classification.** Adjacent-but-insufficient (for
client-integration purposes; perfectly fit for its
own release-readiness purpose). It proves the
repo is ship-ready; it does not prove the MCP
protocol surface.

### 4.3 — Internal `_handle_request` call paths

**What they are.** During Phase 1–6 + Track G / H /
I / J development, `list_tools()` and
`get_tool(name)` callables were exercised
extensively (every closure runs selfcheck which
exercises them in-process). `_handle_request` is
the unified switch that both `_serve_stdio` and
`_MCPHandler.do_POST` dispatch through; it is also
exercised in-process at every commit (because every
commit's `pyproject.toml` is parsed and every
import path is verified).

**What they actually demonstrate.** The internal
control flow paths from `tools/list` / `tools/call`
to the registered tool callables work. The error
envelope shaping (`_make_error`,
`_serialize_tool_result`) produces well-shaped
JSON.

**What they do NOT demonstrate.**

- Demonstration is in-process only. There is no
  test that constructs a JSON-RPC envelope, hands it
  to `_handle_request`, and asserts the response
  shape — `_handle_request` has been **read**
  carefully (Track H §6 contract; Track J §6 / §7
  audit) but not **invoked from the outside** in a
  test.
- The HTTP envelope path
  (`_MCPHandler.do_POST` body parsing → auth gate →
  `_handle_request` → response serialization → wire
  write) has **not** been exercised end-to-end as
  a test.
- The stdio framing path
  (`_serve_stdio` line read → JSON parse →
  `_handle_request` → JSON dump + flush) has
  **not** been exercised end-to-end as a test.
- `initialize` in particular has never been
  exercised as a real protocol-level negotiation;
  it is a switch-arm in `_handle_request` that is
  read-known to return a particular envelope, but
  never observed to do so in response to a real
  client.

**Classification.** Adjacent-but-insufficient.
The internal switch is correct *as read*, but is
not externally probed.

### 4.4 — Track A / Track E reference-stand runbooks

**What they are.** Two runbook documents in
`docs/runbooks/`: `track-a-reference-stand-round-trip.md`
(Track A real binary-backed write path) and
`track-e-multi-version-smoke-matrix.md` (Track E
operator-driven version-evidence runbook).

**What they actually demonstrate.** That the
platform's 1С binary integration paths work on a
real reference stand for the documented
`8.3.27.1859` evidence row. They exercise
`onec-process-runner` calls, `1cv8.exe` invocation,
audit row shape, and snapshot tree creation.

**What they do NOT demonstrate.**

- These runbooks are **1С-binary** runbooks, not
  **MCP-client** runbooks. They prove the platform
  can drive 1cv8.exe; they do not prove a
  real MCP client can drive the platform.
- They do not start any MCP server, do not speak
  JSON-RPC 2.0, and do not exercise any
  transport.

**Classification.** Already-covered (for their own
1С-binary purpose). Orthogonal to Track K's gap.

### 4.5 — Track J Step 4 operator-facing recipe

**What it is.**
[`docs/operators/deployment-boundary.md`](../operators/deployment-boundary.md)
(Track J / Step 4 deliverable; 691 lines).

**What it actually demonstrates.** It documents
how an operator should bind, front-proxy, and
deploy the HTTP listener. It includes operator
decision-point Q&A and abstract nginx / Caddy
snippets.

**What it does NOT demonstrate.**

- It is descriptive of the deployment boundary;
  it does not include **any** real-client smoke,
  any `initialize` / `tools/list` / `tools/call`
  sample, or any operator-runnable verification
  procedure.
- Track J explicitly deferred runtime client
  evidence to a future track (Track J Step 6
  closure narrative recommended-next-track-
  candidates list, item #1: "Real MCP client
  integration test track" — this is Track K).

**Classification.** Adjacent-but-insufficient.
Sets the deployment shape; says nothing about how
to verify a client speaks to the listener.

### 4.6 — `pyproject.toml` `[tool.pytest.ini_options]`

**What it is.**
```
[tool.pytest.ini_options]
testpaths = ["tests"]
```

**What it actually demonstrates.** A pytest
configuration target.

**What it does NOT demonstrate.** The `tests/`
directory does not exist. `pytest` would collect
zero tests. There is no test suite.

**Classification.** Clearly-missing (the
configuration anticipates a test surface that has
never been created).

### 4.7 — Track G / H / I / J commit messages

**What they are.** Honest closure narratives for
five MCP-transport-tracks (Track G stdio, Track H
HTTP, Track I installer auth round-trip, Track J
deployment-boundary recipe). Several of these
explicitly acknowledge the missing real-client gate
as honest constraint.

**What they actually demonstrate.** Documentation
of the gap.

**What they do NOT demonstrate.** Any actual
client interaction.

**Classification.** Adjacent-but-insufficient.
Records the gap without closing it.

---

## 5. Existing reusable surfaces

These pieces are sound and Step 4 / Step 5 likely
lean on them rather than rewrite them.

### 5.1 — The transport runtimes themselves

`_stdio_transport.py` and `_network_transport.py`
are stdlib-only, well-bounded, well-tested by
inspection (Track G / Track H / Track I / Track J
contracts), and ready to receive a real client.
Track K Step 4 (whichever PATH is chosen) **does
not need** to modify them.

### 5.2 — The three `__main__.py` entrypoints

Already byte-identical across the three servers
(except `SERVER_NAME` / `SERVER_VERSION` /
`list_tools` / `get_tool`). A harness can launch
any of them via `python -m mcp_<server>` (or
`subprocess.Popen([sys.executable, "-m", ...])`)
without modifying anything.

### 5.3 — `scripts/dev/bootstrap_paths.ps1` /
`scripts/dev/launch.ps1`

Already document the dev-mode invocation. A
harness shipped under `scripts/dev/` could
dot-source `bootstrap_paths.ps1` to inherit
PYTHONPATH; alternatively a harness in `examples/`
could declare its own minimal path setup.

### 5.4 — Track J operator-facing recipe

`docs/operators/deployment-boundary.md` already
names the deployment shape that a real-HTTP-client
proof would target. Track K Step 4 (PATH A or
PATH C) can cross-link rather than duplicate.

### 5.5 — `tools/list` / `tools/call` envelope shaping

`_handle_request` already produces the shape
Track K Step 4 needs to assert. A harness asserts
shape; it does not need to alter the shape.

---

## 6. Adjacent-but-insufficient surfaces

These are the same artefacts inventoried in §4 but
restated as the 4-class breakdown the Step 1
step-map called for:

- **`selfcheck.py`** — exercises `list_tools()` /
  `ping()` callables in-process. Bypasses transport
  and protocol envelope. Adjacent-but-insufficient.
- **`verify-release.ps1`** — exercises repo shape +
  selfcheck. Inherits §4.1's adjacency limitation.
  Adjacent-but-insufficient.
- **Internal `_handle_request` call paths** —
  read-known correct; never externally probed.
  Adjacent-but-insufficient.
- **Track J operator-facing recipe** — describes
  deployment shape; says nothing about client
  smoke. Adjacent-but-insufficient.
- **Track G / H / I / J commit narratives** —
  document the gap; do not close it. Adjacent-
  but-insufficient.

---

## 7. Missing proof elements

These are the elements that **do not exist anywhere**
in the repo today:

### 7.1 — A runnable harness that opens the stdio wire

There is no script that launches one of the three
MCP servers via `python -m mcp_<server>` (or
equivalent), connects to its stdin/stdout pipes,
sends a JSON-RPC 2.0 `initialize` line, parses the
response, sends `tools/list`, parses the response,
sends one `tools/call`, parses the response,
shuts down cleanly, and prints a pass/fail
verdict.

### 7.2 — A runnable harness that opens the HTTP wire

There is no script that starts one of the three
MCP servers via `--transport http --bind
127.0.0.1:<port> --auth-token-env <VARNAME>`,
sends `POST /mcp` with `Authorization: Bearer
<token>` and a JSON-RPC 2.0 envelope, parses the
response, exercises `tools/list` + `tools/call`,
and shuts down cleanly. (`urllib.request` from the
stdlib would be sufficient — no third-party
client library required.)

### 7.3 — A documented operator-side procedure for
real-client smoke

There is no operator-facing document that walks an
operator through pointing Claude Desktop or
`mcp-cli` (or equivalent) at one of the servers
and observing successful `tools/list` /
`tools/call`. Track J's recipe documents the
deployment shape but does not include a
"verification" section showing the operator how to
prove the listener speaks MCP.

### 7.4 — A test suite that asserts envelope shape
end-to-end

`pyproject.toml` declares `testpaths = ["tests"]`
but `tests/` does not exist. There is no
externally-probed assertion that `initialize`
returns the documented `protocolVersion` /
`capabilities` / `serverInfo` shape, that
`tools/list` returns 15 / 25 / 16 entries with
the documented `inputSchema`, or that `tools/call`
on an unknown tool returns `_make_error` with
code `-32601`.

### 7.5 — A failing-mode end-to-end probe

There is no externally-probed assertion that an
HTTP client missing the `Authorization` header
gets the documented failure-equivalent 401 +
`WWW-Authenticate` + JSON-RPC `-32001` envelope;
that a non-`/mcp` path returns 404; that a wrong
HTTP method on `/mcp` returns 405 + `Allow: POST`;
that an over-1-MiB body returns 413; that a wrong
Content-Type returns 415; that multi-`Authorization`
returns 400 + `-32600`. These behaviours are
**read-known correct** (Track H §6 / §8 contract;
Track J §7 audit) but not **probed**.

### 7.6 — A protocol-version-negotiation observation

The platform advertises `protocolVersion =
"2024-11-05"` in `_handle_request`'s `initialize`
arm. No client has been observed to either accept
or reject this version. Whether the platform's
chosen version is consumable by a real MCP client
is unverified.

---

## 8. Directional Q1–Q6 resolutions

These are descriptive directional findings for
Step 3 to formalize. They are **not** normative.
They consume Step 1 plan §12 directional defaults
and adjust them where Step 2 evidence warrants.

### 8.1 — Q1 (what should count as "real MCP client")

**Step 1 directional default.** Class B (minimum-
viable real-client-compatible harness shipped as a
single new file).

**Step 2 finding.** Confirmed. The repo evidence
strongly favours Class B because:

- The repo ships **zero** test suite today (§4.6,
  §7.4). A new `tests/` directory introduction
  would itself be a process change beyond Track K
  scope.
- The repo ships **zero** existing harness fragment
  (§2.2 — no `*smoke*` Python files). A harness
  must be built fresh whatever PATH is chosen.
- A Class B harness can be stdlib-only (`socket`,
  `json`, `subprocess` for stdio launch,
  `urllib.request` for HTTP) — no new
  `[project.dependencies]` required. This
  preserves Track C honest constraint of empty
  wheel build.
- Class A (third-party real client) is operator-
  side and not byte-replayable from the repo;
  including it as the closure gate would put the
  closure outside the repo's control.
- Class C (both A and B) is feasible but
  redundant for the closure gate; A can be
  recommended-only.

**Step 2 directional default = Class B as closure
gate; Class A as recommended-only documentation
addendum (Step 5 territory).**

### 8.2 — Q2 (stdio only or HTTP also)

**Step 1 directional default.** Stdio + HTTP
(Option B).

**Step 2 finding.** Slight adjustment toward
allowing PATH downgrade. The evidence:

- Stdio is the **default transport**; not
  exercising it would leave the default surface
  unverified.
- HTTP exercises bearer auth + the `/mcp` POST
  endpoint + failure-equivalence + the trusted-
  network deployment shape — substantially more
  surface per dollar.
- Stdio harness cost (≤ ~150 LOC stdlib-only
  using `subprocess.Popen` + line I/O) and HTTP
  harness cost (≤ ~150 LOC stdlib-only using
  `subprocess.Popen` for server + `urllib.request`
  + `socket` for the client-side) are both
  small individually, and **share most logic**
  (envelope shaping, `tools/list` + `tools/call`
  assertions). One harness binary covering both
  transports is plausible at ≤ ~300 LOC total.
- However: HTTP harness needs operator-supplied
  bearer-token env-var **at run time**. The
  harness file commits no real credentials but
  describes how the operator supplies one.
  This is feasible with abstract placeholders
  (`<TOKEN_ENV_VARNAME>`) and requires no real
  credential commit.

**Step 2 directional default = stdio + HTTP
(Option B confirmed). Step 3 contract may
downgrade to stdio-only (Option A) if the contract
author judges the bearer-token env-var ergonomics
are too operator-heavy for closure-gate framing.**

### 8.3 — Q3 (likely Step 4 path)

**Step 1 directional default.** Open between
PATH A docs-only / PATH B narrow harness / PATH C
hybrid.

**Step 2 finding.** Evidence narrows toward
**PATH B (narrow harness)** with PATH C (hybrid)
as a viable alternative:

- **PATH A docs-only** would document an
  operator-side procedure (Class A) but not
  produce a byte-replayable closure artefact.
  This is what Track J Step 4 effectively shipped
  (`deployment-boundary.md`). For Track K's
  specific gap — *real-client end-to-end
  evidence* — a docs-only PATH leaves the
  closure-gate evidence outside the repo.
  PATH A is feasible but weak.
- **PATH B narrow harness** ships exactly the
  byte-replayable closure artefact Track K's
  goal calls for. Cost: one new file ≤ ~300 LOC
  stdlib-only. Ships under `scripts/dev/` (e.g.
  `scripts/dev/mcp_client_smoke.py`) or
  `examples/mcp-client-smoke/run.py` (Step 3
  picks). Step 1 plan §12 Q5 directional default.
- **PATH C hybrid** ships PATH B harness +
  short PATH A document explaining how an
  operator runs the harness and (recommended-
  only) how an operator points a third-party
  real client at the same servers. Slight extra
  cost (~50–100 lines of operator prose) for
  full coverage of the recommended-only Class A
  path.

**Step 2 directional default = PATH B (closure
gate) with PATH C (hybrid; PATH A as
recommended-only operator doc) as a viable
alternative.** Final lock = Step 3 contract.

The audit explicitly does **not** foreclose
PATH A. If Step 3 contract author judges the
narrowest honest closure is operator-side
demonstration recorded in the closure commit
message, PATH A remains available. This document
records that PATH A would leave evidence outside
the repo, which is a downside but not a fatal
flaw.

### 8.4 — Q4 (minimum meaningful end-to-end scenario)

**Step 1 directional default.** `initialize` +
`tools/list` + at least one read-only `tools/call`
on at least one server on at least one transport.

**Step 2 finding.** Confirmed and refined. The
minimum that actually proves the gap is closed:

- **Mandatory.** `initialize` (proves protocol
  negotiation works); `tools/list` (proves the
  registry is exposed correctly); one
  `tools/call` of a read-only tool from
  `mcp-read-server` (proves dispatch + tool
  execution + result serialization works).
- **Strongly recommended for HTTP harness path.**
  A separate failing-mode probe: missing
  `Authorization` header → 401 +
  `WWW-Authenticate` + JSON-RPC `-32001`. This
  is the most operator-visible auth invariant
  and is cheap to assert.
- **Recommended.** Same scenario on at least one
  more server (`mcp-write-server` or
  `mcp-intelligence-server`). Cost: trivial; the
  harness is per-server-parametric. Confirms the
  pattern is not specific to one server.
- **Recommended.** Same scenario on the second
  transport. Cost: shared most logic.

**Step 2 directional default = mandatory =
initialize + tools/list + one read-only
tools/call on one server on one transport.
Strongly recommended for HTTP = add the 401
failing-mode probe. Recommended = expand to
multiple servers / transports as scope-cheap
extensions.**

### 8.5 — Q5 (definitely insufficient as closure
proof)

**Step 1 directional default.** Implied by §4
classifications.

**Step 2 finding.** Explicit list:

- **`selfcheck.py` alone.** Bypasses transport;
  bypasses envelope; in-process callables only.
- **`verify-release.ps1` alone.** Inherits
  selfcheck's limitations; adds repo-shape
  checks irrelevant to client integration.
- **In-process invocation of `_handle_request`
  with a constructed dict.** Closer than
  selfcheck (exercises the switch) but still
  bypasses the wire and the transport-layer
  framing/auth.
- **Reading the contract documents.** Track H §6
  / §8 / Track J §6 / §7 are normative
  statements **about** what the runtime should
  do; they are not evidence that it **does**.
- **Operator-side demonstration without commit-
  recorded evidence.** Track-J-style "I ran
  Claude Desktop and it worked" with no commit
  artefact leaves the closure outside the repo.
- **Track A / Track E reference-stand runbooks.**
  Orthogonal — they prove 1С-binary integration,
  not MCP-client integration.

**Step 2 directional default = the above six are
each insufficient on their own; closure requires
externally-probed wire-level evidence (PATH B
harness output asserted at commit time, or
PATH C harness + operator-side recommendation).**

### 8.6 — Q6 (does Track K likely require any
production code at all)

**Step 1 directional default.** Likely needs code,
but as a new stand-alone file, not modification
to existing production code.

**Step 2 finding.** Confirmed and sharpened.
Three observations:

- **No modification to `_stdio_transport.py`,
  `_network_transport.py`, or `installer.py` is
  needed.** §3 baseline shows the runtime
  already speaks the methods Track K targets
  (`initialize`, `tools/list`, `tools/call`).
  Track G / H / I / J contracts pinned the
  envelope shapes; Step 4 does not need to
  redesign them.
- **A new harness file (PATH B) is one new
  stdlib-only Python file**, ≤ ~300 LOC soft
  cap, importing only `socket` / `json` /
  `subprocess` / `urllib.request` /
  `urllib.parse` / `argparse` / `os` / `sys` /
  `typing`. Zero new
  `[project.dependencies]`.
- **PATH A docs-only would require zero
  production code** but as §8.3 noted leaves
  evidence outside the repo.

**Step 2 directional default = Track K does NOT
require modification to any existing production
code (`apps/*/src/`, `packages/*/src/`,
`scripts/*` outside the new file). PATH B may
add exactly one new file; PATH A adds zero new
code.**

---

## 9. Step 3 handoff note

Items that Step 3 contract should pin (this is the
audit's directional handoff list, not a normative
contract; Step 3 may refine):

1. **Closure-gate definition** — what counts as
   honest end-to-end MCP-client proof. Step 2
   directional recommendation: a byte-replayable
   harness commit (PATH B) plus optional
   operator-side recommendation (PATH C).
2. **Allowed client class** — Class B (minimum-
   viable harness in repo) as closure gate;
   Class A (third-party real client) as
   recommended-only.
3. **Required round-trip envelope** — at minimum
   `initialize` + `tools/list` + one read-only
   `tools/call` on one server on one transport;
   strongly recommended additional 401 failing-
   mode probe for HTTP path.
4. **Transport coverage** — Step 2 default = both
   stdio and HTTP. Step 3 contract may downgrade
   to stdio-only if HTTP token ergonomics are
   judged too operator-heavy for closure-gate
   framing.
5. **Step 4 PATH selection** — Step 2 narrows
   toward PATH B (or PATH C); does not foreclose
   PATH A. Step 3 contract makes the final
   call.
6. **Step 4 file surface** — if PATH B / PATH C:
   exactly one new harness file. Step 3 chooses
   between `scripts/dev/mcp_client_smoke.py` and
   `examples/mcp-client-smoke/run.py`. Default
   recommendation: `scripts/dev/` because the
   harness is operator-runnable diagnostic
   tooling, not a worked-example artefact.
7. **Step 4 content cap** — ≤ ~300 LOC soft cap;
   stdlib-only; no new `[project.dependencies]`.
8. **Step 4 forbidden surface** — no modification
   to `apps/*/src/`, `packages/*/src/`,
   `pyproject.toml`, existing `scripts/*` files,
   `SECURITY.md`, `docs/release-handoff.md`,
   `apps/platform/README.md`, `CHANGELOG.md`,
   `README.md`, `PROJECT-STATUS.md`,
   `examples/*` (existing), Track K Step 1 / 2
   docs.
9. **Abstract-placeholder discipline** — harness
   examples MUST use abstract placeholders
   (`<TOKEN_ENV_VARNAME>`, `<HOST>`, `<PORT>`,
   `<TOOL_NAME>`); zero real credentials, real
   hostnames, real certificates, real internal
   IPs in any committed text.
10. **No registry change** — registries `read =
    15 / write = 25 / intelligence = 16` MUST
    NOT change. Step 3 contract MUST state this
    explicitly as an invariant.
11. **No `1cv8.exe` runs** — Track K operates on
    MCP client / transport layer.
12. **No remote push** — operator action; not part
    of any Track K step.
13. **Carry-forward of Track G / H / I / J
    invariants** — Step 4 harness, if shipped,
    exercises these surfaces but does not
    redesign them. In-process TLS forbidden;
    mTLS forbidden; Forwarded-header MUST-NOT-
    consume policy preserved.
14. **Q7 SemVer expectation** — default = NO-BUMP.
    PATCH `0.5.1 → 0.5.2` only if Step 4 ships
    a defect-class fix observable by end-users
    (which a stand-alone harness file is not).
    MINOR / MAJOR forbidden by track scope.
    Final call = Step 6 closure.

---

## 10. Honest summary

What Track K / Step 2 has established (descriptive
only):

- The platform's runtime (`_stdio_transport.py` +
  `_network_transport.py` + three `__main__.py`)
  **internally implements** the MCP `initialize`
  + `tools/list` + `tools/call` method set with a
  consistent JSON-RPC 2.0 envelope shape, bearer
  auth on HTTP, and well-documented failure
  modes — but no externally-probed evidence
  exists in the repo that this implementation
  actually interoperates with a real MCP client.
- The repo's existing client-integration
  approximations (`selfcheck.py`,
  `verify-release.ps1`, internal
  `_handle_request` paths, Track J recipe,
  closure narratives) all bypass the wire and
  the protocol envelope — they are adjacent-
  but-insufficient for Track K's specific gap.
- The repo ships zero `tests/` directory, zero
  test_*.py files, zero `*smoke*` Python files,
  zero MCP-client harness fragment.
  `pyproject.toml` declares
  `testpaths = ["tests"]` but the directory is
  unrealised.
- The Step 2 4-class breakdown:
  - **Already-covered** = nothing for Track K's
    specific gap.
  - **Adjacent-but-insufficient** = selfcheck,
    verify-release, internal `_handle_request`
    paths, Track J recipe, closure narratives,
    Track A / E reference-stand runbooks
    (orthogonal).
  - **Clearly-missing** = a runnable harness for
    stdio wire, a runnable harness for HTTP wire,
    a documented operator-side procedure, a
    test suite asserting envelope shape end-to-
    end, a failing-mode end-to-end probe, a
    protocol-version-negotiation observation.
  - **Explicitly-out-of-scope** = packaging
    ecosystem, service supervision, new transport
    family, auth redesign, new MCP tools,
    deployment-boundary redesign, enterprise
    identity, 1cv8 work.
- Audit's directional default for Step 4 = PATH B
  (narrow harness) or PATH C (PATH B + operator
  doc); PATH A docs-only is feasible but leaves
  evidence outside the repo, weakening the
  closure gate.
- Audit's directional default for SemVer = NO-BUMP
  (a stand-alone diagnostic harness is not
  consumer-visible runtime capability).
- No code changed during Step 2. No registry
  drift. No new MCP tools. No SemVer bump. No
  `1cv8.exe` runs. No real credentials. No
  remote push. No premature closure language. No
  false implementation claims. No fake "client
  integration solved" / "production-ready client
  compatibility" framing.

What Track K / Step 2 does **not** do:

- Does not formalize anything as MUST / MUST NOT
  — that is Step 3.
- Does not write the harness file or the
  operator-facing demonstration document — that
  is Step 4 territory if Step 3 selects PATH B /
  PATH C.
- Does not pre-empt Step 4 PATH selection beyond
  documenting that PATH B is the audit's
  directional default. PATH A remains a viable
  Step 3 contract choice.
- Does not edit any operator-facing document
  (SECURITY.md, release-handoff.md,
  apps/platform/README.md, manuals, README.md,
  PROJECT-STATUS.md, CHANGELOG.md). Those
  alignments are Step 5 territory.
- Does not bump `pyproject.toml` `version`. That
  is Step 6 territory.
- Does not push to a remote.

Step 2 is therefore closeable as a single
descriptive audit document, with **Track K /
Step 3 — exact client-integration contract /
closure-gate definition** as the next opening.
