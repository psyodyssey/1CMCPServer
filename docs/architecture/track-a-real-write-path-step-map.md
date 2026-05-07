# Parallel Track A — Real Write Path Step Map

Стартовая карта **Parallel Track A — Full Real 1cv8-backed
Write Path**. Семь шагов. Карта ведёт продукт от закрытой
Phase 6 (где `apply_config_from_files` /
`update_database_configuration` остались Phase 2 stub'ами, а
`create_dump_snapshot` имеет partial generic binary-backed
slice) к **finished real-write behavior** на reference
stand'е.

Это **не** новая фаза. Это **post-Phase-6 completion track**,
открытый именно после честного закрытия Phase 6 на Step 9 final
integration pass'е. Здесь нет ни нового MCP tool surface, ни
нового product-layer slice'а ради surface'а — здесь точечное
доведение существующего write-core до finished behavior.

Каждый шаг описан в едином формате:

- **Цель** — что именно должно стать правдой по результату
  шага.
- **Что меняем** — какие подсистемы / документы / артефакты
  меняются. Step 1 — документационный (никакого кода).
  Шаги 2–7 могут писать код, но строго в рамках уже
  наработанной архитектуры Phase 1–6 и без размывания её
  safety guarantees.
- **Затронутые зоны** — границы шага в репозитории.
- **Результат** — какой именно критерий приёмки трека шаг
  закрывает (полностью или частично) и что меняется в
  registries (default — ничего).

Логика трека: **сначала контракт трека и открытые вопросы**
(Step 1), затем **первый из двух stub-backed-путей переводится
на real binary-backed** (Step 2), затем **второй**
(Step 3), затем **унификация / нормализация
`create_dump_snapshot` real path'а + общий payload-контракт**
(Step 4), затем **product-layer integration** через
существующие boundary'и (Step 5), затем **reference stand
multi-step round-trip** (Step 6), затем **закрывающий
integration pass и фиксация закрытия трека** (Step 7). После
Step 7 Track A закрывается; никакого Step 8 не запланировано
(в отличие от Phase 6, у которой было 9 шагов из-за более
широкого scope'а).

Track A **не претендует** на enterprise-вселенную, AST-парсер,
web-UI, packaging ecosystem, full version-matrix, или новый
MCP tool surface. Любая правка существующих серверов
оформляется как минимальная и локальная — по аналогии с
Phase 6 / Step 2 (где `create_dump_snapshot` был расширен
binary-backed branch'ем без добавления нового tool'а).

## Step 1

**Planning Full Real 1cv8-backed Write Path — documentation
entry.**

- **Цель.** Зафиксировать документационный вход в Track A:
  назначение трека, целевой результат, что закрывает трек
  и что НЕ закрывает, чем отличается от Phase 6, пять
  крупных блоков (A–E), guardrails, явный список «что НЕ
  входит», 10 критериев приёмки, открытые вопросы Step 2+.
  Кода не писать. Никаких изменений registry. Никаких
  новых MCP tool'ов. Никакого расширения product-layer
  surface'а.
- **Что меняем.** Только документация:
  - `docs/architecture/track-a-real-write-path-plan.md`
    (новый);
  - `docs/architecture/track-a-real-write-path-step-map.md`
    (новый);
  - корневой `README.md` — добавить раздел «Active
    parallel track» (после закрытых фаз; Track A
    объявлен; Phase 7 явно не открывается);
  - `PROJECT-STATUS.md` — текущий шаг → Parallel Track A /
    Step 1; статус `in progress`; полный detail block;
    следующий шаг → Track A / Step 2.
- **Затронутые зоны.** `docs/architecture/**`,
  `README.md`, `PROJECT-STATUS.md`. **Никаких** изменений
  в `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  `.github/`, `.claude.json`.
- **Результат.** Документационный вход в Track A готов;
  все Steps 2–7 работают от этих контрактов и от open
  questions Step 1. Ни один code-критерий приёмки трека
  на этом шаге не закрывается — Step 1 только открывает
  трек. Registries: `read=15, write=25, intelligence=16`
  без изменений.

## Step 2

**Real binary-backed `apply_config_from_files` contract.**

- **Цель.** Закрыть часть критерия приёмки 1: первый из
  двух Phase 2 stub-backed-путей переходит на honest
  dual-mode contract с real execution. Решить открытые
  вопросы Q1, Q2, Q4, Q6 из Step 1 плана для apply-пути:
  каким полем `EnvironmentConfig` operator объявляет
  apply argv-template; какой набор whitelisted
  placeholders; какая pre-flow validation; какой default
  timeout.
- **Что меняем.**
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `apply_config_from_files` получает branch dispatch:
    при наличии operator-declared argv-template и
    `onec_binary_path` — реальный subprocess через
    `onec_process_runner.run_process` с captured exit
    code + stdout/stderr excerpts; при **отсутствии** —
    старое stub-поведение (`run_stub_apply_process`)
    сохраняется без изменений. Fallback **только
    config-time**, не runtime.
  - `packages/onec-config/src/onec_config/models.py` —
    минимальное расширение: одно новое optional поле в
    `EnvironmentConfig` (точное имя зафиксировано в этом
    шаге решением по Q1: либо
    `onec_apply_command_template`, либо общий
    `onec_command_templates: dict[str, list[str]]`).
  - `packages/onec-config/src/onec_config/loader.py` —
    strict-validation для нового поля fail-closed на bad
    shape; backward-compat: Phase 1–6 конфиги без этого
    поля грузятся без изменений.
  - Payload `apply_config_from_files` получает явные
    маркеры `mode ∈ {"stub", "binary-backed"}`,
    `binary_invoked: bool`, `exit_code: int | None`,
    `command_preview: list[str] | None`, `stdout_excerpt:
    str`, `stderr_excerpt: str` — те же поля, что
    Phase 6 / Step 2 эмитит для `create_dump_snapshot`
    binary-backed branch'а.
  - `run_write_flow` остаётся единственной точкой входа.
    Preflight + snapshot + operation + verify + audit
    обязательны и для binary-backed mode.
  - **Registry write-server'а не меняется** — это та же
    операция с расширенным dispatch'ем.
  - Новая `_APPLY_DEFAULT_TIMEOUT_SECONDS` константа (по
    аналогии с `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS = 300`)
    — точное значение фиксируется в шаге.
- **Затронутые зоны.** Точечно `apps/mcp-write-server/**`
  (один write-tool + возможно shared helper —
  окончательное место shared helper'ов решает Step 4).
  Точечно `packages/onec-config/**` (одно новое
  optional-поле + loader-validation). Read- и
  intelligence-серверы не трогаются. `onec-policy-engine`
  не трогается.
- **Результат.** Закрывается часть критерия приёмки 1 (apply-
  путь имеет binary-backed dispatch при наличии binary
  contract). Часть критерия 4 (no silent fallback)
  подтверждается: при non-zero exit subprocess'а tool
  возвращает `ok=False` с `mode="binary-backed"`, без
  тихого downgrade'а на stub. Часть критерия 5 (payload
  честно показывает mode/exit/excerpts) подтверждается
  для apply. Registries без изменений.

## Step 3

**Real binary-backed `update_database_configuration` contract.**

- **Цель.** Закрыть оставшуюся часть критерия приёмки 1:
  второй Phase 2 stub-backed-путь
  (`update_database_configuration`) переходит на тот же
  honest dual-mode contract. Решить остаточные открытые
  вопросы Q1, Q2, Q4, Q6 для update-db-пути.
- **Что меняем.**
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    — `update_database_configuration` получает branch
    dispatch симметрично с Step 2. Та же дисциплина:
    config-time fallback на stub при отсутствии binary
    contract; runtime-failure при non-zero exit без
    silent stub fallback'а.
  - `packages/onec-config/src/onec_config/models.py` /
    `loader.py` — расширение, симметричное Step 2 (либо
    второе поле `onec_updatedb_command_template`, либо
    дополнительный ключ в общем `onec_command_templates`
    словаре — решение по Q1, принятое в Step 2,
    унаследовано здесь).
  - Payload поля те же (`mode`, `binary_invoked`,
    `exit_code`, `command_preview`, `stdout_excerpt`,
    `stderr_excerpt`).
  - `_UPDATEDB_DEFAULT_TIMEOUT_SECONDS` константа.
  - Если на Step 2 shared helper'ы вынесены в новое место
    (см. Q3) — Step 3 их переиспользует, **не**
    дублирует.
  - **Registry write-server'а не меняется**.
- **Затронутые зоны.** Точечно `apps/mcp-write-server/**`
  (тот же write-tool + переиспользуемые helper'ы из
  Step 2). Точечно `packages/onec-config/**` (одно
  поле / один ключ, расширяется существующая optional-
  surface). Read- / intelligence-серверы не трогаются.
- **Результат.** Полностью закрывается критерий приёмки 1
  (оба Phase 2 stub-backed-пути имеют honest dual-mode
  contract). Подтверждается, что Track A не делает
  copy-paste'а (helper'ы шарятся). Registries без
  изменений.

## Step 4

**Unify / finish `create_dump_snapshot` real path + payload
discipline.**

- **Цель.** Закрыть критерий приёмки 5 (payload честно
  показывает все поля для **всех** binary-backed
  write-tool'ов, не только для apply / update-db).
  Привести Phase 6 / Step 2 binary-backed slice
  `create_dump_snapshot` к тому же общему контракту, к
  которому Step 2 / 3 привели apply / update-db. Решить
  Q3: где живут shared helper'ы.
- **Что меняем.**
  - `apps/mcp-write-server/src/mcp_write_server/tools.py`
    (или вынесенный в Step 2 shared helper):
    - Привести payload-поля `create_dump_snapshot` к
      одинаковой именной convention с apply / update-db
      (если Step 2 / 3 что-то переименовали или
      добавили — здесь зеркало);
    - Если Q3 решён в пользу shared helper-модуля
      (например, `runtime/process_dispatch.py`) —
      `create_dump_snapshot` тоже использует этот модуль,
      без дублирования логики;
    - operator-readable findings codes унифицированы
      (`runtime_binary_invoked:<name>`,
      `runtime_binary_failed:<name>:exit=<N>`,
      `runtime_binary_template_render_failed:<name>`).
  - `apps/mcp-write-server/README.md` обновляется: один
    общий раздел про binary-backed write contract,
    вместо разрозненных описаний по каждому tool'у.
  - **Никаких изменений** в operator-declared контракте
    (placeholders те же; argv-grammar та же; operator
    grammar не ломается). Это рефакторинг внутрь, не
    наружу.
  - **Registry write-server'а не меняется**.
- **Затронутые зоны.** Точечно `apps/mcp-write-server/**`.
  `apps/mcp-write-server/README.md`. Read- / intelligence-
  серверы / `onec-config` / `onec-policy-engine` не
  трогаются.
- **Результат.** Закрывается критерий приёмки 5
  полностью (один shared payload-контракт между всеми
  тремя binary-backed write-tool'ами). Внутренняя
  стоимость поддержки трека снижается (один shared
  helper вместо трёх копий argv-render / spawn / capture
  логики). Registries без изменений.

## Step 5

**Product-layer integration over real write path.**

- **Цель.** Закрыть критерий приёмки 3: один продуктовый
  сценарий проходит поверх real write path через
  существующий `run_guided_workflow`, **без** правок в
  `workflow.py` логике. Решить Q7 (advisory-сообщение в
  smoke plan summary) и Q8 (расширение enterprise
  foundation inspector'а).
- **Что меняем.**
  - **Никаких изменений в логике** существующих
    product-layer boundary'ев (`workflow.py`,
    `recovery.py`, `realstand.py`, `enterprise.py`).
    Цель шага — **проверить**, что real write path
    работает поверх Phase 6 surface'а.
  - **Возможные минимальные правки** (только если
    реально нужны для honest reporting'а):
    - `apps/platform/src/onec_platform/realstand.py`:
      одна строка advisory в smoke plan summary
      («binary-backed dispatch for apply / update-db /
      dumpcfg is configured») — только если
      operator явно ожидает это видеть. Default
      Step 1 — да, добавить, но **только** если smoke
      plan summary действительно теряет полезный
      сигнал без этого.
    - `apps/platform/src/onec_platform/enterprise.py`:
      если Step 2 / 3 ввели новые optional поля в
      `EnvironmentConfig`, foundation inspector
      честно их учитывает на секции D (real-stand /
      binary contract). Это **не** новый раздел
      inspector'а; это расширение существующего
      `_check_real_stand_contract` тем же стилем
      проверок.
  - **Manual integration check**:
    - расширить (или создать второй) phase6/track-a
      check-скрипт, который прогоняет
      `run_guided_workflow` с binary-backed apply /
      update-db / dumpcfg в **synthetic** окружении
      (через `sys.executable` как stand-in 1cv8 binary
      — точно так же, как Phase 6 / Step 9 делает
      smoke). Это validates the integration path, не
      the actual 1cv8 binary;
    - реальный multi-step round-trip с настоящим 1cv8
      binary — это Step 6, не Step 5.
  - **Registry write-server'а не меняется**.
  - **Никакого back-door write channel'а** в product
    layer'е — это инвариант, явно проверяется
    discipline-блоком.
- **Затронутые зоны.** Возможно точечно
  `apps/platform/**` (advisory + foundation extension).
  `apps/mcp-write-server/**` не трогается. Read- /
  intelligence-серверы не трогаются.
  `onec_policy_engine` не импортируется.
- **Результат.** Закрывается критерий приёмки 3
  (продуктовый сценарий поверх real write path). Закрывается
  часть критерия 9 (operator-facing messages честные).
  Подтверждается, что safety guarantees Phase 6
  (`run_write_flow` единственный mutating-путь, no
  back-door channel, intelligence read-only,
  `onec_policy_engine` не импортируется) сохраняются.

## Step 6

**Reference stand multi-step round-trip.**

- **Цель.** Закрыть критерий приёмки 2 — хотя бы один
  полный real round-trip на reference stand'е. Решить
  Q5 (reference stand spec) и Q9 (один или несколько
  round-trip'ов).
- **Что меняем.**
  - В контролируемом окружении (reference stand с
    реальной 1cv8 binary) проходится сценарий:
    real DumpCfg → дамп физически на диске →
    real apply (LoadCfg) обратно → real UpdateDBCfg →
    стенд живёт. Сценарий выполняется через
    существующий `run_guided_workflow` (или, если
    цепочка длиннее, через несколько вызовов
    `run_guided_workflow` подряд — без новых
    workflow'ов на этом шаге) c
    operator-declared argv-templates трёх tool'ов.
  - Сценарий описывается как воспроизводимый runbook:
    - `docs/runbooks/track-a-real-round-trip.md`
      (новый) — точное имя фиксируется в шаге; формат
      Symptom / Cause / Diagnose / Fix / Confirm
      может не подходить, поскольку это runbook
      validation-сценария, а не recovery; разрешается
      adjusted format.
  - Один honest failure path в этом сценарии:
    operator-declared argv-template, который заведомо
    возвращает non-zero exit, — продукт честно
    репортит non-zero, не делает silent fallback'а.
  - **Кода правим минимально** — только если real
    round-trip вскроет реальный blocker (по аналогии с
    Phase 6 / Step 7, где правок не понадобилось вовсе,
    и Phase 6 / Step 9, где понадобились две).
  - **Registry write-server'а не меняется**.
- **Затронутые зоны.** `docs/runbooks/**` (новый
  runbook). Точечно `apps/**` если real round-trip
  вскроет blocker. `mcp-read-server` /
  `mcp-intelligence-server` не трогаются.
- **Результат.** Закрывается критерий приёмки 2
  (multi-step real round-trip). Validation на
  настоящей 1cv8 binary'е, не synthetic stand-in'е,
  подтверждена. Registries без изменений.

## Step 7

**Final integration pass and Track A closure.**

- **Цель.** Подтвердить, что Track A действительно
  ship'нул full real write path slice end-to-end.
  Сделать сквозной интеграционный прогон через каждый
  блок трека (A — real binary-backed contract; B —
  reference stand round-trip; C — product-layer
  integration; D — operator diagnostics; E — closure).
  Зафиксировать закрытие трека.
- **Что меняем.** Кода стараемся **не трогать**.
  Интеграционный прогон по сценариям, наработанным в
  Step 2–6. Если прогон вскроет реальный продуктовый
  blocker — разрешается минимальная точечная правка,
  по аналогии с Phase 5 / Step 8 (где правок не
  понадобилось) и Phase 6 / Step 9 (где понадобились
  две минимальные).
  - `apps/platform/README.md` — раздел «Real write path
    closed» (или эквивалент) с описанием того, что
    закрыл Track A;
  - `apps/mcp-write-server/README.md` — единый раздел
    про binary-backed write contract (если в Step 4
    он не был дописан до финальной формы — здесь
    финализируется);
  - `docs/operator-manual.md` — раздел «как читать
    binary-backed write payload» и «когда binary
    вернул non-zero»;
  - `docs/administrator-manual.md` — раздел про
    operator-declared argv-templates для apply /
    update-db / dumpcfg, whitelisted placeholders,
    timeouts, fallback discipline;
  - `docs/runbooks.md` — добавляется один или два
    recipe'а про честный failure binary-backed write
    paths;
  - корневой `README.md` — Track A помечен как
    **закрыт**; Phase 6 уже закрыта; список того, что
    осталось как parallel tracks ПОСЛЕ Track A,
    обновляется (полная enterprise-вселенная,
    AST-парсер, web-UI, packaging ecosystem,
    multi-version matrix, production-grade transport,
    полная rollback/delete-вселенная — всё это
    остаётся отдельными parallel tracks);
  - `PROJECT-STATUS.md` — текущий шаг помечает Track A
    закрытым; явно сказано «никаких новых треков пока
    не открыто»; следующая активная работа — открытие
    следующего parallel track'а (если решение принято
    оператором проекта); Phase 7 как фаза по-прежнему
    не запланирована.
- **Затронутые зоны.** `docs/`, корневой `README.md`,
  `PROJECT-STATUS.md`; точечно `apps/**` при честной
  необходимости.
- **Результат.** Закрываются финальные критерии приёмки
  6, 7, 8, 9, 10. **Parallel Track A — Full Real
  1cv8-backed Write Path закрыт**. Платформа достигла
  finished real-write behavior на reference stand'е.
  Остаются только non-blocking follow-up'ы / parallel
  tracks за пределами Track A.

---

После Step 7 Track A **закрыт**. Следующая активная работа —
**не Phase 7**. Это либо открытие следующего parallel track'а
(по решению), либо просто фиксация текущего состояния
платформы как достигнутого. В обоих случаях safety guarantees
Phase 1–6 + Track A сохраняются.
