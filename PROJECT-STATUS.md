# PROJECT STATUS — 1C Agent Platform

## Текущий шаг

Активного шага нет. Phase 1–6 закрыты ранее;
двенадцать post-phase parallel track'ов (A, B, C,
D, E, F, G, H, I, J, K, L) полностью закрыты
последовательно (см. блоки «Статус» ниже для Track
L / Track K / Track J / Track I closure narrative).
Phase 7 как линейная фаза не запланирована.
Открытие следующего параллельного трека — отдельное
operator decision; логичные кандидаты перечислены в
README секции «Active parallel track» (без
автоматического открытия). `pyproject.toml`
`version=0.5.1` preserved через Track J / Track K /
Track L NO-BUMP closures.

## Статус

`closed` (для всего Parallel Track L — Service
Supervision and OS Service Registration — Steps 1–6
закрыты последовательно; **Q7 = NO-BUMP**;
`pyproject.toml` `version=0.5.1` preserved через
Track J NO-BUMP closure, Track K NO-BUMP closure, и
Track L NO-BUMP closure; никаких code changes ни в
одном из шести Track L шагов; registry invariant
`read=15 / write=25 / intelligence=16` без drift'а;
никаких 1cv8.exe runs; никаких реальных credentials
в repo / docs / commit messages; никакого remote
push). Шесть meaningful commit'ов в `main`:
`e713f8e` Step 1 (planning) / `d58c8d9` Step 2
(descriptive baseline audit) / `76342a5` Step 3
(normative contract pinning **PATH B** +
systemd-first + all 5 lifecycle verbs mandatory +
`runtime.py` byte-identical NOT extended) /
`efb4ea1` Step 4 (narrow PATH B implementation:
два новых файла под
[`docs/operators/service/`](docs/operators/service/) —
operator-facing recipe
[`service-supervision.md`](docs/operators/service/service-supervision.md)
972 lines с all 5 lifecycle verbs end-to-end на
systemd + cross-OS prose для Windows NSSM и macOS
launchd, и declarative systemd unit-file template
[`mcp-server.service`](docs/operators/service/mcp-server.service)
76 lines с `Type=simple` + placeholders only +
RECOMMENDED defaults `Restart=on-failure` /
`KillSignal=SIGINT` / `KillMode=mixed` /
`TimeoutStopSec=15s`) / `82345b4` Step 5 (narrow
CLASS-1 docs-alignment of README + release-handoff
to reflect Step 4 deliverables) + closure commit
Step 6 (final integration pass and track closure;
этот commit). Track L закрыл следующий честный
эксплуатационный gap: у продукта уже были рабочие
MCP entrypoints + HTTP/stdio transports + bearer
auth + installer integrity + deployment-boundary
recipe + real MCP client smoke proof, но не было
взрослой service-supervision story; recipe и
template вместе take operator on Linux from "I
can run an MCP server in a terminal" to "the MCP
server is supervised by systemd, survives reboots,
responds to start / stop / restart / status / logs,
and logs to journald" — без модификации production
code, `pyproject.toml` или existing `scripts/*`
files. `apps/platform/src/onec_platform/runtime.py`
byte-identical и **не** превращён в service
manager — продолжает supervise только product-
layer subprocesses из `ProductConfig.runtime.services`,
не MCP-серверы сами.

`in progress` (для Parallel Track L / Step 1 — на
момент Step 1 closure commit'а — теперь historical
snapshot после full Track L closure; см. секцию
«Parallel Track L / Step 6 — final integration
pass and track closure (завершён)» ниже для full
closure narrative).

`closed` (для всего Parallel Track K — Real MCP
Client Integration Test — Steps 1–6 закрыты
последовательно; **Q7 = NO-BUMP**; `pyproject.toml`
`version=0.5.1` preserved через Track J NO-BUMP
closure и Track K NO-BUMP closure; никаких code
changes ни в одном из шести Track K шагов;
registry invariant `read=15 / write=25 /
intelligence=16` без drift'а; никаких 1cv8.exe
runs; никаких реальных credentials в repo / docs /
commit messages; никакого remote push). Шесть
meaningful commit'ов в `main`: `02783df` Step 1
(planning) / `62069a5` Step 2 (descriptive
baseline audit) / `ead4a0e` Step 3 (normative
contract pinning **PATH B**) / `979eced` Step 4
(narrow MCP client smoke harness shipped at
[`scripts/dev/mcp_client_smoke.py`](scripts/dev/mcp_client_smoke.py),
341 LOC stdlib-only single new file; runnable;
exit 0; raw `OK` line captured) / `ef9c6c7` Step 5
(narrow CLASS-1 docs-alignment of README +
release-handoff + scripts/dev/README) + closure
commit Step 6 (final integration pass and track
closure; этот commit). Track K закрыл один из
последних честных gaps проекта (отсутствие real
MCP-client-facing end-to-end proof для already-
existing stdio/HTTP transport surfaces); harness
exercises `initialize` + `tools/list` + read-only
`tools/call` round-trip против `mcp-read-server`
по обоим transports + HTTP missing-`Authorization`
401 + `WWW-Authenticate: Bearer realm="mcp"` +
JSON-RPC `-32001` probe.

`closed` (для всего Parallel Track J — Steps 1–6
закрыты последовательно; **Q7 = NO-BUMP**;
`pyproject.toml` `version=0.5.1` preserved от Track I
closure bump; никаких code changes ни в одном Track J
шаге; registry invariant без drift'а; никаких 1cv8.exe
runs; никаких реальных credentials в repo / docs /
commit messages).

`closed` (для всего Parallel Track I — Steps 1–6
закрыты последовательно). Был закрыт
**Parallel Track I — Installer Auth Round-Trip
Integrity**, шесть шагов; шесть meaningful commit'ов
в `main`: `cb79597`
(Step 1 — planning), `e7d9973` (Step 2 — installer
round-trip baseline audit), `525c611` (Step 3 — auth
round-trip preservation contract), `d047a6d` (Step 4 —
narrow installer auth round-trip implementation,
единственный шаг с production code change, +15/-0 LOC),
`2e9e0b8` (Step 5 — operator docs and installer auth
alignment), плюс closure commit Step 6 фиксирует
обновлённые README / PROJECT-STATUS / CHANGELOG +
`pyproject.toml` version bump `0.5.0` → `0.5.1` (Q6 =
PATCH; см. ниже). Открытие следующего параллельного
трека — отдельное operator decision; Phase 7 как
линейная фаза не запланирована.

## Статус

`closed` (для всего Parallel Track I — Steps 1–6 закрыты
последовательно). Track I ship'ил **defect-class round-
trip integrity fix** — `installer.py:_config_to_dict`
теперь emits `auth` section symmetric к existing Phase 6
/ Step 8 enterprise-block emit-only-when-divergent
pattern; operator's `auth.tokens` declarations preserved
byte-identical через install fast-path materialization
round-trip; raw `${ENV:NAME}` strings round-tripped как
configuration data (env resolution остаётся runtime
boundary в `_network_transport._resolve_env_token`, не
install time); empty/default `auth` не injected в
pre-Track-H configs (no implicit `"auth": {}` injection).
Production-код Track I правил **только Step 4** и
**только** в `installer.py:_config_to_dict` (+15 / -0
LOC, 1 file modified); шаги 1, 2, 3, 5, 6 —
documentation / status / version-only. **Q6 resolved**
на Step 6 = **PATCH** (NOT MINOR): `pyproject.toml`
version bumped `0.5.0` → `0.5.1`. Reasoning: Track I —
defect-class round-trip integrity repair, не feature
delta. (1) Step 4 commit (`d047a6d`) — `+15 / -0` LOC в
одной функции, symmetric к существующему Phase 6 /
Step 8 `enterprise_block` pattern. (2) **No new public
API surface**: `ProductAuthSettings` и
`ProductConfig.auth` уже существовали в version 0.5.0
(Track H Step 4); Track I добавил zero new public types
/ functions / module imports / CLI flags / MCP tools /
`mcp_common/__init__.py` `__all__` exports / `[project.scripts]`
entries. (3) **No new runtime capability**: operators
using `--transport http` уже имели рабочие пути
pre-Track-I (declare `auth.tokens` в source config или
use `--auth-token-env` CLI override); Track I closed
silent data-loss bug в install fast-path round-trip,
который operators обходили — net-new capability нет;
есть previously-broken round-trip который теперь
работает. (4) **SemVer prior precedent comparison**:
Track D `0.1.0 → 0.2.0` (env-substitution + verify-release
Check 8 — added 50+ LOC of new credential-resolution
logic + new release-side check); Track F `0.2.0 → 0.3.0`
(rollback whitelist 2→6 — meaningful runtime-reachable
recovery for 4 new tool families); Track G `0.3.0 →
0.4.0` (3 new __main__.py + 245-LOC `_stdio_transport.py`
+ new `[project.scripts]` block — net-new runnable
surface); Track H `0.4.0 → 0.5.0` (549-LOC
`_network_transport.py` + new HTTP/`/mcp` endpoint +
bearer auth + new CLI flags — net-new transport family).
Each of D/F/G/H added a recognizable new external
capability and warranted MINOR. **Track I does not** —
it restores integrity of a flow that should have always
preserved this section. Per Keep-a-Changelog conventions
and SemVer §6, "Bug fixes" → PATCH. Track I plan §10 Q6
explicitly framed PATCH `0.5.1` как «alternative path
только if Step 4 diff truly tiny and framing honest as
defect-fix»; Step 4 diff был 15 LOC (well within "truly
tiny"); fix — genuinely defect-class round-trip
integrity repair. PATCH честно отражает что изменилось.
Никакого full installer ecosystem (`.msi` / `.deb` /
signed distribution / GUI installer / wizard / PyPI
publication / wheel publication beyond
`[project.scripts]`), никакого secret storage / vault /
KMS / OS keychain integration, никакого env-var
resolution at install time (design invariant — resolution
остаётся `_network_transport._resolve_env_token` runtime
boundary), никаких изменений в Track H auth model
(bearer / case-insensitive scheme / constant-time compare
/ failure-equivalence rule preserved byte-identical),
никакого нового transport / network / TLS / mTLS / OAuth
/ JWT / OIDC / SAML / SCIM / RBAC / multi-tenant /
sessions / rate limiting, никакого supervisor / systemd
/ Windows Service / hot reload, никакого web UI,
никакого standalone `apps/platform` entrypoint, никаких
новых MCP tools, никаких 1cv8.exe runs ни на одном шаге
трека. Registry-инвариант `read=15 / write=25 /
intelligence=16` без drift'а на всём треке;
`selfcheck_status=ok`; verify-release.ps1 GREEN на 8
checks. **GitHub remote push не часть трека — operator
action.**

`closed` (для всего Parallel Track H — Steps 1–6 закрыты
последовательно). Track H ship'ил **второй слой зрелости**
поверх Track G: single HTTP/1.1 `/mcp` endpoint с static
bearer authentication, additive над existing local stdio
surface. Production-код Track H правил **только Step 4**
и **только** на explicit allowed surfaces (1 new private
helper `_network_transport.py` + 3 modified `__main__.py`
+ 2 modified `apps/platform` files); шаги 1, 2, 3, 5, 6 —
documentation / status / version-only. **Q7 resolved** на
Step 6 = **ДА**: `pyproject.toml` version bumped `0.4.0`
→ `0.5.0`. Reasoning: Step 4 ship'нул real production
code change с **observable runtime capability delta** —
`python -m <server> --transport http --bind ...
--auth-token-env ...` теперь реально стартует HTTP/1.1
listener с bearer authentication, что до Track H было
невозможно (existing `_stdio_transport._build_arg_parser`
имел `ALLOWED_TRANSPORTS=("stdio",)` rejecting `http` at
argparse level). Backward-compatible new functionality
(existing `--transport stdio` byte-identical через
delegation в `_stdio_transport._serve_stdio`;
`mcp_common/__init__.py` `__all__` byte-identical;
`_stdio_transport.py` byte-identical; `[project.scripts]`
byte-identical; registries `15/25/16` invariant; audit
`details` shape preserved; new `ProductConfig.auth`
optional field с `default_factory` — pre-Track-H configs
load unchanged). Classic MINOR bump per SemVer; precedent
— Track D `0.1.0 → 0.2.0` (env-substitution + verify-
release check 8) и Track F `0.2.0 → 0.3.0` (whitelist
2 → 6) и Track G `0.3.0 → 0.4.0` (stdio entrypoints +
CLI + [project.scripts]) shipped comparable scale
functional delta. Track E (scaffolding only, no
functional delta) → no bump; Track H (real code change)
→ bump. Никакого in-process TLS / HTTPS termination,
никакого mTLS / client certificate authentication,
никакого JWT / OAuth 2.0 / OIDC / SAML / SCIM, никакого
RBAC / ABAC / per-token permissioning / per-tool ACL /
multi-tenant isolation, никаких session cookies / rate
limiting / quotas, никаких WebSocket / Server-Sent
Events / TCP / Unix-socket / named-pipe transports,
никакого supervisor daemon / systemd unit / Windows
Service registration / hot reload / restart watcher,
никакого web UI / dashboard, никакого packaging
ecosystem beyond `[project.scripts]` declarations,
никакого standalone `apps/platform` entrypoint (Q6
carry-over from Track G), никаких новых MCP tools,
никаких 1cv8.exe runs ни на одном шаге трека.
Известный gap: `installer.py:_config_to_dict` не
emit'ит новый `auth` section — install fast path
round-trip silently drops auth.tokens; operator gets
clean fail-closed startup или uses `--auth-token-env
<VARNAME>` to bypass; future post-Track-H fix
analogous Phase 6 / Step 9 service-level + enterprise
round-trip fix. Registry-инвариант `read=15 /
write=25 / intelligence=16` без drift'а на всём треке;
`selfcheck_status=ok`; verify-release.ps1 GREEN на 8
checks. **GitHub remote push не часть трека —
operator action.**

`closed` (для всего Parallel Track G — Steps 1–6 закрыты
последовательно). Track G ship'ил **первый production-grade
operational слой** для трёх MCP servers, закрывая factual gap
«MCP servers cannot start at all»: три canonical
`__main__.py` entrypoint'а
(`apps/mcp-{read,write,intelligence}-server/src/.../`__main__.py``),
один новый private internal helper
(`packages/mcp-common/src/mcp_common/_stdio_transport.py`,
underscore-prefixed, **NOT** экспортирован из
`mcp_common/__init__.py`), `[project.scripts]` block в
`pyproject.toml` с тремя console entries (`mcp-read-server` /
`mcp-write-server` / `mcp-intelligence-server`). Implementation
**PATH B** (Step 4): per Step 3 contract §12.1.4 carve-out для
"duplication otherwise unreasonable" — pure inline PATH A
дал бы ~280 LOC чистого copy-paste через 3 server'а.
Production-код Track G правил **только Step 4** и **только**
на explicit allowed surfaces; шаги 1, 2, 3, 5 —
documentation-only. **Q7 resolved** на Step 6 = **ДА**:
`pyproject.toml` version bumped `0.3.0` → `0.4.0`. Reasoning:
Step 4 ship'нул real production code change с **observable
runtime capability delta** — `python -m mcp_read_server`
(и братья) теперь реально стартуют stdio JSON-RPC server,
что до Track G было невозможно. Backward-compatible new
functionality (existing `list_tools()` / `get_tool(name)` API
preserved byte-identical; `mcp_common` public API
preserved byte-identical; registries `15/25/16` invariant;
audit `details` shape preserved). Classic MINOR bump per
SemVer; precedent — Track D `0.1.0 → 0.2.0` (env-substitution
+ verify-release check 8) и Track F `0.2.0 → 0.3.0`
(whitelist 2 → 6) shipped comparable scale functional delta.
Track E (scaffolding only, PATH B / no functional delta) →
no bump; Track G (real code change) → bump. Никаких
network transport (HTTP / WebSocket / SSE / TCP / named
pipe), никаких authentication / authorization (token /
mTLS / OAuth / RBAC / multi-tenant), никакого supervisor
daemon (systemd / Windows Service / hot reload /
automatic restart), никакого web UI, никакого packaging
ecosystem beyond `[project.scripts]` declarations
(`.msi` / `.deb` / signed distribution / wheel
publication — Track C wheel-build empty constraint
preserved), никакого standalone `apps/platform`
entrypoint (Q6 explicit out-of-scope), никаких новых
MCP tools, никаких 1cv8.exe runs ни на одном шаге трека.
Registry-инвариант `read=15 / write=25 / intelligence=16`
без drift'а на всём треке; `selfcheck_status=ok`;
verify-release.ps1 GREEN на 8 checks. **GitHub remote
push не часть трека — operator action.**

`closed` (для всего Parallel Track F — Steps 1–6 закрыты
последовательно; пять meaningful commit'ов в `main`:
`351278b` (Step 1 — planning rollback whitelist
expansion), `e9725b2` (Step 2 — rollback baseline audit
and candidate selection), `45ad2b2` (Step 3 — rollback
eligibility contract), `cd95627` (Step 4 — narrow rollback
whitelist expansion, единственный шаг с production code
change), `60f1761` (Step 5 — operator docs and rollback
coverage alignment), плюс closure commit Step 6 фиксирует
обновлённые README/PROJECT-STATUS/CHANGELOG +
`pyproject.toml` version bump `0.2.0` → `0.3.0`.
Production-код Track F правил **только два** boundary'а в
одном Step 4 commit'е —
`apps/platform/src/onec_platform/recovery.py`
(`_AUTOMATIC_RECOVERY_SUPPORTED` 2 → 6 entries) и
`apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
(`_ROLLBACK_SUPPORTED_OPERATIONS` mirror 2 → 6 identical +
minor sync-comment wording update); все остальные шаги
(1, 2, 3, 5) — documentation-only. Финальный whitelist:
6 entries identical в обеих mirror frozenset'ах
(`add_catalog_attribute`, `add_document_attribute`,
`add_form_attribute`, `add_form_element`,
`append_module_method`, `replace_module_method_body`).
Coverage = 6 of 25 mutating registry tools = 24% surface;
19 mutating tools остаются manual snapshot-restore
territory by design (Tier 3 categorical exclusions:
`create_*` family, `apply_config_from_files`,
`update_database_configuration`, multi-file ops).
Registry-инвариант `read=15 / write=25 / intelligence=16`
без drift'а на всём треке; `selfcheck_status=ok`.
Никаких реальных credentials ни в одном из шести Track F
commit'ов. Никаких 1cv8.exe runs ни на одном шаге Track F
(трек работает на whitelist configuration уровне, не на
1cv8 binary surface). **No blanket reversibility claim**
unified across SECURITY/release-handoff/README/
apps/platform/README/CHANGELOG).

`closed` (для всего Parallel Track E — Steps 1–6 закрыты
последовательно; пять meaningful commit'ов в `main`:
`1b233ce` (Step 1 — planning multi-version 1C smoke
matrix), `630f837` (Step 2 — current evidence audit and
smoke scenario freeze), `7c08cae` (Step 3 — matrix
scaffolding and operator runbook), `f962d78` (Step 4 —
operator-driven smoke execution and matrix update,
закрыт через PATH B / honest operator-supplied gap —
никаких 1cv8.exe runs, никаких additional evidence
rows), `78d5956` (Step 5 — support statement and docs
alignment), плюс closure commit Step 6 фиксирует
обновлённые README/PROJECT-STATUS/CHANGELOG; production-
код Track E **не правил вообще ни разу** — все
deliverables это planning / audit / scaffolding /
operator runbook / status alignment. Step 4 закрыт
честно через PATH B: на operator machine отсутствуют
1С minor families помимо `8.3.27` (`8.3.27.1859/x64`
reference + `8.3.27.1936/x86` same-family disqualified
per Step 2 §2.2); ENV-substitution credentials не были
выставлены в session. Никаких новых evidence rows в
`docs/version-support-matrix.md` помимо reference row,
зафиксированной copy-only из existing Track A / Step 6
evidence; никаких имитированных additional rows.
Registry-инвариант `read=15 / write=25 /
intelligence=16` без drift'а на всём треке;
`selfcheck_status=ok`. Никаких реальных credentials ни в
одном из шести Track E commit'ов. **No blanket
multi-version support claim**).

`closed` (для всего Parallel Track D — Steps 1–6 закрыты
последовательно; пять meaningful commit'ов в `main`:
`61cf225` (Step 1 — planning operator credentials
hardening), `0d708d1` (Step 2 — credentials flow audit
and contract), `af4436f` (Step 3 — env substitution and
preview redaction), `393e869` (Step 4 — operator docs and
migration alignment), `1fd2d35` (Step 5 — release verify
credential hygiene heuristic), плюс closure commit Step 6
фиксирует обновлённые README/PROJECT-STATUS/CHANGELOG +
version bump `0.1.0` → `0.2.0`; production-код Track D
правил **только два** boundary'а —
`apps/mcp-write-server/.../runtime/binary_dispatch.py`
в write-server runtime layer (Step 3) и
`scripts/release/verify-release.ps1` release-side скрипт
(Step 5); остальные шаги — documentation-only или
выравнивание operator-facing docs. Registry-инвариант
`read=15 / write=25 / intelligence=16` без drift'а на
всём треке; `selfcheck_status=ok`. Никаких реальных
credentials ни в одном из шести Track D commit'ов).

`closed` (для всего Parallel Track C — Steps 1–6 закрыты
последовательно; шесть meaningful commit'ов в `main`:
`af2d7f4` (Step 1 — planning packaging and installer
delivery), `ef087c8` (Step 2 — release-facing verify path
and layout polish), `a4f42f9` (Step 3 — packaging-facing
install flow honest review), `7ca9b3f` (Step 4 — release
handoff documentation), `8ccecf6` (Step 5 — integration
and handoff polish), плюс closure commit Step 6 фиксирует
обновлённые README/PROJECT-STATUS/CHANGELOG; production-
код Track C **не правил вообще ни разу** — все
deliverables это release-facing скрипты, документация и
honest pyproject limitation; registries без drift'а на
всём треке; `selfcheck_status=ok`).

`closed` (для всего Parallel Track B — Steps 1–6 закрыты
последовательно; четыре meaningful commit'а в `main`:
`85a4a7e` (Step 2 — repo hygiene + legal baseline),
`bce8966` (Step 3 — install fast path operator-discoverable),
`fd92477` (Step 4 — operator/dev local launch umbrella),
`0f65c58` (Step 5 — root README quickstart and docs polish),
плюс closure commit `6e2c5ee` (Step 6) фиксирует обновлённые
README/PROJECT-STATUS/CHANGELOG; production-код Track B
**не правил вообще ни разу** — все deliverables это
scripts-only wrapper'ы, repo hygiene и documentation;
registries без drift'а на всём треке;
`selfcheck_status=ok`).

`closed` (для всего Parallel Track A — Phase 1–6
закрыты ранее; Track A / Steps 1–7 закрыты;
Parallel Track A / Step 1 завершён как documentation-only
opening; Step 2 завершён —
`apply_config_from_files(...)` переведён на dual-mode;
Step 3 завершён —
`update_database_configuration(...)` тоже переведён на
dual-mode; Step 4 завершён — внутренняя унификация
binary-backed execution contract'а между всеми тремя
binary-backed write-tool'ами без расширения surface'а;
Step 5 завершён — product-layer surface honestly reflects
the real write contract: Q7 closed in `realstand.py` plan
summary, Q8 closed in `enterprise.py` foundation
inspector; **Step 6 закрыт honestly**: real
multi-step round-trip отработал на real 1cv8 binary'е
(`C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`) и
real file-based инфобазе InfoBase6 — A.2 / A.4 / A.5
все binary-backed зелёные, audit honest (две mutating
audit row + `details.dump_snapshot_path` populated в
обеих); doc/expectation gap (runbook + local chain
ожидали 3 audit row, фактически 2) выровнен под
production-код by design. **Step 7 закрыт без
production-правок**: existing evidence Step 6
round-trip'а покрывает acceptance criteria 1–5,
discipline asserts criteria 6–10 удовлетворены
(registries без drift'а, ноль импортов
`onec_policy_engine` в product/intelligence, нет
back-door write channel'а, operator-facing messages
честные, Track A closed как documented status).
Closure выполнен обновлением closure-status в
`README.md` и `PROJECT-STATUS.md` — без новых
запусков 1cv8.exe. Registry-инвариант **сохранён точно**:
read-server = 15 public tools, write-server = 25 public
tools, intelligence-server = 16 public tools — без
изменений. Никаких новых MCP tool'ов; никаких новых
product-layer slice'ов; никаких изменений в
`mcp-read-server`, `mcp-write-server`,
`mcp-intelligence-server`, `onec-policy-engine`,
`onec-audit`, `onec-health`, `onec-process-runner`,
`onec-troubleshooting`, `mcp-common`, `onec-config`,
`selfcheck.py`, `bootstrap_paths.ps1`, `pyproject.toml`,
`.github/`, `.claude.json`. Все Step 5 правки
локализованы внутри `apps/platform/src/onec_platform/`:
`enterprise.py` (`_check_real_stand_contract` теперь
проверяет все три command template'а; `_SECTION_MAX_SCORE
['binary']` поднят с 2 до 4) + `realstand.py`
(`_build_plan_summary` обновлён + module-docstring) +
`__init__.py` (Step 7-блок package-docstring'а обновлён
до Track A-aware формулировки). Operator-facing argv
grammar / placeholder whitelists per tool / ToolResult
shape / `RealStandSmokeResult` / `EnterpriseFoundationResult`
shape **без изменений**. Step 5 — это **surface-only**
update: продуктовый слой ничего не пишет на диск, не
зовёт `run_write_flow`, не открывает subprocess'ы. Step 6
— **operator-driven exercise**: ship'нут один runbook
+ один prereq-inventory скрипт; production-код **не
тронут**; реальный round-trip запускается оператором
на reference stand'е, который должен быть подготовлен
по runbook'у (declared product-config, real infobase,
real DESIGNER credentials). В текущем dev-окружении
шаг **partial result**: real 1cv8 binary найден на
машине, render-pipeline для всех трёх template'ов OK,
но stand prereq'ы (infobase, source dump, credentials)
отсутствуют, поэтому real round-trip не запускался —
был бы нечестным. Это **partial slice** Track A, не
его финальное закрытие (Step 6 ждёт стенд, Step 7 —
final integration pass + closure). Safety
guarantees Phase 1–6 (`run_write_flow` единственный
mutating-путь; intelligence read-only;
`onec_policy_engine` не импортируется в
product/intelligence; нет back-door write channel'а;
нет `shell=True`; audit append-only; fail-closed по
умолчанию) **сохраняются без изменений**).

После closure'а Track C был открыт четвёртый post-phase track —
**Parallel Track D — Operator Credentials Hardening** — и
закрыт на Step 6 (final integration pass and Track D closure).
Track D ввёл `${ENV:NAME}` substitution путь для DESIGNER
credentials в `onec_*_command_template`-массивах с render-time
fail-closed на missing / empty / mixed формах, password-position
redaction (`<redacted>` в `command_preview` и trimmed excerpt'ах
при сохранённом unredacted subprocess argv), миграцию
operator-facing docs на env-substitution как рекомендованный
default (literal cleartext остался legacy fallback), и 8-й
credential-template-hygiene check в
`scripts/release/verify-release.ps1` (WARN, не FAIL — legacy
templates не блокируют receive-side flow). Это **не**
enterprise security platform: никакого secrets manager / vault /
KMS / OS keychain / SSO / RBAC / encrypted-at-rest secrets file
format / production-grade MCP transport. Registry-инвариант
`read=15 / write=25 / intelligence=16` без drift'а на всём треке;
никаких реальных credentials ни в одном из шести Track D
commit'ов. **GitHub remote push не часть трека — operator action.**

После closure'а Track D был открыт пятый post-phase track —
**Parallel Track E — Multi-Version 1C Smoke Matrix** — и
закрыт на Step 6 (final integration pass and Track E
closure). Track E ship'нул frozen narrow smoke scenario
`frozen-smoke-v1` (cut-down `create_dump_snapshot` через
`/DumpConfigToFiles` only — read-only из перспективы 1С
базы), operator runbook
(`docs/runbooks/track-e-multi-version-smoke-matrix.md`) и
matrix-table doc (`docs/version-support-matrix.md`) с
12-column frozen contract'ом и reference row на
`8.3.27.1859`, заполненной copy-only из existing Track A /
Step 6 evidence (без новых 1cv8.exe runs). Step 4 закрыт
через **PATH B (honest operator-supplied gap)**: на
operator machine отсутствуют 1С minor families помимо
`8.3.27`; никаких additional evidence rows не добавлено,
никакого 1cv8.exe не запускалось. Step 5 выровнял
operator-facing docs (SECURITY / release-handoff / README)
под фактический evidence-уровень: reference есть, matrix
scaffolding есть, additional rows нет, **no blanket
multi-version support claim**. Платформа архитектурно
остаётся multi-version-friendly: оператор сам выбирает
binary path в config'е; Track E добавил evidence-уровень
и docs, **не** архитектуру. Это **не** «поддержка всех
версий», **не** full QA program, **не** performance /
stress / fuzzing track, **не** enterprise certification.
Registry-инвариант `read=15 / write=25 / intelligence=16`
без drift'а на всём треке; никаких реальных credentials
ни в одном из шести Track E commit'ов. **GitHub remote
push не часть трека — operator action.**

После closure'а Track E был открыт шестой post-phase track —
**Parallel Track F — Rollback Whitelist Expansion** — и
закрыт на Step 6 (final integration pass and Track F
closure). Track F расширил `_AUTOMATIC_RECOVERY_SUPPORTED`
whitelist в `apps/platform/src/onec_platform/recovery.py` и
mirror `_ROLLBACK_SUPPORTED_OPERATIONS` в
`apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
с 2 до 6 identical entries — добавлены `add_form_attribute`,
`add_form_element`, `append_module_method`,
`replace_module_method_body`. **Это не** universal rollback,
**не** «rollback теперь есть везде», **не** public
`delete_*` write-tools, **не** multi-file / DB schema
rollback, **не** AST-based semantic reverse engine, **не**
новый MCP surface. Coverage = 6 of 25 mutating registry tools
= 24% surface; 19 mutating tools остаются manual
snapshot-restore territory by design. Платформа архитектурно
осталась при том же подходе: rollback идёт через public
write-tool по `run_write_flow` дисциплине; Track F расширил
**whitelist configuration**, не mechanism. Production-код
Track F правил **только два** boundary'а в одном Step 4
commit'е (`recovery.py` + `flow.py` synchronized); шаги
1, 2, 3, 5 — documentation-only. **Q5 resolved** на Step 6 =
**ДА**: `pyproject.toml` version bumped `0.2.0` → `0.3.0`
(Track F / Step 4 ship'нул real code change с functional
delta = backward-compatible new functionality classifying
as MINOR bump per SemVer; precedent — Track D `0.1.0 → 0.2.0`).
Registry-инвариант `read=15 / write=25 / intelligence=16`
без drift'а на всём треке; никаких реальных credentials ни
в одном из шести Track F commit'ов; никаких 1cv8.exe runs
ни на одном шаге Track F. **GitHub remote push не часть
трека — operator action.**

После closure'а Track F был открыт седьмой post-phase
track — **Parallel Track G — Production-Grade MCP Transport
and CLI** — и закрыт на Step 6 шестью последовательными
шагами. Track G ship'ил **первый production-grade
operational слой** для трёх MCP servers, закрывая factual
gap «MCP servers cannot start at all»: canonical
`__main__.py` для всех трёх MCP servers, minimum-viable
stdio JSON-RPC 2.0 transport (line-delimited, stdlib-only),
minimal CLI surface (`--help`, `--config-path`, `--transport`,
`--log-level`), `[project.scripts]` console entry points в
`pyproject.toml`. Это **не** universal production transport,
**не** network-grade HTTP/WebSocket layer, **не**
authentication / authorization, **не** supervisor daemon,
**не** HA / clustering, **не** web UI, **не** packaging
ecosystem (`.msi` / `.deb` / signed distribution / PyPI
publication beyond `[project.scripts]`), **не** enterprise
super-set (SSO/RBAC/multi-tenant), **не** standalone
`apps/platform` entrypoint (Q6 explicit out-of-scope).
Платформа архитектурно осталась при том же подходе: existing
`server.py:REGISTERED_TOOLS` registries для всех 3 MCP servers
preserved byte-identical (`list_tools()` / `get_tool(name)`
API без изменений); Track G ship'ил **transport layer
поверх** этих registries, не задевая их. Production-код
Track G правил **только Step 4 commit** и **только** на
explicit allowed surfaces (3 new `__main__.py` files +
1 new private `mcp_common._stdio_transport` helper +
`pyproject.toml` `[project.scripts]` block); шаги 1, 2, 3, 5,
6 — documentation/status/version-only. **Q7 resolved** на
Step 6 = **ДА**: `pyproject.toml` version bumped `0.3.0` →
`0.4.0` (Step 4 ship'нул real code change с observable
runtime capability delta — backward-compatible new
functionality classifying as MINOR bump per SemVer;
precedent — Track D `0.1.0 → 0.2.0` и Track F
`0.2.0 → 0.3.0`). Никаких изменений в `tools.py`, `runtime/`
packages, `scripts/release/`, registries (без drift'а),
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`, examples/,
1cv8.exe surface. Никаких 1cv8.exe runs ни на одном шаге
Track G (трек работает на process / transport layer уровне,
не на 1cv8 binary surface). Никаких реальных credentials
ни в одном из шести Track G commit'ов. **GitHub remote
push явно НЕ часть трека** — это operator action.

## Что сделано

### Phase 0 / Step 1 — каркас монорепозитория (завершён)

- Создана корневая папка проекта `C:\Tools\1c-agent-platform`.
- Создана полная структура каталогов монорепозитория:
  - `apps/` с подпапками `mcp-read-server`, `mcp-write-server`, `mcp-intelligence-server`;
  - `packages/` с подпапками `mcp-common`, `onec-process-runner`, `onec-policy-engine`,
    `onec-audit`, `onec-health`, `onec-troubleshooting` (позже добавлен `onec-config`);
  - `docs/` с подпапками `architecture`, `tools-spec`, `safety`, `runbooks`, `api`;
  - `examples/` с подпапками `demo-infobase`, `demo-dumps`, `sample-patches`;
  - `scripts/` с подпапками `dev`, `test`, `release`.
- Созданы базовые файлы в корне репозитория:
  - `README.md`, `PROJECT-STATUS.md`, `.gitignore`.
- В каждой папке первого уровня внутри `apps/`, `packages/`, `docs/`, `examples/`, `scripts/`
  добавлен короткий `README.md` с назначением раздела.

### Phase 0 / Step 2 — root-конфиг и Python bootstrap (завершён)

- Добавлен корневой `pyproject.toml` (минимальный: `hatchling`, метаданные проекта,
  базовые настройки `ruff` и `pytest`, пустой список пакетов в `hatch`).
- Добавлен `.editorconfig` (utf-8, LF, 4 пробела, отдельное правило для `*.md`).
- Добавлен `.python-version` (Python 3.11).
- Создан `src`-bootstrap для каждого приложения и пакета с `__init__.py`
  и собственным `README.md`.

### Phase 0 / Step 3 — базовые общие пакеты-заглушки (завершён)

- `mcp-common`: базовые контексты и исключения.
- `onec-process-runner`: `ProcessRunRequest`, `ProcessRunResult`,
  `run_process` (stub, поднимает `NotImplementedError`).
- `onec-policy-engine`: `PolicyDecision`, `check_write_allowed`.
- `onec-audit`: `AuditRecord`, `format_audit_record`.
- `onec-health`: `HealthCheckResult`, `check_dump_path_exists`.

### Phase 0 / Step 4 — troubleshooting / config / health flow (завершён)

- Добавлен новый пакет `onec-config`:
  `EnvironmentConfig`, `ProjectConfig`, `load_project_config`.
- `onec-troubleshooting`: `TroubleshootingReport`, `diagnose_from_health`.
- `onec-health` расширен: `summarize_health`, stub-проверки
  `check_http_gateway_available`, `check_search_index_available`.

### Phase 0 / Step 5 — skeleton для mcp-read-server (завершён)

- `mcp-read-server`: `ToolResult`, `ping()`, `health_summary(...)`.
- Server registry skeleton (`REGISTERED_TOOLS`, `list_tools()`, `get_tool()`).
- Wiring к `onec-health` и `onec-troubleshooting`.

### Phase 0 / Step 6 — skeleton для mcp-write-server и mcp-intelligence-server (завершён)

- `mcp-write-server`, `mcp-intelligence-server`: `ToolResult`, `ping()`, registry skeleton.
- Все три сервера платформы получили выровненный минимальный bootstrap.

### Phase 0 / Step 7 — workspace / import wiring и self-check (завершён)

- Создан `scripts/dev/bootstrap_paths.ps1` — PowerShell-скрипт,
  выставляющий `PYTHONPATH` под монорепо в **только текущую** сессию
  (10 путей: 3 apps + 7 packages). Не трогает системный PATH и реестр.
- Создан `scripts/dev/selfcheck.py` — минимальный self-check, который
  импортирует все skeleton-модули и безопасно вызывает их базовые функции
  (`ping`, `list_tools`, `check_write_allowed`, `summarize_health`,
  `diagnose_from_health`, `load_project_config`, `format_audit_record`,
  `health_summary`) на встроенных фиктивных данных. Без `try/except` —
  любая ошибка wiring должна валиться честно.
- Создан `scripts/dev/README.md` — описание назначения скриптов
  и команд запуска.
- Подтверждено, что `bootstrap_paths.ps1` отрабатывает корректно:
  `PYTHONPATH` проставляется, все 10 `src/` путей видны в текущей сессии.
- В `selfcheck.py` добавлен реальный вызов `health_summary(...)` через
  wiring `mcp-read-server → onec-health → onec-troubleshooting` и печать
  `health_summary_ok` / `health_summary_problem`.
- После установки реального Python 3.11+ selfcheck запущен локально
  и прошёл успешно: `imports_ok = true`, все три сервера видят свои
  registry-инструменты, `health_summary_ok = false` для заведомо плохих
  входных данных с корректным `health_summary_problem = gateway_down`,
  `selfcheck_status = ok`.

**Итог Step 7:**

- PYTHONPATH bootstrap работает в рамках текущей PowerShell-сессии.
- Все skeleton-модули (`mcp_read_server`, `mcp_write_server`,
  `mcp_intelligence_server`, `onec_policy_engine`, `onec_audit`,
  `onec_config`, `onec_health`, `onec_troubleshooting`) импортируются
  без ошибок.
- `scripts/dev/selfcheck.py` прошёл успешно и выдал
  `selfcheck_status = ok`.

### Phase 0 / Step 8 — mcp-common bootstrap contract и унификация envelope / registry (завершён)

- `mcp-common` расширен shared response envelope:
  `mcp_common/result.py` — dataclass `ToolResult`
  (`ok`, `tool_name`, `message`, `payload`). Это единый конверт ответа
  для всех трёх MCP-серверов платформы.
- `mcp-common` расширен shared registry helpers:
  `mcp_common/registry.py` — `ToolCallable`,
  `build_tool_registry(tools)`, `list_registered_tools(registry)`,
  `get_registered_tool(registry, name)`. Без валидации и магии,
  только стандартная библиотека.
- `mcp_common/__init__.py` теперь экспортирует:
  `OperationContext`, `PlatformError`, `PolicyDeniedError`,
  `ProcessExecutionError`, `HealthCheckError`, `ToolResult`,
  `ToolCallable`, `build_tool_registry`, `list_registered_tools`,
  `get_registered_tool`.
- `mcp-read-server`, `mcp-write-server`, `mcp-intelligence-server`
  приведены к общему контракту:
  - `models.py` в каждом сервере стал compatibility wrapper,
    re-export `ToolResult` из `mcp_common` — старые внутренние
    импорты `.models` продолжают работать;
  - `server.py` каждого сервера собирает `REGISTERED_TOOLS`
    через `build_tool_registry(...)`, а `list_tools()` / `get_tool()`
    делегируют shared helpers;
  - `tools.py` по смыслу не менялся.
- README `mcp-common` обновлён: shared exception hierarchy,
  `OperationContext`, shared `ToolResult`, shared registry helpers.
  README трёх серверов помечены как использующие shared contracts из
  `mcp-common`.
- Локальный `scripts/dev/selfcheck.py` (без изменений на этом шаге)
  повторно запущен после унификации и прошёл успешно:
  `imports_ok = true`, registry-составы серверов не изменились
  (`read=['health_summary','ping']`, `write=['ping']`,
  `intelligence=['ping']`), `health_summary_ok = false`,
  `health_summary_problem = gateway_down`, `selfcheck_status = ok`.

### Phase 0 / Step 9 — минимальный CI skeleton + единая команда локальной проверки (завершён)

- Добавлен `scripts/dev/run_dev_check.ps1` — единая локальная dev-check
  команда. Dot-source'ит `bootstrap_paths.ps1` в текущей сессии и
  запускает `selfcheck.py`; при успехе печатает
  `Dev check completed successfully.`, при ошибке завершается с exit
  code, полученным от Python. Ничего не устанавливает и не меняет
  системное окружение.
- Добавлен `.github/workflows/dev-check.yml` — минимальный CI skeleton.
  Один job `dev-check` на `windows-latest`: checkout,
  `actions/setup-python@v5` с Python 3.11, затем в pwsh-шаге
  `bootstrap_paths.ps1` + `selfcheck.py`. Без установки пакетов,
  без pytest, ruff, matrix и других job'ов.
- Добавлен `docs/runbooks/local-dev-check.md` — короткий runbook
  локальной dev-проверки: цель, prerequisites, команда запуска,
  критерии успеха, типовые падения.
- Обновлён `scripts/dev/README.md` — упомянута новая команда
  `run_dev_check.ps1` и соответствие CI workflow. Зафиксировано,
  что это минимальный quality gate Phase 0, проверяющий только
  import/wiring skeleton-проекта.
- Локальный `run_dev_check.ps1` запущен в текущей сессии: bootstrap
  выставляет все 10 `src/` путей, `selfcheck.py` печатает
  `selfcheck_status = ok`, скрипт заканчивает работу сообщением
  `Dev check completed successfully.`

### Phase 0 / Finalize — закрытие инфраструктурной фазы (завершён, Phase 0 закрыта)

- Добавлен `docs/architecture/phase-0-summary.md` — итоги Phase 0:
  назначение, что собрано, что подтверждено на практике, что пока
  ещё не реализовано, вывод по фазе.
- Добавлен `docs/architecture/phase-1-entry.md` — точка входа в Phase 1:
  цель фазы, что готово на входе, первое приближение набора
  read-tools, критерии MVP фазы, риски.
- Корневой `README.md` приведён в актуальное состояние: устаревший
  единичный блок «Статус» заменён на раздел «Текущий статус по фазам»
  с явной отметкой закрытия Phase 0 и входа в Phase 1 и ссылками
  на оба новых документа архитектуры.
- **Phase 0 завершена.** Инфраструктурная база готова:
  монорепо + shared контракты + skeleton трёх серверов + воспроизводимый
  dev-check локально и в CI.
- `dev-check` подтверждён зелёным: `selfcheck_status = ok`,
  `Dev check completed successfully.`
- Следующим этапом открывается Phase 1 — Read MVP.

### Phase 1 / Step 1 — планирование Read MVP и фиксация первого набора реальных read-tools (завершён)

- Phase 0 закрыта; Phase 1 — активная фаза разработки.
- Добавлен `docs/architecture/phase-1-read-mvp-plan.md` — план Read MVP:
  назначение фазы, целевой результат, первый набор инструментов по
  группам A (live-read), B (dump-read), C (health/diagnostics),
  порядок реализации внутри Phase 1, что не входит в Read MVP,
  критерии приёмки.
- Добавлен `docs/architecture/phase-1-step-map.md` — стартовый
  implementation map на первые 6 шагов Phase 1: реальный
  `onec-process-runner`, рабочий `onec-config` окружения,
  реальные live-health-checks в `onec-health`, базовый runtime/adapter
  слой для `mcp-read-server`, первые live-read инструменты,
  первые dump-read инструменты.
- Зафиксирован первый набор инструментов MVP:
  live-read — `get_configuration_info`, `get_metadata_tree`,
  `get_metadata_object`, `get_object_structure`, `get_form_structure`,
  `validate_query`, `execute_read_query`, `get_event_log`;
  dump-read — `read_module_code_from_dump`, `search_code`,
  `search_metadata`;
  diagnostics — `check_runtime_health`, `diagnose_connectivity_issue`.
- Обновлён корневой `README.md`: существующий блок «Текущий статус по
  фазам» уточнён — Phase 1 помечена как активный этап, добавлены
  ссылки на `phase-1-read-mvp-plan.md` и `phase-1-step-map.md`.

### Phase 1 / Step 2 — реальный `onec-process-runner` вместо stub (завершён)

- В `packages/onec-process-runner` stub заменён на реальный runner
  поверх `subprocess.run`. Никаких `shell=True`, `os.system` или
  ручного `Popen`.
- `ProcessRunRequest` расширен до нужного минимума: добавлены
  `env: dict[str, str] | None`, `input_text: str | None`, тип
  `timeout_seconds` расширен до `int | float | None`. `ProcessRunResult`
  оставлен без изменений (`exit_code`, `completed`, `stdout`, `stderr`).
- Runner поддерживает `cwd`, `timeout_seconds`, `env`, `input_text`,
  захват stdout/stderr в текстовом режиме. `check=False` — коды
  возврата не конвертируются в исключения.
- **Timeout** (`subprocess.TimeoutExpired`) не выбрасывается наружу:
  возвращается `ProcessRunResult(completed=False, exit_code=-1, ...)`
  с частично собранным stdout/stderr и служебной пометкой о таймауте
  в stderr.
- **`FileNotFoundError`** (отсутствует исполняемый файл) и прочие
  `OSError` на старте процесса преобразуются в `ProcessExecutionError`
  из `mcp_common` с понятным сообщением.
- README пакета переписан: актуальное поведение, контракт ошибок,
  ограничения (не shell, не логи, не файлы).
- Ручная проверка трёх сценариев выполнена через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - A (success): `completed=True`, `exit_code=0`, `stdout='runner-ok'`;
  - B (timeout): `completed=False`, `exit_code=-1`, stderr содержит
    `[onec-process-runner] process timed out after 0.5 seconds`;
  - C (missing command): поднят `ProcessExecutionError: Executable
    not found: definitely-nonexistent-command-xyz`.
- `dev-check` после изменений остался зелёным: `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 1 / Step 3 — рабочая модель окружения в `onec-config` (завершён)

- `EnvironmentConfig` расширен до рабочей формы: добавлены обязательные
  поля `base_id: str`, `dump_path: str`, `timeout_seconds: int | float`.
  Существующие поля (`name`, `base_path`, `publication_name`,
  `http_base_url`, `allow_write`) сохранены. `allow_write` остаётся
  опциональным со значением по умолчанию `False`. `ProjectConfig`
  без изменений (`environments: dict[str, EnvironmentConfig]`).
- `load_project_config(data)` теперь валидирует структуру:
  `ValueError` при отсутствии ключа `environments`, при пустом
  `environments` и при отсутствии любого обязательного поля в
  окружении — с именем окружения и именем поля в тексте ошибки.
  Никаких файловых операций, `os.environ` или внешнего I/O —
  чистая валидация входного dict'а.
- `__init__.py` уже экспортировал `EnvironmentConfig`, `ProjectConfig`,
  `load_project_config` через `__all__` — оставлен как есть.
- README `onec-config` переписан: перечислены обязательные поля,
  описано поведение loader'а и явно зафиксировано, что чтение из
  файлов/переменных окружения пока не реализовано.
- Ручная проверка трёх сценариев выполнена через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - A (valid config): `environments=['local-dev']`, все поля
    прочитаны корректно, `allow_write=True` учтён;
  - B (missing `environments`): `ValueError: Config is missing
    required key 'environments'.`;
  - C (missing required field `dump_path`): `ValueError: Environment
    'local-dev' is missing required field 'dump_path'.`.
- **Follow-up по `selfcheck.py` выполнен.** В тестовый dict
  `load_project_config` в `scripts/dev/selfcheck.py` добавлены
  безопасные фиктивные значения для новых обязательных полей:
  `base_id="local-dev"`, `dump_path="C:\\tmp\\dump\\local-dev"`,
  `timeout_seconds=30`. Остальная логика selfcheck'а не менялась,
  `run_dev_check.ps1` и `bootstrap_paths.ps1` не трогались.
- **Dev-check снова зелёный** после follow-up:
  `imports_ok = true`, `config_envs = ['local-dev']`,
  `health_summary_ok = false`, `health_summary_problem = gateway_down`,
  `selfcheck_status = ok`, `Dev check completed successfully.`

### Phase 1 / Step 4 — реальные live/dump health checks в `onec-health` (завершён)

- `onec-health` переведён со stub на реальные проверки. Контракт
  `HealthCheckResult` и `summarize_health` не меняются.
- `check_dump_path_exists(path)` — без изменений, уже был реальной
  проверкой через `pathlib.Path.exists()`.
- `check_http_gateway_available(target, timeout_seconds=None)` теперь
  работает в двух режимах:
  - `target: bool` — legacy stub-режим, сохранён ради совместимости
    с текущим `scripts/dev/selfcheck.py`;
  - `target: str` — реальный HTTP probe через `urllib.request`:
    `status="ok"` при HTTP 2xx/3xx, `status="error"` иначе. Сетевые
    исключения, таймауты и `HTTPError` не выходят наружу —
    всегда возвращается `HealthCheckResult` с кратким пояснением.
- `check_search_index_available(target)` также получила два режима:
  - `target: bool` — legacy stub;
  - `target: str` — путь к каталогу выгрузки: `status="ok"`, если
    каталог существует и рекурсивно найден хотя бы один файл `.bsl`;
    иначе `error`. Ошибки сканирования ловятся, не вылетают наружу.
- Добавлена функция
  `check_environment_health(environment: EnvironmentConfig)` —
  запускает три базовых проверки по `EnvironmentConfig` из
  `onec-config` (`dump_path`, `http_base_url` + `timeout_seconds`,
  `dump_path`) и возвращает список из трёх `HealthCheckResult` в
  стабильном порядке.
- `__init__.py` дополнен экспортом `check_environment_health` в
  `__all__`.
- README `onec-health` переписан: явно зафиксирован выход из stub,
  bool-совместимость, контракт новых режимов, what-not-does.
- **Ручная проверка на реальном стенде** выполнена через временные
  скрипты в `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - **A (`dump_path_exists`)**: путь
    `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101`
    существует → `status="ok"`. ✓
  - **B (`http_gateway` по URL
    `http://localhost:8080/InfoBase5/hs/mcp-1c/version`)**:
    `status="error"` — WinError 10061 (connection refused).
    Проверка `Test-NetConnection localhost 8080` подтвердила, что
    TCP-порт 8080 сейчас **не слушается**, то есть Apache стенда
    не запущен. Это не баг реализации, а фактическое состояние
    окружения; инструкция запрещает трогать Apache/публикацию.
  - **B-local (контрольная проверка success-path)**: запущен
    короткоживущий `http.server` внутри того же Python-процесса на
    случайном порту `127.0.0.1:<port>`; `check_http_gateway_available`
    вернул `status="ok"` (HTTP 200). Это подтверждает, что сам
    HTTP-probe (urllib, тайм-аут, обработка кода ответа) работает
    корректно. Отрицательный результат пункта B — честный сигнал
    о состоянии стенда.
  - **C (`search_index` по dump path)**: dump содержит `.bsl` →
    `status="ok"`. ✓
  - **D (`check_environment_health` по реальному `EnvironmentConfig`
    стенда)**: возвращён список из трёх `HealthCheckResult`;
    `dump_path_exists=ok`, `http_gateway=error` (по той же причине,
    что и B), `search_index=ok`. Помимо HTTP-части, ожидание ТЗ
    (три ok) не подтверждено ровно потому, что Apache стенда сейчас
    лежит; сам helper работает правильно — все три проверки
    выполнены в правильном порядке, каждая вернула корректный
    `HealthCheckResult` для фактического состояния ресурса.
- **Dev-check после изменений зелёный:**
  `imports_ok = true`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Сохранённая bool-совместимость
  в `check_http_gateway_available(False)` и
  `check_search_index_available(True)` удерживает skeleton selfcheck
  работоспособным.

### Phase 1 / Step 5 — базовый runtime/adapter слой для `mcp-read-server` (завершён)

- Внутри `apps/mcp-read-server/src/mcp_read_server/` создан подпакет
  `runtime/` — внутренний слой ниже tool-уровня. Пока он не
  используется ни одним зарегистрированным инструментом: `tools.py`,
  `server.py`, верхний `__init__.py` и `models.py` read-server'а
  не тронуты. Skeleton registry остался прежним.
- **`runtime/models.py`** — dataclass `RuntimeContext(environment,
  health_results, health_codes)`. Импортирует `EnvironmentConfig` из
  `onec_config`, `HealthCheckResult` из `onec_health`.
- **`runtime/context.py`** — `build_runtime_context(environment)`:
  вызывает `check_environment_health(environment)`, затем
  `summarize_health(...)`, возвращает `RuntimeContext`. Без
  side-effects и без искусственных исключений.
- **`runtime/live_adapter.py`** — `fetch_json(url, timeout_seconds)`:
  HTTP GET через `urllib.request`, UTF-8 decode, `json.loads`,
  проверка что тело — именно dict. Любые сетевые/decode-ошибки
  заворачиваются в `PlatformError` из `mcp-common`.
  `fetch_json_from_environment(environment, relative_path)` —
  аккуратная сборка `base.rstrip('/') + '/' + relative.lstrip('/')`
  (без двойных слэшей), вызов `fetch_json` с таймаутом окружения.
- **`runtime/dump_adapter.py`** — `resolve_dump_path(environment)`,
  `read_text_file(path)` (UTF-8 + `errors='replace'`, ошибки →
  `PlatformError`), `find_files_by_pattern(root, pattern)`
  (отсортированный `rglob`, `PlatformError` если `root` нет),
  `read_dump_file(environment, relative_path)`.
- **`runtime/__init__.py`** экспортирует в `__all__`: `RuntimeContext`,
  `build_runtime_context`, `fetch_json`, `fetch_json_from_environment`,
  `resolve_dump_path`, `read_text_file`, `find_files_by_pattern`,
  `read_dump_file`.
- README `mcp-read-server` дополнен разделом «Runtime / adapters
  layer» с кратким описанием трёх подсистем (context builder,
  live HTTP adapter, dump file adapter).
- **Ручная проверка 4 сценариев** через временный скрипт в `%TEMP%`
  под bootstrap'нутым `PYTHONPATH`:
  - **A (`build_runtime_context` по реальному `EnvironmentConfig`):**
    `RuntimeContext`, `health_results_len = 3`, `health_codes =
    ['gateway_down']` (как и ожидалось — Apache стенда не запущен).
    Результаты: `dump_path_exists=ok`, `http_gateway=error`,
    `search_index=ok`. ✓
  - **B (`fetch_json` против URL стенда):** `PlatformError: Failed
    to fetch http://localhost:8080/InfoBase5/hs/mcp-1c/version:
    <urlopen error [WinError 10061] ...>` — транспортная ошибка
    корректно заворачивается в `PlatformError`. Apache по-прежнему
    не поднят, инструкция запрещает его трогать.
  - **B-local (success-path `fetch_json`):** локальный
    `socketserver.TCPServer` с `BaseHTTPRequestHandler`, отдающий
    `{"version": "local-test-1.0"}`. Результат:
    `{'version': 'local-test-1.0'}` — JSON правильно раздекодирован
    в dict, dict-guard не ложно-позитивен.
  - **C (`resolve_dump_path` + `find_files_by_pattern`):** путь
    резолвится корректно; `find_files_by_pattern(root, "*.bsl")`
    возвращает 1 файл —
    `CommonModules\MCPTestCode\Ext\Module.bsl`. ✓
  - **D (`read_dump_file` для
    `CommonModules\MCPTestCode\Ext\Module.bsl`):** возвращён
    непустой текст (`text_len = 215`), маркер `MCP_SMOKE_TEST`
    найден, кириллическое имя функции `ПолучитьСтатусMCP` найдено
    (в консоли Windows отображение сбилось по кодовой странице,
    но substring-поиск идёт по Python-строке и честно возвращает
    `True`). ✓
- **Dev-check после изменений зелёный:** `selfcheck_status = ok`,
  `Dev check completed successfully.` Новый подпакет не
  импортируется из skeleton selfcheck (он, согласно ТЗ, не менялся);
  существующий wiring read-server'а сохранён как есть.

### Phase 1 / Step 6 — первые live-read инструменты (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных live-read инструмента поверх runtime/adapter слоя
  Step 5:
  - `get_configuration_info(environment)` — GET
    `<http_base_url>/configuration`;
  - `get_metadata_tree(environment, filter_value=None)` — GET
    `<http_base_url>/metadata`, при заданном `filter_value`
    добавляется `?filter=<urllib.parse.quote(filter_value)>`;
  - `get_metadata_object(environment, object_name)` — GET
    `<http_base_url>/metadata/object?name=<urllib.parse.quote(...)>`.
- Все три tool'а работают по одной схеме: вызывают
  `build_runtime_context(environment)`, кладут `health_codes` в
  `payload.runtime`, вызывают `fetch_json_from_environment(...)` и
  возвращают shared `ToolResult`. Любая `PlatformError` от live
  adapter заворачивается в `ToolResult(ok=False, ...)` — исключение
  наружу не уходит. Существующие `ping` и `health_summary` не
  менялись.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 5 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  отсортированно: `['get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping']`.
- README `mcp-read-server` дополнен: зафиксирована первая волна
  реальных live-read инструментов, общая схема «runtime context →
  fetch_json_from_environment → ToolResult», wiring с новым runtime
  подпакетом и `onec-config`.
- **Ручная проверка 4 сценариев** против реального стенда и
  контрольного локального HTTP-сервера (временный скрипт в
  `%TEMP%`, `PYTHONPATH` через bootstrap):
  - **A `get_configuration_info`**: против реального стенда —
    `ok=False`, `tool="get_configuration_info"`, message
    содержит `Failed to fetch http://localhost:8080/InfoBase5/hs/
    mcp-1c/configuration: <urlopen error [WinError 10061] ...>`,
    `payload.runtime.health_codes=['gateway_down']`. Apache
    по-прежнему не поднят; инструкция запрещает его трогать.
  - **B `get_metadata_tree`**: против реального стенда — `ok=False`,
    URL собран корректно: `/metadata` без query string.
  - **C `get_metadata_tree(filter_value="ОбщиеМодули")`**: против
    реального стенда — `ok=False`, URL
    `/metadata?filter=%D0%9E%D0%B1%D1%89%D0%B8%D0%B5%D0%9C%D0%BE%
    D0%B4%D1%83%D0%BB%D0%B8` (кириллица корректно URL-encoded через
    `urllib.parse.quote`).
  - **D `get_metadata_object("Справочник.Фильмы")`**: против
    реального стенда — `ok=False`, URL
    `/metadata/object?name=%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1
    %87%D0%BD%D0%B8%D0%BA.%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B`.
    Точка между типом и именем сохраняется (это не reserved char).
  - Во всех четырёх случаях tool вернул `ToolResult`, наружу
    исключение не вышло — контракт соблюдён.
  - **Контрольный success-path** на локальном
    `socketserver.TCPServer` с маршрутизацией
    `/configuration` / `/metadata` / `/metadata/object`:
    - `A(local)` — `ok=True`, `data={'name':'DemoConfig',
      'version':'1.0'}`;
    - `B(local)` — `ok=True`, `data.tree` отдан, `filter_echo=None`;
    - `C(local)` — `ok=True`, сервер получил корректно
      URL-encoded фильтр (проверено substring'ом `%D0%9E`);
    - `D(local)` — `ok=True`, name пришло на сервер
      URL-encoded (substring `%D0%A1`), раздекодировано обратно
      корректно.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping']`, `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался — регрессии wiring
  нет.

### Phase 1 / Step 7 — первые dump-read инструменты (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных dump-read инструмента поверх `runtime/dump_adapter.py`
  (без regex, без внешних зависимостей, только стандартная
  библиотека):
  - `read_module_code_from_dump(environment, relative_path)` — читает
    текст одного файла через `read_dump_file(...)`, возвращает
    `ToolResult` с `payload.data = {"relative_path", "text"}`;
  - `search_code(environment, query)` — пробегает все `*.bsl` файлы
    (`find_files_by_pattern(resolve_dump_path(...), "*.bsl")`),
    делает `text.find(query)`, на каждом попадании собирает dict
    `{relative_path, matched=True, preview}`. Preview — фрагмент
    ±80 символов вокруг первого вхождения через общий helper
    `_snippet(...)`, защищённый от выхода за границы строки;
  - `search_metadata(environment, query)` — то же по `*.xml`, но
    совпадение засчитывается и по имени файла, и по содержимому.
    Для filename-only совпадений `preview` — пустая строка; для
    content-совпадений используется тот же `_snippet`.
  - Общая схема всех трёх tool'ов: `build_runtime_context(...)`,
    вызов dump-адаптера, оборачивание в shared `ToolResult`. Любая
    `PlatformError` от adapter-слоя → `ToolResult(ok=False, ...)` с
    `runtime.health_codes` в payload. Существующие ping/health_summary
    и live-tools не менялись.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 8 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  отсортированно:
  `['get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata']`.
- README `mcp-read-server` дополнен описанием первой волны
  dump-read инструментов, обновлён перечень registry (8 имён),
  и зафиксирована единая схема (live + dump) «runtime context →
  adapter → `ToolResult` с оборачиванием `PlatformError` в
  `ok=False`».
- **Ручная проверка 4 сценариев** против реального dump
  `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101`
  (временный скрипт в `%TEMP%`, `PYTHONPATH` через bootstrap):
  - **A `read_module_code_from_dump(env, "CommonModules\\MCPTestCode
    \\Ext\\Module.bsl")`**: `ok=True`,
    `payload.data.text_len = 215`, найдены оба ожидаемых маркера
    (`MCP_SMOKE_TEST` и кириллическое имя функции `ПолучитьСтатусMCP`
    — подтверждено substring-булевами `True`/`True`),
    `runtime.health_codes = ['gateway_down']` (Apache по-прежнему
    лежит, но dump-tool'у это не мешает).
  - **B `search_code(env, "MCP_SMOKE_TEST")`**: `ok=True`,
    `match_count = 1`, единственный match — именно
    `CommonModules\MCPTestCode\Ext\Module.bsl`, `matched=True`,
    `preview` включает BOM и начало модуля с комментарием
    `// MCP_SMOKE_TEST`. Сообщение: `Code search completed
    successfully.`
  - **C `search_metadata(env, "Фильмы")`**: `ok=True`,
    `match_count = 3`:
    `Catalogs\Фильмы.xml` (и по имени файла, и по содержимому),
    `ConfigDumpInfo.xml` и `Configuration.xml` (по содержимому —
    XML-каталоги конфигурации перечисляют имя объекта). В каждой
    строке `preview_len > 0` для content-совпадений. Сообщение:
    `Metadata search completed successfully.`
  - **D `search_code(env, "THIS_STRING_SHOULD_NOT_EXIST_12345")`**:
    `ok=True`, `match_count = 0`, `matches == []`. Сообщение:
    `Code search completed: no matches found.`
  - Во всех четырёх случаях tool вернул `ToolResult`, наружу
    исключение не вышло — dump adapter не ломает контракт.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping', 'read_module_code_from_dump', 'search_code',
  'search_metadata']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 8 — query path: validate_query и execute_read_query (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  два реальных live-tool'а query path поверх уже существующего
  runtime/adapter слоя:
  - `validate_query(environment, query)` — GET
    `<http_base_url>/query/validate?text=<urllib.parse.quote(query)>`,
    возвращает `ToolResult` с `payload.data` от live-адаптера;
  - `execute_read_query(environment, query, row_limit=100)` — GET
    `<http_base_url>/query/execute?text=<urlencoded>&limit=<row_limit>`.
    Перед live-вызовом — **временный read-only guardrail**: текст
    запроса приводится к верхнему регистру и, если встретится любое
    из `_WRITE_KEYWORDS` (`INSERT`, `UPDATE`, `DELETE`, `DROP`,
    `ALTER`, `CREATE`, `TRUNCATE`), сразу возвращается
    `ToolResult(ok=False, message="Only read-only queries are
    allowed.")` без обращения к live. Это stop-gap до появления
    полноценного policy-слоя (Phase 2+).
  - Оба tool'а используют `build_runtime_context(...)`, кладут
    `health_codes` в `payload.runtime`, ловят `PlatformError` от
    live adapter и оборачивают его в `ToolResult(ok=False, ...)` —
    наружу исключение не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 10 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает:
  `['execute_read_query', 'get_configuration_info',
  'get_metadata_object', 'get_metadata_tree', 'health_summary',
  'ping', 'read_module_code_from_dump', 'search_code',
  'search_metadata', 'validate_query']`.
- README `mcp-read-server` дополнен разделом про query path и
  явной пометкой о временном keyword-guardrail; перечень registry
  обновлён до 10 имён.
- **Ручная проверка 5 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A `validate_query(env, "ВЫБРАТЬ 1 КАК Число")` против
    реального стенда**: `ok=False` — transport error ожидаемо
    обёрнут в `ToolResult`; URL собран корректно с URL-encoded
    кириллицей (`%D0%92%D0%AB%D0%91%D0%A0%D0%90%D0%A2%D0%AC ...`);
    `runtime.health_codes=['gateway_down']`. Apache стенда по-прежнему
    не запущен — инструкция запрещает его трогать.
  - **B `execute_read_query(env, "ВЫБРАТЬ 1 КАК Число",
    row_limit=10)` против реального стенда**: guardrail пропустил
    read-query; live endpoint недоступен → `ok=False` с transport
    error; URL содержит `limit=10`.
  - **C `execute_read_query(env, "DELETE FROM Something",
    row_limit=10)`**: `ok=False`, `message="Only read-only queries
    are allowed."`, payload содержит только `runtime`
    (`data_key_present=False`) — **live adapter не вызывался**,
    guardrail сработал до transport.
  - **D Контрольный success-path на локальном in-process HTTP-сервере**
    (`socketserver.TCPServer`, маршруты `/query/validate` и
    `/query/execute`, валидный JSON):
    - `validate_query(..., "ВЫБРАТЬ 1 КАК Число")` → `ok=True`,
      `data={'valid': True, 'text_echo': 'ВЫБРАТЬ 1 КАК Число'}`;
      URL содержит корректно URL-encoded кириллицу (substring-проверка
      `%D0%92%D0%AB%D0%91%D0%A0%D0%90%D0%A2%D0%AC` → True).
    - `execute_read_query(..., "ВЫБРАТЬ 1 КАК Число", row_limit=10)`
      → `ok=True`, `data={'rows': [[1]], 'columns': ['Число'],
      'text_echo': 'ВЫБРАТЬ 1 КАК Число', 'limit_echo': '10'}`;
      URL содержит и URL-encoded query, и `limit=10`
      (substring-проверки обе True).
  - **E Registry check**: `len(REGISTERED_TOOLS) == 10`, `list_tools()`
    возвращает требуемый алфавитный список из 10 имён. ✓
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['execute_read_query',
  'get_configuration_info', 'get_metadata_object',
  'get_metadata_tree', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 9 — get_event_log, get_object_structure, get_form_structure (завершён)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  три реальных live-read инструмента поверх уже существующего
  runtime/adapter слоя:
  - `get_event_log(environment, period_start=None, period_end=None,
    level=None, user=None)` — GET `<http_base_url>/event-log`.
    Переданные фильтры добавляются в query-string парами
    `start`/`end`/`level`/`user` с `urllib.parse.quote`; без
    фильтров URL остаётся без `?...`.
  - `get_object_structure(environment, object_name)` — GET
    `<http_base_url>/object/structure?name=<urllib.parse.quote(...)>`.
  - `get_form_structure(environment, object_name, form_name=None)`
    — GET `<http_base_url>/form/structure?object=<urlencoded>`,
    при переданном `form_name` добавляется `&form=<urlencoded>`.
- Все три tool'а работают по уже сложившейся единой схеме:
  `build_runtime_context(environment)`, `health_codes` в
  `payload.runtime`, вызов `fetch_json_from_environment(...)`,
  обёртка любой `PlatformError` в `ToolResult(ok=False, ...)` —
  наружу исключение не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 13 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Общая архитектура
  `server.py` не менялась. `list_tools()` теперь возвращает
  алфавитный список из 13 имён.
- README `mcp-read-server` дополнен секцией «event log и структура
  объектов/форм» и обновлённым перечнем registry (13 имён).
- **Ручная проверка 5 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A `get_event_log(env)`** против реального стенда: `ok=False`
    (Apache лежит), URL `/event-log` без query-string собран
    корректно, `runtime.health_codes=['gateway_down']`, исключение
    наружу не вышло.
  - **B `get_event_log(env, period_start="2026-01-01",
    period_end="2026-12-31", level="Error", user="user")`** против
    реального стенда: `ok=False`, URL содержит все четыре фильтра
    (`?start=2026-01-01&end=2026-12-31&level=Error&user=user`).
  - **C `get_object_structure(env, "Справочник.Фильмы")`** против
    реального стенда: `ok=False`, URL содержит URL-encoded
    `name=Справочник.Фильмы` (`%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%
    D0%BE%D1%87%D0%BD%D0%B8%D0%BA.%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%
    D1%8B`).
  - **D `get_form_structure(env, "Справочник.Фильмы",
    "ФормаСписка")`** против реального стенда: `ok=False`, URL
    содержит и URL-encoded `object=Справочник.Фильмы`, и
    `form=ФормаСписка`.
  - **E Контрольный success-path** на локальном in-process HTTP
    сервере (`socketserver.TCPServer` + маршруты `/event-log`,
    `/object/structure`, `/form/structure`, валидный JSON):
    - `get_event_log(..., all four filters)` → `ok=True`;
      `data.filters_echo = {'start': '2026-01-01',
      'end': '2026-12-31', 'level': 'Error', 'user': 'admin'}`;
      substring-проверки в `last_path` —
      `has_start/has_end/has_level/has_user` все True;
    - `get_object_structure(..., "Справочник.Фильмы")` → `ok=True`;
      `data.name` round-trip'нулось правильно; substring
      `%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%87%D0%BD%D0%B8%D0%BA`
      → True;
    - `get_form_structure(..., "Справочник.Фильмы",
      "ФормаСписка")` → `ok=True`; в URL присутствуют и
      `object=`, и `form=`;
    - `get_form_structure(..., "Справочник.Фильмы")` без
      `form_name` → `ok=True`, параметр `&form=` **отсутствует**
      в URL (`has_form_param=False`) — опциональная ветка работает.
  - Ни в одном сценарии исключение наружу не вышло.
- **Dev-check после изменений зелёный**:
  `read_server_tools = ['execute_read_query',
  'get_configuration_info', 'get_event_log', 'get_form_structure',
  'get_metadata_object', 'get_metadata_tree',
  'get_object_structure', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`, `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не трогался.

### Phase 1 / Step 10 — diagnostics wrapping (завершён, Phase 1 Read MVP закрыт окончательно)

- В `apps/mcp-read-server/src/mcp_read_server/tools.py` реализованы
  два завершающих диагностических инструмента Phase 1 поверх уже
  готовых блоков (`build_runtime_context`, `check_environment_health`,
  `summarize_health`, `diagnose_from_health`) — без изменений в
  пакетах `onec-health` и `onec-troubleshooting`:
  - `check_runtime_health(environment)` — агрегированный снимок
    здоровья окружения. `ok=True` при `health_codes == ["ok"]`,
    иначе `ok=False`. payload содержит `runtime.health_codes`,
    slice окружения (`name`, `base_id`, `http_base_url`,
    `dump_path`) и полный список `checks` (`check_name`, `status`,
    `message`) из `context.health_results`.
  - `diagnose_connectivity_issue(environment)` — human-readable
    обёртка над `diagnose_from_health`. При `health_codes == ["ok"]`
    возвращается `ok=True` с `data.problem_code/probable_cause/
    recommended_action = None`. При проблемах —
    `ok=False`, `report.problem_code/probable_cause/
    recommended_action` из `onec-troubleshooting`.
  - Оба tool'а следуют общей схеме Phase 1: `build_runtime_context`,
    `health_codes` в `payload.runtime`, исключение наружу не уходит.
- В `apps/mcp-read-server/src/mcp_read_server/server.py` registry
  расширен до 15 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. `list_tools()` теперь
  возвращает:
  `['check_runtime_health', 'diagnose_connectivity_issue',
  'execute_read_query', 'get_configuration_info', 'get_event_log',
  'get_form_structure', 'get_metadata_object', 'get_metadata_tree',
  'get_object_structure', 'health_summary', 'ping',
  'read_module_code_from_dump', 'search_code', 'search_metadata',
  'validate_query']`.
- README `mcp-read-server` дополнен секцией «diagnostics wrapping
  (Phase 1 / Step 10)» и обновлённым перечнем registry (15 имён).
- **Ручная проверка 3 сценариев** через временный скрипт в `%TEMP%`
  (`PYTHONPATH` через bootstrap):
  - **A Реальный стенд** (Apache не запущен):
    - `check_runtime_health(stand_env)` → `ok=False`,
      `message="Runtime health issues detected."`,
      `health_codes=['gateway_down']`, `data.environment` содержит
      name/base_id/http_base_url/dump_path, `checks_count=3` с
      корректным раскладом
      `dump_path_exists=ok / http_gateway=error / search_index=ok`.
    - `diagnose_connectivity_issue(stand_env)` → `ok=False`,
      `message="Connectivity issue diagnosis completed."`,
      `problem_code='gateway_down'`,
      `probable_cause='HTTP gateway is not running or not reachable.'`,
      `recommended_action='Start the HTTP gateway and re-run health
      checks.'`
  - **B Локальный success-path** (in-process `socketserver.TCPServer`
    возвращает 200 на любой GET; реальный dump с `.bsl`):
    - `check_runtime_health(local_env)` → `ok=True`,
      `message="Runtime health check completed successfully."`,
      `health_codes=['ok']`, все три check'а `ok`.
    - `diagnose_connectivity_issue(local_env)` → `ok=True`,
      `message="No connectivity issues detected."`,
      `problem_code=None, probable_cause=None,
      recommended_action=None`.
  - **C Registry check**: `len(REGISTERED_TOOLS) == 15`,
    `list_tools()` — требуемый алфавитный список.
  - Ни в одном сценарии исключение наружу не вышло.
- **Dev-check зелёный** после изменений:
  `read_server_tools` содержит все 15 имён; `selfcheck_status = ok`;
  `Dev check completed successfully.` Skeleton selfcheck не трогался.
- **Phase 1 Read MVP закрыт.** Все 10 шагов фазы выполнены,
  критерии приёмки `phase-1-read-mvp-plan.md` достигнуты на
  уровне контракта и success-path. End-to-end против реального
  Apache стенда не покрыт только потому, что стенд сейчас
  выключен — это эксплуатационный вопрос, а не пробел платформы.

### Phase 2 / Step 1 — планирование Write MVP (завершён)

- Phase 1 Read MVP закрыт; Phase 2 — активная фаза разработки.
- Добавлен `docs/architecture/phase-2-write-mvp-plan.md` —
  план Write MVP: назначение фазы, целевой результат, первый
  набор инструментов по четырём группам (A safety/preflight,
  B controlled write, C verification, D audit/rollback support),
  базовые guardrails фазы (запрет prod по умолчанию, обязательный
  `allow_write=True`, обязательные backup/dump до операции,
  обязательный audit, обязательный verify после, запрет silent
  apply), порядок реализации, что не входит в MVP, критерии
  приёмки.
- Добавлен `docs/architecture/phase-2-step-map.md` — стартовый
  implementation map на первые 7 шагов Phase 2: реальный
  `onec-policy-engine` preflight, append-only JSONL audit store в
  `onec-audit`, runtime-слой `mcp-write-server`,
  safety/preflight tools группы A, единый
  `write_flow` helper (preflight → snapshot → operation → verify
  → audit), первые write-tools группы B
  (`apply_config_from_files`, `update_module_code`,
  `create_common_module`), первые verification-tools группы C.
- Зафиксирован первый набор write-tools Phase 2:
  safety — `check_write_preconditions`, `create_backup_snapshot`,
  `create_dump_snapshot`;
  controlled write — `apply_config_from_files`,
  `update_database_configuration`, `create_common_module`,
  `update_module_code`, `add_catalog_attribute`;
  verification — `verify_metadata_change`, `verify_module_contains`,
  `verify_object_exists`;
  audit/rollback — `write_audit_record`,
  `describe_last_write_operation`, `prepare_rollback_hint`.
- Обновлён корневой `README.md`: блок «Текущий статус по фазам»
  переписан под закрытую Phase 1 и активную Phase 2, добавлены
  ссылки на `phase-2-write-mvp-plan.md` и `phase-2-step-map.md`.

### Phase 2 / Step 2 — реальный write preflight / policy слой в onec-policy-engine (завершён)

- `onec-policy-engine` расширен от skeleton до минимального, но
  уже рабочего policy / preflight слоя. Модели:
  - `PolicyDecision` получила два новых поля: `reason_code: str`
    и `require_snapshots: bool` (плюс существующие `allowed`,
    `reason`). Все четыре — обязательные.
  - Добавлена новая dataclass `WriteIntent(operation_name: str,
    target: str | None = None)`.
- Engine:
  - Зафиксированы два множества операций:
    - mutating (`apply_config_from_files`,
      `update_database_configuration`, `create_common_module`,
      `update_module_code`, `add_catalog_attribute`) — требуют
      snapshot'ов;
    - non-mutating write-side support (`check_write_preconditions`,
      `create_backup_snapshot`, `create_dump_snapshot`,
      `verify_metadata_change`, `verify_module_contains`,
      `verify_object_exists`, `write_audit_record`,
      `describe_last_write_operation`, `prepare_rollback_hint`) —
      без snapshot'ов.
  - Консервативная production-эвристика: окружение считается
    production-like, если в нижнем регистре любое из полей
    `name` / `base_id` / `publication_name` / `http_base_url`
    содержит `prod` или `production`. Это временный guardrail до
    появления в `EnvironmentConfig` отдельного
    `environment_type`.
  - Новый основной режим
    `check_write_allowed(environment: EnvironmentConfig,
    intent: WriteIntent) -> PolicyDecision` даёт пять возможных
    `reason_code`: `production_blocked`, `write_not_allowed`,
    `allowed_mutating`, `allowed_non_mutating`, `unknown_intent`.
- **Backward compatibility сохранена.** Существующий
  `scripts/dev/selfcheck.py` (который трогать нельзя на этом шаге)
  продолжает вызывать legacy-форму
  `check_write_allowed("production", True)` и
  `check_write_allowed("local-dev", False)`. В `engine.py`
  реализован тип-диспатч: при `(str, bool)` уходим в
  `_legacy_check`, который возвращает
  `production_blocked` / `write_not_allowed` / `allowed_legacy`
  (legacy-ветка ставит `require_snapshots=True` как безопасный
  default).
- `__init__.py` экспортирует `PolicyDecision`, `WriteIntent`,
  `check_write_allowed` через явный `__all__`.
- README пакета переписан: описано текущее поведение, модели,
  правила, перечень `reason_code`, две формы вызова и отметка о
  временной legacy-совместимости.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%`:
  - **A Legacy `("production", True)`**: `allowed=False`,
    `reason_code='production_blocked'`, `require_snapshots=False`.
  - **B Legacy `("local-dev", False)`**: `allowed=False`,
    `reason_code='write_not_allowed'`, `require_snapshots=False`.
  - **C New mode, local-dev+`allow_write=True`+mutating intent
    (`update_module_code`)**: `allowed=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`.
  - **D New mode, non-mutating support
    (`describe_last_write_operation`)**: `allowed=True`,
    `reason_code='allowed_non_mutating'`, `require_snapshots=False`.
  - **E New mode, unknown intent (`totally_unknown_operation`)**:
    `allowed=False`, `reason_code='unknown_intent'`, `reason`
    содержит имя операции.
  - Assertion `isinstance(r, PolicyDecision)` на всех пяти
    результатах — OK.
- **Dev-check после изменений зелёный**:
  `production_write_allowed = false`, `local_dev_write_allowed =
  false` (совпадает с требуемыми значениями selfcheck'а благодаря
  legacy-диспатчу), `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался; чужие пакеты
  (`onec-config`, `onec-audit`, `onec-health` и др.) тоже не
  трогались.

### Phase 2 / Step 3 — append-only JSONL audit store в onec-audit (завершён)

- `onec-audit` расширен от форматтера до минимального append-only
  JSONL store. Публичный контракт `AuditRecord` не менялся;
  `format_audit_record(...)` оставлен как канонический форматтер
  (одна запись → одна JSON-строка через `json.dumps`,
  `ensure_ascii=False`).
- В `writer.py` добавлены две функции:
  - `append_record(audit_dir, record) -> str` — создаёт
    `audit_dir` (если нет) через `mkdir(parents=True,
    exist_ok=True)`, открывает `<audit_dir>/audit.jsonl` в режиме
    append/UTF-8, пишет `format_audit_record(record) + "\n"` и
    возвращает строковый путь файла аудита. Ошибки файловой
    системы поднимаются как `OSError` и не проглатываются.
    Append-only, файл никогда не перезаписывается.
  - `read_last_record(audit_dir) -> AuditRecord | None` — читает
    `<audit_dir>/audit.jsonl` в UTF-8, игнорирует пустые строки,
    берёт последнюю непустую, парсит JSON, возвращает
    `AuditRecord(**payload)`. Если файла нет или в нём нет
    непустых строк — `None`. На битой JSON-строке или
    рассогласовании с формой `AuditRecord` — `ValueError` с
    понятным сообщением; `OSError` пробрасывается как есть.
- Имя файла хранилища зафиксировано константой
  `_AUDIT_FILE_NAME = "audit.jsonl"`. Формат — JSONL (одна запись
  = одна строка), UTF-8, переводы `\n`.
- `__init__.py` экспортирует `AuditRecord`, `format_audit_record`,
  `append_record`, `read_last_record` через явный `__all__`.
- README пакета переписан: выход из чистого форматтера,
  описание append-only store, контракт ошибок, явная отметка что
  rotate/search/history не входят в MVP.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%`, с использованием `tempfile.TemporaryDirectory(...)`
  для каждого случая:
  - **A `format_audit_record`**: вернулась однострочная JSON-строка
    c ожидаемыми ключами (`operation_id`, `tool_name`, `status`
    — все `True`), `ensure_ascii=False` сохранил читаемый
    `Local Dev`.
  - **B `append_record` в пустой каталог**: возвращён путь вида
    `<tempdir>\audit.jsonl`, файл создан, в нём ровно **1**
    непустая строка, идентичная canonical JSON.
  - **C append двух записей + `read_last_record`**: записаны
    `op-001 "first"` и `op-002 "second"`; `read_last_record`
    вернул `AuditRecord(operation_id='op-002',
    tool_name='update_module_code', status='error',
    message='second')`; `isinstance(AuditRecord)=True`;
    substring-проверка содержимого подтвердила — это именно
    вторая запись, не первая.
  - **D `read_last_record` на каталоге без `audit.jsonl`**:
    вернулся `None` (`is_none=True`).
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `selfcheck_status = ok`, `Dev check completed successfully.`
  Skeleton selfcheck не трогался; чужие пакеты
  (`onec-policy-engine`, `onec-config`, `onec-health` и др.) тоже
  не трогались.

### Phase 2 / Step 4 — runtime-слой mcp-write-server (завершён)

- Внутри `apps/mcp-write-server/src/mcp_write_server/` создан
  подпакет `runtime/` — внутренний слой ниже tool-уровня. Пока он
  не используется ни одним зарегистрированным инструментом
  write-server'а: `tools.py`, `server.py`, верхний `__init__.py`
  и `models.py` не тронуты; registry остаётся `['ping']`.
- **`runtime/models.py`** — dataclass `WriteRuntimeContext` со
  всеми перечисленными в ТЗ полями: `environment`,
  `intent: WriteIntent`, `health_results`, `health_codes`,
  `policy_decision`, `audit_dir: str`. Импорты согласованы с
  `onec_config`, `onec_health`, `onec_policy_engine`.
- **`runtime/context.py`** —
  `build_runtime_context(environment, intent)`:
  `check_environment_health(...)` → `summarize_health(...)` →
  `check_write_allowed(environment, intent)` (новый режим из
  Step 2, с `WriteIntent`) → `audit_dir` как
  `str(Path(environment.dump_path) / ".audit")` (временное
  правило до появления отдельного поля в `onec-config`).
  Без side-effects, ничего на диск не пишется.
- **`runtime/guards.py`** —
  `require_write_preconditions(context)`:
  fail-fast guard, сначала проверяет
  `context.policy_decision.allowed` (при deny →
  `PolicyDeniedError` из `mcp-common` с текстом
  `policy_decision.reason`), затем `context.health_codes !=
  ["ok"]` (→ `HealthCheckError` с сообщением
  `"Write preconditions failed due to unhealthy runtime: <codes>"`).
  Ничего не возвращает.
- **`runtime/__init__.py`** экспортирует `WriteRuntimeContext`,
  `build_runtime_context`, `require_write_preconditions` через
  явный `__all__`.
- README `mcp-write-server` дополнен разделом «Runtime слой
  (Phase 2 / Step 4)» с кратким описанием трёх символов,
  выводимого правила `audit_dir` и порядка проверок в guard'е.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%` под bootstrap'нутым `PYTHONPATH`:
  - **A Allowed policy + unhealthy runtime** (URL указывает на
    пустой localhost:59999, dump реальный, `allow_write=True`,
    mutating intent): `WriteRuntimeContext` создан,
    `policy.allowed=True`, `reason_code='allowed_mutating'`,
    `health_codes=['gateway_down']`, `audit_dir` заканчивается на
    `\.audit` и равен
    `C:\Tools\mcp-1c\config-dump\InfoBase5-with-code-20260423-004101\.audit`.
    `require_write_preconditions` корректно поднял
    `HealthCheckError: Write preconditions failed due to unhealthy
    runtime: ['gateway_down']`.
  - **B Denied by policy** (тот же URL, но `allow_write=False`):
    `policy.allowed=False`, `reason_code='write_not_allowed'`,
    `require_write_preconditions` поднял `PolicyDeniedError:
    Write operations require allow_write=True.` — policy-guard
    отработал **до** health-проверки (как и требует порядок).
  - **C Production-like deny** (name=`Prod Local`,
    publication/base_id/URL содержат `prod`): `policy.allowed=
    False`, `reason_code='production_blocked'`,
    `PolicyDeniedError: Write operations are forbidden for
    production-like environments by default.`
  - **D Fully healthy local success-path** (in-process
    `socketserver.TCPServer` на случайном `127.0.0.1:<port>`,
    возвращает 200 на любой GET; реальный dump с `.bsl`):
    `health_codes=['ok']`, `policy.allowed=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`,
    `require_write_preconditions` вернул `None` без исключения.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools = ['ping']` (runtime не подключён к
  registry, как и требовалось), `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не
  трогался; read-server, packages и прочее — тоже.

### Phase 2 / Step 5 — safety/preflight tools группы A (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три первых реальных write-side инструмента поверх
  готового runtime-слоя (`build_runtime_context`,
  `require_write_preconditions`), `onec-policy-engine`
  (`WriteIntent` + new-mode `check_write_allowed`) и
  `onec-process-runner` (`run_process`):
  - `check_write_preconditions(environment, intent)` — тонкая
    tool-обёртка над runtime guard; при успехе — `ok=True`,
    `"Write preconditions satisfied."`; при
    `PolicyDeniedError` / `HealthCheckError` — `ok=False` c
    оригинальным текстом. `payload.runtime` несёт
    `health_codes` и `policy.{allowed, reason_code,
    require_snapshots}`; `payload.data.audit_dir` — из
    `WriteRuntimeContext`.
  - `create_backup_snapshot(environment, label)` — **реальный**
    файловый snapshot инфобазы через
    `shutil.copytree(environment.base_path,
    <base_path.parent>/_snapshots/backup-<base_id>-<safe_label>)`.
    `safe_label` получается санитизацией до набора
    ASCII-букв / цифр / `-_`; пустой результат → `"snapshot"`.
    Перед копированием проходит preflight. Если целевой
    snapshot уже существует — `ok=False` без перезаписи. Ошибки
    `OSError` / `shutil.Error` ловятся и заворачиваются в
    `ToolResult(ok=False, ...)`.
  - `create_dump_snapshot(environment, label)` — **временный
    process-backed stub**. Создаёт каталог
    `<dump_path.parent>/_snapshots/dump-<base_id>-<safe_label>`,
    находит `shutil.which("python")`, через `run_process(...)`
    запускает маленький Python-процесс, который пишет
    `dump-created.txt` в каталоге snapshot; после success'а
    tool сам дописывает `dump-meta.json` с `base_id` / `label` /
    `source_dump_path`. Это не настоящий `1cv8 DumpCfg`: цель
    шага — впервые связать preflight + process runner + snapshot
    path; реальный dump придёт позднее, после `write_flow` и
    проброса пути к бинарю через `onec-config`. Честно
    зафиксировано в README сервера.
  - Добавлены два приватных helper'а: `_safe_snapshot_label(label)`
    и `_runtime_payload(context)`.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 4 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`.
  Алфавитный `list_tools()`:
  `['check_write_preconditions', 'create_backup_snapshot',
  'create_dump_snapshot', 'ping']`.
- README `mcp-write-server` дополнен новым разделом «Safety /
  preflight tools (Phase 2 / Step 5)» с явной пометкой, что
  backup реальный (copytree), а dump snapshot пока временный
  process-backed stub; существующий раздел Runtime слоя сохранён.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer` (200 на любой GET). Фейковый
  `base_path` с одним файлом `hello.txt`, фейковый `dump_path`
  с одним `.bsl` — всё во временном каталоге, реальный стенд
  не затрагивался:
  - **A `check_write_preconditions` success**: `ok=True`,
    `reason_code='allowed_mutating'`, `require_snapshots=True`,
    `health_codes=['ok']`, message `"Write preconditions
    satisfied."`
  - **B `check_write_preconditions` denied** (`allow_write=False`):
    `ok=False`, `reason_code='write_not_allowed'`, message из
    policy reason.
  - **C `create_backup_snapshot` success**: `ok=True`,
    `snapshot_path` создан по правилу
    `<base.parent>/_snapshots/backup-<base_id>-<safe_label>`;
    `hello.txt` скопирован внутрь; label `"step5 test"`
    санитизирован в `step5_test`.
  - **D `create_dump_snapshot` success**: `ok=True`,
    `snapshot_path` создан; `dump-created.txt` записан через
    `run_process` (содержимое `"ok"`); `dump-meta.json` содержит
    `base_id="local-dev"`, `label="step5 test"`,
    `source_dump_path=<fake dump path>`.
  - **E Registry check**: `list_tools() == ['check_write_preconditions',
    'create_backup_snapshot', 'create_dump_snapshot', 'ping']`,
    `len(REGISTERED_TOOLS) == 4`.
  - Во всех случаях tool вернул `ToolResult`, исключения наружу
    не выпадали.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['check_write_preconditions',
  'create_backup_snapshot', 'create_dump_snapshot', 'ping']`,
  `selfcheck_status = ok`, `Dev check completed successfully.`
  Skeleton selfcheck не трогался; чужие пакеты и read-server —
  тоже.

### Phase 2 / Step 6 — единый write_flow helper (завершён)

- Внутри `apps/mcp-write-server/src/mcp_write_server/runtime/`
  создан новый файл `flow.py` — внутренняя «труба»
  preflight → snapshot → operation → verify → audit для будущих
  write-tools группы B. На этом шаге новых public tool'ов нет:
  registry write-server остаётся прежним
  (`check_write_preconditions`, `create_backup_snapshot`,
  `create_dump_snapshot`, `ping`).
- Добавлен dataclass **`WriteFlowArtifacts`** (поля
  `backup_snapshot_path`, `dump_snapshot_path`, `audit_path`,
  `operation_payload`, `verify_payload` — все `... | None`) как
  контракт артефактов одного прогона flow.
- Добавлены type alias'ы `OperationCallable = Callable[[WriteRuntimeContext],
  dict]` и `VerifyCallable = Callable[[WriteRuntimeContext, dict],
  dict]`.
- Основная функция
  **`run_write_flow(environment, intent, *, label,
  operation_callable, verify_callable) -> ToolResult`** выполняет
  строго один путь:
  1. `build_runtime_context(environment, intent)`;
  2. preflight через `require_write_preconditions(...)`;
  3. snapshots — если `context.policy_decision.require_snapshots`,
     вызывает существующие из Step 5 `create_backup_snapshot(...)`
     и затем `create_dump_snapshot(...)`;
  4. `operation_callable(context)`;
  5. `verify_callable(context, operation_payload)`;
  6. `append_record(...)` в `context.audit_dir` с свежим
     `operation_id = str(uuid.uuid4())` и `tool_name="run_write_flow"`;
  7. итоговый `ToolResult(ok=True, ...)` с `stage="completed"` и
     всеми артефактами.
- **Исключения наружу не выпускаются.** Для `operation_callable` и
  `verify_callable` ловится `Exception` (tool boundary); на любой
  стадии при ошибке возвращается `ToolResult(ok=False, ...)` с
  `payload.data.stage ∈ {preflight, backup_snapshot, dump_snapshot,
  operation, verify}` и уже собранными артефактами (snapshot refs,
  `operation_id`, `audit_path`). При ошибке audit помечается
  `status="error"`; если сама запись в audit упала `OSError`,
  `audit_path=None` и tool всё равно возвращает `ToolResult` без
  исключений.
- Lazy import `from ..tools import create_backup_snapshot,
  create_dump_snapshot` внутри `run_write_flow` специально
  разрывает циклический импорт между `tools.py` (импортирует
  `.runtime`) и `.runtime.flow` (использует snapshot tools).
- `runtime/__init__.py` расширен: теперь экспортирует
  `WriteRuntimeContext`, `build_runtime_context`,
  `require_write_preconditions`, `WriteFlowArtifacts`,
  `run_write_flow` через явный `__all__`.
- README `mcp-write-server` дополнен разделом «Write-flow
  pipeline (Phase 2 / Step 6)» с явной пометкой, что это **не
  public tool**, registry не меняется, а dump snapshot внутри
  flow по-прежнему идёт через временный process-backed stub из
  Step 5 до появления реального `1cv8 DumpCfg`.
- **Ручная проверка 4 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` + in-process
  `socketserver.TCPServer` (200 на любой GET). Для каждого
  сценария — собственный tempdir с фейковыми `base_path` и
  `dump_path` (`.bsl` внутри). Реальный стенд не затрагивался:
  - **A Успешный flow (mutating intent)**: `ok=True`,
    `stage='completed'`, `operation_id` присутствует,
    `backup_snapshot_path` и `dump_snapshot_path` заполнены, в
    audit_dir реально лежит `audit.jsonl`, `read_last_record`
    вернул `status='ok'` и тот же `operation_id`;
    `operation_payload={'changed': True, 'target': 'Common...'}`,
    `verify_payload={'verified': True, 'target': 'Common...'}`.
  - **B Preflight deny** (`allow_write=False`): `ok=False`,
    `stage='preflight'`, `reason_code='write_not_allowed'`,
    callback'и вообще не вызывались.
  - **C `operation_callable` падает `RuntimeError("boom")`**:
    `ok=False`, `message='Write operation failed: boom'`,
    `stage='operation'`, есть `operation_id` и `audit_path`;
    последняя запись аудита — `status='error'`,
    `message='Write operation failed: boom'`, `operation_id`
    совпадает.
  - **D `verify_callable` падает `RuntimeError("verify failed")`**:
    `ok=False`, `message='Write verify failed: verify failed'`,
    `stage='verify'`, `operation_payload` присутствует в data
    (успешный первый callback), есть `operation_id` и
    `audit_path`; последняя запись аудита — `status='error'`,
    `message='Write verify failed: verify failed'`,
    `operation_id` совпадает.
  - Во всех четырёх сценариях исключение наружу не вышло.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['check_write_preconditions',
  'create_backup_snapshot', 'create_dump_snapshot', 'ping']`
  (registry не меняли, как и требовалось), `selfcheck_status = ok`,
  `Dev check completed successfully.` Skeleton selfcheck не
  трогался; read-server и пакеты — тоже.

### Phase 2 / Step 7 — первые write-tools группы B (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три первых **public write-tool'а группы B**. Каждый
  — тонкая обёртка над `run_write_flow(...)` из Step 6: собственный
  `WriteIntent`, собственный `label`, собственный
  `operation_callable`, собственный `verify_callable`. Общая труба
  `preflight → snapshot → operation → verify → audit` не
  дублируется, после flow `tool_name` в `ToolResult` заменяется на
  имя public-инструмента через небольшой helper
  `_with_tool_name(...)`.
- Добавлен внутренний helper-файл
  `apps/mcp-write-server/src/mcp_write_server/runtime/dump_ops.py`
  с единственной функцией `run_stub_apply_process(source_dump_path)`:
  проверяет каталог, находит `python` в PATH, через
  `onec-process-runner` пишет маркер `apply-stub.txt`, дописывает
  `apply-meta.json`, возвращает dict с `applied`, `mode`,
  `source_dump_path`, `marker_path`. Ошибки валидации/процесса
  поднимаются как `FileNotFoundError` / `RuntimeError` и ловятся
  уже в `run_write_flow` как operation-stage failure — исключения
  наружу не выходят.
- **`apply_config_from_files(environment, source_dump_path,
  label="apply-config")`** — первый реальный public-инструмент
  apply. На этом шаге apply-путь **честный stub-backed process
  apply**, а не настоящий `1cv8 LoadConfigFromFiles`: operation
  идёт через `run_stub_apply_process(...)`, verify проверяет, что
  маркер создан (`marker_exists=True`). Честно зафиксировано в
  README и в docstring.
- **`update_module_code(environment, module_relative_path, new_text,
  label="update-module-code")`** — **реальное** перезаписывание
  файла модуля в `environment.dump_path`. Операция:
  `target = Path(dump_path) / module_relative_path`, проверка
  `target.is_file()`, `target.write_text(new_text, encoding="utf-8")`.
  Verify перечитывает файл и сверяет побайтно с `new_text`. Пустой
  или whitespace-only `new_text` отвергается **до запуска flow**,
  tool возвращает `ToolResult(ok=False, ...)` без snapshots/audit.
- **`create_common_module(environment, module_name,
  initial_text="", label="create-common-module")`** — **реальное**
  создание `CommonModules/<module_name>/Ext/Module.bsl` в dump-
  дереве. Валидация имени — `re.fullmatch(r"\w+", module_name)`
  (латиница/кириллица/цифры/underscore; не пустой; без пробелов);
  при невалидном — `ToolResult(ok=False, ...)` до flow. Если файл
  уже существует — operation raises, flow возвращает
  `ok=False, stage="operation"`. При пустом `initial_text`
  пишется минимальный шаблон `// <module_name>\n`. Verify
  проверяет существование и побайтное совпадение.
- В `apps/mcp-write-server/src/mcp_write_server/server.py` registry
  расширен до 7 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code']`.
- README `mcp-write-server` дополнен разделом «Controlled
  write-tools, группа B (Phase 2 / Step 7)» с явной пометкой, что
  `update_module_code` и `create_common_module` реально меняют
  dump/source tree, а `apply_config_from_files` — честный
  stub-backed process apply до появления пути к реальному `1cv8
  LoadConfigFromFiles`. Указано, что public verification-tools
  группы C — в Step 8.
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer`. Реальный стенд не затрагивался; для
  каждого сценария — собственный tempdir с фейковыми `base_path`
  (с файлом `hello.txt`) и `dump_path` (с `.bsl`-anchor'ом):
  - **A `update_module_code` success**: `ok=True`,
    `tool='update_module_code'`, `stage='completed'`, verify
    вернул `{verified: True, target, text_length: 66}`; файл на
    диске **реально содержит** `new_text` (побайтное сравнение
    True); `audit_path` существует.
  - **B `create_common_module("MCPTestCode2")` success**:
    `ok=True`, `tool='create_common_module'`, `stage='completed'`,
    операция вернула путь
    `CommonModules/MCPTestCode2/Ext/Module.bsl`, verify — тот же
    путь; файл создан в dump-дереве, содержимое — минимальный
    шаблон `// MCPTestCode2\n`.
  - **C `apply_config_from_files` success**: `ok=True`,
    `tool='apply_config_from_files'`, `stage='completed'`,
    `operation_payload.mode='stub-process-apply'`; маркер
    `apply-stub.txt` реально создан (содержимое `'applied'`);
    `apply-meta.json` тоже присутствует; verify получил
    `marker_exists=True`.
  - **D `update_module_code` invalid input (`new_text="   "`)**:
    `ok=False`, `message="new_text must be a non-empty,
    non-whitespace string."`, `payload.keys()=['data']` — в
    payload нет ни `runtime`, ни snapshot refs. Отказ сработал
    **до** `run_write_flow`, как и требовалось ТЗ.
  - **E Registry check**: `list_tools()` вернул 7 имён в
    алфавитном порядке, `len(REGISTERED_TOOLS)==7`.
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не выпало.
- **Dev-check после изменений зелёный**:
  `write_server_tools = ['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code']`, `selfcheck_status = ok`, `Dev check
  completed successfully.` Skeleton selfcheck не трогался;
  read-server (15 tools) и пакеты — тоже.

### Phase 2 / Step 8 — первые verification-tools группы C (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы три public verification-tool'а. Они — **не**
  обёртки над `run_write_flow`: ничего не меняют, не снимают
  snapshot'ов, не пишут audit. Cross-app import разрешён только
  `write → read`: из `mcp_read_server.runtime` используются
  `fetch_json_from_environment`, `read_dump_file`,
  `resolve_dump_path`, `find_files_by_pattern`, `read_text_file`.
  Read-server не менялся; его контракт read-only сохранён.
- **`verify_module_contains(environment, module_relative_path,
  expected_substring)`** — dump-level verify. Через
  `read_dump_file(...)` читает файл модуля и проверяет наличие
  substring'а. Пустой/whitespace-only `expected_substring`
  отвергается до чтения. `PlatformError` от dump adapter
  заворачивается в `ToolResult(ok=False, ...)`. В payload —
  `module_relative_path`, `expected_substring`, `contains`.
- **`verify_object_exists(environment, object_name)`** —
  cross-check live + dump. Live-часть: GET на
  `<http_base_url>/metadata/object?name=<url-encoded object_name>`
  через `fetch_json_from_environment(...)`; `PlatformError`
  превращается в `live_exists=False` + `live_error=<текст>`.
  Dump-часть: `find_files_by_pattern(resolve_dump_path(env),
  "*.xml")` → substring-поиск `object_name` в текстах XML
  (`read_text_file`). `dump_exists = dump_match_count > 0`.
  `ok=True` только когда `live_exists AND dump_exists`. В payload —
  `object_name`, `live_exists`, `dump_exists`, `dump_match_count`,
  опционально `live_error` / `dump_error`.
- **`verify_metadata_change(environment, expectation)`** — фасад
  над минимальным expectation contract. Диспетчер по
  `expectation["kind"]`:
  - `"object_exists"` → делегирует в `verify_object_exists(env,
    expectation["object_name"])`;
  - `"module_contains"` → делегирует в `verify_module_contains(env,
    expectation["module_relative_path"],
    expectation["expected_substring"])`;
  - любой другой `kind` → `ok=False`, `"Unknown metadata
    verification kind: ..."`.
  Итоговый `ToolResult` переписывается так, что `tool_name` всегда
  `"verify_metadata_change"`, а в `payload.data` добавляется
  `verification_kind` (имя выбранной ветки). Отсутствие
  обязательных полей expectation тоже даёт понятный
  `ToolResult(ok=False, ...)` без исключения.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 10 инструментов через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['apply_config_from_files',
  'check_write_preconditions', 'create_backup_snapshot',
  'create_common_module', 'create_dump_snapshot', 'ping',
  'update_module_code', 'verify_metadata_change',
  'verify_module_contains', 'verify_object_exists']`.
- README `mcp-write-server` дополнен разделом «Verification-tools,
  группа C (Phase 2 / Step 8)» с явной отметкой, что cross-app
  import идёт только write→read, перечисленными импортами из
  `mcp_read_server.runtime`, описанием двух форм verification
  (встроенные callback'и в `run_write_flow` из Step 7 + public
  tools из Step 8).
- **Ручная проверка 5 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer`, который маршрутизирует
  `/metadata/object` в валидный JSON. Реальный стенд не
  затрагивался:
  - **A `verify_module_contains` success**: файл содержит
    `MCP_SMOKE_TEST`; `ok=True`, `contains=True`, сообщение
    «Module verification succeeded.»
  - **B `verify_module_contains` failure**: ищется substring,
    которого в файле нет; `ok=False`, `contains=False`, сообщение
    «Expected substring was not found in module.»
  - **C `verify_object_exists` success**: локальный HTTP отдаёт
    JSON, в dump положен XML с `Справочник.Фильмы`;
    `ok=True`, `live_exists=True`, `dump_exists=True`,
    `dump_match_count=1`.
  - **D `verify_object_exists` partial failure**: URL указывает
    на `127.0.0.1:59999/dead` (порт не слушается), dump XML
    содержит объект; `ok=False`, `live_exists=False`,
    `dump_exists=True`, `dump_match_count=1`, в payload есть
    `live_error` с «Failed to fetch …/metadata/object?name=%D0%A1%D0%BF%D1%80…».
  - **E dispatcher**:
    - E1 `kind='object_exists'`: `tool_name='verify_metadata_change'`,
      `verification_kind='object_exists'`, `ok=True`,
      `object_name='Справочник.Фильмы'` пронесено.
    - E2 `kind='module_contains'`: `tool_name='verify_metadata_change'`,
      `verification_kind='module_contains'`, `ok=True`,
      `contains=True`.
  - Во всех случаях исключение наружу не выходит.
- **Dev-check после изменений зелёный**:
  `write_server_tools` содержит 10 имён,
  `read_server_tools` = 15 (не деградировал), `selfcheck_status
  = ok`, `Dev check completed successfully.`

### Phase 2 / Step 9 — оставшиеся B-tools и audit/rollback helpers (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  реализованы **5 новых public tools**. Registry расширен до 15.
- **Группа B (через `run_write_flow`):**
  - `update_database_configuration(environment,
    label="update-database-configuration")` — запуск «обновления
    БД» через полную трубу flow. **Честный stub-backed update-db
    process** до настоящего `1cv8 UpdateDBCfg`: operation через
    `onec-process-runner` пишет маркер
    `<dump_path>/.update-db-stub.txt`, tool дополняет
    `<dump_path>/.update-db-meta.json`. Verify проверяет наличие
    обоих файлов.
  - `add_catalog_attribute(environment, catalog_name,
    attribute_spec, label="add-catalog-attribute")` — **реальный**
    pragmatic text-patch XML-карточки справочника в dump-дереве.
    Pre-flow валидация: `catalog_name` непустой, `attribute_spec`
    — dict, `attribute_spec.name` без edge-whitespace,
    `attribute_spec.type` из whitelist'а
    `{"String", "Number", "Date"}`. Operation читает
    `Catalogs/<catalog_name>.xml`, отказывает, если имя уже
    встречается в тексте, вставляет фрагмент
    `<Attribute name="..."><Type>...</Type>[<Synonym>...</Synonym>]</Attribute>`
    перед последним закрывающим тегом (`rfind("</")`) и пишет
    обратно в UTF-8. Synonym — опциональный. Verify перечитывает
    и проверяет наличие имени и типа. **Это MVP-уровень, не full
    1C XML DOM editor** — честно зафиксировано в README/docstring.
- **Группа D (самостоятельные, не через `run_write_flow`, не
  меняют состояние):**
  - `write_audit_record(environment, record)` — явная запись
    аудита. Требует dict с ненулевыми строковыми
    `operation_id`/`tool_name`/`status`/`message`; `environment`
    и `base_id` `AuditRecord`'а заполняются из `environment`.
    `audit_dir = <dump_path>/.audit`, запись — `append_record(...)`
    из `onec-audit`. `OSError` оборачивается в
    `ToolResult(ok=False, ...)`.
  - `describe_last_write_operation(environment)` — reader поверх
    `read_last_record(...)`. При отсутствии записей — `ok=False,
    "No audit records found."`; при успехе — `ok=True` с полным
    паспортом.
  - `prepare_rollback_hint(environment, operation_id)` —
    human-readable подсказка по ручному откату. **Не выполняет
    rollback.** Читает `<dump_path>/.audit/audit.jsonl`, идёт по
    строкам с конца, ищет запись с заданным `operation_id`. На
    отсутствии файла/записи — `ok=False` с понятным сообщением;
    при успехе — `ok=True` с `audit_status`,
    `suggested_backup_root`, `suggested_dump_root` и `hint_text`
    с подсказкой по ручному откату.
- В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry поднят до 15 через уже существующий
  `build_tool_registry(...)` из `mcp-common`. Алфавитный
  `list_tools()`: `['add_catalog_attribute',
  'apply_config_from_files', 'check_write_preconditions',
  'create_backup_snapshot', 'create_common_module',
  'create_dump_snapshot', 'describe_last_write_operation', 'ping',
  'prepare_rollback_hint', 'update_database_configuration',
  'update_module_code', 'verify_metadata_change',
  'verify_module_contains', 'verify_object_exists',
  'write_audit_record']`.
- README `mcp-write-server` дополнен разделом «Оставшиеся group B
  + audit/rollback helpers (Phase 2 / Step 9)» с явными
  пометками про stub-backed `update_database_configuration`,
  pragmatic XML patch `add_catalog_attribute` и не-выполняющий
  rollback `prepare_rollback_hint`. Все предыдущие разделы
  сохранены.
- **Ручная проверка 6 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process
  `socketserver.TCPServer` (200 на любой GET). Реальный стенд не
  затрагивался:
  - **A `update_database_configuration` success**: `ok=True`,
    `stage='completed'`, `verify_payload.verified=True`;
    `.update-db-stub.txt` и `.update-db-meta.json` реально
    существуют в dump-корне.
  - **B `add_catalog_attribute` success**: `ok=True`,
    `stage='completed'`, после operation XML-файл содержит имя
    атрибута `Жанр`, тип `String` и synonym `Жанр фильма`;
    хвост XML: `<Name>Фильмы</Name><Attribute
    name="Жанр"><Type>String</Type><Synonym>Жанр фильма</Synonym></Attribute></MetaData>`.
    Verify прошёл.
  - **C `write_audit_record` success**: `ok=True`, `audit.jsonl`
    создан; JSON-строка реально содержит
    `operation_id="op-fixed-cde"`, `tool_name="synthetic_operation"`,
    `environment="Local Dev"`, `base_id="local-dev"`, `status="ok"`.
  - **D `describe_last_write_operation` после C**: `ok=True`,
    возвращает именно ту же запись (`operation_id=op-fixed-cde`,
    `status=ok`, `tool_name=synthetic_operation`, матчится с
    данными C).
  - **E `prepare_rollback_hint("op-fixed-cde")` после C**:
    `ok=True`, `audit_status=ok`, `suggested_backup_root` и
    `suggested_dump_root` заполнены (указывают на
    `<workdir>/_snapshots`), `hint_text` длиной 127 символов и
    начинается с «Locate the backup/dump snapshot created around
    this operation».
  - **F Registry check**: `list_tools()` возвращает 15 имён в
    алфавитном порядке; `len(REGISTERED_TOOLS) == 15`.
- **Dev-check после изменений зелёный**:
  `write_server_tools` = 15 имён, `read_server_tools` = 15 (не
  деградировал), `selfcheck_status = ok`, `Dev check completed
  successfully.` Skeleton selfcheck не трогался.

### Phase 2 / Step 10 — final integration pass (завершён, Phase 2 Write MVP закрыт окончательно)

- **Аудит консистентности выполнен.** Проверены все 15
  инструментов write-server'а:
  - все 5 mutating tools группы B (`apply_config_from_files`,
    `update_module_code`, `create_common_module`,
    `update_database_configuration`, `add_catalog_attribute`)
    идут строго через `run_write_flow(...)` — preflight,
    backup+dump snapshots, operation, verify, audit;
  - все 3 verification tools группы C (`verify_module_contains`,
    `verify_object_exists`, `verify_metadata_change`) —
    самостоятельные, состояние не меняют, не пишут audit;
  - все 3 audit/rollback helpers группы D (`write_audit_record`,
    `describe_last_write_operation`, `prepare_rollback_hint`) —
    не меняют state базы/dump; `prepare_rollback_hint` только
    готовит подсказку, rollback не выполняет;
  - все public tools возвращают `ToolResult` с `tool_name` = имя
    public-инструмента (rewrap через `_with_tool_name`);
  - исключения наружу не выпадают ни на одной границе tool.
- **Одна точечная правка сделана.** В
  `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
  функция `_append_audit` теперь записывает
  `tool_name = context.intent.operation_name` вместо жёстко
  прошитого `"run_write_flow"`. Это делает записи аудита
  трассируемыми до точного public-инструмента
  (`update_module_code`, `add_catalog_attribute` и т.д.) и
  согласует поле `tool_name` в `AuditRecord` с одноимённым полем
  в `ToolResult`. Ранее prior ручные проверки на Step 6 не
  завязывались на `tool_name="run_write_flow"` в audit — изменение
  не создаёт регрессий.
- **Интеграционный прогон** через временный скрипт в `%TEMP%`
  с `tempfile.TemporaryDirectory` и in-process HTTP 200 сервером.
  Реальный стенд не затрагивался.
  - **Registry integrity**: `list_tools()` вернул ровно 15
    ожидаемых имён;
    `len(REGISTERED_TOOLS) == 15 and set(...) == EXPECTED = True`.
  - **Scenario A — full write path via `update_module_code`.**
    1. `update_module_code(env, rel_path, new_text)` →
       `ok=True, tool='update_module_code', stage='completed'`,
       присутствуют `backup_snapshot_path`, `dump_snapshot_path`,
       `audit_path`; файл на диске действительно перезаписан
       (`file_on_disk_matches_new_text=True`).
    2. `verify_module_contains(env, rel_path, "MCP_Test")` →
       `ok=True, contains=True` (внешний verify вне flow).
    3. `describe_last_write_operation(env)` →
       `audit.tool_name='update_module_code'` (новое!),
       `audit.status='ok'`, `operation_id` совпадает с
       `data.operation_id` из шага 1.
    4. `prepare_rollback_hint(env, operation_id)` →
       `ok=True`, `audit_status='ok'`, оба
       `suggested_backup_root`/`suggested_dump_root` заполнены,
       `hint_text` непустой.
  - **Scenario B — metadata path via `add_catalog_attribute`.**
    `add_catalog_attribute(env, "Фильмы", {...})` →
    `ok=True, tool='add_catalog_attribute', stage='completed'`,
    audit присутствует. `verify_metadata_change(env,
    {"kind":"module_contains", ..., "expected_substring":"Жанр"})`
    → `ok=True`, `verification_kind='module_contains'`,
    `contains=True` — атрибут реально попал в XML.
    `describe_last_write_operation` → `audit.tool_name
    ='add_catalog_attribute'`, статус `ok`.
  - **Scenario C — failure path: `update_module_code` на
    несуществующий путь.** `ok=False,
    tool='update_module_code'`, `stage='operation'`, присутствуют
    `operation_id` и `audit_path`; message начинается с
    `"Write operation failed: Module not found in dump: ..."`.
    `describe_last_write_operation` →
    `audit.tool_name='update_module_code'`, **`audit.status
    ='error'`**, message совпадает. Исключение наружу не
    вышло — контракт fail-closed подтверждён.
- **README `mcp-write-server`** дополнен новым разделом
  «Write MVP закрыт (Phase 2 / Step 10 — final integration pass)»:
  explicit свод по группам A/B/C/D, перечень гарантий контура,
  честный список временных stub'ов (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`,
  `prepare_rollback_hint`, `add_catalog_attribute`) и пометка,
  что настоящий `1cv8`-integration — отдельный follow-up, не
  блокирующий MVP.
- **Root `README.md`** обновлён: блок «Текущий статус по фазам»
  помечает Phase 2 как завершённую (15 tools, краткий расклад
  по группам + честная пометка про stub'ы), добавлена строка
  «Phase 3 — следующий этап», материалы Phase 2 перенесены в
  список закрытых фаз.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `read_server_tools` = 15, `write_server_tools` = 15,
  `selfcheck_status = ok`, `Dev check completed successfully.`
- **Phase 2 / Write MVP закрыт.** Все 10 шагов фазы выполнены;
  контур preflight → snapshots → operation → verify → audit
  действительно работает как единая система, что подтверждено
  интеграционным прогоном; read-server остался read-only; все
  временные stub'ы явно задокументированы как временные. Критерии
  приёмки `phase-2-write-mvp-plan.md` достигнуты на уровне
  контракта и success-path. End-to-end против реального Apache
  стенда + настоящий `1cv8`-binary — эксплуатационные вопросы,
  не пробел платформы.

### Phase 3 / Step 1 — planning Metadata Changes (завершён)

- Phase 2 / Write MVP закрыт; Phase 3 — активная фаза разработки.
- Добавлен `docs/architecture/phase-3-metadata-changes-plan.md` —
  план Phase 3: назначение фазы (переход от точечных write-операций
  к полноценным metadata-операциям — объекты / реквизиты / формы /
  модули / связи), целевой результат (metadata-oriented изменения
  через тот же `run_write_flow`, internal metadata patch layer,
  обязательные verify + audit, структура ближе к реальному 1C
  dev workflow), стартовый набор инструментов по четырём группам:
  - **A — object-level**: `create_catalog`, `create_document`,
    `create_information_register`, `create_common_module_from_template`,
    `create_role`;
  - **B — attribute/schema**: обновлённый `add_catalog_attribute`,
    `add_document_attribute`, `add_tabular_section`,
    `add_form_attribute`, `change_attribute_type` (с явным intent);
  - **C — form/module structure**: `create_managed_form`,
    `add_form_element`, `bind_form_handler`,
    `append_module_method`, `replace_module_method_body` (с
    подтверждением);
  - **D — verification / structural diagnostics**:
    `verify_attribute_exists`, `verify_form_exists`,
    `verify_module_method_exists`, `verify_metadata_shape`,
    `diff_dump_fragment`.
  Зафиксированы guardrails Phase 3 (жёстче, чем Write MVP):
  production-like blocked, любое metadata change строго через
  полный flow, идемпотентность-или-fail-closed, запрет silent
  mutation, переход от наивного text-patch к structural patch
  там, где возможно, явный intent для необратимых операций,
  verify+audit обязательны в том же flow. Описано, что не входит
  в фазу (autonomous refactoring, production automation,
  self-healing, multi-base, GUI, product workflows, замена stub'ов
  Phase 2 на реальный `1cv8`-binary). Определены критерии приёмки
  (не менее 4–5 mutating metadata tools, 2–3 verification tools,
  audit корректен, end-to-end metadata сценарий подтверждён,
  dev-check зелёный).
- Добавлен `docs/architecture/phase-3-step-map.md` — стартовый
  implementation map на первые 7 шагов Phase 3:
  1. Metadata operation contract / intent model
     (документация + фиксация intent names);
  2. Усиление `onec-policy-engine` (+ опционально `onec-config`)
     под новый список metadata operation names;
  3. Internal metadata patch helper layer в
     `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`
     (без public tools);
  4. Первая волна metadata tools на object/attribute level
     (`create_catalog`, `add_document_attribute`, обновлённый
     `add_catalog_attribute`);
  5. Verification-tools для metadata shape
     (`verify_attribute_exists`, `verify_metadata_shape`,
     `diff_dump_fragment`);
  6. Form/module level tools
     (`create_managed_form`, `add_form_element`,
     `append_module_method`, `replace_module_method_body` с
     подтверждением);
  7. Final integration pass Phase 3.
- Обновлён корневой `README.md`: блок «Текущий статус по фазам»
  помечает Phase 3 как активную фазу, добавлены ссылки на
  `phase-3-metadata-changes-plan.md` и `phase-3-step-map.md`.
- Никаких правок кода на этом шаге не делалось: `apps/`,
  `packages/`, `scripts/`, `.github/`, `pyproject.toml` не
  тронуты. Registry read-server = 15, registry write-server = 15.

### Phase 3 / Step 2 — metadata operation contract в `onec-policy-engine` (завершён)

- **Policy contract расширен до четырёх категорий operation_name.**
  В `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
  добавлены два новых frozenset'а (поверх уже существующих, без
  пересечений):
  - `_METADATA_MUTATING_OPERATIONS` = `create_catalog`,
    `create_document`, `create_information_register`,
    `create_common_module_from_template`, `create_role`,
    `add_document_attribute`, `add_tabular_section`,
    `add_form_attribute`, `change_attribute_type`,
    `create_managed_form`, `add_form_element`, `bind_form_handler`,
    `append_module_method`, `replace_module_method_body`.
  - `_METADATA_SUPPORT_OPERATIONS` = `verify_attribute_exists`,
    `verify_form_exists`, `verify_module_method_exists`,
    `verify_metadata_shape`, `diff_dump_fragment`.
- **Существующие Phase 2 наборы не тронуты.** `_MUTATING_OPERATIONS`
  и `_NON_MUTATING_SUPPORT_OPERATIONS` остались точно в прежнем
  составе; новые metadata-ops добавлены поверх, а не вместо.
  `add_catalog_attribute` и остальные Phase 2 имена остались в
  своих категориях с теми же `reason_code`.
- **`_new_check` расширен двумя ветками** (в порядке: Phase 2
  mutating → Phase 2 support → Phase 3 metadata mutating →
  Phase 3 metadata support → unknown). Новые `reason_code`:
  - `allowed_metadata_mutating` — `require_snapshots=True`, reason
    `"Metadata mutating operation allowed; snapshots are
    required."`;
  - `allowed_metadata_support` — `require_snapshots=False`, reason
    `"Metadata verification/support operation allowed."`.
  Legacy Phase 2 `reason_code` (`allowed_mutating`,
  `allowed_non_mutating`) сохранены ровно в прежнем виде.
- **Backward compatibility сохранена.** `_legacy_check(str, bool)`
  не менялся; `check_write_allowed("production", True)` и
  `check_write_allowed("local-dev", False)` возвращают точно те же
  `PolicyDecision`, что и до шага. `scripts/dev/selfcheck.py` не
  трогался.
- **`models.py` и `__init__.py` не изменялись** — `PolicyDecision`
  уже имеет все нужные поля (`allowed`, `reason`, `reason_code`,
  `require_snapshots`), экспорты корректны.
- **`onec-config` не трогался.** Все заявленные metadata ops
  укладываются в уже существующие поля `EnvironmentConfig`
  (`dump_path`, `base_path`, `publication_name`, `http_base_url`,
  `allow_write`, `timeout_seconds`, `base_id`, `name`). Поле
  `onec_binary_path` — отдельный follow-up для настоящего
  `1cv8`-integration, не нужно для policy contract Phase 3.
- **README `onec-policy-engine` переписан.** Добавлен раздел
  «Категории operation_name» с явным перечислением всех четырёх
  групп; раздел «Коды решений» расширен до шести allow-кодов
  (`allowed_mutating`, `allowed_non_mutating`,
  `allowed_metadata_mutating`, `allowed_metadata_support`,
  `allowed_legacy`) + двух deny-кодов (`production_blocked`,
  `write_not_allowed`) + `unknown_intent`. README `onec-config`
  не трогался.
- **Ручная проверка 6 основных сценариев + 4 дополнительных +
  1 regression** через временный скрипт в `%TEMP%`:
  - **A legacy `("production", True)`**: `allowed=False,
    reason_code='production_blocked', require_snapshots=False`.
  - **B legacy `("local-dev", False)`**: `allowed=False,
    reason_code='write_not_allowed', require_snapshots=False`.
  - **C new-mode `WriteIntent("create_catalog", ...)` на writable
    local-dev**: `allowed=True,
    reason_code='allowed_metadata_mutating',
    require_snapshots=True` — Phase 3 metadata mutating ветка
    сработала, как и требовалось.
  - **D new-mode `WriteIntent("verify_attribute_exists", ...)`**:
    `allowed=True, reason_code='allowed_metadata_support',
    require_snapshots=False`.
  - **E new-mode `WriteIntent("update_module_code", ...)`
    (regression Phase 2)**: `allowed=True,
    reason_code='allowed_mutating', require_snapshots=True` —
    Phase 2 поведение не изменилось.
  - **F new-mode `WriteIntent("totally_unknown_operation")`**:
    `allowed=False, reason_code='unknown_intent',
    require_snapshots=False` — fail-closed.
  - Дополнительно проверены ещё 4 metadata intent'а
    (`create_document`, `append_module_method`,
    `change_attribute_type`, `verify_metadata_shape`,
    `diff_dump_fragment`) — каждый попал в ожидаемую ветку.
  - Regression-контроль: Phase 2 support
    (`describe_last_write_operation`) вернул
    `reason_code='allowed_non_mutating'` — как и прежде.
  - Во всех 11 вызовах результат — `PolicyDecision` (assertion
    через `isinstance` прошла).
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `production_write_allowed = false`, `local_dev_write_allowed =
  false` (точно как в selfcheck'е до шага), `selfcheck_status =
  ok`, `Dev check completed successfully.` Skeleton selfcheck не
  трогался.

### Phase 3 / Step 3 — internal metadata patch helper layer (завершён)

- **Создан новый файл**
  `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`.
  Это **internal** layer: не возвращает `ToolResult`, не ходит в
  HTTP/subprocess/audit/snapshot. Будет использован будущими
  metadata tools Phase 3 / Step 4–6, прямо сейчас **не подключён** к
  `tools.py` / `server.py`. Registry write-server'а не менялся
  (15 инструментов).
- **10 helper'ов в четырёх группах:**
  - **XML / text structural:**
    - `load_xml_text(path)` — UTF-8 `read_text`, `OSError`
      пробрасывается.
    - `insert_before_last_closing_tag(xml_text, fragment)` —
      fallback перед последним `</...>`; `ValueError` если
      closing tag нет.
    - `insert_fragment_into_named_block(xml_text, block_name,
      fragment)` — основной structural helper: поиск парной
      `<block_name>...</block_name>` и вставка перед её
      закрывающим тегом. Требует именно парную структуру
      (self-closing `<block_name/>` не подходит). Отсутствие
      блока → `ValueError` с понятным сообщением.
  - **Fragment builders:**
    - `build_attribute_fragment(name, attr_type, synonym=None)` —
      `<Attribute name="..."><Type>...</Type>[<Synonym>...</Synonym>]</Attribute>`.
    - `build_form_fragment(form_name)` — минимальный `<Form>` stub
      (не полная 1C managed form card).
    - `build_module_method_fragment(method_name, body, export=False)`
      — канонически зафиксированный формат BSL:
      `Процедура <name>() [Экспорт]\n<body>\nКонецПроцедуры\n`.
      Функции / директивы / аннотации — вне контракта Step 3.
  - **BSL helpers:**
    - `module_contains_method(module_text, method_name)` — regex
      `\b(Процедура|Функция|Procedure|Function)\s+<name>\s*\(` с
      `re.IGNORECASE`. Не полноценный парсер, но достаточно для
      smoke-verify.
    - `append_method_to_module(module_text, method_fragment)` —
      предсказуемые разделители строк на стыке.
  - **File patch helpers:**
    - `patch_xml_file(path, patcher)` — read-transform-write в
      UTF-8; `OSError` пробрасывается.
    - `patch_text_file(path, patcher)` — аналог для BSL/plain.
- **`runtime/__init__.py` не трогался.** Подход согласован с
  существующим `dump_ops.py` (Phase 2 / Step 5): helper'ы
  импортируются напрямую из submodule —
  `from .runtime.metadata_ops import ...`, без re-export на
  top-level runtime. Это сохраняет compact public surface.
- **Остальные runtime-файлы (`context.py`, `guards.py`, `flow.py`,
  `models.py`) не трогались.** `tools.py`, `server.py`, верхние
  `models.py` / `__init__.py` write-server'а — тоже не
  трогались. Registry write-server'а = те же 15 имён.
- **Ручная проверка 7 сценариев + 3 дополнительных smoke** через
  временный скрипт в `%TEMP%`:
  - **A `insert_fragment_into_named_block` success** на XML с
    `<Attributes>...</Attributes>`: fragment вставлен именно
    внутрь Attributes перед `</Attributes>` (substring
    `</Attribute></Attributes>` присутствует), `Genre` попал в
    текст.
  - **B `insert_fragment_into_named_block` failure** на XML без
    `<Attributes>`: `ValueError: XML block <Attributes> not
    found (no closing tag).`
  - **C `build_attribute_fragment`**: без synonym — `<Synonym>`
    тега нет; с synonym — есть; имя и тип присутствуют.
  - **D `module_contains_method`**: True для `ПерваяПроцедура`
    (Процедура) и `MCP_Test` (Функция), False для
    несуществующего имени.
  - **E `append_method_to_module`**: результат начинается с
    оригинала, содержит вставленный fragment, новый метод
    детектится через `module_contains_method`, старые методы
    по-прежнему детектятся.
  - **F `patch_xml_file`**: файл на диске реально изменился —
    `name="X"` и `<Type>Number</Type>` присутствуют.
  - **G `patch_text_file`**: BSL-файл на диске действительно
    дополнен; `module_contains_method('Hello')` → True.
  - **Extra smoke**: `load_xml_text` вернул корректную длину;
    `insert_before_last_closing_tag` вставил `<Extra/>` перед
    `</MetaData>`; на входе без `</` — `ValueError: No closing
    tag found in XML text.`; `build_form_fragment` содержит
    переданное имя.
- **README `mcp-write-server`** дополнен новым разделом
  «Internal metadata patch helper layer (Phase 3 / Step 3)» —
  полный перечень helper'ов по 4 группам, выбранный BSL-формат,
  явная отметка «это не public tool layer, registry не меняется».
  Блоки Step 4 / Step 5 / Step 6 / Step 7 / Step 8 / Step 9 /
  Step 10 из Phase 2 сохранены без изменений.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 15 (те же имена, новый helper layer не
  публикуется), `read_server_tools` = 15, `selfcheck_status =
  ok`, `Dev check completed successfully.`

### Phase 3 / Step 4 — первая волна object/attribute metadata tools (завершён)

- **В `apps/mcp-write-server/src/mcp_write_server/tools.py`
  добавлено 2 новых public mutating tool'а и рефакторен
  существующий `add_catalog_attribute`.** Все три tool'а идут
  через `run_write_flow(...)` (preflight → backup+dump snapshots
  → operation → verify → audit); tool_name в итоговом
  `ToolResult` — имя public-инструмента (rewrap через
  `_with_tool_name`). `runtime/metadata_ops.py` из Step 3 не
  менялся — только используется.
- **`create_catalog(environment, catalog_name, spec,
  label="create-catalog")`** — создаёт
  `Catalogs/<catalog_name>.xml` с минимальным stub-карточкой:
  `<MetaData><Name>...</Name>[<Synonym>...</Synonym>]<Attributes></Attributes></MetaData>`.
  Включение пустого `<Attributes></Attributes>` в stub делает
  карточку сразу пригодной для последующего
  `add_catalog_attribute`. Pre-flow валидация: `catalog_name` по
  regex `\w+` (тот же `_MODULE_NAME_RE`, что у
  `create_common_module`), `spec` — dict, `spec.synonym`
  опциональный string. Если файл уже существует —
  `FileExistsError` в operation (flow → `ok=False,
  stage=operation`, audit пишется со `status='error'`).
- **`add_document_attribute(environment, document_name,
  attribute_spec, label="add-document-attribute")`** — добавляет
  атрибут в `Documents/<document_name>.xml`. Целиком поверх
  helper layer Step 3: `build_attribute_fragment(...)` строит
  фрагмент, `insert_fragment_into_named_block(xml_text,
  "Attributes", fragment)` внутри `patch_xml_file(...)` вставляет
  его строго внутрь блока `<Attributes>...</Attributes>`. Если
  такого блока в XML нет — helper поднимает `ValueError`, flow
  отдаёт `ok=False, stage=operation`; **никакого silent fallback
  к последнему `</...>`**. Pre-flow валидация: `document_name`
  непустой, `attribute_spec` — dict, `name` без edge-whitespace,
  `type` из whitelist `{"String", "Number", "Date"}`,
  дубль имени в XML → `FileExistsError`.
- **`add_catalog_attribute(...)` переведён на helper layer Step 3.**
  Внешний public контракт сохранён без изменений: та же сигнатура,
  те же pre-flow валидации, тот же whitelist типов, тот же
  `payload.data` на успехе, те же verify-проверки. Внутри вместо
  старого `rfind("</")` + inline f-string теперь —
  `build_attribute_fragment(...)` + `patch_xml_file(target,
  _patcher)`, где `_patcher` сначала проверяет отсутствие
  дубля имени, затем зовёт `insert_fragment_into_named_block(
  xml_text, "Attributes", fragment)`. Если целевая карточка не
  имеет `<Attributes>` блока — fail-closed (ранее Phase 2 версия
  молча вставляла перед последним `</...>`; сейчас это считается
  ошибкой — соответствует ТЗ Phase 3).
- **В `apps/mcp-write-server/src/mcp_write_server/server.py`
  registry расширен до 17 инструментов** через тот же
  `build_tool_registry(...)` из `mcp-common`. Порядок добавления
  в dict: `ping`, Phase 2 group A (3), group B mutating (3 Step 7
  + 2 Step 9 = 5), group C verify (3), group D audit (3), затем
  2 новых Step 4. Алфавитный `list_tools()`:
  `['add_catalog_attribute', 'add_document_attribute',
  'apply_config_from_files', 'check_write_preconditions',
  'create_backup_snapshot', 'create_catalog',
  'create_common_module', 'create_dump_snapshot',
  'describe_last_write_operation', 'ping', 'prepare_rollback_hint',
  'update_database_configuration', 'update_module_code',
  'verify_metadata_change', 'verify_module_contains',
  'verify_object_exists', 'write_audit_record']`.
- **README `mcp-write-server`** дополнен разделом
  «Object/attribute level metadata tools (Phase 3 / Step 4)»:
  описание всех трёх tool'ов, явная отметка про переход
  `add_catalog_attribute` на helper layer, registry = 17. Блоки
  Step 3 и Phase 2 Step 4–10 сохранены без изменений.
- **Ручная проверка 6 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` + in-process HTTP 200:
  - **A `create_catalog("Контрагенты", {"synonym": ...})`
    success**: `ok=True, stage='completed'`; файл
    `Catalogs/Контрагенты.xml` реально создан со stub-XML
    `<MetaData><Name>Контрагенты</Name><Synonym>Контрагенты
    организации</Synonym><Attributes></Attributes></MetaData>`;
    verify.has_synonym=True; `describe_last_write_operation`
    показывает `audit.tool_name='create_catalog'` и
    `audit.status='ok'` (благодаря правке `_append_audit` из
    Step 10 Phase 2).
  - **B `create_catalog("Dup", {})` над существующим файлом**:
    `ok=False, stage='operation'`, message `"Write operation
    failed: Catalog XML already exists: Catalogs/Dup.xml"`,
    audit записан со `status='error'`, исключение наружу не
    вышло.
  - **C `add_document_attribute("Заказ", {"name":"Сумма",
    "type":"Number", "synonym":"Итоговая сумма"})`**: `ok=True,
    stage='completed'`; XML на диске — `<MetaData><Name>Заказ</Name>
    <Attributes><Attribute name="Сумма"><Type>Number</Type>
    <Synonym>Итоговая сумма</Synonym></Attribute></Attributes>
    </MetaData>`; все три substring-проверки `has_attr_name`,
    `has_type`, `has_synonym` → True.
  - **D `add_document_attribute("НетБлока", {"name":"X",
    "type":"String"})` на XML без `<Attributes>` блока**:
    `ok=False, stage='operation'`, message `"Write operation
    failed: XML block <Attributes> not found (no closing tag)."`,
    **`xml_unchanged=True`** (файл на диске остался идентичным
    исходному — `patch_xml_file` не дошёл до write_text потому что
    patcher поднял ValueError до этого), audit со
    `status='error'`. No silent fallback подтверждён.
  - **E regression `add_catalog_attribute("Фильмы", {...})` на
    карточке с `<Attributes></Attributes>`**: `ok=True,
    stage='completed'`; XML на диске — `<MetaData><Name>Фильмы</Name>
    <Attributes><Attribute name="Жанр"><Type>String</Type>
    <Synonym>Жанр фильма</Synonym></Attribute></Attributes>
    </MetaData>`; substring `</Attribute></Attributes>` присутствует
    → fragment именно внутри Attributes, не перед `</MetaData>`.
    Это ключевое отличие от Phase 2 поведения — новый helper
    layer действительно задействован.
  - **F Registry check**: `len(REGISTERED_TOOLS) == 17`,
    `set(REGISTERED_TOOLS) == EXPECTED_17` (все 15 Phase 2 имён +
    2 новых). ✓
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 17 (два новых имени видны),
  `read_server_tools` = 15 (не деградировал),
  `selfcheck_status = ok`, `Dev check completed successfully.`

### Phase 3 / Step 5 — verification-tools для metadata shape (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py` добавлены
  два новых public read-only tool'а и расширен dispatcher
  `verify_metadata_change`. Все новые/расширенные verification'ы —
  **самостоятельные**, состояние не меняют, snapshot не снимают,
  audit не пишут, **не идут через `run_write_flow`**. Cross-app
  import по-прежнему строго `write → read` (`read_dump_file` из
  `mcp_read_server.runtime`). Новых runtime-файлов не создавалось —
  используется уже существующий helper layer Step 3.
- **Новый tool `verify_attribute_exists(environment, object_name,
  attribute_name)`**: dump-only substring-проверка наличия атрибута
  в XML-карточке resolved-объекта. Приватный helper
  `_resolve_object_xml_path(object_name)` поддерживает MVP-префиксы
  `Справочник.` → `Catalogs/<tail>.xml` и `Документ.` →
  `Documents/<tail>.xml`; другой/пустой префикс → `ok=False` с
  понятным reason. `PlatformError` от dump adapter → `ok=False`
  без утечки исключения. Payload: `object_name`, `attribute_name`,
  `relative_path` (если удалось разрешить), `exists`.
- **Расширение `verify_metadata_change(environment, expectation)`**
  — в dispatcher добавлены три новые ветки по `kind`:
  - `"attribute_exists"` с `object_name`, `attribute_name` —
    делегирует в `verify_attribute_exists(...)`;
  - `"form_exists"` с `object_name`, `form_name` — inline через
    приватный `_verify_form_exists_internal(...)`: MVP dump-level
    substring-поиск имени формы в XML карточки объекта. Отдельного
    public `verify_form_exists` tool'а на этом шаге не создавалось
    — только новая ветка dispatcher'а, как требует ТЗ;
  - `"method_exists"` с `module_relative_path`, `method_name` —
    inline через приватный `_verify_method_exists_internal(...)`:
    читает модуль через `read_dump_file` и проверяет объявление
    метода через уже существующий `module_contains_method` из
    helper layer Step 3.
  Итоговый `tool_name` всегда `"verify_metadata_change"`,
  `payload.data.verification_kind` — имя сработавшей ветки. Старые
  ветки `"object_exists"` / `"module_contains"` сохранены без
  изменений. Неизвестный `kind` по-прежнему fail-closed.
- **Новый tool `diff_dump_fragment(environment, relative_path,
  baseline)`**: unified-diff через `difflib.unified_diff` текста
  dump-файла против переданного baseline. `ok=True`, если файл
  удалось прочитать, независимо от наличия различий — diff это
  информация, не ошибка. `ok=False` только при
  `PlatformError`/отсутствии файла. Diff preview компактный —
  первые `_DIFF_PREVIEW_MAX_LINES=40` строк unified diff с
  маркером `(diff truncated)` при переполнении; при равенстве
  текстов `diff_preview=""`. Payload: `relative_path`, `changed`,
  `current_text_length`, `baseline_length`, `diff_preview`.
- **В `server.py` зарегистрированы два новых tool'а**
  (`verify_attribute_exists`, `diff_dump_fragment`). Registry
  вырос до **19 инструментов**. `verify_metadata_change` уже был
  в registry — получил только новые ветки внутри.
- **README `mcp-write-server`** дополнен разделом «Verification-tools
  для metadata shape (Phase 3 / Step 5)»: описание двух новых
  public tools, трёх новых веток dispatcher'а, явная отметка что
  все verify'и read-only и не идут через flow, registry = 19.
  Блоки Step 3/Step 4 и Phase 2 Step 4–10 сохранены.
- **Ручная проверка 8 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory`. HTTP-сервер в этом
  шаге не нужен — все проверки работают с dump-файлами напрямую.
  Реальный стенд не затрагивался:
  - **A `verify_attribute_exists("Справочник.Фильмы", "Жанр")`
    success**: `ok=True`, `exists=True`,
    `relative_path='Catalogs/Фильмы.xml'`, сообщение «Attribute
    exists in dump XML.»
  - **B `verify_attribute_exists` not found**: та же XML-карточка,
    но без нужного атрибута — `ok=False`, `exists=False`,
    `relative_path` всё ещё корректный.
  - **C `verify_metadata_change(kind="attribute_exists", ...)`**:
    `tool_name='verify_metadata_change'`,
    `verification_kind='attribute_exists'`, `exists=True` —
    dispatcher корректно делегировал в `verify_attribute_exists`.
  - **D form_exists (positive + negative)**: на карточке с
    `<Forms><Form>ФормаСписка</Form></Forms>` positive → `ok=True,
    exists=True`; negative с несуществующим именем формы → `ok=False,
    exists=False`; в обоих случаях `tool_name=verify_metadata_change`,
    `verification_kind=form_exists`.
  - **E method_exists (positive + negative)**: в
    `CommonModules/Test/Ext/Module.bsl` лежит
    `Процедура MCP_Test()`; positive с `method_name='MCP_Test'` →
    `ok=True, exists=True`; negative с несуществующим именем →
    `ok=False, exists=False`; `tool_name=verify_metadata_change`,
    `verification_kind=method_exists`.
  - **F `diff_dump_fragment` changed=False**: baseline идентичен
    файлу — `ok=True, changed=False`, `current_text_length =
    baseline_length = 38`, `diff_preview` пустой.
  - **G `diff_dump_fragment` changed=True**: в файле добавлен
    `<Attribute name="Код"/>` внутри `<Attributes>`; `ok=True,
    changed=True`, lengths 86 vs 63 (наглядно показывают, что
    было добавлено), `diff_preview` содержит корректный unified
    diff с `--- baseline / +++ current / @@ -1 +1 @@` и строками
    `-<MetaData>...<Attributes></Attributes>...</MetaData>` /
    `+<MetaData>...<Attributes><Attribute name="Код"/></Attributes>
    ...</MetaData>`.
  - **H Registry check**: `len(REGISTERED_TOOLS) == 19`,
    `set(REGISTERED_TOOLS) == EXPECTED_19` (все 17 из Step 4 + 2
    новых). ✓
  - Во всех случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 19 (оба новых имени на месте),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 3 / Step 6 — form/module level metadata tools (завершён)

- В `apps/mcp-write-server/src/mcp_write_server/tools.py` добавлены
  **4 новых public mutating tool'а** уровня форм и модулей. Все
  четыре идут через `run_write_flow(...)` — preflight,
  backup+dump snapshots, operation, verify, audit; `tool_name` в
  итоговом `ToolResult` переписывается на имя public-инструмента
  через `_with_tool_name`. Helper layer Step 3 активно
  переиспользуется.
- **`create_managed_form(environment, object_name, form_name,
  label="create-managed-form")`** — вставка `build_form_fragment`
  внутрь блока `<Forms>` resolved-XML объекта через
  `insert_fragment_into_named_block`. Pre-flow валидация
  `object_name` (ненулевая строка + поддерживаемый префикс
  `Справочник.`/`Документ.` через уже существующий
  `_resolve_object_xml_path`) и `form_name` (`\w+`). Fail-closed,
  если `<Forms>` нет в XML или форма уже существует.
- **`add_form_element(environment, object_name, form_name,
  element_spec, label="add-form-element")`** — pragmatic
  structural patch: приватные helper'ы `_find_form_block_bounds`
  и `_build_form_element_fragment` локализуют нужный
  `<Form name="form_name">...</Form>` блок и вставляют элемент
  **именно в его `<Elements>...</Elements>`**, а не в конец XML.
  Fail-closed, если формы нет, у неё нет парного `<Elements>`
  блока, или в ней уже есть элемент с таким именем (коллизия
  проверяется substring'ом `<Element name="element_name">` в
  границах формы). `element_spec`: `name`, `type`, опционально
  `title`.
- **`append_module_method(environment, module_relative_path,
  method_spec, label="append-module-method")`** — добавление
  нового BSL метода в модуль через helper layer Step 3:
  `build_module_method_fragment` → `append_method_to_module` →
  `patch_text_file`. Коллизия — через `module_contains_method`.
  `method_spec`: `name` (`\w+`), `body` (non-empty non-whitespace),
  `export: bool` по умолчанию `False`. Fail-closed при
  отсутствующем модуле или дубликате.
- **`replace_module_method_body(environment,
  module_relative_path, method_name, new_body, *,
  confirm_replace=False, label=...)`** — **намеренно опасная**
  операция. Требует явного `confirm_replace=True`, иначе
  отвергается до flow с понятным сообщением (без snapshots /
  audit). Локализация метода — через осторожный regex
  `_BSL_SIGNATURE_RE_TEMPLATE` +
  `_BSL_END_PROCEDURE_RE` / `_BSL_END_FUNCTION_RE` (совпадают с
  родом keyword'а сигнатуры). Тело заменяется **только между
  найденной сигнатурой и соответствующим end-keyword'ом**,
  никакого глобального replace по имени. Fail-closed, если
  модуля нет, метод не найден, или структура не распознаётся
  однозначно.
- **`runtime/metadata_ops.py`** получил точечное обратно-совместимое
  изменение: `build_form_fragment(form_name)` теперь включает пустой
  `<Elements></Elements>` блок внутри `<Form>`, чтобы будущие
  вызовы `add_form_element` имели детерминированную точку
  вставки. Это единственная правка helper layer Step 3; все
  предыдущие smoke-проверки Step 3 (substring `form_name in
  fragment`) по-прежнему проходят.
- В `server.py` зарегистрированы все 4 новых tool'а. Registry
  write-server'а вырос до **23 инструментов**:
  - group A (safety/preflight) = 3;
  - group B mutating = 5 Phase 2 + 2 Phase 3 Step 4 + 4 Phase 3
    Step 6 = 11;
  - group C verification = 3 Phase 2 + 1 Phase 3 Step 5 + 1
    Phase 3 Step 5 diff = 5;
  - group D audit/rollback = 3;
  - plus `ping`.
- README `mcp-write-server` дополнен разделом «Form/module level
  metadata tools (Phase 3 / Step 6)»: перечень всех 4 tool'ов,
  явная пометка про `confirm_replace` для
  `replace_module_method_body`, явное упоминание точечного
  tweak'а `build_form_fragment`, registry = 23. Блоки Step 3–5
  и Phase 2 Step 4–10 сохранены.
- **Ручная проверка 8 сценариев** через временный скрипт в
  `%TEMP%` с `tempfile.TemporaryDirectory` и in-process HTTP 200.
  Реальный стенд не затрагивался.
  - **A `create_managed_form` success**: XML с `<Forms></Forms>`;
    после вызова — `<Form name="ФормаСписка">...<Elements></Elements></Form>`
    внутри Forms; `ok=True`, `stage='completed'`,
    `form_in_xml=True`, `form_inside_Forms=True`; audit.tool_name=
    `create_managed_form`, status=ok.
  - **B `create_managed_form` без Forms**: XML без `<Forms>` →
    `ok=False, stage='operation'`, message «XML block <Forms>
    not found (no closing tag).»; XML **unchanged** (silent
    fallback отсутствует); audit.status=error.
  - **C `append_module_method` success**: модуль с `Первая()`;
    добавлен новый `Вторая() Экспорт` с body `Возврат 2;`;
    в файле видны обе сигнатуры; `ok=True, stage='completed'`;
    audit.tool_name=`append_module_method`, status=ok.
  - **D `append_module_method` duplicate**: модуль содержит `Dup()`
    → вторая попытка `ok=False, stage='operation'`, message
    «Method 'Dup' already declared…»; text unchanged;
    audit.status=error.
  - **E `replace_module_method_body` without confirm**: `ok=False,
    tool='replace_module_method_body'`, message «requires
    explicit confirm_replace=True.»; **в payload только `data`** —
    нет `runtime`, нет snapshot refs → flow не запускался, как и
    требует ТЗ.
  - **F `replace_module_method_body` with confirm**: в модуле две
    методы (`Первая()` procedure и `Вторая()` function); вызов
    replace на `Первая` с new_body `Возврат 42;` →
    `ok=True, stage='completed'`; в тексте `has_new_body=True`,
    `old_body_gone=True` (Возврат 1 исчез), `Вторая_intact=True`
    (второй метод не тронут — сигнатура + старое тело `Возврат 2;`
    сохранились); audit.tool_name=`replace_module_method_body`,
    status=ok.
  - **G `add_form_element` success**: XML с формой, содержащей
    `<Elements></Elements>`; элемент `КнопкаОк` с Title `ОК`
    реально появился **внутри** Elements блока нужной формы;
    `ok=True, stage='completed'`, `has_element=True`,
    `has_title=True`, `inside_Elements=True`.
  - **H Registry check**: `len(REGISTERED_TOOLS) == 23`,
    `set(REGISTERED_TOOLS) == EXPECTED_23`. ✓
  - Во всех 8 случаях tool вернул `ToolResult`, исключение наружу
    не вышло.
- **Dev-check после изменений зелёный**: `imports_ok = true`,
  `write_server_tools` = 23 (все 4 новых имени видны),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`

### Phase 3 / Step 7 — final integration pass (завершён, Phase 3 закрыт)

- **Интеграционный прогон подтвердил metadata-контур end-to-end.**
  Один сквозной сценарий из 10 шагов (5 mutating + 3 verification +
  `describe_last_write_operation` + `prepare_rollback_hint`) на
  временном окружении + два failure path сценария. Реальный стенд
  не затрагивался.
- **Единственная кодовая правка Step 7** — минимальный обратно-
  совместимый tweak `create_catalog` stub в
  `apps/mcp-write-server/src/mcp_write_server/tools.py`: добавлен
  пустой `<Forms></Forms>` блок в XML-карточку наряду с уже
  присутствующим `<Attributes></Attributes>`. Без этого свежий
  каталог не принимал `create_managed_form` — композабильность
  create_catalog ↔ create_managed_form была сломана. Правка
  симметрична добавленному в Step 6 `<Elements></Elements>` внутри
  `build_form_fragment`. Assertions Step 4 manual check
  (`<Name>` / `<Synonym>` substring-проверки, `verify_has_synonym`)
  по-прежнему проходят.
- **Никаких других кодовых правок.** `runtime/flow.py`,
  `runtime/metadata_ops.py`, `runtime/context.py`, `runtime/guards.py`,
  `runtime/models.py`, `runtime/dump_ops.py`, другие public tools —
  не трогались. Registry write-server'а остался **23 инструмента**
  ровно, как и требовало ТЗ.
- **Scenario A — full end-to-end metadata path:** 10 шагов, все
  `ok=True`:
  1. `create_catalog("ТестовыйСправочник", {"synonym":
     "Тестовый справочник"})` → `ok=True, stage=completed`,
     `operation_id` + backup+dump snapshot + audit.
  2. `add_catalog_attribute("ТестовыйСправочник",
     {"name":"Жанр","type":"String","synonym":"Жанр"})` →
     `ok=True, stage=completed`, свой `operation_id` + audit.
  3. `create_managed_form("Справочник.ТестовыйСправочник",
     "ФормаСписка")` → `ok=True, stage=completed`.
  4. `add_form_element(..., {"name":"КнопкаОк","type":"Button",
     "title":"ОК"})` → `ok=True, stage=completed`.
  5. `append_module_method("CommonModules\\TestModule\\Ext\\Module.bsl",
     {"name":"MCP_Test","body":"\\tВозврат 1;","export":True})` →
     `ok=True, stage=completed`, собственный `op_id_5`.
  6. `verify_metadata_change(kind="attribute_exists", object_name=
     "Справочник.ТестовыйСправочник", attribute_name="Жанр")` →
     `ok=True, verification_kind=attribute_exists, exists=True`.
  7. `verify_metadata_change(kind="form_exists", ..., form_name=
     "ФормаСписка")` → `ok=True, verification_kind=form_exists,
     exists=True`.
  8. `verify_metadata_change(kind="method_exists",
     module_relative_path=<module>, method_name="MCP_Test")` →
     `ok=True, verification_kind=method_exists, exists=True`.
  9. `describe_last_write_operation` → `ok=True,
     audit.tool_name='append_module_method'` (не generic
     `run_write_flow` — подтверждает правку `_append_audit`
     Phase 2 Step 10), `audit.status='ok'`, `operation_id`
     совпадает с `op_id_5`.
  10. `prepare_rollback_hint(env, op_id_5)` → `ok=True,
      audit_status='ok'`, оба `suggested_backup_root` /
      `suggested_dump_root` заполнены, `hint_text` длиной 127
      символов.
  - **Финальное состояние на диске:**
    `Catalogs/ТестовыйСправочник.xml` содержит полную композицию
    `<MetaData><Name>...</Name><Synonym>...</Synonym>
    <Attributes><Attribute name="Жанр"><Type>String</Type>
    <Synonym>Жанр</Synonym></Attribute></Attributes>
    <Forms><Form name="ФормаСписка"><Type>ManagedApplicationForm</Type>
    <Elements><Element name="КнопкаОк"><Type>Button</Type>
    <Title>ОК</Title></Element></Elements></Form></Forms></MetaData>`
    (все 9 checks True).
    Модуль `CommonModules/TestModule/Ext/Module.bsl`: исходный
    якорь сохранён, метод `Процедура MCP_Test() Экспорт` добавлен.
  - **Snapshot artefacts:** 5 `backup-local-dev-<label>` и 5
    `dump-local-dev-<label>` директорий на каждой стороне (baseside
    `_snapshots` и dumpside `_snapshots`), по одной на каждый
    mutating шаг.
  - **Audit:** ровно 5 строк в `dump/.audit/audit.jsonl` —
    соответствует 5 mutating операциям.
- **Scenario B — fail-closed на отсутствие `<Forms>` блока:**
  каталог с `<MetaData><Name>БезФорм</Name><Attributes></Attributes></MetaData>`
  без `<Forms>`. `create_managed_form` → `ok=False,
  stage='operation'`, message «Write operation failed: XML block
  <Forms> not found (no closing tag).»; XML **unchanged**;
  `audit.tool_name='create_managed_form'`, `audit.status='error'`
  (flow всё равно написал audit с error статусом). Исключение
  наружу не вышло.
- **Scenario C — `replace_module_method_body` без
  `confirm_replace=True`:** `ok=False,
  tool='replace_module_method_body'`, message «requires explicit
  confirm_replace=True.»; `payload.keys()=['data']` — **нет
  runtime**, **нет snapshot refs**, **нет audit_path**; файл
  `dump/.audit/audit.jsonl` **не создан** (проверено
  `audit_file.exists()==False`). Flow не запускался вообще.
- **Интеграционные критерии (ТЗ Step 7):**
  1. Все mutating metadata tools Step 4–6 идут через
     `run_write_flow` и оставляют `operation_id`, snapshot refs,
     audit-запись. ✓ (подтверждено 5 mutating шагами сценария A)
  2. Все verification tools Step 5 работают как самостоятельные
     public tools, не идут через flow, не пишут audit. ✓
     (подтверждено 3 verification шагами + сценарием C для
     rollback-hint-path)
  3. `tool_name` в audit = public tool name. ✓ (Scenario A Step 9:
     `audit.tool_name='append_module_method'`)
  4. Registry write-server = 23 (не менялся). ✓
  5. Dev-check зелёный. ✓
- **Dev-check после Step 7:** `imports_ok = true`,
  `write_server_tools` = 23 (все 23 имени на месте),
  `read_server_tools` = 15 (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`
- **README `mcp-write-server`** дополнен разделом «Phase 3
  Metadata Changes закрыт (Phase 3 / Step 7 — final integration
  pass)» с сводкой по составу контура, гарантиями,
  registry = 23, зафиксированной минимальной правкой
  `create_catalog` stub и перечнем остающихся временных stub'ов.
- **Корневой `README.md`** обновлён: Phase 3 помечена завершённой
  с кратким расписыванием по group A/B/C/D, Phase 4 указана как
  следующий этап, материалы Phase 3 перенесены в «Закрытые фазы».
- **Phase 3 / Metadata Changes закрыт.** Критерии приёмки
  `phase-3-metadata-changes-plan.md` достигнуты: ≥ 4–5
  mutating metadata tools (реально 9: 2 создания объектов + 2
  attribute-level Step 4 + 4 form/module-level Step 6 + 1 уже
  существующий `create_common_module`); ≥ 2–3 verification tools
  (`verify_attribute_exists`, `diff_dump_fragment`, расширенный
  `verify_metadata_change` с 5 kind); audit отражает metadata
  operations корректно (`tool_name=intent.operation_name`); dev-check
  зелёный на каждом шаге; подтверждён end-to-end metadata scenario.

### Phase 4 / Step 1 — planning Intelligence Layer (в процессе)

- **Документационный вход в Phase 4 зафиксирован.** Phase 3
  (Metadata Changes) закрыта окончательно; Phase 4 (Intelligence
  Layer) открыта как активная фаза. Кода в Step 1 не пишется:
  затронуты только `docs/architecture/`, корневой `README.md` и
  этот файл.
- **Создан `docs/architecture/phase-4-intelligence-plan.md`** —
  полный плановый документ Phase 4 в стиле phase-плана:
  - **Назначение фазы.** `mcp-intelligence-server` превращается из
    skeleton (только `ping`) в рабочий read-only intelligence layer
    поверх готовых read- (15 tools) и write- (23 tools) серверов.
    Не «магический reasoning», а набор осмысленных read-only
    инструментов: где используется объект, что затронет правка,
    какая последовательность безопаснее, что сломалось по журналу,
    какую подсказку дать пользователю, где подозрительные места.
  - **Целевой результат.** Собственный `runtime/` слой
    intelligence-server'а; public tools, покрывающие dependency
    analysis, impact analysis, troubleshooting, recommendations;
    все intelligence-tools read-only, никогда не запускают
    write-flow; cross-app import строго `intelligence → read` и
    `intelligence → write` (только pure / read-only helpers);
    `ToolResult` явно разделяет `confirmed` / `presumed` источники;
    Phase 1/2/3 контуры не деградируют; `dev-check` зелёный.
  - **Набор инструментов фазы — 16 tools, 4 группы.**
    - Группа A (dependency / structure):
      `analyze_object_dependencies`, `build_dependency_subgraph`,
      `find_references_to_object`, `find_module_method_usages`.
    - Группа B (change impact / pre-change):
      `estimate_change_impact`, `find_affected_forms`,
      `find_affected_modules`, `suggest_safe_change_order`.
    - Группа C (troubleshooting / diagnostics):
      `analyze_runtime_issue`, `analyze_event_log_patterns`,
      `diagnose_broken_form_binding`,
      `diagnose_missing_method_or_attribute`.
    - Группа D (recommendation / assistant):
      `suggest_fix_for_issue`, `suggest_metadata_patch_plan`,
      `summarize_configuration_risk`,
      `prepare_intelligence_report`.
    Для каждого tool'а зафиксировано назначение, слой
    реализации (read-side dump adapter / read-server tools /
    intelligence runtime / pure helpers `metadata_ops`) и MVP
    содержимое payload'а. Это план, а не декларация готового
    продукта; конкретные сигнатуры уточняются в Step 2.
  - **Guardrails фазы.** Intelligence-tools ничего не меняют
    (нет snapshot'ов, нет `run_write_flow`, нет audit). Read-only
    by construction. Cross-app import — только вперёд:
    `intelligence → read` и `intelligence → write` (read-only
    helpers); обратное направление запрещено, чтобы read/write
    остались независимыми и без циклов. Fail-closed при недостатке
    данных (никаких silent-default'ов). Каждый payload честно
    разделяет `confirmed` (прямые данные: dump substring, XML tag,
    event-log row) и `presumed` (эвристики). Рекомендации ≠
    авто-применение: `suggest_*` отдают `suggested_tools` —
    имена существующих public write-tool'ов с набросками
    аргументов, **запуск остаётся за вызывающим**.
    Производительность дешевле точности в MVP (substring,
    `rglob`, lightweight BSL-regex; AST/индексы/graph databases —
    за рамками Phase 4).
  - **Что не входит в Phase 4.** Fully autonomous self-healing,
    auto-apply fixes, production decision making (prod-block
    guardrails Phase 2/3 остаются), multi-agent orchestration,
    настоящий reasoning engine / ML-модели, product workflows
    Phase 5, замена stub'ов Phase 2/3
    (`apply_config_from_files`, `update_database_configuration`,
    `create_dump_snapshot`) на реальный `1cv8`-integration —
    параллельный follow-up.
  - **Критерии приёмки.** Phase 4 закрыта, когда: реализованы
    и зарегистрированы **не менее 4–5** public intelligence-tools,
    покрывающих хотя бы **две** группы из A / B / C / D;
    подтверждены **не менее 2–3** рабочих troubleshooting-сценариев;
    подтверждён **хотя бы один** end-to-end intelligence scenario
    (например, зависимости → impact → порядок правок →
    intelligence report); `dev-check` остаётся зелёным; read- /
    write-серверы (15 / 23 tools) не деградируют; каждый
    intelligence-tool маркирует `confirmed` vs `presumed`.
- **Создан `docs/architecture/phase-4-step-map.md`** — стартовая
  карта Phase 4 на 7 шагов:
  - **Step 1.** Intelligence operation contract / phase planning
    (текущий, документационный).
  - **Step 2.** Подготовка policy / config / contracts (если
    нужно). Возможный вариант: новый frozenset
    `_INTELLIGENCE_OPERATIONS` в `onec-policy-engine` с
    `reason_code="allowed_intelligence"`,
    `require_snapshots=False`. Альтернатива — явно зафиксировать,
    что intelligence не проходит policy-check (read-only, отдельный
    сервер) и policy не трогать. Backward compatibility Phase 2/3
    сохраняется.
  - **Step 3.** Internal analysis helper layer
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`:
    `models.py` (`IntelligenceRuntimeContext`), `context.py`
    (`build_runtime_context` поверх `check_environment_health`),
    `dump_scanner.py` (XML + BSL поиск поверх `read_dump_file` /
    `find_files_by_pattern` / `read_text_file`), `reference_finder.py`,
    `graph.py` (минимальный `DependencyGraph`). Public tools пока
    не появляются; registry intelligence-server по-прежнему
    `['ping']`.
  - **Step 4.** Первая волна public intelligence-tools (группа A):
    `find_references_to_object`, `analyze_object_dependencies`,
    `find_module_method_usages`, опционально
    `build_dependency_subgraph`. Cross-app import — только через
    `mcp_read_server.runtime` и pure helpers
    `mcp_write_server.runtime.metadata_ops`.
  - **Step 5.** Diagnostics tools (группа C):
    `analyze_runtime_issue`, `analyze_event_log_patterns`,
    `diagnose_broken_form_binding`,
    `diagnose_missing_method_or_attribute`. Опираются на
    `get_event_log`, `get_object_structure`, `get_form_structure`,
    `check_runtime_health`, `diagnose_connectivity_issue` из
    read-server и helpers Step 3. Каждый `ToolResult` явно
    разделяет `confirmed` / `presumed`.
  - **Step 6.** Impact / recommendation tools (группы B и D):
    `estimate_change_impact`, `find_affected_forms`,
    `find_affected_modules`, `suggest_safe_change_order`,
    `suggest_fix_for_issue`, `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`,
    `prepare_intelligence_report`. `suggested_tools` ссылается
    **только на существующие** public-инструменты write-server
    (Phase 2/3).
  - **Step 7.** Final integration pass: один сквозной сценарий
    (`find_references_to_object` → `estimate_change_impact` →
    `suggest_safe_change_order` → `prepare_intelligence_report`)
    плюс 1–2 failure-path. Кода стараемся не трогать; разрешена
    минимальная точечная правка только при честной необходимости
    (как в Phase 2 Step 10 / Phase 3 Step 7). Phase 4 закрывается.
- **Корневой `README.md` обновлён.** В блоке «Текущий статус по
  фазам» строка `**Phase 4** — следующий этап.` заменена на
  развернутый абзац: Phase 4 — активная фаза разработки, цель —
  Intelligence Layer (read-only intelligence-tools поверх
  read/write слоёв; dependency / impact analysis, troubleshooting,
  рекомендации; read- и write-серверы не деградируют;
  intelligence-tools не выполняют write-операции и не принимают
  решений за пользователя). Phase 0–3 остались в «Закрытых
  фазах». Добавлен новый раздел «Активная фаза:» со ссылками на
  `phase-4-intelligence-plan.md` и `phase-4-step-map.md`.
- **Никакого кода в Step 1 не написано.** `apps/`, `packages/`,
  `scripts/`, `.github/`, `pyproject.toml`, стенды, `.claude.json`
  не затрагивались. Registry всех трёх серверов **не менялись**:
  `read=15`, `write=23`, `intelligence=['ping']`. `dev-check`
  не запускался — Step 1 чисто документационный.

### Phase 4 / Step 2 — policy / config / contracts для intelligence (завершён)

- **Архитектурное решение Step 2: intelligence-server сознательно
  не проходит через `onec-policy-engine`.** Выбран второй вариант
  из двух, зафиксированных в `phase-4-step-map.md`: вместо добавления
  новой категории `_INTELLIGENCE_OPERATIONS` с
  `reason_code="allowed_intelligence"` контракт зафиксирован как
  отсутствие write-policy роутинга для intelligence.
- **Почему именно этот вариант.**
  1. Phase 4 guardrail требует read-only by construction: intelligence
     никогда не меняет состояние, не запускает `run_write_flow`,
     не пишет audit. Поля `PolicyDecision` (`allow_write`,
     `require_snapshots`) для read-only операций бессодержательны.
  2. `check_write_allowed` семантически про **write**. Добавление
     `_INTELLIGENCE_OPERATIONS` расширило бы поверхность движка и
     форсировало бы преждевременное перечисление 16 intelligence
     operation names, которые реально через движок не авторизуются.
  3. Выбранный вариант зеркалит уже существующий паттерн
     `mcp-read-server`: read-side тоже не роутится через
     write-policy. Единая политика «read-only серверы не трогают
     write-policy» делает архитектуру однородной.
  4. Ветка `unknown_intent` в `_new_check` — бесплатная страховка:
     если intelligence-operation name когда-нибудь случайно попадёт
     в `WriteIntent` и пойдёт через `check_write_allowed`, движок
     честно откажет fail-closed, не придумывая ответ.
- **Что сделано в коде (минимально).**
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
    — **только расширен module docstring** новым абзацем про
    intelligence: явно зафиксировано, что Phase 4 intelligence-ops
    не роутятся через этот движок, и что `unknown_intent` branch
    служит free safety net. Логика `check_write_allowed`,
    `_legacy_check`, `_new_check` и все четыре frozenset'а
    (`_MUTATING_OPERATIONS`, `_NON_MUTATING_SUPPORT_OPERATIONS`,
    `_METADATA_MUTATING_OPERATIONS`, `_METADATA_SUPPORT_OPERATIONS`)
    **не тронуты** — backward compatibility Phase 2/3 полная.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — docstring пакета расширен разделом про Phase 4 контракт:
    read-only by construction; намеренно **не импортирует**
    `onec_policy_engine`; cross-app import идёт строго вперёд
    (`intelligence → read`, `intelligence → write` только через
    pure / read-only helpers). Код (экспорт `ToolResult`, `ping`,
    `list_tools`, `get_tool`) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — docstring модуля расширен явной фиксацией: bootstrap не
    импортирует `onec_policy_engine`. Logика `REGISTERED_TOOLS`,
    `list_tools()`, `get_tool()` не менялась.
- **Что сделано в документации.**
  - `packages/onec-policy-engine/README.md` — добавлен раздел
    «Intelligence-операции (Phase 4) — не проходят через этот
    движок», описывающий принятое решение, его практический эффект
    и bidirectional mirror с intelligence-server README.
  - `apps/mcp-intelligence-server/README.md` — добавлен раздел
    «Read-only контракт Phase 4»: не пишет файлы, не проходит
    через `check_write_allowed`, allowed cross-app import только
    вперёд, fail-closed при недостатке данных. Блок «Чего здесь
    намеренно ещё нет» расширен указанием, что реальные
    intelligence-инструменты появятся в Step 3–6, а текущий шаг
    фиксирует только контракт.
- **`onec-config` не тронут.** Проверено: `EnvironmentConfig` уже
  содержит все поля, которые intelligence runtime ожидает
  использовать в Step 3+ (`name`, `base_id`, `base_path`,
  `publication_name`, `http_base_url`, `dump_path`,
  `timeout_seconds`, `allow_write`). Никаких полей «на будущее»
  не добавлено.
- **`scripts/dev/selfcheck.py` не тронут.** Legacy режим
  `check_write_allowed("production", True)` /
  `check_write_allowed("local-dev", False)` работает как прежде
  (`production_blocked`, `write_not_allowed`).
- **Registry всех трёх серверов не менялись.**
  - `read_server_tools` = 15 (не тронут);
  - `write_server_tools` = 23 (не тронут);
  - `intelligence_server_tools` = `['ping']` (не тронут).
- **Ручная проверка (4 сценария, все зелёные).**
  - **Scenario A — no policy import leak.** Просканированы все
    4 `.py`-файла в
    `apps/mcp-intelligence-server/src/mcp_intelligence_server/`
    на наличие строки-импорта `from onec_policy_engine`/`import
    onec_policy_engine`. Найдено: **0 реальных импортов**. Docstring-
    упоминания (`__init__.py`, `server.py`) — ожидаемые и нужны,
    т.к. именно они фиксируют контракт в коде.
  - **Scenario B — backward compatibility Phase 2/3.** 4 представителя
    + legacy: `apply_config_from_files →
    allowed_mutating/require_snapshots=True`;
    `check_write_preconditions → allowed_non_mutating/False`;
    `create_catalog → allowed_metadata_mutating/True`;
    `verify_attribute_exists → allowed_metadata_support/False`;
    legacy `("production", True) → production_blocked`;
    legacy `("local-dev", False) → write_not_allowed`. Все коды
    `reason_code` и флаги `require_snapshots` совпадают с
    Phase 3 / Step 7 baseline.
  - **Scenario C — free safety net для intelligence-op name в
    WriteIntent.** 7 имён из плана Phase 4 (`find_references_to_object`,
    `analyze_object_dependencies`, `find_module_method_usages`,
    `estimate_change_impact`, `analyze_runtime_issue`,
    `suggest_fix_for_issue`, `prepare_intelligence_report`) → все
    возвращают `allowed=False`, `reason_code=unknown_intent`.
    Штатный путь для intelligence — не сюда; но если случайно
    попадёт, движок fail-closed'ит.
  - **Scenario D — intelligence-server импортируется и работает.**
    `import mcp_intelligence_server` чистый; `ping()` вернул
    `ok=True`, `tool_name='ping'`; `list_tools() == ['ping']`.
    Докстринги и README не сломали runtime.
- **Dev-check после Step 2 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15, `write_server_tools` = 23,
  `intelligence_server_tools = ['ping']`, `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 4 / Step 3 — internal analysis helper layer в `mcp-intelligence-server/runtime/` (в процессе)

- **Создан подпакет
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`**
  — аналог `mcp_read_server.runtime` и
  `mcp_write_server.runtime`, но под **read-only** intelligence
  сценарии. Это внутренний helper-слой, на котором будут стоять
  будущие public intelligence-tools Step 4–6. Public tools на этом
  шаге **не добавляются**; `REGISTERED_TOOLS` intelligence-server'а
  и `list_tools()` остаются равны `['ping']`.
- **Состав подпакета (6 файлов, все новые).**
  - `runtime/models.py` — `IntelligenceRuntimeContext(environment,
    health_results, health_codes, dump_root)`. Data snapshot
    окружения и его health-состояния для одного вызова
    intelligence-инструмента. `dump_root` всегда заполнен
    (`Path(environment.dump_path)`); существует ли он на диске —
    отражено в `health_codes` (напр. `dump_missing`), так что
    context остаётся конструируемым даже для сломанных окружений.
  - `runtime/context.py` — `build_runtime_context(environment)`
    собирает `check_environment_health(...) +
    summarize_health(...)` из `onec-health`, резолвит
    `dump_root`, на диск не пишет, `onec_policy_engine` не
    импортирует.
  - `runtime/dump_scanner.py` — тонкие intelligence-ориентированные
    обёртки поверх `mcp_read_server.runtime` (allowed cross-app
    import направление `intelligence → read`):
    `list_xml_files(dump_root)`, `list_bsl_files(dump_root)`,
    `list_files_by_extensions(dump_root, extensions)`,
    `read_utf8_text(path)`. Нужны, чтобы intelligence-helper'ы
    вызывали осмысленно-именованный API вместо generic read-server
    примитивов напрямую.
  - `runtime/reference_finder.py` — substring поиск по `*.xml` и
    `*.bsl` дампа. Public-функции: `find_references(dump_root,
    needle, *, extensions=None, max_matches=None)` возвращает
    `list[ReferenceMatch]` (frozen dataclass: `relative_path`
    POSIX-style + relative к `dump_root`, `source` ∈ `{xml, bsl}`,
    `line_number` 1-based, `preview` — strip'нутая + обрезанная до
    160 символов matching-строка); `count_references` —
    вспомогательный счётчик. Пустой `needle` fail-closed через
    `ValueError`. Отсутствующее совпадение — пустой список, не
    ошибка.
  - `runtime/graph.py` — минимальный каркас dependency-графа:
    `DependencyNode(name, kind=None)` и `DependencyEdge(from_node,
    to_node, kind=None)` — оба frozen; `DependencyGraph(nodes,
    edges, adjacency)` — обычный dataclass. Helpers: `empty_graph()`,
    идемпотентный `add_node(graph, name, *, kind=None)` (возвращает
    `True/False` — добавил ли), `add_edge(graph, from_node,
    to_node, *, kind=None)` (auto-creates endpoint nodes; duplicates
    в `edges` допустимы, adjacency — без дубликатов),
    `neighbors(graph, name)` — прямые преемники или `[]` для
    неизвестного имени. Это именно маленький честный фундамент;
    реальный subgraph-обход с ограничением глубины появится в
    Step 4+ в public tool `build_dependency_subgraph`.
  - `runtime/__init__.py` — явный `__all__` с 15 именами
    (`IntelligenceRuntimeContext`, `build_runtime_context`,
    `list_xml_files`, `list_bsl_files`, `list_files_by_extensions`,
    `read_utf8_text`, `ReferenceMatch`, `find_references`,
    `count_references`, `DependencyNode`, `DependencyEdge`,
    `DependencyGraph`, `empty_graph`, `add_node`, `add_edge`,
    `neighbors`). Docstring подпакета явно фиксирует
    read-only контракт и разрешённые направления cross-app import.
- **Никаких других файлов не создано**, никакие другие зоны не
  тронуты. Read- и write-серверы, `onec-config`, `onec-health`,
  `onec-policy-engine`, `scripts/dev/selfcheck.py`, `.github/`,
  `pyproject.toml` — без изменений.
- **`mcp-intelligence-server/README.md`** дополнен разделом
  «Internal runtime helper layer (Phase 4 / Step 3)»: состав
  подпакета, описание каждого файла, прямое указание, что это
  **не** public tools и registry не меняется. В блоке «Чего здесь
  намеренно ещё нет» уточнение, что public tools появляются в
  Step 4–6.
- **Ручная проверка (5 сценариев, все зелёные).** Временный
  скрипт `C:\Users\user\AppData\Local\Temp\phase4_step3_checks.py`
  материализует dump на `tempfile.TemporaryDirectory` (3 файла:
  `Catalogs/ТестовыйСправочник.xml`, `Reports/ОбычныйОтчёт.xml`,
  `CommonModules/TestModule/Ext/Module.bsl`) и проверяет:
  - **A.** `build_runtime_context(env)` на temp dump →
    `dump_root == tempdir`; 3 health-check в стабильном порядке
    (`dump_path_exists`, `http_gateway`, `search_index`);
    `health_codes == ['gateway_down']` (dump существует + bsl
    есть → `dump_missing`/`index_lock` отсутствуют; http_base_url
    заведомо нереагирующий → `gateway_down` честно ловится).
  - **B.** `dump_scanner` → `list_xml_files` находит обе
    `*.xml`-карточки, `list_bsl_files` находит `Module.bsl`,
    `list_files_by_extensions(..., ("xml", "bsl"))` возвращает 3
    файла в отсортированном порядке; `read_utf8_text` прочитал
    модуль — 235 байт, содержит `Процедура MCP_Test()` и
    `ТестовыйСправочник`.
  - **C.** `find_references(dump_root, "ТестовыйСправочник")` →
    **4 совпадения** на 3 относительных путях (1 в XML
    каталога — `<Name>`; 2 в BSL — комментарий и вызов
    `Справочники.ТестовыйСправочник.СоздатьЭлемент()`; 1 в XML
    отчёта — `<Reference>`). `sources == ['bsl', 'xml']`.
    `max_matches=2` честно обрывает скан на двух.
    `count_references` == 4. Пустой `needle` → `ValueError(
    "find_references requires a non-empty needle.")`. Несуществующая
    строка → `[] ` (не ошибка).
  - **D.** `empty_graph() → DependencyGraph(nodes=[], edges=[],
    adjacency={})`. `add_node` дважды с тем же именем: первый
    `True`, второй `False` (идемпотентность). `add_edge` от
    `Report.ОбычныйОтчёт` к `Catalog.ТестовыйСправочник` дважды +
    `add_edge` от `CommonModule.TestModule` (не созданного
    явно) к каталогу: `len(nodes)=3`, `len(edges)=3` (дубликат
    edge сохраняется), `adjacency` — без дубликатов target'ов.
    `neighbors(graph, "Report.ОбычныйОтчёт") ==
    ["Catalog.ТестовыйСправочник"]`; `neighbors(graph,
    "Unknown.Name") == []`.
  - **E.** `intelligence_server.list_tools() == ['ping']`;
    `ping().ok == True`. Registry intelligence-server не изменился.
- **Dev-check после Step 3 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), `intelligence_server_tools = ['ping']` (не тронут),
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 4 — первая волна public intelligence-tools группы A (в процессе)

- **Intelligence-server впервые поднят выше skeleton.** Registry
  intelligence-server'а вырос с `['ping']` до
  **`['analyze_object_dependencies', 'find_module_method_usages',
  'find_references_to_object', 'ping']`** (4 инструмента, группа A
  покрыта). Read- и write-серверы не тронуты, их registry
  остались `read=15`, `write=23`.
- **Контрактные инварианты Phase 4 сохранены.**
  - все три новых public tool'а строго **read-only**: не пишут
    файлы, не создают snapshot'ов, не идут через `run_write_flow`,
    не пишут audit;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом по 10 `.py`-файлам
    intelligence-server'а — 0 реальных импортов);
  - cross-app import идёт только через
    `mcp_read_server.runtime` и внутренний
    `mcp_intelligence_server.runtime` Step 3;
  - исключения из runtime-слоя (`PlatformError`, `ValueError`,
    `OSError`) перехватываются внутри public tool'а и
    конвертируются в `ToolResult(ok=False, ...)` — наружу не
    пробрасываются.
- **Единый failure-style.** `ok=False` **только** при реальной
  проблеме (пустой аргумент / dump-root недоступен / объект не
  найден в дампе). Пустой-но-валидный результат поиска — `ok=True`
  с пустым списком и message «No references found» / «No
  occurrences … found».
- **Payload discipline.** В каждом `ToolResult` confirmed-факты
  (подстрочные совпадения в конкретном файле; токены из
  XML-карточки) явно отделены от presumed-выводов (эвристическая
  классификация declaration / usage по шаблону; зависимости,
  извлечённые из BSL, где токен может быть в комментарии или
  строковом литерале). Никакого fake-smart анализа: эвристика
  честно помечена как presumed.
- **Public tools группы A (3 штуки).**
  - **`find_references_to_object(environment, object_name,
    max_matches=None)`** — substring-скан `*.xml` + `*.bsl` под
    `environment.dump_path` через
    `runtime.reference_finder.find_references`. Payload:
    `object_name`, `total_matches`, `confirmed_matches`
    (`relative_path`, `source`, `line_number`, `preview`),
    `confirmed_sources` (уникальные пути), `sources_used`
    (`dump_xml` / `dump_bsl` — булевы), `max_matches_applied`,
    `runtime.health_codes`. Пустой `object_name` → `ok=False`.
  - **`find_module_method_usages(environment, method_name,
    max_matches=None)`** — substring-скан **только `*.bsl`**.
    `confirmed_matches` — все находки; дополнительно
    эвристическая классификация в `presumed_declarations`
    (шаблон `^(Процедура|Функция|Procedure|Function)\s+<name>\s*\(`)
    и `presumed_usages` (всё остальное). `sources_used` →
    `dump_bsl` булев.
  - **`analyze_object_dependencies(environment, object_name)`** —
    локализует XML-карточку объекта (`*.xml` со stem'ом равным
    `simple_name`) и его собственные BSL-модули (путь содержит
    `simple_name` как сегмент). Извлекает known-prefix ссылки
    (`Справочник.`, `Документ.`, `ОбщийМодуль.`, `Catalog.`,
    `CommonModule.` и ещё ~25 прочих, Cyrillic + English форм)
    через regex. Self-references отфильтрованы. Split payload:
    `confirmed_dependencies` (из XML-карточки —
    структурный сигнал), `presumed_dependencies` (из BSL —
    substring/regex heuristic). Возвращает также минимальный
    `graph` (`nodes`, `edges`, `adjacency`) поверх
    `runtime.graph`. Если объект не найден нигде (no XML, no BSL)
    → `ok=False`, честный fail-closed.
- **Опциональный `build_dependency_subgraph` не регистрировался.**
  В ТЗ Step 4 указан как опциональный «если MVP укладывается без
  раздутия». Решение: не добавлять. Минимальный `graph`-объект
  (`nodes`/`edges`/`adjacency`) уже возвращается внутри
  `analyze_object_dependencies`; отдельный public façade с
  depth-traversal добавит алгоритмическую сложность без
  проверяемого benefit на Step 4. Это задача естественно закроется
  в Step 6 (`estimate_change_impact` / `find_affected_*`
  переиспользуют тот же runtime).
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — переписан: добавлены 3 новые public-функции + internal
    helpers (`_runtime_payload`, `_match_to_dict`, `_simple_name`,
    `_extract_prefixed_references`, `_fail`). `ping` сохранён
    как был. Константа `_KNOWN_PREFIXES` (Cyrillic + English форм,
    single + plural).
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь собирается из четырёх callables.
    Docstring модуля (Phase 4 contract, отсутствие импорта
    `onec_policy_engine`) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен тремя новыми именами и добавлены
    соответствующие re-export'ы. Phase 4 contract docstring не
    менялся.
- **Никаких изменений за пределами intelligence-server и README /
  PROJECT-STATUS.** `mcp-read-server`, `mcp-write-server`,
  `packages/**`, `scripts/**`, `.github/**`, `pyproject.toml`,
  корневой `README.md`, plan/step-map Phase 4 — не тронуты.
  `runtime/` подпакет Step 3 — без правок, ни одного нового файла.
- **`mcp-intelligence-server/README.md` переписан.** Раздел «Что
  сейчас внутри» теперь перечисляет четыре tool'а с сигнатурами.
  Добавлен раздел «Public tools группы A (Phase 4 / Step 4)» с
  фиксацией read-only контракта (не пишут, не идут через policy /
  write-flow / audit), единого failure-style, confirmed vs
  presumed discipline и подробным описанием каждого из трёх
  новых инструментов. Блок «Чего здесь намеренно ещё нет»
  приведён в соответствие: группы C / B / D — в Step 5–6;
  `build_dependency_subgraph` пока не отдельный tool; AST-парсинга
  нет (MVP substring + regex).
- **Ручная проверка (6 сценариев, все зелёные).** Временный
  скрипт `C:\Users\user\AppData\Local\Temp\phase4_step4_checks.py`
  материализует в `tempfile.TemporaryDirectory` связный mini-dump
  (Catalogs/Main.xml + Catalogs/Secondary.xml + Reports/UsesMain.xml
  + Catalogs/Main/Ext/ManagerModule.bsl + CommonModules/UtilModule/Ext/Module.bsl)
  с **настоящими** взаимными ссылками между Main и Secondary и
  вызовами `MCP_Test()`, и проверяет:
  - **A.** `find_references_to_object(env, "Main")` → `ok=True`,
    `total_matches=6` на 4 относительных путях (Catalogs/Main.xml,
    Catalogs/Main/Ext/ManagerModule.bsl,
    CommonModules/UtilModule/Ext/Module.bsl, Reports/UsesMain.xml);
    `sources_used={dump_xml:True, dump_bsl:True}`; повторный
    вызов с `max_matches=2` → `total_matches=2`,
    `max_matches_applied=True`.
  - **B.** `find_module_method_usages(env, "MCP_Test")` →
    `ok=True`, `total_matches=3`; `presumed_declarations=1`,
    `presumed_usages=2`; preview declaration содержит
    «Процедура MCP_Test». `max_matches=1` → `total_matches=1`,
    `max_matches_applied=True`.
  - **C.** `analyze_object_dependencies(env, "Main")` → `ok=True`;
    `confirmed_sources=['Catalogs/Main.xml']`;
    `presumed_sources=['Catalogs/Main/Ext/ManagerModule.bsl']`;
    `confirmed_dependencies` содержит `Справочник.Secondary` и
    `Перечисление.ЕдиницыИзмерения`, self-ref `Справочник.Main`
    исключён; `presumed_dependencies` содержит `Справочники.Secondary`,
    `ОбщийМодуль.LegacyUtil`, `Перечисления.ЕдиницыИзмерения`;
    `graph.nodes=6`, `graph.edges=5`, `adjacency['Main']` непустой.
  - **D.** Failure-path'ы, единый стиль: несуществующая строка в
    find_references_to_object → `ok=True, total_matches=0`;
    несуществующий метод → `ok=True, total_matches=0`;
    несуществующий объект в analyze_object_dependencies →
    `ok=False, "not found in dump"`; пустой `object_name` /
    `method_name` → `ok=False`; недоступный dump_root →
    `ok=False, "Dump root does not exist: ..."`. Ни одного
    исключения наружу.
  - **E.** `mis.list_tools() == ['analyze_object_dependencies',
    'find_module_method_usages', 'find_references_to_object',
    'ping']`; `get_tool('find_references_to_object')` возвращает
    callable, `get_tool('nonexistent')` → `None`.
  - **F.** grep `^\s*(from|import)\s+onec_policy_engine\b` по
    всем 10 `.py`-файлам
    `apps/mcp-intelligence-server/src/**/*.py` → **0 реальных
    импортов**. Phase 4 cross-app import контракт сохранён и после
    Step 4.
- **Dev-check после Step 4 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools =
  ['analyze_object_dependencies', 'find_module_method_usages',
  'find_references_to_object', 'ping']`**, `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 4 / Step 5 — diagnostics / troubleshooting tools группы C (завершён)

- **Intelligence-server покрыл вторую группу Phase 4.** Registry
  вырос с 4 (`ping` + 3 tool'а группы A) до **8** tool'ов:
  `['analyze_event_log_patterns', 'analyze_object_dependencies',
  'analyze_runtime_issue', 'diagnose_broken_form_binding',
  'diagnose_missing_method_or_attribute', 'find_module_method_usages',
  'find_references_to_object', 'ping']`. Критерий приёмки фазы
  «≥ 4–5 public tools, покрывающих ≥ 2 группы из A/B/C/D»
  удовлетворён по счёту и охвату групп.
- **Контрактные инварианты Phase 4 сохранены.**
  - все четыре новых Step 5 tool'а строго **read-only**: не пишут,
    не идут через `run_write_flow`, не пишут audit, не создают
    snapshot'ов;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом по 10 `.py`-файлам
    intelligence-server'а — 0 реальных импортов; docstring-упоминания
    остаются ожидаемыми);
  - cross-app import только вперёд: `intelligence → read`
    (`mcp_read_server.tools.{check_runtime_health,
    diagnose_connectivity_issue, get_event_log, get_form_structure}`)
    и `intelligence → write` через **pure read-only helper**
    (`mcp_write_server.runtime.metadata_ops.module_contains_method`
    — чистая substring+regex функция над текстом модуля, без
    побочных эффектов);
  - исключения перехватываются и превращаются в `ToolResult(ok=False, ...)`
    либо в findings — наружу не пробрасываются.
- **Единый failure-style сохранён с Step 4.**
  - `ok=True` — анализ завершён (findings могут быть пустыми).
  - `ok=False` — анализ провести не удалось (некорректный вход,
    критическая зависимость вернула ошибку, dump/модуль недоступен
    там, где критически нужен).
  - Для `analyze_event_log_patterns` и `diagnose_broken_form_binding`
    ошибка read-server'а пробрасывается как `ok=False` с message
    вида `read.<tool> failed: <original>`.
  - Для `analyze_runtime_issue` фиксация найденных health-кодов
    штатно идёт через `ok=True` — сам по себе runtime aggregator
    свою работу сделал.
- **Payload discipline — `confirmed_findings` / `presumed_findings`
  / `recommended_checks` / `sources_used`.**
  - `confirmed_findings` — факты, завязанные на конкретный артефакт
    (health-код из `check_runtime_health`, verdict
    `method_exists`/`method_missing` над реально прочитанным
    модулем, handler с явной привязкой, аттрибут в XML-карточке).
  - `presumed_findings` — эвристические объяснения: probable cause,
    pattern-метка (`error_spike`, `handler_method_missing`,
    `module_file_missing`, `attribute_missing` …).
  - `recommended_checks` — короткие next-step подсказки.
  - `sources_used` — список строковых маркеров использованных
    зависимостей (`read.check_runtime_health`,
    `read.get_event_log`, `dump_scanner.read_utf8_text`,
    `write_runtime.metadata_ops.module_contains_method`,
    `dump_xml:<path>`). Это честная трассируемая цепочка без
    скрытого reasoning.
- **Public tools группы C (4 штуки).**
  - **`analyze_runtime_issue(environment)`** — high-level
    aggregator поверх `read.check_runtime_health` +
    `read.diagnose_connectivity_issue` + intelligence runtime Step 3.
    Каждый non-`ok` health-код (`gateway_down` / `dump_missing`
    / `index_lock`) превращается в `confirmed_findings` с
    детерминированным hint; rule-based вывод
    `diagnose_connectivity_issue` идёт в `presumed_findings`; raw
    per-check snapshot — в `health_checks`; `recommended_checks`
    — под каждый код. `ok=False` только если `environment is None`
    или внутренняя ошибка.
  - **`analyze_event_log_patterns(environment, period_start=None,
    period_end=None, level=None, user=None)`** — делегирует в
    `read.get_event_log` (фильтры пробрасываются verbatim и реально
    доходят до endpoint'а). Полученные entries подсчитываются
    `collections.Counter`: `total_entries`, top-N `top_levels` /
    `top_users` / `top_events`, до 5 `error_samples`. Если
    error/critical entries ≥ 2 — в `presumed_findings` добавляется
    pattern `error_spike`. Пустой лог → `ok=True` с пустыми
    findings. Если read-server вернул `ok=False` — пропускаем с
    тем же message (`read.get_event_log failed: ...`).
  - **`diagnose_broken_form_binding(environment, object_name,
    form_name=None)`** — `read.get_form_structure` (live HTTP) +
    pure helper `module_contains_method` из write-runtime.
    Ожидаемая форма payload'а read-server'а:
    `{elements, handlers:[{event, handler_method}],
    module_relative_path}`. `confirmed_findings` содержит коды
    `form_has_no_elements`, `form_has_no_handlers`,
    `handler_method_missing`, `module_not_readable`; к каждому
    `presumed_findings` добавляет probable-cause narrative.
    `ok=False`, если endpoint/форма недоступны; во всех других
    случаях `ok=True` — даже когда найдены все три типа symptom'ов.
  - **`diagnose_missing_method_or_attribute(environment, *,
    object_name=None, module_relative_path=None, method_name=None,
    attribute_name=None)`** — два комбинируемых режима:
    **method_mode** (`module_relative_path` + `method_name`) —
    модуль читается из дампа, verdict через
    `module_contains_method`; **attribute_mode** (`object_name` +
    `attribute_name`) — XML-карточка ищется по stem-совпадению,
    regex поверх типовых `<Attribute>` форм
    (`<Attribute name="...">` и вложенный `<Name>...`). Verdicts:
    `method_exists` / `method_missing` / `module_file_missing` /
    `attribute_exists` / `attribute_missing` / `xml_card_missing`.
    `ok=False` только если не передан ни один валидный режим или
    dump-root отсутствует; в остальных случаях `ok=True` с
    verdict'ом в `confirmed_findings` и probable-cause narrative в
    `presumed_findings` (только для *missing*-verdict'ов).
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — расширен: новый блок cross-app import'ов (`mcp_read_server.tools`,
    `mcp_write_server.runtime.metadata_ops.module_contains_method`);
    добавлены helper'ы (`_HEALTH_CODE_HINTS`, `_extract_event_entries`,
    `_top_n`, `_ATTRIBUTE_TAG_PATTERNS`, `_xml_declares_attribute`);
    добавлены четыре новые public-функции группы C. Код группы A
    (Step 4) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь из 8 callables. Docstring не
    менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен четырьмя именами; добавлены re-export'ы.
    Phase 4 contract docstring не менялся.
- **Никаких изменений за пределами intelligence-server.**
  `mcp-read-server`, `mcp-write-server`, `packages/**`, `scripts/**`,
  `.github/**`, `pyproject.toml`, корневой `README.md`,
  `phase-4-intelligence-plan.md`, `phase-4-step-map.md`, `runtime/`
  подпакет intelligence-server'а (Step 3) — не тронуты.
- **`mcp-intelligence-server/README.md`** обновлён:
  - блок «Что сейчас внутри» теперь перечисляет **8** tool'ов в
    двух группах (A — Step 4, C — Step 5);
  - блок «Чего намеренно ещё нет» обновлён: группы B/D появятся в
    Step 6; MVP substring+regex остаётся без AST;
  - добавлен раздел «Public tools группы C (Phase 4 / Step 5)» с
    read-only контрактом, единым failure-style, описанием
    confirmed/presumed discipline и подробной спецификацией
    каждого из четырёх tool'ов.
- **Ручная проверка (7 сценариев, все зелёные).** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase4_step5_checks.py` поднимает
  **in-process `ThreadingMixIn`/`TCPServer`** на `127.0.0.1:<rand>`
  (без сетевых вызовов к реальному стенду, без Apache, без `1cv8`)
  и материализует temp-dump в `tempfile.TemporaryDirectory`.
  Эндпоинт честно отдаёт event-log и form/structure, `last_event_log_query`
  фиксирует query-string, пришедшую на endpoint. Сценарии:
  - **A. `analyze_runtime_issue(dead_env)`** (dump жив, http мёртв) →
    `ok=True`, `health_codes` включает `gateway_down`;
    `confirmed_count=1` (gateway_down с hint), `presumed_count=1`
    (вывод `diagnose_connectivity_issue`), `health_checks=3` raw
    row; `sources_used = {read.check_runtime_health,
    read.diagnose_connectivity_issue}`.
  - **B. `analyze_event_log_patterns(env, period_start='2026-04-24',
    level='Error', user='alice')`** при 3 pre-loaded entries:
    `ok=True`, `total_entries=3`, `top_events` содержит
    `ConnectionLost` (2 повторa), `error_samples=2`,
    `presumed_findings=['error_spike']`; фильтры доходят до
    endpoint'а (`start=['2026-04-24'], level=['Error'],
    user=['alice']`) и эхо-отражаются в payload. Пустой лог →
    `ok=True`, `presumed_findings=[]`.
  - **C. `diagnose_broken_form_binding(env, 'Catalog.Main',
    'ФормаСписка')`** с handlers
    `[OnClick→MissingHandler, OnOpen→ExistingHandler]` и модулем,
    который содержит только `ExistingHandler` и `OtherMethod`:
    `ok=True`, `confirmed_findings` содержит
    `handler_method_missing` именно для `MissingHandler`,
    `ExistingHandler` не помечен; `sources_used` включает
    `read.get_form_structure` + `dump_scanner.read_utf8_text` +
    `write_runtime.metadata_ops.module_contains_method`.
  - **D. `diagnose_missing_method_or_attribute`** — пять суб-случаев:
    method positive (`method_exists`, presumed пустой), method
    negative (`method_missing` + probable cause), attribute positive
    (`attribute_exists` для `Main` + `Жанр`), attribute negative
    (`attribute_missing` + probable cause), combined mode
    (method_missing + attribute_exists в одном ответе).
  - **E. failure path (7 подсценариев, единый стиль):**
    пустой `object_name` → `ok=False`; ни один mode не передан →
    `ok=False, "Provide..."`; dead endpoint в
    `analyze_event_log_patterns` → `ok=False, sources_used=[read.get_event_log]`;
    dead endpoint в `diagnose_broken_form_binding` → `ok=False`;
    `environment is None` в `analyze_runtime_issue` → `ok=False,
    "environment is missing"`; несуществующий dump_root в
    `diagnose_missing_method_or_attribute` → `ok=False, "Dump root
    does not exist: ..."`; отсутствующий модульный файл
    (`Catalogs/Ghost/Ext/Module.bsl`) → `ok=True` с
    `confirmed_findings=[{code: module_file_missing, ...}]` —
    finding, не ошибка инструмента. Ни одного исключения наружу.
  - **F. registry invariant:** `mis.list_tools() == ['analyze_event_log_patterns',
    'analyze_object_dependencies', 'analyze_runtime_issue',
    'diagnose_broken_form_binding', 'diagnose_missing_method_or_attribute',
    'find_module_method_usages', 'find_references_to_object', 'ping']`;
    `ping()` работает; `get_tool('analyze_runtime_issue')` возвращает
    функцию; `get_tool('nonexistent')` → `None`.
  - **G. cross-app import контракт:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` (10 файлов) →
    **0 реальных импортов**.
- **Dev-check после Step 5 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools` — 8 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 6 — impact / recommendation tools группы B и D (завершён)

- **Intelligence-server покрыл группы B и D Phase 4.** Registry
  вырос с 8 (`ping` + 3 группа A + 4 группа C) до **16** tool'ов.
  Полный отсортированный список:
  `['analyze_event_log_patterns', 'analyze_object_dependencies',
  'analyze_runtime_issue', 'diagnose_broken_form_binding',
  'diagnose_missing_method_or_attribute', 'estimate_change_impact',
  'find_affected_forms', 'find_affected_modules',
  'find_module_method_usages', 'find_references_to_object', 'ping',
  'prepare_intelligence_report', 'suggest_fix_for_issue',
  'suggest_metadata_patch_plan', 'suggest_safe_change_order',
  'summarize_configuration_risk']`. Покрытие групп Phase 4 теперь
  полное: A (3) + B (4) + C (4) + D (4) + `ping` = 16.
- **Контрактные инварианты Phase 4 сохранены.**
  - все восемь новых Step 6 tool'ов строго **read-only**: не пишут
    файлы, не идут через `run_write_flow`, не пишут audit, не
    создают snapshot'ов;
  - `mcp_intelligence_server` по-прежнему **не импортирует**
    `onec_policy_engine` (подтверждено grep'ом
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` — 0 реальных импортов);
  - cross-app import только вперёд: `intelligence → read` (для
    Step 6 переиспользуется ровно тот же набор, что в Step 5),
    `intelligence → write` исключительно через pure read-only
    helper `module_contains_method` (не активирован новыми
    Step 6 tool'ами напрямую — они опираются на runtime Step 3 и
    public tools Step 4/5);
  - исключения перехватываются и превращаются в `ToolResult(ok=False, ...)`
    либо в findings — наружу не пробрасываются.
- **Единый failure-style сохранён с Step 4/5.**
  - `ok=True` — анализ/рекомендация выполнены (findings могут быть
    пустыми; «ничего не нашли» — валидный результат, а не ошибка).
  - `ok=False` — инструмент не смог отработать (пустой обязательный
    аргумент, dump-root отсутствует там, где он критически нужен,
    неизвестный `issue_code`).
  - `suggest_metadata_patch_plan` для unsupported-kind / unknown-kind
    / deletion-goal возвращает `ok=True` с честным
    `presumed_findings` объяснением и пустым
    `suggested_write_tools` — это рекомендация, а не отказ;
    делать это `ok=False` было бы неискренне.
- **Payload discipline — `confirmed_findings` / `presumed_findings`
  / `recommended_checks` / `suggested_tools` /
  `suggested_write_tools` / `recommended_sequence` /
  `sources_used`.**
  - `confirmed_findings` — факты из dump-сканов (точные счётчики
    ссылок, найденные XML/BSL пути, `health_codes`),
    либо явные входные параметры в plan/recipe инструментах.
  - `presumed_findings` — эвристики (impact band, weak form
    signals, probable causes, объяснение почему план пустой).
  - `suggested_tools` / `suggested_write_tools` — **только реальные
    имена** уже зарегистрированных public-tool'ов. Ни одного
    придуманного имени; будущие capability помечаются как
    отсутствующие через `presumed_findings` (как делает
    `suggest_metadata_patch_plan` для `document` /
    `information_register` / `role` / `report` /
    `data_processor`).
- **Public tools группы B (4 штуки).**
  - **`estimate_change_impact(environment, object_name)`** —
    компактная оценка радиуса. Использует `find_references` и
    `list_xml_files/list_bsl_files` из runtime Step 3.
    `confirmed_findings` — счётчики `reference_count`,
    `xml_references`, `bsl_references`, плюс `own_xml_cards` /
    `own_bsl_modules` (как в `analyze_object_dependencies`) и
    `referenced_paths`. `presumed_findings` — детерминированный
    `impact_level` band (none/low/medium/high от пороговых
    значений 0/5/20), плюс `module_impact_possible` если есть BSL
    hits и `form_impact_possible` если есть form-like пути.
    `suggested_tools` указывает на `find_references_to_object`,
    `analyze_object_dependencies`, `find_affected_forms`,
    `find_affected_modules`. Empty / not-found остаётся
    `ok=True` с честным «0 references».
  - **`find_affected_forms(environment, object_name)`** —
    `find_references` + path-эвристика `_is_form_path`
    (наличие сегмента `Forms`, либо `form` / `форма` в stem).
    Совпадения, попадающие в форму-подобный путь, идут в
    `confirmed_findings`; остальные — в `presumed_findings` с
    pattern `weak_form_signal`. Это MVP: substring + path
    inspection, не XML-парсер. Сильные хиты предполагают
    follow-up через `diagnose_broken_form_binding`.
  - **`find_affected_modules(environment, object_name)`** —
    `find_references`, разбивка по `source`. `*.bsl` matches
    идут в `confirmed_findings` + агрегируются в
    `module_summary` (per-module `match_count`, отсортированный
    по убыванию). `*.xml` matches идут в `presumed_findings` с
    pattern `module_signal_via_xml` (XML может косвенно описывать
    module-level linkage). `suggested_tools`:
    `find_module_method_usages`, `find_references_to_object`.
  - **`suggest_safe_change_order(environment, object_name)`** —
    рекомендательный orchestrator. Дёргает свои же
    `analyze_object_dependencies` и `estimate_change_impact`
    (без побочных эффектов — они read-only) для сбора
    `object_found_in_dump`, `confirmed_dependency_count`,
    `presumed_dependency_count`, `impact_level`. Возвращает
    фиксированный 6-шаговый `recommended_sequence`:
    (1) read-baseline (`get_object_structure`), (2) impact /
    dependency сканы (intelligence + read), (3) preflight
    snapshots (`check_write_preconditions`,
    `create_backup_snapshot`, `create_dump_snapshot`),
    (4) метадата-правка (`create_catalog`,
    `add_catalog_attribute`, `add_document_attribute`,
    `create_managed_form`, `add_form_element`,
    `append_module_method`, `replace_module_method_body`),
    (5) verification (`verify_*`, `diff_dump_fragment`,
    `get_form_structure`), (6) audit/rollback hint
    (`describe_last_write_operation`, `prepare_rollback_hint`).
    `presumed_findings` адаптируется: `cascade_risk` если есть
    зависимости, `object_not_in_dump` если объект не нашли,
    `high_blast_radius` для `impact_level=high`.
- **Public tools группы D (4 штуки).**
  - **`suggest_fix_for_issue(environment, issue_code,
    context_data=None)`** — rule-based mapping
    `_ISSUE_FIX_RULES` (11 codes: `gateway_down`, `dump_missing`,
    `index_lock`, `form_has_no_elements`, `form_has_no_handlers`,
    `handler_method_missing`, `method_missing`,
    `module_file_missing`, `attribute_missing`, `xml_card_missing`,
    `error_spike`). Каждый rule содержит `probable_cause` →
    `presumed_findings`, упорядоченные `steps` →
    `recommended_checks`, `suggested_tools` /
    `suggested_write_tools` — **только реальные** имена. Unknown
    `issue_code` → `ok=False` с message «Unknown issue_code …
    Known codes: [...]» — fail-closed (выбран один стиль и
    выдержан). `context_data` пробрасывается verbatim в
    `confirmed_findings` (MVP не параметризует recipe по
    контексту).
  - **`suggest_metadata_patch_plan(environment, target_kind,
    target_name, change_goal)`** — table-driven plan generator,
    использующий **только** реальные write-server tools.
    `_PATCH_PLAN_RECIPES` покрывает 8 видов: `catalog`,
    `common_module`, `catalog_attribute`, `document_attribute`,
    `managed_form`, `form_element`, `module_method`,
    `module_method_body`. Каждый recipe — упорядоченный список
    write-tool'ов: preconditions → backup → dump snapshot →
    metadata mutation → (опц.) `update_database_configuration`
    → verify. `_PATCH_PLAN_UNSUPPORTED` честно перечисляет
    target_kind'ы, для которых Phase 2/3 write-server **не
    имеет** create-tool (`document`, `information_register`,
    `role`, `report`, `data_processor`) — план возвращается
    пустой с pattern `kind_unsupported` в `presumed_findings`.
    Ключевые слова удаления (`delete`, `remove`, `drop`,
    `удалить`, `удалять`, `убрать`) в `change_goal` дают pattern
    `deletion_not_supported`. Unknown kind → `unknown_kind`.
    `_step_description(...)` подтягивает короткое объяснение
    каждого write-tool из `_WRITE_TOOL_DESCRIPTIONS`. Никаких
    выдуманных tool-имён.
  - **`summarize_configuration_risk(environment, object_name=None)`**
    — короткое rule-based резюме. Глобально (без `object_name`)
    риск задаёт `runtime.health_codes`: `dump_missing` → high,
    `gateway_down` или `index_lock` → medium, иначе low.
    Пер-объект также делает `find_references`, добавляет
    `reference_count` в `confirmed_findings`; > 20 ссылок →
    medium, ≤ 20 — low. `object_not_referenced` поднимается в
    `presumed_findings`, если объект указан, но 0 хитов —
    «либо изолированный, либо misspelled». Никаких категоричных
    утверждений — только pattern-based.
  - **`prepare_intelligence_report(environment, subject,
    include_tools=None)`** — read-only orchestrator.
    Whitelisted whitelist `_REPORT_KNOWN_TOOLS` (9 имён, все —
    public intelligence-tool'ы из этого же модуля). Дефолтный
    набор `_REPORT_DEFAULT_INCLUDE` =
    `(analyze_runtime_issue, analyze_object_dependencies,
    estimate_change_impact, summarize_configuration_risk)`.
    `subject` обязателен (пустой → `ok=False`); по нему
    параметризуются `analyze_object_dependencies` и аналоги
    через таблицу режимов (`no_subject` /
    `subject_as_object_name` / `subject_as_method_name` /
    `subject_as_object_name_optional`). Имена вне whitelist
    падают в `skipped_unknown_tools`, не теряются молча. Каждый
    sub-tool оборачивается `try / except Exception` —
    исключения превращаются в `sections[name]={ok:False,
    message,...}`, наружу никогда не пробрасываются. Aggregate
    включает `confirmed_findings`, `presumed_findings`,
    `recommended_checks`, `suggested_tools` (set, отсортирован),
    каждый item помечен своим `tool` для трассируемости.
- **Что изменилось в коде.**
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/tools.py`
    — расширен: добавлены private helper'ы (`_impact_level`,
    `_is_form_path`, `_step_description`, `_invoke_report_tool`,
    rule-таблицы `_ISSUE_FIX_RULES`, `_PATCH_PLAN_RECIPES`,
    `_PATCH_PLAN_UNSUPPORTED`, `_DELETION_KEYWORDS`,
    `_WRITE_TOOL_DESCRIPTIONS`, `_REPORT_KNOWN_TOOLS`,
    `_REPORT_DEFAULT_INCLUDE`); добавлены восемь новых
    public-функций групп B и D. Код групп A (Step 4) и C
    (Step 5) не менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/server.py`
    — `REGISTERED_TOOLS` теперь из 16 callables; список
    импортов расширен восемью новыми именами. Docstring не
    менялся.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__init__.py`
    — `__all__` расширен восемью именами; добавлены
    re-export'ы; package-level docstring обновлён описанием
    публичной поверхности на конец Step 6 (16 tools, 4 группы).
- **Никаких изменений за пределами intelligence-server.**
  `mcp-read-server`, `mcp-write-server`, `packages/**`, `scripts/**`,
  `.github/**`, `pyproject.toml`, корневой `README.md`,
  `phase-4-intelligence-plan.md`, `phase-4-step-map.md`, `runtime/`
  подпакет intelligence-server'а (Step 3) — не тронуты. Ни одного
  нового файла в проекте: всё уложено в существующие модули.
- **`mcp-intelligence-server/README.md`** обновлён:
  - блок «Что сейчас внутри» теперь перечисляет **16** tool'ов
    в четырёх группах (A — Step 4, C — Step 5, B и D — Step 6);
  - блок «Чего намеренно ещё нет» обновлён: группы B/D больше
    не упоминаются как ожидаемые в Step 6 — они теперь часть
    публичной поверхности; оставлены MVP-honesty-заметки про
    отсутствие AST-парсера и ML-кластеризации;
  - добавлен раздел «Public tools группы B (Phase 4 / Step 6)»
    с подробной спецификацией impact/affected/safe-order
    инструментов;
  - добавлен раздел «Public tools группы D (Phase 4 / Step 6)»
    с подробной спецификацией fix/plan/risk/report
    инструментов и явной фиксацией, что `suggested_tools` /
    `suggested_write_tools` ссылаются исключительно на уже
    существующие public-имена.
- **Ручная проверка (11 сценариев, все зелёные).** Временный
  скрипт
  `C:\Users\user\AppData\Local\Temp\intelligence_step6_check.py`
  материализует синтетический dump в `tempfile.mkdtemp()`
  (`Catalogs/Primary/Primary.xml`,
  `Catalogs/Primary/Forms/ItemForm/Form.xml`,
  `Catalogs/Primary/Ext/Module.bsl`) и проходит:
  - **A. registry invariant.** `mis.list_tools()` возвращает
    ровно 16 имён (см. список выше); `tools == sorted(tools)`
    (стабильный алфавитный порядок); `get_tool('estimate_change_impact')
    is mis.estimate_change_impact`; `get_tool('nonexistent') is None`.
  - **B. `estimate_change_impact`.** «Primary» → `ok=True`,
    `reference_count=4`, `level=low`, 3 presumed findings
    (impact_estimate + module_impact_possible + form_impact_possible).
    «GhostObject» → `ok=True`, 0 ссылок, `level=none`,
    1 presumed (impact_estimate). Empty → `ok=False`. Bad dump
    → `ok=False`.
  - **C. `find_affected_forms`.** «Primary» → `ok=True`,
    1 confirmed (Forms/ItemForm/Form.xml), 3 presumed (XML/BSL
    вне form-пути). «Catalog.Secondary» → `ok=True`,
    0 confirmed, 1 presumed — only-presumed path.
  - **D. `find_affected_modules`.** «Primary» → `ok=True`,
    1 модуль (`Catalogs/Primary/Ext/Module.bsl`), 1 BSL match,
    3 XML signals.
  - **E. `suggest_safe_change_order`.** «Primary» → 6 шагов,
    `impact=low`, `suggested_write_tools` содержит 17 уникальных
    реальных имён write-server'а (`add_catalog_attribute`, …,
    `verify_object_exists`). «GhostObject» (не в дампе) →
    тоже `ok=True`, 6 шагов, `presumed_findings` содержит
    `object_not_in_dump` — sequence отдаётся как generic.
  - **F. `suggest_fix_for_issue`.** Известный
    `handler_method_missing` → `ok=True`, 3 step recipe,
    `suggested_write_tools=[append_module_method,
    verify_module_contains]`. Известный `error_spike` →
    `ok=True`, write-tools пуст. Неизвестный
    `totally_unknown_code` → `ok=False` с message «Unknown
    issue_code … Known codes: [...]» (fail-closed, как
    зафиксировано в ТЗ). Empty → `ok=False`.
  - **G. `suggest_metadata_patch_plan`.** Поддерживаемая задача
    `catalog/create new catalog` → `ok=True`, 6 write-tool
    шагов (`check_write_preconditions` …
    `verify_object_exists`). `module_method/add method` →
    `ok=True`, 5 шагов. Unsupported `document/create document`
    → `ok=True`, пустой план, `presumed_findings=[
    {pattern: kind_unsupported, ...}]`. Unknown
    `weird_thing/do something` → `unknown_kind`. Deletion
    `catalog/delete it` → `deletion_not_supported`. Empty kind
    / empty name → `ok=False`.
  - **H. `summarize_configuration_risk`.** Глобальный режим
    при `gateway_down` (live HTTP в тесте недоступен) →
    `ok=True, risk_level=medium`. Пер-объект «Primary» при том
    же health → `medium` (gateway-rule имеет приоритет, как
    задокументировано). Пер-объект «GhostObject» → тоже
    `medium`, но добавлен `presumed_findings` с
    `object_not_referenced`. Bad dump (`dump_missing` в
    health_codes) → `risk_level=high` глобально и пер-объект.
  - **I. `prepare_intelligence_report`.** Default include
    `(analyze_runtime_issue, analyze_object_dependencies,
    estimate_change_impact, summarize_configuration_risk)` →
    `ok=True`, 4 sections, ни одного skipped. Whitelist
    `[analyze_object_dependencies, find_affected_forms,
    wat_unknown]` → `ok=True`, 2 sections,
    `skipped_unknown_tools=['wat_unknown']`. Empty subject →
    `ok=False`. Bad dump → всё ещё `ok=True`: каждая sub-tool
    отдельно репортит свою ошибку через свой section, наружу
    исключений не выходит.
  - **J. failure-style.** Проверены все обязательные fail-paths
    выше; ни одного исключения наружу — все обработаны
    `ToolResult(ok=False, ...)` или превращены в findings.
  - **K. cross-app import контракт:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/mcp-intelligence-server/src/**/*.py` →
    **0 реальных импортов** (assert в скрипте).
- **Известные MVP-компромиссы Step 6 (зафиксированы честно).**
  - `find_affected_forms` и `find_affected_modules` —
    substring + path-heuristic, не XML/BSL парсер. Это
    осознанное MVP-решение (см. ТЗ: «Никакого AST-парсера»).
  - `suggest_safe_change_order` отдаёт фиксированный 6-шаговый
    шаблон, не настоящий topo-sort по графу зависимостей.
    Решение принимается каллером, какой именно
    `suggested_write_tool` из шага 4 применять.
  - `summarize_configuration_risk` — порог `> 20` references
    → medium и `dump_missing` → high — это rule, не модель.
    Это поведение явно перечислено в docstring и в README.
  - `prepare_intelligence_report` — orchestration по
    whitelisted списку, без условной маршрутизации. Если
    sub-tool вернул `ok=False` (например, dead HTTP в
    `analyze_runtime_issue`), report остаётся `ok=True`, но
    содержимое соответствующей section — `ok=False` со своим
    сообщением. Это сознательное решение: report должен
    собрать всё что смог, а не падать при первой деградации.
- **Dev-check после Step 6 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools` = 23
  (не тронут), **`intelligence_server_tools` — 16 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 4 / Step 7 — final integration pass (завершён, Phase 4 Intelligence Layer закрыт окончательно)

- **Step 7 — это закрывающий integration pass, не новая
  разработка.** В intelligence-server **не добавлено ни одного
  нового public-tool'а**; ни одной новой private-функции, ни
  одного нового файла. Размер registry — 16 tool'ов, как и в
  конце Step 6. Read-server и write-server не тронуты вообще.
- **Никаких точечных правок кода не понадобилось.** Сквозной
  integration pass прошёл с первой попытки на коде, собранном в
  Step 4–6: payload discipline согласована, failure-style един,
  никаких выдуманных tool-имён в `suggested_*`. Это и было
  главной задачей Step 7 — подтвердить, что слой работает как
  единое целое.
- **Сквозной интеграционный сценарий A (happy path, 9 шагов,
  одна цепочка).** Каждый следующий tool работает над фактом,
  подтверждённым предыдущим — это не серия независимых
  вызовов, а реальная цепочка.

  Synthetic dump (`tempfile.mkdtemp()`):
  `Catalogs/Primary/Primary.xml` (с `<Type>Catalog.Primary</Type>`,
  `<Reference>Catalog.Secondary</Reference>`,
  `<Module>CommonModule.Helpers</Module>`),
  `Catalogs/Primary/Forms/ItemForm/Form.xml`,
  `Catalogs/Primary/Ext/Module.bsl` (русские
  `Процедура Старт()` + `Функция РассчитатьИтог() Экспорт`),
  `Catalogs/Secondary/Secondary.xml`,
  `CommonModules/Helpers/Ext/Module.bsl`.

  - **A.1 `find_references_to_object('Primary')`** → `ok=True`,
    4 точных substring-матча, `sources_used.dump_xml=True`,
    `dump_bsl=True`. `confirmed_sources` содержит файлы под
    `Catalogs/Primary/...`. Дальше передаётся
    `target_object='Primary'` (carry-forward).
  - **A.2 `analyze_object_dependencies('Primary')`** → `ok=True`,
    `confirmed_dependencies` = `{Catalog.Secondary,
    CommonModule.Helpers}` (XML-карточка), `presumed_dependencies`
    = русские формы тех же зависимостей (BSL-модуль). **Discipline
    invariant подтверждён скриптом**: `confirmed_names &
    presumed_names == ∅` — на одинаковых именах множества не
    пересекаются.
  - **A.3 `estimate_change_impact('Primary')`** → `ok=True`,
    `reference_count=4`, `impact_level='low'` (det. threshold).
    `sources_used` перечисляет три помощника runtime Step 3.
  - **A.4 `find_affected_forms('Primary')`** → `ok=True`,
    `confirmed_findings` непустой (структурный путь
    `Catalogs/Primary/Forms/ItemForm/Form.xml`),
    `presumed_findings` содержит weak-form-сигналы.
  - **A.5 `find_affected_modules('Primary')`** → `ok=True`,
    `module_summary` непустой (попадание в
    `Catalogs/Primary/Ext/Module.bsl`), XML-сигналы — в
    `presumed_findings`.
  - **A.6 `suggest_safe_change_order('Primary')`** → `ok=True`,
    6 шагов, `impact_level='low'`. `suggested_write_tools`
    содержит **17 уникальных имён** — все проверены скриптом
    через `mws.list_tools()` и подтверждены как реально
    зарегистрированные в write-server.
  - **A.7 `suggest_metadata_patch_plan('common_module', 'Helpers',
    "add a method to the helpers common module")`** → `ok=True`,
    6 write-tool шагов: `check_write_preconditions →
    create_backup_snapshot → create_dump_snapshot →
    create_common_module → update_database_configuration →
    verify_module_contains`. Все 6 имён есть в реальном
    write-registry.
  - **A.8 `suggest_fix_for_issue('handler_method_missing',
    context_data={...Primary, Module.bsl, GhostHandler})`** →
    `ok=True`, 3 step recipe, `suggested_write_tools=
    [append_module_method, verify_module_contains]` — оба
    реальны. `context_data` пробрасывается verbatim в
    `confirmed_findings`.
  - **A.9 `summarize_configuration_risk('Primary')`** →
    `ok=True`, `risk_level='medium'` (gateway_down в health_codes,
    как и предусмотрено правилом).
  - **A.10 `prepare_intelligence_report('Primary')`** →
    `ok=True`, **4 sections** (default include_set), 0 skipped,
    aggregated `confirmed=3, presumed=5, recommended_checks=3,
    suggested_tools=6`. **Provenance discipline подтверждена**:
    каждый item в `confirmed_findings` / `presumed_findings`
    помечен своим `tool` (имя — реальный intelligence-tool),
    каждое имя в aggregated `suggested_tools` — реальный tool
    из intelligence- или read-registry.
- **Failure-path сценарии (5 штук, единый стиль, все зелёные).**
  - **F.1** `analyze_object_dependencies(env_ok,
    'TotallyMissingObject')` → `ok=False`,
    message `Object '...' not found in dump (no XML card, no BSL module).`.
  - **F.2** `diagnose_missing_method_or_attribute(env_ok)` без
    обоих режимов → `ok=False`, message начинается с `Provide`.
  - **F.3** `find_references_to_object(env_ok, "")` →
    `ok=False`, `object_name is empty.`.
  - **F.4** `prepare_intelligence_report(env_no_dump,
    'TotallyMissingObject', include_tools=[
    'analyze_object_dependencies', 'wat_no_such_tool'])` —
    смешанный сценарий: и плохой dump, и неизвестный
    include-name. Результат соответствует контракту: report
    остаётся `ok=True` (orchestrator завершился), `wat_no_such_tool`
    — в `skipped_unknown_tools`, а внутренняя section
    `analyze_object_dependencies` имеет `ok=False`. Sub-tool
    отдельно отчитывается о своей деградации, исключений
    наружу нет.
  - **F.5** `suggest_metadata_patch_plan` под deletion-goal
    (`"delete this catalog"`) → `ok=True` с `recommended_sequence=[]`
    и `presumed_findings` содержит `deletion_not_supported`.
    Параллельно `suggest_metadata_patch_plan('report',
    'AnyReport', 'create a report')` (известный, но
    unsupported kind) → `ok=True`, `recommended_sequence=[]`,
    `presumed_findings == [{pattern: kind_unsupported, ...}]`,
    `suggested_write_tools == []` — никаких выдуманных имён.
- **Real-tool-name discipline (программный assert).** Скрипт
  собирает `mis.list_tools()`, `mrs.list_tools()`,
  `mws.list_tools()` в три set'а и для каждого payload (impact,
  safe-order, plan, fix, report) проверяет: каждое имя в
  `suggested_tools` принадлежит intelligence ∪ read; каждое имя
  в `suggested_write_tools` принадлежит write. **Ни одного
  выдуманного имени** — ни в одной точке цепочки.
- **Read-only контракт подтверждён программно.** В скрипте есть
  жёсткий assert: grep
  `^\s*(from|import)\s+onec_policy_engine\b` по
  `apps/mcp-intelligence-server/src/**/*.py` (10 `.py`-файлов
  пакета) → **0 реальных импортов**. Это автоматическая
  проверка, а не глаз — assert упадёт, если кто-то добавит
  такой импорт.
- **Registry invariants под программным assert.**
  - intelligence: `set(...)==expected_intel`,
    `tools == sorted(tools)` — 16 имён, алфавит;
  - read: `len(...) == 15`;
  - write: `len(...) == 23`.
  Любой дрифт обнаружится падением assert'а.
- **Что изменилось в коде Step 7.** Только PROJECT-STATUS и
  оба README. Ни строчки в `apps/mcp-intelligence-server/src/**`,
  ни в `apps/mcp-read-server/**`, ни в `apps/mcp-write-server/**`,
  ни в `packages/**`, ни в `scripts/**`. Это **сознательный итог
  Step 7** — закрывающий integration pass, не разработка.
- **`mcp-intelligence-server/README.md`** обновлён точечно:
  из блока «Чего намеренно ещё нет» убрана строка про
  «финальной интеграции Phase 4 (один сквозной integration
  pass и фиксация baseline'а — Phase 4 / Step 7)» — этот
  пункт теперь сделан. Остальные MVP-honesty заметки (отсутствие
  AST, ML-кластеризации, настоящего topo-sort, MCP-обвязки)
  оставлены как есть — они и есть честная неполнота, не
  имеющая отношения к закрытию Phase 4.
- **Корневой `README.md`** обновлён: Phase 4 переведена из
  «активная фаза» в «завершён» с краткой сводкой публичной
  поверхности (16 read-only intelligence tool'ов в группах
  A/B/C/D); материалы Phase 4 (`phase-4-intelligence-plan.md`,
  `phase-4-step-map.md`) перемещены в блок «закрытых фаз».
  Phase 5 пока без активной строки — её планирование не
  входит в Step 7.
- **Ручная проверка.** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\intelligence_step7_integration.py`
  единым прогоном выполняет: registry invariants → 9-шаговую
  цепочку Scenario A → 5 failure-path сценариев → grep на
  `onec_policy_engine`. Все assert'ы прошли с первой попытки.
  Финальная строка вывода — `ALL Step 7 integration checks
  passed.`. Скрипт лежит **вне проекта**, в `%TEMP%`, и в
  репозиторий не попадает.
- **Dev-check после Step 7 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (без изменений), `write_server_tools`
  = 23 (без изменений), **`intelligence_server_tools` — 16 tool'ов**,
  `selfcheck_status = ok`, `Dev check completed successfully.`.

### Phase 5 / Step 1 — planning Product Layer (завершён)

- **Стратегический сдвиг фазы.** После закрытия Phase 4 у
  платформы есть полное инженерное ядро: read (15) + write
  (23) + intelligence (16). Phase 5 — **не «ещё несколько
  tool'ов»**: это переход от набора серверов к цельному
  продукту, который можно установить, поднять, подключить
  к 1С, безопасно использовать, сопровождать, откатывать,
  диагностировать и реально выдать другому человеку или
  команде. Step 1 фиксирует этот сдвиг документационно;
  кода в Step 1 не написано.
- **Создано два новых документа в `docs/architecture/`.**
  - `docs/architecture/phase-5-product-layer-plan.md` —
    основной план фазы. Содержит: назначение фазы (почему
    после четырёх закрытых фаз нам всё ещё нужен
    отдельный Product Layer); целевой результат в
    терминах того, что должен уметь пользователь после
    закрытия Phase 5 (8-пунктовый нарратив от установки
    до smoke test'а); прямой mapping незакрытых
    стратегических разрывов на блоки фазы (что
    закрывается полностью, что частично, что остаётся
    enterprise track'ом); сравнение Phase 5 с Phase 1–4
    (адресат меняется с агента на человека); шесть
    продуктовых блоков; список из 20 продуктовых
    capability'ов, сгруппированных по блокам;
    guardrails; явный список того, что **не** входит;
    11 критериев приёмки; связь с предыдущими фазами;
    раздел открытых вопросов для Step 2+.
  - `docs/architecture/phase-5-step-map.md` — стартовая
    карта фазы из 8 шагов в едином формате
    (Цель / Что меняем / Затронутые зоны / Результат):
    Step 1 — product contract / scope / packaging
    (текущий шаг); Step 2 — installer / bootstrap
    contract; Step 3 — runtime orchestration / single
    entry point; Step 4 — environment doctor / health
    dashboard; Step 5 — guided workflow layer (3
    базовых workflow'а); Step 6 — rollback / recovery /
    audit UX; Step 7 — real-stand / 1cv8 binary
    integration track; Step 8 — final integration pass.
- **Ключевые продуктовые блоки, зафиксированные в плане
  (A–F).**
  - **A. Installation / bootstrap** — installer, setup
    wizard, prereqs doctor; режимы установки local-dev /
    stand / enterprise-bootstrap-only.
  - **B. Runtime orchestration** — единая точка входа
    start/stop/status/reload; environment profile
    manager; product-уровневый health dashboard.
  - **C. Safe workflow layer** — 2–3 базовых guided
    workflow'а (safe-add-attribute, safe-add-module-method,
    stand-health-check); запрет silent apply.
  - **D. Rollback / recovery / audit UX** — operation
    history viewer, rollback assistant, recovery workflow.
  - **E. Real-stand / production-readiness** — reference
    stand spec, 1cv8 binary integration contract,
    end-to-end smoke test, packaging, versioning.
  - **F. Operator UX / docs** — operator manual,
    administrator manual, developer manual, user-facing
    message style guide.
- **Какие стратегические разрывы закрывает Phase 5.**
  Полностью закрываются: разрыв (1) runtime/deployment
  слой, (3) installer, (6) автоматический rollback, (7)
  intelligence в продуктовом UX, (8) workflow layer,
  (9) end-to-end на стенде. Частично закрываются:
  разрыв (2) 1cv8 binary integration (Phase 5 даёт
  contract + smoke test, не полное замещение всех
  stub'ов), (4) расширение metadata operations
  (намеренно не расширяется — фаза не про tool surface),
  (5) полное structural editing XML/BSL (AST не
  вводится). Остаётся enterprise track'ом: разрыв (10)
  enterprise hardening (SSO/RBAC, multi-tenant, secrets
  vault, federated audit storage) — отдельный трек
  после Phase 5.
- **Guardrails Phase 5 (зафиксированы в плане).** Запрет
  production write by default; обязательное явное
  targeting окружения; никакого silent apply; install /
  upgrade / rollback только с диагностикой; fail-closed
  при неполных prereqs; честная деградация, а не
  «магия»; **продуктовый UX не размывает safety
  guarantees Phase 2–4** (никакого обхода
  `run_write_flow`, никакого обхода audit, никакого
  обхода snapshot'ов, никакого импорта
  `onec_policy_engine` в intelligence-server, read-only
  intelligence сохраняется).
- **Что не входит в Phase 5 (зафиксировано явно).**
  Fully autonomous agent; magical self-healing
  production; бесконечная оркестрация; полная замена
  1С-администрирования; enterprise-всё-в-одном за один
  шаг; полное замещение всех Phase 2 stub'ов
  настоящей 1cv8-бинарью; AST-парсер XML/BSL;
  крупный рефакторинг read/write/intelligence ради
  продукта.
- **Критерии приёмки Phase 5 (11 пунктов).**
  Установка по короткому понятному сценарию;
  платформа поднимается как согласованный набор
  сервисов; ≥ 2–3 end-to-end user workflows;
  rollback / recovery — реальный продуктовый сценарий;
  реальный стенд / 1cv8 integration имеют явный трек
  готовности; документация существует как продукт;
  dev-check зелёный; read/write/intelligence не
  деградировали (15 / 23 / 16 tools); read-only
  контракт intelligence-server'а сохранён;
  safety guarantees Phase 2–4 не размыты; продукт
  ощутимо ближе к «готовому к выдаче пользователю».
- **Что изменилось в коде Step 1.** **Ничего.** Ни
  одной строчки. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `.github/`, `runtime/`, `tools.py`,
  `server.py` всех трёх серверов — не тронуты.
  Registry'ы read (15), write (23), intelligence (16)
  не менялись. Dev-check остаётся в том же зелёном
  состоянии, что и после Phase 4 / Step 7.
- **Обновлены документы.**
  - Корневой `README.md`: Phase 4 переведена в
    «закрытые фазы», Phase 5 помечена как активная
    фаза с кратким описанием цели (Product Layer);
    добавлены ссылки на оба новых документа
    (`phase-5-product-layer-plan.md`,
    `phase-5-step-map.md`); остальные разделы
    `README.md` не менялись.
  - `PROJECT-STATUS.md`: обновлены шапка (текущий
    шаг → Phase 5 / Step 1, статус → in progress),
    добавлен подробный Step 1 record (этот блок),
    обновлена «Следующий шаг» секция (см. ниже),
    обновлены «Крупные этапы проекта» (Phase 4 →
    Закрыта, Phase 5 → Активная фаза).
- **Открытые вопросы Step 1 (для Step 2+).** В плане
  явно зафиксированы вопросы, на которые Step 1 не
  даёт окончательного ответа: формат релиза (clone
  + lockfile / zip / wheel / installer-скрипт);
  формат product-config (YAML / TOML / JSON);
  транспорт MCP (stdio / TCP / локальный socket);
  интерактивный vs декларативный setup; storage
  operation history; глубина 1cv8-integration в
  smoke test. Step 1 не делает вид, что ответы
  уже найдены.

### Phase 5 / Step 2 — installer / bootstrap contract (завершён)

- **Принятые архитектурные решения Step 2 (закрывают
  открытые вопросы Step 1).**
  - **Расположение product-слоя:** `apps/platform/`,
    пакет `onec_platform`. Решение принято консервативно:
    это исполняемое приложение продукта (не reusable
    library), и оно органично встаёт рядом с тремя
    MCP-серверами в `apps/`. `packages/onec-product/`
    отвергнут, так как product layer — это **сам
    продукт**, а не разделяемая зависимость нескольких
    приложений. Соответствующая правка `apps/README.md`
    выполнена: раздел теперь честно описывает, что в
    `apps/` живут и MCP-серверы, и продуктовое
    приложение.
  - **Формат product-config:** **JSON**. Используем
    `json` из stdlib, новых зависимостей не привносим
    (важно: `pyproject.toml` не тронут). YAML/TOML
    отвергнуты ради нулевых dependency-измений на
    Step 2.
  - **Форма setup:** **декларативная**. Пользователь
    предоставляет JSON-файл product-config'а,
    `bootstrap_product_from_json_file(...)` его читает
    и валидирует. Интерактивный wizard сознательно
    отложен (если потребуется — отдельный шаг **после**
    Step 3).
  - **Транспорт MCP** — **не** решается на Step 2 (этот
    вопрос относится к Step 3 step-map'а). На Step 2
    серверы по-прежнему живут как in-process модули.
- **Что реально появилось в репозитории.**
  - Новое приложение `apps/platform/` со своим
    `README.md`. Содержит src-tree пакета `onec_platform`:
    - `models.py` — dataclass'ы:
      - `ProductConfig` — верхнеуровневый product-конфиг
        (`product_name`, `profile_name`, ссылка на
        `ProjectConfig` из `onec_config`,
        `default_environment`, `servers`, `bootstrap`);
      - `ProductServerToggles` — флаги включения
        `read` / `write` / `intelligence`;
      - `ProductBootstrapSettings` — `work_dir` (опц.) +
        три `require_*` флага (`require_dump_path`,
        `require_base_path`, `require_python`),
        отключение каждого видно как **warning-finding**
        в doctor-отчёте, не молча;
      - `DoctorFinding` — одна находка doctor'а:
        `code`, `severity ∈ {ok, warning, error}`,
        `confidence ∈ {confirmed, presumed}`, `detail`.
        Confirmed/presumed split — та же дисциплина,
        что у Phase 4 intelligence-tools;
      - `DoctorReport` — `findings`, `error_count`,
        `warning_count`, `recommended_actions`;
      - `BootstrapResult` — boundary-результат:
        `ok`, `product_name`, `profile_name`,
        `default_environment`, `doctor`, `message`.
    - `loader.py`:
      - `load_product_config(data: dict) -> ProductConfig`
        — строгая структурная валидация, fail-closed
        через `ValueError`. Делегирует
        `onec_config.load_project_config` для секции
        `project` (никакого дублирования
        `EnvironmentConfig`).
      - `load_product_config_from_json_file(path) ->
        ProductConfig` — чтение JSON-файла + парсинг +
        валидация. Все file-system / JSON-parse ошибки
        конвертируются в `ValueError` для единообразия.
    - `doctor.py`:
      - `run_prereqs_doctor(config) -> DoctorReport` —
        **никогда не бросает**. Проверки:
        1) resolve `default_environment` (defensive);
        2) `base_path` существует
        (skipped с warning-finding'ом, если
        `require_base_path=False`);
        3) `dump_path` существует (аналогично);
        4) `python` на `PATH` через `shutil.which("python")`
        (аналогично);
        5) `http_base_url` парсится в scheme + host —
        **presumed** (реального HTTP-probe нет; это
        Step 4);
        6) для каждого включённого server toggle —
        `importlib.util.find_spec(module_name)`;
        отключённый toggle — warning-finding
        `server_disabled:<name>`, не молчаливый skip;
        7) опциональный `bootstrap.work_dir`
        существует и является директорией.
    - `bootstrap.py`:
      - `bootstrap_product(data) -> BootstrapResult` —
        **boundary-функция, никогда не бросает**.
        Загружает конфиг, гоняет doctor, собирает
        `BootstrapResult` с человекочитаемым `message`.
      - `bootstrap_product_from_json_file(path)` — то
        же, но из JSON-файла.
    - `__init__.py` — публичная поверхность пакета +
      package-level docstring, фиксирующий Phase 5 /
      Step 2 surface и safety-контракт (никаких
      write-операций; никакого старта серверов;
      никакого `onec_policy_engine`-импорта; boundary
      не бросает).
  - `apps/README.md` — обновлён: раздел больше не
    утверждает, что в `apps/` живут только MCP-серверы;
    добавлено описание `platform` как продуктового
    слоя.
  - `scripts/dev/bootstrap_paths.ps1` — добавлен путь
    `apps\platform\src` в `$srcPaths`, чтобы пакет
    `onec_platform` был импортируем во всех скриптах
    проекта. Других изменений в скрипте нет.
- **Чего на Step 2 намеренно ещё нет (зафиксировано в
  README пакета).** MCP-транспорта; `start`/`stop`/
  `status`/`reload` (это Step 3); реального HTTP /
  health probe (это Step 4); реального installer'а
  под ОС; интерактивного wizard'а; реальной
  1cv8-binary интеграции (Step 7); workflow runner'а
  (Step 5); rollback assistant'а (Step 6); запуска
  write-операций — никогда из этого пакета.
- **Safety guarantees Phase 2–4 — что сохраняется.**
  - `mcp-read-server` registry — те же 15 tool'ов, не
    тронут.
  - `mcp-write-server` registry — те же 23 tool'а, не
    тронут. `run_write_flow` остаётся единственным
    путём к mutating операциям.
  - `mcp-intelligence-server` registry — те же 16
    tool'ов, не тронут. Read-only контракт сохранён:
    `onec_policy_engine` не импортируется ни в
    intelligence-server'е, ни в `onec_platform`.
  - `onec-config` — не тронут (используем существующие
    `load_project_config` и `EnvironmentConfig`).
  - `onec-policy-engine` — не тронут и **не**
    импортируется в product layer. Bootstrap — это
    install-readiness, не write-policy-решение.
  - `pyproject.toml`, `.github/`, корневой `README.md`
    (кроме блока «Текущий статус по фазам»),
    `selfcheck.py` — не тронуты.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`bootstrap_product`,
    `bootstrap_product_from_json_file`) **никогда не
    бросают**; на любую проблему отдают
    `BootstrapResult(ok=False, ..., message=...)`.
  - Inner helpers (`load_product_config`,
    `load_product_config_from_json_file`) бросают
    `ValueError` на битый вход — fail-closed, как и
    `onec_config.load_project_config`.
  - `run_prereqs_doctor` тоже никогда не бросает —
    внутренние ошибки оборачиваются как
    `severity="error"` finding.
  - `ok=True` означает «шаг выполнился», не «всё
    здорово». Реальная готовность к запуску — в
    `result.doctor.error_count == 0`.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step2_check.py`
  материализует synthetic temp-директории и JSON-файлы
  через `tempfile.mkdtemp()`. Сценарии:
  - **0. registry invariants** — read=15, write=23,
    intelligence=16 (sanity-check до и после) — без
    изменений.
  - **1. happy path** — валидный config + существующие
    base_path/dump_path + python на PATH + все три
    server-toggle включены → `ok=True`,
    `error_count=0`, `warning_count=0`, 8 ok-findings,
    `confirmed`/`presumed` распределены честно
    (`http_base_url_well_formed` — presumed,
    остальные — confirmed).
  - **2. broken config (3 подсценария).** Отсутствует
    `product_name` → `ok=False` с message содержащим
    имя поля. Root не dict → `ok=False`. Wrong type
    для `servers` → `ok=False`.
  - **3. bad default environment** —
    `default_environment="ghost-env"`, отсутствует в
    `project.environments` → `ok=False`, в message
    перечислены known environments.
  - **4. missing paths** — `base_path` и `dump_path`
    не существуют → `ok=True` (doctor отработал),
    `error_count=2`, findings содержат
    `base_path_missing` и `dump_path_missing` с
    severity=error, recommended_actions содержит
    указания по обоим путям.
  - **5. server toggles** — `intelligence=False` →
    `ok=True`, finding `server_disabled:intelligence`
    severity=warning; ни одного
    `server_module_importable:intelligence` или
    `server_module_missing:intelligence` (отключение
    видно, но importability check не дублируется).
  - **6. JSON file path** —
    `bootstrap_product_from_json_file` на валидный
    JSON-файл → `ok=True`, тот же набор findings, что
    и dict-вход.
  - **7. JSON file errors (3 подсценария).** Файл не
    существует → `ok=False, "not found"`. Файл
    битый JSON → `ok=False, "not valid JSON"`. Путь
    указывает на директорию → `ok=False, "not a
    regular file"`.
  - **8. bootstrap.work_dir variants (3 подсценария).**
    Существующая директория →
    `bootstrap_work_dir_exists` severity=ok.
    Файл (не директория) →
    `bootstrap_work_dir_not_a_dir` severity=error,
    `error_count >= 1`. Несуществующий путь →
    `bootstrap_work_dir_missing` severity=warning.
  - **9. require_python=False** — finding
    `python_check_disabled` severity=warning;
    `python_on_path` / `python_not_on_path` отсутствуют
    (отключение видно, но check не запускается). Это
    проверка дисциплины «никакого silent skipping».
  - **10. malformed http_base_url** —
    `http_base_url="not-a-url"` →
    `http_base_url_malformed` severity=warning,
    confidence=presumed; recommended_actions содержит
    указание исправить URL. Ни одного исключения
    наружу.
- **Dev-check после Step 2 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools`
  = 23 (не тронут), **`intelligence_server_tools` — 16
  tool'ов** (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`. Selfcheck.py
  намеренно не дёргает `onec_platform` — продуктовый
  слой опционален для dev-check'а; интеграция в
  selfcheck (если понадобится) — отдельный шаг после
  Step 3.

### Phase 5 / Step 3 — runtime orchestration / single entry point (завершён)

- **Архитектурная честность Step 3.** Step 3 строит
  **product-level launcher contract**, а не выдумывает MCP
  transport за read/write/intelligence. Сами три сервера
  по-прежнему живут как in-process модули; их встроенный
  CLI / `__main__` / production transport — отдельный
  track, не Step 3. Product layer управляет **только теми
  argv-командами**, которые оператор явно описал в
  `ProductConfig.runtime.services`. Это решение зафиксировано
  и в коде (docstring'и `runtime.py` и `__init__.py`), и в
  README продуктового слоя.
- **`reload` — это controlled stop-then-start, не hot
  reload.** В коде (`reload_product_runtime`) и в README
  явно зафиксировано: PID'ы после reload гарантированно
  новые. Никаких ложных заявлений о zero-downtime поведении.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/process_control.py` —
    cross-platform PID/proc primitives на чистом stdlib.
    POSIX: `os.kill(pid, 0)` для liveness и
    `signal.SIGTERM` для terminate. Windows: `OpenProcess`
    + `WaitForSingleObject` / `TerminateProcess` через
    `ctypes`. На Windows `os.kill(pid, 0)` намеренно
    **не** используется (некоторые сборки CPython при
    `os.kill(pid, sig)` на Windows фактически вызывают
    `TerminateProcess` — это было бы катастрофой для
    liveness-пробы). `spawn_service` детачит stdio в
    `DEVNULL` и стартует ребёнка в своей process group /
    session.
  - `apps/platform/src/onec_platform/state.py` — атомарный
    state-store под `<work_dir>/.runtime/runtime-state.json`.
    Запись через tmp-файл + `os.fsync` + `os.replace`.
    Read fail-closed через `ValueError` на битый JSON и на
    неизвестную `schema_version`. Schema version = 1 на
    Step 3.
  - `apps/platform/src/onec_platform/runtime.py` — четыре
    boundary-функции (`start_product_runtime`,
    `stop_product_runtime`, `get_product_runtime_status`,
    `reload_product_runtime`) + их `_from_json_file`
    варианты. **Никогда не бросают.** Resolve config →
    resolve work_dir → load persisted state → materialize
    services из текущего spec'а (spec — authoritative для
    enabled/configured/command, persisted overlay — для
    pid/status/started_at) → refresh stale PIDs → apply
    `only=…` фильтр → выполнить операцию → атомарно
    сохранить state. `only=` — surgical-фильтр; неизвестное
    имя → warning, не abort.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `ProductServiceSpec`, `ProductRuntimeSettings`,
    `RuntimeServiceState`, `RuntimeStateFile`,
    `RuntimeOperationResult`, `RuntimeStatusResult`;
    `ProductConfig` расширен полем
    `runtime: ProductRuntimeSettings = field(default_factory=...)`,
    что сохраняет полную backward compatibility со Step 2.
    Также добавлены константы `RUNTIME_STATUSES` и
    `RUNTIME_STATE_SCHEMA_VERSION` как единый источник
    правды для тестов / README / runtime-кода.
  - `apps/platform/src/onec_platform/loader.py` — добавлены
    private helper'ы `_parse_runtime` и
    `_parse_service_spec`. `runtime` секция опциональна;
    отсутствие → пустой `ProductRuntimeSettings`.
    Тип-проверки строгие: `command` — non-empty list[str],
    не shell-строка; `working_dir` — string или
    отсутствует; `env_overrides` — dict[str, str].
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 16 новыми
    именами (модели + boundary helpers + `runtime_dir` /
    `state_file_path` для path discovery). package
    docstring переписан под совместное Step 2 + Step 3
    surface с явными honesty-комментариями про MCP
    transport и hot reload.
- **Чего на Step 3 намеренно ещё нет (зафиксировано в
  README пакета).** Production-grade MCP transport внутри
  read/write/intelligence; hot reload (только controlled
  restart); daemon / service manager (нет регистрации
  Windows Service / systemd unit); захват stdout/stderr
  дочерних процессов (DEVNULL — для предсказуемости
  pipe-буфферов); авто-restart упавших сервисов; реального
  HTTP / health probe (Step 4); installer'а под ОС;
  интерактивного wizard'а; реальной 1cv8-binary
  интеграции (Step 7); workflow runner'а (Step 5);
  rollback assistant'а (Step 6); запуска write-операций
  из `onec_platform` (никогда).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`start_product_runtime`,
    `stop_product_runtime`, `get_product_runtime_status`,
    `reload_product_runtime`, плюс `_from_json_file`
    варианты) **никогда не бросают**: на любую проблему
    отдают `RuntimeOperationResult(ok=False, ..., findings=[...])`
    или `RuntimeStatusResult(ok=False, ...)` с
    error-finding'ом.
  - `ok=True` означает «шаг отработал», не «всё в желаемом
    состоянии». Реальный статус сервисов — в
    `result.services[*].status`. Per-service сбои попадают
    в findings по конвенции `<event>:<service>` (например
    `runtime_started:read`, `runtime_command_missing:write`,
    `runtime_pid_stale:read`).
  - Inner helper'ы (`load_product_config`,
    `load_product_config_from_json_file`, `read_state`,
    `write_state`, `spawn_service`) бросают
    `ValueError` / `OSError` fail-closed, но **только
    внутри** — boundary всегда оборачивает.
  - `confirmed`/`presumed` дисциплина из Phase 4 + Step 2
    doctor'а сохранена: каждый finding несёт
    `confidence`, и `is_pid_alive` даёт **confirmed**
    статус, а не presumed (мы реально пробуем системный
    вызов).
- **Safety guarantees Phase 2–4 — что сохраняется.**
  - `mcp-read-server` registry — те же 15 tool'ов, не
    тронут.
  - `mcp-write-server` registry — те же 23 tool'а, не
    тронут. `run_write_flow` остаётся единственным путём
    к mutating операциям. `onec_platform` **не** обходит
    его — он **не вызывает** ни write-tool'ов, ни
    `run_write_flow`, ни audit-API.
  - `mcp-intelligence-server` registry — те же 16 tool'ов,
    не тронут. Read-only контракт сохранён:
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform`.
  - `onec-config`, `onec-policy-engine`, `pyproject.toml`,
    `.github/`, `selfcheck.py`, `bootstrap_paths.ps1` —
    не тронуты на Step 3 (PYTHONPATH `apps\platform\src`
    был добавлен ещё в Step 2).
  - `onec_platform` сам **не выполняет write-операций
    в 1С**. Он управляет PID-ами тех процессов, которые
    оператор описал, и точка. Любая mutating операция
    по-прежнему идёт через write-server и его
    `run_write_flow`.
- **Persisted state file contract.**
  - путь — `<work_dir>/.runtime/runtime-state.json`;
  - `schema_version=1`; неизвестная версия → fail-closed
    через `ValueError`, который boundary оборачивает в
    error-finding `runtime_state_unreadable`;
  - `env_override_keys` — это **ключи** override'ов, не
    значения, чтобы state-файл не утаскивал секреты;
  - запись атомарная (tmp + `os.fsync` + `os.replace`);
  - `.runtime/` — платформенно-владенный подкаталог,
    создаётся автоматически. Сам `work_dir` создаёт
    оператор; платформа его **не** создаёт и **не**
    переиспользует молча.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step3_check.py`
  использует `tempfile.mkdtemp` и **реальные subprocess'ы**
  (`python -c "import time; time.sleep(120)"`) для
  честной проверки PID-liveness. Сценарии: registry
  invariants; happy path start→status→stop с реально
  живыми PID'ами; идемпотентный start (без дубликатов);
  reload даёт новые PID'ы и реально убивает старые;
  `disabled` сервис не стартует; missing command →
  `status=missing`+error finding; stale-PID detection
  (state-файл при этом **не** переписывается);
  bad work_dir в трёх вариантах (None / missing /
  is-file); JSON-file flow эквивалентен dict-flow;
  backward compatibility со Step 2 (config без секции
  `runtime` грузится и работает с warning-finding'ом
  `runtime_contract_empty`); `only=` surgical-фильтр
  с известным и неизвестным именем; битый/отсутствующий
  JSON; битый state-файл (boundary не падает, отдаёт
  finding); финальные registry invariants. Все 13
  сценариев прошли с первой попытки. Каждый спавненный
  subprocess реально reaped через `terminate_pid` до
  завершения скрипта.
- **MVP-компромиссы Step 3 (зафиксированы честно).**
  - **`reload` — controlled stop-then-start.** Не hot
    reload; PID'ы после reload новые. Это в README и в
    коде явно.
  - **Stdio дочерних процессов идёт в `DEVNULL`.**
    Operator должен сам логировать в файл из
    argv-команды. Captured logs с ротацией — possible
    follow-up Step 4 / Step 8.
  - **Нет watch-and-restart.** Если дочерний процесс
    умер вне `stop`, он становится `stale`; чтобы его
    поднять, нужен явный `start`. Auto-restart policy —
    отдельный track.
  - **PID-based supervision, не daemon manager.** Никакой
    регистрации Windows Service / systemd unit на этом
    шаге.
  - **Best-effort `terminate_pid`.** Если SIGTERM /
    `TerminateProcess` вернул ошибку, состояние сервиса
    помечается `error`; следующий `start` всё равно
    спавнит свежий процесс — старый PID может остаться
    жить. Operator handles it. README это фиксирует.
  - **State-файл не переписывается чистым `status`.**
    Stale-detection попадает в результат, но on-disk
    остаётся как есть до следующего `start`/`stop`/`reload`.
    Это намеренное разделение read-only и mutating
    операций.
  - **Команды примера в README** (`python -m
    mcp_read_server` и т.п.) приведены как иллюстрация
    формата. Phase 5 / Step 3 **не утверждает**, что
    у read/write/intelligence уже есть рабочий
    `__main__` / CLI — добавление их остаётся
    follow-up'ом.
- **Dev-check после Step 3 зелёный.** `imports_ok = true`,
  `read_server_tools` = 15 (не тронут), `write_server_tools`
  = 23 (не тронут), **`intelligence_server_tools` — 16**
  (не тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`. Selfcheck.py
  намеренно не дёргает `onec_platform.runtime` — runtime
  ops опциональны для dev-check'а.

### Phase 5 / Step 4 — environment doctor / health dashboard (завершён)

- **Архитектурная честность Step 4.** Step 4 — это
  **product-уровневый aggregation contract**, а не новый
  MCP-сервер и не UI. В пакете `onec_platform` появляется
  одна boundary-функция `build_environment_dashboard(...)`
  (плюс `_from_json_file` вариант), которая собирает в
  один read-only snapshot **уже существующие** сигналы:
  bootstrap doctor (Step 2), runtime status (Step 3),
  `read.check_runtime_health`, `read.diagnose_connectivity_issue`,
  `intelligence.analyze_runtime_issue`,
  `intelligence.summarize_configuration_risk`. Никакой
  новой диагностической логики не изобретается — только
  агрегация.
- **Один источник на секцию.** Фиксированные six sections и
  явные provenance-маркеры:
  - `bootstrap` ← `platform.bootstrap_product`;
  - `runtime` ← `platform.get_product_runtime_status`;
  - `read_health` ← `read.check_runtime_health`;
  - `read_diagnosis` ← `read.diagnose_connectivity_issue`;
  - `intelligence_runtime` ← `intelligence.analyze_runtime_issue`;
  - `intelligence_risk` ← `intelligence.summarize_configuration_risk`.
  `read.health_summary` намеренно **не** включён: это
  легаси-stub helper с булевыми флагами, и его честное
  включение либо дублирует `check_runtime_health`, либо
  даёт ложное «всё ок». Решение явно зафиксировано в
  README продуктового слоя.
- **Verdict — deterministic, hand-written.** Полный
  ruleset документирован в docstring'е `_compute_verdict`
  и в README.
  - **`blocked`** если: bootstrap section ok=False;
    bootstrap doctor имеет error-finding; runtime section
    ok=False; required runtime service в статусе
    `missing` или `error`; read-side health codes содержат
    `dump_missing` или `gateway_down`.
  - **`degraded`** если не blocked, но: runtime service
    в `stale`; read-side health codes содержат любой
    не-ok код вне blocking-списка; bootstrap doctor
    имеет warning; intelligence risk_level
    `medium`/`high`; runtime контракт пуст; любая
    секция помимо уже учтённых отдала ok=False;
    connectivity diagnosis сообщил непустой problem_code.
  - **`healthy`** иначе.
  - `ready_for_workflows = (overall_status == "healthy")`
    — жёсткое правило для Step 5.
- **Required service rule.** Сервис считается обязательным
  для verdict-правил **только** если `enabled=True` и
  `command` непуст. Disabled сервис не валит verdict.
  Сервис без команды → собственный
  `runtime_command_missing:<svc>` finding на runtime-уровне,
  но **не** делает verdict автоматически blocked: оператор
  мог явно решить «этим сервисом я управляю снаружи».
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/dashboard.py` — новая
    boundary + 6 секционных runner'ов + `_compute_verdict`
    + хелперы агрегации/нормализации/тагирования. Cross-app
    импорты идут только в правильном направлении: product
    layer → read, product layer → intelligence. Никакого
    обратного направления.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `DashboardSectionResult`, `DashboardVerdict`,
    `EnvironmentDashboardResult` + константа
    `DASHBOARD_OVERALL_STATUSES`. Step 2/3 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 6 новыми
    именами (3 модели + константа + 2 boundary-функции);
    package docstring обновлён описанием Step 4 surface.
- **Чего на Step 4 намеренно ещё нет (зафиксировано в
  README).** UI / web-dashboard / push subscription;
  кэширования sub-tool вызовов (sub-tools зовутся каждый
  раз, в т.ч. транзитивно — например, `analyze_runtime_issue`
  внутри intelligence-секции сам зовёт
  `check_runtime_health` и `diagnose_connectivity_issue`,
  которые также зовутся read-секцией; это сознательный
  MVP-компромисс ради простоты failure mode); ML-оценок
  риска / здоровья (всё rule-based); собственного
  health-probe внутри dashboard'а (используем уже готовые
  read-tool'ы); Step 5 guided workflows (dashboard их не
  заменяет — он только описывает «что сейчас»).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`build_environment_dashboard`,
    `build_environment_dashboard_from_json_file`)
    **никогда не бросают**.
  - Полный `ok=False` — только когда product config не
    загружается. В остальных случаях — partial dashboard
    with honest degradation: индивидуальный sub-tool сбой
    помечается на уровне секции (`section.ok=False` +
    error-finding в `confirmed_findings` + понятный
    `message`), но dashboard остаётся `ok=True`.
  - Confirmed/presumed дисциплина из Phase 4 + Step 2 не
    размывается. Каждый finding несёт собственный
    `confidence`. На уровне aggregated `confirmed_findings`
    / `presumed_findings` каждый код префиксован именем
    секции (`<section>/<original_code>`) для трассируемой
    provenance.
- **Safety guarantees Phase 2–4 + Step 2/3 — что
  сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform`. Это явно проверено программным
    assert'ом в manual check.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. `onec_platform` его **не
    обходит** и **не вызывает write-tool'ов**.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`, `pyproject.toml`,
    `.github/`, `selfcheck.py`, `bootstrap_paths.ps1` —
    не тронуты на Step 4.
  - Read-server и intelligence-server вызываются через
    публичный Python API их `tools.py` модулей —
    cross-app направление `product layer → read /
    intelligence`, как и было заложено для Phase 5.
- **Ручная проверка (10 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step4_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном порту (`127.0.0.1`)
  для честных read-side вызовов + реальные subprocess'ы
  через Step 3 surface. Сценарии:
  - **0. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. Happy path** — валидный config, существующие
    base/dump, стартованные runtime-сервисы, живой HTTP →
    `ok=True`, `overall_status=healthy`,
    `ready_for_workflows=True`. Все 6 sources_used
    присутствуют и совпадают с ожидаемым множеством.
    Confirmed/presumed split реально присутствует в
    aggregated lists.
  - **B. Bootstrap degraded — base/dump missing** —
    bootstrap doctor находит `base_path_missing` и
    `dump_path_missing` (severity=error) → verdict
    `blocked`, `ready_for_workflows=False`. read-side
    тоже падает с `dump_missing` (так как `dump_path` не
    существует на диске). Dashboard остаётся `ok=True`,
    sections заполнены.
  - **C. Runtime stale** — реально стартуем runtime,
    извне убиваем PIDs (`terminate_pid`), затем
    `build_environment_dashboard`. Runtime section
    показывает services со статусом `stale`, verdict
    `degraded` с warnings `runtime_service_stale:read`
    и `runtime_service_stale:write`.
  - **D. Dead read-side endpoint** — http_url указывает
    на свободный порт без listener'а. read_health
    section ok=False, `gateway_down` в blocking_issues,
    overall_status=blocked. Dashboard сам не падает.
  - **E. Empty runtime contract** — Step 2 config без
    секции `runtime`. Dashboard `ok=True`, verdict
    `degraded` с warning `runtime_contract_empty`. Ни
    одного блокирующего runtime_required_service
    finding'а (потому что нет required services).
  - **F. Bad config JSON (3 sub-сценария).** Malformed
    JSON → `ok=False`, `Product config rejected: ... not
    valid JSON`. Missing file → `ok=False, ... not found`.
    Root not dict → `ok=False, ... must be a dict or a
    pre-loaded ProductConfig`. Никаких исключений
    наружу.
  - **G. Registry invariants (final).** read=15,
    write=23, intelligence=16 — после всех сценариев
    без изменений.
  - **H. Cross-app import contract.** Программный grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**/*.py` и
    `apps/mcp-intelligence-server/src/**/*.py` →
    **0 реальных импортов** (assert).
  - **I. Aggregation provenance.** Программный assert,
    что каждый код в `dash.confirmed_findings +
    dash.presumed_findings` содержит `/` (тег секции).
  - **J. JSON-file flow.** `build_environment_dashboard_from_json_file`
    эквивалентен dict-flow.
  Все 10 сценариев прошли. Каждый спавненный subprocess
  очищен через `terminate_pid` до выхода скрипта; локальный
  HTTPServer останавливается в `finally`-блоке.
- **MVP-компромиссы Step 4 (зафиксированы честно в README).**
  - **Sub-tool вызовы не кэшируются.** В одной dashboard-операции
    `check_runtime_health` и `diagnose_connectivity_issue`
    вызываются дважды — один раз read-секцией,
    второй раз внутри `analyze_runtime_issue` (которая
    сама их вызывает). Это сознательно: shared cache
    усложнил бы failure mode и провенанс.
  - **`health_summary` намеренно не включён.** Это
    легаси-stub helper; его включение либо дублирует
    `check_runtime_health`, либо даёт нечестное «ок».
  - **Connectivity-diagnosis section всегда `ok=True`.**
    Read-side `diagnose_connectivity_issue` сам по себе
    возвращает `ok=False` только при наличии проблемы;
    мы интерпретируем «проблема обнаружена» как
    successful diagnosis run, а не как сбой sub-tool'а.
    Соответствующий warning попадает в presumed_findings
    и в verdict через rule «connectivity_problem:<code>».
  - **`ready_for_workflows = healthy only`.** Это
    жёсткое правило: даже degraded не пускает workflow
    без оператора. Возможный override-флаг — отдельный
    enhancement Step 5.
  - **Подключаем только по умолчанию выбранные sub-tools.**
    `analyze_event_log_patterns` намеренно не включён —
    его включение требовало бы фильтров периода
    (period_start/end), а это уже product-policy решение,
    которое относится скорее к Step 5/6.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`.
  - Никакого UI / web-dashboard.
  - Никакого write-канала из `onec_platform`.
  - Никакого хот-мониторинга / push subscription.
  - Никаких ML-оценок.
  - Никакого Step 5 guided workflow runner.
  - Никаких изменений `selfcheck.py` /
    `bootstrap_paths.ps1` — эти были обновлены ещё в
    Step 2.
- **Dev-check после Step 4 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.dashboard` —
  dashboard опционален для dev-check'а.

### Phase 5 / Step 5 — guided workflow layer (завершён)

- **Архитектурная честность Step 5.** Workflow layer — это
  **product-уровневая оркестрация** уже существующих
  intelligence- и write-surfaces. Никакого собственного
  write channel в `onec_platform` не появилось: каждый
  mutating step идёт через **реальный публичный
  write-tool** (`add_catalog_attribute`,
  `add_document_attribute`, `append_module_method`),
  который сам внутри проходит через `run_write_flow`
  (preflight → backup snapshot → dump snapshot →
  operation → verify → audit). Workflow runner **не
  обходит** ни один из этих шагов.
- **Дисциплина precondition'а.** Mutating workflow'ы
  (`safe-add-attribute`, `safe-add-module-method`)
  стартуют только при выполнении **двух** условий
  одновременно: оператор передал `confirm_execute=True`
  И dashboard.verdict.ready_for_workflows == True. Без
  любого из них workflow возвращает `mode=preview` или
  `mode=blocked`. `stand-health-check` — read-only
  диагностика, она работает даже на degraded/blocked
  окружении (специально вынесено отдельным правилом).
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/workflow.py` — новая
    boundary + три приватных runner'а
    (`_run_safe_add_attribute`, `_run_safe_add_module_method`,
    `_run_stand_health_check`) + helpers для агрегации
    findings, нормализации foreign ToolResult'ов и
    программной фильтрации tool-имён через живые registries.
    Cross-app импорты идут только в правильном
    направлении: product layer → read, product layer →
    intelligence, product layer → write. Никакого
    `onec_policy_engine`-импорта.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `WorkflowStepResult`, `WorkflowPlan`, `WorkflowRunResult`,
    плюс константы `WORKFLOW_NAMES` и `WORKFLOW_MODES`.
    Step 2/3/4 модели не тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 7 новыми
    именами; package docstring расширен описанием
    Step 5 surface.
- **Три текущих workflow.**
  - **`safe-add-attribute`.** Поток: build dashboard →
    verdict gate → intelligence
    (`estimate_change_impact`, `suggest_safe_change_order`,
    `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`) → assemble plan →
    confirm gate → реальный
    `add_catalog_attribute` / `add_document_attribute` →
    `verify_attribute_exists` →
    `describe_last_write_operation` →
    `prepare_rollback_hint`. Поддерживаемые `target_kind`:
    `catalog` и `document`.
  - **`safe-add-module-method`.** Поток: build dashboard →
    verdict gate → intelligence (`estimate_change_impact`,
    `find_affected_modules`, `suggest_safe_change_order`,
    `suggest_metadata_patch_plan`,
    `summarize_configuration_risk`) → assemble plan →
    confirm gate → реальный `append_module_method` →
    `verify_module_contains` →
    `describe_last_write_operation` →
    `prepare_rollback_hint`.
  - **`stand-health-check`.** Read-only diagnostic:
    `build_environment_dashboard` + `analyze_runtime_issue`
    + `summarize_configuration_risk`. **Не требует**
    `ready_for_workflows=True`. Никогда не выполняет
    write-side операций. `mode=diagnostic`.
- **Чего на Step 5 намеренно ещё нет (зафиксировано в
  README пакета).** Реального rollback assistant'а
  (Step 6); UI / web-app поверх workflow runner'а;
  hot reload / hot apply / push subscription;
  собственного write channel в `onec_platform`;
  silent apply; параметризованного
  `prepare_intelligence_report` внутри stand-health-check
  (его контракт требует non-empty subject, которого у
  read-only диагностики нет — добавлять синтетический
  subject было бы нечестно); автоматического retry
  упавших mutating step'ов; параметра override-флага для
  `degraded` dashboard'а (это — возможный enhancement
  более позднего шага, не Step 5).
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`run_guided_workflow`,
    `run_guided_workflow_from_json_file`) **никогда не
    бросают**. Любая непредвиденная ошибка runner'а
    оборачивается в `ok=False`, `mode=rejected`, finding
    `workflow_unexpected_error`.
  - `mode` ∈ `{preview, executed, diagnostic, blocked,
    rejected}` — единый источник правды
    `WORKFLOW_MODES`. `ok` плюс `execution_performed`
    дают честную картину: `executed + ok=False` означает
    «mutating step выполнялся и провалился; план и
    intelligence steps сохранены».
  - При сбое mutating step'а workflow runner **не**
    запускает verify (нечего верифицировать), но всё
    равно подтягивает `describe_last_write_operation`
    как best-effort — `audit/.../audit_describe_last_write_operation`
    может вернуть ok=False, если audit-файла ещё нет;
    это нормально и не флипает overall verdict.
  - `confirmed`/`presumed` дисциплина из Phase 4 + Step 4
    сохраняется. Каждый aggregated finding тагирован
    префиксом step name'а (например
    `intelligence_estimate_change_impact/impact_estimate`)
    для трассируемой провенансы.
- **Real-tool-name discipline.** В `WorkflowPlan`
  `suggested_tools` и `suggested_write_tools` фильтруются
  через приватный `_allow_only_real_tools(...)`, который
  проверяет каждое имя по живому объединению трёх
  registries (`mcp_read_server.list_tools()`,
  `mcp_write_server.list_tools()`,
  `mcp_intelligence_server.list_tools()`) плюс
  фиксированному whitelist платформенных
  boundary-функций. Имена, которых нет в этом множестве,
  молча отбрасываются — план не утверждает наличие
  выдуманных tool'ов. Эта дисциплина программно
  проверяется в manual-check сценарии (`assert_real_tool_names`).
- **Safety guarantees Phase 2–4 + Step 2/3/4 — что
  сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check).
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. `onec_platform` его **не
    обходит** и не вызывает write-tool'ов в обход
    публичных функций. Каждый mutating step workflow'а
    идёт через `add_catalog_attribute` /
    `add_document_attribute` / `append_module_method`,
    которые сами зовут `run_write_flow`.
  - Audit / snapshots / verify не обходятся: mutating
    write-tool'ы выполняют их сами; workflow runner
    только читает результаты через
    `describe_last_write_operation` /
    `prepare_rollback_hint`.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 5**.
- **Ручная проверка (11 сценариев + 5 sub-сценариев K,
  все зелёные).** Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step5_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном `127.0.0.1:<port>`
  для честных read-side вызовов + реальные subprocess'ы
  через Step 3 surface (запускаются при необходимости) +
  реальные write-tool'ы, исполняющиеся против synthetic
  Catalog/Document XML и BSL модулей в tempdir.
  Сценарии:
  - **I. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. preview safe-add-attribute** — `confirm_execute=False`
    → `mode=preview`, `execution_performed=False`,
    plan содержит реальные tool-имена,
    `write_results=[]`, `last_write_operation=None`.
    Программный assert: ни одного `kind="mutating"` /
    `"verify"` / `"audit"` step'а в preview.
  - **B. execute safe-add-attribute** —
    `confirm_execute=True` → `mode=executed`,
    `execution_performed=True`, write_results[0].ok=True,
    verify_results[0].ok=True, last_write_operation
    populated с реальным `operation_id`, rollback_hint
    populated. Файл XML на диске **реально содержит**
    `name="Title"` и `<Type>String</Type>`.
  - **C1+C2. preview + execute safe-add-module-method**
    — модуль на диске реально содержит имя добавленного
    метода (`PrepareReport`); rollback_hint и
    last_write_operation populated.
  - **D. stand-health-check** — `mode=diagnostic`,
    `execution_performed=False`, suggested_write_tools
    пустой, ни одного mutating step'а.
  - **E. blocked by dashboard** — dump_path не
    существует → dashboard блокирует mutating workflow:
    `mode=blocked`, `ok=False`, `execution_performed=False`,
    в steps только precondition. **E2** проверяет, что
    `stand-health-check` всё равно проходит на
    degraded/dead-HTTP окружении — `mode=diagnostic`,
    `execution_performed=False`.
  - **F. confirm missing → preview only** — без
    `confirm_execute` запуск без всяких write-эффектов:
    catalog XML на диске не модифицирован, audit-каталог
    `.audit/` не создан.
  - **G. underlying write failure** — `attribute_spec.type=
    "BogusType"` → write-tool сам fail-closed'ится
    (whitelisted типы только String/Number/Date) →
    `mode=executed`, `execution_performed=True`,
    `ok=False`. Plan и intelligence steps сохранены;
    verify step **не** добавлен (нет смысла верифицировать
    провалившийся write).
  - **H. registry invariants (final)** — read=15,
    write=23, intelligence=16 после всех сценариев.
  - **J. import discipline** — программный grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**/*.py` → **0 реальных импортов**.
  - **K. rejection paths (5 sub-сценариев)** —
    unknown workflow name; invalid params (target_kind
    не "catalog" / "document"); root config not a dict;
    JSON-file flow happy path (`mode=diagnostic`);
    missing JSON file (`mode=rejected`).
  Все assert'ы прошли с первой попытки (после двух
  cosmetic правок: ASCII arrows вместо `→` для cp1251
  console; включение non-empty `runtime.services` в
  тестовом config'е, чтобы dashboard был `healthy`, а
  не `degraded` из-за `runtime_contract_empty`).
- **MVP-компромиссы Step 5 (зафиксированы честно в
  README).**
  - **Mutating workflow'ы требуют `dashboard.verdict.
    overall_status == "healthy"`** (через
    `ready_for_workflows`). Это значит: пустой
    `runtime.services` → degraded → workflow blocked.
    Это **корректное поведение**: оператор должен
    декларировать runtime контракт. Override-флаг для
    `degraded` — отдельный enhancement, не Step 5.
  - **`stand-health-check` не зовёт
    `prepare_intelligence_report`.** Контракт того
    requires non-empty `subject`, которого у read-only
    диагностики стенда нет; добавлять синтетический
    subject было бы нечестно. Соответствующие сигналы
    уже видны через dashboard и через
    `analyze_runtime_issue` / `summarize_configuration_risk`,
    которые workflow вызывает явно.
  - **При сбое mutating step'а verify не запускается.**
    Сознательно: нет смысла верифицировать
    неприменившееся изменение. `audit/...` step'ы
    остаются best-effort и могут вернуть ok=False,
    если audit-файла ещё нет.
  - **Нет автоматического retry.** Сбой → честный
    `ok=False` с сохранённым планом; решение
    «повторить» — за оператором.
  - **`safe-add-module-method` использует имя метода
    как needle в `estimate_change_impact` /
    `find_affected_modules` /
    `summarize_configuration_risk`.** Это намеренно:
    impact для добавления метода — это где этот символ
    сейчас уже встречается в дампе. Если оператор
    добавляет ранее-не-существующее имя, impact будет
    `none` — это и есть честный сигнал.
  - **Workflow runner не делает структурную валидацию
    `attribute_spec.type` отдельно** — это уже
    делает write-tool. Workflow только формирует
    preview, передаёт в write-tool и честно отображает
    его failure (сценарий G).
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`.
  - Никакого собственного write channel в `onec_platform`.
  - Никакого silent apply.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 6 rollback / recovery UX (только
    подтягиваем `describe_last_write_operation` и
    `prepare_rollback_hint` для surface их операторам).
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
- **Dev-check после Step 5 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.workflow` —
  workflow runner опционален для dev-check'а.

### Phase 5 / Step 6 — rollback / recovery / audit UX (завершён)

- **Архитектурная честность Step 6.** Rollback / recovery
  / audit UX — это **read-only product-layer обёртка**
  над уже существующим audit JSONL (write-side append-only
  store) плюс
  `prepare_rollback_hint` /
  `describe_last_write_operation`. Никакого собственного
  write channel в `onec_platform` не появилось: для класса
  операций, у которых **нет** публичного `delete_*`
  write-tool'а (а это сейчас все операции), assistant
  честно отдаёт `mode=unsupported` под `confirm_execute=True`.
  Product layer **не модифицирует** audit JSONL и **не
  переписывает** dump в обход `run_write_flow`.
- **Дисциплина preview / execute.**
  - History viewer и inspect — read-only **всегда**, в
    т.ч. на degraded окружении.
  - Rollback assistant **preview** — read-only всегда; даже
    на degraded окружении preview строится, чтобы оператор
    видел план.
  - Rollback assistant **execution** (`confirm_execute=True`)
    — два независимых gate'а:
    1. Dashboard ready_for_workflows должен быть True;
       иначе → `mode=blocked, ok=False`, preview сохранён.
    2. Tool family должен быть в whitelist
       `_AUTOMATIC_RECOVERY_SUPPORTED`; иначе →
       `mode=unsupported, ok=True`, honest сообщение про
       manual snapshot-restore.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/recovery.py` — новый
    модуль с тремя boundary-функциями + их `_from_json_file`
    вариантами. Внутри: read-only audit-парсер
    (`_read_audit_lines`, `_parse_audit_lines`), фильтрация
    (`_filter_entries`), сводка (`_summarize`), helper
    `_rollback_hint_payload` для безопасного вызова
    write-server `prepare_rollback_hint`, plan builder
    (`_build_rollback_plan`). Cross-app импорты идут только
    в правильном направлении: product → write (read-only
    helpers `prepare_rollback_hint`,
    `describe_last_write_operation`). **Никакого**
    мутирующего write-tool'а recovery не импортирует.
    Дисциплина имён tool'ов делегирована приватной
    `_allow_only_real_tools(...)` из `workflow.py` Step 5
    — единый источник правды.
  - `apps/platform/src/onec_platform/models.py` — добавлены
    `OperationHistoryEntry`, `OperationHistorySummary`,
    `OperationHistoryResult`, `OperationInspectResult`,
    `RollbackPlan`, `RollbackAssistantResult` + константа
    `RECOVERY_MODES = ("preview", "executed", "blocked",
    "unsupported", "rejected")`. Step 2/3/4/5 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 13 новыми
    именами (6 моделей + 1 константа + 6 boundary-функций);
    package docstring расширен описанием Step 6 surface
    с явным указанием на пустой
    `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist.
- **Что Step 6 делает (три boundary-функции).**
  - **`get_operation_history(data, *, limit=None,
    only_status=None)`** — operator-visible audit
    history. Read-only. `ok=True` одинаково покрывает
    «N операций загружено» и «audit файла ещё нет»
    (чистое окружение). Каждая запись normalised в
    `OperationHistoryEntry(position, operation_id,
    tool_name, environment, base_id, status, message,
    raw_line)`. Summary: `total / ok_count / error_count
    / other_count`. Малформированные строки → warning
    findings, не crash.
  - **`inspect_operation(data, *, operation_id)`** —
    focus на одну запись. Подтягивает `prepare_rollback_hint`
    через write-server. Operator summary включает
    `automatic_recovery_supported` явно и snapshot paths.
    Missing operation → `ok=False, operation_found=False`
    (caller ветвится по `operation_found`, не по
    message).
  - **`run_rollback_assistant(data, *, operation_id,
    confirm_execute=False)`** — preview / advisory
    assistant. Mode resolution описан в README продуктового
    слоя; `mode=executed` на Step 6 **недостижим** —
    whitelist пуст.
- **Чего на Step 6 намеренно ещё нет (зафиксировано в
  README пакета).** Автоматического content-level
  rollback'а ни для одного write-tool'а (нет публичных
  `delete_*`); filesystem snapshot-restore тоже **не**
  исполняется автоматически — только surface'ятся
  snapshot-paths и операторские подсказки; модификации
  audit JSONL (он append-only); UI / web frontend / push
  subscription; параллельного writer'а в product layer;
  intelligence-вызовов сверх dashboard'а; CLI / production
  transport у read/write/intelligence; Step 7
  real-stand / 1cv8 integration.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`get_operation_history`,
    `inspect_operation`, `run_rollback_assistant`, плюс
    `_from_json_file` варианты) **никогда не бросают**.
  - `ok=True` covers honest happy paths: history loaded
    (incl. empty), operation inspected, preview built,
    `mode=unsupported` вернулся честно (assistant
    отказался, не упал).
  - `ok=False` reserved for: invalid inputs, missing
    operation_id in audit, unreadable audit file,
    `mode=blocked` (execution requested but environment
    not ready). Boundary-finding всегда несёт `code` +
    `severity` + `confidence`.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4 + 5
    сохранена. Каждый finding несёт собственный
    `confidence`. Малформированные audit lines идут как
    `severity=warning, confidence=confirmed` (мы реально
    видели битую строку в файле).
- **Real-tool-name discipline.** В `RollbackPlan`
  `suggested_tools` и `suggested_write_tools` фильтруются
  через приватный `_allow_only_real_tools(...)` (импортирован
  из Step 5 workflow-слоя — одна точка истины). Имена
  вне registries молча отбрасываются, чтобы план не
  утверждал наличие выдуманных tool'ов. Эта дисциплина
  программно проверяется в manual-check сценариях C, E.
- **Safety guarantees Phase 2–5 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям. Recovery-модуль его **не зовёт**
    и **не обходит**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check, Сценарий M).
  - Audit JSONL — append-only, recovery-модуль только
    читает.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 6**.
- **Ручная проверка (13 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step6_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` на свободном порту для
  honest health probes + **реальные write-tool вызовы**
  через публичный `add_catalog_attribute`, чтобы audit
  JSONL, который читает recovery, был **настоящий**, а
  не hand-crafted. Сценарии:
  - **L. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **A. History viewer happy path с реальными audit
    lines.** Два real-write вызовов
    `add_catalog_attribute` (с distinct snapshot
    label'ами, чтобы избежать collision'ов на уровне
    `_snapshots/backup-…`) → audit JSONL содержит реальные
    JSON-строки. Reading через `get_operation_history` →
    `ok=True`, summary.total>=2, ok_count>=2, оба
    operation_id присутствуют, position монотонна.
  - **N. Filtering** — `only_status="ok"` + `limit=1`
    → ровно 1 запись со status="ok"; `only_status="error"`
    → 0 записей (rejection write3 произошёл pre-flow,
    audit row не появился — это и есть ожидаемое
    поведение).
  - **B. История без audit-файла** — `ok=True, entries=[],
    summary.total=0`, message говорит «empty or absent»
    одинаково.
  - **C. Inspect operation happy path** — найдена запись,
    rollback_hint подтянут, `automatic_recovery_supported=False`,
    operator_summary не пуст, suggested_tools и
    suggested_write_tools проходят real-name assert.
  - **D. Inspect operation: id не в audit log** —
    `ok=False, operation_found=False`. Также: пустой
    `operation_id` → `ok=False, operation_found=False`.
  - **E. Rollback assistant preview** — `mode=preview,
    execution_performed=False, write_results=[],
    plan.automatic_recovery_supported=False`.
    suggested_tools и suggested_write_tools — real names.
  - **F. Confirm missing → preview only** — повторный
    preview-запуск **не модифицирует** ни catalog XML
    на диске, ни audit-файл (длина строк не меняется,
    snapshot файла до и после совпадает).
  - **G. Blocked by dashboard** — `confirm_execute=True`
    + http_url указывает на dead-port → dashboard
    не ready → `mode=blocked, ok=False,
    execution_performed=False`. Preview всё равно
    построен (plan и history_entry присутствуют).
  - **H. Unsupported automatic rollback** —
    `confirm_execute=True` + healthy dashboard + tool
    `add_catalog_attribute` не в whitelist →
    `mode=unsupported, ok=True, execution_performed=False`,
    write_results=[], verify_results=[]. Honest message
    про manual snapshot-restore.
  - **I. Skipped — no executable recovery path** на
    Step 6 (by design).
  - **J. Malformed audit lines** — добавляем в
    реальный audit-файл сначала `{ this is not valid json`,
    потом `"a string, not a dict"`. History viewer
    остаётся `ok=True`, real запись присутствует, две
    warning-finding (`audit_line_invalid_json:1` +
    `audit_line_not_a_dict:2`). Boundary не падает.
  - **K. Suggested-tool discipline** — assert'нуто
    inline в C и E через `assert_real_tool_names(...)`.
  - **M. Import discipline** — программный grep по
    `apps/platform/src/**` + `apps/mcp-intelligence-server/src/**`
    на `^\s*(from|import)\s+onec_policy_engine\b` →
    **0 импортов**.
  - **P. JSON-file flow + rejection paths** —
    `get_operation_history_from_json_file` happy →
    `ok=True`; `inspect_operation_from_json_file` на
    missing JSON → `ok=False`; `run_rollback_assistant`
    на не-dict root → `ok=False, mode=rejected`.
  Все assert'ы прошли (после двух cosmetic правок:
  ASCII arrows вместо `→` для cp1251 console;
  distinct write-tool labels чтобы snapshot
  directory не коллидировал между двумя последовательными
  real-write вызовами).
- **MVP-компромиссы Step 6 (зафиксированы честно в
  README).**
  - **Whitelist `_AUTOMATIC_RECOVERY_SUPPORTED` пуст.**
    Step 6 ship'ит advisory-only. Это **корректное**
    поведение: автоматический content-level rollback без
    публичных `delete_*` write-tool'ов означал бы
    back-door write channel в product layer мимо
    `run_write_flow` / audit / verify. Whitelist
    оставлен в коде как frozenset — будущий шаг
    (или enhancement, когда `delete_*` появятся)
    расширит его без изменения скелета.
  - **Audit JSONL не имеет timestamp'а** — recovery
    использует line-position как стабильный монотонный
    порядок. Это документировано в `OperationHistoryEntry`
    docstring.
  - **Малформированные audit lines пропускаются с
    warning'ом, не abort'ятся.** Operator видит реальные
    записи + честный список «что было пропущено».
  - **Snapshot-restore не автоматизирован.** Suggested
    snapshot paths surface'ятся в plan/operator summary;
    `shutil.copytree`-обратное копирование оператор
    делает сам. Product layer не имеет write channel на
    `dump_path` / `base_path`.
  - **`_allow_only_real_tools` импортирован из
    Step 5 workflow.py** как private symbol. Это
    cross-module import одного помощника между двумя
    sibling-модулями `onec_platform` — не идеальная
    инкапсуляция, но позволяет иметь **один источник
    правды** для tool-name дисциплины. Альтернативы
    (дублирование constants, выделение отдельного
    `_internal.py` module) увеличили бы surface ради
    нулевого product-выигрыша на Step 6.
  - **Connectivity diagnosis / runtime issue / risk
    intelligence** Step 6 берёт через dashboard
    summary, не вызывая sub-tools повторно. Это
    matched сознательное решение Step 4 — sub-tool
    dedup не реализован.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-config`, `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`.
  - Никакого собственного write channel в `onec_platform`.
  - Никакого автоматического content-level rollback.
  - Никакого автоматического snapshot-restore.
  - Никакой модификации audit JSONL.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 7 real-stand / 1cv8 integration.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
- **Dev-check после Step 6 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.recovery` —
  recovery опционален для dev-check'а.

### Phase 5 / Step 7 — real-stand / 1cv8 binary integration track (завершён)

- **Архитектурная честность Step 7.** Step 7 — это
  **product-layer контракт** для реальной 1cv8 binary
  интеграции и **первый controlled smoke test**, не
  подмена Phase 2 stub'ов и не «полная интеграция за один
  шаг». Phase 2 write-tools (`create_dump_snapshot`,
  `apply_config_from_files`,
  `update_database_configuration`) на Step 7 **не**
  переписываются — флипать их на binary-backed branch
  это параллельный track, не scope этого шага.
- **Дисциплина preview / execute.**
  - Readiness boundary — read-only **всегда**.
  - Smoke test **preview** — read-only всегда; даже на
    not-ready конфиге preview строится.
  - Smoke test **execute** (`confirm_execute=True`) —
    два независимых gate'а:
    1. Readiness verdict должен быть `ready_for_real_stand_smoke=True`;
       иначе → `mode=blocked, ok=False`, plan и steps
       сохранены.
    2. Если readiness ready → execute mode **всегда**
       делает filesystem probe (stat) и **дополнительно**
       стартует subprocess через
       `onec_process_runner.run_process` тогда и только
       тогда, когда оператор задал
       `onec_binary_probe_args`. Платформа не подсказывает
       значения этих аргументов и не «угадывает» 1cv8
       CLI: оператор знает свой стенд.
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` расширен двумя опциональными
    полями: `onec_binary_path: str | None = None` и
    `onec_binary_probe_args: list[str] | None = None`.
    Default `None` → полная backward compatibility.
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` парсит обе опциональные строки/
    списки с строгой типовой проверкой: bad shape →
    `ValueError` fail-closed (Сценарий Q manual check'а).
  - `packages/onec-config/README.md` — оба новых поля
    задокументированы.
  - `apps/platform/src/onec_platform/realstand.py` —
    новый модуль с двумя boundary-функциями + их
    `_from_json_file` вариантами + private helper'ами:
    `_inspect_binary` (filesystem-only), `_excerpt`
    (truncate output), `_build_plan_summary`,
    `_readiness_to_step`, `_dashboard_step`. Cross-app
    импорты идут только в правильном направлении:
    product → onec-config, product → onec-process-runner,
    product → дашборд / workflow Step 4/5. **Никакого**
    мутирующего write-tool'а recovery не импортирует.
    `onec_policy_engine` не импортируется.
    `_allow_only_real_tools` импортируется из
    `workflow.py` Step 5 — единая точка истины для
    tool-name дисциплины.
  - `apps/platform/src/onec_platform/models.py` —
    добавлены `RealStandReadinessResult`,
    `RealStandSmokeResult` + константа
    `REAL_STAND_SMOKE_MODES = ("preview", "executed",
    "blocked", "rejected")`. Step 2/3/4/5/6 модели не
    тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 7 новыми
    именами (2 модели + 1 константа + 4 boundary-функции);
    package docstring расширен Step 7 surface description
    с явным указанием что Phase 2 stub'ы не
    переписываются.
- **Что Step 7 делает (две boundary-функции).**
  - **`get_real_stand_readiness(data)`** — read-only
    doctor. Проверяет:
    1. `onec_binary_path` declared (не `None`);
    2. файл существует;
    3. это файл, не директория;
    4. на POSIX — есть хоть один executable bit; на
       Windows — любой regular file принимается;
    5. `base_path` существует;
    6. `dump_path` существует;
    7. dashboard verdict не `blocked`.
    Возвращает `ready_for_real_stand_smoke: bool` как
    единый AND-вердикт. Confirmed/presumed findings
    разделены. `presumed_findings` несёт honest signals
    (degraded dashboard, отсутствующие probe args).
  - **`run_real_stand_smoke_test(data, *, confirm_execute=False)`**
    — preview / executed / blocked / rejected. В
    `mode=executed` всегда делает filesystem probe;
    дополнительно стартует subprocess через
    `onec_process_runner.run_process(ProcessRunRequest(...))`
    с timeout 30s и captured output (excerpts cap 1024
    chars). `binary_invoked` — отдельный флаг,
    отличающий «metadata-only execute» от «real subprocess
    execute»: `execution_performed=True, binary_invoked=False`
    означает «filesystem probe прошёл, но probe args не
    заданы — subprocess не стартовал».
- **Уровень реальности на Step 7.** Уровень **2** по
  градации задания: ship'ится **partial binary-backed
  integration**. Real-stand readiness + filesystem probe
  + controlled subprocess invocation (когда operator
  declared) — это настоящие, проверяемые, не-fake
  binary-backed шаги. Phase 2 stub'ы (`create_dump_snapshot`,
  `apply_config_from_files`, `update_database_configuration`)
  на Step 7 **не** переписываются. Полный
  DESIGNER → BackupCfg → DumpCfg → ENTERPRISE round-trip
  **не** реализован — это требует реальной инфобазы и
  больше operator-контракта, чем Step 7 готов ship'ить
  честно.
- **Чего на Step 7 намеренно ещё нет (зафиксировано в
  README пакета).** Перевода Phase 2 stub'ов на
  binary-backed dispatch (параллельный track);
  валидации 1cv8-CLI семантики (operator-driven);
  открытия 1С GUI; full DESIGNER → DumpCfg → ENTERPRISE
  round-trip против реальной инфобазы; новых MCP
  tool'ов в read/write/intelligence; CLI / production
  transport у трёх MCP-серверов; UI / web frontend;
  Step 8 final integration pass.
- **Failure-style — единая дисциплина.**
  - Boundary helpers (`get_real_stand_readiness`,
    `run_real_stand_smoke_test` + `_from_json_file`
    варианты) **никогда не бросают**.
  - `ok=True` covers honest happy paths: readiness
    reported (даже когда `ready=False`), preview built,
    metadata-only executed (без subprocess), real
    subprocess завершился с exit_code=0.
  - `ok=False` reserved for: invalid input / unloadable
    config (`mode=rejected`); execute-mode blocked by
    readiness gate (`mode=blocked`); execute-mode когда
    subprocess вернул non-zero exit или filesystem probe
    провалился (`mode=executed, ok=False`).
  - `ProcessExecutionError` от `onec-process-runner`
    (binary не запустился) обработана внутри: попадает
    в step result + finding, не пробрасывается.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4 +
    5 + 6 сохранена. Каждый finding несёт собственный
    `confidence`. POSIX executable-bit check — confirmed
    fact. Probe-args absence — presumed warning (это
    operator choice, не блокер).
- **Real-tool-name discipline.** В readiness и smoke
  результатах `suggested_tools` и
  `suggested_write_tools` фильтруются через приватный
  `_allow_only_real_tools(...)` (импортирован из Step 5
  workflow-слоя — одна точка истины). Имена вне
  registries молча отбрасываются. На Step 7
  `suggested_write_tools` ограничен read-side audit
  surface'ами (`describe_last_write_operation`,
  `prepare_rollback_hint`) — никаких mutating write-tool
  имён в плане realstand'а нет, потому что real-stand
  smoke сам по себе не делает mutating операций.
- **Safety guarantees Phase 2–6 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям в инфобазе. Real-stand boundary
    его **не зовёт** и **не обходит**. Subprocess
    invocation в smoke test'е — это вызов
    operator-declared binary с operator-declared argv,
    вне infobase write surface полностью.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём, ни в
    `onec_platform` (программный grep + assert в manual
    check, Сценарий L).
  - `onec-config` — расширен **минимально и backward-compat**
    (две опциональные строки/списка); `selfcheck.py`
    не тронут (он строит env через kwargs которые
    остаются валидными).
  - `onec-policy-engine`, `onec-audit`, `onec-health`,
    `onec-process-runner` (используется как public API,
    без изменений), `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1` — **не тронуты на Step 7**.
- **Ручная проверка (16 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\platform_step7_check.py`
  использует `tempfile.mkdtemp` + локальный
  `http.server.HTTPServer` для honest read-side health
  + **`sys.executable` как реальный binary** —
  `python.exe` стал operator-declared `onec_binary_path`,
  а `onec_binary_probe_args=["--version"]` дал
  предсказуемый subprocess. Это честно: реальный binary,
  реальный subprocess, реальный exit code. Сценарии:
  - **K. Registry invariants (sanity)** — read=15,
    write=23, intelligence=16; assert.
  - **M. Backward compat** — продакт-конфиг **без**
    `onec_binary_*` грузится и проходит bootstrap;
    `EnvironmentConfig.onec_binary_path` /
    `onec_binary_probe_args` имеют дефолт `None`.
  - **A. Readiness happy path** — binary configured +
    probe args set + healthy dashboard → `ready=True`.
    Все 4 ok-finding'а present (binary_path_exists,
    binary_probe_args_configured, base_path_exists,
    dump_path_exists, dashboard_healthy).
  - **B. Readiness failure: binary missing** — путь
    указывает на несуществующий файл → `ready=False`,
    `binary_path_missing` error finding,
    recommended_actions не пуст.
  - **B'. Readiness failure: not configured** —
    `onec_binary_path=None` → `ready=False`,
    `binary_path_not_configured` error finding.
  - **C. Readiness failure: dir** — путь указывает на
    директорию → `ready=False, binary_present=True,
    executable_like=False, binary_path_is_directory`.
  - **D. Smoke preview on ready config** —
    `mode=preview, execution_performed=False, binary_invoked=False`.
    Plan summary не пуст. Ни одного `executed` step'а в
    preview.
  - **E. Smoke preview on not-ready config** — preview
    всё равно строится; `ready=False`,
    `execution_performed=False`, никаких subprocess.
  - **F. Confirm missing → preview only**.
  - **G. Blocked by readiness** — `confirm_execute=True`
    + binary missing → `mode=blocked, ok=False,
    execution_performed=False, binary_invoked=False`.
  - **H. Confirmed execution metadata-only** — ready +
    no probe args → `mode=executed,
    execution_performed=True, binary_invoked=False`.
    Filesystem probe step ok=True. Subprocess не
    стартовал.
  - **I. Confirmed execution: real subprocess** —
    `[sys.executable, "--version"]` через
    `onec_process_runner` → `mode=executed, ok=True,
    execution_performed=True, binary_invoked=True,
    binary_exit_code=0`. `binary_stdout_excerpt`
    содержит "Python 3.14.4\n". binary_probe step
    ok=True. **Это настоящий subprocess invocation, не
    fake.**
  - **J. Underlying binary failure** —
    `[sys.executable, "-c", "import sys; sys.exit(7)"]`
    → `mode=executed, ok=False, binary_invoked=True,
    binary_exit_code=7`. Plan и steps preserved;
    binary_probe step ok=False.
  - **L. Import discipline** — grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` + `apps/mcp-intelligence-server/src/**`
    → **0 импортов** ✓.
  - **P. JSON-file flow + rejection paths** —
    `get_real_stand_readiness_from_json_file` happy →
    `ok=True, ready=True`;
    `run_real_stand_smoke_test_from_json_file` preview →
    `mode=preview`; missing JSON → `ok=False`;
    non-dict root → `ok=False, mode=rejected`.
  - **Q. Shape validation** — bad
    `onec_binary_probe_args` (`[42, "ok"]`) → loader
    рейзит `ValueError` с конкретным указанием на
    `onec_binary_probe_args` и тип `int`.
  Все assert'ы прошли с первой попытки.
- **MVP-компромиссы Step 7 (зафиксированы честно в
  README).**
  - **Phase 2 stub'ы (`create_dump_snapshot`,
    `apply_config_from_files`,
    `update_database_configuration`) не переписаны.**
    Их evolution на binary-backed dispatch с
    `onec_binary_path` — параллельный track, не Step 7.
    Это сознательный compromise: Step 7 ship'ит
    **product-layer контракт + smoke test**, а не
    одновременно invasive write-tool refactor.
  - **Платформа не валидирует семантику
    `onec_binary_probe_args`.** Operator owns the
    choice. Если probe args открывают GUI или
    блокируют — таймаут 30s принудительно завершит
    subprocess, но платформа не пытается «угадать»
    safe args для произвольной версии 1cv8.
  - **На Windows executable-bit check не делается.**
    Windows не экспонирует POSIX-биты; любой regular
    file принимается. На POSIX отсутствие executable
    bit'а даёт warning, не blocking-error (operator
    может намеренно использовать interpreter-style
    binary).
  - **Smoke test ловит только один subprocess
    invocation.** Multi-step smoke (DESIGNER → DumpCfg
    → ENTERPRISE) требует state-machine и реальной
    инфобазы; это out-of-scope.
  - **Output excerpts cap 1024 chars.** Полные логи —
    operator's responsibility (через свой observability
    стек). Платформа не транслирует arbitrary subprocess
    output upstream.
  - **Timeout 30s — fixed**, не настраивается из
    config. Если operator'у нужен другой таймаут — это
    enhancement future-step'а; на Step 7 фиксированный
    cap честнее, чем шириной surface ради «гибкости».
  - **`_allow_only_real_tools` импортирован из Step 5
    `workflow.py`** как private symbol — sibling-модули
    `onec_platform` шарят один источник правды для
    tool-name дисциплины. Та же oversight, что и в
    Step 6: продолжаем тот же compromise, не вводя
    новый `_internal.py` ради нулевого выигрыша.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `onec_policy_engine`,
    `onec-audit`, `onec-health`, `onec-troubleshooting`,
    `mcp-common`. `onec-config` расширен **минимально**
    (две опциональные строки/списка), backward-compat
    полная.
  - Никакого собственного write channel в `onec_platform`.
  - Никакой записи в инфобазу из realstand boundary.
  - Никакого UI / web-dashboard / push subscription.
  - Никакого Step 8 final integration pass.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`.
  - Не переписаны Phase 2 stub'ы (`create_dump_snapshot`
    / `apply_config_from_files` /
    `update_database_configuration`). Это
    **сознательное** out-of-scope, явно зафиксированное
    в README + plan_summary каждого smoke test'а.
- **Dev-check после Step 7 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  **`intelligence_server_tools` — 16** (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.realstand` —
  realstand опционален для dev-check'а.

### Phase 5 / Step 8 — final integration pass (завершён, Phase 5 закрыт)

- **Step 8 — закрывающий, документационный по сути шаг.**
  Сквозной интеграционный прогон прошёл **без правок
  кода** в репозитории: всё, что собиралось на Step 2–7,
  реально склеилось в один продуктовый контур поверх
  существующих read/write/intelligence-серверов.
  Кодовых изменений на Step 8 нет; обновлены только
  `apps/platform/README.md`, корневой `README.md`,
  `PROJECT-STATUS.md`.
- **Что подтвердил интеграционный прогон.** Один
  сквозной Scenario A на временном synthetic-окружении
  (`tempfile.mkdtemp` + локальный in-process
  `http.server.HTTPServer` + реальные subprocess'ы для
  runtime-сервисов и real-stand smoke probe). Реальный
  стенд **не трогался**.
  - **A.1 `bootstrap_product`** → `ok=True`,
    `doctor.error_count=0`.
  - **A.2 `start_product_runtime`** → 3 сервиса реально
    стартовали (`running × 3`), PID'ы реально живые
    (`is_pid_alive` проверен). `get_product_runtime_status`
    отдаёт `running × 3`.
  - **A.3 `build_environment_dashboard`** (Step 4
    boundary) → 6 секций, verdict `healthy`,
    `ready_for_workflows=True`.
  - **A.4 `run_guided_workflow safe-add-attribute`
    `confirm_execute=True`** → реально дописал атрибут
    `Title` в `Catalogs/Items.xml` через **существующий**
    public write-tool `add_catalog_attribute`, который
    сам прошёл через `run_write_flow` (preflight →
    snapshot → operation → verify → audit).
    `verify_attribute_exists` подтвердил наличие на
    диске. `last_write_operation` и `rollback_hint`
    populated.
  - **A.5 `get_operation_history`** → видит реальную
    audit запись с тем же `operation_id`.
  - **A.6 `inspect_operation`** → `operation_found=True`,
    rollback hint приложен, `automatic_recovery_supported=False`
    (Step 6 advisory-only).
  - **A.7 `run_rollback_assistant`** preview → `mode=preview`,
    `execution_performed=False`, никаких write-эффектов.
  - **A.8 `get_real_stand_readiness`** →
    `ready_for_real_stand_smoke=True`,
    `binary_present=True`, `has_probe_args=True`.
  - **A.9 `run_real_stand_smoke_test`
    `confirm_execute=True`** → **реальный** subprocess
    через `onec_process_runner.run_process` запустился
    (`binary_invoked=True, binary_exit_code=0`,
    stdout содержит `Python`).
  - **A.10 `stop_product_runtime`** → все три PID'а
    реально мертвы.
- **Failure paths (4 сценария, все зелёные).**
  - **F1 — workflow blocked by dashboard.** `dump_path`
    отсутствует → `mode=blocked, ok=False,
    execution_performed=False`. Ни одного `mutating /
    verify / audit` step'а в steps.
  - **F2 — rollback assistant unsupported.**
    `confirm_execute=True` на здоровом окружении →
    `mode=unsupported, ok=True,
    execution_performed=False`,
    `automatic_recovery_supported=False`. Catalog XML
    после попытки **не изменился** (программный
    assert на содержимое файла до и после).
  - **F3 — broken JSON config.** Все 9
    `_from_json_file` boundary-функций (`bootstrap`,
    `start`, `dashboard`, `workflow`, `history`,
    `inspect`, `rollback`, `readiness`, `smoke`)
    одинаково отдают `ok=False`. Никаких исключений
    наружу.
  - **F4 — malformed audit line.** В реальный audit
    JSONL дописали `{ this is not valid json` и
    `"a string, not a dict"`; history viewer остаётся
    `ok=True`, реальная запись присутствует, malformed
    строки попадают в `findings` как warnings
    (`audit_line_invalid_json:*`,
    `audit_line_not_a_dict:*`). Boundary не упал.
- **Discipline asserts (программно подтверждены).**
  - **Registry invariants:** `read=15`, `write=23`,
    `intelligence=16` до и после интеграционного
    прогона.
  - **Real-tool-name discipline:** все имена в
    `suggested_tools` / `suggested_write_tools`
    workflow plan, inspect result, rollback plan,
    readiness, smoke result — реальные имена, живущие
    в одном из трёх registries или whitelist'е
    product-layer boundary-функций. Программные
    `assert_only_real_tool_names(...)` для каждого
    payload'а.
  - **Import discipline:** grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` и
    `apps/mcp-intelligence-server/src/**` — **0
    реальных импортов** (assert).
  - **No exception leakage:** boundary-функции
    product layer ни в одном из 14+ под-сценариев не
    выбросили исключение наружу.
- **Что Step 8 не делал (намеренно).**
  - **Не правил код.** Интеграционный прогон прошёл
    out-of-the-box; кодовые изменения не потребовались.
  - **Не расширял scope.** Никаких новых MCP tool'ов,
    никаких новых модулей, никаких изменений в
    registries трёх MCP-серверов.
  - **Не переписывал Phase 2 stub'ы.** Step 7 уже
    зафиксировал текущий уровень реальности; Step 8 —
    интеграция, не новый binary track.
  - **Не вводил новый write channel в `onec_platform`.**
    Все mutating-эффекты по-прежнему идут через
    публичные write-tool'ы → `run_write_flow`.
  - **Не «полировал» документацию ради красоты.**
    Обновлены только три файла (`apps/platform/README.md`,
    корневой `README.md`, `PROJECT-STATUS.md`), и
    только по сути: маркировка Phase 5 как закрытой,
    Step 8 record, явный список оставшихся
    стратегических хвостов.
- **Safety guarantees Phase 2–7 — что сохраняется.**
  - Read=15, write=23, intelligence=16 — без изменений.
  - `run_write_flow` остаётся единственным путём к
    mutating операциям в инфобазе.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в
    intelligence-server, ни в product layer (программно
    проверено grep'ом).
  - Audit JSONL append-only; product layer его только
    читает.
  - Никакого silent apply, никакого обхода snapshots /
    verify / audit.
- **Dev-check после Step 8 зелёный.** `imports_ok=true`,
  `read_server_tools` = 15, `write_server_tools` = 23,
  `intelligence_server_tools` = 16, `selfcheck_status=ok`,
  `Dev check completed successfully.`.

## Phase 5 закрыт

Phase 5 / Product Layer **закрыт** на Step 8 final
integration pass.

В составе закрытой фазы:

- **Step 1** — planning Product Layer (документационный
  вход).
- **Step 2** — installer / bootstrap contract:
  product-config schema, JSON loader, prereqs doctor,
  bootstrap entrypoint.
- **Step 3** — runtime orchestration / single entry
  point: декларативный runtime-контракт, атомарный
  state-файл, cross-platform PID-liveness, четыре
  boundary-функции (`start_product_runtime` /
  `stop_product_runtime` / `get_product_runtime_status` /
  `reload_product_runtime`).
- **Step 4** — environment doctor / health dashboard:
  единый read-only aggregator над bootstrap +
  runtime + read.check_runtime_health +
  read.diagnose_connectivity_issue +
  intelligence.analyze_runtime_issue +
  intelligence.summarize_configuration_risk;
  rule-based verdict (`healthy` / `degraded` /
  `blocked`) + `ready_for_workflows`.
- **Step 5** — guided workflow layer: три
  end-to-end workflow'а (`safe-add-attribute`,
  `safe-add-module-method`, `stand-health-check`) с
  обязательным confirm gate, mutating-исполнение
  через существующие public write-tool'ы → `run_write_flow`.
- **Step 6** — rollback / recovery / audit UX: три
  boundary-функции (`get_operation_history`,
  `inspect_operation`, `run_rollback_assistant`),
  preview / advisory by default, **advisory-only**
  для всех current write-tool families
  (`_AUTOMATIC_RECOVERY_SUPPORTED` whitelist пуст:
  нет публичных `delete_*` write-tool'ов).
- **Step 7** — real-stand / 1cv8 binary integration
  track: optional contract в `onec-config`
  (`onec_binary_path`, `onec_binary_probe_args`),
  readiness boundary + smoke test boundary с
  **реальным** controlled subprocess через
  `onec_process_runner`. Phase 2 stub'ы не
  переписываются — это параллельный track.
- **Step 8** — final integration pass: один
  сквозной Scenario A + 4 failure paths, без
  правок кода.

**Закрытие Phase 5 не означает**, что продукт уже
полностью industrial-grade / enterprise-ready. Это
означает, что у платформы теперь есть цельный
**product-layer контур** поверх существующих
read/write/intelligence-серверов, с честно
зафиксированными границами и безопасными
гарантиями.

### Phase 6 / Step 1 — planning Industrialization & Completion Track (завершён)

- **Стратегический сдвиг.** После закрытых Phase 1–5
  у платформы есть полное инженерное ядро (read/
  write/intelligence) и работающий product-layer
  контур (bootstrap, runtime, dashboard, workflows,
  recovery, real-stand smoke). Это **не** ещё
  финальный индустриальный продукт. Phase 6 —
  специально выделенная фаза доведения продукта до
  finished / deployable состояния, а не очередное
  расширение MCP tool surface. Это закрытие
  разрыва между «у нас сильное ядро + работающий
  product-layer контур» и «это можно установить,
  запустить, использовать, поддерживать и передать
  другому человеку как реальный индустриальный
  продукт».
- **Создано два новых документа в
  `docs/architecture/`.**
  - `docs/architecture/phase-6-industrialization-plan.md`
    — основной план фазы. Содержит: назначение
    фазы (почему после закрытых Phase 1–5 нужна
    именно отдельная фаза industrialization /
    completion); целевой результат в терминах
    finished product behavior на reference stand'е
    (8-пунктовый нарратив от release artifact до
    operator handoff); прямой mapping 10
    стратегических разрывов на блоки фазы (что
    закрывается полностью, что частично, что
    сознательно выносится за пределы); сравнение
    Phase 6 с Phase 1–5 (адресат — человек +
    reference stand, фокус — завершённость, не
    surface expansion); шесть продуктовых блоков
    (A — real 1cv8 execution; B — full rollback /
    recovery; C — installer / packaging; D —
    metadata completion / structural editing; E —
    runtime hardening; F — operator UX / docs;
    G — enterprise foundation); guardrails;
    явный «что НЕ входит в фазу»; **10**
    проверяемых критериев приёмки; раздел
    открытых вопросов для Step 2+.
  - `docs/architecture/phase-6-step-map.md` —
    стартовая карта фазы из 8 шагов в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат): Step 1 — planning; Step 2 — real
    1cv8 execution contract; Step 3 — installer /
    packaging / setup fast path; Step 4 — rollback
    execution track; Step 5 — metadata completion
    / structural editing; Step 6 — runtime
    hardening / supervision / logs; Step 7 —
    real-stand end-to-end validation + docs /
    runbooks; Step 8 — final integration pass и
    закрытие Phase 6.
- **Ключевые продуктовые блоки, зафиксированные в
  плане (A–G).**
  - **A. Real 1cv8-backed execution track.** Замена
    одного Phase 2 stub-backed пути
    (`create_dump_snapshot` /
    `apply_config_from_files` /
    `update_database_configuration`) на реальный
    binary-backed dispatch через `onec_binary_path`
    + `onec-process-runner`. Stub-режим остаётся
    как honest fallback. **Полное замещение всех
    stub'ов в одной фазе не обещается** — это
    parallel track после Phase 6.
  - **B. Full rollback / recovery track.**
    Перевод rollback assistant из advisory-only в
    реально исполнимый хотя бы для одного класса
    write-tool'ов. `_AUTOMATIC_RECOVERY_SUPPORTED`
    whitelist пополняется хотя бы одним именем.
    Mutating recovery — через существующую
    write-дисциплину или её честное эволюционное
    расширение, без back-door channel'а.
  - **C. Installer / packaging / operator startup
    polish.** Документированный install runbook ≤
    5 ручных шагов; declarative product-config
    template; release artifact format фиксируется
    в Step 3.
  - **D. Metadata completion / structural editing
    track.** Точечный добор metadata coverage и
    первый шаг к настоящему structural editing
    (один whitelisted DOM-edit для XML-блока).
    Полный AST остаётся out of scope.
  - **E. Runtime hardening / process supervision.**
    Лог-capture с ротацией для дочерних сервисов
    (вместо текущего `DEVNULL`); базовая restart
    policy (operator-driven, не automatic
    supervisor); более внятный runtime UX. Hot
    reload остаётся out of scope.
  - **F. Operator UX / docs / runbooks.** Standalone
    `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, user-facing
    message style guide, runbooks для типовых
    сценариев — **вне README**, пригодные для
    передачи другому инженеру.
  - **G. Enterprise / production hardening
    foundation.** Только foundation: declarative
    policy surface поверх существующего
    `onec-policy-engine`, audit retention policy,
    deployment discipline. **Полная
    enterprise-вселенная** (SSO/RBAC, multi-tenant,
    secrets vault, federated audit, policy-as-code
    DSL, multi-instance HA) — out of Phase 6.
- **Какие стратегические разрывы закрывает
  Phase 6.** Полностью закрываются: разрыв (2)
  installer/setup, (7) operator/admin/developer
  UX уровня «можно отдать другому человеку»,
  (10) «всё это поверх готового ядра, не ломая
  его» (фиксируется как guardrail). Частично
  закрываются: (1) реальная 1cv8 binary
  integration — **один** stub-backed путь
  переводится; (3) полная rollback / recovery —
  **один** класс становится исполнимым; (4) full
  metadata coverage — точечный добор; (5) full
  XML/BSL structural editing — первый шаг,
  не AST-парсер; (6) stable real-stand
  end-to-end — один сценарий проходит на
  reference stand'е; (8) runtime hardening —
  логи + базовая restart policy. Сознательно
  выносится за пределы: (9) полный enterprise
  super-set — отдельный enterprise track после
  Phase 6.
- **Guardrails Phase 6 (зафиксированы в плане).**
  Никакого размывания safety guarantees Phase 2–5;
  никакого back-door write channel в product
  layer; mutating путь только через существующую
  write-дисциплину или её честное эволюционное
  расширение; intelligence остаётся read-only;
  `onec_policy_engine` не импортируется ни в
  intelligence, ни в product layer; fail-closed
  по умолчанию; никакой фальшивой
  enterprise-ready риторики; честно отделять
  finished product behavior от parallel
  follow-up / enterprise track; dev-check
  зелёный после каждого кодового шага; registry
  трёх MCP-серверов меняется только при реальной
  необходимости (Step 4 / Step 5 могут добавить
  один-два новых write-tool'а — это документируется
  честно).
- **Что не входит в Phase 6 (зафиксировано
  явно).** Полный enterprise super-set; полностью
  автономный агент; полный AST-парсер XML / BSL;
  web-UI / dashboard frontend; полная замена всех
  Phase 2 stub'ов одновременно; полная
  rollback-вселенная для всех write-tool family'й;
  полное metadata coverage; production MCP
  transport / `__main__` / CLI у трёх серверов;
  hot reload без рестарта; OS-level service
  supervision (Windows Service / systemd unit);
  GUI installer / wizard; многосторонний
  end-to-end на матрице 1С версий и стендов.
- **10 проверяемых критериев приёмки Phase 6.**
  (1) Один Phase 2 stub-backed путь имеет
  binary-backed dispatch при наличии
  `onec_binary_path`; явный маркер `mode` в
  payload. (2) `_AUTOMATIC_RECOVERY_SUPPORTED`
  whitelist содержит ≥ 1 имя; `confirm_execute=True`
  достигает `mode=executed`; verify проверен;
  audit row написан. (3) Install runbook ≤ 5
  ручных шагов от «получил релиз» до «bootstrap
  doctor зелёный». (4) Один end-to-end real-stand
  сценарий проходит от setup до smoke с реальной
  binary-backed apply. (5) Standalone
  operator/admin/developer manuals + runbooks
  существуют **вне** README. (6) read=15+ /
  write=23+ / intelligence=16 (intelligence —
  hard guarantee). (7) dev-check зелёный после
  каждого кодового шага. (8) Safety guarantees
  Phase 2–5 сохранены (программный grep). (9)
  Honest fallback дисциплина: никакого silent
  skip / fake success. (10) Документированные
  ограничения честны: каждый шаг явно указывает,
  что parallel-track'ом, какие MVP-компромиссы.
- **Что изменилось в коде Step 1.** **Ничего.**
  Ни одной строчки. `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `.github/`,
  `.claude.json` — не тронуты. Registry'ы read
  (15), write (23), intelligence (16) не
  менялись. Dev-check остаётся в том же зелёном
  состоянии, что и после Phase 5 / Step 8.
- **Обновлены документы.**
  - Корневой `README.md`: Phase 5 остаётся в
    блоке закрытых фаз; Phase 6 помечена как
    активная фаза с подробным описанием цели
    (Industrialization & Completion Track,
    шесть блоков A–G, 10 критериев приёмки,
    явное «не очередное расширение MCP tool
    surface»); добавлены ссылки на оба новых
    документа (`phase-6-industrialization-plan.md`,
    `phase-6-step-map.md`); абзац про Phase 6 в
    блоке «Текущий статус по фазам» явно
    подчёркивает, что закрытие Phase 6 не
    означает полностью industrial-grade /
    enterprise-ready состояние.
  - `PROJECT-STATUS.md`: обновлены шапка
    (текущий шаг → Phase 6 / Step 1, статус →
    in progress); Step 8 Phase 5 остаётся
    помеченным как «завершён, Phase 5 закрыт»;
    добавлен подробный Step 1 record (этот
    блок); обновлена секция «Следующий шаг» под
    Phase 6 / Step 2; в нижних «Крупные этапы»
    Phase 6 → «Активная фаза».
- **Открытые вопросы Step 1 (для Step 2+).** В
  плане явно зафиксированы вопросы, на которые
  Step 1 не даёт окончательного ответа: какой
  Phase 2 stub-backed путь переводится первым;
  контракт 1cv8 CLI (режимы / args / timeout);
  формат релизного артефакта (zip / tar / wheel
  / git tag / standalone-script); какой класс
  recovery ship'ится первым; какие
  metadata-tool'ы добавляются (или ни одного);
  формат лог-файлов runtime services; уровень
  structural editing в block D; глубина
  enterprise foundation в block G. Step 1 не
  делает вид, что ответы уже найдены.

### Phase 6 / Step 2 — contract for real 1cv8 execution / config surface (завершён)

- **Архитектурное решение Step 2.** Из трёх кандидатов
  (`create_dump_snapshot` / `apply_config_from_files` /
  `update_database_configuration`) первым переведён на
  binary-backed dispatch именно **`create_dump_snapshot`**.
  Причины: он наиболее изолирован (создаёт каталог под
  `_snapshots`, не правит сам dump / infobase); его
  поведение естественно связано со snapshot discipline;
  он менее опасен, чем сразу лезть в apply / update-db.
  `apply_config_from_files` и `update_database_configuration`
  на Step 2 **не** тронуты — это будут отдельные шаги
  Phase 6 / parallel track'и после.
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` расширен одним опциональным полем
    `onec_dumpcfg_command_template: list[str] | None = None`.
    Default `None`. Полная backward compatibility.
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` парсит новое поле с **строгой
    типовой валидацией**: bad shape (не list / non-string
    item / пустой list) → `ValueError` fail-closed на
    этапе загрузки.
  - `packages/onec-config/README.md` — задокументировано
    новое поле + добавлена секция «Философия
    binary-related полей» (operator-owned execution
    contract; платформа не угадывает 1cv8 CLI grammar;
    fail-closed на любую ошибку в этих полях).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`:
    - добавлены константы:
      - `_DUMPCFG_TEMPLATE_PLACEHOLDERS = frozenset({
        "binary_path", "output_path", "base_path",
        "base_id", "publication_name", "http_base_url"})`;
      - `_DUMPCFG_OUTPUT_EXCERPT_LIMIT = 1024`;
      - `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS = 300` (cap
        выше Phase 5 / Step 7 30s, потому что real
        DumpCfg может идти заметно дольше).
    - private helper'ы:
      - `_render_dumpcfg_command(template, *,
        environment, binary_path, output_path)` —
        безопасный per-item `str.format_map`-style
        рендер. Через `_PlaceholderProxy`-dict с
        `__missing__`, который рейзит
        `_UnknownPlaceholderError` для unknown
        placeholder'ов. Boundary конвертит это в
        `ValueError` с понятным сообщением и списком
        allowed placeholders.
      - `_excerpt(text)` — обрезает stdout/stderr до
        cap'а с маркером `...[truncated]`.
    - private dispatch helper'ы:
      - `_create_dump_snapshot_stub(...)` — оригинальный
        Phase 2 / Step 5 путь (marker file +
        dump-meta.json), payload теперь несёт явный
        `mode = "stub"`, `binary_invoked = False`;
      - `_create_dump_snapshot_binary_backed(...)` —
        новый путь: рендер argv → run_process с
        timeout 300s → captured exit_code +
        stdout/stderr excerpts → запись
        `dump-meta.json` с `mode = "binary-backed"` +
        `command_preview`.
    - public `create_dump_snapshot(environment, label)`
      превратилась в тонкий dispatcher:
      preflight → resolve target_dir → if (
      `environment.onec_binary_path` AND
      `environment.onec_dumpcfg_command_template`)
      → binary-backed branch; иначе → stub branch.
      Внешний контракт `ToolResult` сохранён.
  - `apps/mcp-write-server/README.md` — обновлён раздел
    `create_dump_snapshot`: оба режима задокументированы
    с явным указанием, что между ними есть **только
    config-time fallback** (одно из полей отсутствует
    → stub); **runtime fallback запрещён** (если
    binary-backed subprocess вернул non-zero,
    `ok=False`, никакого silent перезапуска). Также
    явно зафиксировано, что `apply_config_from_files`
    и `update_database_configuration` на Step 2 **не**
    тронуты.
  - Корневой `README.md` — Phase 6 абзац дополнен
    кратким описанием Step 2 (новый partial slice,
    operator-owned argv template, whitelisted
    placeholders, fixed timeout 300s, no
    runtime-fallback).
- **Расширение payload (внешний контракт сохранён).**
  `ToolResult` shape не менялся, но `payload.data` теперь
  всегда несёт:
  - `mode: "stub" | "binary-backed"`;
  - `binary_invoked: bool`;
  - `snapshot_path` (как и раньше);
  - в binary-backed режиме дополнительно:
    `exit_code`, `completed`, `command_preview`
    (рендерённый argv), `stdout_excerpt`,
    `stderr_excerpt`.
  Excerpts cap 1024 chars: операторские полные логи
  остаются ответственностью самого operator'а через его
  observability стек.
- **Дисциплина fallback'а.**
  - **Config-time fallback:** если хотя бы одно из
    полей (`onec_binary_path`,
    `onec_dumpcfg_command_template`) не задано —
    stub mode. Это **сохраняет полную backward
    compatibility** с Phase 1–5: все существующие
    конфиги, не объявляющие новые поля, работают
    как и раньше.
  - **Runtime-fallback запрещён.** Если operator
    объявил binary-backed контракт и subprocess
    завершился non-zero (или не стартовал) — `ok=False`,
    `mode="binary-backed"`, никакого silent перезапуска
    stub'а. Это явная требование задания Step 2 и
    зафиксировано в коде / README.
  - **Render fail-closed.** Unknown placeholder в
    template → `ok=False`, `binary_invoked=False`,
    subprocess не стартует, message включает список
    allowed placeholders.
- **Safety guarantees Phase 2–5 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственной точкой входа
    к mutating операциям. `create_dump_snapshot` —
    обычный public write-tool группы A; mutating
    write-tool'ы группы B автоматически наследуют
    binary-backed snapshot stage через свой штатный
    `run_write_flow` (это подтверждено integration
    smoke сценарием F: `update_module_code` через
    flow реально использовал binary-backed branch и
    flow завершился `stage=completed`).
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` в продуктовом слое и
    intelligence-server по-прежнему не импортируется.
  - Никакого собственного write channel вне
    write-server'а.
  - Никакой `shell=True` — argv list only через
    `onec_process_runner.run_process`.
  - Никакого 1cv8-CLI guessing: render placeholder'ов
    жёстко whitelisted; argv item'ы — operator
    declaration as-is; платформа не добавляет
    «полезных» дефолтов.
  - `selfcheck.py` не тронут.
  - `apps/`, `scripts/`, `pyproject.toml`, `.github/`,
    `apps/mcp-read-server/**`,
    `apps/mcp-intelligence-server/**`,
    `apps/platform/**` — **не трогали** (только
    `apps/mcp-write-server/{tools.py,README.md}` +
    `packages/onec-config/{models.py,loader.py,README.md}`
    + `README.md` + `PROJECT-STATUS.md`).
- **Ручная проверка (7 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase6_step2_check.py`
  использует `tempfile.mkdtemp` + локальный in-process
  HTTP server + **`sys.executable` как реальный
  binary** с argv `python -c "..."`. Сценарии:
  - **A. Backward compat** — конфиг без
    `onec_dumpcfg_command_template` → `mode="stub"`,
    `ok=True`, `binary_invoked=False`. Marker
    `dump-created.txt` создан как раньше.
  - **B. Happy binary-backed path** — argv template:
    `[{binary_path}, "-c", "...write binary-marker.txt
    inside {output_path}...", {output_path},
    {base_id}]` → `ok=True, mode="binary-backed",
    binary_invoked=True, exit_code=0`. Файл
    `binary-marker.txt` реально создан subprocess'ом
    внутри snapshot-каталога. `dump-meta.json`
    помечен `mode="binary-backed"`. `command_preview`
    содержит реальный путь к python.exe и
    подставленные `{output_path}` / `{base_id}`.
    `stdout_excerpt = "snapshot for local-dev\n"`.
  - **C. Binary-backed runtime failure** — argv
    `[{binary_path}, "-c", "import sys;
    sys.exit(7)", {output_path}]` → `ok=False,
    mode="binary-backed", binary_invoked=True,
    exit_code=7`. **No fallback to stub**: внутри
    snapshot-каталога **нет** `dump-created.txt` и
    **нет** `dump-meta.json` (stub-marker'ы не
    создаются после binary-backed failure).
  - **D. Bad template shape rejected by loader** —
    три sub-сценария: `"string-not-a-list"` →
    `ValueError "must be a list of strings"`;
    `[42, "ok"]` → `ValueError "must contain only
    strings; got int"`; `[]` → `ValueError "must not
    be empty"`. Все fail-closed на этапе loader'а.
  - **E. Unknown placeholder** —
    `[{binary_path}, "-c", "print('hi')",
    {not_a_real_placeholder}]` → `ok=False,
    binary_invoked=False`. Subprocess не стартовал.
    Message: `Unknown placeholder
    {not_a_real_placeholder} in
    onec_dumpcfg_command_template; allowed
    placeholders are: ['base_id', 'base_path',
    'binary_path', 'http_base_url', 'output_path',
    'publication_name']`. Внутри snapshot-каталога —
    никаких marker'ов.
  - **F. Integration smoke через `run_write_flow`** —
    `update_module_code(env, "CommonModules/Helpers
    /Ext/Module.bsl", new_text=...)` с
    binary-backed конфигом. Результат:
    `ok=True`, `tool_name="update_module_code"`
    (tool_name discipline preserved),
    `flow_data.stage="completed"`. Snapshot
    каталог `_snapshots/dump-local-dev-*` реально
    содержит `flow-marker.txt` (= proof, что
    binary-backed branch ran inside the flow);
    **отсутствует** `dump-created.txt` (= proof,
    что stub branch не использовался). Audit row
    `tool_name="update_module_code", status="ok"`
    написан в `dump/.audit/audit.jsonl`.
  - **G. Registry invariants** до и после: read=15,
    write=23, intelligence=16. assert.
- **MVP-компромиссы Step 2 (зафиксированы честно).**
  - **Только один stub переведён.**
    `create_dump_snapshot` — единственный путь, который
    Step 2 переводит на binary-backed dispatch.
    `apply_config_from_files` /
    `update_database_configuration` остаются как
    stub'ы; их перевод — отдельные будущие шаги
    Phase 6 (или parallel-track после), как явно
    задокументировано в README write-server'а.
  - **Литеральные `{`/`}` в operator argv не
    поддерживаются.** `str.format_map`-style рендер
    не позволяет легко передать литеральные
    фигурные скобки в значения; на MVP-уровне это
    приемлемо, потому что 1cv8 в документированных
    DumpCfg-флагах их не использует. Если когда-нибудь
    оператору это понадобится — он pre-render'ит
    argv сам перед декларацией. Зафиксировано в
    docstring'е `_render_dumpcfg_command`.
  - **Timeout фиксированный 300 секунд.** Не
    конфигурируется на Step 2 — это простой honest
    cap для MVP. Possible enhancement: вынести в
    config (`onec_dumpcfg_timeout_seconds`) когда
    появятся реальные стенды с понятным SLA.
  - **`command_preview` — раскрытый argv.** В нём
    видны все placeholder'ные значения после
    подстановки (например, путь к base_path).
    Operator должен помнить: если он положил в
    base_path / dump_path что-то секретное, оно
    окажется в payload'е. На Step 2 это
    accept-as-is; secrets vault — отдельный
    enterprise track.
  - **Excerpts cap 1024 chars.** Полные subprocess
    логи — operator's responsibility (его
    observability stack), как и в Phase 5 / Step 7.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `apply_config_from_files` /
    `update_database_configuration` — это будут
    отдельные шаги Phase 6 (или parallel track после).
  - Никаких изменений `apps/mcp-read-server/**`,
    `apps/mcp-intelligence-server/**`,
    `apps/platform/**`, `scripts/**`, `.github/**`,
    `pyproject.toml`, `.claude.json`.
  - Никакого `shell=True`, никакого 1cv8-CLI
    guessing.
  - Никакого silent runtime fallback с binary-backed
    в stub.
  - Никакого product-layer write channel.
- **Dev-check после Step 2 зелёный.**
  `imports_ok = true`, `read_server_tools` = 15
  (не тронут), `write_server_tools` = 23 (не
  тронут), `intelligence_server_tools` = 16 (не
  тронут), `selfcheck_status = ok`,
  `Dev check completed successfully.`.

### Phase 6 / Step 3 — installer / packaging / setup fast path (завершён)

- **Архитектурное решение Step 3.** Это **fast path**,
  не настоящий industrial installer. Step 3 не делает
  GUI installer, MSI/deb, packaging ecosystem,
  release-artifact-builder, signed binary distribution —
  всё это явно out-of-scope. Сделан минимальный,
  честный, проверяемый product-level install/setup
  contract поверх уже существующего `apps/platform`,
  без изменений MCP server registries и без write
  channel.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/templates.py` —
    новый модуль с одной boundary-функцией:
    - `build_product_config_template(*, product_name,
      profile_name, default_environment, base_path,
      dump_path, http_base_url, ...optional...)` →
      `ProductConfigTemplateResult`. Возвращает
      JSON-serialisable dict, не пишет на диск. Bad
      input → `ok=False` с `template_input_rejected`
      finding (boundary не бросает наружу). Внутренняя
      валидация через приватные `_require_non_empty_str`
      / `_require_int_or_float` /
      `_validate_optional_str_list` /
      `_validate_optional_str` помощников; они
      рейзят `ValueError`, который boundary
      перехватывает.
    - Опциональные binary-related поля
      (`onec_binary_path`,
      `onec_binary_probe_args`,
      `onec_dumpcfg_command_template`) emit'ятся в
      template только когда заданы; absent fields
      просто опускаются — это matched contract'у
      loader'а, который их трактует как optional.
    - Если `work_dir` не указан или binary-backed
      путь не сконфигурирован — добавляются
      **presumed warnings** (не блокирующие):
      `template_work_dir_absent` /
      `template_binary_backed_inactive`.
  - `apps/platform/src/onec_platform/installer.py` —
    новый модуль с тремя boundary-функциями:
    - `inspect_release_layout(root_path)` — read-only
      проверка top-level entries
      (`apps/`, `packages/`, `docs/`, `README.md`,
      `PROJECT-STATUS.md`). `ok=True` даже когда
      какие-то entries отсутствуют (это honest
      finding, не boundary failure). `ok=False`
      только когда сам root path не существует или
      не директория.
    - `run_install_fast_path(data, *,
      output_config_path, confirm_write=False)` —
      главный Step 3 boundary. Поток:
      load_product_config → inspect_release_layout (на
      ближайшем существующем ancestor'е
      `output_config_path`) → bootstrap_product
      (pre-write) → projection в
      JSON-serialisable dict → confirm gate. На
      `confirm_write=False` (default) → `mode="preview"`,
      ничего на диск. На `confirm_write=True` +
      target свободен → атомарная запись (`*.tmp`
      + `Path.replace`), затем
      `bootstrap_product_from_json_file` round-trip
      → `mode="executed"`. На existing target →
      `mode="rejected"` без silent overwrite.
    - `run_install_fast_path_from_json_file(path, *,
      output_config_path, confirm_write=False)` —
      JSON-входной вариант. На missing / malformed
      JSON → `mode="rejected", ok=False`, без
      исключения наружу.
    - `_write_product_config_template(...)` — private
      helper для атомарной записи; сам по себе тоже
      не бросает (возвращает `(bool, error_str|None)`).
      Создаёт parent директорию (часть «уменьшения
      ритуала» — operator не делает `mkdir -p`
      руками).
    - `_infer_layout_root(output_path)` — выбирает
      ближайшего существующего предка
      `output_config_path` для layout inspection,
      чтобы fast path терпимо работал даже когда
      operator показывает на ещё не существующую
      директорию.
  - `apps/platform/src/onec_platform/models.py` —
    добавлены `ProductConfigTemplateResult`,
    `ReleaseLayoutReport`, `InstallFastPathResult`,
    плюс константа `INSTALL_MODES = ("preview",
    "executed", "rejected")`. Step 5/6/7-модели и
    Phase 5 модели не тронуты.
  - `apps/platform/src/onec_platform/__init__.py` —
    публичная поверхность пакета расширена 8
    новыми именами (4 модели + 1 константа + 3
    boundary-функции + `build_product_config_template`).
- **Дисциплина installer'а.**
  - **Никакого silent overwrite.** Existing
    `output_config_path` → `mode="rejected"` с
    finding'ом `output_config_path_exists`. Operator
    выбирает другой путь или удаляет существующий
    файл руками.
  - **Атомарная запись.** Через `<file>.tmp` +
    `Path.replace`. Никакого «полу-записанного»
    config'а на диске даже при сбое.
  - **Создание parent-директории — да** (часть
    сокращения ритуала). Создаются только директории,
    ведущие к `output_config_path`; никаких записей
    вне этого пути.
  - **Round-trip подтверждение.** После записи
    `bootstrap_product_from_json_file` повторно
    читает JSON и прогоняет doctor — это honest
    проверка, что записанный файл валиден как
    product-config.
  - **Никакого запуска runtime / workflows /
    write-tool'ов.** Helper не зовёт
    `start_product_runtime`, `run_guided_workflow`,
    любые MCP write-tool'ы или `onec-process-runner`.
    Запуск runtime — отдельный шаг оператора через
    уже существующие boundary-функции.
  - **Никакого shell.** Никаких `subprocess(shell=True)`,
    никаких CLI-команд из installer helper'а.
- **Короткий install runbook (≤ 5 ручных шагов,
  закрывает критерий приёмки 3 Phase 6).**
  1. Получить релиз (clone репозитория или скачать
     архив).
  2. Запустить `scripts/dev/bootstrap_paths.ps1`
     (PYTHONPATH в текущей PowerShell-сессии).
  3. Подготовить минимальный input dict.
  4. Вызвать `run_install_fast_path(input_dict,
     output_config_path=..., confirm_write=True)`.
  5. После `mode="executed"` запустить runtime /
     dashboard / workflow / real-stand smoke как
     отдельные шаги через существующие
     boundary-функции.
  Это документировано в `apps/platform/README.md`
  как раздел «Короткий install runbook».
- **Чего на Step 3 намеренно ещё нет (зафиксировано
  в README).** GUI installer; release packaging
  ecosystem (`.msi`/`.deb`/`.dmg`/wheel/PyPI release
  artefact); запуск MCP-серверов из helper'а;
  изменения инфобазы; silent overwrite; подмена
  Step 2 binary integration; format релизного
  артефакта как formal contract (Step 1 plan-level
  question); signed binary distribution; multi-version
  release matrix; auto-launcher; setup-wizard.
- **Failure-style — единая дисциплина.**
  - Boundary-функции (`inspect_release_layout`,
    `run_install_fast_path`,
    `run_install_fast_path_from_json_file`,
    `build_product_config_template`) **никогда не
    бросают**.
  - `ok=True` covers honest happy paths: layout
    inspected; preview built; executed write +
    round-trip; template assembled.
  - `ok=False` reserved for: invalid input config,
    layout cannot be inspected (root absent / not
    a dir), existing target file (refusal to
    overwrite), I/O write error, malformed JSON
    input.
  - Confirmed/presumed дисциплина из Phase 4 + Step 4
    + 5 + 6 + 7 сохранена. Каждый finding несёт
    собственный `confidence`. Layout-inspection
    findings — confirmed (мы реально проверили
    наличие entry); template warnings (отсутствие
    work_dir / binary-backed контракта) — presumed.
- **Safety guarantees Phase 2–6 — что сохраняется.**
  - `mcp-read-server` (15), `mcp-write-server` (23),
    `mcp-intelligence-server` (16) — registry **не
    тронуты**.
  - `run_write_flow` остаётся единственной точкой
    входа к mutating операциям. Installer helper его
    **не зовёт** и **не обходит**.
  - Read-only контракт intelligence-server'а сохранён.
    `onec_policy_engine` не импортируется ни в нём,
    ни в `onec_platform` (программный grep + assert
    в manual check, Сценарий L).
  - Никакого собственного write channel в `onec_platform`
    к инфобазе. Запись на диск ограничена единственным
    target-файлом (operator-указанный
    `output_config_path`) и его parent-директорией.
  - `onec-config`, `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `pyproject.toml`, `.github/`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `apps/mcp-read-server/**`,
    `apps/mcp-write-server/**`,
    `apps/mcp-intelligence-server/**`, `scripts/**`,
    `.claude.json` — **не тронуты на Step 3**.
- **Ручная проверка (12 сценариев, все зелёные).**
  Временный скрипт
  `C:\Users\user\AppData\Local\Temp\phase6_step3_check.py`
  использует `tempfile.mkdtemp` + synthetic
  release-like директории + synthetic input
  product-configs. Сценарии:
  - **K (start). Registry invariants** — read=15,
    write=23, intelligence=16; assert.
  - **A. inspect_release_layout happy path** —
    synthetic release с пятью expected entries →
    `ok=True, missing_entries==[]`, у каждого
    entry есть `release_entry_present:*` finding.
  - **A'. inspect_release_layout с partial layout** —
    только `README.md` → `ok=True`, остальные в
    `missing_entries`; присутствующий помечен
    confirmed-ok-finding'ом.
  - **B. inspect_release_layout: non-existent root**
    → `ok=False`, `release_root_missing` finding.
  - **C. inspect_release_layout: root-is-file** →
    `ok=False`, `release_root_not_directory` finding.
  - **D. run_install_fast_path preview** —
    `confirm_write=False`. `mode="preview", ok=True,
    config_written=False`. `output_config_path` **не
    существует** на диске после вызова.
    `template_preview` populated и round-trip'ится
    через `load_project_config`. `bootstrap_pre.ok=True,
    bootstrap_post=None`.
  - **E. run_install_fast_path executed** —
    `confirm_write=True`. `mode="executed", ok=True,
    config_written=True`. JSON реально записан;
    содержит ожидаемые поля. `bootstrap_post.ok=True`
    (round-trip подтверждён).
  - **F. overwrite refusal** — повторный вызов с
    `confirm_write=True` на тот же путь →
    `mode="rejected", ok=False`. Существующий файл
    **на диске не изменился** (assert на
    содержимое до и после).
  - **G. broken input config** — dict без
    обязательных ключей → `mode="rejected", ok=False`,
    output_path **не создан**. Также проверен
    non-dict input (`["not", "a", "dict"]`) → тот же
    `mode="rejected"`.
  - **H. JSON-file flow happy** — записать input
    config как JSON, вызвать `_from_json_file` с
    `confirm_write=True` → `mode="executed", ok=True`.
  - **I. JSON-file flow missing / broken** —
    несуществующий path → `mode="rejected", ok=False`;
    битый JSON → то же. Никаких исключений наружу.
  - **J. build_product_config_template** — happy
    path даёт template, который round-trip'ится
    через `load_product_config`. Bad input
    (empty `product_name`) → `ok=False, template={}`,
    finding `template_input_rejected`. Boundary не
    бросает.
  - **L. Import discipline** — grep
    `^\s*(from|import)\s+onec_policy_engine\b` по
    `apps/platform/src/**` +
    `apps/mcp-intelligence-server/src/**` →
    **0 импортов** ✓.
  - **K (final). Registry invariants** — read=15,
    write=23, intelligence=16 после всех сценариев.
  Все assert'ы прошли с первой попытки.
- **MVP-компромиссы Step 3 (зафиксированы честно в
  README).**
  - **Layout inspection — только top-level.** Не
    walk'ит subtrees, не открывает файлы, не
    проверяет содержимое. Operator видит, что
    `apps/` есть; что внутри — отдельный шаг.
  - **Release artifact format не зафиксирован.**
    Phase 6 Step 1 plan ставил это как open
    question; Step 3 ship'ит fast path над
    «оператор клонировал репо или распаковал
    архив», не выбирает между zip/tar/wheel/git
    tag formal contract'ом. Это enhancement
    дальнейших шагов Phase 6.
  - **Helper не делает atomic install/upgrade
    sequencing.** Если operator уже что-то
    запустил, helper просто не перезаписывает
    config; full upgrade choreography (stop runtime
    → re-write config → start runtime) — это
    operator-driven последовательность, не один
    boundary call.
  - **Шаблон не валидирует cross-field
    consistency.** Например, не проверяет, что
    `base_path` существует на диске — это
    компетенция bootstrap doctor'а (вызывается
    после записи). Template builder honest о том,
    что он только собирает dict.
  - **Создание parent-директории.** Это
    deliberate compromise в пользу UX: operator
    не должен делать `mkdir -p` руками. Никаких
    других директорий вне parent path не
    создаётся.
- **Что не сделано намеренно.**
  - Никаких новых MCP tool'ов в read/write/intelligence.
  - Никаких изменений registry трёх MCP-серверов.
  - Никаких изменений `apply_config_from_files` /
    `update_database_configuration` (это
    parallel-track, не Step 3).
  - Никаких изменений
    `apps/mcp-read-server/**`,
    `apps/mcp-write-server/**`,
    `apps/mcp-intelligence-server/**`,
    `packages/**`, `scripts/**`, `.github/**`,
    `pyproject.toml`, `.claude.json`.
  - Никакого собственного write channel в `onec_platform`
    к инфобазе.
  - Никакого silent overwrite.
  - Никакого GUI / MSI / deb / wheel / PyPI release
    artifact builder'а.
  - Никакого MCP transport / `__main__` / CLI у
    серверов; никакого hot reload; никакого
    auto-launcher'а.
  - Никаких setup-wizard'ов или интерактивных
    диалогов.
  - Никаких изменений `selfcheck.py`,
    `bootstrap_paths.ps1`.
- **Dev-check после Step 3 зелёный.** `imports_ok =
  true`, `read_server_tools` = 15 (не тронут),
  `write_server_tools` = 23 (не тронут),
  `intelligence_server_tools` = 16 (не тронут),
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает `onec_platform.installer` —
  installer helper опционален для dev-check'а.

### Phase 6 / Step 4 — rollback execution track (завершён)

- **Архитектурное решение Step 4.** Это **первый
  honestly-executable rollback** для **минимально
  узкой** полосы write-tool'ов: только
  `add_catalog_attribute` и `add_document_attribute`,
  то есть mutating-операции над **одним** XML-card
  файлом, чьё содержимое полностью описывается этим
  файлом и обратимо ровно копированием
  snapshot-копии этого файла. Step 4 не делает
  full rollback-универсум для всех write-tool family'й
  (это parallel track после Phase 6) и не вводит
  публичные `delete_*` write-tool'ы (это требует
  отдельного решения по семантике удаления в 1С).
  Остальные mutating-инструменты остаются
  advisory-only — продуктовый recovery-ассистент
  показывает snapshot hints, но автоматически
  откатить отказывается.
- **Что реально появилось в коде.**
  - `packages/onec-audit/src/onec_audit/models.py` —
    `AuditRecord` получил optional `details: dict |
    None = None`. Field положен **в конец** dataclass'а,
    после старых полей; backward-compat для
    keyword-конструкторов сохранён.
  - `packages/onec-audit/src/onec_audit/writer.py` —
    `format_audit_record` теперь явно `pop`'ает ключ
    `"details"` из serialised JSON, когда он `None`.
    Это даёт байт-идентичные строки с pre-Step-4
    форматом — старые лог-файлы не «портятся»
    добавлением `"details": null`. Когда `details`
    — dict (даже пустой), он сохраняется как есть.
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py` —
    `_MUTATING_OPERATIONS` пополнен одним именем:
    `restore_dump_file_from_snapshot`. Решение
    `allowed_mutating` / `require_snapshots=True` —
    тот же путь, что у `update_module_code` и
    остальных Phase 2 mutating-tool'ов.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py` —
    добавлена ровно одна новая public-tool:
    - **`restore_dump_file_from_snapshot(environment,
      relative_path, snapshot_file_path,
      label="restore-dump-file")`**. Mutating, идёт
      через `run_write_flow(...)`. Контракт:
      - `relative_path` — non-empty string без
        leading/trailing whitespace; абсолютные пути
        и `..` сегменты отвергаются fail-closed
        **до** preflight'а;
      - `snapshot_file_path` — обязан указывать на
        existing regular file; non-existent /
        non-regular → `ok=False`;
      - parent-directories целевого файла создаются
        по необходимости (только в пределах
        dump-дерева; containment check через
        `Path.relative_to` гарантирует это);
      - in-flow `verify` сравнивает содержимое
        живого target-файла с snapshot-файлом
        byte-for-byte;
      - запись делается atomically: `*.tmp` рядом с
        целевым файлом + `Path.replace`. На failure
        в середине промежуточный частичный файл не
        остаётся внутри dump-дерева.
  - `apps/mcp-write-server/src/mcp_write_server/server.py` —
    регистрация нового tool'а в `REGISTERED_TOOLS`.
    Алфавитный `list_tools()` теперь возвращает 24
    имени (был 23). Read-server (15) и
    intelligence-server (16) **не тронуты**.
  - `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py` —
    `_append_audit` принимает новый optional
    keyword-arg `details: dict | None = None` и
    передаёт его в `AuditRecord(...)`. Step 6 success-path
    `run_write_flow` теперь собирает structured
    `success_details = {"operation_name",
    "rollback_supported", опционально
    "backup_snapshot_path", "dump_snapshot_path",
    "relative_path"}`. Поле `rollback_supported` —
    bool, `True` ровно когда `operation_name` в
    приватной frozenset'е
    `_ROLLBACK_SUPPORTED_OPERATIONS = {
    "add_catalog_attribute",
    "add_document_attribute"}`. Это **зеркало**
    whitelist'а из `onec_platform.recovery`; держится
    вручную в синхроне (для Step 4 — две позиции).
    Pre-Step-4 audit-строки приобретают `details`
    автоматически на следующих write'ах; readers
    видят либо новый dict, либо отсутствие ключа —
    обе формы валидны.
  - `apps/platform/src/onec_platform/recovery.py` —
    `_AUTOMATIC_RECOVERY_SUPPORTED` переехал из
    пустого frozenset'а в frozenset из ровно двух
    имён: `{"add_catalog_attribute",
    "add_document_attribute"}`. Добавлены приватные
    `_entry_details(entry)` (читает `details` из raw
    audit line; pre-Step-4 строка → `None` без
    raise) и `_details_indicate_rollback_supported(
    entry, details)` (тройной AND: tool в
    whitelist'е, details есть, в details
    `dump_snapshot_path` и `relative_path` —
    непустые строки). Любой из трёх отсутствующих
    факторов → honest degrade до `mode='unsupported'`,
    без write'а. Suggested-write-tools и
    suggested-tools поверхности
    `inspect_operation` / `_build_rollback_plan` /
    `RollbackPlan` теперь добавляют
    `restore_dump_file_from_snapshot` и
    `diff_dump_fragment` — **только** когда
    `automatic_recovery_supported=True`.
  - `apps/platform/src/onec_platform/recovery.py`,
    `run_rollback_assistant` — на
    `confirm_execute=True` с healthy dashboard'ом и
    whitelisted tool'ом теперь действительно
    исполняется автоматический rollback:
    1. Защитная re-валидация
       `details["dump_snapshot_path"]` /
       `details["relative_path"]` — оба обязаны
       быть непустыми строками; иначе degrade в
       `unsupported` без write'а.
    2. Existence-check `snapshot_file_path =
       Path(dump_snapshot_path) / relative_path` —
       missing → `mode='executed', ok=False,
       execution_performed=False` с явным
       error-finding'ом, без write'а.
    3. Чтение snapshot baseline text вверху —
       чтобы post-rollback verify сравнивал со
       стабильной копией. `OSError` тут — снова
       без write'а.
    4. Зов public write-tool'а
       `restore_dump_file_from_snapshot(env,
       relative_path, snapshot_file_path,
       label=f"rollback-{operation_id[:8]}")`. Это
       идёт через `run_write_flow` со всей
       дисциплиной (preflight + snapshot +
       operation + verify + audit). `write_results`
       наполняется dict'ом ToolResult'а.
    5. Refresh `last_write_operation` через
       существующий read-only
       `describe_last_write_operation(env)`, чтобы
       клиент видел свежую audit row, написанную
       рестором.
    6. Обязательный post-rollback verify через
       `diff_dump_fragment(env, relative_path,
       baseline)`. Success criterion жёсткий:
       `restore.ok=True` AND `diff.ok=True` AND
       `diff.payload.data.changed=False`. Иначе
       `mode='executed', ok=False` с
       соответствующим сообщением, но
       `execution_performed=True` (попытка реально
       была).
  - **Никаких back-door write-каналов.**
    `recovery.py` не пишет в файловую систему
    напрямую — все mutating effects идут через
    public write-tool. Импорт
    `mcp_write_server.tools.{diff_dump_fragment,
    restore_dump_file_from_snapshot}` добавлен
    рядом с уже имеющимся
    `prepare_rollback_hint` /
    `describe_last_write_operation` (forward-only
    cross-app: product → write).
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step4_check.py`
  прогоняет 14 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Сценарии: A — `details=None`
  байт-идентичен старому формату; B — `details=dict`
  preserved; C — policy engine знает
  `restore_dump_file_from_snapshot` как
  `allowed_mutating`, unknown op остаётся
  `unknown_intent`; D — restore tool отвергает
  empty / non-string / `..` / missing-snapshot inputs
  fail-closed без касания live target; E — happy-path
  `add_catalog_attribute` пишет audit row с полными
  `details` и snapshot-файл байт-равен pre-add
  baseline; F — `inspect_operation` отдаёт
  `automatic_recovery_supported=True` и surface'ит
  два rollback-tool'а в `suggested_write_tools`; G —
  preview без write'ов; H — confirm_execute=True →
  `mode='executed', ok=True, execution_performed=True`,
  ровно один `write_result` (рестор) и один
  `verify_result` с `data.changed=False`, live XML
  байт-равен pre-add; I — то же для
  `add_document_attribute`; J — pre-Step-4 audit row
  (без `details`) → `mode='unsupported'`, no write;
  K — tool вне whitelist'а (`update_module_code`) →
  `mode='unsupported'`, no write (даже если details
  есть); L — gateway остановлен → dashboard не
  ready → `mode='blocked', ok=False`, no write,
  пост-add файл остаётся в post-add состоянии.
  M — registry invariants `read=15 / write=24 /
  intelligence=16`. N — нулевой импорт
  `onec_policy_engine` в product / intelligence
  поверхностях (тонкая проверка реальных import
  statement'ов, не docstring'ов).
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 24 имени включая
  `restore_dump_file_from_snapshot`,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  намеренно не дёргает recovery executed branch —
  manual check покрывает её на synthetic стенде без
  настоящего 1cv8.

### Phase 6 / Step 5 — metadata completion / structural editing (завершён)

- **Архитектурное решение Step 5.** Это **первый
  настоящий structural XML edit slice**: одно
  точечное расширение metadata-поверхности на одном
  объекте (form-level Attributes), сделанное через
  `xml.etree.ElementTree`, а не через
  substring/`rfind` патчинг. Step 5 не ship'ит full
  metadata-вселенную и не переписывает существующие
  Phase 3 mutating tool'ы (`add_catalog_attribute`,
  `add_document_attribute`, form/module-level tools)
  на DOM-edit — это сознательное узкое решение,
  чтобы не размывать scope. Также Step 5 не делает
  `delete_*`-tool'ов, не расширяет rollback whitelist
  Step 4, не вводит BSL AST-парсер, не трогает
  `apply_config_from_files` /
  `update_database_configuration` (это отдельные
  будущие шаги Phase 6).
- **Что реально появилось в коде.**
  - `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`
    — добавлены **шесть новых internal helper'ов** на
    stdlib `xml.etree.ElementTree` (без новых runtime-файлов):
    - `parse_xml_file(path) -> ET.ElementTree` —
      обёртка над `ET.parse`; `OSError` /
      `ET.ParseError` пропагируют (fail-loud, как
      того требует helper layer);
    - `write_xml_file(path, tree) -> None` —
      сериализация UTF-8 + `xml_declaration=True` +
      `short_empty_elements=False`. Последний
      параметр критичен: пустые контейнеры остаются
      в форме `<Tag></Tag>`, не collapse'ятся в
      `<Tag/>`, и downstream substring-based tool'ы
      (например, `add_form_element` со
      своим `</Elements>` lookup'ом) продолжают
      работать;
    - `find_form_element(root, form_name) ->
      ET.Element | None` — рекурсивный поиск
      `<Form name="form_name">`. Поддерживает и flat
      shape (тестовые fixture'ы), и nested shape
      (`<ChildObjects><Forms>` в production-картах);
    - `get_or_create_form_attributes_block(form_elem)
      -> ET.Element` — возвращает существующий
      `<Attributes>` или создаёт новый как
      `SubElement` в конце form'ы. Mutates form_elem
      in place при создании;
    - `add_attribute_to_form_attributes_block(
      attributes_block, name, attr_type, synonym)`
      — структурный append `<Attribute name="..."><Type>...</Type>[<Synonym>...]</Attribute>`;
      без de-dup (вызывающая сторона сама проверяет
      уникальность);
    - `form_has_attribute(form_elem, attribute_name)
      -> bool` — поиск по атрибуту `name="..."`,
      **только** внутри form's own `<Attributes>`
      (object-level Attributes намеренно не
      consult'ятся — это другая metadata surface).
    Helper layer остаётся **internal**: никаких
    ToolResult'ов, никакого `run_write_flow`, никаких
    snapshot/audit обязательств — всё это лежит на
    tool layer и flow.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлен **один новый public mutating tool**:
    - **`add_form_attribute(environment, object_name,
      form_name, attribute_spec, label="add-form-attribute")`**.
      Идёт строго через `run_write_flow(...)`. Pre-flow
      validation: `object_name` через тот же
      `_resolve_object_xml_path` (поддерживает
      `Справочник.<name>` / `Документ.<name>`);
      `form_name` через существующий `_MODULE_NAME_RE`
      (`\w+`); `attribute_spec` — `name` non-empty без
      whitespace, `type` ∈ `_ALLOWED_ATTR_TYPES`
      (`String` / `Number` / `Date`), `synonym`
      опционален. Bad-input возврат — без `runtime` в
      payload, без stage marker'а, без
      backup/dump-snapshot (flow не запускался). В
      operation: парсит XML, ищет форму через
      `find_form_element`, dup-check через
      `form_has_attribute` (по `name=` атрибуту, не
      substring), `<Attributes>` создаётся
      structurally если отсутствует
      (`get_or_create_form_attributes_block`), новый
      `<Attribute>` добавляется через
      `add_attribute_to_form_attributes_block`, дерево
      пишется обратно через `write_xml_file`. Form
      missing → `ValueError` → `stage="operation",
      ok=False`, файл не тронут; duplicate →
      `FileExistsError` → тот же fail-closed путь.
      `operation_payload` несёт
      `attributes_block_created: bool` — True ровно
      когда блок был создан с нуля. Verify в flow
      повторно парсит файл и проверяет
      `form_has_attribute(form, attr_name)`
      structurally, а не substring. Никаких новых
      обязательных параметров у других tool'ов.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`,
    `verify_metadata_change(...)` — добавлена **одна
    новая read-only ветка** dispatcher'а:
    `kind="form_attribute_exists"` (поля expectation:
    `object_name`, `form_name`, `attribute_name`).
    Tool name результата остаётся
    `verify_metadata_change`;
    `payload.data.verification_kind =
    "form_attribute_exists"`. Реализация — приватный
    helper `_verify_form_attribute_exists_internal`
    в том же файле (без новых runtime-файлов): идёт
    через существующий `read_dump_file`,
    `ET.fromstring` на содержимом, `find_form_element`
    + `form_has_attribute`. PlatformError из dump
    adapter'а и `ET.ParseError` на malformed XML
    оба → `ok=False` с конкретным сообщением (не
    crash). Новый standalone public verify-tool
    **не** добавляется — это сознательное решение,
    чтобы public surface оставалась узкой.
  - `apps/mcp-write-server/src/mcp_write_server/server.py`
    — регистрация нового tool'а в
    `REGISTERED_TOOLS`. Алфавитный `list_tools()`
    теперь возвращает 25 имён (был 24). Read-server
    (15) и intelligence-server (16) **не тронуты**.
  - `packages/onec-policy-engine/src/onec_policy_engine/engine.py`
    — **не тронут**. `add_form_attribute` уже был
    зарегистрирован в `_METADATA_MUTATING_OPERATIONS`
    в Phase 3 (как часть планового whitelist'а Phase 3
    metadata-tools) и просто переходит из «namespace
    зарезервирован» в «реализован». Policy decision
    остаётся `allowed_metadata_mutating`,
    `require_snapshots=True`.
- **Что НЕ переписано на structural edit.**
  - `add_catalog_attribute` / `add_document_attribute`
    (object-level Attributes) — продолжают работать
    через `insert_fragment_into_named_block` без
    изменений. Step 5 ship'ит structural edit
    точечно — для form-level Attributes — а не
    сметает все старые tool'ы одним проходом.
  - Form/module level tools Phase 3 / Step 6
    (`create_managed_form`, `add_form_element`,
    `append_module_method`,
    `replace_module_method_body`) — без изменений.
  - `apply_config_from_files` /
    `update_database_configuration` — снова не
    тронуты, это отдельные шаги Phase 6 (или
    parallel-track после).
- **Честные ограничения slice'а.**
  - Нет XML namespace handling. Production-карты 1С
    обычно несут
    `xmlns="http://v8.1c.ru/8.3/MDClasses"`;
    namespaced cards — out of scope для этого slice.
    Tools и helper'ы рассчитаны на un-namespaced XML,
    который используют тестовые fixture'ы и Phase 3
    substring-based tools. Поддержка namespaced cards
    — отдельный будущий step.
  - ElementTree **не** preserves whitespace /
    pretty-print byte-for-byte. После записи файл
    может выглядеть слегка иначе (например, без
    оригинальных переносов строк), хотя
    XML-эквивалентен. Это не ломает downstream
    tool'ы, но честно фиксируется в documentation.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step5_check.py`
  прогоняет 9 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Сценарии: A — registry
  invariants `read=15 / write=25 / intelligence=16`;
  B — form already has `<Attributes>` block →
  `ok=True, stage=completed,
  attributes_block_created=False`, audit row
  `tool_name='add_form_attribute' status='ok'`,
  structural recheck подтверждает атрибут внутри
  нужной формы; C — form has NO `<Attributes>`
  block → tool создаёт блок structurally,
  `attributes_block_created=True`, structural
  recheck тоже подтверждает; D — duplicate в той
  же форме → `ok=False, stage='operation'`, файл
  byte-identical до post-first-add baseline'а,
  audit row `status='error'`; E — form missing →
  `ok=False, stage='operation'`, файл untouched,
  audit row `status='error'`; F — bad
  `attribute_spec.type` → pre-flow rejection (нет
  `runtime` в payload, нет stage marker'а, нет
  audit row на диске, нет `_snapshots` директории);
  G — `verify_metadata_change(kind=
  "form_attribute_exists")` positive → `ok=True,
  verification_kind='form_attribute_exists',
  exists=True`, tool_name `verify_metadata_change`;
  H — то же negative (форма есть, атрибута нет) →
  `ok=False, exists=False`; H' — то же с missing
  form → `ok=False, exists=False` (degrade без
  crash'а на отсутствующей форме); I — registry
  counts (proxy для dev-check invariant'а; реальный
  `run_dev_check.ps1` запускался отдельно).
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён включая
  `add_form_attribute`,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`.
  `selfcheck.py` намеренно не дёргает
  `add_form_attribute` — manual check покрывает
  все ветки на synthetic стенде.

### Phase 6 / Step 6 — runtime hardening / supervision / logs (завершён)

- **Архитектурное решение Step 6.** Это **первый
  честный slice runtime hardening** поверх уже
  существующего product runtime contract из Phase 5 /
  Step 3. Step 6 **не** делает Windows Service / systemd
  unit registration, **не** background watcher /
  supervisor / daemon manager / timer-loop, **не** hot
  reload, **не** journald / log aggregation /
  forwarding, **не** logging framework. Step 6 не
  добавляет ни одного нового MCP tool'а. Все изменения
  локальны в продуктовом слое
  `apps/platform/src/onec_platform/`.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/models.py` —
    добавлена константа `RESTART_POLICIES = ("never",
    "restart-if-stale")`, константа
    `DEFAULT_LOG_MAX_BYTES = 1 MiB`. Класс
    `ProductServiceSpec` получил три optional поля:
    `restart_policy: str = "never"`,
    `logs_enabled: bool = True`,
    `log_max_bytes: int = DEFAULT_LOG_MAX_BYTES`.
    `RUNTIME_STATE_SCHEMA_VERSION` поднят `1 → 2`;
    введена `RUNTIME_STATE_READABLE_SCHEMA_VERSIONS =
    (1, 2)`. Класс `RuntimeServiceState` расширен
    семью persisted-полями: `restart_policy`,
    `restart_attempts: int`, `last_exit_code: int |
    None`, `stdout_log_path: str | None`,
    `stderr_log_path: str | None`,
    `last_started_at: str | None`,
    `last_stopped_at: str | None`. Все default'ы
    consistent — старые dataclass-конструкторы Step 3
    остаются валидны.
  - `apps/platform/src/onec_platform/loader.py` —
    `_parse_service_spec` строго валидирует три новых
    поля: `restart_policy` через whitelist
    `RESTART_POLICIES`, `logs_enabled` как чистый
    `bool` (не bool-ish), `log_max_bytes` как
    положительный `int` с явным отвержением `bool`
    (т.к. `bool ⊂ int` в Python). Bad shape →
    `ValueError`, который boundary-слой переводит в
    `ok=False`. Старые конфиги без этих полей
    продолжают грузиться без изменений.
  - `apps/platform/src/onec_platform/state.py` —
    reader принимает обе `RUNTIME_STATE_READABLE_SCHEMA_VERSIONS`.
    Pre-Step-6 (schema=1) файлы читаются с дефолтами
    для новых полей: `restart_policy="never"`,
    `restart_attempts=0`, остальные `None`. В памяти
    schema нормализуется к текущей версии (2) сразу
    при чтении, чтобы downstream-код видел
    consistent shape. Writer всегда эмитит version=2.
    Unsupported schema versions по-прежнему
    fail-closed.
  - `apps/platform/src/onec_platform/process_control.py`
    — добавлен `get_pid_exit_code(pid)` (Windows: через
    `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` +
    `GetExitCodeProcess`; POSIX: всегда возвращает
    `None` — orchestrator не spawn'ил PID как child
    текущего процесса, поэтому `waitpid` недоступен;
    честная деградация). `spawn_service(...)` получил
    optional kwargs `stdout_handle: IO[bytes] | int |
    None` / `stderr_handle: IO[bytes] | int | None`.
    `None` сохраняет старое Step 3 поведение
    (`DEVNULL`); открытый file handle / int FD
    маршрутизирует поток. `stdin` всегда `DEVNULL`.
    `shell=True` **никогда** не используется.
    `start_new_session=True` (POSIX) /
    `CREATE_NEW_PROCESS_GROUP` (Windows) сохранены без
    изменений.
  - `apps/platform/src/onec_platform/runtime_logs.py`
    (новый, **internal helper module**, ~150 строк) —
    `logs_dir(work_dir)` / `get_log_paths(work_dir,
    service_name)` (path arithmetic, no I/O),
    `prepare_log_dir(work_dir)` (mkdir
    `<work_dir>/.runtime/logs/`, fail-closed на
    отсутствующий work_dir / permission'ы),
    `rotate_log_if_oversized(path, max_bytes)`
    (одна generation: переименовывает в `<file>.1`
    через `os.replace`; old `.1` перезаписывается;
    возвращает `True` ровно когда rotation реально
    случилась), `open_log_handles(stdout_path,
    stderr_path)` (открывает пару в режиме `"ab"`
    binary append, `buffering=0`; на failure второго
    open закрывает первый и пробрасывает `OSError`).
    Никаких ToolResult'ов, никакой stream
    мультиплексации.
  - `apps/platform/src/onec_platform/runtime.py` —
    `_service_state_from_spec` берёт `restart_policy`
    из spec'а; `_merge_persisted_into_spec_state`
    переносит persisted `restart_attempts` /
    `last_exit_code` / log paths / timestamps в
    materialized state, при этом `restart_policy`
    остаётся spec-driven (current config
    authoritative). `_refresh_running_against_pid` при
    обнаружении stale PID best-effort вызывает
    `get_pid_exit_code` и стампит `last_stopped_at` =
    UTC ISO. Добавлен приватный
    `_prepare_logs_for_spawn(spec, work_dir)`,
    собирающий лог-handles + finding'и про rotation /
    log-dir-failed; `_start_one(spec, current,
    work_dir)` (новая сигнатура — третий аргумент
    `work_dir`) использует его, передаёт handles в
    `spawn_service`, при success'е populate'ит
    `stdout_log_path` / `stderr_log_path` /
    `last_started_at`, на любом log-side failure
    (mkdir / rotate / open) возвращает
    `status="error"` без silent-fallback'а на
    DEVNULL. `_start_one` теперь возвращает
    `tuple[RuntimeServiceState, list[DoctorFinding]]`
    (раньше один finding; multiple фактические
    finding'и нужны для отдельного surface'инга
    `runtime_log_paths` / `runtime_log_rotated`).
    `_stop_one` стампит `last_stopped_at`. Добавлен
    `_apply_restart_if_stale(config, services,
    work_dir)` — boundary-only restart path, который
    инкрементит `restart_attempts`, зовёт обычный
    `_start_one` и эмитит `runtime_restart_attempted` /
    `runtime_restart_succeeded` /
    `runtime_restart_failed`. Этот helper зовётся из
    `get_product_runtime_status` (после
    `_refresh_running_against_pid`; persist делается,
    только если что-то реально перезапустилось — иначе
    status остаётся read-only) и из `_run_operation`
    после фазы start/reload. На `stop` помечен явно
    как **не** срабатывающий — оператор только что
    попросил остановить, восстановление было бы
    surprise.
  - **Никаких других runtime-файлов не добавлялось.**
    `dashboard.py` / `workflow.py` / `recovery.py` /
    `realstand.py` / `installer.py` / `templates.py` —
    без изменений. `mcp-read-server` /
    `mcp-write-server` / `mcp-intelligence-server` /
    `onec-policy-engine` / `onec-config` —
    без изменений.
- **Operator-visible findings.** Новые коды:
  `runtime_log_paths:<svc>` (ok), `runtime_log_rotated:<svc>`
  (ok), `runtime_log_dir_failed:<svc>` /
  `runtime_log_open_failed:<svc>` /
  `runtime_log_rotate_failed:<svc>` (error,
  fail-closed для конкретного service'а),
  `runtime_restart_attempted:<svc>` (warning),
  `runtime_restart_succeeded:<svc>` (ok),
  `runtime_restart_failed:<svc>` (error). Существующий
  `runtime_pid_stale:<svc>` обогащён: текст содержит
  `last_exit_code=N` когда он известен, или
  «exit code unavailable on this platform» когда
  POSIX-fallback вернул `None`.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step6_check.py`
  прогоняет 12 сценариев A–K на synthetic tempdir с
  реальными `subprocess.Popen`-вызовами:
  - A — registry invariants (`read=15 / write=25 /
    intelligence=16`);
  - B — happy path start/status/stop с реальным
    long-lived Python sleeper'ом, log paths
    populated, status показывает stdout/stderr-paths
    и `last_started_at`, stop реально kill'ит PID и
    стампит `last_stopped_at`;
  - C — содержимое логов: child пишет маркеры в
    stdout/stderr, после короткого ожидания файлы
    содержат маркеры (sleeper script
    материализуется как файл, не передаётся через
    `python -c` — на Windows multi-line `-c`
    payload'ы могут портиться command-line
    quoting'ом);
  - D — pre-create oversized `.out.log`, start
    эмитит `runtime_log_rotated:svc`,
    `<svc>.out.log.1` создан, новый активный лог
    свежий и меньше старого;
  - E — restart_policy=`"never"` + dead PID в state:
    status reports `stale`, `runtime_pid_stale`
    finding есть, **никаких** restart-attempt-finding'ов,
    `restart_attempts=0`;
  - F — restart_policy=`"restart-if-stale"` + dead PID
    в state: status автоматически перезапускает —
    new PID alive, `restart_attempts=1`,
    `runtime_restart_attempted` +
    `runtime_restart_succeeded` finding'и есть,
    persisted state обновлён (новый PID, счётчик);
  - G — `<work_dir>/.runtime/logs` существует как
    регулярный файл (не директория), start
    fail-closed: `runtime_log_dir_failed:svc`
    finding, `status="error"`, `pid=None`, **никакого**
    silent fallback'а на DEVNULL;
  - H1 — старый config без `restart_policy` /
    `logs_enabled` / `log_max_bytes` всё ещё валиден
    (default'ы применяются);
  - H2 — schema_version=1 persisted state читается
    без crash'а; в памяти schema нормализуется к 2;
    boundary call работает;
  - I — JSON-file flow happy path:
    `start_product_runtime_from_json_file` +
    `get_product_runtime_status_from_json_file`
    срабатывают end-to-end;
  - J — 7 bad-config вариантов
    (`restart_policy="garbage"`, `restart_policy=1`,
    `logs_enabled="true"`, `log_max_bytes=0`,
    `log_max_bytes=-1`, `log_max_bytes=True`,
    `log_max_bytes="1k"`) — все возвращают `ok=False`
    без exception'а наружу, message содержит
    конкретное объяснение;
  - K — registry-counts proxy под dev-check.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений,
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`.
  `selfcheck.py` намеренно не дёргает Step 6
  runtime-flow'ы — manual check покрывает все
  ветки на synthetic subprocess'ах.

### Phase 6 / Step 7 — real-stand end-to-end validation + standalone docs/runbooks (завершён)

- **Архитектурное решение Step 7.** Это **validation + docs**
  step. Никакого расширения surface'а: ни одной новой MCP-tool'и,
  ни одного нового product-layer execution slice'а, ни одного
  нового runtime hardening behavior'а. Цель — подтвердить, что
  Phase 6 (Step 2–6) сходится в один связный сценарий на
  synthetic стенде, и вынести operator/admin/developer
  knowledge из READMEов в standalone-документы.
- **Кодовых правок не было.** Все изменения этого шага — только
  под `docs/`. `apps/` и `packages/` тронуты ровно одним блоком
  (заголовок и pointer-блок в `apps/platform/README.md`),
  чтобы операторы и администраторы видели, куда переехала
  ежедневная документация. Остальные README обновлены только в
  части registry counts / Step переходов, без изменения
  surface'а.
- **Что реально появилось в коде / документации.**
  - `docs/operator-manual.md` (новый) — короткий путь
    install/bootstrap/start/status/dashboard/workflow/history/
    rollback/smoke; что означают `healthy`/`degraded`/`blocked`/
    `preview`/`executed`/`unsupported`/`rejected`; как читать
    rollback preview; честные ограничения Phase 6 списком.
  - `docs/administrator-manual.md` (новый) — product-config
    keys (top-level + per-environment + per-service runtime),
    runtime services / restart_policy / logs / work_dir;
    binary-related поля и их честная семантика; где лежат
    `runtime-state.json` и логи; типовые сбои и что делать;
    что нельзя ожидать от текущей версии.
  - `docs/developer-manual.md` (новый) — архитектурная карта
    read/write/intelligence/platform; куда добавлять новый
    capability какого класса; safety invariants, которые
    нельзя ломать (run_write_flow единственный mutating путь;
    intelligence read-only по конструкции; 0 imports
    onec_policy_engine в product/intelligence; no shell=True;
    atomic writes; boundary helpers never raise); slice map
    Phase 6 (Step 1–7); как правильно писать manual-check
    скрипты (тонкие grit-правила: сценарии без `python -c`
    multi-line на Windows, чтение логов до stop'а, ASCII в
    print'ах для cp1251).
  - `docs/runbooks.md` (новый) — шесть recipes в формате
    Symptom/Cause/Diagnose/Fix/Confirm: RB-1 bootstrap doctor
    red, RB-2 runtime stale pid, RB-3 workflow blocked, RB-4
    rollback preview/executed/unsupported, RB-5 real-stand
    smoke failed, RB-6 malformed audit log lines.
  - `apps/platform/README.md` — заголовок «Что сейчас внутри»
    обновлён до **Step 1–7**; добавлен короткий
    pointer-блок с ссылками на все четыре standalone docs.
    Существующий технический контент сохранён без изменений.
  - `README.md` (root) — Phase 6 параграф расширен Step 7
    sentence (Scenario A end-to-end без правок кода + 5
    failure paths + standalone docs); «Следующий шаг»
    переключён на **Step 8 — foundation for enterprise
    track**.
  - `PROJECT-STATUS.md` — текущий шаг переключён на Step 7;
    Step 6 помечен `(завершён)`; добавлен полный Step 7
    detail block; «Следующий шаг» переписан на Step 8.
- **Что НЕ тронуто.** `apps/mcp-read-server/` /
  `apps/mcp-write-server/` / `apps/mcp-intelligence-server/`
  / `packages/onec-*/` / `apps/platform/src/` (кроме того, что
  ничего не редактировалось в коде, точка) — все без правок.
  Existing `docs/runbooks/local-dev-check.md` не тронут.
  `selfcheck.py`, `scripts/dev/`, `pyproject.toml`,
  `.github/` — без изменений.
- **Manual verification — Scenario A + F1–F5 + discipline.**
  Скрипт `C:/Users/user/AppData/Local/Temp/phase6_step7_check.py`
  собирает один связный сценарий и пять honest failure paths
  на synthetic tempdir + local HTTPServer (gateway) + реальные
  `subprocess.Popen` вызовы (sleeper-сервис в runtime, smoke
  через `sys.executable`).
  - **Scenario A.1–A.13.** `bootstrap_product` →
    `run_install_fast_path(confirm_write=True)` →
    `start_product_runtime` → `get_product_runtime_status`
    (status=`running`, log paths populated) →
    `build_environment_dashboard` (overall_status=`healthy`,
    `ready_for_workflows=True`) →
    `run_guided_workflow(safe-add-attribute,
    target_kind=catalog, confirm_execute=True)`. Mutating
    workflow выбран **именно** под Step 4 whitelist
    (`add_catalog_attribute`); operation_id извлекается из
    `wf_res.last_write_operation["operation_id"]` и
    реально проходит сквозь `get_operation_history` (entry
    есть в списке) + `inspect_operation`
    (`operation_found=True, automatic_recovery_supported=True`)
    + `run_rollback_assistant(confirm_execute=True)`
    (`mode='executed', ok=True, execution_performed=True`,
    one write_result + one verify_result с
    `data.changed=False`). **Post-rollback verify** —
    re-parse XML через `xml.etree.ElementTree` и assert
    что `ScenarioField` исчез structurally **И** что live
    text byte-equals pre-add baseline. Затем
    `get_real_stand_readiness`
    (`ready_for_real_stand_smoke=True`) →
    `run_real_stand_smoke_test(confirm_execute=True)`
    (`mode='executed', binary_invoked=True,
    binary_exit_code=0`) → `stop_product_runtime`
    (PID реально умирает). Все 13 шагов прошли с
    реальными subprocess'ами.
  - **F1.** Workflow blocked — gateway не поднят →
    dashboard не `healthy` → `mode='blocked',
    execution_performed=False`, файл untouched.
  - **F2.** Rollback unsupported — `update_module_code`
    написан напрямую через write-server → audit row есть,
    но `tool_name='update_module_code'` вне Step 4
    whitelist'а → `mode='unsupported', ok=True,
    execution_performed=False, write_results=[],
    verify_results=[]`.
  - **F3.** Broken JSON product-config (`{ this is not
    valid JSON `) — все шесть `*_from_json_file`
    boundary'ев вернули `ok=False` без exception'а наружу:
    `bootstrap_product_from_json_file`,
    `get_product_runtime_status_from_json_file`,
    `build_environment_dashboard_from_json_file`,
    `get_operation_history_from_json_file`,
    `get_real_stand_readiness_from_json_file`,
    `run_real_stand_smoke_test_from_json_file`.
  - **F4.** Malformed audit lines — первая строка
    audit.jsonl сломанная JSON, вторая — корректный
    `AuditRecord`. `get_operation_history` вернул
    `ok=True` с findings'ом
    `audit_line_invalid_json:0` и реальным entry для
    второй строки; `inspect_operation` для
    operation_id `'real-row-1'` отдал
    `tool_name='add_catalog_attribute'`. Boundary не
    упал.
  - **F5.** Real-stand smoke failure path — probe args
    `["-c", "import sys; sys.exit(7)"]` →
    `mode='executed', binary_invoked=True,
    binary_exit_code=7, ok=False`. Никакого fake'а и
    никакого silent fallback'а на «metadata-only ok».
  - **D1.** Registry invariants pre-/post-: `read=15,
    write=25, intelligence=16` — без drift'а.
  - **D2.** Suggested tools/suggested write tools: union
    из 54 реальных registered-имён + 10
    `_KNOWN_PLATFORM_FUNCTIONS`. Made-up имя
    `"totally_made_up_tool_xyz"` корректно отвергнуто
    `_allow_only_real_tools`.
  - **D3.** 0 import'ов `onec_policy_engine` под
    `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/` (тонкая
    проверка реальных `import` / `from ... import ...`
    statement'ов, не docstring'ов).
  - **D4.** Step 7 прошёл без code changes —
    зафиксировано в этом detail block'е и в комментариях
    скрипта.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным. Вывод последнего прогона:
  `imports_ok = true`, registry counts (`read=15,
  write=25, intelligence=16`) — без изменений,
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`
  не тронут.

### Phase 6 / Step 8 — foundation for enterprise track (завершён)

- **Архитектурное решение Step 8.** Это **узкий honest
  foundation slice**, не enterprise version. Задача — дать
  будущему enterprise track реальную опору, не врать про
  enterprise-readiness, не плодить новые MCP tool'ы и не
  расширять surface ради surface. Шаг **не** делает SSO/RBAC,
  multi-tenant, secrets vault, policy-as-code, federated audit
  storage, multi-instance HA, web-UI, новые MCP tool'ы, новые
  runtime supervision slices, новые write tools. Всё это явно
  вынесено в parallel enterprise track ПОСЛЕ Phase 6.
- **Что реально появилось в коде.**
  - `apps/platform/src/onec_platform/models.py` — добавлены
    две константы и две модели:
    - `DEPLOYMENT_TIERS = ("dev", "test", "stage", "prod-like")`
      — ровно четыре whitelisted tier'а;
    - `FOUNDATION_LEVELS = ("absent", "minimal", "partial",
      "strong")` — четыре уровня детерминистического verdict'а;
    - `EnterpriseFoundationSettings` (dataclass; шесть
      optional-полей: `deployment_tier: str | None`,
      `instance_id: str | None`, `config_owner: str | None`,
      `change_control_required: bool = False`,
      `require_operator_identity: bool = False`,
      `runbook_reference: str | None = None`);
    - `EnterpriseFoundationResult` (dataclass; стандартная shape
      с `ok`, `foundation_level`, `ready_for_enterprise_track`,
      зеркалами всех шести полей секции, плюс
      `confirmed_findings` / `presumed_findings` /
      `recommended_actions` / `suggested_tools` /
      `suggested_write_tools` / `message`).
    - `ProductConfig` получил новое optional поле
      `enterprise: EnterpriseFoundationSettings`
      (`field(default_factory=lambda: ...())` — Step 1–7
      конфиги остаются валидны).
  - `apps/platform/src/onec_platform/loader.py` — добавлен
    приватный `_parse_enterprise(...)`. Strict-validation:
    unknown keys reject (typo `deplyoment_tier` → `ValueError`),
    `deployment_tier` whitelisted, `instance_id` /
    `config_owner` / `runbook_reference` non-empty string или
    `None`, два bool-поля строго `bool` (не bool-ish). Missing
    section → empty `EnterpriseFoundationSettings()` (Step 1–7
    backward compat).
  - `apps/platform/src/onec_platform/templates.py` —
    `build_product_config_template(...)` принял **шесть** новых
    optional kwargs: `enterprise_deployment_tier`,
    `enterprise_instance_id`, `enterprise_config_owner`,
    `enterprise_change_control_required`,
    `enterprise_require_operator_identity`,
    `enterprise_runbook_reference`. Pre-flow validation
    зеркалит loader'у: whitelist tier, non-empty strings, strict
    bools. Block эмитится **только** когда хотя бы один
    enterprise_* kwarg передан — Step 1–7 templates остаются
    байт-идентичными.
  - `apps/platform/src/onec_platform/enterprise.py` (новый,
    ~470 строк, **internal+public**) —
    `inspect_enterprise_foundation(data)` /
    `inspect_enterprise_foundation_from_json_file(path)`.
    Read-only по конструкции: не пишет в audit, не зовёт
    `run_write_flow`, не стартует / стопает runtime, не
    вызывает MCP tool'ы. Никогда не raise'ит. Проверяет
    четыре секции:
    - **A. Identity / config discipline.** `deployment_tier`
      declared, `instance_id`, `config_owner`,
      `change_control_required`, `require_operator_identity`.
      Для prod-like (declared OR detected по visible-полям)
      отсутствие `instance_id` / `config_owner` — `error`
      severity.
    - **B. Operability foundation.** `bootstrap.work_dir`,
      `runtime.services` non-empty, `logs_enabled=True` для
      всех enabled-сервисов, `restart_policy` в whitelist'е.
    - **C. Traceability / recovery foundation.** Standalone
      manuals Step 7 (`docs/operator-manual.md`,
      `docs/administrator-manual.md`,
      `docs/developer-manual.md`, `docs/runbooks.md`)
      physically present (через ancestor-walk от модуля до
      repo root); recovery boundaries
      (`get_operation_history`, `inspect_operation`,
      `run_rollback_assistant`) реально callable на
      `onec_platform`. Узкий automatic-rollback whitelist Step 4
      явно отмечен как **honest constraint**, не gap.
    - **D. Real-stand / binary foundation.**
      `onec_binary_path` declared, `onec_dumpcfg_command_template`
      declared. Inspection **контракта**, не probing бинаря —
      ничего не запускается; smoke-test'ы остаются территорией
      `run_real_stand_smoke_test`.
    Verdict через детерминистический `_classify_foundation_level`:
    `"absent"` если секция отсутствует; `"strong"` ровно когда
    все четыре section_score'а на максимуме И нет error-finding'ов;
    `"partial"` для identity ≥ 2 / operability ≥ 2; иначе
    `"minimal"`. `ready_for_enterprise_track` = (`level ==
    "strong"` AND `errors == 0`).
  - `apps/platform/src/onec_platform/__init__.py` — добавлен
    re-export новой поверхности: `inspect_enterprise_foundation`
    / `inspect_enterprise_foundation_from_json_file` /
    `EnterpriseFoundationSettings` / `EnterpriseFoundationResult`
    / `DEPLOYMENT_TIERS` / `FOUNDATION_LEVELS`.
- **Что НЕ тронуто.** `mcp-read-server`, `mcp-write-server`,
  `mcp-intelligence-server`, `onec-policy-engine`, `onec-config`,
  `onec-audit`, `onec-health`, `onec-process-runner`,
  `onec-troubleshooting`, `mcp-common`, `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`, `.github/`,
  `docs/runbooks/local-dev-check.md` — все без правок.
  Никаких новых MCP tool'ов; никакого нового runtime supervision
  slice'а; никакого нового write-tool'а; никакого probing 1cv8
  binary'а.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step8_check.py`
  прогоняет 13 сценариев на synthetic tempdir:
  - **R1** registry invariants pre/post — `read=15, write=25,
    intelligence=16`, без drift'а.
  - **R2** zero `onec_policy_engine` real imports под
    `apps/platform/src/` и `apps/mcp-intelligence-server/src/`.
  - **A1** Step 1–7 config без enterprise секции грузится;
    `bootstrap_product` ok=True.
  - **A2** `build_product_config_template(...)` без
    enterprise_* kwargs **не** эмитит блок; round-trip через
    `load_product_config` валиден.
  - **A2'** template **с** enterprise_* kwargs эмитит блок;
    round-trip восстанавливает все шесть полей.
  - **B1** strong, fully-set foundation:
    `foundation_level='strong'`,
    `ready_for_enterprise_track=True`, sections=(identity=3/3,
    operability=3/3, traceability=2/2, binary=2/2), errors=0.
  - **C1** enterprise секция absent →
    `foundation_level='absent'`, ready=False, finding
    `foundation_enterprise_section_absent`.
  - **C2** prod-like без `instance_id` / `config_owner` →
    ready=False, error-findings
    `foundation_instance_id_missing_on_prod` +
    `foundation_config_owner_missing_on_prod`.
  - **C3** enabled service с `logs_enabled=False` →
    `foundation_level != "strong"`, finding
    `foundation_logs_disabled_on_enabled_services`.
  - **C4** prod-like без binary contract → ready=False,
    error-findings `foundation_onec_binary_path_missing_on_prod` +
    `foundation_onec_dumpcfg_template_missing_on_prod`.
  - **C5** manuals presence detection — exactly one of
    `foundation_manuals_present` / `foundation_manuals_missing`
    fires.
  - **D1** malformed enterprise shape (7 cases:
    `deployment_tier="garbage"`, `deployment_tier=int`,
    `change_control_required="true"`,
    `require_operator_identity=int`, `instance_id=""`, unknown
    key, `enterprise as list`) — все возвращают `ok=False`
    без exception'а наружу.
  - **D2** bad JSON file → `_from_json_file` ok=False.
  - **D3** non-dict root (string / list) → boundary ok=False
    без crash'а.
  - **E1** `suggested_tools` / `suggested_write_tools`
    содержат только реальные имена из live registries +
    `_KNOWN_PLATFORM_FUNCTIONS` whitelist.
- **dev-check.** `scripts/dev/run_dev_check.ps1` остаётся
  зелёным. Registry counts: `read=15, write=25,
  intelligence=16`. `imports_ok = true`,
  `selfcheck_status = ok`. `selfcheck.py` намеренно не дёргает
  Step 8 enterprise-foundation flow — manual check покрывает
  все ветки на synthetic стенде.

### Phase 6 / Step 9 — final integration pass (завершён, Phase 6 закрыта)

- **Архитектурное решение Step 9.** Это не planning-step, не
  расширение surface'а. Это **закрывающий integration прогон
  всей Phase 6** одним связным сценарием + honest failure paths
  + discipline asserts. Brief требовал, чтобы все Phase 6
  slice'ы реально сходились в работающий контур; чтобы
  `add_form_attribute` (Step 5) был exercised именно через
  guided workflow; чтобы binary-backed `create_dump_snapshot`
  (Step 2) был доказан как реальный subprocess-путь, а не stub
  fallback; чтобы post-rollback verify был **содержательный**,
  а не «tool ok=True». Все эти требования сошлись.
- **Кодовые правки Step 9 — две минимальные.** Brief разрешает
  правки, если без них честный прогон невозможен; обе правки
  production-уровня, локальные, без MCP-surface drift'а:
  - `apps/platform/src/onec_platform/workflow.py` +
    `apps/platform/src/onec_platform/models.py`. Добавлен один
    тонкий guided-wrapper `safe-add-form-attribute` над уже
    существующим public `add_form_attribute`. Без него
    brief'овский «`run_guided_workflow → add_form_attribute`»
    структурно невозможен (Step 5 ship'нул только
    write-tool'ный slice без guided-обёртки). `WORKFLOW_NAMES`
    стал из 3 имён 4-мя; `_WORKFLOW_RUNNERS` получил один новый
    runner (`_run_safe_add_form_attribute`); внутри тот же
    pattern, что у `safe-add-attribute`: dashboard-precondition,
    intelligence-сигналы (`estimate_change_impact` +
    `summarize_configuration_risk`), confirm gate, mutating
    write через public `add_form_attribute` (которое само идёт
    через `run_write_flow`), verify через
    `verify_metadata_change(kind="form_attribute_exists")`.
    Plan summary честно говорит, что rollback будет advisory-
    only (whitelist Step 4 не покрывает `add_form_attribute`).
  - `apps/platform/src/onec_platform/installer.py` —
    `_config_to_dict` был **багом-носителем** real Step 6 / 8
    регрессии: helper не эмитил Step 6 service-level поля
    (`restart_policy` / `logs_enabled` / `log_max_bytes`) и
    Step 8 enterprise-блок при install-fast-path round-trip'е.
    То есть оператор пишет в input config'е enterprise-секцию,
    зовёт `run_install_fast_path(confirm_write=True)`, JSON
    материализуется на диск без enterprise-блока, и затем
    `inspect_enterprise_foundation_from_json_file` на этом
    materialised JSON отдаёт `foundation_level='absent'`. Это
    был silent gap между Step 3 и Step 6 / 8. Step 9 закрыл
    его минимально: каждый из новых fields эмитится только
    когда отличается от dataclass default'а (значит, Step 1–5
    конфиги по-прежнему round-trip'ят byte-identical).
  - Никаких других кодовых правок. **MCP registries не
    изменены**: `read=15, write=25, intelligence=16` — без
    drift'а. `onec-policy-engine`, `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`, все
    `packages/onec-*/` — не тронуты.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase6_step9_check.py`
  (~600 строк) на synthetic tempdir + local HTTPServer +
  реальные `subprocess.Popen` (sleeper в runtime, copytree
  для binary-backed snapshot, `print('ok')` / `sys.exit(7)`
  для smoke). Никакого реального 1cv8 binary, никакого
  внешнего интернета.
  - **Scenario A — 16 связных шагов:** A.1 `bootstrap_product`
    → A.2 `run_install_fast_path(confirm_write=True)` (Step 3,
    JSON атомарно записан, round-trip ok) → A.3
    `start_product_runtime_from_json_file` (Step 6, реальный
    PID alive) → A.4 status (PID, log paths, last_started_at)
    → A.5 dashboard `overall_status='healthy'`,
    `ready_for_workflows=True` (Step 4) → A.6
    `run_guided_workflow(safe-add-attribute, target_kind=catalog,
    confirm_execute=True)` — реальный
    `add_catalog_attribute` через `run_write_flow`, real
    binary-backed `create_dump_snapshot` (snapshot directory
    физически содержит **скопированный**
    `Catalogs/SampleCatalog.xml` — это структурное
    доказательство binary-backed mode, а не stub'а; в stub
    режиме была бы только `dump-created.txt` marker'а),
    `operation_id` извлечён из `wf_cat.last_write_operation`
    → A.7 `run_guided_workflow(safe-add-form-attribute,
    confirm_execute=True)` — Step 5 structural slice через
    новый guided-wrapper; ElementTree-путь structurally создаёт
    пустой `<Attributes>` блок внутри `<Form name="MainForm">`
    и вставляет туда новый `<Attribute>`; second snapshot тоже
    binary-backed → A.8 history (обе operation_id'и видны) →
    A.9 inspect (catalog op'а;
    `automatic_recovery_supported=True`) → A.10
    `run_rollback_assistant(confirm_execute=True)` —
    `mode='executed', ok=True, execution_performed=True`,
    идёт через public `restore_dump_file_from_snapshot` (то
    есть через тот же `run_write_flow` — НЕ back-door
    filesystem write); один `write_result` (ok=True) + один
    `verify_result` от `diff_dump_fragment`
    (`data.changed=False`) → A.11 **post-rollback verify** —
    re-parse XML через ElementTree, **структурно** подтверждено
    что нет ни `Step9CatalogField`, ни `Step9FormField`; live
    XML byte-equals оригинальной fixture (snapshot catalog
    op'а был сделан до обоих writes — это honest semantics
    rollback'а: «restore the file to the moment the
    rolled-back operation started», не selective undo) →
    A.12 `get_real_stand_readiness` (Step 7,
    `ready_for_real_stand_smoke=True`) → A.13
    `run_real_stand_smoke_test(confirm_execute=True)` — Step 7
    реальный subprocess через `sys.executable` с probe args
    `["-c", "print('ok')"]`, `binary_invoked=True,
    binary_exit_code=0` → A.14
    `inspect_enterprise_foundation_from_json_file` — Step 8 на
    том же materialised JSON-config'е (после fix'а в
    `_config_to_dict`),
    `foundation_level='strong',
    ready_for_enterprise_track=True` → A.15
    `stop_product_runtime` — PID реально умирает
    (`is_pid_alive(pid)=False` после polling'а) → A.16 log
    files `<work_dir>/.runtime/logs/demo.{out,err}.log`
    physically present.
  - **Шесть honest failure paths (F1–F6):**
    - F1 — workflow blocked by unhealthy dashboard (no
      gateway → `mode='blocked', execution_performed=False`,
      файл untouched);
    - F2 — rollback unsupported для `add_form_attribute`
      (вне Step 4 whitelist'а): сначала запустили workflow
      `safe-add-form-attribute(confirm_execute=True)` чтобы
      получить реальный operation_id; затем
      `run_rollback_assistant(confirm_execute=True)` →
      `mode='unsupported', ok=True,
      execution_performed=False, write_results=[],
      verify_results=[]`;
    - F3 — broken JSON config (`{ this is not json`) через
      **девять** `_from_json_file` boundary'ев (включая
      Step 8 `inspect_enterprise_foundation_from_json_file`,
      Step 7 `run_real_stand_smoke_test_from_json_file`,
      Step 3 `run_install_fast_path_from_json_file`,
      Step 5 `run_guided_workflow_from_json_file`,
      Step 6 `get_product_runtime_status_from_json_file`,
      Step 4 `build_environment_dashboard_from_json_file`,
      Step 2 `bootstrap_product_from_json_file`,
      Step 6 `get_operation_history_from_json_file`,
      Step 7 `get_real_stand_readiness_from_json_file`) —
      все возвращают `ok=False` без exception'а наружу;
    - F4 — real-stand smoke с реальным non-zero exit (probe
      = `["-c", "import sys; sys.exit(7)"]`) →
      `mode='executed', binary_invoked=True,
      binary_exit_code=7, ok=False`;
    - F5 — enterprise foundation на prod-like config'е без
      `instance_id` / `config_owner` / `onec_binary_path` /
      `onec_dumpcfg_command_template` →
      `foundation_level='minimal', ready=False`,
      четыре error-finding'а (`*_missing_on_prod`);
    - F6 — binary-backed `create_dump_snapshot` падает с
      operator-declared template'ом, который exit'ит 7 →
      workflow `ok=False, stage='dump_snapshot'` (т.е. flow
      честно остановился на снапшот-стадии), без silent
      stub fallback'а; live XML untouched (Step 2 «no
      runtime fallback once binary contract is declared»
      contract).
  - **Discipline asserts (D1–D5):**
    - D1 registry invariants pre/post — `read=15, write=25,
      intelligence=16` без drift'а;
    - D2 — 0 реальных import'ов `onec_policy_engine` под
      `apps/platform/src/` и
      `apps/mcp-intelligence-server/src/` (тонкий scan
      только настоящих `import` / `from … import …`
      statement'ов, без docstring-noise'а);
    - D3 — 14 списков `suggested_tools` /
      `suggested_write_tools` собраны со всех Scenario A
      результатов; все имена входят в union live registries
      + `_KNOWN_PLATFORM_FUNCTIONS`; made-up name отвергнут
      `_allow_only_real_tools`;
    - D4 — каждый boundary-вызов в скрипте обёрнут в
      `must_not_raise(...)`; ни один не сработал — ни одна
      product-layer boundary не raise'нула наружу;
    - D5 — отсутствие back-door write channel'а структурно
      следует из D2 (product layer не импортирует
      policy-engine; единственный mutating путь — через
      public write-tools, идущие через `run_write_flow`).
  - Финальная строка скрипта: `All Phase 6 / Step 9
    scenarios passed.`
- **dev-check.** `scripts/dev/run_dev_check.ps1` остаётся
  зелёным после Step 9. Registry counts: `read=15, write=25,
  intelligence=16` — без изменений; `imports_ok = true`,
  `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`, `.github/` не
  тронуты.

### Parallel Track A / Step 1 — planning Full Real 1cv8-backed Write Path (завершён)

- **Почему этот трек открыт.** Phase 6 закрыла product
  contour (install / runtime / dashboard / guided
  workflows / rollback / real-stand smoke / enterprise
  foundation). Это **finished product behavior** на
  reference stand'е в **smoke**-форме. Это **не**
  finished real-write product behavior на реальной 1cv8
  binary'е. Самый жирный незакрытый разрыв сейчас — не
  все mutating-write-path'ы доведены до настоящего
  real 1cv8-backed исполнения:
  `apply_config_from_files` и
  `update_database_configuration` остаются Phase 2
  stub-backed; `create_dump_snapshot` имеет binary-backed
  branch (Phase 6 / Step 2), но это partial generic
  slice, не finished contract; на reference stand'е нет
  настоящего multi-step round-trip'а с реальным 1cv8;
  operator-facing contract для binary-backed write
  execution размыт. Track A открыт как первый из
  parallel / completion tracks **после** закрытой
  Phase 6 чтобы доводить именно эту узкую зону —
  real execution layer для apply / update-db / dumpcfg
  — до honest finished behavior. Это **не** Phase 7;
  Phase 7 как отдельная крупная интеграционная фаза не
  запланирована.
- **Какие два документа созданы.**
  - `docs/architecture/track-a-real-write-path-plan.md`
    (новый, ~285 строк): назначение трека, целевой
    результат (семь пунктов operator-facing нарратива
    после закрытия трека), что именно закрывает трек и
    что НЕ закрывает, чем трек отличается от закрытой
    Phase 6, пять крупных блоков (A — real binary-backed
    dump/apply/update contract; B — reference stand
    execution choreography; C — product-layer
    integration over real write path; D —
    operator-facing diagnostics and honest mode
    reporting; E — final validation and closure),
    guardrails (одиннадцать жёстких инвариантов), явный
    список «что НЕ входит в трек», 10 критериев
    приёмки, 9 открытых вопросов Step 1.
  - `docs/architecture/track-a-real-write-path-step-map.md`
    (новый, ~250 строк): семь шагов трека в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат) — Step 1 documentation-only entry → Step
    2 real binary-backed `apply_config_from_files` → Step
    3 real binary-backed `update_database_configuration`
    → Step 4 unify / finish `create_dump_snapshot` real
    path + payload discipline → Step 5 product-layer
    integration over real write path → Step 6 reference
    stand multi-step round-trip → Step 7 final
    integration pass and Track A closure.
- **Что обновлено в README / status.**
  - Корневой `README.md` — добавлен раздел **«Active
    parallel track»** после блока «Активных фаз нет»;
    Track A объявлен; даны ссылки на оба новых
    документа; явно сказано «Это **post-phase
    completion track**, **не** новая Phase 7»; список
    того, что НЕ входит в Track A, продублирован
    кратко. В разделе документов архива добавлен
    подраздел «Документы parallel-track'ов» со
    ссылками на оба новых документа.
  - `PROJECT-STATUS.md` (этот файл) — заголовок
    «Текущий шаг» переключён на **Parallel Track A /
    Step 1**; статус → `in progress`; полный detail
    block (этот раздел); «Phase 6 закрыта» внизу
    остаётся как окончательная фиксация закрытия
    Phase 6.
- **Кода ничего не менялось.** Это намеренно
  documentation-only opening step. `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `.github/`,
  `.claude.json` — все без правок. Никаких новых MCP
  tool'ов. Никаких новых product-layer boundary'ев.
  Никакого расширения registry. Никакого нового
  payload-поля у write-tool'ов. Никакого нового
  workflow'а / readiness-check'а / inspector'а. Все
  изменения — только в `docs/architecture/` (два
  новых файла) + корневой `README.md` + этот файл.
- **Registry counts без изменений.** read = 15;
  write = 25; intelligence = 16. dev-check остаётся
  зелёным (потому что в коде ничего не менялось —
  специально для documentation-only-шага запускать
  dev-check необязательно, но он по-прежнему зелёный).
- **Какой следующий шаг.** **Parallel Track A / Step 2
  — real binary-backed `apply_config_from_files`
  contract.** Step 2 закроет часть критерия приёмки 1
  трека: первый из двух Phase 2 stub-backed-путей
  переходит на honest dual-mode contract с real
  execution. Затрагиваемые зоны Step 2: точечно
  `apps/mcp-write-server/src/mcp_write_server/tools.py`
  + (возможно) shared helper в `runtime/`; точечно
  `packages/onec-config/src/onec_config/models.py` +
  `loader.py` (одно новое optional-поле в
  `EnvironmentConfig` + strict-validation,
  fail-closed на bad shape). Read- и intelligence-
  серверы Step 2 не трогает. `onec_policy_engine`
  не трогает. Registries Step 2 не растит — это та
  же операция с расширенным dispatch'ем, как
  Phase 6 / Step 2 расширил `create_dump_snapshot`.
  По умолчанию решение по Q1 (одно поле
  `onec_apply_command_template` или общий словарь
  `onec_command_templates`) фиксируется именно в
  Step 2 трека.
- **Что осталось до закрытия трека.** Шесть шагов
  (Step 2–7):
  - Step 2 — real binary-backed
    `apply_config_from_files` contract (часть
    критерия приёмки 1 + 4 + 5);
  - Step 3 — real binary-backed
    `update_database_configuration` contract
    (полное закрытие критерия 1);
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3 + часть критерия 9);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
  По умолчанию каждый шаг (после Step 1) имеет
  собственный manual integration check вне проекта
  (`phase-tracka-stepN-check.py` или эквивалент по
  существующей конвенции `phase6_stepN_check.py`).
  dev-check остаётся зелёным после каждого
  кодового шага.

### Parallel Track A / Step 2 — real binary-backed `apply_config_from_files` contract (завершён)

- **Цель шага.** Перевести существующий public write-tool
  `apply_config_from_files(...)` с чисто stub-backed
  поведения на honest dual-mode contract — симметрично с
  тем, что Phase 6 / Step 2 сделал для
  `create_dump_snapshot(...)`. При наличии полного
  binary contract'а у environment'а (`onec_binary_path` +
  `onec_applycfg_command_template`) — реальный subprocess
  через `onec_process_runner.run_process`. При
  отсутствии — старое stub-backed поведение (Phase 2 /
  Step 7) **без изменений**. Runtime failure в
  binary-backed ветке = honest failure без silent
  fallback'а на stub. Закрывает часть критериев приёмки
  трека 1, 4, 5; полностью **не закрывает** критерий 1
  (Step 3 закроет оставшийся `update_database_configuration`)
  и **не закрывает** критерии 2, 3, 6, 7, 8, 9, 10
  (это работа Step 3–7 трека).
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` получил одно новое optional-поле
    `onec_applycfg_command_template: list[str] | None =
    None`. Default `None` сохраняет backward compatibility:
    Phase 1–6 конфиги без поля грузятся без изменений.
    Docstring расширен абзацем про Track A / Step 2 с
    явной фиксацией философии «platform does not invent
    1cv8 CLI grammar».
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` строго валидирует новое поле
    fail-closed: `None` или `non-empty list[str]`,
    остальное → `ValueError` с понятным сообщением.
    Mirror discipline уже-имеющегося
    `onec_dumpcfg_command_template` validation'а.
  - `packages/onec-config/README.md` — добавлен
    подраздел про новое поле (whitelist placeholders:
    `binary_path` / `source_dump_path` / `base_path` /
    `base_id` / `publication_name` / `http_base_url`) +
    усиленный абзац «Философия binary-related полей»
    (явно сказано «platform does not guess 1cv8 CLI
    grammar», «no shell strings», «unknown placeholder
    fail-closed на render-time»).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три module-level константы:
    `_APPLYCFG_TEMPLATE_PLACEHOLDERS` (frozenset
    из шести whitelisted имён),
    `_APPLYCFG_OUTPUT_EXCERPT_LIMIT = 1024`,
    `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS = 300`.
    Mirror констант, уже имеющихся для dumpcfg.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три приватных helper'а:
    `_render_applycfg_command(...)` (whitelisted
    placeholder substitution, fail-closed на unknown
    placeholder),
    `_build_apply_stub_callables(source_dump_path)`
    (возвращает `(operation, verify)` для legacy stub
    branch'а; обёртывает существующий
    `run_stub_apply_process` чтобы добавить Track A /
    Step 2 honest-mode поля без изменений в самом legacy
    stub helper'е),
    `_build_apply_binary_backed_callables(command,
    source_dump_path)` (возвращает `(operation,
    verify)` для binary-backed branch'а: operation
    спавнит subprocess через `run_process` с captured
    stdout/stderr, **всегда** возвращает dict с
    honest-mode полями; verify проверяет
    `completed=True, exit_code=0` и raise'ит
    `AssertionError` иначе — это и есть
    no-silent-fallback discipline).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `apply_config_from_files(...)` переписан как
    тонкий dispatcher: проверяет наличие обоих полей
    binary contract'а; при unknown placeholder в
    binary-backed branch'е возвращает `ok=False`
    **до** входа в `run_write_flow` (никаких
    snapshots, никаких audit rows для render-failed
    вызовов); при полном contract'е выбирает
    binary-backed callables; при отсутствии — stub
    callables; в обоих случаях идёт через
    `run_write_flow(...)` (preflight + snapshot +
    operation + verify + audit обязательны для обеих
    веток). Tool name результата возвращается через
    существующий `_with_tool_name` — `apply_config_from_files`,
    не внутреннее имя flow'а.
  - **Не тронуто.** `runtime/dump_ops.py` (legacy stub
    helper) не редактировался ни в одной строке — Track
    A / Step 2 обёртывает его, не переписывает.
    `create_dump_snapshot(...)` не редактировался —
    финальная унификация payload-discipline между
    тремя binary-backed write-tool'ами это работа Step
    4 трека. `update_database_configuration` не
    редактировался — это Step 3 трека. Никаких новых
    MCP tool'ов; никакого нового product-layer
    slice'а; никаких изменений в `mcp-read-server`,
    `mcp-intelligence-server`, `apps/platform/`,
    `onec-policy-engine`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
- **Operator-facing payload-контракт (симметрия с
  `create_dump_snapshot`).** В обоих режимах
  `operation_payload` несёт один и тот же набор полей:
  `mode ∈ {"stub", "binary-backed"}`, `binary_invoked: bool`,
  `exit_code: int | None`, `command_preview: list[str] |
  None`, `stdout_excerpt: str | None`,
  `stderr_excerpt: str | None`. Stub-режим эмитит `None`
  / `False` для тех полей, которые ему неприменимы;
  никакой магии, никакого скрытого поведения —
  оператор видит честную картину.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step2-check.py`
  прогоняет 7 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Все семь зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; `apply_config_from_files`
    в registry; никаких новых tool names не
    проскочило (полный whitelist 25 имён сравнён
    set'ом).
  - **B** — backward compatibility: env без
    `onec_applycfg_command_template` →
    `apply_config_from_files` работает в stub-режиме
    как раньше; `operation_payload.mode='stub'`,
    `binary_invoked=False`; legacy `apply-stub.txt`
    + `apply-meta.json` создаются в `source_dump_path`.
  - **C** — happy binary-backed path: env с binary
    contract'ом + operator-declared template'ом
    (`python -c <script>` + marker path); subprocess
    реально запускается; `mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    `command_preview` corretto; **operator-declared
    marker file** physically на диске (доказательство
    реального subprocess'а, не fake'а); legacy stub
    marker `apply-stub.txt` отсутствует в этом
    режиме.
  - **D** — binary-backed runtime failure (template
    exits 7): `ok=False`, `mode='binary-backed',
    binary_invoked=True, exit_code=7`,
    `stage='verify'`; `operation_payload`
    сохраняется (run_write_flow preserves it on
    verify-stage failures); legacy stub marker
    отсутствует — **никакого silent fallback'а**.
  - **E** — loader fail-closed на пять bad-shape
    вариантов (`"not a list"` / `[binary, 1, "-c"]`
    int item / `[]` empty / `[[binary, "-c"]]`
    nested list / `{"argv": [...]}` dict-not-list)
    — все пять `ValueError` с понятным сообщением.
    Positive control: `None` принимается loader'ом
    (legacy compat).
  - **F** — unknown placeholder (`{not_in_whitelist}`
    в template'е): tool возвращает `ok=False` **до**
    запуска subprocess'а; `binary_invoked=False`,
    `command_preview=None`; message содержит список
    allowed placeholders (`binary_path`,
    `source_dump_path`, ...); никакая `_snapshots`
    директория не создаётся.
  - **G** — integration через `run_write_flow`:
    standard flow shape preserved
    (`stage='completed'`, `operation_id`,
    `audit_path`, `backup_snapshot_path`,
    `dump_snapshot_path`, `operation_payload`,
    `verify_payload`); audit row пишется с
    `tool_name='apply_config_from_files'`,
    `status='ok'`; binary-backed branch реально
    отрабатывает (а не silent stub) —
    `operation_payload.mode='binary-backed'` +
    operator-declared marker physically на диске.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 2. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (`apply_config_from_files` уже там, не появился
  как новый), `intelligence_server_tools` — 16 имён
  без изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Пять шагов
  (Step 3–7):
  - Step 3 — real binary-backed
    `update_database_configuration` contract (полное
    закрытие критерия 1);
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 3 —
  real binary-backed `update_database_configuration`
  contract.** Симметричная Step 2 правка для второго
  оставшегося Phase 2 stub-backed-пути. Затрагиваемые
  зоны Step 3: точечно
  `apps/mcp-write-server/src/mcp_write_server/tools.py`
  (использовать helper'ы из Step 2 если они применимы;
  иначе мелкая duplication до Step 4 финальной
  унификации) + `packages/onec-config/` (одно новое
  optional-поле `onec_updatedb_command_template`).
  Read- и intelligence-серверы Step 3 не трогает.
  `onec_policy_engine` не трогает. Registries Step 3
  не растит — это та же операция с расширенным
  dispatch'ем.

### Parallel Track A / Step 3 — real binary-backed `update_database_configuration` contract (завершён)

- **Цель шага.** Перевести существующий public write-tool
  `update_database_configuration(...)` с чисто
  stub-backed поведения на honest dual-mode contract —
  симметрично с тем, что Step 2 трека сделал для
  `apply_config_from_files(...)` и Phase 6 / Step 2 для
  `create_dump_snapshot(...)`. При наличии полного
  binary contract'а у environment'а (`onec_binary_path`
  + `onec_updatedb_command_template`) — реальный
  subprocess через `onec_process_runner.run_process`.
  При отсутствии — старое stub-backed поведение
  (Phase 2 / Step 9) **без изменений**. Runtime failure
  в binary-backed ветке = honest failure без silent
  fallback'а на stub. Закрывает оставшуюся часть
  критерия приёмки 1 трека (после Step 2 закрылась
  apply-часть; теперь updatedb-часть тоже закрыта) и
  часть критериев 4 и 5. Полностью **не закрывает**
  критерии 2, 3, 6, 7, 8, 9, 10 (это работа Step 4–7
  трека).
- **Что реально появилось в коде.**
  - `packages/onec-config/src/onec_config/models.py` —
    `EnvironmentConfig` получил одно новое
    optional-поле `onec_updatedb_command_template:
    list[str] | None = None`. Default `None` сохраняет
    backward compatibility: Phase 1–6 + Track A / Step 2
    конфиги без поля грузятся без изменений. Docstring
    расширен абзацем про Track A / Step 3 с явной
    фиксацией философии «platform does not invent 1cv8
    CLI grammar» и tighter-whitelist (нет
    `{output_path}` / `{source_dump_path}` — UpdateDBCfg
    операционно работает на живой инфобазе).
  - `packages/onec-config/src/onec_config/loader.py` —
    `load_project_config` строго валидирует новое поле
    fail-closed: `None` или `non-empty list[str]`,
    остальное → `ValueError` с понятным сообщением.
    Mirror discipline уже-имеющихся
    `onec_dumpcfg_command_template` /
    `onec_applycfg_command_template` validation'ов.
  - `packages/onec-config/README.md` — добавлен
    подраздел про новое поле (whitelist placeholders:
    `binary_path` / `base_path` / `base_id` /
    `publication_name` / `http_base_url` — пять имён,
    более узкий surface, чем у dumpcfg / applycfg);
    раздел «Философия binary-related полей» обновлён
    под пять полей; явно зафиксирован принцип
    отсутствия premature generalization («Track A /
    Step 3 переводит на binary-backed dispatch
    **только** `update_database_configuration` —
    финальная унификация payload-discipline между
    всеми тремя binary-backed write-tool'ами это
    задача Track A / Step 4»).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три module-level константы:
    `_UPDATEDB_TEMPLATE_PLACEHOLDERS` (frozenset
    из пяти whitelisted имён, без `output_path` /
    `source_dump_path`), `_UPDATEDB_OUTPUT_EXCERPT_LIMIT
    = 1024`, `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS = 300`.
    Mirror констант, уже имеющихся для dumpcfg /
    applycfg.
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — добавлены три приватных helper'а:
    `_render_updatedb_command(...)` (whitelisted
    placeholder substitution через тот же
    `_PlaceholderProxy`-механизм, что у dumpcfg /
    applycfg; fail-closed на unknown placeholder с
    update-db-specific сообщением, перечисляющим
    `_UPDATEDB_TEMPLATE_PLACEHOLDERS`),
    `_build_updatedb_stub_callables()` (возвращает
    `(operation, verify)` для legacy stub branch'а;
    inline-логика стаба сохранена и обёрнута в
    Track A / Step 3 honest-mode поля без изменений в
    самих side-effect'ах stub'а — `.update-db-stub.txt`
    и `.update-db-meta.json` пишутся как раньше),
    `_build_updatedb_binary_backed_callables(command)`
    (возвращает `(operation, verify)` для
    binary-backed branch'а: operation спавнит
    subprocess через `run_process` с captured
    stdout/stderr, **всегда** возвращает dict с
    honest-mode полями; verify проверяет
    `completed=True, exit_code=0` и raise'ит
    `AssertionError` иначе — это и есть
    no-silent-fallback discipline).
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `update_database_configuration(...)` переписан
    как тонкий dispatcher: проверяет наличие обоих
    полей binary contract'а; при unknown placeholder в
    binary-backed branch'е возвращает `ok=False`
    **до** входа в `run_write_flow` (никаких snapshots,
    никаких audit rows для render-failed вызовов); при
    полном contract'е выбирает binary-backed
    callables; при отсутствии — stub callables; в
    обоих случаях идёт через `run_write_flow(...)`
    (preflight + snapshot + operation + verify + audit
    обязательны для обеих веток). Tool name
    результата возвращается через существующий
    `_with_tool_name` —
    `update_database_configuration`, не внутреннее имя
    flow'а.
  - **Не тронуто.** `apply_config_from_files(...)` уже
    переведён на Step 2 — здесь не редактировался ни в
    одной строке. `create_dump_snapshot(...)` тоже не
    редактировался — финальная унификация
    payload-discipline между всеми тремя
    binary-backed write-tool'ами это работа Step 4
    трека. Никаких новых MCP tool'ов; никакого
    нового product-layer slice'а; никаких изменений в
    `mcp-read-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
- **Operator-facing payload-контракт (симметрия с Step 2
  и Phase 6 / Step 2).** В обоих режимах
  `operation_payload` несёт один и тот же набор полей:
  `mode ∈ {"stub", "binary-backed"}`,
  `binary_invoked: bool`, `exit_code: int | None`,
  `command_preview: list[str] | None`,
  `stdout_excerpt: str | None`,
  `stderr_excerpt: str | None`. Stub-режим эмитит
  `None` / `False` для тех полей, которые ему
  неприменимы. Это тот же набор полей, который уже
  эмитят `create_dump_snapshot` (Phase 6 / Step 2) и
  `apply_config_from_files` (Track A / Step 2) —
  единый ментальный шаблон оператора «как читать
  binary-backed write payload».
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step3-check.py`
  прогоняет 7 сценариев на synthetic tempdir + local
  HTTPServer (gateway). Все семь зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а;
    `update_database_configuration` в registry; полный
    whitelist 25 имён сравнён set'ом — никаких новых
    tool names и никаких missing names.
  - **B** — backward compatibility: env без
    `onec_updatedb_command_template` →
    `update_database_configuration` работает в
    stub-режиме как раньше;
    `operation_payload.mode='stub',
    binary_invoked=False`; honest-mode поля
    `exit_code/command_preview/stdout_excerpt/stderr_excerpt`
    все `None`; legacy `.update-db-stub.txt` (`'updated'`)
    и `.update-db-meta.json` (`mode: "stub-update-db"`,
    `base_id: "local-dev"`) создаются в `dump_path`.
  - **C** — happy binary-backed path: env с binary
    contract'ом + operator-declared template'ом
    (`python -c <script>` + marker path); subprocess
    реально запускается; `mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    `command_preview` corretto (argv list с
    `sys.executable`); operator-declared marker file
    (`'updatedb ok'`) physically на диске
    (доказательство реального subprocess'а, не fake'а);
    legacy stub markers `.update-db-stub.txt` и
    `.update-db-meta.json` отсутствуют в этом
    режиме.
  - **D** — binary-backed runtime failure (template
    exits 7): `ok=False`, `mode='binary-backed',
    binary_invoked=True, exit_code=7`,
    `stage='verify'`; `operation_payload`
    сохраняется (run_write_flow preserves it on
    verify-stage failures); legacy stub markers
    отсутствуют — **никакого silent fallback'а**.
  - **E** — loader fail-closed на семь bad-shape
    вариантов (`"not a list"` / `[bin, 1, "-c"]` int
    item / `[bin, True, "-c"]` bool item /
    `[bin, {"k": "v"}, "-c"]` dict item / `[]` empty /
    `[[bin, "-c"]]` nested list / `{"argv": [...]}`
    dict-not-list) — все семь `ValueError` с понятным
    сообщением. Positive controls: `None` принимается
    loader'ом (legacy compat); valid `[bin, "-c",
    "pass"]` сохраняется как
    `EnvironmentConfig.onec_updatedb_command_template`.
  - **F** — unknown placeholder
    (`{not_in_whitelist}` в template'е): tool
    возвращает `ok=False` **до** запуска
    subprocess'а; `binary_invoked=False`,
    `command_preview=None`; message содержит список
    allowed placeholders (`binary_path`, `base_id`,
    ...); никакая `_snapshots` директория не
    создаётся. **Дополнительно:**
    `{output_path}` и `{source_dump_path}` (которые
    в whitelist'е dumpcfg / applycfg, но **не** в
    update-db whitelist'е) тоже отвергнуты —
    подтверждает tighter-whitelist для UpdateDBCfg.
  - **G** — integration через `run_write_flow`:
    standard flow shape preserved
    (`stage='completed'`, `operation_id`,
    `audit_path`, `backup_snapshot_path`,
    `dump_snapshot_path`, `operation_payload`,
    `verify_payload`); audit row пишется с
    `tool_name='update_database_configuration'`,
    `status='ok'`; binary-backed branch реально
    отрабатывает (а не silent stub) —
    `operation_payload.mode='binary-backed'` +
    operator-declared marker physically на диске.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 3. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (`update_database_configuration` уже там, не
  появился как новый), `intelligence_server_tools` —
  16 имён без изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Четыре шага
  (Step 4–7):
  - Step 4 — unify / finish `create_dump_snapshot`
    real path + payload discipline (полное закрытие
    критерия 5 трека; финальная унификация helper'ов
    между всеми тремя binary-backed write-tool'ами);
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 4 —
  unify / finish `create_dump_snapshot` real path +
  payload discipline.** Задача — привести
  payload-поля и shared helper'ы к одному
  contract'у между тремя binary-backed write-tool'ами
  (`create_dump_snapshot`, `apply_config_from_files`,
  `update_database_configuration`). Решает Q3
  открытого вопроса Step 1 плана: где живут shared
  helper'ы (новый module `runtime/process_dispatch.py`
  или private helpers внутри `tools.py`). Затрагиваемые
  зоны Step 4: точечно
  `apps/mcp-write-server/src/mcp_write_server/`
  (рефакторинг внутрь, **не** наружу — operator-
  declared контракт не ломается; placeholders
  остаются те же; argv-grammar остаётся та же).
  Read-, intelligence- и product-серверы Step 4 не
  трогает. Registries Step 4 не растит.

### Parallel Track A / Step 4 — unify / finish create_dump_snapshot real path + payload discipline (завершён)

- **Цель шага.** Закрыть Q3 открытого вопроса Step 1
  плана трека (где живут shared helper'ы) и привести
  внутреннюю реализацию трёх binary-backed write-tool'ов
  (`create_dump_snapshot`, `apply_config_from_files`,
  `update_database_configuration`) к единой shared
  internal-only mechanic'е без расширения surface'а,
  без новых MCP tool'ов, без изменений operator-facing
  argv grammar / placeholder whitelist'ов / ToolResult
  shape. Также — закрыть payload-discipline gap у
  `create_dump_snapshot` (несколько ветвей до Step 4
  не несли всех шести honest-mode полей).
- **Что реально появилось в коде.**
  - **Новый internal-only module:**
    `apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`
    (~280 строк). Не public API, не registered MCP
    tool, не product-layer surface — используется
    только тремя public binary-backed write-tool'ами и
    больше никем. Содержит:
    - `BINARY_OUTPUT_EXCERPT_LIMIT = 1024` — единая
      константа cap'а excerpt'ов;
    - `BINARY_DEFAULT_TIMEOUT_SECONDS = 300` — единый
      default timeout subprocess invocation;
    - `UnknownPlaceholderError` /
      `PlaceholderProxy` — внутренняя механика
      placeholder substitution (раньше жила в
      `tools.py` под underscore-prefix именами);
    - `excerpt(text)` — единый excerpt cap helper;
    - `render_command_template(template, *,
      substitutions, allowed_placeholders,
      template_field_name)` — generic placeholder
      substitution engine. **Whitelist остаётся
      per-tool**: каждый tool передаёт свой
      `allowed_placeholders` set + свой
      `template_field_name` для error message;
    - `stub_honest_mode_fields()` — возвращает unified
      dict шести honest-mode полей для stub-branch'а
      (`mode='stub'`, `binary_invoked=False`,
      остальные четыре `None`);
    - `binary_backed_render_failure_fields()` — для
      случая render-fail до spawn'а
      (`binary_invoked=False`, `command_preview=None`);
    - `binary_backed_start_failure_fields(command)` —
      для случая `PlatformError` от runner'а
      (`binary_invoked=False`, но `command_preview`
      есть);
    - `binary_backed_payload_fields(command,
      process_result)` — для случая, когда subprocess
      реально отработал (`binary_invoked=True`,
      все шесть полей populated, плюс ещё
      `completed` 7-м полем для shape verify check);
    - `is_binary_subprocess_successful(payload)` —
      единый shape verify helper
      (`completed && exit_code == 0`);
    - `honest_mode_keys() -> tuple[str, ...]` —
      utility для тестов / документации.
  - **Refactor `tools.py`:**
    - Удалены три duplicated константы
      `_DUMPCFG_OUTPUT_EXCERPT_LIMIT` /
      `_APPLYCFG_OUTPUT_EXCERPT_LIMIT` /
      `_UPDATEDB_OUTPUT_EXCERPT_LIMIT` (все три =
      1024) — теперь единый
      `BINARY_OUTPUT_EXCERPT_LIMIT` в
      `binary_dispatch`.
    - Удалены три duplicated константы
      `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS` /
      `_APPLYCFG_DEFAULT_TIMEOUT_SECONDS` /
      `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS` (все три =
      300) — теперь единый
      `BINARY_DEFAULT_TIMEOUT_SECONDS` в
      `binary_dispatch`.
    - Удалены `_PlaceholderProxy`,
      `_UnknownPlaceholderError`, `_excerpt` из
      `tools.py` — переехали в `binary_dispatch`.
    - Три `_render_*_command` стали тонкими
      tool-specific wrapper'ами вокруг shared
      `render_command_template`. Каждый передаёт свой
      substitutions dict + свой whitelist + свой
      template field name. **Whitelistы остаются
      per-tool** (намеренно, не объединены в superset):
      6 имён у dumpcfg, 6 имён у applycfg, 5 имён у
      updatedb (tighter — без `output_path` /
      `source_dump_path`).
    - Stub-branch payloads трёх tool'ов теперь
      spread'ят `**stub_honest_mode_fields()` вместо
      inline-копии шести `None` / `False`.
    - Binary-backed-branch payloads трёх tool'ов
      теперь spread'ят
      `**binary_backed_payload_fields(command,
      process_result)` вместо inline-копии семи
      полей.
    - Render-failure payloads (`apply` /
      `update_database_configuration` диспетчеры,
      `create_dump_snapshot` binary-backed branch)
      используют `**binary_backed_render_failure_fields()`.
    - Start-failure payload (`create_dump_snapshot`
      `PlatformError` ветка) использует
      `**binary_backed_start_failure_fields(command)`.
    - Verify callable'ы apply / updatedb используют
      общий `is_binary_subprocess_successful(...)`
      predicate.
  - **Закрытие payload-discipline gap у
    `create_dump_snapshot`.** До Step 4 dump-snapshot
    stub branch (success path, render-fail path,
    PlatformError-fail path, dump-meta-fail path,
    mkdir-fail path) и binary-backed branch
    (render-fail path, mkdir-fail path,
    internal-defensive-check path) **не несли** всех
    шести honest-mode полей: некоторые ветки имели
    только `mode` + `binary_invoked` + tool-specific
    extras, без `exit_code` / `command_preview` /
    `stdout_excerpt` / `stderr_excerpt`. Step 4
    закрыл этот gap — теперь **каждая** ветка
    **каждого** из трёх binary-backed write-tool'ов
    несёт все шесть полей честно (`None` / `False` где
    не применимо, populated в binary-backed success).
- **Что НЕ тронуто.**
  - **Operator-facing surface:** argv grammar,
    placeholder whitelistы (per-tool), ToolResult
    shape, public tool names, registry counts,
    behaviour Step 2 (apply) и Step 3 (updatedb) —
    всё без изменений.
  - **Legacy stub helpers:** `runtime/dump_ops.py`
    (для apply) не тронут — Track A / Step 2 обёртывал
    его, Step 4 не вмешивается. Stub-логика для
    update-db (inline в `tools.py`) и stub-логика для
    `create_dump_snapshot` в принципе сохранили свои
    side-effect'ы (legacy markers / meta files); Step 4
    только нормализовал payload shape вокруг них.
  - **Whitelist placeholders НЕ объединены в superset.**
    Каждый tool сохранил свой собственный whitelist —
    это намеренное анти-расползание surface'а.
  - **`packages/onec-config/` не тронут.** Step 4 —
    refactor внутри write-server, новых config
    surface'ов не добавляет.
  - **Никакого generic helper framework "для всех
    будущих binary-backed write-tools".** Module
    `binary_dispatch` обслуживает ровно три текущих
    binary-backed-tool'а; расширять его surface впрок
    — не задача Step 4.
  - **Никаких новых MCP tool'ов** (registries
    `read=15 / write=25 / intelligence=16` строго
    сохранены).
  - Никаких изменений в `mcp-read-server`,
    `mcp-intelligence-server`, `apps/platform/`,
    `onec-policy-engine`, `onec-audit`,
    `onec-health`, `onec-process-runner`,
    `onec-troubleshooting`, `mcp-common`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`.
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step4-check.py`
  прогоняет 10 сценариев на synthetic tempdir + local
  HTTPServer. Все десять зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; полный whitelist 25
    имён сравнён set'ом — никаких новых tool names
    или missing names.
  - **J** — sanity check shared module: `honest_mode_keys()`
    возвращает ровно шесть имён brief'а;
    `BINARY_DEFAULT_TIMEOUT_SECONDS == 300`;
    `BINARY_OUTPUT_EXCERPT_LIMIT == 1024`.
  - **B** — `create_dump_snapshot` stub branch без
    binary contract'а: `ok=True, mode='stub',
    binary_invoked=False`; legacy
    `dump-created.txt` + `dump-meta.json` markers
    создаются; **все шесть honest-mode полей
    присутствуют** — это gap, закрытый Step 4.
  - **C** — `create_dump_snapshot` binary-backed
    happy path: `ok=True, mode='binary-backed',
    binary_invoked=True, exit_code=0`;
    operator-declared marker physically на диске.
  - **D** — `create_dump_snapshot` binary-backed
    runtime failure (template exits 7): `ok=False,
    mode='binary-backed', binary_invoked=True,
    exit_code=7`; никакого silent fallback'а.
  - **E** — `apply_config_from_files` regression
    через refactor: 4 sub-сценария (E1 stub / E2
    happy binary / E3 binary fail / E4 unknown
    placeholder) — все ведут себя как и до Step 4.
  - **F** — `update_database_configuration`
    regression через refactor: 4 sub-сценария
    (F1 stub / F2 happy binary / F3 binary fail /
    F4 tighter whitelist — `{output_path}` +
    `{source_dump_path}` отвергаются для updatedb,
    подтверждает что whitelist'ы остались per-tool).
  - **G** — payload shape parity: для всех трёх
    public tools во всех трёх ветках (stub success,
    binary-backed success, binary-backed fail)
    payload содержит **все шесть** unified
    honest-mode keys.
  - **H** — integration через `run_write_flow`: один
    mutating call для каждого из трёх tool'ов;
    standard flow shape (stage='completed',
    operation_id, audit_path, snapshot refs) для
    apply / updatedb (которые идут через
    run_write_flow); audit row пишется с правильным
    tool_name; binary-backed branch реально
    отрабатывает (verified через
    operation_payload.mode + operator-declared marker
    на диске).
  - **I** — render-time rejection short-circuit для
    apply и updatedb: unknown placeholder →
    `ok=False` **до** subprocess'а;
    `binary_invoked=False`; `command_preview=None`;
    `_snapshots/` директория не создаётся.
- **dev-check.** `scripts/dev/run_dev_check.ps1`
  остаётся зелёным после Step 4. Вывод последнего
  прогона: `imports_ok = true`,
  `read_server_tools` — 15 имён без изменений,
  `write_server_tools` — 25 имён без изменений
  (никакого drift'а surface'а),
  `intelligence_server_tools` — 16 имён без
  изменений, `selfcheck_status = ok`,
  `Dev check completed successfully.`. `selfcheck.py`,
  `bootstrap_paths.ps1`, `pyproject.toml`,
  `.github/` не тронуты.
- **Что осталось до закрытия Track A.** Три шага
  (Step 5–7):
  - Step 5 — product-layer integration через
    существующие boundary'и без правок их логики
    (критерий 3 трека);
  - Step 6 — reference stand multi-step round-trip с
    настоящим 1cv8 binary'ом (критерий 2 трека);
  - Step 7 — final integration pass + закрытие трека
    (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 5 —
  product-layer integration over real write path** —
  закрыт (см. ниже).

### Parallel Track A / Step 5 — product-layer integration over real write path (завершён)

- **Цель шага.** Закрыть Q7 и Q8 открытых вопросов
  Step 1 плана трека: привести surface двух
  product-layer boundary'ев (`run_real_stand_smoke_test`
  и `inspect_enterprise_foundation`) к honest состоянию
  после того, как Track A / Steps 2–4 уже дали real
  binary-backed write contract всем трём binary-backed
  write-tool'ам в `mcp-write-server`. Само Track A
  Steps 2–4 жили внутри write-server'а; Step 5 — это
  **surface-only** product-layer update, не кодовый
  back-port внутрь write-server'а и не новый
  MCP-tool slice.
- **Что реально появилось в коде.**
  - **`apps/platform/src/onec_platform/enterprise.py`
    (Q8 closure).** В `_check_real_stand_contract`
    раньше score жил в диапазоне 0..2 и проверял только
    `onec_binary_path` + `onec_dumpcfg_command_template`.
    Теперь функция симметрично проверяет все три
    command template'а (dumpcfg / applycfg / updatedb)
    рядом с binary path; score range расширен до 0..4.
    На prod-like config'ах отсутствие любого из трёх
    template'ов превращается в **error** finding
    с code'ами `foundation_onec_applycfg_template_missing_on_prod`
    / `foundation_onec_updatedb_template_missing_on_prod`
    (симметрично уже существовавшему
    `foundation_onec_dumpcfg_template_missing_on_prod`)
    и соответствующим recommended-action'ом, перечисляющим
    placeholder whitelist per-tool. На non-prod —
    presumed warning'и `foundation_onec_<op>_template_missing`
    (без error'ов и без блокировки `ok=True`). При
    полном contract'е (binary + 3 template'а) появляется
    presumed-finding `foundation_real_write_path_contract_complete`;
    при только `binary + dumpcfg` сабсете — старое
    `foundation_real_stand_smoke_contract_available`
    остаётся как валидный fallback advisory (now in an
    `elif` branch). `_SECTION_MAX_SCORE['binary']`
    поднят с 2 до 4. Логика
    `_classify_foundation_level` без изменений —
    `'strong'` автоматически требует full contract
    в section D, потому что `max_total = sum(...)`
    учитывает обновлённый максимум. Docstring
    `inspect_enterprise_foundation` дополнен
    параграфом про Track A integration.
  - **`apps/platform/src/onec_platform/realstand.py`
    (Q7 closure).** В `_build_plan_summary` удалена
    stale advisory строка «Phase 2 stubs … are NOT
    rewritten on this step — that is a parallel
    track». Вместо неё — три новых блока: (1) три
    binary-backed write-tool'а названы по имени
    (`create_dump_snapshot`, `apply_config_from_files`,
    `update_database_configuration`) с явным
    указанием honest dual-mode контракта через unified
    internal `binary_dispatch` helper после Track A /
    Steps 2–4; (2) явное напоминание оператору, что
    smoke сам по себе остаётся **bounded probe** и
    **не** chain'ит dump → apply → updatedb на
    реальном binary'е (multi-step round-trip — это
    Track A / Step 6, не данный surface); (3)
    подтверждение, что infobase не мутируется и
    никакие MCP write-tool'ы из smoke не вызываются.
    Module-docstring `realstand.py` обновлён
    симметрично: «не переписывает Phase 2 stub'ы»
    заменено на честное описание Track A history +
    bounded-probe boundary. В package-docstring'е
    `apps/platform/src/onec_platform/__init__.py`
    Step 7-блок тоже обновлён: убрана фраза «no
    Phase 2 stub … is rewritten — flipping those
    onto a binary-backed branch is a parallel
    track»; вместо неё — Track A-aware
    формулировка.
- **Что НЕ тронуто.**
  - **Никаких изменений** в `apps/mcp-write-server/`
    (binary-backed dispatch уже был там после
    Step 2–4 трека), в `apps/mcp-read-server/`,
    `apps/mcp-intelligence-server/`,
    `packages/onec-policy-engine/`,
    `packages/onec-config/` (full contract уже
    был добавлен в EnvironmentConfig после Track A
    Steps 2–3 — Step 5 только начал **использовать**
    его в product surface'е), `packages/onec-audit/`,
    `packages/onec-health/`, `packages/onec-process-runner/`,
    `packages/onec-troubleshooting/`,
    `packages/mcp-common/`, `selfcheck.py`,
    `bootstrap_paths.ps1`, `pyproject.toml`,
    `.github/`, `.claude.json`.
  - **Никаких новых product-layer boundary'ев.**
    Все правки — внутри двух уже существующих
    функций (`run_real_stand_smoke_test`,
    `inspect_enterprise_foundation`).
  - **`RealStandSmokeResult` и `EnterpriseFoundationResult`
    shape'ы** — без изменений (те же dataclass-поля,
    те же `_from_json_file` варианты). Добавились
    только новые finding-code'ы на готовых списках
    `confirmed_findings` / `presumed_findings` и
    новые recommended-action'ы.
  - **Operator-facing argv grammar / placeholder
    whitelist'ы per-tool / public ToolResult
    shape** — без изменений.
  - **Никаких новых MCP tool'ов** (registries
    `read=15 / write=25 / intelligence=16` строго
    сохранены).
  - **Никакого back-door write channel'а** из
    продуктового слоя: Step 5 ничего не пишет на
    диск, не зовёт `run_write_flow`, не открывает
    subprocess'ы — это **surface-only** update.
  - **`onec_policy_engine` не импортируется** ни
    из `apps/platform/src`, ни из
    `apps/mcp-intelligence-server/src` (отдельно
    проверено сканированием в manual-check
    сценарии G).
- **Manual verification.** Скрипт
  `C:/Users/user/AppData/Local/Temp/phase-tracka-step5-check.py`
  прогоняет 7 сценариев (с раскрытием C на четыре
  под-кейса). Все зелёные:
  - **A** — registry invariants `read=15 / write=25 /
    intelligence=16` без drift'а; полный whitelist 25
    write-имён сравнён set'ом — никаких новых tool
    names или missing names.
  - **B** — backward compatibility: Step 1–4
    product-config (без apply/updatedb template'ов)
    загружается через `inspect_enterprise_foundation`
    с `ok=True`; missing apply/updatedb template'ы
    surface'ятся как presumed warnings
    (`foundation_onec_applycfg_template_missing` /
    `foundation_onec_updatedb_template_missing`); ни
    один из новых `*_missing_on_prod` error code'ов
    не fire'ится.
  - **C1** — enterprise section absent →
    `foundation_level='absent'`,
    `ready_for_enterprise_track=False`.
  - **C2** — только dumpcfg на prod-like → applycfg
    и updatedb missing-on-prod errors,
    `binary=2/4`, `foundation_level != 'strong'`,
    recommended_actions содержат строки про оба
    отсутствующих template'а.
  - **C3** — dumpcfg + applycfg, без updatedb на
    prod-like → updatedb missing-on-prod error
    fire'ится, applycfg missing-on-prod НЕ fire'ится,
    `binary=3/4`, `foundation_level != 'strong'`;
    presumed `foundation_real_write_path_contract_complete`
    ещё не выставлено.
  - **C4** — full contract на prod-like + чистые
    остальные секции (identity / operability /
    traceability) → `binary=4/4`, presumed
    `foundation_real_write_path_contract_complete`
    fire'ится; `foundation_real_stand_smoke_contract_available`
    НЕ fire'ится (это else-branch);
    `foundation_level='strong'`,
    `ready_for_enterprise_track=True`, ноль
    error finding'ов.
  - **D** — real-stand smoke advisory: plan_summary
    упоминает все три binary-backed tool'а
    (`create_dump_snapshot` / `apply_config_from_files`
    / `update_database_configuration`), Track A /
    Steps 2–4, dual-mode contract, bounded probe
    semantics, multi-step round-trip принадлежит
    Track A / Step 6; запрещённые устаревшие фразы
    («Phase 2 stubs», «are NOT rewritten», fake
    chain claims) отсутствуют.
  - **E** — broken JSON paths: оба
    `*_from_json_file` boundary'я возвращают
    `ok=False` без exception'ов — и на
    несуществующем path'е (foundation_rejected /
    mode='rejected'), и на синтаксически битом JSON'е.
  - **F** — suggested-tools discipline: имена в
    `EnterpriseFoundationResult.suggested_tools` /
    `suggested_write_tools` и
    `RealStandSmokeResult.suggested_tools` /
    `suggested_write_tools` все принадлежат union'у
    live registries +
    `_KNOWN_PLATFORM_FUNCTIONS`; made-up имя
    отвергается `_allow_only_real_tools`.
  - **G** — нулевой импорт `onec_policy_engine`
    под `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/`
    (сканирование 26 `.py`-файлов, 0 offender'ов).
- **dev-check.** `scripts/dev/selfcheck.py`
  остаётся зелёным после Step 5 (`imports_ok = true`,
  `read_server_tools` 15 имён без изменений,
  `write_server_tools` 25 имён без изменений,
  `intelligence_server_tools` 16 имён без
  изменений, `selfcheck_status = ok`).
- **Что осталось до закрытия Track A.** Два шага
  (Step 6–7):
  - Step 6 — reference stand multi-step round-trip
    с настоящим 1cv8 binary'ом (real DumpCfg →
    real apply (LoadCfg) → real UpdateDBCfg на
    reference stand'е, фиксируется как
    воспроизводимый runbook; критерий 2 трека);
  - Step 7 — final integration pass + закрытие
    трека (критерии 6, 7, 8, 9, 10).
- **Следующий шаг.** **Parallel Track A / Step 6 —
  reference stand multi-step round-trip** — открыт
  частично (см. ниже). Не закрыт.

### Parallel Track A / Step 6 — reference stand multi-step round-trip (закрыт honestly)

- **Цель шага.** Подтвердить на **реальном** 1cv8 binary
  и **реальной** инфобазе связный сценарий
  `create_dump_snapshot` → `apply_config_from_files` →
  `update_database_configuration`, где все три tool'а
  идут по binary-backed branch'у с
  `mode='binary-backed'`, `binary_invoked=True`,
  `exit_code=0`, без silent fallback'а на stub. Это
  **operator-driven exercise** на reference stand'е;
  Step 6 **не** добавляет MCP tool'ов, **не**
  расширяет registries, **не** требует production-
  правок (dual-mode contract уже введён Steps 2–4,
  product-layer surface уже обновлён Step 5).
- **Что реально появилось.**
  - **Один новый runbook:**
    `docs/runbooks/track-a-reference-stand-round-trip.md`
    — operator-reproducible инструкция: цель, prereq'ы
    (real binary, real infobase, DESIGNER credentials,
    source dump, опциональный gateway), reference
    stand assumptions, точная последовательность
    шагов A.1–A.6 через public write-server tools
    (`mcp_write_server.tools.create_dump_snapshot`
    → `apply_config_from_files` →
    `update_database_configuration`) с примерами
    operator-declared template'ов
    (`/F`, `/N`, `/P`, `/DumpCfg`,
    `/LoadConfigFromFiles`, `/UpdateDBCfg`,
    `/DisableStartupMessages`), критерии «реально
    пошло binary-backed» (`mode`, `binary_invoked`,
    `exit_code`, `command_preview`), пять типовых
    failure cases (missing binary contract / unknown
    placeholder / non-zero exit / stand unavailable /
    silent stub fallback), список ожидаемых
    артефактов (`_snapshots/<id>/Configuration.xml`,
    `audit.jsonl` с тремя `operation_id`-ами,
    шесть unified honest-mode полей в каждом payload),
    что доказывает / не доказывает успешный
    round-trip.
  - **Один новый manual-verification скрипт:**
    `C:/Users/user/AppData/Local/Temp/phase-tracka-step6-prereq-inventory.py`
    — operator-runnable prereq inventory. Шесть
    блоков проверок (P1 registry invariants,
    P2 1cv8 binary discovery, P3 render-pipeline для
    всех трёх template'ов, P4 placeholder whitelist
    enforcement negative, P5 reference stand
    artifacts, P6 discipline asserts).
    Скрипт **не** запускает 1cv8.exe, **не**
    создаёт subprocess'ов — это honest static
    inventory. Exit codes: `0` все prereq'ы готовы,
    `1` partial (binary OK, stand prereq'ы missing),
    `2` discipline broken.
  - **Никаких production-правок.** Полный список
    untouched зон: `apps/mcp-read-server/`,
    `apps/mcp-write-server/`, `apps/mcp-intelligence-server/`,
    `apps/platform/`, `packages/mcp-common/`,
    `packages/onec-process-runner/`,
    `packages/onec-policy-engine/`,
    `packages/onec-audit/`, `packages/onec-health/`,
    `packages/onec-troubleshooting/`,
    `packages/onec-config/`, `scripts/`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`.
- **Результат прогона prereq-inventory в текущем
  dev-окружении.**
  - **P1 — registry invariants: PASS.** read=15,
    write=25, intelligence=16 без drift'а после
    Step 6.
  - **P2 — 1cv8 binary discovery: PASS.** Найдены два
    реальных DESIGNER-capable binary'я:
    - `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`
      (1.8 MB, file=True, executable_like=True)
    - `C:/Program Files (x86)/1cv8/8.3.27.1936/bin/1cv8.exe`
      (1.5 MB, file=True, executable_like=True)
  - **P3 — render-pipeline: PASS.** Все три
    template'а (dumpcfg / applycfg / updatedb) с
    реальным binary path'ом и synthetic placeholder
    values корректно рендерятся через
    `runtime/binary_dispatch.render_command_template`
    в 11-аргументный subprocess argv (без `subprocess`,
    без shell). Это unit-style проверка render-
    pipeline'а, не реальный invocation 1cv8.
  - **P4 — placeholder whitelist enforcement: PASS.**
    Unknown placeholder отвергается `ValueError`-ом
    **до** старта subprocess'а во всех трёх tool'ах
    (с `binary_invoked=False`,
    `command_preview=None`). Tighter whitelist у
    updatedb честно отвергает `{output_path}` и
    `{input_path}` (которые валидны для dumpcfg /
    applycfg).
  - **P5 — reference stand artifacts: MISSING (×4).**
    - `P5.a` MISSING: ноль declared product-config'ов
      с full real-write contract'ом в `examples/`
      или в корне репо (grep по `onec_binary_path` +
      три template'а). Оператор должен
      материализовать config по runbook'у.
    - `P5.b` MISSING: `examples/demo-infobase/`
      пуст — нет реальной целевой инфобазы для
      `base_path`.
    - `P5.c` MISSING: `examples/demo-dumps/`
      пуст — нет source dump tree для apply шага.
    - `P5.d` MISSING:
      `ONEC_DESIGNER_USER` / `ONEC_DESIGNER_PASSWORD`
      env vars не выставлены — DESIGNER credentials
      out-of-band.
  - **P6 — discipline asserts: PASS.** Ноль реальных
    импортов `onec_policy_engine` под
    `apps/platform/src/` и
    `apps/mcp-intelligence-server/src/`.
  - **Verdict prereq-inventory'я в исходном dev-окружении
    был partial (real 1cv8 binary present + render-pipeline
    OK, но stand prereq'ы missing).** Это была честная
    остановка по контракту шага. Позже, когда оператор
    подготовил InfoBase6 + DESIGNER credentials через
    local-only writable config (`%TEMP%/infobase6-writable.config.json`,
    cleartext, never committed), real multi-step round-trip
    был выполнен и Step 6 закрыт honestly — см. блок
    «Step 6 closure on InfoBase6» ниже.
- **Step 6 closure on InfoBase6.**
  - Operator-driven round-trip A.1–A.6 прошёл на real
    1cv8 binary'е (8.3.27.1859) и real file-based
    инфобазе `C:/Users/user/Documents/InfoBase6` через
    local-only writable config с DESIGNER credentials
    out-of-band (cleartext в `%TEMP%`, никогда не
    коммитится).
  - **A.2** `create_dump_snapshot` через
    `/DumpConfigToFiles`: `mode='binary-backed'`,
    `binary_invoked=True`, `exit_code=0`, snapshot tree
    физически на диске под
    `examples/demo-dumps/_snapshots/dump-infobase6-file-step6-A2-...`.
  - **A.4** `apply_config_from_files` через
    `/LoadConfigFromFiles`: `stage='completed'`,
    `mode='binary-backed'`, `exit_code=0`, mutating
    audit row написан с `details.dump_snapshot_path=...`
    указывающим на pre-apply snapshot, созданный
    `run_write_flow`'ом.
  - **A.5** `update_database_configuration` через
    `/UpdateDBCfg`: `stage='completed'`,
    `mode='binary-backed'`, `exit_code=0`, mutating
    audit row написан с `details.dump_snapshot_path=...`
    указывающим на pre-updatedb snapshot.
  - Audit honest по факту: `examples/demo-dumps/infobase6/.audit/audit.jsonl`
    содержит **ровно 2** append-only row'и (для A.4 и
    A.5), не три. Standalone `create_dump_snapshot`
    audit row не пишет by design — он не идёт через
    `run_write_flow`; pre-mutating dump подтверждается
    через `details.dump_snapshot_path` mutating row'и.
    Это намеренная архитектура `runtime/flow.py`
    (snapshot stage запускает internal
    `create_dump_snapshot` без отдельного audit-write,
    success_details mutating row'и захватывает
    `dump_snapshot_path`).
  - **Doc/expectation cleanup без code change.**
    Runbook
    `docs/runbooks/track-a-reference-stand-round-trip.md`
    обновлён в трёх местах: A.2 артефакты, A.6
    post-check item 4, раздел «Ожидаемый минимум
    артефактов» — все три места теперь говорят про
    «две audit row для двух mutating операций +
    `details.dump_snapshot_path`», не про «три audit
    row». Local-only закрытие logic в
    `%TEMP%/infobase6-step6-chain.py` (post-check
    блок A.6) переписан под honest expectation:
    `required = {"apply_config_from_files",
    "update_database_configuration"}` плюс проверка
    `details.dump_snapshot_path` в каждой mutating
    row'е.
  - **Production-кода Step 6 не правил.** `apps/`,
    `packages/`, registries, `examples/demo-infobase/infobase6.config.json`
    (repo candidate config без credentials),
    selfcheck — без изменений. Все правки локализованы
    в repo runbook'е + local-only chain script'е.
- **Что НЕ сделано (намеренно).**
  - **Не запускался synthetic round-trip через
    `sys.executable`.** Step 4 manual-check уже
    подтвердил binary-backed branch на synthetic
    binary'е (`sys.executable` плюс fake marker
    script); Step 6 **должен** быть real или
    partial, third option'а нет.
  - **Не запускался реальный 1cv8.exe** даже с
    headless probe argv'ом. На пустой пробе
    (`/?`) 1cv8.exe открывает GUI dialog (это
    воспроизведено и убито вручную); запуск без
    осмысленной операции по reference stand'у
    был бы тратой ресурсов и потенциально GUI-
    blocker'ом.
  - **Не сгенерирована демо-инфобаза.** Это
    operator-task: invocation `/CreateInfobase`
    запросов и flag'ов выходит за honest рамки
    Step 6 (платформа binary-CLI семантику не
    угадывает, см. Step 7 README); кроме того,
    development-окружение ограничено `\sandbox`-
    профилем без elevated privileges на
    1cv8 install dir.
  - **Не тронут `apps/mcp-write-server/README.md`.**
    Step 6 не меняет write-server surface; ничего
    нового write-server'у сообщить.
- **dev-check.** `scripts/dev/selfcheck.py`
  остаётся зелёным после Step 6 (никакой
  production-код не правился).
  `imports_ok = true`, `read_server_tools` 15 имён,
  `write_server_tools` 25 имён, `intelligence_server_tools`
  16 имён, `selfcheck_status = ok`.
- **Что осталось до закрытия Track A.** Только
  Step 7 — final integration pass + закрытие трека
  (документационный pass).
- **Следующий шаг.** **Parallel Track A / Step 7 —
  final integration pass and Track A closure** —
  открыт сразу после honest closure'а Step 6, не
  потребовал новых binary runs.

### Parallel Track A / Step 7 — final integration pass and Track A closure (закрыт)

- **Цель шага.** Зафиксировать closure всего
  Parallel Track A после того, как Step 6 уже
  отработал honestly на real 1cv8 + real
  InfoBase6: подтвердить, что Track A acceptance
  criteria 1–10 закрыты existing evidence'ом, и
  обновить README/PROJECT-STATUS под closed status.
  По step-map'у это закрывающий, по сути
  documentation-only шаг (по аналогии с
  Phase 5 / Step 8 и Phase 6 / Step 9 final
  integration pass'ами).
- **Никаких новых binary-backed запусков.** Step 7
  целенаправленно **не** перезапускал A.2 / A.4 /
  A.5 — это было бы расточительным повторным
  использованием ресурсов и противоречило бы
  принципу «closure на already proven evidence»;
  все необходимые артефакты от Step 6 уже на диске:
  - `examples/demo-dumps/_snapshots/` — 7 dump
    snapshot директорий (A.2 + A.2 retries +
    A.4 pre-apply + A.5 pre-updatedb);
  - `C:/Users/user/Documents/_snapshots/` —
    2 backup snapshot'а (pre-apply + pre-updatedb);
  - `examples/demo-dumps/infobase6/.audit/audit.jsonl`
    — две append-only mutating audit row'и (A.4 +
    A.5), обе со `status='ok'` и populated
    `details.dump_snapshot_path`.
- **Closure-check на existing evidence.** Read-only
  прогон против уже существующего `audit.jsonl`
  (без вызовов `create_dump_snapshot` /
  `apply_config_from_files` /
  `update_database_configuration`) подтвердил все
  acceptance criteria:
  - **AC 1** (full real binary-backed contract для
    всех трёх write-tool'ов) — закрыт production
    code'ом Steps 2–4: dual-mode dispatcher в
    `tools.py`, unified `binary_dispatch` helper,
    per-tool placeholder whitelists.
  - **AC 2** (multi-step real round-trip на
    reference stand) — закрыт Step 6 evidence'ом
    на InfoBase6.
  - **AC 3** (product-layer integration over real
    write path) — закрыт Step 5 surface'ом и
    подтверждён Step 6 round-trip'ом (A.4 / A.5
    шли через `run_write_flow` со всеми его
    стадиями preflight + snapshot + operation +
    verify + audit).
  - **AC 4** (no silent fallback) — закрыт Steps
    2–4 кодом; в `tools.py` нет ветки fallback'а
    из binary-backed на stub при non-zero exit.
  - **AC 5** (honest payload discipline) — закрыт
    Step 4; evidence Step 6: все шесть unified
    honest-mode полей populated в каждой из трёх
    Step 6 операций.
  - **AC 6** (registries без drift'а) — verified:
    `read_server_tools = 15`,
    `write_server_tools = 25`,
    `intelligence_server_tools = 16`,
    `imports_ok = true`, `selfcheck_status = ok`.
  - **AC 7** (`onec_policy_engine` не импортируется
    в product/intelligence) — invariant сохранён
    (Phase 6 / Step 9 уже его подтвердил, Track A
    кода не правил под `apps/platform/src` и
    `apps/mcp-intelligence-server/src`).
  - **AC 8** (no back-door write channel в product
    layer) — by construction: Step 6 round-trip
    шёл через public write-server tools, A.4 /
    A.5 — через `run_write_flow`.
  - **AC 9** (operator-facing messages честные) —
    runbook + local chain expectation выровнены
    Step 6'ом под фактическое поведение audit
    канала.
  - **AC 10** (Track A closed как documented
    status) — закрывается этим Step'ом
    (README + PROJECT-STATUS обновлены).
- **Какие repo-файлы Step 7 правил.**
  - `README.md` — раздел «Active parallel track»
    переименован в «Closed parallel track»; Step 6
    и Step 7 отмечены как closed; добавлен явный
    блок «Что Track A реально закрыл» и «Что
    Track A не делает индустриальным продуктом
    после closure» (honest constraints).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под closed; Step 6 секция
    дополнена блоком «Step 6 closure on InfoBase6»
    с фактическими evidence; добавлена эта Step 7
    секция.
- **Что Step 7 НЕ правил.**
  - **Никаких production-правок.** `apps/mcp-write-server/`,
    `apps/mcp-read-server/`, `apps/mcp-intelligence-server/`,
    `apps/platform/`, `packages/mcp-common/`,
    `packages/onec-process-runner/`,
    `packages/onec-policy-engine/`,
    `packages/onec-audit/`, `packages/onec-health/`,
    `packages/onec-troubleshooting/`,
    `packages/onec-config/`, `scripts/`,
    `selfcheck.py`, `bootstrap_paths.ps1`,
    `pyproject.toml`, `.github/`, `.claude.json`
    — без изменений.
  - **Никаких registry изменений.** read=15 /
    write=25 / intelligence=16 без drift'а.
  - **Никаких новых runbook'ов.** Step 6 уже
    ship'нул один operator-reproducible runbook;
    Step 7 ничего нового не добавляет — он только
    финализирует closure-status трека.
  - **`docs/architecture/track-a-real-write-path-plan.md`
    и `track-a-real-write-path-step-map.md` не
    тронуты** — они уже описывают Track A
    корректно; closure-статус по контракту проекта
    живёт в README + PROJECT-STATUS, не в
    plan/step-map.
  - **Никаких новых запусков 1cv8.exe.** Existing
    Step 6 evidence полностью покрывает acceptance
    criteria 1–5; повторный round-trip был бы
    избыточным.
  - **`docs/operator-manual.md` /
    `docs/administrator-manual.md` /
    `docs/developer-manual.md` /
    `docs/runbooks.md` /
    `apps/*/README.md`** — не тронуты. Write-server
    behaviour не изменился ни на единый байт после
    Step 6; эти документы уже честны после
    Steps 2–5.
- **Что Track A реально закрыл (final summary).**
  - **Real binary-backed dump/apply/updatedb path**:
    все три ранее stub-backed write-tool'а
    (`create_dump_snapshot`,
    `apply_config_from_files`,
    `update_database_configuration`) теперь имеют
    honest dual-mode contract с real binary-backed
    dispatch'ем при наличии operator-declared
    argv-template'а; production-code visible в
    `apps/mcp-write-server/src/mcp_write_server/tools.py`
    (Steps 2–4) и в shared
    `runtime/binary_dispatch.py` (Step 4).
  - **Final contract correctness**: один shared
    `binary_dispatch` helper, per-tool placeholder
    whitelists (включая tighter whitelist у
    updatedb), fail-closed на unknown placeholder
    до старта subprocess'а, fixed timeout cap
    (300 s default).
  - **No silent fallback**: при non-zero exit
    binary-backed branch'а возвращается honest
    `ok=False` с populated `mode='binary-backed'` /
    `binary_invoked=True` / `exit_code != 0`, без
    тихого downgrade'а на stub. Fallback — только
    config-time, при отсутствии binary contract'а.
  - **Honest payload discipline**: каждая ветка
    каждого из трёх tool'ов несёт все шесть
    unified honest-mode полей (`mode`,
    `binary_invoked`, `exit_code`,
    `command_preview`, `stdout_excerpt`,
    `stderr_excerpt`).
  - **Reference-stand execution layer proven**:
    real multi-step round-trip отработал на
    InfoBase6 (real file-based 1С база), audit
    honest, snapshot trees физически на диске,
    runbook + closure logic выровнены под
    фактическое поведение `run_write_flow`'а.
- **Что Track A НЕ делает «готовым индустриальным
  продуктом» после closure (honest constraints).**
  - **Operator credentials остаются out-of-band** —
    DESIGNER user/password не в product config;
    в Step 6 closure они хранились в local-only
    `%TEMP%/infobase6-writable.config.json`
    (cleartext, никогда не коммитится). Production-
    grade secrets management — out of Track A.
  - **Multi-version matrix не пройдена** — Step 6
    закрылся на single-version smoke
    (8.3.27.1859); другие версии 1С в матрицу
    не входили.
  - **Production runbook ecosystem не построен** —
    Track A ship'нул один reference-stand runbook;
    полная operator runbook collection — отдельный
    track.
  - **Packaging / installer / signed distribution
    / GUI wizard / `.msi` / `.deb`** — не сделано
    (это Phase 6 / parallel track).
  - **Полный enterprise super-set** (SSO/RBAC,
    multi-tenant, secrets vault как сервис,
    federated audit, policy-as-code DSL,
    multi-instance HA) — не открывался.
  - **Web-UI / dashboard frontend** — не сделан.
  - **Полная rollback/delete-вселенная** — whitelist
    остаётся на двух tool'ах
    (`add_catalog_attribute`,
    `add_document_attribute`), как Phase 6 / Step 4
    его и оставил.
  - **Полный AST-парсер XML/BSL** — не написан;
    XML edits идут через `xml.etree.ElementTree`
    DOM-стиль, BSL — substring/regex MVP-патчинг.
  - **Production-grade MCP transport / `__main__` /
    CLI у трёх MCP-серверов** — не сделано.
  - **Hot reload без рестарта процесса**, OS-level
    service supervision (Windows Service / systemd
    unit) — не сделано (Phase 6 / Step 6 ship'нул
    минимальный restart-policy contract).
  - **Полный version-matrix smoke на всех 1С
    версиях и стендах** — не пройден.

  Эти ограничения зафиксированы как **honest
  constraints**: Track A **не** претендовал на
  enterprise-ready / production-ready статус.
  Closure Track A означает буквально «full real
  1cv8-backed write path работает end-to-end на
  reference stand'е», не «продукт готов к prod».
- **Dev-check после Step 7.** Зелёный без правок:
  `imports_ok = true`,
  `read_server_tools = 15` имён,
  `write_server_tools = 25` имён,
  `intelligence_server_tools = 16` имён,
  `selfcheck_status = ok`. (Замечание:
  `health_summary_problem = gateway_down` —
  ожидаемое состояние dev-окружения без HTTP-
  публикации; Step 6 round-trip шёл с локальным
  gateway stub'ом, который сейчас не запущен.
  selfcheck'у он не нужен.)
- **Следующий шаг.** Track A полностью закрыт.
  Никаких новых треков параллельно с Track A не
  открывалось; никаких новых треков closure'ом
  Track A автоматически не открывается. Открытие
  следующего parallel track'а — отдельное решение
  оператора проекта; Phase 7 как линейная фаза
  по-прежнему не запланирована.

### Parallel Track B / Step 1 — planning Productization & Delivery Polish (завершён)

- **Цель шага.** Зафиксировать документационный вход
  в **Parallel Track B — Productization & Delivery
  Polish**: назначение трека, целевой результат, что
  закрывает трек и что НЕ закрывает, чем отличается от
  Phase 6 и Track A, guardrails, явный список «что НЕ
  входит», 10 критериев приёмки, открытые вопросы
  Step 2+. Кода не писать. Никаких изменений registry.
  Никаких новых MCP tool'ов. Никакого расширения
  product-layer surface'а.
- **Назначение трека.** После closure'а Track A
  execution layer real binary-backed write path'а
  доказан. Самый жирный незакрытый разрыв сейчас —
  **не execution layer**, а делiver-сторона:
  репозиторий не git-репозиторий (нет `.git`);
  `.gitignore` минимальный и не покрывает реалии
  проекта (snapshot trees Track A Step 6, audit-
  директории, локальные writable-конфиги); нет
  `LICENSE`, нет `CHANGELOG.md`, нет верхнеуровневого
  «5-минутного quickstart'а» в README; у трёх
  MCP-серверов нет `__main__.py`; `scripts/release/`
  пустая. Track B доводит существующий продукт до
  удобного **install / run / repo / release**
  состояния — не открывая нового execution-core
  sprint'а и не входя в enterprise super-set.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-b-productization-polish-plan.md`
    — назначение Track B, целевой результат (6
    пунктов), что Track B **не** закрывает, guardrails
    (никакого расширения MCP surface, никакого
    back-door write channel, никакого `shell=True`,
    никаких credentials в repo, не претендуем на
    enterprise-ready / production-ready статус),
    10 критериев приёмки, 7 открытых вопросов,
    раздел «связь с Phase 6 / Track A», honest
    constraints после closure.
  - **Один новый step-map:**
    `docs/architecture/track-b-productization-polish-step-map.md`
    — шесть шагов: Step 1 (planning, этот),
    Step 2 (repo hygiene + legal layer), Step 3
    (install fast path operator-discoverable),
    Step 4 (local launch ergonomics), Step 5
    (README + docs polish), Step 6 (final
    integration pass and Track B closure). Каждый
    шаг описан в едином формате (Цель / Что меняем /
    Затронутые зоны / Результат).
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`,
    `.github/`, `.editorconfig`, `.python-version`,
    `.gitignore`, `examples/` — без изменений.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `onec-config`, `selfcheck.py`,
    `bootstrap_paths.ps1`.** Track B / Step 1 это
    documentation-only.
  - **Никакой `git init`** на этом шаге. Это
    Step 2.
  - **Никакого LICENSE / CHANGELOG / SECURITY.**
    Это Step 2.
  - **Никаких новых runbook'ов / manualов.**
- **Что сказали явно в плане трека.**
  - Track B **не** закрывает: production-grade MCP
    transport (auth, multi-tenant, federated
    audit), полный installer ecosystem (`.msi` /
    `.deb` / GUI wizard / signed distribution),
    web-UI / dashboard frontend, полный enterprise
    super-set (SSO/RBAC, multi-tenant, secrets
    vault как сервис, federated audit storage,
    policy-as-code DSL, multi-instance HA), hot
    reload / OS-level service supervision,
    multi-version matrix smoke на всех 1С версиях,
    полный AST-парсер XML/BSL, полная
    rollback/delete-вселенная, новые MCP tools
    (registries `read=15 / write=25 /
    intelligence=16` остаются без drift'а),
    production code rewrite.
  - **GitHub remote push** — operator action, не
    часть трека. Track B доводит до состояния
    «репозиторий готов к выкладке»; нажатие
    `git remote add origin ...` + `git push -u
    origin main` — отдельный operator step.
- **Открытые вопросы Step 2+.** Q1 (лицензия:
  Apache-2.0 как default-предложение, окончательно
  — operator call), Q2 (`main` vs `master`), Q3
  (scope `__main__.py`'ев у MCP-серверов), Q4
  (`__main__.py` для `onec_platform`), Q5
  (`CONTRIBUTING.md` / `SECURITY.md` — нужны ли),
  Q6 (что делать с `examples/demo-dumps/_snapshots/`
  от Track A Step 6 round-trip'а), Q7 (версия
  проекта в `pyproject.toml` — оставить `0.1.0` или
  bump'нуть в `0.2.0`).
- **Selfcheck после Step 1.** Зелёный без правок:
  `imports_ok = true`,
  `read_server_tools = 15` имён,
  `write_server_tools = 25` имён,
  `intelligence_server_tools = 16` имён,
  `selfcheck_status = ok`. Track B / Step 1 не
  правил production-кода, поэтому drift'а быть не
  должно — и его нет.
- **Следующий шаг.** Parallel Track B / Step 2 —
  закрыт; см. секцию ниже.

### Parallel Track B / Step 2 — repo hygiene + legal layer (завершён)

- **Цель шага.** Превратить рабочую директорию в
  git-репозиторий, выровнять `.gitignore` под реалии
  проекта, добавить `LICENSE` / `CHANGELOG.md` /
  `SECURITY.md`, сделать первый meaningful commit.
  Resolve Q1 (license), Q2 (`main` vs `master`), Q5
  (CONTRIBUTING / SECURITY), Q6
  (`examples/demo-dumps/` artifacts), Q7
  (version в `pyproject.toml`).
- **Что сделано.**
  - `git init -b main` в корне `C:\Tools\1c-agent-platform`.
  - `.gitignore` расширен (Python / IDE / OS + 1С DB-
    файлы и locks `*.1CD` / `*.cfl` + Track A
    round-trip evidence (`examples/demo-dumps/_snapshots/`,
    `examples/demo-dumps/infobase6/`) + audit dirs
    `**/.audit/` + runtime state `.runtime/` /
    `**/.runtime/` + bootstrap work dir
    `examples/demo-infobase/_work/` + local writable /
    fixed configs `*-writable.config.json` /
    `*.config.fixed.json` / `*.config.json.bak` +
    scratch `scratch/` / `.scratch/` + editor scratch).
  - `LICENSE` (Apache-2.0, полный стандартный текст —
    header + 9 numbered TERMS + END OF TERMS AND
    CONDITIONS + APPENDIX).
  - `CHANGELOG.md` (заголовок `## 0.1.0 — initial public
    snapshot (in preparation)`; перечень что закрыто до
    0.1.0 — Phases 1–6 + Track A; registry invariant
    15/25/16; honest constraints).
  - `SECURITY.md` (private reporting flow + honest
    constraints — pre-1.0, credentials out-of-band, no
    production transport, single-version smoke, no
    installer ecosystem, limited rollback coverage —
    + safety guarantees: `run_write_flow` единственный
    mutating-путь, intelligence read-only, no
    `shell=True`, append-only audit, fail-closed
    defaults).
  - Initial meaningful commit `85a4a7e` —
    `Initial public snapshot — repo hygiene and legal
    baseline` — 126 файлов, 0 dangerous matches на
    safety scan'е.
- **Что НЕ сделано.** Production-код вообще не
  трогали. `apps/`, `packages/`, `scripts/dev/`,
  `pyproject.toml`, `.github/`, `examples/`, `docs/`
  — без изменений. Registries `read=15 / write=25 /
  intelligence=16` без drift'а. Никакого remote
  push'а.

### Parallel Track B / Step 3 — install fast path operator-discoverable (завершён)

- **Цель шага.** Сделать существующий
  `onec_platform.run_install_fast_path_from_json_file`
  operator-discoverable через тонкий PowerShell
  wrapper в каноническом `scripts/release/`, без
  правки production-installer-core.
- **Что сделано.**
  - `scripts/release/install.ps1` — operator-facing
    PowerShell wrapper. Params: `-ConfigPath`
    (mandatory), `-OutputConfigPath` (mandatory),
    `-Confirm` (switch). Dot-source'ит
    `scripts/dev/bootstrap_paths.ps1`, форвардит
    вызов в Python helper, мапит outcome в exit code
    (`0` preview/executed, `2` rejected, `3` other
    failure, `64` bad args).
  - `scripts/release/_install_runner.py` — тонкий
    Python helper. Underscore-prefixed (не для
    импорта). Принимает 3 positional args, валидирует
    confirm-флаг, вызывает
    `run_install_fast_path_from_json_file`, печатает 7
    ключевых полей результата + findings +
    recommended_actions.
  - `scripts/release/README.md` — operator-facing
    документация: usage (preview + execute),
    параметры, exit codes, явный список «что wrapper
    НЕ делает» (no MCP server start, no write-tools,
    no infobase touch, no `shell=True`, no packaging
    ecosystem, не подменяет launch ergonomics
    Step 4).
  - End-to-end preview-mode прогон verified: `ok=True`,
    `mode=preview`, `config_written=False`,
    bootstrap_pre OK, recommended action — re-run с
    `-Confirm`. Bad-args path возвращает usage и
    exit 64. Selfcheck registries без drift'а.
  - Commit `bce8966` — `Track B / Step 3 —
    operator-discoverable install fast path wrapper`,
    3 файла, 264 insertions.
- **Что НЕ сделано.** Production-код не правили
  (`apps/platform/installer.py` не тронут).
  Registries без drift'а. Никакого packaging
  ecosystem'а.

### Parallel Track B / Step 4 — operator/dev local launch umbrella (завершён)

- **Цель шага.** Снять с оператора/разработчика
  ритуал ручного PYTHONPATH bootstrap'а для типовых
  локальных задач. Один очевидный umbrella entry в
  каноническом `scripts/dev/`.
- **Что сделано.**
  - `scripts/dev/launch.ps1` — PowerShell умbrella с
    четырьмя subcommands: `selfcheck` (delegate в
    существующий `run_dev_check.ps1`), `repl`
    (dot-source bootstrap + interactive `python`),
    `run <script.py> [args…]` (dot-source bootstrap +
    `python @args`), `help` (default at no-args).
    Exit codes: `0` success / help; делегированный
    `$LASTEXITCODE` для `selfcheck` / `run`; `64` —
    unknown command или missing args.
  - `scripts/dev/README.md` — UPDATE одной добавочной
    секцией про `launch.ps1` сверху (без удаления /
    реструктуризации существующих описаний
    `bootstrap_paths.ps1` / `selfcheck.py` /
    `run_dev_check.ps1`).
  - Verification: parse OK, help / selfcheck / `run
    scripts/dev/selfcheck.py` happy paths возвращают
    exit 0 с корректным выводом (registries 15/25/16,
    `selfcheck_status=ok`); unknown command + `run`
    без args возвращают exit 64; `run nope.py`
    propagatе'ит python's exit code (2).
  - Commit `fd92477` — `Track B / Step 4 —
    operator/dev local launch umbrella`, 2 файла, 152
    insertions, 1 deletion.
- **Что НЕ сделано.** Никаких `__main__.py` в
  server-package'ах. Production-код вообще не
  тронут. Никакого MCP-server-launch ритуала
  (production transport — out of Track B). Никакого
  pytest (нет test suite'а). Registries без drift'а.

### Parallel Track B / Step 5 — root README quickstart and docs polish (завершён)

- **Цель шага.** Сделать root README нормальной
  «входной дверью» для нового человека: ≤ 50 строк
  основного текста с 1–2 строками о проекте,
  системными требованиями, install / check / launch
  командами, картой deeper docs, и явным «что
  Quickstart НЕ обещает».
- **Что сделано.**
  - `README.md` — добавлен блок `## Quickstart`
    между intro-параграфом и `## Идея`. Содержит:
    quote-блок «Что это» с current honest state
    (Phases 1–6 + Track A закрыты; Track B in
    progress; обновлён в Step 6 на «закрыт»);
    `### Системные требования`;
    `### Install` (PowerShell-команда + ссылка на
    `scripts/release/README.md`); `### Check`
    (`launch.ps1 selfcheck` + ссылка на
    `run_dev_check.ps1`); `### Local dev launch`
    (четыре umbrella-команды); `### Куда идти
    дальше` (5 pointer'ов на `apps/platform/README.md`,
    `docs/operator-manual.md`, `docs/runbooks/`,
    `docs/architecture/`, `PROJECT-STATUS.md`);
    `### Что Quickstart **не** обещает` (явно: no
    production transport, no installer ecosystem, no
    web UI, no enterprise deployment, no hot reload).
  - +81 insertion, 0 deletion — pure addition; ничего
    не удалено и не реструктурировано.
  - 15 referenced paths валидны (verified `test -e`).
  - Commit `0f65c58` — `Track B / Step 5 — root
    README quickstart and docs polish`, 1 файл.
- **Что НЕ сделано.** `scripts/release/README.md`,
  `scripts/dev/README.md`, `apps/platform/README.md`,
  `docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md` — не
  трогали. Никаких широких docs rewrite'ов.
  Registries без drift'а.

### Parallel Track B / Step 6 — final integration pass and Track B closure (завершён)

- **Цель шага.** Закрыть весь Track B как documented
  status. Read-only final integration check уже
  закрытых Steps 2–5, потом минимальные
  closure-docs/status updates, потом final closure
  commit.
- **Read-only final integration check.**
  - Working tree clean перед началом
    (`git status --short` пуст).
  - Git history линейная и читаемая: `85a4a7e`
    (Step 2) → `bce8966` (Step 3) → `fd92477`
    (Step 4) → `0f65c58` (Step 5).
  - Все Step 2 deliverables на диске: `.git`,
    `.gitignore`, `LICENSE`, `CHANGELOG.md`,
    `SECURITY.md`. Все Step 3 deliverables на месте.
    Все Step 4 deliverables на месте. Step 5
    Quickstart-блок в README присутствует.
  - Production-код вообще не тронут на всём треке —
    подтверждено отсутствием `apps/` / `packages/` в
    diff'ах ни одного из четырёх Track B commit'ов.
- **Что сделано в этом шаге.** Только closure
  docs/status updates (минимальный scope):
  - `README.md` — секция «Active parallel track»
    переработана в «Closed parallel tracks»
    (множественное число) + «Track B detail
    (закрыт)» с per-step описанием Steps 1–6 и
    summary outcomes; явный список «что Track B НЕ
    делает индустриальным продуктом» (honest
    constraints); явное «активного трека сейчас
    нет».
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track B closed; добавлены
    пять новых per-step секций (Steps 2/3/4/5/6).
  - `CHANGELOG.md` — entry `## 0.1.0` приведён в
    соответствие фактическому состоянию (Track B
    Steps 1–6 закрыты, не «in preparation»;
    `## 0.1.0 — initial public snapshot`).
  - Commit `Track B / Step 6 — final integration
    pass and track closure` зафиксирует closure event
    в git history.
- **Что НЕ сделано.** Никакого нового feature work,
  никаких production-правок, никаких новых MCP
  tool'ов, никакого remote push'а. `apps/`,
  `packages/`, `scripts/`, `examples/`,
  `docs/architecture/`, `docs/runbooks/`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`,
  `pyproject.toml`, `.github/`, `.editorconfig`,
  `.python-version`, `.gitignore`, `LICENSE`,
  `SECURITY.md` — **не тронуты** в этом шаге.
- **Что Track B в сумме дал проекту.**
  - Repo стал git-репозиторием на ветке `main` с
    чистой линейной history, легко выкладываемой на
    любой git remote.
  - `.gitignore` корректно покрывает project-specific
    опасные / тяжёлые / локальные артефакты, защищая
    от случайного коммита cleartext credentials или
    snapshot tree'ев.
  - Apache-2.0 license, CHANGELOG, SECURITY на месте
    — legal/doc baseline для honest публикации.
  - Operator-discoverable install:
    `scripts/release/install.ps1` — без знания
    internal Python module path и без ручного
    PYTHONPATH ритуала.
  - Operator/dev local launch umbrella:
    `scripts/dev/launch.ps1` — `selfcheck` / `repl` /
    `run` / `help` за одну команду.
  - Root README имеет верхний Quickstart-блок:
    новый человек за 1–2 минуты понимает что это,
    как поставить, как проверить, куда идти дальше.
  - Production-код не трогали ни разу за весь
    Track B. Registry-инвариант сохранён точно
    `read=15 / write=25 / intelligence=16`.
- **Honest constraints, оставшиеся после closure
  Track B.** Track B **не сделал** проект «глубоким
  индустриальным продуктом». По-прежнему отсутствуют:
  production-grade MCP transport (auth /
  authorisation / network hardening), полный
  installer ecosystem (`.msi` / `.deb` / GUI wizard /
  signed binary distribution), web-UI / dashboard
  frontend, полный enterprise super-set (SSO/RBAC,
  multi-tenant, secrets vault как сервис, federated
  audit storage, policy-as-code DSL, multi-instance
  HA), hot reload / OS-level service supervision,
  multi-version matrix smoke на всех 1С версиях,
  полный AST-парсер XML/BSL, полная rollback/delete-
  вселенная (whitelist остаётся на двух tool'ах),
  production-grade transport / `__main__` / CLI у
  трёх MCP-серверов с auth. Эти направления остаются
  за пределами Track A + Track B.
- **Следующий шаг.** Активного трека нет. Открытие
  следующего parallel track'а — **отдельное решение
  оператора проекта**; Phase 7 как линейная фаза не
  запланирована. Possible candidates (только
  recommendations, без авто-открытия): operator
  credentials hardening track (env-substitution или
  OS keychain integration); multi-version 1С smoke
  track; полный rollback whitelist track. Менее
  рекомендуемые — full enterprise super-set, web-UI,
  packaging ecosystem (более широкий scope, выше
  риск).

### Parallel Track C / Step 1 — planning Packaging & Installer Delivery (завершён)

- **Цель шага.** Зафиксировать документационный вход
  в **Parallel Track C — Packaging & Installer
  Delivery**: назначение трека, целевой результат, что
  закрывает трек и что НЕ закрывает, чем отличается от
  Track A и Track B, guardrails, явный список «что НЕ
  входит», 10 acceptance criteria, открытые вопросы
  Step 2+. Кода не писать. Никаких изменений registry.
  Никаких новых MCP tool'ов. Никакого расширения
  product-layer surface'а.
- **Назначение трека.** Track B закрыл базовую
  productization-полировку (git baseline + install
  wrapper + launch umbrella + README quickstart).
  Самый жирный незакрытый разрыв сейчас — **не
  execution layer и не базовая ergonomics, а
  delivery/packaging слой**: `scripts/release/install.ps1`
  это тонкий wrapper над одной функцией, а не
  полноценный release-facing layer; нет release
  handoff документа для receive-side оператора; нет
  reproducible install-sequence checklist'а с
  системными зависимостями; `pyproject.toml` имеет
  `packages = []` в hatch wheel target (wheel build
  по сути no-op); нет single canonical release
  entrypoint map'а; нет release-time pre-handoff
  sanity check'а. Track C доводит существующий продукт
  до состояния, в котором его удобно передать другому
  человеку как packaged unit'ом — не открывая нового
  execution-core sprint'а и не входя в enterprise
  super-set.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-c-packaging-installer-delivery-plan.md`
    — назначение Track C, целевой результат
    (5-шаговый narrative для receive-side оператора),
    что Track C **не** закрывает (GUI installer
    wizard, signed binary distribution, package-
    manager publication, systemd / Windows Service
    registration, web-UI, full enterprise super-set,
    production-grade MCP transport, multi-version 1С
    matrix, AST-парсер, hot reload, новые MCP tools,
    production code rewrite), guardrails, 10
    acceptance criteria, 6 открытых вопросов
    (Q1—Q6), раздел «связь с Phase 6 / Track A /
    Track B», honest constraints после closure.
  - **Один новый step-map:**
    `docs/architecture/track-c-packaging-installer-delivery-step-map.md`
    — шесть шагов: Step 1 (planning, этот),
    Step 2 (release-facing scripts/release/ layout
    полишинг — `verify-release.ps1` + UPDATE
    `scripts/release/README.md`), Step 3 (packaging-
    facing install flow — `pyproject.toml` honest
    review), Step 4 (release handoff documentation —
    `docs/release-handoff.md`), Step 5 (integration
    & polish), Step 6 (final integration pass and
    Track C closure). Каждый шаг описан в едином
    формате (Цель / Что меняем / Затронутые зоны /
    Результат).
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`,
    `.github/`, `.editorconfig`, `.python-version`,
    `.gitignore`, `examples/`, `LICENSE`,
    `SECURITY.md`, `CHANGELOG.md` — без изменений.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `onec-config`.** Track C / Step 1
    это documentation-only.
  - **Никакого нового `verify-release.ps1`** на этом
    шаге. Это Step 2.
  - **Никакого `pyproject.toml` review.** Это
    Step 3.
  - **Никакого `release-handoff.md`.** Это Step 4.
  - **Никакого CHANGELOG update.** По симметрии с
    Track B (CHANGELOG обновляется один раз на
    closure трека) Track C по default'у будет
    обновлять CHANGELOG только в Step 6.
- **Что сказали явно в плане трека.**
  - Track C **не** закрывает: enterprise super-set,
    web-UI, полный AST-парсер, полную
    rollback/delete-вселенную, production-grade
    MCP transport, multi-version matrix, GUI
    installer wizard, signed binary distribution,
    publication к package managers, systemd /
    Windows Service registration, hot reload,
    новые MCP tools (registries `read=15 / write=25
    / intelligence=16` без drift'а), production
    code rewrite.
  - **GitHub remote push** — operator action, не
    часть трека. Track C готовит repo к handoff'у;
    нажатие `git remote add origin ...` +
    `git push -u origin main` — отдельный operator
    step.
- **Открытые вопросы Step 2+.** Q1 (где живёт
  release-handoff doc — default `docs/release-handoff.md`),
  Q2 (pre-handoff sanity check — отдельный
  `verify-release.ps1` vs `launch.ps1` extension —
  default отдельный скрипт по симметрии с
  `install.ps1`), Q3 (`pyproject.toml`
  `[tool.hatch.build.targets.wheel] packages` — fill
  honestly или explicit no-op comment — default fill
  honestly), Q4 (Windows-only vs cross-platform —
  default Windows-first), Q5 (release entrypoint map
  — отдельный документ vs раздел в root README —
  default отдельный документ), Q6 (CHANGELOG update
  cadence — default один раз на closure Track C).
- **Selfcheck после Step 1.** Зелёный без правок:
  `imports_ok = true`, registries `read=15 /
  write=25 / intelligence=16`, `selfcheck_status =
  ok`. Track C / Step 1 не правил production-кода,
  поэтому drift'а быть не должно — и его нет.
- **Следующий шаг.** **Parallel Track C / Step 2 —
  release-facing `scripts/release/` layout
  полишинг.** Step 2 включает: создание
  `scripts/release/verify-release.ps1` (pre-handoff
  sanity check над уже существующими entry points),
  возможно тонкий `_verify_runner.py` helper, UPDATE
  `scripts/release/README.md` (расширение, не
  переписывание). **Никаких изменений** в
  `scripts/release/install.ps1` (Track B / Step 3
  sealed) и в `scripts/dev/launch.ps1` (Track B /
  Step 4 sealed). Production-код не правится.
  Step 2 я открываю отдельным заходом, не в этом.

### Parallel Track C / Step 2 — release-facing verify path and layout polish (завершён)

- **Цель шага.** Расширить existing `scripts/release/`
  слой одним новым read-only entrypoint'ом —
  `verify-release.ps1` (pre-handoff sanity check над
  уже существующими entry points) — и UPDATE
  `scripts/release/README.md` под трёх-entrypoint
  surface (`install.ps1` + `verify-release.ps1` +
  `launch.ps1`). Никакого расширения write-поверхности,
  никаких изменений в `install.ps1` или `launch.ps1`,
  никакого production-кода.
- **Что реально появилось.**
  - `scripts/release/verify-release.ps1` — read-only
    pre-handoff sanity check: проверяет наличие
    install entrypoint'ов, dev-check workflow, planning
    docs, печатает компактный human-readable отчёт.
    Никаких subprocess'ов 1cv8, никаких side effects.
  - `scripts/release/README.md` — расширен под
    объяснение verify-release.ps1 и трёх-entrypoint
    surface'а. Existing install-секции не переписаны.
- **Что НЕ сделано (намеренно).** `apps/`, `packages/`,
  `pyproject.toml`, `scripts/release/install.ps1`,
  `scripts/dev/launch.ps1`, `docs/architecture/`,
  registries — без изменений. Никакого нового MCP
  surface'а; никакого нового write path'а.
- **Commit.** `ef087c8` — `Track C / Step 2 — release-
  facing verify path and layout polish`.

### Parallel Track C / Step 3 — packaging-facing install flow honest review (завершён)

- **Цель шага.** Честный review packaging-facing части
  `pyproject.toml`: явно зафиксировать, что Phase 6
  продукт **намеренно** не предназначен для publication
  как single Python wheel из-за multi-app monorepo
  shape. Никакого фиктивного wheel build'а; никакого
  package-manager publication'а.
- **Что реально появилось.**
  - `pyproject.toml` — добавлен явный block-комментарий
    рядом с `[tool.hatch.build.targets.wheel]
    packages = []`: это намеренный no-op, операторы
    устанавливают продукт через `scripts/release/install.ps1`
    (Phase 6 boundary `run_install_fast_path`), а не
    через `pip install`. Версия 0.1.0 без bump'а.
  - `scripts/release/README.md` — небольшая secция
    «Packaging story», которая ссылается на
    pyproject-комментарий и явно отвергает GUI
    installer wizard / signed binary distribution /
    package-manager publication как out-of-scope.
- **Что НЕ сделано (намеренно).** Никакого fix'а
  hatch wheel target'а, никакого отдельного `setup.py`,
  никаких GitHub Releases, никаких Docker images,
  никаких `.msi` / `.deb`. Это **review**, не
  packaging-фиксация.
- **Commit.** `a4f42f9` — `Track C / Step 3 — packaging-
  facing install flow honest review`.

### Parallel Track C / Step 4 — release handoff documentation (завершён)

- **Цель шага.** Зафиксировать **один** release handoff
  документ для receive-side оператора. Никакой broad
  docs rewrite; никакого переписывания operator/
  administrator/developer manual'ов; ничего из Phase 6
  / Step 7 manual'ов не дублировать.
- **Что реально появилось.**
  - `docs/release-handoff.md` — новый документ,
    адресованный receive-side оператору, который
    получил репозиторий проекта: что вы получили,
    system prerequisites (Windows + PowerShell + Python
    3.11; `1cv8.exe` опционально и только для real
    write path), reproducible install sequence
    (verify-release.ps1 → install.ps1 preview →
    install.ps1 -Confirm), verify sequence (dev launch
    selfcheck), known limitations honest table
    (production-grade transport / GUI installer /
    enterprise super-set / multi-version matrix —
    out of scope). Без новых обещаний.
- **Что НЕ сделано (намеренно).** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `README.md`,
  `PROJECT-STATUS.md`, `CHANGELOG.md`,
  `docs/architecture/`, `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks*` — без
  изменений. Только один новый файл.
- **Commit.** `7ca9b3f` — `Track C / Step 4 — release
  handoff documentation`.

### Parallel Track C / Step 5 — integration and handoff polish (завершён)

- **Цель шага.** Минимально и честно интегрировать
  `docs/release-handoff.md` в верхнеуровневую
  навигацию проекта: receive-side handoff story должна
  стать discoverable из root README, без раздувания
  документации.
- **Что реально появилось.**
  - `README.md` — четырёхстрочный pointer на
    `docs/release-handoff.md` добавлен в Quickstart
    раздел «Куда идти дальше». Существующая
    структура Quickstart не переписана.
- **Что НЕ сделано (намеренно).** Никакого
  переписывания `docs/release-handoff.md`, никакого
  переписывания `scripts/release/README.md`, никакого
  трогания `PROJECT-STATUS.md`, никакого broad docs
  cleanup. Этот шаг — single high-leverage navigation
  edit.
- **Commit.** `8ccecf6` — `Track C / Step 5 —
  integration and handoff polish`.

### Parallel Track C / Step 6 — final integration pass and Track C closure (завершён)

- **Цель шага.** Закрыть весь Track C как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates, потом final closure commit.
- **Read-only final integration check.**
  - Working tree clean перед началом
    (`git status` пуст).
  - Git history линейная и читаемая: `af2d7f4`
    (Step 1) → `ef087c8` (Step 2) → `a4f42f9` (Step 3)
    → `7ca9b3f` (Step 4) → `8ccecf6` (Step 5).
  - Все Step 1 deliverables на диске
    (`docs/architecture/track-c-*`); Step 2 deliverables
    на диске (`scripts/release/verify-release.ps1`,
    обновлённый `scripts/release/README.md`); Step 3
    deliverables на диске (honest comment в
    `pyproject.toml`, packaging story в release/README);
    Step 4 deliverable на диске (`docs/release-handoff.md`,
    331 строка); Step 5 deliverable на диске (pointer
    в Quickstart README:62-65).
  - Production-код вообще не тронут на всём треке —
    подтверждено отсутствием `apps/` / `packages/` в
    diff'ах ни одного из пяти Track C commit'ов.
- **Что сделано в этом шаге.** Только closure
  docs/status updates (минимальный scope):
  - `README.md` — Quickstart intro обновлён под
    «Активного трека сейчас нет»; «Active parallel
    track» заменён добавлением Track C в «Closed
    parallel tracks» list; новая секция «Track C
    detail (закрыт)» с per-step описанием Steps 1–6
    и явным списком «что Track C НЕ делает
    индустриальным продуктом»; pointer на planning
    docs обновлён («включая Track B и Track C
    planning»).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track C closed; stale
    параграф «Track B сейчас documentation-only»
    заменён на post-Track-C closure narrative;
    добавлены пять новых per-step секций (Steps
    2/3/4/5/6).
  - `CHANGELOG.md` — entry `## 0.1.0` дополнен
    bullet'ом про Parallel Track C closed (Steps
    1–6); honest constraints и registry invariant
    остались без изменений (Track C их не меняет);
    «Active work: None» остаётся корректным после
    Track C closure.
  - Commit `Track C / Step 6 — final integration
    pass and track closure` зафиксирует closure
    event в git history.
- **Что НЕ сделано.** Никакого нового feature work,
  никаких production-правок, никаких новых MCP
  tool'ов, никакого remote push'а. `apps/`,
  `packages/`, `scripts/`, `examples/`,
  `docs/architecture/`, `docs/runbooks/`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`,
  `docs/release-handoff.md`,
  `pyproject.toml`, `.github/`, `.editorconfig`,
  `.python-version`, `.gitignore`, `LICENSE`,
  `SECURITY.md` — **не тронуты** в этом шаге.
- **Что Track C в сумме дал проекту.**
  - Release-facing entrypoint surface стал
    трёх-частным (`install.ps1` + `verify-release.ps1`
    + `launch.ps1`) с человеко-читаемым
    `scripts/release/README.md`.
  - `pyproject.toml` packaging limitation теперь
    явно задокументирована inline комментарием —
    больше не выглядит как «забытый no-op».
  - Receive-side оператор имеет один entry document
    (`docs/release-handoff.md`) с reproducible
    install/verify sequence и honest known
    limitations.
  - Root README quickstart честно ведёт на
    receive-side handoff story (Step 5 pointer).
  - Production-код не трогали ни разу за весь
    Track C. Registry-инвариант сохранён точно
    `read=15 / write=25 / intelligence=16`.
- **Honest constraints, оставшиеся после closure
  Track C.** Track C **не сделал** проект «глубоким
  индустриальным продуктом». По-прежнему отсутствуют:
  GUI installer wizard, `.msi` / `.deb` / signed
  binary distribution, publication к package
  managers (PyPI / Chocolatey / winget / apt),
  systemd / Windows Service registration, hot reload,
  web-UI / dashboard frontend, полный enterprise
  super-set (SSO/RBAC, multi-tenant, secrets vault
  как сервис, federated audit storage, policy-as-code
  DSL, multi-instance HA), production-grade MCP
  transport, multi-version 1С matrix, полный
  AST-парсер XML/BSL, полная rollback/delete-
  вселенная, новые MCP tools, production code
  rewrite. Эти направления остаются за пределами
  Track A + Track B + Track C.
- **Следующий шаг.** Активного трека нет. Открытие
  следующего parallel track'а — **отдельное решение
  оператора проекта**; Phase 7 как линейная фаза не
  запланирована. Possible candidates (только
  recommendations, без авто-открытия): operator
  credentials hardening track (env-substitution или
  OS keychain integration); multi-version 1С smoke
  track; полный rollback whitelist track. Менее
  рекомендуемые — full enterprise super-set, web-UI,
  packaging ecosystem (более широкий scope, выше
  риск).

### Parallel Track D / Step 1 — planning Operator Credentials Hardening (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track D — Operator Credentials Hardening**:
  назначение трека, целевой результат, что закрывает
  трек и что НЕ закрывает, чем отличается от Track A /
  Track B / Track C, guardrails, явный список «что НЕ
  входит», 10 acceptance criteria, открытые вопросы
  Step 2+. Кода не писать. Никаких изменений registry.
  Никаких новых MCP tool'ов. Никаких реальных credentials
  в repo / docs / commit message.
- **Назначение трека.** Track A закрыл execution layer,
  Track B — базовую productization, Track C — delivery /
  packaging / handoff. Самый узкий, окупаемый и честно
  зафиксированный незакрытый разрыв — operator credentials
  flow: DESIGNER credentials попадают в систему через
  `onec_*_command_template`-массивы как литеральные
  позиционные аргументы `/N "<user>"` `/P "<password>"`;
  платформа не делает env-substitution в этих template'ах
  (placeholder-движок поддерживает только whitelisted
  structural placeholder'ы); cleartext literal — самый
  прямой путь, описанный в runbook'е Track A;
  «out-of-band» документирован как набор возможностей,
  но сама платформа ни одной из них не реализует.
  Track D переводит этот honest constraint в узкий
  реализованный hardening-trek без enterprise-secrets
  программы.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-d-operator-credentials-hardening-plan.md`
    — назначение Track D, целевой результат
    (5-пунктовый narrative), что Track D **не**
    закрывает (enterprise vault platform, cloud KMS /
    Secrets Manager / Key Vault как baseline,
    SSO/RBAC/multi-tenant identity, federated audit,
    encrypted-at-rest secrets, OS keychain integration
    как baseline, production-grade MCP transport,
    multi-version 1С matrix, новые MCP tools, 1cv8
    binary changes, remote push), guardrails (no real
    credentials anywhere, no registry drift, backward-
    compat для legacy cleartext template, fail-closed
    на unresolved env, redaction-by-default в
    `command_preview`), 10 acceptance criteria,
    7 открытых вопросов (Q1—Q7), раздел «связь с
    Phase 6 / Track A / Track B / Track C», honest
    constraints после closure.
  - **Один новый step-map:**
    `docs/architecture/track-d-operator-credentials-hardening-step-map.md`
    — шесть шагов: Step 1 (planning, этот),
    Step 2 (credentials-flow audit + contract,
    docs-only — два новых short документа audit +
    contract), Step 3 (env-substitution implementation
    + redaction в `binary_dispatch.render_command_template`
    и `_assemble_command_preview`), Step 4 (operator
    docs / migration / handoff alignment — runbook,
    SECURITY, release-handoff, operator-manual),
    Step 5 (release-verify credential-hygiene heuristic
    — 8-й check в `verify-release.ps1`), Step 6 (final
    integration pass and Track D closure). Каждый шаг
    описан в формате Цель / Что меняем / Что НЕ
    меняем / Результат.
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`,
    `.github/`, `.editorconfig`, `.python-version`,
    `.gitignore`, `examples/`, `LICENSE`,
    `SECURITY.md`, `CHANGELOG.md`,
    `docs/release-handoff.md`,
    `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`,
    `docs/runbooks/*` — без изменений.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, `onec-policy-engine`,
    `onec-audit`, `onec-health`,
    `onec-process-runner`, `onec-troubleshooting`,
    `mcp-common`, `onec-config`.** Track D / Step 1
    это documentation-only.
  - **Никакой env-substitution implementation.** Это
    Step 3.
  - **Никакой docs migration.** Это Step 4.
  - **Никакого верификатор-расширения.** Это Step 5.
  - **Никакого CHANGELOG update.** По симметрии с
    Track B / Track C (CHANGELOG обновляется один раз
    на closure трека).
  - **Никаких реальных credentials** в созданных
    docs / commit message — все примеры через
    abstract placeholder forms (`<password>`,
    `${ENV:ONEC_DESIGNER_PASSWORD}`, `<user>`).
- **Что сказали явно в плане трека.**
  - Track D **не** закрывает: enterprise vault platform,
    cloud KMS / Secrets Manager / Key Vault как
    baseline, SSO / RBAC / multi-tenant identity,
    federated audit, encrypted-at-rest secrets format,
    OS keychain integration (deliberately optional
    research-only note, не implementation), production-
    grade MCP transport, multi-version 1С matrix,
    web-UI, GUI installer, signed distribution,
    package-manager publication, новые MCP tools
    (registries `read=15 / write=25 / intelligence=16`
    без drift'а), 1cv8 binary changes, production code
    rewrite за пределами locator'а env-substitution и
    redaction discipline.
  - **GitHub remote push** — operator action, не часть
    трека.
- **Открытые вопросы Step 2+.** Q1 (env-substitution
  syntax — default `${ENV:NAME}`), Q2 (substitution
  location — default render-time в `binary_dispatch`),
  Q3 (redaction marker — default `/P` and `/Pwd`
  case-insensitive), Q4 (legacy cleartext literal
  semantics — default silent в payload, репортится
  только Step 5 heuristic'ой), Q5 (OS keychain scope —
  default research-only note), Q6 (CHANGELOG cadence —
  default один update на closure), Q7 (`pyproject.toml`
  version bump 0.1.0 → 0.2.0 на closure — resolve
  финально в Step 6).
- **Selfcheck после Step 1.** Зелёный без правок:
  `imports_ok = true`, registries `read=15 /
  write=25 / intelligence=16`, `selfcheck_status =
  ok`. Track D / Step 1 не правил production-кода,
  поэтому drift'а быть не должно — и его нет.
- **Следующий шаг (на момент закрытия Step 1).**
  **Parallel Track D / Step 2 — credentials-flow audit
  and contract (docs-only).** Step 2 / 3 / 4 / 5 / 6
  последовательно пройдены — см. секции ниже.

### Parallel Track D / Step 2 — credentials flow audit and contract (завершён)

- **Цель шага.** Честно описать **существующий**
  credentials surface и зафиксировать **минимальный
  contract** на env-substitution и redaction. Никакой
  implementation. Никаких code changes. Step 2 — чисто
  documentation-only.
- **Что реально появилось в Step 2.**
  - **Новый documentation-only документ:**
    `docs/architecture/track-d-credentials-flow-audit.md`
    (303 строки) — где `/P "<password>"` физически
    появляется в `onec_*_command_template`-массивах сегодня,
    какие payload-поля видят rendered argv (`command_preview`,
    `stdout_excerpt`, `stderr_excerpt`), какие audit-поля
    могут отражать password при cleartext template'е, как
    `.gitignore` (Track B / Step 2) ловит local writable
    config'и, что значит «out-of-band» до Track D и почему
    это аспирация, а не enforced контракт. Optional
    research-note про tier-2 OS keychain (`keyring`) явно
    помечен как research-only, не in-scope.
  - **Новый documentation-only документ:**
    `docs/architecture/track-d-credentials-contract.md`
    (308 строк) — формальный контракт env-substitution
    syntax (`${ENV:NAME}` full-element token), resolution
    order (render-time, после structural-placeholder
    substitution, до запуска subprocess'а), fail-closed
    semantics (missing/empty env → render-time `ok=False`),
    redaction contract (`/P` / `/Pwd` argv-position →
    `<redacted>` в `command_preview` и trimmed excerpt'ах;
    actual subprocess argv остаётся unredacted), backward-
    compat (literal cleartext по-прежнему supported,
    репортится только Step 5 heuristic'ой).
- **Что НЕ сделано (намеренно).** Никаких изменений
  production-кода. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
  `docs/release-handoff.md`, `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*` —
  не тронуты на Step 2 (миграция docs — это Step 4).
- **Selfcheck после Step 2.** Зелёный без правок:
  `imports_ok = true`, registries `read=15 / write=25 /
  intelligence=16`, `selfcheck_status = ok`. Step 2 не
  правил production-кода — drift'а нет.
- **Commit.** `0d708d1` (Track D / Step 2 — credentials
  flow audit and contract).

### Parallel Track D / Step 3 — env substitution and preview redaction (завершён)

- **Цель шага.** Реализовать env-substitution и
  redaction discipline в write-server'е, оставаясь
  backward-compatible с cleartext-template'ом. Один
  boundary-файл, узкий внутренний contract из Step 2.
- **Что реально появилось в Step 3.**
  - **`apps/mcp-write-server/src/mcp_write_server/runtime/binary_dispatch.py`**:
    - `render_command_template(...)` расширен вторым pass'ом
      env-substitution для full-element токенов
      `${ENV:NAME}` после structural-placeholder
      substitution; missing / empty / partial / mixed форма →
      render-fail branch (`mode='binary-backed'`,
      `binary_invoked=False`, `command_preview=None`,
      honest reason); fail-closed по аналогии с
      unknown-placeholder discipline (sealed Track A).
    - `_assemble_command_preview(...)` обращается к
      новому helper'у `_redact_password_args(...)`,
      который сканирует rendered argv list, для argv-
      элементов после `/P` / `/Pwd` (case-insensitive)
      подменяет value на `<redacted>` и возвращает
      редактированный preview. **Actual subprocess argv
      не трогается** — иначе binary не аутентифицируется.
    - Внутренние helper'ы `_resolve_env_token` и
      `_redact_password_args` живут в том же файле, не
      в новом package'е, чтобы не раздувать surface.
- **Backward-compat.** Literal cleartext templates
  по-прежнему render OK, по-прежнему запускают
  subprocess; но `command_preview` для них тоже
  редактируется на `<redacted>` (по той же
  password-position discipline).
- **Что НЕ сделано (намеренно).** Не тронуты:
  `run_write_flow` discipline, structural-placeholder
  whitelists per tool (sealed Track A), `subprocess` без
  `shell=True`, public surface write-server'а (никаких
  новых tools, никаких изменений в JSON shapes для
  existing tools), `onec-config` loader semantics
  (substitution живёт в render-time, не в load-time).
  Никаких изменений в `mcp-read-server`,
  `mcp-intelligence-server`, `apps/platform/`. Никакого
  CHANGELOG update (это closure, Step 6).
- **Selfcheck после Step 3.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  `selfcheck_status=ok`; никаких реальных credentials в
  diff'е.
- **Commit.** `af4436f` (Track D / Step 3 — env
  substitution and preview redaction).

### Parallel Track D / Step 4 — operator docs and migration alignment (завершён)

- **Цель шага.** Перевести operator-facing документацию
  на env-substitution как **default рекомендованный путь**.
  Cleartext literal становится legacy fallback'ом, который
  остаётся supported, но не рекомендуется.
- **Что реально появилось в Step 4.**
  - `docs/runbooks/track-a-reference-stand-round-trip.md`:
    section 3 (product-config example) переписана —
    `"/N", "${ENV:ONEC_DESIGNER_USER}"` /
    `"/P", "${ENV:ONEC_DESIGNER_PASSWORD}"` как baseline;
    добавлен env-substitution callout; failure mode F2
    расширен под env-token failures (missing / empty /
    partial / mixed); credentials-in-logs нота обновлена
    под redaction discipline.
  - `SECURITY.md`: Honest constraints block переписан
    под env-substitution. «Operator credentials are
    out-of-band» теперь имеет конкретную реализацию
    (`${ENV:NAME}` substitution, render-time fail-closed,
    `<redacted>` в `command_preview`); явно перечислено
    что **по-прежнему** out-of-scope: secrets manager,
    vault, KMS, OS keychain integration, encrypted-at-rest
    secrets file format.
  - `docs/release-handoff.md`: Known limitations
    DESIGNER credentials bullet переписан под
    env-substitution как default; legacy cleartext
    отмечен как fallback; redaction contract упомянут
    конкретно.
- **Что НЕ сделано (намеренно).** `docs/operator-manual.md`
  **не тронут** — credentials guidance в нём отсутствует,
  раздувать его новой секцией без существующей опоры
  было бы scope creep. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `CHANGELOG.md`, registries — не
  тронуты. Никакого нового короткого документа
  `docs/operator-credentials.md` (step-map допускал
  optional, но без operator-manual'овского pointer'а
  это был бы orphan).
- **Selfcheck после Step 4.** Зелёный: registries без
  drift'а; selfcheck_status=ok; никаких реальных
  credentials в diff'е.
- **Commit.** `393e869` (Track D / Step 4 — operator docs
  and migration alignment).

### Parallel Track D / Step 5 — release verify credential hygiene heuristic (завершён)

- **Цель шага.** Расширить `scripts/release/verify-release.ps1`
  узкой heuristic'ой, которая ловит наиболее очевидный
  паттерн утечки — literal `/P "<value>"` в tracked
  `*.config.json` без env-substitution-формы и без
  `<password>` placeholder'а.
- **Что реально появилось в Step 5.**
  - `scripts/release/verify-release.ps1`: добавлен
    8-й named check **Credential template hygiene**
    (отдельный от существующего Credential leak guard).
    Heuristic сканирует tracked `*.config.json` через
    `git ls-files`, regex
    `(?i)"/P(?:wd)?"\s*,\s*"([^"]*)"`. Value матчит
    `^\$\{ENV:[A-Z_][A-Z0-9_]*\}$` или `<password>` →
    PASS-skip; пустой value → skip; literal non-empty →
    **WARN** (не FAIL) с `file:line`. Heuristic
    deliberately узкая: только tracked `*.config.json`,
    только `/P` / `/Pwd` adjacency, не сканирует
    runbook'и или другие документы. Header comment +
    summary marker switch + новый блок check 8 — три
    точечных правки скрипта.
  - `scripts/release/README.md`: row 8 в таблице checks +
    короткий disclaimer «не full DLP, узкая heuristic».
  - `docs/release-handoff.md`: «seven» → «eight» в
    четырёх местах + row 8 в verify-таблице.
- **Что НЕ сделано (намеренно).** Existing checks 1–7 в
  `verify-release.ps1` не тронуты. Exit-code semantics:
  WARN не инкрементит `$script:failed`; FAIL остался FAIL
  (default behaviour `Add-Check`). `apps/`, `packages/`,
  `pyproject.toml`, registries не тронуты. CHANGELOG не
  обновлён (это closure, Step 6).
- **Verification.** verify-release.ps1 прогон с
  `-AllowDirtyTree -SkipSelfcheck` и затем с full
  selfcheck — оба GREEN на 8 checks. 10 inline regex
  test cases прошли (env-form / lowercase / Pwd /
  multiline / placeholder → PASS; literal latin/cyrillic
  → WARN; empty → skip; `Program Files` substring + no
  quotes → no match).
- **Commit.** `1fd2d35` (Track D / Step 5 — release
  verify credential hygiene heuristic).

### Parallel Track D / Step 6 — final integration pass and Track D closure (завершён)

- **Цель шага.** Закрыть весь Track D как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates, потом final closure commit. Никакого
  нового feature work, никаких новых MCP tools,
  никакого remote push'а.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 2 → 3 → 4 → 5 → 6
    (все commit'ы существуют);
  - все Step 2 docs на диске (audit + contract,
    303 + 308 строк);
  - env-substitution + redaction присутствуют в
    `binary_dispatch.py` (Step 3): `_resolve_env_token`
    строки 161/209/242, `_redact_password_args` строки
    63/269/284/416/433/445;
  - operator docs обновлены (Step 4): runbook (23 hits
    Track D / env-substitution), SECURITY.md (Track D /
    Step 3 mention), release-handoff.md (4+ hits);
  - 8-й check присутствует в `verify-release.ps1`
    (Step 5);
  - registries `read=15 / write=25 / intelligence=16`
    без drift'а;
  - `verify-release.ps1` GREEN на 8 checks (full selfcheck
    включён);
  - no real credentials в diff'ах ни одного из пяти
    Track D commit'ов.
- **Что реально изменено на Step 6 (closure-docs only).**
  - `pyproject.toml` — version bumped `0.1.0` → `0.2.0`
    (Q7 разрешён в этом шаге; единственное non-doc
    исключение per Track D step-map);
  - `README.md` — Quickstart-блок переписан под Track D
    closed; «Closed parallel tracks» секция дополнена
    Track D bullet'ом (три → четыре закрытых трека);
    «Active parallel track» секция сжата под «нет
    активного трека» с pointer'ом на Track D detail;
    добавлена «Track D detail (закрыт)» секция
    симметрично Track A/B/C detail блокам;
  - `PROJECT-STATUS.md` — header (Текущий шаг + Статус)
    обновлён под Track D closed; общий narrative-блок
    переписан под closure; добавлены пять новых
    per-step секций (Steps 2/3/4/5/6); устаревший
    «Следующий шаг — Step 2» удалён;
  - `CHANGELOG.md` — добавлен новый раздел
    `## 0.2.0 — Parallel Track D — Operator
    Credentials Hardening` с per-step outcomes,
    registry invariant, honest constraints update;
    «Active work» в 0.1.0 секции обновлён под «closed
    in 0.2.0».
- **Что НЕ изменено на Step 6 (закрытый scope).**
  `apps/`, `packages/`, `scripts/release/` (помимо
  Step 5 deliverable),`scripts/dev/`, `examples/`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`, `SECURITY.md` (Step 4 уже
  выровнял), `docs/release-handoff.md` (Step 4 + Step 5
  уже выровняли), `scripts/release/README.md` (Step 5
  уже выровнял), `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*`
  (Step 4 уже выровнял runbook), `docs/architecture/track-d-*`
  (planning / audit / contract docs остаются как
  written), registries, `1cv8.exe` не запускался.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на
  8 checks; никаких реальных credentials в Step 6
  diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track D).**
  Активного шага не было. После Track D closure открыт
  пятый post-phase track — **Parallel Track E —
  Multi-Version 1C Smoke Matrix** — Step 1 которого
  закрыт сразу следом (см. секцию ниже).

### Parallel Track E / Step 1 — planning Multi-Version 1C Smoke Matrix (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track E — Multi-Version 1C Smoke Matrix**:
  назначение трека, целевой результат, что закрывает трек
  и что НЕ закрывает, чем отличается от Track A / B / C / D,
  guardrails, acceptance criteria, открытые вопросы Q1–Q7.
  Кода не писать. Никаких изменений registry. Никаких
  новых MCP tool'ов. Никаких запусков 1cv8.exe.
- **Назначение трека.** Track A доказал, что real
  binary-backed write path работает, но evidence ship'нут
  только на одном reference stand'е (InfoBase6) и одной
  1С версии (`8.3.27.1859`). Все последующие треки
  (B repo hygiene, C delivery / packaging, D operator
  credentials hardening) расширяли surface вокруг этого
  single-version evidence, но **не** расширяли саму
  evidence base. Track A plan уже явно вынес multi-version
  matrix за пределы своего scope: «Полное покрытие matrix'ы
  версий 1С — отдельный parallel track»
  (`docs/architecture/track-a-real-write-path-plan.md`).
  Track E — тот самый отдельный track: он расширяет
  evidence-уровень, не платформу.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-e-multi-version-smoke-matrix-plan.md` —
    зачем нужен Track E после Track D, стартовая точка
    (current evidence baseline на `8.3.27.1859`), gap /
    problem statement (скрытая дрожь argv-grammar'а
    между версиями + скрытая зависимость от particular
    install layout'а), целевой результат (frozen smoke
    scenario + documented matrix-table + operator runbook
    + aligned support statement), что входит / не входит,
    guardrails, 10 acceptance criteria, honest constraints
    after closure, связь с Track A / B / C / D, 7 open
    questions Q1–Q7.
  - **Один новый step-map:**
    `docs/architecture/track-e-multi-version-smoke-matrix-step-map.md` —
    шесть шагов: Step 1 (planning, этот), Step 2
    (current evidence baseline audit + version selection
    criteria + smoke scenario freeze, docs-only), Step 3
    (matrix scaffolding — operator runbook + matrix-table
    template, docs-only), Step 4 (operator-driven smoke
    runs на дополнительных versions, **operator gate**),
    Step 5 (support statement / docs alignment в
    SECURITY.md / release-handoff.md / README), Step 6
    (final integration pass and Track E closure). Каждый
    шаг описан в формате Цель / Что меняем / Что НЕ меняем
    / Результат.
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`, `.github/`,
    `.editorconfig`, `.python-version`, `.gitignore`,
    `examples/`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`,
    `docs/release-handoff.md`, `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks/*` — без
    изменений на Step 1.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, всех packages/.** Track E / Step 1
    это documentation-only.
  - **Никакого реального прогона 1cv8.exe** — это Step 4
    operator gate.
  - **Никакого нового runbook'а или matrix-table doc'а** —
    это Step 3.
  - **Никаких docs migration** в SECURITY.md /
    release-handoff.md / README — это Step 5.
  - **Никакого CHANGELOG update.** По симметрии с Track
    A / B / C / D (CHANGELOG обновляется один раз на
    closure трека).
  - **Никаких реальных credentials** в созданных docs /
    commit message — все примеры через abstract
    placeholder forms (`<password>`, `${ENV:NAME}`).
- **Что сказали явно в плане трека.**
  - Track E **не** закрывает: полная QA-программа
    (test pyramid, performance benchmarking, stress / load
    testing, fuzzing, mutation testing), enterprise
    certification claims / compliance attestations,
    «universal / full version support» marketing, feature
    additions для конкретных 1С версий, version-sniffing в
    платформе, новые MCP tools (registries `read=15 /
    write=25 / intelligence=16` без drift'а), 1cv8 binary
    changes, transport rewrite, packaging rewrite, broad
    platform rewrite, CI matrix runner для multi-version
    1cv8, полный AST-парсер, полная rollback / delete-
    вселенная, production-grade MCP transport / auth.
  - **GitHub remote push** — operator action, не часть
    трека.
- **Открытые вопросы Step 2+.** Q1 (version selection
  breadth — default 2 additional versions поверх reference,
  resolve в Step 2), Q2 (smoke scenario depth — default
  cut-down `create_dump_snapshot` через
  `/DumpConfigToFiles`, resolve в Step 2), Q3 (matrix-table
  location — default `docs/version-support-matrix.md`
  top-level, resolve в Step 3), Q4 (operator-supplied gap
  fallback — default «закрываем с honest gap notation»,
  resolve в Step 4), Q5 (closure version bump 0.2.0 → 0.3.0
  — default «да если ship'нута хотя бы одна additional row,
  иначе нет», resolve в Step 6), Q6 (SECURITY.md /
  release-handoff.md tone — default «короткий narrative +
  pointer на matrix-table», resolve в Step 5), Q7
  (post-closure evidence cadence — default «doc-only update
  без re-open Track E», resolve в Step 6).
- **Selfcheck после Step 1.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track E / Step 1 не правил
  production-кода — drift'а нет.
- **Следующий шаг (на момент закрытия Step 1).**
  **Parallel Track E / Step 2 — current evidence baseline
  audit + version selection criteria + smoke scenario freeze
  (docs-only).** Step 2 / 3 / 4 / 5 / 6 последовательно
  пройдены — см. секции ниже.

### Parallel Track E / Step 2 — current evidence audit and smoke scenario freeze (завершён)

- **Цель шага.** Честно описать **существующую**
  single-version evidence base, зафиксировать
  **principle-based criteria** отбора target версий, и
  **freeze'нуть** узкий smoke scenario для будущих
  comparable runs. Никакая implementation. Никаких code
  changes. Никакого 1cv8.exe.
- **Что реально появилось в Step 2.**
  - **Новый documentation-only документ:**
    `docs/architecture/track-e-current-evidence-audit.md`
    (descriptive — что доказано на reference version
    `8.3.27.1859`: full Track A round-trip + physical
    artifacts; чего пока **нет** — additional version rows,
    matrix-table, comparable smoke evidence; почему
    single-version evidence недостаточен — argv-grammar
    drift между versions, install layout dependency,
    stand-shape dependency; strict separation
    proven / inferred / not-yet-run / operator-supplied
    future inputs).
  - **Новый documentation-only документ:**
    `docs/architecture/track-e-smoke-scenario.md`
    (prescriptive **FROZEN** — scenario name
    `frozen-smoke-v1`; what it does — cut-down
    `create_dump_snapshot` через `/DumpConfigToFiles` only,
    read-only из перспективы 1С базы; what it does NOT do;
    operator-side preconditions; principle-based version
    selection criteria — one newer + one older
    `8.3.<minor>` family beyond reference; build-level
    diffs внутри одной minor НЕ additional evidence;
    pre-8.3 / pre-release / server-mode stands out-of-scope;
    12-column matrix shape; PASS / FAIL / NOT RUN semantics
    с явными conditions; required evidence fields;
    non-goals; Step 4 execution boundary).
- **Что НЕ сделано (намеренно).** Никаких изменений
  production-кода. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
  `docs/release-handoff.md`, `docs/operator-manual.md`,
  `docs/runbooks/*` — без изменений на Step 2 (alignment
  operator-facing docs — это Step 5).
- **Selfcheck после Step 2.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Step 2 не правил production-кода —
  drift'а нет.
- **Commit.** `630f837` (Track E / Step 2 — current
  evidence audit and smoke scenario freeze).

### Parallel Track E / Step 3 — matrix scaffolding and operator runbook (завершён)

- **Цель шага.** Создать operator-facing scaffolding для
  будущего Step 4: operator runbook + matrix-table doc,
  чтобы multi-version smoke matrix можно было заполнять
  по одному и тому же frozen scenario'ю без переизобретения
  формата и без новых запусков 1cv8.exe на этом шаге.
- **Что реально появилось в Step 3.**
  - **Новый operator runbook:**
    `docs/runbooks/track-e-multi-version-smoke-matrix.md`
    (484 строки) — Windows-first; preconditions (repo
    state / install / credentials через Track D / Step 3
    env-substitution / tooling); explicit list «what
    runbook does NOT do»; frozen scenario reference (no
    extension); required operator inputs (7-row table);
    step-by-step execution procedure (config / env vars /
    PYTHONPATH / pre-check / run / post-run / cleanup);
    what to record after each run (12-column contract);
    PASS / FAIL / NOT RUN handling с явными conditions;
    evidence capture rules (что в repo, что НЕ в repo);
    common stop conditions; honest constraints; Step 4
    closure boundary.
  - **Новый matrix-table doc:**
    `docs/version-support-matrix.md` (top-level, 258
    строк) — short intro «evidence table != blanket support
    claim»; column contract (12 frozen colonкол copy 1:1
    из Step 2 scenario doc); **Reference Row 1**
    (`8.3.27` / `1859` / `x64` / file-based InfoBase6 /
    `stronger-than-frozen-smoke-v1` / `PASS` / 2 mutating
    audit rows + snapshot trees) заполнена copy-only из
    existing Track A / Step 6 evidence без новых 1cv8.exe
    runs; никаких имитированных additional rows.
- **Что НЕ сделано (намеренно).** Никаких изменений
  production-кода. `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
  `docs/release-handoff.md`, `README.md`, Track A runbook,
  Track E planning/audit/scenario docs — без изменений на
  Step 3. Никакого 1cv8.exe run.
- **Selfcheck после Step 3.** Зелёный: registries без
  drift'а; selfcheck_status=ok; никаких credentials в
  diff'е.
- **Commit.** `7c08cae` (Track E / Step 3 — matrix
  scaffolding and operator runbook).

### Parallel Track E / Step 4 — operator-driven smoke execution and matrix update (завершён, PATH B)

- **Цель шага.** Прогнать `frozen-smoke-v1` на доступных
  у operator'а дополнительных 1С версиях и заполнить
  evidence rows; либо честно зафиксировать operator-supplied
  gap без имитации evidence. **Это единственный шаг Track
  E, где допускались real 1cv8.exe runs.**
- **Что реально показал operator-side inventory.**
  - `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe` —
    minor family `8.3.27`, build `1859`, x64 — **reference,
    already represented**.
  - `C:/Program Files (x86)/1cv8/8.3.27.1936/bin/1cv8.exe` —
    minor family `8.3.27`, build `1936`, x86 — **same minor
    family** as reference, **disqualified** as additional
    evidence per Step 2 §2.2 (build-level разница внутри
    одной minor family ≠ additional evidence).
  - Прочие typical install paths (`C:/Tools/1cv8`,
    `C:/1cv8`, `D:/1cv8`, `D:/Program Files/1cv8`) —
    **absent** на этой машине.
  - ENV-substitution credentials
    (`ONEC_DESIGNER_USER` / `ONEC_DESIGNER_PASSWORD`) —
    NOT SET в session; даже на reference run frozen-smoke-v1
    был бы render-fail before subprocess start.
- **Decision: PATH B (honest operator-supplied gap).** Per
  Track E plan Q4 + step-map Step 4: «если operator
  additional versions не предоставит — Track E закрывается
  с явным operator-supplied gap, без имитации evidence».
  Это **не** track failure; это honest closure под
  фактический evidence-уровень.
- **Что реально появилось в Step 4.**
  `docs/version-support-matrix.md` дополнен новой
  подсекцией `#### Track E / Step 4 closure note —
  operator-supplied gap` под `### Additional rows`:
  inventory-таблица operator-side окружения (3 строки:
  reference, disqualified same-family x86, absent typical
  paths); explicit list «что отсутствует на operator side
  для PATH A»; explicit list «что Step 4 сознательно не
  делал» (6 пунктов: no run на same-family x86, no rerun
  reference, no scenario expansion, no contract changes,
  no fabricated rows, no real credentials); explanation
  почему PATH B honest closure не failure;
  operator next-action option post-closure.
- **Что НЕ сделано (намеренно).** Никаких 1cv8.exe runs.
  Никаких additional evidence rows. Никакого rerun
  reference. Никакого scenario expansion. Reference row
  preserved unchanged (copy-only из Track A). 12-column
  contract intact. Никаких изменений в `apps/`,
  `packages/`, `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`, `README.md`,
  Track E planning/audit/scenario/runbook docs.
- **Verification.** `verify-release.ps1 -AllowDirtyTree`
  GREEN на 8 checks; registries `read=15 / write=25 /
  intelligence=16` без drift'а; credential template hygiene
  PASS.
- **Commit.** `f962d78` (Track E / Step 4 — operator-driven
  smoke execution and matrix update).

### Parallel Track E / Step 5 — support statement and docs alignment (завершён)

- **Цель шага.** Выровнять operator-facing и
  status-adjacent docs под фактический Step 4 PATH B
  результат. Не менять продукт, не менять сценарий, не
  менять evidence — только wording alignment там, где он
  должен отражать уже известный результат.
- **Что реально появилось в Step 5.** Пять точечных
  правок в трёх operator-facing docs:
  - `SECURITY.md`: bullet «Single-version 1С evidence»
    переименован в «Single-version 1С evidence (with
    multi-version scaffolding)» с pointer'ом на
    `docs/version-support-matrix.md`, mention
    `frozen-smoke-v1` + operator runbook, Track E / Step 4
    PATH B context, и «no blanket multi-version support
    claim» disclaimer.
  - `docs/release-handoff.md`: Known limitations bullet
    «No multi-version 1С smoke matrix» переписан под
    «Multi-version 1С smoke matrix — scaffolding only»
    с pointers на matrix doc и operator runbook + Step 4
    PATH B context. Companion «Single-version 1С
    coverage» bullet расширен matrix-doc pointer'ом как
    single source of truth.
  - `README.md`: Quickstart paragraph переписан — убрано
    stale «planning-only, Step 1»; убрана broad «matrix
    из нескольких 1С версий» implication; новый honest
    snapshot (scaffolding + reference row + honest
    operator-supplied gap) + matrix-doc pointer. «Куда
    идти дальше» navigation обогащён: existing
    `docs/runbooks/` bullet расширен Track E operator
    runbook mention; новый bullet на
    `docs/version-support-matrix.md`; existing
    `docs/architecture/` bullet расширен Track E mention.
- **Единый support statement** (теперь aligned across
  SECURITY / release-handoff / README): reference
  single-version evidence есть; matrix scaffolding
  существует; additional rows нет; Step 4 PATH B honest
  gap; `docs/version-support-matrix.md` — single source of
  truth; **no blanket multi-version support claim**.
- **Что НЕ сделано (намеренно).** `PROJECT-STATUS.md`
  и `CHANGELOG.md` не тронуты — closure deliverables
  Step 6 (Track A/B/C/D pattern: header alignment и
  CHANGELOG entry — не intermediate-step concerns).
  Никаких изменений в `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, registries, Track E planning /
  audit / scenario / runbook docs (factual anchors,
  уже точны после Step 4), `docs/version-support-matrix.md`
  (точен после Step 4 PATH B note), `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`.
- **Selfcheck после Step 5.** Зелёный: registries без
  drift'а; selfcheck_status=ok; verify-release.ps1 GREEN
  на 8 checks; никаких 1cv8.exe runs; никаких real
  credentials.
- **Commit.** `78d5956` (Track E / Step 5 — support
  statement and docs alignment).

### Parallel Track E / Step 6 — final integration pass and Track E closure (завершён)

- **Цель шага.** Закрыть весь Track E как documented
  status. Read-only final integration check уже закрытых
  Steps 1–5, потом минимальные closure-docs/status
  updates, потом final closure commit. Никакого нового
  feature work, никаких новых MCP tools, никакого remote
  push'а, никакого 1cv8.exe run, никакого «дожимания»
  Step 4 задним числом.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 2 → 3 → 4 → 5 → 6
    (все commit'ы на месте);
  - все 6 Step 1–5 deliverables на диске:
    `track-e-multi-version-smoke-matrix-plan.md` (328
    строк), `track-e-multi-version-smoke-matrix-step-map.md`
    (324), `track-e-current-evidence-audit.md` (292),
    `track-e-smoke-scenario.md` (436),
    `docs/runbooks/track-e-multi-version-smoke-matrix.md`
    (484), `docs/version-support-matrix.md` (258 строк
    с reference row + Step 4 PATH B note);
  - Step 4 PATH B closure note на месте в matrix doc
    (lines 129–178);
  - Step 5 alignment confirmed в SECURITY +
    release-handoff;
  - registries `read=15 / write=25 / intelligence=16`
    без drift'а;
  - `verify-release.ps1 -AllowDirtyTree` GREEN на
    8 checks;
  - no real credentials в diff'ах ни одного из пяти
    Track E commit'ов.
- **Q5 resolved (closure decision).** Version bump
  0.2.0 → 0.3.0 — **НЕТ.** Track E ship'нул scaffolding +
  status alignment без functional delta (production code
  untouched, registries без drift'а, никаких evidence rows
  beyond reference). По SemVer logic'у MINOR bump
  оправдан для backward-compatible new functionality;
  Track E — pure documentation/process maturity track
  без functional change. Track E логически закрывается
  под существующим 0.2.0 как closure follow-up
  (симметрично pattern'у Track A/B/C под 0.1.0).
- **Что реально изменено на Step 6 (closure-docs only).**
  - `README.md` — Quickstart paragraph переписан под
    «Активного трека сейчас нет»; «Closed parallel
    tracks» list дополнен Track E bullet'ом
    (четыре → пять закрытых треков); «Active parallel
    track» секция сжата под «нет активного трека» с
    pointer'ом на Track E detail; добавлена «Track E
    detail (закрыт)» секция полным блоком симметрично
    Track A/B/C/D detail блокам (per-step bullets с
    commit hashes, что Track E реально закрыл, что
    Track E **не делает** «полной совместимостью»
    после closure, registry invariant).
  - `PROJECT-STATUS.md` — header (Текущий шаг + Статус)
    обновлён под Track E closed; общий narrative-блок
    переписан под closure; добавлены пять новых
    per-step секций (Steps 2/3/4/5/6); устаревший
    «Следующий шаг — Step 2» помечен как
    historical-snapshot.
  - `CHANGELOG.md` — добавлен новый «Parallel Track E
    follow-up — Multi-Version 1C Smoke Matrix» subsection
    под существующий 0.2.0 раздел с per-step outcomes,
    registry invariant note, honest constraints update;
    «Active work» в 0.2.0 секции обновлён под Track E
    closure («Track E was opened and closed within 0.2.0
    as a documentation/scaffolding follow-up, without a
    minor version bump»).
- **Что НЕ изменено на Step 6 (закрытый scope).**
  `pyproject.toml` (Q5 = НЕТ, version `0.2.0` сохраняется);
  `apps/`, `packages/`, `scripts/`, `examples/`, `.github/`,
  `.editorconfig`, `.python-version`, `.gitignore`,
  `LICENSE`; `SECURITY.md` (Step 5 уже выровнял);
  `docs/release-handoff.md` (Step 5 уже выровнял);
  `docs/version-support-matrix.md` (точен после Step 4);
  Track E planning/audit/scenario docs (frozen);
  `docs/runbooks/track-e-multi-version-smoke-matrix.md`
  (Step 3 deliverable, точен);
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*`
  (не задеты Track E); registries; `1cv8.exe` не
  запускался ни на одном шаге Track E.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на
  8 checks; никаких реальных credentials в Step 6 diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track E).**
  Активного шага не было. После Track E closure открыт
  шестой post-phase track — **Parallel Track F —
  Rollback Whitelist Expansion** — Step 1 которого
  закрыт сразу следом (см. секцию ниже).

### Parallel Track F / Step 1 — planning Rollback Whitelist Expansion (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track F — Rollback Whitelist Expansion**:
  назначение трека, целевой результат, что закрывает трек
  и что НЕ закрывает, чем отличается от Track A / B / C / D
  / E, guardrails, acceptance criteria, открытые вопросы
  Q1–Q7. Кода не писать. Никаких изменений registry. Никаких
  новых MCP tool'ов. Никаких запусков 1cv8.exe.
- **Назначение трека.** Существующий `_AUTOMATIC_RECOVERY_SUPPORTED`
  whitelist (`apps/platform/src/onec_platform/recovery.py:126-131`)
  содержит только два tool'а — `add_catalog_attribute` и
  `add_document_attribute`. Это наследие Phase 6 / Step 4,
  которая ship'нула minimum consistent slice (single-XML-file
  ops) и **зарезервировала expansion как отдельный шаг**
  (см. `apps/platform/README.md:799-802`). Phase 6 docs /
  Track A / D plans все ссылаются на «полная rollback-
  вселенная не покрыта (whitelist на двух tool'ах)» как на
  post-Phase-6 follow-up. Track F — тот самый отдельный
  шаг: он не переписывает архитектуру recovery'а, не
  добавляет новые MCP tools, не делает «universal rollback»
  fantasy. Его единственный честный продукт — узкое
  расширение whitelist'а для нескольких конкретных
  file-based mutating tools, чьи inverse semantics уже
  честно покрываются existing `restore_dump_file_from_snapshot`
  mechanism'ом.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-f-rollback-whitelist-expansion-plan.md` —
    зачем нужен Track F после Track E, стартовая точка
    (current rollback baseline + eligibility contract из
    `recovery.py:118-125` + `_KNOWN_WRITE_TOOL_FAMILIES`
    informational set), gap statement (asymmetric operator
    UX между whitelisted и Phase 6 / Step 5 add_form_attribute;
    готовность mechanism'а; existing honest follow-up
    constraint), целевой результат (formalized eligibility
    contract + per-tool audit + точечно расширенный
    whitelist + aligned operator-facing docs + no blanket
    reversibility claim), что входит / не входит,
    guardrails, 10 acceptance criteria, honest constraints
    after closure, связь с Track A / B / C / D / E, 7 open
    questions Q1–Q7.
  - **Один новый step-map:**
    `docs/architecture/track-f-rollback-whitelist-expansion-step-map.md` —
    шесть шагов: Step 1 (planning, этот), Step 2 (rollback
    baseline audit + candidate selection, docs-only —
    per-tool evaluation против criteria a/b/c, Tier 1/2/3/4
    breakdown, resolve Q2), Step 3 (rollback eligibility
    contract, docs-only — formalize a/b/c criteria + 3
    runtime gates + post-verify discipline + non-goals),
    Step 4 (narrow whitelist implementation — единственный
    шаг с production code change, **только**
    `apps/platform/src/onec_platform/recovery.py`,
    расширение `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset
    под Step 2 target set), Step 5 (operator/docs alignment
    — `apps/platform/README.md`, `README.md`,
    `docs/release-handoff.md` точечные wording-edits),
    Step 6 (final integration pass + Track F closure;
    Q5 — version bump 0.2.0 → 0.3.0 default ДА). Каждый
    шаг описан в формате Цель / Что меняем / Что НЕ меняем
    / Результат.
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`, `.github/`,
    `.editorconfig`, `.python-version`, `.gitignore`,
    `examples/`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`,
    `docs/release-handoff.md`, `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks/*`,
    `apps/platform/README.md` — без изменений на Step 1.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/src/onec_platform/recovery.py`, всех
    packages/.** Track F / Step 1 это documentation-only.
  - **Никакого реального rollback run** — production code
    не правился в этом шаге.
  - **Никакого audit doc, contract doc или whitelist
    expansion** — это Step 2 / Step 3 / Step 4
    соответственно.
  - **Никаких docs migration** в SECURITY.md /
    release-handoff.md / README — это Step 5.
  - **Никакого CHANGELOG update.** По симметрии с Track
    A / B / C / D / E (CHANGELOG обновляется один раз на
    closure трека).
  - **Никаких реальных credentials** в созданных docs /
    commit message — Track F не задевает credentials
    surface.
- **Что сказали явно в плане трека.**
  - Track F **не** закрывает: universal / arbitrary
    rollback для любого write-tool, AST-based semantic
    reverse engine, broad policy engine rewrite, public
    `delete_*` write-tools (categorically out-of-scope),
    multi-file / full filesystem snapshot-restore,
    rollback для `apply_config_from_files` (multi-file
    impact — violates criterion (a)) и
    `update_database_configuration` (DB schema migration —
    violates criterion (b)), rollback для `create_*` family
    (Tier 3 categorical exclusion — нет inverse semantics
    через snapshot restore), новые MCP tools (registries
    `read=15 / write=25 / intelligence=16` без drift'а),
    изменения `restore_dump_file_from_snapshot` API,
    изменения audit row format, execution-core rewrite,
    transport / UI / packaging work, enterprise governance /
    policy track, web UI, multi-version 1С matrix expansion
    (Track E территория), 1cv8.exe runs.
  - **GitHub remote push** — operator action, не часть
    трека.
- **Открытые вопросы Step 2+.** Q1 (eligibility criteria
  final formulation — default formalize existing
  `recovery.py:118-125` comment в Step 3), Q2 (exact target
  set tools для Step 4 — default candidate Tier 1 subset:
  `add_form_attribute`, `append_module_method`,
  `replace_module_method_body`; resolve в Step 2), Q3
  (`restore_dump_file_from_snapshot` API changes —
  default НЕТ), Q4 (audit row `details` format changes —
  default НЕТ; existing shape уже несёт всё необходимое),
  Q5 (closure version bump 0.2.0 → 0.3.0 — default ДА,
  Step 4 ship'ит real production code change с functional
  delta; resolve в Step 6), Q6 (operator-facing docs
  scope — default `apps/platform/README.md` + `README.md`
  + `docs/release-handoff.md`; resolve в Step 5), Q7
  (server-side write-server code changes допустимы —
  default НЕТ, Track F ограничивается `recovery.py`).
- **Selfcheck после Step 1.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track F / Step 1 не правил
  production-кода — drift'а нет.
- **Следующий шаг (на момент закрытия Step 1).**
  **Parallel Track F / Step 2 — rollback baseline audit and
  candidate selection (docs-only).** Step 2 / 3 / 4 / 5 / 6
  последовательно пройдены — см. секции ниже.

### Parallel Track F / Step 2 — rollback baseline audit and candidate selection (завершён)

- **Цель шага.** Read-only manual code review текущего
  rollback baseline + per-tool evaluation полного write-surface
  registry против eligibility criteria a/b/c + selection
  exact Step 4 target set (Q2 resolution). Никакая
  implementation. Никаких code changes. Никакого 1cv8.exe.
- **Что реально появилось в Step 2.** Один новый
  documentation-only документ:
  `docs/architecture/track-f-rollback-baseline-audit.md` (637
  строк). 9 sections: Purpose / scope; Current rollback
  baseline (две mirror frozenset'ы — critical finding о sync
  constraint в `flow.py:100-103`; `_RELATIVE_PATH_KEYS` 4-tuple;
  `_extract_relative_path` lookup; runtime gates; existing
  eligibility comment); Audited write surface (Group A/B/C/D/E/F
  breakdown 25 tools); Tiered candidate classification с
  per-tool manual code review evidence (file/line + payload
  key) — **Tier 4** (already, 2: `add_catalog_attribute`
  `catalog_relative_path` + `add_document_attribute`
  `document_relative_path`); **Tier 1** (strong, 4:
  `add_form_attribute` 3512-3520 `relative_path`,
  `add_form_element` 2680-2687 `relative_path`,
  `append_module_method` 2833-2838 `module_relative_path`,
  `replace_module_method_body` 2994-2999
  `module_relative_path`); **Tier 2** (deferred, 1:
  `update_module_code` payload key `target` НЕ matches
  `_RELATIVE_PATH_KEYS`); **Tier 3** (categorically excluded,
  5: 3 `create_*` family + `apply_config_from_files` +
  `update_database_configuration` с per-criterion violation
  citation); **Exact Step 4 target set recommendation (Q2
  resolution)**; Manual code review note (no runtime testing,
  no 1cv8.exe runs); Honest non-goals; Step 3 handoff note;
  Honest summary.
- **Что НЕ сделано (намеренно).** Никаких изменений
  production-кода. `recovery.py`, `flow.py`, `tools.py`,
  registries — все untouched. README / PROJECT-STATUS /
  CHANGELOG / SECURITY / release-handoff не тронуты (Step 5/6
  deliverables). Никаких runtime testing.
- **Q2 resolved.** Step 4 target set = 4 Tier 1 tools:
  `add_form_attribute`, `add_form_element`,
  `append_module_method`, `replace_module_method_body`.
  Whitelist 2 → 6 (на верхней границе plan'а Q2 «max 4»).
- **Selfcheck после Step 2.** Зелёный без правок: registries
  `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track F / Step 2 не правил
  production-кода — drift'а нет.
- **Commit.** `e9725b2` (Track F / Step 2 — rollback
  baseline audit and candidate selection).

### Parallel Track F / Step 3 — rollback eligibility contract (завершён)

- **Цель шага.** Formalize existing in-code eligibility
  comment (`recovery.py:118-125`) в отдельный prescriptive
  normative document. Никакого code change.
- **Что реально появилось в Step 3.** Один новый
  prescriptive normative document:
  `docs/architecture/track-f-rollback-eligibility-contract.md`
  (633 строки) с RFC 2119-style MUST / MUST NOT / SHALL /
  MAY wording — 64 normative keyword usages. 9 sections:
  Purpose / scope; Relationship to Step 2 audit (descriptive
  vs normative split); Current rollback model recap;
  **Eligibility criteria 4.A–4.F** (4.A payload shape via
  `flow.py:_RELATIVE_PATH_KEYS`; 4.B restore semantics
  single-file overwrite from snapshot; 4.C verification via
  existing `diff_dump_fragment`; 4.D sync discipline across
  both mirror frozenset'ов; 4.E non-expansion — exact Step 2
  target set; 4.F implementation surface — только
  `recovery.py` + `flow.py`); 9 categorical exclusions
  (multi-file / DB / create_* / public delete_* / AST /
  multi-file restore / new recovery API / audit shape
  changes / new MCP surface); Exact Step 4 implementation
  boundary с per-tool sanity check anchors + escape clause
  без silent target-set drift + verification protocol;
  Backward compatibility statement; Honest non-goals; Step 4
  handoff note.
- **Что НЕ сделано (намеренно).** Никакого code change.
  `recovery.py`, `flow.py`, `tools.py`, registries —
  untouched. Никаких изменений Step 2 audit'а или Step 2
  target set без proven blocker'а. Step 3 contract MUST
  NOT дублировать per-tool tier breakdown — это Step 2
  audit territory.
- **Resolved Q3, Q4.** Q3 (`restore_dump_file_from_snapshot`
  API без изменений) = ДА; Q4 (audit row `details` format
  без изменений) = ДА — оба явно зафиксированы в contract'е
  как нормативные обязательства.
- **Selfcheck после Step 3.** Зелёный: registries без
  drift'а; selfcheck_status=ok.
- **Commit.** `45ad2b2` (Track F / Step 3 — rollback
  eligibility contract).

### Parallel Track F / Step 4 — narrow rollback whitelist expansion (завершён)

- **Цель шага.** Расширить `_AUTOMATIC_RECOVERY_SUPPORTED` +
  `_ROLLBACK_SUPPORTED_OPERATIONS` mirror frozenset'ы до Step 2
  / Q2 target set строго в рамках Step 3 contract. **Это
  единственный шаг Track F с production code change.**
- **Что реально появилось в Step 4.** Two-file narrow
  expansion:
  - `apps/platform/src/onec_platform/recovery.py:126-133` —
    `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset 2 → 6 entries
    (added `add_form_attribute`, `add_form_element`,
    `append_module_method`, `replace_module_method_body`
    alphabetically). Eligibility comment lines 118-125
    untouched per minimal-touch preference.
  - `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:104-111`
    — `_ROLLBACK_SUPPORTED_OPERATIONS` frozenset 2 → 6
    identical entries. Plus minor sync-comment wording update
    lines 97-103: «Step 4 ships exactly two entries» →
    «Track F / Step 4 expanded this to six entries — keep
    identical to `_AUTOMATIC_RECOVERY_SUPPORTED` in
    `onec_platform.recovery`» (allowed per Step 3 contract
    Section 6.3.1).
- **Per-tool sanity check** в commit message с
  `tools.py` line numbers: add_form_attribute 3512-3520
  `relative_path`; add_form_element 2680-2687 `relative_path`;
  append_module_method 2833-2838 `module_relative_path`;
  replace_module_method_body 2994-2999 `module_relative_path`
  — все members `flow.py:_RELATIVE_PATH_KEYS`.
- **Что НЕ сделано (намеренно).** Никаких изменений
  `tools.py` (write-tool definitions); `_RELATIVE_PATH_KEYS`,
  `_extract_relative_path`, `_KNOWN_WRITE_TOOL_FAMILIES`,
  audit row `details` shape, runtime gates в
  `recovery.py:285,869`, `restore_dump_file_from_snapshot`
  API — всё untouched. Никаких изменений в `mcp-read-server`,
  `mcp-intelligence-server`, `apps/platform/` за пределами
  `recovery.py`, `packages/`, `scripts/`, `pyproject.toml`
  (это Step 6 territory если Q5 = ДА), `examples/`,
  `SECURITY.md`, `CHANGELOG.md`, operator-facing docs (это
  Step 5 territory). Никаких target-set drift'а; никаких
  опportunistic «while here» additions; никаких 1cv8.exe runs.
- **Verification.** verify-release.ps1 GREEN на 8 checks;
  registries `read=15 / write=25 / intelligence=16` без
  drift'а; selfcheck_status=ok. Identical 6-entry sets в
  обеих frozenset'ах verified Python parse.
- **Diff:** 2 files, +17 / -7 (recovery.py +4 / flow.py
  +13 / -7).
- **Commit.** `cd95627` (Track F / Step 4 — narrow rollback
  whitelist expansion).

### Parallel Track F / Step 5 — operator docs and rollback coverage alignment (завершён)

- **Цель шага.** Точечно выровнять operator-facing и
  project-facing docs под фактический post-Step-4 state
  (whitelist 2 → 6). Не менять продукт, не менять mechanism,
  не менять evidence — только wording alignment.
- **Что реально появилось в Step 5.** 8 точечных
  wording-edits в трёх docs:
  - `apps/platform/README.md` (5 правок): RECOVERY_MODES
    `executed`-mode wording (убрано stale «недостижимо: пуст»,
    добавлен evolution Phase 5→6→Track F с явным списком 6
    entries); section heading «Почему `_AUTOMATIC_RECOVERY_SUPPORTED`
    пуст» → «исторически был пуст и как он расширялся» с
    bridge paragraph про two-pass expansion + pointer на
    Track F eligibility contract; «Что rollback / recovery /
    audit UX сейчас НЕ делает» bullet «не выполняет ни для
    одного» → «выполняет только для whitelisted tools» с
    явным списком 6 entries; Phase 6 / Step 4 historical
    «Whitelist жёстко зафиксирован» bullet расширен под
    operationalized criterion (`_RELATIVE_PATH_KEYS`) +
    Track F / Step 4 4-tool addition citation; «Что Phase 6
    / Step 4 НЕ делал» bullets aligned + новая «Track F /
    Step 4 — расширение whitelist до 6 tools» subsection с
    rationale + invariants + Track F out-of-scope.
  - `README.md` (2 правки): Quickstart Track F open
    paragraph переписан под explicit «2 → 6 tools» с full
    list; Track A detail honest constraints bullet «whitelist
    остаётся на двух tool'ах» переписан под «расширен до 6
    tools после Track F / Step 4 ... всё ещё narrow set».
  - `docs/release-handoff.md` (1 правка): Known limitations
    «Limited rollback coverage» bullet переписан под explicit
    post-Track-F status с full 6-entry list + 24% surface
    metric + pointers на Track F plan/audit/contract docs.
- **Единый support statement** теперь aligned across 3
  modified docs: whitelist расширен 2 → 6; coverage broader
  but still narrow (24% mutating surface); not universal
  rollback; Tier 3 categorical exclusions remain
  out-of-scope.
- **Что НЕ сделано (намеренно).** PROJECT-STATUS.md и
  CHANGELOG.md не тронуты — closure deliverables Step 6.
  SECURITY.md не тронут — wording «small, deliberate set»
  остаётся качественно accurate (6 — still small set; 24%
  surface — still limited coverage); no direct factual drift.
  Никаких изменений в `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, registries, Track F planning / audit /
  contract docs, operator/admin/developer manuals,
  runbooks/*. Никаких 1cv8.exe runs. Никаких real
  credentials.
- **Selfcheck после Step 5.** Зелёный: registries без
  drift'а; verify-release.ps1 GREEN на 8 checks.
- **Commit.** `60f1761` (Track F / Step 5 — operator docs
  and rollback coverage alignment).

### Parallel Track F / Step 6 — final integration pass and Track F closure (завершён)

- **Цель шага.** Закрыть весь Track F как documented status.
  Read-only final integration check уже закрытых Steps 1–5,
  потом минимальные closure-docs/status updates +
  `pyproject.toml` version bump (Q5 = ДА), потом final
  closure commit. Никакого нового feature work, никаких
  новых MCP tools, никакого remote push'а, никакого
  1cv8.exe run.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 2 → 3 → 4 → 5 → 6 (все
    commit'ы на месте: `351278b → e9725b2 → 45ad2b2 →
    cd95627 → 60f1761 → этот closure`);
  - все Step 1–5 deliverables на диске: planning + step-map
    (358+326), audit (637), contract (633) docs;
  - Step 4 production code change verified: identical
    6-entry frozensets в обеих mirror locations (Python
    parse `recovery.py size=6 flow.py size=6 IDENTICAL=True`);
  - Step 5 operator-facing docs alignment confirmed: всех 3
    modified docs упоминают «6 entries/tools»;
  - registries `read=15 / write=25 / intelligence=16` без
    drift'а;
  - `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks
    с full selfcheck;
  - no real credentials в diff'ах ни одного из пяти Track F
    commit'ов;
  - никаких 1cv8.exe runs ни на одном шаге Track F.
- **Q5 resolved (closure decision) = ДА.** Version bump
  `0.2.0` → `0.3.0`. Reasoning: Track F / Step 4 ship'нул
  real production code change с **observable runtime
  behaviour delta** — `automatic_recovery_supported=True`
  теперь runtime-достижим для 4 дополнительных tool families
  через `run_rollback_assistant`. Это backward-compatible new
  functionality (existing 2 whitelisted tools работают
  identically; pre-Track-F audit rows backward-compat
  `details=None` → `mode='unsupported'` honest degrade;
  public API signatures preserved; audit `details` shape
  preserved). По SemVer logic'у это classic MINOR bump.
  Direct precedent — Track D `0.1.0 → 0.2.0` shipped
  comparable scale functional delta (`binary_dispatch.py`
  env-substitution + verify-release check 8); Track F
  shipped analogous (`recovery.py` + `flow.py` mirror
  frozenset extension). Track E (scaffolding only, no
  functional delta) → no bump; Track F (real code change)
  → bump.
- **Что реально изменено на Step 6 (closure-docs only).**
  - `pyproject.toml` — version `0.2.0` → `0.3.0` (Q5 = ДА).
  - `README.md` — Quickstart paragraph переписан под
    «Активного трека сейчас нет»; «Closed parallel tracks»
    list дополнен Track F bullet'ом (пять → шесть закрытых
    треков); «Active parallel track» секция сжата под «нет
    активного трека» с pointer'ом на Track F detail;
    добавлена «Track F detail (закрыт)» секция полным
    блоком симметрично Track A/B/C/D/E detail (per-step
    bullets с commit hashes, что Track F реально закрыл,
    что Track F **не делает** «полным rollback'ом всего»,
    registry invariant).
  - `PROJECT-STATUS.md` — header (Текущий шаг + Статус)
    обновлён под Track F closed + Q5 = ДА явное упоминание +
    5 commit hashes + factual whitelist size + 24% coverage
    metric + Tier 3 exclusions; общий narrative-блок
    переписан под closure; добавлены пять новых per-step
    секций (Steps 2/3/4/5/6); устаревший «Следующий шаг —
    Step 2» помечен как historical-snapshot.
  - `CHANGELOG.md` — добавлен новый раздел `## 0.3.0 —
    Parallel Track F — Rollback Whitelist Expansion` с
    per-step outcomes, registry invariant, honest
    constraints update (no blanket reversibility claim).
- **Что НЕ изменено на Step 6 (закрытый scope).** `apps/`,
  `packages/`, `scripts/`, `examples/`, `.github/`,
  `.editorconfig`, `.python-version`, `.gitignore`,
  `LICENSE`; `SECURITY.md` (Step 5 inventory подтвердил
  «small, deliberate set» wording качественно accurate);
  `docs/release-handoff.md` (Step 5 уже выровнял);
  `apps/platform/README.md` (Step 5 уже выровнял);
  Track F planning / audit / contract docs (frozen
  Step 1/2/3 anchors); Track A/B/C/D/E docs; runbooks;
  registries; `1cv8.exe` не запускался ни на одном шаге
  Track F.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8 checks;
  никаких реальных credentials в Step 6 diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track F).**
  Активного шага не было. После Track F closure открыт
  седьмой post-phase track — **Parallel Track G —
  Production-Grade MCP Transport and CLI** — Step 1
  которого закрыт сразу следом (см. секцию ниже).

### Parallel Track G / Step 1 — planning Production-Grade MCP Transport and CLI (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track G — Production-Grade MCP Transport and
  CLI**: назначение трека, целевой результат, что
  закрывает трек и что НЕ закрывает, чем отличается от
  Track A / B / C / D / E / F, guardrails, acceptance
  criteria, открытые вопросы Q1–Q7. Кода не писать.
  Никаких изменений registry. Никаких новых MCP tool'ов.
  Никаких запусков 1cv8.exe.
- **Назначение трека.** После closure'а Track F (Rollback
  Whitelist Expansion) у проекта есть сильное
  execution-ядро (Phase 1–6) + сильная docs/product
  shell (Tracks B/C/D/E) + расширенная rollback coverage
  (Track F), но **operational run story для MCP servers
  всё ещё не доведена до production-grade состояния**.
  Concrete gaps: никакого `__main__.py` ни в одном из
  4 packages (`mcp_read_server`, `mcp_write_server`,
  `mcp_intelligence_server`, `onec_platform`); никакого
  `[project.scripts]` console entry points в
  `pyproject.toml`; никакого MCP protocol implementation
  (server.py содержит только tool registry skeleton, не
  JSON-RPC framing); никакого CLI surface; никакого
  operator-facing «how to start MCP server in production»
  SSOT runbook. Этот gap уже зафиксирован как honest
  constraint в `SECURITY.md` («No production-grade MCP
  transport yet»), `docs/release-handoff.md`, `README.md`
  Quickstart, Track A/D plan + Phase 6 docs + Track F
  closure recommendation. Track G — седьмой post-phase
  parallel track, который ship'ит **первый
  production-grade слой** этого operational gap'а.
- **Что реально появилось в Step 1.**
  - **Один новый план трека:**
    `docs/architecture/track-g-production-grade-mcp-transport-and-cli-plan.md`
    — зачем нужен Track G после Track F, стартовая точка
    (read-only inventory: 4 packages без `__main__.py`;
    `pyproject.toml` без `[project.scripts]`; `server.py`
    skeleton только с `list_tools()` / `get_tool(name)`;
    existing `apps/platform/runtime.py` Phase 5/Step 3 +
    Phase 6/Step 6 process orchestration layer не задевается),
    gap statement (5 concrete gaps), целевой результат
    (canonical `__main__.py` × 3 + minimal stdio JSON-RPC
    transport + CLI surface + `[project.scripts]` console
    entries + aligned operator-facing docs + no security
    claim beyond local trusted environment), что входит /
    не входит, guardrails, 11 acceptance criteria, honest
    constraints after closure, связь с Track A / B / C / D /
    E / F, 7 open questions Q1–Q7.
  - **Один новый step-map:**
    `docs/architecture/track-g-production-grade-mcp-transport-and-cli-step-map.md`
    — шесть шагов: Step 1 (planning, этот), Step 2
    (transport / entrypoint baseline audit, docs-only —
    per-server inventory + integration points + resolve
    Q1/Q2/Q6), Step 3 (exact runtime / CLI / entrypoint
    contract, docs-only — RFC 2119-style normative contract:
    `__main__.py` shape, CLI surface, transport contract,
    tool dispatch, auth contract «none on transport»,
    supervision integration через existing product runtime,
    `[project.scripts]` contract, backward compatibility,
    implementation surface, non-goals, verification
    contract; resolve Q3/Q4/Q5), Step 4 (narrow
    implementation slice — единственный шаг с production
    code change: 3 new `__main__.py` files + minimal stdio
    MCP transport + CLI flag parsing + `[project.scripts]`
    block в `pyproject.toml`; optional minor adjustments
    в `server.py` если absolutely necessary; verification
    `python -m <server> --help` все возвращают exit 0 +
    non-empty usage), Step 5 (operator/docs alignment —
    Quickstart + handoff + SECURITY + apps/platform/README
    + scripts/dev/launch.ps1 + optional new short runbook),
    Step 6 (final integration pass + Track G closure;
    Q7 default ДА version bump 0.3.0 → 0.4.0). Каждый шаг
    описан в формате Цель / Что меняем / Что НЕ меняем /
    Результат.
- **Что НЕ сделано (намеренно).**
  - **Никаких изменений production-кода.** `apps/`,
    `packages/`, `scripts/`, `pyproject.toml`, `.github/`,
    `.editorconfig`, `.python-version`, `.gitignore`,
    `examples/`, `LICENSE`, `SECURITY.md`, `CHANGELOG.md`,
    `docs/release-handoff.md`, `docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks/*`,
    `apps/platform/README.md`, `server.py` files — без
    изменений на Step 1.
  - **Никаких изменений в `mcp-read-server`,
    `mcp-write-server`, `mcp-intelligence-server`,
    `apps/platform/`, всех packages/.** Track G / Step 1
    это documentation-only.
  - **Никакого `__main__.py` файла** — это Step 4.
  - **Никакого baseline audit doc** — это Step 2.
  - **Никакого normative contract** — это Step 3.
  - **Никакого docs migration** — это Step 5.
  - **Никакого CHANGELOG update.** По симметрии с Track
    A / B / C / D / E / F (CHANGELOG обновляется один
    раз на closure трека).
  - **Никаких реальных credentials** в созданных docs /
    commit message — Track G не задевает credentials
    surface.
- **Что сказали явно в плане трека.**
  - Track G **не** закрывает: HTTP / WebSocket / SSE
    network transports (отдельный subsequent track),
    authentication / authorization / token validation /
    mTLS / OAuth / SAML / OpenID Connect / RBAC /
    multi-tenant isolation, supervision daemon / systemd
    unit / Windows Service registration / automatic
    restart watcher, HA / clustering / multi-node,
    service discovery / load balancing, distributed
    tracing / observability stack, web UI / dashboard
    frontend, packaging ecosystem (`.msi` / `.deb` / GUI
    installer / signed distribution / PyPI publication)
    beyond `[project.scripts]` console entries, full
    enterprise super-set (SSO/RBAC/multi-tenant/secrets
    vault as service / federated audit / policy-as-code
    DSL), 1cv8.exe execution work, rollback work,
    AST / metadata work, multi-version 1С matrix
    expansion, новые MCP tools (registries без drift'а),
    hot reload, remote push.
  - **GitHub remote push** — operator action, не часть
    трека.
- **Открытые вопросы Step 2+.** Q1 (transport choice
  для Step 4 — default stdio only; HTTP/WebSocket
  out-of-scope; resolve в Step 2), Q2 (`mcp` Python SDK
  vs custom — default «зависит от availability в
  dependency graph» с manual code review SDK shape;
  resolve в Step 2), Q3 (CLI flag set — default minimal:
  `--help`, `--config-path`, `--transport stdio`,
  `--log-level`; resolve в Step 3), Q4 (auth posture —
  default НЕТ на transport уровне; security model =
  trusted local environment; resolve в Step 3), Q5
  (supervision integration — default через existing
  `apps/platform/runtime.py` boundary; никакого нового
  supervisor daemon Track G не ship'ит; resolve в Step 3),
  Q6 (`apps/platform` standalone entrypoint —
  out-of-scope initial Track G по умолчанию; resolve в
  Step 2), Q7 (closure version bump 0.3.0 → 0.4.0 —
  default ДА; Step 4 ship'ит real code change with
  functional delta = backward-compatible new
  functionality, classic MINOR bump per SemVer; resolve
  в Step 6).
- **Selfcheck после Step 1.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track G / Step 1 не правил
  production-кода — drift'а нет.
- **Следующий шаг (historical snapshot, на момент
  закрытия Step 1).** Parallel Track G / Step 2 —
  transport / entrypoint baseline audit (docs-only).
  Этот раздел сохранён как исторический снимок намерений
  на момент Step 1; фактический Step 2 закрылся
  отдельным заходом — см. секцию Step 2 ниже.

### Parallel Track G / Step 2 — transport baseline audit (завершён)

- **Цель шага.** Закрыть Q1 (transport choice), Q2
  (`mcp` Python SDK availability vs custom), Q6
  (`apps/platform` standalone entrypoint scope) на основе
  read-only evidence — без code changes, без новых planning
  документов помимо одного descriptive audit. Никакого 1cv8.exe.
- **Что реально сделано.** Один новый documentation-only
  audit-документ
  `docs/architecture/track-g-transport-baseline-audit.md`
  (587 строк) — per-server inventory current state,
  4-class breakdown (already useful baseline / adjacent
  insufficient / clearly missing / out-of-scope),
  read-only evidence ссылки. Critical findings: pyproject.toml
  имеет zero declared runtime deps (no `[project.dependencies]`
  block at all), zero MCP SDK imports anywhere в repo,
  все 3 MCP server packages идентичная structure без
  `__main__.py`, `apps/platform/runtime.py` 8 boundary
  functions — generic process orchestration, не MCP transport,
  `scripts/dev/launch.ps1` явно говорит «does NOT start MCP
  servers».
- **Resolved decisions.**
  - **Q1 = stdio only.** HTTP / WebSocket / SSE / TCP /
    named pipe network transports — out-of-scope Track G;
    trusted local environment security model.
  - **Q2 = CUSTOM IMPLEMENTATION на stdlib only.** Никаких
    новых deps в `pyproject.toml`, никакого upstream `mcp`
    PyPI SDK, никаких third-party JSON-RPC libraries
    (`jsonrpcserver` / `jsonrpc-base` / etc.). Reasoning
    evidence-grounded: zero deps declared, zero SDK
    imports.
  - **Q6 = OUT-OF-SCOPE Track G.** Step 4 ship'ит
    `__main__.py` для **3 MCP server packages, не 4**;
    `apps/platform` standalone entrypoint — отдельный
    future track.
- **Что НЕ изменено на Step 2.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `docs/release-handoff.md`, `docs/operator-manual.md`,
  `apps/platform/README.md`, `README.md`,
  `PROJECT-STATUS.md`, `CHANGELOG.md`. Production-код
  не правится. Registries `15/25/16` без drift'а.
  Никаких 1cv8.exe runs.
- **Selfcheck после Step 2.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `6f3ad73`.

### Parallel Track G / Step 3 — runtime CLI and entrypoint contract (завершён)

- **Цель шага.** Зафиксировать exact prescriptive
  normative contract для Step 4 narrow implementation
  slice — какие правила соблюдает каждый `__main__.py`,
  какой exact CLI shape, какой exact transport scope,
  какой server binding / dispatch contract, какая auth /
  supervision posture, какой `[project.scripts]` block,
  какие backward compatibility guarantees, какая exact
  Step 4 implementation surface (allowed / forbidden
  files), какой verification protocol. Никакого code
  change. Никакого 1cv8.exe.
- **Что реально сделано.** Один новый prescriptive
  normative document
  `docs/architecture/track-g-runtime-cli-entrypoint-contract.md`
  (879 строк) с RFC 2119-style MUST / MUST NOT / SHALL /
  SHOULD / MAY wording (85 normative keyword usages).
  15 sections: Purpose / scope; Relationship to Step 1
  plan and Step 2 audit (descriptive vs normative split);
  Inherited fixed decisions (Q1 / Q2 / Q6); `__main__.py`
  contract (exact 3 file paths + main() shape + 6 required
  responsibilities + forbidden patterns); CLI contract
  (exact 4 flags `--help` / `--config-path` /
  `--transport` / `--log-level` + validation +
  forbidden subcommands); Transport contract (stdio
  JSON-RPC 2.0 only + forbidden libraries +
  stdout/stderr discipline + minimum-viable MCP method
  set initialize/tools.list/tools.call + error
  handling); Server binding / dispatch contract (allowed
  imports + tool registry consumption via existing
  `list_tools()` / `get_tool()` boundary +
  `server.py` adjustment policy + `run_write_flow`
  invariants); Auth contract (no auth, trusted local
  stdio); Supervision contract (reuse existing
  `runtime.py` boundary без extension);
  `[project.scripts]` contract (3 entries; no
  `[project.dependencies]`); Backward compatibility
  (15/25/16 registries + `mcp_common` API +
  scripts/dev/release + audit shape preserved); **Exact
  Step 4 implementation surface** — 4 allowed file
  groups (3 new `__main__.py` + `pyproject.toml`
  `[project.scripts]` + optional minor `__init__.py` /
  `server.py` doc adjustments + optional private
  `mcp_common._stdio_transport` helper if reduces ≥ 50%
  duplication; default inlined); comprehensive forbidden
  file list; scope-creep markers; Verification contract;
  Honest non-goals; Step 4 handoff note.
- **Что НЕ изменено на Step 3.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `README.md`, `PROJECT-STATUS.md`, `CHANGELOG.md`.
  Production-код не правится. Registries `15/25/16` без
  drift'а. Никаких 1cv8.exe runs.
- **Selfcheck после Step 3.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `8bb3883`.

### Parallel Track G / Step 4 — narrow stdio transport and CLI entrypoints (завершён)

- **Цель шага.** Единственный шаг Track G с production
  code change. Реализовать ровно тот узкий implementation
  slice, который зафиксирован в Step 3 contract: 3 new
  `__main__.py` files + `pyproject.toml [project.scripts]`
  + optional private helper. Никакого scope creep,
  никаких новых MCP tools, никакого 1cv8.exe.
- **Implementation path = PATH B.** PATH A pure inline был
  отвергнут потому что каждый `__main__.py` carried бы
  ~140 LOC идентичных argparse / JSON-RPC framing /
  dispatch logic — ~280 LOC pure copy-paste через 3
  server'а — qualifies as "duplication otherwise
  unreasonable" под Step 3 contract §12.1.4. PATH C
  (`server.py` adjustments) был отвергнут как unnecessary —
  existing `list_tools()` / `get_tool(name)` boundary
  достаточен.
- **Ship'нуто 5 файлов (+361 lines).**
  - `packages/mcp-common/src/mcp_common/_stdio_transport.py`
    (новый, 245 LOC) — underscore-prefixed internal
    helper, **NOT** экспортирован из
    `mcp_common/__init__.py`; pure stdlib (`argparse`,
    `json`, `logging`, `inspect`, `sys`); реализует
    line-delimited JSON-RPC 2.0 loop, четыре required
    CLI флага, handlers для `initialize` / `ping` /
    `tools/list` / `tools/call` /
    `notifications/initialized` /
    `notifications/cancelled`, serialization
    `ToolResult` → MCP envelope (`content` +
    `structuredContent` + `isError`),
    top-of-`run_main` exception boundary; stdout
    reserved для JSON-RPC envelopes, диагностика —
    в stderr через `logging`.
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
    (новый, ~30 LOC).
  - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
    (новый, ~30 LOC).
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    (новый, ~30 LOC) — каждый определяет `main() →
    int` которая зовёт `run_main` с per-package's
    existing `list_tools` / `get_tool` boundary и
    per-server name + version. No `__init__.py` edits,
    no `server.py` edits, no `tools.py` / `models.py`
    / `runtime/` / `apps/platform/` touches.
  - `pyproject.toml` (edit) — добавлен
    `[project.scripts]` block с ровно тремя console
    entries (`mcp-read-server`, `mcp-write-server`,
    `mcp-intelligence-server`). Никаких новых deps;
    `[tool.hatch.build.targets.wheel] packages = []`
    preserved unchanged (Track C / Step 3 honest
    constraint kept).
- **Verification.**
  - `python -m mcp_read_server --help` → exit 0;
    usage shows все четыре required flags.
  - `python -m mcp_write_server --help` → exit 0, same.
  - `python -m mcp_intelligence_server --help` →
    exit 0, same.
  - `verify-release.ps1 -AllowDirtyTree` GREEN на 8
    checks; selfcheck registries `read=15 / write=25 /
    intelligence=16; status=ok`; `imports_ok=true`.
  - Narrow stdio sanity: piping
    `initialize` / `tools/list` / `tools/call ping`
    в `mcp_read_server` returns valid JSON-RPC
    envelopes (15 tools enumerated с docstring-
    derived descriptions; ping `ToolResult` serialized
    as `content` + `structuredContent` с
    `isError=false`); EOF on stdin → clean exit 0;
    garbled input → `-32700 Parse error` envelope с
    continued loop (§6.6 fail-soft behavior verified).
- **Что НЕ изменено на Step 4.** `apps/*/src/*/server.py`,
  `apps/*/src/*/__init__.py`, `apps/*/src/*/tools.py`,
  `apps/*/src/*/models.py`, `apps/*/src/*/runtime/*`,
  `apps/platform/*`, `packages/*/src/*` (кроме нового
  private `_stdio_transport.py` в `mcp_common`),
  `scripts/*`, `examples/*`, all docs (Step 5/6
  territory), registries. Никаких 1cv8.exe runs.
- **Selfcheck после Step 4.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks. Commit `370c5a8`.

### Parallel Track G / Step 5 — operator docs and transport alignment (завершён)

- **Цель шага.** Точечно выровнять operator-facing и
  status-adjacent документацию под фактический
  transport / CLI surface, который ship'нут на Step 4 —
  без раздувания в closure narrative Step 6.
  Docs-only; никакого production code change; никакого
  pyproject.toml; никаких registry changes; никакого
  1cv8.exe.
- **Что реально сделано (6 files +229/-81 lines).**
  - `README.md` — Quickstart paragraph переписан под
    Steps 1-4 closed / Step 5 active; «Что Quickstart
    не обещает» reworded acknowledging local stdio
    baseline while keeping network / auth / installer /
    web-UI / supervisor / wheel /
    `apps/platform`-standalone gaps explicit; «Active
    parallel track» секция enumerates closed Steps
    1-4 с artifacts, фактический Step 4 launch surface,
    registries invariant, canonical Step 6 next.
    Track G НЕ объявлен closed; трек НЕ перенесён в
    closed list; никакого version bump.
  - `SECURITY.md` — bullet «No production-grade MCP
    transport yet» заменён на «Local stdio MCP
    transport only» block: explicit list что Step 4
    ship'нул; threat model = local trusted stdio
    boundary; explicit list что still NOT built-in
    (auth / multi-tenant / hardened network /
    supervisor / systemd / Windows Service); explicit
    «не претендует на production-readiness для
    adversarial network deployment».
  - `docs/release-handoff.md` — новый bullet под «What
    is in this handoff» listing три `python -m`
    entrypoints + CLI flags + `[project.scripts]`
    console entries с trusted-stdio-only caveat;
    «What is NOT in this handoff» reworded; «Local
    check / launch sequence» parenthetical replaced;
    «Known limitations» bullet aligned с new SECURITY.md.
  - `apps/platform/README.md` — 4 locations rewritten
    под Step 4 baseline: Phase 5 / Step 3 callout про
    CLI / `__main__`; «Чего сейчас намеренно ещё нет»
    production-grade-transport item; parallel listing;
    Phase 6 honest-constraints «Нет production-grade
    MCP transport / `__main__` / CLI» item — все
    acknowledge Step 4 closure of local trusted-stdio
    baseline preserving network / auth / supervisor
    out-of-scope.
  - `scripts/dev/launch.ps1` — header comment block +
    `Show-Usage` help text — operators pointed at
    `python -m <server> --help`; transport caveat
    preserved.
  - `scripts/dev/README.md` — две parenthetical
    wording fixes + CI workflow note distinguishes
    live MCP runtime от import / wiring / registry-
    count selfcheck.
- **Что НЕ изменено на Step 5.** Production code
  (`apps/*/src`, `packages/*/src` — Step 5 docs-only by
  contract), `pyproject.toml` (Q7 = Step 6 territory),
  registries / new MCP tools (`read=15 / write=25 /
  intelligence=16` invariant), `PROJECT-STATUS.md`
  (header + per-step closure narrative + final closure
  summary block — Step 6 territory per Track A/B/C/D/E/F
  symmetry), `CHANGELOG.md` (новая `## 0.4.0` section —
  Q7 / Step 6 closure deliverable).
- **Verification.** Working tree contains только 6
  expected docs changes; production code untouched;
  `verify-release.ps1 -AllowDirtyTree` GREEN на 8
  checks; selfcheck registries `read=15 / write=25 /
  intelligence=16; status=ok`; никаких 1cv8.exe runs;
  никаких premature Track G closure phrasings (grep
  verified — единственный `Track G closure` match —
  это forward-looking name следующего Step 6 «final
  integration pass and Track G closure», не current
  closure claim); никаких false network / auth claims.
- **Selfcheck после Step 5.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks. Commit `5890ba5`.

### Parallel Track G / Step 6 — final integration pass and Track G closure (завершён)

- **Цель шага.** Закрыть весь Track G как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates + `pyproject.toml` version bump
  (Q7 = ДА), потом final closure commit. Никакого
  нового feature work, никаких новых MCP tools,
  никакого remote push'а, никакого 1cv8.exe run.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 2 → 3 → 4 → 5 → 6
    (все commit'ы на месте: `7a39454 → 6f3ad73 →
    8bb3883 → 370c5a8 → 5890ba5 → этот closure`);
  - все Step 1–5 deliverables на диске: 4 architecture
    docs (plan + step-map + baseline-audit + contract);
    4 Step 4 implementation files (3 `__main__.py` +
    `_stdio_transport.py`); `pyproject.toml`
    `[project.scripts]` block at line 22;
  - Step 5 operator-facing docs alignment confirmed:
    SECURITY / release-handoff / apps/platform/README /
    scripts/dev/* всё говорят one truth — local stdio
    transport baseline exists, network / auth /
    supervisor still out-of-scope;
  - registries `read=15 / write=25 / intelligence=16`
    без drift'а;
  - `verify-release.ps1 -AllowDirtyTree` GREEN на 8
    checks с full selfcheck;
  - no real credentials в diff'ах ни одного из пяти
    Track G commit'ов;
  - никаких 1cv8.exe runs ни на одном шаге Track G.
- **Q7 resolved (closure decision) = ДА.** Version bump
  `0.3.0` → `0.4.0`. Reasoning: Track G / Step 4
  ship'нул real production code change с **observable
  runtime capability delta** — `python -m
  mcp_read_server`, `python -m mcp_write_server`,
  `python -m mcp_intelligence_server` теперь реально
  стартуют stdio JSON-RPC 2.0 server, что до Track G
  было невозможно (`No module named ...` error).
  Backward-compatible new functionality (existing
  `list_tools()` / `get_tool(name)` API preserved
  byte-identical; `mcp_common` public API export'ы
  preserved byte-identical — helper underscore-prefixed
  и **NOT** добавлен в `__init__.py`'s `__all__`;
  registries `15/25/16` invariant; audit `details`
  shape preserved; no public symbol removed or
  renamed). По SemVer logic'у это classic MINOR bump.
  Direct precedent — Track D `0.1.0 → 0.2.0`
  (env-substitution + verify-release check 8) и
  Track F `0.2.0 → 0.3.0` (whitelist 2 → 6) shipped
  comparable scale functional delta. Track E
  (scaffolding only, PATH B / no functional delta) →
  no bump; Track G (real code change) → bump.
- **Что реально изменено на Step 6 (closure-docs only).**
  - `pyproject.toml` — version `0.3.0` → `0.4.0`
    (Q7 = ДА).
  - `README.md` — Quickstart paragraph переписан под
    «Активного трека сейчас нет»; «Closed parallel
    tracks» list дополнен Track G bullet'ом
    (шесть → семь закрытых треков); «Active parallel
    track» секция сжата под «нет активного трека» с
    pointer'ом на Track G detail; добавлена «Track G
    detail (закрыт)» секция полным блоком симметрично
    Track A/B/C/D/E/F detail (per-step bullets с
    commit hashes, что Track G реально закрыл, что
    Track G **не делает** «production-deployment-ready
    MCP сервером для adversarial network», registry
    invariant).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track G closed + Q7 = ДА
    явное упоминание + 6 commit hashes + factual
    Step 4 surface + PATH B reasoning; общий
    narrative-блок переписан под closure; добавлены
    пять новых per-step секций (Steps 2/3/4/5/6);
    устаревший «Следующий шаг — Step 2» помечен как
    historical-snapshot.
  - `CHANGELOG.md` — добавлен новый раздел `## 0.4.0
    — Parallel Track G — Production-Grade MCP Transport
    and CLI` с per-step outcomes, registry invariant,
    actual launch surface, honest constraints update
    (no network / auth / supervisor / standalone
    `apps/platform` / 1cv8 / new MCP tools).
- **Что НЕ изменено на Step 6 (закрытый scope).**
  `apps/`, `packages/`, `scripts/`, `examples/`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`; `SECURITY.md` (Step 5
  inventory подтвердил «Local stdio MCP transport
  only» wording качественно accurate);
  `docs/release-handoff.md` (Step 5 уже выровнял);
  `apps/platform/README.md` (Step 5 уже выровнял);
  `scripts/dev/launch.ps1` + `scripts/dev/README.md`
  (Step 5 уже выровнял); Track G planning / audit /
  contract docs (frozen Step 1/2/3 anchors); Track
  A/B/C/D/E/F docs; runbooks; registries; `1cv8.exe`
  не запускался ни на одном шаге Track G.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks; никаких реальных credentials в Step 6
  diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track G).**
  Активного шага нет. Семь post-phase parallel track'ов
  (A, B, C, D, E, F, G) закрыты последовательно;
  Phase 7 как линейная фаза не запланирована. Открытие
  следующего параллельного трека — отдельное operator
  decision. Логичные кандидаты (без автоматического
  открытия): network-grade MCP transport track
  (HTTP / WebSocket / SSE поверх Track G stdio
  baseline), authentication / authorization track,
  supervisor / service-registration track,
  `apps/platform` standalone entrypoint track,
  packaging ecosystem track, real MCP client
  integration test track, multi-version 1С matrix
  expansion (post-Track-E follow-up).

  Один из этих кандидатов был выбран: см. секцию
  Track H / Step 1 ниже.

### Parallel Track H / Step 1 — planning Network-Grade MCP Transport and Authentication Boundary (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track H — Network-Grade MCP Transport and
  Authentication Boundary**: назначение трека (следующий
  слой зрелости поверх Track G — добавить один
  network-facing MCP transport family и один minimum
  authentication baseline, additive над existing local
  stdio surface), целевой результат, что закрывает /
  не закрывает Track H, чем отличается от Tracks A–G,
  guardrails, acceptance criteria, открытые вопросы Q1–Q7.
  Кода не писать. Никаких изменений registry. Никаких
  новых MCP tool'ов. Никаких запусков 1cv8.exe.
- **Что реально сделано (документ-only Step 1).**
  Ship'нуты два planning-документа в
  `docs/architecture/`:
  - `track-h-network-grade-mcp-transport-and-authentication-boundary-plan.md` —
    plan-уровень: 11 sections (зачем нужен Track H после
    Track G; стартовая точка post-Track-G factual
    baseline + per-package gap inventory verified
    grep'ом zero hits на `http.server` / `aiohttp` /
    `websockets` / `socketserver` / `asyncio.start_server`
    / `bearer` / `jwt` / `oauth` / `x509` в `apps/*/src` и
    `packages/*/src`; цель Track H; что входит in scope —
    documentation surface + Step 4 implementation surface
    + Step 5 docs alignment + Step 6 closure deliverables;
    что НЕ входит — full enterprise identity stack /
    full zero-trust perimeter / web UI / packaging
    ecosystem / full service management ecosystem /
    новые MCP tools / 1cv8 work / rollback / AST /
    multi-version / standalone `apps/platform` /
    distributed tracing / remote push; 13 guardrails
    (registry invariant, no new MCP tools, stdio
    baseline preserved, `mcp_common` public API
    byte-identical, `run_write_flow` discipline preserved,
    read-only intelligence preserved, no
    `[project.dependencies]` as mandatory baseline без
    обоснования, no real credentials, no 1cv8.exe runs,
    production code only Step 4 на explicit allowed
    surfaces, wheel-build empty preserved, no premature
    enterprise-ready claim, no remote push); 12
    acceptance criteria; honest constraints после closure;
    relation to prior tracks A–G; open questions Q1–Q7
    с default recommendations).
  - `track-h-network-grade-mcp-transport-and-authentication-boundary-step-map.md` —
    step map: 6 шагов (Step 1 planning / Step 2 baseline
    audit / Step 3 normative contract / Step 4
    implementation / Step 5 docs alignment / Step 6
    closure) с per-step Цель / Что меняем / Что НЕ
    меняем / Результат format'ом, mirror Track G
    step-map structure.
- **Open questions Q1–Q7 (default recommendations).**
  - **Q1 = HTTP-based MCP boundary** (default planning
    anchor; финал — Step 2 audit / Step 3 contract).
    Reasoning: ближе к practical client/server deployment
    story, честнее для near-enterprise trajectory, чем
    raw WebSocket-first.
  - **Q2 = exactly one** transport family. Reasoning:
    narrowest honest scope; multi-transport matrix —
    отдельный future track.
  - **Q3 = static bearer token** (default planning
    anchor; финал — Step 2 / Step 3). Reasoning:
    минимальный реальный security perimeter без
    enterprise identity explosion; переиспользует
    Track D `${ENV:NAME}` pattern для secret config.
  - **Q4 = existing config model boundary** (default;
    финал — Step 3). Reasoning: никакого parallel
    config path; operator-managed secret path остаётся
    acceptable; vault / KMS / OS keychain — post-Track-H
    tracks.
  - **Q5 = НЕТ supervisor / service layer внутри
    Track H.** Reasoning: не смешивать transport / auth
    с process lifecycle track; supervisor / systemd /
    Windows Service / hot reload — отдельный следующий
    трек post-Track-H.
  - **Q6 = НЕТ standalone `apps/platform` entrypoint
    в Track H.** Carry-over out-of-scope from Track G
    Q6.
  - **Q7 = likely YES** (`0.4.0` → `0.5.0`) если Step 4
    ship'нет real transport/auth capability; финальное
    решение — Step 6 closure decision на основе
    фактического Step 4 functional delta. Precedent —
    Track D `0.1.0 → 0.2.0`, Track F `0.2.0 → 0.3.0`,
    Track G `0.3.0 → 0.4.0`.
- **Что НЕ изменено на Step 1 (закрытый scope).**
  `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*`,
  `apps/platform/README.md`, server `server.py` files,
  three `__main__.py` files, `_stdio_transport.py`
  helper. Никаких real credentials в commit message —
  Track H не задевает credentials infrastructure.
  Никакого 1cv8.exe.
- **Selfcheck после Step 1.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track H / Step 1 не правил
  production-кода — drift'а нет.
- **Следующий шаг (historical snapshot, на момент
  закрытия Step 1).** Parallel Track H / Step 2 —
  transport / auth baseline audit (docs-only). Этот
  раздел сохранён как исторический снимок намерений
  на момент Step 1; фактический Step 2 закрылся
  отдельным заходом — см. секцию Step 2 ниже.

### Parallel Track H / Step 2 — transport and auth baseline audit (завершён)

- **Цель шага.** Resolve Q1 (transport family), Q2
  (transport family count), Q3 (auth baseline), Q4
  (auth config home) на основе read-only inspection
  current repo state. Никакого code change. Никакого
  1cv8.exe.
- **Что реально сделано.** Один новый descriptive
  audit-документ
  `docs/architecture/track-h-transport-and-auth-baseline-audit.md`
  (1085 lines, 11 sections). Per-server / per-package /
  per-pyproject inventory + 4-class breakdown
  (11 reusable surfaces / 8 adjacent / 11 missing
  pieces / 12 out-of-scope) + read-only evidence
  (zero hits across 8 grep categories: HTTP server
  libs, SSE, WebSocket, TCP, TLS, auth, sessions,
  rate-limit). Per-Q resolution с per-option pros/cons
  + per-option rejection reasoning.
- **Resolved decisions.**
  - **Q1 = HTTP-based MCP transport** (line-delimited
    POST + optional SSE deferred). Reasoning: stdlib
    `http.server.ThreadingHTTPServer` достаточен для
    Q2-inheritance pure-stdlib baseline без
    `[project.dependencies]`; reverse-proxy ecosystem
    даёт TLS-termination story; MCP-spec compatibility;
    WebSocket / raw SSE / TCP / Unix socket / named
    pipe rejected per-option.
  - **Q2 = exactly one** transport family. Track H
    plan §4.2 + §6 guardrail #2 + Track G precedent +
    multi-transport-matrix complexity rejection.
  - **Q3 = static bearer token** via `Authorization:
    <scheme> <token>` header, scheme accepted case-
    insensitively, token compared byte-exactly through
    `hmac.compare_digest`, fail-closed on missing /
    empty / malformed / invalid. Reasoning: minimum
    real security perimeter, stdlib-only, Track D
    `${ENV:NAME}` pattern reuse; JWT / OAuth / OIDC /
    SAML / Basic / HMAC / mTLS rejected.
  - **Q4 = `ProductConfig.auth` optional section +
    `${ENV:NAME}` env-substitution + complementary
    `--auth-token-env <VARNAME>` CLI flag** (CLI wins,
    replace not merge). Reasoning: pattern proven
    twice (runtime Phase 5/Step 3, enterprise Phase
    6/Step 8); single source of truth via
    `--config-path`; vault-as-baseline rejected per
    plan §5.2.
- **Step 3 handoff list.** 10 normative items для
  Step 3 contract: transport family normative + auth
  contract + config schema + `mcp_common` integration
  + `__main__.py` integration + pyproject posture +
  backward compat + Step 4 allowed surfaces + Step 4
  forbidden surfaces + verification protocol.
- **Что НЕ изменено на Step 2.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `README.md`. Production-
  код не правится. Registries `15/25/16` без drift'а.
  Никаких 1cv8.exe runs.
- **Selfcheck после Step 2.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `3c74564`.
- **Step 2 follow-up commit `0628f4c`.** Narrow
  one-file fix removed 4 literal credential-leak-guard
  pattern strings из l.277-281 audit doc'а после того
  как файл стал tracked и начал self-matching против
  `verify-release.ps1` Check 7 (`git grep` сканирует
  только tracked files; на Step 2 verify-time файл
  был untracked под `-AllowDirtyTree`, поэтому Check
  7 PASS). Paraphrased в "three PEM private-key header
  variants — generic, RSA, OpenSSH — plus the well-
  known AWS secret-access-key token". 1 file +10/-5;
  semantic meaning preserved; `scripts/release/verify-
  release.ps1` deliberately not touched (touching
  scripts/* было бы scope creep для Track H docs
  follow-up). Path A chosen and executed before Step 3
  commit, preserving one-logical-event-per-commit
  discipline. Selfcheck зелёный; verify-release GREEN
  на 8 checks; никаких 1cv8.exe runs.

### Parallel Track H / Step 3 — network transport and auth contract (завершён)

- **Цель шага.** Зафиксировать exact prescriptive
  normative contract для Step 4 narrow implementation
  slice — exact transport family + framing + endpoint
  + MCP method coverage + JSON-RPC ↔ HTTP boundary +
  concurrency + auth + config schema + CLI surface +
  integration boundary + backward compat + TLS posture
  + pyproject posture + Step 4 implementation surface
  + verification protocol + honest non-goals + Step 4
  handoff. Никакого code change. Никакого 1cv8.exe.
- **Что реально сделано.** Один новый prescriptive
  normative document
  `docs/architecture/track-h-network-transport-and-auth-contract.md`
  (1650 lines, 293 RFC 2119 keyword usages: 199 MUST,
  74 MUST NOT, 17 MAY, 2 SHOULD, 1 SHALL). 18
  sections; resolved every Step 2 §C ambiguity
  (C.1-C.41) into concrete normative rules.
  Pre-write review с outline + ambiguity list +
  proposed normative decisions согласован с user;
  единственная mandatory amendment — C.21 (case-
  insensitive scheme name + exact constant-time token
  compare).
- **Что НЕ изменено на Step 3.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `README.md`,
  `PROJECT-STATUS.md`. Production-код не правится.
  Registries `15/25/16` без drift'а. Никаких 1cv8.exe
  runs.
- **Selfcheck после Step 3.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `2e76061`.

### Parallel Track H / Step 4 — narrow HTTP transport and bearer auth boundary (завершён)

- **Цель шага.** Единственный шаг Track H с production
  code change. Реализовать ровно тот узкий
  implementation slice, который зафиксирован в Step 3
  contract: один HTTP/1.1 `/mcp` endpoint + один static
  bearer auth model, additive поверх existing Track G
  stdio baseline. Никакого scope creep, никаких новых
  MCP tools, никакого 1cv8.exe.
- **Implementation path = PATH A.** §15.1 optional
  PATH B refactor (extract `_jsonrpc_dispatch.py`
  shared dispatch core) не понадобился — direct
  import existing `_stdio_transport` private internals
  из нового helper'а дал full dispatch reuse без
  модификации старого модуля. `_stdio_transport.py`
  byte-identical per §11.3.
- **§11.4 narrow interpretation документирован в
  commit message.** Unified `run_main_http(...)` с
  single argparser owns dispatch (а не split между
  `run_main` / `run_main_http` в каждом __main__.py),
  потому что §16.1.1 mandates unconditional `--help`
  lists `http` as additional valid `--transport`
  value, что not satisfiable если stdio path uses
  Track G's stdio-only argparser; alternative —
  modify `_stdio_transport.ALLOWED_TRANSPORTS` —
  §11.3 disfavours by default.
- **Ship'нуто 5 файлов (+877/-35).**
  - `packages/mcp-common/src/mcp_common/_network_transport.py`
    (новый, 549 LOC, underscore-prefixed private,
    **NOT** в `mcp_common/__init__.py` `__all__`,
    pure stdlib `http.server.ThreadingHTTPServer` +
    `hmac.compare_digest` + `email.message.Message`
    + `re` + stdlib HTTP/auth helpers); содержит
    `_MCPHandler` (BaseHTTPRequestHandler subclass с
    POST /mcp / GET 405+`Allow:POST` / non-/mcp 404 /
    Content-Type validation 415+-32600 / 1 MiB body
    cap 413+-32600 / multiple Authorization 400+-32600
    / case-insensitive Bearer scheme / constant-time
    token compare / failure-equivalence 401+
    `WWW-Authenticate: Bearer realm="mcp"`+JSON-RPC
    `-32001` для missing/empty/malformed/invalid
    token / notifications → 204 / complete redaction
    discipline), `_serve_http` (ThreadingHTTPServer
    one-thread-per-request с daemon_threads), unified
    `run_main_http(...)` (single argparser supporting
    `--transport {stdio,http}` + `--bind` +
    `--auth-token-env`; stdio path delegates to
    `_stdio_transport._serve_stdio` byte-identically;
    http path runs new HTTP loop).
  - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
    (modified) — switched import `_stdio_transport.run_main`
    → `_network_transport.run_main_http`; `SERVER_VERSION`
    bumped 0.3.0→0.4.0; module docstring describes
    both transports; `main() -> int` signature
    preserved.
  - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
    (modified) — same shape; `run_write_flow`
    discipline preservation noted in docstring.
  - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
    (modified) — same shape; read-only-by-construction
    contract preserved.
  - `apps/platform/src/onec_platform/models.py`
    (modified) — added `ProductAuthSettings` dataclass
    с `tokens: list[str] = field(default_factory=list)`
    + `auth: ProductAuthSettings` field на
    `ProductConfig` с `default_factory` (Phase 5/Step 3
    runtime + Phase 6/Step 8 enterprise additive-
    optional-section pattern reuse).
  - `apps/platform/src/onec_platform/loader.py`
    (modified) — added `re` import + `_AUTH_ENV_TOKEN_RE`
    constant byte-identical к Track D pattern; added
    `_parse_auth(auth_raw) -> ProductAuthSettings`
    с unknown-keys reject, list-of-strings validation,
    env-substitution regex enforce per entry, literal
    cleartext fail-closed at config-load time. Wired
    into `load_product_config`.
- **Verification.** 51/51 PASS через одноразовый
  `.tmp_track_h_smoke.py` smoke harness (deleted
  pre-commit) на всех 3 servers:
  - per-server `--help` exits 0 + lists
    `--transport {stdio,http}` + `--bind` +
    `--auth-token-env`;
  - HTTP startup negative tests (missing `--bind`,
    missing token source, unresolved env-var) → exit
    2 + single stderr line + no traceback;
  - HTTP positive smoke (tools/list valid Bearer →
    200 с правильным tool count 15/25/16);
  - **byte-identical 401 fail-closed** для
    no-Authorization vs Bearer wrong-token (status
    code, headers, JSON-RPC envelope с `-32001`
    byte-equal);
  - case-insensitive scheme через 4 variants
    {`Bearer`, `bearer`, `BEARER`, `BeArEr`} × 3
    servers = 12 successful ping calls;
  - GET 405+`Allow: POST`, POST /other 404, malformed
    JSON 400+`-32700`, wrong Content-Type 415+`-32600`,
    unknown method 200+`-32601` (id preserved),
    multiple Authorization headers 400+`-32600`,
    notification 204+empty body, `tools/call ping`
    200+`isError:false`;
  - cross-transport parity (sorted stdio names ==
    sorted http names) для всех 3 servers;
  - verify-release.ps1 -AllowDirtyTree GREEN на 8
    checks; selfcheck `read=15 / write=25 /
    intelligence=16; status=ok`; `imports_ok=true`.
- **Что НЕ изменено на Step 4.** `pyproject.toml`
  (version 0.4.0 preserved; no new
  [project.dependencies]; [project.scripts]
  unchanged); `mcp_common/__init__.py` `__all__`
  byte-identical (10 names); `_stdio_transport.py`
  byte-identical (orphaned-but-preserved `run_main`;
  PATH B refactor not taken); все 3 `server.py` /
  `tools.py` / per-server `models.py` / `runtime/*`
  byte-identical; `apps/platform/{bootstrap,doctor,
  dashboard,enterprise,installer,process_control,
  realstand,recovery,runtime,runtime_logs,state,
  templates,workflow}.py` byte-identical; `scripts/*`
  byte-identical; `examples/*`; всех Track H + A-G
  architecture docs (frozen anchors); README/
  PROJECT-STATUS/CHANGELOG/SECURITY/release-handoff/
  apps-platform-README/scripts-dev (Step 5/6
  territories). Никаких 1cv8.exe runs. Никаких real
  credentials в commit/diff (smoke harness ephemeral
  token in deleted file). Registries `15/25/16` без
  drift'а.
- **Selfcheck после Step 4.** Зелёный: registries
  `read=15 / write=25 / intelligence=16; status=ok`;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks. Known limitation: `installer.py:_config_to_dict`
  не emit'ит новый `auth` section — install fast path
  round-trip silently drops auth.tokens (operator
  получает clean fail-closed startup или uses
  `--auth-token-env <VARNAME>` to bypass). `installer.py`
  forbidden in Step 4 per §11.5; documented в commit
  message; Step 5 docs alignment item. Commit
  `5814041`.

### Parallel Track H / Step 5 — operator docs and security alignment (завершён)

- **Цель шага.** Точечно выровнять operator-facing и
  security-facing документацию под фактический
  post-Step-4 transport + auth surface, без раздувания
  в closure narrative Step 6. Docs-only; никакого
  production code change; никакого pyproject.toml;
  никаких registry changes; никакого 1cv8.exe.
- **Что реально сделано (6 files +410/-173 lines).**
  - `README.md` — Quickstart paragraph rewritten под
    combined stdio + HTTP+bearer baseline + exhaustive
    out-of-scope list; «Что Quickstart не обещает»
    rewritten с trusted-network-deployment-not-hostile-
    internet framing; «Active parallel track» секция
    rewritten — Steps 1-4 enumerated с commit hashes
    `563b27b/3c74564+0628f4c/2e76061/5814041`, 51/51
    verification artefact summary, известный installer
    auth-round-trip gap, canonical Step 6 next, full
    track-H docs index. Track H НЕ объявлен closed на
    Step 5; трек НЕ перенесён в closed list.
  - `SECURITY.md` — bullet «Local stdio MCP transport
    only» replaced со structured per-transport block
    (stdio threat model + http threat model); pinned
    exhaustive still-NOT list (in-process TLS / mTLS /
    JWT/OAuth/OIDC/SAML/SCIM / RBAC/ABAC/multi-tenant /
    token rotation/refresh/sessions / rate limiting /
    WebSocket/SSE/TCP/pipe / supervisor/systemd/
    Windows-Service/hot-reload / web UI); installer
    auth-round-trip gap added.
  - `docs/release-handoff.md` — 4 locations updated:
    «What is in this handoff» two-transport bullet;
    «What is NOT in this handoff» rewritten с тем же
    exhaustive still-NOT list + installer gap; «Local
    check / launch sequence» parenthetical updated;
    «Known limitations» rewritten.
  - `apps/platform/README.md` — 4 locations updated:
    Phase 5/Step 3 callout acknowledges Track H Step 4
    source of `--transport http` extension; «Чего
    сейчас намеренно ещё нет» renamed «Hostile-network
    transport / enterprise auth / supervisor» с full
    still-NOT enumeration; 2 lower-section parallel
    lists similarly updated.
  - `scripts/dev/launch.ps1` — header comment block +
    Show-Usage help text — both transports described;
    in-process TLS not provided framing.
  - `scripts/dev/README.md` — launch.ps1 parenthetical
    rewritten с per-transport description.
- **Что НЕ изменено на Step 5.** Production code
  (`apps/*/src`, `packages/*/src` — Step 5 docs-only
  by contract); `pyproject.toml` (Q7 = Step 6
  territory); registries / new MCP tools (`read=15 /
  write=25 / intelligence=16` invariant); `PROJECT-STATUS.md`
  (header + per-step closure narrative + final
  closure summary block — Step 6 territory per Track
  A-G symmetry); `CHANGELOG.md` (новая `## 0.5.0 —
  Track H` section — Q7 / Step 6 closure deliverable).
  Track H planning / audit / contract docs (frozen
  Step 1/2/3 anchors).
- **Verification.** Working tree contained exactly
  the 6 expected files. `verify-release.ps1
  -AllowDirtyTree` GREEN на 8 checks. Selfcheck
  registries `read=15 / write=25 / intelligence=16;
  status=ok`; `imports_ok=true`. Никаких 1cv8.exe runs.
  Никаких premature Track H closure phrasings (grep
  verified zero hits). Никаких false claims о TLS /
  mTLS / OAuth / production-ready / enterprise-ready
  being implemented (single grep hit на «hostile-
  internet» — denial sentence «не hostile-internet
  zero-trust posture»).
- **Selfcheck после Step 5.** Зелёный: registries
  `read=15 / write=25 / intelligence=16; status=ok`.
  Commit `407a2f2`.

### Parallel Track H / Step 6 — final integration pass and Track H closure (завершён)

- **Цель шага.** Закрыть весь Track H как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates + `pyproject.toml` version bump
  (Q7 = ДА), потом final closure commit. Никакого
  нового feature work, никаких новых MCP tools,
  никакого remote push'а, никакого 1cv8.exe run.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 5 + Step 2
    follow-up + closure (все commit'ы на месте:
    `563b27b → 3c74564 → 0628f4c → 2e76061 →
    5814041 → 407a2f2 → этот closure`);
  - все Step 1–5 deliverables на диске: 4
    architecture docs (plan + step-map + audit +
    contract); 1 new private helper
    `_network_transport.py`; 3 modified `__main__.py`
    (Track H Step 4); `ProductAuthSettings` dataclass
    + `auth` field в `models.py`; `_AUTH_ENV_TOKEN_RE`
    + `_parse_auth` в `loader.py`; existing Track G
    artefacts byte-identical (3 stdio `__main__.py` /
    `_stdio_transport.py` / `[project.scripts]`);
  - Step 5 unified support statement consistent
    across все 6 modified docs (`--transport http` +
    bearer / Authorization / auth.tokens /
    `--auth-token-env` mentioned uniformly);
  - production code untouched since Step 4 (zero
    diffs `407a2f2..HEAD` pre-closure);
  - registries `read=15 / write=25 / intelligence=16`
    без drift'а;
  - `verify-release.ps1` GREEN на clean tree pre-
    closure (8 checks PASS);
  - no real credentials в diff'ах ни одного из
    шести Track H commit'ов плюс Step 2 follow-up;
  - никаких 1cv8.exe runs ни на одном шаге Track H.
- **Q7 resolved (closure decision) = ДА.** Version
  bump `0.4.0` → `0.5.0`. Reasoning: Track H / Step 4
  ship'нул real production code change с **observable
  runtime capability delta** — `python -m <server>
  --transport http --bind ... --auth-token-env ...`
  теперь реально стартует HTTP/1.1 listener с bearer
  authentication, что до Track H было невозможно
  (existing `_stdio_transport._build_arg_parser` имел
  `ALLOWED_TRANSPORTS=("stdio",)` rejecting `http`
  at argparse level). Backward-compatible new
  functionality (existing `--transport stdio` byte-
  identical через delegation в
  `_stdio_transport._serve_stdio`;
  `mcp_common/__init__.py` `__all__` byte-identical;
  `_stdio_transport.py` byte-identical;
  `[project.scripts]` byte-identical; registries
  `15/25/16` invariant; audit `details` shape
  preserved; new `ProductConfig.auth` optional field
  с `default_factory` — pre-Track-H configs load
  unchanged). Classic MINOR bump per SemVer; precedent
  — Track D `0.1.0 → 0.2.0`, Track F `0.2.0 → 0.3.0`,
  Track G `0.3.0 → 0.4.0`. Track E (no functional
  delta) → no bump; Track H (real code change) →
  bump.
- **Что реально изменено на Step 6 (closure-docs only).**
  - `pyproject.toml` — version `0.4.0` → `0.5.0`
    (Q7 = ДА).
  - `README.md` — Quickstart paragraph переписан под
    «Активного трека сейчас нет»; «Closed parallel
    tracks» list дополнен Track H bullet'ом
    (семь → восемь закрытых треков); «Active parallel
    track» секция сжата под «нет активного трека» с
    pointer'ом на Track H detail; добавлена «Track H
    detail (закрыт)» секция полным блоком симметрично
    Track A/B/C/D/E/F/G detail (per-step bullets с
    commit hashes, что Track H реально закрыл, что
    Track H **не делает** «hostile-network-ready
    enterprise deployment», known installer auth-
    round-trip gap, registry invariant).
  - `PROJECT-STATUS.md` — header (Текущий шаг +
    Статус) обновлён под Track H closed + Q7 = ДА
    явное упоминание + 7 commit hashes + factual
    Step 4 surface + PATH A reasoning; общий
    narrative-блок переписан под closure;
    добавлены пять новых per-step секций (Steps
    2/3/4/5/6); устаревший «Следующий шаг — Step 2»
    в Step 1 секции помечен как historical-snapshot.
  - `CHANGELOG.md` — добавлен новый раздел `## 0.5.0
    — Parallel Track H — Network-Grade MCP Transport
    and Authentication Boundary` с per-step outcomes,
    actual launch surface block, registry invariant
    carried through, honest constraints update,
    Active work = None.
- **Что НЕ изменено на Step 6 (закрытый scope).**
  `apps/`, `packages/`, `scripts/`, `examples/`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`; `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `scripts/dev/*` (Step 5 уже выровнял; the post-
  closure unified support statement remains
  qualitatively accurate); Track H planning / audit
  / contract docs (frozen Step 1/2/3 anchors); Track
  A/B/C/D/E/F/G docs; runbooks; registries.
  `1cv8.exe` не запускался ни на одном шаге Track H.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks; никаких реальных credentials в Step 6
  diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track H).**
  Активного шага нет. Восемь post-phase parallel
  track'ов (A, B, C, D, E, F, G, H) закрыты
  последовательно; Phase 7 как линейная фаза не
  запланирована. Открытие следующего параллельного
  трека — отдельное operator decision. Логичные
  кандидаты (без автоматического открытия):
  installer.py auth round-trip fix track (analogous
  Phase 6/Step 9 service-level + enterprise round-
  trip fix), TLS-in-process / reverse-proxy
  integration track, supervisor / service-registration
  track, real MCP client integration test track,
  WebSocket / SSE transport track (post-Track-H
  network family expansion), enterprise identity
  stack track (SSO / OIDC / RBAC / multi-tenant) —
  значительно больше Track H scope; multi-version
  1С matrix expansion (post-Track-E follow-up).

  Один из этих кандидатов был выбран первым: см.
  секцию Track I / Step 1 ниже.

### Parallel Track I / Step 1 — planning installer auth round-trip integrity (завершён)

- **Цель шага.** Зафиксировать документационный вход в
  **Parallel Track I — Installer Auth Round-Trip
  Integrity**: назначение трека (узкий follow-up к
  Track H — закрывает один honest gap из Track H closure
  narrative: `installer.py:_config_to_dict` не emit'ит
  новый `auth` section, install fast path round-trip
  silently drops `auth.tokens`), целевой результат, что
  закрывает / не закрывает Track I, чем отличается от
  Tracks A–H, guardrails, acceptance criteria, открытые
  вопросы Q1–Q7. Кода не писать. Никаких изменений
  registry. Никаких новых MCP tool'ов. Никаких запусков
  1cv8.exe.
- **Что реально сделано (документ-only Step 1).**
  Ship'нуты два planning-документа в `docs/architecture/`:
  - `track-i-installer-auth-round-trip-integrity-plan.md`
    — plan-уровень: 11 sections (зачем нужен Track I
    после Track H + concrete behaviour pre-Track-I; стартовая
    точка post-Track-H factual baseline + per-installer-
    surface inventory + Track H auth surfaces preserved
    byte-identical anchor + existing precedent for
    additive-installer-fix pattern (Phase 6/Step 6
    service-level + Phase 6/Step 8 enterprise emit-only-
    when-divergent); цель Track I; что входит in scope —
    documentation surface + Step 4 implementation surface
    + Step 5 docs alignment + Step 6 closure deliverables;
    что НЕ входит — auth design changes / secret storage /
    packaging ecosystem / transport-network changes /
    service-supervisor / новые MCP tools / 1cv8 work /
    rollback / AST / multi-version / standalone
    apps/platform / web UI / enterprise identity / remote
    push; 13 guardrails; 10 acceptance criteria; honest
    constraints после closure; relation to prior tracks
    A-H; open questions Q1-Q7 с default recommendations).
  - `track-i-installer-auth-round-trip-integrity-step-map.md`
    — step map: 6 шагов (Step 1 planning / Step 2
    installer round-trip baseline audit / Step 3 auth
    round-trip preservation contract / Step 4 narrow
    installer auth round-trip implementation / Step 5
    operator/security docs alignment / Step 6 final
    integration pass and closure) с per-step Цель / Что
    меняем / Что НЕ меняем / Результат format'ом, mirror
    Track H step-map structure.
- **Open questions Q1–Q7 (default recommendations).**
  - **Q1 = `installer.py` only** (default planning anchor;
    финал — Step 2 audit / Step 3 contract). Reasoning:
    Phase 6/Step 9 precedent (service-level + enterprise
    extensions без modification of `_install_runner.py`);
    gap pattern matches — missing emit branch для `auth`
    block, ~10–15 LOC symmetric к existing `enterprise_block`.
    Alternative `installer.py + _install_runner.py`
    rejected as default (explicit reporting hook expands
    scope без shipping value).
  - **Q2 = preserve `auth` section presence + `tokens`
    list shape + order + raw `${ENV:NAME}` form +
    empty/default no-implicit-injection** (default;
    финал — Step 3 contract). Reasoning: symmetric к
    existing `enterprise_block` emit-only-when-divergent
    pattern; raw env-substitution form preserved as
    configuration data (никаких env-resolution at install
    time — это Track H `_resolve_env_token` boundary
    territory at server startup).
  - **Q3 = forbidden = no env-resolution at install time
    / no cleartext token writing / no Track H auth model
    changes / no secret storage / no broad packaging
    rewrite / no `[project.scripts]` changes / no helper
    file introduction unless absolutely justified**
    (default; финал — Step 3 contract).
  - **Q4 = backward compat preserved** (pre-Track-H
    configs round-trip byte-identical; stdio-only configs
    work; configs without `auth` section still load).
    Carry-over из Track H §12 backward-compatibility
    invariants.
  - **Q5 = expected docs scope on Step 5** = `SECURITY.md`
    «Honest constraints» known installer auth-round-trip
    gap removed/updated; `docs/release-handoff.md` «What
    is NOT» / «Known limitations» installer gap bullets;
    `apps/platform/README.md` «Чего сейчас намеренно ещё
    нет» installer gap mention; `README.md` Quickstart
    + active parallel track section if remaining drift;
    `scripts/dev/launch.ps1` + `scripts/dev/README.md`
    only if direct user-facing drift; `scripts/release/
    README.md` possibly. Default: check во время Step 5
    inventory; не пред-открывать.
  - **Q6 = likely YES** (`0.5.0 → 0.6.0`) если Step 4
    ship'ит real production code change с observable
    configuration-round-trip behaviour delta; alternative
    PATCH (`0.5.0 → 0.5.1`) — only if Step 4 diff
    действительно tiny (~5 LOC) и framing честнее как
    defect-fix чем feature; финал — Step 6 closure
    decision. Precedent — Track D / F / G / H all MINOR
    bumps.
  - **Q7 = closure не означает** «full installer
    ecosystem solved» / «deployment solved» / «packaging
    solved» / «enterprise-ready». Только installer auth
    round-trip integrity fixed.
- **Что НЕ изменено на Step 1 (закрытый scope).**
  `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `examples/`, `LICENSE`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*`,
  `apps/platform/README.md`, server `server.py` files,
  three `__main__.py` files, `_stdio_transport.py`
  helper, `_network_transport.py` helper, `installer.py`,
  `models.py`, `loader.py`, `bootstrap.py`. Никаких real
  credentials в commit message — Track I round-trips
  raw `${ENV:NAME}` strings, никогда не resolves them.
  Никакого 1cv8.exe.
- **Selfcheck после Step 1.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Track I / Step 1 не правил
  production-кода — drift'а нет.
- **Следующий шаг (historical snapshot, на момент
  закрытия Step 1).** Parallel Track I / Step 2 —
  installer round-trip baseline audit (docs-only). Этот
  раздел сохранён как исторический снимок намерений на
  момент Step 1; фактический Step 2 закрылся отдельным
  заходом — см. секцию Step 2 ниже.

### Parallel Track I / Step 2 — installer round-trip baseline audit (завершён)

- **Цель шага.** Закрыть Q1 (implementation surface),
  Q2 (preservation target), Q3 (forbidden behaviours) на
  основе read-only inspection текущего installer
  round-trip path. Никакого code change. Никакого
  1cv8.exe.
- **Что реально сделано.** Один новый descriptive
  audit-документ
  `docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md`
  (889 lines, 12 sections): purpose / method / current
  installer round-trip path (operator entry
  `install.ps1` → `_install_runner.py` → boundary
  helper `run_install_fast_path` orchestrator → `_config_to_dict`
  projection function); per-section `_config_to_dict`
  inventory (table of 9 logical sections — 8 already
  round-trip-safe under unconditional или emit-only-when-
  divergent patterns + 1 missing); auth-specific gap
  walk-through (concrete pre-Track-I behaviour); existing
  precedent (Phase 6/Step 6 service-level fields +
  Phase 6/Step 8 enterprise block); 4-class breakdown
  (CLASS 1 already round-trip-safe = 8 sections; CLASS 2
  partially preserved = empty; CLASS 3 currently dropped
  = только `auth`; CLASS 4 explicitly out-of-scope = 11
  items); Q1 / Q2 / Q3 resolutions с file/line evidence
  anchors; Step 3 handoff note (10 normative items); honest
  summary.
- **Resolved decisions.**
  - **Q1 = `installer.py` only** (verified by Phase 6
    /Step 6 service-level + Phase 6/Step 8 enterprise
    single-file precedents).
  - **Q2 = 5 preservation rules** (auth section
    presence; tokens list shape JSON array of strings;
    token entry order; raw `${ENV:NAME}` form
    preservation as configuration data; empty/default
    no-implicit-injection).
  - **Q3 = 11 forbidden sub-rules** (no env-resolution
    at install time; no cleartext token writing; no
    Track H auth model changes; no secret storage; no
    broad packaging rewrite; no `[project.scripts]`
    changes; no `_install_runner.py`/`install.ps1`/
    `bootstrap_paths.ps1` touches; no `models.py`/
    `loader.py` touches; no `_network_transport.py`/
    `_stdio_transport.py` touches; no three `__main__.py`
    touches; no installer-time auth side-effects).
- **Что НЕ изменено на Step 2.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `README.md`. Production-код
  не правится. Registries `15/25/16` без drift'а.
  Никаких 1cv8.exe runs.
- **Selfcheck после Step 2.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `e7d9973`.

### Parallel Track I / Step 3 — auth round-trip preservation contract (завершён)

- **Цель шага.** Зафиксировать exact prescriptive
  normative contract для Step 4 narrow implementation
  slice. Никакого code change. Никакого 1cv8.exe.
- **Что реально сделано.** Один новый prescriptive
  normative document
  `docs/architecture/track-i-installer-auth-round-trip-contract.md`
  (843 lines, 118 RFC 2119 keyword usages: 78 MUST, 32
  MUST NOT, 4 SHOULD, 3 MAY, 1 SHALL); 11 sections
  pinning purpose / Step 1 plan + Step 2 audit
  relationship / current model recap / inherited fixed
  decisions (Q1/Q2/Q3 + plan §5 carry-over) / auth round-
  trip preservation contract (round-trip integrity
  definition `C2.auth.tokens == C.auth.tokens`; emit-
  branch presence after `enterprise_block` at l.314;
  emit-branch shape `auth_block: dict[str, Any] = {}`
  accumulator + conditional append + conditional attach;
  tokens list shape JSON array of strings; empty/default
  no-implicit-injection; token order positional 0-indexed;
  `list(config.auth.tokens)` copy discipline; raw
  `${ENV:NAME}` byte-identical preservation; output JSON
  shape ordinary serialisable top-level placement) / 9
  sub-sections of forbidden behaviour / exact Step 4
  implementation surface (allowed file singular
  installer.py + exhaustive forbidden file list +
  default-zero allowed import additions + forbidden
  imports os/subprocess/urllib/hashlib/hmac/third-party)
  / 6 backward-compatibility invariant classes /
  verification contract for Step 4 (6 positive checks +
  6 negative checks + 4 insufficient-verification
  exclusions + no-real-MCP-client-gate carry-over) / 15
  honest non-goals each followed by "No ..." denial
  clauses / Step 4 handoff note (8 numbered preconditions
  + 11-item prohibition list).
- **Что НЕ изменено на Step 3.** `apps/`, `packages/`,
  `scripts/`, `pyproject.toml`, `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `README.md`,
  `PROJECT-STATUS.md`. Production-код не правится.
  Registries `15/25/16` без drift'а. Никаких 1cv8.exe
  runs.
- **Selfcheck после Step 3.** Зелёный без правок:
  registries `read=15 / write=25 / intelligence=16`,
  `selfcheck_status=ok`. Commit `525c611`.

### Parallel Track I / Step 4 — narrow installer auth round-trip implementation (завершён)

- **Цель шага.** Единственный шаг Track I с production
  code change. Реализовать ровно тот узкий
  implementation slice, который зафиксирован в Step 3
  contract: additive emit branch для `auth` section в
  `installer.py:_config_to_dict` symmetric к existing
  Phase 6 / Step 8 enterprise-block emit-only-when-
  divergent pattern. Никакого scope creep, никаких новых
  MCP tools, никакого 1cv8.exe.
- **Ship'нуто 1 файл (+15 / -0 LOC).** Additive emit
  branch в `apps/platform/src/onec_platform/installer.py:_config_to_dict`
  между existing `enterprise_block` attach (l.314) и
  `return out`:

  ```python
  auth_block: dict[str, Any] = {}
  if config.auth.tokens:
      auth_block["tokens"] = list(config.auth.tokens)
  if auth_block:
      out["auth"] = auth_block
  ```

  Comment block описывает Track I provenance + raw
  `${ENV:NAME}` preservation + resolution boundary в
  `_network_transport.py`. **No new imports** (`Any`
  already imported at l.33 per Step 3 §7.3); **no edits
  в existing 8 emit branches** (per §7.1 byte-identical);
  **no helper extraction** / refactor / cleanup churn.
- **Verification.** 14/14 PASS через одноразовый
  `.tmp_track_i_smoke.py` smoke harness (deleted
  pre-commit):
  - **§9.1 positive (8 PASS):** multi-token round-trip
    preserved с order; single-token round-trip; empty/
    default no-injection across 3 cases (default
    factory, explicit empty list, pre-Track-H input
    dict); pre-Track-H reload defaults to empty; token
    order positionally preserved через 3 distinct
    entries; raw `${ENV:NAME}` byte-for-byte preserved
    WITHOUT populating os.environ.
  - **§9.2 negative (3 PASS):** no env resolution at
    install time (TRACK_I_ENV_RESOLUTION_PROBE set в
    os.environ → resolved value «should-never-appear-
    in-projection» never appears в projected JSON;
    projected token остаётся
    `${ENV:TRACK_I_ENV_RESOLUTION_PROBE}`); literal
    cleartext rejected fail-closed by
    `loader._parse_auth` upstream; empty/default not
    spuriously emitted (cross-check).
  - **End-to-end (3 PASS):** real file IO install fast-
    path executed-mode round-trip с
    `run_install_fast_path_from_json_file(confirm_write=True)`
    → result.ok=True, mode=executed → materialised JSON
    contains auth.tokens byte-identical к source →
    `bootstrap_product_from_json_file` re-load preserves
    auth.tokens element-wise.
  - `verify-release.ps1 -AllowDirtyTree` GREEN на 8
    checks; selfcheck registries `read=15 / write=25 /
    intelligence=16; status=ok`; `imports_ok=true`.
- **Что НЕ изменено на Step 4.** `apps/platform/src/onec_platform/`
  все остальные файлы (models.py, loader.py,
  bootstrap.py, doctor.py, dashboard.py, enterprise.py,
  process_control.py, realstand.py, recovery.py,
  runtime.py, runtime_logs.py, state.py, templates.py,
  workflow.py, __init__.py) byte-identical; все 3 MCP
  server packages byte-identical; все packages/* byte-
  identical (mcp_common/__init__.py __all__ +
  _stdio_transport.py + _network_transport.py); scripts/release/install.ps1
  + _install_runner.py + scripts/dev/* byte-identical;
  pyproject.toml (version 0.5.0 preserved; Q6 = Step 6);
  README/PROJECT-STATUS/CHANGELOG/SECURITY/release-handoff/
  apps-platform-README (Step 5/6 territories per Step 3
  §6.9); Track I plan/step-map/audit/contract (frozen
  Step 1/2/3 anchors); Track A-H architecture docs
  (frozen). Никаких 1cv8.exe runs. Никаких real
  credentials в commit/diff (smoke harness ephemeral
  test placeholders + canary string в deleted file).
  Registries `15/25/16` без drift'а.
- **Selfcheck после Step 4.** Зелёный: registries
  `read=15 / write=25 / intelligence=16; status=ok`;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks. Commit `d047a6d`.

### Parallel Track I / Step 5 — operator docs and installer auth alignment (завершён)

- **Цель шага.** Точечно выровнять operator-facing /
  security-facing документацию под фактический
  post-Step-4 fix state. Docs-only; никакого production
  code change; никакого pyproject.toml; никаких registry
  changes; никакого 1cv8.exe.
- **Что реально сделано (3 files +185/-84 lines).**
  - `SECURITY.md` — single bullet под "Honest
    constraints" replaced: «Known limitation in install
    fast path round-trip» → «Install fast path auth
    round-trip preserved (Track I / Step 4)» с post-
    Step-4 truthful framing (auth.tokens preserved
    byte-identical; raw `${ENV:NAME}` strings remain
    raw configuration data; empty/default no implicit
    injection; resolution at server startup not install
    time) + pointer на `docs/release-handoff.md` для
    full carry-forward list of broader installer /
    packaging / deployment ecosystem limitations.
  - `docs/release-handoff.md` — 2 locations updated:
    «What is NOT in this handoff» bullet «Known install
    fast path limitation» → «Install fast path auth
    round-trip preserved (Track I / Step 4)» с тем же
    truthful framing; «Known limitations» pointer
    updated.
  - `README.md` — 2 locations updated: Quickstart
    paragraph rewritten under Steps 1-4 closed + Step 5
    active framing; «Active parallel track» section
    rewritten enumerating 4 closed steps с commit
    hashes (`cb79597 / e7d9973 / 525c611 / d047a6d`),
    actual Step 4 fix shape (5-line emit branch в
    `_config_to_dict`), 14/14 verification artefact
    summary, canonical Step 6 next.
- **Drift inventory classified 8 candidates:** 3 CLASS-1
  (touched), 3 CLASS-2 (apps/platform/README.md +
  scripts/dev/launch.ps1 + scripts/dev/README.md —
  qualitatively still accurate, no gap mention; verified
  by grep), 2 CLASS-3 (PROJECT-STATUS.md + CHANGELOG.md
  — closure narrative territory, deferred to Step 6).
- **Что НЕ изменено на Step 5.** Production code
  (apps/*/src, packages/*/src — Step 5 docs-only by
  contract); pyproject.toml (Q6 = Step 6 territory);
  registries / new MCP tools (`read=15 / write=25 /
  intelligence=16` invariant); apps/platform/README.md;
  scripts/dev/launch.ps1; scripts/dev/README.md;
  PROJECT-STATUS.md; CHANGELOG.md; Track I plan /
  step-map / audit / contract docs (frozen Step 1/2/3
  anchors); Track A-H docs.
- **Verification.** Working tree contained exactly the
  3 expected files. `verify-release.ps1 -AllowDirtyTree`
  GREEN на 8 checks. Selfcheck registries `read=15 /
  write=25 / intelligence=16; status=ok`;
  `imports_ok=true`. Никаких 1cv8.exe runs. Никаких
  premature Track I closure phrasings (grep verified
  zero hits). Никаких false maturity claims (grep
  verified zero hits на «installer solved» /
  «deployment solved» / «packaging solved» /
  «enterprise-ready» / «hostile-network ready»).
- **Selfcheck после Step 5.** Зелёный: registries
  `read=15 / write=25 / intelligence=16; status=ok`.
  Commit `2e9e0b8`.

### Parallel Track I / Step 6 — final integration pass and Track I closure (завершён)

- **Цель шага.** Закрыть весь Track I как documented
  status. Read-only final integration check уже
  закрытых Steps 1–5, потом минимальные closure-docs/
  status updates + `pyproject.toml` version bump
  (Q6 = PATCH per below), потом final closure commit.
  Никакого нового feature work, никаких новых MCP tools,
  никакого remote push'а, никакого 1cv8.exe run.
- **Read-only final integration check (pre-closure).**
  - working tree clean перед началом — gate PASS;
  - git history линейная Step 1 → 2 → 3 → 4 → 5 → 6
    (все commit'ы на месте: `cb79597 → e7d9973 →
    525c611 → d047a6d → 2e9e0b8 → этот closure`);
  - все Step 1–5 deliverables на диске: 4 architecture
    docs (plan + step-map + audit + contract); Step 4
    production code (`auth_block` emit branch в
    `installer.py` l.317-330); Step 5 docs alignment
    (3 modified files);
  - production code untouched since Step 4 (zero diffs
    `2e9e0b8..HEAD` pre-closure);
  - registries `read=15 / write=25 / intelligence=16`
    без drift'а;
  - `verify-release.ps1` GREEN на clean tree pre-closure
    (8 checks PASS);
  - no real credentials в diff'ах ни одного из пяти
    Track I commit'ов;
  - никаких 1cv8.exe runs ни на одном шаге Track I.
- **Q6 resolved (closure decision) = PATCH (NOT MINOR).**
  Version bump `0.5.0` → `0.5.1`. См. raison d'être
  выше в "Статус" блоке: Track I — defect-class round-
  trip integrity fix, не feature delta (no new public
  API surface, no new runtime capability for end users,
  +15/-0 LOC defect-class repair); D/F/G/H precedent
  added recognizable new external capability and
  warranted MINOR while Track I does not; per Keep-a-
  Changelog conventions and SemVer §6 "Bug fixes" →
  PATCH; Track I plan §10 Q6 explicitly framed PATCH
  `0.5.1` as the alternative path "only if Step 4 diff
  truly tiny and framing honest as defect-fix" — both
  conditions met.
- **Что реально изменено на Step 6 (closure-docs only).**
  - `pyproject.toml` — version `0.5.0` → `0.5.1`
    (Q6 = PATCH).
  - `README.md` — Quickstart paragraph переписан под
    «Активного трека сейчас нет — Track I закрыт
    девятым по счёту post-phase треком»; «Closed
    parallel tracks» list дополнен Track I bullet'ом
    (восемь → девять закрытых треков); «Active parallel
    track» секция сжата под «нет активного трека» с
    pointer'ом на Track I detail; добавлена «Track I
    detail (закрыт)» секция полным блоком симметрично
    Track A/B/C/D/E/F/G/H detail (per-step bullets с
    commit hashes; что Track I реально закрыл; что
    Track I **не делает** «installer ecosystem solved»;
    Q6 = PATCH reasoning; registry invariant; honest
    constraints).
  - `PROJECT-STATUS.md` — header (`Текущий шаг` +
    `Статус`) обновлён под Track I closed + Q6 = PATCH
    explicit reasoning + 6 commit hashes; общий
    narrative-блок переписан под closure; добавлены
    пять новых per-step секций (Steps 2/3/4/5/6); Step
    1 «Следующий шаг — Step 2» tail помечен как
    historical-snapshot.
  - `CHANGELOG.md` — добавлен новый раздел `## 0.5.1 —
    Parallel Track I — Installer Auth Round-Trip
    Integrity` с per-step outcomes, actual round-trip
    preservation surface, registry invariant carried
    through, honest constraints update, Active work =
    None.
- **Что НЕ изменено на Step 6 (закрытый scope).**
  `apps/`, `packages/`, `scripts/`, `examples/`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`; `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/README.md`,
  `scripts/dev/*` (Step 5 уже выровнял; the post-Step-5
  unified support statement remains qualitatively
  accurate); Track I planning / audit / contract docs
  (frozen Step 1/2/3 anchors); Track A-H docs;
  runbooks; registries. `1cv8.exe` не запускался ни на
  одном шаге Track I.
- **Selfcheck после Step 6.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; verify-release.ps1 GREEN на 8
  checks; никаких реальных credentials в Step 6
  diff'е.
- **Следующий шаг (на момент закрытия Step 6 / Track I).**
  Активного шага нет. Девять post-phase parallel
  track'ов (A, B, C, D, E, F, G, H, I) закрыты
  последовательно; Phase 7 как линейная фаза не
  запланирована. Открытие следующего параллельного
  трека — отдельное operator decision. Логичные
  кандидаты (без автоматического открытия): TLS-in-
  process / reverse-proxy integration track; supervisor
  / service-registration track; real MCP client
  integration test track; WebSocket / SSE transport
  track (post-Track-H network family expansion);
  enterprise identity stack (значительно больше Track
  H scope); multi-version 1С matrix expansion (post-
  Track-E follow-up); packaging ecosystem track
  (`.msi`/`.deb`/wheel publication beyond
  `[project.scripts]`). **Историческая правка
  (Track J / Step 6):** первый из этих кандидатов
  открыт и **полностью закрыт** как Track J — TLS and
  Reverse-Proxy Deployment Boundary, intentionally
  docs-only formalization track. Шесть meaningful
  commit'ов: `e203e43` Step 1 / `344129c` Step 2 /
  `4e04771` Step 3 / `5c793c1` Step 4 / `19e8923`
  Step 5 / closure commit Step 6. **Q7 = NO-BUMP** —
  закрыт под existing `0.5.1` без further version
  bump (zero production code change; zero defect-class
  fix; zero new external capability). См. per-step
  секции «Parallel Track J / Step 1–6 (завершён)»
  ниже для подробностей.

### Parallel Track J / Step 1 — planning TLS and reverse-proxy deployment boundary (завершён)

- **Цель.** Открыть десятый post-phase parallel track —
  Track J — как **planning-only** документационный шаг,
  который формализует "trusted-network behind operator-
  owned reverse proxy" general-policy statement из Track
  H Step 3 contract §13 в operator-facing single-source-
  of-truth deployment-boundary recipe (точная bind-host
  guidance для трёх deployment scenarios — loopback /
  private subnet / public-facing-through-reverse-proxy;
  reverse-proxy integration expectations с explicit
  policy что `_MCPHandler` не consume / trust
  `X-Forwarded-*` headers; TLS termination point —
  operator's reverse proxy only, in-process TLS
  forbidden carry-over от Track H §13.1; exposure rules
  matrix; explicit `/healthz` endpoint resolution).
  Step 1 — два planning-документа без code changes;
  Step 4 path (docs-only PATH A vs narrow ≤15 LOC code
  PATH B vs hybrid PATH C) **остаётся открытым** до
  Step 2 audit + Step 3 contract.
- **Что shipped в Step 1.**
  - `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-plan.md` —
    11-секционный planning-документ: §0 purpose, §1
    factual baseline (Track H §13 carry-over,
    `_network_transport.py` runtime behaviour,
    `_MCPHandler` auth path), §2 in-scope (deployment-
    boundary docs SSOT + bind-host guidance + reverse-
    proxy expectations + exposure-rule matrix +
    `/healthz` resolution), §3 out-of-scope (in-process
    TLS forbidden, mTLS forbidden, no enterprise
    identity stack, no zero-trust posture, no hostile-
    internet ready, no WAF/IDS/rate-limit, no
    observability stack, no service supervisor, no
    packaging ecosystem, no web UI, no standalone
    `apps/platform` entrypoint, no new MCP tools, no
    1cv8 work, no real-MCP-client integration test as
    closure gate, no remote push), §4 guardrails (13
    hard constraints), §5 acceptance criteria for
    Track-J closure (11 items), §6 honest constraints
    (что **не** выйдет из Track J), §7 relation to
    prior tracks (G/H/I surfaces preserved byte-
    identical at PATH A; narrow additive at PATH B/C),
    §8–§14 Q1–Q7 with default recommendations (Q1 =
    hybrid reverse-proxy-first + in-process TLS
    deferred per Track H §13.1 carry-over; Q2 = open
    until Step 2 audit; Q3 = trusted internal network
    behind operator-owned reverse proxy; Q4 = bind-
    host treatment, reverse-proxy header policy
    explicitly "not consulted", three exposure
    scenarios, `/healthz` endpoint open question; Q5 =
    documentation surfaces inventory; Q6 = Step 4 path
    deferred; Q7 = SemVer Q open until Step 6 — PATCH
    default if Step 4 PATH A docs-only).
  - `docs/architecture/track-j-tls-and-reverse-proxy-deployment-boundary-step-map.md` —
    6-step map в формате «Цель / Что меняем / Что НЕ
    меняем / Результат» для каждого шага; track-
    invariants block с 13 hard constraints включая
    «Track H Step 3 §13.1 in-process-TLS-forbidden
    invariant inherited and NOT reversed by Track J»;
    Step 4 explicitly preserves PATH A/B/C openness;
    Step 6 — закрытие трека с честным итогом.
- **Что Step 1 НЕ делал.**
  - Не правил production-код (никаких изменений в
    `apps/*/src/`, `packages/*/src/`, `scripts/dev/*`,
    `scripts/release/*`).
  - Не открывал и не правил Step 2 audit / Step 3
    contract — это уже следующие шаги.
  - Не менял registries (`read=15 / write=25 /
    intelligence=16` invariant carried through; никаких
    новых MCP tool'ов в Step 1).
  - Не bumped'ил `pyproject.toml` `version` (остаётся
    `0.5.1` от Track I closure до Track J Step 6 — Q7
    bump deferred, default PATCH 0.5.1→0.5.2 если Step
    4 идёт PATH A docs-only).
  - Не запускал `1cv8.exe` (Track J работает на
    network/deployment boundary layer, не на 1cv8
    binary surface).
  - Не вводил никаких реальных credentials в repo /
    docs / commit message.
  - Не делал remote push / GitHub release —
    operator action, не часть трека.
  - Не открывал Track J Step 2 в этом же commit'е.
- **Документ scope.** Ровно четыре файла: 2 новых
  planning-документа в `docs/architecture/` + README.md
  (Quickstart paragraph + Active parallel track section)
  + PROJECT-STATUS.md (header rewrite + this section).
  Никаких других файлов Step 1 не трогает.
- **Verify-release.ps1 -AllowDirtyTree.** GREEN на 8
  checks; никаких реальных credentials в Step 1 diff'е;
  registries без drift'а.
- **Selfcheck после Step 1.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; никаких реальных credentials в
  Step 1 diff'е.
- **Следующий шаг.** **Parallel Track J / Step 2 —
  deployment-boundary baseline audit (docs-only).**
  Новый short audit-документ с inventory existing TLS
  / reverse-proxy / bind-host text in Track H contract
  / SECURITY / release-handoff / apps/platform/README /
  scripts/dev/* / scripts/release/* + inventory
  `_network_transport.py` runtime behaviour (bind-host
  validation, forwarded-header treatment, non-`/mcp`
  404 response, `WWW-Authenticate` 401) + 4-class
  breakdown (already formalized at general-policy
  level / partially documented scattered / clearly
  missing / out-of-scope) + resolve Q1 (target =
  hybrid reverse-proxy-first + in-process TLS deferred
  per Track H §13.1 carry-over), Q2 (Step 4 PATH
  choice based on evidence — preliminary recommendation
  PATH A docs-only unless audit reveals concrete bind-
  host or `/healthz` gap that needs ≤15 LOC fix),
  Q3 (trusted internal network behind operator-owned
  reverse proxy as canonical threat model), Q4
  (deployment surfaces enumerated с three scenarios).
  Production-код Step 2 не правит. Никаких real
  credentials. **GitHub remote push — operator
  action, не часть трека.**

### Parallel Track J / Step 2 — deployment-boundary baseline audit (завершён)

- **Цель.** Превратить general-policy statement из
  Track H §13 в descriptive baseline audit:
  inventory всех существующих deployment-boundary
  surfaces в repo (runtime: `_network_transport.py`,
  `_stdio_transport.py`, three `__main__.py`,
  `_parse_bind`, `_MCPHandler`; operator-facing docs:
  Track H Step 3 contract §10 / §13, SECURITY.md
  "Honest constraints" bullet, `docs/release-handoff.md`
  "What is NOT", `apps/platform/README.md` Track-H
  citations, manuals); 4-class breakdown
  (already-reusable / adjacent-but-insufficient /
  clearly-missing / explicitly-out-of-scope);
  directional Q1–Q6 resolutions для Step 3 contract
  consumption.
- **Что shipped.** Один новый descriptive
  audit-документ:
  `docs/architecture/track-j-deployment-boundary-baseline-audit.md`
  (980 lines, 10 sections). Section 9 — 14-item
  Step 3 handoff list. Никаких других файлов Step 2
  не правил.
- **Ключевые находки.** Code уже enforce'ит
  deployment-boundary invariants Track J хотел
  formalize (bind validation, fail-closed startup,
  `/mcp` POST-only, bearer auth с failure-equivalence
  + redaction discipline, deterministic 404 на
  non-`/mcp`, нулевой consumption `X-Forwarded-*` /
  `Forwarded` / `X-Real-IP` / `client_ip` /
  `peer_ip` для access-control); dominant gap =
  documentation, не behaviour; recommended Step 4
  PATH A docs-only.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries `read=15 / write=25 / intelligence=16`
  без drift'а; никаких реальных credentials в
  audit; никаких 1cv8.exe runs; `pyproject.toml`
  `version=0.5.1` preserved.
- **Commit.** `344129c` (`Track J / Step 2 —
  deployment-boundary baseline audit`).

### Parallel Track J / Step 3 — deployment-boundary contract (завершён)

- **Цель.** Promote Step 2 directional findings в
  normative contract: pin final Step 4 PATH; codify
  per-scenario MUST/SHOULD/MAY matrix; codify
  Forwarded-header MUST-NOT-consume policy; codify
  `/healthz` decision; codify `0.0.0.0` runtime-
  warning decision; lock Step 4 file surface; lock
  Step 4 verification harness; preserve Track G /
  Track H / Track I invariants byte-identical.
- **Что shipped.** Один новый normative contract-
  документ:
  `docs/architecture/track-j-deployment-boundary-contract.md`
  (1150 lines, 15 sections, RFC 2119 MUST / MUST NOT
  / SHOULD / SHOULD NOT / MAY language). Никаких
  других файлов Step 3 не правил.
- **Ключевые decisions.**
  - **Step 4 PATH A (docs-only) pinned** в §9.1;
    PATH B (narrow ≤15 LOC code) и PATH C (hybrid)
    explicitly rejected в §9.3 / §9.4 (PATH B's
    `0.0.0.0` warning fully documentable в PATH A
    prose; `/healthz` = net-new external capability
    that would force MINOR SemVer question, deferred
    by §8).
  - **Forwarded-header policy** (§6.1): listener
    **MUST NOT** consume `X-Forwarded-For` /
    `X-Forwarded-Proto` / `X-Forwarded-Host` /
    `X-Forwarded-Port` / `X-Forwarded-Server` /
    `X-Real-IP` / `Forwarded` / `True-Client-IP` /
    `CF-Connecting-IP` для **any** access-control,
    trust, allow-listing, identity, audit, or
    routing decision. Step 4 inherits as
    invariant.
  - **Per-scenario MUST/SHOULD/MAY matrix** (§7.1):
    три scenarios (loopback / trusted private
    subnet / public-facing-through-reverse-proxy)
    с per-row bind-host / reverse-proxy /
    TLS-termination / token-wire-confidentiality
    columns. Public-routable bind без fronting TLS
    proxy = **NOT SUPPORTED** (§7.2).
  - **`/healthz` defer** (§8): Step 4 **MUST NOT**
    add `/healthz` / `/readyz` / `/livez`. Strict-
    2xx-only probers решают через probe-config
    override или reverse-proxy synthesised 2xx.
  - **TLS posture carry-forward** (§5): in-process
    TLS forbidden (Track H §13.1); mTLS forbidden
    (§13.3); TLS termination at operator's reverse
    proxy only (§13.2).
- **Step 4 surface lock.** Allowed: exactly один
  новый файл, default `docs/operators/deployment-
  boundary.md`. Forbidden: production code,
  `pyproject.toml`, `scripts/*`, `SECURITY.md`,
  `docs/release-handoff.md`, `apps/platform/
  README.md`, manuals, `README.md`,
  `PROJECT-STATUS.md`, `CHANGELOG.md`,
  `examples/*`, Track J Step 1/2/3 docs, new MCP
  tools, registry changes.
- **Step 4 verification harness lock** (§12):
  18-check protocol across scope (1-file new, no
  modifications), selfcheck (registries
  `15/25/16`, status=ok), release-verify
  (`verify-release.ps1 -AllowDirtyTree` GREEN на 8
  checks), honesty (no 1cv8.exe, no real
  credentials, no premature closure language, no
  enterprise-ready / hostile-network framing), and
  doc-consistency (matrix byte-identical to §7.1;
  Forwarded-header / `/healthz` / threat-model
  consistent with §6 / §8 / §4).
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в contract; никаких 1cv8.exe runs;
  `pyproject.toml` `version=0.5.1` preserved.
- **Commit.** `4e04771` (`Track J / Step 3 —
  deployment-boundary contract`).

### Parallel Track J / Step 4 — operator deployment-boundary recipe (завершён)

- **Цель.** Operationalize Step 3 contract как
  single operator-facing deployment recipe (PATH A
  docs-only). Recipe **MUST** содержать: per-
  scenario matrix (byte-identical к contract §7.1);
  per-scenario walkthroughs; Forwarded-header
  policy; `/healthz` non-shipping explanation;
  ≤3 concrete reverse-proxy snippets с abstract
  placeholders only; 8 operator decision-point
  Q&A; honest non-goals.
- **Что shipped.** Один новый operator-facing
  recipe-документ: [`docs/operators/deployment-boundary.md`](docs/operators/deployment-boundary.md)
  (691 lines, 10 sections; well под contract §10.5
  ≤1500-line soft cap). Создан новый каталог
  `docs/operators/`. Никаких других файлов Step 4
  не правил.
- **Содержание.** §1 Purpose; §2 Threat-model
  summary (in-scope диаграмма, trusted parties,
  untrusted parties, NOT-supported list, honest
  summary phrase); §3 Per-scenario deployment
  matrix; §4 Per-scenario walkthroughs (A
  local-only / B trusted private subnet с B1
  proxy-fronted и B2 proxy-omitted variants /
  C public-facing-through-reverse-proxy); §5
  Forwarded-header policy (full 9-header list);
  §6 `/healthz` non-shipping (rationale +
  workarounds для strict-2xx-only probers);
  §7 Concrete reverse-proxy snippets (nginx +
  Caddy; abstract placeholders only; explicit
  deferral note для третьего snippet'а под
  contract §10.3 ≤3 cap); §8 Operator decision-
  point Q&A (8 questions byte-faithful к contract
  §7.4); §9 Cross-references (links к Track J
  Step 1/2/3 docs, Track H Step 3 contract,
  SECURITY.md, release-handoff.md, apps/platform/
  README.md, manuals; не modify ни один из них —
  Step 5 territory); §10 Honest non-goals.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в recipe (placeholders:
  `<PUBLIC_HOSTNAME>`, `<CERT_PATH>`, `<KEY_PATH>`,
  `<LISTENER_PORT>`, `<VARNAME>`); никаких
  1cv8.exe runs; `pyproject.toml` `version=0.5.1`
  preserved.
- **Commit.** `5c793c1` (`Track J / Step 4 —
  operator deployment-boundary recipe`).

### Parallel Track J / Step 5 — operator docs and deployment-boundary alignment (завершён)

- **Цель.** Узкое CLASS-1 docs-alignment:
  обновить только те operator/security/release-
  facing docs, у которых после Step 4 появился
  прямой factual drift. Track J остаётся active
  на Step 5 (closure narrative — Step 6
  territory).
- **Drift inventory.**
  - **CLASS 1 (direct factual drift, fixed):**
    `README.md` Quickstart paragraph (говорил
    "Step 1, planning-only" — stale); `README.md`
    Active parallel track section (говорил
    "Track J сейчас на Step 1" — stale);
    `docs/release-handoff.md` "What is in this
    handoff" + "Where to read deeper" lists (не
    referenced new recipe at all).
  - **CLASS 2 (narrow cross-link applied):**
    `SECURITY.md` "Threat model for HTTP" bullet —
    one-sentence cross-link в конец existing
    bullet pointing к `docs/operators/deployment-
    boundary.md`.
  - **CLASS 3 (closure territory, NOT touched):**
    `PROJECT-STATUS.md`, `CHANGELOG.md`, README
    Closed parallel tracks list / Track-J-detail
    section, `pyproject.toml`. Step 6 territory.
  - **Out of scope, NOT touched:**
    `apps/platform/README.md` (no factual drift,
    only optional cross-link); manuals (no
    actively-misleading text); `scripts/*`,
    production code, `examples/*`, Track J Step
    1–4 deliverables.
- **Что shipped.** Три файла modified:
  `README.md` (Quickstart paragraph + Active
  parallel track section refreshed; Track J
  framed as **active** — not moved to closed
  list); `SECURITY.md` (single-sentence
  cross-link added к existing transports
  bullet); `docs/release-handoff.md` (one new
  bullet в "What is in this handoff" list +
  one new bullet в "Where to read deeper" list).
  154 insertions, 76 deletions, 0 new files.
- **Verify-release.** GREEN на 8 checks;
  selfcheck registries без drift'а; никаких
  реальных credentials в commit'е; никаких
  1cv8.exe runs; `pyproject.toml` `version=0.5.1`
  preserved; Track J still active framed
  везде (`PROJECT-STATUS.md` / `CHANGELOG.md`
  /closed-tracks list untouched).
- **Commit.** `19e8923` (`Track J / Step 5 —
  operator docs and deployment-boundary
  alignment`).

### Parallel Track J / Step 6 — final integration pass and track closure (завершён)

- **Цель.** Final integration pass над Track J
  Steps 1–5 + честное Q7-решение + closure
  narrative в README / PROJECT-STATUS / CHANGELOG.
  Закрыть весь Track J. Active tracks remaining =
  none после Step 6.
- **Q7 = NO-BUMP.** Track J закрыт под existing
  `0.5.1` без further version bump. Защита
  решения:
  - **Zero production code change** across all six
    Track J steps. `apps/*/src/`, `packages/*/src/`,
    `_network_transport.py`, `_stdio_transport.py`,
    `installer.py` byte-identical к Track I closure
    state (`d408dd2`).
  - **Zero defect-class fix.** Step 2 audit
    explicitly показал, что runtime уже
    enforce'ил deployment-boundary invariants
    Track J formalize'ил. Не было broken behaviour,
    silent failure, или operator workaround.
  - **Zero new external capability.** No new
    `/healthz` endpoint, no new `--bind` warning,
    no new CLI flag, no new MCP tool, no new auth
    scheme, no new transport. Step 3 contract
    pinned PATH A specifically чтобы избежать
    net-new capability.
  - **Zero new public API surface.** No new public
    types, functions, imports, `__all__` exports,
    `[project.scripts]` entries, или config schema
    changes.
  - **SemVer §6 не оправдывает PATCH.** PATCH =
    "backward-compatible bug fixes"; Track J не
    fix'ил никакого bug.
  - **Track I PATCH precedent не переносится.**
    Track I имел `+15 LOC` production code И
    previously-broken round-trip (silent data loss
    в `installer.py:_config_to_dict`); Track J не
    имеет ни того, ни другого.
  - **Track A / B / C / E precedent.** Те docs-heavy
    треки тоже закрылись без separate version
    bumps — отсутствуют как `## VERSION — Track X`
    headings в `CHANGELOG.md`.
  - **Step 1 plan §14 / Step 3 contract §3.7 /
    §11.5** explicitly authorize NO-BUMP if Step 6
    = closure-doc alignment с no version-relevant
    change.
- **Closure scope (narrowest honest).** Touched:
  `README.md` (Quickstart paragraph flipped from
  active → no-active-track wording; Active
  parallel track section compressed back to
  no-active-track; new "Track J detail (закрыт)"
  section added above "Track I detail (закрыт)";
  Closed parallel tracks list extended from девять
  to десять с Track J entry); `PROJECT-STATUS.md`
  (header rewritten от "Track J / Step 1 in
  progress" к "no active step + Track J fully
  closed"; historical-edit annotation updated;
  per-step closure sections для Step 2 / Step 3 /
  Step 4 / Step 5 / Step 6 inserted между Step 1
  section и `## Phase 6 закрыта`); `CHANGELOG.md`
  (Track J closure narrative inserted под existing
  `## 0.5.1` heading с explicit NO-BUMP framing).
  **NOT touched:** `pyproject.toml` (NO-BUMP);
  `SECURITY.md`; `docs/release-handoff.md`;
  `apps/platform/README.md`;
  `docs/operators/deployment-boundary.md`; Track J
  Step 1–4 architecture docs; production code;
  `scripts/*`; `examples/*`; manuals.
- **Verify-release.** GREEN на 8 checks pre-commit
  (`-AllowDirtyTree`) и post-commit (clean tree);
  selfcheck registries `read=15 / write=25 /
  intelligence=16` без drift'а; никаких реальных
  credentials в closure commit'е; никаких 1cv8.exe
  runs; никакого remote push.
- **Track J closure итог.** Десять post-phase
  parallel track'ов (A, B, C, D, E, F, G, H, I, J)
  полностью закрыты. Phase 7 как линейная фаза не
  запланирована. Открытие следующего параллельного
  трека — отдельное operator decision. **Историческая
  правка (Track K / Step 6):** первый из recommended-
  next-track candidates ("real MCP client integration
  test track") выбран как следующий открываемый трек —
  открыт как Track K на Step 1 и **полностью закрыт**
  на Step 6 как Real MCP Client Integration Test
  (PATH B narrow harness, **Q7 = NO-BUMP**, закрыт
  под existing `0.5.1` без further bump). См. секции
  «Parallel Track K / Step 1–6 (завершён)» ниже для
  подробностей. После Track K closure'а — одиннадцать
  post-phase parallel track'ов закрыты последовательно
  (A/B/C/D/E/F/G/H/I/J/K); активного трека нет.

### Parallel Track K / Step 1 — planning real MCP client integration test (завершён)

- **Цель.** Открыть одиннадцатый post-phase parallel
  track — Track K — как **planning-only** документационный
  шаг, который закрывает один из последних честных
  gaps проекта: нет real MCP-client-facing end-to-end
  proof. Каждое предыдущее MCP-transport-track closure
  (Tracks G / H / I / J) explicitly flagged эту gap
  как honest constraint, не hidden defect. Step 1 —
  два planning-документа без code changes; Step 4
  design-question (docs-only PATH A vs narrow ≤300
  LOC harness PATH B vs hybrid PATH C) **остаётся
  открытым** до Step 2 audit + Step 3 contract.
- **Что shipped в Step 1.**
  - `docs/architecture/track-k-real-mcp-client-integration-test-plan.md` —
    14-секционный planning-документ: §1 purpose / why
    track exists, §2 current post-Track-J baseline,
    §3 honest gap statement, §4 why not redundant
    with existing smoke (`selfcheck.py` /
    `verify-release.ps1` / internal unit-shape
    paths), §5 goal of the track, §6 in-scope (6
    bullet points), §7 out-of-scope (17 bullet
    points), §8 guardrails (13 hard invariants),
    §9 acceptance criteria for eventual closure
    (11 items), §10 honest constraints after closure
    (carry-forward from Tracks G / H / I / J), §11
    relationship to Tracks G / H / I / J table,
    §12 Q1–Q7 open questions с directional
    recommendations only (no fake certainty), §13
    step trajectory preview table, §14 honest
    summary.
  - `docs/architecture/track-k-real-mcp-client-integration-test-step-map.md` —
    6-step map в формате «Goal / What changes /
    What does NOT change / Result» для каждого шага;
    track-invariants block с 15 hard constraints
    включая "Track J §13 / §6 / §7 / §8 carry-
    forward unchanged"; hard out-of-scope list с
    16 categorical denials; Step 4 explicitly
    preserves PATH A / B / C openness; Step 6 — Q7
    decision rule с NO-BUMP / PATCH framing
    (MINOR / MAJOR forbidden by track scope).
- **Q1–Q7 directional defaults (plan §12).** Q1 =
  Class B (minimum-viable real-client-compatible
  harness shipped как single new file); Q2 = stdio +
  HTTP both (best coverage; cheap once one harness
  works); Q3 = minimum-viable harness (Class B);
  Q4 = one client / one transport sufficient для
  closure gate; multiple = recommended-only; Q5 =
  likely needs code, but a new stand-alone harness
  file, not modification к existing production
  code; Q6 = `pyproject.toml` untouched везде кроме
  Step 6 Q7-bump; `scripts/*` untouched except Step
  4 may add one new file under `scripts/dev/` or
  `examples/mcp-client-smoke/`; Q7 = NO-BUMP
  preferred; PATCH `0.5.1 → 0.5.2` только если
  Step 4 ship'нет defect-class fix observable by
  end-users; MINOR / MAJOR forbidden by track scope.
- **Что Step 1 НЕ делал.**
  - Не правил production-код (никаких изменений в
    `apps/*/src/`, `packages/*/src/`,
    `_stdio_transport.py`, `_network_transport.py`,
    `installer.py`).
  - Не открывал и не правил Step 2 audit / Step 3
    contract / Step 4 implementation — это уже
    следующие шаги.
  - Не менял registries (`read=15 / write=25 /
    intelligence=16` invariant carried through;
    никаких новых MCP tool'ов в Step 1).
  - Не bumped'ил `pyproject.toml` `version`
    (остаётся `0.5.1` от Track I closure bump через
    Track J NO-BUMP closure; Track K Q7 bump deferred
    до Step 6 — default NO-BUMP).
  - Не правил `SECURITY.md`, `docs/release-handoff.md`,
    `apps/platform/README.md`, `CHANGELOG.md`, manuals,
    Closed parallel tracks list (Track K не moved
    туда — Track K active).
  - Не запускал `1cv8.exe` (Track K работает на MCP
    client / transport layer, не на 1cv8 binary
    surface).
  - Не вводил никаких реальных credentials в repo /
    docs / commit message.
  - Не делал remote push / GitHub release —
    operator action, не часть трека.
  - Не открывал Track K Step 2 в этом же commit'е.
- **Документ scope.** Ровно четыре файла: 2 новых
  planning-документа в `docs/architecture/` + README.md
  (Quickstart paragraph + Active parallel track section
  reopened) + PROJECT-STATUS.md (header rewrite + this
  section). Никаких других файлов Step 1 не трогает.
- **Verify-release.ps1 -AllowDirtyTree.** GREEN на 8
  checks; никаких реальных credentials в Step 1 diff'е;
  registries без drift'а.
- **Selfcheck после Step 1.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без drift'а;
  selfcheck_status=ok; никаких реальных credentials
  в Step 1 diff'е.
- **Следующий шаг (historical snapshot на момент
  Step 1 closure).** Тогда — Track K / Step 2
  (baseline audit of current client-integration gap,
  docs-only). На момент Step 6 closure'а — этот шаг
  уже закрыт (см. секцию «Parallel Track K / Step 2
  (завершён)» ниже).

### Parallel Track K / Step 2 — baseline audit of current client-integration gap (завершён)

- **Цель.** Превратить general gap statement из Step 1
  plan §3 в descriptive baseline audit: inventory всех
  существующих client-integration approximations в
  repo (`scripts/dev/selfcheck.py`, `_handle_request`
  internal switch в `_stdio_transport.py` /
  `_network_transport.py`, JSON-RPC envelope shaping,
  in-process unit-shape assertions); inventory того,
  что real-MCP-client end-to-end proof would require
  (subprocess MCP server, JSON-RPC 2.0 over wire,
  envelope-shape assertions external к runtime);
  4-class breakdown (already-covered / adjacent-but-
  insufficient / clearly-missing / out-of-scope);
  directional Q1–Q6 resolutions для Step 3 contract
  consumption.
- **Что shipped.** Один новый descriptive
  audit-документ:
  `docs/architecture/track-k-real-mcp-client-integration-test-baseline-audit.md`
  (1076 lines, 10 sections). Section 9 — 14-item
  Step 3 handoff list. Никаких других файлов Step 2
  не правил.
- **Ключевые находки.**
  - Repo evidence unambiguous about the gap: zero
    `tests/` directory, zero `test_*.py` files, zero
    `*smoke*` Python files, no MCP-client harness
    fragment в `examples/` / `scripts/dev/` /
    `scripts/release/`.
  - `selfcheck.py` и `verify-release.ps1` bypass
    transport entirely — invoke `list_tools` /
    `ping` callables in-process как Python functions,
    never speak JSON-RPC 2.0 over any wire, never
    start `_serve_stdio` или `_serve_http`. Adjacent-
    but-insufficient для Track K's gap.
  - Track A / Track E reference-stand runbooks
    orthogonal (1С-binary integration, не MCP-client
    integration).
  - Runtime **internally consistent** с plausible MCP
    interpretation, но externally unverified.
- **Q1–Q6 directional resolutions.** Q1 = Class B
  (minimum-viable harness in repo) as closure gate;
  Class A (third-party real client) — recommended-
  only. Q2 = stdio + HTTP (default Option B). Q3 =
  narrowing toward **PATH B (narrow harness)** или
  PATH C (PATH B + operator doc); does not foreclose
  PATH A. Final lock = Step 3 contract. Q4 =
  mandatory closure scenario = `initialize` +
  `tools/list` + one read-only `tools/call` on one
  server on one transport; strongly recommended для
  HTTP = 401 failing-mode probe. Q5 = insufficient-
  on-its-own list: selfcheck alone, verify-release
  alone, in-process `_handle_request` invocation,
  contract reading, operator-side demonstration
  without commit artefact, Track A/E runbooks
  (orthogonal). Q6 = no modification existing
  production code needed; PATH B = one new stdlib-
  only harness file ≤ ~300 LOC; PATH A = zero new
  code.
- **Что Step 2 НЕ делал.** Не правил production-код;
  не открывал Step 3 contract / Step 4 implementation;
  не менял registries; не bumped'ил `pyproject.toml`
  `version` (`0.5.1` preserved); не запускал
  `1cv8.exe`; не вводил real credentials; не делал
  remote push.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries `read=15 / write=25 / intelligence=16`
  без drift'а; никаких реальных credentials в audit;
  никаких 1cv8.exe runs; `pyproject.toml`
  `version=0.5.1` preserved.
- **Commit.** `62069a5` (`Track K / Step 2 —
  client integration baseline audit`).

### Parallel Track K / Step 3 — client integration contract (завершён)

- **Цель.** Promote Step 2 directional findings в
  normative contract: pin final Step 4 PATH; codify
  closure-gate scenario; codify synthetic-token
  discipline; lock Step 4 file surface; lock Step 4
  verification harness; preserve Track G / Track H /
  Track I / Track J invariants byte-identical.
- **Что shipped.** Один новый normative contract-
  документ:
  `docs/architecture/track-k-real-mcp-client-integration-test-contract.md`
  (1302 lines, 15 sections, RFC 2119 MUST / MUST NOT
  / SHOULD / SHOULD NOT / MAY language). Никаких
  других файлов Step 3 не правил.
- **Ключевые decisions.**
  - **Step 4 PATH B (narrow harness) pinned** в §9.1.
    PATH A (docs-only) explicitly rejected because
    Track K's gap is *evidence-of-runtime-behaviour*
    и prose cannot supply it. PATH C (hybrid)
    rejected as scope creep without corresponding
    closure-strength benefit.
  - **Closure-gate scenario locked** (§7). Для
    каждого `(server, transport)` pair (closure-gate
    minimum = `(mcp-read-server, stdio)` +
    `(mcp-read-server, http)`): `initialize` request
    → assert `protocolVersion == "2024-11-05"` +
    well-shaped `serverInfo` / `capabilities`;
    `tools/list` → assert non-empty array + per-entry
    shape; `tools/call` (one read-only tool) →
    assert `_serialize_tool_result`-shaped envelope.
    HTTP pass also includes failure-equivalence probe:
    missing `Authorization` → 401 +
    `WWW-Authenticate: Bearer realm="mcp"` +
    JSON-RPC `-32001`.
  - **Synthetic-token discipline locked** (§6.4).
    Harness generates own bearer token via
    `secrets.token_urlsafe(N≥32)` at run time;
    exports via `os.environ[<SYNTHETIC_VARNAME>]`;
    passes `--auth-token-env <SYNTHETIC_VARNAME>` к
    server subprocess; **MUST NOT** print token value
    at any verbosity level.
- **Step 4 file surface locked.** Allowed: exactly
  один новый файл at **`scripts/dev/mcp_client_smoke.py`**
  (§10.1, canonical pinned location chosen over
  `examples/mcp-client-smoke/run.py` because
  operator-runnable diagnostic tooling analogous к
  `selfcheck.py`). ≤300 LOC stdlib-only soft cap
  (§10.5); ≤400 LOC stdlib-only hard cap (§10.6);
  no new `[project.dependencies]`; no modification к
  any existing file.
- **Step 4 verification harness locked** (§12).
  22-check protocol across scope (1-file new at
  canonical location, no other modifications, no
  production-code/pyproject/scripts/operator-facing-
  doc edits), selfcheck (registries `15/25/16`,
  status=ok), release-verify (`verify-release.ps1
  -AllowDirtyTree` GREEN на 8 checks), honesty (no
  1cv8.exe, no real credentials, no premature
  closure language, no false implementation claims,
  no fake "client integration solved" framing), и
  harness-runnability (`python scripts\dev\mcp_client_smoke.py
  --server read --transport both` exits 0; final
  summary contains literal `OK`; non-zero on
  assertion failure; no orphan processes; no token
  value printed; raw `OK` line recorded в commit
  message as evidence).
- **Q1–Q7 normative resolutions** (contract §3).
  Q1 = Class B closure gate; Class A recommended-
  only. Q2 = both stdio + HTTP MUST be exercised.
  Q3 = PATH B pinned. Q4 = §7 minimum scenario
  (initialize + tools/list + one read-only
  tools/call; HTTP also 401 probe). Q5 =
  insufficient-list pinned (§8). Q6 = no
  production-code modification permitted. Q7 =
  Step 6 territory; default NO-BUMP; PATCH only if
  defect-class fix; MINOR / MAJOR forbidden.
- **Что Step 3 НЕ делал.** Не правил production-код;
  не открывал Step 4 implementation; не менял
  registries; не bumped'ил `pyproject.toml`
  `version` (`0.5.1` preserved); не запускал
  `1cv8.exe`; не вводил real credentials; не делал
  remote push.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в contract; никаких 1cv8.exe runs;
  `pyproject.toml` `version=0.5.1` preserved.
- **Commit.** `ead4a0e` (`Track K / Step 3 —
  client integration contract`).

### Parallel Track K / Step 4 — narrow MCP client smoke harness (завершён)

- **Цель.** Operationalize Step 3 contract как single
  operator-runnable harness (PATH B narrow harness).
  Harness **MUST** be stdlib-only, single-file, под
  canonical pinned location `scripts/dev/mcp_client_smoke.py`,
  exercise full closure-gate scenario for `(server,
  transport)` matrix with per-method envelope-shape
  assertions, honour synthetic-token discipline,
  clean up subprocess on success and on failure, и
  exit 0 with literal `OK` line on success.
- **Что shipped.** Один новый stdlib-only harness
  файл: `scripts/dev/mcp_client_smoke.py` (341 LOC,
  под contract §10.6 ≤400 hard cap). Zero modified
  files; zero production code changes; zero
  `pyproject` changes; no new dependencies; no
  registry change; no new MCP tools.
- **CLI surface.** `--server {read,write,intelligence}`
  default `read`; `--transport {stdio,http,both}`
  default `both`. Builds own PYTHONPATH (mirrors
  `bootstrap_paths.ps1`'s 11 src paths) — runs even
  without operator pre-bootstrap.
- **Closure-gate scenario exercised.** Для каждого
  `(server, transport)` pair: `initialize` → asserts
  `protocolVersion == "2024-11-05"` + non-empty
  `serverInfo.name` / `version` + `capabilities.tools`
  present; `tools/list` → asserts non-empty `tools`
  array + per-entry `name` / `description` /
  `inputSchema` shape; one read-only `tools/call`
  с empty args → asserts either well-shaped `result`
  envelope (content array) или well-shaped `error`
  envelope (code int + message str). Для HTTP:
  missing-`Authorization` probe → asserts `401` +
  `WWW-Authenticate: Bearer realm="mcp"` + JSON-RPC
  `error.code == -32001`.
- **Synthetic-token discipline.** Token generated
  via `secrets.token_urlsafe(32)` at run time;
  exported via `os.environ["MCP_CLIENT_SMOKE_TOKEN"]`
  для server subprocess only; never printed to
  stdout или stderr. Token value never appears in
  source, output, или commit message.
- **Subprocess lifecycle.** Stdio: stdin/stdout
  piped, stderr → DEVNULL, line-buffered text I/O.
  HTTP: all I/O → DEVNULL, ephemeral port via
  `socket.bind(("127.0.0.1", 0))`, port readiness
  poll с 10s timeout. Cleanup: close stdin →
  `proc.terminate()` → `wait(5s)` → escalate к
  `proc.kill()`. No orphan processes verified after
  three test runs.
- **Run results captured в commit body.**
  - Primary closure-gate: `python scripts/dev/mcp_client_smoke.py
    --server read --transport both` → exit 0, final
    line `OK (server=read transport=both)`. Chosen
    tool: `check_runtime_health` (first в
    `mcp-read-server` tools/list).
  - Spot-check 1: `--server write --transport stdio`
    → `OK (server=write transport=stdio)` (chosen
    tool: `add_catalog_attribute`).
  - Spot-check 2: `--server intelligence --transport
    http` → `OK (server=intelligence transport=http)`.
- **Что Step 4 НЕ делал.** Не правил production-код;
  не правил `pyproject`; не модифицировал existing
  `scripts/*` files; не правил operator-facing docs;
  не менял registries; не добавлял new MCP tools;
  не запускал `1cv8.exe`; не вводил real
  credentials; не делал remote push; не переписывал
  Track K Step 1/2/3 docs.
- **Contract compliance (22 checks per §12).** All
  GREEN: 7 scope checks; 2 selfcheck checks; 1
  release-verify check; 5 honesty checks; 7 harness-
  runnability checks.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в harness; никаких 1cv8.exe runs;
  `pyproject.toml` `version=0.5.1` preserved.
- **Commit.** `979eced` (`Track K / Step 4 —
  narrow MCP client smoke harness`).

### Parallel Track K / Step 5 — operator docs and client-integration alignment (завершён)

- **Цель.** Узкое CLASS-1 docs-alignment: обновить
  только те docs, у которых после Step 4 появился
  прямой factual drift. Track K остаётся active на
  Step 5 (closure narrative — Step 6 territory).
- **Drift inventory.**
  - **CLASS 1 (direct factual drift, fixed):**
    `README.md` Quickstart paragraph (говорил
    "Track K planning-only, Step 1" — stale после
    Steps 2/3/4 закрытых); `README.md` Active
    parallel track section (same staleness +
    outdated "next step = Step 2" pointer);
    `docs/release-handoff.md` "What is in this
    handoff" + "Where to read deeper" lists (не
    mention now-shipped `scripts/dev/mcp_client_smoke.py`);
    `scripts/dev/README.md` "Содержимое" section
    (enumerated 4 dev scripts но directory now
    contains 5).
  - **CLASS 2 (cross-link skipped):**
    `SECURITY.md` (harness не меняет security
    claim); `apps/platform/README.md` (no factual
    drift); manuals (no actively-misleading text).
  - **CLASS 3 (closure territory, NOT touched):**
    `PROJECT-STATUS.md`, `CHANGELOG.md`,
    `pyproject.toml` `version`, README's "Closed
    parallel tracks" list / Track K detail (закрыт)
    section. Step 6 territory.
- **Что shipped.** Три файла modified, ноль new
  files: `README.md` (Quickstart paragraph + Active
  parallel track section refreshed; Track K framed
  as **active** — not moved to closed list);
  `docs/release-handoff.md` (one new bullet в
  "What is in this handoff" + one new bullet в
  "Where to read deeper"); `scripts/dev/README.md`
  ("Содержимое" section updated to include
  `mcp_client_smoke.py` alongside existing dev
  scripts).
- **Что Step 5 НЕ делал.** No Track K closure
  language; Track K still framed as **active**
  (Step 5 active, Step 6 closure впереди); не
  moved к Closed parallel tracks list (остаётся
  десять закрытых: A–J); no Track K detail (закрыт)
  section added; no SemVer decision; no CHANGELOG
  entry; no PROJECT-STATUS edit; no production
  code change; no `pyproject` change; no
  modification к `scripts/dev/mcp_client_smoke.py`
  itself (Step 4 deliverable immutable). Фразы
  "client integration solved" / "production-ready
  client compatibility" / "all clients supported"
  appear в touched docs только как explicit
  DENIALS — honest-non-goals framing.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в commit'е; никаких 1cv8.exe runs;
  `pyproject.toml` `version=0.5.1` preserved;
  Track K still active framed везде
  (`PROJECT-STATUS.md` / `CHANGELOG.md` /
  closed-tracks list untouched).
- **Commit.** `ef9c6c7` (`Track K / Step 5 —
  operator docs and client-integration alignment`).

### Parallel Track K / Step 6 — final integration pass and track closure (завершён)

- **Цель.** Final integration pass над Track K
  Steps 1–5 + честное Q7-решение + closure
  narrative в README / PROJECT-STATUS / CHANGELOG.
  Закрыть весь Track K. Active tracks remaining =
  none после Step 6.
- **Q7 = NO-BUMP.** Track K закрыт под existing
  `0.5.1` без further version bump. Защита
  решения:
  - **Zero production code change** across all six
    Track K steps. `apps/*/src/`, `packages/*/src/`,
    `_network_transport.py`, `_stdio_transport.py`,
    `installer.py` byte-identical к Track J closure
    state (`dd86261`).
  - **Zero defect-class fix.** Step 2 audit
    explicitly показал, что runtime internally
    consistent с plausible MCP interpretation;
    Track K не fix'ил bug, а добавил replayable
    external proof уже-существующего behaviour.
  - **Zero new external capability для ordinary
    product consumers.** Harness живёт под
    `scripts/dev/`, симметрично `selfcheck.py`;
    не в `[project.scripts]`; не importable от
    external consumers; не часть pip-install
    surface (если он когда-нибудь появится).
  - **Zero new public API surface.** No new public
    types, functions, imports, `__all__` exports,
    `[project.scripts]` entries, `ProductConfig`
    schema fields, или CLI flags на existing
    servers.
  - **SemVer §6 не оправдывает PATCH.** PATCH =
    "backward-compatible bug fixes"; Track K не
    fix'ил никакого bug.
  - **Track I PATCH precedent не переносится.**
    Track I имел `+15 LOC` production code И
    previously-broken installer round-trip (silent
    data loss в `installer.py:_config_to_dict`);
    Track K не имеет ни того, ни другого.
  - **Track J NO-BUMP precedent applies directly.**
    Track J тоже закрылся без bump'а под existing
    `0.5.1`, с docs + один operator-facing
    artefact (recipe). Track K следует тому же
    pattern'у (docs + один operator-runnable
    diagnostic artefact).
  - **Track A / B / C / E precedent.** Те docs-
    heavy треки тоже закрылись без separate
    version bumps — отсутствуют как `## VERSION —
    Track X` headings в `CHANGELOG.md`.
  - **Step 1 plan §12 Q7 / Step 3 contract §3.Q7 /
    §11.5** explicitly authorize NO-BUMP if Step 4
    не ship'нет defect-class fix observable by
    end-users. Step 4 ship'нул operator-runnable
    diagnostic harness, не defect fix. Оба условия
    NO-BUMP выполнены.
- **Closure scope (narrowest honest).** Touched:
  `README.md` (Quickstart paragraph flipped от
  active → no-active-track wording; Active
  parallel track section compressed back к no-
  active-track; new "Track K detail (закрыт)"
  section added above "Track J detail (закрыт)";
  Closed parallel tracks list extended from десять
  to одиннадцать с Track K entry);
  `PROJECT-STATUS.md` (header rewritten от
  "Track K / Step 1 in progress" к "no active step
  + Track K fully closed"; historical-edit
  annotation на конце Track J Step 6 section
  updated; per-step closure sections для Step 2 /
  Step 3 / Step 4 / Step 5 / Step 6 inserted);
  `CHANGELOG.md` (Track K closure narrative
  inserted под existing `## 0.5.1` heading с
  explicit NO-BUMP framing). **NOT touched:**
  `pyproject.toml` (NO-BUMP); `SECURITY.md`;
  `docs/release-handoff.md` (Step 5 уже выровнял);
  `apps/platform/README.md`;
  `docs/operators/deployment-boundary.md` (Track J
  artefact); `scripts/dev/mcp_client_smoke.py`
  (Step 4 deliverable immutable);
  `scripts/dev/README.md` (Step 5 уже выровнял);
  Track K Step 1–4 architecture docs (frozen
  anchors); production code; `apps/*/src/`;
  `packages/*/src/`; остальные `scripts/*`;
  `examples/*`; manuals.
- **Verify-release.** GREEN на 8 checks pre-commit
  (`-AllowDirtyTree`) и post-commit (clean tree);
  selfcheck registries `read=15 / write=25 /
  intelligence=16` без drift'а; никаких реальных
  credentials в closure commit'е; никаких 1cv8.exe
  runs; никакого remote push.
- **Track K closure итог.** Одиннадцать post-phase
  parallel track'ов (A, B, C, D, E, F, G, H, I, J,
  K) полностью закрыты. Phase 7 как линейная фаза
  не запланирована. Открытие следующего
  параллельного трека — отдельное operator
  decision. Логичные кандидаты (без автоматического
  открытия): TLS-in-process / mTLS expansion
  (отдельный enterprise-grade identity track),
  service supervision / packaging ecosystem track,
  multi-version 1С matrix expansion (post-Track-E
  follow-up), full rollback / AST work (post-
  Track-F / post-Track-A follow-ups),
  observability stack track, web UI / dashboard
  frontend track. Эти кандидаты — recommendation
  only, не auto-opened. **Историческая правка
  (Track L / Step 6):** "service supervision /
  packaging ecosystem track" из списка recommended-
  next-track candidates был частично выбран как
  следующий открываемый трек — открыт как **Track L
  — Service Supervision and OS Service
  Registration** и **полностью закрыт** на Step 6
  (PATH B docs + one declarative systemd unit
  template; **Q7 = NO-BUMP**, закрыт под existing
  `0.5.1` без further bump; packaging-ecosystem
  часть из recommended-list оставлена за пределами
  scope как отдельный potential track). См. секции
  «Parallel Track L / Step 1–6 (завершён)» ниже для
  подробностей. После Track L closure'а —
  двенадцать post-phase parallel track'ов закрыты
  последовательно (A/B/C/D/E/F/G/H/I/J/K/L);
  активного трека нет.

### Parallel Track L / Step 1 — planning service supervision and OS service registration (завершён)

- **Цель.** Открыть двенадцатый post-phase parallel
  track — Track L — как **planning-only**
  документационный шаг, который закрывает следующий
  честный эксплуатационный gap: у продукта уже есть
  рабочие MCP entrypoints (Track G), HTTP/stdio
  transports (Tracks G/H), bearer auth (Track H),
  installer integrity (Track I), deployment-boundary
  recipe (Track J) и real MCP client smoke proof
  (Track K), но у него всё ещё нет взрослой
  service-supervision story. Step 1 — два planning-
  документа без code changes; Step 4 design-question
  (docs-only PATH A vs docs + template PATH B vs
  docs + template + wrapper script PATH C)
  **остаётся открытым** до Step 2 audit + Step 3
  contract.
- **Что shipped в Step 1.**
  - `docs/architecture/track-l-service-supervision-and-os-service-registration-plan.md` —
    14-секционный planning-документ: §1 purpose /
    why track exists, §2 current post-Track-K
    baseline (existing launch surfaces vs what is
    not in repo today), §3 honest gap statement
    (three independently verifiable observations),
    §4 why gap not already solved (rejection of
    five candidate "we already have this"
    arguments), §5 goal of the track, §6 in-scope,
    §7 out-of-scope (18 explicit denials), §8
    guardrails (13 hard invariants), §9 acceptance
    criteria for eventual closure (11 items), §10
    honest constraints after closure (carry-forward
    from Tracks G/H/I/J/K), §11 relationship to
    Tracks G/H/I/J/K table, §12 Q1–Q7 open
    questions с directional recommendations only
    (no fake certainty), §13 step trajectory
    preview table, §14 honest summary.
  - `docs/architecture/track-l-service-supervision-and-os-service-registration-step-map.md` —
    6-step map в формате «Goal / What changes /
    What does NOT change / Result» для каждого
    шага; track-invariants block с 16 hard
    constraints включая "Track J §13 / §6 / §7 /
    §8 carry-forward unchanged", "Track K
    diagnostic harness byte-identical", "no new
    MCP tools / no registry drift / no 1cv8.exe /
    no remote push"; hard out-of-scope list с 18
    categorical denials; Step 4 explicitly
    preserves PATH A / B / C openness; Step 6 —
    Q7 framing с NO-BUMP default + PATCH/MINOR/
    MAJOR conditions.
- **Q1–Q7 directional defaults (plan §12).** Q1 =
  closure-gate = one documented unit-file template
  + documented operator workflow для register /
  start / stop / restart / status / logs; broader
  code-level supervisor explicitly rejected. Q2 =
  OS-family target = **systemd / Linux first**
  (broadest precedent; cleanest declarative model)
  с cross-OS prose covering Windows / macOS. Q3 =
  Step 4 PATH = default **PATH B** (docs + one
  declarative template); PATH A (docs-only) и
  PATH C (docs + template + wrapper script)
  acceptable per Step 3 contract decision. Q4 =
  template location = `docs/operators/service/` by
  default (co-located с Track J's
  `docs/operators/deployment-boundary.md`); wrapper
  script (если PATH C) под `scripts/release/`. Q5 =
  all five lifecycle verbs (start / stop / restart
  / status / logs) **mandatory for closure**;
  partial coverage explicitly rejected. Q6 =
  **NO production code modification** — existing
  foreground-blocking server entrypoints already
  the correct shape для `Type=simple` systemd unit /
  Windows SCM-managed wrapper / launchd plist;
  `Type=forking` / `daemonize=true` rejected. Q7 =
  **NO-BUMP** default (Track J / Track K precedent
  applies); PATCH considered только если Step 4 =
  PATH C с honest defect-class framing (default:
  not the case); MINOR considered только если Step
  4 ships net-new CLI flag (default: rejected by
  Q6); MAJOR forbidden by track scope.
- **Что Step 1 НЕ делал.**
  - Не правил production-код (никаких изменений в
    `apps/*/src/`, `packages/*/src/`,
    `_stdio_transport.py`, `_network_transport.py`,
    `installer.py`).
  - Не открывал и не правил Step 2 audit / Step 3
    contract / Step 4 implementation — это уже
    следующие шаги.
  - Не менял registries (`read=15 / write=25 /
    intelligence=16` invariant carried through;
    никаких новых MCP tool'ов в Step 1).
  - Не bumped'ил `pyproject.toml` `version`
    (остаётся `0.5.1` через Track J и Track K
    NO-BUMP closures; Track L Q7 bump deferred до
    Step 6 — default NO-BUMP).
  - Не правил `SECURITY.md`, `docs/release-handoff.md`,
    `apps/platform/README.md`, `CHANGELOG.md`,
    `scripts/dev/README.md`, manuals, Closed
    parallel tracks list (Track L не moved туда —
    Track L active).
  - Не правил `docs/operators/deployment-boundary.md`
    (Track J artefact, не в Track L scope) или
    `scripts/dev/mcp_client_smoke.py` (Track K
    artefact, byte-identical).
  - Не запускал `1cv8.exe` (Track L работает на
    process-supervision layer, не на 1cv8 binary
    surface).
  - Не вводил никаких реальных credentials в repo /
    docs / commit message (placeholders only:
    `<USER>`, `<HOST>`, `<PORT>`, `<UNIT_NAME>`,
    `<SERVICE_NAME>`, `<LOG_PATH>`, `<VARNAME>`).
  - Не делал remote push / GitHub release —
    operator action, не часть трека.
  - Не открывал Track L Step 2 в этом же commit'е.
  - Не использовал premature closure language —
    Track L framed как **active** (Step 1
    in-progress, Step 2–6 впереди); фразы "service
    supervision solved" / "production-ready
    service supervision" / "all OS families
    supported" / "clustered HA" / "zero-downtime
    restart" появляются в touched docs **только**
    как explicit DENIALS.
- **Документ scope.** Ровно четыре файла: 2 новых
  planning-документа в `docs/architecture/` +
  README.md (Quickstart paragraph дополнен Track L
  active narrative; Active parallel track section
  reopened) + PROJECT-STATUS.md (header rewrite +
  this section).
- **Verify-release.ps1 -AllowDirtyTree.** GREEN на
  8 checks; никаких реальных credentials в Step 1
  diff'е; registries без drift'а.
- **Selfcheck после Step 1.** Зелёный: registries
  `read=15 / write=25 / intelligence=16` без
  drift'а; selfcheck_status=ok; никаких реальных
  credentials в Step 1 diff'е.
- **Следующий шаг (historical snapshot на момент
  Step 1 closure).** Тогда — Track L / Step 2
  (baseline audit of current long-running-process /
  service gap, docs-only). На момент Step 6
  closure'а — этот шаг уже закрыт (см. секцию
  «Parallel Track L / Step 2 (завершён)» ниже).

### Parallel Track L / Step 2 — service supervision baseline audit (завершён)

- **Цель.** Превратить general gap statement из Step 1
  plan §3 в descriptive baseline audit: inventory
  всех существующих launch surfaces (три
  `__main__.py` foreground-blocking entrypoints,
  `scripts/dev/launch.ps1` foreground-only dev
  wrapper, `scripts/release/install.ps1` materialise-
  but-not-register install fast-path); inventory
  supervision-adjacent surfaces (whole-repo grep
  для `systemd` / `launchd` / `Restart=` / `sc.exe` /
  `nssm` / `pywin32` / `supervisor` / `daemon` /
  `pidfile` / `--background` / `--fork` /
  `--daemonize` patterns); inventory signal-handling
  shape в `_stdio_transport.py:208` /
  `_network_transport.py:618-624` (оба catch
  `KeyboardInterrupt`; HTTP path `daemon_threads=True`
  at `:606-607`); 4-class breakdown (already-
  reusable / adjacent-but-insufficient / clearly-
  missing / explicitly-out-of-scope); directional
  Q1–Q6 resolutions с evidence-grounded
  recommendations + 14-item Step 3 handoff list.
- **Что shipped.** Один новый descriptive audit-
  документ:
  `docs/architecture/track-l-service-supervision-and-os-service-registration-baseline-audit.md`
  (966 lines, 9 sections). Никаких других файлов
  Step 2 не правил.
- **Ключевые находки.**
  - Foreground-blocking shape MCP server
    entrypoints **уже** correct для `Type=simple`
    systemd unit; нет необходимости в production
    code change.
  - 10 enumerated absences в repo at HEAD
    `e713f8e`: zero systemd unit files; zero
    launchd plists; zero Windows Service registration
    helpers; zero pidfile plumbing; zero
    `signal.signal(SIGTERM, ...)` handler; zero
    documented operator lifecycle vocabulary; zero
    journald-Event-Viewer integration; zero
    `EnvironmentFile=` recipe для MCP_TOKEN-class
    secrets; zero `Restart=` policy guidance; zero
    `User=` / `Group=` / service-account
    discipline.
  - **Critical adjacent-but-orthogonal finding:**
    `apps/platform/src/onec_platform/runtime.py`
    (Phase 5 / Step 3 + Phase 6 / Step 6) — in-
    process supervisor для operator-declared
    product-layer subprocesses (declared в
    `ProductConfig.runtime.services` с
    `restart_policy ∈ {"never", "restart-if-stale"}`).
    Module docstring lines 21–31 explicitly: "not a
    daemon manager / service manager (no Windows
    Service / systemd unit registration on this
    step)", "does NOT start MCP transports inside
    the three servers". Track L MUST keep
    supervision concern **outside** platform
    process tree on the OS layer; extending
    `runtime.py` rejected.
- **Q1–Q6 directional resolutions.** Q1 = closure-
  gate = recipe + declarative template + 5 lifecycle
  verbs. Q2 = systemd / Linux first; cross-OS prose
  для Windows + macOS. Q3 = default **PATH B**
  (docs + one declarative template); PATH A / PATH C
  acceptable per Step 3 decision. Q4 = all 5
  lifecycle verbs mandatory. Q5 = insufficient
  evidence list: "just use python -m"; launch
  instructions only; release docs only; generic
  prose without OS-facing recipe; operator lore;
  extending runtime.py in-process. Q6 = no
  production code change (foreground-blocking shape
  already `Type=simple`-compatible).
- **Что Step 2 НЕ делал.** Не правил production-код;
  не открывал Step 3 contract; не менял registries;
  не bumped'ил `pyproject.toml`; не запускал
  `1cv8.exe`; не вводил real credentials; не делал
  remote push.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries `read=15 / write=25 / intelligence=16`
  без drift'а; никаких реальных credentials в audit;
  никаких 1cv8.exe runs.
- **Commit.** `d58c8d9` (`Track L / Step 2 —
  service supervision baseline audit`).

### Parallel Track L / Step 3 — service supervision contract (завершён)

- **Цель.** Promote Step 2 directional findings в
  normative contract: lock final Step 4 PATH;
  codify systemd-first OS-family target; codify all
  5 lifecycle verbs mandatory; lock Step 4 file
  surface; lock Step 4 forbidden-files list; lock
  Step 4 verification protocol; preserve Track G /
  H / I / J / K invariants byte-identical; preserve
  `apps/platform/src/onec_platform/runtime.py`
  byte-identical NOT extended.
- **Что shipped.** Один новый normative contract-
  документ:
  `docs/architecture/track-l-service-supervision-and-os-service-registration-contract.md`
  (1401 lines, 14 sections, RFC 2119 MUST / MUST
  NOT / SHOULD / SHOULD NOT / MAY language).
  Никаких других файлов Step 3 не правил.
- **Ключевые decisions.**
  - **Step 4 PATH B locked** в §7.1 (PATH A docs-
    only rejected в §7.2 — prose alone cannot close
    "zero systemd unit files" gap honestly; PATH C
    docs+template+wrapper rejected в §7.3 — POSIX
    operators don't use PowerShell wrappers, sibling
    `.sh` wrapper maintenance liability for marginal
    benefit).
  - **systemd / Linux first locked** в §5.1 as
    implementation-covered closure-gate OS family;
    cross-OS Windows + macOS prose-only mandatory
    в §5.3; cross-OS template artefacts forbidden
    в Step 4 (§5.4).
  - **All 5 lifecycle verbs (start / stop /
    restart / status / logs) mandatory** в §6.1;
    partial coverage rejected в §6.2.
  - **No production code change** в §10.1 / §10.2 /
    §10.5; `runtime.py` byte-identical NOT extended
    в §3 fact #4 / §9.1 item 6 / §10.2.
  - **Closure-gate contract C1–C10** locked в §4.1:
    recipe + template + 5 verbs + 1 OS family
    implementation + cross-OS prose + placeholder
    discipline + honest non-goals + carry-forward
    invariants + verify-release GREEN + selfcheck
    OK.
  - **15-item insufficient-evidence list** locked в
    §9.1.
  - **11 forbidden maturity-claim phrases** locked
    в §9.3.
- **Step 4 file surface lock.** Allowed: exactly two
  new files at `docs/operators/service/service-
  supervision.md` (recipe; ≥10 sections;
  ≤1200 soft / ≤1500 hard LOC) и
  `docs/operators/service/mcp-server.service`
  (systemd template; ≤80 LOC including comments;
  `Type=simple`; placeholders only). Forbidden:
  exhaustive list в §8.4 (production code,
  pyproject, scripts, all Track / closure docs,
  Track-precedent artefacts, examples, all
  Track L Step 1–3 docs).
- **Step 4 verification protocol locked** в §11.1
  как 22 checks: S1–S6 scope; Z1–Z2 selfcheck;
  R1 release-verify; H1–H7 honesty; C1–C10 recipe
  / template coverage. Plus P1–P4 post-commit;
  V1–V7 Step 5 carry-forward; W1–W8 Step 6 carry-
  forward.
- **Что Step 3 НЕ делал.** Не правил production-
  код; не открывал Step 4 implementation; не менял
  registries; не bumped'ил `pyproject.toml`; не
  запускал `1cv8.exe`; не вводил real credentials;
  не делал remote push.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в contract; никаких 1cv8.exe runs.
- **Commit.** `76342a5` (`Track L / Step 3 —
  service supervision contract`).

### Parallel Track L / Step 4 — service supervision recipe and systemd template (завершён)

- **Цель.** Operationalize Step 3 contract как
  narrow PATH B implementation: два новых файла
  под `docs/operators/service/` — operator-facing
  recipe + declarative systemd unit-file template.
  Никаких production code changes; никаких
  pyproject changes; никаких scripts changes.
- **Что shipped.** Ровно два новых файла:
  - `docs/operators/service/service-supervision.md`
    (972 lines под contract §8.5 ≤1200 soft / ≤1500
    hard caps; 15 top-level sections: §1 Purpose с
    explicit denial list, §2 Supported closure
    target (Linux/systemd implementation-covered +
    Windows/macOS prose-only), §3 Preconditions,
    §4 Service model с §4.2 Type=simple defence +
    §4.3 runtime.py non-extension explanation + §4.4
    signal handling, §5 Start с one-time install +
    systemctl start, §6 Stop с KillSignal=SIGINT
    explanation + in-flight abandonment policy, §7
    Restart с stop-then-start semantics + rate
    limit, §8 Status с systemctl status + show +
    is-enabled, §9 Logs с journalctl -f / --since /
    -p err, §10 Environment / token configuration с
    full placeholder vocabulary table + Track H /
    Track D cross-references, §11 Reverse proxy /
    TLS boundary reminder (Track H / Track J carry-
    forward), §12 Cross-OS notes для Windows NSSM +
    macOS launchd prose-only с explicit gap-naming,
    §13 Honest non-goals across 7 subcategories +
    §13.8 11 forbidden phrases, §14 Cross-
    references, §15 Honest summary).
  - `docs/operators/service/mcp-server.service`
    (76 lines including comments под contract §8.5
    ≤80 hard cap; declarative systemd unit с
    [Unit] / [Service] / [Install] sections;
    `Type=simple`; placeholders exclusive — `<USER>`,
    `<GROUP>`, `<WORKING_DIR>`, `<ENV_FILE_PATH>`,
    `<PYTHONPATH>`, `<PYTHON_BIN>`,
    `<MCP_SERVER_MODULE>`, `<TRANSPORT>`,
    `<CONFIG_PATH>`, `<HOST>`, `<PORT>`,
    `<MCP_TOKEN_VARNAME>`; RECOMMENDED defaults
    inline `Restart=on-failure` / `RestartSec=5s` /
    `StartLimitBurst=5` /
    `StartLimitIntervalSec=600s` /
    `KillSignal=SIGINT` / `KillMode=mixed` /
    `TimeoutStopSec=15s`).
- **No production code change.** Foreground-
  blocking shape `__main__.py` modules already
  `Type=simple`-compatible. `KillSignal=SIGINT` в
  template re-routes service stop к existing
  `KeyboardInterrupt` graceful path в
  `_stdio_transport.py:208` /
  `_network_transport.py:618-624` без Python-side
  signal handler.
- **All 5 lifecycle verbs end-to-end на systemd.**
  §5 start: `systemctl start <UNIT_NAME>`. §6 stop:
  `systemctl stop <UNIT_NAME>` (KillSignal=SIGINT
  routes to KeyboardInterrupt path). §7 restart:
  `systemctl restart` (stop-then-start; not hot
  reload). §8 status: `systemctl status` + `show`
  + `is-enabled`. §9 logs: `journalctl -u
  <UNIT_NAME> -f` / `--since` / `-p err`. Cross-OS
  verbs в §12.1 Windows (NSSM start / stop /
  restart, sc query, log files) и §12.2 macOS
  (launchctl bootstrap / bootout / kickstart /
  print, log files) prose only.
- **22-check Step 3 §11.1 verification protocol all
  PASS.** S1–S6 scope (exactly 2 new files at exact
  paths, no forbidden modifications, recipe 972 LOC
  ≤ 1500, template 76 LOC ≤ 80). Z1–Z2 selfcheck.
  R1 release-verify GREEN. H1–H7 honesty. C1–C10
  recipe/template coverage (15 sections ≥ 10, all
  5 verbs, Windows + macOS sections, RECOMMENDED
  defaults documented, 11 forbidden phrases as
  denials, cross-references to G/H/I/J/K, valid
  systemd syntax, placeholders exclusive,
  Type=simple).
- **Что Step 4 НЕ делал.** Не правил production-
  код; не правил `pyproject.toml`; не правил
  existing `scripts/*`; не правил
  `docs/operators/deployment-boundary.md`; не
  правил `apps/platform/README.md`; не правил
  SECURITY.md; не правил README / PROJECT-STATUS /
  CHANGELOG; не правил manuals; не запускал
  `1cv8.exe`; не вводил real credentials; не делал
  remote push; не extending `runtime.py`.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в recipe / template; никаких
  1cv8.exe runs.
- **Commit.** `efb4ea1` (`Track L / Step 4 —
  service supervision recipe and systemd
  template`).

### Parallel Track L / Step 5 — operator docs and service-supervision alignment (завершён)

- **Цель.** Узкое CLASS-1 docs-alignment:
  обновить только те operator/release-facing docs,
  у которых после Step 4 появился прямой factual
  drift. Track L остаётся active на Step 5 (closure
  narrative — Step 6 territory).
- **Drift inventory.**
  - **CLASS 1 (direct factual drift, fixed):**
    `README.md` Quickstart paragraph (говорил
    "Step 1 — planning-only, documentation-only" —
    stale); `README.md` Active parallel track
    section (говорил "Track L сейчас на Step 1" с
    "Следующий шаг — Step 2" — stale);
    `docs/release-handoff.md` "What is NOT in this
    handoff" line (говорил "supervisor daemon /
    systemd unit / Windows Service registration /
    hot reload" not in handoff — stale после Step 4
    shipped systemd unit template + recipe);
    `docs/release-handoff.md` "Known limitations"
    supervisor bullet и Stdio + HTTP baseline
    supervisor mention (same stale claim);
    `docs/release-handoff.md` "What is in this
    handoff" (missing parallel Track L bullet);
    `docs/release-handoff.md` "Where to read
    deeper" (missing parallel Track L bullet).
  - **CLASS 2 (cross-link skipped per Step 3
    contract default):** `SECURITY.md` (recipe §10
    placeholders only; no security claim change);
    `apps/platform/README.md` (runtime.py byte-
    identical, README's existing supervisor non-
    goals inventory still qualitatively accurate);
    `scripts/dev/README.md` (no service/supervisor
    mention); manuals (no actively-misleading
    text).
  - **CLASS 3 (closure territory, NOT touched):**
    `PROJECT-STATUS.md`, `CHANGELOG.md`,
    `pyproject.toml` `version`, README's "Closed
    parallel tracks" list, README's "Track L
    detail (закрыт)" section.
- **Что shipped.** Два файла modified: `README.md`
  (Quickstart paragraph + Active parallel track
  section rewritten с per-step bullets для Steps
  1–4 closed + Step 5 active framing) и
  `docs/release-handoff.md` (six narrow CLASS-1
  edits across "What is in this handoff", "What is
  NOT in this handoff", "Known limitations" x2, и
  "Where to read deeper"). 252 insertions, 102
  deletions; zero new files.
- **Verify-release.** GREEN на 8 checks; selfcheck
  registries без drift'а; никаких реальных
  credentials в commit'е; никаких 1cv8.exe runs;
  `pyproject.toml` `version=0.5.1` preserved;
  Track L still active framed везде
  (`PROJECT-STATUS.md` / `CHANGELOG.md` /
  closed-tracks list untouched).
- **Commit.** `82345b4` (`Track L / Step 5 —
  operator docs and service-supervision
  alignment`).

### Parallel Track L / Step 6 — final integration pass and track closure (завершён)

- **Цель.** Final integration pass над Track L
  Steps 1–5 + честное Q7-решение + closure
  narrative в README / PROJECT-STATUS / CHANGELOG.
  Закрыть весь Track L. Active tracks remaining =
  none после Step 6.
- **Q7 = NO-BUMP.** Track L закрыт под existing
  `0.5.1` без further version bump. Защита
  решения:
  - **Zero production code change** across all six
    Track L steps. `apps/*/src/`, `packages/*/src/`,
    `_network_transport.py`, `_stdio_transport.py`,
    `installer.py`, `runtime.py`,
    `process_control.py`, `runtime_logs.py`,
    `models.py` byte-identical к Track K closure
    state (`0e40056`).
  - **Zero defect-class fix.** Step 2 audit
    explicitly показал, что foreground-blocking
    shape MCP server entrypoints **уже** correct
    для `Type=simple` systemd unit; Track L
    добавил operator-runnable documentation +
    declarative template для уже-существующего
    behaviour, не fix'ил bug.
  - **Zero new external capability для ordinary
    product consumers.** Recipe и template живут
    под `docs/operators/service/`, симметрично
    Track J recipe; не в `[project.scripts]`; не
    importable от external consumers; не часть
    pip-install surface; не запускаются
    automatically install fast-path'ом.
  - **Zero new public API surface.** No new public
    types, functions, imports, `__all__` exports,
    `[project.scripts]` entries, `ProductConfig`
    schema fields, CLI flags на existing servers,
    или HTTP endpoints.
  - **SemVer §6 не оправдывает PATCH.** PATCH =
    "backward-compatible bug fixes"; Track L не
    fix'ил никакого bug.
  - **Track I PATCH precedent не переносится.**
    Track I имел `+15 LOC` production code И
    previously-broken installer round-trip; Track
    L не имеет ни того, ни другого.
  - **Track J NO-BUMP precedent applies directly.**
    Track J тоже закрылся без bump'а под existing
    `0.5.1`, с docs + один operator-facing
    artefact. Track L following same pattern с
    docs + один operator-facing recipe + один
    declarative template.
  - **Track K NO-BUMP precedent applies directly.**
    Track K тоже закрылся без bump'а под existing
    `0.5.1`, с docs + один operator-runnable
    diagnostic artefact. Track L matches that
    pattern.
  - **Track A / B / C / E precedent.** Те docs-
    heavy треки тоже закрылись без separate
    version bumps в `CHANGELOG.md`.
  - **Step 1 plan §12.Q7 / Step 3 contract §10.4 /
    §14** explicitly authorize NO-BUMP if Step 4
    не ship'нет defect-class fix observable by
    end-users и не вводит new CLI flag. Step 4
    ship'нул operator-facing recipe + declarative
    template, не defect fix; не new CLI flag. Все
    условия NO-BUMP выполнены.
- **Closure scope (narrowest honest).** Touched:
  `README.md` (Quickstart paragraph flipped от
  active → no-active-track wording; Active
  parallel track section compressed back к
  no-active-track; new "Track L detail (закрыт)"
  section added above "Track K detail (закрыт)";
  Closed parallel tracks list extended from
  одиннадцать to двенадцать с Track L entry);
  `PROJECT-STATUS.md` (header rewritten от
  "Track L / Step 1 in progress" к "no active
  step + Track L fully closed"; historical-edit
  annotation на конце Track K Step 6 section
  updated; per-step closure sections для Step 2 /
  Step 3 / Step 4 / Step 5 / Step 6 inserted);
  `CHANGELOG.md` (Track L closure narrative
  inserted под existing `## 0.5.1` heading с
  explicit NO-BUMP framing). **NOT touched:**
  `pyproject.toml` (NO-BUMP); `SECURITY.md`;
  `docs/release-handoff.md` (Step 5 уже выровнял);
  `apps/platform/README.md`;
  `docs/operators/deployment-boundary.md` (Track J
  artefact); `docs/operators/service/service-
  supervision.md` (Step 4 deliverable immutable);
  `docs/operators/service/mcp-server.service`
  (Step 4 deliverable immutable);
  `scripts/dev/README.md`; Track L Step 1–4
  architecture docs (frozen anchors); production
  code; `apps/*/src/`; `packages/*/src/`; всё
  остальное `scripts/*`; `examples/*`; manuals.
- **Verify-release.** GREEN на 8 checks pre-commit
  (`-AllowDirtyTree`) и post-commit (clean tree);
  selfcheck registries `read=15 / write=25 /
  intelligence=16` без drift'а; никаких реальных
  credentials в closure commit'е; никаких 1cv8.exe
  runs; никакого remote push.
- **Track L closure итог.** Двенадцать post-phase
  parallel track'ов (A, B, C, D, E, F, G, H, I, J,
  K, L) полностью закрыты. Phase 7 как линейная
  фаза не запланирована. Открытие следующего
  параллельного трека — отдельное operator
  decision. Логичные кандидаты (без автоматического
  открытия): TLS-in-process / mTLS expansion
  (отдельный enterprise-grade identity track);
  full packaging ecosystem track (`.msi` / `.deb` /
  signed distribution / GUI installer / wizard /
  PyPI wheel publication); multi-version 1С matrix
  expansion (post-Track-E follow-up); full
  rollback / AST work (post-Track-F / post-
  Track-A follow-ups); full observability stack
  track (OpenTelemetry / Prometheus / log
  aggregation); web UI / dashboard frontend track;
  in-repo daemon framework / pywin32 service
  wrapper / launchd plist artefacts as a separate
  track. Эти кандидаты — recommendation only, не
  auto-opened.

## Phase 6 закрыта

**Phase 6 закрыта на Step 9.**

Что закрыто честно (Phase 1–5 + Phase 6 / Step 1–9 в
одном связном продуктовом контуре):

- Phase 1 — read MVP.
- Phase 2 — write MVP с `run_write_flow` дисциплиной как
  единственным mutating-путём.
- Phase 3 — Phase 3 metadata changes (object/attribute/form/
  module-level mutating tools и verify-tools на substring-патч'е).
- Phase 4 — intelligence MVP (read-only по конструкции).
- Phase 5 — product layer (bootstrap / install / runtime /
  dashboard / workflows / rollback / real-stand) на восьми
  шагах с финальным integration pass'ом.
- **Phase 6 — Industrialization & Completion Track:**
  - Step 2: один real binary-backed slice
    (`create_dump_snapshot`); operator-declared argv-template
    с whitelisted placeholder'ами; runtime failure НЕ
    падает в silent stub fallback.
  - Step 3: install / setup fast path сокращает manual
    ritual до одной boundary-функции; атомарная запись
    JSON; round-trip через `bootstrap_product_from_json_file`.
  - Step 4: первый исполняемый rollback path для двух
    tool'ов whitelist'а (`add_catalog_attribute`,
    `add_document_attribute`); реализация **только** через
    public `restore_dump_file_from_snapshot` (не back-door);
    обязательный post-rollback verify через
    `diff_dump_fragment`; audit-row `details` дополнение
    backward-compatible.
  - Step 5: первый structural XML edit slice
    (`add_form_attribute`); шесть DOM-style helper'ов в
    `metadata_ops.py`; новая verify-ветка
    `kind="form_attribute_exists"`; на Step 9 добавлен
    минимальный guided-wrapper `safe-add-form-attribute`
    (см. выше) — это не новый MCP tool, а thin guide над
    существующим write-tool'ом.
  - Step 6: structured runtime logs +
    rotate-if-exceeds-size в одно поколение, узкий
    `restart_policy ∈ {"never","restart-if-stale"}`
    (boundary-only, no daemon); enriched
    `RuntimeServiceState` + `runtime-state.json` schema 2
    с backward-compat reader'ом.
  - Step 7: standalone manuals + runbooks
    (`docs/operator-manual.md`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks.md`); сам
    Step 7 — documentation-only.
  - Step 8: узкий enterprise-foundation contract + read-only
    `inspect_enterprise_foundation` boundary; четыре
    проверяемые секции; верт `foundation_level ∈
    {"absent","minimal","partial","strong"}` плюс
    отдельный `ready_for_enterprise_track`. Никакого
    fake `enterprise_ready` флага.
  - Step 9: integration pass всего вышеперечисленного в
    одном связном сценарии + шесть honest failure paths +
    пять discipline asserts. Две минимальные кодовые
    правки (`safe-add-form-attribute` workflow +
    `_config_to_dict` round-trip fix).

Что осталось до состояния finished industrial product
(парallel / enterprise tracks **после** Phase 6):

- **Полное замещение Phase 2 stub'ов:** Phase 6 закрыла
  один binary-backed путь (`create_dump_snapshot`).
  `apply_config_from_files` и `update_database_configuration`
  остаются stub-backed (process apply / process update,
  не настоящие `1cv8 LoadConfigFromFiles` / `UpdateDBCfg`).
  Полный набор binary-backed dispatch'ей —
  parallel track.
- **Полная rollback-вселенная:** Phase 6 закрыла rollback
  для двух tool'ов из 25 в registry write-server'а.
  Расширение whitelist'а (включая нетривиальные case'ы
  типа `delete_*` write-tool'ов, у которых пока нет
  семантики удаления в 1С) — parallel track.
- **Полное metadata coverage и AST-парсер:** Phase 6
  ship'нула один structural edit (`add_form_attribute`).
  Полный DOM-edit для всех metadata-операций, BSL
  AST-парсер, namespaced 1cv8 cards — отдельные
  технологические track'и.
- **Production-grade process supervision:** Windows
  Service / systemd unit registration, hot reload, real
  background watcher, exponential backoff / max-restarts,
  multi-generation log rotation, journald / log
  aggregation / forwarding — parallel track.
- **Полный enterprise super-set:** SSO/RBAC, multi-tenant,
  secrets vault как сервис, federated audit storage,
  policy-as-code DSL, multi-instance HA, web-UI /
  dashboard frontend, federated identity. Step 8 шипнул
  только foundation; полная enterprise-вселенная —
  parallel track.
- **Production-grade MCP transport:** `__main__` / CLI у
  трёх MCP-серверов; production-grade transport
  (HTTP/stdio); auth между orchestrator'ом и MCP клиентами.
  Parallel track.
- **GUI installer / wizard / `.msi` / `.deb` / signed
  binary distribution / packaging ecosystem:** parallel
  track. Phase 6 ship'нул только short install script +
  declarative template.
- **Полный version-matrix smoke на всех 1С версиях и
  стендах:** parallel track. Phase 6 ship'нул только
  controlled smoke contract.
- **Полная intelligence-вселенная:** ML / clustering
  поверх `analyze_event_log_patterns`; настоящий
  topo-sort `suggest_safe_change_order` по графу
  зависимостей. Parallel track.
- **Operator runbook coverage:** Phase 6 / Step 7
  ship'нул шесть recipes. Production runbook
  ecosystem — parallel track.

Эти ограничения зафиксированы как **honest constraints**:
платформа НЕ претендует на enterprise-ready / production-
ready статус. `ready_for_enterprise_track=True` (Step 8)
означает буквально «foundation under next-step enterprise
work собран», не «готовы к prod».

Non-blocking follow-ups, явно вынесенные за пределы
Phase 6 (или в parallel / enterprise tracks):

- **Полное замещение всех Phase 2 stub'ов
  одновременно** на сетку режимов
  `DESIGNER` / `ENTERPRISE` / `DumpCfg` —
  parallel track после Phase 6. Phase 6
  ship'ит **один** binary-backed путь, не три
  одновременно.
- **Полная rollback-вселенная** для всех
  write-tool family'й — parallel track. Phase 6
  ship'ит исполнимый rollback хотя бы для
  одного класса.
- **Полное metadata coverage** (все возможные
  `delete_*`, `replace_*`, `refactor_*`) —
  parallel track. Phase 6 — точечный добор.
- **Полный AST-парсер XML / BSL** — отдельный
  технологический track. Phase 6 — один шаг к
  structural editing.
- **Полный enterprise super-set:** SSO/RBAC,
  multi-tenant, secrets vault как сервис,
  federated audit storage, policy-as-code DSL,
  multi-instance HA — отдельный
  enterprise-track после Phase 6.
- **Production-grade MCP transport / `__main__`
  / CLI у трёх MCP-серверов** — отдельный
  track.
- **Hot reload без рестарта процесса**, OS-level
  service supervision (Windows Service / systemd
  unit), automatic-restart-supervisor —
  отдельный track.
- **Web-UI / dashboard frontend / workflow
  runner UI / rollback assistant UI** —
  отдельный track после Phase 6.
- **Многосторонний end-to-end на матрице 1С
  версий и стендов** — отдельный track.
- **Настоящий topo-sort
  `suggest_safe_change_order` по графу
  зависимостей; ML / clustering поверх
  `analyze_event_log_patterns`** — оба
  остаются parallel tracks.
- **GUI installer / wizard** — out of Phase 6
  scope (Phase 6 ship'ит short install script
  + declarative template).
- **Override-флаг для запуска mutating
  workflow'ов на `degraded` dashboard'е**;
  **автоматический retry transient mutating
  step'ов**; **shared sub-tool cache внутри
  dashboard-операции**; **настраиваемый
  timeout для smoke probe** — все возможные
  enhancements, не входят в Phase 6.

## Крупные этапы проекта (что ещё осталось)

- **Phase 0 — инфраструктурная база.** Каркас монорепо, базовые конфиги,
  общие пакеты-заглушки, CI-скелет. **Закрыта.**
- **Phase 1 — read MVP.** Минимальный рабочий `mcp-read-server`: чтение метаданных,
  конфигурации и данных 1С через MCP. **Закрыта.**
- **Phase 2 — write MVP.** Минимальный рабочий `mcp-write-server`: безопасные
  операции изменения с политиками и аудитом. **Закрыта.**
- **Phase 3 — metadata changes.** Полноценные операции над метаданными
  конфигурации 1С (объекты, реквизиты, формы, модули). **Закрыта.**
- **Phase 4 — intelligence layer.** `mcp-intelligence-server`: read-only
  intelligence-tools поверх read/write слоёв — dependency / impact
  analysis, troubleshooting, рекомендации. **Закрыта** (16 public
  tools, группы A/B/C/D полностью покрыты, integration pass
  Step 7 пройден).
- **Phase 5 — product layer.** Переход от набора серверов и tool'ов
  к цельному продуктовому контуру: bootstrap, runtime orchestration,
  health dashboard, guided workflows, rollback / recovery / audit
  UX, real-stand / 1cv8 binary integration track. **Закрыта**
  (Step 1–8 завершены; final integration pass пройден без
  правок кода; product-layer контур end-to-end отрабатывает на
  synthetic-окружении; см. `docs/architecture/phase-5-step-map.md`).
  Закрытие Phase 5 **не означает** полностью industrial-grade /
  enterprise-ready продукт — крупные хвосты адресованы Phase 6
  (точечно) и parallel-track'ами после.
- **Phase 6 — industrialization & completion track.** Доведение
  продукта до finished / deployable состояния поверх готового
  ядра Phase 1–5: реальный 1cv8-backed dispatch (хотя бы для
  одного Phase 2 stub-backed пути), исполнимый rollback хотя
  бы для одного класса write-tool'ов, короткий install/setup
  сценарий (≤ 5 ручных шагов), real-stand end-to-end smoke на
  reference stand'е, runtime hardening (логи + базовая restart
  policy), operator/admin/developer manuals + runbooks как
  standalone docs, foundation для enterprise-трека.
  **Активная фаза** (Step 1 — planning Industrialization &
  Completion Track — в процессе; всего планируется 8 шагов,
  см. `docs/architecture/phase-6-step-map.md`). Закрытие
  Phase 6 **не означает** полностью enterprise-ready
  продукт — полная enterprise-вселенная (SSO/RBAC,
  multi-tenant, secrets vault, federated audit, policy-as-code
  DSL, multi-instance HA), полный AST-парсер, web-UI,
  multi-instance HA остаются за пределами фазы как parallel
  track'и / enterprise track после Phase 6.
