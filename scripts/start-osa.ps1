$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path); Set-Location $Root
& .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8787
