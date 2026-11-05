"""Text decoding helpers shared by extraction and enrichment."""

from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    """Read source and JSON files using the project encoding fallback order."""
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "gb18030", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")
