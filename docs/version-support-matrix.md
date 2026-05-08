# Version Support Matrix — 1C Agent Platform

> **Track:** Parallel Track E — Multi-Version 1C Smoke Matrix.
> **Step:** Step 3 deliverable (matrix scaffolding).
> **Companion:** [`docs/runbooks/track-e-multi-version-smoke-matrix.md`](runbooks/track-e-multi-version-smoke-matrix.md)
> (operator runbook).
> **Frozen contract:** [`docs/architecture/track-e-smoke-scenario.md`](architecture/track-e-smoke-scenario.md).
> **Current evidence audit:** [`docs/architecture/track-e-current-evidence-audit.md`](architecture/track-e-current-evidence-audit.md).

---

## What this document is

Это **evidence table**, а не blanket support claim. Каждая row
ниже — это **одна** конкретная версия 1С, на которой был
прогнан конкретный (frozen) smoke scenario, с conkretным
verdict'ом и со ссылками на physical artifacts.

Что эта таблица **не** делает:

- **не** обещает «полную совместимость» с какой-либо версией;
- **не** заменяет full QA-программу, performance benchmarking,
  stress / load testing, fuzzing;
- **не** даёт enterprise certification;
- **не** делает feature parity claims между версиями;
- **не** гарантирует backwards compatibility для будущих
  версий, ещё не вышедших на момент row entry.

Что таблица делает:

- фиксирует **одну** evidence-row на версию по **одному и тому
  же** узкому сценарию (`frozen-smoke-v1`), чтобы results были
  comparable;
- даёт reader'у quick view of «что **именно** проверено и
  чем».

Любая корректировка scenario / column shape — отдельный track /
step (через bump до `frozen-smoke-v2`), не in-flight правка
таблицы.

---

## How rows are added

Future rows добавляются operator'ом по
[`docs/runbooks/track-e-multi-version-smoke-matrix.md`](runbooks/track-e-multi-version-smoke-matrix.md)
после фактического прогона `frozen-smoke-v1` на operator-
supplied 1С версии (Track E / Step 4 — operator gate).

Для добавления новой row:

1. Прогнать runbook на target version.
2. Дописать **одну** row в раздел «Evidence rows» ниже по
   12-column shape.
3. Закоммитить как часть Track E / Step 4 (отдельный commit).
4. Никаких real credentials, никакой PII / business data.

Если operator не имеет доступа к target version — row не
добавлять; отсутствие row = отсутствие evidence.

---

## Column contract (frozen, copy from Step 2 scenario doc)

Точный column contract (12 полей) зафиксирован в Step 2
scenario doc и не должен меняться без bump до
`frozen-smoke-v2`:

| # | Column | What goes there |
|---|---|---|
| 1 | Version family | `8.3.<minor>` (e.g. `8.3.27`) |
| 2 | Build | full build number (e.g. `1859`) |
| 3 | OS arch | `x64` / `x86` |
| 4 | Binary path | absolute path к `1cv8.exe` (operator-supplied; sanitised если internal-only) |
| 5 | Stand type | `file-based` (only baseline shape для Track E) |
| 6 | Scenario | `frozen-smoke-v1` для additional rows; reference row может иметь `stronger-than-frozen-smoke-v1` (см. ниже) |
| 7 | Run date | `YYYY-MM-DD` |
| 8 | Verdict | `PASS` / `FAIL` / `NOT RUN` |
| 9 | Audit row reference | path к operator's audit.jsonl + line N, или `none (smoke-v1 — no audit row)` для standalone smoke runs (`create_dump_snapshot` не идёт через `run_write_flow` → audit row не пишется by design) |
| 10 | Snapshot tree path | path к dump output на operator-side диске (или `<operator infra — not committed>`) |
| 11 | Key deviations | argv-grammar изменения / added flags, или `none` |
| 12 | Notes | короткий free-text комментарий, без PII / credentials |

---

## Evidence rows

> **Reading the rows:** каждая row представлена вертикально
> ниже (12 fields подряд), а не одной горизонтальной 12-column
> markdown table — это компромисс читаемости в plain text.
> Comparison между rows делается scan'ом по одинаковым полям.

### Row 1 — Reference (copy-only из Track A / Step 6 evidence)

> **Status:** existing evidence; **никакой новый прогон 1cv8.exe
> на Step 3 не делался**. Эта row копирует уже зафиксированные
> Track A / Step 6 artifacts. Её scope **шире**, чем
> `frozen-smoke-v1`, что явно отмечено ниже.

| # | Column | Value |
|---|---|---|
| 1 | Version family | `8.3.27` |
| 2 | Build | `1859` |
| 3 | OS arch | `x64` |
| 4 | Binary path | `C:/Program Files/1cv8/8.3.27.1859/bin/1cv8.exe` |
| 5 | Stand type | `file-based` (InfoBase6 — `C:/Users/user/Documents/InfoBase6`) |
| 6 | Scenario | **`stronger-than-frozen-smoke-v1`** — full Track A round-trip (`/DumpConfigToFiles` + `/LoadConfigFromFiles` + `/UpdateDBCfg`), не cut-down dump-only |
| 7 | Run date | `2026-05-07` (approximation per `audit.jsonl` file mtime; actual evidence — Track A / Step 6 closure event) |
| 8 | Verdict | `PASS` |
| 9 | Audit row reference | `examples/demo-dumps/infobase6/.audit/audit.jsonl` — **2 mutating rows** (line 1 — `apply_config_from_files`, line 2 — `update_database_configuration`); both carry populated `details.dump_snapshot_path`. Standalone `create_dump_snapshot` audit row не пишется by design (он не идёт через `run_write_flow`); pre-mutating dump-snapshot подтверждается через `details.dump_snapshot_path` mutating rows. |
| 10 | Snapshot tree path | dump tree: `examples/demo-dumps/infobase6/` (real `Configuration.xml`, `ConfigDumpInfo.xml`, `1Cv8.cf` + директории `Catalogs/`, `CommonModules/`, `Enums/`); per-stage snapshot trees: `examples/demo-dumps/_snapshots/dump-infobase6-file-step6-A2-dump`, `examples/demo-dumps/_snapshots/dump-infobase6-file-step6-A4-apply-1778104376`, `examples/demo-dumps/_snapshots/dump-infobase6-file-step6-A5-updatedb-1778104777` |
| 11 | Key deviations | `none` (reference baseline; argv grammar точно соответствует Track A runbook) |
| 12 | Notes | Reference row. **Copy-only** — не новый прогон. **Stronger-than-frozen-smoke-v1**: evidence covers full mutating round-trip (apply + updatedb), а не только cut-down `create_dump_snapshot`. Это обусловлено тем, что reference row копируется из existing Track A / Step 6 closure evidence, которая исторически проводилась как **полный** round-trip, до того как `frozen-smoke-v1` был сформулирован в Step 2. Honest payload discipline (mode/binary_invoked/exit_code/command_preview/stdout_excerpt/stderr_excerpt) populated в каждом ответе. |

### Additional rows

> **Currently empty.** Additional version evidence rows
> добавляются на Track E / Step 4 (operator gate). Step 3
> deliberately ship'ит matrix scaffolding с **только** reference
> row; никаких имитированных additional results, никаких
> placeholder'ов «coming soon».

Если на момент чтения этой таблицы дополнительных rows нет —
это означает буквально, что additional version evidence ещё не
зарегистрирован. Это **не** означает, что другие версии не
работают; это означает, что repo не делает claim про другие
версии до фактического evidence.

---

## Honest limitations

- **Reference row scope mismatch.** Reference row покрывает
  full Track A round-trip, что **шире**, чем
  `frozen-smoke-v1`. Любое сравнение reference row с
  additional rows должно учитывать это: PASS на reference row
  = full round-trip works; PASS на additional row =
  cut-down dump-only works. Это асимметрия by design (Step 2
  scenario doc, section 2.1: «Reference row не требует
  нового прогона на Step 4 — она копируется из existing
  audit'а»), не bug в matrix.
- **No build-level coverage claim.** Build-level разница
  внутри одной minor family (e.g. `8.3.27.1859` vs
  `8.3.27.1936`) **не** засчитывается за additional
  evidence. PASS row для `8.3.27.1859` не extrapolates на
  другие builds `8.3.27.<other>`.
- **No automated runner.** Нет CI runner'а для multi-version
  1cv8 в repo (это physical operator infrastructure).
  Каждая row — manual operator-driven прогон.
- **No production-grade evidence preservation.** Operator-side
  dump trees / audit.jsonl operator decides, что committable;
  matrix row — single source of truth для evidence claim, не
  full artifact archive.
- **Open-ended scope.** `frozen-smoke-v1` — minimum viable
  multi-version evidence unit. Расширение (например, до full
  round-trip per version) — отдельный track post-closure
  Track E.
- **Evidence не stale-detected.** Если 1С версия выпустит
  build с argv-grammar break после того, как row была
  добавлена, существующая row остаётся historically true,
  но не пересчитывается. Re-run после major version events —
  доброе дело, но не enforced.

---

## When this matrix should be re-read

- Перед любым support claim, который опирается на «работает
  на 1С версии X» — reader должен убедиться, что row для X
  существует и имеет `Verdict = PASS`.
- Перед открытием PR / track, который меняет
  `binary_dispatch.py` или argv-template handling — reader
  должен учесть current evidence breadth.
- Перед operator'ским handoff'ом сторонней команде — row'ы
  показывают reader'у границы доказанной поддержки.

---

## Where to read deeper

- **Frozen scenario contract:** [`docs/architecture/track-e-smoke-scenario.md`](architecture/track-e-smoke-scenario.md).
- **Current evidence audit:** [`docs/architecture/track-e-current-evidence-audit.md`](architecture/track-e-current-evidence-audit.md).
- **Operator runbook:** [`docs/runbooks/track-e-multi-version-smoke-matrix.md`](runbooks/track-e-multi-version-smoke-matrix.md).
- **Reference round-trip runbook (Track A):** [`docs/runbooks/track-a-reference-stand-round-trip.md`](runbooks/track-a-reference-stand-round-trip.md).
- **Track E plan / step-map:**
  [`docs/architecture/track-e-multi-version-smoke-matrix-plan.md`](architecture/track-e-multi-version-smoke-matrix-plan.md),
  [`docs/architecture/track-e-multi-version-smoke-matrix-step-map.md`](architecture/track-e-multi-version-smoke-matrix-step-map.md).
- **Release handoff (general project context):**
  [`docs/release-handoff.md`](release-handoff.md). Note: на
  момент Step 3 closure release-handoff still describes
  «No multi-version 1С smoke matrix» as honest constraint
  (single-version evidence). Это будет выровнено на Step 5
  per Track E step-map.
