# run_dev_check.ps1
# Единая команда локальной проверки skeleton-проекта 1C Agent Platform.
# Выполняет bootstrap PYTHONPATH и запускает selfcheck в текущей сессии.
# Ничего не устанавливает, не меняет системное окружение.

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$bootstrap = Join-Path $root "scripts\dev\bootstrap_paths.ps1"
$selfcheck = Join-Path $root "scripts\dev\selfcheck.py"

. $bootstrap

python $selfcheck
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Dev check completed successfully."
} else {
    exit $exitCode
}
