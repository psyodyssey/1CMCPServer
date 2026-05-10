# Operator-Facing Deployment-Boundary Recipe

> **Audience.** Operators who run the 1C Agent Platform's
> three MCP servers (`mcp-read-server`, `mcp-write-server`,
> `mcp-intelligence-server`) on `--transport http` and need
> a single practical recipe for deploying them safely.
>
> **What this document is.** A practical recipe — not a
> contract, not an architecture document, not a security
> policy. The normative source-of-truth for everything
> below is the Track J Step 3 contract
> (`docs/architecture/track-j-deployment-boundary-contract.md`)
> and Track H Step 3 contract §10 / §13. This document
> operationalizes them for an operator who needs to bring
> the platform up correctly.
>
> **What this document is NOT.** It is not a deployment
> automation cookbook, an enterprise-readiness statement,
> a hostile-internet hardening guide, a multi-tenant
> integration spec, or a TLS-in-process recipe. The
> platform does **not** support those shapes; this document
> documents the shapes it **does** support.

---

## 1. Purpose

You are reading this because you have built or received
the 1C Agent Platform (project version `0.5.1` as of
this document) and you need to run one or more of its
three MCP servers on `--transport http`. The Track H
runtime and Track J Step 3 contract together define a
narrow, honest deployment shape — **trusted internal
network behind an operator-owned reverse proxy that
terminates TLS** — and you need to wire this up
correctly.

This document answers, in order:

- where TLS terminates;
- what bind / exposure patterns are acceptable;
- what is trusted vs untrusted;
- what the reverse proxy does vs what the MCP process
  does;
- what is explicitly not supported;
- what concrete deployment shapes are reasonable.

If you are looking for stdio-only operation
(`--transport stdio`), this recipe does not apply — stdio
is a trusted-local-subprocess channel with no listener
and no deployment boundary. See Track G Step 4 / Track G
contract for stdio.

---

## 2. Threat-model summary

### 2.1 — In-scope environment

The HTTP transport (`--transport http` on any of the
three MCP servers) is supported in exactly this shape:

```
[remote MCP client]
       │
       │ TLS (terminated at operator's reverse proxy)
       ▼
[operator-owned reverse proxy: nginx / Caddy /
 Apache / cloud load balancer]
       │
       │ plain HTTP/1.1 (operator's trusted network
       │   segment: loopback or private subnet)
       ▼
[1C Agent Platform MCP listener bound to
 loopback or private interface, plain HTTP/1.1]
```

Restated as plain English: TLS lives at the reverse
proxy. The hop from the reverse proxy to the listener is
plain HTTP/1.1 over a trusted network segment. The
listener itself never speaks TLS.

### 2.2 — Trusted parties

For the purposes of this recipe:

- **You, the operator.** You configure
  `auth.tokens` / `--auth-token-env`, start the MCP
  server, and operate the reverse proxy.
- **The reverse proxy you own.** nginx / Caddy / Apache
  / cloud LB / managed equivalent — the platform
  treats it as part of your trust boundary because
  you operate it.
- **MCP clients reaching the listener via the reverse
  proxy with a valid bearer token.** They are trusted
  iff they validate; the proxy is what gates wire-level
  access.
- **The trusted network segment between the proxy and
  the listener.** Loopback if same host; private subnet
  / VPN if not. You are responsible for keeping this
  hop trusted.

### 2.3 — Untrusted parties

- Anyone on the wire upstream of the reverse proxy —
  the proxy's TLS terminates them; transit
  confidentiality is the proxy's job, not the
  listener's.
- Anyone on the wire between the reverse proxy and the
  listener if that hop somehow crosses an untrusted
  segment (you must keep it trusted).
- Any client without a valid bearer token (rejected with
  failure-equivalent 401).
- Any client supplying multiple `Authorization` headers
  (rejected with 400).

### 2.4 — Out-of-scope (NOT supported)

The platform does **NOT** support these deployment
shapes; do not deploy this way:

- **Direct exposure of the listener to the public
  internet without a fronting TLS-terminating reverse
  proxy.** The bearer token is wire-readable on plain
  HTTP and a passive on-path attacker captures it.
  There is no in-process TLS, no client-cert auth, no
  IP allow-list mitigation.
- **Hostile-internet-grade adversarial exposure.** The
  listener handles 401 / 400 / 404 / 405 / 413 / 415
  cleanly per Track H Step 3 contract, but it is not
  designed for sustained protocol-level attack.
- **Multi-tenant identity.** One bearer-token list per
  process; no per-tenant ACL.
- **Zero-trust posture.** No mTLS, no continuous
  authentication, no per-request client identity
  verification beyond the static bearer.
- **Enterprise ingress** (SSO / SAML / OIDC / SCIM /
  federated audit / policy-as-code DSL). Not shipped.
- **Token rotation endpoint / refresh tokens / session
  cookies.** Not shipped.
- **Rate limiting / WAF / IDS / DDoS protection.** That
  is your reverse proxy's job, not the listener's.
- **Service supervision** (systemd / Windows Service /
  hot reload / restart watcher / auto-update). Not
  shipped.

### 2.5 — Honest summary phrase

> A trusted-internal-network HTTP MCP listener with
> static bearer authentication, fronted by an operator-
> owned reverse proxy that terminates TLS. Not
> hostile-internet ready. Not enterprise-identity ready.
> Not multi-tenant. Not load-balanced. Not observed.
> Not supervised.

This is the shape this document operationalizes. It
does not change any of the second-half "not"s.

---

## 3. Per-scenario deployment matrix

This is the canonical operator-facing decision table.
Use it to find your scenario and read the row.

| Scenario | Bind host | Reverse proxy | TLS termination | Token wire-confidentiality |
|---|---|---|---|---|
| **A. Local-only / development on your own machine.** Listener and any client share the same OS host. | `127.0.0.1` or `::1` (loopback) **MUST** | **MAY** be omitted (curl from the same host bypasses any proxy) | n/a (loopback only; no off-host wire) | n/a (loopback only) |
| **B. Trusted private subnet (LAN / VPN / corporate network).** Listener exposed to other hosts on the same trusted segment, with or without a fronting proxy. | Loopback **SHOULD**; private IP **MAY**, only if needed for off-host reach within the trusted segment | **SHOULD** be present if any client is off-host; **MUST** be present if exposing beyond the trusted segment | At the reverse proxy if present; n/a only if all clients reach via loopback | Wire-confidential **only** behind a TLS-terminating proxy; otherwise the bearer token is plain-HTTP-readable to anyone on the segment |
| **C. Public-facing-through-reverse-proxy.** Listener is reachable to off-network clients via the reverse proxy. | Loopback **SHOULD**; private IP **MAY**; **MUST NOT** bind to a public-routable interface directly | **MUST** be present and **MUST** terminate TLS | At the reverse proxy | Wire-confidential at the reverse proxy; plain HTTP between proxy and listener (you **MUST** keep the hop trusted) |

If your situation does not fit one of A / B / C cleanly,
you are likely in territory the platform does not
support — re-read §2.4 and choose a different deployment
shape, or fall back to scenario A.

A note on **public-routable bind without a fronting
TLS proxy**: if the listener binds directly to
`0.0.0.0` (or any interface that is reachable from a
network you do not fully trust) without a TLS-
terminating reverse proxy in front of it, the bearer
token is wire-readable and a passive on-path attacker
captures it. The listener has no mitigation. **This is
NOT SUPPORTED**; do not do this.

---

## 4. Per-scenario walkthroughs

These walkthroughs are practical, not exhaustive. They
walk you through how to think about each scenario; they
do not script the deployment for you.

### 4.1 — Scenario A: local-only / development

**When this applies.** You are on your own machine
exploring the platform, running `curl` from the same
host, or wiring up a local MCP client that runs as a
sibling process.

**What to do.**

- Start the server with
  `python -m mcp_read_server --transport http
  --bind 127.0.0.1:<port> --auth-token-env <VARNAME>`
  (substitute the appropriate server module and a
  variable name you have populated with a token in
  your shell environment).
- Use a high non-privileged port number you choose;
  there is no default and no recommended specific
  number — pick something you know is free on your
  host.
- No reverse proxy is required; same-host clients
  reach the listener directly via loopback.
- TLS is not relevant — there is no off-host wire.

**What to avoid.**

- Do not use `0.0.0.0` here just to "make it
  reachable from another VM"; that is scenario B or C
  and demands a reverse proxy.
- Do not commit your token environment variable
  value to a file under version control; the platform
  enforces `${ENV:NAME}` substitution and the
  `verify-release.ps1` credential leak guard is your
  safety net, but the human discipline is yours.

### 4.2 — Scenario B: trusted private subnet

**When this applies.** Listener and clients are on the
same trusted network (LAN, VPN, corporate intranet),
and the listener needs to be reachable to other hosts
on that segment.

**What to do.**

- Two viable shapes, depending on whether you front the
  listener with a reverse proxy on the trusted segment:
  - **B1 — proxy-fronted.** Bind the listener to
    loopback; run a reverse proxy (operator-owned, on
    the same host or a sibling host on the trusted
    segment) that terminates TLS for other-host
    clients and forwards plain HTTP/1.1 to the
    listener. This is the recommended shape.
  - **B2 — proxy-omitted.** Bind the listener to a
    private IP on the trusted segment. Other-host
    clients reach the listener via plain HTTP/1.1.
    The bearer token is plain-HTTP-readable to
    anyone on the segment; this is acceptable
    **only** if you fully trust everyone with
    layer-2/3 access to that segment.
- In both shapes, the network segment between the
  listener and any reverse proxy / client must remain
  trusted.

**What to avoid.**

- Do not bind to `0.0.0.0` and assume the segment
  reach is "private enough" — be explicit about
  the bind interface.
- Do not configure your reverse proxy to use
  `set_real_ip_from` / `real_ip_header` / equivalent
  with the expectation that the listener will pick up
  the recovered client IP for any trust decision; it
  will not (see §5).

### 4.3 — Scenario C: public-facing-through-reverse-proxy

**When this applies.** External (off-network) clients
must reach the listener through a reverse proxy you
operate.

**What to do.**

- Bind the listener to **loopback** (preferred) or a
  private IP. Never bind directly to a public-routable
  interface.
- Run an operator-owned reverse proxy on the same host
  or a host that has a trusted hop to the listener.
- Configure the reverse proxy to terminate TLS for
  upstream clients and forward `POST /mcp` requests as
  plain HTTP/1.1 to the listener.
- The reverse proxy preserves `Content-Type:
  application/json` and `Authorization: Bearer
  <token>` byte-identical (no header rewriting, no
  token re-signing).
- Keep the proxy → listener hop on a trusted network
  segment.

**What to avoid.**

- Do not bind the listener to a public-routable
  interface "for convenience" while also running a
  reverse proxy in front of it; this exposes a parallel
  plain-HTTP path that bypasses your TLS. Bind to
  loopback or private IP only.
- Do not assume your CDN / cloud LB's "request
  inspection" / "WAF" features compensate for the
  listener's lack of in-process TLS. The listener is
  plain HTTP; your proxy / LB does the TLS, and the
  hop between them must be trusted.

---

## 5. Forwarded-header policy

The listener does **not** consume any of the following
HTTP request headers for **any** access-control, trust,
allow-listing, identity, audit, or routing decision:

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

Practical consequences for you, the operator:

- **IP-based allow-listing must happen at the reverse-
  proxy layer** if you want it. The listener has no
  IP allow-list and will not gain one as part of
  Track J.
- **The listener treats every reachable client as
  authenticated iff the bearer token validates**,
  regardless of any injected client-IP metadata.
- **Do not configure** `set_real_ip_from` /
  `real_ip_header` / equivalents on the assumption
  that the listener will pick up the recovered client
  IP for any decision. It will not. Such configuration
  is harmless but pointless from the listener's
  perspective.
- The listener's diagnostic log line records the **TCP
  peer's connect address** (i.e., the reverse proxy's
  address when proxied), not the original client. If
  you need per-original-client log correlation,
  configure that at the reverse-proxy layer (proxy
  access logs typically include both the upstream
  client and the proxied request).

The bearer token is the **sole** authentication signal
reaching the listener. Because the listener does not
enforce TLS itself, the token is wire-readable on
plain HTTP — you **must** ensure TLS termination
upstream of the listener for any non-loopback
exposure (scenarios B1 and C).

---

## 6. `/healthz` non-shipping

The platform does **not** ship a `/healthz`, `/readyz`,
or `/livez` HTTP endpoint. There is no plan to ship one
as part of Track J.

What this means in practice:

- **TCP-connectable + HTTP-known-status** load-balancer
  probes work today. Point your probe at any non-`/mcp`
  URL — the listener returns deterministic `404 Not
  Found` (`text/plain; charset=utf-8`, body `"Not
  Found\n"`) without requiring auth. Configure the
  probe to treat 404 as alive. This covers the most
  common health-probe class.
- **Strict 2xx-only health probers** cannot use this.
  You have two practical workarounds:
  - reconfigure the probe to accept 4xx as alive
    (typical override on most LB platforms);
  - have the reverse proxy synthesise a 2xx response
    on a dedicated probe path. nginx supports this
    natively (`location /healthz { return 200; }`)
    and Caddy / Apache equivalents are similarly
    short.

This document does **not** promise a future `/healthz`
endpoint. That is not a Track J commitment, and the
project may never ship one. Plan around the current
behaviour, not around an aspirational endpoint.

---

## 7. Concrete reverse-proxy snippets

The two snippets below are **illustrative**, not
production-grade. They show the minimum shape for the
proxy → listener hop and use only abstract placeholders.
Do not paste them into a production reverse proxy
without auditing them against your own deployment
constraints (TLS cert source, listen address, ACL,
logging, request-size limits, etc.).

Both snippets assume:

- the listener is bound to loopback at port `<LISTENER_PORT>`
  on the same host as the reverse proxy;
- the reverse proxy terminates TLS for upstream clients;
- the reverse proxy forwards `POST /mcp` byte-identical
  (no header rewriting, no body rewriting);
- the operator has obtained a TLS certificate and a
  private key by their own means (this is out of scope
  for this recipe).

### 7.1 — nginx

```nginx
# 1C Agent Platform MCP listener — proxy_pass example.
# Replace <PUBLIC_HOSTNAME>, <CERT_PATH>, <KEY_PATH>,
# <LISTENER_PORT> with values appropriate to your
# deployment. Bodies up to 1 MiB; align with the
# listener's body cap.
server {
    listen 443 ssl;
    server_name <PUBLIC_HOSTNAME>;

    ssl_certificate     <CERT_PATH>;
    ssl_certificate_key <KEY_PATH>;

    client_max_body_size 1m;

    location /mcp {
        # Listener accepts POST /mcp only; method gating
        # at the proxy is optional but documents intent.
        limit_except POST { deny all; }

        proxy_pass http://127.0.0.1:<LISTENER_PORT>;
        proxy_http_version 1.1;

        # Preserve the request byte-identical at the
        # listener boundary; do NOT rewrite Authorization
        # or Content-Type. proxy_set_header lines below
        # are illustrative for nginx-side correlation
        # only — the listener itself does not consume
        # them.
        proxy_set_header Host             $host;
        proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Reminder: the `X-Forwarded-*` lines above are for
nginx-side log correlation only. The listener does not
consume them (see §5).

### 7.2 — Caddy

```caddy
# 1C Agent Platform MCP listener — Caddy reverse_proxy
# example. Replace <PUBLIC_HOSTNAME> and <LISTENER_PORT>.
# Caddy obtains certificates automatically when its
# managed-TLS prerequisites are met; if you provide your
# own cert, replace the auto-TLS shorthand with explicit
# cert configuration per Caddy's documentation.
<PUBLIC_HOSTNAME> {
    request_body {
        max_size 1MB
    }

    handle /mcp {
        reverse_proxy 127.0.0.1:<LISTENER_PORT> {
            transport http {
                versions 1.1
            }
        }
    }
}
```

### 7.3 — A note on the third snippet

Track J Step 3 contract §10.3 caps the recipe at three
concrete proxy examples. This document ships exactly
two (nginx and Caddy). Apache and cloud-LB equivalents
follow the same shape — terminate TLS, forward `POST
/mcp` byte-identical to a loopback or trusted-private
listener — and are deliberately not reproduced here.
Operators using those proxies adapt the same shape to
their tool's syntax.

---

## 8. Operator decision-point Q&A

These are the eight questions operators most often need
answered when bringing the HTTP transport up. The
answers are byte-faithful to Track J Step 3 contract
§7.4.

**1. Where should I bind the listener?**

Loopback (`127.0.0.1` / `::1`) by default. Per the
matrix in §3:

- scenario A: loopback **MUST**;
- scenario B: loopback **SHOULD**, private IP **MAY** if
  needed for off-host reach within the trusted segment;
- scenario C: loopback **SHOULD**, private IP **MAY**,
  public-routable interface **MUST NOT**.

There is no default `--bind` value. You must specify
one explicitly (this is deliberate; see Track H Step 3
contract §10.3).

**2. Do I need a reverse proxy?**

- Scenario A: optional (loopback-only clients work
  without one).
- Scenario B: **SHOULD** if any client is off-host;
  **MUST** if exposing beyond the trusted segment.
- Scenario C: **MUST**.

**3. Where does TLS terminate?**

At your reverse proxy. Always. Never at the listener.
The listener binds plain HTTP/1.1 by design; in-process
TLS is forbidden by Track H Step 3 contract §13.1.

**4. Does the listener trust `X-Forwarded-*`?**

No. The listener does not consume `X-Forwarded-*` /
`Forwarded` / `X-Real-IP` / similar headers for any
access-control, trust, allow-listing, identity,
audit, or routing decision. See §5.

**5. What load-balancer health probe shape works?**

Any non-`/mcp` path returns deterministic `404 Not
Found` without requiring a token — point your probe at
a path like `/probe` or `/` and accept 404 as alive. A
strict 2xx-only probe needs either a probe-config
override or a reverse-proxy `return 200` on a
synthesized probe path. The listener does not ship
`/healthz`. See §6.

**6. What request-size limit should I set on the
reverse proxy?**

1 MiB (`1m` in nginx, `1MB` in Caddy). The listener
caps bodies at 1 MiB and returns 413 if the proxy
forwards a larger body; aligning the proxy's limit
prevents wasted bytes and gives a cleaner error
surface to clients.

**7. What happens if I don't supply a bearer token?**

`401 Unauthorized` + `WWW-Authenticate: Bearer
realm="mcp"` + JSON-RPC `-32001` envelope. This is
identical to every other auth failure (failure-
equivalence per Track H §8.4). The listener does not
distinguish "missing token" from "wrong token" in its
response; the token value is never logged in any form.

**8. What happens if I supply a wrong / malformed /
wrong-scheme token?**

Same as question 7: identical 401 +
`WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
`-32001`. The scheme match is case-insensitive
(`Bearer` / `bearer` / `BEARER` all accepted); a
multi-`Authorization` request is rejected with `400
Bad Request` + JSON-RPC `-32600` instead. Token
comparison uses `hmac.compare_digest` byte-exact —
no partial-match behaviour, no length leak.

---

## 9. Cross-references

This recipe operationalizes statements made in the
following normative / canonical documents. If anything
in this recipe drifts from them, the source documents
win and the discrepancy is a documentation bug.

- **Track J Step 3 contract** —
  `docs/architecture/track-j-deployment-boundary-contract.md`.
  Pins the per-scenario matrix, the Forwarded-header
  policy, the `/healthz` defer decision, the PATH A
  selection for this step, and the verification harness
  this document was built against.
- **Track J Step 2 audit** —
  `docs/architecture/track-j-deployment-boundary-baseline-audit.md`.
  Describes the runtime baseline this recipe documents.
- **Track J Step 1 plan / step-map** —
  `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-plan.md`,
  `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-step-map.md`.
  Open-track scope and 6-step roadmap.
- **Track H Step 3 contract** —
  `docs/architecture/track-h-network-transport-and-auth-contract.md`.
  Pins `/mcp` POST endpoint shape (§4–§8), `--bind` /
  `--auth-token-env` flag rules (§10.3–§10.6), TLS
  posture (§13.1 in-process TLS forbidden, §13.2
  reverse-proxy deployment model, §13.3 mTLS out-of-
  scope).
- **Project security baseline** — `SECURITY.md`. Honest
  constraints on transports, credentials, and supply-
  chain limitations. Currently asserts the same trusted-
  network-behind-reverse-proxy posture this recipe
  operationalizes; Step 5 of Track J will add a
  cross-link from `SECURITY.md` to this recipe.
- **Release handoff** — `docs/release-handoff.md`. Lists
  what is and is not in the handoff; currently mirrors
  this recipe's threat-model in prose. Step 5 of Track
  J will add a cross-link from `release-handoff.md` to
  this recipe.
- **Product layer surface** — `apps/platform/README.md`.
  Cites Track H §13 in several places. Step 5 of
  Track J will add a cross-link to this recipe.
- **Operator manual / administrator manual / developer
  manual** — `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`. Currently say nothing
  about the deployment boundary; Step 5 of Track J
  will decide whether and how to link this recipe from
  them.

This document does not modify any of the above. Step 5
(operator / security / release alignment) is the next
opening of Track J.

---

## 10. Honest non-goals

For absolute clarity about what this document and the
platform's HTTP transport do **not** promise:

- **No enterprise-ready ingress.** No SSO, SAML, OIDC,
  SCIM, federated identity, multi-tenant identity, or
  policy-as-code DSL. Static bearer only.
- **No hostile-internet readiness.** The listener is
  designed for trusted-internal-network deployment
  behind an operator-owned reverse proxy. Public
  internet exposure without that proxy is not a
  supported baseline.
- **No in-process TLS.** The listener binds plain
  HTTP/1.1. There is no `--cert-file` / `--key-file`
  / `--ca-cert` flag and there will not be one as part
  of Track J.
- **No mTLS / client certificate authentication.** Not
  shipped. Operators requiring mTLS terminate it at
  the reverse-proxy layer; the inner hop remains plain
  bearer.
- **No OAuth 2.0 / OIDC / SAML / JWT / RBAC / ABAC /
  per-tool ACL / per-tenant isolation.** Not shipped.
- **No token rotation endpoint, refresh tokens,
  session cookies.** Not shipped.
- **No rate limiting, WAF, IDS, DDoS protection,
  anomaly detection in the listener.** That is your
  reverse proxy's responsibility.
- **No service supervision** (systemd unit, Windows
  Service registration, launchd, hot reload, restart
  watcher, auto-update). The listener is a foreground
  process you start and stop yourself.
- **No packaging ecosystem solved.** No `.msi`,
  `.deb`, signed distribution, GUI installer, wizard,
  PyPI publication, or wheel publication beyond
  `[project.scripts]`. Local development uses the
  documented PYTHONPATH bootstrap; release operators
  use `scripts/release/install.ps1` to materialize
  product configs.
- **No web UI / dashboard frontend.**
- **No observability stack** (OpenTelemetry, Jaeger,
  Prometheus, OpenMetrics, log aggregation,
  distributed tracing). Diagnostic logs go to stderr;
  whatever your platform does with stderr is up to
  you.
- **No `/healthz` / `/readyz` / `/livez` endpoint.**
  See §6.
- **No `0.0.0.0` runtime warning.** The risk is
  documented here in prose; the listener does not
  emit a runtime warning on `--bind 0.0.0.0:<port>`.
- **No multi-version 1С matrix expansion is part of
  this recipe.** Track E covers that orthogonally.
- **No rollback / AST / re-parse work is part of this
  recipe.** Track F / Track A cover those orthogonally.
- **No deployment is "solved" by this document.** It
  is a recipe for the supported deployment shape. If
  your environment does not fit one of the three
  scenarios in §3, the platform may not be the right
  fit for that environment.

If you find yourself wishing one of the above were
shipped, that is a signal to reconsider whether the
1C Agent Platform is the right tool for your specific
deployment, or to wait for a future track that
explicitly addresses the gap. This recipe is what is
honestly available today.
