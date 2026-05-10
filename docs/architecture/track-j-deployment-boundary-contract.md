# Track J — Deployment-Boundary Contract (Normative)

> **Status.** Track J / Step 3 — normative contract.
> Step 1 (commit `e203e43`) opened the track with a
> planning document and a step-map. Step 2 (commit
> `344129c`) shipped a descriptive baseline audit. This
> document — Step 3 — is the **normative** layer: it
> formalizes the deployment-boundary rules, pins the
> final Step 4 PATH selection, and constrains Step 4 /
> Step 5 / Step 6 surfaces so that Track J cannot drift
> into TLS-in-process, mTLS, enterprise identity,
> packaging, supervisor, or generic ops-platform work.
>
> Normative keywords (**MUST**, **MUST NOT**, **SHOULD**,
> **SHOULD NOT**, **MAY**) follow RFC 2119 / RFC 8174
> conventions. Where this document re-states a rule
> already pinned by Track H Step 3 contract §10 / §13, it
> does so by **carry-forward** and **MUST NOT** weaken
> the original rule.

> **Authoritative version pin (read-time grounding).**
> `pyproject.toml` `version = 0.5.1` (Track I closure
> bump). Registry invariants `read = 15 / write = 25 /
> intelligence = 16` carried through unchanged from
> Track I closure into Track J / Step 1 / Step 2 / this
> document. HEAD before this commit = `344129c`.

---

## 1. Purpose / scope

### 1.1 — Why this contract exists

Track J formalizes the platform's existing
"trusted-internal-network behind operator-owned reverse
proxy" general-policy statement (Track H Step 3 contract
§13) into a single normative deployment-boundary
contract. Step 2's descriptive audit established that
the runtime **already** enforces the right invariants
(bind validation, fail-closed startup, `/mcp` POST-only,
bearer auth with failure-equivalence + redaction
discipline, no consumption of `X-Forwarded-*` /
`Forwarded` / `X-Real-IP`, no in-process TLS code
path). The dominant gap is therefore documentation, not
behaviour.

This contract pins the rules that make Step 4 nearly
mechanical. It explicitly forecloses scope creep into
adjacent territories (in-process TLS, mTLS, enterprise
identity stack, packaging ecosystem, service supervisor,
observability stack, web UI, multi-tenant identity).

### 1.2 — What this contract does

- Carries forward Track H Step 3 contract §13.1 / §13.2
  / §13.3 byte-identical (no weakening).
- Promotes Track H §13.2's one-sentence bind-host SHOULD
  guidance into a per-scenario MUST / SHOULD / MAY
  matrix.
- States explicitly the Forwarded-header policy
  (listener **MUST NOT** consume `X-Forwarded-*` /
  `Forwarded` / `X-Real-IP` for any access-control
  purpose). This is observable today; this contract
  pins it as an invariant Step 4 inherits.
- Pins the `/healthz` decision = **defer**.
- Pins the `0.0.0.0` warning decision = **PATH A
  document, not PATH B ship**.
- Pins the final Step 4 PATH = **PATH A (docs-only)**.
- Pins Step 4's exact allowed file surface.
- Pins the Step 4 verification protocol.

### 1.3 — What this contract does NOT do

- **MUST NOT** rewrite any production code.
- **MUST NOT** add or change MCP tools.
- **MUST NOT** change registries (`read = 15 / write =
  25 / intelligence = 16` invariant).
- **MUST NOT** change `pyproject.toml`.
- **MUST NOT** change `scripts/*`.
- **MUST NOT** change `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `CHANGELOG.md`, `README.md`, `PROJECT-STATUS.md`,
  `examples/*`. Those are Step 5 alignment territory.
- **MUST NOT** rewrite Track H Step 3 contract or any
  earlier-track contract. Where this document
  references them, it does so by citation.
- **MUST NOT** redesign Track G stdio transport.
  Track G threat model preserved byte-identical.
- **MUST NOT** redesign Track H HTTP transport, auth
  scheme, or error envelopes. Track H runtime preserved
  byte-identical (PATH A).
- **MUST NOT** introduce in-process TLS, mTLS, JWT,
  OAuth, OIDC, SAML, SCIM, RBAC, ABAC, per-tool ACL,
  per-tenant isolation, rate limiting, WAF, IDS, DDoS
  protection, supervisor daemon / systemd unit /
  Windows Service / hot reload, web UI, observability
  stack, packaging ecosystem (`.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI / wheel
  publication beyond `[project.scripts]`), standalone
  `apps/platform` entrypoint, multi-version 1С matrix
  expansion, rollback whitelist expansion, AST work,
  or any 1cv8 work.
- **MUST NOT** make a SemVer decision. The bump (if
  any) is Step 6 / Q7 territory; default expectation
  per Step 1 plan §14 is PATCH `0.5.1 → 0.5.2`.
- **MUST NOT** push to a remote. Remote push is operator
  action and is not part of any Track J step.

---

## 2. Relationship to Step 1 plan and Step 2 audit

### 2.1 — Layer roles

| Step | Role | Output |
|---|---|---|
| Step 1 | Direction-setter | Plan + step-map; opens the track and pins scope/openness boundaries. |
| Step 2 | Descriptive baseline | Audit document; states what already exists, what is missing, and directional Q1–Q6 resolutions. |
| **Step 3 (this doc)** | **Normative layer** | **Contract; promotes Step 2 directional findings into MUST / SHOULD / MAY rules and pins Step 4 PATH.** |
| Step 4 | Implementation or docs-only operationalization | Per the PATH this contract pins: **one operator-facing deployment-boundary recipe document**. |
| Step 5 | Operator / security / release alignment | Edits SECURITY.md / release-handoff.md / apps/platform/README.md / manuals / README.md / PROJECT-STATUS.md / CHANGELOG.md to point at the Step 4 deliverable. |
| Step 6 | Closure | Final integration pass; SemVer bump (if any); track closure language. |

### 2.2 — Re-litigation rule

This contract **MUST NOT** relitigate Step 2 evidence
without new contradictory facts. Step 2's audit
methodology — full read of `_network_transport.py` /
`_stdio_transport.py` / one `__main__.py` / SECURITY.md
/ release-handoff.md / Track H §10/§13; whole-repo grep
for `X-Forwarded-*` / `Forwarded` / `X-Real-IP` /
`client_ip` / `peer_ip`; manuals grep — produced the
findings this contract consumes. Step 3 drafting did
not surface contradictory evidence. Therefore Step 3
**MUST** consume Step 2 findings as load-bearing.

### 2.3 — Carried-forward invariants from earlier tracks

The following are **not** Track J's to change; this
contract preserves them by reference:

- **Track G / Step 4** — stdio transport runtime
  (`_stdio_transport.py`); CLI flag set on stdio path;
  Track G threat model (trusted local subprocess; no
  auth; line-delimited JSON-RPC 2.0 over stdin/stdout).
- **Track H / Step 3 contract §10** — `--bind` flag
  rules (no default; required-when-http; `socket.gethostbyname`
  validation; port-range gate; fail-closed startup);
  `--auth-token-env` flag rules; CLI-vs-config
  precedence (CLI wins, replace not merge).
- **Track H / Step 3 contract §13** — TLS posture
  (in-process TLS forbidden; operator-owned reverse-
  proxy deployment model; mTLS out-of-scope).
- **Track H / Step 3 contract §6 / §8** — bearer auth
  failure-equivalence (401 + `WWW-Authenticate: Bearer
  realm="mcp"` + JSON-RPC `-32001` envelope); single
  ASCII space scheme; case-insensitive `Bearer`;
  `hmac.compare_digest` token compare; multi-
  Authorization → 400 / `-32600`; complete redaction
  discipline.
- **Track H / Step 4 implementation** —
  `ThreadingHTTPServer((bind_host, bind_port), handler_class)`
  binding plain HTTP/1.1; `_MCPHandler` shape; 1 MiB
  body cap; non-`/mcp` 404; non-POST `/mcp` 405 +
  `Allow: POST`; 413 over-cap; 415 wrong content-type;
  startup line `"Starting <server> HTTP transport
  (JSON-RPC 2.0) on <host>:<port> with <N> valid
  token(s)."`.
- **Track I / Step 4 implementation** —
  `installer.py:_config_to_dict` auth round-trip
  preservation. Track J does **not** touch this.

---

## 3. Inherited fixed decisions from Step 2

The following Step 2 directional findings are
**promoted** in this contract from "directional" to
"normative". This section is the bridge from Step 2's
descriptive language to Step 3's MUST/SHOULD/MAY
language.

### 3.1 — Q1 normative resolution

> Track J's normative primary target is
> **reverse-proxy-first deployment-boundary
> formalization**. In-process TLS is **forbidden** (Track
> H §13.1 carry-forward). The hybrid framing —
> reverse-proxy-first now + any in-process TLS question
> deferred to a hypothetical future track outside Track
> J — is the only stance compatible with Track H §13.1.

### 3.2 — Q2 normative resolution

> Step 4 **MUST** be **PATH A (docs-only)**. PATH B
> (narrow ≤15 LOC code) and PATH C (hybrid) are
> rejected by §9 of this contract for the reasons given
> there.

### 3.3 — Q3 normative resolution

> The supported deployment threat model is **trusted
> internal network behind operator-owned reverse
> proxy**. Hostile public internet is **NOT** a
> supported baseline. Multi-tenant identity / zero-trust
> posture / enterprise ingress are **OUT OF SCOPE**.
> See §4 for the full threat-model contract.

### 3.4 — Q4 normative resolution

> The deployment-boundary surfaces Track J formalizes
> are exactly: `--bind` flag and its `_parse_bind`
> validation; `/mcp` POST endpoint shape; TLS
> termination point (operator's reverse proxy only);
> bind-host MUST/SHOULD/MAY tier; reverse-proxy trust
> assumptions; Forwarded-header MUST-NOT-consume
> policy. No other surfaces are in scope.

### 3.5 — Q5 normative resolution

> `/healthz` is **deferred**. Step 4 **MUST NOT** add a
> `/healthz` / `/readyz` / `/livez` endpoint. See §8
> for rationale.

### 3.6 — Q6 normative resolution

> Track J **MUST NOT** ship production code. Track J's
> Step 4 deliverable is exclusively documentation. See
> §9 / §10.

### 3.7 — What about Q7 (SemVer)?

> Step 3 **MUST NOT** decide the SemVer bump. The bump
> is Step 6 closure territory. Default expectation per
> Step 1 plan §14 is PATCH `0.5.1 → 0.5.2`; Step 6 may
> revisit only if Step 4 deliverable somehow ships
> meaningful new external capability — which it
> **MUST NOT** under §9 of this contract. Therefore
> Step 6 SemVer call is constrained to PATCH or
> "no-bump" (the latter only if Step 6 closure is
> entirely doc alignment with no version-relevant
> change).

---

## 4. Deployment threat-model contract

### 4.1 — In-scope environment

The platform's HTTP transport (`--transport http` on
any of the three MCP servers) is supported in
exactly the following deployment shape:

```
[remote MCP client]
       │
       │ TLS (terminated at operator's reverse proxy)
       ▼
[operator-owned reverse proxy: nginx / Caddy /
 Apache / cloud LB]
       │
       │ plain HTTP/1.1 (operator's trusted network
       │   segment: loopback or private subnet)
       ▼
[1C Agent Platform MCP listener bound to
 loopback or private interface, plain HTTP/1.1]
```

This is byte-identical to Track H Step 3 contract §13.2.

### 4.2 — Trusted parties

The following are **trusted** for the purposes of this
contract:

- The operator (the human or automation that runs the
  install fast path, configures `auth.tokens` /
  `--auth-token-env`, and starts the MCP server
  process).
- The operator-owned reverse proxy (nginx / Caddy /
  Apache / cloud LB; or a managed equivalent operated
  by the same organisation).
- MCP clients reaching the listener via the reverse
  proxy with a valid bearer token.
- The trusted network segment between the reverse
  proxy and the listener (the operator is responsible
  for keeping this hop on a trusted internal network —
  loopback if same host; private subnet / VPN if not).

### 4.3 — Untrusted parties

The following are **untrusted**:

- Anyone on the wire upstream of the reverse proxy
  (the proxy's TLS terminates them; transit
  confidentiality is the proxy's responsibility, not
  the listener's).
- Anyone on the wire between the reverse proxy and
  the listener if that hop crosses an untrusted
  segment — operator **MUST** keep that hop trusted.
- Any client lacking a valid bearer token (rejected
  with failure-equivalent 401 per Track H §6 / §8).
- Any client supplying multiple `Authorization`
  headers (rejected with 400 + `-32600` per Track H
  §8.6).

### 4.4 — Out-of-scope environments

The following deployment shapes are **NOT** supported
by this contract and Track J **MUST NOT** claim them:

- Direct exposure of the listener to the public
  internet without a fronting TLS-terminating reverse
  proxy. (The bearer token is wire-readable on plain
  HTTP; passive attackers can capture it.)
- Hostile-internet-grade exposure with adversarial
  clients attempting protocol-level attacks beyond
  the 401/400/404/405/413/415 envelope set Track H
  Step 3 contract enforces.
- Multi-tenant identity (different bearer tokens for
  different tenants with per-tenant ACL).
- Zero-trust posture (per-request continuous
  authentication beyond the static bearer; no mTLS;
  no client identity verification).
- Enterprise ingress (SSO / SAML / OIDC / SCIM /
  federated audit / policy-as-code DSL).
- Hostile-network-aware authentication (token
  rotation endpoint; refresh tokens; session
  cookies).
- Rate limiting / WAF / IDS / DDoS protection — those
  are operator-owned reverse-proxy responsibilities,
  not the listener's.

### 4.5 — Honest summary phrase (normative)

The product after Track H / Track I is precisely:

> A trusted-internal-network HTTP MCP listener with
> static bearer authentication, fronted by an
> operator-owned reverse proxy that terminates TLS.
> Not hostile-internet ready. Not enterprise-identity
> ready. Not multi-tenant. Not load-balanced. Not
> observed. Not supervised.

Track J formalizes the **first half** of this phrase
into an operator-facing recipe (Step 4); Track J
**MUST NOT** change the second half.

---

## 5. Reverse-proxy and TLS-boundary contract

### 5.1 — In-process TLS

Step 4 **MUST NOT** introduce in-process TLS. Specifically,
Step 4 **MUST NOT**:

- import `ssl` beyond what stdlib transitively pulls
  via `http.server` / `socketserver` / `socket`;
- call `ssl.wrap_socket`, instantiate `ssl.SSLContext`,
  load certificates, load private keys, load CA
  bundles;
- add any `--cert-file` / `--key-file` / `--ca-cert` /
  `--client-cert` / `--ssl-mode` flag or any
  equivalent.

This is byte-identical carry-forward of Track H §13.1.

### 5.2 — TLS termination point

TLS termination **MUST** happen at the operator's
reverse proxy. The listener **MUST** bind plain
HTTP/1.1. This is byte-identical carry-forward of
Track H §13.2.

### 5.3 — mTLS

Mutual TLS / client certificate authentication **MUST
NOT** be implemented in any Track J step. Operators
requiring mTLS terminate it at the reverse proxy
layer. This is byte-identical carry-forward of Track
H §13.3.

### 5.4 — Reverse-proxy responsibilities (operator-owned)

The reverse proxy fronting the listener is **operator-
owned** (the operator deploys, configures, operates,
and keeps it patched). Track J's contract assumes the
proxy:

- terminates TLS for upstream clients;
- forwards `POST /mcp` requests to the listener as
  plain HTTP/1.1;
- preserves `Content-Type: application/json` and the
  `Authorization: Bearer <token>` header byte-
  identical (no header rewriting, no token
  re-signing);
- keeps its `proxy_pass` (or equivalent) hop on a
  trusted network segment to the listener;
- **MAY** inject `X-Forwarded-*` / `Forwarded` /
  `X-Real-IP` headers — the listener does not consume
  them (see §6) so operator's choice here is
  cosmetic / log-routing only;
- **SHOULD** enforce its own request-size limit
  consistent with the listener's 1 MiB body cap;
- **SHOULD** enforce its own connection / rate /
  abuse policies (the listener does not).

### 5.5 — App responsibilities (the listener)

The listener is responsible for:

- binding the operator-supplied `--bind HOST:PORT`
  per Track H §10.3 / `_parse_bind` validation;
- enforcing `/mcp` POST-only access at the
  application layer (other paths → 404; other methods
  → 405 + Allow: POST);
- enforcing 1 MiB body cap (over-cap → 413);
- enforcing `application/json` Content-Type (other →
  415);
- enforcing bearer auth with failure-equivalence,
  redaction discipline, and `WWW-Authenticate` header
  per Track H §6 / §8;
- writing diagnostic logs to stderr through the
  configured logger; no token data ever in logs.

The listener is **NOT** responsible for:

- TLS termination;
- IP-based allow-listing;
- per-client rate limiting / quotas;
- per-tenant routing;
- session persistence;
- distributed tracing / metric emission;
- any form of identity beyond the static bearer.

---

## 6. Forwarded-header and trust-consumption contract

### 6.1 — MUST NOT consume rule

The listener **MUST NOT** consume any of the following
HTTP request headers for **any** access-control,
trust, allow-listing, identity, audit, or routing
decision:

- `X-Forwarded-For`
- `X-Forwarded-Proto`
- `X-Forwarded-Host`
- `X-Forwarded-Port`
- `X-Forwarded-Server`
- `X-Real-IP`
- `Forwarded` (RFC 7239)
- `True-Client-IP` (Cloudflare-style)
- `CF-Connecting-IP` (Cloudflare-style)
- Any other proxy-injected client-metadata header.

This is **observable today** in
`packages/mcp-common/src/mcp_common/_network_transport.py`:
zero references in `_MCPHandler` to any of the above.
Step 4 **MUST** preserve this property.

### 6.2 — Diagnostic logging

`_MCPHandler.log_message` writes `address_string()` —
the **TCP peer's connect address** — to the
diagnostic log via the configured logger. When the
listener is fronted by a reverse proxy, that address
is the proxy's address, not the original client's.
Step 4 **MUST NOT** change this.

If an operator wants per-original-client log
correlation, they configure that at the reverse-proxy
layer (proxy-side access logs include both the
upstream client and the proxied request); the
listener does not attempt to recover the original
client address.

### 6.3 — Operator-facing wording

Step 4 (PATH A docs-only) **MUST** include a
single explicit paragraph in the deployment-boundary
recipe stating that the listener does not consume
forwarded headers, with the consequence that:

- IP-based allow-listing **MUST** happen at the
  reverse-proxy layer if needed at all;
- the listener treats every reachable client as
  authenticated iff the bearer token validates,
  regardless of injected client-IP metadata;
- operators **SHOULD NOT** configure
  `set_real_ip_from` / `real_ip_header` / equivalents
  on the assumption that the listener will pick up
  the recovered client IP for any decision (it will
  not).

### 6.4 — Token wire-confidentiality consequence

Because the listener does not enforce TLS itself and
does not recover any out-of-band client identity, the
bearer token is the **sole** authentication signal
reaching the listener. Step 4 (PATH A) **MUST**
state explicitly that the bearer token is wire-
readable on plain HTTP and that operators **MUST**
ensure TLS termination upstream of the listener for
any non-loopback exposure.

---

## 7. Exposure / bind / operator deployment contract

### 7.1 — Per-scenario MUST/SHOULD/MAY matrix

Step 4 (PATH A docs-only) **MUST** publish a
deployment-boundary recipe document that includes
exactly the following per-scenario matrix:

| Scenario | Bind host | Reverse proxy | TLS termination | Token wire-confidentiality |
|---|---|---|---|---|
| **A. Local-only / development on the operator's own machine.** Listener and any client share the same OS host. | `127.0.0.1` or `::1` (loopback) **MUST** | **MAY** be omitted (curl from the same host bypasses any proxy) | n/a (loopback only; no off-host wire) | n/a (loopback only) |
| **B. Trusted private subnet (LAN / VPN / corporate network).** Listener exposed to other hosts on the same trusted segment, with or without a fronting proxy. | Loopback **SHOULD**; private IP **MAY**, only if needed for off-host reach within the trusted segment | **SHOULD** be present if any client is off-host; **MUST** be present if exposing beyond the trusted segment | At the reverse proxy if present; n/a only if all clients reach via loopback | Wire-confidential **only** behind a TLS-terminating proxy; otherwise the bearer token is plain-HTTP-readable to anyone on the segment |
| **C. Public-facing-through-reverse-proxy.** Listener is reachable to off-network clients via the reverse proxy. | Loopback **SHOULD**; private IP **MAY**; **MUST NOT** bind to a public-routable interface directly | **MUST** be present and **MUST** terminate TLS | At the reverse proxy | Wire-confidential at the reverse proxy; plain HTTP between proxy and listener (operator **MUST** keep the hop trusted) |

The matrix above **is the canonical operator-facing
table for the platform**; Step 4 reproduces it in the
deployment-boundary recipe document.

### 7.2 — Public-interface bind without fronting proxy

Step 4 (PATH A) **MUST** state explicitly that
**binding the listener directly to a public-routable
interface (e.g., `0.0.0.0` on a host with a public
IP) without a TLS-terminating reverse proxy is NOT
SUPPORTED**. Specifically:

- the bearer token is wire-readable on plain HTTP and
  a passive on-path attacker captures it;
- the listener has no mitigation for that case (no
  in-process TLS, no client-cert auth, no IP allow-
  list);
- operators who do this are operating outside the
  supported deployment shape.

### 7.3 — `0.0.0.0` runtime warning

This contract **MUST NOT** require Step 4 to add a
runtime warning when `--bind 0.0.0.0:<port>` is
specified. The risk is documented in Step 4's recipe
(per §7.2). Adding a runtime warning is a code change
out of scope for PATH A; deferring it is the chosen
PATH A trade-off and §9 explains why.

### 7.4 — Operator decision points

The deployment-boundary recipe **MUST** answer at
minimum the following operator questions:

1. Where should I bind the listener? (Per scenario,
   per matrix in §7.1.)
2. Do I need a reverse proxy? (Per scenario.)
3. Where does TLS terminate? (Operator's reverse
   proxy; never the listener.)
4. Does the listener trust `X-Forwarded-*`? (No —
   per §6.)
5. What load-balancer health probe shape works? (Any
   non-`/mcp` path returns deterministic 404 without
   requiring a token; no `/healthz` is shipped — per
   §8.)
6. What request-size limit should I set on the
   reverse proxy? (Aligned with listener's 1 MiB body
   cap.)
7. What happens if I don't supply a bearer token?
   (401 + `WWW-Authenticate: Bearer realm="mcp"` +
   JSON-RPC `-32001` envelope.)
8. What happens if I supply a wrong / malformed /
   wrong-scheme token? (Identical 401 — per Track H
   §8.4 failure-equivalence.)

The recipe **MUST** answer these in operator-readable
prose and **MAY** include concrete `nginx` and
`Caddy` configuration snippets (see §10 for allowed
example shapes).

---

## 8. `/healthz` decision

### 8.1 — Decision

Step 4 **MUST NOT** add a `/healthz`, `/readyz`, or
`/livez` HTTP endpoint. The decision is **defer**.

### 8.2 — Rationale

- Any non-`/mcp` path on the listener returns
  deterministic `404 Not Found` (`text/plain;
  charset=utf-8`, body `"Not Found\n"`) **without**
  requiring auth. A "TCP-connectable + HTTP-known-
  status" load-balancer probe (the most common
  health-probe class) can already health-check the
  listener by pointing at any non-`/mcp` URL and
  treating 404 as alive.
- A strict 2xx-only health prober cannot use the
  current behaviour; that is the only operator class
  not covered. Adding a `/healthz` endpoint to
  accommodate that class is **net-new external
  capability** (see Step 1 plan §14: meaningful new
  external capability would warrant MINOR SemVer
  bump). Track J's cost discipline (narrowest honest
  formalization; see Step 1 step-map track-invariants
  block) argues against shipping new external
  capability when the documentation gap is the
  dominant one.
- Adding a `/healthz` endpoint is also code (not
  docs); PATH A excludes code. Including `/healthz`
  would force a re-decision to PATH B/C, which §9 of
  this contract rejects.

### 8.3 — Operator-facing consequence

The Step 4 recipe **MUST** explicitly document the
strict-2xx-only-prober limitation: operators using
load balancers / orchestrators that **only** treat
2xx as alive **MUST** either reconfigure the prober
to accept 4xx as alive (typical override), or front
the listener with a proxy that synthesises a 2xx
response on a dedicated probe path (the reverse
proxy can already do this — `nginx` `location /healthz
{ return 200; }` etc.).

The recipe **MUST NOT** promise a future `/healthz`;
that is not a Track J commitment and may never be
made.

---

## 9. Final Step 4 PATH selection and rationale

### 9.1 — Decision

**Step 4 MUST be PATH A (docs-only).**

PATH B (narrow ≤15 LOC code addition) and PATH C
(hybrid) are **rejected**.

### 9.2 — Why PATH A

The dominant Track J gap is **operator-facing
deployment-boundary documentation**, not runtime
behaviour. Step 2 audit established:

- `_parse_bind` already enforces HOST:PORT shape +
  range + `socket.gethostbyname` validation;
- no default `--bind` exists (deliberate, per Track H
  §10.3);
- `_MCPHandler` already enforces single-`/mcp`-POST,
  1 MiB cap, bearer auth with failure-equivalence
  and redaction discipline, deterministic 404 on
  non-`/mcp`;
- `_serve_http` uses `ThreadingHTTPServer` plain
  HTTP/1.1 with zero `ssl` imports beyond stdlib's
  indirect pulls;
- whole-repo grep confirmed zero consumption of
  `X-Forwarded-*` / `Forwarded` / `X-Real-IP` /
  `client_ip` / `peer_ip` for access-control
  purposes;
- in-process TLS is and remains forbidden per Track
  H §13.1.

Step 4 (PATH A) operationalizes this by writing a
single operator-facing deployment-boundary recipe
document. It does not mutate runtime.

### 9.3 — Why not PATH B

PATH B would have shipped a narrow ≤15 LOC code
addition in `_network_transport.py` — typically a
runtime warning when `--bind 0.0.0.0:<port>` is
specified, or a `/healthz` endpoint.

This contract rejects PATH B because:

- the `0.0.0.0` warning is **fully documentable** in
  PATH A prose without a code change. The risk is
  not behavioural-novel; it is operator-policy
  framing of the same plain-HTTP listener Track H
  §13.2 already pinned. Adding a runtime warning is
  a nice-to-have, not a correctness gap.
- the `/healthz` endpoint is **net-new external
  capability** that would force the SemVer bump
  question into MINOR territory (per Step 1 plan
  §14). It is rejected by §8 of this contract.
- any other ≤15 LOC change would either be cosmetic
  (a log line phrasing tweak — out of scope for
  Track J's deployment-boundary mandate) or material
  (and out of PATH A's narrow remit).
- shipping code in Track J widens the verification
  surface unnecessarily: PATH A verification is
  doc-consistency; PATH B verification adds runtime
  proof.

### 9.4 — Why not PATH C

PATH C (hybrid: PATH A + a tiny code change) inherits
PATH B's rejection rationale and adds no value:
the deployment-boundary recipe is already complete
without the runtime warning, so the code addition
would be redundant relative to documentation.

### 9.5 — Reversibility

Future tracks (post-Track-J) **MAY** revisit
`/healthz` or a `0.0.0.0` warning if operator-facing
demand surfaces. That is a separate-track decision
with its own scope, plan, audit, contract,
implementation, alignment, and closure. Track J
**MUST NOT** preempt it.

---

## 10. Exact Step 4 implementation surface

### 10.1 — Allowed file surface for Step 4

Step 4 **MUST** ship exactly one new file:

- `docs/operators/deployment-boundary.md` (default
  filename; Step 4 **MAY** finalize the exact
  filename / location at Step 4 opening, but the
  file **MUST** be a single new operator-facing
  document and **MUST** live under `docs/`).

Step 4 **MUST NOT** modify any other file. This is a
single-file PATH A closure.

### 10.2 — Forbidden file surface for Step 4

Step 4 **MUST NOT** modify or create:

- any file under `apps/*/src/`,
  `packages/*/src/` (no production code);
- `pyproject.toml` (no SemVer bump in Step 4; that's
  Step 6);
- `scripts/*` (release/dev wrappers);
- `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `CHANGELOG.md`,
  `README.md`, `PROJECT-STATUS.md`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md` — those are Step 5
  alignment territory;
- `examples/*`;
- `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-plan.md`,
  `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-step-map.md`,
  `docs/architecture/track-j-deployment-boundary-baseline-audit.md`,
  this contract (Step 1 / 2 / 3 deliverables —
  finalized; Step 4 cites them but **MUST NOT**
  modify them);
- any new MCP tool / new registry entry / new tool
  module.

### 10.3 — Required content of the Step 4 deliverable

The Step 4 deliverable file **MUST** include at
minimum the following sections (Step 4 **MAY**
choose section numbering and headings):

1. **Purpose / audience** — operator-facing recipe;
   not an architecture document.
2. **Threat model summary** — restate §4 of this
   contract in operator-readable prose.
3. **Per-scenario matrix** — reproduce the §7.1
   table.
4. **Per-scenario walkthroughs** — for each of the
   three scenarios (A/B/C in the matrix), one short
   prose section explaining bind, reverse proxy,
   TLS, token wire-confidentiality.
5. **Forwarded-header policy** — restate §6 in
   operator-readable prose.
6. **`/healthz` non-shipping** — restate §8.3
   operator-facing consequence.
7. **Concrete reverse-proxy snippets** — at least
   one `nginx` and one `Caddy` example, abstract
   placeholders only (no real hostnames, no real
   tokens, no real env-var values, no real
   certificates). Step 4 **MAY** add `Apache` or
   cloud-LB examples but **MUST NOT** ship more
   than three concrete proxy examples (cost-
   discipline cap).
8. **Operator decision-point Q&A** — at minimum
   the eight questions in §7.4.
9. **Cross-references** — link to Track H Step 3
   contract §10 / §13, to SECURITY.md, to
   `docs/release-handoff.md`, to this contract.
   The Step 4 deliverable does **not** rewrite
   those documents; it points at them.
10. **Honest non-goals** — restate §4.4 of this
    contract in operator-readable prose, so the
    reader knows what the document is **not**
    promising.

### 10.4 — Forbidden content of the Step 4 deliverable

The Step 4 deliverable file **MUST NOT** contain:

- any real bearer token, real env-var value, real
  reverse-proxy hostname, real TLS certificate
  fragment, real internal IP, real DNS name —
  examples are abstract or omitted;
- any claim of enterprise-readiness / hostile-
  internet-readiness / multi-tenant-readiness /
  zero-trust-readiness / "deployment solved" /
  "production-ready for arbitrary deployment";
- any forward-looking promise about `/healthz`,
  in-process TLS, mTLS, or any out-of-scope
  capability — those remain explicitly deferred and
  **MUST NOT** be characterized as "coming soon" or
  "future Track J work";
- any new MUST / MUST NOT rule the Step 4 author
  invents on their own. Step 4 is operationalization,
  not normative re-design. If a new rule needs to be
  pinned, the Step 4 author **MUST** stop and
  surface it as a Step 3 contract amendment, not
  ship it directly.

### 10.5 — Length and tone

Step 4 deliverable **SHOULD** be operator-readable
prose, ≤ 1500 lines (cost-discipline soft cap).
Step 4 **MUST NOT** drift into architecture-document
abstraction; this is a recipe, not a contract.

---

## 11. Backward compatibility statement

### 11.1 — Track G stdio baseline

`packages/mcp-common/src/mcp_common/_stdio_transport.py`
is preserved byte-identical from Track G / Step 4
forward through Track J / Step 4 / Step 5 / Step 6.
Step 4 **MUST NOT** touch this file.

### 11.2 — Track H HTTP baseline

`packages/mcp-common/src/mcp_common/_network_transport.py`
is preserved byte-identical from Track H / Step 4 /
Track I / Step 4 forward through Track J / Step 4 /
Step 5 / Step 6. Step 4 **MUST NOT** touch this file.
This is the §10.2 forbidden-surface rule restated as
an invariant.

### 11.3 — Track I installer baseline

`apps/platform/src/onec_platform/installer.py`
auth round-trip preservation (Track I / Step 4) is
preserved unchanged. Step 4 **MUST NOT** touch this
file.

### 11.4 — Registries

Registry counts **MUST** remain `read = 15 / write =
25 / intelligence = 16` through Track J / Step 4 /
Step 5 / Step 6. Step 4 **MUST NOT** add or remove
any MCP tool. The selfcheck at every step **MUST**
confirm `selfcheck_status=ok` and the three-count
invariant.

### 11.5 — `pyproject.toml`

`pyproject.toml` **MUST** remain `version = 0.5.1`
through Step 3 (this commit), Step 4, Step 5. Step 6
**MAY** bump per Q7 default (PATCH `0.5.1 → 0.5.2`)
or hold at `0.5.1` if Step 6 is purely closure-doc
alignment with no version-relevant change. Step 6
**MUST NOT** bump MINOR or MAJOR — see §3.7.

### 11.6 — No secret-management / hostile-network claims

Track J at no step **MUST NOT** characterize the
platform as "secrets-managed", "vault-backed",
"KMS-integrated", "hostile-internet-ready",
"enterprise-ingress-ready", "zero-trust-ready", or
similar. The supported deployment shape is exactly
§4.1 / §7.1; Step 4 / Step 5 / Step 6 deliverables
**MUST NOT** weaken this.

---

## 12. Verification contract for Step 4

Step 4's commit **MUST** demonstrate the following at
the time of commit:

### 12.1 — Scope checks

1. Working tree contains exactly one expected new
   file (the Step 4 deliverable).
2. No other file is modified.
3. Production code untouched (`apps/*/src/`,
   `packages/*/src/`).
4. `pyproject.toml` untouched (`version = 0.5.1`
   preserved).
5. `scripts/*` untouched.
6. `SECURITY.md` / `docs/release-handoff.md` /
   `apps/platform/README.md` / `CHANGELOG.md` /
   `README.md` / `PROJECT-STATUS.md` / manuals /
   `examples/*` untouched.

### 12.2 — Registry / selfcheck checks

7. `selfcheck_status=ok`.
8. Registries `read = 15 / write = 25 /
   intelligence = 16` confirmed unchanged.

### 12.3 — Release-verify check

9. `verify-release.ps1 -AllowDirtyTree` GREEN on all
   eight checks (Repo layout / Release entrypoints /
   Important docs / Working tree (1 uncommitted
   accepted) / Git baseline / Selfcheck / Credential
   leak guard / Credential template hygiene).

### 12.4 — Honesty checks

10. No `1cv8.exe` runs in Step 4.
11. No real credentials in committed text (no real
    tokens, env-var values, hostnames, certificate
    fragments). Verified by manual review of the
    deliverable.
12. No premature Track-J closure language. Verified
    by grep on `Track J.*(закрыт|completed|shipped
    production|implemented in Step 4|merged|
    finalized|GA-ready|production-ready|enterprise-
    ready|deployment solved)` returning zero
    matches against the Step 4 deliverable.
13. No false implementation claims. Verified by
    grep on `now ships|now supports|now provides|
    new MCP tool|new flag|new endpoint|new
    capability` against the Step 4 deliverable; any
    match must reflect Track H / Track I existing
    capability being **re-stated**, not Track J
    inventing it.
14. No fake "deployment solved" / "enterprise-ready
    ingress" / "hostile-network-ready" framing.
    Verified by grep on `enterprise-ready|hostile-
    network-ready|zero-trust-ready|deployment
    solved|production-ready|battle-tested`.

### 12.5 — Doc-consistency checks (PATH A specific)

15. The Step 4 deliverable's per-scenario matrix is
    byte-identical to §7.1 of this contract (the
    canonical table).
16. The Step 4 deliverable's Forwarded-header
    section is consistent with §6 of this
    contract.
17. The Step 4 deliverable's `/healthz` paragraph
    is consistent with §8 of this contract.
18. The Step 4 deliverable's threat-model summary
    is consistent with §4 of this contract and
    Track H §13.

### 12.6 — Verification verdict

If checks 1–18 are GREEN, Step 4 closes. If any
check fails, Step 4 **MUST NOT** be committed; the
author **MUST** fix the deliverable and re-verify.

---

## 13. Honest non-goals (carry-forward, restated)

This contract restates the Track J non-goals so they
are MUST-NOT-do for Step 4 / Step 5 / Step 6:

- **MUST NOT** introduce in-process TLS / HTTPS
  termination (Track H §13.1 carry-forward).
- **MUST NOT** introduce mTLS / client certificate
  authentication (Track H §13.3 carry-forward).
- **MUST NOT** introduce JWT / OAuth 2.0 / OIDC /
  SAML / SCIM / federation.
- **MUST NOT** introduce RBAC / ABAC / per-tool ACL
  / per-tenant isolation / multi-tenant identity.
- **MUST NOT** introduce token rotation endpoint /
  refresh tokens / session cookies.
- **MUST NOT** introduce rate limiting / WAF / IDS
  / DDoS protection / anomaly detection.
- **MUST NOT** introduce supervisor daemon / systemd
  unit / Windows Service registration / launchd /
  hot reload / restart watcher / auto-update.
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
- **MUST NOT** introduce a standalone `apps/platform`
  entrypoint (Tracks G / H / I carry-forward).
- **MUST NOT** introduce `/healthz` / `/readyz` /
  `/livez` endpoints (this contract §8).
- **MUST NOT** introduce a `0.0.0.0` runtime warning
  (this contract §7.3).
- **MUST NOT** add new MCP tools or change registries
  (this contract §11.4).
- **MUST NOT** add to `pyproject.toml` outside Step 6
  Q7 SemVer bump (PATCH or none).
- **MUST NOT** run `1cv8.exe` (Track J operates on
  network/deployment-boundary layer; not on 1cv8
  binary surface).
- **MUST NOT** push to a remote (operator action;
  not part of any Track J step).
- **MUST NOT** commit real credentials or real
  hostnames in any deliverable.
- **MUST NOT** rewrite Track G / Track H / Track I
  contracts or runtime.
- **MUST NOT** redesign auth scheme, error envelopes,
  or HTTP method/path policy.
- **MUST NOT** expand multi-version 1С matrix /
  rollback whitelist / AST coverage in any Track J
  step.
- **MUST NOT** make any `1.0.0` / `production-
  ready` / `GA` claim.

---

## 14. Step 4 handoff note

### 14.1 — Step 4 opening ritual

When Step 4 opens, the author **MUST**:

1. Confirm clean working tree (HEAD = the Step 3
   commit).
2. Re-read this contract end-to-end. Step 4 **MUST
   NOT** start drafting before this.
3. Confirm Step 1 plan / Step 2 audit / this contract
   are all citable (Step 4 deliverable references
   them; modifying them is forbidden).
4. Choose final filename within the §10.1 constraint
   (default `docs/operators/deployment-boundary.md`).

### 14.2 — Step 4 output ritual

When Step 4 commits:

1. Subject **MUST** be exactly:
   `Track J / Step 4 — operator-facing deployment-
   boundary recipe`.
2. Body **MUST** include: why one new doc file is
   sufficient; exact file added; what was
   intentionally NOT touched; verification summary
   (per §12); explicit confirmation that no
   registries changed / no new MCP tools /
   no `1cv8.exe` / no remote push / no real
   credentials / PATH A pinned per this contract.
3. Step 5 (operator / security / release alignment)
   is the next opening and **MUST NOT** be opened
   in the same commit.

### 14.3 — Step 4 verification harness

Step 4 author **MUST** run, at minimum:

```
git status --short
.\scripts\release\verify-release.ps1 -AllowDirtyTree
```

…and the eighteen checks listed in §12. If any fail,
Step 4 commit **MUST NOT** be created.

### 14.4 — What Step 4 does NOT do

- Does not edit Step 1 plan / Step 2 audit / this
  contract.
- Does not edit `SECURITY.md` / release-handoff.md
  / apps/platform/README.md / manuals / README.md /
  PROJECT-STATUS.md / CHANGELOG.md (Step 5
  territory).
- Does not bump SemVer (Step 6 territory).
- Does not run `1cv8.exe`.
- Does not push to a remote.
- Does not invent new normative rules.

### 14.5 — Step 5 / Step 6 preview

This contract pins enough to make Step 5 mechanical:

- Step 5 = update SECURITY.md "Honest constraints"
  bullet on transports to point at Step 4
  deliverable; update `docs/release-handoff.md`
  "What is NOT in this handoff" / "Local check /
  launch sequence" to point at Step 4 deliverable;
  update `apps/platform/README.md` Track-H-citation
  paragraphs to point at Step 4 deliverable; update
  `README.md` Active parallel track section /
  Closed parallel tracks list / Track-J-detail
  paragraph; update `PROJECT-STATUS.md` per-step
  closure section template; update `CHANGELOG.md`
  with whichever SemVer bump Step 6 picks.
- Step 6 = final integration pass; SemVer call (per
  §3.7); track-closure narrative (Track J becomes
  the tenth closed post-phase parallel track);
  no production-code changes.

---

## 15. Honest summary

This contract:

- Carries forward Track H §10 / §13 byte-identical
  (no weakening).
- Promotes Step 2 audit's directional Q1–Q6
  resolutions to normative MUST / SHOULD / MAY rules.
- Pins **PATH A (docs-only)** as the final Step 4
  PATH on the basis that the dominant Track J gap is
  documentation, not behaviour, and that PATH B / C
  introduce code that is either redundant relative
  to documentation or constitutes net-new external
  capability that Track J should not ship.
- Pins the §7.1 per-scenario matrix as the canonical
  operator-facing deployment table.
- Pins the §6 Forwarded-header MUST-NOT-consume
  policy as an invariant Step 4 inherits.
- Defers `/healthz`. Defers a `0.0.0.0` runtime
  warning. Both deferrals are explicit, not silent.
- Constrains Step 4's allowed file surface to one
  new operator-facing document under `docs/`.
- Constrains Step 4's verification harness to 18
  concrete checks across scope, selfcheck, release-
  verify, and honesty.
- Forbids any maturity / hostile-network /
  enterprise framing in Step 4 / Step 5 / Step 6.
- Forbids SemVer pre-commit (Step 6 / Q7 territory;
  default expectation is PATCH or none).
- Forbids code changes, registry changes, new MCP
  tools, `1cv8.exe` runs, real credentials, and
  remote push at every Track J step.

Step 3 is therefore closeable as a single normative
contract document, with **Track J / Step 4 —
operator-facing deployment-boundary recipe (PATH A,
docs-only)** as the next opening.
