#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 -m venv "$root/.venv"
"$root/.venv/bin/python" -m pip install -r "$root/requirements.txt"
"$root/.venv/bin/python" -c 'import docx, clang.cindex; print("Dependencies ready")'
printf '%s\n' 'Installed. Copy model.env.example to model.env, configure the LLM, then run .venv/bin/python run_v3_full.py --help'
