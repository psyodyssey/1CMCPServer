# Track F — rollback eligibility contract

> **Companion files:**
> `track-f-rollback-whitelist-expansion-plan.md` (Step 1 plan),
> `track-f-rollback-whitelist-expansion-step-map.md` (Step 1
> step-map), `track-f-rollback-baseline-audit.md` (Step 2 audit).

> **Status:** Track F / Step 3 deliverable. Documentation-only.
> **Prescriptive normative contract** for Step 4 narrow whitelist
> implementation. Уровень формальности — RFC 2119-style:
> **MUST** / **MUST NOT** / **SHALL** / **MAY** имеют точный
> нормативный смысл. **Этот документ не меняет код**;
> он формулирует правила, которым Step 4 обязан следовать.

---

## 1. Purpose / scope

Этот документ — **нормативный contract** для Track F / Step 4
(narrow whitelist implementation). Он отвечает на **один**
вопрос:

> «По каким exact правилам tool допускается к narrow rollback
> whitelist expansion в рамках Track F, и какие invariants
> Step 4 implementation обязан соблюдать?»

Документ нормирует:

- **eligibility criteria** для tool-кандидатов;
- **exclusions**, которые остаются hard out-of-scope;
- **exact Step 4 implementation boundary** (target set + minimal
  code touches + invariant preservation);
- **backward compatibility guarantees** для existing rollback
  surface.

Документ **не** нормирует и **не** покрывает:

- per-tool descriptive evaluation (это Step 2 audit territory
  — `track-f-rollback-baseline-audit.md`);
- in-code comment / constant rewrites (`recovery.py:118-125`
  comment остаётся как есть; этот document — отдельная
  documentation layer);
- runtime testing methodology (Track F не запускает 1cv8.exe);
- operator-facing wording alignment (это Step 5 deliverable);
- closure narrative / version bump decision (это Step 6
  deliverable; Q5 resolved финально только в Step 6).

---

## 2. Relationship to Step 2 audit

Track F deliberately разделяет **descriptive** и **normative**
layers, чтобы каждый layer оставался single source of truth по
своей роли:

| Step | Role | Language style | Source of truth для |
|---|---|---|---|
| Step 2 audit (`track-f-rollback-baseline-audit.md`) | **descriptive** | observational, past tense | current baseline, per-tool tier breakdown, Q2 target set selection |
| Step 3 contract (this doc) | **normative** | prescriptive, MUST/MAY | eligibility rules, Step 4 boundary, exclusions, backward-compat guarantees |
| Step 4 implementation | **execution** | code change | actual whitelist expansion в обоих mirror frozenset'ах |

**Step 3 contract MUST NOT** дублировать per-tool tier
breakdown из Step 2 audit. Reader, который ищет per-tool
rationale, обращается к Step 2 audit. Reader, который ищет
формальные правила обязательств для Step 4 implementation,
обращается сюда.

**Step 3 contract MUST NOT** revising Step 2 target set без
proven blocker'а. Если Step 4 obnaружит implementation issue
для одного из 4 target tools — его обработка должна следовать
Section 6.4 escape clause этого contract'а, не silent
target-set drift.

---

## 3. Current rollback model (нормативный recap)

Track F operates **only inside** existing rollback model. Этот
section фиксирует model на которую опирается contract; никаких
изменений model'и Step 4 не делает.

- **Snapshot-restore based.** Rollback semantics — копирование
  одного pre-state file из existing dump-snapshot tree обратно
  в dump path. **No multi-file restore**, **no semantic
  inversion**, **no DB-level rollback**.
- **Public write-tool driven.** Rollback execution идёт через
  public `mcp_write_server.tools.restore_dump_file_from_snapshot`,
  proходящий через `run_write_flow` (preflight → snapshot →
  operation → verify → audit). **No back-door filesystem
  channel** в product layer'е.
- **Two-frozenset whitelist.** Eligibility encoded в **двух**
  mirror frozenset'ах:
  - `apps/platform/src/onec_platform/recovery.py:_AUTOMATIC_RECOVERY_SUPPORTED`
    (product layer);
  - `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py:_ROLLBACK_SUPPORTED_OPERATIONS`
    (write-server runtime layer).
- **Three runtime gates** (recovery.py + apps/platform/README:874-881):
  `mode='executed'` достижим **только** при одновременном:
  (1) tool name в whitelist; (2) audit row carries non-None
  `details`; (3) `details` содержит non-empty
  `dump_snapshot_path` AND `relative_path`.
- **Post-rollback verify discipline.** Success считается ровно
  тогда, когда `restore.ok=True` AND
  `diff_dump_fragment(env, relative_path, baseline_text).data.changed=False`.
- **Practical criterion (a) operationally encoded** as
  `flow.py:_RELATIVE_PATH_KEYS = ('catalog_relative_path',
  'document_relative_path', 'module_relative_path',
  'relative_path')`. `_extract_relative_path(operation_payload)`
  silently returns None для key вне этого 4-элементного tuple.

**Track F MUST NOT** изменять any of вышеперечисленных
constants кроме whitelist set membership. Step 4
implementation MUST add new tool names в **обе** frozenset'ы;
никаких других changes в `recovery.py` / `flow.py` Track F не
санкционирует.

---

## 4. Exact eligibility criteria

Tool name **MAY** быть added в `_AUTOMATIC_RECOVERY_SUPPORTED`
и `_ROLLBACK_SUPPORTED_OPERATIONS` **только если** все
нижеперечисленные criteria одновременно выполнены. Failure
любого criterion — tool **MUST** оставаться вне whitelist'а.

### 4.A — Payload shape criterion

**Statement.** Tool's `operation_callable` (передаваемое в
`run_write_flow`) **MUST** возвращать dict, содержащий ровно
один **non-empty string** value по одному из следующих keys:

```
"catalog_relative_path"
"document_relative_path"
"module_relative_path"
"relative_path"
```

**Rationale.** `flow.py:_RELATIVE_PATH_KEYS` это hard contract
для `_extract_relative_path`. Любой другой key (e.g. `target`,
`module_path`, `dump_relative_path`) silently игнорируется и
audit row будет omit `details.relative_path` → runtime gate (3)
fail → `mode='unsupported'`. Whitelist membership без payload
key match даёт false positive в `success_details["rollback_supported"]`
без actual recovery capability.

**MUST NOT.** Step 4 **MUST NOT** обходить criterion 4.A
расширением `_RELATIVE_PATH_KEYS` или добавлением tool-specific
extraction logic. Если у tool'а payload key вне current set —
tool **MUST** оставаться deferred до tool-side normalization
(вне Track F scope).

**Verification at Step 4.** Per-tool manual code review
**MUST** подтвердить exact line + key для каждого new tool в
target set. Step 4 commit message **MUST** ссылаться на эти
line numbers как evidence.

### 4.B — Restore semantics criterion

**Statement.** Inverse операции tool'а **MUST** быть полностью
покрыта **single-file overwrite** из pre-state snapshot.
Specifically:

1. Pre-state file **MUST** существовать в момент создания
   pre-mutating snapshot (т.е. перед операцией file существовал
   на disk и попал в snapshot tree).
2. Inverse **MUST NOT** требовать coordinated multi-file
   restore.
3. Inverse **MUST NOT** требовать deletion existing file
   (snapshot restore копирует **из** snapshot **в** dump; нет
   semantics удаления).
4. Inverse **MUST NOT** иметь side effects beyond restored
   file (e.g. внешние database mutations, cross-file references
   которые ломаются после restore).

**Rationale.** `restore_dump_file_from_snapshot(env,
relative_path, snapshot_file_path, label)` — single-file
copy operation. Любая операция с pre-state-creates-file
semantics (`create_*` family) violates clause 1; multi-file
ops (`apply_config_from_files`) violate clause 2; semantic-
only ops (`update_database_configuration`) violate clauses
1-2-4.

**MUST NOT.** Step 4 **MUST NOT** добавлять multi-file
restore tool, deletion tool, или semantic inversion engine.

### 4.C — Verification criterion

**Statement.** Rollback success **MUST** оставаться verifiable
через existing post-restore discipline:

1. `restore_dump_file_from_snapshot` возвращает `ok=True`;
2. `diff_dump_fragment(env, relative_path, baseline_text)`
   возвращает `data.changed=False` для baseline equal к
   snapshot file content.

**MUST NOT.** Step 4 **MUST NOT** вводить new verification
tool, new diff tool, new comparison semantics. Existing
`diff_dump_fragment` discipline покрывает все 4 target tools
(их inverse — restore single XML / BSL file; existing diff
работает по-байтово).

### 4.D — Sync / implementation discipline criterion

**Statement.** Whitelist constants encoded в **двух** mirror
frozenset'ах (см. Section 3). Step 4 implementation **MUST**:

1. **Update both** `_AUTOMATIC_RECOVERY_SUPPORTED` (recovery.py)
   AND `_ROLLBACK_SUPPORTED_OPERATIONS` (flow.py).
2. **Identical content.** После Step 4 обе frozenset'ы
   **MUST** содержать ровно identical set of strings.
3. **Single commit.** Synchronization **MUST** произойти в
   одном commit Step 4; partial update только одной стороны
   запрещён.
4. **No silent drift.** Step 4 **MUST NOT** оставлять comment
   `flow.py:100-103` («Keep the two in sync by hand for now —
   Step 4 ships exactly two entries») в устаревшем виде; minor
   wording update этого comment'а (e.g. «Step 4 ships X
   entries — keep in sync with recovery.py») **MAY** быть
   включён в Step 4 commit как часть minimal code touch.
5. **No mechanism change.** `_RELATIVE_PATH_KEYS`,
   `_extract_relative_path`, `_KNOWN_WRITE_TOOL_FAMILIES`,
   runtime gates в `recovery.py:285,869`, audit row formation
   в `flow.py:271-294` — **MUST** остаться без изменений.

**Rationale.** Two-frozenset model — design choice, не bug.
Расщепление позволяет product layer и write-server runtime
layer оставаться loosely coupled (write-server не зависит от
`apps/platform/`); цена — manual sync constraint. Track F
inherits эту constraint без попытки её устранить (устранение
требует архитектурного refactoring — out-of-scope Track F).

### 4.E — Non-expansion criterion

**Statement.** Step 4 **MUST** implement ровно target set,
selected в Step 2 audit (Q2 resolution):

```
{
    "add_form_attribute",
    "add_form_element",
    "append_module_method",
    "replace_module_method_body",
}
```

**MUST.** Step 4 commit **MUST**:

1. Add **exactly** эти 4 string literals в обе frozenset'ы.
2. Preserve existing 2 entries (`add_catalog_attribute`,
   `add_document_attribute`) без изменений.

**MUST NOT.** Step 4 **MUST NOT**:

1. Включать additional tool names «pока тут» (no opportunistic
   «while here» additions).
2. Удалять any existing whitelist entry.
3. Reorder existing entries без functional reason (frozenset
   semantics order-independent).
4. Расширять scope до Tier 2 candidates (`update_module_code`)
   без resolved blocker через отдельный track / step.
5. Добавлять Tier 3 categorically excluded tools (см. Section 5).

**Rationale.** Step 2 audit deliberately resolved Q2 narrowly
(2 → 6 tools, верхняя граница plan'а). Любое расширение target
set сверх audit'а ломает trust contract между descriptive
selection (Step 2) и normative implementation (Step 4).

### 4.F — Implementation surface criterion

**Statement.** Step 4 production code touches **MUST** быть
ограничены **двумя файлами**:

1. `apps/platform/src/onec_platform/recovery.py` — extension
   `_AUTOMATIC_RECOVERY_SUPPORTED` frozenset.
2. `apps/mcp-write-server/src/mcp_write_server/runtime/flow.py`
   — extension `_ROLLBACK_SUPPORTED_OPERATIONS` frozenset (и
   optional minor wording update sync comment'а).

**MUST NOT.** Step 4 **MUST NOT** trogать:

1. `apps/mcp-write-server/src/mcp_write_server/tools.py`
   (write-tool definitions);
2. `apps/mcp-read-server/`, `apps/mcp-intelligence-server/`,
   `apps/platform/` за пределами `recovery.py`;
3. `packages/*/src/`;
4. `scripts/`, `examples/`, `pyproject.toml` (closure version
   bump — Step 6 territory если Q5 = ДА);
5. `apps/platform/README.md` или другие operator-facing
   docs (это Step 5 deliverable);
6. `docs/architecture/track-f-*` (Step 1 / 2 / 3 deliverables
   — frozen historical anchors);
7. tests / runtime fixtures (если такой harness существует —
   Step 4 не вводит новые tests).

**Rationale.** Минимальная implementation surface = минимальный
risk regression + clean reviewability. Любое расширение surface
требует separate justification и обычно — separate track /
step.

---

## 5. Exact exclusions (out-of-scope)

Следующие классы операций **MUST NOT** быть added в whitelist
в рамках Track F. Каждое exclusion — categorical, не conditional
on per-tool review.

### 5.1 — Multi-file operations

`apply_config_from_files` и любые потенциальные multi-file
mutating tools. **Reason:** violates Section 4.A (no single
relative_path) AND 4.B clause 2 (multi-file restore требует).
Inverse механизм — fundamentally different (multi-file
copytree restore tool, который Track F NOT ship'ит).

### 5.2 — DB / schema mutations

`update_database_configuration` и любые потенциальные DB
schema migration tools. **Reason:** violates Section 4.A (no
file-based payload) AND 4.B clauses 1, 4 (irreversible через
file-restore; DB binary state mutated). Inverse требует
external pre-migration database backup + manual restore через
1С platform tools — operator-level discipline, not platform-
level rollback.

### 5.3 — Create-* families без file-restore fit

`create_catalog`, `create_common_module`, `create_managed_form`
и любые потенциальные `create_*` tools. **Reason:** violates
Section 4.B clause 1 (pre-state file does NOT exist; snapshot
pre-create empty for that path). Restore copying **from**
snapshot **to** dump cannot delete existing file — это требует
public `delete_*` semantics, которая deliberately out-of-scope.

### 5.4 — Public delete_* expansion

Track F **MUST NOT** ship public `delete_*` write-tools (e.g.
`delete_catalog_attribute`, `remove_module_method`,
`delete_catalog`). **Reason:** semantics удаления в 1С
undecided; introducing them — отдельный design decision требующий
separate track. Track F operates within snapshot-restore
model only.

### 5.5 — AST semantic inversion

Track F **MUST NOT** add BSL / XML AST parser, semantic
diff/patch engine, structural inverse computation. **Reason:**
вне scope file-byte-restore model. Tools которые нуждаются в
semantic inverse (e.g. `update_module_code` через структурное
diff'ование original vs new code) — отдельный technological
track.

### 5.6 — Multi-file restore framework

Track F **MUST NOT** ship multi-file restore tool, copytree-
restore boundary, or full filesystem snapshot rollback. Existing
single-file `restore_dump_file_from_snapshot` остаётся
exclusive mutating mechanism для rollback assistant.

### 5.7 — New recovery API

Track F **MUST NOT** add new public recovery API surface.
Specifically:

- `run_rollback_assistant(...)` signature **MUST** остаться
  unchanged;
- `restore_dump_file_from_snapshot(...)` signature **MUST**
  остаться unchanged;
- `_KNOWN_WRITE_TOOL_FAMILIES` set **MAY** быть extended
  Track F-related entries (informational only; не функциональное
  изменение), но это **OPTIONAL** — Step 4 может оставить set
  без изменений если minimal touch принципе предпочтителен.

### 5.8 — Audit / details shape changes

Track F **MUST NOT** изменять audit row `details` shape.
Existing fields (`operation_name`, `rollback_supported`,
`backup_snapshot_path`, `dump_snapshot_path`, `relative_path`)
покрывают все 4 target tools без изменений. Pre-Track-F audit
rows (with `details=None` или missing keys) **MUST** оставаться
backward-compatible — recovery degrades to `mode='unsupported'`
honestly.

### 5.9 — Transport / UI / packaging / new MCP surface

Track F **MUST NOT** trogать:

- production-grade MCP transport / authentication / network
  hardening;
- web UI, dashboard frontend, GUI installer;
- packaging ecosystem (`.msi` / `.deb` / signed distribution);
- new MCP tools registry expansion (registries
  `read=15 / write=25 / intelligence=16` **MUST** остаться без
  drift'а на всём треке);
- `restore_dump_file_from_snapshot` API расширение.

---

## 6. Exact Step 4 implementation boundary

### 6.1 — Exact target set

Step 4 **MUST** add ровно эти 4 tool names в обе frozenset'ы:

1. `add_form_attribute`
2. `add_form_element`
3. `append_module_method`
4. `replace_module_method_body`

После Step 4 обе frozenset'ы (`_AUTOMATIC_RECOVERY_SUPPORTED`
в `recovery.py`, `_ROLLBACK_SUPPORTED_OPERATIONS` в `flow.py`)
**MUST** содержать ровно 6 entries:

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

### 6.2 — Per-tool sanity check

Step 4 commit message **MUST** включать per-tool sanity check
artifact, ссылающийся на line numbers `tools.py` где payload
key подтверждается:

| Tool | tools.py operation payload line | Payload key |
|---|---|---|
| `add_form_attribute` | 3512–3520 | `relative_path` |
| `add_form_element` | 2680–2687 | `relative_path` |
| `append_module_method` | 2833–2838 | `module_relative_path` |
| `replace_module_method_body` | 2994–2999 | `module_relative_path` |

Это — defence-in-depth повторение manual code review из Step 2
audit (`track-f-rollback-baseline-audit.md` Section 4 Tier 1).

### 6.3 — Allowed minor touches

Step 4 commit **MAY** включать дополнительно:

1. Minor wording update комментария `flow.py:100-103` (sync
   comment) — например, обновление «Step 4 ships exactly two
   entries» на «Track F / Step 4 ships six entries — keep in
   sync with recovery.py». **MUST** оставаться informational
   только, не functional.
2. Optional minor wording update комментария
   `recovery.py:118-125` (eligibility comment) — например,
   pointer на Step 3 contract document как formal source of
   truth для criteria. **MUST** не противоречить Step 3
   contract.

Эти minor touches — **OPTIONAL**. Step 4 commit **MAY**
ограничиваться чисто frozenset extensions; minimal-touch
preference applies.

### 6.4 — Escape clause (per-tool implementation issue)

Если Step 4 implementation обнаружит per-tool issue для одного
из 4 target tools (например, обнаружится что
`operation_callable` payload key изменился между Step 2 audit и
Step 4 implementation), Step 4 **MUST**:

1. Документировать issue прямо в Step 4 commit message;
2. **NOT silently dropping** этого tool из target set без
   commit-level disclosure;
3. Либо: defer этот tool через отдельный subsequent step
   (whitelist 5 tools instead of 6) — это считается honest
   narrow degrade, не Step 2 target set drift;
4. Либо: stop Step 4 entirely и open separate audit step для
   resolving issue — preserve Step 2 audit's selection
   integrity.

Step 4 **MUST NOT** «silently fix» обнаруженную issue
изменением `tools.py` или payload-key conventions без
explicit Track F scope расширения через отдельный track / step.

### 6.5 — Verification at Step 4

Step 4 commit **MUST** проходить verify-release.ps1 GREEN на
8 checks с full selfcheck. Specifically:

- registries `read=15 / write=25 / intelligence=16` без
  drift'а;
- `selfcheck_status=ok`;
- credential leak guard / credential template hygiene PASS.

Step 4 **MUST NOT** запускать 1cv8.exe. Per-tool sanity check —
manual code review only.

---

## 7. Backward compatibility statement

После Step 4 closure backward compatibility **MUST** сохраняться
по всем нижеперечисленным surfaces:

### 7.1 — Existing whitelisted tools

`add_catalog_attribute` и `add_document_attribute` **MUST**
оставаться в whitelist'е без поведенческих изменений. Существующие
code paths которые их используют (recovery.py, flow.py audit
formation, runtime gates) **MUST** работать identically.

### 7.2 — Recovery API shape

Public boundary functions **MUST** сохранить signatures без
изменений:

- `run_rollback_assistant(...)` — boundary в product layer'е;
- `restore_dump_file_from_snapshot(...)` — public write-tool;
- `prepare_rollback_hint(...)` — read-only tool;
- `get_operation_history(...)`, `inspect_operation(...)` —
  read-only boundaries.

ToolResult shape, RECOVERY_MODES (`preview`, `executed`,
`blocked`, `unsupported`, `rejected`), payload field
conventions — **MUST** остаться идентичными.

### 7.3 — Audit row `details` shape

`details` dict shape:

```
{
    "operation_name": str,
    "rollback_supported": bool,
    "backup_snapshot_path": str | absent,
    "dump_snapshot_path": str | absent,
    "relative_path": str | absent,
}
```

— **MUST** остаться без изменений. Pre-Track-F audit rows
(где `details=None` или некоторые keys missing) **MUST**
читаться backward-compatible; recovery degrades to
`mode='unsupported'` honest.

### 7.4 — `_KNOWN_WRITE_TOOL_FAMILIES`

Step 4 **MAY** оставить set без изменений (он — informational
hint surface для assistant-side messages, не functional gate).
Если Step 4 включает новые target tools в этот set — это
**OPTIONAL** minor doc-only change, не функциональное.

### 7.5 — Invariants preserved

- **No new MCP tools.** Registries `read=15 / write=25 /
  intelligence=16` без drift'а.
- **No back-door write channel.** Product layer
  (`recovery.py`) сам не пишет файлы. Rollback execution идёт
  через public write-tool.
- **No new boundary in product layer.** `apps/platform/src/`
  surface unchanged.
- **No 1cv8.exe runs at any Track F step.** Track F operates
  на whitelist configuration уровне; никаких runtime
  invocations 1С binary'а Track F не делает.

---

## 8. Honest non-goals (повтор для ясности)

Track F (включая Step 4 implementation после этого contract'а)
**не**:

- ship'ит **universal rollback** для произвольного write-tool;
- ship'ит **arbitrary reverse semantics** через AST inversion
  или structural diff;
- ship'ит **multi-file restore framework**;
- ship'ит **public delete_* tools** для general reversibility;
- ship'ит **DB / schema rollback**;
- ship'ит **transactional rollback** для multi-step chains
  (e.g. apply + updatedb sequence не имеет atomic rollback);
- расширяет **`restore_dump_file_from_snapshot` API**;
- меняет **audit row `details` format**;
- meняет **registries** (`read=15 / write=25 / intelligence=16`);
- запускает **1cv8.exe** на любом шаге трека;
- даёт **blanket reversibility claim** даже после closure
  (после Step 4 — 6 of 25 mutating registry tools = 24%
  surface; 11 mutating tools остаются manual snapshot-restore
  territory by design).

---

## 9. Step 4 handoff note

После Step 3 closure (этот contract document shipped), Step 4
имеет:

1. **Exact target set** (Section 6.1) — нормативно фиксирован
   как 4 tool names.
2. **Per-tool sanity check evidence** (Section 6.2) — line-
   number anchors для defence-in-depth manual code review.
3. **Implementation surface** (Section 4.F) — 2 файла, обе
   frozenset'ы updated identically в одном commit.
4. **Allowed minor touches** (Section 6.3) — sync comment
   wording update, eligibility comment pointer.
5. **Escape clause** (Section 6.4) — поведение при per-tool
   implementation issue без silent target-set drift.
6. **Verification protocol** (Section 6.5) — verify-release.ps1
   GREEN on 8 checks; no 1cv8.exe runs.
7. **Backward compatibility guarantees** (Section 7) — что
   именно не должно сломаться.

Step 4 **MUST NOT**:

- расширять target set без resolved blocker через separate
  step (Section 4.E + Section 6.1);
- trogать write-tool definitions в `tools.py` (Section 4.F + 5.7);
- изменять `_RELATIVE_PATH_KEYS`, `_extract_relative_path`,
  audit row formation, или runtime gates (Section 3 +
  Section 4.D point 5);
- ship'ить multi-file / DB / AST inversion / public delete_*
  / new MCP surface (Section 5);
- запускать 1cv8.exe (Section 6.5);
- затрагивать operator-facing docs (это Step 5 territory).

После Step 4 closure project имеет:

- 6-tool whitelist (2 → 6, 2x growth);
- two mirror frozenset'ы synchronized;
- existing recovery mechanism unchanged but applicable к
  expanded target set;
- per-tool sanity check evidence в commit history;
- ground для Step 5 wording alignment в operator-facing docs.

Step 5 (operator/docs alignment) и Step 6 (closure) — out of
scope этого contract'а; они оперируют над фактическим
post-Step-4 state.
