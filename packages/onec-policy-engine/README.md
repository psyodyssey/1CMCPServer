# onec-policy-engine

Движок политик / preflight для write-операций платформы 1C Agent
Platform. Начиная с Phase 2 принимает осмысленные решения по
write-намерениям; в Phase 3 контракт расширен поддержкой
metadata-операций — у них отдельная категория решения и отдельные
`reason_code`, так что write-server может надёжно отличать обычную
Phase-2 write-операцию от Phase-3 metadata mutation.

## Что внутри

- `WriteIntent(operation_name, target=None)` — описание одной
  write-операции, которая рассматривается движком.
- `PolicyDecision(allowed, reason, reason_code, require_snapshots)`
  — результат проверки. `reason_code` предназначен для машинной
  обработки, `reason` — для human-readable сообщений,
  `require_snapshots` говорит write-server'у, нужно ли снимать
  backup/dump перед операцией.
- `check_write_allowed(...)` — основной entry-point,
  поддерживающий две формы вызова (см. ниже).

## Категории operation_name

Поддерживаются четыре категории operation_name плюс fallback:

1. **Phase 2 mutating** — `apply_config_from_files`,
   `update_database_configuration`, `create_common_module`,
   `update_module_code`, `add_catalog_attribute`. Возвращает
   `reason_code="allowed_mutating"`, `require_snapshots=True`.
2. **Phase 2 non-mutating support** — `check_write_preconditions`,
   `create_backup_snapshot`, `create_dump_snapshot`,
   `verify_metadata_change`, `verify_module_contains`,
   `verify_object_exists`, `write_audit_record`,
   `describe_last_write_operation`, `prepare_rollback_hint`.
   Возвращает `reason_code="allowed_non_mutating"`,
   `require_snapshots=False`.
3. **Phase 3 metadata mutating** — `create_catalog`,
   `create_document`, `create_information_register`,
   `create_common_module_from_template`, `create_role`,
   `add_document_attribute`, `add_tabular_section`,
   `add_form_attribute`, `change_attribute_type`,
   `create_managed_form`, `add_form_element`, `bind_form_handler`,
   `append_module_method`, `replace_module_method_body`. Возвращает
   `reason_code="allowed_metadata_mutating"`, `require_snapshots=True`.
4. **Phase 3 metadata support / verification** —
   `verify_attribute_exists`, `verify_form_exists`,
   `verify_module_method_exists`, `verify_metadata_shape`,
   `diff_dump_fragment`. Возвращает
   `reason_code="allowed_metadata_support"`,
   `require_snapshots=False`.

Неизвестные `operation_name` отбрасываются как `unknown_intent`
(fail-closed).

Имена Phase 2 остаются в своих оригинальных категориях; Phase 3
расширяет набор поверх существующего, без пересечений.

## Intelligence-операции (Phase 4) — не проходят через этот движок

Phase 4 intelligence-tools (`mcp-intelligence-server`) по построению
**read-only**: не меняют файлы, не запускают `run_write_flow`, не
пишут audit. Контракт Phase 4 явно фиксирует, что intelligence
**не проходит** `check_write_allowed`. Это зеркалит существующий
паттерн `mcp-read-server` — read-side тоже не роутится через
write-policy — и сохраняет смысл движка узким: он решает **write**,
а не read.

Практический эффект:

- В `onec-policy-engine` не добавлено никакой категории
  `_INTELLIGENCE_OPERATIONS` и никакого `reason_code="allowed_intelligence"`.
  Поверхность движка осталась ровно четыре категории Phase 2/3.
- Enforcement идёт через отсутствие импорта:
  `mcp_intelligence_server` не импортирует
  `onec_policy_engine.check_write_allowed`.
- Если intelligence-operation name когда-нибудь случайно попадёт в
  `WriteIntent` и будет проверен на write-стороне — движок честно
  вернёт `unknown_intent` (fail-closed). Это бесплатная страховка,
  а не штатный путь.

Обратная совместимость Phase 2/3 полностью сохранена: поведение
`check_write_allowed` в новом и legacy режимах не изменилось.

## Правила

1. **Production-like окружения блокируются по умолчанию.**
   Любая операция отклоняется, если имя окружения, `base_id`,
   `publication_name` или `http_base_url` содержит подстроку `prod`
   или `production` (в нижнем регистре). Это консервативный
   временный guardrail — пока в `EnvironmentConfig` нет отдельного
   `environment_type`.
2. **Write только при `allow_write=True`.** Если окружение не
   production-like, но `allow_write=False`, запись отклоняется.
3. **Mutating операции (обеих групп) требуют snapshot'ов.**
   `require_snapshots=True` для Phase 2 mutating и для Phase 3
   metadata mutating.
4. **Support операции (обеих групп) разрешены без snapshot'ов.**
   `require_snapshots=False` для Phase 2 non-mutating support и
   для Phase 3 metadata support/verification.
5. **Unknown intents отклоняются.** `reason_code="unknown_intent"`.

## Формы вызова

- **Новая:** `check_write_allowed(environment: EnvironmentConfig,
  intent: WriteIntent) -> PolicyDecision`. Применяется всем
  write-server кодом Phase 2 и Phase 3.
- **Legacy:** `check_write_allowed(environment_name: str,
  allow_write: bool) -> PolicyDecision`. Сохранена **временно**
  ради совместимости с текущим `scripts/dev/selfcheck.py`
  (там всё ещё `("production", True)` и `("local-dev", False)`).
  Будет убрана, когда selfcheck перейдёт на новую форму.

## Коды решений

- `production_blocked` — окружение помечено как production-like.
- `write_not_allowed` — `allow_write=False`.
- `allowed_mutating` — Phase 2 mutating write operation; нужны
  snapshot'ы.
- `allowed_non_mutating` — Phase 2 non-mutating support; snapshot'ы
  не нужны.
- `allowed_metadata_mutating` — Phase 3 metadata mutating; нужны
  snapshot'ы.
- `allowed_metadata_support` — Phase 3 metadata verification/support;
  snapshot'ы не нужны.
- `allowed_legacy` — legacy-режим вызова `(str, bool)`, запись
  разрешена; `require_snapshots=True` как безопасный default.
- `unknown_intent` — operation_name не распознан ни в одной из
  четырёх групп.
