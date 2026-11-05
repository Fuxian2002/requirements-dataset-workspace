"""Export libclang-compatible compile commands from legacy VCXPROJ files."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional


MSBUILD_VARIABLE = re.compile(r"\$\([^)]*\)|%\([^)]*\)")
INCLUDED_SOURCE = re.compile(r'^\s*#\s*include\s+"(?P<path>[^"]+\.(?:c|cc|cpp|cxx))"', re.M | re.I)


def project_configuration(project: Path) -> tuple[str, str]:
    try:
        root = ET.parse(project).getroot()
    except (ET.ParseError, OSError):
        return "Debug", "Win32"
    for element in root.iter():
        if element.tag.endswith("ProjectConfiguration"):
            value = element.attrib.get("Include", "")
            if "|" in value:
                return tuple(value.split("|", 1))
    return "Debug", "Win32"


def split_msbuild_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip() and not MSBUILD_VARIABLE.search(item)]


def matching_clcompile(root: ET.Element, configuration: str, platform: str) -> Optional[ET.Element]:
    marker = f"'{configuration}|{platform}'"
    for group in root.iter():
        if not group.tag.endswith("ItemDefinitionGroup") or marker not in group.attrib.get("Condition", ""):
            continue
        for child in group:
            if child.tag.endswith("ClCompile"):
                return child
    return None


def element_text(element: Optional[ET.Element], suffix: str) -> str:
    if element is None:
        return ""
    for child in element:
        if child.tag.endswith(suffix):
            return child.text or ""
    return ""


def project_sources(project: Path, root: ET.Element) -> list[Path]:
    sources = []
    for element in root.iter():
        if element.tag.endswith("ClCompile") and "Include" in element.attrib:
            source = (project.parent / element.attrib["Include"]).resolve()
            if source.is_file():
                sources.append(source)
    return sorted(set(sources))


def included_c_sources(sources: list[Path]) -> list[Path]:
    included = set()
    pending = list(sources)
    scanned = set()
    while pending:
        source = pending.pop()
        if source in scanned:
            continue
        scanned.add(source)
        try:
            text = source.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in INCLUDED_SOURCE.finditer(text):
            candidate = (source.parent / match.group("path")).resolve()
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() == ".c":
                included.add(candidate)
            else:
                pending.append(candidate)
    return sorted(included)


def export_vcxproj_database(project: Path, output: Path) -> dict:
    """Export a selected VCXPROJ configuration as compile_commands.json.

    The project is assumed to have been built by MSBuild already. Arguments are
    expressed in Clang form so libclang can consume the actual MSBuild macros
    and include paths. C files textually included by project C++ adapters are
    added as C translation units with the adapter's build configuration.
    """
    project = project.resolve()
    root = ET.parse(project).getroot()
    configuration, platform = project_configuration(project)
    clcompile = matching_clcompile(root, configuration, platform)
    include_dirs = [str((project.parent / item).resolve()) for item in split_msbuild_list(element_text(clcompile, "AdditionalIncludeDirectories"))]
    definitions = split_msbuild_list(element_text(clcompile, "PreprocessorDefinitions"))
    sources = project_sources(project, root)
    sources.extend(included_c_sources(sources))
    sources = sorted(set(sources))

    entries = []
    for source in sources:
        language = "c" if source.suffix.lower() == ".c" else "c++"
        arguments = ["clang", "-x", language]
        arguments.extend(f"-D{definition}" for definition in definitions)
        for include_dir in include_dirs:
            arguments.extend(["-I", include_dir])
        arguments.extend(["-c", str(source)])
        entries.append(
            {
                "directory": str(project.parent),
                "file": str(source),
                "arguments": arguments,
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "configuration": configuration,
        "platform": platform,
        "entries": len(entries),
        "output": str(output),
    }
