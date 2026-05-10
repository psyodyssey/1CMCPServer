# Track J — Deployment-Boundary Baseline Audit

> **Status.** Track J / Step 2 — descriptive baseline audit
> (docs-only). This document **describes** the deployment-
> boundary surfaces that already exist in the repository as
> of HEAD `e203e43` (Track J / Step 1 closed). It does NOT
> add normative MUST / MUST NOT language; that is reserved
> for Step 3 (contract). It does NOT change production
> code. It does NOT pre-commit Step 4 to docs-only or to a
> code change — Step 4 PATH A / PATH B / PATH C openness is
> preserved per the Step 1 plan / step-map.

> **Authoritative version pin (read-time grounding).**
> `pyproject.toml` `version = 0.5.1` (Track I closure
> bump); registry invariants `read = 15 / write = 25 /
> intelligence = 16` carried through unchanged from
> Track I closure into Track J / Step 1.

---

## 1. Purpose / scope

### 1.1 — Why this audit exists

Track J / Step 1 (commit `e203e43`) opened the tenth post-
phase parallel track to formalize the existing "trusted-
network behind operator-owned reverse proxy" general-
policy statement (Track H Step 3 contract §13) into an
operator-facing single-source-of-truth deployment-
boundary recipe. Step 1 was deliberately planning-only:
two architecture documents (plan + step-map) and narrative
updates to `README.md` / `PROJECT-STATUS.md`, no code
changes.

Step 2 — this document — is a descriptive audit of what
the repository already says and does about deployment
boundary, so that Step 3 (contract) can formalize on the
basis of observed reality rather than aspirational
guesses.

### 1.2 — What this audit must answer

Per Step 1 plan §8–§14 and Step 1 step-map Step 2 row,
this audit must directionally resolve:

- Q1 — honest primary target of Track J;
- Q2 — likely Step 4 path (PATH A docs-only / PATH B tiny
  code / PATH C hybrid);
- Q3 — exact deployment threat model realistic after
  Track H/I;
- Q4 — exact surfaces relevant to deployment boundary;
- Q5 — whether `/healthz` is genuinely needed in Track J
  or scope creep;
- Q6 — whether Track J actually needs production code at
  all, or whether the bigger gap is operator-facing docs;
- Q7 — handoff list for Step 3 contract.

### 1.3 — Hard scope limits

This audit:

- **Does NOT** rewrite Track J Step 1 plan or step-map.
  Their statements stand. Where this audit narrows a
  Step 1 open question, that narrowing is explicitly
  tagged as a **directional** finding for Step 3 to
  consume, not a normative re-decision.
- **Does NOT** propose Step 4 implementation.
- **Does NOT** propose any code change.
- **Does NOT** propose any pyproject / scripts /
  SECURITY.md / release-handoff.md / apps/platform/
  README.md / CHANGELOG.md / README.md / PROJECT-STATUS.md
  edit. These remain Step 5 / Step 6 territory and Track J
  / Step 2 commits exactly one new file.
- **Does NOT** invent a new threat model. The threat
  model audit-described here is the one observable in
  existing repository text (Track H §13, SECURITY.md,
  release-handoff.md, apps/platform/README.md).
- **Does NOT** claim the platform is production-ready,
  enterprise-ready, hostile-internet ready, or
  multi-tenant ready. None of those are true.

---

## 2. Method / evidence sources

### 2.1 — Files inspected

Read top-to-bottom or large-section-grepped:

- `packages/mcp-common/src/mcp_common/_network_transport.py`
  (HTTP transport runtime — full read).
- `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  (stdio transport runtime — full read).
- `apps/mcp-read-server/src/mcp_read_server/__main__.py`
  (entrypoint shape — full read; the other two
  `__main__.py` are byte-equivalent in dispatch shape and
  were not separately re-read in Step 2).
- `SECURITY.md` (full read).
- `docs/release-handoff.md` (full read).
- `docs/architecture/track-h-network-transport-and-auth-contract.md`
  §10.3–§10.6 (bind / auth flag rules — full read of those
  sections), §13 (TLS posture — full read).
- `apps/platform/README.md` (grep-only for
  `TLS|reverse|proxy|--bind|deployment|loopback|trusted-
  network|hostile|exposure`; the file is 42K+ tokens, full
  read was not necessary for the boundary question).
- `docs/{operator,administrator,developer}-manual.md`
  (grep-only for the same pattern set).
- `scripts/dev/{launch.ps1,run_dev_check.ps1,selfcheck.py,README.md}`
  (grep-only for `--bind|--transport|TLS|reverse|http`).
- `scripts/release/README.md` (grep-only).
- `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-{plan,step-map}.md`
  (already-shipped Step 1 documents, used here as the
  contract for Step 2 scope, not as evidence about the
  product itself).

### 2.2 — Evidence types

The audit distinguishes:

- **Code evidence** — actual runtime behaviour observable
  in `_network_transport.py` / `_stdio_transport.py` /
  `__main__.py`. Highest weight.
- **Contract evidence** — normative statements in the
  Track H Step 3 contract document. Already authoritative
  across the platform; serves as canonical text Track J
  builds on.
- **Operator-facing doc evidence** — statements in
  SECURITY.md, release-handoff.md, apps/platform/README.md,
  manuals. Lower weight than code/contract; useful for
  measuring documentation drift.
- **Track-J-already-shipped evidence** — Step 1 plan /
  step-map. Used only to confirm Track J scope; not
  re-litigated.

### 2.3 — Out-of-bounds

- `1cv8.exe` was not run for Step 2.
- No live MCP client was used.
- No real reverse proxy (nginx / Caddy / Apache / cloud
  LB) was stood up for Step 2.
- No real bearer token, real env var, or real production
  config was exercised.

---

## 3. Current deployment-boundary baseline

### 3.1 — stdio transport (Track G / Step 4)

`_stdio_transport.py` provides `_serve_stdio` and
`run_main`:

- Line-delimited JSON-RPC 2.0 over `sys.stdin` / `sys.stdout`.
- Diagnostic logging to `sys.stderr` only.
- No network listener. No socket. No bind.
- No authentication (`Track G threat model: trusted local
  subprocess`).
- `--transport stdio` is the default in the unified Track H
  argparser (`_network_transport._build_arg_parser`).
- `--bind` and `--auth-token-env` are **silently ignored**
  on stdio path per Track H Step 3 contract §10.3 / §10.4.

**Observed deployment-boundary characteristic of stdio.**
The boundary is the operating-system process boundary.
Whoever started the subprocess controls the channel;
there is no perimeter to expose, no bind to misconfigure,
no proxy to front.

### 3.2 — HTTP transport (Track H / Step 4)

`_network_transport.py` provides `run_main_http`,
`_serve_http`, `_MCPHandler`, `_parse_bind`,
`_resolve_token_sources`, `_resolve_config_tokens`,
`_resolve_env_token`, `_auth_header_passes`,
`_content_type_is_json`, `_make_handler_class`.

#### 3.2.1 — Listener shape

- `http.server.ThreadingHTTPServer((bind_host, bind_port),
  handler_class)` — stdlib, plain HTTP/1.1, threaded
  (one-thread-per-request).
- `protocol_version = "HTTP/1.1"`. Default
  `Connection: close`-style behaviour (no explicit
  keep-alive promise per Track H contract §4.7).
- `daemon_threads = True` (Ctrl-C does not wait for
  in-flight requests).
- Single endpoint `/mcp`. Any other path → `404 Not
  Found` (`_send_plain` with `text/plain; charset=utf-8`).
- Method gate: `POST` only. `GET / PUT / DELETE / PATCH /
  OPTIONS / HEAD` on `/mcp` → `405 Method Not Allowed`
  with `Allow: POST`. Same methods on a non-`/mcp` path
  → `404 Not Found` first (path check is first).
- Body cap: `1024 * 1024` bytes (1 MiB). Over-cap → `413
  Request Entity Too Large` + JSON-RPC `-32600` envelope.

#### 3.2.2 — Bind validation

`_parse_bind(bind_value, prog)` (lines 173–193):

- Regex `BIND_RE = ^(.+):(\d+)$` — host non-empty,
  port digits.
- Empty host → fail-closed.
- Port not int / out of range `1..65535` → fail-closed.
- `socket.gethostbyname(host)` resolution failure →
  fail-closed (the OSError message is **not** echoed;
  operator gets only the host they typed).

There is **no default `--bind` value**. Operator must
always specify it explicitly when `--transport http`
(per Track H §10.3, "deliberate: prevents accidental
`0.0.0.0:8000` exposure or unhelpful default ports").

#### 3.2.3 — Auth gate

- `Authorization` header parsed by `AUTH_HEADER_RE =
  ^([A-Za-z]+) ([^\s].*)$` — single ASCII space,
  case-insensitive scheme matched against `bearer`,
  byte-exact `hmac.compare_digest` against each entry in
  `valid_tokens` tuple.
- Multiple `Authorization` headers → `400 Bad Request` +
  JSON-RPC `-32600` envelope.
- Missing / empty / malformed / scheme-mismatch /
  token-mismatch all converge on identical `401
  Unauthorized` + `WWW-Authenticate: Bearer realm="mcp"`
  + JSON-RPC `-32001` envelope (failure-equivalence per
  Track H §8.4).
- Token values **never** appear in stderr / logs / response
  bodies / error messages (Track H §6.5 / §8.7 redaction
  discipline).

#### 3.2.4 — Forwarded-header treatment

`_MCPHandler` does **not** read, parse, or trust any of
the following headers:

- `X-Forwarded-For`
- `X-Forwarded-Proto`
- `X-Forwarded-Host`
- `X-Real-IP`
- `Forwarded` (RFC 7239)
- Any other proxy-injected metadata header.

A grep across the entire repo for `X-Forwarded` /
`forwarded.header` / `forwarded.for` / `client_ip` /
`peer_ip` returns zero matches in production code. This
is observable behaviour, not aspiration: nothing in the
HTTP path consumes these headers, so the listener cannot
be tricked into trusting client-supplied proxy metadata.

`log_message` (lines 314–328) writes
`address_string()` to the diagnostic log; this is the
stdlib default — the TCP peer's connect address. When the
listener is fronted by a reverse proxy, that address is
the proxy's address, not the original client's. The
listener does not attempt to recover the original client
address.

#### 3.2.5 — Logging shape

- Diagnostic logs go to `sys.stderr` via the
  `mcp_common._stdio_transport._configure_logging`
  helper (re-used by HTTP path — `_network_transport`
  imports it).
- `BaseHTTPRequestHandler.log_message` is overridden to
  route through the structured logger (uniform line
  format; no token data; no path-data leak vector since
  tokens live only in headers).
- Startup line: `"Starting <server> HTTP transport
  (JSON-RPC 2.0) on <host>:<port> with <N> valid
  token(s)."` — exposes count, never values.

#### 3.2.6 — Failure modes (bind / auth / startup)

`_fail(prog, message)` writes a single
`<prog>: <message>` line to stderr and raises
`SystemExit(2)`. No Python traceback reaches operator
stderr. Exit code matches argparse-style usage failure.

#### 3.2.7 — No `/healthz`, no `/readyz`, no `/livez`

`_MCPHandler.do_POST` short-circuits to `404` for
`self.path != "/mcp"`. There is no
liveness / readiness / health endpoint. Track H Step 3
contract §13 does not mention one. The existing
`runtime.py` / `process_control.py` "liveness probe"
language refers to OS-level PID checks for 1С
subprocesses, **not** to an HTTP probe.

### 3.3 — Three `__main__.py` entrypoints

`apps/mcp-read-server/src/mcp_read_server/__main__.py`,
`apps/mcp-write-server/src/mcp_write_server/__main__.py`,
`apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
all dispatch through `mcp_common._network_transport.run_main_http`
with their own `SERVER_NAME` / `SERVER_VERSION` /
`list_tools` / `get_tool` callables. CLI flag set is
identical across all three. `SERVER_VERSION` strings are
all `0.4.0` (Track H Step 4 baseline; not refreshed by
Track I PATCH bump because that bump touched
`pyproject.toml` only).

### 3.4 — Implicit threat model (observed)

The threat model that the **code actually assumes** —
not the marketing surface, not the aspiration:

- **stdio path.** Trusted local subprocess. Channel is a
  pair of pipes inherited from the parent process. No
  attacker between parent and child.
- **HTTP path.** Trusted internal network. The listener
  binds plain HTTP/1.1; bearer token gives integrity
  against passive snooping only if the wire is
  TLS-wrapped externally; if the wire is plain TCP, a
  passive attacker on the path can recover the token.
  Therefore **the channel is only secure when an external
  TLS-terminating reverse proxy fronts the listener**.
  This is exactly Track H §13.2's deployment model:
  `[client] ─TLS→ [reverse proxy] ─plain HTTP→ [listener
  on loopback / private interface]`.

Operator therefore **MUST** treat any `--bind` host
reachable from a hostile network as a token-leak risk in
the absence of fronting TLS. The current text says this
in scattered locations (Track H §13.2 SHOULD; SECURITY.md
"Honest constraints"; release-handoff.md "What is NOT");
no single recipe consolidates it.

---

## 4. Existing reusable surfaces (already-good)

These pieces are descriptively sound and Step 3 / Step 4
likely cite them rather than rewrite them.

### 4.1 — Track H Step 3 contract §13 (TLS posture)

The canonical normative source. Three sub-sections:

- §13.1 — In-process TLS = forbidden. No `ssl.wrap_socket`,
  no `ssl.SSLContext`, no certificate loading.
- §13.2 — Operator deployment model (the
  client→TLS→reverse-proxy→plain-HTTP→listener diagram).
  "Operator SHOULD bind to loopback or private interface;
  MAY bind public with explicit risk acceptance."
- §13.3 — mTLS = explicit out-of-scope.

This is already at MUST / MUST NOT / SHOULD / MAY
granularity. Track J does **not** re-litigate it.

### 4.2 — Track H Step 3 contract §10.3–§10.6 (bind /
auth startup gates)

Codified rules: no default `--bind`; required-when-http
gate; `socket.gethostbyname` validation; port range gate;
fail-closed startup. These are in production and are
exactly what an operator-facing recipe needs to cite when
explaining "how to bind safely."

### 4.3 — `_parse_bind` runtime validation

`packages/mcp-common/src/mcp_common/_network_transport.py:173–193`.
Already enforces shape, range, resolution. No drift
detected against §10.3 / §10.6.

### 4.4 — `_MCPHandler` non-consumption of forwarded headers

Observable from code: zero references to
`X-Forwarded-*`, `Forwarded`, `X-Real-IP`, etc., across
the entire repository. This is already the right
behaviour for "do not trust client-supplied proxy
metadata", but it has never been **stated** as a policy
anywhere in operator-facing docs. Step 3 / Step 5 should
state it explicitly.

### 4.5 — SECURITY.md "Honest constraints" bullet on transports

`SECURITY.md` lines 40–78 already say:

- two transports with their threat models named;
- "Threat model for HTTP = trusted-network deployment
  behind an operator-owned reverse proxy that terminates
  TLS";
- "Operator SHOULD bind the listener to a loopback or
  private interface and front-proxy it";
- explicit "Still NOT shipped" list (in-process TLS,
  mTLS, JWT/OAuth/OIDC/SAML, RBAC/ABAC, supervisor
  daemon, etc.).

This is dense and correct; it is **not** a recipe and
does **not** contain a per-scenario matrix, but the
underlying statements do not need rewriting.

### 4.6 — `docs/release-handoff.md` "What is NOT in this
handoff" bullet

Lines 128–164 mirror the SECURITY.md statements at the
right level. Same observation: dense, correct, not a
recipe.

---

## 5. Adjacent but insufficient surfaces

These pieces are partially in place but are scattered or
partial relative to the Track J goal.

### 5.1 — Bind-host guidance (single sentence, no matrix)

Current state across SECURITY.md / release-handoff.md /
Track H §13.2: one SHOULD ("loopback or private
interface") + one MAY ("public interface with operator's
risk acceptance"). No table that walks an operator
through:

| Scenario | Bind host | Reverse proxy needed? | TLS termination | Token wire-confidentiality |
|---|---|---|---|---|
| Local development on the operator's own laptop | `127.0.0.1` / `::1` | Optional (curl from same host) | n/a if loopback only | n/a if loopback only |
| Trusted private subnet (LAN / VPN) | private IP | **Required** if exposing beyond loopback | Reverse proxy | Wire-confidential only behind proxy |
| Public-facing through reverse proxy | Loopback (recommended) or private IP | **Required** | Reverse proxy | Wire-confidential only behind proxy |

Gap: the table above is **not present anywhere** in the
repo. Each row's facts are derivable from existing text,
but no operator-facing document presents them as a single
decision matrix.

### 5.2 — Reverse-proxy integration recipe (no concrete example)

No existing document shows:

- a concrete `nginx` `location /mcp { proxy_pass ... }`
  block;
- a concrete `Caddy` site block;
- guidance on which `Host` header / `proxy_pass` URL to
  use;
- explicit statement that the reverse proxy **MAY**
  inject `X-Forwarded-*` headers but the listener will
  **not** consume them (so no `set_real_ip_from` /
  `real_ip_header` configuration is required for
  correctness);
- what the operator should do about request-size limits
  at the proxy layer (the listener caps bodies at 1 MiB;
  proxies typically have their own caps and can be
  configured to align).

Gap: the concept "trusted-network deployment behind
operator-owned reverse proxy" is asserted; the recipe to
**actually do it** is left to the operator.

### 5.3 — Forwarded-header policy (silent, not stated)

Observable in code: not consumed.
Policy-stated anywhere: no.

The closest text is Track H Step 3 contract §13.2 which
implies the listener trusts only its bound interface, but
does not name `X-Forwarded-*` directly. A single-paragraph
explicit statement in operator-facing docs would prevent
operators from assuming the listener does IP-based
allow-listing on the basis of proxy-injected headers
(which it does not).

### 5.4 — Exposure-rule / "safe to expose" wording

`SECURITY.md` says "trusted-network deployment behind an
operator-owned reverse proxy that terminates TLS." This
is the right policy. What's missing is a sharper
operator-facing rule, e.g.:

> Bind the listener to `127.0.0.1` or a private interface
> only. If you need to expose `/mcp` to clients off-host,
> place an operator-owned reverse proxy in front of the
> listener and have the proxy terminate TLS. **Do not
> bind the listener directly to a public interface without
> a fronting TLS proxy** — the bearer token is wire-
> readable on plain HTTP and the listener does not
> validate origin IP from `X-Forwarded-*` headers.

This sharper wording is **not** in the repo today.

### 5.5 — `apps/platform/README.md` deployment-boundary
references

The file already cites the trusted-network deployment
model and the no-in-process-TLS posture in multiple
places (lines 697–739, 1326–1328, 1972–1974 per grep).
These are **citations** of Track H §13, not a recipe;
they correctly identify the boundary but do not
operationalize it.

### 5.6 — `scripts/dev/*` and `scripts/release/*`

`scripts/dev/launch.ps1`, `scripts/dev/run_dev_check.ps1`,
`scripts/dev/README.md`, `scripts/release/README.md` —
mention `--transport`, `--bind`, `http` only in passing.
None ship a "how to deploy behind a reverse proxy" recipe
or a worked example of a fronting TLS proxy. This is
honest scope (the scripts intentionally do **not** start
the MCP servers — see release-handoff.md "Local check /
launch sequence"); but it means there is no
deployment-boundary recipe living in the scripts tree
either.

### 5.7 — Manuals

Grep across `docs/{operator,administrator,developer}-
manual.md` for `TLS|reverse.proxy|--bind|trusted-network|
loopback|0\.0\.0\.0|127\.0\.0\.1|hostile|exposure|
deployment.boundary|X-Forwarded` returns one match —
`administrator-manual.md:48` — a config fragment using
`http://127.0.0.1:8080/local-dev` as an example
`http_base_url` for an unrelated runtime field (not the
HTTP transport bind). Effectively, the operator manuals
**do not currently say anything about Track J's
deployment boundary**. This is the largest single
documentation gap.

---

## 6. Missing pieces

These are pieces that do not exist in the repository at
all today. Step 3 will decide which of them Track J
formalizes; Step 4 will decide which of them Track J
ships.

### 6.1 — Single-source-of-truth deployment-boundary recipe

A canonical document (working title:
`docs/operators/deployment-boundary.md` or similar; final
location is Step 3 / Step 5 territory) that:

- names the three deployment scenarios (loopback /
  private subnet / public-facing-through-reverse-proxy);
- gives the bind-host decision per scenario;
- gives a concrete reverse-proxy integration recipe
  (nginx / Caddy snippet);
- states the X-Forwarded-* policy ("not consumed by
  listener");
- states the TLS termination point ("operator's reverse
  proxy only; in-process TLS forbidden");
- states the token wire-confidentiality model ("bearer
  token is wire-readable on plain HTTP; therefore
  operator MUST ensure TLS termination upstream of the
  listener");
- cross-references SECURITY.md / release-handoff.md /
  Track H §13.

This document does **not** exist today. Creating it is
PATH A (docs-only).

### 6.2 — Per-scenario matrix table

A single dense table (similar to the one in §5.1 above)
that an operator can read in 30 seconds. No equivalent
table exists today.

### 6.3 — Explicit X-Forwarded-* policy paragraph

A single paragraph stating that the listener does not
consume `X-Forwarded-*` / `Forwarded` / `X-Real-IP` and
operators should not configure the reverse proxy under
the assumption that injected client IP will reach the
listener for any kind of allow-listing. Today this is
only inferable from absence-of-code.

### 6.4 — Bind-host warning for `0.0.0.0` (optional, PATH B)

A possible ≤15-LOC addition in
`_network_transport._serve_http` (or in the existing
`_parse_bind` validation) that emits a single
operator-readable warning line on stderr when
`bind_host` resolves to `0.0.0.0` / `::` / a public-
facing IP, alerting the operator that the listener does
**not** front itself with TLS and the bearer token is
wire-readable.

This is **not** present today. Step 3 will decide
whether this warning is in scope; Step 4 (PATH B) would
implement it; Step 4 (PATH A) would document the same
behaviour in prose without code change.

### 6.5 — `/healthz` endpoint (optional, PATH B/C)

A possible ≤15-LOC addition in `_MCPHandler.do_GET` that
returns `200 OK` + `text/plain; charset=utf-8` body
`"ok\n"` for `GET /healthz`, **without** auth, so a
load-balancer health probe can confirm the listener is
alive without holding a bearer token.

Today there is no `/healthz`. Today the only way to
probe liveness from outside is to `POST /mcp` with a
valid token, which is more than a load balancer should
need to do.

This is genuinely operator-convenience-shaped; whether
Track J ships it depends on Step 3 contract decision.
See §8.5 (Q5 directional resolution) for the audit's
recommendation.

### 6.6 — Concrete `nginx` / `Caddy` proxy_pass snippets

These are not in the repo. Their absence is exactly the
gap Track J intends to close (PATH A primary deliverable).

---

## 7. Current honest threat model

Restated tightly, from observable code + observable text:

### 7.1 — stdio path

- **Boundary.** OS process boundary (parent ↔ child
  pipes).
- **Trusted parties.** Whoever started the subprocess.
- **Untrusted parties.** None inside the boundary.
- **Wire confidentiality.** Not applicable — no wire.
- **Authentication.** Not applicable — boundary is OS-
  level.
- **Survives.** Compromised user account → compromised
  channel; this is the OS's problem, not the platform's.
- **Does NOT survive.** Hostile network attacker
  (irrelevant — no network) / privileged-process
  injection (OS's problem).

### 7.2 — HTTP path

- **Boundary.** TCP listener bound to `bind_host:bind_port`,
  expecting an operator-owned reverse proxy in front of
  it for any non-loopback exposure.
- **Trusted parties.** Operator; operator-owned reverse
  proxy; clients reaching the listener via the reverse
  proxy.
- **Untrusted parties.** Anyone on the wire upstream of
  the reverse proxy (the proxy's TLS terminates them);
  anyone on the wire between proxy and listener if that
  hop crosses an untrusted segment (operator's
  responsibility to keep the inner hop on a trusted
  network).
- **Wire confidentiality.** Provided by the reverse
  proxy's TLS termination, **not** by the listener.
- **Authentication.** Static bearer token, byte-exact
  `hmac.compare_digest`, single ASCII-space scheme,
  failure-equivalent 401 responses, complete redaction
  discipline.
- **Survives.** Forgotten Authorization header /
  malformed token / wrong scheme / token mismatch (all
  → identical 401). Multi-Authorization (→ 400). Body
  over 1 MiB (→ 413). Unknown path (→ 404). Wrong method
  on `/mcp` (→ 405 + Allow). Bind-host typo at startup
  (→ fail-closed exit 2). Missing token source at
  startup (→ fail-closed exit 2).
- **Does NOT survive.** Operator binds listener to a
  public interface without a fronting TLS proxy and a
  passive attacker on the path captures the bearer
  token. (This is the canonical "do not do this"
  scenario Track J intends to operationalize.)
- **Does NOT survive.** Operator places listener behind
  a reverse proxy and assumes `X-Forwarded-*` is
  consulted for allow-listing. (It is not. The listener
  treats every reachable client as authenticated iff the
  bearer token validates, regardless of injected
  client-IP metadata.)
- **Does NOT survive.** Adversary with mTLS-capable
  client expecting client-cert auth. (Not implemented.)
- **Does NOT survive.** Adversary expecting JWT / OAuth /
  OIDC / SAML / SCIM / RBAC / ABAC / per-tool ACL /
  rate-limiting / WAF / IDS / DDoS protection / observability
  hooks. (None implemented; explicit out-of-scope.)

### 7.3 — Honest summary phrase

The product after Track H / Track I is:

> A trusted-internal-network HTTP MCP listener with
> static bearer authentication, fronted by an
> operator-owned reverse proxy that terminates TLS. Not
> hostile-internet ready. Not enterprise-identity ready.
> Not multi-tenant. Not load-balanced. Not observed.
> Not supervised.

This is true. Track J formalizes the **first half** of
this phrase ("trusted-internal-network ... fronted by an
operator-owned reverse proxy that terminates TLS") into
an operator-facing recipe; Track J does **not** change
the second half.

---

## 8. Directional Q1–Q6 resolutions

These are descriptive directional findings for Step 3 to
formalize. They are **not** normative.

### 8.1 — Q1 (honest primary target)

**Directional finding.** Reverse-proxy-first boundary
formalization. In-process TLS is **NOT** the target —
Track H §13.1 already forbids it and Track J inherits
that invariant unchanged. Hybrid (reverse-proxy-first +
deferred in-process TLS as future track) is the
realistic framing: Track J formalizes the reverse-proxy
deployment and explicitly defers any in-process TLS
question to a hypothetical future track outside Track J's
scope.

**Evidence.** `_network_transport.py` has zero `ssl`
imports beyond what stdlib pulls indirectly; Track H §13.1
forbids `ssl.wrap_socket` / `SSLContext` / certificate
loading; SECURITY.md "Still NOT shipped" lists in-process
TLS first; Step 1 plan §8 Q1 default = hybrid (reverse-
proxy-first + in-process TLS deferred).

### 8.2 — Q2 (Step 4 path direction)

**Directional finding.** PATH A (docs-only) is the most
honest default. PATH B (narrow ≤15 LOC code) is viable
**only** if Step 3 contract finds a concrete behavioural
gap that prose cannot close (e.g., decides the bind-host
warning at `0.0.0.0` is required, or decides `/healthz`
is required for operator deployment ergonomics). PATH C
(hybrid) is viable if Step 3 lands both: the recipe doc +
one of those tiny code additions.

**The audit does not lock Q2.** Step 1 step-map's
"Track invariant: Step 4 PATH A/B/C openness preserved"
stands. The audit's preliminary direction is **PATH A**
because:

- the dominant gap is **operator-facing recipe absence**,
  not behavioural absence;
- runtime behaviour already enforces fail-closed bind /
  auth and fails on `socket.gethostbyname` / port-range /
  port-in-use without code change;
- non-`/mcp` already returns 404, so a load balancer
  pointed at any path other than `/mcp` already gets a
  deterministic non-2xx without a token — `/healthz` is
  a convenience, not a correctness gap;
- Track J's stated cost discipline ("narrowest honest
  formalization") aligns with PATH A.

**The audit explicitly does not foreclose PATH B or PATH C.**
If Step 3 finds the X-Forwarded-* policy is more
operator-protective when paired with a `0.0.0.0` warning,
or that `/healthz` is genuinely needed by load-balancer-
class operators, PATH B becomes the right call. Step 3
makes that decision on evidence at that point.

### 8.3 — Q3 (deployment threat model)

**Directional finding.** Trusted internal network behind
operator-owned reverse proxy. Operator-owned LAN / VPN /
corporate network. **Explicitly not** hostile public
internet. Explicitly not multi-tenant. Explicitly not a
zero-trust posture (no per-request client identity
verification beyond the static bearer; no continuous
authentication; no mTLS).

**Evidence.** Track H §13.2 deployment model diagram;
SECURITY.md "Honest constraints" "trusted-network
deployment"; release-handoff.md "What is NOT" list;
absence of `X-Forwarded-*` consumption in code
(consistent with "not zero-trust", since the listener
has no per-request client-IP signal).

### 8.4 — Q4 (deployment-boundary surfaces)

**Directional finding.** Track J's relevant surfaces are
exactly:

- `--bind <HOST>:<PORT>` startup flag and its validation
  (`_parse_bind`);
- the proxy-facing endpoint shape (`/mcp` POST only;
  `application/json`; 1 MiB cap; bearer auth; failure-
  equivalent 401 with `WWW-Authenticate`);
- TLS termination point — operator's reverse proxy
  only; in-process TLS forbidden carry-over from §13.1;
- exposed-interface guidance — bind to loopback /
  private interface; expose only via reverse proxy;
- reverse-proxy trust assumptions — operator owns the
  proxy; the inner hop (proxy → listener) is on a
  trusted network segment;
- forwarded-header policy — listener **does not consume**
  `X-Forwarded-*` / `Forwarded` / `X-Real-IP`; semantics
  do **not** matter to listener correctness.

**Out of Q4 scope.** Anything that requires a code
change Track J is unwilling to make (see Q2 / §8.2
PATH discipline).

### 8.5 — Q5 (`/healthz` endpoint genuinely needed?)

**Directional finding.** Discretionary, not strictly
required. Recommendation = **defer by default to PATH A**.

**Reasoning.**

- Today, any non-`/mcp` path returns deterministic `404
  Not Found` with no auth required. A load balancer that
  treats "TCP-connectable + HTTP-2xx-or-known-4xx" as
  alive can already health-check the listener by
  pointing at `/healthz` (and seeing 404) without
  carrying a bearer token. Strict 2xx-only health
  probers cannot, however.
- Adding a 2xx-returning unauthenticated `/healthz` is
  technically tiny (≤15 LOC in `do_GET` + path branch),
  but it is **net-new external capability**. Track J's
  cost discipline argues against shipping new external
  capability when the documentation gap is the dominant
  one.
- If Step 3 contract finds operator-facing demand
  (load-balancer-class deployments) for a 2xx-only
  health probe, `/healthz` becomes a candidate Step 4
  PATH B addition. The audit does not lock this out.

**Audit recommendation to Step 3.** Default = defer.
Document the `404` health-probing mode explicitly in the
deployment-boundary recipe (operators with strict-2xx
load balancers learn what to expect). Re-visit if a
concrete operator-facing need surfaces during Step 3.

### 8.6 — Q6 (does Track J need code at all?)

**Directional finding.** Probably no. Bigger gap is
operator-facing deployment contract / docs.

**Reasoning summary.**

- Code-level invariants Track J would want — bind
  validation, fail-closed startup, `/mcp` POST-only,
  bearer auth with redaction, 401 failure-equivalence,
  no `X-Forwarded-*` consumption — **are all already in
  place** from Track H Step 4.
- The gaps are exclusively documentation gaps: no
  recipe, no scenario matrix, no `X-Forwarded-*` policy
  paragraph, no nginx/Caddy snippet.
- A `0.0.0.0` warning (PATH B candidate) and a
  `/healthz` endpoint (PATH B/C candidate) are **nice to
  have**, not load-bearing for the deployment-boundary
  formalization itself.

**Audit recommendation to Step 3.** Default = PATH A
(docs-only). Step 4 ships an operator-facing
deployment-boundary recipe document and the Step 5
operator-facing alignment touches SECURITY.md /
release-handoff.md / apps/platform/README.md as needed
to point at it. PATH B / PATH C remain available if
Step 3 evidence pushes the other way.

---

## 9. Step 3 handoff note

Items that Step 3 contract should pin (this is the
audit's directional handoff list, not a normative
contract; Step 3 may refine):

1. **Track J's normative TLS posture** = byte-identical
   carry-forward of Track H §13.1 (in-process TLS
   forbidden) / §13.2 (operator-owned reverse-proxy
   deployment model) / §13.3 (mTLS out-of-scope). Track
   J **MUST NOT** weaken §13.1.
2. **Bind-host SHOULD/MAY tier** — operator **SHOULD**
   bind to loopback / private interface; operator **MAY**
   bind to a public interface only with explicit risk
   acceptance and only behind an operator-owned TLS-
   terminating reverse proxy. (Promotes existing §13.2
   one-sentence guidance to per-scenario MUST/SHOULD/MAY
   matrix.)
3. **Forwarded-header policy** — listener **MUST NOT**
   consume `X-Forwarded-*` / `Forwarded` / `X-Real-IP`
   for any access-control purpose. Step 3 **MUST** state
   this explicitly. Step 4 inherits this as an invariant
   regardless of PATH A / B / C.
4. **Per-scenario exposure rules** — Step 3 contract
   must define the three deployment scenarios (loopback /
   private subnet / public-facing-through-reverse-proxy)
   with bind-host, reverse-proxy-required, TLS-
   termination-point, and token-wire-confidentiality
   for each.
5. **`/healthz` resolution** — Step 3 contract decides:
   defer (default per audit recommendation) or ship.
   Either way must be explicit and operator-readable in
   Step 4 / Step 5 deliverables.
6. **`0.0.0.0` warning resolution** — Step 3 contract
   decides: PATH A document the risk in prose / PATH B
   ship a runtime warning line. Either way must be
   explicit.
7. **PATH A/B/C selection** — Step 3 contract pins the
   final Step 4 path on the basis of items 5–6 and any
   evidence that surfaces in Step 3's normative
   exercise. If Step 3 selects PATH A, Step 4 ships a
   single operator-facing deployment-boundary recipe
   document. If PATH B, ship a single ≤15 LOC code
   addition (no docs file). If PATH C, ship both.
8. **No SemVer pre-commit** — Step 3 contract does
   **not** decide the SemVer bump; that is Step 6 / Q7
   territory. Default expectation per Step 1 plan §14
   remains PATCH `0.5.1 → 0.5.2` if Step 4 is PATH A or
   PATH B narrow, MINOR `0.5.1 → 0.6.0` only if Step 4
   ships meaningful new external capability (e.g.
   `/healthz` endpoint that didn't exist before).
9. **No registry change** — registries `read = 15 /
   write = 25 / intelligence = 16` MUST NOT change in
   Track J. Step 3 contract MUST state this explicitly
   as an invariant.
10. **No changes to existing Track G stdio threat model**
    — stdio path is byte-identical from Track G / Step 4
    forward. Track J does **not** touch
    `_stdio_transport.py`.
11. **No changes to existing Track H `_MCPHandler` shape**
    *unless* Step 3 explicitly chooses PATH B or PATH C,
    and even then only the narrowest possible addition
    (`do_GET` for `/healthz`, or a single warning line in
    `_serve_http`).
12. **No changes to `pyproject.toml`** outside the Step 6
    Q7 SemVer bump (if any). Step 3 is documentation-
    only.
13. **No remote push** — operator action, not part of
    any Track J step.
14. **No real credentials anywhere** — Step 3 contract,
    Step 4 deliverable, Step 5 alignment, Step 6 closure
    all forbid real bearer tokens / real env-var values
    / real reverse-proxy hostnames in committed text.
    Examples MUST use abstract placeholders.

---

## 10. Honest summary

What Track J / Step 2 has established (descriptive only):

- The platform's HTTP transport (`_network_transport.py`
  + three `__main__.py`) **already** behaves correctly
  for a "trusted-internal-network behind operator-owned
  reverse proxy" deployment posture: bind validation,
  fail-closed startup, single POST `/mcp` endpoint,
  bearer auth with failure-equivalence + redaction
  discipline, no consumption of forwarded headers, no
  in-process TLS code path.
- The platform's documentation **scattered-asserts** the
  same posture (Track H §13, SECURITY.md "Honest
  constraints", release-handoff.md "What is NOT",
  apps/platform/README.md citations) but **does not
  consolidate it** into an operator-facing recipe with
  per-scenario matrix, X-Forwarded-* policy paragraph,
  and concrete reverse-proxy snippet examples.
- The dominant Track J gap is therefore documentation,
  not behaviour. Audit's directional default for Step 3 /
  Step 4 = PATH A (docs-only).
- PATH B and PATH C remain open. The audit explicitly
  preserves them, per Step 1 step-map's track-
  invariants block.
- No code changed during Step 2. No registry drift. No
  new MCP tools. No SemVer bump. No `1cv8.exe` runs.
  No real credentials. No remote push. No premature
  closure language. No false implementation claims.

What Track J / Step 2 does **not** do:

- Does not formalize anything as MUST / MUST NOT — that
  is Step 3.
- Does not write a deployment-boundary recipe document —
  that is Step 4 (PATH A) or Step 4 (PATH C) territory.
- Does not implement a `/healthz` endpoint or a
  `0.0.0.0` warning — that is Step 4 (PATH B) or Step 4
  (PATH C) territory if Step 3 selects them.
- Does not edit any operator-facing document
  (SECURITY.md, release-handoff.md, apps/platform/
  README.md, manuals, README.md, PROJECT-STATUS.md,
  CHANGELOG.md). Those alignments are Step 5 territory.
- Does not bump `pyproject.toml` `version`. That is
  Step 6 territory.
- Does not push to a remote. Operator action; not part
  of any Track J step.

Step 2 is therefore closeable as a single descriptive
audit document, with Step 3 (deployment-boundary
contract, normative) as the next opening.
