# Phase 4 Step Map

Стартовая карта Phase 4. Покрывает первые практические шаги, после
которых у платформы появляется intelligence contract, внутренний
analysis layer `mcp-intelligence-server` и первая волна public
intelligence-tools. Шаг 7 замыкает фазу одним сквозным
intelligence-сценарием и закрывает Phase 4.

## Step 1

**Intelligence operation contract / phase planning.**

- **Цель.** Зафиксировать документационный вход в фазу: назначение,
  группы tool'ов (A / B / C / D), guardrails, критерии приёмки — всё
  в `phase-4-intelligence-plan.md` и `phase-4-step-map.md`. Кода
  не писать.
- **Что меняем.** Только документация. В `docs/architecture/`
  появляются два плановых документа; корневой `README.md` и
  `PROJECT-STATUS.md` помечают Phase 4 активной, Phase 0–3
  остаются в «Закрытых фазах».
- **Затронутые зоны.** `docs/architecture/**`, `README.md`,
  `PROJECT-STATUS.md`.
- **Результат.** Документационный вход в Phase 4 готов. Все
  дальнейшие Steps 2–7 работают от этих контрактов.

## Step 2

**Подготовка policy / config / contracts (если нужно).**

- **Цель.** Привести политику и config в соответствие с новыми
  intelligence operation names — **без write-веток**.
  Intelligence-операции read-only.
- **Что меняем.**
  - В `onec-policy-engine` возможный вариант: добавить новый
    frozenset `_INTELLIGENCE_OPERATIONS` и новую ветку в
    `_new_check` с `reason_code="allowed_intelligence"`,
    `require_snapshots=False`. Альтернатива — явно зафиксировать
    в phase-plan, что intelligence не проходит policy-check
    (все операции read-only и живут в отдельном сервере),
    и тогда policy не трогать. Выбор — на этом шаге.
  - В `onec-config` ничего не менять, если существующего
    `EnvironmentConfig` достаточно.
  - При необходимости — минимальный точечный follow-up по
    `scripts/dev/selfcheck.py` (как было в Phase 3 Step 3), чтобы
    не сломать dev-check.
  Backward compatibility Phase 2/3 сохраняется полностью.
- **Затронутые зоны.** Опционально
  `packages/onec-policy-engine/**` и `scripts/dev/selfcheck.py`.
  `onec-config`, `apps/`, read/write servers — не трогаются.
- **Результат.** Контракт политики зафиксирован; следующие шаги
  могут без двусмысленностей регистрировать intelligence-ops.

## Step 3

**Internal analysis helper layer в
`mcp-intelligence-server/runtime/`.**

- **Цель.** Создать собственный `runtime/` подпакет
  intelligence-server'а — аналог `mcp_read_server.runtime` и
  `mcp_write_server.runtime`. Внутренний helper-слой, на котором
  будут стоять все будущие public intelligence-tools Step 4–6.
  Public tools пока не появляются.
- **Что меняем.** Новый подпакет
  `apps/mcp-intelligence-server/src/mcp_intelligence_server/runtime/`
  с несколькими небольшими helper-модулями (состав уточняется в
  процессе, но минимально ожидаются):
  - `models.py` — `IntelligenceRuntimeContext` (`environment`,
    `health_results`, `health_codes`, ссылки на использованные
    источники).
  - `context.py` — `build_runtime_context(environment)` на базе
    `check_environment_health` из `onec-health`.
  - `dump_scanner.py` — базовые helper'ы поиска ссылок в dump
    (XML + BSL), сверху на `read_dump_file` / `find_files_by_pattern`
    / `read_text_file` из read-server runtime.
  - `reference_finder.py` — тонкий слой substring/regex поиска для
    `find_references_to_object` и смежных tool'ов.
  - `graph.py` — минимальный тип `DependencyGraph`
    (`nodes`, `edges`) + утилиты построения ограниченного
    подграфа.
  Cross-app import — только `intelligence → read` и
  `intelligence → write` (pure/read-only helpers типа
  `module_contains_method`).
- **Затронутые зоны.**
  `apps/mcp-intelligence-server/**`. Read- и write-серверы не
  трогаются.
- **Результат.** Общий внутренний analysis API готов.
  `dev-check` зелёный. Registry intelligence-server по-прежнему
  `['ping']`.

## Step 4

**Первая волна public intelligence-tools — dependency / reference
analysis.**

- **Цель.** Перевести intelligence-server из skeleton в реальный
  сервер с содержательными read-only tool'ами.
- **Что меняем.** В
  `apps/mcp-intelligence-server/src/.../tools.py` и
  `server.py` регистрируются (через `build_tool_registry` из
  `mcp-common`) первые public tools группы A:
  - `find_references_to_object`,
  - `analyze_object_dependencies`,
  - `find_module_method_usages`,
  - опционально `build_dependency_subgraph` (если MVP-
    реализация укладывается без раздутия).
  Все возвращают `ToolResult`, не идут через write-flow, не пишут
  audit. Cross-app import — только через
  `mcp_read_server.runtime` и pure helpers из
  `mcp_write_server.runtime.metadata_ops`.
- **Затронутые зоны.** `apps/mcp-intelligence-server/**`.
- **Результат.** Registry intelligence-server впервые содержит
  осмысленные tool'ы; `dev-check` зелёный; появляется первый
  ручной сценарий «найти все ссылки на объект», работающий на
  временной копии dump'а.

## Step 5

**Diagnostics / troubleshooting tools.**

- **Цель.** Добавить intelligence-tools для пост-фактум
  диагностики.
- **Что меняем.** В intelligence-server добавляются public tools
  группы C:
  - `analyze_runtime_issue`,
  - `analyze_event_log_patterns`,
  - `diagnose_broken_form_binding`,
  - `diagnose_missing_method_or_attribute`.
  Они опираются на read-server tools
  (`get_event_log`, `get_object_structure`,
  `get_form_structure`, `check_runtime_health`,
  `diagnose_connectivity_issue`) и на internal helpers Step 3.
  Каждый `ToolResult` явно разделяет `confirmed` / `presumed`.
- **Затронутые зоны.** `apps/mcp-intelligence-server/**`.
- **Результат.** Покрыты 2–3 диагностических сценария,
  требуемых критериями приёмки. `dev-check` остаётся зелёным.

## Step 6

**Impact / recommendation tools.**

- **Цель.** Закрыть оставшиеся группы B и D — impact analysis и
  рекомендации.
- **Что меняем.** В intelligence-server добавляются public tools
  групп B и D:
  - `estimate_change_impact`,
  - `find_affected_forms`,
  - `find_affected_modules`,
  - `suggest_safe_change_order`,
  - `suggest_fix_for_issue`,
  - `suggest_metadata_patch_plan`,
  - `summarize_configuration_risk`,
  - `prepare_intelligence_report`.
  Каждый переиспользует intelligence runtime + tools Step 4/5.
  `suggested_tools` в рекомендациях ссылается **только на
  существующие** public-инструменты write-server (Phase 2/3).
- **Затронутые зоны.** `apps/mcp-intelligence-server/**`.
- **Результат.** Полный Phase 4 tool set собран. Registry
  intelligence-server соответствует критериям приёмки (≥ 4–5
  tools, покрытие групп A/B/C/D).

## Step 7

**Final integration pass фазы.**

- **Цель.** Подтвердить intelligence-контур end-to-end и закрыть
  Phase 4.
- **Что меняем.** Кода стараемся не трогать. Интеграционный
  прогон: как минимум один сквозной сценарий вроде
  «`find_references_to_object` → `estimate_change_impact` →
  `suggest_safe_change_order` → `prepare_intelligence_report`»
  плюс 1–2 failure-path (недостаток данных, несуществующий
  объект, пустой event log). Если integration pass выявляет
  реальный блокер — разрешается минимальная точечная правка
  кода, как это было в Phase 2 Step 10 и Phase 3 Step 7;
  только при честной необходимости, без рефакторинга.
- **Затронутые зоны.**
  `apps/mcp-intelligence-server/README.md`, корневой `README.md`,
  `PROJECT-STATUS.md` — все помечают Phase 4 закрытой; в
  крупных этапах Phase 4 становится «Закрыта», Phase 5 — «Следующая
  фаза».
- **Результат.** Phase 4 / Intelligence Layer закрыта по
  критериям `phase-4-intelligence-plan.md`. Платформа готова к
  Phase 5 (product layer) и/или к параллельному follow-up по
  реальному `1cv8`-integration из Phase 2.
