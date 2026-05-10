# Parallel Track J — TLS and Reverse-Proxy Deployment Boundary (plan)

> **Companion file:**
> `track-j-tls-and-reverse-proxy-deployment-boundary-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 4 —
> отдельный заход; **может** быть docs-only operationalization,
> либо tiny code-change addition, либо гибрид. Это design-
> question, который Step 1 deliberately оставляет открытым до
> Step 2 audit + Step 3 contract.

---

## 1. Зачем нужен Track J после Track I

После closure'а Track I (Installer Auth Round-Trip Integrity;
commit `d408dd2`, project version `0.5.1`) у проекта есть
два transport baselines (stdio из Track G + HTTP/1.1 `/mcp`
из Track H), static bearer authentication boundary, и
working install fast-path round-trip integrity для auth
section. Honest support statement сейчас:

- stdio = trusted local subprocess boundary;
- http = trusted-network behind operator-owned reverse proxy;
- no in-process TLS;
- no mTLS / JWT / OAuth / OIDC / SAML / RBAC / multi-tenant;
- no rate limiting;
- no service supervision;
- no packaging ecosystem beyond current `[project.scripts]`.

Текущий "trusted-network behind operator-owned reverse
proxy" — это general-policy statement (Track H Step 3
contract §13.1–§13.3 + SECURITY.md "Honest constraints" +
docs/release-handoff.md "Known limitations"), но **не
operator-facing deployment contract**:

- Оператор знает, что он "обязан" поставить reverse proxy
  перед HTTP listener'ом, но точная shape этого контракта
  (которые headers ожидать, какой bind host выбрать, какие
  forwarded-identity assumptions делать) **нигде не
  формализована** — оператор должен догадаться из общей
  логики или прочитать Track H Step 3 contract §13 целиком.
- `--bind` flag в `_network_transport.py` принимает любой
  host/port без warning'а на `0.0.0.0` или другие public-
  facing interfaces; safety здесь только через documentation
  recommendation, не через runtime gate.
- Точная shape "what is and is not safe to expose" не
  записана как single-source-of-truth: SECURITY.md говорит
  "treat as local development service", release-handoff
  говорит "behind reverse proxy", apps/platform/README.md
  говорит "operator's reverse proxy responsibility" — все
  правильно по содержанию, но не дают operator'у concrete
  deployment recipe.
- Нет явной формализации, нужен ли `/healthz` / `/readyz` /
  liveness/readiness endpoint или эта функциональность
  deliberately deferred. Сейчас в коде такого endpoint нет
  (`_MCPHandler` отвечает 404 на anything except `POST /mcp`);
  это design choice, но не documented contract.

Concrete gaps, которые Track J адресует:

1. **No formalized deployment boundary contract** — есть
   general-policy text в трёх разных местах, но нет single
   normative document, который оператор может прочитать
   и получить full deployment recipe.
2. **No explicit bind-host guidance** в operator-facing
   docs — `--bind` flag принимает что угодно, и оператор
   должен сам сообразить, что `127.0.0.1:8765` ≫
   `0.0.0.0:8765` для безопасности. Track H Step 3 contract
   §13.2 имеет "Operator SHOULD bind the listener to a
   loopback or private interface" but это buried в RFC 2119
   contract document, не surfaced operator.
3. **No explicit reverse-proxy header expectations** — какие
   headers Track J listener пропускает / игнорирует /
   полагается на (X-Forwarded-For, X-Real-IP, X-Forwarded-
   Proto, X-Forwarded-Host)? Currently `_MCPHandler` не
   обрабатывает forwarded headers вообще — это design choice
   (auth boundary не depends on client IP), но operator
   должен это знать explicitly.
4. **No explicit exposure-rules statement** для трёх
   stratified deployment scenarios:
   - loopback-only (development, local AI agent client);
   - operator-owned LAN/VPN (small team, trusted network);
   - public-facing through reverse proxy (operator accepts
     adversarial-internet risk).
   Currently все три scenarios "supported" implicitly,
   но без operator-facing contract о trade-offs.
5. **No explicit health/readiness endpoint statement** —
   `/healthz` / `/readyz` / liveness probes требуются
   reverse-proxy / load-balancer / orchestration tooling
   для health checking. Track H Step 3 contract §5.2
   forbids `resources/list` / `prompts/list` / etc. as
   non-MCP-method surface, но НЕ запрещает explicitly
   dedicated health endpoint — это grey zone, который
   Track J обязан решить (either "deferred to future
   track" или "ship narrow `/healthz` GET endpoint").

Track J — отдельный узкий parallel track, который ship'ит
**deployment boundary contract** для существующего HTTP
transport, без изменения transport / auth model:

- ship'ит документированную deployment recipe для
  reverse-proxy-first deployment;
- ship'ит точную bind-host guidance как operator-facing
  rule;
- ship'ит точную reverse-proxy header expectation contract
  (forwarded-identity assumptions);
- ship'ит точные exposure rules для трёх deployment
  scenarios;
- решает grey zone про health/readiness endpoint (либо
  ship'ит narrow endpoint, либо явно defers с rationale);
- **может или не может** включать narrow code change в
  `_network_transport.py` — это design question, который
  Step 2 audit + Step 3 contract решит на основе evidence;
- **не** реализует in-process TLS (это carry-over Track H
  §13.1 forbidden Step 4 baseline);
- **не** делает enterprise identity / OAuth / JWT / RBAC /
  multi-tenant;
- **не** делает service supervisor / systemd / Windows
  Service / hot reload;
- **не** делает packaging ecosystem;
- **не** делает web UI;
- **не** добавляет new MCP tools.

## 2. Стартовая точка (post-Track-I factual baseline)

### 2.1 Existing transport / auth / bind surface (Track G + H output, Track I integrity)

- `packages/mcp-common/src/mcp_common/_stdio_transport.py` —
  Track G stdio transport, byte-identical через Track H/I.
- `packages/mcp-common/src/mcp_common/_network_transport.py`
  (549 LOC) — Track H HTTP/1.1 ThreadingHTTPServer на
  `bind_host:bind_port` (validated через
  `socket.gethostbyname(host)` + port range 1..65535 в
  `_parse_bind`); single endpoint `/mcp`; POST only;
  application/json; 1 MiB body cap; case-insensitive Bearer
  scheme; constant-time token compare; failure-equivalence
  401; complete redaction discipline.
- `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  — Track I round-trip preservation для `auth.tokens`.
- `apps/platform/src/onec_platform/{models.py,loader.py}` —
  `ProductAuthSettings`, `ProductConfig.auth`, `_parse_auth`,
  `_AUTH_ENV_TOKEN_RE`.

### 2.2 Existing TLS / reverse-proxy posture (text only, no code)

Track H Step 3 contract `track-h-network-transport-and-auth-contract.md`
§13 уже задокументировал deployment posture **на уровне
general-policy normative wording**:

- §13.1 — In-process TLS = forbidden:
  > "Step 4 **MUST NOT** terminate TLS in-process. The HTTP
  > listener **MUST** bind plain HTTP/1.1 (no TLS,
  > `ssl.wrap_socket`, `ssl.SSLContext`, certificate loading
  > code, `ssl` module imports beyond what stdlib indirectly
  > pulls)."
- §13.2 — Operator deployment model:
  > "[remote MCP client] ─TLS─→ [reverse proxy: nginx /
  > Caddy / Apache / cloud LB] ─plain HTTP─→ [Track H
  > listener bound to 127.0.0.1]"
  >
  > "Operator SHOULD bind the listener to a loopback or
  > private interface (`127.0.0.1`, `::1`, or private IP)
  > and expose it through the operator's reverse proxy."
- §13.3 — mTLS = explicit out-of-scope (carry-over from
  plan §5.2).

`SECURITY.md` "Honest constraints" l.63-65:
> "Threat model for HTTP = **trusted-network deployment**
> behind an operator-owned reverse proxy that terminates
> TLS. The listener itself binds plain HTTP/1.1; in-process
> TLS is not provided. Operator SHOULD bind the listener
> to a loopback or private interface ..."

`docs/release-handoff.md` "Known limitations" + "What is
NOT in this handoff" repeat the same wording in operator-
facing language.

### 2.3 What is NOT yet on disk (Track J gap inventory)

- **No `docs/operator-deployment-guide.md`** или эквивалент
  single-source-of-truth document с concrete reverse-proxy
  config snippets, bind-host decision tree, exposure-scenario
  matrix.
- **No formal `track-j-...-contract.md`** — нормативный
  contract про deployment boundary не написан (Track H §13
  это про in-process TLS, не про full deployment shape).
- **No bind-host runtime warning** в `_network_transport.py`
  для `0.0.0.0` / public-facing interface (only fail-closed
  on `gethostbyname` failure, не warning на public bind).
- **No `/healthz` / `/readyz` endpoint** в `_MCPHandler`.
  Currently any non-`POST /mcp` request returns 404 plain
  text. Reverse-proxy / load-balancer health-check
  integrations должны полагаться либо на TCP connect, либо
  на rejected `POST /mcp` без auth (returning 401 — which
  is a "live but not authenticated" signal, not a clean
  health probe).
- **No explicit forwarded-header policy** в `_MCPHandler` —
  X-Forwarded-For / X-Real-IP / X-Forwarded-Proto /
  X-Forwarded-Host пропускаются, но не обрабатываются и не
  влияют на auth (auth is bearer-token-only). Это
  правильное поведение для current threat model, но не
  documented as explicit contract.

---

## 3. Цель Track J

Ship'ить **deployment boundary contract** для existing
HTTP MCP transport — formalize "trusted-network behind
operator-owned reverse proxy" general-policy statement в
single-source-of-truth operator-facing deployment recipe
с точными bind-host rules, reverse-proxy integration
contract, exposure scenario matrix, и решение про
health/readiness endpoint.

Что **точно НЕ** входит в Track J — см. §5.

## 4. Что входит в Track J (in scope)

### 4.1 Documentation surface (always)

- `track-j-...-plan.md` (этот документ).
- `track-j-...-step-map.md` (6 шагов).
- Step 2 deliverable:
  `track-j-deployment-boundary-baseline-audit.md` —
  descriptive read-only audit current deployment-related
  surfaces:
  - inventory of existing TLS / reverse-proxy / bind-host
    text in Track H contract / SECURITY / release-handoff
    / apps/platform/README / scripts/dev/* / scripts/release/*;
  - inventory of `_network_transport.py` runtime behaviour
    (bind-host validation, forwarded-header treatment,
    non-`/mcp` 404 response, `WWW-Authenticate` 401);
  - 4-class breakdown (already-formalized / partially-
    documented / clearly-missing / out-of-scope);
  - resolve Q1 (target deployment posture: hybrid =
    reverse-proxy-first default + in-process TLS deferred);
  - resolve Q2 directionally (Step 4 = docs-only OR
    docs-plus-tiny-code based on audit evidence);
  - resolve Q3 (deployment threat model: trusted internal
    network behind reverse proxy, NOT hostile-internet by
    default);
  - resolve Q4 (deployment surfaces enumerated: bind
    host/port, reverse-proxy headers, TLS termination
    point, forwarded-identity assumptions, exposure rules,
    loopback/private/public interface choices).
- Step 3 deliverable:
  `track-j-deployment-boundary-contract.md` — prescriptive
  normative document, RFC 2119-style; точные deployment-
  boundary rules; точные allowed/forbidden Step 4 file
  surfaces; точный verification protocol.

### 4.2 Implementation surface (Step 4, conditional)

**Step 4 surface remains an open design question** until
Step 2 audit + Step 3 contract resolve it. Three honest
candidate paths:

- **PATH A — docs-only operationalization.** Ship a new
  `docs/operator-deployment-guide.md` or
  `docs/runbooks/track-j-deployment.md` с reverse-proxy
  config snippets (nginx / Caddy minimal examples),
  bind-host decision tree, exposure scenario matrix, и
  explicit deferral statement про health/readiness
  endpoint. Production code byte-identical через Track J.
  No `pyproject.toml` change. Q7 likely PATCH on closure.

- **PATH B — minimal code addition** (very narrow):
  - optionally add a runtime-side `--bind` warning или
    refusal на `0.0.0.0` / public-facing interface без
    explicit operator override flag (e.g.,
    `--bind-public-allow-risk`);
  - and/or add minimal `GET /healthz` endpoint that
    returns 200 plain text "ok\n" without auth (because
    health probes can't carry tokens) — but only if the
    audit decides this materially helps reverse-proxy
    integration vs plain TCP connect probe;
  - and/or extend `--help` output to mention reverse-
    proxy expectation.
  Each addition would be ~5-15 LOC in `_network_transport.py`,
  preserving Track H Step 3 §11.3 invariant
  (`_stdio_transport.py` byte-identical) and §11.6
  (`mcp_common/__init__.py` `__all__` byte-identical).

- **PATH C — hybrid** (PATH A docs + PATH B narrow code).

The honest narrowest path is decided by Step 2 audit
evidence + Step 3 contract — **not** pre-committed at
Step 1. Step 1 plan deliberately preserves all three
options.

### 4.3 Operator / docs alignment (Step 5)

After Step 4:
- update `SECURITY.md` "Honest constraints" → reflect
  post-Step-4 deployment-boundary contract status (the
  general-policy "trusted-network behind reverse proxy"
  stays accurate но gains pointer to new operator-facing
  guide if PATH A/C taken);
- update `docs/release-handoff.md` "What is in this
  handoff" / "What is NOT" / "Known limitations" sections;
- update `apps/platform/README.md` if direct factual
  drift;
- update `README.md` Quickstart + active parallel track
  section;
- update `scripts/dev/launch.ps1` / `scripts/dev/README.md`
  / `scripts/release/README.md` only if direct user-facing
  drift relative to bind-host / reverse-proxy expectation.

Точный финал docs scope — Step 5 inventory.

### 4.4 Closure deliverables (Step 6)

- `pyproject.toml` version bump (Q7 default; resolve в
  Step 6 на основе фактического Step 4 functional delta).
  PATCH `0.5.1 → 0.5.2` likely if Step 4 ships PATH A
  docs-only or PATH B/C tiny code; MINOR `0.5.1 → 0.6.0`
  только if Step 4 ships meaningful new external
  capability (e.g., `/healthz` endpoint that didn't exist
  before).
- `README.md` move Track J в Closed parallel tracks list
  (9 → 10) + add «Track J detail (закрыт)» section
  symmetric к Tracks A/B/C/D/E/F/G/H/I detail blocks.
- `PROJECT-STATUS.md` header rewrite + per-step closure
  sections.
- `CHANGELOG.md` new section under whichever version Q7
  dictates.

## 5. Что НЕ входит в Track J (out of scope)

Out of scope категорически (повтор для ясности; нарушение
этого списка — scope creep, а не валидное расширение
Track J):

### 5.1 Не enterprise identity stack

- **SSO / SAML / OIDC federation / SCIM provisioning.**
- **OAuth 2.0 / OpenID Connect.**
- **JWT / token introspection / refresh tokens / token
  rotation endpoint.**
- **RBAC / ABAC / per-token permissioning / per-tool ACL /
  per-tenant isolation / multi-tenant policy engine.**
- **Identity provider integration.**

### 5.2 Не in-process TLS / mTLS

- **In-process TLS / HTTPS termination.** Carry-over from
  Track H Step 3 §13.1 (Step 4 baseline forbidden); Track
  J **does not reverse this**. Operator's reverse proxy
  remains the TLS termination point.
- **mTLS / client certificate authentication.** Carry-
  over from Track H §13.3.
- **Certificate loading code, `ssl.SSLContext`, ALPN
  negotiation, OCSP stapling.**
- **Track J Step 4 MUST NOT add `ssl` module import to
  `_network_transport.py`.**

### 5.3 Не service supervisor / OS service

- **systemd unit / Windows Service / `launchd` plist
  registration.**
- **Hot reload / restart watcher / auto-update.**
- **Docker / Kubernetes deployment manifests, Helm
  charts, Kustomize.**
- **`supervisor` / `runit` / `s6` recipes.**
- **HA / clustering / multi-instance / load balancing.**

### 5.4 Не packaging ecosystem

- **`.msi` / `.deb` / signed binary distribution / GUI
  installer / wizard / PyPI publication / wheel
  publication beyond existing `[project.scripts]`
  declarations.** Track C wheel-build empty constraint
  preserved.
- **Auto-update, package signing, upgrade migration
  helpers.**

### 5.5 Не web UI / observability stack

- **Web UI / dashboard frontend / admin portal.**
- **Distributed tracing / observability stack
  (OpenTelemetry / Jaeger / Prometheus / OpenMetrics).**
- **Log aggregation (`journald` / `syslog` / ELK).**
- **Real-time metrics / monitoring / alerting.**
- **Web Application Firewall (WAF) integration.**

### 5.6 Не auth model redesign

- Track J **MUST NOT** modify Track H bearer auth model.
- `Authorization` header parsing, case-insensitive scheme
  handling, `hmac.compare_digest` validation, failure-
  equivalence rule, fail-closed startup gate, complete
  redaction discipline — all preserved byte-identical.

### 5.7 Не transport family redesign

- **No new transport family** beyond Track G stdio +
  Track H HTTP (no WebSocket / SSE / TCP / Unix-socket /
  named-pipe transports).
- **No HTTP/2 / HTTP/3 / QUIC.**
- **No long-poll / streaming endpoints beyond what
  `_serialize_tool_result` returns synchronously.**

### 5.8 Прочее out-of-scope

- **Новые MCP tools.** Registry invariant `read=15 /
  write=25 / intelligence=16` carried through.
- **1cv8.exe execution work.** Track J operates на
  network/deployment boundary layer; 1cv8 binary surface
  не задействуется.
- **Rollback / AST / multi-version 1С matrix expansion.**
  Track A / E / F territories.
- **Standalone `apps/platform` entrypoint.** Carry-over
  out-of-scope from Tracks G/H.
- **Real MCP client integration test as closure gate.**
  Recommended но не blocker (carry-over Track G/H/I
  pattern).
- **Rate limiting / quotas / throttling.** Reverse proxy's
  responsibility, not Track J's.
- **GitHub remote push.** Operator action, не часть
  трека.

## 6. Guardrails

Жёсткие инварианты, которые Track J **MUST** соблюдать на
каждом step:

1. **Registry invariant.** `mcp-read-server=15 /
   mcp-write-server=25 / mcp-intelligence-server=16` без
   drift'а ни на одном шаге; selfcheck зелёный.
2. **No new MCP tools.** `server.py:REGISTERED_TOOLS` для
   всех 3 servers — identical content / identical lookup
   functions / identical tool callable signatures.
3. **Track H + Track I auth surfaces preserved
   byte-identical.** `ProductAuthSettings`,
   `ProductConfig.auth`, `_parse_auth`,
   `_AUTH_ENV_TOKEN_RE`, `_resolve_token_sources`,
   `_resolve_env_token`, `Authorization` header parsing,
   case-insensitive scheme, `hmac.compare_digest`,
   failure-equivalence rule, fail-closed startup gate,
   redaction discipline, install fast-path round-trip
   integrity — all byte-identical.
4. **`mcp_common/__init__.py` `__all__` byte-identical**
   (10 names). New helpers (если any) — только
   underscore-prefixed private modules, аналогично
   Track G/H/I pattern.
5. **`_stdio_transport.py` byte-identical.** Track G
   surface preserved unchanged.
6. **`run_write_flow` discipline preserved.** Track J не
   trogает write-flow surface.
7. **Read-only-by-construction discipline preserved** для
   `mcp-intelligence-server`.
8. **No `[project.dependencies]` changes.** Track J
   implementation pure stdlib (Track G/H/I carry-over).
9. **No real credentials в repo / docs / commit messages.**
10. **No 1cv8.exe runs ни на одном шаге Track J.** Трек
    работает на network/deployment boundary layer.
11. **No premature production-readiness claim.** Track J
    closure ships deployment-boundary contract — это
    operator-facing recipe, не "production-ready"
    declaration.
12. **No reversal of Track H Step 3 §13.1 in-process-TLS-
    forbidden invariant** в Step 4 (in-process TLS
    остаётся out-of-scope; Track J formalizes the
    reverse-proxy alternative, не reverses TLS forbid).
13. **No remote push.** GitHub remote push — operator
    action, не часть трека.

## 7. Acceptance criteria (closure check Step 6)

Track J считается честно закрытым на Step 6, когда
**все 11 пунктов** одновременно выполнены:

1. **Documented plan + step-map + audit + contract.**
   Plan + step-map (Step 1) + baseline audit (Step 2) +
   normative contract (Step 3) — на диске, ship'нутые
   отдельными commit'ами.
2. **Step 4 deliverable** ship'нут: либо docs-only
   operator-facing deployment guide (PATH A), либо tiny
   code addition (PATH B), либо hybrid (PATH C). Решение
   документировано в Step 3 contract.
3. **Bind-host guidance** zafix'ena: operator может
   читать single-source-of-truth document и понимать,
   как выбрать `--bind <HOST>:<PORT>` для своего
   deployment scenario.
4. **Reverse-proxy header expectation** zafix'ena:
   operator знает, что `_MCPHandler` не doверяет / не
   потребляет X-Forwarded-* headers (auth is bearer-only;
   client IP not consulted for authorization).
5. **Exposure rules statement** zafix'ena для трёх
   scenarios: loopback-only / private subnet / public-
   facing-through-proxy.
6. **Health/readiness endpoint resolution** zafix'ena
   (либо ship'нут narrow `/healthz`, либо явно deferred
   с rationale).
7. **Track H + Track I surfaces byte-identical.** Diff
   против Track I closure state (commit `d408dd2`) для
   `_stdio_transport.py`, `_network_transport.py` (если
   PATH A — без изменений; если PATH B/C — narrow
   additive только в специфичных местах per Step 3
   contract), `installer.py:_config_to_dict`,
   `models.py`, `loader.py`, three `__main__.py`,
   `mcp_common/__init__.py` — empty или narrow per
   contract.
8. **Registry invariant.** Selfcheck сообщает
   `read_server_tools` len = 15, `write_server_tools`
   len = 25, `intelligence_server_tools` len = 16,
   `imports_ok=true`, `selfcheck_status=ok`.
9. **No new MCP tools.** Diff `REGISTERED_TOOLS` keys —
   empty.
10. **Operator / security docs alignment.** `SECURITY.md`,
    `docs/release-handoff.md`, `README.md`,
    `apps/platform/README.md` (если applicable),
    `scripts/dev/*` / `scripts/release/*` (если
    applicable) говорят one truth о post-Step-4
    deployment boundary; nothing claims «zero-trust» /
    «hostile-internet ready» / «enterprise-ready
    ingress» / «WAF/IDS/rate-limit solved».
11. **Linear history Step 1 → Step 6.** `git log
    --oneline` показывает шесть commit'ов с exact subject
    pattern `Track J / Step N — ...`, в правильном
    порядке.

## 8. Honest constraints, которые останутся после Track J closure

Track J **не закрывает** следующее (это не gaps Track J,
это explicit out-of-scope; см. §5):

- **Не zero-trust deployment.** Threat model остаётся
  "trusted internal network behind reverse proxy" — не
  "untrusted-by-default with mTLS / token introspection /
  per-request authorization"; zero-trust posture —
  отдельный значительно более широкий future track.
- **Не hostile-internet exposure.** Operator может
  выставить HTTP listener в Internet через reverse
  proxy с TLS, но это operator's risk acceptance, не
  Track J support claim.
- **Не enterprise-ready ingress stack.** No WAF / IDS /
  rate-limit / DDoS protection / anomaly detection
  integration — это reverse-proxy / cloud-LB / dedicated
  appliance territory.
- **Не observability solved.** Track J ship'ит
  deployment boundary, не distributed tracing / metrics /
  logging / alerting.
- **Не auth redesign.** Track H bearer model preserved
  byte-identical.
- **Не in-process TLS** (carry-over §5.2).
- **Не mTLS** (carry-over §5.2).
- **Не enterprise identity** (carry-over §5.1).
- **Не service supervision** (carry-over §5.3).
- **Не packaging ecosystem** (carry-over §5.4).
- **Не web UI** (carry-over §5.5).
- **Не new MCP tools** (carry-over §5.8).
- **Не 1cv8 work** (carry-over §5.8).
- **Не GitHub remote push** (carry-over §5.8).

После Track J closure honest support statement становится:

> Track G stdio baseline + Track H HTTP/1.1 `/mcp` with
> bearer auth + Track I install fast-path auth round-trip
> integrity + **Track J formalized deployment-boundary
> contract**: operator has a single-source-of-truth
> deployment recipe with explicit bind-host guidance,
> reverse-proxy integration expectations, exposure-rule
> matrix for three scenarios (loopback / private subnet /
> public-through-proxy), and explicit resolution on
> `/healthz` / `/readyz` endpoint (either narrow ship or
> explicit deferral with rationale). Threat model =
> trusted-network behind operator-owned reverse proxy
> that terminates TLS; in-process TLS is not provided
> (reverse proxy responsibility); mTLS / OAuth / JWT /
> RBAC / multi-tenant / WAF / rate-limit / observability
> stack — out-of-scope. The full Track G/H/I out-of-scope
> list (no full installer ecosystem, no secret storage
> beyond `${ENV:NAME}`, no Track H auth model changes,
> no service supervision, no web UI, no standalone
> `apps/platform` entrypoint, no new MCP tools, no
> 1cv8 work) carries forward unchanged.

## 9. Relation to prior tracks

- **Track A (Full Real 1cv8-backed Write Path).** Track J
  не trogает 1cv8 surface; никаких 1cv8.exe runs.
- **Track B (Productization & Delivery Polish).** Track J
  не реструктурирует repo hygiene / install fast path /
  scripts umbrella; `scripts/release/install.ps1` thin
  wrapper, `scripts/dev/launch.ps1` umbrella, и
  `scripts/dev/bootstrap_paths.ps1` остаются unchanged
  (potential narrow Step 5 wording-only update only if
  direct user-facing drift).
- **Track C (Packaging & Installer Delivery).** Track J
  carry-over honest constraint: wheel build остаётся
  пуст; никаких `.msi` / `.deb` / signed distribution.
- **Track D (Operator Credentials Hardening).** Track J
  не trogает `${ENV:NAME}` env-substitution model;
  Track D pattern preserved.
- **Track E (Multi-Version 1C Smoke Matrix).** Track J
  ortogonal — Track E работает с 1С platform versions
  evidence; Track J работает с network/deployment
  boundary.
- **Track F (Rollback Whitelist Expansion).** Track J
  ortogonal — Track F работает с rollback whitelist
  config; Track J — с network/deployment boundary.
- **Track G (Production-Grade MCP Transport and CLI).**
  Track J не trogает stdio surface; existing 3 `__main__.py`
  (preserved byte-identical в most cases — narrow
  additive change только if Step 4 takes PATH B/C);
  `_stdio_transport.py` byte-identical.
- **Track H (Network-Grade MCP Transport and
  Authentication Boundary).** Track J — **прямой
  следующий слой** поверх Track H: Track H §13 general-
  policy TLS posture формализуется в operator-facing
  contract; Track H bearer auth model preserved byte-
  identical; `_network_transport.py` либо byte-identical
  (PATH A), либо narrow additive (PATH B/C, e.g. bind
  warning, optional `/healthz` endpoint). Track H Step 3
  contract §13.1–§13.3 anchors are inherited as-is.
- **Track I (Installer Auth Round-Trip Integrity).**
  Track J ortogonal — Track I работает с install fast-
  path round-trip; Track J — с runtime deployment
  boundary. Track I `installer.py:_config_to_dict`
  byte-identical через Track J.

## 10. Open questions Q1–Q7

### Q1. Is the honest target for Track J: in-process TLS, reverse-proxy-first, or hybrid?

**Default planning anchor (резолвится в Step 2 / Step 3):**
**hybrid = reverse-proxy-first deployment boundary as
default; in-process TLS explicitly deferred** (carry-over
from Track H Step 3 §13.1 forbidden Step 4 baseline).

**Reasoning:**
- Track H Step 3 §13.1 already forbids in-process TLS in
  Step 4 baseline; Track J must not reverse this without
  proven blocker;
- reverse-proxy-first is widely supported by stdlib
  `http.server` (no TLS dependency required) and matches
  most existing operator workflows (nginx / Caddy /
  Apache / cloud LB are universal);
- in-process TLS would require either (a) `ssl` stdlib
  module integration (forbidden Step 4 surface) or (b)
  third-party PyPI dependency (forbidden by Track G/H/I
  inheritance §6 guardrail #8 / #14 wheel-build empty);
- "hybrid" framing means: documented reverse-proxy-first
  deployment is the supported default; in-process TLS is
  explicitly deferred to a future post-Track-J track if
  there is operator demand and a stdlib-only path
  evidence.

**Финальное решение** — Step 2 audit / Step 3 contract.

### Q2. Should Track J Step 4 be docs-only, minimal code change, or conditional?

**Default planning anchor:** **conditional based on Step 2
audit evidence**.

**Reasoning:**
- Step 1 plan deliberately preserves all three options
  (PATH A docs-only / PATH B narrow code / PATH C
  hybrid);
- the audit must surface concrete evidence whether
  bind-host warning, `/healthz` endpoint, or other narrow
  additions materially help operator-facing reverse-proxy
  integration vs being just-doc-able;
- pre-committing to docs-only or to code-addition at
  Step 1 would violate the discipline of letting Step 2
  evidence drive Step 3/4.

**Финальное решение** — Step 2 audit + Step 3 contract.

### Q3. What exact deployment threat model is being targeted?

**Default planning anchor:** **trusted internal network
behind operator-owned reverse proxy that terminates TLS**;
specifically:

- operator-owned LAN / VPN / private subnet;
- reverse proxy is in operator's trust boundary;
- operator owns DNS / TLS certificates / firewall rules;
- network between reverse proxy and Track J HTTP listener
  is trusted (loopback или private interface);
- explicitly **NOT** hostile public Internet by default
  (operator may expose to Internet through proxy at their
  own risk acceptance).

**Reasoning:**
- carries forward Track H §8.5 single-tier auth model
  (valid token grants full access; no per-request
  identity-based authorization);
- carries forward SECURITY.md "trusted-network deployment"
  honest constraint;
- matches typical small-team / single-organization MCP
  server deployment scenarios;
- does NOT promise zero-trust posture или hostile-internet
  hardening — those are explicit out-of-goal per §5.

**Финальное решение** — Step 3 contract.

### Q4. What exact deployment surfaces will be discussed?

**Default planning anchor:** Track J Step 3 contract MUST
discuss at minimum:

1. **Bind host/port choice** — three deployment scenarios
   (loopback / private subnet / public-facing through
   proxy); `_parse_bind` rules; recommendation matrix.
2. **Reverse-proxy headers** — explicit contract that
   `_MCPHandler` does NOT trust / consume X-Forwarded-*
   headers for authentication or authorization (auth is
   bearer-token-only, not client-IP-derived); operator-
   facing implication.
3. **TLS termination point** — operator's reverse proxy
   only; in-process TLS forbidden carry-over.
4. **Forwarded-identity assumptions** — none (Track H
   bearer auth is the only auth boundary; client IP and
   X-Forwarded-User не consulted).
5. **Exposure rules** — three scenarios:
   - **Scenario A: loopback-only** (`127.0.0.1` или `::1`)
     — local AI agent client, development, single-host
     deployment; safest default.
   - **Scenario B: private subnet** (e.g.,
     `10.x.x.x` / `172.16.x.x` / `192.168.x.x` или VPN
     overlay) — small team, trusted-network LAN; operator
     owns network boundary.
   - **Scenario C: public-facing-through-reverse-proxy**
     — operator binds to private interface that reverse
     proxy can reach; reverse proxy public-facing with
     TLS; explicit operator risk acceptance for adversarial-
     internet exposure.
6. **`/healthz` endpoint** — either narrow ship in Step 4
   PATH B/C OR explicit deferral with rationale (TCP
   connect probe is sufficient for health checking;
   reverse-proxy `proxy_pass` upstream health checks
   work without dedicated endpoint).

**Финальное решение** — Step 3 contract pins exact wording.

### Q5. What is explicitly NOT promised even after Track J closure?

**Default planning anchor:** Track J closure narrative
MUST explicitly state that closure does NOT mean any of:

- zero-trust deployment posture;
- hostile-internet exposure ready;
- enterprise-ready ingress stack;
- WAF / IDS / rate-limit / DDoS protection solved;
- observability stack solved (no distributed tracing,
  metrics, logging, alerting);
- auth redesign (Track H bearer model preserved);
- in-process TLS / mTLS;
- enterprise identity;
- service supervisor / OS service registration;
- packaging ecosystem;
- web UI.

**Финальное решение** — Step 6 closure narrative.

### Q6. Relationship to future likely tracks

**Default planning anchor:** Track J is **one maturity
layer**, not the last one. After Track J, future post-
Track-J tracks могут (without auto-opening):

- **Service supervision track** (systemd unit / Windows
  Service / `launchd` plist registration; hot reload;
  restart watcher) — separate maturity layer over Track
  G/H/J entrypoints.
- **Real MCP client integration test track** (Claude
  Desktop / MCP CLI smoke as full closure gate, not just
  recommendation).
- **Enterprise identity stack track** (SSO / OIDC / RBAC
  / multi-tenant) — significantly broader than Track H/J;
  multiple sub-tracks expected.
- **Packaging ecosystem track** (`.msi` / `.deb` /
  signed distribution / wheel publication beyond
  `[project.scripts]`).
- **In-process TLS track** (only if operator demand and
  stdlib-only evidence; otherwise stays deferred).
- **Multi-version 1С matrix expansion** (post-Track-E
  follow-up).

Track J framing in plan / step-map / contract / README /
PROJECT-STATUS / CHANGELOG **MUST** make clear that
closure ships one maturity layer (deployment-boundary
contract), not "deployment fully solved".

**Финальное решение** — Step 3 contract + Step 6 closure
narrative.

### Q7. Version-bump default for future Step 6

**Default planning anchor:** Q7 stays **open** until Step 6;
honest direction depends on Step 4 PATH choice:

- **PATH A docs-only** → likely PATCH (`0.5.1 → 0.5.2`)
  per Track I precedent (defect-class / docs-class fix);
- **PATH B narrow code** → likely PATCH (`0.5.1 → 0.5.2`)
  if change is bind-host warning / `--help` extension
  (no new external capability); MINOR (`0.5.1 → 0.6.0`)
  only if Step 4 ships meaningful new external capability
  (e.g., `/healthz` endpoint that didn't exist);
- **PATH C hybrid** → depends on code component scope.

**Counter-consideration**: Track J might honestly close
under MINOR if the operator-facing deployment guide is
substantial and qualitatively shifts the project from
"general-policy reverse-proxy posture" to "operator can
deploy from a recipe", even with docs-only Step 4. Honest
framing decision.

**Финальное решение** — Step 6 closure decision based on
фактический Step 4 functional / docs delta + SemVer
semantics review. Default expectation: PATCH; alternative
MINOR is acceptable если Step 4 ships ≥ one observable
new external capability.

---

## 11. Step trajectory (preview)

Подробности — в companion `track-j-...-step-map.md`.
Краткое резюме шести шагов:

1. **Step 1 — planning** (этот шаг). Два planning-документа
   + минимальные status-правки в README / PROJECT-STATUS
   под открытие active track'а J.
2. **Step 2 — deployment-boundary baseline audit**
   (docs-only). Один новый descriptive audit-документ;
   resolve Q1 (target = hybrid reverse-proxy-first), Q2
   (Step 4 PATH choice based on evidence), Q3 (threat
   model), Q4 (deployment surfaces enumerated).
3. **Step 3 — TLS / reverse-proxy / exposure contract**
   (docs-only). Один новый prescriptive normative document,
   RFC 2119-style; точные deployment-boundary rules; точные
   allowed/forbidden Step 4 file surfaces.
4. **Step 4 — deployment boundary deliverable** (docs-only
   PATH A, или narrow code PATH B, или hybrid PATH C; final
   choice in Step 3 contract). Default expectation: tight
   minimal deliverable — operator-facing deployment guide
   plus optional ≤ 15 LOC narrow additive code change in
   `_network_transport.py` if audit evidence supports.
5. **Step 5 — operator/security/release docs alignment**
   (docs-only). Точечная alignment SECURITY / release-
   handoff / README / apps/platform/README / возможно
   scripts/* под фактический post-Step-4 deployment-
   boundary state.
6. **Step 6 — final integration pass and Track J closure**.
   Q7 resolve (PATCH default; MINOR if Step 4 ships
   meaningful new external capability); pyproject version
   bump; README + PROJECT-STATUS + CHANGELOG closure
   narrative симметрично Track A/B/C/D/E/F/G/H/I pattern.
   **GitHub remote push — operator action, не часть
   трека.**
