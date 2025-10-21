"""PL/SQL language support using text-based extraction.

Since tree-sitter-plsql lacks Python bindings, this implementation uses
regex-based text scanning to extract entities. The approach handles:
- Packages (spec and body) as class-like containers
- Procedures and functions with signatures
- Parameter lists and RETURN types
- Leading comment documentation
- Complex PL/SQL syntax (quoted identifiers, nested blocks, etc.)

Note: This module uses mock parser/tree objects to satisfy the BaseLanguage
interface while performing all extraction via text analysis.
"""

from typing import Dict, List, Optional, Any
from tree_sitter import Tree

from ts_tool.languages.base import BaseLanguage
from ts_tool.languages.plsql_parser import MockPlsqlTree
from ts_tool.languages import plsql_scanner


class PlsqlLanguage(BaseLanguage):
    """PL/SQL language implementation using text-based extraction.

    This class provides PL/SQL support for the ace_proto code explorer
    without relying on tree-sitter parsing. Instead, it uses proven
    regex-based text scanning to identify and extract code entities.
    """

    @property
    def language_name(self) -> str:
        """The name of the language.

        Returns:
            'plsql'
        """
        return "plsql"

    def parse(self, code: str) -> Tree:
        """Parse PL/SQL code (returns mock tree).

        Since we don't have tree-sitter grammar, this returns a mock
        tree object that stores the code. Actual extraction happens
        in the other methods using text-based scanning.

        Args:
            code: PL/SQL source code to parse

        Returns:
            MockPlsqlTree containing the code
        """
        return self.parser.parse(code.encode("utf-8"))

    def get_entity_names(self, tree: Tree) -> Dict[str, List[str]]:
        """Get entity names from code.

        Extracts names of packages, procedures, and functions.

        Args:
            tree: Parsed tree (MockPlsqlTree)

        Returns:
            Dict with 'classes' (packages), 'functions' (procedures/functions),
            and 'variables' (currently empty)
        """
        if isinstance(tree, MockPlsqlTree):
            code = tree.code.decode('utf-8')
        else:
            return {"classes": [], "functions": [], "variables": []}

        packages = plsql_scanner.gather_packages(code)
        subprograms = plsql_scanner.gather_subprograms(code)

        return {
            "classes": [p['name'] for p in packages],
            "functions": [s['name'] for s in subprograms],
            "variables": []
        }

    def get_entity_node(self, tree: Tree, entity_type: str, entity_name: str):
        """Get node for specific entity.

        Not implemented for mock tree since we use text-based extraction.

        Args:
            tree: Parsed tree
            entity_type: Type of entity ('class', 'function', etc.)
            entity_name: Name of the entity

        Returns:
            None (not supported with mock tree)
        """
        return None

    def get_documentation(self, node, code: str) -> Optional[str]:
        """Extract documentation from a node.

        For PL/SQL, node is not used since we have a text-based parser.
        Instead, this returns None and documentation is extracted during
        get_public_interface() by the plsql_scanner.

        Args:
            node: Ignored (PL/SQL uses text-based extraction)
            code: The original source code

        Returns:
            None (documentation extracted by plsql_scanner during interface extraction)
        """
        # PL/SQL documentation is extracted by plsql_scanner.gather_subprograms()
        # and plsql_scanner.gather_packages() which find leading comments.
        # It's already attached to entities during get_public_interface().
        return None

    def get_module_docstring(self, tree: Tree, code: str) -> Optional[str]:
        """Extract module-level documentation from file header.

        Looks for leading comments at the top of the file before
        any code begins.

        Args:
            tree: Parsed tree (ignored)
            code: Source code

        Returns:
            Module documentation string, or None if not found
        """
        clean = plsql_scanner.mask_comments_and_strings(code)

        # Find first non-space character
        import re
        first_code = re.search(r"\S", clean)
        cutoff = first_code.start() if first_code else len(code)

        # Extract leading block comment
        k = cutoff
        while k > 1 and code[k - 1].isspace():
            k -= 1

        if k >= 2 and code[k - 2:k] == '*/':
            b = code.rfind('/*', 0, k - 2)
            if b != -1:
                text = code[b + 2:k - 2].strip()
                if text:
                    return text

        # Extract leading -- lines
        lines = []
        pos = 0
        while pos < cutoff:
            nxt = code.find('\n', pos)
            if nxt == -1 or nxt > cutoff:
                nxt = cutoff
            line = code[pos:nxt].strip()
            if line.startswith('--'):
                lines.append(line[2:].lstrip())
                pos = nxt + 1
            elif not line:
                pos = nxt + 1
            else:
                break

        if lines:
            return '\n'.join(lines).strip() or None

        return None

    def get_imports(self, tree: Tree, code: str) -> List[str]:
        """Extract import statements.

        PL/SQL doesn't have imports like other languages.

        Args:
            tree: Parsed tree (ignored)
            code: Source code (ignored)

        Returns:
            Empty list (PL/SQL has no imports)
        """
        return []

    def get_public_interface(self, tree: Tree, code: str) -> Dict[str, Any]:
        """Extract public interface: packages as classes, procedures/functions, variables.

        This is the main extraction method that returns all public entities
        from the PL/SQL code.

        Args:
            tree: Parsed tree (MockPlsqlTree)
            code: Source code

        Returns:
            Dict with keys:
            - 'classes': List of package specs/bodies (with name, line_range,
              byte_range, docstring, methods - subprograms linked to package)
            - 'functions': List of procedures/functions (with name, line_range,
              byte_range, docstring, signature, return_type, package_name)
            - 'variables': List of global variables (with name, line_range,
              byte_range, var_type, default_value, package_name)
        """
        if isinstance(tree, MockPlsqlTree):
            code = tree.code.decode('utf-8')

        line_starts = plsql_scanner.build_line_index(code)

        # Extract packages as classes
        packages = plsql_scanner.gather_packages(code)
        classes: List[Dict[str, Any]] = []

        for pkg in packages:
            # Only include package bodies (skip specs since they're just declarations)
            # Package bodies contain the actual implementation
            if not pkg.get("is_body", False):
                continue

            sl, sc = plsql_scanner.byte_to_line_col(pkg["start"], line_starts)
            el, ec = plsql_scanner.byte_to_line_col(pkg["end"], line_starts)

            classes.append({
                "name": pkg["name"],
                "line_range": ((sl, sc), (el, ec)),
                "byte_range": (pkg["start"], pkg["end"]),
                "docstring": pkg.get("docstring"),
                "methods": [],  # Will be populated below
                "is_body": pkg.get("is_body", False)
            })

        # Extract procedures/functions and link to packages
        subprograms = plsql_scanner.gather_subprograms(code)
        functions: List[Dict[str, Any]] = []

        for sub in subprograms:
            sl, sc = plsql_scanner.byte_to_line_col(sub["start"], line_starts)
            el, ec = plsql_scanner.byte_to_line_col(sub["end"], line_starts)

            # Determine if this subprogram is inside a package
            package_name = None
            for pkg in packages:
                if pkg["start"] < sub["start"] < pkg["end"]:
                    package_name = pkg["name"]
                    # Add to package's methods list
                    for cls in classes:
                        if cls["name"] == package_name:
                            cls["methods"].append({
                                "name": sub["name"],
                                "signature": sub["signature"],
                                "line_range": ((sl, sc), (el, ec)),
                                "byte_range": (sub["start"], sub["end"]),
                                "return_type": sub.get("return_type"),
                                "docstring": sub.get("docstring")
                            })
                    break

            func_dict = {
                "name": sub["name"],
                "line_range": ((sl, sc), (el, ec)),
                "byte_range": (sub["start"], sub["end"]),
                "docstring": sub.get("docstring"),
                "signature": sub["signature"],
                "return_type": sub.get("return_type")
            }

            if package_name:
                func_dict["package_name"] = package_name

            functions.append(func_dict)

        # Extract global variables and link to packages
        vars_list = plsql_scanner.gather_variables(code)
        variables: List[Dict[str, Any]] = []

        for var in vars_list:
            sl, sc = plsql_scanner.byte_to_line_col(var["start"], line_starts)
            el, ec = plsql_scanner.byte_to_line_col(var["end"], line_starts)

            # Determine if this variable is inside a package
            package_name = None
            for pkg in packages:
                if pkg["start"] < var["start"] < pkg["end"]:
                    package_name = pkg["name"]
                    break

            var_dict = {
                "name": var["name"],
                "line_range": ((sl, sc), (el, ec)),
                "byte_range": (var["start"], var["end"]),
                "docstring": var.get("docstring"),
                "type_hint": var["var_type"],  # Map var_type to type_hint for standard API
                "value": var.get("default_value")  # Map default_value to value for standard API
            }

            if package_name:
                var_dict["package_name"] = package_name

            variables.append(var_dict)

        return {
            "classes": classes,
            "functions": functions,
            "variables": variables
        }
