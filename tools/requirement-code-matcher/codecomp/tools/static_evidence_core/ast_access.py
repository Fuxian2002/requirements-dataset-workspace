"""Small, conservative libclang access facts used by the extractor."""

from __future__ import annotations

from typing import Any, List, Set


ASSIGNMENT_TOKENS = {"=", "+=", "-=", "*=", "/=", "%="}


def pointer_parameter_writes(function_cursor: Any, cindex: Any) -> Set[str]:
    """Return pointer parameters written through inside a function body.

    The result deliberately excludes a reassignment of the local pointer
    variable itself (``pointer = other``).  It includes only an array/member
    lvalue or an explicit dereference, which changes caller-visible storage.
    """
    pointer_parameters = {
        parameter.spelling
        for parameter in function_cursor.get_arguments()
        if "*" in parameter.type.spelling
    }
    writes: Set[str] = set()
    if not pointer_parameters:
        return writes

    def referenced_parameters(cursor: Any) -> Set[str]:
        names: Set[str] = set()
        referenced = getattr(cursor, "referenced", None)
        if (
            referenced is not None
            and referenced.kind == cindex.CursorKind.PARM_DECL
            and referenced.spelling in pointer_parameters
        ):
            names.add(referenced.spelling)
        for child in cursor.get_children():
            names.update(referenced_parameters(child))
        return names

    def is_indirect_lvalue(cursor: Any) -> bool:
        tokens = {token.spelling for token in cursor.get_tokens()}
        return bool(tokens & {"[", "->", "*"})

    def visit(cursor: Any) -> None:
        if cursor.kind in {
            cindex.CursorKind.BINARY_OPERATOR,
            cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR,
        }:
            children = list(cursor.get_children())
            tokens = {token.spelling for token in cursor.get_tokens()}
            if len(children) >= 2 and tokens & ASSIGNMENT_TOKENS:
                left = children[0]
                if is_indirect_lvalue(left):
                    writes.update(referenced_parameters(left))
        for child in cursor.get_children():
            visit(child)

    visit(function_cursor)
    return writes


def _decode_bytes(data: bytes) -> str:
    for encoding in ("utf-8-sig", "gb18030", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def call_site_arguments(function_cursor: Any, cindex: Any, source_bytes: bytes) -> List[dict]:
    """Collect direct call sites inside a function body from the AST.

    Each entry has ``callee`` (spelled function name), ``line`` and ``args``:
    the exact argument expression texts, restored from each argument cursor's
    source extent.  Unlike a regex over the code line this is immune to nested
    parentheses, subscripts and compound expressions (``&tmBuf[34 + i * 4]``,
    ``pIp->mController[0].Up``).  Macro invocations (``IPCALL``/``IPCREATE``)
    are not ``CallExpr`` nodes unless the macro expands to a real call, so
    they are intentionally left to the regex fallback in the caller.
    """
    calls: List[dict] = []
    seen: Set[tuple] = set()

    def callee_name(cursor: Any) -> str:
        # CallExpr.spelling is the called function name; keep a referenced-symbol
        # scan as a fallback for spellings that may be empty on some backends.
        if cursor.spelling:
            return cursor.spelling
        for child in cursor.get_children():
            referenced = getattr(child, "referenced", None)
            if referenced is not None and referenced.spelling:
                return referenced.spelling
        return ""

    def visit(cursor: Any) -> None:
        if cursor.kind == cindex.CursorKind.CALL_EXPR:
            name = callee_name(cursor)
            args = [
                _decode_bytes(
                    source_bytes[arg.extent.start.offset:arg.extent.end.offset]
                ).strip()
                for arg in cursor.get_arguments()
            ]
            key = (name, cursor.extent.start.line, tuple(args))
            if key not in seen:
                seen.add(key)
                calls.append({
                    "callee": name,
                    "line": cursor.extent.start.line,
                    "args": args,
                })
        for child in cursor.get_children():
            visit(child)

    visit(function_cursor)
    return calls
