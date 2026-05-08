# Parallel Track F — Rollback Whitelist Expansion (plan)

> **Companion file:** `track-f-rollback-whitelist-expansion-step-map.md`
> (пошаговый map). Этот документ — **plan-уровень**: назначение
> трека, целевой результат, что входит / не входит, guardrails,
> acceptance criteria, открытые вопросы Step 2+.

> **Status:** active planning (Step 1). Implementation Step 4 —
> отдельный заход; единственный шаг трека с production code
> change.

---

## 1. Зачем нужен Track F после Track E

После closure'а Track E (Multi-Version 1C Smoke Matrix) у проекта
есть честно зафиксированный, но узкий rollback baseline:
**`_AUTOMATIC_RECOVERY_SUPPORTED` whitelist содержит ровно два
tool'а** — `add_catalog_attribute` и `add_document_attribute`
(`apps/platform/src/onec_platform/recovery.py:126-131`). Это —
наследие Phase 6 / Step 4, которая выбрала минимальный consistent
slice (single-XML-file ops) и явно **зарезервировала expansion
как отдельный шаг** (см. `apps/platform/README.md:799-802`:
«Whitelist `_AUTOMATIC_RECOVERY_SUPPORTED` оставлен в коде ...
будущий шаг ... расширит его без изменения скелета assistant'а»;
`README.md:1064` Track A detail: «полная rollback-вселенная не
покрыта (whitelist на двух tool'ах)»; PROJECT-STATUS / Phase 6
docs все ссылаются на это как на post-Phase-6 work).

Track F — тот самый отдельный шаг. Он **не** переписывает
архитектуру recovery'а; он **не** добавляет новые MCP tools; он
**не** делает «universal rollback» fantasy. Его единственный
честный продукт — **узкое расширение whitelist** для нескольких
конкретных file-based mutating tools, чьи inverse semantics уже
честно покрываются existing `restore_dump_file_from_snapshot`
mechanism'ом.

## 2. Стартовая точка

### 2.1 Текущий rollback baseline (read-only факты)

**Whitelist (2 tools):**
- `add_catalog_attribute`
- `add_document_attribute`

**Mechanism:** `run_rollback_assistant` (boundary в product layer'е)
на `confirm_execute=True` + healthy dashboard + tool_name в
whitelist + audit row carries `details` с непустыми
`dump_snapshot_path` + `relative_path` → вызывает public
`mcp_write_server.tools.restore_dump_file_from_snapshot` →
proходит через `run_write_flow` (preflight + snapshot + operation
+ verify + audit) → post-rollback verify через
`diff_dump_fragment` → success = `restore.ok=True AND
diff.data.changed=False`.

**No back-door write channel:** product layer (`recovery.py`) сам
не пишет файлы; всё mutating идёт через public write-tool.

### 2.2 Eligibility contract (in-code сегодня)

`recovery.py:118-125` (комментарий перед whitelist'ом) уже
содержит формальные критерии:

> (a) их `operation_payload` carries a single `relative_path`,
> (b) они reasonably restorable by overwriting that one file,
> (c) их inverse semantics honestly captured by snapshot restore
>     (не e.g. `delete_module` whose snapshot still contains the
>     dependent code that referenced it).

Track F formalize'ует этот контракт в отдельный документ Step 3 и
расширяет whitelist строго в его рамках.

### 2.3 Informational set `_KNOWN_WRITE_TOOL_FAMILIES`

`recovery.py:139-153` содержит 11-tool список, по которому
assistant печатает honest «snapshot-restore is the manual path»
hints для non-whitelisted ops:

```
add_catalog_attribute, add_document_attribute,
append_module_method, create_catalog, create_common_module,
create_managed_form, add_form_element, update_module_code,
replace_module_method_body, apply_config_from_files,
update_database_configuration
```

Это — известный инвентарь write-tool families, по которому Step 2
audit пройдётся per-tool eligibility evaluation.

### 2.4 Архитектурный context

Платформа **не делает** новые MCP tools на этом треке: registries
`read=15 / write=25 / intelligence=16` остаются без drift'а на
всём Track F. Public `restore_dump_file_from_snapshot` уже
существует (Phase 6 / Step 4) и используется как есть. Расширение
whitelist'а — это **single-file change** в `recovery.py` с
per-tool verification, что operation_payload satisfies criteria
a/b/c.

## 3. Gap / problem statement

**Сегодняшний honest gap:** существующий strong write-path
(create_/add_/append_/replace_/update_ ops + два real-write tools
`apply_config_from_files` / `update_database_configuration`)
покрывается **automatic recovery** только для 2 из 25 mutating
tools (8% surface). Это:

1. **Создаёт асимметричный operator UX.** Operator может
   уверенно прогнать `add_catalog_attribute` зная, что
   `run_rollback_assistant` имеет `mode='executed'` path.
   Для symmetric `add_form_attribute` (Phase 6 / Step 5) тот
   же ассистент возвращает `mode='unsupported'` несмотря на то,
   что **технически** inverse semantics такие же (single-file
   XML restore через DOM-level pre-state).
2. **Не отражает существующую готовность mechanism'а.**
   `restore_dump_file_from_snapshot` уже принимает
   `(environment, relative_path, snapshot_file_path, label)` и
   готов к использованию для любого file-based mutating tool с
   single `relative_path` payload. Whitelist — это просто
   **конфигурация**, какие tool families разрешены.
3. **Хвост уже честно зафиксирован как future work.** Phase 6
   docs / Track A plan / Track D plan — все ссылаются на
   «полная rollback-вселенная не покрыта» как explicit
   post-phase parallel track follow-up.

Track F закрывает эти три риска **узко**: документированный
eligibility contract + per-tool evaluation + точечное расширение
whitelist'а на subset, чьи inverse semantics проверены вручную.
**Не больше.**

## 4. Целевой результат

После closure Track F у проекта есть:

1. **Formalized eligibility contract document** (Step 3
   deliverable) — formal a/b/c criteria + 3 runtime gates +
   post-verify discipline + non-goals; symmetric Track D /
   Step 2 contract style.
2. **Documented rollback baseline audit** (Step 2 deliverable) —
   per-tool evaluation `_KNOWN_WRITE_TOOL_FAMILIES` + Phase 6 /
   Step 5 `add_form_attribute`; разделение Tier 1 (strong
   candidates) / Tier 2 (нужна evaluation) / Tier 3
   (categorically excluded) / Tier 4 (already in whitelist);
   resolve Q2 (target set Step 4).
3. **Expanded `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset**
   (Step 4 deliverable) — точечно расширен до Step 2 / Q2
   target set; per-tool manual code review подтвердил, что
   operation_payload carries `relative_path` и что inverse
   semantics проходит criteria a/b/c.
4. **Aligned operator-facing docs** (Step 5 deliverable) —
   `apps/platform/README.md` («whitelist пуст»/«whitelist на
   двух tools» обновлено под фактический size); README /
   release-handoff «Limited rollback coverage» bullet;
   SECURITY.md если applicable.
5. **No blanket reversibility claim** — even after closure,
   Track F даёт «automatic recovery расширен на N tools по
   such-and-such criteria»; не «rollback теперь есть везде»;
   Tier 3 categorically excluded; multi-file / DB-meta ops
   остаются manual snapshot-restore territory.

## 5. Что входит в Track F

- Step 1 — planning (этот заход): plan + step-map docs +
  minimal README / PROJECT-STATUS update.
- Step 2 — rollback baseline audit + candidate selection
  (docs-only).
- Step 3 — rollback eligibility contract (docs-only).
- Step 4 — narrow whitelist implementation (single-file
  code change в `recovery.py`).
- Step 5 — operator/docs alignment.
- Step 6 — final integration pass + Track F closure.

## 6. Что НЕ входит в Track F

**Out-of-scope deliberately, никаких скрытых гэпов:**

- universal / arbitrary rollback для любого write-tool;
- AST-based semantic reverse engine для BSL / XML;
- broad policy engine rewrite;
- public `delete_*` write-tools (categorically out-of-scope —
  semantics удаления в 1С undecided; **не** часть Track F);
- multi-file / full filesystem snapshot-restore (single-file
  только; `restore_dump_file_from_snapshot` остаётся как есть);
- rollback для `apply_config_from_files` (multi-file impact —
  violates criterion (a)) и `update_database_configuration` (DB
  schema migration — violates criterion (b));
- rollback для `create_*` tools (`create_catalog`,
  `create_common_module`, `create_managed_form`) — inverse =
  delete; snapshot pre-create не содержит file'а;
  `restore_dump_file_from_snapshot` копирует **из** snapshot,
  не удаляет existing файлы; **критерий (c) violated**;
- новые MCP tools (registries `read=15 / write=25 /
  intelligence=16` без drift'а);
- изменения `restore_dump_file_from_snapshot` public API;
- изменения audit row format / `details` shape;
- execution-core rewrite, transport / UI / packaging work;
- enterprise governance / policy track, full QA program,
  performance / stress / fuzzing, multi-version 1С matrix
  expansion (Track E территория);
- web UI / dashboard frontend;
- 1cv8.exe runs (Track F работает над whitelist
  configuration, не над 1cv8 binary surface);
- remote push / GitHub publishing.

## 7. Guardrails

- **No new MCP tools.** Registries `read=15 / write=25 /
  intelligence=16` без drift'а на каждом step.
- **No back-door write channel.** Track F не добавляет
  filesystem write code в product layer; rollback по-прежнему
  идёт через public `restore_dump_file_from_snapshot`.
- **No audit format break.** Pre-Track-F audit rows остаются
  backward-compatible reader'ом (existing `details=None`
  handling сохраняется).
- **Eligibility a/b/c per tool.** Каждое имя в whitelist'е
  должно пройти manual code review против criteria — без
  «оптимистичного include».
- **Tier 3 categorical exclusion.** `apply_config_from_files`,
  `update_database_configuration`, `create_*` ops остаются
  out-of-whitelist по дизайну; их inverse semantics не
  покрывается single-file restore.
- **Production code touch:** только Step 4, только
  `apps/platform/src/onec_platform/recovery.py`. Никаких других
  файлов в `apps/`, `packages/`, `scripts/`,
  `pyproject.toml` (за исключением Step 6 closure version bump
  если Q5 resolved YES).
- **No 1cv8.exe runs anywhere в треке.** Track F работает над
  whitelist configuration; testing rollback assistant'а на
  real stand'е — отдельный operator-driven exercise, не часть
  трека.
- **No real credentials в repo / docs / commit messages.**

## 8. Acceptance criteria (closure)

Track F закрыт, если **все** ниже выполнены:

1. Step 1–6 пройдены последовательно; linear git history
   Step 1 → 2 → 3 → 4 → 5 → 6.
2. Step 2 audit doc существует; per-tool evaluation
   завершено; Tier 1 / 2 / 3 / 4 разделение зафиксировано;
   Q2 target set resolved.
3. Step 3 eligibility contract doc существует; a/b/c criteria
   formalized; runtime gates документированы; non-goals
   перечислены.
4. Step 4: `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset
   расширен до точного Step 2 target set; per-tool sanity
   check (manual code review) подтвердил criteria; pre-Track-F
   2 tools (`add_catalog_attribute`, `add_document_attribute`)
   остаются в whitelist'е; никаких unrelated changes в
   `recovery.py`.
5. Step 5 operator-facing docs aligned под актуальный
   whitelist size; «whitelist пуст»/«whitelist на двух tools»
   wording обновлён.
6. Registries `read=15 / write=25 / intelligence=16` без
   drift'а на всём треке; selfcheck_status=ok;
   verify-release.ps1 GREEN на 8 checks.
7. No back-door filesystem write введён в product layer.
8. Audit row format не сломан; pre-Track-F rows остаются
   backward-compatible.
9. Никаких 1cv8.exe runs; никаких real credentials в Track F
   commits.
10. Honest limits explicitly зафиксированы в closure docs:
    Tier 3 categorically excluded, no blanket reversibility
    claim, no public `delete_*`, no multi-file restore.

## 9. Honest constraints after closure

Даже после Track F закрытия **остаётся**:

- **No blanket multi-tool rollback.** Whitelist остаётся
  ограничен набором tools, чьи inverse semantics file-restore-
  compatible. Любой tool вне whitelist'а → `mode='unsupported'`.
- **No `delete_*` semantics.** Public `delete_*` write-tools
  по-прежнему отсутствуют; reverse операций `create_*`
  по-прежнему — manual operator job.
- **No multi-file restore.** `apply_config_from_files`-class
  operations по-прежнему manual snapshot-restore territory.
- **No DB schema rollback.** `update_database_configuration`
  inverse — operator's external backup; не Track F territory.
- **No transactional rollback.** Track F расширяет automatic
  recovery для отдельных file-based ops; multi-step transactions
  (e.g. apply + updatedb chain) не имеют atomic rollback.
- **No CI / regression suite.** Per-tool eligibility — manual
  code review; никакого automated test harness против
  rollback assistant runtime path.
- **No marketing claim.** Track F не говорит «1С Agent Platform
  has rollback». Track F говорит «automatic recovery covers N
  named tools by the documented contract; remaining tools
  remain manual snapshot-restore».

## 10. Связь с Track A / B / C / D / E

- **Track A** ship'нул real binary-backed write path; Track F
  не модифицирует write path.
- **Track B** ship'нул repo hygiene + install layer; Track F
  не задевает.
- **Track C** ship'нул release verify + handoff docs; Track F
  использует `verify-release.ps1` как есть для invariant
  checks.
- **Track D** ship'нул env-substitution credentials path;
  Track F не задевает credentials surface.
- **Track E** ship'нул multi-version smoke matrix scaffolding;
  Track F не задевает version evidence layer.

Track F — **первый post-Phase-6 track, который меняет
production code** в Phase 6 области (`recovery.py`). Track A
менял write-server runtime layer (`binary_dispatch.py`); Track D
менял write-server runtime layer (`binary_dispatch.py`); Track F
меняет product-layer recovery module. Все три — narrow,
single-file changes без architectural rewrite.

## 11. Open questions (Step 2+)

- **Q1 — eligibility criteria final formulation.** Default:
  formalize existing `recovery.py:118-125` comment в отдельный
  contract document (Step 3) — уточнить wording, добавить
  explicit Tier categorization, документировать 3 runtime gates.
  Resolve финально в Step 3.
- **Q2 — exact target set tools для Step 4.** Default
  candidate (subset Tier 1): **`add_form_attribute`** (Phase 6
  / Step 5 — single XML DOM edit), **`append_module_method`**
  (single BSL append), **`replace_module_method_body`** (single
  BSL edit). Возможно дополнительно `update_module_code`
  если Step 2 audit подтвердит operation_payload single
  `relative_path` shape. Минимум для closure non-trivial: 1
  additional tool; recommended 2-3; максимум для одного
  захода: 4. Resolve финально в Step 2.
- **Q3 — `restore_dump_file_from_snapshot` API changes.**
  Default: **НЕТ.** Public write-tool API остаётся как есть;
  Track F работает чисто на whitelist configuration уровне.
  Resolve финально в Step 3.
- **Q4 — audit row `details` format changes.** Default:
  **НЕТ.** Existing `details` shape (`operation_name`,
  `rollback_supported`, `backup_snapshot_path`,
  `dump_snapshot_path`, `relative_path`) уже несёт всё
  необходимое; pre-Track-F backward-compat reader сохраняется.
  Resolve финально в Step 3.
- **Q5 — closure version bump 0.2.0 → 0.3.0.** Default:
  **ДА.** Step 4 ship'ит real production code change
  (расширение `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset с
  functional delta — `automatic_recovery_supported=True`
  достижим для дополнительных tools). Это backward-compatible
  new functionality (existing 2 tools работают; pre-Track-F
  rows backward-compat); MINOR bump оправдан по SemVer.
  Resolve финально в Step 6.
- **Q6 — operator-facing docs scope для Step 5.** Default:
  `apps/platform/README.md` (whitelist size + behavior
  sections), `README.md` Quickstart Track A detail bullet
  «whitelist на двух tool'ах», `docs/release-handoff.md`
  «Limited rollback coverage» bullet. SECURITY.md — only if
  applicable (rollback не security-direct surface). Resolve
  финально в Step 5.
- **Q7 — server-side write-server code changes.** Default:
  **НЕТ.** Track F ограничивается
  `apps/platform/src/onec_platform/recovery.py`; никаких
  изменений в `apps/mcp-write-server/`, `apps/mcp-read-server/`,
  `apps/mcp-intelligence-server/`, `packages/*/src/`. Resolve
  финально в Step 4.
