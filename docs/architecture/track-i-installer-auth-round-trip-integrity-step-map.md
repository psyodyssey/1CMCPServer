# Parallel Track I — Installer Auth Round-Trip Integrity (step map)

> **Companion file:**
> `track-i-installer-auth-round-trip-integrity-plan.md`
> (план трека). Этот файл — пошаговый map. Каждый шаг
> открывается отдельным заходом, не комбинируется в один
> commit с другим step'ом.

> **Track invariants** (повтор из плана §6; нарушение любого
> = stop and surface, не silent fix):
> - registries `read=15 / write=25 / intelligence=16` без
>   drift'а на каждом step;
> - никаких новых MCP tools;
> - Track H auth surfaces (`ProductAuthSettings`,
>   `ProductConfig.auth`, `_parse_auth`,
>   `_AUTH_ENV_TOKEN_RE`, `_network_transport.py`, three
>   `__main__.py`, `Authorization` header parsing,
>   case-insensitive scheme, `hmac.compare_digest`,
>   failure-equivalence rule) preserved byte-identical;
> - `mcp_common/__init__.py` `__all__` byte-identical
>   (10 names); никаких добавленных / удалённых /
>   переименованных public exports;
> - existing `_stdio_transport.py` byte-identical;
> - existing 3 `__main__.py` byte-identical;
> - existing `[project.scripts]` block byte-identical;
> - `[tool.hatch.build.targets.wheel] packages = []`
>   preserved (Track C honest constraint carried through);
> - никакого `[project.dependencies]` / `[project.optional-
>   dependencies]` block changes;
> - никакого back-door write channel; `run_write_flow`
>   discipline для write-tools preserved; read-only-by-
>   construction discipline для intelligence-server
>   preserved;
> - никаких 1cv8.exe runs ни на одном шаге трека (Track I
>   работает на install/materialization layer уровне);
> - production code touched **только в Step 4** и **только**
>   на explicit allowed surfaces (default expectation:
>   только `installer.py:_config_to_dict`; финал — Step 3
>   contract);
> - никаких real credentials в repo / docs / commit
>   messages; bearer tokens — только raw `${ENV:NAME}`
>   strings round-tripped as configuration data, никогда не
>   resolved at install time;
> - никакого secrets storage / vault / KMS / OS keychain
>   integration;
> - никакого packaging ecosystem (`.msi` / `.deb` / signed
>   distribution / PyPI publication / wheel publication)
>   beyond existing `[project.scripts]`;
> - никакого supervisor / service registration / hot reload
>   / web UI / standalone `apps/platform` entrypoint в
>   текущем scope трека;
> - GitHub remote push — operator action, не часть трека.

---

## Step 1 — planning installer auth round-trip integrity (этот шаг)

**Цель.** Зафиксировать документационный вход в Track I:
назначение трека, целевой результат, что закрывает / не
закрывает Track I, чем отличается от Tracks A–H, guardrails,
acceptance criteria, открытые вопросы Q1–Q7 с default
recommendations.

**Что меняем.** Только два planning-документа:

- `docs/architecture/track-i-installer-auth-round-trip-integrity-plan.md`
  (новый, plan-уровень).
- `docs/architecture/track-i-installer-auth-round-trip-integrity-step-map.md`
  (новый, step-map; этот файл).

Плюс минимальные status-правки в `README.md` и
`PROJECT-STATUS.md` под открытие active track'а I:

- `README.md` — Quickstart paragraph (после Track H closure
  говорит «Активного трека сейчас нет» — переводим в
  «Активный трек: Track I planning-only»); «Active parallel
  track» секция (после Track H closure компактна — добавляем
  minimal Track I opening block с pointer'ом на planning
  docs; никаких premature implementation claims).
- `PROJECT-STATUS.md` — header `Текущий шаг` + `Статус`
  (после Track H closure говорят «Активного шага нет» /
  `closed` для Track H — переводим в `in progress` для
  Track I / Step 1); добавляем одну новую per-step opening
  section
  `### Parallel Track I / Step 1 — planning installer auth
  round-trip integrity (завершён)` симметрично Track H /
  Step 1 / Track G / Step 1 patterns.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `examples/`, `LICENSE`,
`SECURITY.md`, `CHANGELOG.md`, `docs/release-handoff.md`,
`docs/operator-manual.md`, `docs/administrator-manual.md`,
`docs/developer-manual.md`, `docs/runbooks/*`,
`apps/platform/README.md`, `apps/*/src/**`,
`packages/*/src/**`, server `server.py` files, three
`__main__.py` files, `_stdio_transport.py` helper,
`_network_transport.py` helper, `installer.py` —
без изменений на Step 1.

**Результат.** Track I открыт как active planning-only трек.
Implementation Step 4 не открывается в этом же заходе.
Никаких production code changes; никаких registry changes;
никаких 1cv8.exe runs.

---

## Step 2 — installer round-trip baseline audit (docs-only)

**Цель.** Честно описать current state `installer.py:_config_to_dict`
с точки зрения round-trip preservation per existing section
(`product_name` / `profile_name` / `default_environment` /
`project.environments` / `servers` / `bootstrap` / `runtime` /
`enterprise` / `auth`), classify caждый existing emit branch,
зафиксировать factual evidence для Q1 / Q2 / Q3 final
resolution. Никакого code change.

**Что меняем.** Один новый descriptive audit-документ:

- `docs/architecture/track-i-installer-auth-round-trip-baseline-audit.md`
  (новый, descriptive read-only audit).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 2 (новая `### Parallel Track I / Step 2 —
installer round-trip baseline audit (завершён)` section
симметрично Track H / Step 2).

**Содержимое audit-документа** (минимальный obligatory
shape):

1. **Per-section inventory of `_config_to_dict`.** Каждая
   existing emit branch: точные file/line refs, какие fields
   эмитятся, какие conditions emit-only-when-divergent, какие
   default behaviours.
2. **4-class breakdown.** Каждая section классифицирована:
   - Class 1 — **already round-trip-safe** (mandatory sections
     emitted unconditionally или emit-only-when-divergent
     pattern preserved correctly);
   - Class 2 — **partially preserved** (если any) — например,
     fields на ProductConfig dataclass present, но не все
     эмитятся;
   - Class 3 — **dropped on round-trip** — точно where the
     gap lives (currently: only `auth` section);
   - Class 4 — **explicitly out-of-scope Track I** — fields,
     которые специально не должны emit'иться (например,
     resolved env values).
3. **Read-only evidence.** Подтверждённый inspection'ом:
   - exact file/line refs `_config_to_dict` (currently
     `installer.py:228`–`317`);
   - exact diff `ProductConfig` dataclass fields vs
     `_config_to_dict` emit branches (auth gap formally
     identified);
   - precedent for emit-only-when-divergent pattern (Phase
     6/Step 6 service-level fields; Phase 6/Step 8
     enterprise block).
4. **Q1 resolution.** Финальная implementation surface choice
   для Step 4 (default: только `installer.py`; alternative:
   `installer.py + _install_runner.py` с per-option
   reasoning). Default expectation: Q1 = installer.py only.
5. **Q2 resolution.** Финальные preservation rules:
   - `auth` section presence when source has non-empty
     `auth.tokens`;
   - `tokens` list shape as JSON array of strings;
   - order preservation;
   - raw `${ENV:NAME}` form preservation as configuration
     data;
   - empty/default behaviour (no implicit injection for
     pre-Track-H configs).
6. **Q3 resolution.** Финальные forbidden behaviours:
   - no env-resolution at install time;
   - no cleartext token writing;
   - no Track H auth model changes;
   - no secret storage introduction;
   - no broad packaging rewrite.
7. **Open questions для Step 3 contract.** Точная dataclass-
   to-dict projection shape, точная test/verification
   protocol structure, точная backward-compat assertion
   shape.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md` (после Step 1 уже открыл active track —
дополнительно не правим), three `__main__.py`,
`_stdio_transport.py`, `_network_transport.py`,
`installer.py` (production code не trogается на Step 2).

**Результат.** Q1 / Q2 / Q3 resolved; Step 3 contract имеет
фактическую basis. Production-код не правится. Registries
`15/25/16` без drift'а. Никаких 1cv8.exe runs.

---

## Step 3 — auth round-trip preservation contract (docs-only)

**Цель.** Зафиксировать exact prescriptive normative contract
для Step 4 narrow implementation slice — точные preservation
rules для `auth` section, точная shape Step 4 diff, точные
allowed / forbidden Step 4 file surfaces, точный verification
protocol. Никакого code change. Никакого 1cv8.exe.

**Что меняем.** Один новый prescriptive normative document:

- `docs/architecture/track-i-installer-auth-round-trip-contract.md`
  (новый, RFC 2119-style; MUST / MUST NOT / SHALL / SHOULD /
  MAY с точным нормативным смыслом).

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 3 (новая `### Parallel Track I / Step 3 —
auth round-trip preservation contract (завершён)` section).

**Минимальный obligatory shape contract'а** (mirror Track H
contract structure, ~12 sections):

1. **Purpose / scope.** Что contract нормирует, что не
   нормирует.
2. **Relationship to Step 1 plan and Step 2 audit.**
   Descriptive vs normative split.
3. **Inherited fixed decisions.** Q1 / Q2 / Q3 inherited
   resolution from Step 2 audit + carry-over из Track H §3.5
   out-of-scope items.
4. **Auth section preservation contract.** Exact emit
   branch shape (emit-only-when-divergent symmetric to
   `enterprise_block`); exact dict layout (`{"tokens":
   [...]}`); exact list ordering rule; exact byte-equality
   rule for `${ENV:NAME}` strings; exact empty/default
   behaviour.
5. **Backward compatibility contract.** Pre-Track-H configs
   round-trip byte-identical; stdio-only configs unchanged;
   configs without `auth` section still load. Existing
   Phase 6/Step 6 service-level + Phase 6/Step 8 enterprise
   round-trip behaviour byte-identical.
6. **Forbidden install-time behaviours.** No env-resolution;
   no cleartext token acceptance; no Track H auth model
   changes; no secret storage; no broad packaging changes;
   no `[project.scripts]` changes; no helper file
   introduction unless absolutely justified.
7. **Step 4 allowed file surfaces.** Default: only
   `apps/platform/src/onec_platform/installer.py`. If Step 2
   audit / Step 3 reasoning identifies sympathetic `_install_runner.py`
   need, contract documents exact scope. Default expectation:
   single file + no helper introduction.
8. **Step 4 forbidden file surfaces.** Exhaustive:
   `apps/*/src/*` (all three MCP servers); other
   `apps/platform/src/onec_platform/*.py` files
   (`bootstrap.py`, `loader.py`, `models.py`, `doctor.py`,
   `dashboard.py`, `enterprise.py`, `runtime.py`,
   `runtime_logs.py`, `process_control.py`,
   `realstand.py`, `recovery.py`, `state.py`,
   `templates.py`, `workflow.py`); `packages/*/src/*`;
   `scripts/*`; `examples/*`; `pyproject.toml`;
   `mcp_common/__init__.py`; `_stdio_transport.py`;
   `_network_transport.py`; three `__main__.py`; all docs
   за пределами Track I docs themselves; Track I planning /
   audit / contract docs (frozen Step 1 / 2 / 3 anchors);
   Track A-H architecture docs; `.github/`,
   `.editorconfig`, `.python-version`, `.gitignore`,
   `LICENSE`.
9. **Verification contract for Step 4.** Required positive
   checks (sample `ProductConfig` round-trip preservation
   проверен через `_config_to_dict` → `json.dumps` →
   `json.loads` → `load_product_config` cycle для
   non-empty / empty / default cases; Track H / Step 4
   smoke list re-runs without regression; verify-release.ps1
   GREEN); required negative checks (no 1cv8.exe; no real
   credentials; no registry drift; no new MCP tools; no
   forbidden surface touched; no env-resolution at install
   time).
10. **Backward compatibility statement.** Existing
    `bootstrap_product_from_json_file` post-write round-trip
    confirms readability; existing install fast path mode
    semantics (preview / executed / rejected) preserved.
11. **Honest non-goals.** Restate Track I §5 out-of-scope
    items so Step 4 reader does not chase plan.
12. **Step 4 handoff note.** Numbered preconditions Step 4
    MUST satisfy.

**Что НЕ меняем.** `apps/`, `packages/`, `scripts/`,
`pyproject.toml`, `SECURITY.md`, `CHANGELOG.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`README.md`.

**Результат.** Step 3 contract на диске; Step 4
implementation имеет точные allowed / forbidden file lists,
exact diff shape, exact verification protocol. Production-код
не правится. Registries `15/25/16` без drift'а. Никаких
1cv8.exe runs.

---

## Step 4 — narrow installer auth round-trip implementation

**Цель.** Единственный шаг Track I с production code change.
Реализовать ровно тот узкий implementation slice, который
зафиксирован в Step 3 contract: emit `auth` section через
`_config_to_dict` symmetric to existing `enterprise_block`
pattern. Никакого scope creep, никаких новых MCP tools,
никакого 1cv8.exe.

**Что меняем (default expected shape; финальный список —
Step 3 contract).**

- `apps/platform/src/onec_platform/installer.py` —
  modification к `_config_to_dict(config: ProductConfig) ->
  dict`. Default expected diff shape (~10–15 LOC) symmetric
  к existing `enterprise_block`:

  ```python
  # After the existing enterprise_block emit logic
  # (currently around line 314):
  auth_block: dict[str, Any] = {}
  if config.auth.tokens:
      auth_block["tokens"] = list(config.auth.tokens)
  if auth_block:
      out["auth"] = auth_block
  ```

  Точный финальный shape — Step 3 contract (включая exact
  position в functon, exact comment text, exact handling
  edge cases).

**Что НЕ меняем (forbidden Step 4 surfaces; финальный
список — Step 3 contract).**

- `apps/platform/src/onec_platform/models.py` —
  `ProductAuthSettings` / `ProductConfig.auth` byte-
  identical;
- `apps/platform/src/onec_platform/loader.py` —
  `_parse_auth` / `_AUTH_ENV_TOKEN_RE` byte-identical;
- `apps/platform/src/onec_platform/{bootstrap,doctor,
  dashboard,enterprise,process_control,realstand,recovery,
  runtime,runtime_logs,state,templates,workflow}.py`
  byte-identical;
- `_install_runner.py` byte-identical (default; resolve
  иначе только если Step 3 contract это явно требует);
- `apps/*/src/**` — все 3 MCP server packages
  byte-identical (server.py, tools.py, models.py,
  runtime/*, three `__main__.py`);
- `packages/*/src/**` — все mcp_common / onec_audit /
  onec_health / onec_policy_engine / onec_process_runner /
  onec_troubleshooting / onec_config byte-identical
  (`mcp_common/__init__.py` `__all__` preserved;
  `_stdio_transport.py`, `_network_transport.py` byte-
  identical);
- `scripts/*` — release / dev wrappers byte-identical;
- `pyproject.toml` — version, `[project.dependencies]`,
  `[project.optional-dependencies]`, `[project.scripts]`,
  `[tool.hatch.build.targets.wheel]` byte-identical (Q6
  version bump = Step 6 territory, не Step 4);
- `examples/*` — sample configs byte-identical;
- documentation за пределами status-правок в `PROJECT-STATUS.md`
  (closure narrative + per-step section) — `SECURITY.md`,
  `CHANGELOG.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `README.md` (Step 5/6
  territory); все Track I planning / audit / contract docs
  (frozen Step 1/2/3 anchors); все Track A-H architecture
  docs.

**Verification (минимально obligatory; финал — Step 3
contract).**

- Inline Python smoke harness (или эквивалент narrow
  artifact deleted before commit) демонстрирует:
  - `ProductConfig` с non-empty `auth.tokens=["${ENV:MCP_TOKEN}"]`
    проходит `_config_to_dict` → `json.dumps` →
    `json.loads` → `load_product_config` round-trip; final
    `ProductConfig.auth.tokens` byte-equal к исходному;
  - `ProductConfig` с empty `auth.tokens=[]` (default)
    проходит `_config_to_dict` round-trip; output dict
    **MUST NOT** содержит `"auth"` ключ;
  - pre-Track-H sample config (без `auth` section в JSON)
    проходит `load → _config_to_dict → dump` round-trip
    byte-identical к исходному JSON.
- Track H Step 4 smoke list re-runs without regression
  (per-server `--help`, HTTP startup negative tests,
  byte-identical 401 fail-closed, case-insensitive scheme,
  GET 405, non-`/mcp` 404, malformed JSON 400, wrong CT 415,
  unknown method 200+`-32601`, multi-Auth 400+`-32600`,
  notification 204, tools/call ping 200, cross-transport
  parity).
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks.
- Selfcheck registries `read=15 / write=25 /
  intelligence=16; status=ok`; `imports_ok=true`.
- Никаких 1cv8.exe runs.
- Никаких real credentials в commit / diff.

**Результат.** Auth round-trip preservation ship'нут как
narrow defect-fix; existing surfaces preserved byte-identical;
registries без drift'а; Track H surfaces preserved
byte-identical.

---

## Step 5 — operator docs and security alignment (docs-only)

**Цель.** Точечно выровнять operator-facing и security-
adjacent документацию под фактический post-Step-4 fix
state, без раздувания в closure narrative Step 6. Docs-only;
никакого production code change; никакого pyproject.toml;
никаких registry changes; никакого 1cv8.exe.

**Что меняем (predicted scope; финальный список — Step 5
inventory).**

1. **`SECURITY.md`** — обновить «Local stdio plus narrow
   HTTP+bearer transport baseline» block: removed «Known
   limitation in install fast path round-trip» bullet
   (gap → fixed); statement «`installer.py:_config_to_dict`
   does not yet emit the new `auth` section» replaced с
   correct post-Step-4 wording.
2. **`docs/release-handoff.md`** — обновить «What is NOT
   in this handoff» / «Known limitations» installer
   round-trip gap mentions.
3. **`apps/platform/README.md`** — обновить «Чего сейчас
   намеренно ещё нет» installer gap mention.
4. **`README.md`** — обновить Quickstart paragraph + "Что
   Quickstart не обещает" + active parallel track section
   (если remaining drift есть).
5. **`scripts/dev/launch.ps1` + `scripts/dev/README.md`** —
   только если operator-facing wording реально drift'ует;
   default expectation: не trogать (Track H Step 5 wording
   про launch.ps1 не упоминает installer gap directly).
6. **`scripts/release/README.md`** — possibly если install
   fast path documentation references the gap. Default:
   check во время Step 5 inventory; не пред-открывать.

Плюс минимальные status-правки в `PROJECT-STATUS.md` под
закрытие Step 5 (новая `### Parallel Track I / Step 5 —
operator docs and security alignment (завершён)` section).

**Что НЕ меняем.** Production code (`apps/*/src`,
`packages/*/src` — Step 5 docs-only by contract);
`pyproject.toml` (Q6 = Step 6 territory); registries / new
MCP tools (`read=15 / write=25 / intelligence=16` invariant);
`CHANGELOG.md` (новая `## 0.6.0 — Track I` section — Q6 /
Step 6 closure deliverable); все Track I planning / audit /
contract docs (frozen Step 1 / 2 / 3 anchors); Track A-H
docs.

**Результат.** Operator-facing docs не лгут об actual
post-Step-4 fix state. Никакой premature Track I closure
language. Никаких false claims про packaging / deployment /
enterprise being solved. verify-release.ps1 остаётся GREEN.
Registries без drift'а. Никаких 1cv8.exe runs.

---

## Step 6 — final integration pass and Track I closure

**Цель.** Закрыть весь Track I как documented status. Read-
only final integration check уже закрытых Steps 1-5, потом
минимальные closure-docs/status updates + `pyproject.toml`
version bump (Q6 resolve), потом final closure commit.
Никакого нового feature work, никаких новых MCP tools,
никакого remote push'а, никакого 1cv8.exe run.

**Pre-closure read-only check (mandatory gate).**

- working tree clean перед началом — gate PASS;
- git history линейная Step 1 → 2 → 3 → 4 → 5 → 6 (все
  commit'ы на месте; никаких accidental extra commits
  inside Track I scope);
- все Step 1–5 deliverables на диске: 3 architecture docs
  (plan + step-map + audit + contract — точное количество
  4, финал на основе Step 3 result), Step 4 implementation
  diff (`installer.py:_config_to_dict` extension); existing
  Track G + Track H artefacts preserved byte-identical;
- Step 5 operator-facing alignment confirmed;
- registries `read=15 / write=25 / intelligence=16` без
  drift'а;
- `verify-release.ps1 -AllowDirtyTree` GREEN на 8 checks
  с full selfcheck;
- no real credentials в diff'ах ни одного из пяти Track I
  commit'ов;
- никаких 1cv8.exe runs ни на одном шаге Track I.

**Q6 resolve (closure decision).** Default ДА (`0.5.0 →
0.6.0`) если Step 4 ship'нул real production code change с
observable configuration-round-trip behaviour delta. Final
reasoning — закрепляется в Step 6 commit body на основе
фактического Step 4 functional delta:

- Step 4 ship'нул real installer fix с **observable
  round-trip behaviour delta** — operator's `auth.tokens`
  declarations теперь preserved through install fast path
  materialization, что до Track I silently dropped →
  backward-compatible new functionality classifying as
  classic MINOR bump per SemVer → bump.
- Precedent: Track D `0.1.0 → 0.2.0`, Track F `0.2.0 →
  0.3.0`, Track G `0.3.0 → 0.4.0`, Track H `0.4.0 → 0.5.0`
  — все шли с MINOR bump на real production code change.
  Track E (no functional delta, scaffolding only) → no
  bump.
- Counter-consideration: Track I diff size меньше чем
  Tracks D/F/G/H. Could argue PATCH bump (`0.5.0 → 0.5.1`)
  на основе "narrow defect-fix" framing. Финальное
  решение — Step 6 closure decision на основе фактического
  Step 4 diff size + SemVer semantics review. Default =
  MINOR (`0.6.0`); PATCH (`0.5.1`) — alternative path
  только если Step 4 diff действительно tiny (~5 LOC) и
  framing честнее как defect-fix чем feature.

**Что меняем (closure-docs only; финальный scope = symmetric
с Track A-H closure pattern).**

- `pyproject.toml` — version `0.5.0` → `0.6.0` (если Q6 =
  ДА; default expected). Никаких других changes; existing
  `[project.scripts]` preserved; `[tool.hatch.build.targets.wheel]
  packages = []` preserved.
- `README.md` — Quickstart paragraph переписан под
  «Активного трека сейчас нет — Track I закрыт девятым по
  счёту post-phase треком»; «Closed parallel tracks» list
  дополнен Track I bullet'ом (восемь → девять закрытых
  треков); «Active parallel track» секция сжата под «нет
  активного трека» с pointer'ом на Track I detail;
  добавлена «Track I detail (закрыт)» секция полным блоком
  симметрично Track A/B/C/D/E/F/G/H detail (per-step
  bullets с commit hashes; что Track I реально закрыл; что
  Track I **не делает** «full installer ecosystem solved»;
  registry invariant; honest constraints).
- `PROJECT-STATUS.md` — header (`Текущий шаг` + `Статус`)
  обновлён под Track I closed + Q6 resolution явное
  упоминание + 6 commit hashes + factual Step 4 surface;
  общий narrative-блок переписан под closure; добавлены
  пять новых per-step секций (Steps 2/3/4/5/6) симметрично
  Track G / Step 2-6 + Track H / Step 2-6 patterns.
- `CHANGELOG.md` — добавлен новый раздел `## 0.6.0 —
  Parallel Track I — Installer Auth Round-Trip Integrity`
  (или `## 0.5.1 —` если Q6 = PATCH) с per-step outcomes,
  actual round-trip preservation surface, registry
  invariant carried through, honest constraints update,
  Active work = None.

**Что НЕ меняем (закрытый scope).** `apps/`, `packages/`,
`scripts/`, `examples/`, `.github/`, `.editorconfig`,
`.python-version`, `.gitignore`, `LICENSE`; `SECURITY.md`,
`docs/release-handoff.md`, `apps/platform/README.md`,
`scripts/dev/*` (Step 5 уже выровнял); Track I planning /
audit / contract docs (frozen Step 1 / 2 / 3 anchors);
Track A-H docs; runbooks; registries. `1cv8.exe` не
запускался ни на одном шаге Track I.

**Результат.** Track I закрыт как documented status. Все
10 acceptance criteria из плана §7 выполнены. Активного
трека нет; девять post-phase parallel track'ов
(A, B, C, D, E, F, G, H, I) закрыты последовательно;
открытие следующего трека — отдельное operator decision.
**GitHub remote push не часть Track I — repo готов к
выкладке, но пушить — operator action.**
