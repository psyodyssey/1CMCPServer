# Parallel Track C — Packaging & Installer Delivery Step Map

Стартовая карта **Parallel Track C — Packaging & Installer
Delivery**. Шесть шагов. Карта ведёт продукт от закрытого
Track B (productization & delivery polish: git baseline +
install wrapper + launch umbrella + README quickstart) к
**доведению до состояния, в котором проект удобно передать
другому человеку как packaged unit**.

Это **не** новая фаза. Это **post-Track-B packaging &
installer delivery track**, открытый именно после честного
закрытия Track B на Step 6 final integration pass'е. Здесь
нет ни нового MCP tool surface, ни нового execution-core
slice'а, ни нового enterprise-track'а — здесь точечное
доведение существующего продукта до удобного release / handoff
состояния.

Каждый шаг описан в едином формате:

- **Цель** — что именно должно стать правдой по результату
  шага.
- **Что меняем** — какие подсистемы / документы / артефакты
  меняются. Step 1 — документационный (никакого кода).
  Шаги 2–6 могут писать scripts и docs, но **не** правят
  production code (`apps/*/src/**/*.py`,
  `packages/*/src/**/*.py`) — единственное допустимое
  минимальное касание production-area это `pyproject.toml`
  в Step 3, и только если без этого Q3 plan'а буквально
  недостижим.
- **Затронутые зоны** — границы шага в репозитории.
- **Результат** — какой именно критерий приёмки трека шаг
  закрывает (полностью или частично) и что меняется в
  registries (default — ничего).

Логика трека: **сначала контракт трека и открытые вопросы**
(Step 1), затем **release-facing scripts/release/ layout
становится полноценным delivery layer'ом** (Step 2), затем
**packaging-facing install flow честный**
(Step 3, включая `pyproject.toml`-honest review), затем
**release handoff документация для receive-side оператора**
(Step 4), затем **integration & polish** (Step 5), затем
**закрывающий integration pass и фиксация закрытия трека**
(Step 6). После Step 6 Track C закрывается; никакого Step 7
не запланировано.

Track C **не претендует** на enterprise-вселенную,
GUI installer wizard, signed binary distribution,
publication к package managers, AST-парсер, web-UI, full
version-matrix, или новый MCP tool surface. Любая правка
существующих entry points оформляется как минимальная и
локальная — по аналогии с Track B, где production-кода
вообще не трогали.

## Step 1

**Planning Packaging & Installer Delivery — documentation
entry.**

- **Цель.** Зафиксировать документационный вход в Track C:
  назначение трека, целевой результат, что закрывает трек
  и что НЕ закрывает, чем отличается от Track A и Track B,
  guardrails, явный список «что НЕ входит», 10 критериев
  приёмки, открытые вопросы Step 2+. Кода не писать.
  Никаких изменений registry. Никаких новых MCP tool'ов.
  Никакого расширения product-layer surface'а.
- **Что меняем.** Только документация:
  - `docs/architecture/track-c-packaging-installer-delivery-plan.md`
    (новый);
  - `docs/architecture/track-c-packaging-installer-delivery-step-map.md`
    (новый);
  - `README.md` — изменить раздел «Closed parallel tracks»
    (чтобы отразить, что Track C открыт как active);
    добавить секцию «Active parallel track» про Track C /
    Step 1 (planning); явно сказать, что это
    **packaging & installer delivery**, не новый
    execution-core и не enterprise track;
  - `PROJECT-STATUS.md` — текущий шаг → Parallel Track C /
    Step 1; статус `in progress`; добавить новую секцию
    про Track C / Step 1; следующий шаг → Track C /
    Step 2.
- **Затронутые зоны.** `docs/architecture/**`,
  `README.md`, `PROJECT-STATUS.md`. **Никаких** изменений
  в `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`,
  `examples/`.
- **Результат.** Документационный вход в Track C готов;
  все Steps 2–6 работают от этих контрактов и от open
  questions Step 1. Ни один code-критерий приёмки трека
  на этом шаге не закрывается. Registries: `read=15,
  write=25, intelligence=16` без изменений.

## Step 2

**Release-facing `scripts/release/` layout полишинг.**

- **Цель.** Закрыть критерий приёмки 4 (release-facing
  scripts/release/ layout честный). Расширить existing
  thin wrapper до полноценного release scaffolding слоя.
  Решить open question Q2 (pre-handoff sanity check —
  отдельный скрипт vs `launch.ps1` extension).
- **Что меняем.**
  - `scripts/release/verify-release.ps1` (новый, если Q2
    разрешается в пользу отдельного скрипта) — pre-handoff
    sanity check. Что он делает: (a) `git status` clean
    или explicit warning; (b) `git ls-files | grep
    -iE "<credential-pattern>"` пусто; (c) selfcheck
    invocation через existing `scripts/dev/launch.ps1
    selfcheck` и проверка exit code; (d) registry-list
    parse и сравнение с invariant 15/25/16; (e) проверка
    что все referenced пути из README quickstart
    физически существуют. Скрипт не правит production-
    кода, не запускает 1cv8.exe.
  - Возможно `scripts/release/_verify_runner.py` (тонкий
    Python helper, по аналогии с `_install_runner.py`),
    если без него verify-release.ps1 становится
    неудобным.
  - `scripts/release/README.md` — UPDATE (расширение, не
    переписывание): добавить секцию про verify-release,
    обновить «Файлы» список, обновить «Related».
  - **Никаких изменений** в `scripts/release/install.ps1`
    (Track B / Step 3 уже sealed). **Никакого расширения**
    `scripts/dev/launch.ps1` если Q2 разрешается в пользу
    отдельного скрипта.
- **Затронутые зоны.** `scripts/release/**` (один-два
  новых файла + UPDATE README). **Никаких** изменений в
  `apps/`, `packages/`, `scripts/dev/`,
  `pyproject.toml`, `.github/`, `examples/`, `docs/`,
  root `README.md`, `PROJECT-STATUS.md`, `CHANGELOG.md`.
- **Результат.** Закрывается критерий приёмки 3
  (pre-handoff sanity check присутствует) и часть
  критерия 4 (release-facing layout). Registries без
  изменений.

## Step 3

**Packaging-facing install flow honest review.**

- **Цель.** Закрыть критерий приёмки 5 (`pyproject.toml`
  packaging targets honest). Решить Q3 — fill `[tool.hatch.build.targets.wheel]
  packages` честным списком vs explicit honest comment'ом.
- **Что меняем.**
  - `pyproject.toml` — **минимальная допустимая правка
    production-area** в этом шаге. Один из двух honest
    путей:
    - **Path A (preferred default)**: заполнить
      `[tool.hatch.build.targets.wheel] packages` честным
      списком (все `apps/*/src/<package>` и
      `packages/*/src/<package>`). Это меняет wheel
      build с no-op на meaningful artifact без нового
      surface'а. Production-import-логика не правится.
    - **Path B (fallback)**: оставить `packages = []` с
      явным `# wheel build intentionally no-op until full
      packaging track after Track C; reason: <...>`
      комментарием.
    Окончательный выбор фиксируется в этом шаге решением
    по Q3 (operator-confirmable default — Path A).
  - `scripts/release/README.md` — короткое расширение
    раздела про packaging-side: «build a wheel via
    `python -m build` — currently produces meaningful
    artifact / intentionally no-op (link to ADR /
    explanation)».
  - **Никаких изменений** в `apps/*/src/`,
    `packages/*/src/`. Это касается только packaging
    metadata в `pyproject.toml`, не production code.
- **Затронутые зоны.** `pyproject.toml` (одно поле или
  одно поле + comment). Возможно `scripts/release/README.md`
  (короткое расширение). **Никаких** изменений в
  production code.
- **Результат.** Закрывается критерий приёмки 5.
  Registries без изменений (packaging metadata не
  затрагивает MCP tool registries). Selfcheck должен
  оставаться зелёным.

## Step 4

**Release handoff documentation.**

- **Цель.** Закрыть критерии приёмки 1 (release entrypoint
  map), 2 (reproducible install sequence checklist), 6
  (release handoff docs не врут). Решить Q1 (где живёт
  release-handoff doc), Q4 (Windows-only vs
  cross-platform), Q5 (отдельный document vs раздел в
  root README).
- **Что меняем.**
  - `docs/release-handoff.md` (новый, если Q1 разрешается
    в пользу отдельного документа — default). Содержит:
    - **Что вы получили**: короткое описание repo +
      ссылка на root README + ссылка на CHANGELOG.
    - **Системные требования**: Windows + PowerShell
      version + Python 3.11 + опциональный `1cv8.exe`,
      явно с проверочными командами на каждом пункте
      (Windows-only по Q4 default'у).
    - **Reproducible install sequence**: пошаговая
      checklist от чистой машины до зелёного
      `selfcheck_status=ok` (через
      `scripts/release/install.ps1` →
      `scripts/dev/launch.ps1 selfcheck` →
      `scripts/release/verify-release.ps1`).
    - **Release entrypoint map**: одна таблица всех
      release-facing entry points (install / verify /
      launch / handoff) с путями и кратким описанием.
    - **Что входит в handoff и что НЕ входит**: явные
      honest constraints (no GUI installer, no signed
      distribution, no production transport, no
      enterprise deployment, single-version 1С coverage,
      etc.).
    - **Куда смотреть для дальнейшего деплоя**: pointer
      map на `apps/platform/README.md`,
      `docs/operator-manual.md`, `docs/runbooks/`.
  - Возможно `docs/operator-manual.md` — точечная
    consistency правка, если release-handoff документ
    обнажит явный gap. По default'у не трогается.
  - **Никаких** изменений в `scripts/`, `apps/`,
    `packages/`, `pyproject.toml`, `.github/`,
    `examples/`, root `README.md` (root README получит
    pointer на release-handoff в Step 5).
- **Затронутые зоны.** `docs/release-handoff.md` (новый).
  Возможно точечно `docs/operator-manual.md` (только если
  обнаружится прямой gap).
- **Результат.** Закрываются критерии приёмки 1, 2, 6.
  Registries без изменений.

## Step 5

**Integration & polish.**

- **Цель.** Закрыть критерий приёмки 9 (honest
  constraints зафиксированы в README + CHANGELOG +
  release-handoff document). Точечно интегрировать новые
  Step 2–4 deliverables в существующую документацию.
- **Что меняем.**
  - `README.md` — добавить **одну** ссылку из Quickstart
    раздела «Куда идти дальше» на новый
    `docs/release-handoff.md`. Никаких других правок в
    Quickstart. Никакого переписывания root README.
  - `scripts/release/README.md` — финальная синхронизация
    с release-handoff documentом, если в Step 4
    обнаружились расхождения. По default'у — нет правок.
  - `scripts/dev/README.md` — point-update если verify-
    release script упоминается там корректным путём. По
    default'у — нет правок.
  - **Никаких** изменений в production code,
    `pyproject.toml`, `examples/`,
    `docs/runbooks/`, `docs/architecture/`,
    `docs/administrator-manual.md`,
    `docs/developer-manual.md`, `docs/runbooks.md`,
    LICENSE, SECURITY, `.gitignore`, `.github/`.
- **Затронутые зоны.** `README.md` (одна ссылка).
  Возможно точечно `scripts/release/README.md` или
  `scripts/dev/README.md`.
- **Результат.** Закрывается часть критерия 9
  (constraints зафиксированы). Закрывается критерий 10
  частично (repo по-прежнему готов к выкладке).
  Registries без изменений.

## Step 6

**Final integration pass and Track C closure.**

- **Цель.** Подтвердить, что Track C действительно
  ship'нул packaging & installer delivery slice
  end-to-end. Сделать сквозной read-only integration
  check. Зафиксировать закрытие трека.
- **Что меняем.** Кода стараемся **не** трогать —
  даже минимально. Интеграционный прогон по сценариям,
  наработанным в Step 2–5. Если прогон вскроет реальный
  блокер closure (например, `release-handoff.md`
  ссылается на несуществующий путь, или `verify-release.ps1`
  не работает на чистой checkout) — разрешается
  минимальная точечная правка по аналогии с
  Track B / Step 6.
  - **Manual closure check (read-only).**
    1. `git status` — working tree clean.
    2. `git log --oneline` — commits Track C / Steps 2–5
       присутствуют в линейной последовательности.
    3. `git ls-files | xargs grep -l <credential-pattern>`
       — ноль false-positive'ов.
    4. `python scripts/dev/selfcheck.py` через
       `bootstrap_paths.ps1` — `imports_ok = true`,
       registries `read=15 / write=25 / intelligence=16`,
       `selfcheck_status = ok`.
    5. `scripts/release/verify-release.ps1` — exit 0.
    6. `docs/release-handoff.md` прочитывается и логически
       проходит на бумаге — все ссылки указывают на
       существующие пути, все команды копируются и
       выполняются.
    7. `.github/workflows/dev-check.yml` зелёный.
  - `README.md` — раздел «Active parallel track»
    переименовывается в «Closed parallel tracks»
    (расширение существующей формулировки на третий
    track); Track C помечается как **закрыт**; список
    того, что осталось как parallel tracks ПОСЛЕ
    Track C, обновляется (operator credentials
    hardening, multi-version 1С matrix, full enterprise
    super-set, AST-парсер, web-UI, GUI installer
    ecosystem, signed distribution, production
    transport, полная rollback/delete-вселенная — всё
    это остаётся отдельными parallel tracks).
  - `PROJECT-STATUS.md` — текущий шаг помечает Track C
    закрытым; явно сказано «никаких новых треков пока
    не открыто»; следующая активная работа — открытие
    следующего parallel track'а (если решение принято
    оператором проекта).
  - `CHANGELOG.md` — обновляется одной строкой о Track C
    closure под заголовком `## 0.1.0 — initial public
    snapshot` (по симметрии с Track B / Step 6
    closure).
  - **GitHub remote push** — **не** часть Step 6.
    Operator action.
- **Затронутые зоны.** `README.md`, `PROJECT-STATUS.md`,
  `CHANGELOG.md`. Опционально точечные правки если
  closure-check вскрыл реальный блокер. Никаких
  изменений в `apps/`, `packages/`, `scripts/` (за
  исключением мелких docs fix'ов).
- **Результат.** Закрываются финальные критерии приёмки
  7, 8, 10. **Parallel Track C — Packaging & Installer
  Delivery закрыт**. Платформа достигла состояния
  «удобно передать другому человеку как packaged unit».
  Остаются только non-blocking follow-up'ы / parallel
  tracks за пределами Track C.

---

После Step 6 Track C **закрыт**. Следующая активная работа
— **не Phase 7**. Это либо открытие следующего parallel
track'а (по решению оператора проекта; recommendations:
operator credentials hardening track, multi-version 1С
matrix track), либо просто фиксация текущего состояния
платформы как достигнутого. В обоих случаях safety
guarantees Phase 1–6 + Track A + Track B + Track C
сохраняются.
