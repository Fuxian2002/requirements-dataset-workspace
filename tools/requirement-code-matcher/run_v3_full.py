"""One entry point for Word + source -> codeComp -> reviewed V3 report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from codecomp_bridge import run_codecomp, verify_graph_source
from llm_match import load_model_config
from review_requirements import REVIEW_PROMPT, load_review, review_document
import hashlib


HERE = Path(__file__).resolve().parent


def invoke(script: str, **kwargs: object) -> None:
    command = [sys.executable, str(HERE / script)]
    for name, value in kwargs.items():
        if value is True:
            command.append("--" + name.replace("_", "-"))
        elif value is not None and value is not False:
            command += ["--" + name.replace("_", "-"), str(value)]
    subprocess.run(command, cwd=HERE, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Word + source to reviewed requirement/code HTML")
    ap.add_argument("--document", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--model-env", type=Path, required=True)
    ap.add_argument("--model", help="Optional override of LLM_MODEL in the config file")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--graph", type=Path, help="Reuse an enriched codeComp graph")
    ap.add_argument("--baseline", type=Path, help="Optional V2 retrieval hints, same document and graph only")
    ap.add_argument("--code-tool", type=Path, default=HERE / "codecomp" / "tools")
    ap.add_argument("--backend", choices=("auto", "clang", "fallback"), default="clang")
    ap.add_argument("--prepare-build", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-rounds", type=int, choices=(1, 2, 3, 4), default=2,
                    help="Maximum code evidence retrieval rounds per step")
    ap.add_argument("--checkpoint-from", type=Path,
                    help="Previous output directory for unchanged per-step matching checkpoints")
    ap.add_argument("--embedding-model", type=Path,
                    help="Local embedding model directory for hybrid function retrieval")
    ap.add_argument("--embedding-weight", type=float, default=1.0)
    ap.add_argument("--no-structure-expand", action="store_true")
    args = ap.parse_args()
    if args.workers < 1:
        ap.error("--workers must be positive")
    if args.output.resolve().is_relative_to(args.source.resolve()):
        ap.error("--output must be outside the source tree to keep source hashes stable")
    args.output.mkdir(parents=True, exist_ok=True)
    config = load_model_config(args.model_env, args.model or "")
    if "your-provider.example" in config["base_url"] or config["api_key"].startswith("replace-"):
        ap.error("Edit model.env with a real LLM endpoint and API key before running")
    review_path = args.output / "requirements_review.json"
    try:
        previous_review = load_review(review_path, args.document.resolve())
        if (previous_review.get("model") != config["model"] or
                previous_review.get("review_prompt_sha256") != hashlib.sha256(
                    REVIEW_PROMPT.encode("utf-8")).hexdigest()):
            raise ValueError("Review model or prompt changed")
        if not previous_review.get("selected_requirement_count"):
            ap.error(f"No code-verifiable requirements; see {review_path.with_suffix('.html')}")
        print(f"Reusing requirement review: {review_path}", flush=True)
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError):
        review_document(args.document.resolve(), config, review_path)
    graph = args.graph
    if graph is None:
        graph_dir = args.output / "codecomp"
        graph_dir.mkdir(exist_ok=True)
        graph = run_codecomp(args.source.resolve(), args.code_tool.resolve(), graph_dir,
                             backend=args.backend, prepare_build=args.prepare_build,
                             model=config["model"], base_url=config["base_url"],
                             api_key=config["api_key"], concurrency=args.workers)
    alignment = verify_graph_source(graph.resolve(), args.source.resolve())
    print(f"Graph/source alignment: {alignment['checked']} functions, "
          f"{alignment['truncated_prefixes']} truncated graph excerpts", flush=True)
    common = {"document": args.document.resolve(), "graph": graph.resolve(),
              "source": args.source.resolve(), "model_env": args.model_env.resolve(),
              "model": config["model"], "output": args.output.resolve()}
    invoke("match_v3.py", **common, reviewed_input=review_path.resolve(),
           baseline=args.baseline.resolve() if args.baseline else None,
           workers=args.workers, max_rounds=args.max_rounds,
           embedding_model=args.embedding_model.resolve() if args.embedding_model else None,
           embedding_weight=args.embedding_weight,
           no_structure_expand=True if args.no_structure_expand else None,
           checkpoint_from=args.checkpoint_from.resolve() if args.checkpoint_from else None)
    invoke("audit_v3.py", **common, input=args.output / "matches_v3.json")
    invoke("reuse_v3.py", **common, input=args.output / "matches_v3_audited.json")
    invoke("scope_audit_v3.py", **common, input=args.output / "matches_v3_final.json")
    invoke("verify_recoded_v3.py", **common, input=args.output / "matches_v3_scope_audited.json")
    invoke("guard_scope_v3.py", document=args.document.resolve(), graph=graph.resolve(),
           source=args.source.resolve(), output=args.output.resolve(),
           input=args.output / "matches_v3_reviewed.json")
    print(f"Report: {args.output / 'report_v3_guarded.html'}")


if __name__ == "__main__":
    main()
