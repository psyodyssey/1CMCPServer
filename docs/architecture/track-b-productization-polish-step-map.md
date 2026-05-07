# Parallel Track B — Productization & Delivery Polish Step Map

Стартовая карта **Parallel Track B — Productization & Delivery
Polish**. Шесть шагов. Карта ведёт продукт от закрытого
Track A (где execution layer real-write полностью доказан, но
репозиторий ещё не git-репозиторий и не доведён до
выкладочного состояния) к **operator-friendly install / launch /
release-ready** состоянию.

Это **не** новая фаза. Это **post-Track-A productization
track**, открытый именно после честного закрытия Track A на
Step 7 final integration pass'е. Здесь нет ни нового MCP
tool surface, ни нового execution-core slice'а, ни нового
enterprise-track'а — здесь точечное доведение существующего
продукта до удобного install / run / repo / release состояния.

Каждый шаг описан в едином формате:

- **Цель** — что именно должно стать правдой по результату
  шага.
- **Что меняем** — какие подсистемы / документы / артефакты
  меняются. Step 1 — документационный (никакого кода).
  Шаги 2–6 могут писать код, но строго в рамках уже
  наработанной архитектуры Phase 1–6 + Track A и без
  размывания её safety guarantees. Production code (под
  `apps/*/src/**/*.py`, `packages/*/src/**/*.py`) трогаем
  только в одном случае — Step 4 минимальный `__main__.py`
  для local-dev launcher'ов, и только если без этого Step 4
  buy-and-large недостижим.
- **Затронутые зоны** — границы шага в репозитории.
- **Результат** — какой именно критерий приёмки трека шаг
  закрывает (полностью или частично) и что меняется в
  registries (default — ничего).

Логика трека: **сначала контракт трека и открытые вопросы**
(Step 1), затем **репо превращается в git-репозиторий с
честной hygiene и legal layer'ом** (Step 2), затем
**install fast path делается operator-discoverable**
(Step 3), затем **local launch ergonomics** (Step 4), затем
**README / docs polish** (Step 5), затем **закрывающий
integration pass + GitHub-ready закрытие трека** (Step 6).
После Step 6 Track B закрывается; никакого Step 7 не
запланировано.

Track B **не претендует** на enterprise-вселенную, AST-парсер,
web-UI, полный packaging ecosystem, full version-matrix, или
новый MCP tool surface. Любая правка существующих серверов
оформляется как минимальная и локальная — по аналогии с
Track A / Step 7 (где правок production-кода вообще не
понадобилось).

## Step 1

**Planning Productization & Delivery Polish — documentation
entry.**

- **Цель.** Зафиксировать документационный вход в Track B:
  назначение трека, целевой результат, что закрывает трек
  и что НЕ закрывает, чем отличается от Phase 6 и Track A,
  guardrails, явный список «что НЕ входит», 10 критериев
  приёмки, открытые вопросы Step 2+. Кода не писать.
  Никаких изменений registry. Никаких новых MCP tool'ов.
  Никакого расширения product-layer surface'а.
- **Что меняем.** Только документация:
  - `docs/architecture/track-b-productization-polish-plan.md`
    (новый);
  - `docs/architecture/track-b-productization-polish-step-map.md`
    (новый);
  - корневой `README.md` — заменить раздел «Closed parallel
    track» на «Closed parallel tracks» (Track A) +
    «Active parallel track» (Track B); явно сказать, что
    это productization, не execution-core и не enterprise;
  - `PROJECT-STATUS.md` — текущий шаг → Parallel Track B /
    Step 1; статус `in progress`; полный detail block;
    следующий шаг → Track B / Step 2.
- **Затронутые зоны.** `docs/architecture/**`,
  `README.md`, `PROJECT-STATUS.md`. **Никаких** изменений
  в `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`.
- **Результат.** Документационный вход в Track B готов;
  все Steps 2–6 работают от этих контрактов и от open
  questions Step 1. Ни один code-критерий приёмки трека
  на этом шаге не закрывается — Step 1 только открывает
  трек. Registries: `read=15, write=25, intelligence=16`
  без изменений.

## Step 2

**Repo hygiene + legal layer.**

- **Цель.** Закрыть критерии приёмки 1, 2, 3, 4. Превратить
  рабочую директорию в git-репозиторий, выровнять `.gitignore`
  под реалии проекта, добавить `LICENSE` и `CHANGELOG.md`,
  сделать первый осмысленный commit. Решить открытые
  вопросы Q1 (лицензия), Q2 (`main` vs `master`), Q5
  (CONTRIBUTING / SECURITY), Q6 (`examples/demo-dumps/`),
  Q7 (версия в `pyproject.toml`).
- **Что меняем.**
  - `git init` в корне `C:\Tools\1c-agent-platform`. Имя
    основной ветки выбирается в этом шаге (Q2). **Никакого
    push'а на remote** — это operator action, не часть
    шага.
  - `.gitignore` расширяется до:
    - `examples/demo-dumps/_snapshots/` (heavy
      A.2/A.4/A.5 артефакты Track A Step 6);
    - `examples/demo-dumps/**/.audit/` (audit-директории);
    - `examples/demo-infobase/_work/` (bootstrap work
      directories);
    - `**/.runtime/` (runtime state директории Phase 6 /
      Step 6);
    - `*-writable.config.json` и аналоги (local-only
      configs с cleartext credentials);
    - `*.bak`, `*~` (редакторский мусор).
  - `LICENSE` (root) — содержимое определяется решением
    Q1; default proposal — Apache-2.0 baseline. Файл
    создаётся ровно один; копии лицензии в подпапках не
    делаются.
  - `CHANGELOG.md` (root) — компактный, с одной записью
    `## 0.1.0 — initial public release` и кратким honest
    перечнем закрытого (Phase 1–6, Track A, registries
    `read=15 / write=25 / intelligence=16`, list of
    honest constraints).
  - `SECURITY.md` (root) — минимальный (по Q5 default'у),
    одна-две строки про reporting flow.
  - **Не создаём** `CONTRIBUTING.md` — оно становится
    нужным только при public PR-flow; пока репозиторий
    не на GitHub, это premature.
  - **Manual hygiene check** (read-only) — пройти
    `git status` и удостовериться, что ни один cleartext
    credential, ни один `1Cv8.1CD`, ни один большой
    snapshot tree не находится в working tree после
    обновления `.gitignore`.
  - **Первый commit** делается **только после** того, как
    оператор подтвердил `git status` чистым от sensitive
    содержимого. Это явный operator gate в шаге.
  - `pyproject.toml` — Q7 разрешается, version по default'у
    остаётся `0.1.0`. Если Q7 отвечает «bump» — bump'аем
    до `0.2.0` в этом шаге.
- **Затронутые зоны.** Корень репозитория:
  `.git/` (новый), `.gitignore` (правится), `LICENSE`
  (новый), `CHANGELOG.md` (новый), `SECURITY.md` (новый),
  возможно `pyproject.toml` (одна строка version).
  **Никаких** изменений в `apps/`, `packages/`,
  `scripts/`, `docs/`, `examples/`, `.github/`,
  `.editorconfig`, `.python-version`.
- **Результат.** Закрываются критерии приёмки 1 (repo —
  git-репозиторий), 2 (`.gitignore` покрывает реальные
  артефакты), 3 (`LICENSE` присутствует), 4
  (`CHANGELOG.md` присутствует). Q1, Q2, Q5, Q6, Q7 —
  resolved. Registries без изменений. Selfcheck должен
  оставаться зелёным; если что-то сломалось, шаг **не**
  закрывается.

## Step 3

**Install fast path operator-discoverable.**

- **Цель.** Закрыть часть критерия приёмки 6
  (operator-friendly install / launch). Существующий
  `apps/platform/onec_platform.installer.run_install_fast_path`
  должен быть discoverable за один взгляд в README, и
  иметь один operator-friendly entry-point (PowerShell
  wrapper или documented one-liner) с воспроизводимым
  поведением.
- **Что меняем.**
  - **Production-кода не правим.** `installer.py` не
    трогается. Track B не переписывает installer'ы.
  - `scripts/release/install.ps1` (новый) — тонкий
    PowerShell wrapper: принимает `-WorkDir <path>`,
    рендерит минимальный `data` dict в одну атомарную
    JSON-инвокацию `run_install_fast_path` через
    `python -c` или через выделенный helper-скрипт.
    **Никакого state'а в самом wrapper'е**, никакого
    bypass'а existing safety guarantees. Wrapper —
    documented one-liner over Phase 6 install fast path.
  - `scripts/release/README.md` (новый) — короткий: что
    делает каждый release-скрипт, какие он принимает
    параметры, что проверять после.
  - В корневом `README.md` Step 3 **пока** ничего не
    меняет (это работа Step 5). Здесь только готовится
    artifact, на который Step 5 ссылается.
  - **Manual smoke** (без 1cv8.exe): запустить
    `scripts/release/install.ps1` против чистого
    temp-каталога, убедиться что он honestly создаёт
    product-config + проходит round-trip
    `bootstrap_product_from_json_file`. Это уже покрыто
    `installer.py` логикой; шаг просто verifies wrapper.
- **Затронутые зоны.** `scripts/release/**` (новые
  файлы); опционально один маленький helper-скрипт.
  **Никаких** изменений в `apps/`, `packages/`,
  `docs/`, `examples/`, `.github/`, `pyproject.toml`,
  `.gitignore`. Никаких изменений production-кода.
- **Результат.** Закрывается часть критерия приёмки 6
  (operator получает воспроизводимый install entry-point).
  Registries без изменений. Selfcheck зелёный.

## Step 4

**Local launch ergonomics.**

- **Цель.** Закрыть остаток критерия приёмки 6 (запустить
  серверы / `selfcheck` локально без ручного PYTHONPATH
  бубна). Решить Q3, Q4 (scope `__main__.py`'ев).
- **Что меняем.** Здесь **разрешена минимальная
  production-правка** — и только она:
  - **Один** `__main__.py` на каждый из четырёх
    package'ей, **только если** без этого Step 4
    buy-and-large недостижим:
    - `apps/mcp-read-server/src/mcp_read_server/__main__.py`
      — печатает sorted list registered tools и выходит
      `0`; **не** запускает MCP-server-loop, **не**
      открывает порт, **не** делает auth. Docstring явно
      говорит: «local-dev launcher; production-grade MCP
      transport — out of Track B».
    - `apps/mcp-write-server/src/mcp_write_server/__main__.py`
      — то же самое.
    - `apps/mcp-intelligence-server/src/mcp_intelligence_server/__main__.py`
      — то же самое.
    - `apps/platform/src/onec_platform/__main__.py` —
      печатает `selfcheck`-style summary
      (`imports_ok`, `registered tools`,
      `selfcheck_status`) и выходит. Эквивалент
      `python scripts/dev/selfcheck.py`, но через
      package interface.
  - **Альтернатива (preferred если возможно).** Если
    существующий `python scripts/dev/selfcheck.py` +
    `bootstrap_paths.ps1` уже даёт оператору всё
    необходимое (а это де-факто так), Step 4 может
    закрыться **без** добавления `__main__.py`'ев —
    добавив один общий `scripts/dev/launch.ps1` (тонкий
    composer над `bootstrap_paths.ps1`), который тонко
    оборачивает запуск selfcheck'а. Решение
    («`__main__.py`'и или скрипт») принимается в начале
    шага по open question Q3/Q4 — и **по умолчанию
    выбирается scripts-only вариант** как менее
    инвазивный.
  - **Никакого CLI с argparse, subcommand'ами,
    daemon-mode'ом**. Track B не строит CLI ecosystem.
- **Затронутые зоны.** Если выбран scripts-only
  вариант — `scripts/dev/**` (один новый wrapper),
  никакого production-кода вообще. Если выбран
  `__main__.py` вариант — четыре файла под
  `apps/*/src/**/__main__.py` плюс возможный
  scripts wrapper, и это единственное допустимое
  касание production-кода во всём треке. Registries
  не меняются.
- **Результат.** Закрывается остаток критерия приёмки
  6. Если был выбран `__main__.py` вариант —
  registries формально остаются те же
  (`__main__.py` не считается tool'ом), но `imports_ok`
  и selfcheck должны остаться зелёными. Если какой-то
  selfcheck сломался от добавления `__main__.py` — шаг
  откатывается.

## Step 5

**README + docs polish.**

- **Цель.** Закрыть критерий приёмки 5 (5-минутный
  quickstart в README), часть критерия 9 (honest
  constraints зафиксированы). README превращается из
  730-строчной стены в structured surface с явным
  top-level entry'ем для нового читателя.
- **Что меняем.**
  - `README.md` (root) — добавляется новый верхний
    раздел `## Quickstart` сразу после `## Идея` /
    `## Архитектура`. Содержание:
    - системные требования (Windows + Python 3.11 +
      опциональный 1cv8.exe);
    - как клонировать repo (одна команда);
    - как поставить базовые зависимости (одна команда,
      ссылается на `scripts/release/install.ps1` или
      эквивалент из Step 3);
    - как запустить selfcheck (одна команда —
      `scripts/dev/run_dev_check.ps1` или эквивалент
      из Step 4);
    - что должно быть видно при успехе (`imports_ok =
      true`, registries без drift'а, `selfcheck_status
      = ok`);
    - короткая ссылочная карта: «глубже — см.
      `apps/platform/README.md`, `docs/operator-manual.md`,
      `docs/runbooks.md`, `PROJECT-STATUS.md`».
    - размер блока — compact, не больше 50 строк.
  - Существующий контент README **не** удаляется и
    **не** реструктурируется агрессивно. Quickstart
    добавляется в начало; всё остальное остаётся ниже.
  - В разделе «Closed parallel tracks» (после Track A
    closure update'а в Step 1) добавляется **одна
    строка** про active Track B — без дублирования
    track-b plan/step-map.
  - `apps/platform/README.md`, `apps/mcp-write-server/README.md`,
    `apps/mcp-read-server/README.md`,
    `apps/mcp-intelligence-server/README.md` —
    проходим **только** на consistency: одна-две правки
    для устранения явных рассинхронов с фактическим
    кодом, если они есть. Никаких полных переписываний.
  - `docs/operator-manual.md`, `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks.md` —
    **не** трогаются. Они уже честные после Phase 6 /
    Step 7 + Track A.
- **Затронутые зоны.** `README.md` (root, добавление
  блока), опционально точечные правки в
  `apps/*/README.md`. Никаких изменений в `apps/*/src/`,
  `packages/`, `scripts/`, `docs/architecture/`,
  `pyproject.toml`, `.github/`, `.gitignore`.
- **Результат.** Закрывается критерий приёмки 5.
  Закрывается часть критерия 9 (constraints в README).
  Registries без изменений.

## Step 6

**Final integration pass and Track B closure.**

- **Цель.** Подтвердить, что Track B действительно
  ship'нул productization slice end-to-end. Сделать
  сквозной интеграционный read-only прогон. Зафиксировать
  закрытие трека.
- **Что меняем.** Кода стараемся **не** трогать —
  даже минимально. Интеграционный прогон по сценариям,
  наработанным в Step 2–5. Если прогон вскроет реальный
  блокер closure (например, README ссылается на
  несуществующий путь, или `.gitignore` пропустил
  очевидный артефакт) — разрешается минимальная точечная
  правка по аналогии с Track A / Step 7.
  - **Manual closure check (read-only).**
    1. `git status` — working tree чистый или содержит
       только намеренные in-progress правки трека.
    2. `git log --oneline` — есть осмысленные commit'ы
       Steps 2–5.
    3. `git ls-files | xargs grep -l <secret-pattern>`
       — ноль false-positive'ов. Никаких cleartext
       credentials в indexed файлах.
    4. `python scripts/dev/selfcheck.py` (через
       `bootstrap_paths.ps1`) — `imports_ok = true`,
       registries `read=15 / write=25 / intelligence=16`,
       `selfcheck_status = ok`.
    5. README quickstart прочитывается и логически
       проходит на бумаге — все ссылки указывают на
       существующие пути, все команды копируются и
       выполняются.
    6. `.github/workflows/dev-check.yml` зелёный
       локально (по факту — как только репо станет
       git'овым и попадёт на GitHub, CI проверит сам;
       до выкладки — проверка локальная).
  - `README.md` — раздел «Active parallel track»
    переименовывается в «Closed parallel tracks»
    (множественное число); Track B помечается как
    **закрыт**; список того, что осталось как parallel
    tracks ПОСЛЕ Track B, обновляется (полный
    enterprise super-set, AST-парсер, web-UI, full
    packaging ecosystem, multi-version matrix,
    production-grade transport, полная rollback/delete-
    вселенная — всё это остаётся отдельными parallel
    tracks).
  - `PROJECT-STATUS.md` — текущий шаг помечает Track B
    закрытым; явно сказано «никаких новых треков пока
    не открыто»; следующая активная работа — открытие
    следующего parallel track'а (если решение принято
    оператором проекта); Phase 7 как фаза по-прежнему
    не запланирована.
  - `CHANGELOG.md` — обновляется одной строкой о Track B
    closure под заголовком `## 0.1.0 — initial public
    release`.
  - **GitHub remote push** — **не** часть Step 6. По
    closure'у Step 6 операторский gate: оператор
    решает, делать ли `git remote add origin ...` +
    `git push -u origin main` сам. Track B
    предоставляет «repo готов к выкладке», не «repo
    выложен».
- **Затронутые зоны.** `README.md`,
  `PROJECT-STATUS.md`, `CHANGELOG.md`. Опционально
  точечные правки если closure-check вскрыл реальный
  блокер. Никаких изменений в `apps/`, `packages/`,
  `scripts/` (за исключением мелких docs fix'ов).
- **Результат.** Закрываются финальные критерии приёмки
  7, 8, 9, 10. **Parallel Track B — Productization &
  Delivery Polish закрыт**. Платформа достигла
  operator-friendly install / launch / release-ready
  состояния. Остаются только non-blocking follow-up'ы /
  parallel tracks за пределами Track B.

---

После Step 6 Track B **закрыт**. Следующая активная работа —
**не Phase 7**. Это либо открытие следующего parallel track'а
(по решению оператора проекта), либо просто фиксация текущего
состояния платформы как достигнутого. В обоих случаях safety
guarantees Phase 1–6 + Track A + Track B сохраняются.
