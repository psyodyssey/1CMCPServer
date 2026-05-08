# Track G — runtime / CLI / entrypoint contract

> **Companion files:**
> `track-g-production-grade-mcp-transport-and-cli-plan.md` (Step 1
> plan), `track-g-production-grade-mcp-transport-and-cli-step-map.md`
> (Step 1 step-map),
> `track-g-transport-baseline-audit.md` (Step 2 descriptive
> baseline audit).

> **Status:** Track G / Step 3 deliverable. Documentation-only.
> **Prescriptive normative contract** для Step 4 narrow
> implementation. RFC 2119-style: **MUST** / **MUST NOT** / **SHALL** /
> **SHOULD** / **MAY** имеют точный нормативный смысл. **Этот
> документ не меняет код**; он формулирует правила, которым
> Step 4 implementation обязан следовать.

---

## 1. Purpose / scope

Этот документ — **нормативный contract** для Track G / Step 4
(narrow implementation slice). Он отвечает на **один** вопрос:

> «По каким exact правилам Step 4 имеет право добавить
> production-grade entrypoint / CLI / stdio transport для трёх
> MCP servers, и какие invariants implementation обязан
> соблюдать?»

Документ нормирует:

- exact `__main__.py` shape для трёх MCP server packages;
- exact CLI surface (flags, defaults, exit codes, error
  behaviour);
- exact transport surface (stdio JSON-RPC; out-of-scope items);
- exact server binding / dispatch contract (как `__main__`
  consumes existing `server.py` registry);
- auth / security stance (deliberate no-auth posture для Track
  G);
- supervision / runtime integration stance (через existing
  product runtime layer без extension);
- `[project.scripts]` surface (3 console entries, no new
  dependencies);
- backward compatibility guarantees;
- exact Step 4 implementation surface (allowed files / forbidden
  touches / minor-touch criteria);
- verification contract для Step 4.

Документ **не** делает:

- ship код — это Step 4 territory;
- описывает current state — это Step 2 audit territory
  (`track-g-transport-baseline-audit.md`);
- alignning operator-facing docs — это Step 5 territory;
- making closure narrative claims — это Step 6 territory;
- pretend'ует, что transport уже implemented;
- pretend'ует, что MCP Python SDK интегрирован (он **не**
  интегрирован — verified Step 2 audit §7);
- открывает новый Q-set за пределы Step 1 plan + Step 2 audit
  resolutions.

---

## 2. Relationship to Step 1 plan and Step 2 audit

Track G deliberately splits concerns между тремя layers:

| Step | Role | Language style | Source of truth для |
|---|---|---|---|
| Step 1 plan + step-map | **direction** | descriptive plan + step formats | track scope, 6-step trajectory, 7 open questions Q1–Q7 |
| Step 2 audit (`track-g-transport-baseline-audit.md`) | **descriptive** | observational, current-state | per-surface inventory, 4-class breakdown, Q1/Q2/Q6 resolutions |
| **Step 3 contract (this doc)** | **normative** | RFC 2119-style, prescriptive | exact Step 4 implementation rules, allowed surfaces, verification protocol |
| Step 4 | **execution** | code change | actual `__main__.py` files + `[project.scripts]` block + minimal stdio transport |

**Step 3 contract MUST NOT** revise Step 2 audit findings без
proven blocker. **Step 3 contract MUST NOT** revise Step 1
plan scope без proven blocker. **Step 3 contract MUST NOT**
duplicate descriptive content from Step 2 audit; reader
обращается к Step 2 audit для current-state evidence, к этому
contract — для implementation rules.

---

## 3. Inherited fixed decisions

Following decisions **MUST** be inherited без re-litigation.
Они resolved в Step 2 audit на основе read-only evidence;
Step 3 contract строится на их фундаменте.

### 3.1 — Q1: transport = **stdio only**

Track G ship'ит **stdio JSON-RPC 2.0 transport only.** HTTP /
WebSocket / SSE network transports — **MUST NOT** быть added в
Step 4. Эти transports — отдельные subsequent tracks
post-Track-G.

### 3.2 — Q2: implementation = **custom stdlib only; NO new pyproject dependency**

Step 4 implementation **MUST** be pure stdlib (`sys`, `json`,
`argparse`, `logging`, `signal` или эквивалент). `pyproject.toml`
**MUST NOT** acquire `[project.dependencies]` block через
Track G. Upstream `mcp` Python SDK или any third-party
JSON-RPC library **MUST NOT** be imported by Step 4 code.

Verified Step 2 audit §7: project имеет zero declared
runtime dependencies; zero MCP SDK imports anywhere в repo;
custom-implementation forced choice.

### 3.3 — Q6: `apps/platform` standalone entrypoint = **OUT-OF-SCOPE Track G**

Step 4 **MUST** ship `__main__.py` ровно для **3 MCP server
packages** (`mcp_read_server`, `mcp_write_server`,
`mcp_intelligence_server`). Step 4 **MUST NOT** add
`__main__.py` для `onec_platform` package. Standalone
entrypoint для product layer — отдельный future track,
никак не связан с Track G.

---

## 4. `__main__.py` contract

### 4.1 — Exact files

Step 4 **MUST** create **exactly three** new files, ровно по
этим путям:

1. `apps/mcp-read-server/src/mcp_read_server/__main__.py`
2. `apps/mcp-write-server/src/mcp_write_server/__main__.py`
3. `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`

Step 4 **MUST NOT** create:

- `apps/platform/src/onec_platform/__main__.py` (per §3.3);
- `__main__.py` файлы в любых других packages
  (`packages/*/`, `apps/*/src/*/runtime/`, etc.).

### 4.2 — Required structure

Each `__main__.py` **MUST** define a `main()` function
(callable без аргументов; suitable как target для
`[project.scripts]` console entry point per §10).

Each `__main__.py` **MUST** support invocation through
`python -m <package_name>` (i.e., when Python runs the package
as a script), которое **MUST** call `main()`.

### 4.3 — Required responsibilities of `main()`

`main()` для каждого из трёх servers **MUST** perform
следующие шаги в этом порядке:

1. **Parse CLI arguments** через `argparse` (per §5 CLI
   contract).
2. **Configure logging** через `logging.basicConfig` (logs
   **MUST** be written to `sys.stderr`, не `sys.stdout` —
   per §6.4).
3. **Load product config (optional)** если `--config-path`
   provided — через existing `onec_platform` boundary
   (`bootstrap_product_from_json_file` или эквивалент); если
   `--config-path` not provided — server **MUST** start без
   config-dependent operations (transport не зависит от
   product config; tool dispatch может потребовать context —
   tools handle это сами).
4. **Setup transport** через stdio (per §6 transport
   contract).
5. **Run server loop** — read JSON-RPC requests от stdin,
   dispatch, write JSON-RPC responses к stdout (per §7
   server binding / dispatch contract).
6. **Graceful exit** на EOF stdin / SIGINT / SIGTERM (where
   supported by platform).

Each `main()` **MUST** return `int` exit code (0 = clean
exit; non-zero = error). Each `main()` **MUST NOT** raise
uncaught Python exceptions to operator (catch boundary at top
of `main()`; convert exceptions to `logger.exception(...)` +
non-zero exit).

### 4.4 — Forbidden in `__main__.py`

Each `__main__.py` **MUST NOT**:

- import upstream `mcp` SDK или any third-party JSON-RPC
  library (per §3.2);
- mutate `REGISTERED_TOOLS` registry, `list_tools()`, или
  `get_tool(name)` boundary в `server.py`;
- import packages outside its own server package + `mcp_common`
  + `onec_platform` (last only для optional config loading);
- write to `sys.stdout` для anything other than valid JSON-RPC
  response messages (per §6.4);
- introduce shell invocation, subprocess spawning, network
  socket binding, file watching, или any background daemon
  pattern;
- introduce auth-related code (per §8);
- contain real credentials, API keys, или operator-secret
  defaults.

---

## 5. CLI contract

### 5.1 — Required flags

Each `__main__.py` **MUST** support exactly these CLI flags
(no more, no less в Step 4 baseline):

| Flag | Type | Default | Required | Allowed values |
|---|---|---|---|---|
| `--help` / `-h` | flag | — | optional | (argparse-provided) |
| `--config-path` | string (path) | unset | optional | absolute или relative path к product config JSON |
| `--transport` | string | `stdio` | optional | exactly `stdio` (only valid value в Step 4) |
| `--log-level` | string | `INFO` | optional | exactly one of: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### 5.2 — Default values

- `--transport` default = `stdio`. Если operator не указывает —
  server starts в stdio mode.
- `--log-level` default = `INFO`. Если operator не указывает —
  server logs at INFO level.
- `--config-path` default = unset. Если operator не указывает —
  server starts без product config dependency.

### 5.3 — Validation

- `--transport` **MUST** validate против allowed values
  (`stdio` only в Step 4). Invalid value → fail-closed exit
  с non-zero code + message к stderr; **MUST NOT** start
  server loop.
- `--log-level` **MUST** validate против allowed values.
  Invalid value → fail-closed exit с non-zero code +
  message к stderr.
- `--config-path` если provided **MUST** be loaded через
  `onec_platform.bootstrap_product_from_json_file` (или
  эквивалент); ошибки loading'а → fail-closed exit с non-zero
  code.

### 5.4 — Error behaviour

- Unknown flag → argparse default behaviour (exit 2 + usage
  message к stderr). **MUST NOT** start server loop.
- `--help` / `-h` → argparse usage output к stdout, exit 0.
  Это **deliberate exception** к §6.4 «logs к stderr» — это
  CLI help output, не log message.
- Argument parsing exceptions **MUST NOT** crash с raw Python
  traceback; argparse handles this naturally.

### 5.5 — Forbidden CLI surface в Step 4

Step 4 **MUST NOT** introduce:

- `--port`, `--host`, `--bind`, `--listen` (network surface,
  out-of-scope per §3.1);
- `--auth-token`, `--api-key`, `--cert-file`, `--key-file`
  (auth surface, out-of-scope per §8);
- `--daemon`, `--pidfile`, `--background` (supervision
  surface, out-of-scope per §9);
- `--reload`, `--watch-config` (hot-reload surface,
  out-of-scope);
- любые subcommands beyond exactly one server entry (никаких
  `<server> serve`, `<server> status`, etc.).

---

## 6. Transport contract

### 6.1 — Transport scope

Step 4 **MUST** implement **stdio JSON-RPC 2.0 transport
only.** This means:

- input messages: read from `sys.stdin`;
- output messages: written to `sys.stdout`;
- message framing: line-delimited JSON (one JSON object per
  line; trailing newline after each output message);
- protocol version: JSON-RPC 2.0 (`"jsonrpc": "2.0"` field
  required в каждом message envelope).

### 6.2 — Forbidden transports

Step 4 **MUST NOT** implement или start:

- HTTP server (raw, FastAPI, Flask, aiohttp, etc.);
- WebSocket server;
- SSE (Server-Sent Events) endpoint;
- TCP socket listener;
- Unix domain socket;
- named pipe / Windows IPC;
- any network-bound transport.

### 6.3 — Implementation baseline (per Q2 inheritance)

Step 4 transport implementation **MUST** be pure stdlib:

- `sys.stdin` / `sys.stdout` для I/O;
- `json` module для parse / serialize;
- `argparse` для CLI;
- `logging` для diagnostic output;
- `signal` (where supported) для graceful shutdown.

Step 4 **MUST NOT** import:

- upstream `mcp` PyPI SDK;
- `jsonrpcserver`, `jsonrpc-base`, `jsonrpcclient` или any
  third-party JSON-RPC library;
- `aiohttp`, `httpx`, `requests`, `urllib3` или any
  HTTP/network library;
- `websockets`, `wsproto`, `websocket-client`;
- `fastapi`, `starlette`, `flask`;
- `pydantic` (если уже не используется elsewhere в monorepo);
- any other third-party transport library.

### 6.4 — stdout / stderr discipline

- `sys.stdout` **MUST** be reserved для valid JSON-RPC
  response messages **only.** Никаких log lines, никаких
  print statements, никаких partial JSON, никаких empty
  newlines.
- `sys.stderr` **MUST** be used для all diagnostic output:
  log lines, error messages, debug traces.
- This discipline — necessary because MCP clients (Claude
  Desktop, MCP CLI) parse stdout strictly как JSON-RPC
  message stream; ANY noise on stdout breaks integration.

### 6.5 — Minimum-viable stdio JSON-RPC scope

Step 4 transport **MUST** support these MCP protocol methods
(see §7 dispatch contract для details):

1. **`initialize`** — capability handshake;
2. **`tools/list`** — enumerate tools;
3. **`tools/call`** — invoke tool by name with arguments.

Step 4 transport **MAY** support дополнительные MCP
protocol methods (e.g. `ping`, `notifications/cancelled`)
если minimal effort. **MUST NOT** support:

- `resources/list` / `resources/read` (out-of-scope —
  Track G это transport, не MCP resource framework);
- `prompts/list` / `prompts/get` (out-of-scope аналогично);
- `completion/complete` (out-of-scope);
- streaming responses или server-initiated notifications
  beyond minimal lifecycle (`initialized`, `cancelled`).

### 6.6 — Error handling

- Malformed JSON input → respond с JSON-RPC error envelope
  (`-32700 Parse error` или `-32600 Invalid Request` per
  spec); continue server loop.
- Unknown method → respond с `-32601 Method not found`;
  continue server loop.
- Tool dispatch exception → respond с `-32603 Internal
  error` + message; **MUST NOT** crash server loop.
- EOF on stdin → graceful exit с code 0.
- SIGINT / SIGTERM → graceful exit с code 0.
- Uncaught exception в server loop **MUST NOT** propagate to
  raw Python traceback на operator; top-of-`main()` boundary
  catches и returns non-zero.

---

## 7. Server binding / dispatch contract

### 7.1 — Allowed imports в `__main__.py`

Each `__main__.py` **MAY** import:

- from same-package internal modules (`from .server import
  list_tools, get_tool`);
- from `mcp_common` (`ToolResult`, `ToolCallable`, error
  types);
- from `onec_platform` **ONLY** для optional product config
  loading через documented boundary functions
  (`bootstrap_product_from_json_file` или эквивалент);
- stdlib modules (`sys`, `json`, `argparse`, `logging`,
  `signal`, `pathlib`, `traceback`, etc.).

Each `__main__.py` **MUST NOT** import:

- third-party packages (per §6.3);
- internal modules beyond above list (no
  `mcp_read_server.runtime.dump_adapter`, no
  `mcp_write_server.tools`, etc. — `tools.py` content reached
  через `get_tool(name)(...)` indirection only).

### 7.2 — Tool registry consumption

Step 4 transport **MUST** consume tool registry **only через
existing public boundary**:

- `tools/list` MCP method → call `list_tools()` from
  `<server_package>.server`. Result — `list[str]` of tool
  names.
- `tools/call` MCP method → call `get_tool(name)` from
  `<server_package>.server`. Если result is None →
  `-32601 Method not found` JSON-RPC error. Если result is
  callable → invoke с request arguments; serialize
  `ToolResult` к MCP `tools/call` response shape.

Step 4 transport **MUST NOT**:

- access `REGISTERED_TOOLS` dict directly (use `list_tools()` /
  `get_tool()` indirection);
- mutate `REGISTERED_TOOLS` или its derived dict;
- skip `mcp_common.build_tool_registry` indirection;
- introduce new tool registration paths.

### 7.3 — `server.py` adjustment policy

Step 4 **SHOULD** keep `server.py` для каждого MCP server
package untouched. Existing public boundary (`list_tools()`,
`get_tool(name)`, `REGISTERED_TOOLS`) is sufficient.

Step 4 **MAY** make minor `server.py` adjustments **only if
absolutely necessary** для transport integration. Examples
of acceptable minor adjustments:

- adding a re-export of `list_tools` / `get_tool` from
  package `__init__.py` если import paths Step 4 transport
  cleaner this way (this is `__init__.py`, не `server.py` —
  same minor touch principle applies);
- adding a documented `__all__` declaration in `server.py`
  if Step 4 imports require it;
- adding a comment in `server.py` pointing to new `__main__.py`
  для discoverability.

Step 4 **MUST NOT**:

- modify `REGISTERED_TOOLS` content (no new tools, no
  removals, no reordering);
- modify `list_tools()` или `get_tool()` function signatures
  или behaviour;
- add new public functions к `server.py` beyond above
  documentation/re-export adjustments;
- inline transport logic into `server.py` (transport lives в
  `__main__.py`, не в `server.py`).

### 7.4 — Tool dispatch invariants

Step 4 tool dispatch **MUST** preserve `run_write_flow`
discipline для write tools (Phase 2 invariant; Track A/D/F
preserved). Specifically:

- `tools/call` для write-server tools **MUST NOT** bypass
  `run_write_flow` discipline (preflight + snapshot +
  operation + verify + audit);
- this is enforced naturally because Step 4 calls existing
  `get_tool(name)(...)` which already routes через
  `run_write_flow`. Step 4 **MUST NOT** introduce parallel
  write paths.

---

## 8. Auth / security stance contract

### 8.1 — No auth on transport

Step 4 transport **MUST NOT** implement any of:

- token validation (Bearer, JWT, API key);
- mutual TLS (mTLS);
- OAuth 2.0 / OpenID Connect;
- SAML;
- HTTP Basic / Digest authentication;
- session / cookie management;
- RBAC / ABAC / claims-based authorization;
- multi-tenant isolation;
- rate limiting.

This is **deliberate scope boundary**, not an oversight.

### 8.2 — Security model = trusted local stdio boundary

Track G assumes:

- MCP server runs as a **local subprocess** of MCP-aware
  client (e.g. Claude Desktop launches server via `python -m
  mcp_read_server`);
- stdio communication channel — **trusted** (operator-owned
  process boundary);
- no network exposure;
- threat model = local trusted environment, not adversarial
  network.

Operators who require network-exposed MCP servers **MUST**
wait для subsequent network-MCP-transport track post-Track-G;
Track G **MUST NOT** be claimed as production-ready для
network deployment.

### 8.3 — No credentials в Track G code

Step 4 implementation **MUST NOT**:

- contain real credentials, API keys, or operator-secret
  defaults в any committed file;
- log credentials к stderr или stdout;
- accept credentials через CLI flags (no `--api-key`, no
  `--auth-token`);
- accept credentials через environment variables defined by
  Track G (existing `${ENV:NAME}` substitution pattern из
  Track D applies к product config, не к transport-level
  auth).

---

## 9. Supervision / runtime integration stance contract

### 9.1 — What is reused

После Step 4 ship'ит `__main__.py`, operator **MAY** use
existing `apps/platform/src/onec_platform/runtime.py` boundary
functions (Phase 5 / Step 3 + Phase 6 / Step 6) для process
orchestration:

- `start_product_runtime(...)` / `stop_product_runtime(...)`
  / `get_product_runtime_status(...)` / `reload_product_runtime(...)`
  + their `_from_json_file` variants;
- declared MCP server invocation в `runtime.services`
  config section (operator-supplied argv pointing to
  `python -m mcp_read_server` или console entry binary);
- existing structured logs (`<work_dir>/.runtime/logs/<service>.{out,err}.log`),
  rotate-if-exceeds-size, restart-policy
  `"never" | "restart-if-stale"` (boundary-only).

### 9.2 — What is NOT reused / NOT extended

Step 4 **MUST NOT**:

- modify `apps/platform/src/onec_platform/runtime.py`;
- modify `apps/platform/src/onec_platform/runtime_logs.py`;
- introduce a parallel supervision layer внутри MCP server
  packages;
- add background watchers, daemons, или automatic restart
  loops внутри `__main__.py` (server runs as single-shot
  process; supervisor — operator's responsibility through
  existing runtime layer или OS-level supervision tools).

### 9.3 — What remains outside Track G

Following supervision concerns **MUST** stay outside Track G
scope:

- systemd unit registration;
- Windows Service registration;
- `launchd` plist registration;
- Docker / Kubernetes deployment configuration;
- `supervisor`, `runit`, `s6` integration recipes;
- automatic restart-on-config-change / hot reload;
- log aggregation (`journald`, `syslog`, ELK, etc.);
- distributed tracing / observability stack (OpenTelemetry,
  Jaeger, Prometheus, etc.);
- multi-instance load balancing.

These — отдельные subsequent tracks post-Track-G; Track G
ship'ит entrypoint, не deployment ecosystem.

---

## 10. `[project.scripts]` contract

### 10.1 — Required entries

Step 4 `pyproject.toml` `[project.scripts]` block **MUST**
contain exactly **three** entries, no more, no less:

```toml
[project.scripts]
mcp-read-server = "mcp_read_server.__main__:main"
mcp-write-server = "mcp_write_server.__main__:main"
mcp-intelligence-server = "mcp_intelligence_server.__main__:main"
```

### 10.2 — Forbidden entries

Step 4 `[project.scripts]` block **MUST NOT** contain:

- `mcp-platform`, `onec-platform`, или any entry pointing к
  `onec_platform.__main__:main` (per §3.3 Q6 inheritance);
- subcommand entries (no `mcp-server start`, etc.);
- aliases для existing scripts (no `mcp-read =
  mcp_read_server.__main__:main` short alias).

### 10.3 — `[project.dependencies]` policy

Step 4 `pyproject.toml` **MUST NOT** acquire
`[project.dependencies]` block via Track G. Custom-stdlib
implementation (per §3.2) makes new dependencies unnecessary.

### 10.4 — Wheel-build policy

Step 4 `pyproject.toml` **MUST NOT** modify
`[tool.hatch.build.targets.wheel] packages = []` block.
Track C / Step 3 honest constraint (no wheel build) preserved.
`[project.scripts]` entries only become installable binaries
when project ships как wheel; Track G не ship'ит wheel —
entries — preparatory для future packaging track.

---

## 11. Backward compatibility statement

After Step 4 closure backward compatibility **MUST** be
preserved by всё below:

### 11.1 — Tool registries

`server.py:REGISTERED_TOOLS` для всех 3 MCP servers **MUST**
remain identical to pre-Step-4 content:

- `mcp-read-server` — 15 public tools, identical names;
- `mcp-write-server` — 25 public tools, identical names;
- `mcp-intelligence-server` — 16 public tools, identical
  names.

`list_tools()` / `get_tool(name)` / `ToolCallable` signatures
**MUST** remain identical.

### 11.2 — `mcp_common` API

`mcp_common.__init__.py` exports **MUST** remain identical:
`HealthCheckError`, `PlatformError`, `PolicyDeniedError`,
`ProcessExecutionError`, `ToolCallable`, `build_tool_registry`,
`get_registered_tool`, `list_registered_tools`, `ToolResult`,
`OperationContext`. Step 4 **MUST NOT** add transport
helpers к `mcp_common` (default minimal-touch preference; if
shared transport helper genuinely reduces code duplication,
it's per-server inlined, не shared library extension).

### 11.3 — Existing scripts

`scripts/dev/*` and `scripts/release/*` **MUST** remain
functionally backward-compatible. Step 5 (operator/docs
alignment) **MAY** add new `launch.ps1` subcommand для server
start; Step 4 — implementation only, не scripts touch.

### 11.4 — `pyproject.toml` non-script blocks

Step 4 **MUST NOT** modify:

- `[build-system]` block;
- `[project]` core fields (`name`, `version`, `description`,
  `requires-python`, `readme`, `authors`); version bump
  (Q7) — Step 6 closure territory;
- `[tool.ruff]`, `[tool.pytest.ini_options]`,
  `[tool.hatch.build.targets.wheel]` blocks.

Step 4 **MAY** add new top-level block ровно `[project.scripts]`
per §10.1.

### 11.5 — Audit / details shape

Track G ship'ит transport, не write-flow. `details` dict
shape в audit rows (Track A/D/F invariant) **MUST** remain
unchanged.

### 11.6 — Pre-Track-G code paths

Existing code which imports `from <server_package>.server
import list_tools, get_tool` **MUST** continue работать
identically. New `__main__.py` **MUST** be additive, not
replace these existing import paths.

---

## 12. Exact Step 4 implementation surface

### 12.1 — Allowed files

Step 4 production code touches **MUST** be limited to:

1. **Three new files** (per §4.1):
   - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
   - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
   - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`

2. **One existing file**:
   - `pyproject.toml` — adding `[project.scripts]` block per
     §10.1.

3. **Optional minor adjustments** (per §7.3) **only if
   absolutely necessary** для transport integration:
   - `apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/__init__.py`
     (re-exports / `__all__` if Step 4 imports require);
   - `apps/mcp-{read,write,intelligence}-server/src/mcp_{read,write,intelligence}_server/server.py`
     (documentation comment pointing к `__main__.py`; **NO**
     functional changes).

4. **Optional shared transport helper** (per §11.2 default
   minimal-touch — preferred inlined per-server). **If** Step 4
   determines что shared helper genuinely reduces ≥ 50% code
   duplication across 3 servers без expanding `mcp_common`
   public API surface — Step 4 **MAY** add a new private
   module `mcp_common._stdio_transport` (or similar
   underscore-prefixed name) **deliberately marked private**
   с docstring ясно говорящим «internal helper для Track G
   stdio transport, не public API». Default — НЕ создавать;
   inline в каждый `__main__.py`.

### 12.2 — Forbidden files

Step 4 **MUST NOT** touch:

- `apps/mcp-{read,write,intelligence}-server/src/.../tools.py`
  (write-tool definitions — Track A/F territory);
- `apps/mcp-{read,write,intelligence}-server/src/.../runtime/*`
  (server-internal runtime layers — sealed);
- `apps/mcp-{read,write,intelligence}-server/src/.../models.py`
  (data models — sealed);
- `apps/platform/` весь — product layer (per §3.3 Q6;
  per §9.2 supervision layer не extend'ится);
- `packages/*/src/*` (internal packages — sealed except
  optional `mcp_common._stdio_transport` per §12.1.4);
- `scripts/*` (Step 5 territory; Track G core — implementation,
  не scripts);
- `examples/*`;
- `docs/architecture/track-g-*` (frozen Step 1/2/3 anchors);
- `README.md`, `PROJECT-STATUS.md`, `CHANGELOG.md`,
  `SECURITY.md`, `docs/release-handoff.md`,
  `docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*` (Step 5
  alignment + Step 6 closure territories);
- `apps/platform/README.md` (Step 5 territory);
- `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`.

### 12.3 — Scope creep markers

Following changes constitute Step 4 **scope creep** и **MUST
NOT** appear:

- new MCP tool registration (registries `read=15 / write=25
  / intelligence=16` invariant violation);
- new public functions в `server.py`;
- new public exports в `mcp_common`;
- HTTP / WebSocket / network code (per §6.2);
- auth code (per §8.1);
- SDK dependency addition (per §3.2);
- supervision daemon code (per §9.2);
- 1cv8.exe invocation в `__main__.py` (Track G operates на
  process / transport layer — 1cv8 binary surface не
  задействуется);
- README / status doc updates (Step 5 / Step 6 territory);
- registries content modification;
- audit row `details` shape modification;
- write-flow discipline modification;
- pre-existing tool implementation edits.

---

## 13. Verification contract for Step 4

### 13.1 — Required positive verification

Step 4 commit message **MUST** include sanity-check artifact
demonstrating:

1. `python -m mcp_read_server --help` returns exit code 0
   с non-empty usage output;
2. `python -m mcp_write_server --help` returns exit code 0 с
   non-empty usage output;
3. `python -m mcp_intelligence_server --help` returns exit
   code 0 с non-empty usage output;
4. `verify-release.ps1 -AllowDirtyTree` returns GREEN на 8
   checks (Step 4 не добавляет new release-side checks;
   existing 8 checks 1–8 покрывают presence новых files
   implicitly где applicable);
5. selfcheck registries: `read=15 / write=25 /
   intelligence=16; status=ok`;
6. credential leak guard / credential template hygiene PASS.

### 13.2 — Required negative verification

Step 4 **MUST NOT**:

- run `1cv8.exe` ни одного раза;
- add real credentials anywhere в commit;
- introduce registry drift (any deviation from `15/25/16`
  → Step 4 commit invalid);
- introduce uncaught Python exceptions в `__main__.py`
  paths (test через `--help` invocation per §13.1);
- ship code violating any §3–§12 contract clause.

### 13.3 — Per-server smoke test (optional, recommended)

Step 4 **SHOULD** include в commit message verification что
`--help` output mentions all required CLI flags from §5.1
(visual check; не automated test). Если automated test
infrastructure (pytest или эквивалент) уже exists в repo —
Step 4 **MAY** add narrow smoke test для CLI behaviour
(strict opt-in; default — visual verification only).

### 13.4 — No real MCP client integration testing

Step 4 verification **MUST NOT** require real MCP client
integration test (Claude Desktop, MCP CLI launching server)
as a closure gate. Such testing — Step 5 (operator/docs
alignment) territory; recommended но не blocker. Reasoning:
real client testing requires operator infrastructure (MCP
client installed, configured); это вне Track G developer
loop.

---

## 14. Honest non-goals (повтор для ясности)

Track G после closure **не** делает:

- universal production-grade MCP transport (stdio только);
- network-grade HTTP / WebSocket / SSE transports;
- authentication / authorization / token / mTLS / OAuth /
  SAML / RBAC / multi-tenant;
- supervision daemon / systemd unit / Windows Service
  registration / automatic restart watcher;
- HA / clustering / multi-node / service discovery / load
  balancing;
- distributed tracing / observability stack;
- web UI / dashboard frontend;
- packaging ecosystem beyond `[project.scripts]` console
  entries (`.msi` / `.deb` / signed distribution / PyPI
  publication);
- full enterprise super-set (SSO/RBAC/multi-tenant/secrets
  vault as service / federated audit / policy-as-code DSL);
- 1cv8.exe execution work (Track A territory);
- rollback work (Track F territory);
- AST / metadata / new MCP tools (registries `15/25/16`
  invariant);
- multi-version 1С matrix expansion (Track E territory);
- hot reload;
- multi-instance configuration;
- standalone entrypoint для `apps/platform` / `onec_platform`
  (separate future track);
- real MCP client integration testing as closure gate;
- production deployment readiness для adversarial network
  environment.

Track G ship'ит **first practical baseline** для MCP server
standup в trusted local environment. Большой step forward
от «cannot start at all», но **не** «full production
deployment ready».

---

## 15. Step 4 handoff note

После Step 3 closure (этот contract document shipped), Step 4
имеет:

1. **Exact 3 file paths** для new `__main__.py` (per §4.1).
2. **Exact `main()` shape** + responsibilities + forbidden
   patterns (per §4.2–§4.4).
3. **Exact CLI surface** (per §5).
4. **Exact transport scope** + forbidden libraries + stdout/
   stderr discipline (per §6).
5. **Exact dispatch contract** для tool registry consumption
   (per §7).
6. **Auth + supervision posture** explicitly «no auth, no
   supervisor» (per §8, §9).
7. **Exact `pyproject.toml` `[project.scripts]` block content**
   (per §10).
8. **Backward compatibility guarantees** для existing surfaces
   (per §11).
9. **Exact allowed / forbidden file list** (per §12).
10. **Verification protocol** (per §13).

Step 4 **MUST NOT**:

- expand scope beyond §12.1 allowed files;
- add SDK dependency (per §3.2);
- add `__main__.py` для onec_platform (per §3.3);
- add network transport (per §6.2);
- add auth (per §8.1);
- add supervision daemon (per §9.2);
- modify registries / `mcp_common` public API / audit shape
  (per §11);
- introduce uncaught exceptions or stdout noise (per §4.3,
  §6.4);
- run 1cv8.exe (per §13.2);
- touch operator-facing docs (Step 5 territory).

Step 5 (operator/docs alignment) и Step 6 (closure) — out of
scope этого contract; они оперируют над фактическим
post-Step-4 state.
