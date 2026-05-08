"""Shared internal helpers for binary-backed write-tool dispatch.

This module is **internal**. It is consumed by exactly three public
write-tools:

- :func:`mcp_write_server.tools.create_dump_snapshot`
  (Phase 6 / Step 2 binary-backed branch)
- :func:`mcp_write_server.tools.apply_config_from_files`
  (Parallel Track A / Step 2 binary-backed branch)
- :func:`mcp_write_server.tools.update_database_configuration`
  (Parallel Track A / Step 3 binary-backed branch)

Parallel Track A / Step 4 — internal unification slice. Before
Step 4 each of the three tools carried its own copy of:

- a ``_*_OUTPUT_EXCERPT_LIMIT`` constant (all three set to 1024);
- a ``_*_DEFAULT_TIMEOUT_SECONDS`` constant (all three set to 300);
- a ``_render_*_command`` function with the same shape, differing
  only in tool-specific substitutions / whitelist / config-field
  name in the error message;
- inline construction of the operator-visible honest-mode payload
  fields (``mode`` / ``binary_invoked`` / ``exit_code`` /
  ``command_preview`` / ``stdout_excerpt`` / ``stderr_excerpt``);
- the shape verify check (``completed && exit_code == 0``).

Step 4 lifts these into one shared place. The diff is internal:
operator-facing argv grammar, placeholder whitelists per tool, and
``ToolResult`` shape are unchanged.

What this module is NOT:

- it does **not** introduce new MCP tools or change any registry;
- it does **not** wrap ``run_write_flow`` and is not aware of
  audit / snapshots / verify stages — those concerns stay in
  ``runtime/flow.py`` and in the per-tool dispatchers;
- it does **not** know about per-tool placeholder whitelists —
  the whitelist is passed in from the caller, so the tool-specific
  intent stays explicit at the call site;
- it does **not** ship a "binary-backed framework for all future
  write-tools" — only the three current binary-backed paths use it.

Failure model:

- :func:`render_command_template` raises :class:`ValueError` on
  unknown placeholder, non-string template entry, or any other
  malformed shape — fail-closed by design. Callers translate that
  into a structured ``ToolResult(ok=False, ...)`` at the boundary.
- All other helpers are pure dict / value transformations and do
  not raise unless the caller passes structurally-broken input
  (which is a programming error, not a runtime condition).

Track D / Step 3 additions:

- :func:`render_command_template` now also resolves full-element
  env-substitution tokens of the shape ``${ENV:NAME}`` against the
  process environment. Missing / empty / mixed / partial forms are
  fail-closed via :class:`ValueError` (same boundary discipline as
  unknown structural placeholders). See
  ``docs/architecture/track-d-credentials-contract.md`` for the
  normative contract.
- :func:`binary_backed_start_failure_fields` and
  :func:`binary_backed_payload_fields` now build
  ``command_preview`` through :func:`_redact_password_args`, which
  replaces the argv element immediately following ``/P`` / ``/Pwd``
  (case-insensitive) with the sentinel ``"<redacted>"``. The actual
  argv passed to the subprocess runner is **not** modified —
  redaction is observation-side only.
"""

from __future__ import annotations

import os
import re
from typing import Any

from onec_process_runner import ProcessRunResult


# ---------------------------------------------------------------------------
# Unified constants.
# ---------------------------------------------------------------------------


# Maximum bytes of stdout / stderr surfaced in a binary-backed
# write-tool's payload. The same cap applies to all three current
# binary-backed write-tools — operator's full logs remain operator
# territory (operator manuals).
BINARY_OUTPUT_EXCERPT_LIMIT: int = 1024


# Default subprocess timeout for binary-backed write-tools. A real
# 1cv8 run (DumpCfg / LoadCfg / UpdateDBCfg) can take noticeably
# longer than the Phase 5 / Step 7 smoke probe (30 s); the 300 s
# cap is the operator-friendly default that all three tools share.
BINARY_DEFAULT_TIMEOUT_SECONDS: int = 300


# ---------------------------------------------------------------------------
# Placeholder substitution.
# ---------------------------------------------------------------------------


class UnknownPlaceholderError(KeyError):
    """Internal signal raised by :class:`PlaceholderProxy` for unknown keys.

    Caller (typically :func:`render_command_template`) translates
    this into a descriptive :class:`ValueError` that names the
    config field and the allowed placeholders. The class is public
    inside this module so the proxy / render layer can be unit-tested
    independently of any specific tool.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name


class PlaceholderProxy(dict):
    """Tiny dict-like façade that fail-closes on unknown placeholders.

    ``str.format_map`` calls ``__getitem__`` for every ``{name}`` it
    encounters. Unknown names are translated into
    :class:`UnknownPlaceholderError`, which the caller turns into a
    descriptive :class:`ValueError`.
    """

    def __init__(self, substitutions: dict[str, str]) -> None:
        super().__init__(substitutions)

    def __missing__(self, key: str):  # noqa: D401
        raise UnknownPlaceholderError(key)


# ---------------------------------------------------------------------------
# Track D / Step 3 — env-substitution token (${ENV:NAME}).
# ---------------------------------------------------------------------------
#
# Operator may write a full-element token of the shape ``${ENV:NAME}``
# in any argv position of the template. The render step resolves the
# token against ``os.environ`` and substitutes the value into the
# rendered argv list passed to the subprocess runner. Missing or
# empty env, or a partial / mixed token (anything other than the
# full-element regex below), is fail-closed via :class:`ValueError`
# — the same boundary discipline as unknown structural placeholders.
#
# Per Track D / Step 2 contract, env tokens and structural
# placeholders never coexist in one element (mixing is fail-closed).
# We therefore dispatch by element-entry inspection: an element that
# contains the ``${ENV:`` substring goes through the env resolver;
# any other element goes through ``str.format_map`` for structural
# substitution. Without this dispatch, ``format_map`` would
# misinterpret ``${ENV:NAME}`` as a structural ``{ENV:NAME}``
# placeholder named ``ENV`` with format-spec ``NAME``, defeating
# the env path.
_ENV_TOKEN_SUBSTRING: str = "${ENV:"
_ENV_TOKEN_RE: re.Pattern[str] = re.compile(
    r"^\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}$"
)


def _resolve_env_token(value: str, *, template_field_name: str) -> str:
    """Resolve a full-element env-substitution token against the
    process environment, fail-closed on any non-full-element form
    or missing / empty value.

    Returns ``value`` unchanged when it does not contain the
    ``${ENV:`` substring at all (the literal / structural-only
    path). Raises :class:`ValueError` when the substring is present
    but the element is not a full-element token, or when the named
    env var is missing or empty.
    """
    if _ENV_TOKEN_SUBSTRING not in value:
        return value
    match = _ENV_TOKEN_RE.match(value)
    if match is None:
        raise ValueError(
            f"{template_field_name} entry contains an invalid "
            f"env-substitution form; only a full-element token of "
            f"the shape ${{ENV:NAME}} is supported (no substring "
            f"mixing, no partial concatenation, no multi-token in "
            f"one element)."
        )
    name = match.group(1)
    resolved = os.environ.get(name)
    if not resolved:
        raise ValueError(
            f"{template_field_name} references env var '{name}' "
            f"which is not set or is empty; set it before rendering, "
            f"or replace the token with a literal value."
        )
    return resolved


def render_command_template(
    template: list[str],
    *,
    substitutions: dict[str, str],
    allowed_placeholders: frozenset[str] | set[str],
    template_field_name: str,
) -> list[str]:
    """Render an operator-declared argv template with whitelisted
    placeholders and full-element env-substitution tokens.

    Substitution is per-item, no shell. Each element is dispatched
    by inspection:

    - if the element contains the ``${ENV:`` substring, it is
      treated as a full-element env-substitution token and resolved
      via :func:`_resolve_env_token` (fail-closed on partial /
      mixed forms and missing / empty env);
    - otherwise the element is treated as a structural template and
      passed through :meth:`str.format_map` with
      :class:`PlaceholderProxy`. Each ``{name}`` reference must
      appear in ``allowed_placeholders``; otherwise a
      :class:`ValueError` is raised so the boundary can fail-closed.

    Per Track D / Step 2 contract, env tokens and structural
    placeholders never coexist in one element. Bare ``{`` / ``}``
    (i.e. literal braces in the operator argv) is intentionally
    not supported on this slice — operators who really need a
    literal brace in a 1cv8 argv should escape it via their own
    pre-rendering, since 1cv8 itself does not require curly braces
    in any documented flag of the supported flows (DumpCfg,
    LoadConfigFromFiles, UpdateDBCfg).

    The ``template_field_name`` argument names the
    ``EnvironmentConfig`` field whose template is being rendered
    (e.g. ``"onec_dumpcfg_command_template"``); it is woven into
    the error message so an operator who saw an unknown-placeholder
    rejection immediately knows which field to fix. The
    ``allowed_placeholders`` set is also surfaced in the error
    message so the operator can correct the typo without consulting
    documentation.
    """
    rendered: list[str] = []
    for raw in template:
        if not isinstance(raw, str):
            raise ValueError(
                f"{template_field_name} entry is not a string."
            )
        if _ENV_TOKEN_SUBSTRING in raw:
            value = _resolve_env_token(
                raw, template_field_name=template_field_name
            )
        else:
            try:
                value = raw.format_map(PlaceholderProxy(substitutions))
            except UnknownPlaceholderError as exc:
                raise ValueError(
                    f"Unknown placeholder {{{exc.name}}} in "
                    f"{template_field_name}; allowed placeholders are: "
                    f"{sorted(allowed_placeholders)}."
                ) from None
        rendered.append(value)
    return rendered


# ---------------------------------------------------------------------------
# Track D / Step 3 — preview redaction for password-position argv.
# ---------------------------------------------------------------------------
#
# 1С DESIGNER CLI takes the password as a positional argument
# immediately following ``/P`` or ``/Pwd`` (case-insensitive).
# The actual argv list passed to ``subprocess`` carries the real
# value (otherwise the binary would not authenticate); however,
# every observable copy that lands in the ``command_preview``
# payload field — which is in turn surfaced to the MCP client and
# to the audit row's ``details`` — goes through
# :func:`_redact_password_args` and has the password-position
# value replaced with the sentinel ``"<redacted>"``.
#
# Redaction is positional only — no pattern-matching on the value
# itself. The sentinel applies regardless of whether the original
# value came from a literal cleartext template (legacy path) or
# from an env-substitution token resolved at render time. Username
# (``/N``) is *not* redacted: usernames have lower sensitivity and
# redacting them would give a false sense of security at the
# observation layer while the (more important) password redaction
# still relies on the same positional rule.
_PASSWORD_FLAG_TOKENS: frozenset[str] = frozenset({"/P", "/PWD"})
_REDACTION_SENTINEL: str = "<redacted>"


def _redact_password_args(argv: list[str]) -> list[str]:
    """Return a copy of ``argv`` with password-position values
    replaced by the redaction sentinel.

    Walks the argv list; whenever an element compares
    case-insensitive-equal to ``/P`` or ``/Pwd``, the element
    immediately following it (if any) is replaced by
    :data:`_REDACTION_SENTINEL` in the returned list. The input
    list is not modified — the actual subprocess argv stays
    unredacted.

    A trailing ``/P`` / ``/Pwd`` with no following element is
    surfaced as-is; redaction has nothing to substitute and is
    silent in that pathological case.
    """
    redacted: list[str] = []
    n = len(argv)
    i = 0
    while i < n:
        elem = argv[i]
        redacted.append(elem)
        if isinstance(elem, str) and elem.upper() in _PASSWORD_FLAG_TOKENS:
            if i + 1 < n:
                redacted.append(_REDACTION_SENTINEL)
                i += 2
                continue
        i += 1
    return redacted


# ---------------------------------------------------------------------------
# Output excerpt cap.
# ---------------------------------------------------------------------------


def excerpt(text: str | None) -> str | None:
    """Cap subprocess output at :data:`BINARY_OUTPUT_EXCERPT_LIMIT`.

    Returns ``None`` for ``None`` input (so stub-mode payloads can
    honestly carry ``stdout_excerpt = None`` without special-casing
    at every call site). Truncation is marked with an explicit
    ``...[truncated]`` suffix.
    """
    if text is None:
        return None
    if len(text) <= BINARY_OUTPUT_EXCERPT_LIMIT:
        return text
    return text[:BINARY_OUTPUT_EXCERPT_LIMIT] + "...[truncated]"


# ---------------------------------------------------------------------------
# Honest-mode payload fields — the unified six.
# ---------------------------------------------------------------------------
#
# Operator-visible discipline (Track A / Steps 2–4): every binary-
# backed write-tool emits the same six fields in its payload data,
# regardless of branch. In stub mode the binary-backed-only fields
# are honestly ``None`` / ``False`` (never silently omitted). In
# binary-backed mode they are populated by
# :func:`binary_backed_payload_fields`. Tool-specific keys
# (``snapshot_type``, ``snapshot_path``, ``source_dump_path``,
# ``marker_path``, …) live alongside these six and are unchanged
# by the unification.


_HONEST_MODE_KEYS: tuple[str, ...] = (
    "mode",
    "binary_invoked",
    "exit_code",
    "command_preview",
    "stdout_excerpt",
    "stderr_excerpt",
)


def stub_honest_mode_fields() -> dict[str, Any]:
    """Return the unified honest-mode field dict for the stub branch.

    All binary-backed-only fields are explicitly ``None`` / ``False``
    so callers can spread this into their stub payload via ``**``
    without forgetting any field.
    """
    return {
        "mode": "stub",
        "binary_invoked": False,
        "exit_code": None,
        "command_preview": None,
        "stdout_excerpt": None,
        "stderr_excerpt": None,
    }


def binary_backed_render_failure_fields() -> dict[str, Any]:
    """Return the unified honest-mode field dict for the case when
    rendering the operator-declared argv template failed
    (e.g. unknown placeholder).

    ``mode`` is ``"binary-backed"`` (the operator did declare the
    binary contract — that's why we entered this branch in the
    first place), but ``binary_invoked`` is honestly ``False``
    because no PID was ever produced. ``command_preview`` is
    ``None`` because the render failed before we had any rendered
    argv to surface.
    """
    return {
        "mode": "binary-backed",
        "binary_invoked": False,
        "exit_code": None,
        "command_preview": None,
        "stdout_excerpt": None,
        "stderr_excerpt": None,
    }


def binary_backed_start_failure_fields(
    command: list[str],
) -> dict[str, Any]:
    """Return the honest-mode field dict for the case when the
    subprocess could not be started at all (``PlatformError`` from
    the runner — missing binary, etc).

    ``binary_invoked`` is ``False`` because no PID was produced.
    ``command_preview`` is the rendered argv with password-position
    values redacted (Track D / Step 3) — we have the rendered argv
    because render succeeded and only the spawn failed; the operator
    can read exactly what we tried to run, while any
    ``/P`` / ``/Pwd`` value is replaced by the redaction sentinel.
    """
    return {
        "mode": "binary-backed",
        "binary_invoked": False,
        "exit_code": None,
        "command_preview": _redact_password_args(command),
        "stdout_excerpt": None,
        "stderr_excerpt": None,
    }


def binary_backed_payload_fields(
    command: list[str],
    process_result: ProcessRunResult,
) -> dict[str, Any]:
    """Return the honest-mode field dict for the case when the
    subprocess actually ran (``binary_invoked = True``), regardless
    of whether it returned 0 or non-zero exit.

    ``completed`` is added as a 7th field beyond the unified six —
    it is what the tool-specific verify step uses to decide
    success / failure (see :func:`is_binary_subprocess_successful`).
    ``command_preview`` is built through :func:`_redact_password_args`
    (Track D / Step 3) so that any password-position argv element
    is surfaced as the redaction sentinel rather than the actual
    value; the input ``command`` list (the real subprocess argv) is
    not modified. Tool-specific extras (``snapshot_path``,
    ``source_dump_path``, …) are merged in by the caller.
    """
    return {
        "mode": "binary-backed",
        "binary_invoked": True,
        "exit_code": process_result.exit_code,
        "completed": process_result.completed,
        "command_preview": _redact_password_args(command),
        "stdout_excerpt": excerpt(process_result.stdout),
        "stderr_excerpt": excerpt(process_result.stderr),
    }


def is_binary_subprocess_successful(payload_fields: dict[str, Any]) -> bool:
    """Return True iff the binary-backed payload describes a clean
    subprocess run (``completed=True`` and ``exit_code == 0``).

    Used by tool-specific verify callables that need to decide
    success / failure based on the captured subprocess outcome.
    Discipline: the payload fields **must** come from
    :func:`binary_backed_payload_fields` (i.e. the subprocess
    actually ran). For render-failure / start-failure variants the
    caller does not call this — those fail fail-closed before
    any verify happens.
    """
    return (
        bool(payload_fields.get("completed"))
        and payload_fields.get("exit_code") == 0
    )


# ---------------------------------------------------------------------------
# Honest-mode payload field set — for tests / docs.
# ---------------------------------------------------------------------------


def honest_mode_keys() -> tuple[str, ...]:
    """Return the unified six honest-mode field names.

    Useful for parity-asserting tests: every binary-backed-tool
    payload (in any branch) must contain at least these six keys.
    """
    return _HONEST_MODE_KEYS
