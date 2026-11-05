$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -m venv (Join-Path $root '.venv')
} else {
    $launcher = Get-Command py -ErrorAction Stop
    & $launcher.Source -3 -m venv (Join-Path $root '.venv')
}
if ($LASTEXITCODE -ne 0) { throw 'Python virtual environment creation failed' }
$venvPython = Join-Path $root '.venv\Scripts\python.exe'
& $venvPython -m pip install -r (Join-Path $root 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& $venvPython -c "import docx, clang.cindex; print('Dependencies ready')"
if ($LASTEXITCODE -ne 0) { throw 'Dependency import check failed' }
Write-Host "Installed. Copy model.env.example to model.env, configure the LLM, then run .venv\Scripts\python.exe run_v3_full.py --help"
