#!/usr/bin/env python3
"""Extract direct, function-local static evidence from a C source project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from static_evidence_core.ast_access import (
    call_site_arguments,
    pointer_parameter_writes,
)
from static_evidence_core.clang_config import (
    CompilationDatabase,
    discover_build_evidence,
    discover_include_directories,
    discover_missing_header_directories,
    find_compilation_database,
    load_compilation_database,
    prepare_compilation_database,
)
from static_evidence_core.text import read_text


# Optional user configuration. Keep this empty when one workspace contains
# multiple repositories; then --root/--code-dir is required for every run.
CODE_DIR = ""
REPO_LABEL = None  # None = auto-detect from CODE_DIR basename.


C_KEYWORDS = {
    "if",
    "for",
    "while",
    "switch",
    "return",
    "sizeof",
    "case",
    "break",
    "continue",
    "do",
    "else",
}


GENERATED_BUILD_DIRECTORIES = {
    ".static-evidence-build",
    "build",
    "CMakeFiles",
}


CALL_IGNORE = C_KEYWORDS | {
    "IPCALL",
    "IPCREATE",
    "NULL_STATEMENT",
    "fun",
}


# Words that can only be part of a parameter type, never the parameter name.
# Used to reject the last identifier of a declaration when it is a type token
# (an unnamed parameter or a function pointer such as ``int (*fn)(void)``).
PARAM_NAME_SKIP_TOKENS = C_KEYWORDS | {
    "void", "char", "int", "float", "double", "long", "short", "signed",
    "unsigned", "const", "volatile", "restrict", "static", "extern",
    "struct", "enum", "union",
}


# Clang reports an unresolvable #include as ``'fsw/data_bus.h' file not found``.
# Capturing the include string lets the extractor locate the header on disk and
# derive the include directory that would resolve it (see
# discover_missing_header_directories), instead of silently leaving the
# included structs as incomplete types with no member-level extraction.
_MISSING_HEADER_PATTERN = re.compile(
    r"['\"]([^'\"]+\.h)['\"]\s+file not found", re.IGNORECASE
)


def missing_header_strings(translation_unit) -> List[str]:
    """Include strings (e.g. ``fsw/data_bus.h``) libclang could not resolve."""
    include_strings: List[str] = []
    for diag in translation_unit.diagnostics:
        match = _MISSING_HEADER_PATTERN.search(diag.spelling or "")
        if not match:
            continue
        include_string = match.group(1).replace("\\", "/")
        if include_string not in include_strings:
            include_strings.append(include_string)
    return include_strings


ROLE_MARKERS = [
    ("input", ("输入端口", "输入变量", "Input")),
    ("output", ("输出端口", "输出变量", "Output")),
    ("inout", ("输入输出端口", "输入输出变量", "I/O")),
    ("state", ("状态变量", "状态")),
    ("parameter", ("参数变量", "参数")),
    ("interface", ("接口函数", "接口")),
]


@dataclass
class FieldEvidence:
    name: str
    type: str
    comment: str = ""
    role: str = ""


@dataclass
class StructEvidence:
    name: str
    tag: str
    file: str
    start_line: int
    end_line: int
    comment: str = ""
    fields: List[FieldEvidence] = field(default_factory=list)


@dataclass
class FunctionEvidence:
    name: str
    signature: str
    file: str
    start_line: int
    end_line: int
    code: str
    leading_comment: str = ""
    ast_callees: List[str] = field(default_factory=list)
    ast_macro_calls: List[dict] = field(default_factory=list)
    ast_parameter_writes: List[str] = field(default_factory=list)
    ast_member_accesses: List[dict] = field(default_factory=list)
    ast_ipcalls: List[dict] = field(default_factory=list)
    ast_global_accesses: List[dict] = field(default_factory=list)
    ast_call_arguments: List[dict] = field(default_factory=list)
    parser: str = "fallback"


@dataclass
class FunctionCallOccurrence:
    caller: str
    callee: str
    line: int
    order: int
    statement: str
    condition: str = ""
    branch: str = ""
    selection_group: str = ""


def decode_bytes(data: bytes) -> str:
    for encoding in ("utf-8-sig", "gb18030", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def rel_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        # Fallback: path is not under root (e.g. cross-drive on Windows,
        # or a libclang diagnostic points to a system header outside the
        # source tree). Return the absolute POSIX-style path instead.
        return path.resolve().as_posix()


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def offset_of_line(text: str, line: int) -> int:
    if line <= 1:
        return 0
    offset = 0
    for _ in range(line - 1):
        next_newline = text.find("\n", offset)
        if next_newline < 0:
            return len(text)
        offset = next_newline + 1
    return offset


def strip_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)


def strip_comments_preserving_lines(text: str) -> str:
    """Remove comments without changing offsets used for source line evidence."""
    def replace(match: re.Match) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group(0))

    return re.sub(r"/\*.*?\*/|//[^\n]*", replace, text, flags=re.S)


def clean_comment(comment: str) -> str:
    comment = comment.strip()
    comment = re.sub(r"^/\*+", "", comment)
    comment = re.sub(r"\*/$", "", comment)
    comment = re.sub(r"^\s*//", "", comment, flags=re.M)
    lines = []
    for line in comment.splitlines():
        line = re.sub(r"^\s*\* ?", "", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines).strip()


def comment_before(text: str, offset: int, max_gap_lines: int = 3) -> str:
    """Return only the contiguous comment block immediately above an item.

    Stop as soon as code is encountered while walking upward. In particular,
    comments belonging to a preceding function must not be carried into the
    next function's evidence.
    """
    comment_pattern = re.compile(r"/\*.*?\*/|//[^\r\n]*", re.S)
    comments = list(comment_pattern.finditer(text, 0, offset))
    cursor = offset

    while cursor > 0 and text[cursor - 1].isspace():
        cursor -= 1
    gap_lines = text[cursor:offset].count("\n")
    if gap_lines > max_gap_lines:
        return ""

    contiguous_comments = []
    for match in reversed(comments):
        if match.end() != cursor:
            break
        contiguous_comments.append(match.group(0))
        cursor = match.start()
        while cursor > 0 and text[cursor - 1].isspace():
            cursor -= 1

    return clean_comment("\n".join(reversed(contiguous_comments)))


def matching_brace(text: str, open_index: int) -> int:
    depth = 0
    i = open_index
    in_string: Optional[str] = None
    in_line_comment = False
    in_block_comment = False
    escaped = False

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue
        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue
        if ch in ("'", '"'):
            in_string = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def iter_c_files(root: Path) -> Iterable[Path]:
    for suffix in ("*.c", "*.h"):
        yield from (
            path
            for path in sorted(root.rglob(suffix))
            if not is_generated_build_path(path, root)
        )


def iter_translation_units(root: Path) -> Iterable[Path]:
    yield from (
        path
        for path in sorted(root.rglob("*.c"))
        if not is_generated_build_path(path, root)
    )


def is_generated_build_path(path: Path, root: Path) -> bool:
    """Exclude CMake/build outputs from the source-evidence traversal."""
    try:
        parts = path.resolve().relative_to(root.resolve()).parts
    except ValueError:
        return False
    return any(part in GENERATED_BUILD_DIRECTORIES for part in parts)


def extract_functions(path: Path, root: Path) -> List[FunctionEvidence]:
    text = read_text(path)
    candidates: List[FunctionEvidence] = []
    pattern = re.compile(
        r"^[ \t]*(?P<sig>(?:(?:static|extern|inline|const|volatile|unsigned|signed|long|short|struct|enum|union)\s+)*"
        r"(?:[A-Za-z_]\w*\s+)+[*\s]*(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\))\s*\{",
        re.M,
    )
    for match in pattern.finditer(text):
        name = match.group("name")
        if name in C_KEYWORDS:
            continue
        original_open = text.find("{", match.end() - 1)
        original_close = matching_brace(text, original_open)
        if original_open < 0 or original_close < 0:
            continue
        start = match.start("sig")
        while start < len(text) and text[start].isspace():
            start += 1
        end = original_close + 1
        signature = text[start:original_open].strip()
        candidates.append(
            FunctionEvidence(
                name=name,
                signature=" ".join(signature.split()),
                file=rel_path(path, root),
                start_line=line_of_offset(text, start),
                end_line=line_of_offset(text, end),
                code=text[start:end],
                leading_comment=comment_before(text, start),
            )
        )
    return candidates


def import_clang():
    vendor_root = Path(__file__).resolve().parent / ".vendor"
    if vendor_root.is_dir() and str(vendor_root) not in sys.path:
        sys.path.insert(0, str(vendor_root))
    try:
        from clang import cindex  # type: ignore
        # Disable strict compatibility check so that missing C++ method
        # introspection functions (e.g. clang_CXXMethod_isDeleted) are
        # skipped with a warning instead of crashing the extraction.
        cindex.Config.compatibility_check = False
    except Exception as exc:  # pragma: no cover - depends on local environment
        return None, exc
    return cindex, None


def same_file(cursor_file, path: Path) -> bool:
    if cursor_file is None:
        return False
    try:
        return Path(str(cursor_file)).resolve() == path.resolve()
    except OSError:
        return False


def walk_cursor(cursor):
    yield cursor
    for child in cursor.get_children():
        yield from walk_cursor(child)


def clang_call_name(cursor) -> str:
    referenced = getattr(cursor, "referenced", None)
    if referenced is not None and getattr(referenced, "spelling", ""):
        return referenced.spelling
    for child in cursor.get_children():
        referenced = getattr(child, "referenced", None)
        if referenced is not None and getattr(referenced, "spelling", ""):
            return referenced.spelling
        if getattr(child, "spelling", ""):
            return child.spelling
    return cursor.spelling or cursor.displayname or ""


def clang_function_signature(cursor) -> str:
    result_type = getattr(cursor.result_type, "spelling", "") or ""
    args = []
    for arg in cursor.get_arguments():
        arg_type = getattr(arg.type, "spelling", "")
        arg_name = arg.spelling
        args.append(f"{arg_type} {arg_name}".strip())
    prefix = ""
    try:
        if str(cursor.storage_class).endswith(".STATIC"):
            prefix = "static "
    except Exception:
        prefix = ""
    return f"{prefix}{result_type} {cursor.spelling}({', '.join(args)})".strip()


def extract_functions_libclang(
    root: Path,
    verbose: bool = False,
    compilation_database: Optional[CompilationDatabase] = None,
) -> Tuple[List[FunctionEvidence], List[dict], Optional[str]]:
    cindex, import_error = import_clang()
    if cindex is None:
        return [], [], f"clang.cindex import failed: {import_error}"

    functions: List[FunctionEvidence] = []
    diagnostics: List[dict] = []
    index = cindex.Index.create()
    clang_args = [
        "-x",
        "c",
        "-std=c99",
        f"-I{root}",
        f"-I{root / 'iplib'}",
    ]
    if compilation_database is None:
        # Without compile_commands.json the struct definitions a project
        # keeps under include/ (see Makefile -I flags) would stay incomplete
        # types, and member-level parameter extraction would silently produce
        # nothing.  Discover conventional and Makefile-declared include dirs.
        for include_dir in discover_include_directories(root):
            clang_args.append(f"-I{include_dir}")

    def parse_translation_unit(path: Path, parse_args: List[str]):
        """Parse one translation unit; return (tu, its collected diagnostics)."""
        try:
            # Keep macro invocations as preprocessor cursors.  IPCALL is a
            # macro, so it is otherwise represented only as an indirect .fun
            # call and its instance argument is lost.
            tu = index.parse(
                str(path), args=parse_args,
                options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
            )
        except Exception as exc:
            return None, [
                {
                    "file": rel_path(path, root),
                    "severity": "fatal",
                    "message": f"parse failed: {exc}",
                }
            ]
        collected = []
        for diag in tu.diagnostics:
            diag_file = str(diag.location.file) if diag.location.file else ""
            collected.append(
                {
                    "file": rel_path(Path(diag_file), root) if diag_file and Path(diag_file).is_absolute() and Path(diag_file).exists() else diag_file,
                    "line": diag.location.line,
                    "column": diag.location.column,
                    "severity": diag.severity,
                    "message": diag.spelling,
                }
            )
        return tu, collected

    include_fallback_exhausted = False
    for path in iter_translation_units(root):
        if verbose:
            print(f"[libclang] parsing {rel_path(path, root)}")
        parse_args = compilation_database.get(path.resolve(), clang_args) if compilation_database else clang_args
        tu, tu_diagnostics = parse_translation_unit(path, parse_args)
        if not include_fallback_exhausted and compilation_database is None and tu is not None:
            # The conventional/Makefile include search failed to resolve a
            # header (e.g. an include folder renamed to an unconventional
            # name).  Locate the missing header on disk, derive the -I
            # directory that would resolve its include string, and reparse so
            # the included structs are not left as incomplete types with no
            # member-level extraction.
            missing = missing_header_strings(tu)
            if not missing:
                # Nothing unresolved on this translation unit; keep the
                # fallback armed in case a later unit needs it.
                pass
            else:
                derived = discover_missing_header_directories(root, missing)
                extra = [f"-I{include_dir}" for include_dir in derived if f"-I{include_dir}" not in clang_args]
                if extra:
                    clang_args.extend(extra)
                    tu, tu_diagnostics = parse_translation_unit(path, parse_args + extra)
                else:
                    # No new directory resolved the missing header; further
                    # globbing would not help any translation unit.
                    include_fallback_exhausted = True
        diagnostics.extend(tu_diagnostics)
        if tu is None:
            continue

        source_bytes = path.read_bytes()
        source_text = read_text(path)
        for cursor in walk_cursor(tu.cursor):
            if cursor.kind != cindex.CursorKind.FUNCTION_DECL or not cursor.is_definition():
                continue
            if not same_file(cursor.location.file, path):
                continue
            start = cursor.extent.start.offset
            end = cursor.extent.end.offset
            if start < 0 or end <= start:
                continue
            code = decode_bytes(source_bytes[start:end])
            signature = code.split("{", 1)[0].strip() if "{" in code else clang_function_signature(cursor)
            callees = []
            macro_calls = []
            member_accesses = []
            global_accesses = []
            ipcalls = []
            for macro in walk_cursor(tu.cursor):
                if macro.kind != cindex.CursorKind.MACRO_INSTANTIATION:
                    continue
                if not same_file(macro.location.file, path):
                    continue
                if not start <= macro.location.offset < end:
                    continue
                tokens = list(macro.get_tokens())
                if macro.spelling not in {"IPCALL", "IPCREATE"} and len(tokens) >= 2 and tokens[1].spelling == "(":
                    macro_calls.append({"name": macro.spelling, "line": macro.location.line})
                if macro.spelling != "IPCALL":
                    continue
                # The preprocessor gives the exact invocation tokens:
                # IPCALL ( concrete_instance ).  Do not infer this from text.
                identifiers = [token.spelling for token in tokens if token.kind.name == "IDENTIFIER"]
                if len(identifiers) == 2:
                    ipcalls.append({
                        "instance": identifiers[1],
                        "line": macro.location.line,
                        "statement": statement_at_line_from_source(source_text, macro.location.line),
                    })
            for child in walk_cursor(cursor):
                if child.kind == cindex.CursorKind.CALL_EXPR:
                    name = clang_call_name(child)
                    # A call expression produced by a function-like macro is
                    # an implementation detail of that macro (Fabsx -> fabs),
                    # not a source-level direct call.
                    macro_expansion = next((item for item in macro_calls if item["line"] == child.location.line), None)
                    if macro_expansion:
                        name = macro_expansion["name"]
                    if name and name not in CALL_IGNORE and name != cursor.spelling:
                        callees.append(name)
                elif child.kind == cindex.CursorKind.MEMBER_REF_EXPR:
                    referenced = child.referenced
                    if not referenced or referenced.kind != cindex.CursorKind.FIELD_DECL:
                        continue
                    member_start = child.extent.start.offset
                    member_end = child.extent.end.offset
                    # Macro argument cursors may have an empty extent even
                    # though their source location still identifies the field.
                    if member_start < 0:
                        continue
                    if member_end <= member_start:
                        member_start = child.location.offset
                        member_end = member_start + len(referenced.spelling)
                    if member_start < 0 or member_end <= member_start:
                        continue
                    via = normalize_snippet(decode_bytes(source_bytes[member_start:member_end]))
                    if not via or "->" not in via and "." not in via:
                        # Macro-argument cursors often point at the field but
                        # have no usable extent. Reconstruct only its AST base
                        # declaration; no source-pattern guessing is involved.
                        bases = [item for item in walk_cursor(child) if item.kind == cindex.CursorKind.DECL_REF_EXPR]
                        if bases:
                            via = f"{bases[0].spelling}->{referenced.spelling}"
                    if not via:
                        continue
                    before = decode_bytes(source_bytes[max(0, member_start - 12):member_start])
                    tail = decode_bytes(source_bytes[member_end:member_end + 80])
                    is_read, is_write = access_mode(tail, before)
                    dereferenced = bool(re.search(r"\*\s*$", before))
                    subscript = re.match(r"\s*(\[[^\]]+\])", tail)
                    pointee_via = via
                    if dereferenced:
                        pointee_via = f"*{via}"
                    elif subscript:
                        pointee_via = f"{via}{subscript.group(1)}"

                    # Pointer-member dereferences and subscripts write storage
                    # reached through the member.  An embedded array subscript
                    # writes the structure's own storage and must not become
                    # an input merely because it uses ``[]``.
                    field_is_pointer = referenced.type.kind.name == "POINTER"
                    through_member_storage = (
                        field_is_pointer
                        and (dereferenced or subscript is not None)
                        and is_write
                    )
                    if through_member_storage:
                        is_read = True
                    base_types = set()
                    global_bases = set()
                    for descendant in walk_cursor(child):
                        if descendant.kind == cindex.CursorKind.DECL_REF_EXPR:
                            spelling = descendant.type.spelling
                            if spelling:
                                base_types.add(spelling)
                            declaration = descendant.referenced
                            parent = declaration.semantic_parent if declaration else None
                            if (
                                declaration
                                and declaration.kind == cindex.CursorKind.VAR_DECL
                                and parent
                                and parent.kind == cindex.CursorKind.TRANSLATION_UNIT
                            ):
                                global_bases.add(declaration.spelling)
                    owner = referenced.semantic_parent.spelling if referenced.semantic_parent else ""
                    member_accesses.append(
                        {
                            "name": referenced.spelling,
                            "owner": owner,
                            "base_types": sorted(base_types),
                            "global_bases": sorted(global_bases),
                            "field_type_kind": referenced.type.kind.name,
                            "offset": member_start,
                            "line": child.location.line,
                            "address_taken": bool(re.search(r"&\s*$", before)),
                            "read_via": via if through_member_storage else pointee_via,
                            "write_via": pointee_via,
                            "read": is_read,
                            "write": is_write,
                        }
                    )
                elif child.kind == cindex.CursorKind.DECL_REF_EXPR:
                    declaration = child.referenced
                    parent = declaration.semantic_parent if declaration else None
                    if not (
                        declaration and declaration.kind == cindex.CursorKind.VAR_DECL
                        and parent and parent.kind == cindex.CursorKind.TRANSLATION_UNIT
                    ):
                        continue
                    access_start = child.extent.start.offset
                    access_end = child.extent.end.offset
                    # Member bases are recorded by MEMBER_REF_EXPR instead of
                    # pretending the complete object is read or written.
                    following = decode_bytes(source_bytes[access_end:access_end + 2]).lstrip()
                    if following.startswith(".") or following.startswith("->"):
                        continue
                    before = decode_bytes(source_bytes[max(0, access_start - 12):access_start])
                    tail = decode_bytes(source_bytes[access_end:access_end + 80])
                    if re.search(r"&\s*$", before):
                        continue
                    is_read, is_write = access_mode(tail, before)
                    global_accesses.append({
                        "name": declaration.spelling,
                        "read": is_read,
                        "write": is_write,
                        "offset": access_start,
                    })
            parameter_writes = sorted(pointer_parameter_writes(cursor, cindex))
            call_arguments = sorted(
                call_site_arguments(cursor, cindex, source_bytes),
                key=lambda item: (item["line"], item["callee"]),
            )
            functions.append(
                FunctionEvidence(
                    name=cursor.spelling,
                    signature=" ".join(signature.split()),
                    file=rel_path(path, root),
                    start_line=cursor.extent.start.line,
                    end_line=cursor.extent.end.line,
                    code=code,
                    leading_comment=comment_before(source_text, offset_of_line(source_text, cursor.extent.start.line)),
                    ast_callees=sorted(set(callees)),
                    ast_macro_calls=macro_calls,
                    ast_parameter_writes=parameter_writes,
                    ast_member_accesses=member_accesses,
                    ast_ipcalls=ipcalls,
                    ast_global_accesses=global_accesses,
                    ast_call_arguments=call_arguments,
                    parser="libclang",
                )
            )

    # If the same function is seen more than once through an unusual include
    # arrangement, keep the first real definition from its owning file.
    deduped: Dict[Tuple[str, str, int], FunctionEvidence] = {}
    for func in functions:
        deduped[(func.file, func.name, func.start_line)] = func
    return list(deduped.values()), diagnostics, None


def extract_inline_comment(line: str) -> str:
    comments = re.findall(r"/\*(.*?)\*/|//(.*)$", line)
    parts = []
    for block, slash in comments:
        parts.append(block or slash)
    return clean_comment("\n".join(parts))


def infer_role(line: str, current_role: str) -> str:
    comments = extract_inline_comment(line)
    probe = f"{line}\n{comments}"
    for role, markers in ROLE_MARKERS:
        if any(marker in probe for marker in markers):
            return role
    return current_role


def parse_field(line: str, current_role: str) -> Optional[FieldEvidence]:
    code = strip_comments(line).strip()
    if not code or not code.endswith(";"):
        return None
    if code.startswith(("typedef ", "#")):
        return None
    code = code[:-1].strip()
    if ":" in code and re.search(r"\bunsigned\b|\bsigned\b|\bint\b", code):
        code = code.split(":", 1)[0].strip()
    declarator = code.split(",")[0].strip()
    match = re.search(r"([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*$", declarator)
    if not match:
        return None
    name = match.group(1)
    type_part = declarator[: match.start(1)].strip()
    if not type_part:
        return None
    return FieldEvidence(
        name=name,
        type=" ".join(type_part.split()),
        comment=extract_inline_comment(line),
        role=current_role,
    )


def extract_structs(path: Path, root: Path) -> List[StructEvidence]:
    text = read_text(path)
    structs: List[StructEvidence] = []
    pattern = re.compile(
        r"typedef\s+struct\s+(?P<tag>[A-Za-z_]\w*)?\s*\{(?P<body>.*?)\}\s*(?P<name>[A-Za-z_]\w*)\s*;",
        re.S,
    )
    for match in pattern.finditer(text):
        body = match.group("body")
        current_role = ""
        fields: List[FieldEvidence] = []
        for line in body.splitlines():
            next_role = infer_role(line, current_role)
            if next_role:
                current_role = next_role
            field_ev = parse_field(line, current_role)
            if field_ev:
                fields.append(field_ev)
        structs.append(
            StructEvidence(
                name=match.group("name"),
                tag=match.group("tag") or "",
                file=rel_path(path, root),
                start_line=line_of_offset(text, match.start()),
                end_line=line_of_offset(text, match.end()),
                comment=comment_before(text, match.start()),
                fields=fields,
            )
        )
    return structs


def split_top_level_args(arg_text: str) -> List[str]:
    args = []
    depth = 0
    start = 0
    for i, ch in enumerate(arg_text):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(arg_text[start:i].strip())
            start = i + 1
    tail = arg_text[start:].strip()
    if tail:
        args.append(tail)
    return args


def extract_ipcreate_instances(text: str, path: Path, root: Path) -> List[dict]:
    instances = []
    pattern = re.compile(r"IPCREATE\s*\((?P<args>.*?)\)\s*;", re.S)
    for match in pattern.finditer(text):
        args = split_top_level_args(match.group("args"))
        if len(args) < 2:
            continue
        struct_name = args[0].strip()
        instance_name = args[1].strip()
        initializer = ", ".join(args[2:]).strip()
        instances.append(
            {
                "name": instance_name,
                "type": struct_name,
                "function": f"{struct_name}Fun",
                "initializer": initializer,
                "file": rel_path(path, root),
                "line": line_of_offset(text, match.start()),
                "kind": "IPCREATE",
            }
        )
    return instances


def extract_initializer_instances(text: str, path: Path, root: Path) -> List[dict]:
    instances = []
    pattern = re.compile(
        r"(?P<type>[A-Za-z_]\w*)\s+(?P<name>[A-Za-z_]\w*)\s*=\s*\{(?P<body>.*?)\}\s*;",
        re.S,
    )
    for match in pattern.finditer(text):
        body = match.group("body")
        fun_match = re.search(r"\.fun\s*=\s*(?P<fun>[A-Za-z_]\w*)", body)
        if not fun_match:
            continue
        instances.append(
            {
                "name": match.group("name"),
                "type": match.group("type"),
                "function": fun_match.group("fun"),
                "initializer": body.strip(),
                "file": rel_path(path, root),
                "line": line_of_offset(text, match.start()),
                "kind": "initializer",
            }
        )
    return instances


def extract_instances(root: Path) -> List[dict]:
    instances = []
    seen = set()
    for path in iter_c_files(root):
        text = read_text(path)
        for item in extract_ipcreate_instances(text, path, root) + extract_initializer_instances(text, path, root):
            key = (item["name"], item["function"], item["file"], item["line"])
            if key in seen:
                continue
            seen.add(key)
            instances.append(item)
    return instances


def extract_instances_libclang(
    root: Path,
    known_structs: Iterable[str],
    function_names: Iterable[str],
    compilation_database: Optional[CompilationDatabase] = None,
) -> List[dict]:
    """Read concrete IP objects from top-level VAR_DECL cursors.

    This intentionally does not inspect IPCREATE's macro definition: its
    formal names (IpName and InstName) are not program objects.  libclang
    exposes every expanded, file-scope declaration with its actual type/name.
    """
    cindex, _ = import_clang()
    if cindex is None:
        return []
    try:
        index = cindex.Index.create()
    except Exception:
        return []
    struct_names = set(known_structs)
    known_functions = set(function_names)
    clang_args = ["-x", "c", "-std=c99", f"-I{root}", f"-I{root / 'iplib'}"]
    if compilation_database is None:
        # Match extract_functions_libclang: resolve conventional header
        # locations so instance types are not read as incomplete structs.
        for include_dir in discover_include_directories(root):
            clang_args.append(f"-I{include_dir}")
    instances = []
    seen = set()
    for path in iter_translation_units(root):
        try:
            args = compilation_database.get(path.resolve(), clang_args) if compilation_database else clang_args
            tu = index.parse(str(path), args=args)
        except Exception:
            continue
        for cursor in tu.cursor.get_children():
            if cursor.kind != cindex.CursorKind.VAR_DECL or not same_file(cursor.location.file, path):
                continue
            type_name = cursor.type.spelling.replace("struct ", "").strip()
            if type_name not in struct_names:
                continue
            function_name = f"{type_name}Fun"
            if function_name not in known_functions:
                continue
            key = (cursor.spelling, path.resolve(), cursor.location.line)
            if not cursor.spelling or key in seen:
                continue
            seen.add(key)
            instances.append({
                "name": cursor.spelling,
                "type": type_name,
                "function": function_name,
                "initializer": "",
                "file": rel_path(path, root),
                "line": cursor.location.line,
                "kind": "ast_var_decl",
            })
    return sorted(instances, key=lambda item: (item["file"], item["line"], item["name"]))


def find_ipcalls(function: FunctionEvidence, instance_to_function: Dict[str, str]) -> List[dict]:
    if function.parser == "libclang":
        return [
            {
                **call,
                "resolved_function": instance_to_function.get(call["instance"]),
            }
            for call in function.ast_ipcalls
        ]
    calls = []
    for match in re.finditer(r"\bIPCALL\s*\(\s*(?P<inst>[A-Za-z_]\w*)\s*\)", function.code):
        inst = match.group("inst")
        resolved = instance_to_function.get(inst)
        line = function.start_line + function.code.count("\n", 0, match.start())
        calls.append(
            {
                "instance": inst,
                "resolved_function": resolved,
                "line": line,
                "statement": statement_at_line(function, line),
            }
        )
    return calls


def extract_function_like_macros(root: Path) -> List[str]:
    macros = set()
    for path in iter_c_files(root):
        text = read_text(path)
        for match in re.finditer(r"^\s*#\s*define\s+([A-Za-z_]\w*)\s*\(", text, re.M):
            macros.add(match.group(1))
    return sorted(macros)


def find_direct_calls(function: FunctionEvidence, macro_names: Optional[Iterable[str]] = None) -> List[str]:
    if function.ast_callees:
        return sorted(set(function.ast_callees))

    code = strip_comments(function.code)
    names = []
    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", code):
        name = match.group(1)
        if name == function.name or name in CALL_IGNORE:
            continue
        names.append(name)
    return sorted(set(names))


ASSIGNMENT_RE = r"(?:=(?!=)|\+\+|--|\+=|-=|\*=|/=|%=)"
VALUE_ASSIGNMENT_RE = r"(?:=(?!=)|\+=|-=|\*=|/=|%=)"
MEMBER_SELECTOR_RE = r"(?:\[[^\]]*\]\s*|\.\s*[A-Za-z_]\w*\s*|->\s*[A-Za-z_]\w*\s*)*"


def access_mode(tail: str, before: str = "") -> Tuple[bool, bool]:
    """Classify a member-like access from its immediate source context.

    The selector portion deliberately accepts nested members such as
    ``pIp->mController[0].Up``.  The graph records the declared top-level
    interface field, while this helper still sees the write to its child.
    """
    write_match = re.match(
        rf"\s*{MEMBER_SELECTOR_RE}(?:\)\s*)*{ASSIGNMENT_RE}", tail
    )
    if write_match:
        operator = write_match.group(0)
        return (
            any(token in operator for token in ("++", "--", "+=", "-=", "*=", "/=", "%=")),
            True,
        )
    if re.search(r"(?:\+\+|--)\s*$", before):
        return True, True
    return True, False


def first_access_is_write(code: str, pattern: str) -> bool:
    """Return whether the first source-level access matched by *pattern* writes.

    This is a deliberately intraprocedural rule: it only removes an input when
    the function itself initializes the object before any visible read.  It
    avoids claiming that a value is externally required merely because it is
    read back after that initialization.
    """
    match = re.search(pattern, code)
    if not match:
        return False
    before = code[max(0, match.start() - 12) : match.start()]
    reads, writes = access_mode(code[match.end() : match.end() + 80], before)
    return writes and not reads


def type_refers_to_struct(type_spelling: str, struct_name: str) -> bool:
    """Whether an AST type spelling names the requested structure type."""
    return bool(re.search(rf"\b{re.escape(struct_name)}\b", type_spelling))


def extract_member_accesses(
    function: FunctionEvidence,
    struct: Optional[StructEvidence],
    parameter_name: str = "",
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Return interface-member reads/writes as field-to-source-path mappings.

    The libclang path follows MEMBER_REF_EXPR cursors, so member access through
    a local alias such as ``ctx->count`` is tied to its declared structure
    type instead of relying on the local variable being named ``pIp``.  The
    old convention-based scan remains only as a fallback when no AST facts are
    available.
    """
    if struct and function.ast_member_accesses:
        field_names = {field.name for field in struct.fields}
        reads: Dict[str, str] = {}
        writes: Dict[str, str] = {}
        first_accesses: Dict[str, dict] = {}
        accesses_by_field: Dict[str, List[dict]] = {}
        for access in sorted(function.ast_member_accesses, key=lambda item: item["offset"]):
            field = access["name"]
            if field not in field_names:
                continue
            if parameter_name and not re.match(
                rf"\*?\s*{re.escape(parameter_name)}\s*(?:->|\.)",
                access["read_via"].lstrip(),
            ):
                continue
            owner_matches = access["owner"] == struct.name
            base_matches = any(
                type_refers_to_struct(type_spelling, struct.name)
                for type_spelling in access["base_types"]
            )
            if not owner_matches and not base_matches:
                continue
            if parameter_name and access["address_taken"]:
                # Taking a member's address (``&param->member``) binds a
                # pointer to later writes elsewhere; it neither consumes nor
                # overwrites the member's value here.  Same rule as the
                # global/instance member paths.
                continue
            first_accesses.setdefault(field, access)
            accesses_by_field.setdefault(field, []).append(access)
            if access["read"]:
                reads.setdefault(field, access["read_via"])
            if access["write"]:
                writes.setdefault(field, access["write_via"])

        # A field initialized before any read does not require a caller-supplied
        # value.  Keep an input when the initialization statement itself also
        # reads the field (for example ``field = field + 1``).
        for field, first_access in first_accesses.items():
            if not first_access["write"] or first_access["read"]:
                continue
            first_line = first_access["line"]
            statement_reads_field = any(
                access["line"] == first_line and access["read"]
                for access in accesses_by_field[field]
            )
            if not statement_reads_field:
                reads.pop(field, None)
        if reads or writes:
            return reads, writes

    if parameter_name:
        # No AST facts (fallback backend): scan the body text for the
        # parameter's own member accesses, using the same conventions as the
        # pIp scan below.  This keeps pointer-to-struct member extraction
        # consistent across backends instead of dropping it when libclang is
        # unavailable.
        if struct is None:
            return {}, {}
        body = strip_comments(split_function_body(function))
        field_names = {item.name for item in struct.fields}
        field_is_pointer = {item.name: "*" in item.type for item in struct.fields}
        reads: Dict[str, str] = {}
        writes: Dict[str, str] = {}
        pattern = (
            rf"\b{re.escape(parameter_name)}\s*(?P<sep>->|\.)\s*([A-Za-z_]\w*)"
        )
        for match in re.finditer(pattern, body):
            field = match.group(2)
            if field not in field_names:
                continue
            base_via = f"{parameter_name}{match.group('sep')}{field}"
            tail = body[match.end(): match.end() + 80]
            before = body[max(0, match.start() - 12): match.start()]
            is_read, is_write = access_mode(tail, before)
            dereferenced = bool(re.search(r"\*\s*$", before))
            subscript = re.match(r"\s*(\[[^\]]+\])", tail)
            pointee_via = base_via
            if dereferenced:
                pointee_via = f"*{base_via}"
            elif subscript:
                pointee_via = f"{base_via}{subscript.group(1)}"
            through_member_storage = (
                field_is_pointer.get(field, False)
                and (dereferenced or subscript is not None)
                and is_write
            )
            if through_member_storage:
                is_read = True
            if is_write:
                writes.setdefault(field, pointee_via)
                if is_read:
                    reads.setdefault(field, base_via)
            elif is_read:
                reads.setdefault(field, pointee_via)
        for field in list(writes):
            if (
                field in reads
                and first_access_is_write(
                    body,
                    rf"\b{re.escape(parameter_name)}\s*(?:->|\.)\s*{re.escape(field)}\b",
                )
            ):
                reads.pop(field, None)
        return reads, writes

    code = strip_comments(function.code)
    reads: Dict[str, str] = {}
    writes: Dict[str, str] = {}
    field_is_pointer = {
        item.name: "*" in item.type
        for item in (struct.fields if struct else [])
    }
    # Function interface members are accessed through the conventional pIp
    # pointer.  Do not promote members of local unions/temporaries into the
    # function interface (for example tmpw.Byte and tmpw.Float).
    for match in re.finditer(r"\bpIp\s*->\s*([A-Za-z_]\w*)", code):
        field = match.group(1)
        tail = code[match.end() : match.end() + 80]
        before = code[max(0, match.start() - 12) : match.start()]
        is_read, is_write = access_mode(tail, before)
        dereferenced = bool(re.search(r"\*\s*$", before))
        subscript = re.match(r"\s*(\[[^\]]+\])", tail)
        pointee_via = f"pIp->{field}"
        if dereferenced:
            pointee_via = f"*{pointee_via}"
        elif subscript:
            pointee_via = f"{pointee_via}{subscript.group(1)}"
        through_member_storage = (
            field_is_pointer.get(field, False)
            and (dereferenced or subscript is not None)
            and is_write
        )
        if through_member_storage:
            is_read = True
        if is_write:
            writes.setdefault(field, pointee_via)
            if is_read:
                reads.setdefault(field, f"pIp->{field}")
        elif is_read:
            reads.setdefault(field, pointee_via)
    for field in list(writes):
        if (
            field in reads
            and writes[field] == f"pIp->{field}"
            and first_access_is_write(
            code, rf"\bpIp\s*->\s*{re.escape(field)}\b"
            )
        ):
            del reads[field]
    return reads, writes


def struct_pointer_parameters(
    function: FunctionEvidence,
    structs_by_name: Dict[str, StructEvidence],
) -> Dict[str, StructEvidence]:
    """Return pointer parameters whose declared pointee type is a known struct."""
    match = re.search(r"\((.*)\)", function.signature)
    if not match:
        return {}
    parameters = {}
    for declaration in split_top_level_args(match.group(1)):
        if "*" not in declaration:
            continue
        parameter_name = parameter_declaration_name(declaration)
        if not parameter_name:
            continue
        for struct_name, struct in structs_by_name.items():
            if re.search(rf"\b{re.escape(struct_name)}\b", declaration):
                parameters[parameter_name] = struct
                break
    return parameters


def extract_global_accesses(
    function: FunctionEvidence,
    global_names: Iterable[str],
    excluded_names: Iterable[str] = (),
) -> Tuple[List[str], List[str]]:
    """Return accesses to global state, excluding IP instance objects.

    An IP instance is a file-scope object, but treating its use as a generic
    global I/O hides the more useful IPCALL/member evidence already emitted
    elsewhere in the graph.
    """
    if function.parser == "libclang":
        excluded = set(excluded_names)
        reads = set()
        writes = set()
        for access in function.ast_global_accesses:
            name = access["name"]
            if name in excluded:
                continue
            if access["read"]:
                reads.add(name)
            if access["write"]:
                writes.add(name)
        for access in function.ast_member_accesses:
            for base in access["global_bases"]:
                if base in excluded:
                    continue
                if access["name"] == "fun":
                    # ``IPCALL(x)`` expands to ``x.fun(&x)``.  The dispatch
                    # pointer is macro machinery, not function-local I/O.
                    continue
                name = f"{base}.{access['name']}"
                if access["address_taken"]:
                    # Passing a member's address does not itself consume or
                    # overwrite its value in this function.
                    continue
                if access["read"]:
                    reads.add(name)
                if access["write"]:
                    writes.add(name)
        for name in list(writes):
            # A member initialized before it is ever read is an output only.
            member_facts = [
                item for item in function.ast_member_accesses
                if item["global_bases"]
                and any(f"{base}.{item['name']}" == name for base in item["global_bases"])
            ]
            if member_facts and member_facts[0]["write"] and not member_facts[0]["read"]:
                reads.discard(name)
        return sorted(reads), sorted(writes)

    code = strip_comments(function.code)
    reads = set()
    writes = set()
    excluded = set(excluded_names)
    for name in global_names:
        if name in excluded:
            continue
        for match in re.finditer(rf"\b{re.escape(name)}\b", code):
            tail = code[match.end() : match.end() + 80]
            before = code[max(0, match.start() - 12) : match.start()]
            prefix = code[max(0, match.start() - 4) : match.start()]
            if re.search(r"(?:\.|->)\s*$", prefix):
                continue
            # ``object.member`` uses the object only as a member base and
            # ``&object`` only supplies an address.  Neither reads or writes
            # the object's value, so they belong to member/pointer-binding
            # analysis rather than generic global I/O.
            if re.match(r"\s*(?:\.|->)", tail) or re.search(r"&\s*$", before):
                continue
            is_read, is_write = access_mode(tail, before)
            if is_write:
                writes.add(name)
                if is_read:
                    reads.add(name)
            elif is_read:
                reads.add(name)
        has_member_access = bool(
            re.search(rf"\b{re.escape(name)}\s*(?:\.|->)", code)
        )
        if (
            name in reads
            and name in writes
            and not has_member_access
            and first_access_is_write(code, rf"\b{re.escape(name)}\b")
        ):
            reads.remove(name)
    return sorted(reads), sorted(writes)


def extract_instance_member_accesses(
    function: FunctionEvidence,
    instance_names: Iterable[str],
) -> Tuple[List[str], List[str]]:
    """Return reads/writes of concrete IPCREATE/initializer instance members.

    Instances are intentionally excluded from generic global access analysis,
    because ``instance.member`` carries more useful interface information than
    an opaque global-variable edge.  Keep the full dotted name to avoid
    conflating identically named fields on distinct instances.
    """
    if function.parser == "libclang":
        instances = set(instance_names)
        reads = set()
        writes = set()
        first_access: Dict[str, dict] = {}
        for access in sorted(function.ast_member_accesses, key=lambda item: item["offset"]):
            for instance in access["global_bases"]:
                if instance not in instances:
                    continue
                if access["name"] == "fun":
                    continue
                name = f"{instance}.{access['name']}"
                first_access.setdefault(name, access)
                if access["address_taken"]:
                    continue
                if access["read"]:
                    reads.add(name)
                if access["write"]:
                    writes.add(name)
        for name, access in first_access.items():
            if access["write"] and not access["read"]:
                reads.discard(name)
        return sorted(reads), sorted(writes)

    code = strip_comments(function.code)
    reads = set()
    writes = set()
    for instance in instance_names:
        for match in re.finditer(rf"\b{re.escape(instance)}\s*\.\s*([A-Za-z_]\w*)", code):
            field = match.group(1)
            qualified_name = f"{instance}.{field}"
            before = code[max(0, match.start() - 12) : match.start()]
            is_read, is_write = access_mode(code[match.end() : match.end() + 80], before)
            if is_write:
                writes.add(qualified_name)
                if is_read:
                    reads.add(qualified_name)
            elif is_read:
                reads.add(qualified_name)
        for qualified_name in writes.copy():
            instance_name, field = qualified_name.split(".", 1)
            if qualified_name in reads and first_access_is_write(
                code,
                rf"\b{re.escape(instance_name)}\s*\.\s*{re.escape(field)}\b",
            ):
                reads.remove(qualified_name)
    return sorted(reads), sorted(writes)


def parameter_declaration_name(declaration: str) -> Optional[str]:
    """Return the declared parameter name from a single C parameter declaration.

    A trailing array dimension may contain a macro (``const int active[N]``
    names ``active``, not ``N``), and function pointers declare their name
    inside ``(*name)``, so the last identifier is not always the parameter
    name.  Returns ``None`` for an unnamed parameter.
    """
    text = declaration.strip().rstrip(";")
    # Drop a trailing array dimension so its size expression (which may be a
    # macro such as AOCS_WHEEL_COUNT) is not mistaken for the parameter name.
    text = re.sub(r"\s*\[[^\]]*\]\s*$", "", text)
    names = re.findall(r"[A-Za-z_]\w*", text)
    if not names:
        return None
    candidate = names[-1]
    if candidate in PARAM_NAME_SKIP_TOKENS:
        pointer_name = re.search(r"\(\s*\*\s*([A-Za-z_]\w*)\s*\)", text)
        return pointer_name.group(1) if pointer_name else None
    return candidate


def function_parameters(function: FunctionEvidence) -> List[str]:
    """Extract named C parameters from a normalized function signature."""
    match = re.search(r"\((.*)\)", function.signature)
    if not match:
        return []
    parameters = []
    for declaration in split_top_level_args(match.group(1)):
        declaration = declaration.strip()
        if not declaration or declaration == "void" or declaration == "...":
            continue
        name = parameter_declaration_name(declaration)
        if name:
            parameters.append(name)
    return parameters


def extract_call_arguments(statement: str, callee: str) -> List[str]:
    """从一行调用语句中提取调用 *callee* 时的实参表达式列表。

    实参按位置与函数形参一一对应（C 语言按位置传参）。语句可能带
    ``if (...) { ... }`` 等前缀，因此从 ``callee(`` 开始做括号深度匹配，
    而不是简单取第一个括号对。``&tmBuf[28]`` 这类带下标/取地址的实参
    通过 ``split_top_level_args`` 的嵌套括号计数正确处理。
    """
    match = re.search(rf"\b{re.escape(callee)}\s*\(", statement)
    if not match:
        return []
    start = match.end()          # '(' 之后的位置
    depth = 1
    for j in range(start, len(statement)):
        ch = statement[j]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                return split_top_level_args(statement[start:j])
    return []


def call_site_origins(
    callee_name: str,
    ast_call_args_by_callee: Dict[str, List[dict]],
    call_occurrences_by_function: Dict[Tuple[str, str, int], List[FunctionCallOccurrence]],
    parameters: List[str],
) -> Dict[str, List[str]]:
    """把辅助函数的形参名映射到所有图内调用点传入的实参表达式。

    节点 inputs/outputs 里记录的 name 是函数体内部的形参名（如 ``val``、
    ``buf``），而调用点实参（如 ``attirate[2]``、``&tmBuf[28]``）才是数据
    真正的原始来源。此函数按调用位置把两者对齐，返回
    ``{形参名: [实参表达式, ...]}``（去重、保持出现顺序）。

    两个数据来源，前者优先：
    1. libclang AST（``CallExpr.get_arguments()``）：精确实参表达式；
    2. 正则退化/补充：覆盖宏调用（``IPCALL`` 等，不是 CallExpr 节点）
       以及 fallback 解析器（没有 AST 事实）。
    """
    origins: Dict[str, List[str]] = {}

    def record(args: List[str]) -> None:
        for param, arg in zip(parameters, args):
            if not arg or not param:
                continue
            current = origins.get(param, [])
            if arg not in current:
                current.append(arg)
                origins[param] = current

    for call in ast_call_args_by_callee.get(callee_name, []):
        record(call["args"])
    for occurrences in call_occurrences_by_function.values():
        for occ in occurrences:
            if occ.callee != callee_name:
                continue
            record(extract_call_arguments(occ.statement, callee_name))
    return origins


def parameter_is_pointer(function: FunctionEvidence, name: str) -> bool:
    """Whether *name* decays to a pointer: a ``*name`` or an array parameter."""
    return bool(
        re.search(rf"\*+\s*{re.escape(name)}\b", function.signature)
        or re.search(rf"\b{re.escape(name)}\s*\[", function.signature)
    )


def extract_parameter_accesses(
    function: FunctionEvidence,
    interface_struct: str = "",
) -> Tuple[List[str], List[str]]:
    """Return parameter reads and writes visible in the function body.

    A pointer parameter is an output only when the function writes through
    that pointer (``buf[i] =`` or ``*buf =``). Reassigning or incrementing the
    local pointer variable (``buf++`` / ``buf = other``) is not an externally
    visible write. Scalar parameters are passed by value and are never output.
    """
    body = strip_comments_preserving_lines(split_function_body(function))
    reads = set()
    writes = set(function.ast_parameter_writes)
    for name in function_parameters(function):
        interface_alias = bool(interface_struct) and bool(re.search(
            rf"\b{re.escape(interface_struct)}\s*\*\s*\w+\s*=\s*"
            rf"\(\s*{re.escape(interface_struct)}\s*\*\s*\)\s*{re.escape(name)}\b",
            body,
        ))
        if interface_alias:
            continue
        is_pointer = parameter_is_pointer(function, name)
        pointer_write_offsets = set()
        if is_pointer:
            pointer_write_patterns = (
                rf"\b(?P<name>{re.escape(name)})\s*\[[^\]]*\]\s*{VALUE_ASSIGNMENT_RE}",
                rf"\*\s*(?P<name>{re.escape(name)})\b\s*{VALUE_ASSIGNMENT_RE}",
                rf"\*\s*\(\s*(?P<name>{re.escape(name)})\s*(?:[+-][^()\n]*)?\)\s*{VALUE_ASSIGNMENT_RE}",
            )
            for pattern in pointer_write_patterns:
                for write_match in re.finditer(pattern, body):
                    pointer_write_offsets.add(write_match.start("name"))
                    writes.add(name)
        first_pointer_access = None
        for match in re.finditer(rf"\b{re.escape(name)}\b", body):
            if first_pointer_access is None:
                first_pointer_access = match.start()
            tail = body[match.end() : match.end() + 80]
            before = body[max(0, match.start() - 12) : match.start()]
            statement_start = max(body.rfind(";", 0, match.start()), body.rfind("{", 0, match.start())) + 1
            statement_prefix = body[statement_start : match.start()]
            on_right_hand_side = bool(re.search(r"(?<![=!<>])=(?!=)", statement_prefix))
            array_write = bool(re.match(
                r"\s*\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|%=)", tail
            ))
            dereference_write = bool(
                re.search(r"\*\s*$", before)
                and re.match(r"\s*(?:\+\+|--)?\s*(?:=(?!=)|\+=|-=|\*=|/=|%=)", tail)
                and not on_right_hand_side
            )
            if is_pointer and (array_write or dereference_write):
                writes.add(name)
            if match.start() not in pointer_write_offsets:
                reads.add(name)
        if is_pointer and first_pointer_access in pointer_write_offsets:
            reads.discard(name)
    return sorted(reads), sorted(writes)


def return_expression_name(expression: str) -> str:
    """Return the concrete object name when a return expression names one."""
    normalized = expression.strip()
    while normalized.startswith("(") and normalized.endswith(")"):
        normalized = normalized[1:-1].strip()
    match = re.search(r"([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*$", normalized)
    return match.group(1) if match else normalized


def extract_return_outputs(function: FunctionEvidence) -> List[dict]:
    """Extract source-level return expressions as concrete function outputs."""
    body = strip_comments(split_function_body(function))
    outputs = []
    seen = set()
    for match in re.finditer(r"\breturn\s+(?P<expression>[^;]+);", body, re.S):
        expression = " ".join(match.group("expression").split())
        if not expression or expression in seen:
            continue
        seen.add(expression)
        outputs.append({
            "name": return_expression_name(expression),
            "via": expression,
            "comment": "",
        })
    return outputs


def extract_globals(root: Path) -> List[str]:
    names = set()
    pattern = re.compile(
        r"^(?:extern\s+)?(?:const\s+)?(?:volatile\s+)?[A-Za-z_]\w*(?:\s+\*|\s+)+(?P<name>[A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:=|;)",
        re.M,
    )
    for path in iter_c_files(root):
        text = strip_comments(read_text(path))
        for match in pattern.finditer(text):
            names.add(match.group("name"))
    return sorted(names)


def clean_comment(raw: str) -> str:
    """Strip comment decoration (``/* */``, leading ``*``, ``//``) and collapse lines."""
    lines = []
    for line in raw.strip().splitlines():
        text = line.strip()
        text = re.sub(r"^/\**\s*", "", text)   # 块注释头 /* ...
        text = re.sub(r"^\*+\s*", "", text)    # 块注释续行 * ...
        text = re.sub(r"^//\s*", "", text)     # 行注释 //
        text = re.sub(r"\s*\**/$", "", text)   # 块注释尾 ... */
        text = text.rstrip("*").strip()
        if text and not re.fullmatch(r"[*=\-~\s]+", text):
            lines.append(text)
    return " ".join(lines)


GLOBAL_DECL_RE = re.compile(
    r"^(?:static\s+)?(?:extern\s+)?(?:const\s+)?(?:volatile\s+)?[A-Za-z_]\w*(?:\s+\*|\s+)+"
    r"(?P<name>[A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*(?:=|\;)",
    re.M,
)


def leading_comment_block(lines: List[str], line_no: int) -> str:
    """Collect the contiguous comment block directly above ``line_no``."""
    block: List[str] = []
    for idx in range(line_no - 1, -1, -1):
        text = lines[idx].strip()
        if not text:
            continue  # 注释块与声明之间允许空行
        if text.startswith("/*") or text.startswith("*") or text.startswith("//"):
            block.append(text)
            if text.startswith("/*") or text.startswith("//"):
                break
            continue
        break
    return "\n".join(reversed(block))


def extract_global_dictionary(root: Path, names: Iterable[str]) -> List[dict]:
    """Return ``[{name, comment}]`` for file-scope variables.

    The comment is the declarative text nearest the definition site: an
    end-of-line comment first, otherwise the contiguous comment block directly
    above the declaration.  It becomes the requirement/business name in the
    symbol dictionary (e.g. ``控制姿态角`` for ``attiang``); empty when the
    declaration carries no comment.
    """
    want = set(names)
    comment_by_name: Dict[str, str] = {}
    for path in iter_c_files(root):
        text = read_text(path)
        lines = text.splitlines()
        for match in GLOBAL_DECL_RE.finditer(text):
            name = match.group("name")
            if name not in want or name in comment_by_name:
                continue
            line_no = text[: match.start()].count("\n")
            line = lines[line_no] if line_no < len(lines) else ""
            comment = ""
            trailing = re.search(r"(?:/\*.*?\*/|//.*)$", line)
            if trailing:
                comment = clean_comment(trailing.group(0))
            else:
                comment = clean_comment(leading_comment_block(lines, line_no))
            if comment:
                comment_by_name[name] = comment
    return [{"name": name, "comment": comment_by_name.get(name, "")} for name in names]


def extract_globals_libclang(
    root: Path, compilation_database: Optional[CompilationDatabase] = None
) -> List[str]:
    """Collect file-scope variables through libclang when it is available.

    The regex fallback cannot reliably distinguish local declarations from
    globals and historically missed ``static`` arrays such as ``tmBuf``.
    Cursor ownership makes this distinction available without changing the
    extractor's fallback mode.
    """
    cindex, _ = import_clang()
    if cindex is None:
        return []
    try:
        index = cindex.Index.create()
    except Exception:
        return []

    clang_args = ["-x", "c", "-std=c99", f"-I{root}", f"-I{root / 'iplib'}"]
    names = set()
    for path in iter_translation_units(root):
        try:
            parse_args = compilation_database.get(path.resolve(), clang_args) if compilation_database else clang_args
            translation_unit = index.parse(str(path), args=parse_args)
        except Exception:
            continue
        for cursor in translation_unit.cursor.get_children():
            if cursor.kind != cindex.CursorKind.VAR_DECL:
                continue
            if same_file(cursor.location.file, path) and cursor.spelling:
                names.add(cursor.spelling)
    return sorted(names)


CONTROL_CALL_RE = re.compile(
    r"^(?:}\s*)?(?P<head>else\s+if|if|else|for|while|switch|case|default|do)\b(?P<tail>.*)"
)


def normalize_snippet(code: str, limit: int = 140) -> str:
    code = " ".join(code.strip().split())
    if len(code) <= limit:
        return code
    return code[: limit - 3].rstrip() + "..."


def statement_at_line_from_source(source: str, line: int) -> str:
    lines = source.splitlines()
    if 1 <= line <= len(lines):
        return normalize_snippet(lines[line - 1])
    return ""


def function_id(file: str, start_line: int, name: str) -> str:
    return f"func:{file}:{start_line}:{name}"


def function_id_for(function: FunctionEvidence) -> str:
    return function_id(function.file, function.start_line, function.name)


def resolve_function_id(
    name: str,
    caller_file: str,
    functions_by_name: Dict[str, List[FunctionEvidence]],
) -> Optional[str]:
    candidates = functions_by_name.get(name, [])
    if not candidates:
        return None
    same_file = [func for func in candidates if func.file == caller_file]
    if len(same_file) == 1:
        return function_id_for(same_file[0])
    return function_id_for(candidates[0])


def split_function_body(function: FunctionEvidence) -> str:
    open_index = function.code.find("{")
    close_index = function.code.rfind("}")
    if open_index < 0 or close_index <= open_index:
        return ""
    return function.code[open_index + 1:close_index]


def parse_control_context(line: str) -> Tuple[str, str, str]:
    match = CONTROL_CALL_RE.match(line.strip())
    if not match:
        return "", "", ""
    head = " ".join(match.group("head").split())
    tail = match.group("tail").strip()
    if head == "else":
        return "else", "false", "else"
    if head == "else if":
        return normalize_snippet(f"else if {tail}"), "else_if", "if"
    if head in ("if", "for", "while", "switch"):
        return normalize_snippet(f"{head} {tail}"), "true", head
    if head in ("case", "default"):
        return normalize_snippet(f"{head} {tail}"), "case", head
    if head == "do":
        return "do", "loop_body", "do"
    return normalize_snippet(line), "", head


def line_function_calls(
    line: str,
    instance_to_function: Dict[str, str],
    function_names: Iterable[str],
) -> List[str]:
    names = set(function_names)
    callees: List[str] = []

    for match in re.finditer(r"\bIPCALL\s*\(\s*(?P<inst>[A-Za-z_]\w*)\s*\)", line):
        resolved = instance_to_function.get(match.group("inst"))
        if resolved in names:
            callees.append(resolved)

    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", line):
        name = match.group(1)
        if name in names:
            callees.append(name)

    deduped = []
    seen = set()
    for callee in callees:
        if callee not in seen:
            deduped.append(callee)
            seen.add(callee)
    return deduped


def extract_function_call_occurrences(
    function: FunctionEvidence,
    instance_to_function: Dict[str, str],
    function_names: Iterable[str],
) -> List[FunctionCallOccurrence]:
    body = split_function_body(function)
    if not body:
        return []

    occurrences: List[FunctionCallOccurrence] = []
    active_controls: List[dict] = []
    depth = 0
    order = 1
    next_control_id = 1
    selection_orders: Dict[str, int] = {}

    for offset, raw_line in enumerate(body.splitlines(), start=1):
        code_line = strip_comments(raw_line).strip()
        if not code_line:
            depth += raw_line.count("{") - raw_line.count("}")
            depth = max(depth, 0)
            continue

        leading_closes = len(re.match(r"^\s*}*", raw_line).group(0).replace(" ", "").replace("\t", ""))
        effective_depth = max(depth - leading_closes, 0)
        inline_condition, inline_branch, inline_kind = parse_control_context(code_line)
        starts_new_case = inline_kind in ("case", "default")
        is_break = code_line.startswith("break")
        retained_controls = []
        for item in active_controls:
            kind = item.get("kind", "")
            if kind in ("case", "default"):
                keep = effective_depth >= item["depth"] and not starts_new_case and not is_break
            else:
                keep = effective_depth > item["depth"]
            if keep:
                retained_controls.append(item)
        active_controls = retained_controls

        nearest_control = active_controls[-1] if active_controls else {}
        condition = inline_condition or nearest_control.get("condition", "")
        branch = inline_branch or nearest_control.get("branch", "")
        switch_control = next(
            (item for item in reversed(active_controls) if item.get("kind") == "switch"),
            {},
        )
        selection_group = ""
        if branch == "case" and switch_control:
            selection_group = f"switch:{switch_control['id']}"

        for callee in line_function_calls(code_line, instance_to_function, function_names):
            if callee == function.name:
                continue
            if selection_group:
                occurrence_order = selection_orders.setdefault(selection_group, order)
                if occurrence_order == order:
                    order += 1
            else:
                occurrence_order = order
                order += 1
            occurrences.append(
                FunctionCallOccurrence(
                    caller=function.name,
                    callee=callee,
                    line=function.start_line + offset,
                    order=occurrence_order,
                    statement=normalize_snippet(code_line),
                    condition=condition,
                    branch=branch,
                    selection_group=selection_group,
                )
            )

        if inline_condition:
            active_controls.append(
                {
                    "id": next_control_id,
                    "condition": inline_condition,
                    "branch": inline_branch,
                    "kind": inline_kind,
                    "depth": effective_depth,
                }
            )
            next_control_id += 1

        depth += raw_line.count("{") - raw_line.count("}")
        depth = max(depth, 0)

    return occurrences


def build_function_flow_edges(
    function: FunctionEvidence,
    call_occurrences: List[FunctionCallOccurrence],
    functions_by_name: Dict[str, List[FunctionEvidence]],
) -> List[dict]:
    edges = []
    parent_id = function_id_for(function)

    def add_exec_order(previous: FunctionCallOccurrence, current: FunctionCallOccurrence) -> None:
        """Record an order relation guaranteed after *previous* executes."""
        if previous.callee == current.callee:
            return
        prev_id = resolve_function_id(previous.callee, function.file, functions_by_name)
        curr_id = resolve_function_id(current.callee, function.file, functions_by_name)
        if not prev_id or not curr_id:
            return
        edges.append(
            {
                "id": (
                    f"edge:{prev_id}->{curr_id}"
                    f":exec_order:{parent_id}:{previous.order:04d}-{current.order:04d}"
                ),
                "type": "exec_order",
                "source": prev_id,
                "target": curr_id,
                "parent_function": parent_id,
                "call_order": current.order,
                "evidence": {
                    "file": function.file,
                    "source_call": {
                        "start_line": previous.line,
                        "end_line": previous.line,
                        "statement": previous.statement,
                    },
                    "target_call": {
                        "start_line": current.line,
                        "end_line": current.line,
                        "statement": current.statement,
                    },
                },
            }
        )

    for prev, curr in zip(call_occurrences, call_occurrences[1:]):
        if prev.callee == curr.callee:
            continue
        # Entering a conditional call is not an unconditional successor of
        # the preceding call. Switch groups are handled below from each case
        # to their common post-switch successor.
        if curr.condition or prev.selection_group:
            continue
        add_exec_order(prev, curr)

    # A switch case is a special call step: exactly one listed branch may
    # execute. Every executed branch reaches the first later unconditional
    # call, so emit one path-valid order edge per branch.
    groups: Dict[str, List[Tuple[int, FunctionCallOccurrence]]] = {}
    for index, occurrence in enumerate(call_occurrences):
        if occurrence.selection_group:
            groups.setdefault(occurrence.selection_group, []).append((index, occurrence))
    for members in groups.values():
        after_group = max(index for index, _ in members) + 1
        successor = next(
            (
                occurrence
                for occurrence in call_occurrences[after_group:]
                if not occurrence.condition
            ),
            None,
        )
        if successor:
            for _, branch_call in members:
                add_exec_order(branch_call, successor)

    for occ in call_occurrences:
        if not occ.condition:
            continue
        callee_id = resolve_function_id(occ.callee, function.file, functions_by_name)
        if not callee_id:
            continue
        edges.append(
            {
                "id": f"edge:{parent_id}->{callee_id}:control:{occ.order:04d}",
                "type": "control",
                "source": parent_id,
                "target": callee_id,
                "condition": occ.condition,
                "branch": occ.branch,
                "evidence": {
                    "file": function.file,
                    "start_line": occ.line,
                    "end_line": occ.line,
                    "statement": occ.statement,
                },
            }
        )
    return edges


def statement_at_line(function: FunctionEvidence, line: int) -> str:
    """Return a normalized source line for a source-backed candidate."""
    offset = line - function.start_line
    lines = function.code.splitlines()
    if 0 <= offset < len(lines):
        return normalize_snippet(lines[offset])
    return ""


def build_graph(
    root: Path,
    backend: str = "auto",
    verbose: bool = False,
    compilation_database: Optional[CompilationDatabase] = None,
) -> dict:
    files = list(iter_c_files(root))
    structs = [struct for path in files for struct in extract_structs(path, root)]
    diagnostics: List[dict] = []
    parser_backend = "fallback"
    backend_message = ""

    functions: List[FunctionEvidence] = []
    if backend in ("auto", "clang"):
        functions, diagnostics, clang_error = extract_functions_libclang(
            root,
            verbose=verbose,
            compilation_database=compilation_database,
        )
        if functions:
            parser_backend = "libclang"
        elif backend == "clang":
            raise RuntimeError(clang_error or "libclang backend produced no function definitions")
        else:
            backend_message = clang_error or "libclang backend produced no function definitions; falling back"

    if not functions:
        if verbose and backend_message:
            print(f"[fallback] {backend_message}")
        if verbose:
            print("[fallback] scanning source files")
        functions = [func for path in files for func in extract_functions(path, root)]

    # AST declarations are authoritative.  The text parser is strictly a
    # fallback for environments where libclang is unavailable.
    instances = extract_instances_libclang(
        root,
        (struct.name for struct in structs),
        (function.name for function in functions),
        compilation_database,
    )
    if not instances and parser_backend != "libclang":
        instances = extract_instances(root)
    global_names = extract_globals_libclang(root, compilation_database) or extract_globals(root)
    globals_ = extract_global_dictionary(root, global_names)
    macro_names = extract_function_like_macros(root)

    struct_by_name = {struct.name: struct for struct in structs}
    instance_to_function = {item["name"]: item["function"] for item in instances}
    function_names = {func.name for func in functions}
    functions_by_name: Dict[str, List[FunctionEvidence]] = {}
    for func in functions:
        functions_by_name.setdefault(func.name, []).append(func)

    instances_by_function: Dict[str, List[dict]] = {}
    for item in instances:
        instances_by_function.setdefault(item["function"], []).append(item)

    # These per-function caches are keyed by (file, name, start_line) — the
    # same triple that dedupes FunctionEvidence — never by bare name.  Two
    # translation units can define the same function name (e.g. main in the
    # program and in its test harness); name-keyed caches would let the later
    # definition overwrite the earlier one and silently drop its edges.
    FunctionKey = Tuple[str, str, int]

    caller_ids: Dict[str, List[str]] = {}
    node_calls: Dict[FunctionKey, List[str]] = {}
    ipcall_evidence: Dict[FunctionKey, List[dict]] = {}
    for func in functions:
        key = (func.file, func.name, func.start_line)
        ipc = find_ipcalls(func, instance_to_function)
        ipcall_evidence[key] = ipc
        direct = find_direct_calls(func, macro_names)
        resolved_ip = [item["resolved_function"] for item in ipc if item["resolved_function"]]
        callees = sorted(set(direct + resolved_ip))
        node_calls[key] = callees
        for callee in callees:
            # The reverse index records caller *ids* so a duplicated caller
            # name (two mains) does not collapse to an arbitrary definition.
            if callee in function_names:
                caller_ids.setdefault(callee, []).append(function_id_for(func))

    call_occurrences_by_function: Dict[FunctionKey, List[FunctionCallOccurrence]] = {}
    for func in functions:
        key = (func.file, func.name, func.start_line)
        call_occurrences_by_function[key] = extract_function_call_occurrences(
            func,
            instance_to_function,
            function_names,
        )

    # Caller-side argument spellings collected from the AST (libclang backend).
    # Indexed by callee name so helper-function parameters can be mapped back to
    # the actual expressions passed at every in-graph call site.
    ast_call_args_by_callee: Dict[str, List[dict]] = {}
    for func in functions:
        for call in func.ast_call_arguments:
            ast_call_args_by_callee.setdefault(call["callee"], []).append(call)

    nodes = []
    for func in functions:
        related_instances = instances_by_function.get(func.name, [])
        related_struct = ""
        if related_instances:
            related_struct = related_instances[0]["type"]
        elif func.name.endswith("Fun") and func.name[:-3] in struct_by_name:
            related_struct = func.name[:-3]

        struct = struct_by_name.get(related_struct) if related_struct else None
        member_reads, member_writes = extract_member_accesses(func, struct)
        global_reads, global_writes = extract_global_accesses(
            func,
            global_names,
            instance_to_function,
        )
        instance_member_reads, instance_member_writes = extract_instance_member_accesses(
            func,
            instance_to_function,
        )
        parameter_reads, parameter_writes = extract_parameter_accesses(func, related_struct)
        parameter_structs = struct_pointer_parameters(func, struct_by_name)
        parameter_member_reads: Dict[str, str] = {}
        parameter_member_writes: Dict[str, str] = {}
        parameter_member_comments: Dict[str, str] = {}
        expanded_parameter_reads = set()
        expanded_parameter_writes = set()
        for parameter_name, parameter_struct in parameter_structs.items():
            reads, writes = extract_member_accesses(func, parameter_struct, parameter_name)
            for field, via in reads.items():
                parameter_member_reads.setdefault(field, via)
                parameter_member_comments.setdefault(
                    field,
                    next(
                        (item.comment for item in parameter_struct.fields if item.name == field),
                        "",
                    ),
                )
                expanded_parameter_reads.add(parameter_name)
            for field, via in writes.items():
                parameter_member_writes.setdefault(field, via)
                parameter_member_comments.setdefault(
                    field,
                    next(
                        (item.comment for item in parameter_struct.fields if item.name == field),
                        "",
                    ),
                )
                expanded_parameter_writes.add(parameter_name)

        # A struct-pointer parameter whose interface is expanded to member
        # level is fully described by those member entries.  Suppress the
        # whole-parameter name from both directions (a pure-output parameter
        # such as an initialized structure must not surface as an input).
        expanded_parameter_names = expanded_parameter_reads | expanded_parameter_writes

        field_comments = {f.name: f.comment for f in struct.fields} if struct else {}
        # Build unified inputs / outputs arrays
        inputs_arr = []
        input_seen = set()
        for field, via in sorted(member_reads.items()):
            inputs_arr.append({
                "name": field,
                "via": via,
                "comment": field_comments.get(field, ""),
            })
            input_seen.add(field)
        for name in global_reads:
            if name not in input_seen:
                inputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
        for name in instance_member_reads:
            if name not in input_seen:
                inputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
                input_seen.add(name)
        for name in parameter_reads:
            if name in expanded_parameter_names:
                continue
            if name not in input_seen:
                inputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
                input_seen.add(name)
        for field, via in sorted(parameter_member_reads.items()):
            if field not in input_seen:
                inputs_arr.append({
                    "name": field,
                    "via": via,
                    "comment": parameter_member_comments.get(field, ""),
                })
                input_seen.add(field)

        outputs_arr = []
        output_seen = set()
        for field, via in sorted(member_writes.items()):
            outputs_arr.append({
                "name": field,
                "via": via,
                "comment": field_comments.get(field, ""),
            })
            output_seen.add(field)
        for name in global_writes:
            if name not in output_seen:
                outputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
        for name in instance_member_writes:
            if name not in output_seen:
                outputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
                output_seen.add(name)
        for name in parameter_writes:
            if name in expanded_parameter_names:
                continue
            if name not in output_seen:
                outputs_arr.append({
                    "name": name,
                    "via": name,
                    "comment": "",
                })
                output_seen.add(name)
        for field, via in sorted(parameter_member_writes.items()):
            if field not in output_seen:
                outputs_arr.append({
                    "name": field,
                    "via": via,
                    "comment": parameter_member_comments.get(field, ""),
                })
                output_seen.add(field)
        for return_output in extract_return_outputs(func):
            if return_output["name"] not in output_seen:
                outputs_arr.append(return_output)
                output_seen.add(return_output["name"])

        # 辅助函数（带真实形参）：inputs/outputs 里的 name 是函数体内形参名，
        # 并非调用点的真实数据来源。对形参条目补 origins 字段，记录各调用点
        # 传入的实参表达式（如形参 buf <- &tmBuf[28]）；空数组表示图内没有
        # 可解析的调用点。成员/全局/return 条目不受影响，不追加该字段。
        params = function_parameters(func)
        param_set = set(params)
        origins_map = (
            call_site_origins(
                func.name,
                ast_call_args_by_callee,
                call_occurrences_by_function,
                params,
            )
            if params else {}
        )
        for item in inputs_arr + outputs_arr:
            if item["name"] in param_set:
                item["origins"] = origins_map.get(item["name"], [])

        node = {
            "id": function_id_for(func),
            "name": func.name,
            "ip_struct": related_struct or "",
            "comment": func.leading_comment,
            "description": "",
            "inputs": inputs_arr,
            "outputs": outputs_arr,
            "callers": sorted(set(caller_ids.get(func.name, []))),
            "callees": [
                resolved if resolved else f"macro_or_external:{name}"
                for name in node_calls.get((func.file, func.name, func.start_line), [])
                for resolved in [resolve_function_id(name, func.file, functions_by_name)]
            ],
            "evidence": {
                "file": func.file,
                "start_line": func.start_line,
                "end_line": func.end_line,
                "code": func.code,
            },
            "instances": related_instances,
            "ipcalls": ipcall_evidence.get((func.file, func.name, func.start_line), []),
        }
        nodes.append(node)

    edges = []
    edge_seen = set()
    for func in functions:
        for occurrence in call_occurrences_by_function.get((func.file, func.name, func.start_line), []):
            callee = occurrence.callee
            # A conditional invocation is represented by its control edge.
            # Emitting a second unconditional call-dependency edge would
            # erase the branch precondition from the graph.
            if occurrence.condition:
                continue
            if callee not in function_names:
                continue
            callee_id = resolve_function_id(callee, func.file, functions_by_name)
            if not callee_id:
                continue
            # Identity-key the dedup so two callers that share a name (two
            # mains) never suppress each other's dependency edges.
            key = (function_id_for(func), callee, "call", occurrence.order)
            if key in edge_seen:
                continue
            edge_seen.add(key)
            evidence = {
                "file": func.file,
                "start_line": occurrence.line,
                "end_line": occurrence.line,
                "statement": occurrence.statement,
            }
            edges.append(
                {
                    "id": (
                        f"edge:{function_id_for(func)}->{callee_id}"
                        f":function_dependency:{occurrence.order:04d}"
                    ),
                    "type": "function_dependency",
                    "source": function_id_for(func),
                    "target": callee_id,
                    "evidence": evidence,
                }
            )
    for func in functions:
        for edge in build_function_flow_edges(
            func,
            call_occurrences_by_function.get((func.file, func.name, func.start_line), []),
            functions_by_name,
        ):
            key = (
                edge.get("type"),
                edge.get("source"),
                edge.get("target"),
                edge.get("parent_function"),
                edge.get("call_order"),
                edge.get("condition", ""),
            )
            if key in edge_seen:
                continue
            edge_seen.add(key)
            edges.append(edge)

    return {
        "schema_version": "0.5",
        "root": "",
        "parser": {
            "backend": parser_backend,
            "diagnostics": diagnostics,
            "macro_names": macro_names,
        },
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(edges, key=lambda item: item["id"]),
        "evidence_index": {
            "structs": [
                {
                    "name": struct.name,
                    "tag": struct.tag,
                    "comment": struct.comment,
                    "file": struct.file,
                    "start_line": struct.start_line,
                    "end_line": struct.end_line,
                    "fields": [field.__dict__ for field in struct.fields],
                }
                for struct in sorted(structs, key=lambda item: item.name)
            ],
            "instances": instances,
            "globals": globals_,
        },
    }


def resolve_source_root(root_arg: Optional[str], configured_root: str, script_dir: Path) -> Optional[Path]:
    chosen_root = root_arg or configured_root
    if not chosen_root:
        return None

    raw = Path(chosen_root)
    if raw.is_absolute():
        return raw.resolve()

    candidates = [
        (Path.cwd() / raw).resolve(),
        (script_dir / raw).resolve(),
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[0]


def main() -> int:
    # ── Repo configuration ──────────────────────────────────────────
    # When adapting for a different repo, reassign these two variables
    # (or pass the equivalent CLI args):
    #   DEFAULT_REPO_ROOT   = "path/to/your/code"
    #   DEFAULT_REPO_LABEL  = "your-repo-label"
    # ────────────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="Extract function-level static evidence JSON.")
    parser.add_argument(
        "--root",
        "--code-dir",
        dest="root",
        default=None,
        help="Required C source directory, for example code or groundtruth.",
    )
    parser.add_argument(
        "--repo-label",
        default=REPO_LABEL,
        help="Short identifier used in output filenames to avoid mixing repos. "
             "Auto-derived from root path basename when not set.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output JSON path. Defaults to tools/<repo-label>/raw_graph.json.",
    )
    parser.add_argument(
        "--backend",
        choices=("auto", "clang", "fallback"),
        default="auto",
        help="Parser backend. auto uses libclang when available and falls back otherwise.",
    )
    parser.add_argument(
        "--prepare-build",
        action="store_true",
        help="Build a detected CMake/Make project to obtain compile_commands.json before parsing.",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output.")
    args = parser.parse_args()

    # Default output: tools/<repo_label>/raw_graph.json
    script_dir = Path(__file__).resolve().parent
    root = resolve_source_root(args.root, CODE_DIR, script_dir)
    if root is None:
        print(
            "error: source directory is required.\n"
            "       Pass --root/--code-dir, for example:\n"
            "       python extract_evidence.py --code-dir E:\\project\\code\n"
            "       Or set CODE_DIR at the top of extract_evidence.py.",
            file=sys.stderr,
        )
        return 1

    if not root.is_dir():
        print(
            f"error: source directory not found: {root}\n"
            "       Pass --root/--code-dir with the C source directory.",
            file=sys.stderr,
        )
        return 1

    repo_label = args.repo_label or root.name
    default_out = Path(repo_label) / "raw_graph.json"
    out_path = Path(args.out) if args.out else default_out
    if not out_path.is_absolute():
        out_path = script_dir / out_path

    compilation_database = None
    build_messages = []
    compilation_database_path = find_compilation_database(root)
    if args.prepare_build:
        compilation_database_path, build_messages = prepare_compilation_database(root)
        for message in build_messages:
            print(f"[build-discovery] {message}")
    if compilation_database_path is not None:
        try:
            compilation_database = load_compilation_database(compilation_database_path)
            print(f"Compilation database: {compilation_database_path}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(
                f"Warning: ignoring invalid compile_commands.json: {exc}",
                file=sys.stderr,
            )
            compilation_database_path = None

    graph = build_graph(
        root,
        backend=args.backend,
        verbose=not args.quiet,
        compilation_database=compilation_database,
    )

    # Attach repo identity so downstream tools know which source this came from
    graph["repo_label"] = repo_label
    graph["root"] = str(root.resolve())
    graph["parser"]["compilation_database"] = (
        str(compilation_database_path) if compilation_database_path else ""
    )
    graph["parser"]["build_evidence"] = [
        {"kind": item.kind, "path": str(item.path)}
        for item in discover_build_evidence(root)
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Repo label : {repo_label}")
    print(f"Root       : {root}")
    print(f"Parser backend: {graph['parser']['backend']}")
    print(f"Diagnostics: {len(graph['parser']['diagnostics'])}")
    print(f"Nodes: {len(graph['nodes'])}, edges: {len(graph['edges'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
