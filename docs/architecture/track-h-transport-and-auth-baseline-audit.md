# Parallel Track H — Transport and Auth Baseline Audit (Step 2)

> **Companion files:**
> `track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md`
> (Step 1 plan), `track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md`
> (Step 1 step-map). Этот документ — Step 2 deliverable:
> **descriptive read-only audit** текущего transport/auth
> baseline'а после Track G closure, плюс evidence-grounded
> Step 2 resolutions для Q1 / Q2 / Q3 / Q4.

> **Status:** Track H / Step 2 deliverable. Documentation-only.
> **Descriptive**, не prescriptive: фиксирует current state и
> Step 2 directional answers; нормативные правила для Step 4
> implementation формализуются отдельно в Step 3 contract.

> **Этот документ ничего не реализует.** Никакого `__main__.py`
> расширения, никакого нового helper'а, никакого
> `pyproject.toml` change'а, никакого CLI flag'а — только
> read-only audit и направление для Step 3 / Step 4.

---

## 1. Purpose / scope

Этот документ — **descriptive Step 2 audit** для Track H.
Он отвечает на следующие вопросы на основе read-only
inspection текущего repository state:

1. Что фактически существует сейчас в repo относительно
   network MCP transport и authentication boundary?
2. Какие existing surfaces можно переиспользовать в
   Track H?
3. Какие existing surfaces **adjacent**, но не являются
   решением?
4. Чего **concretely не хватает**?
5. Что вынесено за scope Track H целиком?
6. Какой transport family выбран как Step 2 directional
   answer (Q1)?
7. Сколько transport families ship'ит Track H (Q2)?
8. Какой auth baseline выбран (Q3)?
9. Где живёт auth config (Q4)?

Документ **не**:

- ship'ит код (Step 4 territory);
- формулирует normative MUST/MUST NOT contract
  (Step 3 territory);
- alignment'ит operator-facing docs (Step 5 territory);
- открывает closure narrative (Step 6 territory);
- pretend'ит, что transport / auth уже implemented
  (zero-implementation document);
- меняет `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  registries, CHANGELOG, SECURITY, README, PROJECT-STATUS,
  release-handoff, apps/platform/README.

---

## 2. Method

Audit опирается на:

1. **Read-only grep** по `apps/*/src/` и `packages/*/src/`
   с расширением `*.py` для каждой релевантной категории
   (HTTP server libs, SSE/streaming, WebSocket, TCP/socket
   server, TLS/SSL, auth, sessions/cookies, rate limiting,
   process supervision).
2. **Read-only inspection** existing transport surfaces,
   которые ship'нул Track G (`_stdio_transport.py`,
   три `__main__.py`, `[project.scripts]`).
3. **Read-only inspection** `pyproject.toml` на наличие
   `[project.dependencies]` / `[project.optional-dependencies]`
   blocks, `[project.scripts]` entries, `[tool.hatch.build.targets.wheel]`
   constraint.
4. **Read-only inspection** existing config schema
   (`ProductConfig` dataclass в `apps/platform/src/onec_platform/models.py`)
   на наличие optional sections, в которые auth config
   мог бы additively встать.
5. **Read-only inspection** Track D credential pattern
   (`${ENV:NAME}` env-substitution + `_redact_password_args`)
   в `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`.
6. **Read-only inspection** existing operator-facing docs
   (`SECURITY.md`, `docs/release-handoff.md`, `README.md`,
   `apps/platform/README.md`, `scripts/dev/*`) на их
   текущий support statement.

Все evidence ниже подкреплены конкретными file/line
references; никаких inferred claims без grep'а.

---

## 3. Current baseline by surface

### 3.1 Three MCP server packages (post-Track-G)

После Track G / Step 4 (commit `370c5a8`) три MCP server
packages имеют идентичную structure:

| Package | `__main__.py` | `server.py` | `tools.py` | Tools |
|---|---|---|---|---|
| `mcp_read_server` | `apps/mcp-read-server/src/mcp_read_server/__main__.py` (~30 LOC) | `server.py` exposes `list_tools()` / `get_tool(name)` | 15 read tools | 15 |
| `mcp_write_server` | `apps/mcp-write-server/src/mcp_write_server/__main__.py` (~30 LOC) | `server.py` exposes `list_tools()` / `get_tool(name)` | 25 write tools | 25 |
| `mcp_intelligence_server` | `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py` (~30 LOC) | `server.py` exposes `list_tools()` / `get_tool(name)` | 16 intelligence tools | 16 |

Каждый `__main__.py` импортирует
`mcp_common._stdio_transport.run_main` и зовёт его с
package's local `list_tools` / `get_tool`. Никаких
parallel registration paths; никаких back-door write
channels.

### 3.2 `mcp_common` shared package

- `packages/mcp-common/src/mcp_common/__init__.py` —
  public API surface: `OperationContext`, `PlatformError`,
  `PolicyDeniedError`, `ProcessExecutionError`,
  `HealthCheckError`, `ToolResult`, `ToolCallable`,
  `build_tool_registry`, `list_registered_tools`,
  `get_registered_tool` (10 names в `__all__`).
- `packages/mcp-common/src/mcp_common/_stdio_transport.py` —
  underscore-prefixed **private** module (NOT в
  `__init__.py`'s `__all__`, NOT в imports), 245 LOC.
  Pure stdlib (`argparse`, `inspect`, `json`, `logging`,
  `sys`, `typing.Callable`, `.result.ToolResult`).
  Реализует:
  - `_build_arg_parser(prog, description)` — 4 CLI
    флага (`--config-path`, `--transport stdio`,
    `--log-level {DEBUG,INFO,WARNING,ERROR}`, плюс
    `--help` от argparse);
  - `_configure_logging(level_name, server_name)` —
    stderr-only diagnostic output;
  - `_maybe_load_product_config(path, logger)` —
    optional `onec_platform.bootstrap_product_from_json_file`
    boundary call;
  - `_handle_request(req, ...)` — dispatch для
    `initialize` / `ping` / `tools/list` / `tools/call`
    / `notifications/initialized` /
    `notifications/cancelled`;
  - `_serialize_tool_result(result)` — `ToolResult` →
    MCP envelope (`content` text + optional
    `structuredContent` payload + `isError`);
  - `_serve_stdio(server_name, ..., list_tools_fn,
    get_tool_fn, logger)` — line-delimited stdio
    JSON-RPC 2.0 loop, EOF/SIGINT graceful exit,
    fail-soft `-32700 Parse error` на garbled input;
  - `run_main(prog, description, server_name,
    server_version, list_tools_fn, get_tool_fn, argv)` —
    top-level entry с exception boundary (catches all
    exceptions, logs, returns non-zero exit code).
- Других modules в `packages/mcp-common/src/mcp_common/`
  кроме `errors.py`, `registry.py`, `result.py`,
  `types.py`, `__init__.py`, `_stdio_transport.py` —
  **нет**. Никакого `_network_transport.py` /
  `_auth.py` / `_http_server.py` пока не существует.

### 3.3 `pyproject.toml` after Track G closure

`pyproject.toml` после Track G / Step 6 closure (commit
`b8ed7d6`):

- `[build-system]` — `requires = ["hatchling"]`,
  `build-backend = "hatchling.build"`.
- `[project]`:
  - `name = "1c-agent-platform"`;
  - `version = "0.4.0"` (Track G closure bump
    `0.3.0 → 0.4.0`);
  - `description`, `requires-python = ">=3.11"`,
    `readme = "README.md"`, `authors`.
- `[project.scripts]` — три console entries
  (`mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`); каждая указывает на
  `<package>.__main__:main`.
- `[project.dependencies]` — **block отсутствует целиком**.
- `[project.optional-dependencies]` — **block отсутствует
  целиком**.
- `[tool.ruff]`, `[tool.pytest.ini_options]` — присутствуют.
- `[tool.hatch.build.targets.wheel] packages = []` —
  пуст по Track C / Step 3 honest constraint (carry-
  through).

Это означает: **Track H starts с zero declared runtime
dependencies**. Любая Q1 transport choice, требующая
третьесторонней библиотеки, обязана либо обосновать
добавление `[project.dependencies]`, либо использовать
stdlib-only path.

### 3.4 `ProductConfig` schema

`apps/platform/src/onec_platform/models.py:149` —
`ProductConfig` dataclass с следующими top-level fields:

- `product_name: str`,
- `profile_name: str`,
- `project: ProjectConfig`,
- `default_environment: str`,
- `servers: ProductServerToggles`,
- `bootstrap: ProductBootstrapSettings`,
- `runtime: ProductRuntimeSettings = field(default_factory=...)` —
  Phase 5 / Step 3 optional section; Phase 6 / Step 6
  расширил schema до v2 backward-compatibly;
- `enterprise: EnterpriseFoundationSettings = field(default_factory=...)` —
  Phase 6 / Step 8 optional section.

Pattern «add new optional section default-factory»
доказан backward-compatibly дважды (Phase 5/Step 3 для
`runtime`; Phase 6/Step 8 для `enterprise`). Track H
может additively встроить новый optional section без
breaking Step 2 configs.

### 3.5 Track D credential pattern

`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
содержит готовый working pattern для secret config:

- l.135-160 — block comments документирующие
  `${ENV:NAME}` substitution.
- l.155 — `_ENV_TOKEN_SUBSTRING = "${ENV:"`.
- l.157 — regex `r"^\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}$"`.
- l.161 — `_resolve_env_token(value, *, template_field_name)`
  — fail-closed на missing/empty/partial-mixed forms.
- l.55-67 — `_redact_password_args(...)` — `command_preview`
  redaction pattern для argv elements following `/P` /
  `/Pwd`.

Это **adjacent reusable pattern** для bearer token
secret config. Track H может (и, по Q4 audit answer,
**должен**) переиспользовать env-substitution discipline
без копирования кода (Track D pattern остаётся applied к
1С DESIGNER credentials в command templates; Track H
shipper может либо вызвать тот же helper, либо ship'ить
narrow его адаптацию — точное решение зафиксируется в
Step 3 contract).

### 3.6 Existing operator-facing support statement (post-Track-G)

После Track G / Step 5 docs alignment + Step 6 closure
unified support statement зафиксирован в:

- `SECURITY.md` l.40-65 — «Local stdio MCP transport only»
  block; явно перечислены: «По-прежнему нет: built-in
  authentication / authorisation, multi-tenant isolation,
  hardened network transport (HTTP / WebSocket / SSE /
  TCP / named pipe), token / mTLS / OAuth / SAML / RBAC,
  supervisor daemon / systemd unit / Windows Service
  registration.»
- `docs/release-handoff.md` Known limitations + What is
  NOT in this handoff.
- `README.md` Quickstart + Track G detail (закрыт)
  section.
- `apps/platform/README.md` (4 locations) — все
  acknowledge Step 4 baseline preserving network/auth/
  supervisor out-of-scope.
- `scripts/dev/launch.ps1` + `scripts/dev/README.md` —
  «не стартует MCP-серверы; transport — local-stdio only,
  без network / auth».
- `CHANGELOG.md` `## 0.4.0` section «Honest constraints
  update under Track G closure»: «No network transport
  ... A future post-Track-G network transport track is
  the right place for any of those.»

Track H / Step 5 обязан этот unified statement обновить
под фактический post-Step-4 surface — но это Step 5
territory, не Step 2.

### 3.7 Existing scripts (`scripts/dev/*`, `scripts/release/*`)

- `scripts/dev/bootstrap_paths.ps1` — set'ит PYTHONPATH
  для 11 internal `src/` directories. Не задевается
  Track H.
- `scripts/dev/launch.ps1` — operator/dev umbrella;
  явно НЕ стартует MCP servers (это Track G entrypoints
  territory).
- `scripts/dev/run_dev_check.ps1`, `scripts/dev/selfcheck.py` —
  imports + registry counts + health summary; никакой
  network / auth invocation.
- `scripts/release/install.ps1`, `scripts/release/_install_runner.py`,
  `scripts/release/verify-release.ps1` — release-facing
  wrappers (Track B / C territory); 8 release-facing
  checks including the credential leak guard (three PEM
  private-key header variants — generic, RSA, OpenSSH —
  plus the well-known AWS secret-access-key token; the
  exact pattern strings are defined in
  `scripts/release/verify-release.ps1` itself, and this
  document deliberately does not re-quote them so it stays
  outside the guard's match set) and the credential
  template hygiene check (`/P` / `/Pwd` argv positions in
  tracked `*.config.json` files, env-substitution form
  `${ENV:NAME}` accepted as the documented safe form).

---

## 4. Read-only evidence for absence of network / auth code

Следующие grep checks **подтверждены zero hits** по
`apps/*/src/` и `packages/*/src/` (ripgrep, case-
insensitive, Python files only):

| Category | Patterns checked | Hits |
|---|---|---|
| HTTP server libs | `http\.server`, `wsgiref`, `wsgi\b`, `asgi\b`, `fastapi`, `flask`, `aiohttp`, `starlette`, `werkzeug`, `bottle` | **0** |
| SSE / streaming | `EventSource`, `text/event-stream`, `Server-Sent`, `sse_starlette`, `sseclient` | **0** |
| WebSocket | `websockets`, `wsproto`, `websocket-client`, `aiohttp\.ws`, `ws://`, `wss://` | **0** |
| TCP / socket server | `socketserver`, `socket\.socket`, `asyncio\.start_server`, `asyncio\.open_connection`, `AF_INET`, `AF_UNIX` | **0** |
| TLS / SSL | `\bssl\b`, `TLSContext`, `wrap_socket`, `create_default_context`, `SSLContext` | **0** |
| Auth | `\bbearer\b`, `\bjwt\b`, `\boauth\b`, `api[_-]?key`, `x509`, `\bsaml\b`, `\boidc\b`, `openidconnect`, `token_validation`, `HTTP[_-]?Basic`, `Authorization\s*:`, `WWW-Authenticate` | **0** |
| Sessions / cookies | `Set-Cookie`, `request\.cookies`, `session_id`, `session_token`, `csrf`, `sessionid` | **0** |
| Rate limiting | `rate[_-]?limit`, `throttle`, `leaky_bucket`, `token_bucket`, `429` | **0** |
| Process supervision | `uvicorn`, `gunicorn`, `hypercorn`, `supervisord`, `systemd`, `launchd`, `win32serviceutil` | **1, denial-only** |

«Denial-only» одиночный hit:
`apps/platform/src/onec_platform/runtime.py:29` — это
**docstring statement**: «it is not a daemon manager /
service manager (no Windows Service / systemd unit
registration on this step)». Это explicit absence
declaration, не implementation reference.

Outbound `urllib.request` usage (зафиксированный
отдельно — это **client-side** outbound HTTP probes
к 1С infobase HTTP-publication endpoint, **не** MCP
transport server):

- `apps/mcp-read-server/src/mcp_read_server/runtime/live_adapter.py:10,19`;
- `packages/onec-health/src/onec_health/checks.py:10,41,59`.

Эти upstream-направленные client probes **не задевают**
MCP transport surface и не входят в Track H scope.

`pyproject.toml` `[project.dependencies]` — **block
отсутствует целиком**. Нет declared runtime dependencies.
Это означает что любая Track H Step 4 implementation,
требующая третьесторонний package, обязана либо
обосновать добавление optional dependencies group, либо
использовать stdlib-only path.

---

## 5. CLASS 1 / 2 / 3 / 4 breakdown

### 5.1 CLASS 1 — already reusable for Track H

Existing surfaces, которые Track H Step 4 implementation
может **переиспользовать as-is** без модификации:

1. **`mcp_common.ToolResult` envelope** (`packages/mcp-common/src/mcp_common/result.py`).
   `ok: bool`, `tool_name: str`, `message: str`,
   `payload: dict | None`. Network transport должен
   использовать тот же serialization map, что и
   `_stdio_transport._serialize_tool_result` для MCP
   `tools/call` response shape — это даёт client-side
   parity между stdio и network paths.
2. **`mcp_common.ToolCallable` type alias** (`packages/mcp-common/src/mcp_common/registry.py`).
   `Callable[..., object]`. Network dispatch принимает
   тот же callable signature, идущий через
   `get_tool(name)(...)` indirection.
3. **`list_tools()` / `get_tool(name)` boundary** в каждом
   из трёх `server.py`. Network dispatch обязан идти
   через эти existing functions; никакого parallel
   registration path; `run_write_flow` discipline для
   write-tools preserved automatically.
4. **`_stdio_transport.py` JSON-RPC 2.0 dispatch logic**
   (`_handle_request`, `_make_error`, `_make_result`,
   `_serialize_tool_result`, MCP method set
   `initialize`/`ping`/`tools/list`/`tools/call`/
   `notifications/initialized`/`notifications/cancelled`).
   Network transport может либо извлечь dispatch core в
   shared private helper (по pattern Track G PATH B), либо
   inline'ить — точное решение Step 3 contract.
5. **CLI flag parsing pattern** (`_build_arg_parser`).
   Network transport должен extend существующий argparse
   shape, не replace его: existing flags `--config-path`,
   `--transport`, `--log-level` сохраняются; new
   `--transport <name>` добавляется как valid choice;
   new transport-specific flags (`--bind`,
   `--auth-token-env` или эквивалент) добавляются как
   conditional на active transport.
6. **`_maybe_load_product_config(path, logger)` config
   loading boundary**. Network transport также может
   опционально грузить product config из `--config-path`
   — если auth config живёт там (Q4 answer), это
   единственный путь.
7. **Track D `${ENV:NAME}` env-substitution pattern**
   (`apps/mcp-write-server/.../binary_dispatch.py:155-167`).
   Bearer token value — никогда literal в committed
   file; всегда через env-substitution. Pattern уже
   готов; Track H либо переиспользует helper, либо
   ship'ит narrow его адаптацию — точное решение Step 3
   contract.
8. **`ProductConfig` additive optional section pattern**.
   `runtime` (Phase 5/Step 3) и `enterprise` (Phase
   6/Step 8) уже доказали backward-compatible additive
   shape. Auth config (Q4) встаёт по тому же pattern.
9. **Three `__main__.py` entrypoints**. Track H Step 4
   расширяет каждый минимально (новая transport branch
   на `args.transport == <new-family>`); existing
   `--transport stdio` default preserved; `main()`
   signature без изменений; `run_main(...)` с
   per-server name + version invocation сохраняется.
10. **`[project.scripts]` console entries**. Не меняются
    Track H — три console entries (`mcp-read-server` /
    `mcp-write-server` / `mcp-intelligence-server`)
    остаются wrapper'ом над `python -m <package>`;
    network transport activates через `--transport
    <name>` flag, не через новый script entry.
11. **Selfcheck + verify-release pipeline**. Track H не
    добавляет новых release-facing checks; existing 8
    checks (registry counts, working tree, git baseline,
    selfcheck status, credential leak guard, credential
    template hygiene) покрывают presence новых files
    implicitly.

### 5.2 CLASS 2 — adjacent but not sufficient

Existing surfaces, которые **выглядят релевантно**, но
**не являются решением** для Track H:

1. **`apps/platform/src/onec_platform/runtime.py`** —
   process orchestration boundary (Phase 5/Step 3 + Phase
   6/Step 6). Запускает operator-declared subprocesses
   через argv, поддерживает per-service log files и
   restart policy. **НЕ MCP transport**: оператор сам
   объявляет, через какой entrypoint и какой argv
   стартовать сервис. Track H ship'ит entrypoint, не
   supervisor; existing `runtime.py` boundary не
   задевается.
2. **`urllib.request` client probes** в
   `live_adapter.py` (read-server) и
   `onec_health/checks.py`. **НЕ MCP transport server**:
   это outbound HTTP **client** к 1С infobase HTTP-
   publication endpoint, фундаментально иная архитектура
   (client probe vs server listener). Никакого reuse не
   возможно.
3. **`scripts/dev/launch.ps1` umbrella** — operator/dev
   umbrella для типовых local actions; явно НЕ стартует
   MCP servers. Track H Step 4 не модифицирует launch.ps1;
   Step 5 может добавить minimal pointer на network-
   transport startup, но это Step 5 territory.
4. **`scripts/release/install.ps1` install fast path** —
   материализует product config; не стартует MCP
   servers. Track H не задевает.
5. **Track D `_redact_password_args`** в
   `binary_dispatch.py`. Pattern shape для redaction
   useful, но scope Track D applies к 1С DESIGNER
   `/P` / `/Pwd` argv positions; bearer token
   redaction для MCP transport auth — narrow
   адаптация, Step 3 contract решит точную shape.
6. **`PROTOCOL_VERSION = "2024-11-05"` constant** в
   `_stdio_transport.py`. Network transport должен
   использовать тот же protocol version (cross-transport
   parity — MCP-aware client должен видеть identical
   `initialize` capabilities независимо от transport).
   Pattern reusable; constant либо вытаскивается в
   shared helper, либо дублируется (Step 3 contract).
7. **`apps/platform/src/onec_platform/loader.py`**
   `bootstrap_product_from_json_file` boundary. Если
   auth config живёт в `ProductConfig` (Q4 answer),
   network transport грузит product config через тот же
   loader — adjacent, useful, но точная wiring shape —
   Step 3 contract.
8. **`PROJECT-STATUS.md` Phase 5 / Step 3 runtime contract**
   ([линии 3884, 4134] упоминают «транспорт MCP (stdio /
   TCP / локальный socket)»). **Adjacent**: это часть
   Phase 5 narrative о том, что product layer **не**
   изобретает MCP transport за серверы; не impl. guidance.

### 5.3 CLASS 3 — concretely missing pieces

Что **точно не существует** в repo сейчас, и что Track H
Step 4 (или supporting Step 3 contract / Step 5 docs)
обязан ship'ить:

1. **Network MCP transport listener.** Никакого HTTP
   server (или WebSocket / SSE / TCP listener) в коде
   нет. Step 4 ship'ит ровно один listener family.
2. **Transport-level error envelope mapping.** Не
   существует mapping JSON-RPC error codes →
   transport-level status (например, JSON-RPC `-32601
   Method not found` → HTTP `404 Not Found` или `200
   OK с error envelope`; auth failure → `401
   Unauthorized` + JSON-RPC error). Step 3 contract
   формализует точный mapping.
3. **Auth header / token presentation contract.** Никакого
   `Authorization: Bearer <token>` extraction в коде нет.
   Step 4 implementation должна prematurely читать
   header, валидировать token, и fail-closed на
   missing / invalid.
4. **Token validation logic.** Никакого `hmac.compare_digest`
   или constant-time compare для tokens сейчас нет в
   transport layer (есть `_resolve_env_token` для
   substitution, но не token validation).
5. **Token redaction in transport-level logs.** Log
   format'у `_stdio_transport._configure_logging` пока
   safe (логирование bearer token не возникает в stdio
   path); network path обязан **никогда** не логгировать
   bearer token в stderr / structured log / audit
   `details` / response envelopes / error messages.
   Step 3 contract формализует точную redaction
   discipline.
6. **CLI flags для network transport.** `--transport
   <new-family>`, `--bind <host:port>`, `--auth-token-env
   <varname>` (или эквивалент) — отсутствуют в существующем
   argparse. Step 3 contract фиксирует точный flag list +
   validation.
7. **`ProductConfig` `auth` (или `transport_network`)
   optional section.** Не существует в `models.py`.
   Step 3 contract фиксирует точную shape (token sources,
   env-substitution forms, validation rules).
8. **`mcp_common._network_transport.py` (или эквивалент)
   underscore-prefixed private helper.** Не существует.
   Step 4 PATH B ship'ит helper; PATH A inline'ит в
   каждый `__main__.py`. Точный путь — Step 3 contract.
9. **Verification protocol для network transport.**
   `--help` exit code check легко делается; sample
   request с valid/invalid token — требует actual
   listener up-and-running. Step 3 contract фиксирует
   точные verification steps для Step 4.
10. **TLS / HTTPS posture statement.** Existing transport
    code stdlib-only; network transport, run без
    reverse proxy в untrusted network — не Track H
    threat model. Step 3 contract фиксирует точный
    deployment expectation (reverse-proxy-trusted-network
    posture; built-in TLS — explicit MAY, не MUST).
11. **Operator-facing wording** про network transport
    surface, threat model, deployment expectation
    (`SECURITY.md`, `docs/release-handoff.md`,
    `README.md`, `apps/platform/README.md`,
    `scripts/dev/*`). Step 5 territory — не задевается
    Step 2.

### 5.4 CLASS 4 — explicitly out-of-scope for Track H

Carry-over из Track H plan §5 — нарушение этого списка
будет scope creep, не валидное расширение Track H:

1. **Full enterprise identity stack:** SSO / SAML / OIDC
   federation / SCIM provisioning / organizational RBAC
   platform / multi-tenant policy engine / per-token
   permissioning / per-tool ACL / per-tenant isolation.
2. **Full zero-trust perimeter:** mTLS-everywhere
   mandatory baseline / service mesh (Istio / Linkerd /
   Consul Connect) / KMS-as-required / vault-as-mandatory
   / secret rotation platform / encrypted-at-rest
   secrets file format.
3. **Web UI / dashboard frontend:** browser-facing
   admin portal / MCP traffic visualization / request-
   response inspector / audit log explorer.
4. **Packaging ecosystem:** `.msi` / `.deb` / signed
   binary distribution / GUI installer / wizard / PyPI
   publication / public registry / wheel publication
   (Track C wheel-build empty constraint preserved).
5. **Full service management ecosystem:** systemd unit
   registration / Windows Service registration /
   `launchd` plist / Docker / Kubernetes deployment
   manifests / `supervisor` / `runit` / `s6` recipes /
   auto-update / orchestration templates / HA / clustering
   / load balancing / hot reload / supervisor daemon
   с restart watcher / background config watcher.
6. **Distributed tracing / observability stack:**
   OpenTelemetry / Jaeger / Prometheus / OpenMetrics
   exporter / structured tracing infrastructure.
7. **New MCP tools.** Registry invariant `read=15 /
   write=25 / intelligence=16` carried through unchanged.
8. **1cv8.exe execution work.** Track H operates на
   process / transport / auth layer уровне; 1cv8 binary
   surface не задействуется ни на одном шаге.
9. **Rollback / AST / multi-version 1С matrix expansion.**
   Track A / E / F territories.
10. **Standalone `apps/platform` entrypoint.** Carry-over
    out-of-scope from Track G Q6.
11. **Real MCP client integration test as closure gate.**
    Recommended но не blocker (наследуется из Track G
    pattern — `--help` exit code + sample request smoke
    sufficient).
12. **GitHub remote push.** Operator action, не часть
    трека.

---

## 6. Q1 resolution — chosen transport family

**Q1 answer (Step 2 directional, finalized in Step 3 contract):
HTTP-based MCP transport, line-delimited HTTP POST + optional
SSE for streaming responses.**

Reasoning grounded in audit evidence (§3 / §4):

1. **Stdlib-only preserved.** Python stdlib `http.server`
   (с `BaseHTTPRequestHandler` + `ThreadingHTTPServer`) +
   `socketserver.ThreadingMixIn` достаточны для
   minimum-viable HTTP listener. WebSocket требует
   третьесторонний `websockets` или `wsproto`; SSE
   server-side требует `sse-starlette` или эквивалент
   (raw stdlib SSE возможен, но fragile, особенно
   client-side reconnect logic). HTTP-only path
   позволяет Track H сохранить Q2-inheritance
   «pure-stdlib baseline» из Track G без принудительного
   `[project.dependencies]` block.
2. **Reverse-proxy ecosystem story.** HTTP as transport
   даёт оператору working TLS-termination posture без
   ship'инга TLS внутри Track H — стандартные nginx /
   Caddy / Apache / cloud LB конфигурации работают
   out-of-the-box. Это переводит TLS из «надо ship'ить»
   в «recommended deployment» — что согласуется с Track
   H §5.2 explicit out-of-scope «mTLS-everywhere
   mandatory baseline». Raw TCP / Unix socket / named
   pipe не имеют такого ecosystem.
3. **MCP-spec compatibility.** Upstream MCP spec уже
   описывает HTTP-with-SSE как canonical network
   transport; existing MCP-aware clients (Claude
   Desktop, MCP CLI) знают, как с ним говорить. Track
   H additive layer over Track G stdio cleanly
   оборачивается в этот стандартный shape.
4. **Reverse-compatible с stdio dispatch core.**
   `_stdio_transport._handle_request` принимает `req:
   dict`, отдаёт `dict | None`. HTTP path парсит
   `request body` → `req: dict`, идёт через тот же
   dispatch, serializes `dict` обратно в `response
   body`. Никакой изменения dispatch logic — только
   transport-уровневая обвязка.
5. **WebSocket / SSE рассмотрены и rejected как Q1
   primary choice.**
   - WebSocket: требует `websockets` PyPI dep (или
     `wsproto`); добавляет full-duplex connection
     lifecycle complexity (heartbeat, reconnect,
     close-frame handling); MCP-spec network transport
     ушёл от WebSocket-only в сторону HTTP+SSE; чистый
     stdlib WebSocket server непосильно дорог.
   - Raw stdlib SSE-only (без HTTP request side):
     fundamentally one-way push — не работает для
     `tools/call` request-response semantics.
   - Unix domain socket / named pipe: deployment story
     ограничена (нет cross-host story, нет reverse-
     proxy ecosystem), threat model сводится к local
     filesystem permission model — это **expansion
     local stdio, не сдвиг к network maturity**, что
     противоречит Track H purpose.
   - Raw TCP: нет ecosystem для TLS termination /
     reverse proxy / authn header convention; фактически
     придётся ship'ить ad-hoc framing — больше
     complexity, чем HTTP, без выигрыша.
6. **Точное HTTP shape (line-delimited POST vs SSE for
   streaming responses)** — Step 3 contract решит. На
   уровне Step 2 audit достаточно зафиксировать family
   = HTTP-based.

### 6.1 Что не зафиксирован Step 2 audit

- Точный shape POST request / response framing
  (single-message-per-POST vs multi-message JSON
  array). Step 3 contract.
- Точные endpoint paths (`/mcp` / `/v1/mcp` / etc.).
  Step 3 contract.
- Точная shape SSE event stream для `tools/call`
  responses (если SSE используется для streaming
  output). Step 3 contract.
- Точный mapping JSON-RPC error codes → HTTP status
  codes. Step 3 contract.
- Concurrent-request handling (sequential per-connection
  vs threaded vs async). Step 3 contract — default
  Track H plan §6 anchor — sequential per-connection
  для simplicity.
- Точное behaviour `initialize` / `ping` / `tools/list`
  / `tools/call` / `notifications/*` методов поверх
  HTTP transport. Step 3 contract.

---

## 7. Q2 resolution — count of transport families

**Q2 answer (Step 2, final): exactly one transport
family.**

Reasoning grounded in audit evidence:

1. **Track H plan §4.2 in-scope statement** прямо
   фиксирует «exactly one» как narrowest honest scope.
2. **Track H plan §6 guardrail #2** перечисляет «exactly
   one transport family» как hard invariant.
3. **Track G precedent.** Track G ship'нул ровно один
   transport (stdio) и сознательно не добавил второй —
   тот же pattern наследуется Track H.
4. **Multi-transport matrix complexity.** Two families
   потребуют Step 3 contract нормализовать cross-
   transport semantics (как клиент выбирает transport
   на runtime, parity matrix между transport behaviours,
   dispatch routing, per-transport auth pattern). Это
   significant additional contract complexity без
   shipping value — каждый дополнительный transport
   family заслуживает собственный track.
5. **Stdio inherited preserved.** Track G stdio surface
   остаётся supported (existing `--transport stdio`
   default flag, existing `_stdio_transport.py`
   helper). С точки зрения user-visible behaviour
   после Track H closure transport count = stdio
   (Track G) + new HTTP (Track H) = 2 user-facing
   transports, но **в scope Track H работа ведётся
   только над одним новым family**. Это критическое
   разделение: Track H **adds** один, не **manages**
   суммарно два.

### 7.1 Что не зафиксирован Step 2 audit

- Track H **может** в будущем расшириться до multi-
  transport (например, Track I — WebSocket, Track J
  — TCP). Но это explicitly post-Track-H decisions;
  Step 2 фиксирует только current count.

---

## 8. Q3 resolution — chosen auth baseline

**Q3 answer (Step 2 directional, finalized in Step 3 contract):
static bearer token presented в HTTP `Authorization: Bearer
<token>` header, validated against operator-supplied valid
token list через constant-time comparison, fail-closed на
missing / empty / invalid token.**

Reasoning grounded in audit evidence:

1. **Minimum real security perimeter.** Static bearer —
   первый шаг от «no auth» к real perimeter; не
   декоративный; fail-closed semantics implementable
   stdlib-only (`hmac.compare_digest` для constant-time
   compare).
2. **HTTP transport native fit.** Bearer token presents
   в standard HTTP header; не требует custom framing,
   не требует additional handshake. Reverse proxy-friendly
   (header passthrough — стандартное поведение nginx /
   Caddy / Apache / cloud LB).
3. **Stdlib-only.** `hmac.compare_digest` доступен в
   stdlib без `[project.dependencies]`. JWT / OAuth /
   OIDC требуют PyPI dependencies (`pyjwt`,
   `authlib`, `oauthlib`) — Track H §5.1 explicit
   out-of-scope.
4. **Track D credential pattern переиспользуется.**
   Bearer token value — никогда literal в committed
   file; всегда через `${ENV:NAME}` env-substitution
   (Track D / Step 3 pattern,
   `apps/mcp-write-server/.../binary_dispatch.py:155-167`).
   Operator-managed secret path — single discipline
   через весь project.
5. **Fail-closed semantics.** Missing
   `Authorization` header → `401 Unauthorized` + MCP
   error envelope; mismatched token → `401 Unauthorized`
   + MCP error envelope; никакого partial acceptance,
   никакого silent bypass, никакого «empty token =
   anonymous».
6. **Non-goals.** Track H **не** делает per-token
   permissioning, per-tool ACL, per-tenant isolation,
   token introspection endpoint, OAuth flow,
   refresh tokens, token rotation policy. Single-tier
   auth — valid token → access full registry.
7. **Альтернативы рассмотрены и rejected как Q3
   primary choice.**
   - **API key as query param / config-only:** менее
     standard, не header-canonical, легче утекает в
     access logs.
   - **HMAC request signing:** добавляет per-request
     signature complexity; полезно когда token
     рассматривается как long-lived; для Track H
     minimum-viable scope — overkill.
   - **HTTP Basic auth:** уже близок к bearer, но
     credentials-pair (username + password) shape
     сложнее env-substitution; единый bearer token
     честнее single-tier model'у.
   - **mTLS:** §5.2 explicit out-of-scope (mandatory
     mTLS-everywhere — separate post-Track-H track).

### 8.1 Что не зафиксирован Step 2 audit

- Точный list valid tokens (один shared token vs
  список tokens). Step 3 contract.
- Token rotation discipline (does config reload
  pick up new token? does operator restart server?).
  Step 3 contract.
- Точная error envelope shape для auth failure
  (HTTP status code + JSON-RPC code + message
  redaction). Step 3 contract.
- TLS posture statement (operator's reverse proxy
  responsibility vs built-in optional TLS listener).
  Step 3 contract.

---

## 9. Q4 resolution — chosen auth config home

**Q4 answer (Step 2 directional, finalized in Step 3 contract):
existing `ProductConfig` model, extended with new optional
`auth` (или `transport_network`) section; bearer token value
обязательно через `${ENV:NAME}` env-substitution, никогда
literal в committed file. Complementary CLI flag
`--auth-token-env <varname>` для operator override.**

Reasoning grounded in audit evidence:

1. **Pattern уже доказан.** `ProductConfig` имеет два
   precedent additive optional sections (`runtime`
   Phase 5/Step 3, `enterprise` Phase 6/Step 8) с
   `field(default_factory=...)`. Pre-Track-H configs
   продолжают грузиться без изменений; добавление
   третьего optional section follows established
   pattern.
2. **Single source of truth.** Existing operator
   workflow — `--config-path` указывает на product
   config JSON, `bootstrap_product_from_json_file`
   грузит его. Auth config в том же месте — никакого
   parallel config path; никакого «auth config где-то
   в другом файле».
3. **Track D env-substitution discipline reused.**
   Bearer token value — через `${ENV:NAME}` form,
   проверенный fail-closed на missing/empty/partial-
   mixed forms. Existing `verify-release.ps1` Check 8
   (credential template hygiene) уже scan'ит config
   files; pattern может extend'иться на auth section
   без изменения guard logic core (fine-tuning Step 3
   contract / Step 5 docs alignment).
4. **CLI flag complementary, not replacement.**
   `--auth-token-env <varname>` — позволяет operator
   override env-var name на runtime без изменения
   config file (полезно для local dev / testing).
   Существующий `--config-path` flag preserved;
   точная wiring — Step 3 contract.
5. **No vault platform as baseline.** Track H §5.2
   explicit out-of-scope — KMS / HashiCorp Vault /
   AWS Secrets Manager / OS keychain integrations.
   Operator-managed secret path — sufficient для
   trusted-network Track H threat model. Если
   operator хочет vault-backed token, оператор
   feed'ит env var из своей vault infrastructure
   ДО запуска сервера — единый pattern с DESIGNER
   credentials через Track D.
6. **Альтернативы рассмотрены и rejected как Q4
   primary choice.**
   - **CLI-only (no config file):** не масштабируется
     если operator хочет multiple auth tokens, или
     transport-specific тонкая настройка; unifies
     bad с existing config-driven flow.
   - **Dedicated separate auth config file:** parallel
     config path; нарушает single-source-of-truth
     discipline; complicate `--config-path` semantics.
   - **Env-only (no config schema entry):** теряется
     declarative shape; operator не видит full server
     config в одном файле; нарушает «product config
     describes everything operator declared» pattern.
   - **Secrets vault integration as baseline:**
     §5.2 explicit out-of-scope; preserves option for
     post-Track-H tracks без блокировки этой track'а.

### 9.1 Что не зафиксирован Step 2 audit

- Точные key names в `auth` section (`tokens` /
  `valid_tokens` / `bearer_tokens`). Step 3 contract.
- Loader validation rules (точный fail-closed shape
  на missing env / empty token / malformed config).
  Step 3 contract.
- Backward compat: configs без `auth` section
  продолжают грузиться, но `--transport <network>`
  без auth config → fail-closed на startup. Step 3
  contract фиксирует точную error message + exit
  code.
- Interaction with existing `--config-path` (auth
  config обязателен только если `--transport
  <network>` active; для `--transport stdio` auth
  config ignored). Step 3 contract.

---

## 10. Step 3 handoff note

Step 3 (network transport / auth contract, docs-only)
обязан formalize следующий список normative items на
основе этого Step 2 audit, чтобы Step 4 implementation
не импровизировал:

1. **Transport family normative.** RFC 2119-style
   `MUST` / `MUST NOT` для:
   - exact transport family = HTTP-based (per Q1);
   - exact framing (POST + SSE for streaming, or
     POST-only — final choice in Step 3 contract);
   - exact endpoint paths;
   - exact MCP method coverage (`initialize` / `ping`
     / `tools/list` / `tools/call` / `notifications/*`
     — same set as `_stdio_transport.py`);
   - exact JSON-RPC error → HTTP status mapping;
   - exact concurrent-request semantics (default
     sequential per-connection per Track H plan §6);
   - exact lifecycle (request validation → auth check
     → dispatch → response serialization);
   - forbidden transports (WebSocket / SSE-only /
     TCP / Unix socket / named pipe — explicit out
     of scope per Q2 single-family rule).
2. **Auth contract normative.**
   - exact token presentation form
     (`Authorization: Bearer <token>` header per Q3);
   - exact token validation (constant-time compare
     via `hmac.compare_digest`);
   - exact fail-closed semantics на missing /
     empty / invalid token (HTTP 401 + JSON-RPC
     error envelope shape);
   - exact redaction discipline (token never logged
     to stderr / structured logs / response
     envelopes / error messages / audit `details`);
   - forbidden auth shapes (JWT / OAuth / OIDC /
     SAML / mTLS-mandatory — per Q3 / §5.1 / §5.2).
3. **Config schema normative.**
   - exact `ProductConfig` `auth` section shape
     (per Q4);
   - exact key names + types + validation rules;
   - exact backward-compat: configs без `auth`
     section + `--transport stdio` → загружаются
     unchanged; `--transport <network>` без auth
     config → fail-closed startup;
   - exact interaction с existing `${ENV:NAME}`
     pattern (Track D inheritance; new section
     обязан следовать той же substitution
     discipline);
   - new CLI flag `--auth-token-env <varname>`
     (или эквивалент);
   - existing CLI flags `--config-path` /
     `--transport` / `--log-level` preserved.
4. **`mcp_common` integration normative.**
   - new private underscore-prefixed helper
     (например, `mcp_common._network_transport`) —
     **NOT** в `__init__.py`'s `__all__`;
   - exact `mcp_common/__init__.py` byte-identical
     preservation (no exports added / removed /
     renamed);
   - dispatch core либо извлекается в shared
     private helper, либо дублируется (PATH B vs
     PATH A — final choice in Step 3 contract на
     основе duplication-reduction estimate, по
     Track G precedent).
5. **`__main__.py` integration normative.**
   - additive new transport branch на
     `args.transport == <network>` без удаления
     existing `--transport stdio` default;
   - existing `main()` signature preserved;
   - existing `run_main(...)` invocation preserved
     для stdio path;
   - exact branch shape (early-validation +
     dispatch + exit code) для network path.
6. **`pyproject.toml` posture normative.**
   - existing `[project.scripts]` 3 entries
     preserved;
   - existing `[tool.hatch.build.targets.wheel]
     packages = []` preserved (Track C carry-
     through);
   - **default — никакого `[project.dependencies]`
     block**; если Step 3 contract выбирает
     stdlib-only HTTP path, dep block остаётся
     отсутствующим. Если Step 3 contract принимает
     решение допустить optional HTTP/TLS/auth
     dependencies — **только optional**, через
     `[project.optional-dependencies]`, в narrow
     extras group (например, `network`); никаких
     mandatory deps; exact shape — Step 3 contract
     обязан justifry evidence-grounded.
7. **Backward compatibility normative.**
   - registries `read=15 / write=25 /
     intelligence=16` byte-identical;
   - `mcp_common.__init__.py` `__all__`
     byte-identical;
   - existing `_stdio_transport.py` public shape
     byte-identical;
   - existing three `__main__.py` `main()`
     signatures byte-identical;
   - existing three `server.py` files
     byte-identical;
   - existing CLI flag set (`--help` /
     `--config-path` / `--transport` /
     `--log-level`) preserved;
   - existing `tools.py` / `models.py` /
     `runtime/*` packages byte-identical;
   - `apps/platform/*` byte-identical (Q6
     carry-over);
   - audit row `details` shape byte-identical;
     `run_write_flow` discipline preserved.
8. **Step 4 allowed file surfaces.**
   - new `mcp_common._network_transport.py`
     (или эквивалент underscore-prefixed name);
   - additive minor extensions в трёх
     `__main__.py`;
   - `pyproject.toml` only if Step 3 contract
     допускает optional `[project.optional-dependencies]`
     extras group (default — без изменений);
   - new optional `auth` section в
     `apps/platform/src/onec_platform/models.py`
     `ProductConfig` + соответствующая loader
     wiring в `loader.py` (если Q4 / Step 3
     contract это требует);
   - **точный финальный список** — Step 3
     contract.
9. **Step 4 forbidden file surfaces.**
   - registry contents (никаких новых MCP tools);
   - `tools.py` всех серверов;
   - `runtime/*` packages всех серверов;
   - `mcp_common/__init__.py` `__all__`;
   - `_stdio_transport.py` (сохраняется как-есть);
   - `scripts/*`;
   - `examples/*`;
   - documentation за пределами `PROJECT-STATUS.md`
     (Step 5/6 territory) и track-h docs themselves;
   - `SECURITY.md` / `CHANGELOG.md` /
     `docs/release-handoff.md` / `apps/platform/README.md`
     (Step 5/6 territory);
   - track-h planning / audit / contract docs
     (frozen Step 1/2/3 anchors).
10. **Verification protocol для Step 4.**
    - `python -m mcp_read_server --transport stdio
      --help` → exit 0 + non-empty usage (existing
      path preserved);
    - `python -m mcp_read_server --transport <network>
      --help` → exit 0 + non-empty usage (new path);
    - sample HTTP request с valid bearer token →
      success path, valid JSON-RPC envelope;
    - sample HTTP request с missing/invalid bearer
      → fail-closed (точная shape — Step 3 contract);
    - existing `verify-release.ps1 -AllowDirtyTree`
      GREEN на 8 checks;
    - selfcheck `read=15 / write=25 / intelligence=16
      ; status=ok`;
    - `imports_ok=true`;
    - никаких 1cv8.exe runs;
    - никаких real credentials в diff;
    - никаких MCP tool registry changes.

---

## 11. Honest summary

После Step 2 (этот audit ship'нут отдельным commit'ом):

**Что доказано read-only inspection'ом:**

- Никакого network MCP transport / auth кода в
  `apps/*/src/` или `packages/*/src/` нет (zero-hits
  grep по 8 категориям паттернов).
- Существующий Track G stdio surface полный, рабочий,
  reusable (CLASS 1 — 11 surfaces).
- Существующие adjacent surfaces не являются решением
  (CLASS 2 — 8 surfaces; client-side urllib +
  product-runtime supervisor + scripts/dev/launch +
  Track D pattern + others).
- Concretely missing pieces инвентаризованы (CLASS 3 —
  11 items).
- Out-of-scope items зафиксированы (CLASS 4 — 12
  items, carry-over из Track H plan §5).

**Что зафиксировано как Step 2 directional answer
(финал — Step 3 contract):**

- Q1 = HTTP-based MCP transport (line-delimited POST +
  optional SSE).
- Q2 = exactly one transport family.
- Q3 = static bearer token via `Authorization: Bearer
  <token>` header, constant-time validation, fail-closed.
- Q4 = `ProductConfig.auth` optional section + Track D
  `${ENV:NAME}` env-substitution + complementary
  `--auth-token-env` CLI flag.

**Что только planned, не доказано:**

- Точная HTTP framing shape (Step 3 contract).
- Точный CLI flag list (`--bind` / `--auth-token-env` /
  др.) (Step 3 contract).
- Точный `auth` config schema shape (Step 3 contract).
- Точный `_network_transport.py` helper shape (Step 3
  contract / Step 4 implementation).
- Точная operator-facing wording (Step 5).
- Точное Q7 closure decision (Step 6 на основе фактического
  Step 4 functional delta).

**Чего всё ещё нет в repo на момент Step 2 closure:**

- Никакого network listener в коде.
- Никакого auth header extraction в коде.
- Никакого token validation в коде.
- Никаких новых CLI flags.
- Никакого `auth` config schema.
- Никаких новых dependencies.
- Никаких изменений в `pyproject.toml` (`version=0.4.0`
  preserved).
- Никаких изменений в registries (`read=15 / write=25 /
  intelligence=16`).
- Никаких изменений в `mcp_common` public API.
- Никаких изменений в operator-facing docs за пределами
  Track H planning + audit + step-map.

Track H после Step 2 остаётся **planning/audit-only**.
Implementation первый и единственный раз появляется на
Step 4. Step 3 contract фиксирует точные правила, по
которым Step 4 implementation сможет работать без
импровизации.
