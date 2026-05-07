"""Tiny operator-facing runner for ``run_install_fast_path_from_json_file``.

Called by ``scripts/release/install.ps1``. Not meant to be imported.
This file deliberately has no logic of its own beyond argument
parsing, calling the existing boundary helper, printing the result
fields, and mapping the dataclass outcome to a process exit code.

Argv contract (positional, no flags):

    _install_runner.py <input-config-path> <output-config-path> <confirm-flag>

``confirm-flag`` is the literal string ``true`` or ``false``.

Exit codes:

- ``0`` — ``ok=True`` and ``mode in {"preview", "executed"}``.
- ``2`` — ``mode="rejected"`` (operator gate, e.g., target path
  already exists, bad config, layout problem).
- ``3`` — any other failure (``ok=False`` outside the rejected path).
- ``64`` — wrapper invoked with bad arguments (EX_USAGE-ish).
"""

from __future__ import annotations

import sys

from onec_platform import run_install_fast_path_from_json_file


_USAGE = (
    "usage: _install_runner.py <input-config-path> <output-config-path> "
    "<true|false>"
)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(_USAGE, file=sys.stderr)
        return 64

    config_path, output_config_path, confirm_flag = argv
    if confirm_flag not in ("true", "false"):
        print(
            f"confirm flag must be 'true' or 'false', got {confirm_flag!r}",
            file=sys.stderr,
        )
        return 64

    confirm_write = confirm_flag == "true"

    result = run_install_fast_path_from_json_file(
        config_path,
        output_config_path=output_config_path,
        confirm_write=confirm_write,
    )

    print(f"ok                 : {result.ok}")
    print(f"mode               : {result.mode}")
    print(f"product_name       : {result.product_name}")
    print(f"profile_name       : {result.profile_name}")
    print(f"default_environment: {result.default_environment}")
    print(f"output_config_path : {result.output_config_path}")
    print(f"config_written     : {result.config_written}")

    if result.confirmed_findings:
        print("confirmed findings :")
        for f in result.confirmed_findings:
            print(f"  [{f.severity}] {f.code}: {f.detail}")

    if result.presumed_findings:
        print("presumed findings  :")
        for f in result.presumed_findings:
            print(f"  [{f.severity}] {f.code}: {f.detail}")

    if result.recommended_actions:
        print("recommended actions:")
        for a in result.recommended_actions:
            print(f"  - {a}")

    if result.ok and result.mode in ("preview", "executed"):
        return 0
    if result.mode == "rejected":
        return 2
    return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
