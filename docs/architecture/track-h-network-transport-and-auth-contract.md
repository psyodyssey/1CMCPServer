# Parallel Track H — Network Transport and Auth Contract (Step 3)

> **Companion files:**
> `track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`
> (Step 1 plan), `track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`
> (Step 1 step-map), `track-h-transport-and-auth-baseline-audit.md`
> (Step 2 descriptive baseline audit). Этот документ — Step 3
> deliverable: **prescriptive normative contract** для Step 4
> narrow implementation slice.

> **Status:** Track H / Step 3 deliverable. Documentation-only.
> **Prescriptive normative contract** для Step 4 implementation.
> RFC 2119-style: **MUST** / **MUST NOT** / **SHALL** /
> **SHOULD** / **MAY** имеют точный нормативный смысл. **Этот
> документ не меняет код**; он формулирует правила, которым
> Step 4 implementation обязан следовать.

> **Scope discipline.** Этот документ не открывает новые
> вопросы за пределы Step 1 plan §5 / §6 + Step 2 audit
> Q1 / Q2 / Q3 / Q4 directional resolutions. Он не делает
> closure narrative по Track H целиком (это Step 6 territory),
> не выравнивает operator-facing docs (Step 5 territory) и не
> ship'ит код (Step 4 territory).

---

## 1. Purpose / scope

Этот документ — **нормативный contract** для Track H / Step 4
(narrow implementation slice). Он отвечает на **один** вопрос:

> «По каким exact правилам Step 4 имеет право добавить
> network-grade MCP transport family с minimum authentication
> boundary поверх existing Track G stdio baseline, и какие
> invariants implementation обязан соблюдать?»

Документ нормирует:

- exact network transport family + framing + endpoint shape;
- exact MCP method coverage над transport;
- exact JSON-RPC ↔ HTTP boundary (status code mapping, error
  envelope shapes);
- exact concurrency semantics;
- exact authentication contract (token presentation, validation,
  fail-closed semantics, redaction discipline);
- exact `ProductConfig.auth` schema + CLI flag wiring;
- exact `mcp_common` integration boundary (private helper
  shape, public API preservation);
- exact `__main__.py` integration shape;
- backward compatibility guarantees;
- TLS / HTTPS posture;
- `pyproject.toml` posture (no new dependencies);
- exact Step 4 implementation surface (allowed files /
  forbidden files / scope-creep markers);
- verification contract для Step 4.

Документ **не**:

- ship'ит код — это Step 4 territory;
- описывает current state — это Step 2 audit territory
  (`track-h-transport-and-auth-baseline-audit.md`);
- alignning operator-facing docs — это Step 5 territory;
- making closure narrative claims — это Step 6 territory;
- pretend'ует, что transport/auth уже implemented;
- добавляет normative work в out-of-scope items из Step 1
  plan §5 (full enterprise identity stack / zero-trust
  perimeter / web UI / packaging ecosystem / service
  management ecosystem / new MCP tools / 1cv8 / rollback /
  AST / multi-version / standalone `apps/platform` /
  distributed tracing / remote push).

---

## 2. Relationship to Step 1 plan and Step 2 audit

Track H deliberately splits concerns между тремя layers:

| Step | Role | Language style | Source of truth для |
|---|---|---|---|
| Step 1 plan + step-map | **direction** | descriptive plan + step formats | track scope, 6-step trajectory, 7 open questions Q1–Q7 |
| Step 2 audit (`track-h-transport-and-auth-baseline-audit.md`) | **descriptive** | observational, current-state | per-surface inventory, 4-class breakdown, Q1/Q2/Q3/Q4 directional resolutions |
| **Step 3 contract (this doc)** | **normative** | RFC 2119-style, prescriptive | exact Step 4 implementation rules, allowed surfaces, verification protocol |
| Step 4 | **execution** | code change | actual `_network_transport.py` helper + `__main__.py` extensions + `ProductConfig.auth` + minimum bearer auth |

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

### 3.1 — Q1: transport family = HTTP-based

Track H ship'ит **HTTP-based MCP transport** (line-delimited
HTTP POST). WebSocket / raw SSE-only / TCP / Unix domain
socket / named pipe transports — **MUST NOT** быть added
в Step 4. Эти transports — отдельные subsequent tracks
post-Track-H.

### 3.2 — Q2: exactly one transport family

Track H ship'ит ровно **один** новый transport family. Step 4
**MUST NOT** add a second network transport family. Existing
Track G stdio transport остаётся supported byte-identically
(per §12); это **не** второй family добавленный Track H — это
preserved Track G inheritance.

### 3.3 — Q3: auth = static bearer token, constant-time validation

Step 4 **MUST** implement static bearer token authentication
поверх HTTP transport, presented через
`Authorization: <scheme> <token>` header (scheme accepted
case-insensitively per §8), validated constant-time через
`hmac.compare_digest`. JWT / OAuth / OIDC / SAML / mTLS-as-mandatory
/ HTTP Basic / HMAC request signing / API-key-as-query-param —
**MUST NOT** быть implemented. Эти shapes — отдельные
subsequent tracks post-Track-H.

### 3.4 — Q4: auth config home = `ProductConfig.auth` + `${ENV:NAME}` + CLI override

Step 4 **MUST** добавить optional `auth` section к
`ProductConfig` dataclass. Token values **MUST** быть
specified только через `${ENV:NAME}` env-substitution form
(Track D pattern). CLI flag `--auth-token-env <VARNAME>`
**MUST** быть provided как complementary override.
Vault / KMS / OS keychain integrations — **MUST NOT** быть
added; это explicit out-of-scope Track H per Step 1 plan §5.2.

### 3.5 — Carry-over out-of-scope from Step 1 plan §5

Following items **MUST NOT** be touched в Step 4:

- Full enterprise identity stack (SSO / SAML / OIDC / SCIM /
  RBAC platform / multi-tenant policy engine / per-token
  permissioning / per-tool ACL / per-tenant isolation).
- Full zero-trust perimeter (mTLS-everywhere / service mesh /
  KMS / vault as mandatory).
- Web UI / dashboard frontend.
- Packaging ecosystem (`.msi` / `.deb` / signed distribution
  / GUI installer / wizard / PyPI publication / wheel
  publication beyond declared `[project.scripts]`).
- Service management ecosystem (systemd / Windows Service /
  `launchd` / auto-update / Docker / Kubernetes deployment
  manifests / `supervisor` / `runit` / `s6` / orchestration
  templates / HA / clustering / load balancing / hot reload
  / supervisor daemon с restart watcher / background config
  watcher).
- Distributed tracing / observability stack (OpenTelemetry /
  Jaeger / Prometheus / OpenMetrics).
- New MCP tools (registries `read=15 / write=25 /
  intelligence=16` invariant).
- 1cv8.exe execution work.
- Rollback / AST / multi-version 1С matrix expansion.
- Standalone `apps/platform` entrypoint (Track G Q6
  carry-over).
- Real MCP client integration test as closure gate.
- GitHub remote push.

---

## 4. Network transport contract

### 4.1 — Family

Step 4 **MUST** implement HTTP/1.1 server based on Python
stdlib `http.server.BaseHTTPRequestHandler` +
`http.server.ThreadingHTTPServer`. Step 4 **MUST NOT** import
any third-party HTTP framework (`fastapi`, `flask`, `aiohttp`,
`starlette`, `werkzeug`, `bottle`, `tornado`, `uvicorn`,
`gunicorn`, `hypercorn` — exhaustive forbidden list).

### 4.2 — Endpoint path

Step 4 server **MUST** accept requests at exactly one path:
**`/mcp`**. All MCP methods are dispatched by JSON-RPC
`method` field в request body, **MUST NOT** by URL path.
Requests to any other path **MUST** return HTTP 404 with empty
body and `Content-Type: text/plain`.

### 4.3 — HTTP method allowed set

Server **MUST** accept only HTTP `POST` on `/mcp`. Any other
method (`GET` / `PUT` / `DELETE` / `PATCH` / `OPTIONS` /
`HEAD` / etc.) **MUST** return HTTP 405 with header
`Allow: POST` and empty body.

### 4.4 — Request framing

Each HTTP POST body **MUST** contain exactly **one** JSON-RPC
2.0 message (a JSON object). The following framing variants
**MUST NOT** be supported в Step 4:

- JSON-RPC batch arrays (`[{...},{...}]`);
- newline-delimited multiple JSON objects per body;
- chunked / multipart bodies.

Server **MUST** reject batch arrays with HTTP 400 +
`-32600 Invalid Request` envelope (per §6).

### 4.5 — Content-Type

Request `Content-Type` **MUST** be `application/json`. Server
**MAY** accept `application/json; charset=utf-8` and other
RFC-7231-compliant parameters following the media type. Any
other request `Content-Type` **MUST** be rejected with HTTP
415 + `-32600 Invalid Request` envelope (per §6).

Server response `Content-Type` **MUST** be `application/json`
для all JSON-RPC envelope responses (success and error).
Plain-text responses (HTTP 405 / 404 per §4.2 / §4.3) **MUST**
use `Content-Type: text/plain; charset=utf-8`.

### 4.6 — Maximum body size

Server **MUST** enforce a maximum request body size of
**1 MiB (1,048,576 bytes)**. Bodies exceeding this limit
**MUST** be rejected with HTTP 413 + `-32600 Invalid Request`
envelope. Limit **MUST** be a constant; Step 4 **MUST NOT**
make the limit configurable (configurable size limit is
out-of-scope post-Track-H decision).

### 4.7 — Connection lifecycle

Server **MUST** rely on HTTP/1.1 default connection handling
provided by stdlib `http.server`. Server **MUST NOT** make
explicit keep-alive guarantees beyond stdlib defaults.
Client **MAY** assume close-after-response semantics. Step 4
**MUST NOT** implement WebSocket-style long-lived
connections, server-push beyond response body, or HTTP/2.

### 4.8 — Forbidden transports

Step 4 **MUST NOT** implement OR start any of:

- WebSocket server (raw, `websockets`, `wsproto`,
  `aiohttp.ws`);
- Server-Sent Events (SSE) server (raw stdlib SSE,
  `sse-starlette`, etc.) — see §4.9 for SSE-role
  clarification;
- TCP socket listener beyond what `http.server` provides;
- Unix domain socket listener;
- named pipe / Windows IPC listener;
- HTTPS / TLS listener в process (TLS termination is
  operator-side reverse proxy responsibility per §13).

### 4.9 — SSE role

Step 4 baseline **MUST NOT** implement Server-Sent Events.
Each `/mcp` request **MUST** receive a single complete HTTP
response body (request → response, no streaming). The
"optional SSE for streaming responses" wording из Step 2
audit §6 is **explicitly resolved as out-of-scope для Step 4**;
existing tools surface returns complete `ToolResult`
envelopes without partial streaming, so SSE provides no
shipping value at Step 4 maturity. Future SSE addition is a
separate post-Track-H decision.

---

## 5. MCP method coverage

### 5.1 — Required methods

Network transport **MUST** dispatch the following six MCP
methods (exactly the set covered by `_stdio_transport.py`):

1. `initialize` — capability handshake;
2. `ping` — liveness check;
3. `tools/list` — enumerate registered tools;
4. `tools/call` — invoke tool by name with arguments;
5. `notifications/initialized` — client lifecycle notification;
6. `notifications/cancelled` — client cancellation notification.

### 5.2 — Forbidden methods

Step 4 network transport **MUST NOT** implement:

- `resources/list`, `resources/read`;
- `prompts/list`, `prompts/get`;
- `completion/complete`;
- streaming responses or server-initiated notifications
  beyond the minimal lifecycle (`initialized`, `cancelled`).

These are explicit Track H out-of-scope (carry-over from
Track G §6.5 pattern).

### 5.3 — Cross-transport parity

For each method/tool covered, network transport **MUST**
return semantically equivalent JSON-RPC `result` envelope
to existing stdio transport. Specifically:

- `initialize` **MUST** return identical `protocolVersion` /
  `capabilities` / `serverInfo` shape (per `_stdio_transport`'s
  response shape).
- `tools/list` **MUST** return identical tool-name set
  (alphabetically sorted); same `name`, `description`,
  `inputSchema` for each entry.
- `tools/call` **MUST** invoke the same `get_tool(name)(...)`
  callable and **MUST** serialize the returned `ToolResult`
  to identical MCP envelope shape (per `_stdio_transport.
  _serialize_tool_result`).
- `ping` **MUST** return identical `result` envelope (empty
  object).

The only allowed behavioural divergence is transport-level
(HTTP status code, auth check); JSON-RPC application-layer
behaviour **MUST** be identical.

### 5.4 — Notifications dispatch

JSON-RPC requests with no `id` field (notifications) **MUST**
receive HTTP 204 No Content with empty body and
`Content-Type` header omitted. Server **MUST NOT** echo any
JSON-RPC envelope for notifications. Server **MUST NOT**
attempt to send any response after the 204 status line.

---

## 6. JSON-RPC ↔ HTTP boundary

This section pins HTTP status code + envelope shape for each
failure class. Every rule is testable at the wire level.

### 6.1 — Success path (request with `id`)

Successful dispatch **MUST** return:

- HTTP status `200 OK`;
- header `Content-Type: application/json`;
- body = JSON-RPC response envelope:
  `{"jsonrpc":"2.0","id":<request-id>,"result":<result>}`.

This includes `tools/call` invocations where `ToolResult.ok`
is `False`: the JSON-RPC layer is success (HTTP 200), and
the `isError: true` flag lives inside the `result.content`
envelope per `_serialize_tool_result` shape (per §6.7).

### 6.2 — Auth failure → HTTP 401

Missing / empty / malformed / invalid `Authorization` header
(per §8.4) **MUST** return:

- HTTP status `401 Unauthorized`;
- header `WWW-Authenticate: Bearer realm="mcp"`;
- header `Content-Type: application/json`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":null,"error":{"code":-32001,"message":"Unauthorized"}}`.

The error code `-32001` is the implementation-defined
JSON-RPC code reserved by Step 4 for auth failure. Server
**MUST** use exactly this code; **MUST NOT** use `-32600`,
`-32602`, `-32603`, `-32700`, or any of the standard
JSON-RPC reserved codes for auth-related failure.

### 6.3 — Parse error → HTTP 400

Malformed request body (non-JSON, non-object, parse error)
**MUST** return:

- HTTP status `400 Bad Request`;
- header `Content-Type: application/json`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":null,"error":{"code":-32700,"message":"Parse error"}}`.

### 6.4 — Invalid Request → HTTP 400

Body parses to JSON but fails JSON-RPC envelope validation
(missing `jsonrpc` field, missing `method` field, batch
array per §4.4, multiple `Authorization` headers per §8.6,
wrong `Content-Type` per §4.5, oversized body per §4.6)
**MUST** return:

- HTTP status `400 Bad Request` (or `413 Payload Too Large`
  for §4.6 size violation; or `415 Unsupported Media Type`
  for §4.5 content-type violation);
- header `Content-Type: application/json`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":<id-or-null>,"error":{"code":-32600,"message":"Invalid Request"}}`.

`<id-or-null>` **MUST** be the request `id` if recoverable
from the parsed body, else `null`.

### 6.5 — Method not found → HTTP 200

Unknown JSON-RPC method (not in §5.1 set) **MUST** return:

- HTTP status `200 OK`;
- header `Content-Type: application/json`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":<request-id>,"error":{"code":-32601,"message":"Method not found"}}`.

This is canonical JSON-RPC: HTTP success, application-layer
error.

### 6.6 — Invalid params → HTTP 200

`tools/call` with bad arguments shape (params not an object,
missing `name` field, `arguments` not an object, callable
raises `TypeError` on invocation) **MUST** return:

- HTTP status `200 OK`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":<request-id>,"error":{"code":-32602,"message":"Invalid params"}}`.

Error message **MAY** include a sanitized hint (e.g.
`"Invalid params for tool 'ping': unexpected keyword 'foo'"`)
but **MUST NOT** include any token value, env-var value,
file path containing secrets, or raw Python traceback.

### 6.7 — Internal error → HTTP 200

Tool dispatch raises non-`TypeError` exception **MUST**
return:

- HTTP status `200 OK`;
- body = JSON-RPC error envelope:
  `{"jsonrpc":"2.0","id":<request-id>,"error":{"code":-32603,"message":"Internal error"}}`.

Exception type and message **MUST** be logged to stderr via
`logging.exception(...)`. Raw traceback **MUST NOT** appear
in response body. Error message in envelope **MAY** include
the exception class name (e.g.
`"Internal error: ProcessExecutionError"`) but **MUST NOT**
include any token value, env-var value, or file content.

### 6.8 — `ToolResult` with `ok=False`

When `tools/call` invokes a callable that returns
`ToolResult(ok=False, ...)`, the response **MUST** be HTTP 200
with JSON-RPC `result` envelope (not error envelope), where
`result.content` is the same shape as `_stdio_transport.
_serialize_tool_result` produces, including
`"isError": true` and the populated `structuredContent` if
`payload` is non-None. This is **not** an HTTP-layer error
and **not** a JSON-RPC-layer error.

### 6.9 — Notifications path → HTTP 204

Per §5.4, notifications **MUST** return HTTP 204 No Content
with empty body. No JSON-RPC envelope.

### 6.10 — Unknown URL path → HTTP 404 (per §4.2)

Plain text body, no JSON-RPC envelope.

### 6.11 — Unknown HTTP method → HTTP 405 (per §4.3)

Plain text body, no JSON-RPC envelope, `Allow: POST` header
required.

---

## 7. Concurrency semantics

### 7.1 — Server class

Step 4 **MUST** use `http.server.ThreadingHTTPServer` (one
thread per request, stdlib). Step 4 **MUST NOT** use
`http.server.HTTPServer` (single-threaded, blocks under
concurrent requests) or `socketserver.ForkingMixIn`
(process-per-request, expensive on Windows).

### 7.2 — Per-request independence

Each request **MUST** be handled independently. Server
**MUST NOT** maintain per-client session state across
requests beyond what stdlib socket layer provides (i.e.,
zero application-level session). Cookies, server-side
session stores, in-memory request rate counters, per-token
state — all **MUST NOT** be added in Step 4.

### 7.3 — Ordering guarantees

Server **MUST NOT** guarantee any ordering across
concurrent requests. Tool dispatch within a single request
inherits the existing `run_write_flow` discipline for
write-tools (preflight → snapshot → operation → verify →
audit), which is single-threaded inside the dispatch
boundary; concurrent network requests may invoke concurrent
write-tool dispatches. Tool registry contents (`list_tools()`,
`get_tool(name)`) are read-only at runtime per existing
Track G invariant — concurrent reads are safe.

### 7.4 — Thread-safety of underlying layers

Step 4 **MUST NOT** modify `_stdio_transport.py` or
`server.py` files for thread-safety. Existing dispatch
boundary functions are already structured as pure-function
lookups; Step 4 inherits this without modification. If
Step 4 implementation discovers a thread-safety hazard in
existing code, Step 4 **MUST** stop and surface the issue
rather than silently patching code outside §15 allowed
surfaces.

### 7.5 — Resource limits Step 4 MAY defer

Following items are **NOT** required для Step 4 closure:

- maximum concurrent connection cap;
- per-IP rate limiting;
- request timeout enforcement;
- graceful shutdown coordination beyond stdlib defaults.

Step 4 **MAY** rely on operator's reverse proxy for these
concerns. Adding any of them would be Step 4 scope creep.

---

## 8. Auth contract

### 8.1 — Token presentation

Client **MUST** present bearer token in HTTP `Authorization`
request header:

```
Authorization: <scheme> <token>
```

### 8.2 — Scheme name (case-insensitive)

The scheme name **MUST** be matched **case-insensitively**.
Server **MUST** accept:

- `Authorization: Bearer <token>`
- `Authorization: bearer <token>`
- `Authorization: BEARER <token>`
- mixed-case variants (`bEaReR`, etc.)

Server **MUST NOT** require a specific scheme-name
capitalisation. Token value comparison itself remains exact
(per §8.5).

### 8.3 — Single-space separator

Exactly one ASCII space `0x20` **MUST** separate scheme name
and token value. Tab characters, multiple spaces, or other
whitespace **MUST NOT** be tolerated; server **MUST**
reject such headers as malformed (per §8.4).

### 8.4 — Failure-equivalence rule

The following input states **MUST** all map to the same
HTTP 401 response shape (per §6.2):

- no `Authorization` header present;
- `Authorization` header present but value is empty;
- value does not match the regex `^(?i:bearer) (.+)$`
  (any case for scheme name; non-empty token);
- token value matches the regex but does not equal any
  configured valid token (per §8.5);
- multiple `Authorization` headers present (per §8.6 — note:
  §8.6 specifies a different response code; this bullet is
  resolved by §8.6, not §8.4).

The 401 response body **MUST NOT** leak which mode failed.
Server log **MAY** record the mode for operator debugging
but **MUST NOT** include the offending token value (per
§8.7).

### 8.5 — Token validation

Server **MUST** validate the presented token against the
list of configured valid tokens (per §9). Comparison
**MUST**:

- be byte-exact (no case-folding, no whitespace trimming
  beyond what regex `(.+)` captures);
- use `hmac.compare_digest` (constant-time) or equivalent
  Python stdlib primitive that protects against timing
  oracle attacks;
- iterate the valid token list with **per-token**
  `hmac.compare_digest` and short-circuit on first match;
  the iteration timing leak (number of tokens) is acceptable
  per Track H threat model (operator-controlled trusted
  network).

Server **MUST NOT** use `==` operator, substring matching,
or any non-constant-time comparison primitive on the token
value.

### 8.6 — Multiple `Authorization` headers

Multiple `Authorization` headers in a single request
**MUST** result in HTTP 400 + `-32600 Invalid Request`
envelope (per §6.4). Reasoning: stdlib `http.server` exposes
header dict semantics that make duplicate-header handling
ambiguous; explicit reject is safer than silent first-or-last
selection.

### 8.7 — Redaction discipline

Token value **MUST NOT** appear anywhere in:

- stderr logs (server-side);
- structured logs;
- HTTP response body;
- HTTP response headers;
- JSON-RPC error message text;
- audit row `details` field;
- Python traceback emitted by uncaught exceptions.

Server **MUST NOT** log:

- the token value itself;
- the token length;
- the token prefix or suffix;
- a hash of the token;
- a fingerprint of the token.

Server **MAY** log only:

- the fact that auth was attempted (at DEBUG level);
- the fact that auth succeeded or failed (at INFO level);
- the env-var name being read (at DEBUG level), since
  env-var names are not secrets;
- the source of resolution (CLI flag vs config) (at DEBUG
  level).

### 8.8 — Forbidden auth shapes

Step 4 **MUST NOT** implement any of:

- JWT (RS256 / HS256 / etc.);
- OAuth 2.0 / OIDC / OpenID Connect;
- SAML;
- HTTP Basic auth (username + password);
- HMAC request signing;
- mutual TLS (mTLS) — note: optional inbound TLS at all is
  forbidden per §13;
- API key as query parameter or URL fragment;
- session cookies;
- token refresh / rotation endpoints.

These are explicit out-of-scope per §3.5 / Step 1 plan §5.1.
Adding any of them in Step 4 is scope creep.

---

## 9. Config contract

### 9.1 — `ProductConfig.auth` shape

Step 4 **MUST** add to
`apps/platform/src/onec_platform/models.py` a new dataclass:

```python
@dataclass
class ProductAuthSettings:
    tokens: list[str] = field(default_factory=list)
```

`ProductConfig.auth` **MUST** be a new field with
`default_factory=ProductAuthSettings` so configs without an
`auth` section continue to load unchanged. The field type
**MUST** be exactly `ProductAuthSettings`.

### 9.2 — Token entry shape

Each entry in `ProductAuthSettings.tokens` **MUST** be a
string matching the env-substitution regex:

```
^\$\{ENV:[A-Za-z_][A-Za-z0-9_]*\}$
```

This is byte-identical to Track D's `_ENV_TOKEN_REGEX`
(`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`).
Step 4 **MUST** validate this at config-load time inside
`apps/platform/src/onec_platform/loader.py`. Validation
failure **MUST** be a fail-closed startup: the loader
**MUST** raise an explicit error (or return a fail-closed
result, depending on existing loader convention) and
server startup **MUST NOT** proceed.

Literal cleartext tokens (e.g. `"tokens": ["abc123"]`)
**MUST** be rejected. Empty strings **MUST** be rejected.
Strings containing `${ENV:` substring but failing full
regex match **MUST** be rejected (no partial / mixed
forms).

### 9.3 — Env resolution at startup

For each token entry of the form `${ENV:NAME}`, server
**MUST** resolve the env-var `NAME` exactly once at
startup (before binding the listening socket). Resolution
**MUST** be:

- successful only if `os.environ[NAME]` exists and is
  non-empty;
- otherwise fail-closed startup with explicit error message
  to stderr (per §10.6).

Resolved token values **MUST** be held in process memory
only for the lifetime of the server process. Server
**MUST NOT** write resolved token values to any disk
location (no cache file, no log file, no temp file).

### 9.4 — Backward compat

Configs without an `auth` section **MUST** continue to load
unchanged — `ProductConfig.auth` defaults to
`ProductAuthSettings(tokens=[])`. Such configs **MUST**
remain compatible with `--transport stdio` invocation
(stdio path ignores `auth` section entirely per §11.2).

### 9.5 — Required-when-network rule

When operator invokes `--transport http`, server startup
**MUST** require **at least one** valid token source —
either non-empty `auth.tokens` in product config, or
`--auth-token-env <VARNAME>` CLI flag pointing to a
non-empty env-var. Both empty / absent → fail-closed
startup with explicit error message to stderr (per §10.6).

When operator invokes `--transport stdio` (existing
default), `auth` section **MUST** be ignored by the server.
The product config loader **MAY** still validate the
`auth` section structurally (regex check on entries), but
the resolved token list is not consumed by stdio transport.

---

## 10. CLI surface contract

### 10.1 — Existing flags preserved

Step 4 **MUST** preserve byte-identically all existing CLI
flags from Track G (per `_stdio_transport._build_arg_parser`):

| Flag | Type | Default | Allowed values |
|---|---|---|---|
| `--help` / `-h` | flag | — | argparse-provided |
| `--config-path` | string (path) | unset | absolute or relative path |
| `--transport` | string | `stdio` | see §10.2 |
| `--log-level` | string | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

Step 4 **MUST NOT** rename, remove, or change defaults of
these flags.

### 10.2 — `--transport` extension

Step 4 **MUST** extend the `--transport` flag's accepted
values to exactly two:

- `stdio` — existing Track G transport (default; behaviour
  byte-identical to pre-Track-H);
- `http` — new Track H transport (HTTP per §4).

Any other value **MUST** cause argparse-level fail-closed
exit (existing Track G behaviour preserved). Step 4
**MUST NOT** add `--transport` values like `network`,
`http+sse`, `websocket`, `tcp`, etc.

### 10.3 — New `--bind` flag

Step 4 **MUST** add a new flag:

```
--bind <HOST>:<PORT>
```

Rules:

- The flag is **required** when `--transport http`. Server
  startup **MUST** fail-closed if `--transport http` is
  supplied without `--bind`.
- The flag **MUST** be ignored when `--transport stdio`.
- `<HOST>` **MUST** be a literal IPv4 / IPv6 address or
  hostname; argparse-level validation **MAY** be minimal
  (parser accepts string), but server **MUST** fail-closed
  on `socket.gethostbyname` resolution failure at startup.
- `<PORT>` **MUST** be parseable as an integer in range
  1..65535. Out-of-range values **MUST** cause fail-closed
  startup.
- There **MUST NOT** be a default value. Operator MUST
  always specify the bind explicitly when using
  `--transport http`. This rule is deliberate: prevents
  accidental `0.0.0.0:8000` exposure or unhelpful default
  ports.

### 10.4 — New `--auth-token-env` flag

Step 4 **MUST** add a new flag:

```
--auth-token-env <VARNAME>
```

Rules:

- The flag is optional. Step 4 **MUST NOT** make it
  argparse-required.
- The flag is meaningful only with `--transport http`.
  When `--transport stdio`, server **MUST** ignore this
  flag (no warning, no error — silent ignore).
- `<VARNAME>` **MUST** match the regex
  `^[A-Za-z_][A-Za-z0-9_]*$`. Otherwise fail-closed
  startup.
- When supplied, server **MUST** resolve token from
  `os.environ[<VARNAME>]` at startup. Missing or empty
  env-var → fail-closed startup (per §10.6).
- See §10.5 for precedence with `auth.tokens` config.

### 10.5 — Precedence between CLI flag and config

When both `--auth-token-env <VARNAME>` and non-empty
`auth.tokens` are present, the CLI flag **MUST** win
(replace, not merge). Specifically:

- effective valid token list = exactly one entry, the value
  resolved from `os.environ[<VARNAME>]`;
- `auth.tokens` from config **MUST** be ignored entirely.

Reasoning: predictable override semantics; matches typical
CLI-vs-config convention; eliminates implicit merge
ambiguity. Operators who need multi-token deployment use
`auth.tokens` only (no `--auth-token-env`).

### 10.6 — Startup failure modes

Following conditions **MUST** cause non-zero exit (recommend
exit code 2 to match argparse-style usage failures):

- `--transport http` without `--bind`;
- `--bind` value that fails parse (`HOST:PORT` shape) or
  `<PORT>` out of range;
- `--bind` `<HOST>` that fails `socket.gethostbyname`
  resolution;
- `--bind` `<PORT>` already in use (`OSError` from
  `bind()`);
- `--transport http` without any valid token source (per
  §9.5);
- `--auth-token-env` with `<VARNAME>` that does not match
  the regex;
- `--auth-token-env` with `<VARNAME>` whose env-var is
  missing or empty;
- `auth.tokens` entry that fails env-substitution regex
  validation;
- `auth.tokens` entry whose env-var is missing or empty
  at resolution time;
- malformed product config JSON (existing fail-closed
  behaviour preserved).

Each failure **MUST** produce a single stderr line of the
form:

```
<prog>: <error message>
```

where `<prog>` is the argparse `prog=` value (e.g.
`python -m mcp_read_server`) and `<error message>` is a
brief human-readable description that **MUST NOT** include
any token value, env-var value, or stack trace.

Step 4 **MUST NOT** emit a Python traceback to stderr for
any of the §10.6 failure modes. The `run_main` /
`run_main_http` exception boundary (per §11.3) catches
these.

### 10.7 — Forbidden CLI surface

Step 4 **MUST NOT** introduce any of:

- `--cert-file`, `--key-file`, `--ca-cert` (TLS surface,
  out-of-scope per §13);
- `--port`, `--host` (replaced by `--bind`);
- `--auth-token-file` (file-based secret reading; redirected
  through `${ENV:NAME}` per §3.4);
- `--auth-tokens-env-list <VARNAME>` (multi-env-var split;
  use `auth.tokens` config for multi-token deployments);
- `--api-key`, `--auth-token` (literal token on CLI; never
  acceptable per §8.7 redaction rule);
- subcommands of any kind (no `serve`, `start`, `status`,
  etc.; existing flat `python -m <pkg>` surface preserved);
- `--reload`, `--watch-config` (hot-reload surface, §3.5
  out-of-scope);
- `--daemon`, `--pidfile`, `--background` (supervision
  surface, §3.5 out-of-scope);
- `--max-connections`, `--rate-limit` (per §7.5 deferred);
- `--cors-origin`, `--cors-headers` (CORS surface; explicit
  out-of-scope post-Track-H).

---

## 11. Integration boundary (mcp_common / `__main__.py` / `apps/platform`)

### 11.1 — New private helper module

Step 4 **MUST** create exactly one new file:

```
packages/mcp-common/src/mcp_common/_network_transport.py
```

Constraints:

- Underscore-prefixed name; **MUST NOT** be added to
  `mcp_common/__init__.py`'s `__all__`;
- **MUST NOT** be imported from `mcp_common/__init__.py`
  (no `from ._network_transport import ...` line in
  `__init__.py`);
- Module docstring **MUST** explicitly state "Not part of
  the public ``mcp_common`` API" по pattern Track G
  `_stdio_transport.py`;
- Pure stdlib only (`http.server`, `socketserver`, `hmac`,
  `os`, `re`, `json`, `argparse`, `logging`, `sys`,
  `signal`, `pathlib`, `urllib.parse`, `email.message`,
  `typing.Callable`); third-party imports **MUST NOT**
  appear.

### 11.2 — Public-to-package function: `run_main_http`

The new helper module **MUST** expose exactly one
public-to-package function:

```python
def run_main_http(
    *,
    prog: str,
    description: str,
    server_name: str,
    server_version: str,
    list_tools_fn: Callable[[], list[str]],
    get_tool_fn: Callable[[str], object],
    argv: list[str] | None = None,
) -> int:
    ...
```

Signature **MUST** be parallel to existing
`_stdio_transport.run_main(...)` so that three `__main__.py`
files can dispatch to either based on `--transport` value.

`run_main_http(...)` is responsible for:

1. parsing CLI arguments (extending the existing arg
   parser per §10);
2. configuring stderr-only logging (per §8.7 redaction
   rule);
3. validating `--bind`, resolving auth token source
   (per §10.5);
4. constructing the `ThreadingHTTPServer` instance bound
   to `<HOST>:<PORT>`;
5. running the server loop with graceful shutdown on
   SIGINT / SIGTERM (where supported);
6. returning process exit code (0 = clean exit; non-zero =
   error).

### 11.3 — Existing `_stdio_transport.run_main` preservation

Step 4 **MUST NOT** modify
`packages/mcp-common/src/mcp_common/_stdio_transport.py`.
Existing function `run_main(...)` keeps its current
signature byte-identical. Existing constants
(`PROTOCOL_VERSION`, `ALLOWED_TRANSPORTS`,
`ALLOWED_LOG_LEVELS`) **MAY** be referenced from
`_network_transport.py` (read-only import); they **MUST NOT**
be modified.

If `_network_transport.py` needs a shared dispatch core
(per Track G PATH B precedent), Step 4 **MAY** extract
small private helpers from `_stdio_transport.py` into a
**new** private module
`packages/mcp-common/src/mcp_common/_jsonrpc_dispatch.py`
(or similar underscore-prefixed name) and update both
existing `_stdio_transport.py` and new `_network_transport.py`
to import from it. If Step 4 takes this path:

- the extraction **MUST** be a refactor with
  byte-identical observable behaviour for stdio path;
- the new shared module **MUST** be underscore-prefixed
  and **MUST NOT** be added to `mcp_common/__init__.py`'s
  `__all__`;
- Step 4 commit message **MUST** explicitly call out the
  refactor and provide evidence that stdio behaviour is
  byte-identical (e.g. unchanged `--help` output, unchanged
  smoke `tools/list` output).

If Step 4 instead inlines dispatch in
`_network_transport.py` (PATH A), the file **MAY**
duplicate small portions of `_stdio_transport.py` without
extracting a shared module. Step 4 implementation **MUST**
choose one of the two paths and document the choice in
commit message.

### 11.4 — Three `__main__.py` extensions

Step 4 **MUST** modify all three files:

- `apps/mcp-read-server/src/mcp_read_server/__main__.py`;
- `apps/mcp-write-server/src/mcp_write_server/__main__.py`;
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`.

Modification shape:

- The existing `def main() -> int:` signature **MUST** be
  preserved.
- The existing `if __name__ == "__main__": raise
  SystemExit(main())` block **MUST** be preserved.
- Inside `main()`, Step 4 **MUST** add minimal logic that
  inspects `argv` (via a pre-parse or by examining
  `sys.argv`) to determine which `run_main` /
  `run_main_http` to call. The pre-parse **MUST NOT**
  duplicate full argparse logic; minimal inspection
  (e.g., `"http" in argv and `--transport http`-detection
  helper exposed by the new module) is acceptable.
- Existing per-server `SERVER_NAME` / `SERVER_VERSION`
  constants **MUST** be passed unchanged to whichever
  `run_main` is selected.
- No new top-level imports **MUST** appear except the new
  `run_main_http` import from `mcp_common._network_transport`.

### 11.5 — `apps/platform` changes

Step 4 **MUST** modify exactly two files in `apps/platform/`:

1. `apps/platform/src/onec_platform/models.py` —
   add `ProductAuthSettings` dataclass per §9.1; add
   `auth` field to `ProductConfig` per §9.1.
2. `apps/platform/src/onec_platform/loader.py` — add
   validation logic for the new `auth` section per §9.2
   / §9.3.

Step 4 **MUST NOT** modify any other file under
`apps/platform/src/onec_platform/`. Specifically forbidden:

- `bootstrap.py`;
- `dashboard.py`;
- `doctor.py`;
- `enterprise.py`;
- `installer.py`;
- `process_control.py`;
- `realstand.py`;
- `recovery.py`;
- `runtime.py`;
- `runtime_logs.py`;
- `state.py`;
- `templates.py`;
- `workflow.py`;
- `__init__.py` (no new exports — `ProductAuthSettings`
  **MAY** be re-exported from `__init__.py` only if
  loader logic outside `apps/platform` requires it; default
  is not to re-export).

### 11.6 — Three `server.py` files preservation

Step 4 **MUST NOT** modify any of:

- `apps/mcp-read-server/src/mcp_read_server/server.py`;
- `apps/mcp-write-server/src/mcp_write_server/server.py`;
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`.

`REGISTERED_TOOLS` content, `list_tools()` /
`get_tool(name)` signatures and bodies **MUST** remain
byte-identical.

### 11.7 — `tools.py` / `models.py` / `runtime/*` preservation

Step 4 **MUST NOT** modify any of:

- `apps/*/src/*/tools.py` (write-tool / read-tool /
  intelligence-tool definitions);
- `apps/*/src/*/models.py` for any of the three MCP server
  packages (i.e., the per-server `models.py`, distinct from
  `apps/platform/src/onec_platform/models.py` which §11.5
  addresses);
- `apps/*/src/*/runtime/*` packages (write-server runtime
  layers including `binary_dispatch.py`, `flow.py`,
  `metadata_ops.py`, etc.; read-server runtime including
  `live_adapter.py`; intelligence-server runtime).

---

## 12. Backward compatibility

Following invariants **MUST** be preserved byte-identically
through Step 4:

### 12.1 — Tool registries

`server.py:REGISTERED_TOOLS` для всех 3 MCP servers:

- `mcp-read-server` — exactly 15 public tools, identical
  names;
- `mcp-write-server` — exactly 25 public tools, identical
  names;
- `mcp-intelligence-server` — exactly 16 public tools,
  identical names.

`list_tools()` / `get_tool(name)` / `ToolCallable`
signatures **MUST** remain byte-identical.

### 12.2 — `mcp_common` public API

`mcp_common/__init__.py` `__all__` **MUST** remain
byte-identical:

```
OperationContext, PlatformError, PolicyDeniedError,
ProcessExecutionError, HealthCheckError, ToolResult,
ToolCallable, build_tool_registry, list_registered_tools,
get_registered_tool
```

No additions, no removals, no renames. New helpers
(`_network_transport`, optional `_jsonrpc_dispatch`)
**MUST** be underscore-prefixed and **MUST NOT** appear
в `__init__.py`.

### 12.3 — Existing CLI flag set

The four existing flags (`--help`, `--config-path`,
`--transport`, `--log-level`) **MUST** remain functional with
identical semantics for `--transport stdio`. Specifically:

- `python -m <server> --help` **MUST** continue to exit 0
  with non-empty usage output;
- `python -m <server> --transport stdio` **MUST** continue
  to start the existing stdio JSON-RPC loop with
  byte-identical observable behaviour;
- `python -m <server> --config-path <path>` **MUST**
  continue to load product config через existing
  `bootstrap_product_from_json_file` boundary;
- `python -m <server> --log-level <level>` **MUST**
  continue to configure stderr logging with identical
  level mapping.

### 12.4 — `[project.scripts]` console entries

`pyproject.toml` `[project.scripts]` block **MUST** remain
unchanged (three entries: `mcp-read-server`,
`mcp-write-server`, `mcp-intelligence-server`). Step 4
**MUST NOT** add new console entries; **MUST NOT** rename
existing ones; **MUST NOT** redirect existing entries to
network-only mode.

### 12.5 — Audit `details` shape

Audit row `details` dict shape (Track A / D / F invariant)
**MUST** remain unchanged. Track H ships transport, не
write-flow. `run_write_flow` discipline preserved.

### 12.6 — `apps/platform` remaining files

All `apps/platform/src/onec_platform/` files except those
explicitly allowed in §11.5 **MUST** remain byte-identical.

### 12.7 — Read-only-by-construction invariant

`mcp-intelligence-server` package **MUST** remain read-only.
No import of `onec_policy_engine`. No call to
`run_write_flow`. Step 4 transport additions
**MUST NOT** introduce write paths to the intelligence
server.

### 12.8 — Pre-Track-H product configs

Existing product configs (without `auth` section) **MUST**
continue to load and run with `--transport stdio` exactly
as before Step 4 (per §9.4).

---

## 13. TLS / HTTPS posture

### 13.1 — In-process TLS = forbidden

Step 4 **MUST NOT** terminate TLS in-process. The HTTP
listener **MUST** bind plain HTTP/1.1 (no TLS,
no `ssl.wrap_socket`, no `ssl.SSLContext`, no certificate
loading code, no `ssl` module imports beyond what stdlib
indirectly pulls).

### 13.2 — Operator deployment model

The supported deployment model is:

```
[remote MCP client] ─TLS─→ [reverse proxy: nginx / Caddy /
                            Apache / cloud LB]
                          ─plain HTTP→ [Track H listener
                                        bound to 127.0.0.1]
```

Operator **SHOULD** bind the listener to a loopback or
private interface (`127.0.0.1`, `::1`, or private IP) and
expose it through the operator's reverse proxy. Operator
**MAY** bind to a public interface only with explicit
understanding that no in-process TLS is provided; this
is operator's risk acceptance.

Step 4 documentation (Step 5 territory) will spell out
this posture; Step 4 implementation only honours the
contract above.

### 13.3 — mTLS = explicit out-of-scope

Mutual TLS / client certificate authentication **MUST NOT**
be implemented in Step 4. This is carry-over from §3.5
(plan §5.2). Operators requiring mTLS terminate it at the
reverse proxy layer; the result is plain bearer-token auth
on the inner HTTP/1.1 hop.

---

## 14. `pyproject.toml` posture

### 14.1 — No new mandatory dependencies

Step 4 **MUST NOT** add `[project.dependencies]` block.
The full network transport implementation **MUST** be
pure-stdlib using only:

- `http.server` (`BaseHTTPRequestHandler`,
  `ThreadingHTTPServer`);
- `socketserver` (for `ThreadingMixIn` if needed);
- `hmac` (for `compare_digest`);
- `os` (for `os.environ`);
- `re` (for env-substitution regex);
- `json`;
- `argparse`;
- `logging`;
- `sys`;
- `signal` (where supported by platform);
- `pathlib`;
- `urllib.parse` (for header parsing if needed);
- `email.message` (for header parsing if needed);
- `typing` (`Callable`, etc.).

### 14.2 — No new optional dependencies

Step 4 **MUST NOT** add `[project.optional-dependencies]`
block. Step 4 **MUST NOT** add an `extras` group named
`network` / `http` / `auth` / similar. Reasoning: stdlib
HTTP path is sufficient for Step 4 closure; adding
optional deps invites scope creep without delivering
Track H goals; preserves Track G Q2 inheritance ("custom
stdlib only; NO new pyproject dependency").

### 14.3 — `[project.scripts]` preservation

`[project.scripts]` block **MUST** remain unchanged (per
§12.4): three entries pointing at existing
`<package>.__main__:main`. Step 4 **MUST NOT** add new
console entries.

### 14.4 — Wheel-build empty preserved

`[tool.hatch.build.targets.wheel] packages = []` **MUST**
remain byte-identical (Track C / Step 3 honest constraint
carry-through).

### 14.5 — Version field

Step 4 **MUST NOT** modify `version` field в
`pyproject.toml`. Version bump (per Track H plan §10
Q7) is Step 6 closure deliverable, not Step 4.

### 14.6 — Other pyproject sections

Step 4 **MUST NOT** modify `[build-system]`,
`[tool.ruff]`, `[tool.pytest.ini_options]`, or any other
existing `pyproject.toml` section.

---

## 15. Exact Step 4 implementation surface

### 15.1 — Allowed files (exhaustive list)

Step 4 production-code touches **MUST** be limited to:

1. **One new file:**
   - `packages/mcp-common/src/mcp_common/_network_transport.py`
     (per §11.1 / §11.2).

2. **Optional one new file (PATH B refactor only):**
   - `packages/mcp-common/src/mcp_common/_jsonrpc_dispatch.py`
     (per §11.3 — only if Step 4 chooses extraction path).

3. **Three modified files:**
   - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
     (per §11.4);
   - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
     (per §11.4);
   - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
     (per §11.4).

4. **Two modified files in `apps/platform`:**
   - `apps/platform/src/onec_platform/models.py` (per
     §11.5 — add `ProductAuthSettings` dataclass + `auth`
     field on `ProductConfig`);
   - `apps/platform/src/onec_platform/loader.py` (per
     §11.5 — add validation for `auth` section).

5. **Optional one modified file (PATH B refactor only):**
   - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
     (per §11.3 — only if Step 4 extracts shared dispatch
     core; the modification **MUST** be a behaviour-
     preserving refactor with explicit byte-identical
     stdio smoke proof in commit message).

Total: **5 to 7 files** depending on PATH A vs PATH B
choice.

### 15.2 — Forbidden files (non-exhaustive critical list)

Step 4 **MUST NOT** touch:

- `pyproject.toml` (per §14);
- registry contents in any `server.py` (per §11.6 / §12.1);
- any `tools.py` / `models.py` (server-package) /
  `runtime/*` (per §11.7);
- `apps/platform/src/onec_platform/` files other than
  `models.py` and `loader.py` (per §11.5);
- `mcp_common/__init__.py`'s `__all__` or any of its
  imports (per §12.2);
- existing `_stdio_transport.py` **except** for §11.3 PATH B
  refactor case;
- `scripts/*` (release scripts territory, Track B / C);
- `examples/*`;
- documentation за пределами Track H docs themselves
  (Step 5 / Step 6 territory):
  - `README.md`,
  - `PROJECT-STATUS.md`,
  - `CHANGELOG.md`,
  - `SECURITY.md`,
  - `docs/release-handoff.md`,
  - `docs/operator-manual.md`,
  - `docs/administrator-manual.md`,
  - `docs/developer-manual.md`,
  - `docs/runbooks/*`,
  - `apps/platform/README.md`,
  - `apps/*/README.md`;
- Track H planning / audit / contract docs (frozen Step
  1 / 2 / 3 anchors):
  - `docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`,
  - `docs/architecture/track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`,
  - `docs/architecture/track-h-transport-and-auth-baseline-audit.md`,
  - this document
    (`docs/architecture/track-h-network-transport-and-auth-contract.md`);
- Track A / B / C / D / E / F / G architecture docs;
- `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`.

### 15.3 — Scope creep markers

Following changes **MUST NOT** appear in Step 4 commit
diff. Each, if present, **MUST** cause Step 4 review to
stop and surface the violation:

- new MCP tool registration (registry counts must remain
  `15 / 25 / 16`);
- new public exports in `mcp_common/__init__.py`;
- new `[project.dependencies]` or
  `[project.optional-dependencies]` block;
- TLS / `ssl` module imports (per §13.1);
- WebSocket / SSE / TCP listener (per §4.8);
- supervisor / systemd / Windows Service / hot reload
  / restart watcher / background daemon code (per §3.5);
- web UI / HTML / Jinja / static asset directory (per
  §3.5);
- third-party HTTP framework imports (per §4.1);
- third-party JSON-RPC library imports (Track G inheritance);
- third-party MCP SDK imports (Track G inheritance);
- per-token permissioning / per-tool ACL / per-tenant
  isolation logic (per §3.5 / §8.8);
- token rotation endpoint / refresh endpoint (per §8.8);
- session cookies (per §7.2 / §8.8);
- rate-limiting / throttling code (per §7.5);
- CORS handler / preflight logic (per §10.7);
- 1cv8.exe invocation (per §3.5);
- standalone `apps/platform` entrypoint (per §3.5);
- README / PROJECT-STATUS / CHANGELOG / SECURITY /
  release-handoff / apps/platform/README updates (Step
  5 / Step 6 territory);
- registries content modification;
- audit row `details` shape modification;
- write-flow discipline modification;
- pre-existing tool implementation edits;
- introduction of new `__main__.py` for `onec_platform`
  package (Track G Q6 carry-over);
- `pyproject.toml` modifications of any kind (per §14).

---

## 16. Verification contract for Step 4

### 16.1 — Required positive verification

Step 4 commit message **MUST** include sanity-check artifacts
demonstrating, for each of the three MCP server packages
(`mcp_read_server`, `mcp_write_server`,
`mcp_intelligence_server`):

1. **Stdio path preserved.**
   - `python -m <server> --transport stdio --help` returns
     exit 0 + non-empty usage output that includes the
     four existing flags;
   - `python -m <server> --help` (default transport)
     returns exit 0 + non-empty usage and lists `http`
     as an additional valid `--transport` value.

2. **HTTP path help.**
   - `python -m <server> --transport http --help` returns
     exit 0 + non-empty usage output that includes
     `--bind` and `--auth-token-env` flags.

3. **HTTP path startup negative checks.**
   - `python -m <server> --transport http` (without
     `--bind`) returns non-zero exit + single stderr line
     identifying the missing `--bind` requirement (no
     traceback);
   - `python -m <server> --transport http --bind 127.0.0.1:0`
     (without auth source) returns non-zero exit + single
     stderr line identifying the missing token source (no
     traceback).

4. **HTTP path startup positive smoke.** Step 4 commit
   message **MUST** include one demonstration of:
   - server started with `--transport http --bind
     127.0.0.1:<port> --auth-token-env <NAME>`;
   - environment variable `<NAME>` set to a non-empty
     test value;
   - one POST `/mcp` `tools/list` request with
     `Authorization: Bearer <test-value>` header
     returning HTTP 200 + JSON-RPC envelope listing all
     15 / 25 / 16 tool names (sorted, matching stdio
     output);
   - one POST `/mcp` `tools/list` request without
     `Authorization` header returning HTTP 401 +
     `{"jsonrpc":"2.0","id":null,"error":{"code":-32001,
     "message":"Unauthorized"}}` envelope (per §6.2);
   - one POST `/mcp` `tools/list` request with
     `Authorization: Bearer wrong-value` header returning
     **byte-identical** 401 response to the no-header
     request (status code, headers, body — proves §8.4
     failure-equivalence);
   - one POST `/mcp` `tools/call` request invoking `ping`
     tool with valid auth, returning HTTP 200 + JSON-RPC
     envelope with `result.content` matching stdio
     `tools/call ping` output;
   - one GET `/mcp` request returning HTTP 405 with
     `Allow: POST` header (per §4.3);
   - one POST to a non-`/mcp` path returning HTTP 404
     (per §4.2);
   - one POST `/mcp` with malformed JSON body returning
     HTTP 400 + `-32700 Parse error` envelope (per §6.3);
   - one POST `/mcp` with `Content-Type: text/plain`
     returning HTTP 415 + `-32600 Invalid Request`
     envelope (per §6.4 / §4.5).

5. **Cross-transport parity.** The set of tool names
   returned by `tools/list` over HTTP **MUST** equal the
   set returned by `tools/list` over stdio (sorted,
   element-wise byte-identical) for each server. Step 4
   commit **MUST** explicitly demonstrate this for at
   least one server package; **MAY** assert by reasoning
   for the other two if implementation path is shared.

6. **Existing release verification preserved.**
   - `scripts/release/verify-release.ps1 -AllowDirtyTree`
     returns GREEN on all 8 checks (existing checks
     unchanged; no new checks added in Step 4);
   - selfcheck registries: `read=15 / write=25 /
     intelligence=16; status=ok`;
   - `imports_ok=true`.

7. **Credential leak guard / hygiene preserved.**
   - `verify-release.ps1` Check 7 (PEM / AWS markers) and
     Check 8 (credential template hygiene `/P` / `/Pwd`
     argv positions) remain GREEN;
   - no real bearer token value in commit / diff (all
     references go through `${ENV:NAME}` substitution
     pattern).

### 16.2 — Required negative verification

Step 4 commit **MUST NOT**:

- run `1cv8.exe` ни одного раза;
- add real credentials anywhere в commit или working tree
  (включая any product config, any test artifact, any
  log line in commit message);
- introduce registry drift (any deviation from `15 / 25
  / 16` → Step 4 commit invalid);
- introduce uncaught Python exceptions to operator on
  `--help` paths or normal startup-failure paths (test
  via §10.6 modes);
- ship code violating any §3–§14 contract clause;
- modify any file outside §15.1 allowed list;
- introduce any of §15.3 scope creep markers.

### 16.3 — What does NOT count as sufficient verification

The following **MUST NOT** be accepted as sufficient
Step 4 verification:

- only `--help` exits without HTTP path smoke (§16.1.4
  required);
- HTTP smoke without auth fail-closed proof (§16.1.4
  identical-byte-401 required);
- HTTP smoke without cross-transport parity check
  (§16.1.5 required);
- "transport works on my machine" without explicit
  evidence in commit message;
- assertion that real MCP client (Claude Desktop /
  MCP CLI) works without smoke evidence — real-client
  testing is **NOT** required (per §16.4) but **also
  cannot substitute** for the §16.1 smoke list.

### 16.4 — No real MCP client integration test as gate

Step 4 verification **MUST NOT** require a real MCP
client integration test (e.g., Claude Desktop launching
the server, MCP CLI dispatching a request) as a closure
gate. Such testing — Step 5 (operator/docs alignment)
recommendation territory; recommended но не blocker.
Reasoning: real client testing requires operator
infrastructure (MCP client installed, configured); это
вне Step 4 developer loop. Pattern carry-over from
Track G §13.4.

---

## 17. Honest non-goals (повтор для ясности)

Track H после closure **не** делает:

- universal production-grade MCP transport (HTTP only,
  sequential per-request through stdlib threading; not
  async, not HTTP/2, not gRPC);
- network-grade WebSocket / SSE / TCP / Unix-socket /
  named-pipe transports;
- advanced authentication / authorization (only static
  bearer; no JWT / OAuth / OIDC / SAML / mTLS / HTTP
  Basic / HMAC signing / RBAC / ABAC / multi-tenant /
  per-token permissioning / token rotation endpoint /
  refresh tokens);
- TLS / HTTPS termination в process (operator's reverse
  proxy responsibility);
- supervision daemon / systemd unit / Windows Service
  registration / `launchd` plist / Docker / Kubernetes
  deployment manifests / `supervisor` / `runit` / `s6`
  recipes / auto-update / hot reload / background
  watcher;
- HA / clustering / multi-node / service discovery /
  load balancing;
- distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics);
- web UI / dashboard frontend;
- packaging ecosystem beyond `[project.scripts]` console
  entries (`.msi` / `.deb` / signed distribution / GUI
  installer / wizard / PyPI publication / wheel
  publication);
- full enterprise super-set (SSO / SAML / OIDC / SCIM /
  RBAC platform / multi-tenant / secrets vault as
  service / federated audit / policy-as-code DSL);
- 1cv8.exe execution work;
- rollback / AST / metadata / new MCP tools;
- multi-version 1С matrix expansion;
- standalone `apps/platform` entrypoint;
- real MCP client integration testing as Step 4 closure
  gate;
- production deployment readiness для adversarial
  internet (trusted-network deployment posture only).

Track H ship'ит **second baseline** для MCP server
network deployment — local trusted-stdio (Track G) +
trusted-network HTTP с bearer-token perimeter (Track H).
Большой step forward от «local-only MCP servers», но
**не** «full enterprise-ready production deployment».

---

## 18. Step 4 handoff note

После Step 3 closure (этот contract document shipped),
Step 4 имеет:

1. **Exact transport family** + framing + endpoint shape
   + Content-Type + body limit + connection lifecycle
   (per §4).
2. **Exact MCP method set** + cross-transport parity rule +
   notifications dispatch (per §5).
3. **Exact JSON-RPC ↔ HTTP boundary** — every failure mode
   has pinned HTTP status + envelope (per §6).
4. **Exact concurrency model** (`ThreadingHTTPServer`,
   stateless per-request, no ordering guarantees, deferred
   resource limits) (per §7).
5. **Exact auth contract** — header format (case-insensitive
   scheme), single-space separator, failure-equivalence
   class, constant-time validation, redaction discipline,
   forbidden auth shapes (per §8).
6. **Exact `ProductConfig.auth` schema** + env-substitution
   rule + backward-compat behaviour (per §9).
7. **Exact CLI surface** — preserved existing flags + new
   `--bind` (required-when-http) + new `--auth-token-env`
   (optional, CLI-wins precedence) + startup failure shape
   + forbidden flags (per §10).
8. **Exact integration boundary** — new
   `_network_transport.py` private helper +
   `run_main_http(...)` parallel signature + three
   `__main__.py` extension shape + `apps/platform/models.py`
   + `apps/platform/loader.py` changes; everything else
   byte-identical (per §11).
9. **Backward compatibility** — registries / `mcp_common`
   API / `_stdio_transport.py` (modulo §11.3 refactor) /
   existing CLI flags / tools.py / runtime/* / audit shape
   (per §12).
10. **TLS posture** — explicit no-in-process-TLS;
    operator's reverse proxy responsibility (per §13).
11. **`pyproject.toml` posture** — no new deps, no
    optional deps, no script changes, no version bump,
    wheel-build empty preserved (per §14).
12. **Exact allowed / forbidden file list** + scope creep
    markers (per §15).
13. **Verification protocol** — required positive smoke +
    required negative checks + what does NOT count (per
    §16).

Step 4 **MUST NOT**:

- expand scope beyond §15.1 allowed files;
- add SDK or third-party dependency (per §14);
- add network transport beyond HTTP (per §4.8);
- add auth shape beyond static bearer (per §8.8);
- add supervision / service / hot-reload code (per §3.5);
- modify registries / `mcp_common` public API / audit
  shape (per §12);
- introduce uncaught Python exceptions or stdout/stderr
  noise on auth-fail / startup-fail paths (per §6 / §10.6);
- run 1cv8.exe (per §3.5);
- touch operator-facing docs (Step 5 territory);
- claim closure (Step 6 territory).

Step 5 (operator/docs alignment) и Step 6 (closure) — out
of scope этого contract; они оперируют над фактическим
post-Step-4 state.
