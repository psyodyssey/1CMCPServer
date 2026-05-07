# scripts/release

Operator-facing release / install scripts for **1C Agent Platform**.

This directory holds thin wrappers around already-existing
product-layer helpers. The wrappers do **not** introduce a new
install ecosystem — no `.msi`, no `.deb`, no GUI wizard, no signed
distribution — they only make the existing helpers
operator-discoverable.

## install.ps1

Thin PowerShell wrapper around the install fast path helper
`onec_platform.run_install_fast_path_from_json_file` (defined in
`apps/platform/src/onec_platform/installer.py`, originally shipped
in Phase 6 / Step 3).

The wrapper bootstraps `PYTHONPATH` for the monorepo (via
`scripts/dev/bootstrap_paths.ps1`) and forwards the call to the
fast-path helper through `_install_runner.py`. No production code
is touched.

### Usage

Preview (no file is written):

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json
```

Execute (actually writes the JSON config):

```powershell
.\scripts\release\install.ps1 `
    -ConfigPath examples\demo-infobase\infobase6.config.json `
    -OutputConfigPath C:\path\to\target\product.config.json `
    -Confirm
```

### Parameters

- `-ConfigPath` (mandatory) — path to the input product config
  JSON. This is the operator-authored product config that should be
  validated and (optionally) materialised at the target location.
- `-OutputConfigPath` (mandatory) — where the materialised JSON
  should be written. The underlying helper refuses to overwrite an
  existing file (`mode=rejected`).
- `-Confirm` (switch, default off) — when present, the wrapper
  calls the helper with `confirm_write=True` and the file is
  actually written. When absent, the wrapper runs in preview mode
  and writes nothing.

### Output and exit codes

The wrapper prints a banner with the resolved paths, dot-sources
`bootstrap_paths.ps1`, runs the helper, and then prints the result
fields:

- `ok`, `mode`, `product_name`, `profile_name`,
  `default_environment`, `output_config_path`, `config_written`;
- any `confirmed findings` and `presumed findings` with their
  severity and code;
- any `recommended actions`.

Exit codes:

| Code | Meaning |
|------|---------|
| `0`  | `ok=True` and `mode in {"preview", "executed"}` |
| `2`  | `mode="rejected"` (target path exists, bad config, layout problem) |
| `3`  | any other failure (`ok=False` outside the rejected path) |
| `64` | wrapper invoked with bad arguments |

### What this wrapper deliberately does NOT do

- Does **not** start MCP servers.
- Does **not** invoke any `mcp_write_server` tool.
- Does **not** touch a 1С infobase.
- Does **not** use `shell=True`.
- Does **not** ship a packaging ecosystem (`.msi` / `.deb` / GUI
  wizard / signed distribution).
- Does **not** replace operator launch ergonomics for the three
  MCP servers — that is planned separately as Track B / Step 4
  and out of Step 3 scope.

### Files

- `install.ps1` — operator entry point.
- `_install_runner.py` — small Python helper called by the
  wrapper. Not meant to be imported. Underscore-prefixed by
  convention.
- `README.md` — this file.

### Related

- `apps/platform/src/onec_platform/installer.py` — the boundary
  helper this wrapper calls. The wrapper has no logic of its own
  beyond argument forwarding and exit-code mapping.
- `scripts/dev/bootstrap_paths.ps1` — PYTHONPATH bootstrap that
  the wrapper dot-sources.
- `apps/platform/README.md` — bigger picture of the product layer.
