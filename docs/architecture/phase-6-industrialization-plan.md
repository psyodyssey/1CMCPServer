# Phase 6 Industrialization & Completion Plan

## Назначение фазы

Phase 1–5 дали платформе:

- `mcp-read-server` (15 tools) — чтение конфигурации,
  метаданных, кода, журналов, диагностика окружения;
- `mcp-write-server` (23 tools) — контролируемые правки
  через `run_write_flow` (preflight → snapshot → operation
  → verify → audit), включая metadata-level операции
  Phase 3;
- `mcp-intelligence-server` (16 tools) — read-only
  intelligence-tools поверх read/write слоёв;
- продуктовый слой `apps/platform/onec_platform`
  (Phase 5 / Step 2–8) — bootstrap, runtime orchestration,
  health dashboard, guided workflows, rollback / recovery
  / audit UX, real-stand / 1cv8 binary integration track,
  пройденный final integration pass.

Это серьёзное **ядро**. Это **не** ещё **финальный
индустриальный продукт**.

В реальной операторской поверхности всё ещё:

- mutating-путь к **самой инфобазе** упирается в
  Phase 2 stub'ы (`apply_config_from_files`,
  `update_database_configuration`, `create_dump_snapshot`)
  — они проходят через `run_write_flow` со всеми
  гарантиями, но конкретное «применилось ли это в живой
  1С» остаётся за рамками stub-backed эмуляции;
- rollback / recovery — **advisory-only**: нет публичных
  `delete_*` write-tool'ов и нет автоматического
  снимок-restore'а. Operator получает hint, не reverse
  apply;
- установка и запуск всё ещё требуют ручного
  `bootstrap_paths.ps1` + ручного product-config'а +
  ручного запуска runtime-сервисов. Никакого
  release-артефакта (нет `.msi` / wheel / архива с
  installer'ом);
- metadata-операции покрывают object/attribute/form/
  module-level, но `add_form_element`,
  `replace_module_method_body` и подобные patches —
  pragmatic substring/regex, а не настоящее structural
  editing XML/BSL;
- end-to-end на реальном стенде существует как
  controlled binary probe (Step 7 smoke) с одним
  subprocess invocation. Multi-step DESIGNER → BackupCfg
  → DumpCfg → ENTERPRISE round-trip — не делается;
- runtime supervision — pid-based в одном процессе
  оркестратора. Нет watch-and-restart, нет log capture
  с ротацией, нет hot reload;
- enterprise-поверхности (SSO/RBAC, multi-tenant,
  secrets vault, federated audit, policy-as-code,
  multi-instance HA) **нет**;
- operator/admin/developer manuals существуют как
  разделы README, но не как standalone docs/runbooks,
  пригодные для передачи продукта другому человеку
  без сопровождающего инженера.

**Phase 6 — это специально выделенная фаза доведения
продукта до finished / deployable state.** Это
закрытие разрыва между «у нас сильное ядро и
работающий product-layer контур» и «это можно
установить, запустить, использовать, поддерживать и
передать другому человеку как реальный
индустриальный продукт».

Это **не** «ещё один MCP-расширение поверхности» и
**не** ещё один Phase 5-тип обвязки. Phase 6 — про
**завершённость**: real execution вместо stubs,
настоящий rollback вместо hint, короткий setup
вместо bootstrap-ритуала, real-stand validation
вместо synthetic-теста, операторские runbooks вместо
README-секций.

## Целевой результат

К моменту закрытия Phase 6 платформа должна
выдерживать честный пользовательский нарратив:

1. Новый оператор берёт релизный артефакт, проходит
   **короткий** install/setup путь (минимум ручных
   шагов; release packaging задокументирован) и
   получает работающую платформу.
2. Оператор подключает её к реальному 1cv8 binary;
   платформа честно проверяет binary, окружение,
   стенд и **переводит хотя бы один Phase 2 stub-backed
   путь** (`create_dump_snapshot` или
   `apply_config_from_files` или
   `update_database_configuration`) на **реальный
   binary-backed dispatch** через `onec_binary_path` +
   `onec-process-runner`. Stub-режим остаётся как
   honest fallback с явным маркером.
3. Оператор проходит реальный end-to-end сценарий
   против reference stand: setup → bootstrap →
   runtime → guided workflow с реальной mutating
   операцией → verify → audit. Это **smoke level**, не
   полный production round-trip, но это не synthetic
   subprocess.
4. Оператор может реально откатить как минимум
   ограниченный набор операций — automatic rollback
   path хотя бы для **одного** класса write-tool'ов
   (выбирается в Step 4 step-map'а), с явным
   confirm gate, через существующую write-дисциплину
   или её честное эволюционное расширение.
5. Оператор имеет **standalone operator/admin
   manuals** (вне README), пригодные для передачи
   продукта другому инженеру, без необходимости
   приходить к авторам платформы за пояснениями.
6. Runtime supervision: оператор видит логи дочерних
   сервисов, имеет хотя бы базовую restart policy
   (например, по явной operator-команде), и runtime
   UX даёт честные сообщения об ошибках.
7. Phase 1–5 surface не деградировал: read=15,
   write=23+ (если Phase 6 honestly расширил
   metadata coverage), intelligence=16.
8. dev-check зелёный после каждого кодового шага
   фазы.

Закрытие Phase 6 **не** означает, что продукт стал
полностью enterprise-ready (см. «Что НЕ входит в эту
фазу»). Оно означает, что у платформы есть честное
**finished product behavior** на reference stand'е, с
реальной 1cv8-binary связкой хотя бы в одной точке,
исполнимым rollback path, понятным install/setup и
операторскими runbooks.

## Что именно закрывает Phase 6

Опорный стратегический gap list (из задания
Step 1) маппится на Phase 6 следующим образом:

**Закрывается полностью в Phase 6:**

- **(2) Easy installer / setup / release packaging.**
  Block C закрывает: release artifact format,
  install script с короткой последовательностью
  шагов, prereqs validation как первый шаг install'а,
  setup-runbook в operator manual.
- **(7) Operator/admin/developer UX уровня «можно
  отдать другому человеку».** Block F (operator UX
  / docs / runbooks) — это standalone operator
  manual + administrator manual + developer manual
  + user-facing message style guide; не как README
  абзацы, а как документы, по которым реальный
  инженер может работать без авторов.
- **(10) Всё это поверх уже готового ядра, не ломая
  его.** Этот gap фиксируется как guardrail (см.
  ниже): любой кодовый шаг Phase 6 не размывает
  Phase 2–5 safety guarantees, не меняет registries
  без реальной необходимости, не вводит back-door
  write channel.

**Закрывается частично в Phase 6 (приоритезированный
slice):**

- **(1) Реальная 1cv8 binary integration.** Block A
  выбирает **один** Phase 2 stub-backed путь и
  переводит его на binary-backed dispatch через
  `onec_binary_path` + `onec-process-runner`. Stub
  остаётся как honest fallback. Полное замещение
  всех stub'ов на сетку режимов
  `DESIGNER` / `ENTERPRISE` / `DumpCfg` остаётся
  follow-up'ом — Phase 6 ship'ит первый честный
  binary-backed путь и контракт его расширения, а
  не одновременно три полных integration'а.
- **(3) Полная rollback / recovery story.** Block B
  выбирает **один** класс write-tool'ов (наиболее
  безопасный с точки зрения reverse-applicability —
  кандидаты: snapshot-based filesystem restore над
  ограниченными scope'ами / supported delete для
  metadata, выбирается в Step 4) и ship'ит для него
  реально исполнимый rollback path. Полная
  rollback-вселенная для всех write-tool family'й —
  follow-up.
- **(4) Full metadata operation coverage.** Block D
  расширяет coverage точечно (например, добавляет
  один или два недостающих metadata-tool'а или
  fixes одну pragmatic-patching pain point), не
  пытаясь закрыть всю metadata-вселенную сразу.
- **(5) XML/BSL structural editing.** Block D также
  включает один шаг к настоящему structural editing
  (например, минимальный whitelisted DOM-edit для
  одного типа операций); полноценный AST-парсер
  XML/BSL остаётся **вне** Phase 6.
- **(6) Stable real-stand end-to-end.** Block A
  включает один реальный end-to-end сценарий
  (setup → bootstrap → runtime → guided workflow →
  verify) на reference stand. Полная prod-grade
  validation матрица — follow-up.
- **(8) Runtime hardening.** Block E ship'ит лог-capture
  с ротацией, базовую restart policy (хотя бы
  «restart-on-explicit-command» или
  «restart-if-stale»), и более внятный runtime UX.
  Hot reload остаётся вне scope.

**Сознательно выносится за пределы Phase 6:**

- **(9) Enterprise hardening** в полном объёме:
  SSO/RBAC, multi-tenant, secrets vault, federated
  audit storage, policy-as-code, multi-instance HA.
  Block G ship'ит **foundation**: policy-config
  surface (декларативные ограничения), audit
  retention policy, deployment discipline (кто и
  как роняет релиз). Полная enterprise-вселенная —
  отдельная Phase 7+ или enterprise track. Вынесение
  большей части (9) за Phase 6 — сознательное
  решение, иначе фаза станет бесконечной.
- **Полностью автономный агент.** Не задача Phase 6.
- **Web-UI / dashboard frontend.** Не задача Phase 6.
- **AST-парсер XML / BSL** в полноценном объёме.
  Phase 6 включает один точечный шаг к structural
  editing, не AST на всю кодовую базу.
- **Multi-instance HA / federated deployment.**
  Не Phase 6.

## Чем Phase 6 отличается от Phase 1–5

| Phase | Что добавляет | Адресат |
|------|---------------|---------|
| Phase 1 | read MCP surface | агент |
| Phase 2 | write MCP surface + safety primitives | агент |
| Phase 3 | metadata-level write operations | агент |
| Phase 4 | intelligence MCP surface | агент |
| Phase 5 | bootstrap / runtime / dashboard / workflow / recovery / real-stand product layer | человек / команда |
| **Phase 6** | **real 1cv8-backed execution точечно, реальный rollback хотя бы для одного класса, install/setup polish, operator runbooks, runtime hardening, enterprise foundation** | **человек / команда + reference stand** |

Phase 5 поворачивалась лицом к человеку. Phase 6
поворачивается лицом к **законченности продукта на
реальном стенде**. Phase 6 — про **завершение** того,
что Phase 5 декларировала как product layer, до
состояния, в котором продукт реально работает на
живой 1С, реально откатывает хотя бы что-то, и
реально устанавливается без ритуала.

## Крупные продуктовые блоки фазы

Шесть смысловых блоков. Они не равны шагам один-к-одному;
один блок может закрываться несколькими шагами
implementation map (см. `phase-6-step-map.md`), а
часть смежных capability'ов между блоками может
консолидироваться, если это укрепляет продукт.

### A. Real 1cv8-backed execution track

Цель: убрать иллюзию «всё уже работает с 1С» хотя бы в
**одной** точке.

Ключевые направления:

- выбрать **один** Phase 2 stub-backed путь
  (`create_dump_snapshot` / `apply_config_from_files`
  / `update_database_configuration`) для замены на
  binary-backed dispatch;
- зафиксировать **controlled CLI contract** для
  1cv8: какие режимы используются, какие args
  передаются, как читается результат, как ловится
  ошибка, как делается honest fallback на stub
  если binary не задан;
- сохранить write-дисциплину Phase 2: preflight,
  snapshot, operation, verify, audit. Binary-backed
  путь должен **не обходить**, а **удовлетворять**
  существующий `run_write_flow`;
- исполнимый end-to-end сценарий против reference
  stand'а: setup → bootstrap → runtime → guided
  workflow с binary-backed apply → verify → audit;
- честная развилка: при отсутствии `onec_binary_path`
  путь honestly stub'ится как и раньше; при наличии —
  binary-backed dispatch.

### B. Full rollback / recovery track

Цель: перевести rollback assistant из advisory-only в
**реально исполнимый** хотя бы для одного класса
сценариев.

Ключевые направления:

- выбрать кандидатный класс recovery (Step 4
  step-map'а решит конкретику; кандидаты: snapshot-based
  filesystem restore над ограниченным scope'ом
  через `shutil.copytree` обратно с явным confirm;
  введение public `delete_*` write-tool'ов для
  поддержанной inverse-операции; либо комбинация);
- mutating-путь для recovery идёт через **существующую**
  write-дисциплину (или её эволюцию, если новый
  write-tool реально нужен) — никакого back-door
  channel'а в product layer;
- assistant получает реальный supported branch:
  `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist
  пополняется хотя бы одним именем; `mode=executed`
  становится достижимым;
- preview / confirm / blocked / unsupported modes
  Step 6 сохраняются;
- post-rollback verify обязателен, как и для
  forward-apply.

### C. Installer / packaging / operator startup polish

Цель: оператор может пройти короткий install / setup
без бутстрап-ритуала.

Ключевые направления:

- определить **формат релизного артефакта**: zip /
  tar / wheel / standalone-script / git tag — выбор
  фиксируется в Step 3 step-map'а;
- install script с короткой последовательностью
  шагов: проверить prereqs → разместить артефакт →
  сгенерировать starter product-config →
  запустить bootstrap doctor → сообщить статус;
- начальный product-config может быть
  declarative-template (заполняется оператором в
  одном файле) — wizard режим явно остаётся out
  of scope;
- versioning: какая версия платформы у релиза,
  какие версии 1cv8 supported (объявляется как
  contract, а не угадывается);
- documented setup runbook в operator manual.

### D. Metadata completion / structural editing track

Цель: точечно закрыть один или два болезненных gap'а
metadata coverage и сделать **первый честный шаг** от
pragmatic patching к structural editing.

Ключевые направления:

- выбор metadata-tool'а(ов), которые честно нужны
  для product workflow'ов и сейчас отсутствуют или
  ограничены — Step 5 step-map'а решит конкретику.
  Кандидаты: `delete_*` для одного типа объектов
  (что одновременно поддержит block B);
  расширение `replace_module_method_body` на более
  безопасный structural patch; добавление
  `delete_form_element`;
- **минимальный** structural-editing helper для
  одного класса операций (например, для XML — DOM-
  парсинг через `xml.etree.ElementTree` для одного
  whitelisted тега/блока). Полный AST/DOM поверх
  всей XML/BSL вселенной остаётся out of scope;
- сохранение write-дисциплины Phase 2/3:
  preflight, snapshot, verify, audit;
- if расширение write surface происходит — registry
  write-server честно растёт, в отчётах фиксируется.

### E. Runtime hardening / process supervision

Цель: runtime UX становится менее «голым PID-ом» и
более operator-friendly.

Ключевые направления:

- лог-capture для дочерних сервисов: stdout/stderr
  идут в файлы под `<work_dir>/.runtime/logs/<service>/`
  (вместо текущего `DEVNULL`); ротация по размеру
  или по дням;
- базовая restart policy: хотя бы
  `restart-on-explicit-command` (`reload_product_runtime
  --only=<svc>` уже есть; добавить «restart if stale»
  как opt-in флаг);
- более внятный status: дополнительные поля runtime
  state (последний exit code если процесс уже мёртв
  и был известен; PID restart count в текущей
  сессии оркестратора);
- **никакого** automatic-restart-supervisor'а на
  уровне OS (Windows Service / systemd unit) на
  Phase 6 — это отдельный enterprise track;
- log-tailing helper в operator manual.

### F. Operator UX / docs / runbooks

Цель: документация продукта существует **вне** README
как standalone docs, по которым другой инженер может
работать.

Ключевые направления:

- **operator manual** (`docs/operator-manual.md` или
  директория с подшагами): установка, ежедневная
  эксплуатация, типовые сбои, типовые workflow'ы,
  log locations, environment toggling;
- **administrator manual** (`docs/administrator-manual.md`):
  конфигурация окружений, allow_write, retention
  audit, snapshot rotation, security baseline;
- **developer manual** (`docs/developer-manual.md`):
  расширение workflow'ов, добавление новых
  read-tool'ов, contracts intelligence/read/write;
- **user-facing message style guide**: формат
  ошибок, формат статусов, формат подсказок —
  чтобы продукт говорил с оператором consistently;
- runbooks для типовых операций
  (`docs/runbooks/safe-add-attribute.md`,
  `docs/runbooks/rollback-recovery.md`,
  `docs/runbooks/real-stand-smoke.md`) — пошаговые
  инструкции для конкретных сценариев.

### G. Enterprise / production hardening foundation

Цель: заложить foundation, **не** ship'ить полную
enterprise-поверхность.

Ключевые направления:

- declarative policy surface поверх существующего
  `onec-policy-engine`: возможность объявить в
  product-config more granular constraints (e.g.
  «эта operation запрещена на этом окружении») —
  не подменяя existing engine;
- audit retention policy: формальное правило сколько
  audit JSONL хранить, как ротировать (manual либо
  через operator command, не automatic supervisor);
- deployment discipline: документированный путь
  release → install → upgrade → rollback (для
  самой платформы, не для инфобазы), документ
  «как роняется релиз и кто за что отвечает»;
- **что foundation НЕ ship'ит:** SSO/RBAC,
  multi-tenant, secrets vault как сервис, federated
  audit storage, policy-as-code DSL, multi-instance
  HA. Это отдельный enterprise-track после Phase 6.

## Основные guardrails Phase 6

Phase 6 **не** размывает существующие safety
guarantees Phase 2–5. Она только добавляет к ним.

- **Никакого размывания safety guarantees Phase 2–5.**
  `run_write_flow` остаётся единственным путём к
  mutating операциям; preflight + snapshot + verify
  + audit обязательны; intelligence остаётся
  read-only; product layer не превращается в
  back-door write channel.
- **Никакого back-door write channel.** Все
  binary-backed dispatch'и из block A проходят через
  существующий `run_write_flow` (либо его честное
  эволюционное расширение, **не подмену**).
  Recovery executable path block B исполняется через
  существующие public write-tool'ы или их минимальное
  безопасное расширение.
- **Mutating путь только через существующую
  write-дисциплину или её честное эволюционное
  расширение.** Если block D добавляет новый
  write-tool — он наследует contract Phase 2 / Phase 3:
  preflight, snapshot, verify, audit, registry
  registration, dev-check pass.
- **Intelligence остаётся read-only.**
  `mcp-intelligence-server` не получает новых
  mutating-tool'ов и не начинает писать. Никакого
  импорта `onec_policy_engine` ни в intelligence,
  ни в product layer.
- **Fail-closed по умолчанию.** Если binary не
  настроен — block A честно деградирует на stub
  (как Phase 5 / Step 7 делает). Если recovery
  unsupported — assistant возвращает honest
  `mode=unsupported`, не пытается «угадать».
- **Никакой фальшивой enterprise-ready риторики.**
  Ни в коде, ни в README, ни в release notes.
  Block G ship'ит foundation, и так и пишется в
  документации; не «продукт enterprise-ready»,
  а «foundation для enterprise track'а заложен».
- **Честно отделять finished product behavior от
  parallel follow-up / enterprise track.** Каждый
  выпускаемый шаг должен явно указывать: что
  ship'нуто как finished, что остаётся parallel
  track'ом. README и PROJECT-STATUS обязаны это
  отражать.
- **dev-check зелёный после каждого кодового
  шага.** Без compromise.
- **Registry трёх MCP-серверов меняется только при
  реальной необходимости.** Если block D добавляет
  один-два metadata-tool'а — это документируется,
  но никакого «добавил ради расширения surface».
  Чем меньше изменений, тем лучше.
- **Честная развилка stub vs binary-backed.** В
  любом коде block A — два режима: без
  `onec_binary_path` старое stub-поведение
  сохраняется; с `onec_binary_path` включается
  binary-backed; режим явно отражён в payload и
  в documentation.

## Что НЕ входит в эту фазу

Чтобы Phase 6 была закрываемой, а не бесконечной,
явно отсекаем:

- **полный enterprise super-set:** SSO/RBAC,
  multi-tenant, secrets vault как сервис, federated
  audit storage, policy-as-code DSL, multi-instance
  HA, GDPR-compliance audit trail, signed binary
  distribution. Phase 6 ship'ит **foundation**
  только;
- **полностью автономный агент.** Платформа
  продолжает быть инструментом, которым
  пользуется агент или человек. Никакого
  самопринимающего write-решения;
- **полный AST-парсер XML / BSL.** Phase 6 включает
  один точечный structural-editing шаг, не AST на
  всю кодовую базу. Полный AST — отдельный
  технологический track;
- **web-UI / dashboard frontend / workflow UI /
  rollback assistant UI.** Out of Phase 6 scope;
- **полная замена всех Phase 2 stub'ов
  одновременно.** Block A выбирает **один**
  stub-backed путь. Полное замещение —
  parallel track после Phase 6;
- **полная rollback-вселенная.** Block B даёт
  исполнимый rollback **хотя бы для одного**
  класса. Универсальный rollback для всех
  write-tool family'й — parallel track;
- **полное metadata coverage.** Block D — **точечный**
  добор. Полная metadata-вселенная (все
  возможные delete_*, replace_*, refactor_*) —
  parallel track;
- **production MCP transport / `__main__` / CLI у
  read/write/intelligence.** Серверы остаются
  in-process модулями, как это определено
  Phase 5 / Step 3. Production transport —
  отдельный track;
- **hot reload без рестарта процесса.** Out of
  Phase 6 scope;
- **OS-level service supervision** (Windows Service
  / systemd unit). Out of Phase 6;
- **GUI installer / wizard.** Block C ship'ит
  short install script + declarative product-config
  template, не GUI;
- **многосторонний end-to-end на матрице 1С версий
  и стендов.** Block A ship'ит один reference
  stand smoke, не version-matrix.

## Критерии приёмки Phase 6

Phase 6 считается закрытой, когда **все** следующие
условия выполнены. Это не «есть код» — это
проверяемое продуктовое поведение.

1. **Хотя бы один Phase 2 stub-backed путь
   (`create_dump_snapshot` / `apply_config_from_files`
   / `update_database_configuration`) переведён на
   честный binary-backed dispatch** при наличии
   `onec_binary_path`. Stub-режим сохраняется как
   honest fallback при отсутствии binary path. Это
   программно проверяемо: payload write-tool'а
   несёт явный маркер `mode = "stub" | "binary-backed"`
   (или эквивалентное), и при наличии binary path
   реальный subprocess через `onec-process-runner`
   стартует.
2. **Существует исполнимый rollback path хотя бы
   для одного класса write-tool'ов.**
   `_AUTOMATIC_RECOVERY_SUPPORTED` whitelist
   содержит хотя бы одно имя; `run_rollback_assistant`
   с `confirm_execute=True` для этого класса
   достигает `mode=executed`; результат
   verify-проверен; audit row написан.
3. **Установка/запуск по короткому сценарию реально
   сокращены.** Документированный install runbook
   умещается в N коротких шагов (точное N
   фиксируется в Step 3 step-map'а; ориентир — не
   больше 5 ручных шагов от «получил релиз» до
   «boot strap doctor зелёный»). Это
   проверяется тем, что новый оператор, следуя
   только operator manual'у, проходит install/setup
   без необходимости читать исходники.
4. **Хотя бы один end-to-end real-stand сценарий
   проходит** от setup до smoke с реальной
   binary-backed apply (через block A) **в
   контролируемом окружении** (не synthetic). Это
   ловится Step 7 step-map'а; результат — honest
   smoke-pass document с снимком payload'ов и
   оператором-author'ом.
5. **Продукт можно передать другому человеку с
   operator/admin docs.** Существуют как минимум:
   - `docs/operator-manual.md` (или эквивалент);
   - `docs/administrator-manual.md`;
   - `docs/developer-manual.md`;
   - user-facing message style guide;
   - runbooks для базовых сценариев
     (`safe-add-attribute`, `rollback-recovery`,
     `real-stand-smoke`).
   Эти документы существуют **вне README** и
   reference друг друга consistently. Это
   проверяется тем, что инженер, не работавший с
   платформой ранее, может пройти один workflow
   end-to-end по docs.
6. **read/write/intelligence не деградировали.**
   Read=15 (или больше, если block D расширил read
   surface — что **не предполагается**, но
   фиксируется честно), write=23+ (если block D
   добавил metadata-tool'ы), intelligence=16 (без
   изменений — это hard guarantee). Программно
   проверяемо через `list_tools()` каждого сервера.
7. **dev-check зелёный после каждого кодового шага
   фазы** (Step 2–8). Без compromise. Программно
   проверяется через `scripts/dev/run_dev_check.ps1`.
8. **Safety guarantees Phase 2–5 сохранены.** Никакого
   silent apply; никакого обхода `run_write_flow`;
   никакого back-door write channel в product
   layer; никакого импорта `onec_policy_engine` ни
   в intelligence-server, ни в `onec_platform`.
   Программно проверяемо через grep на каждом шаге.
9. **Honest fallback дисциплина.** Любой шаг, где
   binary / runtime / recovery недоступен,
   деградирует через honest finding'и (как Phase 5
   уже делает), не через silent skip и не через
   fake success.
10. **Документированные ограничения честны.** Каждый
    кодовый шаг (Step 2–8) явно указывает в README /
    PROJECT-STATUS / step-map: что именно ship'нуто,
    какие части parallel-track'ом остались, какие
    MVP-компромиссы сделаны. Без enterprise-ready
    риторики там, где есть только partial
    implementation.

При невыполнении любого из критериев Phase 6 не
закрывается; вместо этого открывается дополнительный
follow-up step внутри той же фазы (как делалось в
Phase 2 / Step 10, Phase 3 / Step 7, Phase 4 / Step 7,
Phase 5 / Step 8 — все были «closing pass»-style).

## Связь с предыдущими фазами

- **Phase 1 (read MVP)** — фундамент для health
  dashboard, environment doctor, read-only сегментов
  workflow'ов. Phase 6 не переписывает read-tool'ы;
  максимум использует их.
- **Phase 2 (write MVP)** — `run_write_flow` остаётся
  единственным путём к mutating операциям. Block A
  расширяет один stub-backed путь до binary-backed
  **внутри** `run_write_flow`, не подменяя его.
- **Phase 3 (metadata changes)** — block D точечно
  добавляет metadata-tool'ы по тому же contract'у:
  preflight + snapshot + verify + audit. Тонкий
  helper-слой `runtime/metadata_ops.py` остаётся
  source-of-truth для XML/BSL fragment-операций.
- **Phase 4 (intelligence layer)** — Phase 6 **не
  трогает** intelligence registry. Все 16 tool'ов
  остаются. Никаких новых intelligence-tool'ов;
  никаких mutation-эффектов; никакого
  `onec_policy_engine`-импорта.
- **Phase 5 (product layer)** — Phase 6 строится
  **поверх** product layer'а:
  - block A модифицирует write-tool'ы и/или
    `realstand` boundary, но product layer
    boundaries (`bootstrap`, `runtime`,
    `dashboard`, `workflow`, `recovery`,
    `realstand`) сохраняют свой external contract;
  - block B расширяет recovery whitelist;
  - block C добавляет install-helper'ы (возможно в
    `apps/platform/`);
  - block D / E / F / G работают по тому же
    принципу: продуктовый слой не ломается, а
    дополняется.

## Открытые вопросы Step 1 (для Step 2 step-map'а)

Этот раздел существует, чтобы Step 2 не начался с
пустого листа. Перечень открытых вопросов, которые
нужно решить в ходе Phase 6:

- **Какой именно Phase 2 stub-backed путь** будет
  переведён на binary-backed dispatch первым.
  Кандидаты: `create_dump_snapshot` (наиболее
  изолированный, обратимый),
  `apply_config_from_files` (наиболее ценный
  product-wise), `update_database_configuration`
  (наиболее опасный — оставить последним).
  Решение в Step 2 step-map'а.
- **Контракт 1cv8 CLI:** какие режимы вызываются,
  какой timeout фиксируется (Phase 5 / Step 7 имеет
  fixed 30s — для apply, вероятно, нужен больший
  cap), как ловится ошибка при non-zero exit.
- **Формат релиза:** zip / tar / wheel / git tag /
  standalone-script. Решение в Step 3 step-map'а.
- **Какой класс recovery** будет ship'нут как первый
  supported. Кандидаты: snapshot-based filesystem
  restore (через `shutil.copytree` обратно с
  confirm); supported `delete_catalog_attribute` +
  `add_*` reverse path; либо комбинация.
- **Какие metadata-tool'ы** добавляются в block D
  (или ни одного, если block B покрыт без
  расширения write surface).
- **Формат лог-файлов** runtime services: один файл
  на сервис или per-day rotation; какой parser
  использует operator manual.
- **Уровень structural editing** в block D: только
  один whitelisted DOM-edit или базовый XML DOM
  helper для нескольких операций.
- **Глубина enterprise foundation** в block G:
  policy-config surface как dataclass или как
  отдельный config файл; audit retention как
  manual command или как scheduled rotation.

Эти вопросы фиксируются здесь намеренно: Step 1 не
делает вид, что ответы уже найдены.
