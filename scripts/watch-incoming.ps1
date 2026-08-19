$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
while($true){ & "$Root\.venv\Scripts\python.exe" "$Root\scripts\import_data.py"; Start-Sleep -Seconds 30 }
