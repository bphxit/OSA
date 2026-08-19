param([switch]$NoScheduledTask)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $PSScriptRoot
Set-Location $Root
Write-Host '=== OSA Therapy System - Windows 11 Installer ==='
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Python 3.11+ is required. Install Python and rerun.' }
py -3 -m venv .venv
& .venv\Scripts\python.exe -m pip install --upgrade pip
& .venv\Scripts\python.exe -m pip install -r requirements.txt
& .venv\Scripts\python.exe -c "from app.core.db import connect; connect().close(); print('Local database initialized.')"
New-Item -ItemType Directory -Force data\incoming,data\processed,data\archive,data\medical,data\reports | Out-Null
if (-not $NoScheduledTask) {
 $task='OSA Therapy Data Watcher'; $cmd="powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Root\scripts\watch-incoming.ps1`""; schtasks.exe /Create /TN $task /TR $cmd /SC ONLOGON /RL LIMITED /F | Out-Null
}
Write-Host 'Installation complete.'
