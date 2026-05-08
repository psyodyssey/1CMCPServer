# Parallel Track G — Production-Grade MCP Transport and CLI (plan)

> **Companion file:** `track-g-production-grade-mcp-transport-and-cli-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 4 —
> отдельный заход; единственный шаг трека с production code
> change.

---

## 1. Зачем нужен Track G после Track F

После closure'а Track F (Rollback Whitelist Expansion) у проекта
есть сильное execution-ядро (Phase 1–6) + сильная docs/product
shell (Tracks B/C/D/E) + расширенная rollback coverage (Track F),
но **operational run story для MCP servers всё ещё не доведена
до production-grade состояния**. Этот gap уже зафиксирован как
honest constraint в нескольких местах repository:

- `SECURITY.md` стр. ~40: «No production-grade MCP transport
  yet. The three MCP servers are intended for local / controlled
  use. There is no built-in authentication, authorisation,
  multi-tenant isolation, or hardened network transport.»
- `docs/release-handoff.md` Known limitations: «No
  production-grade MCP transport. Treat the servers as you would
  any local development service.»
- `README.md` Quickstart «Что Quickstart **не** обещает»:
  «production-grade MCP transport (нет authentication /
  authorisation / network hardening)».
- Track A / D plan + Phase 6 docs + Track F closure
  recommendation — все упоминают «production-grade MCP transport
  / `__main__` / CLI у трёх MCP-серверов» как next parallel
  track candidate.

Concrete gaps:

1. **Никакой `__main__.py`** ни в одном из 4 packages
   (`mcp_read_server`, `mcp_write_server`,
   `mcp_intelligence_server`, `onec_platform`) — оператор не
   может сделать `python -m mcp_read_server`.
2. **Никакой `[project.scripts]`** console entry points в
   `pyproject.toml` — нет installable CLI binaries.
3. **Никакой MCP protocol implementation** — `server.py`
   содержит только `list_tools()` / `get_tool(name)` boundary;
   реальный JSON-RPC framing + stdio loop отсутствует.
4. **Никакой CLI surface** (`--help`, `--config-path`,
   `--transport`, `--log-level`).
5. **Никакой operator-facing «how to start MCP server in
   production» SSOT runbook**.

Track G — отдельный узкий парallel track, который ship'ит
**первый production-grade слой** этого operational gap'а:
canonical entrypoints + minimal stdio transport + CLI surface.
Это **не** «полный production-grade transport solution»
сразу — это **первый сильный baseline**, поверх которого
будущие parallel tracks могут добавить HTTP/network transports,
authentication, supervision daemons и т.д.

## 2. Стартовая точка

### 2.1 Текущее состояние server packages

- `apps/mcp-read-server/src/mcp_read_server/server.py` —
  registry skeleton: 15 tools registered; `list_tools()` /
  `get_tool(name)` boundary; **no `__main__.py`**.
- `apps/mcp-write-server/src/mcp_write_server/server.py` —
  registry skeleton: 25 tools registered; **no `__main__.py`**.
  Module docstring явно: «Skeleton server bootstrap... Real
  MCP transport, policy enforcement, backup/dump/apply/verify
  flows will be added later.»
- `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py` —
  registry skeleton: 16 tools registered; **no `__main__.py`**.
- `apps/platform/src/onec_platform/` — product layer; не MCP
  server по архитектуре, но имеет related runtime layer (см.
  ниже).

### 2.2 Existing process orchestration layer

`apps/platform/src/onec_platform/runtime.py` (Phase 5 / Step 3
+ Phase 6 / Step 6 hardening):

- `start_product_runtime(...)` / `stop_product_runtime(...)` /
  `get_product_runtime_status(...)` / `reload_product_runtime(...)` —
  long-lived **product service** orchestration через
  operator-declared argv в `runtime.services` config section;
- structured `stdout` / `stderr` logs под
  `<work_dir>/.runtime/logs/<service>.{out,err}.log` с
  rotate-if-exceeds-size (default 1 MiB);
- `restart_policy ∈ {"never", "restart-if-stale"}` (default
  `"never"`); boundary-only invocation, нет background
  watcher'а;
- persisted `runtime-state.json` с PID liveness tracking.

**Это generic process management abstraction**; она MCP servers
**не запускает** напрямую (нет `__main__` чтобы запустить), но
после Track G implementation (когда `__main__` появится),
operator может объявить `runtime.services` entries для каждого
MCP server и использовать existing runtime layer без изменений.

### 2.3 Existing scripts / wrappers

- `scripts/dev/launch.ps1` — operator/dev umbrella:
  `selfcheck` / `repl` / `run` / `help` subcommands. Это
  **dev-side wrapper** для adhoc Python invocation, не для MCP
  server start.
- `scripts/dev/bootstrap_paths.ps1` — PYTHONPATH bootstrap.
- `scripts/dev/run_dev_check.ps1` / `scripts/dev/selfcheck.py` —
  CI-aligned health verification.
- `scripts/release/install.ps1` / `verify-release.ps1` —
  product config materialization + release verify.

**Никакого `start-mcp-server.ps1` или эквивалентного script'а
для MCP server standup сейчас нет.**

### 2.4 Tool registries (Track G не задевает)

- `mcp-read-server` — 15 public tools.
- `mcp-write-server` — 25 public tools.
- `mcp-intelligence-server` — 16 public tools.

Track G **MUST NOT** менять эти counts. Single source of truth —
`server.py:REGISTERED_TOOLS` / `list_tools()`. Track G ship'ит
transport/entrypoint **поверх** этих registries, не задевая их.

## 3. Gap / problem statement

**Операционный gap** сегодня:

1. **Cannot start any MCP server.** Без `__main__.py`,
   `python -m mcp_read_server` не работает; без MCP protocol
   implementation, даже если получится import'ить server.py,
   никакого JSON-RPC framing нет.
2. **No canonical CLI.** Operator не имеет single command для
   server invocation; нет `--help`, `--config-path`,
   `--transport`, `--log-level`.
3. **No installable entry points.** `pyproject.toml` не
   объявляет `[project.scripts]`; даже если бы wheel build
   работал, не было бы binaries в `bin/`.
4. **No production-run SSOT.** `apps/platform/README.md`,
   `docs/operator-manual.md`, `docs/runbooks.md` всё описывают
   `selfcheck` flow, но не «как поднять servers в работающее
   состояние».
5. **Existing runtime layer не может быть использован**
   операторами для MCP servers — потому что нет executable
   entrypoint, который operator может объявить в
   `runtime.services` argv-template.

**Track G закрывает первый этого gap'а:** ship'ит canonical
`__main__` + minimal stdio transport + CLI + console entry
points. **Не больше.** Network / HTTP / auth / supervision —
остаются отдельными parallel tracks post-Track G.

## 4. Целевой результат

После closure Track G у проекта есть:

1. **Canonical `__main__.py`** для трёх MCP servers
   (`mcp_read_server`, `mcp_write_server`,
   `mcp_intelligence_server`). `python -m <server>` работает.
2. **Minimal CLI surface** для каждого server'а: `--help`,
   `--config-path <path>`, `--transport stdio` (default + only
   supported в Step 4), `--log-level {DEBUG,INFO,WARNING,ERROR}`.
3. **Minimum-viable stdio MCP transport** — JSON-RPC 2.0 over
   stdin/stdout с line-delimited JSON framing. Existing
   `list_tools()` / `get_tool()` registry интегрирован как
   server-side handler. **No HTTP/WebSocket/SSE.**
4. **`[project.scripts]` console entry points** в
   `pyproject.toml` — installable binaries (`mcp-read-server` /
   `mcp-write-server` / `mcp-intelligence-server`); запускаются
   `python -m`-эквивалентно через wheel install.
5. **Aligned operator-facing docs** — Quickstart upd,
   `docs/release-handoff.md` обновлены под new entrypoints;
   short runbook section / launch.ps1 update под start
   command.
6. **No security claim beyond local trusted environment.**
   Track G явно фиксирует, что transport — local-only, no
   auth, no network hardening; production deployment beyond
   trusted local — отдельный track.

## 5. Что входит в Track G

- Step 1 — planning (этот заход): plan + step-map docs +
  minimal README / PROJECT-STATUS update.
- Step 2 — transport / entrypoint baseline audit (docs-only):
  descriptive per-server inventory + где integration point
  для MCP protocol; resolve Q1 (transport choice).
- Step 3 — exact runtime / CLI / entrypoint contract
  (docs-only): prescriptive normative contract — `__main__`
  shape, CLI surface, transport choice, auth posture
  (none-on-transport), supervision integration (через existing
  product runtime), exclusions.
- Step 4 — narrow implementation slice: production code change.
  Добавление `__main__.py` для трёх MCP servers + minimal
  stdio JSON-RPC transport + CLI argument parsing +
  `[project.scripts]` entries в `pyproject.toml`.
- Step 5 — operator/docs alignment: Quickstart + handoff +
  launch.ps1 + new short runbook про "how to start MCP servers"
  pointing на new entrypoints.
- Step 6 — final integration pass + Track G closure (Q7 —
  version bump 0.3.0 → 0.4.0; default ДА).

## 6. Что НЕ входит в Track G (deliberately)

**Out-of-scope categorically, никаких скрытых гэпов:**

- **HTTP / WebSocket / SSE network transports** — Track G ship'ит
  только stdio. Network transports — **отдельный subsequent
  parallel track** (e.g. Track H — Network MCP Transport);
- **Authentication / authorization** на transport уровне —
  никаких token validation, mTLS, OAuth, SAML, OpenID
  Connect, RBAC, multi-tenant isolation. Security model = trusted
  local environment;
- **Supervision daemon** — никакого background watcher'а,
  systemd/Windows Service registration, automatic restart
  daemon. Track G integrates с existing
  `apps/platform/runtime.py` boundary (Phase 5 / Step 3 + Phase 6
  / Step 6) — без расширения этого layer'а;
- **HA / multi-node / cloud control plane** — single-process per
  server; no clustering;
- **Service discovery / load balancing** — single-instance;
- **Distributed tracing / observability stack** —
  `--log-level` flag только; structured tracing — отдельный
  track;
- **Web UI / dashboard frontend** — Track G чисто backend
  transport;
- **Packaging ecosystem** (`.msi` / `.deb` / GUI installer /
  signed distribution / wheel publication к PyPI) — отдельный
  track (Track C honest constraint остаётся);
- **Full enterprise super-set** (SSO/RBAC/multi-tenant/secrets
  vault as service/federated audit/policy-as-code DSL) —
  отдельный enterprise track;
- **1cv8.exe execution work** — Track A territory;
- **Rollback work** — Track F territory;
- **AST / metadata work** — отдельные technological tracks;
- **Multi-version 1С matrix expansion** — Track E territory;
- **New MCP tools** — registries `read=15 / write=25 /
  intelligence=16` **MUST** остаться без drift'а; Track G
  поверх existing tool surface, не extend'ит её;
- **`apps/platform`** standalone server entrypoint — это
  product layer, не MCP server; `__main__` для него — отдельное
  обсуждение out-of-scope Track G initial scope (можно
  рассмотреть как Q-расширение в Step 2);
- **Hot reload** — никакой server restart-on-config-change;
- **Remote push** — operator action, не часть трека.

## 7. Guardrails

- **No new MCP tools.** Registries без drift'а на каждом step.
- **No registry-content changes.** `server.py:REGISTERED_TOOLS`
  для всех 3 servers **MUST** остаться identical: identical
  tool names, identical lookup functions, identical tool
  callable signatures.
- **No back-door write channel.** Track G transport — pure
  read/forward (server side dispatches к existing tools);
  никаких новых mutating paths не вводится.
- **No 1cv8.exe runs anywhere в треке.** Track G работает на
  process / transport layer; 1cv8 binary surface не задействуется.
- **Production code touches:** только Step 4. Files допустимы:
  `apps/mcp-read-server/src/mcp_read_server/__main__.py` (new),
  `apps/mcp-write-server/src/mcp_write_server/__main__.py` (new),
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
  (new), `pyproject.toml` (new `[project.scripts]` block +
  optional version bump на Step 6). Optional minor:
  `server.py` для каждого MCP server (если minor adjustments
  для transport integration требуются — preferred minimal
  touch).
- **No code change в product layer / packages / scripts /
  registries** outside Step 4 explicit allowed surfaces.
- **No real credentials в repo / docs / commit messages.**

## 8. Acceptance criteria (closure)

Track G закрыт, если **все** ниже выполнены:

1. Step 1–6 пройдены последовательно; linear git history
   Step 1 → 2 → 3 → 4 → 5 → 6.
2. Step 2 baseline audit doc на диске.
3. Step 3 contract doc на диске (RFC 2119-style normative).
4. Step 4 ship'ит:
   - `__main__.py` для трёх MCP servers;
   - minimal stdio transport implementation;
   - minimal CLI flag parsing (`--help`, `--config-path`,
     `--transport`, `--log-level`);
   - `[project.scripts]` entries в `pyproject.toml`.
5. После Step 4: `python -m mcp_read_server --help`,
   `python -m mcp_write_server --help`, `python -m
   mcp_intelligence_server --help` все работают (отображают
   short usage без crash'а).
6. Step 5 operator-facing docs (Quickstart + handoff +
   launch.ps1) aligned под new entrypoints.
7. Registries `read=15 / write=25 / intelligence=16` без
   drift'а на всём треке; selfcheck_status=ok.
8. `verify-release.ps1` GREEN на 8 checks (без новых
   release-side checks; existing checks 1–8 покрывают новые
   files как «present» где applicable).
9. Никаких `1cv8.exe` runs ни на одном шаге Track G.
10. Никаких real credentials в Track G commits.
11. Honest non-goals явно зафиксированы в closure docs:
    no network transport, no auth, no supervision, no HA, no
    web UI, no packaging.

## 9. Honest constraints after closure

Даже после Track G closure **остаётся**:

- **No network transport.** Servers всё ещё local-only через
  stdio. Operator может connect только через MCP-aware client
  на той же machine.
- **No authentication / authorization** на transport уровне.
  Security model = «trusted local environment»; servers
  treated как local development services.
- **No supervision daemon.** Existing
  `apps/platform/runtime.py` boundary (start/stop/status/reload)
  работает без background watcher'а; restart policy
  `"restart-if-stale"` срабатывает только на boundary calls.
- **No service discovery / load balancing / clustering / HA.**
- **No production-grade observability** (нет distributed
  tracing, нет log aggregation, нет metrics endpoint).
- **No web UI.**
- **No packaging ecosystem** beyond `[project.scripts]` console
  entries (no `.msi`, no `.deb`, no signed distribution, no
  PyPI publication).
- **No enterprise super-set** (SSO/RBAC/multi-tenant/secrets
  vault as service / federated audit / policy-as-code DSL).
- **No multi-instance configuration** — single process per
  server invocation.
- **No hot reload.**

Track G **только** перевёл platform с «MCP servers cannot start
at all» на «MCP servers can start in trusted local mode via
stdio». Это first practical baseline — большой step forward от
«registry skeleton», но **не** «full production deployment
ready».

## 10. Связь с Track A / B / C / D / E / F

- **Track A** ship'нул real binary-backed write path; Track G
  не задевает 1cv8 execution.
- **Track B** ship'нул repo hygiene + dev launch umbrella;
  Track G дополнит operator scripts new MCP server start
  command, но не реструктурирует existing dev wrappers.
- **Track C** ship'нул release verify + handoff docs +
  packaging honest review; Track G использует
  `verify-release.ps1` как есть; new entrypoints должны
  pass'ить existing checks.
- **Track D** ship'нул env-substitution credentials path;
  Track G respects ту же `${ENV:NAME}` substitution
  для любых credentials в server config (если CLI
  `--config-path` указывает на product config).
- **Track E** ship'нул multi-version smoke matrix scaffolding;
  Track G не задевает version evidence layer; Track G
  servers могут запускаться на любой 1С version, потому что
  они не запускают 1cv8 binary напрямую.
- **Track F** ship'нул rollback whitelist expansion; Track G
  не задевает rollback model; новые transport не вводят new
  mutating paths.

Track G — **третий post-Phase-6 track, который меняет
production code** (после Track A binary_dispatch и Track D
env-substitution + verify check 8 и Track F rollback whitelist).
В отличие от Track A/D/F (single-line или narrow code changes),
Track G Step 4 ship'ит **новые файлы** (`__main__.py` × 3) +
содержательный stdio transport implementation. Это самый
крупный single-step code change среди всех Track A–G **на
момент написания этого plan'а**, что делает eligibility
contract Step 3 особенно важным.

## 11. Open questions (Step 2+)

- **Q1 — transport choice для Step 4.** Default candidate:
  **stdio only** (line-delimited JSON-RPC 2.0 over stdin/stdout).
  Reasoning: minimum-viable production model для local trusted
  environment; не требует network stack; cleanly closes
  initial gap «cannot start at all»; consistent с typical MCP
  client integration patterns (Claude Desktop, MCP CLI tools)
  которые ожидают stdio transport. HTTP / WebSocket / SSE —
  явно out-of-scope (subsequent track). Resolve финально в
  Step 2.
- **Q2 — `mcp` Python SDK или custom implementation.** Default
  candidate: **зависит от availability в dependency graph**.
  Если `mcp` Python SDK lightweight enough и не вводит
  объёмных transitive deps — использовать его (производственно-
  правильный path). Если — write minimal JSON-RPC + stdio loop
  on stdlib only (≤ 200 lines per server). Resolve финально в
  Step 2 с manual code review SDK shape.
- **Q3 — CLI flag set.** Default minimal: `--help`,
  `--config-path <path>` (optional, для product config
  loading), `--transport stdio` (default + only supported в
  Step 4), `--log-level {DEBUG,INFO,WARNING,ERROR}` (default
  `INFO`). Никаких additional flags на initial Step 4.
  Resolve финально в Step 3.
- **Q4 — auth posture.** Default: **none на transport уровне.**
  Security model = trusted local environment. Документирован
  как honest constraint. Authentication — **отдельный
  post-Track-G track**. Resolve финально в Step 3.
- **Q5 — supervision integration.** Default: **через existing
  `apps/platform/runtime.py` boundary** (Phase 5 / Step 3 +
  Phase 6 / Step 6). После Step 4 ship'ит executable
  entrypoints, operator может объявить MCP servers в
  `runtime.services` config section и использовать
  `start_product_runtime` / `stop_product_runtime` без
  изменений в runtime layer. **Никакого нового supervision
  daemon Track G не ship'ит.** Resolve финально в Step 3.
- **Q6 — `apps/platform` standalone entrypoint.** Default:
  **out-of-scope initial Track G.** `apps/platform` — product
  layer, не MCP server по архитектуре; CLI для product
  operations (install / verify / status) уже частично покрыт
  через `scripts/release/install.ps1`. Расширение `__main__`
  для product layer — possible Q-extension в Step 2 audit
  если operator demand явный; default НЕТ. Resolve финально
  в Step 2.
- **Q7 — closure version bump 0.3.0 → 0.4.0 на Step 6.**
  Default: **ДА.** Step 4 ship'ит real production code change
  с functional delta — `python -m mcp_*_server` теперь работает,
  console entry points добавляются, stdio transport
  доступен. Это backward-compatible new functionality (existing
  registry contracts preserved; tool counts preserved).
  Classic MINOR bump per SemVer. Direct precedent — Track D
  `0.1.0 → 0.2.0` и Track F `0.2.0 → 0.3.0` shipped real
  code changes; Track G logically continues этот pattern.
  Resolve финально в Step 6.
