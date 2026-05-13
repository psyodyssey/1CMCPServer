# ============================================================================
# first_run.ps1 - 1C Agent Platform first-run configurator
# Track Q / Step 4. Single user-facing surface after install per contract
# sec.8 / sec.9. Runs in Windows PowerShell 5.1+ (no PowerShell 7 required).
#
# Behaviour (locked by contract sec.8):
#   First run  - prompt for two paths (1cv8 executable + file-based 1C
#                infobase folder), validate, synthesise the input-config JSON,
#                call the existing fast-path helper through the bundled
#                python.exe, display + clipboard the Claude MCP snippet.
#   Later run  - display the existing config summary + the Claude MCP
#                snippet; offer Reconfigure.
#   Never      - spawn the MCP server, install autostart, install tray icon,
#                modify Claude's MCP config, modify PATH, modify production
#                code, write to anywhere other than %LOCALAPPDATA%\1C Agent
#                Platform\.
# ============================================================================

$ErrorActionPreference = 'Stop'

# --- Paths and constants -----------------------------------------------------

$InstallDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe  = Join-Path $InstallDir 'python\python.exe'
$StateDir   = Join-Path $env:LOCALAPPDATA '1C Agent Platform'
$ConfigPath = Join-Path $StateDir 'config.json'
$DumpsDir   = Join-Path $StateDir 'dumps'
$WorkDir    = Join-Path $StateDir '.runtime'
$ProductName = '1C Agent Platform'

Add-Type -AssemblyName System.Windows.Forms

# --- UI helpers --------------------------------------------------------------

function Show-Info {
    param([string]$Text, [string]$Title = $ProductName)
    [System.Windows.Forms.MessageBox]::Show(
        $Text, $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

function Show-Error {
    param([string]$Text)
    [System.Windows.Forms.MessageBox]::Show(
        $Text, "$ProductName — Ошибка",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
}

function Build-McpSnippet {
    $jsonPython = $PythonExe.Replace('\', '\\')
    return @"
{
  "mcpServers": {
    "1c-agent-platform-read": {
      "command": "$jsonPython",
      "args": ["-m", "mcp_read_server"]
    }
  }
}
"@
}

function Show-McpSnippet {
    param([string]$Preamble)
    $snippet = Build-McpSnippet
    $clipboardOk = $true
    try { Set-Clipboard -Value $snippet -ErrorAction Stop } catch { $clipboardOk = $false }
    $clipNote = if ($clipboardOk) {
        'Этот фрагмент уже скопирован в буфер обмена.'
    } else {
        'Скопировать в буфер обмена не удалось — скопируйте фрагмент вручную.'
    }
    Show-Info -Text @"
$Preamble

Вставьте этот фрагмент в настройку MCP-серверов вашего Claude-клиента:

$snippet

$clipNote

Claude сам запустит встроенный python.exe как stdio-подпроцесс и направит MCP read-инструменты к настроенной файловой базе 1С. Сейчас MCP-сервер не запущен — Claude поднимет его в следующей сессии.
"@
}

# --- Pickers -----------------------------------------------------------------

function Pick-1CV8Executable {
    param([string]$Default = '')
    $dlg = New-Object System.Windows.Forms.OpenFileDialog
    $dlg.Title = 'Выберите исполняемый файл 1cv8'
    $dlg.Filter = 'Исполняемые файлы 1С (1cv8.exe; 1cestart.exe)|1cv8.exe;1cestart.exe|Все файлы (*.*)|*.*'
    $dlg.CheckFileExists = $true
    $dlg.Multiselect = $false
    if ($Default -and (Test-Path -LiteralPath $Default)) {
        $dlg.InitialDirectory = Split-Path -Parent $Default
        $dlg.FileName = Split-Path -Leaf $Default
    }
    if ($dlg.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
    return $dlg.FileName
}

function Pick-FileBasedInfobase {
    param([string]$Default = '')
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description = 'Выберите папку файловой базы 1С (на верхнем уровне должен лежать файл .1cd). Клиент-серверные базы в этой версии не поддерживаются.'
    $dlg.ShowNewFolderButton = $false
    if ($Default -and (Test-Path -LiteralPath $Default -PathType Container)) {
        $dlg.SelectedPath = $Default
    }
    if ($dlg.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
    return $dlg.SelectedPath
}

function Test-IsFileBasedInfobase {
    param([string]$Folder)
    if (-not (Test-Path -LiteralPath $Folder -PathType Container)) { return $false }
    $found = Get-ChildItem -LiteralPath $Folder -Filter '*.1cd' -File -ErrorAction SilentlyContinue
    return ($null -ne $found -and @($found).Count -ge 1)
}

# --- Input-config synthesis (locked by contract sec.8.4) ---------------------

function Build-InputConfig {
    param([string]$OnecBinary, [string]$BasePath)
    return [ordered]@{
        product_name        = $ProductName
        profile_name        = 'default'
        default_environment = 'main'
        project = [ordered]@{
            environments = [ordered]@{
                main = [ordered]@{
                    name              = 'main'
                    base_id           = 'main'
                    base_path         = $BasePath
                    publication_name  = ''
                    http_base_url     = ''
                    dump_path         = $DumpsDir
                    timeout_seconds   = 600
                    allow_write       = $false
                    onec_binary_path  = $OnecBinary
                }
            }
        }
        servers   = [ordered]@{ read = $true; write = $false; intelligence = $false }
        bootstrap = [ordered]@{ work_dir = $WorkDir }
    }
}

# --- Fast-path invocation (locked by contract sec.8.5) ----------------------

function Invoke-FastPath {
    param([System.Collections.IDictionary]$InputObj)
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        Show-Error "Встроенный python.exe не найден по пути:`n$PythonExe`n`nПереустановите $ProductName."
        return $false
    }
    $tempDir = Join-Path $env:TEMP "$ProductName first run"
    if (-not (Test-Path -LiteralPath $tempDir)) {
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    }
    $tempInput = Join-Path $tempDir ("input-" + [Guid]::NewGuid().ToString() + ".json")
    try {
        if (-not (Test-Path -LiteralPath $StateDir)) {
            New-Item -ItemType Directory -Path $StateDir -Force | Out-Null
        }
        if (Test-Path -LiteralPath $ConfigPath) {
            Remove-Item -LiteralPath $ConfigPath -Force
        }
        # PowerShell 5.1 Set-Content -Encoding UTF8 emits a BOM, which Python
        # json.load rejects. Use .NET WriteAllText with explicit BOM-less UTF-8.
        [System.IO.File]::WriteAllText($tempInput, ($InputObj | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
        $py = @"
from onec_platform.installer import run_install_fast_path_from_json_file
r = run_install_fast_path_from_json_file(r'''$tempInput''', output_config_path=r'''$ConfigPath''', confirm_write=True)
print('ok=' + str(r.ok))
print('mode=' + str(r.mode))
for f in (r.confirmed_findings or []):
    print('finding=' + getattr(f, 'severity', '?') + ':' + getattr(f, 'code', '?') + ':' + getattr(f, 'detail', '?'))
import sys
sys.exit(0 if r.ok else 3)
"@
        $output = & $PythonExe -c $py 2>&1
        $code = $LASTEXITCODE
        if ($code -ne 0) {
            $detail = ($output -join "`n")
            Show-Error "Помощник установки завершился с ошибкой (код $code).`n`n$detail"
            return $false
        }
        if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
            Show-Error "Помощник установки сообщил об успехе, но файл $ConfigPath не создан."
            return $false
        }
        return $true
    } finally {
        try { Remove-Item -LiteralPath $tempInput -Force -ErrorAction SilentlyContinue } catch {}
        try { Remove-Item -LiteralPath $tempDir -Force -ErrorAction SilentlyContinue } catch {}
    }
}

# --- Configuration flow ------------------------------------------------------

function Invoke-Configure {
    param([string]$DefaultOnec = '', [string]$DefaultBase = '')

    $onec = Pick-1CV8Executable -Default $DefaultOnec
    if (-not $onec) { Show-Error 'Выбор исполняемого файла 1cv8 отменён. Изменения не сохранены.'; return $false }
    if (-not (Test-Path -LiteralPath $onec -PathType Leaf)) {
        Show-Error "Указанный путь к 1cv8 не существует:`n$onec"
        return $false
    }

    $base = Pick-FileBasedInfobase -Default $DefaultBase
    if (-not $base) { Show-Error 'Выбор папки информационной базы отменён. Изменения не сохранены.'; return $false }
    if (-not (Test-Path -LiteralPath $base -PathType Container)) {
        Show-Error "Указанная папка информационной базы не существует:`n$base"
        return $false
    }

    if (-not (Test-IsFileBasedInfobase $base)) {
        Show-Error @"
Выбранная папка не является файловой базой 1С (на верхнем уровне не найден файл .1cd).

Клиент-серверные информационные базы 1С в этой версии $ProductName не поддерживаются.

Инструкция по существующему инженерному пути для клиент-серверных баз (через scripts/release/install.ps1 + написанный вручную input JSON) находится в файле docs/operators/installer/windows-setup-exe.md.

Выбранная папка:
$base
"@
        return $false
    }

    $inputObj = Build-InputConfig -OnecBinary $onec -BasePath $base
    if (-not (Invoke-FastPath -InputObj $inputObj)) { return $false }

    Show-McpSnippet -Preamble "Конфигурация сохранена в файл:`n$ConfigPath`n`n  Исполняемый файл 1cv8 : $onec`n  Папка информационной базы : $base"
    return $true
}

function Invoke-SubsequentLaunch {
    try {
        $existing = Get-Content -LiteralPath $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $envMain = $existing.project.environments.main
        $existingOnec = $envMain.onec_binary_path
        $existingBase = $envMain.base_path
    } catch {
        Show-Error "Не удалось прочитать существующий файл конфигурации:`n$ConfigPath`n`n$($_.Exception.Message)`n`nЧтобы начать заново, удалите этот файл вручную."
        return
    }

    $summary = @"
Текущая конфигурация ${ProductName}:
  Исполняемый файл 1cv8     : $existingOnec
  Папка информационной базы : $existingBase
  Файл конфигурации         : $ConfigPath
"@

    $choice = [System.Windows.Forms.MessageBox]::Show(
        "$summary`n`nНажмите ОК — чтобы увидеть фрагмент настройки Claude MCP (и одновременно скопировать его в буфер обмена).`nНажмите Отмена — чтобы перенастроить с новыми путями.",
        "$ProductName — Текущая конфигурация",
        [System.Windows.Forms.MessageBoxButtons]::OKCancel,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )

    if ($choice -eq [System.Windows.Forms.DialogResult]::Cancel) {
        Invoke-Configure -DefaultOnec $existingOnec -DefaultBase $existingBase | Out-Null
    } else {
        Show-McpSnippet -Preamble $summary
    }
}

# --- Entry point -------------------------------------------------------------

if (Test-Path -LiteralPath $ConfigPath -PathType Leaf) {
    Invoke-SubsequentLaunch
} else {
    Show-Info -Text @"
Добро пожаловать в $ProductName.

Это разовая настройка. Сейчас потребуется указать:
  1. Исполняемый файл 1cv8 (1cv8.exe или 1cestart.exe).
  2. Папку файловой базы 1С (на верхнем уровне должен лежать файл .1cd).

Клиент-серверные информационные базы 1С в этой версии не поддерживаются — для них есть отдельный инженерный путь через scripts/release/install.ps1 (см. инструкцию оператора).
"@ -Title "$ProductName — Первый запуск"
    Invoke-Configure | Out-Null
}
