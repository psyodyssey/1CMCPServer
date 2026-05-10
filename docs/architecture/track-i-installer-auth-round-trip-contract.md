# Parallel Track I — Installer Auth Round-Trip Contract (Step 3)

> **Companion files:**
> `track-i-installer-auth-round-trip-integrity-plan.md` (Step 1
> plan), `track-i-installer-auth-round-trip-integrity-step-map.md`
> (Step 1 step-map), `track-i-installer-auth-round-trip-baseline-audit.md`
> (Step 2 descriptive baseline audit). Этот документ — Step 3
> deliverable: **prescriptive normative contract** для Step 4
> narrow implementation slice.

> **Status:** Track I / Step 3 deliverable. Documentation-only.
> **Prescriptive normative contract** для Step 4 implementation.
> RFC 2119-style: **MUST** / **MUST NOT** / **SHALL** /
> **SHOULD** / **MAY** имеют точный нормативный смысл. **Этот
> документ не меняет код**; он формулирует правила, которым
> Step 4 implementation обязан следовать.

> **Scope discipline.** Этот документ не открывает новые вопросы
> за пределы Step 1 plan §5 / §6 + Step 2 audit Q1 / Q2 / Q3
> directional resolutions. Он не делает closure narrative по
> Track I целиком (это Step 6 territory), не выравнивает
> operator-facing docs (Step 5 territory) и не ship'ит код
> (Step 4 territory).

---

## 1. Purpose / scope

Этот документ — **нормативный contract** для Track I / Step 4
(narrow implementation slice). Он отвечает на **один** вопрос:

> «По каким exact правилам Step 4 имеет право добавить emit-
> branch для `auth` section в `apps/platform/src/onec_platform/installer.py:_config_to_dict`,
> и какие invariants implementation обязан соблюдать?»

Документ нормирует:

- exact allowed implementation surface (по Step 2 audit Q1
  resolution);
- exact emit-branch placement, shape, and accumulation
  pattern;
- exact preservation semantics для `auth` section через
  install fast-path round-trip;
- exact forbidden side effects;
- exact backward compatibility guarantees;
- exact verification protocol для Step 4;
- exact closure boundary of the Step 4 fix (no scope creep
  into packaging / deployment / secret storage / transport
  redesign).

Документ **не**:

- ship'ит код — это Step 4 territory;
- описывает current state — это Step 2 audit territory
  (`track-i-installer-auth-round-trip-baseline-audit.md`);
- alignment'ит operator-facing docs — это Step 5 territory;
- making closure narrative claims — это Step 6 territory;
- pretend'ит, что installer round-trip уже fixed;
- расширяет out-of-scope items из Step 1 plan §5 (full
  installer ecosystem / secret storage / transport-network
  changes / service-supervisor / new MCP tools / 1cv8 work
  / rollback / AST / multi-version / standalone
  apps/platform / web UI / enterprise identity / remote
  push).

---

## 2. Relationship to Step 1 plan and Step 2 audit

Track I deliberately splits concerns между четырьмя layers:

| Step | Role | Language style | Source of truth для |
|---|---|---|---|
| Step 1 plan + step-map | **direction** | descriptive plan + step formats | track scope, 6-step trajectory, 7 open questions Q1–Q7 |
| Step 2 audit (`track-i-installer-auth-round-trip-baseline-audit.md`) | **descriptive** | observational, current-state | per-installer-section inventory, 4-class breakdown, Q1/Q2/Q3 directional resolutions, file/line evidence |
| **Step 3 contract (this doc)** | **normative** | RFC 2119-style, prescriptive | exact Step 4 implementation rules, allowed surfaces, verification protocol |
| Step 4 | **execution** | code change | actual `_config_to_dict` extension с emit branch для `auth` |
| Step 5 | **alignment** | docs alignment | operator/security docs alignment под фактический post-Step-4 state |
| Step 6 | **closure** | closure narrative + version bump | README + PROJECT-STATUS + CHANGELOG closure pass; Q6 default ДА |

**Step 3 contract MUST NOT** revise Step 2 audit findings
без proven blocker. **Step 3 contract MUST NOT** revise
Step 1 plan scope без proven blocker. **Step 3 contract
MUST NOT** duplicate descriptive content from Step 2 audit;
reader обращается к Step 2 audit для current-state evidence,
к этому contract — для implementation rules.

---

## 3. Current model recap (brief, non-duplicative)

The current install fast-path round-trip path is:
`scripts/release/install.ps1` → `scripts/release/_install_runner.py`
→ `apps/platform/src/onec_platform/installer.py:run_install_fast_path_from_json_file`
→ `installer.py:run_install_fast_path` → `installer.py:_config_to_dict`
(called twice: pre-write bootstrap + template_preview) →
atomic write → `bootstrap_product_from_json_file` (post-
write reload). `_config_to_dict` (l.228-317) currently emits
8 of 9 logical sections of `ProductConfig`; the `auth`
section (`ProductConfig.auth: ProductAuthSettings`, added
by Track H / Step 4) is the only Class-3 gap. Two existing
proven precedents для additive optional-block fix exist:
Phase 6 / Step 6 service-level fields (l.265-273) and
Phase 6 / Step 8 enterprise block (l.295-315), both using
the emit-only-when-divergent pattern. Full evidence,
file/line anchors, and per-section inventory live in Step 2
audit document — see §10–§12 there.

---

## 4. Inherited fixed decisions

Following decisions **MUST** be inherited без re-litigation.
Они resolved в Step 2 audit на основе read-only evidence;
Step 3 contract строится на их фундаменте.

### 4.1 — Q1: implementation surface = `installer.py` only

Step 4 implementation **MUST** be limited to a single file:
`apps/platform/src/onec_platform/installer.py`. Per Step 2
audit §8 (verified by Phase 6 / Step 6 service-level +
Phase 6 / Step 8 enterprise single-file precedents). No
other file in `apps/platform/src/onec_platform/` and no
file outside `apps/platform/` is touched.

### 4.2 — Q2: preservation target = 5 rules

Step 4 implementation **MUST** preserve через
`_config_to_dict` round-trip (per Step 2 audit §9):

1. `auth` section presence when `config.auth.tokens` is
   non-empty;
2. `tokens` list shape as JSON array of strings;
3. token entry order;
4. raw `${ENV:NAME}` form preservation as configuration
   data (NOT resolved env values);
5. empty/default behaviour: section MUST NOT be emitted
   when `config.auth.tokens == []` (no implicit injection).

### 4.3 — Q3: forbidden behaviour = 11 sub-rules

Step 4 implementation **MUST NOT** do any of (per Step 2
audit §10):

1. resolve `os.environ` values during install/materialization;
2. write cleartext token literals;
3. change Track H auth model semantics;
4. introduce secret storage;
5. perform broad packaging rewrite;
6. change `[project.scripts]`;
7. touch `_install_runner.py` / `install.ps1` /
   `bootstrap_paths.ps1`;
8. touch `models.py` / `loader.py`;
9. touch `_network_transport.py` / `_stdio_transport.py`;
10. touch three `__main__.py` files;
11. introduce installer-time auth side-effects.

### 4.4 — Carry-over out-of-scope from Step 1 plan §5

Following items **MUST NOT** be touched в Step 4:

- full installer ecosystem (`.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI publication
  / wheel publication beyond existing `[project.scripts]`);
- secret storage / vault / KMS / OS keychain integration;
- env-var resolution at install time (this is design
  invariant, not gap);
- Track H auth model changes (bearer / case-insensitive
  scheme / constant-time compare / failure-equivalence
  rule preserved byte-identical);
- new transport / network / TLS / mTLS / OAuth / JWT /
  OIDC / SAML / SCIM / RBAC / multi-tenant / sessions /
  rate limiting;
- supervisor daemon / systemd unit / Windows Service
  registration / hot reload / restart watcher;
- web UI / dashboard frontend;
- standalone `apps/platform` entrypoint;
- new MCP tools (registry invariant `read=15 / write=25 /
  intelligence=16`);
- 1cv8.exe execution work;
- rollback / AST / multi-version 1С matrix expansion;
- distributed tracing / observability stack;
- real MCP client integration test as closure gate;
- GitHub remote push.

---

## 5. Auth round-trip preservation contract

This section pins exact normative behaviour Step 4
implementation **MUST** deliver.

### 5.1 — Definition of round-trip integrity for `auth`

Round-trip integrity means: for any `ProductConfig` value
`C` produced by `load_product_config(...)` from a valid
input JSON, the value `C2` produced by re-loading the
output of `json.dumps(_config_to_dict(C))` through
`load_product_config(...)` **MUST** satisfy:

```
C2.auth.tokens == C.auth.tokens
```

(element-wise equal, same order, same string values,
including byte-identical `${ENV:NAME}` strings).

This rule applies for both the non-empty case
(`C.auth.tokens != []`) and the empty case
(`C.auth.tokens == []`).

### 5.2 — Emit-branch presence

`_config_to_dict` **MUST** include a new emit branch for
`auth` after the existing `enterprise_block` emit logic
(currently around `installer.py:l.314`, immediately
preceding `return out`). The branch **MUST** be
syntactically and semantically symmetric to the existing
`enterprise_block` pattern (per Step 2 audit §6.2).

### 5.3 — Emit-branch shape (normative)

Step 4 **MUST** implement the emit branch using the
following accumulation-and-conditional-attach pattern:

1. The branch **MUST** declare a local accumulator
   variable. Recommended name: `auth_block: dict[str, Any]
   = {}`. The exact identifier name **MAY** vary но
   **SHOULD** match the precedent (`auth_block`).
2. The branch **MUST** copy `config.auth.tokens` into the
   accumulator under key `"tokens"` only when
   `config.auth.tokens` is non-empty:

   ```python
   if config.auth.tokens:
       auth_block["tokens"] = list(config.auth.tokens)
   ```

   The `list(...)` wrapping **MUST** be present (rule §5.6).
3. The branch **MUST** attach the accumulator to the
   output dict only when the accumulator itself is
   non-empty:

   ```python
   if auth_block:
       out["auth"] = auth_block
   ```

   This conditional attach is the empty/default backward-
   compat anchor (rule §5.5).

### 5.4 — `tokens` list shape

The emitted `auth.tokens` value **MUST** be a JSON array
(serialised from a Python `list`). It **MUST NOT** be:

- a JSON object / dict (no per-token key/value mapping);
- a JSON scalar (no string flattening of the list);
- a JSON `null` (no nullification of empty lists; instead,
  the `auth` block MUST be omitted entirely per §5.5);
- a generator / iterator type whose JSON serialisation is
  implementation-dependent.

Each element of the array **MUST** be a JSON string. No
nested objects, arrays, numbers, booleans, or `null`
elements are permitted in `auth.tokens`. (This is enforced
on the reload side by `loader.py:_parse_auth` regex check
at l.486-490; Step 4 emit branch **MUST NOT** weaken this
contract by emitting non-string token entries.)

### 5.5 — Empty / default behaviour

When `config.auth.tokens == []` (the default factory
state, including pre-Track-H configs that load without
an `auth` section), `_config_to_dict` **MUST NOT** emit
an `"auth"` key in the output dict. Specifically:

- `out["auth"] = {}` is forbidden;
- `out["auth"] = {"tokens": []}` is forbidden;
- `out["auth"] = None` is forbidden;
- the `"auth"` key MUST be entirely absent in this case.

This rule guarantees byte-identical round-trip for pre-
Track-H configs (which have no `auth` key in their source
JSON and load to default `ProductAuthSettings(tokens=[])`).

### 5.6 — Token order and copying discipline

The emitted JSON array's element order **MUST** match the
in-memory `config.auth.tokens` list element order
(positional, 0-indexed, no reordering, no deduplication,
no sorting). Step 4 **MUST** wrap the in-memory list in
`list(...)` when copying into the accumulator
(`auth_block["tokens"] = list(config.auth.tokens)`); this
prevents accidental aliasing of the dataclass field's
underlying list and matches the precedent at l.250
(`list(env.onec_binary_probe_args)`).

### 5.7 — Raw `${ENV:NAME}` string preservation

Each element of the emitted array **MUST** be the
character-by-character byte-identical copy of the
corresponding element of `config.auth.tokens`. The emit
branch **MUST NOT**:

- call `os.environ.get(...)` or any other env-resolution
  primitive on token values;
- call `str.format(...)`, `str.format_map(...)`, regex
  substitution, or any other string transformation that
  could alter `${ENV:NAME}` syntax;
- truncate, redact, hash, base64-encode, or otherwise
  modify token values;
- replace `${ENV:NAME}` with the resolved env value (this
  would constitute writing cleartext tokens — rule §6.1).

Resolution of `${ENV:NAME}` happens exclusively at server
startup in `packages/mcp-common/src/mcp_common/_network_transport.py:_resolve_env_token`
(Track H §8.7). The installer is a configuration-data
round-trip layer, not a secret-resolution layer.

### 5.8 — Output JSON shape

The output dict produced by `_config_to_dict` **MUST**
remain ordinary JSON-serialisable structure (already true
for the existing 8 sections). Step 4 **MUST NOT**
introduce custom JSON encoders, default factories that
produce non-JSON types, or any structure that
`json.dumps(..., ensure_ascii=False)` cannot serialise
out-of-the-box.

The `auth` block, when emitted, **MUST** sit at the top
level of the output dict (sibling to `product_name`,
`profile_name`, `default_environment`, `project`,
`servers`, `bootstrap`, `runtime`, `enterprise`). It
**MUST NOT** be nested inside any other section.

---

## 6. Forbidden behaviour (normative restatement of §4.3)

Step 4 implementation **MUST NOT** do any of the following.
Each rule is testable by inspection of the Step 4 commit
diff and/or by verification harness output.

### 6.1 — No env resolution at install time

The emit branch **MUST NOT** call `os.environ`, `os.getenv`,
`subprocess.*`, or any other primitive that reads or
materialises environment variable values during
`_config_to_dict` execution. Token values are configuration
data, not secrets to be resolved at this layer.

### 6.2 — No cleartext token writing

The emit branch **MUST NOT** introduce a code path that
accepts a literal cleartext token string (a non-`${ENV:NAME}`
string) and writes it to the output dict. Cleartext tokens
are already rejected at config-load time by
`loader.py:_parse_auth` (l.486-490); Step 4 **MUST NOT**
become a back-door path that bypasses that validation.

### 6.3 — No Track H auth model semantics change

Step 4 **MUST NOT** modify any of:

- `Authorization` header parsing in `_network_transport._MCPHandler`;
- case-insensitive scheme handling per Track H §8.2;
- `hmac.compare_digest` token validation per Track H §8.5;
- failure-equivalence rule per Track H §8.4;
- fail-closed startup gate per Track H §10.6;
- redaction discipline per Track H §8.7.

These are all in `packages/mcp-common/src/mcp_common/_network_transport.py`,
which is forbidden surface (§7.2).

### 6.4 — No secret storage introduction

Step 4 **MUST NOT** introduce:

- a new module under `apps/platform/src/onec_platform/`
  for secrets management;
- a vault / KMS / HashiCorp Vault / AWS Secrets Manager /
  Azure Key Vault / OS keychain integration;
- an encrypted-at-rest secrets file format;
- a token cache file on disk;
- any disk persistence of resolved env values.

Operator-managed `${ENV:NAME}` path remains the only
documented secret discipline (carry-over from Track D Step
3 + Track H §8.5).

### 6.5 — No broad packaging rewrite

Step 4 **MUST NOT** modify:

- `pyproject.toml` (no `[project.dependencies]` /
  `[project.optional-dependencies]` / `[project.scripts]` /
  `[tool.hatch.build.targets.wheel]` / version field
  changes; version bump = Step 6 territory);
- `[project.scripts]` block specifically (existing 3
  console entries `mcp-read-server` / `mcp-write-server`
  / `mcp-intelligence-server` byte-identical);
- wheel-build configuration (Track C Step 3 honest
  constraint preserved).

### 6.6 — No installer ecosystem fantasy

Step 4 **MUST NOT** introduce:

- `.msi` / `.deb` / signed binary distribution / GUI
  installer / wizard / PyPI publication;
- automatic prerequisite installation;
- post-install service registration;
- post-install shortcut creation;
- a separate "installer" CLI subcommand or executable;
- any feature that turns `install fast path` from a
  config-materialisation helper into an OS-level
  installation system.

### 6.7 — No touches to forbidden surfaces

Step 4 **MUST NOT** modify any of (exhaustive — see §7
for the complete forbidden file list):

- `scripts/release/*` (including `install.ps1` and
  `_install_runner.py`);
- `scripts/dev/*`;
- `scripts/test/*`;
- `apps/platform/src/onec_platform/{bootstrap,doctor,
  dashboard,enterprise,loader,models,process_control,
  realstand,recovery,runtime,runtime_logs,state,
  templates,workflow}.py`;
- `apps/platform/src/onec_platform/__init__.py`;
- `apps/mcp-{read,write,intelligence}-server/src/**`;
- `packages/mcp-common/src/mcp_common/**`;
- `packages/onec-{audit,config,health,policy-engine,
  process-runner,troubleshooting}/src/**`;
- `pyproject.toml`;
- `README.md`, `PROJECT-STATUS.md`, `CHANGELOG.md`,
  `SECURITY.md`, `docs/release-handoff.md`,
  `apps/platform/README.md`, `docs/operator-manual.md`,
  `docs/administrator-manual.md`,
  `docs/developer-manual.md`, `docs/runbooks/*`;
- Track A / B / C / D / E / F / G / H architecture docs;
- Track I planning / step-map / audit / contract docs
  (frozen Step 1 / 2 / 3 anchors);
- `.github/`, `.editorconfig`, `.python-version`,
  `.gitignore`, `LICENSE`;
- `examples/*`.

### 6.8 — No installer-time auth side-effects

Step 4 **MUST NOT** introduce any side effect during
`_config_to_dict` execution beyond projecting the
`ProductConfig` into a dict. Specifically forbidden:

- HTTP probes against any endpoint (including the new
  Track H `/mcp` endpoint);
- subprocess spawning;
- file I/O beyond what `run_install_fast_path` already
  performs (atomic JSON write happens AFTER
  `_config_to_dict` returns);
- logging of token values (no token value, length,
  prefix, suffix, hash, or fingerprint emitted to
  stderr / structured logs / audit details);
- mutation of the input `ProductConfig` instance (the
  `list(config.auth.tokens)` wrap per §5.6 is the
  protective pattern).

### 6.9 — No premature closure / status changes

Step 4 commit **MUST NOT**:

- claim Track I is closed;
- bump `pyproject.toml` version (Q6 = Step 6 territory);
- update `README.md` Active parallel track section;
- update `PROJECT-STATUS.md` header;
- update `CHANGELOG.md`;
- update `SECURITY.md` known-installer-gap statement
  (Step 5 territory);
- update `docs/release-handoff.md` (Step 5 territory);
- update `apps/platform/README.md` (Step 5 territory).

---

## 7. Exact implementation surface for Step 4

### 7.1 — Allowed file (singular)

Step 4 production-code touches **MUST** be limited to
exactly **one** file:

```
apps/platform/src/onec_platform/installer.py
```

The expected diff size is approximately **6–15 LOC**
additive emit branch (per Step 2 audit §6.3 pattern-shape-
for-Track-I derivation), plus optional small comment block
explaining the Track I provenance (analogous to the
existing Phase 6 / Step 6 + Phase 6 / Step 8 comment
blocks at l.265-267 and l.295-299).

Step 4 **MUST NOT** rewrite or relocate any existing logic
in `installer.py` outside the new emit branch. The branch
**MUST** be additive in nature: existing emit branches for
8 sections (`product_name`, `profile_name`,
`default_environment`, `project.environments`, `servers`,
`bootstrap`, `runtime`, `enterprise`) **MUST** remain
byte-identical.

### 7.2 — Forbidden files (exhaustive)

See §6.7 above. The list is exhaustive: anything not in
§7.1 is forbidden surface for Step 4.

### 7.3 — Allowed import additions

Step 4 **MAY** add to `installer.py` only the imports
strictly needed by the new emit branch. In the expected
PATH A shape (per §5.3), no new imports are required:
`config.auth.tokens` is reached through the existing
`config: ProductConfig` parameter; `list(...)` and `dict
literal` are builtins; `Any` is already imported (l.33:
`from typing import Any`). Step 4 **SHOULD NOT** add
imports unless absolutely necessary; if it does, the
commit body **MUST** explicitly justify each new import.

### 7.4 — Forbidden import additions

Step 4 **MUST NOT** add imports of:

- `os` (would enable env resolution — rule §6.1);
- `subprocess` (no install-time side-effects — rule §6.8);
- `urllib`, `http.client`, `requests`, `httpx` (no probes
  — rule §6.8);
- `hashlib`, `hmac` (no hashing/fingerprinting of token
  values — rule §6.8);
- third-party packages of any kind (Track C wheel-build
  empty constraint + Step 3 §3 carry-over).

---

## 8. Backward compatibility statement

Step 4 implementation **MUST** preserve the following
invariants:

### 8.1 — Pre-Track-H configs

Configs without an `auth` section in their source JSON
**MUST** continue to:

- load successfully via `load_product_config_from_json_file`
  (already true; `_parse_auth(None)` returns default empty
  `ProductAuthSettings()`);
- materialize via install fast-path executed mode without
  acquiring an implicit `"auth": {}` block (rule §5.5);
- be runnable with `--transport stdio` exactly as before
  (Track G surface byte-identical).

### 8.2 — Stdio-only configs

Configs intended for `--transport stdio` use only **MUST**
continue to function regardless of whether they contain
an `auth` section. Track G stdio surface and
`_stdio_transport.py` byte-identical.

### 8.3 — Track H auth surfaces

The following surfaces **MUST** remain byte-identical
through Track I:

- `apps/platform/src/onec_platform/models.py` —
  `ProductAuthSettings` dataclass shape;
  `ProductConfig.auth` field; all other `ProductConfig`
  fields;
- `apps/platform/src/onec_platform/loader.py` —
  `_AUTH_ENV_TOKEN_RE` regex; `_parse_auth` validator;
  wiring at `load_product_config` line ~142;
- `packages/mcp-common/src/mcp_common/_network_transport.py`
  — `_resolve_token_sources`, `_resolve_env_token`,
  `_resolve_config_tokens` boundaries; HTTP handler;
  argparser; `run_main_http` entry;
- `packages/mcp-common/src/mcp_common/_stdio_transport.py`
  — entire module byte-identical;
- `apps/mcp-{read,write,intelligence}-server/src/.../`__main__.py``
  — all three entrypoints byte-identical;
- `packages/mcp-common/src/mcp_common/__init__.py` `__all__`
  list (10 names byte-identical).

### 8.4 — Registries and tool surfaces

Registry counts **MUST** remain `read=15 / write=25 /
intelligence=16`. Server-side `REGISTERED_TOOLS` dicts in
the three MCP server packages **MUST** remain byte-
identical.

### 8.5 — Track H verification artifact

Track H Step 4 51/51 verification artifact (per-server
`--help`, HTTP startup negative tests, byte-identical 401
fail-closed, case-insensitive scheme, GET 405, non-`/mcp`
404, malformed JSON 400, wrong CT 415, unknown method
200+`-32601`, multiple Authorization 400+`-32600`,
notification 204, `tools/call ping` 200, cross-transport
parity) **MUST** remain GREEN through Track I (no
regression).

### 8.6 — Existing install fast-path semantics

The mode contract (`preview` / `executed` / `rejected`)
**MUST** remain byte-identical. The `InstallFastPathResult`
dataclass shape **MUST** remain byte-identical. Operator-
visible behaviour (refusal to overwrite existing target,
atomic write through `*.tmp + os.replace`, post-write
`bootstrap_product_from_json_file` round-trip
confirmation) **MUST** remain byte-identical.

---

## 9. Verification contract for Step 4

Step 4 commit **MUST** include a verification artifact
demonstrating each of the following classes. The harness
**MUST** be a one-off ephemeral file (e.g.
`.tmp_track_i_smoke.py`) deleted before the Step 4 commit;
no permanent test file is expected to be added (carry-
over from Track H precedent).

### 9.1 — Required positive verification

1. **Round-trip preservation (non-empty `auth.tokens`).**
   Sample `ProductConfig` value `C` constructed with
   `auth = ProductAuthSettings(tokens=["${ENV:MCP_TOKEN_A}",
   "${ENV:MCP_TOKEN_B}"])` (multi-token, deterministic
   order). After `json.dumps(_config_to_dict(C))` →
   `json.loads(...)` → `load_product_config(...)` round-
   trip, the resulting `C2.auth.tokens` **MUST** equal
   `["${ENV:MCP_TOKEN_A}", "${ENV:MCP_TOKEN_B}"]` element-
   wise.

2. **Round-trip preservation (single-token `auth.tokens`).**
   Same shape, single-element list `["${ENV:MCP_TOKEN}"]`.

3. **Empty/default `auth` not injected.** Sample
   `ProductConfig` value `C` constructed without an `auth`
   section in source JSON (`auth` field defaults to
   `ProductAuthSettings(tokens=[])`). After
   `_config_to_dict(C)` projection, the resulting dict
   **MUST NOT** contain an `"auth"` key. If present, Step
   4 verification **MUST** fail closed.

4. **Pre-Track-H config byte-identical round-trip.** A
   sample input JSON config without `auth` section (modelled
   on a real pre-Track-H product config shape) **MUST**
   round-trip through `load → _config_to_dict → json.dumps`
   such that the resulting JSON is byte-identical to the
   source JSON for shared keys (modulo whitespace /
   formatting differences from `json.dumps`).

5. **Token order preservation.** For multi-token
   `ProductAuthSettings(tokens=[t1, t2, t3])` with distinct
   ordered values, the materialised JSON array order
   **MUST** match the source list order positionally.

6. **Raw `${ENV:NAME}` form preservation.** For an input
   token value `"${ENV:OPERATOR_TOKEN_PROD}"`, the output
   string **MUST** equal `"${ENV:OPERATOR_TOKEN_PROD}"`
   character-by-character. No env resolution. The
   verification harness **MUST NOT** populate
   `os.environ["OPERATOR_TOKEN_PROD"]` to demonstrate the
   round-trip; if it does (for unrelated reasons), the
   output string **MUST** still equal the source `${ENV:...}`
   form.

### 9.2 — Required negative verification

7. **Track H 51/51 smoke list re-runs without regression.**
   Per-server `--help` exits 0; HTTP startup negative tests
   (missing `--bind`, missing token source, unresolved env);
   per-server HTTP positive smoke (`tools/list` valid Bearer
   → 200 with correct tool count 15/25/16); byte-identical
   401 fail-closed; case-insensitive scheme through 4
   variants × 3 servers; GET 405 + `Allow: POST`; non-`/mcp`
   404; malformed JSON 400 + `-32700`; wrong Content-Type
   415 + `-32600`; unknown JSON-RPC method 200 + `-32601`;
   multiple Authorization headers 400 + `-32600`;
   notification 204 + empty body; `tools/call ping` 200 +
   `isError:false`; cross-transport parity (sorted stdio
   names == sorted http names).

   The Step 4 verification harness **SHOULD** drive at
   least the install-fast-path round-trip checks (§9.1
   items 1-6) directly. Track H 51/51 may be re-run via
   the same kind of ephemeral harness Track H Step 4 used,
   or implicitly via `verify-release.ps1` selfcheck for
   import / registry health.

8. **`verify-release.ps1 -AllowDirtyTree` GREEN on 8
   checks** before commit; `verify-release.ps1` GREEN on
   clean tree post-commit.

9. **Selfcheck registries `read=15 / write=25 /
   intelligence=16; status=ok`; `imports_ok=true`.**

10. **No 1cv8.exe runs at any point during Step 4.**

11. **No real credentials in commit / diff.** All token
    references in commit body and verification harness
    **MUST** use abstract `${ENV:NAME}` notation or
    operator-supplied test values that are deleted before
    commit (e.g. ephemeral `"smoke-test-bearer-token-not-
    real-secret"` strings inside the deleted harness). The
    commit **MUST NOT** contain any string that could be
    interpreted as a real bearer token.

12. **No unrelated file touches.** `git diff --stat` for
    the Step 4 commit **MUST** show exactly one file
    changed: `apps/platform/src/onec_platform/installer.py`.
    Any deviation **MUST** cause Step 4 to stop and
    surface the issue rather than silently widening
    scope.

### 9.3 — What does NOT count as sufficient verification

The following **MUST NOT** be accepted as Step 4
verification:

- "the diff is small so it's fine" without round-trip
  artifact;
- post-write `bootstrap_product_from_json_file` returning
  `ok=True` (already returns `ok=True` even without the
  fix, because empty auth is a valid load — see Step 2
  audit §3.3 for evidence);
- a single-token round-trip without empty/default
  no-injection check (§9.1 item 3 is required);
- claims of "Track H smoke still passes" without explicit
  re-run evidence in the commit body or verification
  harness output snippet.

### 9.4 — No real MCP client integration test

Step 4 verification **MUST NOT** require a real MCP client
integration test (Claude Desktop, MCP CLI launching the
server) as a closure gate. Carry-over from Track G §13.4
+ Track H §16.4. Recommended но не blocker.

---

## 10. Honest non-goals

Track I after closure **does NOT** mean any of:

- **Packaging solved.** No `.msi` / `.deb` / signed
  distribution / GUI installer / wizard / PyPI publication
  / wheel publication beyond existing `[project.scripts]`.
  Track C wheel-build empty constraint preserved.
- **Deployment solved.** Operator's reverse proxy / TLS
  termination / supervisor / OS service registration /
  hot reload / restart watcher remain operator's
  responsibility.
- **Enterprise-ready installer.** No SSO / OIDC / RBAC /
  multi-tenant / federated identity integration.
- **Secret-management platform.** No vault / KMS / OS
  keychain / encrypted-at-rest secrets file format.
  Operator-managed `${ENV:NAME}` path remains the only
  documented secret discipline.
- **Auth redesign.** Track H auth model (bearer / case-
  insensitive scheme / constant-time compare / failure-
  equivalence rule / fail-closed startup) preserved
  byte-identical.
- **Transport redesign.** Track G stdio + Track H HTTP
  baselines preserved byte-identical. No WebSocket / SSE
  / TCP / Unix-socket / named-pipe transports added.
- **Service supervision.** No systemd / Windows Service
  / `launchd` / hot reload / restart watcher.
- **Web UI / dashboard.** None.
- **Standalone `apps/platform` entrypoint.** Carry-over
  out-of-scope from Tracks G / H.
- **New MCP tools.** Registry invariant carried through.
- **1cv8 work.** Track A/E territories.
- **Rollback / AST / multi-version expansion.**
  Track A / E / F territories.
- **Distributed tracing / observability stack.**
- **Real MCP client integration test as closure gate.**
  Recommended only.
- **GitHub remote push.** Operator action.

Track I closure ships exactly one defect-class fix:
**install fast-path round-trip preservation for the
`auth` section symmetric to existing Phase 6 / Step 8
enterprise-block emit-only-when-divergent pattern**.
Nothing more, nothing less.

---

## 11. Step 4 handoff note

После Step 3 closure (этот contract document shipped),
Step 4 имеет:

1. **Exact 1 file path** для production code change
   (`apps/platform/src/onec_platform/installer.py` per
   §4.1 / §7.1).
2. **Exact emit-branch placement** (after existing
   `enterprise_block` emit logic at l.314, immediately
   preceding `return out`; per §5.2).
3. **Exact emit-branch shape** (accumulator-and-conditional-
   attach pattern symmetric to `enterprise_block`; per
   §5.3).
4. **Exact preservation rules** (5 rules per §5.4 / §5.5
   / §5.6 / §5.7 / §5.8).
5. **Exact list copying discipline** (`list(config.auth.tokens)`
   per §5.6).
6. **Exact forbidden behaviour** (11 sub-rules + import
   restrictions per §6 / §7.4).
7. **Exact backward-compatibility invariants** (§8 — six
   classes of preservation requirements).
8. **Exact verification protocol** (§9 — 6 positive checks
   + 6 negative checks + 4 insufficient-verification
   exclusions + no-real-MCP-client-gate carry-over).

Step 4 **MUST NOT**:

- expand scope beyond §7.1 allowed file;
- add imports beyond what the emit branch strictly
  requires (default: zero new imports per §7.3);
- add network / auth / installer-side-effect logic
  (per §6.8);
- modify registries / `mcp_common` public API / audit
  shape / Track H surfaces (per §8);
- touch operator-facing docs (Step 5 territory);
- claim closure (Step 6 territory);
- bump `pyproject.toml` version (Q6 = Step 6 decision);
- run 1cv8.exe (per §9.2);
- commit real credentials (per §9.2);
- ship without the §9.1 + §9.2 verification artifact in
  the commit body.

Step 5 (operator/security docs alignment) и Step 6
(closure) — out of scope этого contract; они оперируют
над фактическим post-Step-4 state.
