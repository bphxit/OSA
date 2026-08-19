$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $PSScriptRoot
$Incoming=Join-Path $Root 'data\incoming'
New-Item -ItemType Directory -Force $Incoming | Out-Null
New-Item -ItemType Directory -Force (Join-Path $Root 'data\reports') | Out-Null
& "$Root\.venv\Scripts\python.exe" "$Root\scripts\import_data.py" | Out-File -Append -FilePath "$Root\data\reports\ingestion.log" -Encoding utf8
$watcher=New-Object System.IO.FileSystemWatcher $Incoming,'*.csv'
$watcher.EnableRaisingEvents=$true
$action={
  Start-Sleep -Seconds 2
  try { & "$Root\.venv\Scripts\python.exe" "$Root\scripts\import_data.py" | Out-File -Append -FilePath "$Root\data\reports\ingestion.log" -Encoding utf8 }
  catch { $_ | Out-File -Append -FilePath "$Root\data\reports\ingestion-error.log" -Encoding utf8 }
}
Register-ObjectEvent $watcher Created -Action $action | Out-Null
while ($true) { Start-Sleep -Seconds 30 }
