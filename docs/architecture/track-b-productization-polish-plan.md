# Parallel Track B — Productization & Delivery Polish Plan

## Назначение трека

Phase 1–6 закрыты. Parallel Track A — Full Real 1cv8-backed Write
Path — закрыт на Step 7 (final integration pass). У платформы
есть:

- `mcp-read-server` (15 tools), `mcp-write-server` (25 tools),
  `mcp-intelligence-server` (16 tools);
- `apps/platform/onec_platform` — bootstrap / installer / runtime
  layer / health dashboard / guided workflows / rollback
  assistant / real-stand smoke / enterprise foundation
  inspector;
- доказанный binary-backed write path для всех трёх ранее
  stub-backed write-tool'ов (real round-trip отработал на
  InfoBase6 в рамках Track A / Step 6);
- selfcheck зелёный, registries `read=15 / write=25 /
  intelligence=16` без drift'а;
- один operator-reproducible runbook
  (`docs/runbooks/track-a-reference-stand-round-trip.md`);
- standalone manuals (`docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks.md`).

Самый жирный незакрытый разрыв сейчас — **не execution layer**.
Execution layer Track A закрыл. Незакрыто другое: **продукт ещё
не доведён до удобного install / run / repo / release
состояния**. Конкретно:

- Папка `C:\Tools\1c-agent-platform` **не является git-репозиторием**
  (нет `.git`). Любая публикация / передача / pull-request flow —
  невозможны как факт.
- `.gitignore` — минимальный (стандартные Python-артефакты), но
  не покрывает реалии этого репозитория: артефакты
  `examples/demo-dumps/_snapshots/` (сгенерированные round-trip'ом
  Track A Step 6), `examples/demo-dumps/<env>/.audit/`, локальные
  writable config'и (если оператор их случайно положит в repo),
  `.runtime/` директории.
- Нет `LICENSE` файла. Передача / публикация без явной лицензии —
  юридически мутно.
- Нет `CHANGELOG.md`. История фаз / track'ов разбросана по
  `PROJECT-STATUS.md` (~8500 строк) и не имеет компактной формы
  «что в каком релизе».
- Нет верхнеуровневого «5-минутного quickstart'а». `README.md`
  — 730 строк, для нового читателя это документация-стена; первый
  опыт «как это вообще установить и запустить» нужно собирать из
  кусков `apps/platform/README.md` + `docs/operator-manual.md`.
- У трёх MCP-серверов **нет `__main__.py`**: запустить сервер
  локально без явного PYTHONPATH manipulation и явной import-сборки
  оператор не может. Это было явно вынесено в parallel-track'и
  после Phase 6 как «production-grade MCP transport», но честный
  **минимальный local-dev launcher** (без auth / без HTTP / без
  сервиса) — намного уже, чем full transport, и был бы вполне
  уместен здесь.
- `scripts/release/` пустая. `pyproject.toml` имеет
  `[tool.hatch.build.targets.wheel] packages = []` — wheel build
  по сути no-op.
- В корне нет `CONTRIBUTING.md`, нет `SECURITY.md`. Для
  one-author / closed репозитория это допустимо, но при выкладке
  на GitHub приходится решать ad hoc.
- `apps/platform/installer.py` — оператор-discoverable только
  через документацию (`docs/operator-manual.md`); командной
  строки `1c-agent-platform install` нет.

Этот разрыв — **не execution-core**, **не enterprise-вселенная**,
**не AST-парсер**, **не web-UI**, **не production-grade MCP
transport с auth**. Это **доведение существующего продукта до
удобного install / run / repo / release состояния**. Все safety
guarantees Phase 1–6 + Track A (`run_write_flow` единственный
mutating-путь, intelligence read-only, нет back-door write
channel'а, fail-closed по умолчанию, audit append-only, нет
`shell=True`) **сохраняются без изменений**.

Это **не** новый MCP-surface sprint и **не** новый execution-core
sprint. Это **post-Track-A productization track** на узкую зону
delivery / package / repo polish.

Назвать это «Phase 7» или новой «Phase» было бы нечестно: ни
одной новой execution-фазы не запланировано. Этот трек —
**Parallel Track B — Productization & Delivery Polish** —
открывается как parallel-track после закрытой Phase 6 + Track A.

## Целевой результат

К моменту закрытия Track B платформа должна выдерживать honest
operator-facing нарратив:

1. **Repo is a git repository.** В корне есть `.git/`, есть
   первый осмысленный initial commit с фиксацией текущего
   честного состояния (Phase 1–6 закрыты, Track A закрыт).
   Ветка `main` (или `master` — выбор оператора) существует.
   Никаких force push'ей, никаких rewrite'ов истории. **Push
   на GitHub remote — отдельный operator step**, не часть
   трека: Track B готовит репозиторий *к* выкладке, а не
   делает выкладку.
2. **Repo hygiene честный.** `.gitignore` покрывает реальные
   артефакты этого проекта (snapshot trees, audit-директории,
   локальные writable-конфиги, runtime state, IDE-мусор); ни
   один cleartext credential ни одной dev-итерации не попадает
   в commit history. Есть `LICENSE` (выбор лицензии — operator
   call), есть минимальный `CHANGELOG.md` с записью «0.1.0 —
   initial public release» и кратким перечнем «что закрыто к
   моменту первого релиза».
3. **Verifiable install fast path operator-discoverable.**
   Существующий `apps/platform/onec_platform.installer.run_install_fast_path`
   имеет один operator-friendly entry-point (минимальный
   PowerShell wrapper в `scripts/release/` или `scripts/dev/`,
   либо documented one-liner в `README.md` quickstart), и он
   воспроизводимо ставит платформу в `<work_dir>` за ≤ 5
   шагов на чистой машине Windows. Никакого нового
   installer-ecosystem'а, никакого `.msi`, никакого signed
   binary distribution.
4. **Local launch ergonomic.** У трёх MCP-серверов и у
   `onec_platform` есть способ запустить их локально одной
   командой без ручного `PYTHONPATH` бубна. Минимум:
   запуск-скрипты в `scripts/dev/` или один-единственный
   `__main__.py` в каждом server-package с явным «это
   local-dev launcher, не production transport»
   docstring'ом. **Production-grade MCP transport (HTTP /
   stdio с auth, supervision) — out of Track B**; здесь —
   только honest dev-launch.
5. **README.md operator-friendly.** Верх README имеет
   «5-минутный quickstart»: что это, какие требования
   (Windows + Python 3.11 + 1cv8.exe path), как установить,
   как проверить, что всё ок. После quickstart'а — ссылки на
   углублённые манualы. Нынешняя 730-строчная документация
   остаётся, но превращается из стены текста в
   structured surface: top-level summary → quickstart →
   detailed phases → runbooks. Никаких новых документов
   ради документов.
6. **Repo готов к выкладке на GitHub.** Все honest constraints
   (operator credentials out-of-band, single-version smoke,
   no production transport, no GUI, no enterprise super-set)
   зафиксированы в README + LICENSE + CHANGELOG, и ничто из
   репозитория не выглядит как «брошенный workspace».
   `.github/workflows/dev-check.yml` продолжает быть зелёным.
   Никаких новых workflow'ов ради workflow'ов.

## Что Track B **не** закрывает (явно)

- **Production-grade MCP transport** — HTTP/stdio с
  authentication / authorization, multi-tenant, federated
  audit. Out of scope.
- **Полный installer ecosystem** — `.msi` / `.deb` / GUI
  wizard / signed binary distribution / packaging service.
  Out of scope. Track B ship'ит только operator-friendly
  shortcut над существующим `run_install_fast_path`.
- **Web-UI / dashboard frontend / workflow runner UI** — out
  of scope.
- **Полный enterprise super-set** (SSO/RBAC, multi-tenant,
  secrets vault, federated audit storage, policy-as-code DSL,
  multi-instance HA) — out of scope.
- **Hot reload / OS-level service supervision** (Windows
  Service / systemd unit, automatic-restart-supervisor) —
  out of scope.
- **Multi-version matrix smoke** на всех 1С версиях и
  стендах — out of scope. Track B не запускает 1cv8.exe
  вообще; `1cv8`-evidence уже зафиксировано Track A.
- **Полный AST-парсер XML/BSL** — out of scope.
- **Полная rollback/delete-вселенная** — out of scope.
- **Новые MCP tools** — out of scope. Registry'ы остаются
  `read=15 / write=25 / intelligence=16` без drift'а.
- **Production code rewrite** — out of scope. Track B
  целевым образом не правит `apps/*/src/**/*.py` /
  `packages/*/src/**/*.py`. Минимальные исключения,
  если они понадобятся (например, добавление одного
  `__main__.py` в server-package'ы), оговариваются в
  step-map'е и допускаются только если без этого Track B
  buy-and-large недостижим.
- **GitHub remote push** — operator action, не часть
  трека. Track B доводит до состояния «репозиторий готов
  к выкладке»; нажатие `git remote add` + `git push` —
  отдельный step, который выполняет оператор.
- **Многосторонний end-to-end на матрице 1С версий и
  стендов** — остаётся parallel track'ом после Track B.

## Guardrails

- **Никакого расширения MCP surface'а.** read=15 /
  write=25 / intelligence=16 — инвариант. Любое нарушение
  — failed shape check.
- **Никакого back-door write channel'а.** Product layer
  по-прежнему не пишет ни в инфобазу, ни в audit, ни в
  snapshot tree вне `run_write_flow`. Track B этим тоже
  не занимается.
- **Никаких `shell=True`.** Если в трек попадёт subprocess
  invocation (например, `git init` или `python -m`), он
  идёт через `subprocess.run` с argv-list или через
  `onec_process_runner`-стиль argv.
- **Никаких credentials в repo.** Никакие cleartext
  пароли / токены / ключи / `1Cv8.1CD`-файлы не
  коммитятся. `.gitignore` ловит local writable config'и
  по содержательному pattern'у.
- **Никаких новых runbook'ов ради новых runbook'ов.**
  Существующие manualы остаются как есть, если только не
  всплывает реальный gap.
- **Не претендуем на enterprise-ready / production-ready
  статус.** Closure Track B означает буквально «продукт
  удобно установить и запустить, репо готов к выкладке»,
  не «готовы в prod».

## Критерии приёмки

1. **Repo — git-репозиторий.** `git status` в корне работает;
   `git log` показывает хотя бы один осмысленный commit с
   фиксацией текущего состояния. История чистая (никаких
   force push'ей, rewrite'ов).
2. **`.gitignore` покрывает реальные артефакты.** Snapshot
   trees, audit-директории, локальные writable-конфиги
   (`*-writable.config.json` и аналоги), runtime state
   (`.runtime/`), IDE-мусор, OS-мусор, Python-артефакты —
   всё в ignore. Manual review подтверждает, что ни один
   cleartext credential не висит в working tree до commit'а.
3. **`LICENSE` присутствует.** Выбор лицензии — operator
   call (рекомендации могут быть даны в Step 2). Файл
   читается стандартными license-detector'ами.
4. **`CHANGELOG.md` присутствует.** Минимум одна запись
   «0.1.0 — initial public release» с честным перечнем
   закрытого (Phase 1–6 + Track A).
5. **Quickstart в README.md.** Верх README имеет блок
   «как установить за 5 минут», после которого идут
   ссылки на углублённые манualы. Размер quickstart'а —
   compact (не больше 50 строк).
6. **Operator-friendly install/launch.** На чистой машине
   Windows с Python 3.11 оператор по quickstart'у может:
   (a) клонировать repo, (b) выполнить bootstrap, (c)
   запустить selfcheck, (d) увидеть `selfcheck_status =
   ok`. Это покрывается одним из:
   - PowerShell wrapper в `scripts/dev/` или `scripts/release/`,
   - documented one-liner в README,
   - `__main__.py` в server-package'ах (если step-map это
     допустит).
7. **Selfcheck остаётся зелёным.** `imports_ok = true`,
   registries без drift'а, `selfcheck_status = ok`.
   `.github/workflows/dev-check.yml` зелёный.
8. **Никаких production-правок core.** `apps/mcp-*/src/**/*.py`,
   `packages/*/src/**/*.py`, `apps/platform/src/onec_platform/*.py`
   (за исключением минимального `__main__.py`, если step-map
   это допустит) — без изменений.
9. **Honest constraints зафиксированы.** README прямо
   называет, что Track B **не** закрывает (см. список
   выше); CHANGELOG это повторяет компактно.
10. **Repo готов к выкладке.** Manual visual review: ни
    одного credential в commit history, ни одного
    «брошенного» артефакта вроде `*.bak` / `Thumbs.db` /
    `.DS_Store`, README читается осмысленно, LICENSE на
    месте, CI зелёный, нет TODO-pollution.

## Открытые вопросы (resolve в Step 2+)

- **Q1. Лицензия.** Apache-2.0, MIT, BSD-3-Clause, или
  proprietary с операторским disclaim'ом? Решение оператора;
  Step 2 предложит default (Apache-2.0 как baseline для
  open-source-style передачи) и попросит подтверждения.
- **Q2. Главная ветка — `main` или `master`?** Default
  GitHub'а сейчас `main`; PROJECT-STATUS уже использует
  лексику в духе «ветка master / main». Оператор выбирает
  один раз в Step 2.
- **Q3. Какой scope `__main__.py`'ев у MCP-серверов.**
  Полный CLI с argparse и subcommand'ами — нет, это
  parallel track. Минимальный «`python -m mcp_read_server`
  печатает registered tools list и выходит» — допустим
  как honest local-dev launcher. Решение в Step 4.
- **Q4. `__main__.py` для `onec_platform`?** Аналогичный
  вопрос. Минимум — печать `selfcheck` summary; это
  существенно перекрывает текущий ритуал
  `python scripts/dev/selfcheck.py`. Решение в Step 4.
- **Q5. `CONTRIBUTING.md` и `SECURITY.md` — нужны ли?**
  Для one-author / closed репозитория — нет; для GitHub
  выкладки — желательно. Default Step 2 — пропустить
  CONTRIBUTING (просто README с парой строк «PR welcome /
  see issue tracker»), но создать минимальный
  `SECURITY.md` со строкой «report security issues
  privately to <owner>».
- **Q6. Что делать с `examples/demo-dumps/_snapshots/`?**
  В нынешнем состоянии там 7 dump-snapshot'ов от Track A
  Step 6 round-trip'а; они большие и не нужны другим
  читателям. Default — добавить `examples/demo-dumps/`
  в `.gitignore` и оставить **только** README в
  examples/, объясняющий назначение. Окончательное
  решение в Step 2.
- **Q7. Версия проекта в `pyproject.toml`.** Сейчас
  `0.1.0`. После closure Track B остаётся `0.1.0` (это
  и есть «initial public release»), или bump'нуть в
  `0.2.0` чтобы отметить productization layer? Default —
  оставить `0.1.0` и зафиксировать его как первый
  публичный release; bump происходит при следующем
  parallel track'е.

## Связь с Phase 6 / Track A

- **Phase 6 (Industrialization & Completion Track) ship'нул
  первый install fast path** (`run_install_fast_path` в
  `apps/platform/onec_platform/installer.py`). Track B
  поверх этого не пишет новый installer; он делает
  существующий **discoverable** (operator-friendly
  shortcut + quickstart в README). Phase 6 / Step 7
  ship'нул standalone manuals; Track B не дублирует их,
  а добавляет один верхнеуровневый entry в README.
- **Track A ship'нул** binary-backed write path и
  reference-stand round-trip evidence. Track B не трогает
  ни write-server, ни runbook Track A'я; он только
  обеспечивает, чтобы repo был git-репозиторием и был
  выкладываем.

## Что Track B **не делает** «готовым индустриальным продуктом» после closure (honest constraints)

- **Operator credentials остаются out-of-band.** Track B
  не вводит secrets-management; cleartext credentials по
  прежнему оператор хранит у себя, не в config-файле в
  repo.
- **Multi-version matrix не пройдена.** Track B не
  запускает 1cv8.exe вообще; multi-version evidence —
  отдельный track.
- **Production-grade MCP transport отсутствует.**
  Local-dev launcher — это local-dev launcher;
  authentication / authorization / supervision — отдельные
  track'и.
- **Packaging ecosystem не построен.** Wheel-target в
  `pyproject.toml` после Track B может стать честно
  заполненным, но `.msi` / `.deb` / signed distribution —
  отдельные track'и.
- **GUI / web-UI / dashboard frontend нет.** Не входит.
- **Полный enterprise super-set не открыт.** Не входит.
- **Multi-instance HA нет.** Не входит.

Эти ограничения — явные honest constraints, **не** скрытые
гэпы. Closure Track B означает «продукт удобно установить и
запустить локально, репо готов к выкладке на GitHub»,
**не** «продукт готов к prod».

## Структура шагов

См. `track-b-productization-polish-step-map.md`. Шесть
шагов. Step 1 — этот planning document; Steps 2–5 —
practical productization работа; Step 6 — final
integration / closure pass.

## Что **не** входит в Track B (повтор для ясности)

Track B **не** закрывает: enterprise super-set, web-UI,
полный AST-парсер, полную metadata-вселенную, полную
rollback/delete-вселенную, production-grade MCP transport,
полный packaging ecosystem, multi-version matrix в полном
объёме, hot reload, OS service supervision. Эти направления
остаются **другими** parallel track'ами после
Phase 6 / Track A / Track B.
