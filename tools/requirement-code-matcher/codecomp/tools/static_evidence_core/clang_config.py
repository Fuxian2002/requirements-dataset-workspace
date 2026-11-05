"""Optional compilation-database support for libclang parsing."""

from __future__ import annotations

import glob
import json
import re
import shlex
import shutil
import subprocess
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .text import read_text
from .vs_compile_database import export_vcxproj_database, project_configuration


CompilationDatabase = Dict[Path, List[str]]


@dataclass(frozen=True)
class BuildEvidence:
    kind: str
    path: Path


def find_tool(source_root: Path, name: str) -> Optional[str]:
    """Prefer a workspace-local tool bundle before the system PATH."""
    executable = f"{name}.exe" if os.name == "nt" else name
    tool_roots = [Path(__file__).resolve().parents[1] / ".tools"]
    tool_roots.extend(parent / ".tools" for parent in (source_root, *source_root.parents))
    for tools_root in tool_roots:
        if not tools_root.is_dir():
            continue
        for candidate in tools_root.rglob(executable):
            return str(candidate)
    return shutil.which(name)


def find_msbuild() -> Optional[str]:
    """Locate MSBuild even when a legacy Visual Studio install is off PATH."""
    found = shutil.which("msbuild")
    if found:
        return found
    windows = Path(os.environ.get("WINDIR", r"C:\Windows"))
    for candidate in (
        windows / "Microsoft.NET" / "Framework" / "v4.0.30319" / "MSBuild.exe",
        windows / "Microsoft.NET" / "Framework64" / "v4.0.30319" / "MSBuild.exe",
        Path(r"C:\Program Files (x86)\MSBuild\4.0\Bin\MSBuild.exe"),
    ):
        if candidate.is_file():
            return str(candidate)
    return None


def discover_build_evidence(source_root: Path) -> List[BuildEvidence]:
    """Find build-system files that can provide real compiler arguments."""
    evidence = []
    database = find_compilation_database(source_root)
    if database:
        evidence.append(BuildEvidence("compile_commands", database))
    for name, kind in (
        ("CMakeLists.txt", "cmake"),
        ("CMakePresets.json", "cmake"),
        ("Makefile", "make"),
        ("makefile", "make"),
    ):
        path = source_root / name
        if path.is_file():
            evidence.append(BuildEvidence(kind, path))
    for pattern, kind in (("*.sln", "visual_studio"), ("*.vcxproj", "visual_studio")):
        for path in sorted(source_root.rglob(pattern)):
            evidence.append(BuildEvidence(kind, path))
    return evidence


def prepare_compilation_database(source_root: Path) -> Tuple[Optional[Path], List[str]]:
    """Build a real database from a recognized local build system when safe.

    Existing databases are always preferred. CMake is configured and built only
    when a CMake project exists at the requested source root. Make projects
    require Bear to capture their real compiler commands. Visual Studio projects
    are rebuilt through MSBuild and exported from their selected VCXPROJ
    configuration.
    """
    existing = find_compilation_database(source_root)
    if existing:
        return existing, [f"using existing compilation database: {existing}"]

    evidence = discover_build_evidence(source_root)
    messages = [f"found {item.kind} evidence: {item.path}" for item in evidence]
    cmake_file = source_root / "CMakeLists.txt"
    if cmake_file.is_file():
        cmake = find_tool(source_root, "cmake")
        if cmake is None:
            messages.append("CMake project detected, but cmake is not installed")
            return None, messages
        build_dir = source_root / ".static-evidence-build"
        command = [
            cmake,
            "-S",
            str(source_root),
            "-B",
            str(build_dir),
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
        ]
        ninja = find_tool(source_root, "ninja")
        if ninja:
            command.extend(["-G", "Ninja", f"-DCMAKE_MAKE_PROGRAM={ninja}"])
        try:
            subprocess.run(command, check=True)
            subprocess.run([cmake, "--build", str(build_dir)], check=True)
        except subprocess.CalledProcessError as exc:
            messages.append(f"CMake build failed: {exc}")
            return None, messages
        database = build_dir / "compile_commands.json"
        if database.is_file():
            messages.append(f"generated compilation database: {database}")
            return database.resolve(), messages
        messages.append("CMake build completed without compile_commands.json")
        return None, messages

    if (source_root / "Makefile").is_file() or (source_root / "makefile").is_file():
        bear = find_tool(source_root, "bear")
        if bear is None:
            messages.append("Make project detected, but Bear is not installed")
            return None, messages
        make = find_tool(source_root, "make")
        if make is None:
            messages.append("Make project detected, but make is not installed")
            return None, messages
        database = source_root / "compile_commands.json"
        try:
            subprocess.run([bear, "--output", str(database), "--", make], cwd=source_root, check=True)
        except subprocess.CalledProcessError as exc:
            messages.append(f"Bear capture failed: {exc}")
            return None, messages
        if database.is_file():
            messages.append(f"captured compilation database: {database}")
            return database.resolve(), messages

    if any(item.kind == "visual_studio" for item in evidence):
        msbuild = find_msbuild()
        if msbuild:
            messages.append(f"Visual Studio project and MSBuild detected: {msbuild}")
            project = next((item.path for item in evidence if item.path.suffix.lower() == ".vcxproj"), None)
            if project is not None:
                configuration, platform = project_configuration(project)
                try:
                    subprocess.run(
                        [
                            msbuild,
                            str(project),
                            "/t:Rebuild",
                            f"/p:Configuration={configuration};Platform={platform}",
                            "/nologo",
                            "/v:minimal",
                        ],
                        check=True,
                    )
                    messages.append(f"MSBuild rebuild succeeded: {project} ({configuration}|{platform})")
                    database = source_root / "compile_commands.json"
                    exported = export_vcxproj_database(project, database)
                    messages.append(
                        f"exported {exported['entries']} compile commands: {database}"
                    )
                    return database.resolve(), messages
                except (OSError, ValueError) as exc:
                    messages.append(f"Visual Studio compile-command export failed: {exc}")
                except subprocess.CalledProcessError as exc:
                    messages.append(f"MSBuild rebuild failed: {exc}")
        else:
            messages.append("Visual Studio project detected, but MSBuild was not found")
        messages.append("Visual Studio compilation-database export was not completed")
    if not messages:
        messages.append("no supported build-system evidence found")
    return None, messages


def discover_include_directories(source_root: Path) -> List[str]:
    """Return include directories usable as libclang ``-I`` flags.

    Without ``compile_commands.json`` the extractor only knows the source
    root and ``root/iplib``, so struct definitions in conventional header
    locations stay incomplete and member-level parameter extraction silently
    produces nothing.  Add the conventional header directories plus any ``-I``
    flags a Makefile declares, so types resolve even without a compilation
    database.  A compilation database remains authoritative when present.
    """
    candidates: List[Path] = [source_root]
    for name in ("include", "inc", "src"):
        candidates.append(source_root / name)
    for makefile_name in ("Makefile", "makefile"):
        makefile = source_root / makefile_name
        if not makefile.is_file():
            continue
        for line in read_text(makefile).splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            for match in re.finditer(r"-I\s*([^\s;]+)", line):
                value = match.group(1)
                if value.startswith("$") or value.startswith("("):
                    # Variable references such as $(INCLUDE_DIR) are not
                    # resolvable here; skip them instead of guessing.
                    continue
                path = Path(value)
                if not path.is_absolute():
                    path = source_root / path
                candidates.append(path)
    resolved: List[str] = []
    for path in candidates:
        absolute = path.resolve()
        if absolute.is_dir() and str(absolute) not in resolved:
            resolved.append(str(absolute))
    return resolved


def discover_missing_header_directories(
    source_root: Path, include_strings: List[str]
) -> List[str]:
    """Derive include directories that resolve the given include strings.

    Called only when the conventional/Makefile include search still failed to
    resolve a header (e.g. the include folder was renamed and the Makefile
    references it only through a variable such as ``-I$(INCLUDE_DIR)``).  For
    each unresolved include string such as ``fsw/data_bus.h``, glob the source
    tree for its basename; a file whose path ends in the full include string
    resolves it from the directory obtained by stripping that path.  This
    keeps struct types from silently degrading to incomplete types when
    headers live in an unconventional location.
    """
    resolved: List[str] = []
    for include_string in include_strings:
        normalized = include_string.replace("\\", "/").lstrip("./")
        components = [part for part in normalized.split("/") if part]
        if not components or ".." in components:
            continue
        basename = components[-1]
        for file_path in source_root.rglob(glob.escape(basename)):
            if not file_path.is_file():
                continue
            file_parts = list(file_path.parts)
            if len(file_parts) < len(components):
                continue
            tail = file_parts[-len(components) :]
            if [part.lower() for part in tail] != [
                part.lower() for part in components
            ]:
                continue
            directory = Path(*file_parts[: len(file_parts) - len(components)])
            if not directory.is_dir():
                continue
            absolute = str(directory.resolve())
            if absolute not in resolved:
                resolved.append(absolute)
    return resolved


def find_compilation_database(source_root: Path) -> Optional[Path]:
    """Find an existing standard compilation database without generating one."""
    candidates = (
        source_root / "compile_commands.json",
        source_root / "build" / "compile_commands.json",
        source_root.parent / "build" / "compile_commands.json",
    )
    return next((path.resolve() for path in candidates if path.is_file()), None)


def load_compilation_database(path: Path) -> CompilationDatabase:
    """Load `compile_commands.json` and index normalized arguments by source."""
    raw_entries = json.loads(read_text(path))
    if not isinstance(raw_entries, list):
        raise ValueError("compile_commands.json must contain an array")

    database: CompilationDatabase = {}
    for entry in raw_entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            continue
        directory = Path(entry.get("directory") or path.parent)
        source = Path(entry["file"])
        if not source.is_absolute():
            source = directory / source
        arguments = entry.get("arguments")
        if not isinstance(arguments, list):
            command = entry.get("command")
            if not isinstance(command, str):
                continue
            arguments = shlex.split(command, posix=False)
        database[source.resolve()] = normalize_compile_arguments(
            [str(argument) for argument in arguments],
            directory.resolve(),
            source.resolve(),
        )
    return database


def normalize_compile_arguments(
    arguments: List[str], directory: Path, source: Path
) -> List[str]:
    """Remove compiler/output arguments and resolve paths for libclang."""
    normalized: List[str] = []
    index = 1
    path_options = {"-I", "/I", "-isystem", "-include", "-iquote"}
    skip_value_options = {"-o", "-MF", "-MT", "-MQ"}
    while index < len(arguments):
        argument = arguments[index]
        if argument in {"-c", "/c"}:
            index += 1
            continue
        if argument in skip_value_options:
            index += 2
            continue
        candidate = Path(argument)
        if argument == str(source) or (
            not candidate.is_absolute() and (directory / candidate).resolve() == source
        ):
            index += 1
            continue
        if argument in path_options and index + 1 < len(arguments):
            value = Path(arguments[index + 1])
            normalized.extend([argument, str((directory / value).resolve()) if not value.is_absolute() else str(value)])
            index += 2
            continue
        if argument.startswith("-I") and len(argument) > 2:
            value = Path(argument[2:])
            normalized.append("-I" + str((directory / value).resolve()) if not value.is_absolute() else argument)
            index += 1
            continue
        normalized.append(argument)
        index += 1
    return normalized
