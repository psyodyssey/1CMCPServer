# Parallel Track E — Multi-Version 1C Smoke Matrix (plan)

> **Companion file:** `track-e-multi-version-smoke-matrix-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 2+ —
> отдельные заходы.

---

## 1. Зачем нужен Track E после Track D

После закрытия **Track A — Full Real 1cv8-backed Write Path**
платформа имеет один реальный binary-backed round-trip
(`/DumpConfigToFiles` → `/LoadConfigFromFiles` → `/UpdateDBCfg`),
выполненный на **одном** reference stand'е InfoBase6 и **одной**
версии 1С — `8.3.27.1859`. Все последующие треки (B repo
hygiene + productization, C delivery + handoff, D operator
credentials hardening) honestly **расширяли surface вокруг** этого
single-version evidence, но **не** расширяли саму evidence base.

Single-version evidence уже зафиксирован как honest constraint в
четырёх местах: `SECURITY.md` («Single-version 1С evidence. Real
binary-backed round-trip has been exercised on `8.3.27.1859`.
Other versions are not yet covered.»),
`docs/release-handoff.md` («No multi-version 1С smoke matrix.»;
«Single-version 1С coverage — `8.3.27.1859`.»),
`CHANGELOG.md` (0.1.0 carried-forward constraint),
`README.md` (Track A detail: «multi-version matrix на всех 1С
версиях не пройдена»). Track A plan **именно так** и описал
multi-version coverage — как **отдельный parallel track**:
«Полное покрытие matrix'ы версий 1С — отдельный parallel track»
(`docs/architecture/track-a-real-write-path-plan.md`).

Track E — это тот самый отдельный track. Он **не** переписывает
платформу; он **не** добавляет новые feature surface; он **не**
делает full QA program. Его единственный честный продукт —
**документированная smoke matrix**: фиксированный узкий сценарий,
прогнанный на нескольких 1С версиях, с записями evidence и
operator-facing docs, выровненными под фактический уровень
evidence.

## 2. Стартовая точка

### 2.1 Текущая evidence base (read-only факты)

- **Reference version:** `8.3.27.1859` (Windows x64 build).
  Установлен на dev-машине в
  `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe`.
- **Reference stand:** `C:/Users/user/Documents/InfoBase6` —
  file-based 1С база (`1Cv8.1CD`, `1Cv8JobScheduler/`,
  `1Cv8Log/`).
- **Reference scenario:** Track A / Step 6 round-trip — три
  binary-backed write-tool'а отработали зелёным: A.2
  `create_dump_snapshot` через `/DumpConfigToFiles`
  (`mode='binary-backed'`, `binary_invoked=True`,
  `exit_code=0`); A.4 `apply_config_from_files` через
  `/LoadConfigFromFiles` (`stage='completed'`); A.5
  `update_database_configuration` через `/UpdateDBCfg`
  (`stage='completed'`). Audit honest: две mutating row +
  populated `details.dump_snapshot_path` в каждой.
- **Reference артефакты на диске:** реальный
  `Configuration.xml` + поддиректории под dump path; два
  backup snapshot'а перед mutating операциями; два
  pre-mutating dump-snapshot'а; audit.jsonl с двумя
  mutating row.

### 2.2 Архитектурный context

Платформа **не делает** version-sniffing — runbook
`docs/runbooks/track-a-reference-stand-round-trip.md` стр. 242
и стр. 609 явно фиксируют это как design choice:
оператор задаёт абсолютный путь к `1cv8.exe` нужной версии в
`onec_binary_path`, плюс полный operator-declared argv-template
с whitelisted placeholder'ами. Это означает, что **архитектурно
multi-version поддержка уже on the operator side**: оператор
подключает другую версию 1cv8, перезапускает round-trip, фиксирует
результат. Track E **не требует rewrite** execution layer'а — он
требует evidence + docs.

### 2.3 Что Track E **не** наследует

- никаких credentials в repo / docs / commit messages — Track D
  / Step 3 + Step 4 уже зафиксировали env-substitution path
  (`${ENV:NAME}`); Track E использует ту же дисциплину для
  любых operator-driven прогонов;
- никаких автоматических CI matrix runner'ов — в репо нет
  multi-version 1cv8 build pool'а (это physical operator
  infrastructure, out-of-scope трека);
- никакого version-specific code path'а в платформе.

## 3. Gap / problem statement

**Single-version evidence создаёт два честных риска:**

1. **Скрытая дрожь argv-grammar'а между версиями 1С.** Operator-
   declared command templates содержат позиционные argv
   (`/DumpConfigToFiles`, `/LoadConfigFromFiles`, `/UpdateDBCfg`,
   `/DisableStartupMessages`, `/F`, `/N`, `/P`). На отличающихся
   minor / major версиях возможны: переименование флагов,
   изменение exit-code семантики, изменение output-формата
   `Configuration.xml`. Single-version evidence не отвечает на
   эти вопросы, а позиция «не должно отличаться» — это
   предположение, не доказательство.
2. **Скрытая зависимость от particular install layout'а.** Все
   evidence ship'нут с `C:/Program Files/1cv8/<version>/bin/`;
   real-world варианты — x86 install, network-mounted install,
   portable build — реальной evidence не имеют.

**Track E закрывает эти риски** ровно настолько, насколько
достаточно для честного support-statement: documented matrix с
N версий и одним узким сценарием. Не больше, не меньше.

## 4. Целевой результат

После closure Track E у проекта есть:

1. **Frozen smoke scenario** — узкий повторяемый набор шагов,
   привязанный к минимальной evidence-достаточности (default
   candidate: cut-down Track A round-trip — только
   `create_dump_snapshot` через `/DumpConfigToFiles`; optional
   extended scenario — full A.2 → A.4 → A.5).
2. **Documented matrix-table** — `docs/version-support-matrix.md`
   с per-version evidence-row'ами (version family, binary path,
   scenario, audit-row reference, verdict, date). Минимум одна
   row (reference `8.3.27.1859`); operator-supplied
   additional rows — фактический evidence трека.
3. **Operator runbook** — `docs/runbooks/track-e-multi-version-smoke-matrix.md`,
   как прогнать matrix smoke на любой operator-supplied 1С
   версии без feature changes в платформе.
4. **Aligned support statement** — SECURITY.md / release-handoff.md
   / README / CHANGELOG переведены с «single-version evidence»
   на «smoke evidence on V1, V2, …». Если operator additional
   versions не предоставил, статус остаётся single-version, но
   Track E фиксирует **процесс** и matrix template.
5. **Honest constraint after closure** — даже после Track E
   закрытия проект **не** претендует на «полная совместимость
   со всеми 1С версиями». Это явно записано в plan и в closure
   docs.

## 5. Что входит в Track E

- Step 1 — planning (этот заход): два planning-документа +
  минимальный README / PROJECT-STATUS update под active track.
- Step 2 — current evidence baseline audit (docs-only) +
  version selection criteria (principle-based, не конкретные
  номера) + smoke scenario freeze.
- Step 3 — matrix scaffolding (docs-only): operator runbook +
  matrix-table template; никакого реального прогона.
- Step 4 — operator-driven smoke runs на дополнительных
  версиях (operator gate); evidence-row'ы дополняются по
  факту. Operator-supplied gap явно фиксируется, **не**
  имитируется.
- Step 5 — support statement / docs alignment.
- Step 6 — final integration pass and Track E closure.

## 6. Что НЕ входит в Track E

**Out-of-scope deliberately, никаких скрытых гэпов:**

- полная QA-программа (тест-пирамида, performance
  benchmarking, stress/load testing, fuzzing, mutation
  testing);
- enterprise certification claims / compliance attestations;
- «universal / full version support» marketing — только
  evidence на N узких версиях по одному узкому сценарию;
- feature additions для конкретных 1С версий
  (version-specific code path'ы);
- version-sniffing в платформе (architectural choice
  сохраняется: оператор выбирает binary path в config'е);
- новые MCP tools — registries `read=15 / write=25 /
  intelligence=16` без drift'а;
- 1cv8 binary changes / external rebuild;
- transport rewrite, packaging rewrite, broad platform
  rewrite;
- CI matrix runner для multi-version 1cv8 (нет такой
  infra; physical operator territory);
- полный AST-парсер XML / BSL — отдельный technological
  track;
- полная rollback / delete-вселенная — отдельный track;
- production-grade MCP transport / auth — отдельный
  track;
- remote push / GitHub publishing — operator action.

## 7. Guardrails

- никакого 1cv8.exe запуска внутри planning steps (1, 2, 3,
  5, 6); запуск 1cv8 происходит **только** на operator-driven
  Step 4 на operator infrastructure;
- никакого silent смешивания Track E с unrelated changes;
- никаких real credentials в repo / docs / commit messages —
  любые operator-driven прогоны Step 4 используют
  `${ENV:NAME}` substitution path (Track D / Step 3
  contract);
- registries без drift'а на каждом step;
- production code untouched на каждом step (одно допустимое
  исключение — closure-time `pyproject.toml` version bump,
  если Q-решение принято в Step 6);
- никаких новых MCP tools;
- evidence фиксируется только по фактическим прогонам,
  никакой имитации evidence;
- operator-supplied gap (если additional versions
  отсутствуют) фиксируется явно, без скрытия.

## 8. Acceptance criteria (closure)

Track E закрыт, если **все** ниже выполнены:

1. Step 1–6 пройдены последовательно; linear git history
   Step 1 → 2 → 3 → 4 → 5 → 6.
2. Frozen smoke scenario существует в Step 2 deliverable.
3. Matrix-table doc существует в Step 3 deliverable;
   evidence-row format описан и стабилен.
4. Reference-version evidence-row (`8.3.27.1859`) присутствует
   в matrix-table — копируется из Track A / Step 6 audit
   (read-only, новые прогоны 1cv8 не нужны).
5. Operator runbook для smoke matrix существует в Step 3
   deliverable.
6. Step 4 closure: либо additional version evidence-row'ы
   ship'нуты по факту, либо operator-supplied gap явно
   зафиксирован — без имитации.
7. SECURITY.md / release-handoff.md / README / CHANGELOG
   honestly обновлены под фактически собранный evidence-уровень.
8. Registries `read=15 / write=25 / intelligence=16` без drift'а
   на всём треке; selfcheck_status=ok.
9. verify-release.ps1 GREEN на 8 checks (без новых checks).
10. Никаких реальных credentials ни в одном Track E commit'е.

## 9. Honest constraints after closure

Даже после Track E закрытия **остаётся**:

- никакого secrets manager / vault / KMS / OS keychain
  integration (Track D / Step 3 границы) — Track E не
  меняет credentials story;
- никакого version-sniffing в платформе — оператор
  по-прежнему сам выбирает binary path;
- никакой полной QA-программы — Track E это smoke matrix,
  не test pyramid;
- никакой enterprise certification — evidence-rows ≠
  certification claim;
- никакого long-tail backwards compatibility guarantee —
  matrix покрывает только зафиксированные version family'и
  на момент closure, не любую будущую версию;
- никакого performance / stress / fuzzing evidence — это
  out-of-scope трека по дизайну;
- никакого universal-version-support marketing — статус
  trek'а после closure формулируется как «smoke evidence
  on V1, V2, …», не «multi-version supported».

## 10. Связь с Track A / B / C / D

- **Track A** ship'нул binary-backed round-trip и оставил
  multi-version matrix как explicit follow-up. Track E —
  тот самый follow-up; реальный binary-backed путь Track A
  не модифицируется.
- **Track B** ship'нул repo hygiene + install / launch /
  quickstart layer; Track E не модифицирует ничего из
  него.
- **Track C** ship'нул release verify path / handoff /
  packaging honest review; Track E использует существующие
  release-facing скрипты как есть, не расширяет.
- **Track D** ship'нул env-substitution `${ENV:NAME}`
  contract; Track E использует тот же путь для любых
  operator-driven Step 4 прогонов на дополнительных
  версиях. Никаких credentials в repo / commit message.

Параллельные / enterprise tracks **после** Track E (рекомендации
без открытия): rollback whitelist expansion track,
production-grade MCP transport / `__main__` track, full
AST-парсер track, full enterprise super-set. Открытие
следующего track'а — отдельное operator-решение.

## 11. Open questions (Step 2+)

- **Q1 — version selection breadth.** Сколько additional
  версий разумно брать? Default candidate principle:
  **2** дополнительные version family поверх reference
  (одна newer, одна older — если обе доступны у operator'а).
  Минимум — **1** дополнительная (точно достаточная для
  multi-version statement). Максимум для одного трека —
  **3** (за пределами — это уже отдельный extended track).
  Resolve финально в Step 2.
- **Q2 — smoke scenario depth.** Default candidate: **узкий
  cut-down** — только `create_dump_snapshot` через
  `/DumpConfigToFiles` (read-only из перспективы 1С базы:
  dump snapshot не мутирует базу). Optional extended:
  full A.2 → A.4 → A.5 round-trip симметрично Track A. По
  умолчанию trade-off — узкий sufficient: дешевле для
  operator'а, не требует write-allowed config'а на
  каждой target версии. Resolve финально в Step 2.
- **Q3 — matrix-table location.** Default candidate:
  `docs/version-support-matrix.md` (top-level, легко
  discover'абельный). Альтернатива — `docs/runbooks/`
  (привязка к runbook'у). Default стоит на top-level
  потому что matrix — support statement, не runbook.
  Resolve финально в Step 3.
- **Q4 — operator-supplied gap fallback.** Если на Step 4
  оператор не может предоставить additional versions,
  закрываем ли Track E на minimum один row (reference) с
  honest gap notation, или ждём additional evidence
  отдельным захождом? Default candidate: **закрываем**
  с honest gap; `version-support-matrix.md` явно
  фиксирует «matrix template ready, operator-supplied
  evidence pending». Это backward-compatible с дальнейшими
  evidence-row дополнениями вне трека. Resolve финально
  в Step 4.
- **Q5 — closure version bump.** Bumpаем ли
  `pyproject.toml` 0.2.0 → 0.3.0 на closure Track E?
  Симметрично Q7 Track D. Default candidate: **да**, если
  Step 4 ship'ит хотя бы одну additional evidence-row;
  **нет**, если Track E закрывается с operator-supplied
  gap (тогда docs-only status alignment, не minor release).
  Resolve финально в Step 6.
- **Q6 — SECURITY.md / release-handoff.md tone.** Должно
  ли support statement читаться как таблица version family
  + verdict, или как narrative? Default candidate: **обе
  формы** — таблица в `docs/version-support-matrix.md`
  (детально), narrative в SECURITY.md / release-handoff.md
  (короткий pointer на таблицу). Resolve финально в Step 5.
- **Q7 — additional evidence cadence post-closure.** После
  closure Track E добавление новой evidence-row при
  появлении новой 1С версии — это reopened-Track E или
  documentation-only update? Default candidate: **doc-only
  update** против `version-support-matrix.md` без re-open
  Track E. Resolve финально в Step 6.
