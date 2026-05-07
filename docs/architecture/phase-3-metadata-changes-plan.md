# Phase 3 Metadata Changes Plan

## Назначение фазы

Phase 2 / Write MVP дал ограниченный, но честный write-контур:
preflight → snapshots → operation → verify → audit. С его помощью
агент уже умеет делать несколько базовых правок в dump/source tree
(`update_module_code`, `create_common_module`, `add_catalog_attribute`)
и запускать stub-backed apply/update-db.

Phase 3 — следующий уровень. Это переход от «нескольких точечных
правок через text patch» к **полноценным, осмысленным операциям над
метаданными конфигурации 1С**. Цель — чтобы агент мог системно
работать со структурой конфигурации:

- объекты (справочники, документы, регистры, общие модули, роли);
- реквизиты (объектов, форм, табличных частей);
- формы (управляемые формы, элементы, привязка обработчиков);
- модули (методы, тела функций, экспортность);
- связи между всеми этими сущностями.

Это **не просто больше write-инструментов**. Это разворачивание
платформы в сторону реального developer workflow 1С: создать
объект — добавить реквизит — сделать форму — привязать обработчик —
добавить метод в модуль — проверить, что всё связано корректно.

## Целевой результат

К моменту закрытия Phase 3:

- `mcp-write-server` умеет делать **metadata-oriented изменения** не
  только через грубые text-patch'и, но и через более структурные
  операции. Каждый metadata-tool по-прежнему идёт через единый
  `run_write_flow(...)`: preflight, snapshots, operation, verify,
  audit. Guardrails, введённые в Phase 2, действуют и в Phase 3 —
  плюс более жёсткие проверки для структурных операций (см. ниже).
- Появляется новый **internal metadata patch layer** в `runtime/`
  write-server'а: небольшой helper слой, в котором живёт логика
  XML/ text-patch'инга, структурно осмысленная и переиспользуемая
  между tools. `tools.py` должен остаться тонким.
- Verify и audit продолжают быть обязательными. Добавляются
  specialized verification tools для metadata shape (наличие
  реквизита, формы, метода).
- Read-server остаётся опорой для verify/live-check. Cross-app
  import по-прежнему допустим **только в сторону write → read**.
- Структура становится ближе к реальному 1C dev workflow. Агент
  должен уметь описывать намерение («добавить реквизит такой-то
  справочнику такому-то») как `WriteIntent`, а не как серию
  низкоуровневых правок.

## Набор инструментов фазы

Ниже — **предлагаемый стартовый набор**, а не декларация готового
продукта. Конкретные формы сигнатур и payload будут уточнены в
Step 1 (metadata operation contract).

### A. Object-level metadata operations

Создают новые объекты конфигурации в dump-дереве. Все — mutating,
идут через `run_write_flow`.

- **`create_catalog(environment, catalog_name, spec)`** — создать
  новый справочник: минимальные XML-карточки `Catalogs/<name>.xml`
  + связанные директории форм/модулей. `spec` — whitelist полей
  (код, наименование, иерархия, представления).
  Слой: metadata patch helper + onec-process-runner.
  Зачем: первый полноценный «создай объект» сценарий.
  Ограничения: имя валидируется как `module_name` сейчас;
  перезапись существующего каталога отсутствует.
- **`create_document(environment, document_name, spec)`** — аналог
  для документов (Documents/...).
- **`create_information_register(environment, register_name, spec)`**
  — регистр сведений, с поддержкой измерений/ресурсов/реквизитов
  в `spec`.
- **`create_common_module_from_template(environment, module_name,
  template)`** — усиленная версия уже существующего
  `create_common_module`: имя модуля + шаблон (например, «модуль с
  экспортной функцией по умолчанию»).
- **`create_role(environment, role_name, spec)`** — добавить роль
  доступа (Roles/...).

### B. Attribute / schema operations

Изменяют схему существующих объектов. Все — mutating, через flow.

- **`add_catalog_attribute(environment, catalog_name, attribute_spec)`**
  — **уже существует** как pragmatic text-patch с Phase 2. В Phase 3
  планируется замена/усиление: более структурная вставка, защита от
  дублирующих имён на уровне metadata patch layer.
- **`add_document_attribute(environment, document_name,
  attribute_spec)`** — аналог для документов.
- **`add_tabular_section(environment, catalog_name, ts_spec)`** —
  табличная часть.
- **`add_form_attribute(environment, object_name, form_name,
  attribute_spec)`** — реквизит формы.
- **`change_attribute_type(environment, object_name, attribute_name,
  new_type)`** — смена типа реквизита. **Потенциально
  необратимая** операция; требует явного intent и обязательного
  snapshot'а (см. guardrails).

### C. Form / module structure operations

Работают со структурой форм и модулей.

- **`create_managed_form(environment, object_name, form_name, spec)`**
  — создать управляемую форму для существующего объекта.
- **`add_form_element(environment, object_name, form_name, element_spec)`**
  — добавить элемент управления на форму.
- **`bind_form_handler(environment, object_name, form_name, event,
  handler_method)`** — привязать обработчик события к методу
  модуля формы.
- **`append_module_method(environment, module_relative_path,
  method_spec)`** — дописать в модуль новый метод (без перезаписи
  существующих).
- **`replace_module_method_body(environment, module_relative_path,
  method_name, new_body)`** — аккуратно заменить тело метода,
  сохранив сигнатуру и директивы. **Опаснее** чем
  `update_module_code` (который перезаписывает весь файл):
  требует structural patching, а не наивного text-replace.

### D. Verification / structural diagnostics

Read-only, **не** через flow. Специфичные для metadata проверки.

- **`verify_attribute_exists(environment, object_name,
  attribute_name)`** — проверить, что реквизит есть в карточке
  объекта.
- **`verify_form_exists(environment, object_name, form_name)`** —
  проверить, что форма реально создана в dump.
- **`verify_module_method_exists(environment, module_relative_path,
  method_name)`** — проверить наличие метода в модуле
  (парсинг BSL минимальной глубины: имя + директива + экспортность).
- **`verify_metadata_shape(environment, expectation)`** —
  общая проверка формы: expectation описывает, что должно быть
  (реквизиты, табличные части, формы, модули) — tool проверяет
  согласованность.
- **`diff_dump_fragment(environment, relative_path, baseline)`** —
  diff между текущим состоянием файла/каталога и переданным
  baseline'ом. Полезен для post-operation self-check и для
  интеграционных сценариев.

## Основные guardrails Phase 3

Phase 3 опаснее Write MVP: структурные операции могут нарушить
целостность метаданных более коварно, чем text patch. Поэтому
guardrails жёстче.

- **Production-like окружения blocked by default.** Никаких
  послаблений. `onec-policy-engine` продолжает работать как в
  Phase 2.
- **Любое metadata change идёт строго через `run_write_flow`.**
  preflight → backup+dump snapshots → operation → verify → audit.
  Ни один metadata-tool группы A/B/C **не имеет права** обходить
  `run_write_flow`. Подрядчик-callback внутри operation работает
  только со snapshot'ом на диске, не меняя «боевой» dump напрямую
  до финального commit (см. metadata patch layer, Step 3).
- **Идемпотентность или fail-closed.** Если операция по смыслу
  может быть запущена повторно (create_catalog с тем же именем,
  add_attribute с тем же именем) — она должна либо быть
  идемпотентной и вернуть тот же результат, либо явно отказывать
  с диагностикой до любых мутаций. Никаких частичных записей.
- **Никакого silent mutation.** Каждое metadata-изменение
  отражается в `ToolResult.payload.data` максимально подробно:
  что создано, что изменено, какие дополнительные файлы
  затронуты. Нет «тихих» side-effects.
- **Уход от наивного text patch там, где это возможно.** Там,
  где сейчас Phase 2 использует rfind/write_text (как
  `add_catalog_attribute`), Phase 3 должна предоставить более
  структурные операции через metadata patch helper layer: хотя
  бы на уровне «найти правильную точку вставки по
  структуре», а не «по последнему `</`».
- **Необратимые/неоднозначные изменения не выполняются
  автоматически без явного intent.** `change_attribute_type`,
  `replace_module_method_body` и подобные требуют либо отдельного
  `confirm` в intent, либо явного non-default параметра, чтобы
  случайный вызов их не спровоцировал.
- **Verify обязательна в том же flow.** Для каждого metadata-tool
  группы A/B/C operation_callable сопровождается verify_callable,
  который подтверждает изменение как на dump-уровне, так и
  (где возможно) на live-уровне.
- **Audit расширяется metadata-awareness.** Запись `AuditRecord`
  по-прежнему идёт через `onec-audit.append_record`; `tool_name`
  берётся из `intent.operation_name` (как сделано в Step 10
  Phase 2). Для metadata ops audit должен содержать достаточно
  контекста, чтобы rollback hint был осмысленным.

## Что не входит в эту фазу

- **Full autonomous refactoring agent.** Агент не принимает
  самостоятельных решений вроде «давай я сам переименую тут и тут
  и пофикшу все ссылки». Это тема пост-MVP intelligence layer.
- **Production automation.** По-прежнему только local-dev.
  Production-like блокируется policy.
- **Self-healing / intelligence auto-fix.** Правки на основе
  анализа журналов и автоматическое лечение — Phase 4 / 5.
- **Multi-base orchestration.** Никаких «применить это изменение
  к 5 базам сразу» в Phase 3.
- **Полноценный GUI/UX слой.** Tools остаются tool-level
  контрактом; любые UI/IDE-интеграции — отдельный слой поверх.
- **Product workflows Phase 5.** Сценарии для конечных пользователей
  поверх платформы — не в Phase 3.
- **Замена stub'ов Phase 2 на реальный `1cv8 LoadConfigFromFiles`
  / `UpdateDBCfg` / `DumpCfg`.** Это параллельный follow-up, не
  MVP-блокирующий Phase 3. Может быть выполнен в любой момент,
  когда в `onec-config.EnvironmentConfig` появится путь к бинарю.

## Критерии приёмки Phase 3

Phase 3 считается закрытой, когда:

- реализованы и зарегистрированы **не менее 4–5** metadata-write
  tools группы A/B (с учётом обновлённого
  `add_catalog_attribute`);
- для metadata changes существует **хотя бы 2–3** specialized
  verification tool'а группы D (`verify_attribute_exists`,
  `verify_metadata_shape` или эквивалент,
  `diff_dump_fragment`);
- audit-записи отражают metadata operations корректно:
  `tool_name = public operation`, `status` честный,
  `message` информативен;
- read-server подтверждает изменения на live/dump уровне через
  уже существующие read-tools (`get_metadata_object`,
  `get_object_structure`, `read_module_code_from_dump`);
- **`dev-check` зелёный** на каждом шаге;
- подтверждён **хотя бы один end-to-end metadata scenario**: что-то
  вроде «создать справочник → добавить реквизит → создать форму
  → привязать обработчик → проверить структуру → показать rollback
  hint» — целиком через flow, с audit, с verify.

До этого порога фаза остаётся `in progress`.
