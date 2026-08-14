$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$pythonPath = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Không tìm thấy .venv. Hãy chạy: python -m venv .venv"
}

& $pythonPath -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
