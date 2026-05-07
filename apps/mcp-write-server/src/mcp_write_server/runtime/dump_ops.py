"""Low-level dump / source-tree helpers for write-flow operation callables."""

import json
import shutil
from pathlib import Path

from onec_process_runner import ProcessRunRequest, run_process


def run_stub_apply_process(source_dump_path: str) -> dict:
    """Run the temporary stub apply process that writes marker + meta.

    This is NOT a real ``1cv8 LoadConfigFromFiles``. It is a deliberate
    Phase 2 / Step 7 placeholder that exercises the full write-flow wiring
    (preflight → snapshot → operation → verify → audit) end-to-end while
    the real 1C binary integration is still pending.

    Raises:
        FileNotFoundError: if ``source_dump_path`` is missing or
            ``python`` is not available on PATH.
        RuntimeError: if the underlying process did not complete with
            ``exit_code == 0``.
    """
    source = Path(source_dump_path)
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(
            f"source_dump_path does not exist or is not a directory: {source_dump_path}"
        )
    python_exe = shutil.which("python")
    if python_exe is None:
        raise FileNotFoundError(
            "Python interpreter not found in PATH for stub apply."
        )

    marker_path = source / "apply-stub.txt"
    process_result = run_process(
        ProcessRunRequest(
            command=[
                python_exe,
                "-c",
                "import sys; open(sys.argv[1], 'w', encoding='utf-8').write('applied')",
                str(marker_path),
            ],
            timeout_seconds=10,
        )
    )
    if not process_result.completed or process_result.exit_code != 0:
        raise RuntimeError(
            f"Stub apply process failed: completed={process_result.completed} "
            f"exit_code={process_result.exit_code} stderr={process_result.stderr!r}"
        )

    meta = {
        "mode": "stub-process-apply",
        "source_dump_path": source_dump_path,
    }
    (source / "apply-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False), encoding="utf-8"
    )
    return {
        "applied": True,
        "mode": "stub-process-apply",
        "source_dump_path": source_dump_path,
        "marker_path": str(marker_path),
    }
