# Parallel Track I — Installer Round-Trip Baseline Audit (Step 2)

> **Companion files:**
> `track-i-installer-auth-round-trip-integrity-plan.md` (Step 1
> plan), `track-i-installer-auth-round-trip-integrity-step-map.md`
> (Step 1 step-map). Этот документ — Step 2 deliverable:
> **descriptive read-only audit** текущего installer round-trip
> path относительно `auth` section, плюс evidence-grounded Step 2
> resolutions для Q1 / Q2 / Q3.

> **Status:** Track I / Step 2 deliverable. Documentation-only.
> **Descriptive**, не prescriptive: фиксирует current state и
> Step 2 directional answers; нормативные правила для Step 4
> implementation формализуются отдельно в Step 3 contract.

> **Этот документ ничего не реализует.** Никакого `installer.py`
> изменения, никакого нового helper'а, никакого `pyproject.toml`
> change'а — только read-only audit и направление для Step 3 /
> Step 4.

---

## 1. Purpose / scope

Этот документ — **descriptive Step 2 audit** для Track I.
Он отвечает на следующие вопросы на основе read-only inspection
текущего repository state:

1. Что фактически делает install fast-path round-trip path
   сейчас?
2. Какие sections `_config_to_dict` уже preserves, и по какой
   pattern logic (unconditional vs emit-only-when-divergent)?
3. Где именно `auth` section теряется, и почему это silent
   configuration data loss, а не silent insecure success?
4. Какие existing installer pattern'ы можно и нужно
   переиспользовать в Step 4?
5. Какой transport / auth surface остаётся byte-identically
   preserved через Track I (Track H carry-over invariants)?
6. Какой transport / auth surface MUST NOT be touched by Step
   4 (forbidden boundaries)?
7. Какой transport / auth surface готов как-есть к Step 4 fix
   (already-existing infrastructure on which the fix builds)?
8. Q1 (implementation surface для Step 4), Q2 (preservation
   target), Q3 (forbidden behaviours) — final descriptive
   resolutions для входа в Step 3 contract.

Документ **не**:

- ship'ит код (Step 4 territory);
- формулирует normative MUST/MUST NOT contract (Step 3
  territory);
- alignment'ит operator-facing docs (Step 5 territory);
- открывает closure narrative (Step 6 territory);
- pretend'ит, что installer round-trip уже fixed
  (zero-implementation document);
- меняет `apps/`, `packages/`, `scripts/`, `pyproject.toml`,
  registries, CHANGELOG, SECURITY, README, PROJECT-STATUS,
  release-handoff, apps/platform/README.

---

## 2. Method

Audit опирается на:

1. **Read-only inspection** `scripts/release/install.ps1` +
   `scripts/release/_install_runner.py` — operator-facing
   wrappers; Track B / Step 3 territory.
2. **Read-only inspection** `apps/platform/src/onec_platform/installer.py`
   с фокусом на `_config_to_dict(config: ProductConfig) ->
   dict` (Phase 6 / Step 3 entry) и `run_install_fast_path` /
   `run_install_fast_path_from_json_file` boundary helpers.
3. **Read-only inspection** `apps/platform/src/onec_platform/models.py`
   (`ProductAuthSettings`, `ProductConfig.auth` field) —
   Track H / Step 4 surfaces.
4. **Read-only inspection** `apps/platform/src/onec_platform/loader.py`
   (`_parse_auth`, `_AUTH_ENV_TOKEN_RE`, `load_product_config`
   wiring) — Track H / Step 4 surfaces.
5. **Read-only inspection** `packages/mcp-common/src/mcp_common/_network_transport.py`
   `_resolve_token_sources` boundary — для подтверждения
   gap classification (silent data loss vs silent insecure
   success).

Все evidence ниже подкреплены конкретными file/line
references; никаких inferred claims без anchor'а.

---

## 3. Current installer round-trip path

### 3.1 Operator entry point

`scripts/release/install.ps1` (Track B / Step 3, l.1-73) —
тонкий PowerShell-wrapper над `_install_runner.py`. Принимает
mandatory flags `-ConfigPath <input>` / `-OutputConfigPath
<output>` + optional `-Confirm` switch. Bootstraps PYTHONPATH
через `scripts/dev/bootstrap_paths.ps1`, then forwards to
the Python runner. Не содержит никакой config-shape логики;
не trogает `_config_to_dict`. Track I не trogает `install.ps1`.

### 3.2 Python runner

`scripts/release/_install_runner.py` (l.1-89) — argv parser
(positional 3 args), вызывает existing boundary
`run_install_fast_path_from_json_file(input, output_config_path,
confirm_write)` через `from onec_platform import ...`. Печатает
plain-text result fields (`ok`, `mode`, `product_name`,
`profile_name`, `default_environment`, `output_config_path`,
`config_written`, findings, recommended actions). Не содержит
config-shape логики; не trogает `_config_to_dict`. Track I не
trogает `_install_runner.py` (Q1 default — только `installer.py`).

### 3.3 Boundary helper

`apps/platform/src/onec_platform/installer.py:run_install_fast_path`
(l.~370-577) — orchestrator, **never raises**, returns
`InstallFastPathResult`. Sequence per docstring:

1. **Resolve input config.** `_resolve_input_config(data)`
   accepts pre-loaded `ProductConfig` или dict; on dict
   delegates to `load_product_config(...)` per loader
   contract.
2. **Inspect release layout.** `inspect_release_layout(...)`
   informational only.
3. **Pre-write bootstrap.** `bootstrap_product(_config_to_dict(config))`
   at l.431 — note: this passes the **projected dict** (через
   `_config_to_dict`) обратно в `bootstrap_product`, который
   снова вызывает `load_product_config(...)`. Это означает,
   что **pre-write bootstrap уже видит auth section как
   empty** (because `_config_to_dict` drops it pre-write
   too). Implication: existing `bootstrap_pre.message`
   нечестен относительно auth source-of-truth, потому что
   проецированный config уже потерял `auth.tokens`.
4. **Build template_preview.** `_config_to_dict(config)` at
   l.439 — повторный вызов того же projection function;
   результат сохраняется в `template_preview` для preview-
   mode operator inspection.
5. **Preview vs executed branch.** If `confirm_write=False`:
   stop, return `mode="preview"`, no file written. If
   `confirm_write=True`: refuse to overwrite existing target
   (`mode="rejected"`); otherwise atomically write
   `template_preview` JSON via `_write_product_config_template`,
   then re-load output file via `bootstrap_product_from_json_file`
   (post-write bootstrap).
6. **Post-write bootstrap** at l.531. Loads the freshly-
   written file через `load_product_config_from_json_file`.
   Если materialized JSON has no `auth` section, loader's
   `_parse_auth(None)` returns default empty
   `ProductAuthSettings(tokens=[])` — **valid load**, не
   error. So `bootstrap_post.ok = True`, no failure
   surfaced. This is exactly why the gap is silent.

### 3.4 Projection function

`apps/platform/src/onec_platform/installer.py:_config_to_dict`
(l.228-317, ~89 LOC) — **the single point of truth** for
`ProductConfig → dict` projection used by the install fast
path. Three observed emit patterns:

- **Mandatory unconditional emit.** `product_name`,
  `profile_name`, `default_environment`, `project`,
  `servers`, `bootstrap`, `runtime` are written into the
  output dict every time, even when their values are at
  defaults. `runtime` always emits a `runtime.services`
  dict (possibly empty).
- **Emit-only-when-divergent — service-level fields**
  (Phase 6 / Step 6, l.265-273). Per-service
  `restart_policy`, `logs_enabled`, `log_max_bytes`
  emitted only when divergent from dataclass defaults
  (`"never"`, `True`, `DEFAULT_LOG_MAX_BYTES`). Comment at
  l.265-267: «Phase 6 / Step 6 service-level fields. Emit
  each one only when it deviates from the dataclass default
  so Step 1–5 configs round-trip byte-identical.»
- **Emit-only-when-divergent — top-level enterprise block**
  (Phase 6 / Step 8, l.295-315). Builds local
  `enterprise_block: dict[str, Any] = {}`; appends each
  field only when it diverges from default (e.g.
  `e.deployment_tier is not None`,
  `e.change_control_required` is `True`); emits
  `out["enterprise"] = enterprise_block` **only if**
  `enterprise_block` is non-empty. Comment at l.295-299:
  «Phase 6 / Step 8 — preserve the operator's enterprise-
  foundation block through the install fast path round-
  trip. Emit only the fields that diverge from the empty
  default so Step 1–7 configs without an enterprise block
  remain byte-identical (no implicit `"enterprise":
  {...defaults...}` injection).»

There is **no `auth` block emit logic** anywhere в
`_config_to_dict`. Это и есть Track I gap.

### 3.5 Auth surfaces (Track H carry-over, byte-identical)

- `apps/platform/src/onec_platform/models.py:149` —
  `ProductAuthSettings(tokens: list[str] = field(default_factory=list))`
  dataclass.
- `apps/platform/src/onec_platform/models.py:207` —
  `ProductConfig.auth: ProductAuthSettings = field(default_factory=ProductAuthSettings)`.
- `apps/platform/src/onec_platform/loader.py:40` —
  `_AUTH_ENV_TOKEN_RE = re.compile(r"^\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}$")`
  (byte-identical к Track D pattern).
- `apps/platform/src/onec_platform/loader.py:142` —
  `auth = _parse_auth(data.get("auth"))` wired into
  `load_product_config`.
- `apps/platform/src/onec_platform/loader.py:439-498` —
  `_parse_auth(auth_raw) -> ProductAuthSettings` validator
  (unknown-keys reject; list-of-strings; per-entry
  env-substitution regex enforce; literal cleartext fail-
  closed at config-load time; `auth_raw is None` → empty
  default).
- `packages/mcp-common/src/mcp_common/_network_transport.py:_resolve_token_sources`
  — runtime boundary; reads `--auth-token-env` env var
  first (CLI wins precedence per Track H §10.5), else loads
  ProductConfig directly via
  `load_product_config_from_json_file` and reads
  `config.auth.tokens`. If neither source is available,
  fail-closed startup with operator-readable single-line
  stderr.

**Все 5 surfaces preserved byte-identical через Track I**
(Track H carry-over invariants; см. Track I plan §6
guardrail #3).

---

## 4. Per-section `_config_to_dict` inventory

Тable enumerates каждую logical section, текущий emit pattern,
и Track I action (если any).

| # | Section | Source field on `ProductConfig` | Emit pattern in `_config_to_dict` | File / line | Status | Track I action |
|---|---|---|---|---|---|---|
| 1 | `product_name` | `config.product_name: str` | mandatory unconditional | l.277 | already round-trip-safe | none |
| 2 | `profile_name` | `config.profile_name: str` | mandatory unconditional | l.278 | already round-trip-safe | none |
| 3 | `default_environment` | `config.default_environment: str` | mandatory unconditional | l.279 | already round-trip-safe | none |
| 4 | `project.environments` | `config.project.environments: dict[str, EnvironmentConfig]` | mandatory unconditional iteration; per-environment optional fields emitted only when non-`None` | l.235-255, l.280 | already round-trip-safe | none |
| 5 | `servers` | `config.servers: ProductServerToggles` | mandatory unconditional (3 booleans) | l.281-285 | already round-trip-safe | none |
| 6 | `bootstrap` | `config.bootstrap: ProductBootstrapSettings` | mandatory unconditional (4 fields) | l.286-291 | already round-trip-safe | none |
| 7 | `runtime` | `config.runtime: ProductRuntimeSettings` | mandatory unconditional `runtime.services` dict (possibly empty); per-service fields mix of unconditional and emit-only-when-divergent (Phase 6 / Step 6) | l.257-274, l.292 | already round-trip-safe (Phase 6 / Step 6 fix) | none |
| 8 | `enterprise` | `config.enterprise: EnterpriseFoundationSettings` | emit-only-when-divergent (Phase 6 / Step 8); `out["enterprise"] = enterprise_block` only if non-empty | l.295-315 | already round-trip-safe (Phase 6 / Step 8 fix) | none |
| 9 | **`auth`** | `config.auth: ProductAuthSettings` (Track H / Step 4) | **NOT EMITTED — no branch exists in `_config_to_dict`** | absent | **dropped on round-trip** | **Step 4 fix target** |

**Conclusion.** Out of 9 logical sections, 8 are already
round-trip-safe under one of two existing patterns
(unconditional or emit-only-when-divergent). Только
**`auth` (#9)** dropped. Track I scope = exactly one missing
emit branch, of the same shape as the existing `enterprise`
block.

---

## 5. Auth-specific round-trip gap

### 5.1 Concrete walk-through pre-Track-I

1. Operator пишет input config с valid auth section, e.g.:
   ```json
   {
     "product_name": "platform-prod",
     "profile_name": "prod",
     "project": {"environments": {"prod": {...}}},
     "default_environment": "prod",
     "auth": {"tokens": ["${ENV:MCP_PROD_TOKEN}"]}
   }
   ```
2. Operator runs:
   ```powershell
   .\scripts\release\install.ps1 `
       -ConfigPath input.config.json `
       -OutputConfigPath out.config.json `
       -Confirm
   ```
3. `install.ps1` → `_install_runner.py` → `run_install_fast_path_from_json_file(...)`.
4. `run_install_fast_path` (`installer.py`) loads input via
   `load_product_config_from_json_file` (через
   `_resolve_input_config`). Loader's `_parse_auth` accepts
   `["${ENV:MCP_PROD_TOKEN}"]` (matches `_AUTH_ENV_TOKEN_RE`),
   produces `ProductConfig.auth = ProductAuthSettings(tokens=["${ENV:MCP_PROD_TOKEN}"])`.
5. Pre-write bootstrap (l.431) calls
   `bootstrap_product(_config_to_dict(config))`. The
   projected dict уже не содержит `"auth"` ключа — pre-write
   bootstrap re-loads без auth section, `bootstrap_pre.ok =
   True` (because empty auth is valid default). Operator
   sees no warning here.
6. `template_preview = _config_to_dict(config)` (l.439).
   Same projected dict; still no `"auth"` key.
7. Atomic write of `template_preview` to `out.config.json`
   (через `_write_product_config_template`). Output file
   missing the `auth` section.
8. Post-write bootstrap (l.531) loads `out.config.json`.
   Loader's `_parse_auth(None)` returns
   `ProductAuthSettings(tokens=[])` (default empty). Loader
   succeeds. `bootstrap_post.ok = True`.
9. Operator sees `mode="executed"`, `config_written=True`,
   no error finding про auth. Round-trip considered
   "successful" by install fast-path's own criteria.

Steps 5, 6, 8 all silently drop the auth section without
surfacing it. The operator has no way to know from the
install fast-path output that their `auth.tokens`
declarations did not survive.

### 5.2 Operator-facing consequence

Eventually operator runs:
```powershell
python -m mcp_read_server `
    --transport http `
    --bind 127.0.0.1:8765 `
    --config-path out.config.json
```

Track H `_network_transport.run_main_http` calls
`_resolve_token_sources(args, prog, logger)`. Since
`args.auth_token_env is None` and
`config.auth.tokens` is empty, the function fails-closed at
startup per Track H §10.6:

> `python -m mcp_read_server: --transport http requires
> --auth-token-env or auth.tokens in product config`

Single stderr line; non-zero exit; no traceback. **This is
the correct Track H behaviour.** It is **not** silent
insecure success — it is fail-closed by design. But the
operator now has to debug why `auth.tokens` "vanished" from
their config, since they declared it in the input. The
recovery path — either re-add the section by hand or use
`--auth-token-env <VARNAME>` CLI flag to bypass the config
— is mentioned across Step 5 docs but is operator-visible
friction caused by silent installer data loss.

### 5.3 Why this is silent configuration data loss

- **Silent**: install fast-path returns `ok=True`,
  `mode="executed"`, `config_written=True`; no finding
  surfaces the auth-section drop.
- **Configuration data loss**: operator's declared
  `auth.tokens` strings (raw `${ENV:NAME}` env-substitution
  forms, никогда не resolved env values) are lost from the
  materialized JSON.
- **Not silent insecure success**: at runtime, missing
  tokens produce fail-closed startup, not silent
  acceptance of unauthenticated requests. Track H's
  `--transport http requires ...` startup gate handles
  the bad state cleanly.
- **Breaks declarative round-trip guarantee**: Phase 6 /
  Step 6 service-level fields and Phase 6 / Step 8
  enterprise block both round-trip byte-identical via the
  emit-only-when-divergent pattern. The auth section
  introduced by Track H / Step 4 was not registered in
  `_config_to_dict` at the time per Track H Step 3
  contract §11.5 (which forbade touching `installer.py`
  during Track H Step 4); Track H Step 6 closure
  narrative explicitly logged this as the known gap to
  be fixed by a separate post-Track-H follow-up, namely
  this Track I.

---

## 6. Existing precedent for additive-installer-fix pattern

`_config_to_dict` already extended twice with backward-
compatible additive fixes of the same shape Track I will
need:

### 6.1 Phase 6 / Step 6 — service-level fields

Service-level fields (`restart_policy`, `logs_enabled`,
`log_max_bytes`) added in `_parse_service_spec` of `loader.py`
and projected by per-service block of `_config_to_dict`
(installer.py l.265-273) using:

```python
if spec.restart_policy != "never":
    svc["restart_policy"] = spec.restart_policy
if spec.logs_enabled is not True:
    svc["logs_enabled"] = spec.logs_enabled
if spec.log_max_bytes != DEFAULT_LOG_MAX_BYTES:
    svc["log_max_bytes"] = spec.log_max_bytes
```

Per Step 6 docstring comment (installer.py l.265-267): «Emit
each one only when it deviates from the dataclass default so
Step 1–5 configs round-trip byte-identical.»

### 6.2 Phase 6 / Step 8 — enterprise block

Top-level `enterprise` section added in `_parse_enterprise`
of `loader.py` and projected by `_config_to_dict` (installer.py
l.295-315) using:

```python
enterprise_block: dict[str, Any] = {}
e = config.enterprise
if e.deployment_tier is not None:
    enterprise_block["deployment_tier"] = e.deployment_tier
if e.instance_id is not None:
    enterprise_block["instance_id"] = e.instance_id
if e.config_owner is not None:
    enterprise_block["config_owner"] = e.config_owner
if e.change_control_required:
    enterprise_block["change_control_required"] = True
if e.require_operator_identity:
    enterprise_block["require_operator_identity"] = True
if e.runbook_reference is not None:
    enterprise_block["runbook_reference"] = e.runbook_reference
if enterprise_block:
    out["enterprise"] = enterprise_block
```

Per Step 8 docstring comment (installer.py l.295-299):
«Emit only the fields that diverge from the empty default
so Step 1–7 configs without an enterprise block remain
byte-identical (no implicit `"enterprise": {...defaults...}`
injection).»

### 6.3 Pattern shape для Track I

`auth` is the same class of additive top-level optional
section как `enterprise`. The pattern Track I Step 4 will
apply (final shape — Step 3 contract):

```python
# After the existing enterprise_block emit logic at l.314:
auth_block: dict[str, Any] = {}
if config.auth.tokens:
    auth_block["tokens"] = list(config.auth.tokens)
if auth_block:
    out["auth"] = auth_block
```

This is byte-symmetric to the existing `enterprise_block`
shape. Diff size estimated at ~6 LOC additive emit branch +
small comment block (~10-15 LOC total). No new helpers,
no schema changes, no `pyproject.toml` changes, no API
surface widening.

---

## 7. CLASS 1 / 2 / 3 / 4 breakdown

### 7.1 CLASS 1 — already round-trip-safe

Sections that already round-trip byte-identical через
existing `_config_to_dict` logic; **NOT** Track I targets:

1. `product_name` (mandatory unconditional, l.277).
2. `profile_name` (mandatory unconditional, l.278).
3. `default_environment` (mandatory unconditional, l.279).
4. `project.environments[*]` (mandatory unconditional dict
   iteration; per-environment optional fields use
   `if env.<field> is not None: emit` pattern at l.247-254).
5. `servers` (mandatory unconditional 3 booleans, l.281-285).
6. `bootstrap` (mandatory unconditional 4 fields,
   l.286-291).
7. `runtime.services[*]` (mandatory unconditional dict
   iteration + per-service mix of unconditional core and
   emit-only-when-divergent Phase 6 / Step 6 fields,
   l.257-274).
8. `enterprise` block (Phase 6 / Step 8 emit-only-when-
   divergent local-block-with-conditional-attach pattern,
   l.295-315).

### 7.2 CLASS 2 — partially preserved / conditionally emitted

**Empty.** No section currently lives in this class. The
patterns observed (mandatory unconditional and emit-only-
when-divergent) are fully consistent: each section either
always emits its core, or never emits an empty default
block. There is no third "halfway" state.

### 7.3 CLASS 3 — currently dropped on round-trip

1. **`auth` (Track H / Step 4)**. `ProductConfig.auth:
   ProductAuthSettings` exists on the dataclass and is
   populated by loader, but `_config_to_dict` has no
   corresponding emit branch. Source of all Track I
   motivation. **Step 4 fix target.**

This is the **only** section in this class. The `auth` gap
is precisely scoped: a single missing emit branch in a
single file, of identical shape to existing `enterprise_block`
logic.

### 7.4 CLASS 4 — explicitly out-of-scope for Track I

Sections that Track I **MUST NOT** add or modify
(carry-over from Track I plan §5):

- **Resolved env values for `auth.tokens`.** Installer
  must round-trip raw `${ENV:NAME}` strings; resolution
  remains `_network_transport._resolve_env_token` boundary
  at server startup.
- **Cleartext token literals.** Already rejected at
  config-load by `_parse_auth`; installer must not become
  a back-door path that emits cleartext.
- **New top-level sections beyond `auth`.** No `transport`,
  `tls`, `vault`, `secrets`, `rbac`, `multi-tenant`, or
  similar sections. Track I scope is exactly one section.
- **Per-server auth differentiation.** Single-tier auth
  (Track H §8.5: «valid token grants access to the full
  registry»); installer must not introduce per-server
  token mappings.
- **New helper modules in `apps/platform/src/onec_platform/`.**
  Default Q1 = `installer.py` only.
- **Changes to `_install_runner.py` / `install.ps1` /
  `bootstrap_paths.ps1`.** Track B / C territory; no
  reporting hook needed for the auth section status (the
  existing `bootstrap_post` re-load already exercises
  whatever path is materialized).
- **Changes to `models.py` / `loader.py`.** Track H Step 4
  surfaces preserved byte-identical.
- **Changes to `_network_transport.py`.** Track H Step 4
  surface preserved byte-identical.
- **Changes to `[project.scripts]` / `[project.dependencies]`
  / wheel build.** Track C honest constraints carried
  through unchanged.
- **New MCP tools.** Registry invariant `read=15 / write=25
  / intelligence=16` carried through.
- **1cv8 work.** Track I works at install/materialization
  layer; 1cv8 binary surface не задействуется.

---

## 8. Q1 resolution — implementation surface for future Step 4

**Q1 answer (Step 2 final, descriptive evidence):
`apps/platform/src/onec_platform/installer.py` only.**

Reasoning grounded in evidence:

1. **Phase 6 / Step 6 precedent** added service-level
   fields entirely inside `_config_to_dict` (installer.py
   l.265-273) without modification of `_install_runner.py`,
   `install.ps1`, or any other file. Round-trip works
   correctly because post-write `bootstrap_product_from_json_file`
   re-load exercises whatever the projected JSON contains.
2. **Phase 6 / Step 8 precedent** added top-level
   `enterprise` block entirely inside `_config_to_dict`
   (installer.py l.295-315) using the local-block-with-
   conditional-attach pattern. Same single-file scope; same
   absence of helper-module introduction.
3. **`_install_runner.py` is already result-shape-agnostic**
   (l.57-78): it iterates over `result.confirmed_findings`,
   `result.presumed_findings`, `result.recommended_actions`
   without inspecting config shape. Adding a separate
   "auth section preserved" finding in the result would
   be additional reporting surface that **does not
   contribute to the actual round-trip integrity**; the
   round-trip integrity is delivered entirely by the
   `_config_to_dict` extension.
4. **Bootstrap layer is already auth-aware** through loader
   (`_parse_auth` validates the round-tripped JSON on
   post-write `bootstrap_post` step). No additional
   bootstrap-layer logic needed; missing auth section in
   input still loads (default empty) — that's the correct
   loader contract for backward compat.
5. **`scripts/release/install.ps1` is shape-agnostic
   PowerShell wrapper.** Touches no Python config logic;
   nothing to change.

**Alternative considered + rejected:** `installer.py +
_install_runner.py` (with a new "auth section round-tripped"
reporting finding). Rejected because: (a) reporting is
informational only; (b) post-write `bootstrap_product_from_json_file`
already validates the materialized JSON, including the
`auth` section through `_parse_auth`; (c) the install
fast-path mode contract (`preview` / `executed` /
`rejected`) does not need a per-section reporting
expansion; (d) adds scope without shipping value.

**Final**: Q1 = **installer.py only**.

---

## 9. Q2 resolution — exact preservation target

**Q2 answer (Step 2 final, descriptive evidence):**

Step 4 implementation MUST preserve the following through
`_config_to_dict` round-trip:

1. **`auth` section presence** when `config.auth.tokens`
   is non-empty. By symmetry with `enterprise_block`
   pattern (l.314: `if enterprise_block: out["enterprise"] =
   enterprise_block`), the section MUST be emitted as a
   top-level dict with a `tokens` key only when there is
   non-empty content to emit.

2. **`tokens` list shape** as a JSON array of strings.
   `ProductAuthSettings.tokens: list[str]` translates to a
   JSON array; each element is a string (`${ENV:NAME}`
   form). Any other JSON shape (object map, scalar, null)
   would violate `_parse_auth` regex enforcement on the
   reload side.

3. **Token entry order preservation.** `_parse_auth`
   constructs `tokens` as an ordered list (l.482:
   `for index, entry in enumerate(tokens_raw): ...
   tokens.append(entry)`). The materialized JSON array
   order MUST match the source list order so the reloaded
   `ProductConfig.auth.tokens` is element-wise equal.
   This matters for operator-deterministic behaviour
   though the runtime auth iteration is order-independent
   (`_resolve_token_sources` short-circuits on first
   `hmac.compare_digest` match per Track H §8.5).

4. **Raw `${ENV:NAME}` string form preservation as
   configuration data.** Each token entry is round-tripped
   character-by-character byte-identical to the source
   string after `json.dumps` / `json.loads`. **Installer
   MUST NOT resolve `os.environ` values during projection**
   — resolution remains `_network_transport._resolve_env_token`
   territory at server startup. This is critical because
   resolved values would be bare cleartext bearer tokens,
   which `_parse_auth` (loader.py l.486-490) rejects fail-
   closed at next reload, AND would create a credential
   leak vector through the materialized JSON file on disk.

5. **Empty/default behaviour: section MUST NOT be emitted
   when `config.auth.tokens == []`.** By symmetry with the
   `enterprise_block` pattern: `auth_block` accumulator
   stays empty; `if auth_block:` gate prevents
   `out["auth"] = {}` injection. This preserves byte-
   identical round-trip for pre-Track-H configs (which
   have no `auth` key in source JSON and load to default
   `ProductAuthSettings(tokens=[])`).

These five rules anchor in observed `_config_to_dict`
evidence; they do not introduce new design. The final
prescriptive normative wording (MUST / MUST NOT) is Step 3
contract territory.

### 9.1 What Q2 explicitly does NOT add to the preservation
target

- No preservation of comments / formatting / whitespace
  in the input JSON file. JSON is the source of truth
  for structure; `json.dumps` decides serialisation
  details. Same constraint already applies to existing
  sections.
- No preservation of key ordering inside the `auth`
  block beyond what `json.dumps(..., sort_keys=False)`
  default semantics provide. Track I plan §5 does not
  promise this; it would be scope creep.
- No round-trip of resolved env values. Forbidden per
  Q3 (§10) and Track H §8.7 redaction discipline; see §10.

---

## 10. Q3 resolution — explicit forbidden behaviour for future
fix

**Q3 answer (Step 2 final, descriptive evidence):**

Step 4 implementation MUST NOT do any of:

1. **Resolve `os.environ` values during install/materialization.**
   `${ENV:NAME}` strings are configuration data, not secrets
   awaiting resolution at this layer. The existing
   resolution boundary lives in
   `packages/mcp-common/src/mcp_common/_network_transport.py`
   `_resolve_env_token` (Track H Step 4), called at
   **server startup**, not at install time. Anchoring
   evidence: Track H §6.2 contract ("`Resolution remains
   `_network_transport._resolve_env_token` boundary at
   server startup`"); Track H §8.7 redaction discipline
   ("Token value MUST NOT appear anywhere in stderr logs
   / structured logs / response bodies / error messages /
   audit `details`"). Writing resolved values into the
   materialized JSON file would create a persistent disk-
   resident bearer-token leak.

2. **Write cleartext tokens (literal non-`${ENV:NAME}`
   strings) into materialized JSON.** This cannot happen
   accidentally because the input was already validated by
   loader's `_parse_auth` (loader.py l.486-490) which
   rejects literal cleartext fail-closed at config-load
   time. Step 4 round-trips already-validated strings; it
   does not re-introduce a cleartext acceptance path.
   Anchoring evidence: loader.py l.486-490 regex check;
   Track H §3.4 ("each entry MUST match the env-substitution
   form `${ENV:NAME}`").

3. **Change Track H auth model semantics.** No changes to
   `Authorization` header parsing, case-insensitive scheme
   handling (Track H §8.2), `hmac.compare_digest` validation
   (Track H §8.5), failure-equivalence rule (Track H §8.4),
   or fail-closed startup gate (Track H §10.6). Anchoring
   evidence: Track H Step 3 contract sections 8 and 10.

4. **Introduce secret storage.** No vault / KMS / OS
   keychain integration / encrypted-at-rest secrets file
   format. Operator-managed `${ENV:NAME}` path remains the
   only documented secret discipline. Anchoring evidence:
   `SECURITY.md` "Honest constraints" l.36-39 ("The
   platform does **not** ship a secrets manager / vault /
   KMS / OS keychain integration / encrypted-at-rest
   secrets file format. Operators who need any of those
   pull values into env vars from their own secrets
   infrastructure before invoking the platform.").

5. **Broad packaging rewrite.** No new wheel build / PyPI
   publication / `.msi` / `.deb` / GUI installer / signed
   distribution. Anchoring evidence: `pyproject.toml`
   `[tool.hatch.build.targets.wheel] packages = []`
   comment block (l.34-44) — Track C Step 3 honest
   constraint carried through.

6. **`[project.scripts]` changes.** Existing 3 console
   entries (`mcp-read-server`, `mcp-write-server`,
   `mcp-intelligence-server`) preserved byte-identical.
   Track I introduces no new console entry.

7. **Touching `_install_runner.py` / `install.ps1` /
   `bootstrap_paths.ps1`.** Per Q1 final resolution:
   `installer.py` only. The wrappers are config-shape-
   agnostic; touching them adds no round-trip integrity
   value.

8. **Touching `models.py` / `loader.py`.** Track H Step 4
   surfaces preserved byte-identical (carry-over §6
   guardrail #3).

9. **Touching `_network_transport.py` or `_stdio_transport.py`.**
   Track G + Track H surfaces preserved byte-identical
   (carry-over §6 guardrail #3 / #4).

10. **Touching three `__main__.py` files.** Existing
    `main()` boundaries byte-identical.

11. **Adding installer-time auth side-effects** (e.g.,
    pinging an HTTP endpoint with the resolved token to
    "verify auth works", or writing a test request log).
    Install fast-path is fail-closed and never starts MCP
    servers; that boundary is preserved.

These eleven rules anchor in Track H contract + observed
`_config_to_dict` evidence. The final prescriptive
normative wording is Step 3 contract territory.

---

## 11. Step 3 handoff note

Step 3 (auth round-trip preservation contract, docs-only)
обязан formalize следующий список normative items на основе
этого Step 2 audit, чтобы Step 4 implementation не
импровизировал:

1. **Exact emit branch placement** — после existing
   `enterprise_block` emit logic at installer.py l.314
   (per Q1 / §6.3); no other location.
2. **Exact emit branch shape** — local accumulator
   `auth_block: dict[str, Any] = {}`; conditional append
   for `tokens` only when `config.auth.tokens` is non-
   empty; conditional attach `out["auth"] = auth_block`
   only when `auth_block` is non-empty (per Q2 / §9 / §6.3).
3. **Exact list copying discipline** — `list(config.auth.tokens)`
   to avoid aliasing the dataclass field's underlying list
   (consistent with existing `list(env.onec_binary_probe_args)`
   pattern at l.250).
4. **Exact backward-compat verification protocol** —
   pre-Track-H sample config (no `auth` section in input
   JSON) must round-trip byte-identical (no implicit
   `"auth": {}` injection); pre-Track-I config with
   non-empty `auth.tokens` must round-trip with element-
   wise equal `tokens` list after reload.
5. **Exact forbidden side-effects** — no `os.environ.get`
   calls anywhere in `_config_to_dict`; no string
   transformation of `${ENV:NAME}` entries; no logging
   of token values during projection.
6. **Exact verification artifact shape** — sample config
   round-trip via inline Python smoke (similar to Track H
   Step 4 verification harness pattern); no permanent
   test file commit; harness deleted before Step 4
   commit.
7. **Exact Step 4 allowed file surface** — `installer.py`
   only; ~10-15 LOC additive diff; no other file in
   `apps/platform/src/onec_platform/` or elsewhere.
8. **Exact Step 4 forbidden file surface** — exhaustive
   list (per §7.4 + §10); models.py / loader.py /
   _network_transport.py / _stdio_transport.py / three
   __main__.py / mcp_common/__init__.py / scripts/* /
   pyproject.toml / examples/* / README / SECURITY /
   release-handoff / apps/platform/README / CHANGELOG /
   PROJECT-STATUS / Track I plan / step-map / contract /
   audit (frozen anchors) / Track A-H docs / .github /
   LICENSE.
9. **Exact verification protocol для Step 4** — required
   positive checks (round-trip preservation through
   `_config_to_dict`; pre-Track-H sample config
   byte-identical; verify-release.ps1 GREEN; selfcheck
   registries `15/25/16; status=ok`); required negative
   checks (no 1cv8.exe; no real credentials in commit /
   diff; no resolved env values in materialized JSON;
   no `[project.dependencies]` change; no scope creep
   markers).
10. **Exact backward-compatibility statement** — Track H
    Step 4 verification artifact (51/51 PASS) MUST remain
    GREEN through Track I (no regression on transport
    surfaces; auth surfaces preserved byte-identical).

---

## 12. Honest summary

После Step 2 (этот audit ship'нут отдельным commit'ом):

**Что доказано read-only inspection'ом:**

- Установлен exact path install fast-path round-trip:
  `install.ps1` → `_install_runner.py` →
  `run_install_fast_path_from_json_file` → `_config_to_dict`
  (called twice for pre-write bootstrap and template
  preview) → atomic write → `bootstrap_product_from_json_file`
  post-write reload.
- Установлены exact 8 sections, которые `_config_to_dict`
  уже round-trips correctly under one of two patterns
  (mandatory unconditional or emit-only-when-divergent),
  с file/line anchors.
- Установлено, что **`auth` is the only section in CLASS 3
  (currently dropped on round-trip)**; gap precisely
  scoped to a single missing emit branch.
- Установлены два proven precedents for additive-installer-
  fix pattern (Phase 6 / Step 6 service-level fields;
  Phase 6 / Step 8 enterprise block) с экземплярами кода —
  Track I Step 4 будет следовать тому же patternу.
- Установлено, что gap — silent **configuration data
  loss**, не silent insecure success: Track H startup gate
  fails-closed clean при missing token source.
- Установлено, что Track H auth surfaces (5 anchors:
  `ProductAuthSettings`, `ProductConfig.auth`,
  `_AUTH_ENV_TOKEN_RE`, `_parse_auth`,
  `_resolve_token_sources`) полностью готовы и должны
  остаться byte-identical через Track I.

**Что зафиксировано как Step 2 final answer (descriptive,
финал normative — Step 3 contract):**

- Q1 = `installer.py` only (verified by Phase 6 / Step 9
  and Phase 6 / Step 8 precedents).
- Q2 = preserve auth section presence + tokens list shape +
  order + raw `${ENV:NAME}` form preservation as
  configuration data + empty/default no-implicit-injection
  (anchored in 5 file/line refs).
- Q3 = forbidden = no env-resolution at install time / no
  cleartext token writing / no Track H auth model changes /
  no secret storage introduction / no broad packaging
  rewrite / no `[project.scripts]` change / no
  `_install_runner.py` change / no `models.py` /
  `loader.py` / `_network_transport.py` /
  `_stdio_transport.py` / three `__main__.py` change / no
  installer-time auth side-effects (anchored in 11 sub-
  rules).

**Что только planned, не доказано (deferred to Step 3 /
Step 4):**

- Точный wording emit branch (комментарии, comment style
  matching existing Phase 6 / Step 8 enterprise block
  comment shape) — Step 3 contract.
- Точный verification harness shape — Step 3 contract /
  Step 4 implementation.
- Точная operator-facing wording после Step 4 fix —
  Step 5 territory.
- Точное Q6 closure decision (version bump 0.5.0 → 0.6.0
  default, alternative PATCH 0.5.0 → 0.5.1) — Step 6
  closure narrative.

**Чего всё ещё нет в repo на момент Step 2 closure:**

- Никакого `_config_to_dict` extension — `auth` section
  по-прежнему dropped on round-trip.
- Никакого `installer.py` modification.
- Никакого нового `auth_block` emit logic.
- Никаких изменений в `pyproject.toml` (`version=0.5.0`
  preserved).
- Никаких изменений в registries (`read=15 / write=25 /
  intelligence=16`).
- Никаких изменений в Track H Step 4 surfaces.
- Никаких изменений в operator-facing docs за пределами
  Track I planning + audit + step-map.

Track I после Step 2 остаётся **planning/audit-only**.
Implementation первый и единственный раз появляется на
Step 4. Step 3 contract фиксирует точные правила, по
которым Step 4 implementation сможет работать без
импровизации.
