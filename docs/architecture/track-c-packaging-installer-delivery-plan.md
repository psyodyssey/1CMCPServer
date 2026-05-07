# Parallel Track C — Packaging & Installer Delivery Plan

## Назначение трека

Phase 1–6 закрыты. Parallel Track A — Full Real 1cv8-backed Write
Path — закрыт на Step 7. Parallel Track B — Productization &
Delivery Polish — закрыт на Step 6. У платформы есть:

- работающее ядро (`mcp-read-server` 15 tools, `mcp-write-server`
  25 tools, `mcp-intelligence-server` 16 tools, product layer
  `onec_platform`);
- доказанный binary-backed write path с reference-stand round-trip
  evidence;
- git-репозиторий на ветке `main` с linear history;
- `.gitignore` под project-specific артефакты, `LICENSE`
  (Apache-2.0), `CHANGELOG.md`, `SECURITY.md`;
- operator-discoverable install fast path:
  `scripts/release/install.ps1` (тонкий wrapper);
- operator/dev local launch umbrella: `scripts/dev/launch.ps1`
  (`selfcheck` / `repl` / `run` / `help`);
- root README с верхним Quickstart-блоком (install / check /
  launch + map of deeper docs).

Track B закрыл базовую productization-полировку. **Самый жирный
незакрытый разрыв сейчас — не execution layer и не базовая
ergonomics, а delivery/packaging слой.** Конкретно:

- `scripts/release/install.ps1` — это **тонкий wrapper над одной
  install-функцией** (`run_install_fast_path_from_json_file`).
  Это не полноценный release-facing layer — нет pre-handoff
  sanity check'а, нет release-time consistency verify, нет
  bundle preparation step'а.
- **Нет release handoff документа для receive-side оператора**.
  Текущие manuals (`docs/operator-manual.md`,
  `docs/administrator-manual.md`, `docs/developer-manual.md`)
  ориентированы на оператора, который уже работает с проектом.
  Для операторa, к которому проект *передают*, нет короткого
  "вот что вы получили / вот как принять / вот как проверить"
  документа.
- **Нет reproducible install-sequence checklist'а** с системными
  зависимостями. Quickstart упоминает Python 3.11 + PowerShell +
  опциональный `1cv8.exe`, но не даёт пошаговую честную последо-
  вательность от чистой машины до зелёного `selfcheck_status=ok`.
- `pyproject.toml` имеет `[tool.hatch.build.targets.wheel] packages
  = []` — **wheel build по сути no-op**. Trying to `python -m
  build` сейчас не даст meaningful artifact. Это технический
  долг, который Track B сознательно не трогал.
- **Нет single canonical release entrypoint map'а**: install /
  verify / launch / handoff entrypoints разбросаны по
  `scripts/release/README.md`, `scripts/dev/README.md`, root
  Quickstart, и отдельным docs. Для нового оператора нет одного
  места, где всё это собрано.
- **Нет release-time pre-handoff sanity check'а** — единого
  скрипта, который перед handoff'ом проверяет: working tree
  clean, registries без drift'а, references valid, никаких
  cleartext credentials в working tree, никаких stale lockfile'ов.

Этот разрыв — **не enterprise-вселенная**, **не production-grade
transport**, **не AST-парсер**, **не web-UI**. Это **доведение
существующего продукта до состояния, в котором его удобно
передать другому человеку как packaged unit'ом**. Все safety
guarantees Phase 1–6 + Track A + Track B (`run_write_flow`
единственный mutating-путь, intelligence read-only, нет
back-door write channel'а из product layer'а, fail-closed по
умолчанию, audit append-only, нет `shell=True`) **сохраняются
без изменений**.

Это **не** новый MCP-surface sprint и **не** новый execution-core
sprint. Это **post-Track-B packaging & installer delivery
track** на узкую зону release scaffolding.

Назвать это «Phase 7» было бы нечестно: ни одной новой
execution-фазы не запланировано. Этот трек —
**Parallel Track C — Packaging & Installer Delivery** —
открывается как третий parallel-track после закрытых Phase 6,
Track A и Track B.

## Целевой результат

К моменту закрытия Track C новый operator/developer, получивший
repository, должен иметь возможность в чёткой discoverable
последовательности:

1. **Понять что это** — за 1–2 минуты по root README + одному
   release-receive-стороннему документу.
2. **Подготовить окружение** — pre-install checklist (Windows +
   PowerShell версия + Python 3.11 + опциональный `1cv8.exe`),
   воспроизводимый на чистой машине.
3. **Установить** — через `scripts/release/install.ps1`, без
   знания internal Python module path и без ручного PYTHONPATH
   ритуала.
4. **Проверить** — через `scripts/release/verify-release.ps1`
   (новый pre-handoff sanity wrapper) или эквивалент, который
   честно говорит, готов ли recipient к handoff.
5. **Передать дальше** — `docs/release-handoff.md` (новый)
   объясняет, как принять repo, как проверить целостность, как
   воспроизвести install/check/launch, как отдать другому.

При этом Track C должен оставаться **scripts-only / docs-only**
по стилю — production-код не правится, registries без drift'а,
никаких новых MCP tool'ов.

## Что Track C **не** закрывает (явно)

- **GUI installer wizard** — никаких graphical installer flows.
  Out of scope.
- **Signed binary distribution** — `.msi`, `.deb`, signed
  artifacts. Out of scope.
- **Packaging для package managers** — публикация на PyPI,
  Chocolatey, winget, apt и т.п. Out of scope. (Wheel build
  внутри проекта — да, через `pyproject.toml`; публикация — нет.)
- **systemd unit / Windows Service registration** — out of
  scope. (Phase 6 / Step 6 ship'нул минимальный `restart_policy`
  contract; полная supervisor integration остаётся parallel
  track'ом.)
- **Enterprise deployment platform** (SSO/RBAC, multi-tenant,
  secrets vault как сервис, federated audit storage,
  policy-as-code DSL, multi-instance HA) — out of scope.
- **Web-UI / dashboard frontend / workflow runner UI** — out of
  scope.
- **Production-grade MCP transport** — authentication /
  authorisation / multi-tenant isolation / hardened network
  transport. Out of scope. (Track C может зафиксировать в
  release-handoff документе **honest constraint**, но не
  закрывает его.)
- **Новые MCP tools** — registry'ы остаются `read=15 / write=25
  / intelligence=16` без drift'а. Любое нарушение — failed shape
  check.
- **Production code rewrite** — Track C не правит
  `apps/*/src/**/*.py` или `packages/*/src/**/*.py`. Минимальное
  допустимое касание production area — `pyproject.toml` (если
  фактическое packaging targets list требует обновления для
  honesty), но и это решается отдельной justification'ой в
  соответствующем шаге.
- **Multi-version 1С matrix smoke** — out of scope. Track C
  вообще не запускает `1cv8.exe`.
- **Полный AST-парсер XML/BSL** — out of scope.
- **Полная rollback/delete-вселенная** — out of scope.
- **Hot reload, OS-level service supervision** — out of scope.
- **GitHub remote push / publication / GitHub Pages /
  GitHub Releases auto-build** — out of scope. Track C готовит
  repo к handoff'у, но не делает publication. Push — operator
  action.

## Guardrails

- **Никакого расширения MCP surface'а.** `read=15 / write=25 /
  intelligence=16` — invariant. Любое нарушение — failed shape
  check.
- **Никакого back-door write channel'а.** Product layer
  по-прежнему не пишет ни в инфобазу, ни в audit, ни в snapshot
  tree вне `run_write_flow`.
- **Никаких `shell=True`.** Если в трек попадёт subprocess
  invocation, он идёт через argv-list или через
  `onec_process_runner`-стиль argv.
- **Никаких credentials в repo.** Никакие cleartext пароли /
  токены / ключи / `1Cv8.1CD`-файлы не коммитятся. `.gitignore`
  уже ловит local writable config'и (Track B / Step 2 baseline).
- **Никаких новых runbook'ов ради новых runbook'ов.**
  Существующие manualы остаются как есть, если только не
  всплывает реальный gap.
- **Не претендуем на enterprise-ready / production-ready
  статус.** Closure Track C означает буквально «продукт удобно
  передать другому человеку как packaged unit», не «продукт
  готов в prod».
- **Scripts-only / docs-only по умолчанию.** Production-code
  changes допустимы только если будет доказано, что без них
  шаг буквально недостижим (по аналогии с Track B / Step 4
  default'ом).

## Критерии приёмки

1. **Release entrypoint map присутствует.** Один canonical
   document (например, `docs/release-handoff.md` или раздел в
   уже существующем месте) перечисляет все release-facing entry
   points: install / verify / launch / handoff. Поддерживаемый
   как single source of truth.
2. **Reproducible install sequence checklist присутствует.**
   Чёткая, проверяемая последовательность от чистой Windows
   машины до зелёного `selfcheck_status=ok`. Все
   референсируемые файлы реально существуют.
3. **Pre-handoff sanity check присутствует.** Скрипт или
   documented procedure, который перед handoff'ом проверяет:
   working tree clean, registries без drift'а, references valid,
   никаких cleartext credentials, никаких stale lockfile'ов.
4. **Release-facing scripts/release/ layout честный.** README
   директории описывает структуру; entry points понятны;
   underscore-prefix конвенция (`_install_runner.py`)
   соблюдается для не-public helpers.
5. **`pyproject.toml` packaging targets honest.** Либо
   `[tool.hatch.build.targets.wheel] packages` заполнен реальным
   списком, либо явный комментарий, что wheel build намеренно
   no-op в этом track'е и почему.
6. **Release handoff docs не врут.** `docs/release-handoff.md`
   (новый) или эквивалент честно перечисляет: что входит в
   handoff, что НЕ входит, какие honest constraints остаются
   после Track C, куда смотреть для дальнейшего деплоя.
7. **Selfcheck остаётся зелёным.** `imports_ok = true`,
   registries без drift'а, `selfcheck_status = ok`.
   `.github/workflows/dev-check.yml` зелёный.
8. **Никаких production-правок core.** `apps/*/src/**/*.py`,
   `packages/*/src/**/*.py` — без изменений на всём track'е.
   Минимальное касание `pyproject.toml` — только если требуется
   для критерия 5 и обосновано в соответствующем шаге.
9. **Honest constraints зафиксированы.** README, CHANGELOG и
   release-handoff документ прямо перечисляют, что Track C **не**
   закрывает (см. список выше).
10. **Repo по-прежнему готов к выкладке.** Manual visual review:
    ни одного credential в commit history, ни одного «брошенного»
    артефакта, README читается осмысленно, CI зелёный,
    pre-handoff sanity check возвращает зелёный.

## Открытые вопросы (resolve в Step 2+)

- **Q1. Где именно живёт release-handoff документ?** Default
  proposal — `docs/release-handoff.md` (по симметрии с
  существующими manualами). Альтернатива —
  `docs/release/handoff.md` или прямо в `scripts/release/README.md`
  как расширенная секция. Решение в Step 4.
- **Q2. Pre-handoff sanity check — отдельный скрипт или
  расширение существующего `scripts/dev/launch.ps1`?** Default
  proposal — отдельный `scripts/release/verify-release.ps1`
  (по симметрии с `install.ps1`); если можно честно сделать как
  `launch.ps1 verify-release` — допустимая альтернатива. Решение
  в Step 2.
- **Q3. `pyproject.toml` `[tool.hatch.build.targets.wheel]
  packages`** — заполнить честным списком (все
  `apps/*/src/<package>` и `packages/*/src/<package>`) или
  оставить пустым с явным comment'ом «wheel build намеренно
  no-op до настоящего packaging track'а после Track C»?
  Default proposal — заполнить честным списком, потому что
  это меняет wheel build с no-op на meaningful artifact без
  нового surface'а; но это **минимальная production-area
  правка** и требует явного operator gate. Решение в Step 3.
- **Q4. Reproducible install sequence — Windows-only или
  кросс-платформенно?** Текущие entrypoints — PowerShell.
  Default — оставить Windows-first (документировать только
  Windows + PowerShell путь). Cross-platform — out of Track C
  scope. Подтвердить в Step 4.
- **Q5. Release entrypoint map — отдельный документ или
  раздел в root README?** Root README уже имеет Quickstart;
  добавление release entrypoint map'а в него рискует раздуть
  README. Default proposal — отдельный документ под
  `docs/release-handoff.md` с pointer'ом из root README.
  Решение в Step 4.
- **Q6. CHANGELOG.md обновляется ли на каждом step'е Track C?**
  Track B следовал политике «CHANGELOG обновляется один раз на
  closure трека (Step 6)». Track C по симметрии может следовать
  той же политике; default — да, CHANGELOG обновляется только в
  Step 6 закрытия Track C. Подтвердить в Step 5.

## Связь с Phase 6 / Track A / Track B

- **Phase 6 / Step 3** ship'нул `run_install_fast_path` в
  `apps/platform/onec_platform/installer.py`. Track B / Step 3
  обернул его в `scripts/release/install.ps1`. **Track C / Step 2
  поверх этого не пишет новый installer**; он расширяет
  release-facing layout (verify-release, prepare-handoff если
  нужны), не дублируя existing install-логику.
- **Track A** ship'нул binary-backed write path и reference-stand
  round-trip evidence. Track C **не** трогает write-server,
  runbook Track A'я, или execution-core. Honest constraint
  «multi-version 1С coverage отсутствует» Track C просто
  фиксирует в release-handoff документе.
- **Track B** ship'нул git baseline + install wrapper + launch
  umbrella + README quickstart. Track C **не** дублирует это; он
  достраивает release-facing layer поверх Track B baseline'а,
  закрывая разрыв «удобно отдать другому человеку».

## Что Track C **не делает** «глубоким индустриальным продуктом» после closure (honest constraints)

- **Operator credentials остаются out-of-band.** Track C не
  вводит secrets-management; cleartext credentials по-прежнему
  оператор хранит у себя, не в config-файле в repo. Это могло
  бы быть отдельным **operator credentials hardening track**'ом
  после Track C.
- **Multi-version 1С matrix не пройдена.** Track C не запускает
  `1cv8.exe` вообще; multi-version evidence — отдельный track.
- **Production-grade MCP transport отсутствует.** Local-dev
  launcher остаётся local-dev launcher'ом; authentication /
  authorisation / supervision — отдельные track'и.
- **GUI installer / `.msi` / `.deb` / signed distribution** —
  не делается.
- **Web-UI / dashboard frontend** — не делается.
- **Полный enterprise super-set** не открывается.
- **Multi-instance HA** — не делается.
- **Полная rollback/delete-вселенная** — не покрывается.
- **Полный AST-парсер XML/BSL** — не пишется.
- **Hot reload / OS-level service supervision** — не делается.

Эти ограничения — явные honest constraints, **не** скрытые
гэпы. Closure Track C означает «продукт удобно передать
другому человеку как packaged unit», **не** «продукт готов в
prod».

## Структура шагов

См. `track-c-packaging-installer-delivery-step-map.md`. Шесть
шагов. Step 1 — этот planning document; Steps 2–5 — practical
delivery scaffolding работа; Step 6 — final integration /
closure pass.

## Что **не** входит в Track C (повтор для ясности)

Track C **не** закрывает: enterprise super-set, web-UI,
полный AST-парсер, полную metadata-вселенную, полную
rollback/delete-вселенную, production-grade MCP transport,
multi-version matrix в полном объёме, GUI installer wizard,
signed binary distribution, packaging для package managers
(PyPI / Chocolatey / winget / apt), systemd / Windows Service
registration, hot reload, web-UI / dashboard frontend, новые
MCP tools, production code rewrite. Эти направления остаются
**другими** parallel track'ами после Track A / Track B / Track C.
