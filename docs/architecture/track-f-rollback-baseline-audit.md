# Track F — rollback baseline audit and candidate selection

> **Companion files:**
> `track-f-rollback-whitelist-expansion-plan.md`,
> `track-f-rollback-whitelist-expansion-step-map.md`,
> `track-f-rollback-eligibility-contract.md` (Step 3 partner —
> formalized contract).

> **Status:** Track F / Step 2 deliverable. Documentation-only.
> Read-only audit current rollback baseline + per-tool eligibility
> evaluation + exact Step 4 target set recommendation. **Никаких
> production-code changes**, никаких 1cv8.exe runs, никаких
> новых MCP tools. Все findings — результат manual code review
> source files, не runtime testing.

---

## 1. Purpose / scope

Этот документ отвечает на **один** вопрос:

> «Какой exact rollback baseline у проекта сейчас, и какой
> narrow candidate set разумно брать дальше в Step 4?»

Документ **не**:
- меняет production code (это Step 4);
- formalize'ует eligibility contract (это Step 3 — отдельный
  document);
- делает реальный rollback run (это operator-driven exercise
  out-of-scope Track F полностью);
- расширяет Track F scope за пределы whitelist configuration;
- обещает universal rollback или multi-file restore;
- предлагает new MCP tools / public `delete_*` / AST-based
  semantic reverse;
- alignning operator-facing docs (это Step 5).

Документ **строго отделяет** четыре категории кандидатов
(Tier 1 / Tier 2 / Tier 3 / Tier 4) и для каждой даёт per-tool
rationale на основе **manual code review** (см. section 6).

---

## 2. Current rollback baseline

### 2.1 Whitelist live в **двух** mirror frozenset'ах

**Это критический finding Step 2 audit'а:** existing rollback
baseline опирается на **two parallel frozenset'ы**, которые
обязаны быть синхронизированы вручную. Step 4 implementation
должен обновить **обе**:

1. `apps/platform/src/onec_platform/recovery.py:126-131` —
   `_AUTOMATIC_RECOVERY_SUPPORTED`:
   ```python
   _AUTOMATIC_RECOVERY_SUPPORTED: frozenset[str] = frozenset(
       {
           "add_catalog_attribute",
           "add_document_attribute",
       }
   )
   ```
   Используется `run_rollback_assistant` в `recovery.py:285,869`
   как gate для `mode='executed'` vs `mode='unsupported'`.

2. `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:104-109`
   — `_ROLLBACK_SUPPORTED_OPERATIONS`:
   ```python
   _ROLLBACK_SUPPORTED_OPERATIONS: frozenset[str] = frozenset(
       {
           "add_catalog_attribute",
           "add_document_attribute",
       }
   )
   ```
   Используется `run_write_flow` в `flow.py:280` для записи
   `success_details["rollback_supported"] = ...` в audit row.

**Comment в `flow.py:100-103`** явно говорит:
> `Keep the two in sync by hand for now (Step 4 ships exactly
> two entries).`

Step 4 Track F **обязан** обновить **обе** frozenset'ы одной
коммиточкой. Оба используют идентичный set strings; никакого
расхождения set'ов не должно появиться.

### 2.2 Existing recovery mechanism (high-level)

`run_rollback_assistant(...)` (boundary в product layer'е) на
`confirm_execute=True` + healthy dashboard + tool_name в
whitelist + audit row carries `details` с непустыми
`dump_snapshot_path` + `relative_path` →

→ вызывает public `mcp_write_server.tools.restore_dump_file_from_snapshot`
с `(environment, relative_path, snapshot_file_path, label)` →

→ proходит через `run_write_flow` (preflight + snapshot +
operation + verify + audit) →

→ post-rollback verify через `diff_dump_fragment(env,
relative_path, baseline_text)` →

→ success = `restore.ok=True AND diff.data.changed=False`.

**No back-door write channel:** product layer (`recovery.py`)
сам не пишет файлы; всё mutating идёт через public write-tool
(`restore_dump_file_from_snapshot` line 3139:
`intent = WriteIntent("restore_dump_file_from_snapshot",
relative_path)`).

### 2.3 Practical eligibility criterion (a) is hard-coded as `_RELATIVE_PATH_KEYS`

`apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:112-117`:

```python
_RELATIVE_PATH_KEYS: tuple[str, ...] = (
    "catalog_relative_path",
    "document_relative_path",
    "module_relative_path",
    "relative_path",
)
```

`flow.py:120-135` — `_extract_relative_path(operation_payload)`
делает best-effort lookup: для каждого key из этого ровно
четырёх-элементного tuple проверяет, является ли value
non-empty string. Если ни один key не matches → returns None →
`success_details["relative_path"]` **omitted**.

**Practical impact:** tool eligible per criterion (a) **только
если** его `operation_callable` returns dict с одним из этих
exact keys. Любой другой key (например, `target`,
`module_path`, `dump_relative_path`) — **не** eligible через
existing mechanism. Это hard contract.

### 2.4 Three runtime gates (recovery.py + apps/platform/README:874-881)

`automatic_recovery_supported=True` runtime достижим **только**
при одновременном выполнении:

1. `entry.tool_name in _AUTOMATIC_RECOVERY_SUPPORTED` (whitelist
   gate);
2. audit row carries non-None `details` dict;
3. `details` содержит non-empty `dump_snapshot_path` AND
   `relative_path`.

Любой пропущенный фактор → `mode='unsupported'` honest degrade
без write'а. Это автоматически закрывает pre-Track-F audit
rows (где `details=None`).

### 2.5 Existing eligibility comment (recovery.py:118-125)

`recovery.py:118-125` (комментарий перед `_AUTOMATIC_RECOVERY_SUPPORTED`):

> `Adding more tool families here in the future requires that:`
> `(a) their operation_payload carries a single relative_path,`
> `(b) they are reasonably restorable by overwriting that one
>     file,`
> `(c) their inverse semantics are honestly captured by snapshot
>     restore (not e.g. delete_module whose snapshot still
>     contains the dependent code that referenced it).`

Track F / Step 3 formalize'ует этот comment в отдельный
contract document. В этом audit'е criterion (a) интерпретируется
**operationally** через `_RELATIVE_PATH_KEYS` (см. 2.3 выше).

---

## 3. Audited write surface

Полный inventory `mcp-write-server` registry (25 tools per
`server.py:42-67`):

### 3.1 Group A — preflight / snapshot / audit infrastructure (7 tools, **NOT candidates**)

`ping`, `check_write_preconditions`, `create_backup_snapshot`,
`create_dump_snapshot`, `write_audit_record`,
`describe_last_write_operation`, `prepare_rollback_hint`.

**Why not candidates:** эти tools либо meta-функции (`ping`),
либо preflight/snapshot infrastructure (не mutating 1С базу
напрямую — они **формируют** dump trees, audit, rollback
hints), либо read-only views поверх audit. У них нет
mutating-with-restore-able-pre-state shape.
`create_dump_snapshot` через `/DumpConfigToFiles` — read-only из
перспективы 1С базы (см. Track E `frozen-smoke-v1`).

### 3.2 Group B — read-only verify (5 tools, **NOT candidates**)

`verify_module_contains`, `verify_object_exists`,
`verify_metadata_change`, `verify_attribute_exists`,
`diff_dump_fragment`.

**Why not candidates:** ToolResult-only read-only operations.
Не идут через `run_write_flow`, не пишут audit row, не carry
`operation_payload`. Categorical exclusion.

### 3.3 Group C — file-based mutating ops (7 tools — main audit focus)

Detailed per-tool evaluation в section 4.

### 3.4 Group D — create-new-object ops (3 tools)

`create_catalog`, `create_common_module`, `create_managed_form`.
Detailed per-tool evaluation в section 4.

### 3.5 Group E — multi-file / DB-meta ops (2 tools)

`apply_config_from_files`, `update_database_configuration`.
Detailed per-tool evaluation в section 4.

### 3.6 Group F — rollback infrastructure (1 tool, **NOT candidate**)

`restore_dump_file_from_snapshot`.

**Why not candidate:** это сам rollback tool. Включить его в
whitelist — meaningless (rollback'ить rollback). Categorical
exclusion.

---

## 4. Tiered candidate classification

Format каждого entry: tool name → краткая операция → manual
code review evidence (file/line + payload key) → eligibility
verdict (a/b/c) → tier.

### Tier 4 — already in whitelist

**`add_catalog_attribute`** — добавляет `<Attribute>` в
существующий `<Catalog>` XML.

- `tools.py:1583` — `intent = WriteIntent("add_catalog_attribute",
  catalog_name)`.
- `tools.py:1612,1636` — operation/verify payload includes
  `"catalog_relative_path": catalog_relative_path` ✅
  (matches `_RELATIVE_PATH_KEYS[0]`).
- (a) ✅ — single `catalog_relative_path`;
- (b) ✅ — restorable through file-overwrite;
- (c) ✅ — pre-state file существовал (catalog already
  existed); inverse через snapshot restore returns pre-state
  with attribute removed.
- **Tier 4** — already in whitelist. Reference precedent для
  Tier 1 audit.

**`add_document_attribute`** — симметричная операция для
`<Document>`.

- `tools.py:2013` — `intent = WriteIntent("add_document_attribute",
  document_name)`.
- `tools.py:2042,2071` — payload includes
  `"document_relative_path": document_relative_path` ✅
  (matches `_RELATIVE_PATH_KEYS[1]`).
- (a)/(b)/(c) — все ✅ симметрично.
- **Tier 4** — already in whitelist.

### Tier 1 — strong candidates (pass a/b/c, payload key in `_RELATIVE_PATH_KEYS`)

**`add_form_attribute`** (Phase 6 / Step 5) — добавляет
`<Attribute>` в `<Form>` через ElementTree DOM edit.

- `tools.py:3478` — `intent = WriteIntent("add_form_attribute",
  form_name)`.
- `tools.py:3512-3520` — operation payload contains
  `"relative_path": relative_path` ✅ (matches
  `_RELATIVE_PATH_KEYS[3]`).
- `tools.py:3505,3519` — `attributes_block_pre_existing` flag +
  `attributes_block_created` payload field. Если block был
  создан by operation, pre-state file НЕ содержал `<Attributes>` —
  snapshot restore returns to that exact pre-state, корректно.
- (a) ✅ — single `relative_path`;
- (b) ✅ — restorable through file-overwrite (DOM rewrite файла);
- (c) ✅ — pre-state file существовал (object file present
  до операции); ElementTree DOM edit полностью обратим через
  file-restore; new `<Attributes>` block creation тоже clean
  rollback (snapshot pre-state → no attributes block).
- **Tier 1** — strong candidate.

**`add_form_element`** — добавляет `<Element>` внутрь form's
`<Elements>` block через substring patch.

- `tools.py:2635` — `intent = WriteIntent("add_form_element",
  element_name)`.
- `tools.py:2680-2687` — operation payload contains
  `"relative_path": relative_path` ✅ (matches
  `_RELATIVE_PATH_KEYS[3]`).
- `tools.py:2666-2670` — operation требует existing
  `<Elements>` block в pre-state file (fail-closed если
  отсутствует); pre-state always carries clean structure.
- (a) ✅ — single `relative_path`;
- (b) ✅ — restorable through file-overwrite;
- (c) ✅ — pre-state file existed and contained valid
  `<Elements>` block; substring patch полностью обратим через
  file-restore.
- **Tier 1** — strong candidate. Note: использует substring
  patch (не DOM); inverse через snapshot restore работает
  одинаково — file restore byte-for-byte returns pre-state.

**`append_module_method`** — добавляет BSL `Процедура` /
`Функция` в существующий module file.

- `tools.py:2811` — `intent = WriteIntent("append_module_method",
  method_name)`.
- `tools.py:2833-2838` — operation payload contains
  `"module_relative_path": module_relative_path` ✅ (matches
  `_RELATIVE_PATH_KEYS[2]`).
- `tools.py:2825-2830` — fail-closed если method already
  declared (pre-state file существовал и содержал module).
- (a) ✅ — single `module_relative_path`;
- (b) ✅ — restorable through file-overwrite;
- (c) ✅ — pre-state file существовал и содержал module
  (без appended method); inverse через file-restore returns
  pre-state.
- **Tier 1** — strong candidate.

**`replace_module_method_body`** — заменяет body existing BSL
method, preserving signature.

- `tools.py:2949` — `intent = WriteIntent("replace_module_method_body",
  method_name)`.
- `tools.py:2994-2999` — operation payload contains
  `"module_relative_path": module_relative_path` ✅ (matches
  `_RELATIVE_PATH_KEYS[2]`).
- `tools.py:2876` — explicit `confirm_replace=True` gate
  (deliberately dangerous tool); fail-closed без `confirm`.
- `tools.py:2965-2987` — signature regex с unambiguous match
  requirement; fail-closed на ambiguous structure.
- (a) ✅ — single `module_relative_path`;
- (b) ✅ — restorable through file-overwrite;
- (c) ✅ — pre-state file существовал и содержал method
  (с original body); inverse через file-restore returns
  pre-state body.
- **Tier 1** — strong candidate. Tighter operator gate
  (`confirm_replace=True`) — это tool-level safety, не
  rollback-eligibility concern.

### Tier 2 — нужна доп. evaluation / payload key gap (defer)

**`update_module_code`** — overwrite contents existing module
file.

- `tools.py:887` — `intent = WriteIntent("update_module_code",
  module_relative_path)`.
- `tools.py:896-900` — operation payload contains
  `"target": module_relative_path` ❌ (key name `target` is
  **NOT** in `_RELATIVE_PATH_KEYS`).
- (a) **❌ practically violated** — `_extract_relative_path`
  scan не найдёт key; `details.relative_path` будет omitted;
  recovery degrades к `mode='unsupported'` даже если tool в
  whitelist'е.
- (b) ✅ structurally — single-file overwrite (operation
  fundamentally restorable);
- (c) ✅ structurally — pre-state file existed (overwrite
  presupposes existing target).

**Verdict:** **Tier 2 — defer.** Tool semantically eligible
(b/c clean), но practical inclusion blocked payload key naming
mismatch. Три option'а для будущего unblock'а:

1. Изменить `update_module_code.operation()` чтобы возвращал
   `module_relative_path` вместо `target` — **out-of-scope
   Track F** per Step 1 plan (Track F не задевает write-tool
   definitions в `tools.py`);
2. Добавить `target` в `_RELATIVE_PATH_KEYS` — но `target`
   слишком generic как key name; collision risk с другими
   payload contexts; **not recommended**;
3. Wait for normalization pass (отдельный hygiene track или
   tool maintenance work post-Track-F).

Track F **deferr** этот tool без attempting unblock в Step 4.
Step 5 docs alignment может явно упомянуть deferred status.

### Tier 3 — categorically excluded

**`create_catalog`** / **`create_common_module`** /
**`create_managed_form`** — create new objects.

- `tools.py:1867,944,2476` — все имеют WriteIntent.
- Operation payloads содержат `catalog_relative_path` (1904) /
  `module_relative_path` (968) / `relative_path` (2503) ✅
  technically (a) passes.
- (b) ✅ structurally — single-file write, file-overwriteable
  (по форме).
- (c) **❌ violated** — pre-state file did NOT exist before
  create. Snapshot pre-create captures состояние **без** этого
  file. `restore_dump_file_from_snapshot(env, relative_path,
  snapshot_file_path)` копирует **из** snapshot к dump path;
  если snapshot не содержит file, restore failure: либо
  `FileNotFoundError` для snapshot path, либо tool returns
  `ok=False`. Fundamental issue — **inverse семантика =
  delete file**, не restore.

**Practical impact:** даже если включить в whitelist, runtime
gate (3) `details.dump_snapshot_path + relative_path` пройдёт,
но `restore_dump_file_from_snapshot` сам fail'нёт fail-closed
с honest error. Это **behavioral correctness** через
fail-closed, но **не useful UX** — assistant не сделает то,
что operator ожидает («автоматически удалить созданный
объект»).

Inverse через `delete_*` write-tool — **отдельная семантика
удаления в 1С**, undecided; deliberately out-of-scope Track F.

**Verdict:** **Tier 3 — categorically excluded** в текущем
Track F scope. Их inverse semantics требует public `delete_*`
write-tool family, который **deliberately НЕ ship'ится**
Track F'ом.

**`apply_config_from_files`** — applies entire config tree из
dump path; multi-file impact.

- `tools.py:829` — `intent = WriteIntent("apply_config_from_files",
  source_dump_path)`.
- Operation payload (line 778+) — multi-file output; **не
  carries** один из `_RELATIVE_PATH_KEYS` (potentially
  thousands of files affected; нет single `relative_path`).
- (a) **❌ violated fundamentally** — multi-file impact, не
  single relative_path.
- (b) **❌ violated** — full restore требует multi-file
  copytree, не `restore_dump_file_from_snapshot` (single-file
  только).
- (c) **❌ violated** — inverse требует full pre-apply tree
  restore, не single-file snapshot copy.

**Verdict:** **Tier 3 — categorically excluded.** `apply_config_from_files`
нужен fundamentally different rollback mechanism (multi-file
restore tool, который **deliberately НЕ ship'ится** Track F'ом).

**`update_database_configuration`** — DB schema migration
through `/UpdateDBCfg`.

- `tools.py:1479` — `intent = WriteIntent("update_database_configuration",
  environment.base_id)`.
- Operation payload — DB metadata; **не file-based**.
- (a) **❌ violated** — нет relative_path в file system
  semantics.
- (b) **❌ violated fundamentally** — DB schema migration
  irreversible через file-restore (database state changed at
  binary level).
- (c) **❌ violated** — inverse требует external pre-migration
  database backup + manual restore through 1С platform tools,
  не platform-level rollback.

**Verdict:** **Tier 3 — categorically excluded.**
`update_database_configuration` rollback требует external DB
backup operator-level discipline, не Track F territory.

---

## 5. Exact Step 4 target set recommendation (Q2 resolution)

**Рекомендованный Step 4 target set — 4 tools (Tier 1):**

1. **`add_form_attribute`**
2. **`add_form_element`**
3. **`append_module_method`**
4. **`replace_module_method_body`**

**Rationale:**

- Все 4 имеют existing implementation в `tools.py` без изменений
  required;
- Все 4 проходят eligibility a/b/c per manual code review (см.
  section 4 Tier 1);
- Все 4 carry один из `_RELATIVE_PATH_KEYS` в operation_callable
  payload (verified line-by-line);
- Все 4 имеют clean pre-state file existence (criterion (c)
  holds);
- Track F plan допускал максимум 4 tools для одного захода
  (`track-f-rollback-whitelist-expansion-plan.md` Q2:
  «recommended 2-3 tools, максимум для одного захода: 4»). 4
  tools — на верхней границе recommended scope.
- 2x growth whitelist'а (2 → 6 tools); reasonable pace без
  «universal» fantasy.

**Exact Step 4 work:**

После расширения, оба mirror frozenset'а должны выглядеть так
(ровно 6 entries each, identical content):

```python
{
    "add_catalog_attribute",
    "add_document_attribute",
    "add_form_attribute",
    "add_form_element",
    "append_module_method",
    "replace_module_method_body",
}
```

Никаких других изменений в `recovery.py` / `flow.py` Step 4 не
делает. Никаких изменений в `tools.py` (write-tool definitions)
вообще. Никаких новых MCP tools.

### Tools explicitly deferred

**`update_module_code`** — Tier 2; payload key naming mismatch
(`target` vs `module_relative_path`); deferred pending tool
definition normalization (out-of-scope Track F).

### Tools explicitly excluded (Tier 3)

- `create_catalog`, `create_common_module`, `create_managed_form` —
  inverse = delete; нет public `delete_*` write-tool family;
  snapshot pre-create не содержит file для restore.
- `apply_config_from_files` — multi-file impact; criterion (a)
  violated fundamentally.
- `update_database_configuration` — DB schema migration;
  criteria (a), (b), (c) все violated; нужен external DB
  backup mechanism, not Track F.

---

## 6. Manual code review note

Этот audit основан **исключительно** на manual read-only
inspection source files:

- `apps/mcp-write-server/src/mcp_write_server/server.py:42-67`
  (registry — 25 tools confirmed).
- `apps/mcp-write-server/src/mcp_write_server/tools.py:872-3548`
  (all mutating tool definitions read line-by-line; payload
  keys verified).
- `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:100-294`
  (mirror frozenset + `_RELATIVE_PATH_KEYS` + audit row
  formation).
- `apps/platform/src/onec_platform/recovery.py:118-153,275-294,830-870`
  (whitelist + eligibility comment + runtime gates +
  rollback execution path).
- `packages/onec-policy-engine/src/onec_policy_engine/models.py:17-21`
  (WriteIntent shape — confirmed `target` is operator label,
  not relative_path).

**No runtime testing.** No `1cv8.exe` runs. No actual rollback
runs against any stand. No `python` execution of recovery code
path. Все findings — pure code-reading evidence.

**No wishful thinking.** Каждый Tier 1 candidate verified via
exact `operation_callable` return dict literal в source. Каждый
Tier 3 exclusion verified против criteria (a)/(b)/(c) с цитатой
relevant code section.

**No modification.** Этот audit document — **только**
descriptive snapshot текущего состояния. Никаких изменений в
`recovery.py`, `flow.py`, `tools.py`, registries, или любом
другом source file Step 2 не делал и не планирует.

---

## 7. Honest non-goals

Этот audit (и Track F в целом) **не**:

- ship'ит **universal rollback** для произвольного write-tool;
- ship'ит **multi-file rollback** (single-file restore только);
- ship'ит **reverse semantics для arbitrary create/delete/update
  families** — только narrow file-based mutating ops с known
  pre-state file existence;
- ship'ит **public `delete_*` write-tools** (semantics удаления
  в 1С undecided; categorically out-of-scope);
- ship'ит **DB / schema rollback** (`update_database_configuration`
  inverse требует external DB backup mechanism, not platform-
  level rollback);
- ship'ит **AST-based semantic inversion** для BSL / XML
  (file-byte-restore только, no semantic understanding);
- расширяет **`restore_dump_file_from_snapshot` API** (Step 4
  не задевает write-tool surface; whitelist расширение only);
- меняет **audit row `details` format** (existing shape
  достаточен; pre-Track-F backward-compat reader сохраняется);
- запускает **1cv8.exe** на любом шаге Track F (трек работает
  на whitelist configuration уровне, не на 1cv8 binary surface);
- делает **broad compatibility claim**: после Track F closure
  whitelist расширен на 4 tools (если Step 4 ship'ит default
  Q2 target set); этого **не** достаточно для blanket
  «rollback есть везде» claim.

---

## 8. Step 3 handoff note

После Step 2 closure (этот audit doc shipped), Step 3 формализует
eligibility contract в отдельный document
`docs/architecture/track-f-rollback-eligibility-contract.md`. Его
contract обязан:

- formalize criteria a/b/c из `recovery.py:118-125` comment'а
  как стандартизированный contract (без code change в comment'е);
- явно зафиксировать operationally that **criterion (a) =
  payload key in `_RELATIVE_PATH_KEYS`** (не general «single
  relative_path» wording);
- documentation 3 runtime gates из `recovery.py` /
  `apps/platform/README.md:874-881`;
- documentation post-rollback verify discipline через
  `diff_dump_fragment` + binary verdict semantics;
- backward compatibility statement (pre-Track-F audit rows
  без `details` остаются `mode='unsupported'` honest degrade);
- explicit non-goals list (мirror section 7 этого audit'а);
- resolve **Q3** (`restore_dump_file_from_snapshot` API без
  изменений) и **Q4** (audit row `details` format без
  изменений) явно.

Step 3 contract document **не** должен переписывать этот audit
или дублировать его per-tool evaluation. Step 3 — это
prescriptive contract; этот audit — descriptive snapshot. Они
дополняют друг друга.

После Step 3 closure Step 4 имеет:
- clear target set (этот audit, section 5);
- formal eligibility contract (Step 3 deliverable);

И может ship'нуть narrow 2-line code change в обе frozenset'ы
с per-tool sanity check artifact (manual code review repeated
для defence-in-depth) и без расширения scope.

---

## 9. Honest summary (one paragraph)

На сегодня (Track F / Step 2 closure) проект имеет automatic
rollback only для **2 of 25** write-tool registry surface
(`add_catalog_attribute`, `add_document_attribute`). Per-tool
audit 12 mutating tools (Group C/D/E) показал: **4 strong
candidates** (`add_form_attribute`, `add_form_element`,
`append_module_method`, `replace_module_method_body`) проходят
eligibility a/b/c через existing mechanism без ANY code
changes outside narrow whitelist update; **1 deferred**
candidate (`update_module_code`) blocked payload key naming
mismatch; **5 categorically excluded** (`create_*` × 3,
`apply_config_from_files`, `update_database_configuration`)
через violation criterion (c) (no inverse через snapshot
restore без public `delete_*`) либо criteria (a)/(b)
(multi-file / DB-schema). **Step 4 target set:** 4 Tier 1
tools, расширение whitelist'а 2 → 6 (две parallel mirror
frozenset'ы в `recovery.py` + `flow.py`). **No blanket
reversibility claim** даже после Track F closure: 6 of 25
mutating registry tools = 24% surface; 11 mutating tools
остаются manual snapshot-restore territory by design.
