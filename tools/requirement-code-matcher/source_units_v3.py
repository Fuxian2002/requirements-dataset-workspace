"""Source units outside codeComp's function graph for V3 evidence retrieval."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


SKIP = {"tests", "test", "unit-test", "unit_test", "stubs", "mocks", "third_party", "third-party",
        ".git", ".venv", "__pycache__", "build"}
SYMBOL = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Za-z0-9_]{3,}(?![A-Za-z0-9_])")


def _unit(root: Path, path: Path, start: int, end: int, kind: str, name: str,
          lines: list[str]) -> dict[str, Any]:
    rel = path.relative_to(root).as_posix()
    excerpt = "\n".join(lines[start - 1:end])
    return {"id": f"{kind}:{rel}:{start}", "name": name, "file": rel,
            "line_start": start, "line_end": end, "kind": kind,
            "summary": (name + " " + excerpt[:650]).strip(),
            "conditions": [], "code_excerpt": excerpt,
            "callers": [], "callees": []}


class SourceUnits:
    def __init__(self, root: Path):
        self.root = root
        self.units: list[dict[str, Any]] = []
        self.by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.references: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._scan()
        for units in self.by_symbol.values():
            units.sort(key=lambda unit: (len(Path(unit["file"]).parts), unit["file"],
                                         unit["line_start"]))

    def _add(self, unit: dict[str, Any], symbols: set[str] | None = None) -> None:
        self.units.append(unit)
        for name in symbols or set(SYMBOL.findall(unit["name"])):
            self.by_symbol[name].append(unit)
        for name in set(SYMBOL.findall(unit["code_excerpt"])):
            self.references[name].append(unit)

    def _scan(self) -> None:
        has_src = (self.root / "src").is_dir()
        for path in sorted(self.root.rglob("*.h")):
            rel = path.relative_to(self.root)
            if any(part.lower() in SKIP for part in rel.parts):
                continue
            if has_src and rel.parts[0] not in {"src", "conf"}:
                continue
            if not has_src and "Tools" in rel.parts:
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for number, line in enumerate(lines, 1):
                matched = re.match(r"\s*#\s*define\s+([A-Z][A-Za-z0-9_]+)\b", line)
                if matched:
                    name = matched.group(1)
                    end = number
                    while end < len(lines) and lines[end - 1].rstrip().endswith("\\") and end - number < 5:
                        end += 1
                    self._add(_unit(self.root, path, number, end, "macro", name, lines), {name})
            # Small typedef structs are direct evidence for fields that are absent/present.
            for match in re.finditer(r"typedef\s+struct(?:\s+\w+)?\s*\{", "\n".join(lines)):
                start = "\n".join(lines)[:match.start()].count("\n") + 1
                end = next((i for i in range(start + 1, min(start + 85, len(lines)) + 1)
                            if re.search(r"}\s*[A-Za-z_]\w*\s*;", lines[i - 1])), None)
                if end:
                    alias = re.search(r"}\s*([A-Za-z_]\w*)\s*;", lines[end - 1])
                    self._add(_unit(self.root, path, start, end, "struct",
                                    alias.group(1) if alias else path.stem, lines),
                              {alias.group(1)} if alias else set())

        # CAN callbacks and other drivers often define bit positions locally
        # in .c files. Index those definitions as citable units too.
        c_roots = [self.root / "src"] if has_src else [self.root]
        for path in sorted(p for c_root in c_roots for p in c_root.rglob("*.c")):
            rel = path.relative_to(self.root)
            if any(part.lower() in SKIP for part in rel.parts):
                continue
            if not has_src and "Tools" in rel.parts:
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for number, line in enumerate(lines, 1):
                # codeComp may omit whole conditionally compiled modules. Keep
                # their function bodies searchable, including lowercase names
                # and public entry points (preflight, console, MAVMission, etc.).
                function = re.match(
                    r"\s*(?:(?:static|inline|extern)\s+)*"
                    r"[A-Za-z_]\w*(?:\s+|\s*\*\s*)"
                    r"([A-Za-z_]\w*)\s*\([^;]*\)\s*(?:\{|$)", line)
                if function:
                    # Preserve static implementations excluded by the active
                    # preprocessor configuration; prototypes end in ';'.
                    following = "\n".join(lines[number - 1:min(len(lines), number + 16)])
                    brace = following.find("{")
                    semicolon = following.find(";")
                    if brace >= 0 and (semicolon < 0 or brace < semicolon):
                        opened = number - 1 + following[:brace].count("\n")
                        depth = 0
                        for end_index in range(opened, min(len(lines), opened + 240)):
                            depth += lines[end_index].count("{") - lines[end_index].count("}")
                            if depth == 0 and end_index > opened:
                                self._add(_unit(self.root, path, number, end_index + 1,
                                                "source_function", function.group(1), lines),
                                          {function.group(1)})
                                break
                matched = re.match(r"\s*#\s*define\s+([A-Z][A-Za-z0-9_]+)\b", line)
                if not matched:
                    continue
                end = number
                while end < len(lines) and lines[end - 1].rstrip().endswith("\\") and end - number < 5:
                    end += 1
                name = matched.group(1)
                self._add(_unit(self.root, path, number, end, "macro", name, lines), {name})

        config_root = self.root / "conf" / "bms"
        if config_root.is_dir():
            for path in sorted(config_root.glob("*.json")):
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                # Each named value or diagnosis entry becomes a compact citable unit.
                for number, line in enumerate(lines, 1):
                    match = re.search(r'"(?:name|event)"\s*:\s*"([A-Za-z][A-Za-z0-9_]*)"', line)
                    if not match:
                        continue
                    name = match.group(1)
                    end = min(len(lines), number + (8 if '"event"' in line else 4))
                    self._add(_unit(self.root, path, max(1, number - 1), end,
                                    "config", name, lines), {name})

        # C configuration initializers and the build generator contain behaviour
        # absent from function-level graphs. Index bounded source windows.
        paths = list((self.root / "src").rglob("*_cfg.c"))
        paths += [p for p in (self.root / "src").rglob("*_cfg.h")
                  if "config" in p.relative_to(self.root).parts]
        paths += list((self.root / "tools" / "waf_tools").glob("*config*.py"))
        for path in sorted(paths):
            rel = path.relative_to(self.root)
            if any(part.lower() in SKIP for part in rel.parts):
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            if path.suffix == ".py":
                for number, line in enumerate(lines, 1):
                    default = re.match(r"\s*([a-z][a-z0-9_]+)\s*:\s*\w+\s*=\s*(?:False|True)\b", line)
                    if default:
                        self._add(_unit(self.root, path, max(1, number - 2),
                                        min(len(lines), number + 2), "default_config",
                                        default.group(1), lines), {default.group(1)})
            for start in range(1, len(lines) + 1, 35):
                end = min(len(lines), start + 39)
                excerpt = "\n".join(lines[start - 1:end])
                names = set(SYMBOL.findall(excerpt))
                if not names:
                    continue
                name = f"{path.stem} {start}-{end} " + " ".join(sorted(names)[:6])
                self._add(_unit(self.root, path, start, end, "source", name, lines), names)

        # Repositories such as MatrixPilot have no src/conf layout. Their
        # simulator, desktop utilities, IDE projects and generators are still
        # executable/configuration evidence, so index bounded source windows.
        if not (self.root / "src").is_dir():
            extensions = {".py", ".pyw", ".cs", ".xml", ".mcp", ".csproj",
                          ".vcxproj", ".c", ".h", ".cpp", ".hpp", ".mk"}
            for path in sorted(self.root.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in extensions:
                    continue
                rel = path.relative_to(self.root)
                if any(part.lower() in SKIP for part in rel.parts) or path.stat().st_size > 1_000_000:
                    continue
                if path.suffix.lower() in {".c", ".h", ".cpp", ".hpp"} and "Tools" not in rel.parts:
                    continue  # Main C/C++ functions are already in codeComp.
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                for start in range(1, len(lines) + 1, 45):
                    end = min(len(lines), start + 59)
                    excerpt = "\n".join(lines[start - 1:end])
                    names = set(SYMBOL.findall(excerpt))
                    name = f"{rel.as_posix()} {start}-{end} " + " ".join(sorted(names)[:8])
                    self._add(_unit(self.root, path, start, end,
                                    "auxiliary_source", name, lines), names)

    def expand_symbols(self, text: str, limit: int = 18) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        seen = set()
        names = set(SYMBOL.findall(text))
        for _ in range(3):
            for symbol in sorted(names):
                for unit in self.by_symbol.get(symbol, [])[:3]:
                    if unit["id"] not in seen:
                        found.append(unit)
                        seen.add(unit["id"])
            if len(found) >= limit:
                break
            expanded = set(names)
            for unit in found:
                expanded.update(SYMBOL.findall(unit["code_excerpt"]))
            if expanded == names:
                break
            names = expanded
        return found[:limit]
