"""
PL/SQL Parser and Structure Extractor

This module provides tokenization and structure extraction for PL/SQL code,
handling Oracle-specific syntax including comments, string literals, q-quotes,
and nested BEGIN/END blocks.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import re


# PL/SQL keywords we care about for structure analysis
KEYWORDS = {
    "procedure", "function", "begin", "end", "is", "as", "package", "body",
    "create", "or", "replace", "trigger", "type", "declare", "exception",
    "when", "then", "cursor", "pragma"
}


@dataclass
class Token:
    """Represents a token in PL/SQL source code."""
    kind: str
    text: str
    start: int
    end: int

    def __repr__(self):
        return f"Token({self.kind!r}, {self.text!r}, {self.start}, {self.end})"


@dataclass
class PlSqlUnit:
    """Represents a logical unit in PL/SQL code (procedure, function, package, etc.)."""
    unit_type: str  # 'procedure', 'function', 'package_spec', 'package_body', 'trigger', 'type'
    name: str
    start_pos: int
    end_pos: int
    start_line: int
    end_line: int
    signature: Optional[str] = None
    package_name: Optional[str] = None  # For subprograms within packages
    dependencies: List[str] = None  # Identifiers referenced

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


def tokenize_plsql(src: str) -> List[Token]:
    """
    Tokenize PL/SQL source, ignoring comments and string literals.
    
    Args:
        src: PL/SQL source code as a string
        
    Returns:
        List of Token objects
    """
    i = 0
    n = len(src)
    toks: List[Token] = []
    lower = src.lower()

    def add_token(kind: str, start: int, end: int):
        toks.append(Token(kind, src[start:end], start, end))

    while i < n:
        ch = src[i]

        # Line comment --
        if ch == '-' and i + 1 < n and src[i + 1] == '-':
            j = i + 2
            while j < n and src[j] != '\n':
                j += 1
            i = j
            continue

        # Block comment /* ... */
        if ch == '/' and i + 1 < n and src[i + 1] == '*':
            j = i + 2
            while j < n - 1 and not (src[j] == '*' and src[j + 1] == '/'):
                j += 1
            i = j + 2 if j < n - 1 else n
            continue

        # String literal '...'
        if ch == "'":
            j = i + 1
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":  # escaped ''
                        j += 2
                        continue
                    j += 1
                    break
                j += 1
            i = j
            continue

        # q-quote literal q'[...]' etc.
        if lower.startswith("q'", i):
            j = i + 2
            if j < n:
                opener = src[j]
                closers = {
                    '[': ']',
                    '(': ')',
                    '{': '}',
                    '<': '>',
                }
                closer = closers.get(opener, opener)
                j += 1
                while j < n - 1:
                    if src[j] == closer and src[j + 1] == "'":
                        j += 2
                        break
                    j += 1
                i = j
                continue

        # Quoted identifiers "..."
        if ch == '"':
            j = i + 1
            while j < n:
                if src[j] == '"':
                    j += 1
                    break
                j += 1
            add_token("ident", i, j)
            i = j
            continue

        # Identifiers/keywords
        if ch.isalpha() or ch == '_' or ch == '$' or ch == '#':
            j = i + 1
            while j < n and (src[j].isalnum() or src[j] in ('_', '$', '#')):
                j += 1
            text = src[i:j]
            ltext = text.lower()
            if ltext in KEYWORDS:
                add_token(ltext, i, j)
            else:
                add_token("ident", i, j)
            i = j
            continue

        # Semicolon
        if ch == ';':
            add_token("semicolon", i, i + 1)
            i += 1
            continue

        # Other single-char symbols
        if ch in '()[],.':
            add_token(ch, i, i + 1)
            i += 1
            continue

        # Skip whitespace and other characters
        i += 1

    return toks


def get_line_number(src: str, pos: int) -> int:
    """Get line number for a position in source code (1-based)."""
    return src[:pos].count('\n') + 1


def read_identifier(tokens: List[Token], k: int) -> Tuple[Optional[str], int]:
    """
    Read an identifier from the token stream.
    
    Returns:
        Tuple of (identifier_text, next_index)
    """
    if k < len(tokens) and tokens[k].kind == "ident":
        text = tokens[k].text.strip('"')
        return text, k + 1
    return None, k


def find_package_units(src: str) -> List[PlSqlUnit]:
    """
    Find package specifications and bodies.
    
    Returns:
        List of PlSqlUnit objects for packages
    """
    toks = tokenize_plsql(src)
    results: List[PlSqlUnit] = []
    i = 0

    while i < len(toks):
        # Look for CREATE [OR REPLACE] PACKAGE [BODY] <name>
        if toks[i].kind == "create":
            j = i + 1
            
            # Skip OR REPLACE
            if j < len(toks) - 1 and toks[j].kind == "or" and toks[j + 1].kind == "replace":
                j += 2
            
            # Check for PACKAGE
            if j < len(toks) and toks[j].kind == "package":
                j += 1
                is_body = False
                
                # Check for BODY keyword
                if j < len(toks) and toks[j].kind == "body":
                    is_body = True
                    j += 1
                
                # Get package name
                name, j = read_identifier(toks, j)
                if name:
                    # Find IS/AS
                    start_pos = toks[i].start
                    while j < len(toks) and toks[j].kind not in ("is", "as"):
                        j += 1
                    
                    if j < len(toks):
                        # Find matching END;
                        end_pos = find_matching_end(toks, j + 1, src)
                        if end_pos:
                            unit_type = "package_body" if is_body else "package_spec"
                            results.append(PlSqlUnit(
                                unit_type=unit_type,
                                name=name,
                                start_pos=start_pos,
                                end_pos=end_pos,
                                start_line=get_line_number(src, start_pos),
                                end_line=get_line_number(src, end_pos)
                            ))
        i += 1

    return results


def find_subprograms(src: str, package_name: Optional[str] = None) -> List[PlSqlUnit]:
    """
    Find procedures and functions in PL/SQL source.
    
    Args:
        src: PL/SQL source code
        package_name: If provided, marks subprograms as belonging to this package
        
    Returns:
        List of PlSqlUnit objects for procedures and functions
    """
    toks = tokenize_plsql(src)
    results: List[PlSqlUnit] = []
    i = 0

    while i < len(toks):
        tk = toks[i]
        
        if tk.kind in ("procedure", "function"):
            unit_type = tk.kind
            header_start = tk.start

            # Get the name
            name, j = read_identifier(toks, i + 1)
            if name is None:
                i += 1
                continue

            # Check if this is a body (has IS/AS) or just a declaration
            k = j
            saw_is_or_as = False
            signature_end = k
            
            while k < len(toks):
                if toks[k].kind in ("is", "as"):
                    saw_is_or_as = True
                    signature_end = toks[k].start
                    k += 1
                    break
                if toks[k].kind == "semicolon":
                    signature_end = toks[k].start
                    break
                k += 1

            if not saw_is_or_as:
                # Declaration only; skip
                i = k + 1
                continue

            # Extract signature
            signature = src[header_start:signature_end].strip()

            # Find matching END
            end_pos = find_matching_end(toks, k, src)
            
            if end_pos:
                results.append(PlSqlUnit(
                    unit_type=unit_type,
                    name=name,
                    start_pos=header_start,
                    end_pos=end_pos,
                    start_line=get_line_number(src, header_start),
                    end_line=get_line_number(src, end_pos),
                    signature=signature,
                    package_name=package_name
                ))
                i = k
            else:
                i += 1
        else:
            i += 1

    return results


def find_matching_end(tokens: List[Token], start_idx: int, src: str) -> Optional[int]:
    """
    Find the matching END; for a block starting at start_idx.
    
    Args:
        tokens: List of tokens
        start_idx: Index to start searching from
        src: Original source code
        
    Returns:
        End position in source code, or None if not found
    """
    depth = 0
    i = start_idx

    while i < len(tokens):
        if tokens[i].kind == "begin":
            depth += 1
        elif tokens[i].kind == "end":
            if depth == 0:
                # Find the semicolon
                j = i + 1
                while j < len(tokens) and tokens[j].kind != "semicolon":
                    j += 1
                if j < len(tokens):
                    return tokens[j].end
                return tokens[i].end
            else:
                depth -= 1
        i += 1

    return None


def find_triggers(src: str) -> List[PlSqlUnit]:
    """
    Find trigger definitions in PL/SQL source.
    
    Returns:
        List of PlSqlUnit objects for triggers
    """
    toks = tokenize_plsql(src)
    results: List[PlSqlUnit] = []
    i = 0

    while i < len(toks):
        if toks[i].kind == "create":
            j = i + 1
            
            # Skip OR REPLACE
            if j < len(toks) - 1 and toks[j].kind == "or" and toks[j + 1].kind == "replace":
                j += 2
            
            # Check for TRIGGER
            if j < len(toks) and toks[j].kind == "trigger":
                j += 1
                start_pos = toks[i].start
                
                # Get trigger name
                name, j = read_identifier(toks, j)
                if name:
                    # Find the end (triggers typically end with END; or just ;)
                    # Scan until we find a top-level END or semicolon after the body
                    end_pos = find_trigger_end(toks, j, src)
                    if end_pos:
                        results.append(PlSqlUnit(
                            unit_type="trigger",
                            name=name,
                            start_pos=start_pos,
                            end_pos=end_pos,
                            start_line=get_line_number(src, start_pos),
                            end_line=get_line_number(src, end_pos)
                        ))
        i += 1

    return results


def find_trigger_end(tokens: List[Token], start_idx: int, src: str) -> Optional[int]:
    """Find the end of a trigger definition."""
    # Look for BEGIN...END pattern or just a semicolon
    i = start_idx
    found_begin = False
    
    while i < len(tokens):
        if tokens[i].kind == "begin":
            found_begin = True
            # Find matching END
            return find_matching_end(tokens, i + 1, src)
        elif tokens[i].kind == "semicolon" and not found_begin:
            # Simple trigger without BEGIN block
            return tokens[i].end
        i += 1
    
    return None


def extract_all_units(src: str) -> List[PlSqlUnit]:
    """
    Extract all logical units from PL/SQL source code.
    
    This includes packages, procedures, functions, triggers, etc.
    For package bodies, it also extracts individual subprograms.
    
    Returns:
        List of all PlSqlUnit objects found
    """
    results: List[PlSqlUnit] = []
    
    # Find top-level packages
    packages = find_package_units(src)
    results.extend(packages)
    
    # For each package body, extract subprograms
    for pkg in packages:
        if pkg.unit_type == "package_body":
            pkg_src = src[pkg.start_pos:pkg.end_pos]
            subprograms = find_subprograms(pkg_src, package_name=pkg.name)
            # Adjust positions to be relative to full source
            for subprog in subprograms:
                subprog.start_pos += pkg.start_pos
                subprog.end_pos += pkg.start_pos
                subprog.start_line = get_line_number(src, subprog.start_pos)
                subprog.end_line = get_line_number(src, subprog.end_pos)
            results.extend(subprograms)
    
    # Find standalone procedures and functions
    standalone_subprograms = find_subprograms(src)
    results.extend(standalone_subprograms)
    
    # Find triggers
    triggers = find_triggers(src)
    results.extend(triggers)
    
    return results


def get_unit_source(src: str, unit: PlSqlUnit) -> str:
    """Extract the source code for a specific unit."""
    return src[unit.start_pos:unit.end_pos]
