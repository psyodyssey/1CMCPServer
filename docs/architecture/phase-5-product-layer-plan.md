# Phase 5 Product Layer Plan

## Назначение фазы

Phase 1–4 дали платформе полное **инженерное ядро**:

- `mcp-read-server` (15 tools) умеет собрать конфигурацию,
  метаданные, код, журналы, выполнить read-query и
  диагностику окружения.
- `mcp-write-server` (23 tools) умеет вносить ограниченные и
  аудируемые правки через единый `run_write_flow` — preflight
  → snapshots → operation → verify → audit, включая
  metadata-level операции Phase 3.
- `mcp-intelligence-server` (16 tools) умеет рассуждать о
  конфигурации поверх read/write слоёв в read-only режиме —
  dependency / impact / diagnostics / recommendations.

Эти три сервера решают инженерную задачу. Они **не** решают
**продуктовую**.

Сегодняшнее состояние можно честно описать так: «есть очень
мощный конструктор из исходников, который инженер с рабочей
станцией способен запустить локально и которым может
пользоваться агент по MCP-контракту». Этого недостаточно.
Чтобы платформа стала продуктом, она должна:

- ставиться по короткому понятному сценарию, а не «склонируйте
  репо, добавьте PYTHONPATH, прочитайте seven-step bootstrap
  скрипт»;
- запускаться как согласованный, наблюдаемый набор сервисов;
- иметь руководство оператора, разработчика и
  администратора — не как `README.md`-обрывки, а как
  системную поверхность;
- иметь end-to-end сценарии, которые не требуют от пользователя
  вручную выстраивать цепочку из десятков tool-вызовов;
- иметь rollback и recovery как один цельный продуктовый
  capability, а не как набор низкоуровневых примитивов;
- иметь честный путь от MVP-stub'ов Phase 2 (apply / update-db /
  dump snapshot) к настоящей `1cv8`-интеграции;
- держать read/write/intelligence safety guarantees на всём
  пути.

**Phase 5 — это переход от «есть набор серверов и tool'ов» к
«это можно поставить, поднять, подключить к 1С, безопасно
использовать, сопровождать, откатывать, диагностировать и
выдать другому человеку или команде как продукт».**

Phase 5 — **не «ещё несколько tool'ов»**. Это слой, который
собирает уже готовые серверы в продукт. Никакой новый MCP tool
сам по себе цели Phase 5 не достигает; добавление tool'а
оправдано только тогда, когда оно нужно для одного из
продуктовых блоков, описанных ниже.

## Целевой результат

К моменту закрытия Phase 5 платформа должна выдерживать
следующий честный пользовательский нарратив, без скрытой
ручной возни:

1. Новый пользователь получает релизный артефакт платформы
   (clone + lockfile, либо упакованный installer-скрипт — на
   выбор Phase 5 / Step 1) и проходит **короткий**, описанный
   шагами setup-flow. Setup проверяет prereqs (Python, путь
   к 1cv8, сетевые доступы, права на dump_path) и либо
   успешно завершается, либо честно объясняет, что не
   найдено.
2. Пользователь конфигурирует **окружение** через единый
   product-уровневый конфиг (имя окружения, base_path,
   publication, dump_path, http_base_url, allow_write).
   Окружений может быть несколько одновременно (local-dev /
   stage / prod-readonly).
3. Пользователь запускает платформу одной точкой входа
   (`platform up` / `platform start` — конкретное имя
   фиксируется в Step 1). После запуска у него поднят
   согласованный набор: read-server, write-server,
   intelligence-server, плюс соответствующие health-сигналы.
4. Пользователь видит **environment doctor / preflight
   dashboard**: статус каждого окружения, статус каждого
   сервера, статус 1cv8, статус dump'а, список known issues с
   их `health_codes`. Никакой магии — все статусы трассируются
   до уже существующих read/intelligence tool'ов.
5. Пользователь запускает **guided workflow**: например,
   «добавить реквизит к справочнику с проверкой влияния и
   откатом». Workflow внутри сам собирает корректную
   последовательность intelligence + write вызовов
   (`estimate_change_impact` → `find_affected_forms` →
   `check_write_preconditions` → `create_backup_snapshot` →
   `create_dump_snapshot` → `add_catalog_attribute` →
   `verify_attribute_exists` → audit), показывает их
   пользователю и ждёт явного подтверждения. **Silent apply
   запрещён.**
6. Если что-то пошло не так — пользователь видит **rollback
   assistant**, который показывает последнюю операцию (через
   уже существующий `describe_last_write_operation`) и
   предлагает honest recovery path с явным указанием, что
   именно будет восстановлено и из какого snapshot'а.
7. Пользователь имеет **operator manual / admin manual**, в
   котором описаны: установка, конфигурация, верификация,
   обновление, откат, безопасность, troubleshooting.
   Документация — обязательная часть продукта, не «опционально».
8. На реальном стенде с реальной 1cv8 binary платформа
   проходит честный end-to-end smoke test (как минимум —
   create_common_module + add_catalog_attribute + verify), и
   этот smoke test описан как воспроизводимый сценарий.

Это и есть «продуктовое состояние Phase 5».

## Что именно закрывает эта фаза

Опорный список незакрытых продуктовых разрывов (из задания
Step 1) маппится на Phase 5 следующим образом:

**Закрываются полностью в Phase 5:**

- (1) нет законченного runtime/deployment слоя как продукта —
  закрывается blocks A + B (installer/bootstrap + runtime
  orchestration);
- (3) нет простого установщика / удобного развёртывания —
  закрывается block A (installer/bootstrap layer);
- (6) нет автоматического rollback как законченной
  продуктовой функции — закрывается block D (rollback /
  recovery / audit UX) поверх уже существующих
  `describe_last_write_operation` /
  `prepare_rollback_hint` / snapshot-инструментов Phase 2;
- (7) intelligence layer уже есть как фаза, но ещё не собран
  в продуктовый UX — закрывается blocks C + F (workflow
  layer и operator UX);
- (8) нет product/workflow layer — закрывается block C
  (safe workflow layer);
- (9) нет стабильной end-to-end работы на реальном стенде
  как продукта — закрывается block E (real-stand /
  enterprise hardening) на уровне «есть честный smoke
  test», полная prod-готовность остаётся enterprise
  follow-up (см. ниже).

**Закрываются частично:**

- (2) нет реальной интеграции с 1cv8 binary — Phase 5
  вводит binary integration **track** в block E:
  фиксируется, что stub'ы Phase 2 (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`)
  имеют явный путь до настоящего `1cv8`, описаны их
  invariants и есть smoke test против реальной binary в
  контролируемом окружении. **Полное замещение всех
  stub'ов** на сетку реальных режимов `DESIGNER` /
  `ENTERPRISE` / `DumpCfg` остаётся продуктовым track'ом
  после Phase 5 — слишком большой по объёму, чтобы быть
  одним под-шагом;
- (4) нет полного покрытия metadata operations — Phase 3
  закрыла object/attribute/form/module level. Phase 5 не
  расширяет write surface намеренно; **расширение** покрытия
  (например, full document type system,
  information-register full spec, role spec) остаётся
  parallel-track'ом и не блокирует выпуск продукта;
- (5) нет полного structural editing XML/BSL —
  intelligence-tools уже честно отделяют confirmed (XML
  card / BSL substring) от presumed (substring/regex). Phase 5
  не вводит AST-парсер; задача структурного редактирования
  остаётся вне продуктовой границы Phase 5.

**Остаются как enterprise / follow-up track (не входит в
Phase 5):**

- (10) enterprise hardening — полноценная enterprise
  поверхность (SSO/RBAC мульти-арендный режим, secrets
  vault, policy as code, multi-instance HA, federated
  audit storage) — отдельный enterprise-track после
  закрытия Phase 5. Phase 5 фиксирует **базовые** safety
  гарантии и **не размывает** уже существующие. Полная
  enterprise-история — за рамками этой фазы.

В этой фазе мы не пытаемся одновременно «дописать всё
оставшееся». Цель — сделать платформу **выдаваемым продуктом**
для типичного 1С-инженера / типичной команды разработки на
типичном стенде. Enterprise scope получает свой путь после.

## Чем Product Layer отличается от Phase 1–4

| Phase | Что добавляет | Кто пользуется |
|------|---------------|---------------|
| Phase 1 | read MCP surface | агент |
| Phase 2 | write MCP surface + safety primitives | агент |
| Phase 3 | metadata-level write operations | агент |
| Phase 4 | intelligence MCP surface | агент |
| **Phase 5** | **установка, запуск, конфигурация, workflows, rollback, реальный стенд, документация оператора** | **человек / команда** |

Phase 1–4 расширяли поверхность для **агента**. Phase 5
впервые серьёзно поворачивается лицом к **человеку**, который
ставит, конфигурирует, запускает, сопровождает и откатывает
систему. Это смена адресата.

Поэтому Phase 5:

- работает поверх уже существующего read/write/intelligence
  surface, **не** расширяя tool-set ради расширения;
- добавляет небольшой набор продукт-уровневых компонентов
  (installer, doctor, runner, workflow runner, rollback
  assistant), которые **внутри себя** дёргают существующие
  tools;
- вводит обязательную документацию как продукт;
- вводит реальный стенд как обязательный artifact, а не
  как демо.

## Крупные продуктовые подсистемы фазы

Шесть смысловых блоков. Они не равны шагам — один блок может
закрываться несколькими шагами implementation map (см.
`phase-5-step-map.md`), а часть смежных capability'ов между
блоками может консолидироваться, если это укрепляет продукт.

### A. Installation / bootstrap layer

Устанавливает платформу и приводит её в работоспособное
состояние.

Цель: новый пользователь должен пройти install по короткому,
понятному, fail-closed сценарию, а не разбираться в
PYTHONPATH вручную.

Ключевые направления:

- единый installer / setup flow (скрипт + документ);
- проверка prereqs: Python ≥ 3.11, доступ к 1cv8 binary
  (если требуется), сетевые доступы до publication-URL,
  права на `dump_path`, версия ОС;
- bootstrap проекта: создание / валидация product-config,
  создание рабочих директорий, начальный health-snapshot;
- режимы установки: **local-dev** (одна машина, без 1cv8 на
  этом этапе), **stand** (контролируемый стенд с
  реальной 1cv8), **enterprise-bootstrap-only** (минимально
  жизнеспособная инсталляция, дальнейшая doc-страница
  объясняет hand-off в enterprise track).

### B. Runtime orchestration layer

Поднимает и держит согласованный набор серверов.

Цель: не «руками открыть три PowerShell-окна и в каждом
запустить свой сервер», а одна точка входа, поднимающая
read + write + intelligence как один связный runtime.

Ключевые направления:

- единый runner / lifecycle: start / stop / status / reload,
  с явным выводом, какой сервер чем занят;
- environment profiles: каждое окружение из product-config
  получает запускаемый профиль; для prod профиля
  `allow_write` остаётся `False` по умолчанию;
- product-уровневый health dashboard: агрегирует
  `health_summary`, `check_runtime_health`,
  `analyze_runtime_issue` — но **не** дублирует их, а
  собирает в один читаемый снимок;
- preflight orchestration: до старта проверяется prereqs +
  целостность product-config + достижимость dump_path и
  publication URL — fail-closed.

### C. Safe workflow layer

Превращает наборы tool-вызовов в guided user-facing
workflows.

Цель: пользователь не должен ставить руками семь tool'ов в
правильном порядке. Workflow ставит их сам, показывает план,
требует подтверждения, никогда не применяет молча.

Ключевые направления:

- 2–3 базовых end-to-end workflow на старте Phase 5: пример
  набора — **«добавить реквизит безопасно»**, **«добавить
  метод в модуль безопасно»**, **«проверить здоровье
  стенда»**. Конкретный набор фиксируется в Step 1 / Step 5
  step-map'а;
- workflow внутри собирает план через
  `suggest_safe_change_order` / `suggest_metadata_patch_plan`
  и явно показывает пользователю предложенную
  последовательность;
- workflow всегда проходит через preflight + snapshots +
  verify + audit (никаких обходов `run_write_flow`);
- silent apply запрещён: пользователь должен явно
  подтвердить план;
- workflow деградирует честно: если intelligence-step не
  смог дать план — workflow не запускается «на удачу», а
  отдаёт честный fail-closed.

### D. Rollback / recovery / audit UX

Делает rollback цельным capability'ом, а не набором
примитивов.

Цель: пользователь должен видеть «вот что произошло, вот
куда мы можем откатиться, вот цена отката, нажмите для
подтверждения».

Ключевые направления:

- история операций: один читаемый список последних
  write-операций (поверх уже существующего audit JSONL и
  `describe_last_write_operation`);
- rollback assistant: показывает последнюю операцию,
  доступные snapshot'ы, последствия отката, и при явном
  подтверждении исполняет восстановительный workflow
  (recovery — это тоже workflow из block C, не отдельный
  silent apply);
- recovery path для типовых сбоев (сбой apply, сбой
  verify, сбой update-db) — описан как сценарий, не как
  «откройте audit и прочитайте JSON»;
- audit review UX: средство просмотра / фильтрации
  audit-trail (по operation_id, по environment, по статусу).

### E. Real-stand and production-readiness track

Закрывает разрыв между «локально проходит dev-check» и
«это работает на реальном стенде».

Цель: иметь воспроизводимый stand, на котором smoke test
проходит на настоящей 1cv8 binary, и понятный список
ограничений «куда мы пока не готовы».

Ключевые направления:

- описание standard reference stand'а: версия 1С, версия
  Windows, сетевая топология, права;
- 1cv8 binary integration **track**: явный путь от Phase 2
  stub'ов (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`)
  к реальным режимам `DESIGNER` / `ENTERPRISE` / `DumpCfg`,
  в виде описанного контракта и smoke-теста — но **не**
  обязательное полное замещение всех stub'ов в одной
  фазе;
- end-to-end smoke test на реальном стенде (минимум:
  create_common_module + add_catalog_attribute +
  verify_*); описан как сценарий, который должен пройти
  перед релизом;
- packaging: формат релиза (zip / git tag / wheel /
  installer-скрипт — фиксируется в Step 1);
- versioning / compatibility expectations: какие версии
  1cv8 поддерживаются, что считается breaking change;
- minimal hardening: фиксация safety guarantees Phase 2–4
  (никакого silent prod write, обязательные snapshots,
  обязательный verify, обязательный audit) на уровне
  product-config.

### F. Operator UX / docs layer

Документация и user-facing surface как часть продукта.

Цель: продукт нельзя сдавать без manuals. Документация —
обязательная подсистема Phase 5, а не follow-up.

Ключевые направления:

- **operator manual** — установка, конфигурация, лог,
  диагностика, типовые сбои, contacts;
- **developer manual** — расширение workflow'ов, добавление
  собственных read/intelligence-инструментов в локальной
  установке, contract intelligence/read/write;
- **administrator manual** — управление окружениями,
  policy/allow_write, rotation snapshot'ов, retention
  audit, безопасность;
- guided diagnostics UX: связки health → analyze_runtime_issue
  → suggest_fix_for_issue → operator manual section,
  показанные одним сообщением;
- предсказуемые статусы и понятные ошибки: единый формат
  user-facing messages (не «трейсбэк наружу», а honest
  фразы со ссылкой на manual section).

## Набор продуктовых capability'ов фазы

Это не «новые public MCP tools». Это **продуктовые
capabilities** — компоненты, ощущаемые пользователем. Каждый
из них собирается из уже существующих read/write/intelligence
tool'ов или small product-уровневых обвязок над ними.
Конкретные имена компонентов фиксируются в соответствующих
Steps step-map'а.

### Installation / bootstrap (block A)

1. **Installer / setup flow** — единый воспроизводимый
   сценарий установки (script + manual section), с
   prereqs check и fail-closed диагностикой.
2. **Setup wizard / config initializer** — генерация
   product-config: окружения, dump_path, publication,
   binary, allow_write defaults; интерактивный или
   декларативный (выбор фиксируется в Step 1).
3. **Prereqs doctor** — отдельный compound check над
   Python-runtime / сетью / 1cv8 / правами; читает
   product-config, опирается на `health_summary` и
   `check_runtime_health`.

### Runtime orchestration (block B)

4. **Platform runner** — единая точка входа start / stop /
   status / reload; знает все три сервера и запускает их
   как согласованный набор.
5. **Environment profile manager** — управление multi-env
   product-config'ом (local-dev / stand / prod-readonly);
   каждый profile несёт свои allow_write, dump_path,
   publication, http_base_url.
6. **Health dashboard** — агрегированный снимок,
   собирающий `health_summary` (read-server),
   `check_runtime_health` (read-server),
   `analyze_runtime_issue` (intelligence-server) в одно
   читаемое представление; не вводит новый MCP tool, а
   собирает готовые.

### Safe workflow layer (block C)

7. **Workflow runner** — исполнитель guided workflow'ов;
   единое место, через которое любая user-facing
   последовательность tool-вызовов проходит preflight +
   план + подтверждение + verify + audit.
8. **Workflow: safe-add-attribute** — конкретный
   end-to-end workflow «добавить реквизит безопасно»
   (impact → план → backup → snapshot → write → verify →
   audit). Использует
   `estimate_change_impact`, `find_affected_forms`,
   `add_catalog_attribute` или `add_document_attribute`,
   `verify_attribute_exists`.
9. **Workflow: safe-add-module-method** — добавить метод
   в модуль безопасно. Использует
   `find_module_method_usages`, `append_module_method`,
   `verify_module_contains`.
10. **Workflow: stand-health-check** — комплексный
    health-чек стенда; не пишет, использует
    `analyze_runtime_issue` + `summarize_configuration_risk`
    + `prepare_intelligence_report`. Это пример **read-only
    workflow**, важный как образец для не-mutating user
    tasks.

### Rollback / recovery / audit (block D)

11. **Operation history viewer** — список последних
    write-операций (operation_id, tool_name, environment,
    status, время) поверх уже существующего audit JSONL
    и `describe_last_write_operation`.
12. **Rollback assistant** — показ конкретной операции,
    список доступных snapshot'ов, цена отката, явное
    подтверждение, исполнение recovery workflow'а через
    workflow runner. Опирается на
    `prepare_rollback_hint` и существующие snapshot-tool'ы
    Phase 2.
13. **Recovery workflow** — описанный сценарий восстановления
    после типового сбоя (сбой apply / сбой verify); живёт
    как workflow в workflow runner, не как silent apply.

### Real-stand / hardening (block E)

14. **Reference stand spec** — документ, описывающий
    эталонный стенд (версии 1С, ОС, сеть, права), и
    воспроизводимый smoke test; обязателен для релиза.
15. **1cv8 binary integration contract** — явное описание
    границы между MVP-stub'ами Phase 2 и реальной
    `1cv8`-бинарью; описание команд / режимов /
    invariants; минимальный smoke-test against real
    binary в контролируемом окружении. Полный
    обязательный замещающий пас остаётся track'ом после
    Phase 5.
16. **Release packaging spec** — формат релиза (clone +
    lockfile / zip / wheel / installer-скрипт), versioning
    contract, compatibility expectations.

### Operator UX / docs (block F)

17. **Operator manual** — установка, эксплуатация,
    диагностика, типовые сбои.
18. **Administrator manual** — окружения, allow_write,
    rotation snapshot'ов, retention audit, безопасность.
19. **Developer manual** — расширение workflow'ов и
    локальное встраивание собственных инструментов.
20. **User-facing message style guide** — единый формат
    статусов и ошибок (для всех точек, где платформа
    говорит с человеком).

19–20 — обязательные artifacts, не «приятные дополнения».
Без них продукт не считается выдаваемым.

## Основные guardrails Phase 5

Phase 5 **не** размывает существующие safety guarantees
Phase 2–4. Она только добавляет к ним продукт-уровневые.

- **Запрет production write by default.** Любой product-config,
  не помеченный явно как allow_write, обращается с
  write-server'ом в режиме «верифицировать, но не применять».
  Это поведение наследуется из Phase 2 и Phase 5 его
  закрепляет.
- **Обязательное явное targeting окружения.** Любая
  product-уровневая команда (installer, runner, workflow,
  rollback) принимает имя окружения **явно** или
  fail-closed. Никаких «по умолчанию prod».
- **Никакого silent apply.** Ни один workflow не запускает
  mutating операцию без отдельного, явного подтверждения от
  пользователя. План показывается до подтверждения, после
  подтверждения — выполняется и логируется.
- **Install / upgrade / rollback — только с диагностикой.**
  Любая из этих операций обязана выдать понятный статусный
  payload (что произошло, что не получилось, что делать
  дальше). Молча падать запрещено.
- **Fail-closed при неполных prereqs.** Если doctor / setup
  не нашёл нужный binary, dump_path или сеть — installer
  не «угадывает», а останавливается с честным сообщением.
- **Честная деградация, а не «магия».** Если
  intelligence-tool вернул `ok=False` или пустой результат —
  workflow / dashboard показывает это как есть, а не
  заменяет тихим заглушкой.
- **Продуктовый UX не должен размывать safety guarantees
  Phase 2–4.** Никаких обходов `run_write_flow`. Никаких
  обходов audit. Никаких обходов snapshot'ов. Никаких
  intelligence-tool'ов, которые внезапно начинают что-то
  писать. Никакого импорта `onec_policy_engine` в
  intelligence-server.
- **Конфиг — единый источник истины.** Несколько копий
  настроек в разных местах запрещены. Product-config — один.
- **Cross-app направление сохраняется.** Cross-app import
  по-прежнему только: write → read; intelligence → read,
  intelligence → write через pure helpers; product layer
  → read / write / intelligence напрямую (через MCP-вызовы
  или внутренние tool registries), но **не** наоборот.

## Что не входит в эту фазу

Чтобы Phase 5 была закрываемой, а не бесконечной, явно
отсекаем:

- **fully autonomous agent.** Платформа продолжает быть
  инструментом, которым пользуется агент или человек.
  Никакого самопринимающего решения «применил без подтверждения,
  потому что был уверен»;
- **magical self-healing production.** Никакого автоматического
  восстановления prod-инфобазы. Recovery остаётся явным
  user-confirmed workflow'ом;
- **бесконечная оркестрация всего подряд.** Workflow layer
  фиксирует **2–3 базовых** end-to-end сценария на старте
  Phase 5. Остальные — после, по мере необходимости;
- **полная замена 1С-администрирования.** Платформа — про
  configuration / metadata / code workflows, не про SQL-
  администрирование, не про backup кластера, не про
  репликацию;
- **enterprise-всё-в-одном за один шаг.** SSO/RBAC,
  multi-tenant, secrets vault, federated audit storage,
  policy-as-code, multi-instance HA — отдельный
  enterprise-track после Phase 5;
- **полное замещение всех Phase 2 stub'ов настоящей
  1cv8-бинарью.** Phase 5 фиксирует контракт интеграции и
  smoke test, но **не** обязана полностью переписать все
  stub'ы в одной фазе. Остаток — продуктовый track после
  Phase 5;
- **AST-парсер XML/BSL.** Не вводится в Phase 5; это
  отдельный технологический track. Substring + regex Phase 4
  остаются базой;
- **новые большие подсистемы вне списка из шести блоков.**
  Phase 5 не превращается в «давайте заодно сделаем»;
- **рефакторинг read/write/intelligence ради продукта.**
  Если для продуктового слоя нужна точечная правка в
  существующем сервере — она оформляется как минимальная,
  локальная и доказуемо безопасная (как было в Phase 2 /
  Step 10 и Phase 3 / Step 7). Большой рефакторинг
  откладывается.

## Критерии приёмки Phase 5

Phase 5 считается закрытой, когда **все** перечисленные
условия выполняются. Это продуктовые критерии: не «есть
код», а «продукт ведёт себя так».

1. **Установка возможна по короткому понятному сценарию.**
   Описан и воспроизведён installer / setup flow; новый
   пользователь, следуя инструкции, доходит до рабочего
   состояния либо до честного fail-closed reason'а.
2. **Платформа поднимается как согласованный набор
   сервисов.** Одна точка входа поднимает read + write +
   intelligence; статус виден.
3. **Есть как минимум 2–3 end-to-end user workflows.**
   Каждый workflow внутри собирает преflight + план +
   подтверждение + verify + audit; ни один не обходит
   `run_write_flow`.
4. **Rollback / recovery path реально существует как
   продуктовый сценарий.** Пользователь может в одной
   поверхности увидеть последнюю операцию, выбрать
   snapshot, откатиться с явным подтверждением.
5. **Реальный стенд / реальная интеграция имеют явный
   трек готовности.** Описан reference stand; описан
   1cv8 integration contract; есть smoke test против
   реальной binary; знаемые ограничения честно
   зафиксированы.
6. **Документация существует как продукт.** Operator
   manual, administrator manual, developer manual, user-
   facing message style guide — присутствуют и
   согласованы. Не «как-нибудь потом».
7. **dev-check остаётся зелёным на всех шагах.**
8. **read-server (15 tools), write-server (23 tools),
   intelligence-server (16 tools) не деградировали.**
   Ни в количестве, ни в семантике (failure-style,
   confirmed/presumed, sources_used).
9. **Read-only контракт intelligence-server сохранён.**
   `onec_policy_engine` по-прежнему не импортируется в
   intelligence-server; продуктовые workflow'ы не
   превращают intelligence-tool в писатель.
10. **Safety guarantees Phase 2–4 не размыты.** Никакого
    silent prod write; никакого обхода audit; никакого
    обхода snapshot'ов.
11. **Продукт ощутимо ближе к «готовому к выдаче
    пользователю».** Это субъективный критерий, но
    проверяется честным внешним выполнением сценариев
    из manuals: установить, поднять, пройти один
    workflow, увидеть rollback, выключить.

При невыполнении любого из критериев Phase 5 не
закрывается; вместо этого открывается follow-up step
внутри той же фазы.

## Связь с предыдущими фазами

- **Phase 1 (read MVP)** даёт фундамент для health
  dashboard, environment doctor и read-only сегментов
  workflow'ов. Никакие read-tool'ы не переписываются.
- **Phase 2 (write MVP)** даёт `run_write_flow`,
  preflight, snapshots, verify, audit. Все mutating
  workflow'ы Phase 5 проходят через него; product layer
  его не дублирует.
- **Phase 3 (metadata changes)** даёт object/attribute/
  form/module-level write surface. Workflow runner
  использует именно эти tool'ы; никакие из них не
  расширяются ради продукта без отдельного решения.
- **Phase 4 (intelligence layer)** даёт impact analysis,
  recommendations, troubleshooting. Workflow runner и
  health dashboard используют именно эти tool'ы; никакой
  intelligence-tool не превращается в writer.

Phase 5 строится **поверх** этого, а не **вместо** этого.

## Открытые вопросы Step 1 (для Step 2 step-map'а)

Этот раздел существует, чтобы Step 2 не начался с пустого
листа. Перечень открытых вопросов, которые нужно решить в
ходе Phase 5 (по мере прохождения шагов step-map'а):

- **Формат релиза.** Clone + lockfile vs упакованный
  installer vs wheel vs архив. Решение в Step 1
  step-map'а.
- **Формат product-config.** YAML vs TOML vs JSON.
  Учитывая, что в проекте уже есть `pyproject.toml` и
  `EnvironmentConfig` через `onec-config` — выбор
  стремится в сторону единства, но фиксируется явно.
- **Транспорт MCP.** Сегодня сервера живут как
  in-process модули. Решение, какой транспорт
  выставлять наружу для product runner'а (stdio vs
  TCP vs локальный socket) — отдельный вопрос Step 3
  step-map'а.
- **Интерактивный setup vs декларативный.** Setup wizard
  может быть интерактивным (вопрос-ответ) или
  декларативным (положите готовый product-config).
  Решение в Step 2 step-map'а.
- **Storage operation history.** Где хранить читаемую
  history list — отдельный JSON-индекс над audit JSONL
  или вычислять «на лету» при каждом запросе. Решение
  в Step 6 step-map'а.
- **Глубина 1cv8-integration в smoke test.** Какие
  именно workflow'ы обязательны для smoke test
  («только create_common_module + verify» или больше).
  Решение в Step 7 step-map'а.

Эти вопросы фиксируются здесь намеренно: Step 1 не делает
вид, что ответы уже найдены.
