"""Create a relocatable source bundle with an allowlist and file hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent
NAME = "requirements-code-matcher-v3"
ROOT_FILES = (
    "run_v3_full.py", "main.py", "codecomp_bridge.py", "llm_match.py",
    "candidate_index.py", "semantic_index.py", "structural_candidates.py", "match_v3.py", "review_requirements.py", "source_units_v3.py", "report_v2.py",
    "audit_v3.py", "reuse_v3.py", "scope_audit_v3.py",
    "verify_recoded_v3.py", "guard_scope_v3.py", "requirements.txt",
    "model.env.example", "install.ps1", "install.sh", "install_embedding.ps1",
    "requirements-embedding.txt", "PORTABLE_README.md",
)
CODECOMP_FILES = (
    "codecomp/tools/extract_evidence.py", "codecomp/tools/llm_enrich.py",
    "codecomp/tools/static_evidence_core/__init__.py",
    "codecomp/tools/static_evidence_core/ast_access.py",
    "codecomp/tools/static_evidence_core/clang_config.py",
    "codecomp/tools/static_evidence_core/text.py",
    "codecomp/tools/static_evidence_core/vs_compile_database.py",
    "codecomp/tools/prompts/description_system.md",
    "codecomp/tools/prompts/group_summary_system.md",
)
TEST_FILES = ("tests/test_pipeline.py", "tests/test_match_v3.py", "tests/test_report_v2.py",
              "tests/test_review_requirements.py", "tests/test_semantic_index.py",
              "tests/test_structural_candidates.py")


def main() -> None:
    selected = sorted(set(ROOT_FILES + CODECOMP_FILES + TEST_FILES))
    missing = [name for name in selected if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("Missing release files: " + ", ".join(missing))
    files = {name: (ROOT / name).read_bytes() for name in selected}
    forbidden = ("D:\\数据集构建".encode("utf-8"), b"C:\\Users\\10590")
    for name, data in files.items():
        if any(marker in data for marker in forbidden):
            raise SystemExit(f"Local workspace path found in release file: {name}")
    manifest = {"name": NAME, "format": 1,
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
                "requirements": "Python 3.10+; install requirements.txt; configure model.env"}
    files["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output = ROOT / "dist" / f"{NAME}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(f"{NAME}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o755 if name.endswith(".sh") else 0o644) << 16
            archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    print(f"{output} ({output.stat().st_size} bytes, {len(files)} files)")


if __name__ == "__main__":
    main()
