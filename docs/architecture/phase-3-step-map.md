# Phase 3 Step Map

Стартовая карта Phase 3. Покрывает первые практические шаги, после
которых у платформы появляется metadata operation contract, internal
patch layer, первая волна реальных metadata tools и соответствующие
verification. Вся фаза сюда не входит — это карта старта, а не полный
roadmap.

## Step 1

**Metadata operation contract / intent model.**

- **Цель.** Зафиксировать единую модель namanja metadata-операций:
  какие intent names существуют, какие из них mutating, какие —
  verification-oriented, как они разбиваются на категории
  (object / attribute / form / module / diagnostic), какие общие
  поля несёт intent за рамками `operation_name` и `target`.
- **Что меняем.** Только документация (возможно, небольшой раздел
  в README write-server). Желательно зафиксировать список metadata
  operation names в `phase-3-metadata-changes-plan.md`, чтобы
  `onec-policy-engine._MUTATING_OPERATIONS` и
  `_NON_MUTATING_SUPPORT_OPERATIONS` знали, что будет добавляться.
  В коде ещё ничего не пишем.
- **Затронутые зоны.** `docs/architecture/`, возможно README
  write-server. Без правок кода.
- **Результат.** Все участники (write-server, policy engine,
  будущий metadata patch layer) имеют согласованный список
  metadata intent names и их семантику. Step 2 начинается без
  неопределённости в контрактах.

## Step 2

**Усиление `onec-config` / `onec-policy-engine` при необходимости.**

- **Цель.** Подготовить общие пакеты к metadata-операциям. Сейчас
  `EnvironmentConfig` не содержит поля пути к 1С-бинарю, а
  `onec-policy-engine` знает только про Phase 2 intent names.
- **Что меняем.**
  - В `onec-policy-engine._MUTATING_OPERATIONS` и
    `_NON_MUTATING_SUPPORT_OPERATIONS` добавить новые metadata
    operation names (по списку из Step 1). Backward compatibility
    сохранить (старые intent'ы продолжают работать).
  - При необходимости — опциональное поле в
    `EnvironmentConfig` (например, `onec_binary_path: str | None`)
    для будущего follow-up по реальному `1cv8`-integration. Если
    решим, что это именно Phase 3 / parallel follow-up — отложить.
- **Затронутые зоны.** `packages/onec-policy-engine/`, опционально
  `packages/onec-config/` и `scripts/dev/selfcheck.py` (точечный
  follow-up, как после Step 3 Phase 1).
- **Результат.** Policy и config готовы пропускать и принимать
  решения по новым metadata-операциям. `dev-check` остаётся
  зелёным.

## Step 3

**Internal metadata patch helper layer в write-server runtime.**

- **Цель.** Завести небольшой внутренний слой для metadata-patching,
  так же как Step 5 Phase 2 завёл `dump_ops.py`. Там будет жить
  логика structural вставок в XML-карточки объектов, поиска точек
  вставки по форме документа (не по `rfind("</")`), минимального
  BSL-парсинга для модулей.
- **Что меняем.** Создать
  `apps/mcp-write-server/src/mcp_write_server/runtime/metadata_ops.py`
  с тонкими вспомогательными функциями: нормализация
  relative_path, безопасная вставка XML-фрагмента в конкретный
  родительский тег, поиск метода по имени в тексте модуля,
  аккуратная замена тела метода с сохранением сигнатуры. **Public
  tools пока не появляются**.
- **Затронутые зоны.** `apps/mcp-write-server/src/mcp_write_server/runtime/`.
- **Результат.** Есть общая, протестированная (ручными check'ами)
  helper-библиотека, на которую Step 4–6 будут опираться. `tools.py`
  остаётся тонким.

## Step 4

**Первая волна metadata tools — object/attribute level.**

- **Цель.** Дать платформе возможность создавать первые полноценные
  metadata-объекты и наращивать их реквизиты через структурный
  patch.
- **Что меняем.** В `tools.py` write-server'а добавляются public
  tools (все через `run_write_flow`):
  - `create_catalog(environment, catalog_name, spec)`;
  - `add_document_attribute(environment, document_name,
    attribute_spec)`;
  - опционально `create_document(...)`, `create_information_register(...)`;
  - `add_catalog_attribute` переводится на metadata patch helper
    из Step 3, но с сохранением совместимости сигнатуры и поведения
    (verify по-прежнему должен находить имя и тип).
- **Затронутые зоны.** `apps/mcp-write-server/src/mcp_write_server/tools.py`,
  `server.py` (registry расширяется).
- **Результат.** Появляется минимум 3–4 новых public mutating tools
  группы A/B; все идут через flow; ручная проверка подтверждает,
  что новые объекты действительно создаются, реквизиты действительно
  добавляются, audit пишется.

## Step 5

**Verification-tools для metadata shape.**

- **Цель.** Самостоятельные public read-only verification-tools,
  подтверждающие metadata-изменения независимо от write-flow
  verify_callable.
- **Что меняем.** В `tools.py` добавляются:
  - `verify_attribute_exists(environment, object_name, attribute_name)`;
  - `verify_metadata_shape(environment, expectation)` — расширенный
    dispatcher поверх существующего `verify_metadata_change`, с
    новыми kinds (`attribute_exists`, `form_exists`, `method_exists`);
  - `diff_dump_fragment(environment, relative_path, baseline)` —
    diff по UTF-8 тексту против переданного baseline'а.
  Cross-app import строго write→read (как в Phase 2 Step 8).
- **Затронутые зоны.** `apps/mcp-write-server/src/mcp_write_server/tools.py`,
  `server.py`. Read-server не трогаем.
- **Результат.** Metadata operations из Step 4 теперь имеют
  отдельные public verification-tools, которые можно вызвать
  после flow или в отдельном сценарии.

## Step 6

**Form/module level metadata tools.**

- **Цель.** Поднять работу со структурой форм и модулей — наиболее
  сложная часть Phase 3.
- **Что меняем.** В `tools.py` добавляются:
  - `create_managed_form(environment, object_name, form_name, spec)`;
  - `add_form_element(environment, object_name, form_name, element_spec)`;
  - `append_module_method(environment, module_relative_path,
    method_spec)`;
  - `replace_module_method_body(environment, module_relative_path,
    method_name, new_body)` — **с явным non-default параметром
    подтверждения**, чтобы случайный вызов не триггерил
    structural rewrite.
  Все идут через `run_write_flow`; operation_callable опирается на
  helper'ы из Step 3; verify_callable сверяет изменения.
- **Затронутые зоны.** `apps/mcp-write-server/src/mcp_write_server/tools.py`,
  `server.py`, metadata_ops.py (может понадобиться расширение
  BSL-helper'ов).
- **Результат.** Появляется возможность программно наращивать
  структуру форм и методов модулей с обязательным verify и audit.

## Step 7

**Final integration pass фазы.**

- **Цель.** Подтвердить, что metadata-контур Phase 3 работает как
  единая система: от создания объекта до привязки обработчика
  формы с корректным verify и audit.
- **Что меняем.** Не новый код, а интеграционный прогон:
  как минимум один сценарий вида «create_catalog → add_catalog_attribute
  → create_managed_form → append_module_method → bind_form_handler
  → verify_metadata_shape → describe_last_write_operation →
  prepare_rollback_hint». Плюс 1–2 короткий failure path
  (structural rejection, несуществующий объект). README
  write-server дополняется блоком «Phase 3 Metadata Changes
  закрыт» с итоговым registry. Root README и PROJECT-STATUS
  обновляются до закрытия фазы.
- **Затронутые зоны.** `apps/mcp-write-server/README.md`,
  `README.md` (root), `PROJECT-STATUS.md`. Код — только если
  при прогоне вскроются узкие места.
- **Результат.** Phase 3 закрыта по критериям приёмки
  `phase-3-metadata-changes-plan.md`. Платформа готова к Phase 4
  (intelligence layer) — или к параллельной замене stub'ов
  Phase 2 на настоящий `1cv8`-integration, если к этому моменту
  уже появится путь к бинарю.
