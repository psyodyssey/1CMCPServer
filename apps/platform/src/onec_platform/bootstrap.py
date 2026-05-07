"""Bootstrap entrypoint for the product layer (Phase 5 / Step 2).

The bootstrap helper is the **boundary** between user-facing product
code and the strict (raising) loader/doctor helpers below it. By
contract:

- :func:`bootstrap_product` and :func:`bootstrap_product_from_json_file`
  **never raise**. Every error is wrapped into a structured
  :class:`BootstrapResult`.
- They never start MCP servers, never contact a real 1C stand, never
  perform a write operation.
- ``ok=True`` means bootstrap completed (config loaded and doctor
  ran). It does **not** mean "everything is healthy" — the caller
  must still check ``result.doctor.error_count`` to decide if the
  product is actually ready to run.

Step 2 stops here on purpose. Real start/stop/status orchestration
of the three MCP servers, plus an MCP transport layer, are the job
of Step 3 (runtime orchestration).
"""

from pathlib import Path

from .doctor import run_prereqs_doctor
from .loader import (
    load_product_config,
    load_product_config_from_json_file,
)
from .models import BootstrapResult, ProductConfig


def _bootstrap_loaded(config: ProductConfig) -> BootstrapResult:
    """Run doctor and assemble a :class:`BootstrapResult` for a loaded config."""
    doctor = run_prereqs_doctor(config)
    if doctor.error_count > 0:
        message = (
            f"Bootstrap completed with {doctor.error_count} blocking "
            f"finding(s) and {doctor.warning_count} warning(s). "
            "Product is not ready to run; see doctor.recommended_actions."
        )
    elif doctor.warning_count > 0:
        message = (
            f"Bootstrap completed with {doctor.warning_count} warning(s); "
            "product can run but operator review is recommended."
        )
    else:
        message = (
            "Bootstrap completed successfully; all prereqs checks ok."
        )
    return BootstrapResult(
        ok=True,
        product_name=config.product_name,
        profile_name=config.profile_name,
        default_environment=config.default_environment,
        doctor=doctor,
        message=message,
    )


def _bootstrap_rejected(reason: str) -> BootstrapResult:
    """Build an ``ok=False`` :class:`BootstrapResult` for an unloadable config."""
    return BootstrapResult(
        ok=False,
        product_name=None,
        profile_name=None,
        default_environment=None,
        doctor=None,
        message=f"Product config rejected: {reason}",
    )


def bootstrap_product(data: dict) -> BootstrapResult:
    """Boundary entrypoint. Validate a dict-shaped product config and run doctor.

    Sequence:

    1. :func:`load_product_config` — structural validation, raises
       :class:`ValueError` on bad input. Caught here.
    2. :func:`run_prereqs_doctor` — observe prereqs. Never raises.
    3. Build a :class:`BootstrapResult` with a human-readable message.

    Never raises. On a rejected config returns ``ok=False`` with the
    reason in ``message``; otherwise returns ``ok=True`` with a
    populated ``doctor`` field. ``doctor.error_count`` is the right
    signal for "is the product ready to run".
    """
    try:
        config = load_product_config(data)
    except (ValueError, TypeError) as exc:
        return _bootstrap_rejected(str(exc))
    return _bootstrap_loaded(config)


def bootstrap_product_from_json_file(path: str | Path) -> BootstrapResult:
    """Same as :func:`bootstrap_product`, but read the config from a JSON file.

    File-system errors and JSON-parse errors are converted into
    ``ok=False`` results by :func:`load_product_config_from_json_file`,
    which raises :class:`ValueError`; this boundary helper catches
    that and never propagates it.
    """
    try:
        config = load_product_config_from_json_file(path)
    except (ValueError, TypeError) as exc:
        return _bootstrap_rejected(str(exc))
    return _bootstrap_loaded(config)
