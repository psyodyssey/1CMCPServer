# Parallel Track H — Network-Grade MCP Transport and Authentication Boundary (plan)

> **Companion file:**
> `track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 4 —
> отдельный заход; единственный шаг трека с production code
> change.

---

## 1. Зачем нужен Track H после Track G

После closure'а Track G (Production-Grade MCP Transport and CLI;
commit `b8ed7d6`, project version `0.4.0`) проект уже имеет
**первый production-grade operational слой** для трёх MCP servers:

- три canonical entrypoint'а
  (`python -m mcp_read_server` / `python -m mcp_write_server` /
  `python -m mcp_intelligence_server`),
- minimum-viable line-delimited stdio JSON-RPC 2.0 transport
  (stdlib-only, no third-party SDK),
- minimal CLI surface
  (`--help`, `--config-path`, `--transport stdio`, `--log-level`),
- три `[project.scripts]` console entries в `pyproject.toml`.

Но этот baseline сознательно ограничен **trusted local stdio
boundary**. Concrete gaps уже зафиксированы как honest constraints
в нескольких местах repository:

- `SECURITY.md` «Local stdio MCP transport only» block: «По-прежнему
  нет: built-in authentication / authorisation, multi-tenant
  isolation, hardened network transport (HTTP / WebSocket / SSE /
  TCP / named pipe), token / mTLS / OAuth / SAML / RBAC,
  supervisor daemon / systemd unit / Windows Service registration.»
- `docs/release-handoff.md` Known limitations: «Local stdio MCP
  transport only — no network / auth / service story.»
- `README.md` Quickstart «Что Quickstart **не** обещает»:
  «**не** network-grade MCP transport (HTTP / WebSocket / SSE /
  TCP / named pipe), **не** authentication / authorisation
  (token / mTLS / OAuth / RBAC).»
- `apps/platform/README.md` (4 locations after Track G / Step 5):
  «Network transport (HTTP / WebSocket / SSE / TCP / named pipe),
  authentication / authorization (token / mTLS / OAuth / RBAC),
  supervisor daemon ... по-прежнему out-of-scope».
- Track G closure narrative в `CHANGELOG.md` (`## 0.4.0`):
  «No network transport ... A future post-Track-G network
  transport track is the right place for any of those.»

Concrete gaps, которые Track H адресует:

1. **Никакого network MCP transport.** Серверы сейчас работают
   только когда MCP-aware client запускает их как local
   subprocess через stdio; никакого remote MCP-aware client
   не может подключиться по сети.
2. **Никакого authentication boundary.** Threat model = trusted
   local stdio (operator-owned process). Любой сосед-процесс
   с доступом к stdin/stdout запущенного сервера — full
   control. Это OK для local subprocess deployment, но
   неприемлемо для network-facing surface.
3. **Никакого documented deployment perimeter** для non-local
   use. Operator доменно знает только «местный subprocess»;
   никаких рекомендаций по network-listener'у, network exposure,
   reverse-proxy posture.
4. **Никакого honest support statement** уровня «local stdio
   exists, network/auth perimeter exists, supervisor/deployment
   posture at least bounded». После Track G честный support
   statement укладывается в первую часть; Track H закрывает
   следующий уровень — middle часть.

Track H — отдельный узкий parallel track, который ship'ит
**следующий слой зрелости** поверх Track G:

- уже не только local stdio,
- уже есть network-facing MCP transport,
- уже есть minimum authentication boundary,
- но всё ещё без enterprise fantasy и без scope explosion.

Это **не** «полный production-grade enterprise transport
solution» сразу — это второй сильный baseline, поверх которого
будущие parallel tracks (supervisor / systemd / packaging /
SSO / multi-tenant) могут добавлять свои слои.

## 2. Стартовая точка (post-Track-G factual baseline)

### 2.1 Существующий transport/entrypoint surface (Track G output)

- `apps/mcp-read-server/src/mcp_read_server/__main__.py` (~30 LOC) —
  `main()` зовёт `mcp_common._stdio_transport.run_main` с
  per-server name/version и existing `list_tools` / `get_tool`.
- `apps/mcp-write-server/src/mcp_write_server/__main__.py` (~30 LOC) —
  идентично shape.
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
  (~30 LOC) — идентично shape.
- `packages/mcp-common/src/mcp_common/_stdio_transport.py` (~245 LOC) —
  underscore-prefixed internal helper, **NOT** экспортирован
  из `mcp_common/__init__.py`; pure stdlib (`argparse`, `json`,
  `logging`, `inspect`, `sys`); реализует line-delimited
  JSON-RPC 2.0 loop, четыре required CLI флага, handlers для
  `initialize` / `ping` / `tools/list` / `tools/call` /
  `notifications/initialized` / `notifications/cancelled`,
  `ToolResult` → MCP envelope serialization, top-of-`run_main`
  exception boundary.
- `pyproject.toml` `[project.scripts]` block с тремя console
  entries (`mcp-read-server` / `mcp-write-server` /
  `mcp-intelligence-server`); никаких declared
  `[project.dependencies]`; `[tool.hatch.build.targets.wheel]
  packages = []` preserved (Track C honest constraint).

### 2.2 Что фактически отсутствует на 2026-05-10 (factual gap inventory)

Confirmed read-only check'ом по implementation surface
(`packages/mcp-common`, three MCP server packages):

- **Никакого HTTP server / handler.** Грep `http.server`,
  `socketserver`, `wsgi`, `asgi`, `fastapi`, `flask`,
  `aiohttp`, `starlette`, `werkzeug` по `apps/*/src` и
  `packages/*/src` → **zero hits**. Единственное упоминание
  `urllib.request` — в `apps/mcp-read-server/src/mcp_read_server/runtime/live_adapter.py`
  как outbound HTTP **client** к 1С infobase HTTP-publication
  endpoint (read-side probe), **не** MCP transport server.
- **Никакого WebSocket server.** Грep `websockets`, `wsproto`,
  `websocket`, `ws://`, `wss://` → **zero hits**.
- **Никакого SSE / streaming transport.** Грep
  `EventSource`, `text/event-stream`, `Server-Sent` → **zero
  hits**.
- **Никакого TCP server.** Грep `socket\.socket`,
  `socket\.AF_INET`, `asyncio.start_server`,
  `socketserver.TCPServer` → **zero hits**.
- **Никакого Unix domain socket / named pipe server.** Грep
  `AF_UNIX`, `\\\\\.\\pipe\\`, `mkfifo`, `os.mkfifo` →
  **zero hits**.
- **Никакой authentication / token validation infrastructure.**
  Грep `bearer`, `jwt`, `oauth`, `x509`, `ssl\.`,
  `tls`, `mtls`, `api_key`, `token_validation` по
  `apps/*/src` и `packages/*/src` → **zero hits** (substring
  matches только в docstring / comment контексте, не
  implementation code).
- **Никакого session / cookie / state management.** Грep
  `Set-Cookie`, `request\.cookies`, `session_id`,
  `session_token` → **zero hits**.
- **Никакого rate limiting / throttling.** Грep `rate_limit`,
  `throttle`, `bucket` → **zero hits**.
- **Никакого third-party MCP SDK или JSON-RPC library import'а.**
  Грep `from mcp\b`, `import mcp\b`, `jsonrpcserver`,
  `jsonrpc-base`, `jsonrpcclient` → **zero hits** anywhere
  в repo.
- **`pyproject.toml` имеет zero declared `[project.dependencies]`
  block at all.** Project пока живёт как pure stdlib install.

Это даёт Track H honest blank-slate: implementation will
**add** the network transport layer, не replace existing
local stdio transport, и **add** auth boundary как новый
optional perimeter, не модифицируя existing tool registry
boundary.

### 2.3 Existing operator/security wording после Track G / Step 5

`SECURITY.md`, `docs/release-handoff.md`, `README.md`,
`apps/platform/README.md`, `scripts/dev/launch.ps1`,
`scripts/dev/README.md` после Track G / Step 5 alignment
говорят one truth:

- local stdio MCP transport baseline exists
  (`python -m <server>`);
- threat model = local trusted stdio boundary
  (operator-owned process);
- network / auth / supervisor / hot reload / web UI /
  packaging-beyond-`[project.scripts]` / standalone
  `apps/platform` entrypoint — explicitly out-of-scope.

Track H будет `out-of-scope` пункты network / auth (и **только**
их) переводить в `in-scope`, оставляя supervisor / hot reload /
web UI / packaging / standalone-platform как
post-Track-H tracks.

## 3. Цель Track H

Ship'ить **второй production-grade operational слой** для трёх
MCP servers, который добавляет:

- canonical network MCP transport (один transport family,
  additive поверх existing stdio),
- minimum authentication boundary (один auth model,
  применяется ровно на network transport surface; stdio
  surface сохраняет existing trusted-local threat model
  без auth требований),
- aligned operator/security docs, отражающие фактический
  network deployment perimeter после Track H closure,
- honest support statement, который не путает «можно
  выставить network MCP server в trusted интранете с
  bearer-token auth» с «production-deployment-ready
  enterprise MCP solution».

Что **точно НЕ** входит в Track H — см. §5.

## 4. Что входит в Track H (in scope)

### 4.1 Documentation surface

- `track-h-...-plan.md` (этот документ).
- `track-h-...-step-map.md` (6 шагов).
- Step 2 deliverable: `track-h-transport-and-auth-baseline-audit.md` —
  descriptive read-only audit current state + per-server /
  per-package / per-pyproject inventory + 4-class breakdown +
  resolve Q1 / Q2 / Q3 / Q4 (transport family / count / auth
  baseline / config home).
- Step 3 deliverable: `track-h-network-transport-and-auth-contract.md` —
  prescriptive normative document, RFC 2119-style; точная
  спецификация network transport shape (framing, lifecycle,
  error envelope), exact auth model (token presentation,
  validation, fail-closed semantics, redaction), exact
  config schema, exact `mcp_common` integration boundary,
  exact `__main__.py` integration shape, allowed /
  forbidden Step 4 file surfaces, verification protocol.

### 4.2 Implementation surface (Step 4 only)

Track H ship'ит ровно **одну** transport family + ровно **один**
auth baseline. Default candidates (резолвятся в Step 2 /
Step 3, но фиксируются как planning anchor):

- transport family default = HTTP-based MCP boundary
  (см. Q1 ниже);
- auth baseline default = static bearer token (см. Q3 ниже).

Implementation **дополняет** existing stdio baseline; existing
`__main__.py` files, `_stdio_transport.py` helper, и
`[project.scripts]` console entries сохраняются. Track H
расширяет CLI surface новой транспортной flag-семьёй
(`--transport http` или эквивалент) и добавляет новые auth
flags / config keys; existing `--transport stdio` остаётся
default.

### 4.3 Operator / security docs alignment (Step 5)

- `SECURITY.md` — обновить «Local stdio MCP transport only»
  bullet под фактический post-Track-H state: «Local stdio +
  one bounded network transport with minimum auth»; явно
  оставить на местах не-закрытые пункты (full enterprise
  identity / mTLS-everywhere / supervisor / packaging).
- `docs/release-handoff.md` — обновить «What is in this
  handoff» (новый bullet про network transport entrypoint) +
  «What is NOT in this handoff» (still no enterprise identity
  stack / no service ecosystem / no web UI / no packaging
  beyond `[project.scripts]`) + «Known limitations».
- `README.md` — обновить Quickstart paragraph (network
  transport + auth теперь часть baseline'а) + Active
  parallel track section.
- `apps/platform/README.md` — точечный update «Чего сейчас
  намеренно ещё нет» list под фактический post-Track-H
  state.
- `scripts/dev/launch.ps1` + `scripts/dev/README.md` —
  только если есть direct user-facing drift в help/usage
  wording; default — не трогать.

### 4.4 Closure deliverables (Step 6)

- `pyproject.toml` version bump (Q7 default ДА; resolve в
  Step 6 на основе фактического Step 4 functional delta).
- `README.md` move Track H в Closed parallel tracks list +
  add «Track H detail (закрыт)» section симметрично Track
  A/B/C/D/E/F/G detail blocks.
- `PROJECT-STATUS.md` header rewrite + per-step closure
  sections.
- `CHANGELOG.md` new section under whichever version Q7
  dictates.

## 5. Что НЕ входит в Track H (out of scope)

Out of scope категорически (повтор для ясности; нарушение
этого списка — scope creep, а не валидное расширение Track H):

### 5.1 Full enterprise identity stack

- **SSO / SAML / OIDC federation.** Track H ship'ит один
  minimum auth model; integration с identity providers —
  отдельный future track.
- **SCIM** / user provisioning / directory sync.
- **Organizational RBAC platform** beyond simple "valid token
  → access". Per-tool RBAC, per-resource ACL, per-tenant
  policy — отдельные future tracks.
- **Multi-tenant policy engine** / tenant isolation.

### 5.2 Full zero-trust perimeter

- **mTLS everywhere.** Track H **может** support TLS / HTTPS
  termination как option (resolve в Step 3 contract), но
  не делает mTLS mandatory baseline.
- **Service mesh** (Istio / Linkerd / Consul Connect).
- **Secret rotation platform** / KMS / HashiCorp Vault /
  cloud-native secrets manager как mandatory baseline.
- **Encrypted-at-rest secrets file format.**

### 5.3 Web UI / dashboard frontend

- Никакого browser-facing UI для MCP traffic visualization /
  request/response inspection / audit log explorer.
- Никакого admin web portal.

### 5.4 Packaging ecosystem

- `.msi` / `.deb` / signed binary distribution / GUI
  installer / wizard.
- PyPI / public package publication strategy.
- Wheel build (Track C wheel-build empty constraint
  preserved).

### 5.5 Full service management ecosystem

- **systemd unit registration** / Windows Service
  registration / `launchd` plist registration.
- **Auto-update** mechanism.
- **Orchestration templates** (Helm / Kustomize / Docker
  Compose / Kubernetes manifests).
- **HA / clustering / load balancing** / multi-instance
  service discovery.
- **Background watchers** / hot reload / automatic restart
  на изменения config / supervisor daemon.

### 5.6 Прочее out-of-scope

- **Новые MCP tools.** Registry invariant `read=15 / write=25
  / intelligence=16` carried through unchanged.
- **1cv8.exe execution work.** Track H operates на process /
  transport / auth layer уровне; 1cv8 binary surface не
  задействуется.
- **Rollback / AST / multi-version 1С matrix expansion.**
  Track A / E / F territories.
- **Standalone `apps/platform` entrypoint.** Carry-over
  out-of-scope from Track G Q6.
- **Real MCP client integration test as closure gate.**
  Recommended но не blocker (наследуется из Track G
  pattern).
- **Distributed tracing / observability stack**
  (OpenTelemetry / Jaeger / Prometheus).
- **Rate limiting / throttling / quotas** — может быть в
  honest non-goal, но decision финальный в Step 3 contract.
- **GitHub remote push.** Operator action, не часть трека.

## 6. Guardrails

Жёсткие инварианты, которые Track H **MUST** соблюдать на
каждом step:

1. **Registry invariant.** `mcp-read-server=15 /
   mcp-write-server=25 / mcp-intelligence-server=16` без
   drift'а ни на одном шаге; selfcheck зелёный.
2. **No new MCP tools.** `server.py:REGISTERED_TOOLS` для
   всех 3 servers — identical content / identical lookup
   functions / identical tool callable signatures на всех
   шагах. Network transport дополняет dispatch surface, не
   меняет registry surface.
3. **Stdio baseline preserved.** Existing `python -m
   <server>` invocation + `--transport stdio` default flag +
   `_stdio_transport.py` internal helper — продолжают
   работать без изменения public API. Track H — additive,
   не replacement.
4. **`mcp_common` public API surface preserved
   byte-identical.** Существующий `mcp_common/__init__.py`
   `__all__` (`OperationContext`, `PlatformError`,
   `PolicyDeniedError`, `ProcessExecutionError`,
   `HealthCheckError`, `ToolResult`, `ToolCallable`,
   `build_tool_registry`, `list_registered_tools`,
   `get_registered_tool`) — без удалений, без переименований.
   Любые new helpers из Track H — только underscore-prefixed
   private modules, аналогично Track G `_stdio_transport.py`
   pattern.
5. **`run_write_flow` discipline preserved.** `tools/call`
   через network transport идёт через тот же
   `get_tool(name)(...)` boundary, который для write-tools
   роутится через `run_write_flow` (preflight → snapshot →
   operation → verify → audit). Никаких parallel write
   paths.
6. **Read-only-by-construction discipline preserved.**
   `mcp-intelligence-server` остаётся read-only;
   `onec_policy_engine` не импортируется в intelligence
   package.
7. **No `[project.dependencies]` block as mandatory
   baseline unless absolutely justified.** Default — pure
   stdlib implementation (Track G precedent — `argparse`,
   `json`, `logging`, `inspect`, `sys`). Если transport
   choice (Q1) делает stdlib implementation честно
   неподъёмным (например, full HTTPS+TLS+ALPN production
   stack), это decision финальный в Step 3 contract; Step
   2 audit обязан собрать evidence.
8. **No real credentials в repo / docs / commit messages.**
   Bearer tokens — только в env-substitution form
   (`${ENV:NAME}`) или в operator-private overlay-файлах,
   namesake которых не committed.
9. **No 1cv8.exe runs ни на одном шаге Track H.** Трек
   работает на process / transport / auth layer уровне,
   не на 1cv8 binary surface.
10. **Production code touched только в Step 4** и **только**
    на explicit allowed surfaces (resolve в Step 3
    contract). Шаги 1, 2, 3, 5, 6 — documentation /
    status / version-only.
11. **`pyproject.toml` `[tool.hatch.build.targets.wheel]
    packages = []` preserved** (Track C honest constraint
    carried through unchanged).
12. **No premature "production-ready for adversarial
    network deployment" claim.** Threat model для network
    transport честно отражает уровень — minimum auth
    boundary, trusted-network посыл, не «zero-trust
    enterprise-grade».
13. **No remote push.** GitHub remote push — operator
    action, не часть трека.

## 7. Acceptance criteria (closure check Step 6)

Track H считается честно закрытым на Step 6, когда **все
12 пунктов** одновременно выполнены:

1. **Documented transport/auth plan and contract.** Plan +
   step-map (Step 1) + baseline audit (Step 2) + normative
   contract (Step 3) — на диске, ship'нутые отдельными
   commit'ами, без нарушения Step format.
2. **Implemented network-grade MCP transport on top of
   Track G baseline.** `python -m mcp_read_server
   --transport <new-family> --help` (точное имя — Q1
   resolve) returns exit 0 + non-empty usage; transport
   loop поднимается; minimum-viable MCP method set
   (`initialize` / `ping` / `tools/list` / `tools/call`)
   работает поверх network transport.
3. **Implemented minimum authentication boundary.**
   Sample request без valid auth artifact → fail-closed
   с appropriate transport-level error envelope (точная
   shape — Q3 / Step 3 contract); sample request с valid
   auth artifact → success path.
4. **Local stdio Track G surface preserved.** Все три
   `python -m <server> --transport stdio --help` exit 0
   + non-empty usage; stdio JSON-RPC dispatch works
   без regression; existing `[project.scripts]` console
   entries не deprecated.
5. **`mcp_common` public API preserved byte-identical.**
   Diff `mcp_common/__init__.py` против Track G closure
   state — empty (no exports added / removed / renamed).
6. **Registry invariant.** Selfcheck сообщает
   `read_server_tools` len = 15, `write_server_tools` len
   = 25, `intelligence_server_tools` len = 16,
   `imports_ok = true`, `selfcheck_status = ok`.
7. **No new MCP tools.** Diff `REGISTERED_TOOLS` keys для
   всех 3 servers — empty (никаких additions, removals,
   renames).
8. **Operator / security docs alignment.** `SECURITY.md`,
   `docs/release-handoff.md`, `README.md`,
   `apps/platform/README.md`, `scripts/dev/*` (если
   применимо) говорят one truth о network/auth surface;
   nothing claims «enterprise-ready» / «zero-trust» / «full
   identity stack».
9. **Honest limitations explicitly preserved.** SECURITY.md
   "Honest constraints", release-handoff "What is NOT in
   this handoff", CHANGELOG closure section все явно
   перечисляют out-of-scope (5.1–5.6 этого плана),
   nothing claims their resolution.
10. **Linear history Step 1 → Step 6.** `git log --oneline`
    показывает шесть commit'ов с exact subject pattern
    `Track H / Step N — ...`, в правильном порядке, без
    accidental extra commits inside Track H scope.
11. **`verify-release.ps1` GREEN на clean tree** (no
    `-AllowDirtyTree`); 8 checks PASS / SKIP; selfcheck
    registries и status корректны.
12. **No 1cv8.exe runs ни на одном шаге Track H; no real
    credentials в diff'ах; no remote push.**

## 8. Honest constraints, которые останутся после Track H closure

Track H **не закрывает** следующее (это не gaps Track H, это
explicit out-of-scope; см. §5):

- никакого full enterprise identity stack (SSO / SAML /
  OIDC / SCIM / RBAC / multi-tenant);
- никакого full zero-trust perimeter (mTLS everywhere /
  service mesh / KMS / vault как mandatory);
- никакого web UI / dashboard;
- никакого packaging ecosystem beyond `[project.scripts]`
  declarations (`.msi` / `.deb` / signed distribution /
  PyPI / wheel publication);
- никакого full service management ecosystem (systemd /
  Windows Service / `launchd` / auto-update / HA /
  clustering / load balancing / hot reload / supervisor
  daemon с restart watcher);
- никаких новых MCP tools;
- никакого 1cv8 work;
- никакого rollback / AST / multi-version expansion;
- никакого standalone `apps/platform` entrypoint;
- никакого distributed tracing / observability stack;
- никакого real MCP client integration test as closure
  gate;
- никакого remote push.

После Track H closure honest support statement становится:

> Local stdio MCP transport baseline (Track G) **plus** one
> network MCP transport family with minimum authentication
> boundary (Track H). Threat model network surface =
> trusted-network deployment with token-based auth perimeter,
> **не** adversarial-internet zero-trust posture, **не**
> enterprise-grade SSO/RBAC/multi-tenant. Operator-owned
> process model сохраняется; lifecycle / supervisor /
> packaging остаются operator's responsibility.

## 9. Relation to prior tracks

- **Track A (Full Real 1cv8-backed Write Path).** Track H
  не задевает 1cv8 surface; `run_write_flow` discipline для
  write-tools preserved; никаких 1cv8.exe runs.
- **Track B (Productization & Delivery Polish).** Track H
  не реструктурирует repo hygiene / install fast path /
  scripts umbrella; `scripts/release/install.ps1`,
  `scripts/dev/launch.ps1`, `scripts/dev/bootstrap_paths.ps1`
  не изменяются на Step 4 (Step 5 trogат launch.ps1 /
  README только если direct user-facing drift).
- **Track C (Packaging & Installer Delivery).** Track H
  carry-over honest constraint: wheel build остаётся пуст
  (`[tool.hatch.build.targets.wheel] packages = []`); никаких
  `.msi` / `.deb` / signed distribution / PyPI publication.
  `[project.scripts]` block может расшириться (например,
  если auth/transport ship'ит свой console entry — resolve
  в Step 3 contract; default — нет).
- **Track D (Operator Credentials Hardening).** Track H
  **переиспользует** existing `${ENV:NAME}` env-substitution
  pattern для bearer token / auth secret config (resolve в
  Step 3 contract); никакого parallel credentials path.
  `command_preview` redaction discipline не задевается
  (Track D applies к 1С DESIGNER credentials, не к MCP
  transport auth).
- **Track E (Multi-Version 1C Smoke Matrix).** Track H
  ortogonal — Track E работает с 1С platform versions
  evidence; Track H работает с MCP transport / auth.
  Никаких изменений в `docs/version-support-matrix.md`.
- **Track F (Rollback Whitelist Expansion).** Track H
  ortogonal — Track F работает с rollback whitelist
  config; Track H работает с MCP transport / auth.
  `_AUTOMATIC_RECOVERY_SUPPORTED` / `_ROLLBACK_SUPPORTED_OPERATIONS`
  frozensets не задеваются.
- **Track G (Production-Grade MCP Transport and CLI).**
  Track H — **прямой следующий слой** поверх Track G:
  существующий stdio entrypoint / CLI / `_stdio_transport.py`
  helper preserved; Track H добавляет новый transport
  family (additive) и auth boundary (additive). Track G
  Step 3 contract patterns (RFC 2119-style normative,
  exact allowed/forbidden file surfaces, narrow Step 4
  implementation boundary) переиспользуются как структурный
  precedent.

## 10. Open questions Q1–Q7

### Q1. Какой network transport family брать первым?

**Default planning anchor (резолвится в Step 2 / Step 3):**
HTTP-based MCP boundary (например, HTTP+SSE per current
MCP-spec drafts).

**Reasoning:**
- ближе к practical client/server deployment story
  (reverse proxy / load balancer compatibility / standard
  TLS termination patterns);
- честнее для near-enterprise trajectory, чем raw
  WebSocket-first или TCP-first;
- standard HTTP server stdlib (`http.server`) даёт первый
  approximation без mandatory third-party dependency.

**Что ещё рассмотреть в Step 2:**
- HTTP + SSE (server-sent events для streaming responses);
- pure HTTP request/response (без SSE);
- WebSocket (ws:// / wss://);
- TCP socket (raw JSON-RPC framing);
- Unix domain socket / named pipe.

**Финальное решение** — Step 3 contract.

### Q2. Сколько transport families брать в Track H?

**Default:** **exactly one.**

**Reasoning:**
- narrowest honest scope;
- не плодить multi-transport matrix на первом шаге;
- следующий transport family (если потребуется) — отдельный
  post-Track-H track.

### Q3. Какой auth baseline брать первым?

**Default planning anchor (резолвится в Step 2 / Step 3):**
static bearer token (`Authorization: Bearer <token>` header
или transport-equivalent), валидируемый против operator-
supplied list / env-substitution.

**Reasoning:**
- минимальный реальный security perimeter (уже не «no
  auth»);
- без enterprise identity explosion (никакого OAuth flow,
  никакого token introspection endpoint, никакого OIDC);
- честно отражает trusted-network deployment story;
- переиспользует Track D `${ENV:NAME}` pattern для secret
  config.

**Что ещё рассмотреть в Step 2:**
- API key (header / query param / config-only);
- HMAC signature (request signing);
- HTTP Basic auth;
- mutual TLS (out-of-scope per §5.2 — не mandatory baseline,
  но **может** быть upgrade option в Step 3 contract).

**Финальное решение** — Step 3 contract.

### Q4. Где должен жить auth config?

**Default:** в **existing config model boundary** (продолжение
product-config schema из Phase 5, расширенное новой
optional `auth` section), без vault platform as baseline.

**Reasoning:**
- никакого parallel config path для transport-level secrets;
- operator-managed secret path остаётся acceptable
  (`${ENV:NAME}` env-substitution из Track D);
- stronger secret-management tracks (KMS / vault / OS
  keychain) могут прийти позже как post-Track-H tracks.

**Финальное решение** — Step 3 contract (точная shape новой
config section).

### Q5. Нужен ли supervisor / service layer внутри Track H?

**Default:** **НЕТ.**

**Reasoning:**
- не смешивать transport / auth с process lifecycle track;
- supervisor / systemd / Windows Service / hot reload =
  отдельный следующий трек post-Track-H;
- Track H ship'ит entrypoint, как Track G; lifecycle
  management — operator's responsibility (или existing
  `apps/platform/runtime.py` boundary, который Track H **не**
  расширяет — наследуется Track G §9.2 invariant).

**Финальное решение** — фиксируется в Step 3 contract (Step
4 implementation surface forbidden list explicitly включает
supervisor / service registration code).

### Q6. Нужно ли трогать apps/platform standalone entrypoint?

**Default:** **НЕТ.**

**Reasoning:**
- explicit carry-over out-of-scope from Track G Q6;
- standalone entrypoint для product layer — отдельный
  future track.

**Финальное решение** — Step 3 contract (Step 4 forbidden
list).

### Q7. Нужен ли version bump на closure Track H?

**Default planning anchor:** likely **YES** (`0.4.0 → 0.5.0`)
если Step 4 ship'ит real transport/auth capability с
observable runtime behaviour delta.

**Reasoning:**
- precedent — Track D `0.1.0 → 0.2.0`, Track F
  `0.2.0 → 0.3.0`, Track G `0.3.0 → 0.4.0` — все шли
  с MINOR bump на real production code change;
- backward-compatible new functionality (existing stdio
  transport preserved, public API preserved) → classic
  MINOR bump per SemVer.

**Финальное решение** — Step 6 closure decision (на основе
фактического Step 4 functional delta).

---

## 11. Step trajectory (preview)

Подробности — в companion `track-h-...-step-map.md`. Краткое
резюме шести шагов:

1. **Step 1 — planning** (этот шаг). Два planning-документа +
   минимальные status-правки в README / PROJECT-STATUS под
   открытие active track'а H.
2. **Step 2 — transport / auth baseline audit** (docs-only).
   Один новый descriptive audit-документ; resolve Q1 / Q2 /
   Q3 / Q4.
3. **Step 3 — network transport / auth contract** (docs-only).
   Один новый prescriptive normative document, RFC 2119-style;
   точные allowed/forbidden Step 4 surfaces; resolve финальные
   transport family + auth model + config schema +
   verification protocol.
4. **Step 4 — narrow network transport and auth implementation**
   (production code change, единственный шаг). Implementation
   ровно одной transport family + одного auth model по Step 3
   contract; existing stdio surface preserved; registries без
   drift'а; no new MCP tools.
5. **Step 5 — operator docs and security alignment**
   (docs-only). Точечная alignment SECURITY / release-handoff
   / README / apps/platform/README / возможно scripts/dev/*
   под фактический post-Step-4 surface.
6. **Step 6 — final integration pass and Track H closure**.
   Q7 resolve; pyproject version bump (если Q7 = ДА);
   README + PROJECT-STATUS + CHANGELOG closure narrative
   симметрично Track A/B/C/D/E/F/G pattern. **GitHub remote
   push — operator action, не часть трека.**
