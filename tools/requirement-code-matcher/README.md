# Requirements ↔ Code Matcher V3

This bundle accepts one Word `.docx` requirements document and its source tree. Before code understanding and matching, an LLM reviews the extracted requirements and processing steps. It excludes obligations outside source/configuration scope and document debris, and splits compound embedded-device actions into atomic acquisition, perception, interaction, or computation steps. The review preserves every original requirement and step with its inclusion decision and new step IDs. The final deliverables are `requirements_review.html`/`.json`, `report_v3_guarded.html`, and `matches_v3_guarded.json` in the output directory.

## Requirements

- Windows, macOS, or Linux with 64-bit Python 3.10–3.13 and internet access to install the pinned Python dependencies and call the configured LLM. The installer creates a local `.venv` and does not need a system-wide Python package installation. This release was acceptance-tested on Windows; macOS/Linux require a local installation check.
- A provider that exposes an HTTPS OpenAI-compatible `/chat/completions` endpoint and supports JSON-object responses. The foxBMS 2 experiment used DeepSeek `deepseek-flash`.
- The project source tree. For the same code understanding result, use the same source revision, build configuration, parser backend, model, and prompt version. Model sampling temperature is set to zero, but provider-side changes and nondeterminism can still change decisions. The bundle reproduces the workflow and evidence format, not a guarantee of byte-identical labels.

## Install and configure

Windows PowerShell:

```powershell
./install.ps1
Copy-Item model.env.example model.env
```

macOS/Linux:

```sh
sh install.sh
cp model.env.example model.env
```

Edit **only** `model.env` to set `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`. Keep this file private. Do not put the key in command arguments or share an output directory that contains secrets.

## Run from Word and source

Windows:

```powershell
.venv/Scripts/python.exe run_v3_full.py --document "C:/work/requirements.docx" --source "C:/work/project" --model-env model.env --output "C:/work/result"
```

macOS/Linux:

```sh
.venv/bin/python run_v3_full.py --document /work/requirements.docx --source /work/project --model-env model.env --output /work/result
```

The default `clang` backend requires `libclang`, installed by the setup script. If the source project needs compile flags, provide its `compile_commands.json` in the source tree or use `--prepare-build` when the local build toolchain is installed. `--backend auto` allows the parser's fallback, but may produce different evidence and matching results. `--workers N` controls concurrent model calls.

To reuse an existing enriched codeComp graph, add `--graph /path/to/enriched_raw_graph.json`; this skips code understanding and still checks the matching process against the supplied source directory. `--baseline /path/to/matches_v2.json` optionally supplies old candidate hints when its document and graph hashes match; it never supplies verdicts. For an independent run, omit it.

The pipeline writes checkpoints for each reviewed step and reuses the pre-match review when its Word hash, model, and review prompt are unchanged. Repeating the same command resumes valid checkpoints. Keep the output directory if a model request fails. Inspect `requirements_review.html` before interpreting match rates: excluded and `needs_review` items do not enter the denominator, and an LLM review cannot guarantee that every split preserved the original meaning.

The matcher also uses codeComp caller/callee links and same-file proximity to reserve at most two of the later function slots for structurally related candidates. Up to two exact referenced macros may replace later source-unit slots. The first eight functions and the overall candidate count are preserved. Requirement-document trace appendices are excluded from retrieval so the quality review does not use its own reverse-engineering answer as a search hint. Use `--no-structure-expand` for a lexical/embedding-only comparison.

## Optional local embedding retrieval (Windows)

Run `./install_embedding.ps1` after the normal installer. It downloads the public `BAAI/bge-small-zh-v1.5` model once into `.models/bge-small-zh-v1.5`; no second API key is needed. Add `--embedding-model .models/bge-small-zh-v1.5` to `run_v3_full.py`. The existing lexical top eight is retained for precise symbols; semantic candidates diversify later retrieval positions. The embedding index is cached in the output directory. Embedding similarity only chooses candidates; source citations and step verdicts still follow the same checks. An output produced with this option has different checkpoint fingerprints from a lexical-only run.

## Interpretation

Each selected **step** is binary: `matched` only when all of its required code facts have cited source evidence; otherwise `not_matched`. For a failed step, `reason_kind`, individual claim statuses, citations, and missing evidence remain available to explain why. A **requirement** is `matched` when all selected steps match, `partial` when at least one but not all steps match, and `unmatched` when none match. These labels are an audit queue, not a quality score. A missing candidate does not establish a defect in the Word document. Row citations are range-checked, and the report provides a reverse coverage view; human verification remains necessary for semantic correctness.

No explicit data dictionary is used in this release.

## Verify installation

```sh
python -m unittest discover -s tests -q
```

The release `manifest.json` lists the SHA-256 of every included file. The archive contains source code, prompts, tests, and setup files. It excludes local `.env` files, experiment inputs, result files, Windows-only bundled binaries, and Python caches.
