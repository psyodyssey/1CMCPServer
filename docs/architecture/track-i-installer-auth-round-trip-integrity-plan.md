# Parallel Track I — Installer Auth Round-Trip Integrity (plan)

> **Companion file:**
> `track-i-installer-auth-round-trip-integrity-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 4 —
> отдельный заход; единственный шаг трека с production code
> change.

---

## 1. Зачем нужен Track I после Track H

После closure'а Track H (Network-Grade MCP Transport and
Authentication Boundary; commit `436febc`, project version
`0.5.0`) у проекта есть второй слой зрелости: HTTP/1.1 `/mcp`
endpoint с static bearer authentication, additive поверх Track G
stdio baseline. Operator-supplied auth tokens живут в
`ProductConfig.auth.tokens` как `${ENV:NAME}` env-substitution
строки; loader валидирует их fail-closed на load-time.

Но при closure Track H был honestly зафиксирован один **узкий
operator-facing gap**, который не закрывался в самом Track H:

> `apps/platform/src/onec_platform/installer.py:_config_to_dict`
> does not yet emit the new `auth` section, so a config round-
> tripped through `scripts/release/install.ps1 ... -Confirm`
> silently loses its `auth.tokens` declarations. Operators using
> `--transport http` against a round-tripped config get a clean
> fail-closed startup ("`--transport http requires
> --auth-token-env or auth.tokens in product config`") and either
> re-add the section by hand or use `--auth-token-env <VARNAME>`
> to bypass the config. Future post-Track-H fix to
> `_config_to_dict` is analogous to the Phase 6 / Step 9 service-
> level + enterprise round-trip fix.

(Источник цитаты: `CHANGELOG.md` `## 0.5.0` honest constraints
update + `SECURITY.md` "Honest constraints" + `apps/platform/README.md`
"Чего сейчас намеренно ещё нет" + Track H closure narrative в
`PROJECT-STATUS.md`.)

Этот gap — **install/materialization integrity**, не auth-design
gap. Auth model сам по себе работает корректно (verified Track H
/ Step 4 51/51 smoke run): operator-supplied configs с
`auth.tokens` загружаются и используются как ожидается. Но после
прохождения через `_config_to_dict` (install fast-path
`-Confirm` materialization) выходной JSON теряет `auth` section,
потому что `_config_to_dict` enumerate'ит только те sections,
о которых она знает: `product_name`, `profile_name`,
`default_environment`, `project.environments`, `servers`,
`bootstrap`, `runtime`, optionally `enterprise`. `auth` не в
списке — Track H Step 4 явно forbade трогать `installer.py` per
contract §11.5.

Concrete behaviour pre-Track-I:

1. Operator пишет product config c valid `auth.tokens`
   (e.g. `["${ENV:MCP_TOKEN}"]`).
2. Operator runs `scripts/release/install.ps1 ... -Confirm`.
3. Install fast-path грузит config через
   `load_product_config_from_json_file` (получает
   `ProductConfig.auth = ProductAuthSettings(tokens=[...])`),
   проверяет shape, потом проецирует обратно через
   `_config_to_dict(config)` и записывает результат.
4. `_config_to_dict` НЕ знает про `auth` — выходной dict не
   содержит `"auth": {...}` ключа.
5. Materialized JSON на диске больше не содержит `auth.tokens`.
6. При следующем запуске `python -m <server> --transport http`
   с этим materialized config startup fail-closed:
   `--transport http requires --auth-token-env or auth.tokens
   in product config`.

**Это не silent insecure success** — fail-closed behavior
корректен по Track H contract §10.6. Но это silent
configuration data loss, который ломает declarative round-trip
guarantee, на которую полагаются другие installer paths
(`enterprise` block, `runtime.services[*]` Phase 6/Step 6
service-level fields — оба honored "emit only when divergent
from default" pattern'ом).

Track I — отдельный узкий parallel track, который ship'ит
**fix this single gap** строго в рамках existing Track H auth
design, без расширения scope. Это **не**:

- redesign `ProductAuthSettings` schema;
- changes к auth resolution logic в `_network_transport.py`;
- changes к loader validation в `_parse_auth`;
- introducing secret storage / vault / KMS;
- new MCP tools;
- packaging ecosystem (`.msi` / `.deb` / wheel publication);
- service supervision;
- network hardening;
- enterprise identity stack;
- standalone `apps/platform` entrypoint;
- 1cv8 work.

Это **только**: preserve `ProductConfig.auth.tokens` через
`_config_to_dict` round-trip путь by symmetric extension of the
existing `enterprise` block pattern.

## 2. Стартовая точка (post-Track-H factual baseline)

### 2.1 Existing installer surface

- `apps/platform/src/onec_platform/installer.py:228` —
  `_config_to_dict(config: ProductConfig) -> dict` enumerates
  все known sections и эмитит JSON-serialisable shape. Pattern:
  - mandatory sections (`product_name`, `profile_name`,
    `default_environment`, `project`, `servers`, `bootstrap`,
    `runtime`) всегда эмитятся;
  - `enterprise` (Phase 6/Step 8) эмитится **только когда
    divergent from default** — pre-Phase-6/Step-8 configs
    round-trip byte-identical;
  - `auth` (Track H/Step 4) **не эмитится** — отсутствует в
    функции; это и есть Track I gap.
- `apps/platform/src/onec_platform/installer.py:431` —
  `run_install_fast_path(...)` boundary — preview/executed/
  rejected mode; в executed mode пишет результат
  `_config_to_dict(config)` через атомарный
  `*.tmp + os.replace` pattern, потом round-trip
  `bootstrap_product_from_json_file` для подтверждения
  читаемости.

### 2.2 Existing auth surface (post-Track-H, frozen)

- `apps/platform/src/onec_platform/models.py:149` —
  `ProductAuthSettings(tokens: list[str] = field(default_factory=list))`
  dataclass. Public surface byte-identical to Track H Step 4
  shape; не trogается Track I.
- `apps/platform/src/onec_platform/models.py:207` —
  `auth: ProductAuthSettings = field(default_factory=ProductAuthSettings)`
  field на `ProductConfig`. Public surface byte-identical to
  Track H Step 4 shape; не trogается Track I.
- `apps/platform/src/onec_platform/loader.py:439` —
  `_parse_auth(auth_raw) -> ProductAuthSettings` validator
  (unknown-keys reject, list-of-strings, env-substitution regex
  enforcement, literal cleartext fail-closed). Public surface
  byte-identical to Track H Step 4 shape; не trogается Track I.
- `apps/platform/src/onec_platform/loader.py:40` —
  `_AUTH_ENV_TOKEN_RE` regex byte-identical к Track D pattern;
  не trogается Track I.

### 2.3 Existing precedent for additive-installer-fix pattern

`installer.py:_config_to_dict` уже расширялась двумя
backward-compatible additive fixes того же shape:

- **Phase 6 / Step 6** — добавлены service-level fields
  (`restart_policy`, `logs_enabled`, `log_max_bytes`) с emit-
  only-when-divergent pattern'ом, обеспечивающим, что Step 1–5
  configs round-trip byte-identical.
- **Phase 6 / Step 8** — добавлен `enterprise` block с emit-
  only-when-divergent pattern'ом, обеспечивающим, что Step 1–7
  configs round-trip byte-identical.

Track I следует тому же proven pattern. Diff size ожидаемо
**~10–15 lines** в `installer.py` (по аналогии с enterprise
block size).

### 2.4 Existing fail-closed startup (Track H contract anchor)

`packages/mcp-common/src/mcp_common/_network_transport.py`
содержит `_resolve_token_sources` который требует non-empty
token source при `--transport http` и fail-closed на missing
sources с operator-readable single-line stderr message. Это
behaviour остаётся unchanged — Track I не меняет startup
semantics, только устраняет input data loss.

### 2.5 Existing operator-facing wording (Step 5 unified support
statement)

После Track H / Step 5 alignment + Step 6 closure unified
support statement зафиксирован across:
- `SECURITY.md` "Honest constraints" → "Local stdio plus narrow
  HTTP+bearer transport baseline" block (с known installer
  auth-round-trip gap explicitly stated);
- `docs/release-handoff.md` → "What is in this handoff" /
  "What is NOT in this handoff" / "Known limitations" (с known
  installer gap statement);
- `README.md` Quickstart + "Что Quickstart не обещает" + Track
  H detail (закрыт) section;
- `apps/platform/README.md` (4 locations);
- `scripts/dev/launch.ps1` + `scripts/dev/README.md`;
- `CHANGELOG.md` `## 0.5.0` honest constraints update.

Track I closure (Step 5 / Step 6) обновит wording «known
installer auth round-trip gap» в этих местах под фактический
post-Step-4 fix state. Точные docs-alignment surfaces — Step 5
inventory.

---

## 3. Цель Track I

Ship'ить **install/materialization integrity** для Track H
auth section: после прохождения через
`installer.py:_config_to_dict` operator's `auth.tokens`
declarations preserved byte-identically (raw `${ENV:NAME}`
strings round-tripped as configuration data, не resolved env
values), eliminating the current silent auth-section drop.

Что **точно НЕ** входит в Track I — см. §5.

## 4. Что входит в Track I (in scope)

### 4.1 Documentation surface

- `track-i-...-plan.md` (этот документ).
- `track-i-...-step-map.md` (6 шагов).
- Step 2 deliverable: `track-i-installer-auth-round-trip-baseline-audit.md`
  — descriptive read-only audit current `_config_to_dict`
  behaviour + per-existing-section inventory + 4-class
  breakdown + resolve Q1 / Q2 / Q3 (implementation surface,
  preservation contract, forbidden behaviours).
- Step 3 deliverable:
  `track-i-installer-auth-round-trip-contract.md` — prescriptive
  normative document, RFC 2119-style; точная спецификация
  preservation rules (auth section presence, `tokens` list shape
  + ordering, `${ENV:NAME}` raw form preservation as
  configuration data, empty/default behaviour, forbidden
  resolution-at-install-time, allowed/forbidden Step 4 file
  surfaces, verification protocol).

### 4.2 Implementation surface (Step 4 only)

Track I ship'ит ровно **одну** narrow modification к
`installer.py:_config_to_dict` (default expected path; финал —
Step 3 contract на основе Step 2 audit). Default candidate
shape:

```python
# After the existing enterprise_block emit logic:
auth_block: dict[str, Any] = {}
if config.auth.tokens:
    auth_block["tokens"] = list(config.auth.tokens)
if auth_block:
    out["auth"] = auth_block
```

Это **не**:
- changes к `models.py` (`ProductAuthSettings` / `ProductConfig.auth`
  byte-identical);
- changes к `loader.py` (`_parse_auth` / `_AUTH_ENV_TOKEN_RE`
  byte-identical);
- changes к `_network_transport.py`;
- changes к public API surface `onec_platform/__init__.py`
  (`ProductAuthSettings` остаётся unrebooted);
- introduction нового helper file;
- changes к `bootstrap.py` / `doctor.py` / `dashboard.py` /
  `recovery.py` / `runtime.py` / др. `apps/platform` files.

Если Step 2 audit обнаружит, что `_install_runner.py`
требует sympathetic update (например, для exposing `auth`
section status in `InstallFastPathResult` shape) — это будет
explicitly resolved в Step 3 contract. Default expectation:
**only `installer.py`**.

### 4.3 Operator / docs alignment (Step 5)

- `SECURITY.md` — обновить «known installer auth-round-trip
  gap» wording под фактический post-Step-4 fix state.
- `docs/release-handoff.md` — обновить «What is NOT» и «Known
  limitations» bullets под фактический post-fix state.
- `apps/platform/README.md` — обновить «Чего сейчас намеренно
  ещё нет» и related sections.
- `README.md` — обновить Quickstart paragraph + "Что Quickstart
  не обещает" + active parallel track section (если remaining
  drift есть).
- `scripts/dev/launch.ps1` + `scripts/dev/README.md` — только
  если operator-facing wording реально drift'ует; default не
  трогать.

Точный финал docs scope — Step 5 inventory.

### 4.4 Closure deliverables (Step 6)

- `pyproject.toml` version bump (Q6 default ДА; resolve в
  Step 6 на основе фактического Step 4 functional delta).
- `README.md` move Track I в Closed parallel tracks list +
  add «Track I detail (закрыт)» section симметрично Track
  A/B/C/D/E/F/G/H detail blocks.
- `PROJECT-STATUS.md` header rewrite + per-step closure
  sections.
- `CHANGELOG.md` new section under whichever version Q6
  dictates.

## 5. Что НЕ входит в Track I (out of scope)

Out of scope категорически (повтор для ясности; нарушение
этого списка — scope creep, а не валидное расширение Track I):

### 5.1 Не auth design changes

- **Никаких изменений в `ProductAuthSettings` schema.** `tokens:
  list[str]` field shape preserved byte-identical.
- **Никаких изменений в `_parse_auth` validation contract.**
  Env-substitution regex enforcement + literal cleartext fail-
  closed remain Track H contract anchors.
- **Никаких изменений в `_network_transport.py` auth resolution
  logic.** Track H `_resolve_token_sources` /
  `_resolve_config_tokens` byte-identical.
- **Никаких изменений в `Authorization` header parsing,
  case-insensitive scheme handling, `hmac.compare_digest`
  validation, или failure-equivalence rule.**
- **Никакого token rotation / refresh / introspection
  endpoint** — все Track H §5 / §8 forbidden auth shapes
  carry forward byte-identical.

### 5.2 Не secret storage

- **Никакого vault / KMS / OS keychain / encrypted-at-rest
  secrets file format.** Operator-managed `${ENV:NAME}` path
  remains the only documented secret discipline.
- **Никакого resolving env vars at install / materialization
  time.** Installer round-trips raw `${ENV:NAME}` strings as
  configuration data; resolution remains
  `_network_transport._resolve_env_token` boundary at server
  startup.
- **Никакого writing cleartext tokens anywhere.** Cleartext
  literal в `auth.tokens` уже rejected at config-load by
  `_parse_auth`; installer не должен и не может его принять.

### 5.3 Не packaging ecosystem

- **`.msi` / `.deb` / signed binary distribution / GUI
  installer / wizard / PyPI publication / wheel publication.**
  Track C wheel-build empty constraint preserved.
- **Никакого нового console script / `[project.scripts]`
  entry.** Existing три entries (`mcp-read-server` /
  `mcp-write-server` / `mcp-intelligence-server`) preserved
  byte-identical.

### 5.4 Не transport / network changes

- **Никакого нового MCP transport family.** Stdio (Track G) +
  HTTP/1.1 (Track H) baseline preserved.
- **Никакого TLS-in-process.** Operator's reverse proxy
  responsibility preserved.
- **Никакого WebSocket / SSE / TCP / Unix-socket / named-pipe
  transport.**
- **Никакого rate limiting / sessions / cookies.**

### 5.5 Не service / supervisor

- **Никакого systemd unit / Windows Service registration /
  `launchd` plist / hot reload / restart watcher / supervisor
  daemon.**
- **Никакого auto-update / orchestration templates / HA /
  clustering / load balancing.**

### 5.6 Прочее out-of-scope

- **Новые MCP tools.** Registry invariant `read=15 / write=25
  / intelligence=16` carried through unchanged.
- **1cv8.exe execution work.** Track I operates на
  install/materialization layer; 1cv8 binary surface не
  задействуется ни на одном шаге.
- **Rollback / AST / multi-version 1С matrix expansion.**
  Track A / E / F territories.
- **Standalone `apps/platform` entrypoint.** Carry-over
  out-of-scope from Tracks G/H.
- **Web UI / dashboard frontend.**
- **Distributed tracing / observability stack.**
- **Enterprise identity stack** (SSO / OIDC / RBAC /
  multi-tenant) — significantly broader; warrants own track.
- **GitHub remote push.** Operator action, не часть трека.

## 6. Guardrails

Жёсткие инварианты, которые Track I **MUST** соблюдать на
каждом step:

1. **Registry invariant.** `mcp-read-server=15 /
   mcp-write-server=25 / mcp-intelligence-server=16` без
   drift'а ни на одном шаге; selfcheck зелёный.
2. **No new MCP tools.** `server.py:REGISTERED_TOOLS` для
   всех 3 servers — identical content / identical lookup
   functions / identical tool callable signatures.
3. **Track H auth surfaces preserved byte-identical.**
   - `ProductAuthSettings` dataclass shape unchanged;
   - `ProductConfig.auth` field unchanged;
   - `_parse_auth` validation contract unchanged;
   - `_AUTH_ENV_TOKEN_RE` regex byte-identical;
   - `_network_transport.py` byte-identical;
   - все 3 `__main__.py` byte-identical;
   - `Authorization` header parsing / case-insensitive scheme
     / `hmac.compare_digest` / failure-equivalence rule
     byte-identical.
4. **`mcp_common` public API surface preserved byte-identical.**
   `mcp_common/__init__.py` `__all__` (10 names) без
   изменений. New helpers (если any) только underscore-
   prefixed private modules (default expectation: no new
   helpers needed).
5. **`run_write_flow` discipline preserved.** Track I не
   trogает write-flow surface.
6. **Read-only-by-construction discipline preserved** для
   `mcp-intelligence-server`. Track I не trogает intelligence
   surface.
7. **No `[project.dependencies]` block changes.** Track I
   implementation pure stdlib (Track G/H carry-over).
   `[project.optional-dependencies]` тоже без изменений.
8. **No real credentials в repo / docs / commit messages.**
   Bearer tokens — только через `${ENV:NAME}` env-substitution
   (Track D pattern); Track I round-trips strings, никогда не
   resolves them.
9. **No 1cv8.exe runs ни на одном шаге Track I.** Трек
   работает на install/materialization layer уровне, не на
   1cv8 binary surface.
10. **Production code touched только в Step 4** и **только**
    на explicit allowed surfaces (resolve в Step 3 contract;
    default expectation: только `installer.py:_config_to_dict`).
    Шаги 1, 2, 3, 5, 6 — documentation / status / version-only.
11. **`pyproject.toml` `[tool.hatch.build.targets.wheel]
    packages = []` preserved** (Track C honest constraint
    carried through unchanged).
12. **No premature "production-ready / hostile-network /
    enterprise-ready" claim.** Track I closure only fixes
    install/materialization integrity for auth section;
    threat model и operator-facing wording inherits Track H
    Step 5 / Step 6 honest framing.
13. **No remote push.** GitHub remote push — operator action,
    не часть трека.

## 7. Acceptance criteria (closure check Step 6)

Track I считается честно закрытым на Step 6, когда **все 10
пунктов** одновременно выполнены:

1. **Documented plan + audit + contract.** Plan + step-map
   (Step 1) + baseline audit (Step 2) + normative contract
   (Step 3) — на диске, ship'нутые отдельными commit'ами,
   без нарушения Step format.
2. **Implemented auth round-trip preservation.** Sample
   `ProductConfig` с non-empty `auth.tokens=["${ENV:MCP_TOKEN}"]`
   проходит через `_config_to_dict(...)` → dict → `json.dumps`
   → `json.loads` → `load_product_config(...)` round-trip
   и финальный `ProductConfig.auth.tokens` byte-equal к
   исходному.
3. **Backward compat preserved.** Pre-Track-H configs (без
   `auth` section) проходят through `_config_to_dict` → JSON
   и не получают implicit `"auth": {...}` injection (default
   `ProductAuthSettings(tokens=[])` → no key emitted, by analogy
   with `enterprise` block emit-only-when-divergent pattern).
4. **No env-resolution at install time.** Operator declares
   `${ENV:MCP_TOKEN}` в исходном config; materialized JSON
   contains identical `"${ENV:MCP_TOKEN}"` string (raw
   env-substitution form preserved as configuration data;
   actual env value никогда не embedded в materialized file).
5. **Track H surfaces byte-identical.** Diff
   `models.py:ProductAuthSettings` / `loader.py:_parse_auth` /
   `_AUTH_ENV_TOKEN_RE` / `_network_transport.py` / 3
   `__main__.py` / `mcp_common/__init__.py` против
   Track H Step 6 closure state — empty.
6. **Registry invariant.** Selfcheck сообщает
   `read_server_tools` len = 15, `write_server_tools` len = 25,
   `intelligence_server_tools` len = 16, `imports_ok = true`,
   `selfcheck_status = ok`.
7. **No new MCP tools.** Diff `REGISTERED_TOOLS` keys для всех
   3 servers — empty.
8. **Operator / security docs alignment.** `SECURITY.md`,
   `docs/release-handoff.md`, `README.md`,
   `apps/platform/README.md`, possibly `scripts/dev/*` (Step 5
   inventory) говорят one truth о post-fix install/materialization
   integrity; nothing claims «full installer ecosystem solved»
   / «packaging solved» / «deployment solved» / «enterprise-
   ready».
9. **Linear history Step 1 → Step 6.** `git log --oneline`
   показывает шесть commit'ов с exact subject pattern
   `Track I / Step N — ...`, в правильном порядке, без
   accidental extra commits inside Track I scope.
10. **`verify-release.ps1` GREEN на clean tree** (no
    `-AllowDirtyTree`); 8 checks PASS / SKIP; selfcheck
    registries и status корректны; no real credentials в
    diff'ах ни одного из шести Track I commit'ов; no 1cv8.exe
    runs ни на одном шаге Track I; no remote push.

## 8. Honest constraints, которые останутся после Track I closure

Track I **не закрывает** следующее (это не gaps Track I, это
explicit out-of-scope; см. §5):

- никакого full installer ecosystem (`.msi` / `.deb` / GUI
  installer / wizard / signed distribution / PyPI / wheel
  publication beyond `[project.scripts]`);
- никакого secrets vault / KMS / OS keychain integration;
- никакого env-var resolution at install time (это design
  invariant, не gap);
- никаких изменений в Track H auth model (бearer / case-
  insensitive scheme / constant-time compare / failure-
  equivalence rule);
- никакого нового transport / network / TLS / mTLS / OAuth /
  JWT / OIDC / SAML / SCIM / RBAC / multi-tenant / session /
  rate limiting;
- никакого supervisor / systemd / Windows Service / hot
  reload;
- никакого web UI;
- никакого standalone `apps/platform` entrypoint;
- никаких новых MCP tools;
- никакого 1cv8 work / rollback / AST / multi-version;
- никакого distributed tracing / observability stack;
- никакого remote push.

После Track I closure honest support statement становится:

> Local stdio MCP transport baseline (Track G) plus narrow
> HTTP/1.1 `/mcp` endpoint with static bearer authentication
> (Track H), with install/materialization integrity for the
> auth section (Track I): operator's `auth.tokens` declarations
> are now preserved byte-identically through
> `scripts/release/install.ps1 ... -Confirm` round-trip; raw
> `${ENV:NAME}` strings are round-tripped as configuration
> data without env-resolution at install time. Threat model
> still = trusted-local-stdio for stdio, trusted-network behind
> operator-owned reverse proxy for HTTP. The full set of Track
> H out-of-scope items (in-process TLS, mTLS, JWT/OAuth/OIDC/
> SAML/SCIM, RBAC/ABAC/multi-tenant, WebSocket/SSE/TCP/pipe,
> supervisor/systemd/Windows-Service/hot-reload, web UI,
> packaging beyond `[project.scripts]`, standalone
> `apps/platform` entrypoint, new MCP tools) carries forward
> unchanged.

## 9. Relation to prior tracks

- **Track A (Full Real 1cv8-backed Write Path).** Track I не
  trogает 1cv8 surface; никаких 1cv8.exe runs.
- **Track B (Productization & Delivery Polish).** Track I не
  реструктурирует repo hygiene / install fast path /
  scripts umbrella; `scripts/release/install.ps1` thin
  wrapper над `run_install_fast_path` остаётся unchanged
  (если внутренняя логика `run_install_fast_path` потребует
  exposed gap reporting в `InstallFastPathResult`, это будет
  resolved в Step 3 contract; default — minimal `installer.py`
  edit).
- **Track C (Packaging & Installer Delivery).** Track I
  carry-over honest constraint: wheel build остаётся пуст
  (`[tool.hatch.build.targets.wheel] packages = []`); никаких
  `.msi` / `.deb` / signed distribution / PyPI publication.
  `[project.scripts]` block unchanged.
- **Track D (Operator Credentials Hardening).** Track I
  **переиспользует** existing `${ENV:NAME}` env-substitution
  pattern as round-trip configuration data; никаких изменений
  в Track D credential model. `command_preview` redaction
  discipline не задевается (Track D applies к 1С DESIGNER
  credentials в command templates; Track I round-trips MCP
  bearer token specs).
- **Track E (Multi-Version 1C Smoke Matrix).** Track I
  ortogonal — Track E работает с 1С platform versions
  evidence; Track I работает с install/materialization
  integrity. Никаких изменений в `docs/version-support-matrix.md`.
- **Track F (Rollback Whitelist Expansion).** Track I
  ortogonal — Track F работает с rollback whitelist config;
  Track I работает с install/materialization integrity.
  `_AUTOMATIC_RECOVERY_SUPPORTED` / `_ROLLBACK_SUPPORTED_OPERATIONS`
  frozensets не задеваются.
- **Track G (Production-Grade MCP Transport and CLI).**
  Track I ortogonal — Track G ship'ил stdio entrypoints +
  CLI; existing 3 `__main__.py` byte-identical через Track I;
  `_stdio_transport.py` byte-identical.
- **Track H (Network-Grade MCP Transport and Authentication
  Boundary).** Track I — **прямой узкий follow-up** к Track H:
  Track H auth surfaces (model, loader, network transport)
  preserved byte-identical; Track I closes the single known
  installer round-trip gap that Track H deliberately deferred
  per its §11.5 forbidden-files list. Track H Step 4
  closure narrative honestly предсказала Track I shape:
  «future post-Track-H fix to `_config_to_dict` is analogous
  to the Phase 6 / Step 9 service-level + enterprise round-
  trip fix».

## 10. Open questions Q1–Q7

### Q1. Exact implementation surface for future Step 4

**Default planning anchor (резолвится в Step 2 audit / Step 3
contract):** **`installer.py` only**.

**Reasoning:**
- Phase 6/Step 9 service-level + enterprise round-trip fix
  precedent: both extensions added inside `_config_to_dict`
  без modification of `_install_runner.py` or other helpers;
- Track I gap pattern matches: missing emit branch для
  `auth` block → add ~10–15 LOC in `_config_to_dict` symmetric
  to existing `enterprise_block` shape;
- `_install_runner.py` (Track B/C release wrapper) operates
  on the JSON layer through CLI args; не trogает
  `ProductConfig` shape internals.

**Alternative considered + rejected:** `installer.py +
_install_runner.py` — добавление reporting hook про auth
section status в `InstallFastPathResult`. Rejected as default
because: (a) install fast path executed mode уже round-trip'ит
через `bootstrap_product_from_json_file`, который сам ловит
load errors (rejected mode); auth section presence sanity
check happens implicitly через post-write loader call; (b)
explicit reporting hook expands scope без shipping value.

**Финальное решение** — Step 3 contract (на основе Step 2
audit evidence).

### Q2. What exactly must be preserved through round-trip

**Default planning anchor:**

1. **`auth` section presence** when source config has non-empty
   `auth.tokens`.
2. **`tokens` list shape** as ordered list of strings (Python
   `list[str]` → JSON array of strings).
3. **Order preservation** — entries emitted в том же порядке,
   что в source `ProductConfig.auth.tokens`.
4. **Raw `${ENV:NAME}` string form preserved** as configuration
   data — никакого env-resolution at install time. Each entry
   character-by-character byte-identical к source string after
   `json.dumps` / `json.loads` round-trip.
5. **Empty/default behaviour:** when source config has empty
   `auth.tokens=[]` (default `ProductAuthSettings()`), output
   dict **MUST NOT** contain `"auth"` key — by symmetry with
   `enterprise_block` emit-only-when-divergent pattern. This
   preserves byte-identical round-trip for pre-Track-H configs
   without `auth` section.

**Финальное решение** — Step 3 contract (точная shape).

### Q3. What is explicitly forbidden

**Default (carry-over из guardrails §6 + scope §5):**

- **Resolving env vars during install time.** Никакого
  `os.environ.get(...)` calls inside `_config_to_dict` для
  auth tokens. Raw `${ENV:NAME}` strings round-tripped as
  string data.
- **Writing cleartext tokens.** `_parse_auth` уже rejects
  literal cleartext at config-load time; Track I не вводит
  separate path для cleartext acceptance.
- **Changing auth semantics from Track H.** No changes к
  `Authorization` header parsing, scheme handling, token
  validation, failure-equivalence rule, fail-closed startup.
- **Introducing secret storage.** No vault / KMS / file-based
  secrets cache / encrypted-at-rest format.
- **Broad packaging rewrite.** No new wheel build / PyPI /
  signed distribution / GUI installer / `.msi` / `.deb`.
- **Touching `[project.scripts]`.** Existing 3 console entries
  byte-identical.
- **Touching `_install_runner.py`** unless Step 3 contract
  explicitly requires it (default expectation: not required).

### Q4. Backward compatibility

**Default planning anchor:**

1. **Pre-Track-H configs must still materialize.** Configs
   without `auth` section continue to round-trip
   byte-identical; `_config_to_dict` MUST NOT inject implicit
   `"auth": {...}` for default `ProductAuthSettings()`.
2. **Stdio-only configs must still work.** `--transport stdio`
   path не зависит от `auth` section presence; configs without
   `auth.tokens` continue to start stdio transport correctly.
3. **Configs with empty `auth.tokens=[]` remain valid.**
   Loader continues to accept missing / empty `auth` section
   per `_parse_auth` contract; round-trip preserves emptiness.
4. **Track H Step 4 verification artifact (51/51 PASS) carries
   through.** Existing smoke list (per-server `--help`, HTTP
   startup negative tests, byte-identical 401 fail-closed,
   case-insensitive scheme, GET 405, non-`/mcp` 404, malformed
   JSON 400, wrong CT 415, unknown method 200+`-32601`, multi-
   Auth 400+`-32600`, notification 204, tools/call ping 200,
   cross-transport parity) MUST remain GREEN (no regression).

### Q5. Docs scope on Step 5

**Default planning anchor:**

- **`SECURITY.md`** — обновить «Honest constraints» known
  installer auth-round-trip gap bullet под фактический
  post-Step-4 fix state (gap → fixed).
- **`docs/release-handoff.md`** — обновить «What is NOT in
  this handoff» / «Known limitations» installer gap bullets.
- **`apps/platform/README.md`** — обновить «Чего сейчас
  намеренно ещё нет» installer gap mention.
- **`README.md`** — обновить Quickstart paragraph + "Что
  Quickstart не обещает" + active parallel track section
  (если remaining drift есть).
- **`scripts/dev/launch.ps1`** + **`scripts/dev/README.md`** —
  только если operator-facing wording реально drift'ует;
  default expectation: не trogать (Track H Step 5 wording
  про launch.ps1 не упоминает installer gap directly).
- **`scripts/release/README.md`** — possibly если install
  fast path documentation references the gap. Default: check
  во время Step 5 inventory; не пред-открывать.

**Точный финал docs scope** — Step 5 inventory.

### Q6. Q7 version bump default for future Step 6

**Default planning anchor:** likely **YES** (`0.5.0 → 0.6.0`)
если Step 4 ship'ит real production code change с observable
configuration-round-trip behaviour delta.

**Reasoning:**
- precedent — Track D `0.1.0 → 0.2.0`, Track F `0.2.0 → 0.3.0`,
  Track G `0.3.0 → 0.4.0`, Track H `0.4.0 → 0.5.0` — все шли
  с MINOR bump на real production code change;
- backward-compatible new functionality (existing configs
  preserved byte-identical; pre-Track-H configs without `auth`
  section continue to materialize identically) → classic MINOR
  bump per SemVer.

**Counter-consideration:** Track I scope is significantly
narrower than Track H (single-function ~10–15 LOC fix vs
549 LOC new helper + auth model). Could argue **PATCH** bump
(`0.5.0 → 0.5.1`) на основе "narrow defect-fix" interpretation.

**Финальное решение** — Step 6 closure decision (на основе
фактического Step 4 functional delta + SemVer semantics
review). Default = MINOR (`0.6.0`) для consistency с prior
tracks; PATCH (`0.5.1`) — alternative path только если Step 4
diff действительно tiny (~5 LOC) и framing честнее как
defect-fix чем feature.

### Q7. What closure does NOT mean

**Default (carry-over из honest framing §1 + §8):**

- **Не full installer ecosystem.** `.msi` / `.deb` / GUI
  installer / signed distribution / PyPI / wheel publication
  remain out-of-scope.
- **Не deployment solved.** Operator's reverse proxy / TLS
  termination / supervisor / OS service registration / hot
  reload remain operator's responsibility.
- **Не packaging solved.** Track C wheel-build empty
  constraint preserved.
- **Не enterprise-ready.** Single-tier auth (Track H) preserved;
  no SSO / OIDC / RBAC / multi-tenant added.
- **Только installer auth round-trip integrity fixed.** One
  defect-class gap closed honestly; honest support statement
  для всех остальных Track A-H constraints carries forward
  unchanged.

---

## 11. Step trajectory (preview)

Подробности — в companion `track-i-...-step-map.md`. Краткое
резюме шести шагов:

1. **Step 1 — planning** (этот шаг). Два planning-документа +
   минимальные status-правки в README / PROJECT-STATUS под
   открытие active track'а I.
2. **Step 2 — installer round-trip baseline audit** (docs-only).
   Один новый descriptive audit-документ с per-section inventory
   (`product_name` / `profile_name` / `default_environment` /
   `project.environments` / `servers` / `bootstrap` /
   `runtime` / `enterprise` / `auth`) + 4-class breakdown +
   evidence-grounded Q1 / Q2 / Q3 final resolution.
3. **Step 3 — auth round-trip preservation contract** (docs-only).
   Один новый prescriptive normative document, RFC 2119-style;
   точные allowed/forbidden Step 4 surfaces; resolve финальные
   preservation rules + verification protocol.
4. **Step 4 — narrow installer auth round-trip implementation**
   (production code change, единственный шаг). Implementation
   ровно одного diff в `installer.py:_config_to_dict` по Step 3
   contract; existing surfaces preserved; registries без
   drift'а; no new MCP tools.
5. **Step 5 — operator docs and security alignment**
   (docs-only). Точечная alignment SECURITY / release-handoff
   / README / apps/platform/README / возможно scripts/* под
   фактический post-Step-4 fix state.
6. **Step 6 — final integration pass and Track I closure**.
   Q6 resolve; pyproject version bump (если Q6 = ДА); README
   + PROJECT-STATUS + CHANGELOG closure narrative симметрично
   Track A/B/C/D/E/F/G/H pattern. **GitHub remote push —
   operator action, не часть трека.**
