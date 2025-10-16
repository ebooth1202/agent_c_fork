"""Text-based PL/SQL code scanner.

This module provides regex-based entity extraction for PL/SQL code.
Since tree-sitter-plsql lacks Python bindings, we use proven text
scanning techniques to identify packages, procedures, functions, etc.

The scanner handles:
- Comment masking (-- and /* */)
- String literal masking (including q'X...X' quoted strings)
- Dotted identifiers (schema.package.object)
- Parameter lists with nested parentheses
- Leading documentation comments
- Complex PL/SQL syntax (quoted identifiers, nested blocks, etc.)
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Any, Tuple


def build_line_index(code: str) -> List[int]:
    """Build index of line start positions.

    Returns a list of byte offsets where each line starts (0-based).

    Args:
        code: Source code string

    Returns:
        List of byte offsets for each line start
    """
    starts = [0]
    for i, ch in enumerate(code):
        if ch == '\n':
            starts.append(i + 1)
    return starts


def byte_to_line_col(b: int, line_starts: List[int]) -> Tuple[int, int]:
    """Convert byte index to line and column numbers.

    Args:
        b: Byte position in source
        line_starts: Line start positions from build_line_index()

    Returns:
        Tuple of (line, column), both 0-based (matching tree-sitter convention)
    """
    line = 0
    for i, start in enumerate(line_starts):
        if start > b:
            line = i - 1  # 0-based: subtract 1 to get the actual line index
            break
    else:
        line = len(line_starts) - 1  # 0-based: last line index

    prev = line_starts[line] if line >= 0 else 0
    col = b - prev  # 0-based: no +1 needed
    return line, col


def mask_comments_and_strings(src: str) -> str:
    """Mask comments and string literals with spaces.

    Returns a same-length string where comments and string literals are
    blanked to spaces. This keeps indices aligned while preventing
    false-positive keyword matches.

    Handles:
    - -- line comments
    - /* block comments */
    - '...' string literals (with doubled '' escapes)
    - q'X...X' quoted string literals

    Args:
        src: Source code string

    Returns:
        Masked version of source with comments/strings as spaces
    """
    s = list(src)
    i, n = 0, len(src)
    lower = src.lower()

    def space_out(a: int, b: int):
        """Replace range with spaces."""
        for k in range(max(a, 0), min(b, n)):
            s[k] = ' '

    while i < n:
        ch = src[i]

        # -- line comment
        if ch == '-' and i + 1 < n and src[i + 1] == '-':
            j = i + 2
            while j < n and src[j] != '\n':
                j += 1
            space_out(i, j)
            i = j
            continue

        # /* block comment */
        if ch == '/' and i + 1 < n and src[i + 1] == '*':
            j = i + 2
            while j < n - 1 and not (src[j] == '*' and src[j + 1] == '/'):
                j += 1
            j = j + 2 if j < n - 1 else n
            space_out(i, j)
            i = j
            continue

        # 'string' literal (handle doubled '' escapes)
        if ch == "'":
            j = i + 1
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":
                        j += 2
                        continue
                    j += 1
                    break
                j += 1
            space_out(i, j)
            i = j
            continue

        # q'X...X' quoted string literal
        if lower.startswith("q'", i):
            j = i + 2
            if j < n:
                opener = src[j]
                closers = {'[': ']', '(': ')', '{': '}', '<': '>'}
                closer = closers.get(opener, opener)
                j += 1
                while j < n - 1:
                    if src[j] == closer and src[j + 1] == "'":
                        j += 2
                        break
                    j += 1
                space_out(i, j)
                i = j
                continue

        i += 1

    return ''.join(s)


# Identifier pattern (handles quoted identifiers)
_IDENT = r'(?:[A-Za-z_#$][A-Za-z0-9_#$]*|"(?:[^"]|"")+")'


def read_dotted_ident(clean: str, start: int, src: str) -> Tuple[str, int]:
    """Read dotted identifier like schema.package.name.

    Args:
        clean: Masked source code (comments/strings removed)
        start: Starting position to read from
        src: Original source code (for preserving exact text)

    Returns:
        Tuple of (final_name_part, next_position)
    """
    n = len(clean)
    i = start
    parts: List[str] = []

    while i < n:
        # Skip whitespace
        while i < n and clean[i].isspace():
            i += 1

        m = re.match(_IDENT, src[i:])
        if not m:
            break

        token = m.group(0)
        parts.append(token.strip('"'))
        i += len(token)

        # Skip whitespace
        while i < n and clean[i].isspace():
            i += 1

        if i < n and src[i] == '.':
            i += 1
            continue
        break

    name = parts[-1] if parts else ""
    return name, i


def find_matching_paren(clean: str, open_pos: int) -> int:
    """Find matching ')' for '(' at open_pos.

    Args:
        clean: Masked source code
        open_pos: Position of opening '('

    Returns:
        Position after the matching ')' (exclusive)
    """
    depth = 0
    i, n = open_pos, len(clean)

    while i < n:
        ch = clean[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1

    return open_pos + 1


def scan_until_keywords(clean: str, start: int, keywords: List[str]) -> int:
    """Scan forward until one of the keywords is found.

    Args:
        clean: Masked source code
        start: Starting position
        keywords: List of keywords to search for

    Returns:
        Index of first keyword found, or len(clean) if none found
    """
    pattern = re.compile(r'(?i)' + '|'.join(rf'\b{re.escape(kw)}\b' for kw in keywords))
    m = pattern.search(clean, start)
    return m.start() if m else len(clean)


def extract_leading_doc(src: str, entity_start: int) -> Optional[str]:
    """Extract leading comment documentation before entity_start.

    Collects contiguous leading comments (-- or /* */) immediately
    above the entity position.

    Args:
        src: Original source code
        entity_start: Byte position where entity starts

    Returns:
        Extracted documentation string, or None if no docs found
    """
    # Start from position before entity
    j = entity_start - 1

    # Skip back over whitespace
    while j >= 0 and src[j].isspace():
        j -= 1

    # Check for block comment /* */ ending just before entity
    if j >= 1 and src[j] == '/' and j - 1 >= 0 and src[j - 1] == '*':
        # Found */ - find matching /*
        end_pos = j + 1
        j -= 2
        while j >= 0:
            if j + 1 < len(src) and src[j] == '/' and src[j + 1] == '*':
                # Found start of block comment
                comment_text = src[j + 2:end_pos - 2].strip()
                if comment_text:
                    # Clean up extra asterisks and whitespace from formatted comments
                    lines = []
                    for line in comment_text.split('\n'):
                        line = line.strip()
                        if line.startswith('*'):
                            line = line[1:].lstrip()
                        lines.append(line)
                    return '\n'.join(lines).strip() or None
            j -= 1

    # Reset and collect consecutive -- line comments
    lines = []
    j = entity_start - 1

    # Skip back over whitespace
    while j >= 0 and src[j].isspace():
        j -= 1

    # Collect all consecutive -- comment lines working backwards
    while j >= 0:
        # Find start of current line
        line_start = src.rfind('\n', 0, j)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1

        line = src[line_start:j + 1].strip()

        if line.startswith('--'):
            # Extract comment text
            lines.append(line[2:].lstrip())
            # Move to previous line
            j = line_start - 1
            # Skip whitespace
            while j >= 0 and src[j].isspace():
                if src[j] == '\n':
                    j -= 1
                    break
                j -= 1
        elif not line:
            # Allow one blank line between comment blocks
            j = line_start - 1
            while j >= 0 and src[j].isspace():
                if src[j] == '\n':
                    j -= 1
                    break
                j -= 1
        else:
            # Hit non-comment line
            break

    if lines:
        lines.reverse()
        return '\n'.join(lines).strip() or None

    return None


def normalize_space(s: str) -> str:
    """Collapse multiple whitespace into single spaces.

    Args:
        s: String to normalize

    Returns:
        String with whitespace collapsed
    """
    return re.sub(r'\s+', ' ', s.strip())


def gather_subprograms(src: str) -> List[Dict[str, Any]]:
    """Extract PROCEDURE and FUNCTION definitions.

    Finds standalone and package procedures/functions with their
    signatures, parameters, return types, and documentation.

    Args:
        src: PL/SQL source code

    Returns:
        List of dicts with keys: kind, name, start, end, signature,
        return_type, docstring
    """
    clean = mask_comments_and_strings(src)
    results: List[Dict[str, Any]] = []
    i, n = 0, len(clean)

    while i < n:
        m = re.search(r'(?i)\b(procedure|function)\b', clean[i:])
        if not m:
            break

        kw = m.group(1).lower()
        k_func = i + m.start()  # Position of FUNCTION/PROCEDURE keyword
        k0 = k_func  # Start position for documentation search

        # Back up k0 to include CREATE OR REPLACE if present
        # Search backwards from k_func for CREATE keyword
        prefix_search = clean[max(0, k_func-100):k_func]  # Look back up to 100 chars
        create_match = re.search(r'(?i)\bcreate\s+(?:or\s+replace\s+)?(?:editionable\s+)?$', prefix_search)
        if create_match:
            # Adjust k0 to point to the start of CREATE
            k0 = max(0, k_func - 100) + create_match.start()

        # Read name (starts after the FUNCTION/PROCEDURE keyword)
        name, j = read_dotted_ident(clean, k_func + len(kw), src)
        if not name:
            i = k_func + len(kw)
            continue

        # Skip whitespace
        while j < n and clean[j].isspace():
            j += 1

        # Parameters
        params_text = ""
        if j < n and clean[j] == '(':
            params_end = find_matching_paren(clean, j)
            params_text = src[j:params_end]
            j = params_end

        # Scan to IS/AS
        header_end = scan_until_keywords(clean, j, ['is', 'as'])
        header = src[k0:header_end]

        # Extract RETURN type for functions
        return_type = None
        if kw == 'function':
            retm = re.search(r'(?i)\breturn\b\s+([A-Za-z0-9_%$.()]+(?:\s*%\s*(?:TYPE|ROWTYPE))?)', header)
            if retm:
                return_type = retm.group(1).strip()

        # Find END...;
        # We need to track depth and ensure we've seen at least one BEGIN
        depth = 0
        pos = header_end
        end_pos = None
        seen_begin = False

        while pos < n:
            m2 = re.search(r'(?i)\b(begin|end)\b|;', clean[pos:])
            if not m2:
                break

            kind = m2.group(0).lower()
            p = pos + m2.start()

            if kind == 'begin':
                depth += 1
                seen_begin = True
                pos = p + 5
            elif kind == 'end':
                depth -= 1
                if seen_begin and depth == 0:
                    # This is the END for our procedure/function (back to depth 0)
                    msemi = re.search(r';', clean[p:])
                    end_pos = p + msemi.end() if msemi else p + 3
                    break
                pos = p + 3
            else:  # semicolon
                pos = p + 1

        if end_pos is None:
            # Fallback: find next semicolon after IS/AS
            msemi = re.search(r';', clean[header_end:])
            end_pos = header_end + msemi.end() if msemi else header_end

        # Build signature
        sig_kw = 'PROCEDURE' if kw == 'procedure' else 'FUNCTION'
        signature = normalize_space(
            f"{sig_kw} {name}{params_text}{(' RETURN ' + return_type) if return_type else ''}"
        )

        docstring = extract_leading_doc(src, k0)

        results.append({
            'kind': kw,
            'name': name,
            'start': k0,
            'end': end_pos,
            'signature': signature,
            'return_type': return_type,
            'docstring': docstring
        })

        i = end_pos if end_pos else header_end

    return results


def gather_variables(src: str) -> List[Dict[str, Any]]:
    """Extract global variable declarations.

    Finds package-level variables only. Variables inside procedures/functions
    (whether standalone or in packages) are excluded.

    Args:
        src: PL/SQL source code

    Returns:
        List of dicts with keys: name, start, end, var_type, default_value, docstring
    """
    clean = mask_comments_and_strings(src)
    results: List[Dict[str, Any]] = []

    # First, gather all subprograms so we can exclude variables inside them
    subprograms = gather_subprograms(src)

    # Pattern for variable declarations (e.g., g_var NUMBER := 100;)
    # Look for: identifier type [:= value];
    # Type must be at least 2 characters (not just a single paren or symbol)
    pattern = r'(?i)\b(' + _IDENT + r')\s+([A-Za-z_][A-Za-z0-9_%$.()]*(?:\s*%\s*(?:TYPE|ROWTYPE))?)\s*(?::=\s*([^;]+))?\s*;'

    # Keywords that indicate this is NOT a variable declaration
    non_var_keywords = {'begin', 'end', 'if', 'then', 'else', 'elsif', 'loop', 'while',
                        'for', 'exit', 'return', 'null', 'declare', 'exception', 'when',
                        'procedure', 'function', 'package', 'create', 'alter', 'drop',
                        'in', 'out', 'default', 'constant', 'nocopy', 'type', 'subtype',
                        'cursor', 'record', 'table', 'index', 'by', 'of', 'ref', 'rowtype',
                        'select', 'from', 'where', 'insert', 'update', 'delete', 'into',
                        'values', 'set', 'and', 'or', 'not', 'is', 'as', 'like', 'between',
                        'exists', 'order', 'group', 'having', 'distinct', 'all', 'any',
                        'raise', 'pragma', 'exception_init', 'others', 'goto', 'case',
                        'date', 'timestamp', 'varchar2', 'varchar', 'number', 'integer',
                        'boolean', 'char', 'clob', 'blob', 'raw', 'rowid',
                        'commit', 'rollback', 'savepoint', 'lock', 'grant', 'revoke'}

    for m in re.finditer(pattern, clean):
        var_name = m.group(1).strip('"').lower()
        var_type = m.group(2).strip()
        default_value = m.group(3).strip() if m.group(3) else None

        # Skip if the "variable name" is actually a keyword
        if var_name in non_var_keywords:
            continue

        k0 = m.start()

        # Skip if this variable is inside any subprogram
        inside_subprogram = False
        for sub in subprograms:
            if sub["start"] < k0 < sub["end"]:
                inside_subprogram = True
                break

        if inside_subprogram:
            continue

        docstring = extract_leading_doc(src, k0)

        results.append({
            'name': m.group(1).strip('"'),  # Keep original casing
            'start': k0,
            'end': m.end(),
            'var_type': var_type,
            'default_value': default_value,
            'docstring': docstring
        })

    return results


def gather_packages(src: str) -> List[Dict[str, Any]]:
    """Extract PACKAGE and PACKAGE BODY definitions.

    Finds package specifications and bodies with their documentation.

    Args:
        src: PL/SQL source code

    Returns:
        List of dicts with keys: name, start, end, docstring, is_body
    """
    clean = mask_comments_and_strings(src)
    results: List[Dict[str, Any]] = []

    pattern = r'(?i)\bcreate\s+(or\s+replace\s+)?(editionable\s+|noneditionable\s+)?package(\s+body)?\s+(' + _IDENT + r')'

    for m in re.finditer(pattern, clean):
        k0 = m.start()
        is_body = m.group(3) is not None

        # Extract name from original source
        name_match = re.search(_IDENT, src[m.start(4):])
        if not name_match:
            continue
        name = name_match.group(0).strip('"')

        # Find END...;
        tail = clean[m.end():]
        mend = re.search(r'(?i)\bend\b', tail)
        if not mend:
            continue

        p = m.end() + mend.start()
        msemi = re.search(r';', clean[p:])
        end_pos = p + msemi.end() if msemi else p + 3

        docstring = extract_leading_doc(src, k0)

        results.append({
            'name': name,
            'start': k0,
            'end': end_pos,
            'docstring': docstring,
            'is_body': is_body
        })

    return results
