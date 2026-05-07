# Phase 6 Step Map

Стартовая карта Phase 6 — Industrialization & Completion
Track. Восемь шагов. Карта ведёт продукт от закрытого
Phase 5 product-layer контура к **finished /
deployable** состоянию на reference stand'е.

Каждый шаг описан в едином формате:

- **Цель** — что именно должно стать правдой по
  результату шага.
- **Что меняем** — какие подсистемы / документы /
  артефакты меняются. Step 1 — документационный
  (никакого кода). Шаги 2–8 могут писать код, но
  строго в рамках уже наработанной архитектуры
  Phase 1–5 и без размывания её safety guarantees.
- **Затронутые зоны** — границы шага в репозитории.
- **Результат** — какое условие из критериев приёмки
  Phase 6 шаг закрывает (полностью или частично).

Логика: **сначала контракт фазы** (Step 1), затем
**контракт реальной 1cv8 интеграции** (Step 2), затем
**short install/setup путь** (Step 3), затем
**исполнимый rollback** (Step 4), затем **точечный
metadata добор + один шаг к structural editing**
(Step 5), затем **runtime hardening** (Step 6), затем
**real-stand end-to-end + docs/runbooks** (Step 7),
затем **закрывающий integration pass** (Step 8). После
Step 8 Phase 6 закрывается.

Phase 6 **не** претендует на полную enterprise-вселенную.
Любая правка существующих серверов оформляется как
минимальная и локальная, по аналогии с Phase 2 / Step 10,
Phase 3 / Step 7, Phase 4 / Step 7, Phase 5 / Step 8.

## Step 1

**Planning Industrialization & Completion Track —
documentation entry.**

- **Цель.** Зафиксировать документационный вход в
  Phase 6: назначение фазы, целевой результат, шесть
  продуктовых блоков (A–G), guardrails, явный список
  «что НЕ входит», 10 критериев приёмки, открытые
  вопросы. Кода не писать. Никаких изменений
  registry. Никаких новых MCP tool'ов.
- **Что меняем.** Только документация:
  - `docs/architecture/phase-6-industrialization-plan.md`
    (новый);
  - `docs/architecture/phase-6-step-map.md` (новый);
  - корневой `README.md` (Phase 5 → закрыта; Phase 6
    → активная; ссылки на оба новых документа);
  - `PROJECT-STATUS.md` (текущий шаг → Phase 6 /
    Step 1; Step 8 Phase 5 окончательно закрыт;
    следующий шаг → Phase 6 / Step 2).
- **Затронутые зоны.** `docs/architecture/**`,
  `README.md`, `PROJECT-STATUS.md`. **Никаких**
  изменений в `apps/`, `packages/`, `scripts/`,
  `pyproject.toml`, `.github/`, `.claude.json`.
- **Результат.** Документационный вход в Phase 6
  готов. Все Steps 2–8 работают от этих контрактов.
  Ни один code-критерий приёмки на этом шаге не
  закрывается — Step 1 только открывает фазу.

## Step 2

**Contract for real 1cv8 execution / config surface.**

- **Цель.** Решить ключевые открытые вопросы Step 1
  плана: какой Phase 2 stub-backed путь
  (`create_dump_snapshot` / `apply_config_from_files`
  / `update_database_configuration`) первым переводится
  на binary-backed dispatch; какой 1cv8 CLI contract
  (режимы / args / timeout / ошибки); как делается
  honest fallback на stub при отсутствии binary.
  Зафиксировать контракт в коде минимальной
  правкой write-server'а или его runtime-слоя, без
  размывания `run_write_flow` гарантий.
- **Что меняем.**
  - Точечная правка одного из write-tool'ов
    (`apps/mcp-write-server/src/mcp_write_server/tools.py`
    либо соответствующего helper'а в `runtime/`):
    добавляется dispatch на `onec_binary_path`
    окружения. При отсутствии binary path —
    старое stub-поведение **сохраняется без
    изменений**. При наличии — реальный subprocess
    через `onec_process_runner.run_process` с
    documented argv-templated CLI.
  - Payload write-tool'а получает явный маркер
    `mode = "stub" | "binary-backed"` (или
    эквивалентное поле) — это критерий приёмки 1.
  - `run_write_flow` остаётся единственной точкой
    входа: preflight + snapshot + operation +
    verify + audit обязательны и для binary-backed
    режима.
  - В `apps/platform/src/onec_platform/realstand.py`
    может появиться minor поверхность для
    advisory-сообщения «binary-backed dispatch для
    операции X включён» в smoke-test plan summary.
  - registry write-server **не меняется** (это та же
    операция, просто с расширенным dispatch).
- **Затронутые зоны.** Точечно
  `apps/mcp-write-server/**` (один write-tool /
  один helper). Опционально точечно
  `apps/platform/**` (advisory). Read- и
  intelligence-серверы не трогаются.
  `onec-process-runner` уже умеет всё нужное —
  его не правим.
- **Результат.** Закрывается часть критерия приёмки
  1 (один Phase 2 stub-backed путь имеет
  binary-backed dispatch при наличии binary path).
  Honest fallback дисциплина (критерий 9)
  подтверждена: при отсутствии binary path
  поведение идентично Phase 2.

## Step 3

**Installer / packaging / setup fast path.**

- **Цель.** Закрыть критерий приёмки 3: установка/запуск
  по короткому сценарию реально сокращены.
  Документированный install runbook укладывается в
  ≤ 5 ручных шагов от «получил релиз» до «bootstrap
  doctor зелёный». Решить открытый вопрос Step 1
  плана: формат релиза.
- **Что меняем.**
  - В `apps/platform/` (или в `scripts/dev/`, если
    это уместнее как dev-tool, но скорее
    `apps/platform/`) появляется install-helper:
    короткий script + declarative product-config
    template. Wizard остаётся out of scope
    (declarative-only).
  - Возможно, минимальная правка
    `apps/platform/src/onec_platform/bootstrap.py`
    — но только если это реально нужно для install
    flow'а. По умолчанию bootstrap уже умеет всё.
  - Документирован формат релизного артефакта
    (zip / git tag / standalone-script — выбор
    фиксируется в этом шаге); добавляется
    versioning contract: какие версии 1cv8
    supported, какая версия платформы.
- **Затронутые зоны.** `apps/platform/**` (новый
  install helper / template); `docs/` (install
  runbook, но финальный operator manual — Step 7);
  возможно небольшая правка `scripts/dev/` если
  install-script удобнее жить рядом.
- **Результат.** Закрывается критерий приёмки 3.
  Частично закрывает критерий 5 (operator manual
  получает первый раздел — install runbook).

## Step 4

**Rollback execution track.**

- **Цель.** Закрыть критерий приёмки 2: появляется
  исполнимый rollback path хотя бы для одного
  класса write-tool'ов. Решить открытый вопрос
  Step 1 плана: какой именно класс recovery
  ship'ится первым.
- **Что меняем.**
  - В `apps/platform/src/onec_platform/recovery.py`
    `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist
    пополняется хотя бы одним именем.
    `run_rollback_assistant` с `confirm_execute=True`
    для этого класса достигает `mode=executed`.
  - Mutating recovery исполняется через **существующую**
    write-дисциплину: либо через существующий
    public write-tool (если его inverse уже есть —
    маловероятно), либо через **новый минимальный
    write-tool** (например, `delete_catalog_attribute`),
    зарегистрированный по contract'у Phase 2 / Phase 3
    (preflight + snapshot + verify + audit).
  - Если новый write-tool добавляется — это
    единственное место в Phase 6, где write-server
    registry **может вырасти**, и это происходит
    честно. Регистрируется через
    `build_tool_registry` из `mcp-common`, как все
    остальные write-tool'ы.
  - post-rollback verify обязателен.
  - Альтернативный путь: snapshot-based filesystem
    restore через `shutil.copytree` обратно. Но
    это требует careful contract'а — обсуждается
    в Step 4 при принятии решения; если выбран
    этот путь, write-channel остаётся в
    write-server'е (а не в product layer'е), как
    отдельный write-tool типа
    `restore_dump_from_snapshot`.
- **Затронутые зоны.** Точечно
  `apps/mcp-write-server/**` (если новый
  write-tool); точечно `apps/platform/**`
  (whitelist + plan summary). Read- и
  intelligence-серверы не трогаются.
- **Результат.** Закрывается критерий приёмки 2.
  Если новый write-tool добавлен —
  `mcp-write-server` registry честно растёт (24+).
  Если выбран snapshot-restore — registry не
  растёт, но появляется новая операция для
  filesystem-restore.

## Step 5

**Metadata completion / structural editing track.**

- **Цель.** Закрыть критерии приёмки 4 (частично —
  full metadata coverage) и 5 (частично —
  structural editing). Решить открытый вопрос Step 1
  плана: какие metadata-tool'ы добавляются
  (или ни одного, если Step 4 уже покрыл).
- **Что меняем.**
  - В `apps/mcp-write-server/**` — точечный добор:
    либо один `delete_*` tool (полезный для
    rollback workflow'ов из Step 4), либо
    extension `replace_module_method_body`
    к более safe structural patch, либо
    добавление одного structural-editing helper'а в
    `runtime/metadata_ops.py` (например, минимальный
    DOM-edit для одного whitelisted XML-блока).
  - Все новые/расширенные tool'ы наследуют
    contract Phase 2 / Phase 3.
  - Полный AST-парсер XML / BSL — out of Phase 6.
- **Затронутые зоны.** Точечно
  `apps/mcp-write-server/**`. Read- и
  intelligence-серверы не трогаются.
  `onec-config` / `onec-policy-engine` не трогаются.
- **Результат.** Частично закрывается критерий
  приёмки 4 (metadata coverage честно расширена)
  и 5 (первый шаг к structural editing сделан).
  registry write-server'а может вырасти (зависит
  от того, что выбрано).

## Step 6

**Runtime hardening / supervision / logs.**

- **Цель.** Закрыть критерий приёмки 7 (dev-check
  зелёный) при операторски-улучшенном runtime
  UX. Сделать runtime supervision **менее голым
  PID-ом** и более operator-friendly.
- **Что меняем.**
  - В `apps/platform/src/onec_platform/runtime.py`
    и `process_control.py`:
    - stdio дочерних сервисов перенаправляется в
      файлы под `<work_dir>/.runtime/logs/<service>/`
      (вместо `DEVNULL`); ротация по размеру либо
      по дням (выбор фиксируется на старте Step 6;
      простое решение — N последних файлов на
      сервис);
    - runtime state получает дополнительные поля:
      последний exit code если процесс был известен
      и умер; restart count в текущей сессии
      оркестратора;
    - базовая restart policy: opt-in флаг
      «restart-if-stale» при следующем
      `start_product_runtime` (не automatic
      supervisor — operator-driven).
  - В `apps/platform/src/onec_platform/dashboard.py`:
    runtime section получает поля «последние логи
    доступны по пути X», «restart count».
  - `selfcheck.py` не трогается.
- **Затронутые зоны.** `apps/platform/**`. Read- и
  intelligence-серверы не трогаются.
- **Результат.** Лучший runtime UX: оператор имеет
  логи дочерних процессов и видимость состояния.
  Частично закрывает критерий приёмки 7.

## Step 7

**Real-stand end-to-end validation + docs/runbooks.**

- **Цель.** Закрыть критерии приёмки 4 (один
  end-to-end real-stand сценарий проходит от setup
  до smoke с реальной binary-backed apply) и 5
  (operator/admin/developer manuals + runbooks
  существуют как standalone docs).
- **Что меняем.**
  - В контролируемом окружении (reference stand с
    реальной 1cv8 binary) проходится сценарий:
    setup (через Step 3 install path) → bootstrap →
    runtime → guided workflow с **binary-backed**
    apply (через Step 2 dispatch) → verify → audit.
    Сценарий описывается как воспроизводимый
    runbook.
  - Появляются standalone docs:
    - `docs/operator-manual.md` — установка,
      ежедневная эксплуатация, типовые сбои,
      типовые workflow'ы, log locations,
      environment toggling;
    - `docs/administrator-manual.md` — конфигурация
      окружений, allow_write, retention audit,
      snapshot rotation, security baseline;
    - `docs/developer-manual.md` — расширение
      workflow'ов, добавление новых read-tool'ов,
      contracts intelligence/read/write;
    - user-facing message style guide (часть
      operator manual или отдельный файл);
    - runbooks: `docs/runbooks/safe-add-attribute.md`,
      `docs/runbooks/rollback-recovery.md`,
      `docs/runbooks/real-stand-smoke.md`.
  - Кода правим минимально — только если real-stand
    прогон вскроет реальный blocker.
- **Затронутые зоны.** `docs/**`. Точечно
  `apps/**` если real-stand вскроет blocker.
- **Результат.** Закрываются критерии приёмки 4 и 5
  (полностью). Foundation для критерия 6 (нет
  деградации) проверена на реальной 1С.

## Step 8

**Final integration pass and Phase 6 closure.**

- **Цель.** Подтвердить, что Phase 6 действительно
  ship'нула industrialization slice end-to-end.
  Сделать сквозной интеграционный прогон:
  release → install → bootstrap → runtime →
  dashboard → guided workflow с binary-backed apply
  → recovery preview + executed (для одного
  класса) → real-stand smoke → operator manual
  full traversal. Зафиксировать закрытие Phase 6.
- **Что меняем.** Кода стараемся не трогать.
  Интеграционный прогон по сценариям из manuals.
  Если прогон вскроет реальный продуктовый
  blocker — разрешается минимальная точечная
  правка, по аналогии с Phase 5 / Step 8 (где
  правок не понадобилось вообще). Финализация
  manuals: operator, administrator, developer,
  user-facing message style guide. Корневой
  `README.md` и `PROJECT-STATUS.md` помечают
  Phase 6 закрытой; Phase 6 в крупных этапах —
  «Закрыта». Honest зафиксированные follow-up'ы
  (полное замещение оставшихся stub'ов, full
  enterprise track, AST-парсер, multi-instance
  HA) перечислены отдельно как **не**
  блокирующие закрытие Phase 6.
- **Затронутые зоны.** `docs/`, корневой `README.md`,
  `PROJECT-STATUS.md`; точечно `apps/**` при
  честной необходимости.
- **Результат.** Закрываются финальные критерии
  приёмки 6, 7, 8, 9, 10. **Phase 6 /
  Industrialization & Completion Track закрыта**.
  Платформа достигла finished product behavior на
  reference stand'е. Остаются только non-blocking
  follow-up / enterprise track'и за пределами
  Phase 6.
