# Phase 5 Step Map

Стартовая карта Phase 5 — Product Layer. Восемь шагов. Карта
держит проект на пути от уже готового read/write/intelligence
ядра к выдаваемому продукту.

Каждый шаг описан в одинаковой структуре:

- **Цель** — что именно должно стать правдой по результату шага.
- **Что меняем** — какие подсистемы / документы / артефакты
  меняются. Step 1 — документационный (никакого кода).
  Шаги 2–8 могут писать код, но строго в product layer
  и без переписывания read/write/intelligence.
- **Затронутые зоны** — границы шага в репозитории.
- **Результат** — какое условие из критериев приёмки
  Phase 5 шаг закрывает.

Логика: **сначала контракт продукта** (Step 1), затем
**установка и инициализация** (Step 2), затем **запуск и
наблюдение** (Step 3–4), затем **guided workflow'ы** (Step 5),
затем **откат и аудит** (Step 6), затем **реальный стенд и
интеграция с 1cv8** (Step 7), затем **закрывающий integration
pass** (Step 8). После Step 8 Phase 5 закрывается.

Phase 5 **не** добавляет новые public MCP tools ради
расширения tool-set'а. Любая правка существующих серверов
оформляется как минимальная и локальная, по аналогии с
Phase 2 / Step 10 и Phase 3 / Step 7.

## Step 1

**Product contract / scope / packaging model — planning.**

- **Цель.** Зафиксировать документационный вход в Phase 5:
  назначение фазы, целевой результат, шесть продуктовых
  блоков (A–F), список из 16+ продуктовых capability'ов,
  guardrails, критерии приёмки, явный список того, что
  **не** входит. Кода не писать. Никаких изменений
  registry. Никаких новых MCP tool'ов.
- **Что меняем.** Только документация:
  `docs/architecture/phase-5-product-layer-plan.md` (новый),
  `docs/architecture/phase-5-step-map.md` (новый),
  корневой `README.md` (Phase 4 → закрыта; Phase 5 →
  активная; ссылки на оба новых документа),
  `PROJECT-STATUS.md` (текущий шаг → Phase 5 / Step 1;
  следующий шаг → Phase 5 / Step 2).
- **Затронутые зоны.** `docs/architecture/**`,
  `README.md`, `PROJECT-STATUS.md`. **Никаких** изменений
  в `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`.
- **Результат.** Документационный вход в фазу готов.
  Все Steps 2–8 работают от этих контрактов. Ни один
  code-критерий приёмки на этом шаге не закрывается —
  Step 1 только открывает фазу.

## Step 2

**Installer / bootstrap contract.**

- **Цель.** Зафиксировать формат релиза, формат
  product-config, форму setup-flow'а и **первичную**
  installer-обвязку. Решить открытые вопросы Step 1
  плана: формат релиза, формат product-config,
  интерактивный vs декларативный setup. После шага
  пользователь должен пройти install по короткому
  сценарию.
- **Что меняем.** Появляется новая директория
  product layer'а (имя фиксируется на старте Step 2; в
  плане ожидается что-то вроде `apps/platform/` или
  `packages/onec-product/` — конкретно решается в Step 2
  при принятии packaging-модели). Внутри:
  - product-config schema и loader (тонкая обвязка над
    уже существующим `onec-config.EnvironmentConfig`,
    без переписывания самого `EnvironmentConfig`);
  - prereqs doctor (compound check над Python /
    1cv8 / сетью / правами на dump_path), внутри
    дёргает уже существующие `health_summary` и
    `check_runtime_health` без дублирования;
  - setup-скрипт / setup manual.
  Read-server, write-server и intelligence-server **не**
  трогаются.
- **Затронутые зоны.** Новый product layer пакет /
  директория; `scripts/dev/` дополняется при
  необходимости (минимально); `docs/architecture/`
  получает раздел про packaging contract.
- **Результат.** Закрываются критерии приёмки 1
  (короткий сценарий установки) и часть критерия 8
  (read/write/intelligence не деградируют) — на уровне
  «после Step 2 платформа всё ещё запускается через
  существующий dev-check и проходит новый install
  путь».

## Step 3

**Runtime orchestration layer — single entry point.**

- **Цель.** Поднять read + write + intelligence как
  согласованный набор через одну точку входа.
  Решить открытый вопрос Step 1 плана о транспорте
  MCP (stdio / TCP / локальный socket) для
  product runner'а. После шага пользователь видит
  одну команду, которая разворачивает рабочую
  платформу.
- **Что меняем.** В product layer'е появляется
  platform runner: lifecycle (start / stop /
  status / reload), environment profile manager.
  Внутри runner'а — **только** запуск/остановка
  существующих серверов; никакой новой бизнес-
  логики поверх. Если для согласованности
  потребуется минимальная контрактная правка в
  серверах (например, единый формат `--env` flag),
  она оформляется как точечная правка в
  соответствующем сервере, по строгой аналогии с
  Phase 2 / Step 10 и Phase 3 / Step 7.
- **Затронутые зоны.** Product layer пакет;
  опционально — точечно `apps/mcp-*-server/` (только
  если runner-контракт этого требует). Registry
  каждого сервера не меняется.
- **Результат.** Закрываются критерий приёмки 2
  (платформа поднимается как согласованный набор) и
  часть критерия 8 (нет деградации MCP-серверов).

## Step 4

**Environment doctor / preflight UX / health dashboard.**

- **Цель.** Сделать наблюдаемость продукт-уровневой:
  один читаемый снимок состояния платформы и
  окружений. Без новой логики — собранный из уже
  существующих read/intelligence сигналов.
- **Что меняем.** В product layer'е появляется
  environment doctor / health dashboard. Внутри —
  агрегатор `health_summary` + `check_runtime_health`
  + `analyze_runtime_issue` +
  `summarize_configuration_risk` в одно представление.
  Никаких новых MCP tool'ов в read/intelligence
  серверах. Никаких изменений в существующих
  failure-style и payload discipline.
- **Затронутые зоны.** Product layer пакет; разделы
  Operator manual / Administrator manual в
  `docs/operator-manual/` (директория появляется на
  Step 4, если ещё не создана в Step 2).
- **Результат.** Частично закрывается критерий
  приёмки 6 (документация существует как продукт) —
  в части operator-section'а; полностью обеспечивает
  observability для критериев 2 и 11.

## Step 5

**Guided workflow layer — safe-add-attribute,
safe-add-module-method, stand-health-check.**

- **Цель.** Превратить связки tool-вызовов в
  guided user-facing workflows. Реализовать 2–3
  базовых end-to-end сценария. Запретить silent
  apply.
- **Что меняем.** В product layer'е появляется
  workflow runner и три первых workflow'а:
  - **safe-add-attribute** —
    `estimate_change_impact` →
    `find_affected_forms` →
    `check_write_preconditions` →
    `create_backup_snapshot` → `create_dump_snapshot`
    → `add_catalog_attribute` или
    `add_document_attribute` → `verify_attribute_exists`;
  - **safe-add-module-method** —
    `find_module_method_usages` →
    `check_write_preconditions` →
    `create_backup_snapshot` → `create_dump_snapshot`
    → `append_module_method` → `verify_module_contains`;
  - **stand-health-check** (read-only) —
    `analyze_runtime_issue` +
    `summarize_configuration_risk` +
    `prepare_intelligence_report`.
  Workflow runner показывает план через
  `suggest_safe_change_order` /
  `suggest_metadata_patch_plan`, ждёт явного
  подтверждения, исполняет через
  `run_write_flow` (для mutating workflow'ов),
  пишет audit. Все три workflow'а — это
  **обвязка над существующими public tool'ами**,
  ни один не обходит safety guarantees.
- **Затронутые зоны.** Product layer пакет;
  Operator manual и Developer manual получают
  разделы про workflow'ы.
- **Результат.** Закрывается критерий приёмки 3
  (как минимум 2–3 end-to-end workflows). Также
  усиливается критерий 9 (read-only контракт
  intelligence-server'а сохранён) и критерий 10
  (safety guarantees Phase 2–4 не размыты) —
  через автоматический assert на отсутствие
  silent apply внутри workflow'ов.

## Step 6

**Rollback / recovery / audit UX.**

- **Цель.** Сделать rollback цельным capability'ом,
  а не разрозненными примитивами. Решить открытый
  вопрос Step 1 плана: где хранить читаемую
  operation history — отдельный индекс над audit
  JSONL или live-aggregation.
- **Что меняем.** В product layer'е появляется:
  - operation history viewer над уже существующим
    audit JSONL и `describe_last_write_operation`;
  - rollback assistant — показывает последнюю
    операцию, доступные snapshot'ы, цену отката,
    ждёт явного подтверждения, исполняет recovery
    через workflow runner;
  - recovery workflow для типовых сбоев apply /
    verify; живёт как workflow в workflow runner
    (block C), не как silent apply.
  Никаких новых MCP write-tool'ов. Никаких изменений
  в формате audit JSONL.
- **Затронутые зоны.** Product layer пакет;
  Operator manual получает раздел recovery /
  rollback.
- **Результат.** Закрывается критерий приёмки 4
  (rollback / recovery path как продуктовый
  сценарий) и часть критерия 6 (документация о
  recovery).

## Step 7

**Real-stand / 1cv8 binary integration track.**

- **Цель.** Закрыть разрыв между «локально проходит
  dev-check» и «работает на реальном стенде».
  Решить открытый вопрос Step 1 плана: глубину
  smoke test (минимум обязательных workflow'ов
  для релиза).
- **Что меняем.** Описание reference stand'а
  (версия 1С, ОС, сеть, права);
  1cv8 binary integration contract — явный путь от
  Phase 2 stub'ов
  (`apply_config_from_files`,
  `update_database_configuration`,
  `create_dump_snapshot`) к реальным режимам
  `DESIGNER` / `ENTERPRISE` / `DumpCfg`;
  smoke test против реальной binary в
  контролируемом окружении (минимум —
  `create_common_module` + `add_catalog_attribute` +
  `verify_*`); honest зафиксированные ограничения.
  **Полное замещение всех stub'ов в одной фазе не
  обязательно.** Step 7 устанавливает контракт и
  smoke test, остальное — track после Phase 5.
  Если для smoke test'а нужна точечная правка в
  `onec-process-runner` или write-server — она
  оформляется как минимальная и локальная, без
  переписывания.
- **Затронутые зоны.** `docs/architecture/`
  (reference stand spec, binary integration
  contract); опционально точечно
  `packages/onec-process-runner/` и
  `apps/mcp-write-server/` (только если smoke
  test потребует — без переписывания);
  Operator / Administrator manuals получают
  раздел про реальный стенд.
- **Результат.** Закрывается критерий приёмки 5
  (реальный стенд / интеграция имеют явный
  трек готовности). Ограничения честно
  зафиксированы, а не замазаны.

## Step 8

**Final integration pass / docs / product readiness review.**

- **Цель.** Подтвердить, что Phase 5 действительно
  собрала продукт. Сделать сквозной интеграционный
  прогон через installer → runner → doctor →
  workflow → rollback → smoke test и зафиксировать
  закрытие фазы. Никаких новых tool'ов и подсистем.
- **Что меняем.** Кода стараемся не трогать.
  Интеграционный прогон по сценариям из manuals.
  Если прогон вскрывает реальный продуктовый
  блокер — разрешается минимальная точечная
  правка, по аналогии с Phase 2 / Step 10,
  Phase 3 / Step 7, Phase 4 / Step 7. Финализация
  manuals: operator, administrator, developer,
  user-facing message style guide. Корневой
  `README.md` и `PROJECT-STATUS.md` помечают Phase 5
  закрытой; Phase 5 в крупных этапах — «Закрыта».
  Honest зафиксированные follow-up'ы (полное
  замещение stub'ов, full enterprise track,
  AST-парсер) перечислены отдельно как **не**
  блокирующие закрытие Phase 5.
- **Затронутые зоны.** `docs/`, корневой `README.md`,
  `PROJECT-STATUS.md`; точечно — product layer и/или
  серверы при честной необходимости.
- **Результат.** Закрываются критерии приёмки 6
  (документация полная), 7 (dev-check зелёный),
  8 (read/write/intelligence не деградировали),
  9 (read-only контракт intelligence сохранён),
  10 (safety guarantees Phase 2–4 не размыты),
  11 (продукт ощутимо готов к выдаче).
  **Phase 5 / Product Layer закрыта** — остаются
  только non-blocking enterprise / 1cv8 follow-up
  track'и.
