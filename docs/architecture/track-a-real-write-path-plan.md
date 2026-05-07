# Parallel Track A — Full Real 1cv8-backed Write Path Plan

## Назначение трека

Phase 1–6 закрыты. У платформы есть честное ядро + product layer
+ industrialization slice:

- `mcp-read-server` (15 tools) — read MVP закрыт на Phase 1;
- `mcp-write-server` (25 tools) — write MVP закрыт на Phase 2,
  metadata changes — на Phase 3, structural XML edit slice
  (`add_form_attribute`) — на Phase 6 / Step 5, executable
  rollback path (whitelist из двух tools) — на Phase 6 / Step 4;
- `mcp-intelligence-server` (16 tools) — read-only intelligence
  layer закрыт на Phase 4;
- `apps/platform/onec_platform` — bootstrap / installer / runtime
  layer / health dashboard / guided workflows / rollback
  assistant / real-stand smoke / enterprise foundation
  inspector — Phase 5 + Phase 6 закрыты;
- Phase 6 / Step 9 — final integration pass — пройден одним
  связным сценарием через каждый Phase 6 slice + шесть honest
  failure paths + пять discipline asserts.

Phase 6 закрыла **product contour**. Это — finished product
behavior **на reference stand'е** в smoke-форме. Это **не**
finished real-write product behavior на реальном 1cv8.

Самый жирный незакрытый разрыв сейчас — **не все mutating
write-path'ы доведены до настоящего real 1cv8-backed
исполнения**. Конкретно:

- `apply_config_from_files` остаётся **stub-backed process apply**:
  payload честно помечает `mode="stub"` (или эквивалент),
  через `run_write_flow` проходит вся дисциплина, но **что
  реально применилось внутрь живой инфобазы — не делается**.
- `update_database_configuration` тоже stub-backed: написан как
  process apply, не как настоящий `1cv8 UpdateDBCfg`.
- `create_dump_snapshot` имеет binary-backed branch (Phase 6 /
  Step 2), но это **partial generic** binary-backed slice:
  operator-declared argv-template запускается через
  `onec_process_runner.run_process`, без специализации под
  настоящий 1cv8 DumpCfg / контракт mode-полей / honest
  payload поверх real DumpCfg behavior. Step 2 ship'нул
  один real binary-backed путь, но не довёл его до finished
  contract'а с full operator-facing diagnostics.
- На reference stand'е **нет реального multi-step round-trip'а**
  через всю цепочку DESIGNER → BackupCfg → DumpCfg →
  ENTERPRISE → apply / update-db. Phase 6 / Step 7 ship'нул
  controlled smoke probe (один subprocess invocation),
  Step 9 — synthetic integration через `sys.executable`. Real
  multi-step round-trip с настоящим 1cv8 binary'ом — за
  рамками Phase 6.
- Operator-facing contract для binary-backed write execution
  на сегодня размыт: `mode` поле, `binary_invoked` флаг,
  `binary_exit_code`, `command_preview`, stdout/stderr
  excerpts, fallback discipline — частично определены в
  `create_dump_snapshot` (Step 2), но не унифицированы между
  всеми binary-backed-кандидатами. Operator не имеет одного
  consistent ментального шаблона «как смотреть на real-write
  result».

Этот разрыв — **не enterprise-вселенная** и **не AST-парсер**;
это **доведение существующего write-core до finished behavior**.
Все safety guarantees Phase 1–6 (`run_write_flow` единственный
mutating-путь, intelligence read-only, нет back-door write
channel'а из product layer'а, fail-closed по умолчанию,
audit append-only, нет `shell=True`) **сохраняются без
изменений**.

Это **не** новый MCP-surface sprint и **не** ещё одно
расширение surface'а ради surface'а. Это **post-Phase-6
completion track** на узкую зону real execution.

Назвать это «Phase 7» было бы нечестно: Phase 7 как отдельная
крупная интеграционная фаза не запланирована. Этот трек —
**Parallel Track A — Full Real 1cv8-backed Write Path** —
открывается как первый из parallel / completion tracks **после**
закрытой Phase 6.

## Целевой результат

К моменту закрытия Track A платформа должна выдерживать
honest operator-facing нарратив:

1. **Operator declares the real 1cv8 binary contract.** Тот же
   `EnvironmentConfig.onec_binary_path`, что был введён в
   Phase 5 / Step 7 и расширен в Phase 6 / Step 2 (включая
   `onec_dumpcfg_command_template`), теперь имеет столько же
   полей-template'ов, сколько mutating-операций реально
   binary-backed: операторские command templates для
   `apply_config_from_files`, `update_database_configuration`,
   и (если потребуется унификация) для `create_dump_snapshot`.
   Все templates — argv-list (никаких shell strings), с
   whitelisted placeholder substitution, без скрытых defaults.
   Operator owns argv grammar.
2. **Те write-tools, которые сегодня stub-backed, переведены на
   real binary-backed execution.** `apply_config_from_files`
   и `update_database_configuration` получают честный
   binary-backed branch. При наличии binary contract —
   subprocess через `onec_process_runner.run_process` с
   captured exit code + stdout/stderr excerpts; при
   **отсутствии** — старый stub mode сохраняется без
   изменений (fallback **только config-time**, не runtime).
3. **`create_dump_snapshot` нормализован как finished real path.**
   Тот же набор payload-полей, что у Phase 6 / Step 2
   (`mode`, `binary_invoked`, `exit_code`, `command_preview`,
   `stdout_excerpt`, `stderr_excerpt`), переведён в **общий**
   shared контракт; при необходимости — специализация под
   настоящий 1cv8 DumpCfg semantic (`/DumpCfg`, `/Out`,
   `/DisableStartupDialogs` и т. п. — **operator-declared**,
   не platform-invented).
4. **Один реальный multi-step round-trip на reference stand
   проходит end-to-end.** Это не synthetic `sys.executable`
   вместо 1cv8 (как было в Phase 6). Это последовательность:
   real `onec_binary_path` → real `BackupCfg` → real
   `DumpCfg` → real `LoadCfg` (apply) → real `UpdateDBCfg`
   → reference stand живёт. Сценарий выполняется хотя бы один
   раз в контролируемом окружении и фиксируется как
   воспроизводимый runbook.
5. **Product layer использует это без обхода safety discipline.**
   Существующие boundary'и Phase 5 / Phase 6
   (`run_guided_workflow`, `run_rollback_assistant`,
   `run_real_stand_smoke_test`, `inspect_enterprise_foundation`)
   работают поверх real write path **без правок собственной
   логики** — потому что весь real binary-backed dispatch
   живёт в write-server'е, не в product layer'е. Product
   layer не получает back-door write channel'а; rollback
   discipline остаётся через public
   `restore_dump_file_from_snapshot` (Phase 6 / Step 4).
6. **Honest mode reporting — единый ментальный шаблон.**
   Оператор смотрит на любой mutating-write `ToolResult` и
   видит один consistent набор полей: `payload.data.mode ∈
   {"stub", "binary-backed"}`, `binary_invoked: bool`,
   `exit_code: int | None`, `command_preview: list[str] | None`,
   `stdout_excerpt: str`, `stderr_excerpt: str`. Это
   облегчает диагностику и — что важнее — делает невозможным
   silent runtime fallback (operator всегда видит, что
   реально произошло).
7. **Никакого silent runtime fallback'а.** Если operator
   declared binary contract и runtime subprocess вернул
   non-zero exit, write-tool возвращает `ok=False` с честным
   `mode="binary-backed"`. Никакого автоматического
   downgrade'а на stub mode. Это **уже** контракт Phase 6 /
   Step 2 для `create_dump_snapshot` — он распространяется на
   остальные binary-backed-tools.

После закрытия трека операторский нарратив звучит так:
«Я указал путь к 1cv8 binary и operator-declared argv-templates
для apply / update-db / dumpcfg. Когда я зову guided workflow,
платформа делает реальный subprocess с честно отражённым
mode, exit_code, и captured output. Если subprocess падает —
я это сразу вижу; нет тихого отката на эмуляцию. Один real
multi-step round-trip на моём reference stand'е прошёл
end-to-end.»

## Что именно закрывает этот трек

Трек **закрывает**:

- **Remaining Phase 2 stub gap.** `apply_config_from_files` и
  `update_database_configuration` перестают быть stub-backed-
  только: получают honest dual-mode contract (stub при
  отсутствии binary contract; real binary-backed при наличии).
- **Real apply / update-db path.** Через тот же
  `run_write_flow`, тот же policy engine, тот же audit;
  никакого нового mutating-канала.
- **Tighter contract around 1cv8 argv templates / modes.**
  Один shared набор payload-полей для всех binary-backed
  write-tools; whitelisted-placeholder substitution
  унифицирована; operator-declared argv grammar остаётся
  единственным источником истины.
- **Full round-trip smoke.** Один реальный end-to-end scenario
  на reference stand'е с настоящим 1cv8 binary'ом, не
  `sys.executable`-stand-in'ом. Это включает в себя один
  honest failure path из реальной жизни: обработать ситуацию,
  когда настоящий 1cv8 на каком-то шаге возвращает non-zero
  без silent fallback'а.
- **Operator confidence for real write path.** Один honest
  contract вместо «у нас есть write-tools, но что они делают
  на живой 1С — зависит от того, какой stub'ом они
  back'нуты».

Трек **не закрывает**:

- **Полный enterprise super-set.** SSO/RBAC, multi-tenant,
  secrets vault как сервис, federated audit storage,
  policy-as-code DSL, multi-instance HA, web-UI / dashboard
  frontend, federated identity — отдельные parallel /
  enterprise tracks ПОСЛЕ Track A. Step 8 Phase 6 ship'нул
  только foundation; Track A не расширяет его.
- **UI / web dashboard.** Нет.
- **Полный AST-парсер XML / BSL.** Нет; Track A не трогает
  metadata-tools, только real execution layer для apply /
  update-db / dumpcfg.
- **Полная metadata-вселенная.** `add_catalog_attribute` /
  `add_document_attribute` / `add_form_attribute` /
  `add_form_element` / `append_module_method` /
  `replace_module_method_body` — не трогаются. Их substring/
  DOM-edit статус остаётся as-is.
- **Полная rollback / delete вселенная.** Track A не
  расширяет Step 4 whitelist (whitelist остаётся
  `add_catalog_attribute` + `add_document_attribute`); не
  добавляет `delete_*` write-tools; не переписывает
  rollback assistant.
- **Production-grade MCP transport / `__main__` / CLI.**
  Никаких изменений в server bootstrap / transport. Те же
  registries.
- **Packaging ecosystem.** Никаких `.msi` / `.deb` / signed
  binaries / GUI installer'ов. Phase 6 / Step 3 install
  fast path остаётся короткий script + declarative
  template.
- **Multi-version matrix в полном объёме.** Один **один**
  reference stand с одной версией 1cv8 — этого достаточно
  для закрытия Track A. Полное покрытие matrix'ы версий 1С
  — отдельный parallel track.

## Чем этот трек отличается от закрытой Phase 6

- **Phase 6** была **широкой completion track'ой** на семь
  product-area блоков (binary-backed slice; install fast path;
  executable rollback; structural XML edit; runtime
  hardening; standalone manuals; enterprise foundation) +
  закрывающий integration pass. Phase 6 ставила цель —
  finished product **contour**.
- **Track A** — **узкий completion track** на одну product
  area: real execution layer для оставшихся mutating-tool'ов.
  Track A ставит цель — finished real-write **behavior**
  поверх уже существующего contour'а.
- Phase 6 могла ship'нуть один real binary-backed slice
  (`create_dump_snapshot`) и оставить остальные stub-backed
  без угрозы для своих критериев приёмки. Track A
  **специально занимается** оставшимися stub-backed-путями
  и доводит их до consistent honest dual-mode contract'а.
- Phase 6 / Step 7 ship'нул real-stand smoke как **один
  controlled subprocess invocation** через operator-declared
  probe args. Track A ship'нет real **multi-step
  round-trip** через настоящий 1cv8 binary в контролируемом
  окружении. Это качественно более сильное validation
  событие.
- Phase 6 принципиально **не вводила новых MCP tool'ов** на
  Step 1–9. Track A тоже не должен их вводить **без крайней
  необходимости** (registries не растут без явного решения
  внутри track-а — см. guardrails).
- Phase 6 закрыта одним большим integration pass'ом
  (Step 9). Track A закрывается аналогично: финальный
  integration pass с real round-trip и явной фиксацией
  закрытия трека (Step 7 трека).

Это — **post-phase hardening / completion track**, а не новая
большая фаза ради фазы.

## Крупные блоки трека

### Блок A — Real binary-backed dump / apply / update contract

Доведение трёх mutating-write-tool'ов до consistent honest
dual-mode contract'а:

- `apply_config_from_files` получает binary-backed branch
  через `onec_process_runner.run_process` с
  operator-declared argv template (поле в
  `EnvironmentConfig`, новое или расширение существующего;
  имя поля — открытый вопрос Step 1, фиксируется в Step 2
  трека).
- `update_database_configuration` получает аналогичный
  binary-backed branch.
- `create_dump_snapshot` нормализуется: payload-поля
  выравниваются с тем, что эмитят Track A apply / update;
  internal helpers по подготовке argv-template / capture /
  excerpt-cap выносятся в shared place внутри write-server'а
  (например, в `runtime/process_dispatch.py` — точное имя
  фиксируется в Step 4 трека).
- Все три tool'а сохраняют контракт: `run_write_flow` —
  единственный mutating-путь; preflight + snapshot +
  operation + verify + audit обязательны; никакого
  back-door channel'а из product layer'а; никаких silent
  runtime fallback'ов; honest payload `mode ∈ {"stub",
  "binary-backed"}` + `binary_invoked` + `exit_code` +
  `command_preview` + `stdout_excerpt` + `stderr_excerpt`.

Registry write-server'а **не** растёт от блока A. Это та же
операция, просто с расширенным dispatch'ем — точно как
Phase 6 / Step 2 расширил `create_dump_snapshot` без
добавления нового tool'а.

### Блок B — Reference stand execution choreography

Один реальный multi-step round-trip на reference stand'е:

- Reference stand spec фиксируется (версия 1cv8, OS,
  директории, разрешённые операции, таймауты);
- Сценарий: real DumpCfg → дамп физически на диске →
  real apply (LoadCfg) обратно → real UpdateDBCfg → стенд
  живёт;
- Сценарий выполняется через тот же product-layer guided
  workflow, что и в Phase 6 / Step 9 — никаких alternative
  paths в обход;
- Каждый шаг воспроизводится из runbook'а; runbook
  материализуется в `docs/runbooks/track-a-real-round-trip.md`
  (или эквивалент — точное имя в Step 6);
- Один honest failure case в этом сценарии: операторски
  подсунут заведомо non-zero binary template — продукт
  честно репортит non-zero exit, не делает silent
  fallback'а.

### Блок C — Product-layer integration over real write path

Существующие product-layer boundary'и используют real write
path **без правок собственной логики**:

- `run_guided_workflow` использует те же три обновлённых
  write-tool'а через тот же `run_write_flow`. Никаких
  изменений в `workflow.py` логике;
- `run_rollback_assistant` остаётся advisory-only для
  `apply_config_from_files` / `update_database_configuration`
  (они вне Step 4 whitelist'а — расширение whitelist'а
  **не входит** в Track A); rollback whitelist остаётся
  ровно `add_catalog_attribute` + `add_document_attribute`;
- `run_real_stand_smoke_test` остаётся честным **smoke**
  probe'ом и **не превращается** в multi-step round-trip
  driver. Multi-step round-trip — отдельный сценарий из
  блока B, выполняемый через `run_guided_workflow`, не через
  smoke;
- `inspect_enterprise_foundation` обновляется **только
  если** Track A добавит новые operator-declared optional
  поля в `EnvironmentConfig` (например, новые
  command-template поля для apply / update-db). В таком
  случае foundation inspector честно проверяет их наличие
  на prod-like configs — это локальное расширение секции D
  inspector'а, не нового boundary.

Никакой product-layer не получает прямого write-channel'а на
живой 1cv8 binary; всё идёт через write-server.

### Блок D — Operator-facing diagnostics and honest mode reporting

Один shared operator-facing contract для всех binary-backed
write-tools:

- Стандартный набор payload-полей (`mode`, `binary_invoked`,
  `exit_code`, `command_preview`, `stdout_excerpt`,
  `stderr_excerpt`) одинаков у `create_dump_snapshot`,
  `apply_config_from_files`, `update_database_configuration`;
- `command_preview` — argv list с уже подставленными
  placeholder'ами, для воспроизводимости. Никаких секретов в
  preview (если бы они там были — это отдельный security
  question, который Track A не решает; secrets vault — за
  скобками);
- `stdout_excerpt` / `stderr_excerpt` имеют общий cap (как
  у Phase 6 / Step 2 — 1024 символа); если 1cv8 генерит
  длиннее, оператор видит truncation marker;
- Operator-readable findings codes унифицированы. Тот же
  codenamespace, что Phase 6 / Step 2:
  `runtime_binary_invoked:<name>`,
  `runtime_binary_failed:<name>:exit=<N>`,
  `runtime_binary_template_render_failed:<name>` и т. п.
  Точные коды — в Step 4 трека;
- Документ `docs/operator-manual.md` (Phase 6 / Step 7) и
  `docs/runbooks.md` дополняются разделом «как читать
  binary-backed write payload» и «когда binary вернул
  non-zero». Никаких новых standalone-документов из Track A
  — расширения уже имеющихся.

### Блок E — Final validation and closure

Финальный integration pass трека:

- Один сквозной сценарий проходит **через каждый блок
  трека**: real apply (Блок A) → reference stand round-trip
  (Блок B) → проверка через product-layer boundary (Блок C)
  → operator смотрит на consistent payload (Блок D);
- Каждый блок имеет минимум один honest failure path (см.
  критерии приёмки);
- Discipline asserts (registries pre/post, `onec_policy_engine`
  imports = 0 в product/intelligence, suggested-tools real
  names, no boundary raises, no back-door write) повторяются
  **без drift'а**;
- dev-check остаётся зелёным;
- Документация (root README, PROJECT-STATUS.md,
  `apps/platform/README.md`, `apps/mcp-write-server/README.md`,
  `docs/operator-manual.md`, `docs/administrator-manual.md`,
  `docs/runbooks.md`) обновляется минимально и честно;
- Track A фиксируется как закрытый. Список того, что
  осталось как parallel tracks **после** Track A,
  обновляется в root README.

## Guardrails трека

Жёсткие инварианты, которые **не размываются** ни на одном
шаге трека:

- **`run_write_flow` остаётся единственным mutating path**
  для каждого binary-backed write-tool'а. Preflight +
  snapshot + operation + verify + audit обязательны и для
  binary-backed mode. Никаких обходов discipline.
- **Никакого back-door write из product layer'а.** Никакой
  модуль под `apps/platform/src/onec_platform/` не пишет
  напрямую в живой dump / infobase / гонит subprocess
  поверх 1cv8 binary'а в обход write-server'а. Real
  execution dispatch живёт в `apps/mcp-write-server/`, как
  Phase 6 / Step 2 уже установил.
- **Runtime fallback stub→binary допустим только на
  config-time, но не на runtime failure.** Если operator
  не задал binary contract, write-tool работает в stub
  mode — это **config-time fallback** и он сохраняется без
  изменений. Если operator задал binary contract и
  subprocess вернул non-zero — write-tool возвращает
  `ok=False` с `mode="binary-backed"` и **не** пытается
  тихо переключиться на stub. Это **runtime honesty**.
- **Runtime failure в binary-backed path = honest failure.**
  Никаких retry-loop'ов внутри write-flow. Никаких
  exponential backoff'ов. Operator видит честный exit
  code; решение о retry — на стороне operator'а.
- **No `shell=True`.** Все subprocess'ы идут через
  `subprocess.Popen` с argv list (через
  `onec_process_runner.run_process`). Operator-declared
  argv template — список строк, не shell-команда.
- **Operator owns exact argv grammar.** Платформа **не
  изобретает** 1cv8 CLI semantics. Operator пишет полный
  argv-template с whitelisted placeholder substitution
  (`{binary_path}`, `{output_path}`, `{base_path}`,
  `{base_id}`, `{publication_name}`, `{http_base_url}`, и
  возможные новые placeholders, фиксируемые в Step 2 / 3
  трека). Платформа делает только safe substitution; render
  unknown-placeholder'а fail-closed на render-time.
- **Platform does not invent 1cv8 CLI semantics.** Никаких
  захардкоженных `/DumpCfg`, `/LoadCfg`, `/UpdateDBCfg`,
  `/DisableStartupDialogs`, `/AllowedThicknesses` и т. п.
  Любой такой флаг приходит из operator-declared argv-
  template'а. Платформа просто запускает subprocess.
- **Intelligence remains read-only.** `mcp-intelligence-server`
  не трогается треком вовсе. Никаких новых intelligence-
  tool'ов; никакого write-channel'а в intelligence.
- **`onec_policy_engine` не импортируется** в `apps/platform/`
  и `apps/mcp-intelligence-server/`. Discipline уже есть и
  поддерживается дисциплинарным scan'ом.
- **Registries не расширяются без реальной необходимости.**
  Stated default трека — registry counts остаются
  `read=15, write=25, intelligence=16` от начала и до
  конца. Если **на конкретном шаге** потребуется
  расширение write-server registry (например, если
  выяснится, что binary-backed apply нуждается в отдельном
  helper-tool — что маловероятно), это решение
  фиксируется в shop-step документе и в PROJECT-STATUS,
  никакого silent добавления.
- **dev-check после каждого кодового шага должен быть
  зелёным.** То же правило, что и в Phase 6.
- **Audit append-only.** Никаких новых режимов audit'а;
  никаких mutation in-place. JSONL append-only, как и был.
- **Fail-closed по умолчанию.** Любая validation-ошибка на
  pre-flow / pre-spawn boundary возвращает `ok=False` без
  exception'а наружу.

## Что НЕ входит в трек

Явно вынесено за скобки **ещё** раз, на случай если кто-то
решит, что «раз уж мы тут что-то правим — давайте заодно»:

- **Полный enterprise super-set:** SSO/RBAC, multi-tenant,
  secrets vault как сервис, federated audit storage,
  policy-as-code DSL, multi-instance HA, web-UI / dashboard
  frontend, federated identity. Step 8 Phase 6 ship'нул
  только foundation contract; Track A не делает следующий
  шаг enterprise track'а.
- **UI / web dashboard.** Нет.
- **Полный AST-парсер XML / BSL.** Нет; Track A не трогает
  metadata-write-tools.
- **Полная metadata-вселенная.** `add_catalog_attribute` /
  `add_document_attribute` / `add_form_attribute` /
  `add_form_element` / `create_managed_form` /
  `append_module_method` / `replace_module_method_body` —
  не трогаются.
- **Полная rollback / delete вселенная.** Track A **не**
  расширяет Step 4 whitelist; не добавляет `delete_*`
  write-tools; не переписывает `restore_dump_file_from_snapshot`.
- **Production-grade MCP transport.** Никаких изменений в
  server bootstrap; никаких `__main__` / CLI у MCP
  серверов; те же registries.
- **Packaging ecosystem.** `.msi` / `.deb` / signed binary
  distribution / GUI installer / wizard — нет.
- **Multi-version matrix в полном объёме.** Один reference
  stand с одной зафиксированной версией 1cv8 — достаточно.
- **Hot reload, automatic restart, daemon supervisor.**
  Phase 6 / Step 6 ship'нул `restart_policy ∈
  {"never","restart-if-stale"}` boundary-only; Track A не
  расширяет это. Никаких background watcher'ов.
- **Production-grade logging framework.** Phase 6 / Step 6
  ship'нул per-service log files + один-generation
  rotation; Track A не расширяет это в journald / log
  aggregation / forwarding.
- **Расширение intelligence layer'а.** Никаких новых
  intelligence-tool'ов; никаких новых analyses.
- **Изменения в `selfcheck.py`, `bootstrap_paths.ps1`,
  `pyproject.toml`, `.github/`, `.claude.json`** — без
  крайней необходимости.

## Критерии приёмки трека

Жёсткие проверяемые критерии. Track A считается закрытым
**только** когда все эти критерии одновременно выполнены:

1. **Оставшиеся Phase 2 stub-backed пути либо заменены, либо
   явно переведены на honest dual-mode contract с real
   execution.** Конкретно:
   - `apply_config_from_files` имеет `mode ∈ {"stub",
     "binary-backed"}` payload-поле. При наличии operator-
     declared argv template и binary path — реальный
     subprocess invocation. При отсутствии — stub mode (как
     был в Phase 2).
   - `update_database_configuration` — аналогично.
   - `create_dump_snapshot` — payload-поля выровнены с
     остальными binary-backed-tool'ами; helper'ы вынесены
     в shared место.
2. **Хотя бы один полный real round-trip на reference
   stand'е** проходит end-to-end с настоящим 1cv8
   binary'ом. Сценарий зафиксирован как воспроизводимый
   runbook.
3. **Один продуктовый сценарий проходит поверх real write
   path** через существующий `run_guided_workflow`. Никаких
   правок в `workflow.py` логике.
4. **No silent fallback.** Manual integration check трека
   программно подтверждает: при наличии binary contract +
   non-zero exit subprocess'а — write-tool возвращает
   `ok=False` с `mode="binary-backed"` (не `"stub"`).
5. **Payload честно показывает** `mode` / `binary_invoked` /
   `exit_code` / `command_preview` / `stdout_excerpt` /
   `stderr_excerpt` для всех binary-backed write-tool'ов
   трека. Поля одинаково именуются и одинаково семантически
   ведут себя.
6. **read / write / intelligence registries не деградируют.**
   Default — `read=15, write=25, intelligence=16` остаются
   неизменны на старте и в конце трека. Любое отклонение
   честно обосновано в шаговом документе.
7. **dev-check зелёный** после каждого кодового шага и в
   финале трека.
8. **Documentation обновлена** минимально и честно: root
   README, PROJECT-STATUS, `apps/platform/README.md`,
   `apps/mcp-write-server/README.md`, `docs/operator-manual.md`,
   `docs/administrator-manual.md`, `docs/runbooks.md` —
   только реально затронутые части. Никакой новой большой
   документации beyond двух планировочных документов
   Track A / Step 1.
9. **Operator-facing messages честные.**
   - Никакой message не утверждает, что binary был invoked,
     если он не был.
   - Никакой message не маскирует non-zero exit под
     успех.
   - Никакой message не использует enterprise-marketing
     язык про «production-ready» / «enterprise-ready».
10. **Discipline asserts проходят:** 0 `onec_policy_engine`
    real-import'ов в product/intelligence; suggested-tools
    real names через `_allow_only_real_tools`; ни одна
    boundary-функция product layer'а не raise'ит наружу;
    `run_write_flow` остаётся единственным mutating path'ом.

## Открытые вопросы Step 1 (для Step 2+)

Это **не** дыры в плане; это намеренно вынесенные на
последующие шаги решения, которые без реального стенда
дёргать рано:

- **Q1.** Каким именно полем `EnvironmentConfig` operator
  объявляет binary contract для `apply_config_from_files`
  и `update_database_configuration`? Варианты:
  (a) два отдельных поля `onec_apply_command_template` и
  `onec_updatedb_command_template` симметрично с
  `onec_dumpcfg_command_template`; (b) одно общее поле-словарь
  `onec_command_templates: dict[str, list[str]]` с known
  ключами. Решение в Step 2 трека.
- **Q2.** Какой именно набор whitelisted placeholders
  расширяется (если расширяется) для apply / update-db?
  Phase 6 / Step 2 ввёл `{binary_path}`, `{output_path}`,
  `{base_path}`, `{base_id}`, `{publication_name}`,
  `{http_base_url}`. Apply / UpdateDB могут потребовать,
  например, `{config_files_path}` (для LoadCfg) или
  `{server_user}`. Решение в Step 2 / 3 трека.
- **Q3.** Где живут shared helper'ы (argv render +
  process spawn + excerpt cap + payload assembly): в
  `apps/mcp-write-server/src/mcp_write_server/runtime/` как
  новый модуль (`process_dispatch.py`?) или внутри
  `tools.py` как private helpers, как сейчас. Решение в
  Step 4 трека.
- **Q4.** Делается ли какой-либо специализированный
  pre-flow validation для apply / update-db (например,
  проверка существования source dump path для apply ещё
  до спавна)? Решение в Step 2 / 3 трека; default — да,
  fail-closed как и везде.
- **Q5.** Какова форма reference stand spec? Phase 5 /
  Step 7 ввёл общую идею; Track A фиксирует конкретику:
  версия 1cv8, OS, директории, разрешённые операции,
  таймауты. Решение в Step 6 трека.
- **Q6.** Нужен ли отдельный operator-declared timeout-
  override для apply / update-db (DumpCfg уже имеет
  `_DUMPCFG_DEFAULT_TIMEOUT_SECONDS = 300`), или общий
  default достаточен. Решение в Step 2 / 3 трека.
- **Q7.** Делать ли advisory-сообщение в smoke-test
  plan summary («binary-backed dispatch для apply
  включён») или это лишний шум? Решение в Step 5 трека.
- **Q8.** Будет ли `inspect_enterprise_foundation` (Phase 6 /
  Step 8) расширен новыми required-полями для prod-like
  config'ов? Если Track A добавит новые command-template
  поля, foundation inspector должен честно их учитывать
  на секции D. Решение в Step 5 трека.
- **Q9.** Один ли real round-trip достаточен для
  закрытия трека, или нужны два-три (success + один
  honest failure case)? Default Step 1 — один success +
  один honest failure case (operator-declared bad argv).
  Возможно расширение в Step 6.

Эти вопросы фиксируются в шаговых документах по мере их
решения; финальная Step 7 трека сводит результаты в
закрывающий integration pass.
