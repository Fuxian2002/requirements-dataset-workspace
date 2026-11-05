$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Run install.ps1 first' }
& $python -m pip install -r (Join-Path $root 'requirements-embedding.txt') 'huggingface_hub>=0.24'
if ($LASTEXITCODE -ne 0) { throw 'Embedding dependency installation failed' }
$target = Join-Path $root '.models\bge-small-zh-v1.5'
& $python -c "from huggingface_hub import snapshot_download; import sys; snapshot_download('BAAI/bge-small-zh-v1.5', allow_patterns=['config.json','tokenizer.json','tokenizer_config.json','vocab.txt','model.safetensors','special_tokens_map.json'], local_dir=sys.argv[1])" $target
if ($LASTEXITCODE -ne 0) { throw 'Embedding model download failed' }
Write-Host "Embedding model ready: $target"
