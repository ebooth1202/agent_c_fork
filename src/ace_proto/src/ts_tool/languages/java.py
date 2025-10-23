"""Java language support for tree-sitter code exploration.

This module provides Java-specific functionality for parsing and
extracting information from Java code using tree-sitter.
"""

from typing import Dict, List, Optional, Any, Tuple, Set

from tree_sitter import Node, Tree, Parser

from ts_tool.languages.base import BaseLanguage


class JavaLanguage(BaseLanguage):
    """Java language support for code exploration.

    This class provides Java-specific functionality for parsing and
    extracting information from Java code using tree-sitter.
    """

    # Query for finding classes, interfaces, enums, and annotations
    CLASS_QUERY = """
    (class_declaration
      name: (identifier) @class.name
      body: (class_body) @class.body)

    (interface_declaration
      name: (identifier) @interface.name
      body: (interface_body) @interface.body)

    (enum_declaration
      name: (identifier) @enum.name
      body: (enum_body) @enum.body)

    (annotation_type_declaration
      name: (identifier) @annotation.name
      body: (annotation_type_body) @annotation.body)
    """

    # Query for finding methods and constructors
    FUNCTION_QUERY = """
    (method_declaration
      name: (identifier) @method.name
      parameters: (formal_parameters) @method.params
      body: (block)? @method.body)

    (constructor_declaration
      name: (identifier) @constructor.name
      parameters: (formal_parameters) @constructor.params
      body: (constructor_body) @constructor.body)
    """

    # Query for finding fields and variables
    VARIABLE_QUERY = """
    (field_declaration
      declarator: (variable_declarator
        name: (identifier) @field.name
        value: (_)? @field.value))

    (constant_declaration
      declarator: (variable_declarator
        name: (identifier) @constant.name
        value: (_)? @constant.value))
    """

    # Query for finding import statements
    IMPORT_QUERY = """
    (import_declaration) @import
    """

    # Query for finding comments and Javadoc
    DOCSTRING_QUERY = """
    (block_comment) @comment
    (line_comment) @comment
    """

    # Query for finding package declaration
    PACKAGE_QUERY = """
    (package_declaration) @package
    """

    # Java access modifiers to check for public entities
    PUBLIC_MODIFIERS = ["public"]

    @property
    def language_name(self) -> str:
        """The name of the language."""
        return "java"

    def parse(self, code: str) -> Tree:
        """Parse the given Java code string.

        Args:
            code: The Java source code to parse.

        Returns:
            The parsed syntax tree.
        """
        return self.parser.parse(bytes(code, 'utf8'))

    def get_entity_names(self, tree: Tree) -> Dict[str, List[str]]:
        """Get all named entities from the Java syntax tree.

        Args:
            tree: The parsed syntax tree.

        Returns:
            A dictionary with entity types as keys and lists of entity names as values.
        """
        result = {
            'classes': [],
            'interfaces': [],
            'enums': [],
            'annotations': [],
            'functions': [],
            'methods': [],
            'variables': []
        }

        # Extract class, interface, enum, and annotation names
        class_query = self.get_query(self.CLASS_QUERY)
        for match in class_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id == "class.name":
                    class_name = capture_nodes[0].text.decode('utf8')
                    if self._is_public_entity(capture_nodes[0].parent, tree):
                        result['classes'].append(class_name)
                elif capture_id == "interface.name":
                    interface_name = capture_nodes[0].text.decode('utf8')
                    if self._is_public_entity(capture_nodes[0].parent, tree):
                        result['interfaces'].append(interface_name)
                elif capture_id == "enum.name":
                    enum_name = capture_nodes[0].text.decode('utf8')
                    if self._is_public_entity(capture_nodes[0].parent, tree):
                        result['enums'].append(enum_name)
                elif capture_id == "annotation.name":
                    annotation_name = capture_nodes[0].text.decode('utf8')
                    if self._is_public_entity(capture_nodes[0].parent, tree):
                        result['annotations'].append(annotation_name)

        # Extract method names
        function_query = self.get_query(self.FUNCTION_QUERY)
        for match in function_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id in ["method.name", "constructor.name"]:
                    node = capture_nodes[0]
                    method_name = node.text.decode('utf8')
                    if self._is_public_entity(node.parent, tree):
                        result['methods'].append(method_name)

        # Extract field names
        variable_query = self.get_query(self.VARIABLE_QUERY)
        for match in variable_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id in ["field.name", "constant.name"]:
                    node = capture_nodes[0]
                    var_name = node.text.decode('utf8')
                    if self._is_public_entity(node.parent.parent, tree):
                        result['variables'].append(var_name)

        return result

    def get_entity_node(self, tree: Tree, entity_type: str, entity_name: str) -> Optional[Node]:
        """Get the syntax node for a specific named entity.

        Args:
            tree: The parsed syntax tree.
            entity_type: The type of entity to find ('class', 'method', etc.).
            entity_name: The name of the entity to find.

        Returns:
            The syntax node for the entity, or None if not found.
        """
        return self.find_entity(tree, entity_type, entity_name)

    def find_entity(self, tree: Tree, entity_type: str, entity_name: str) -> Optional[Node]:
        """Find a specific entity in the Java syntax tree.

        Args:
            tree: The parsed syntax tree.
            entity_type: The type of entity to find ('class', 'method', etc.).
            entity_name: The name of the entity to find.

        Returns:
            The tree-sitter node for the entity, or None if not found.
        """
        if entity_type == 'class':
            class_query = self.get_query(self.CLASS_QUERY)
            for match in class_query.matches(tree.root_node):
                for capture_id, capture_nodes in match[1].items():
                    if capture_id == "class.name" and capture_nodes[0].text.decode('utf8') == entity_name:
                        return capture_nodes[0].parent

        elif entity_type == 'interface':
            class_query = self.get_query(self.CLASS_QUERY)
            for match in class_query.matches(tree.root_node):
                for capture_id, capture_nodes in match[1].items():
                    if capture_id == "interface.name" and capture_nodes[0].text.decode('utf8') == entity_name:
                        return capture_nodes[0].parent

        elif entity_type == 'enum':
            class_query = self.get_query(self.CLASS_QUERY)
            for match in class_query.matches(tree.root_node):
                for capture_id, capture_nodes in match[1].items():
                    if capture_id == "enum.name" and capture_nodes[0].text.decode('utf8') == entity_name:
                        return capture_nodes[0].parent

        elif entity_type == 'annotation':
            class_query = self.get_query(self.CLASS_QUERY)
            for match in class_query.matches(tree.root_node):
                for capture_id, capture_nodes in match[1].items():
                    if capture_id == "annotation.name" and capture_nodes[0].text.decode('utf8') == entity_name:
                        return capture_nodes[0].parent

        elif entity_type == 'method':
            # For methods, handle format 'ClassName.method_name'
            if '.' in entity_name:
                class_name, method_name = entity_name.split('.', 1)
                class_node = self.find_entity(tree, 'class', class_name)
                if class_node:
                    body_node = None
                    for child in class_node.children:
                        if child.type == 'class_body':
                            body_node = child
                            break

                    if body_node:
                        function_query = self.get_query(self.FUNCTION_QUERY)
                        for match in function_query.matches(body_node):
                            for capture_id, capture_nodes in match[1].items():
                                if capture_id in ["method.name", "constructor.name"] and \
                                   capture_nodes[0].text.decode('utf8') == method_name:
                                    return capture_nodes[0].parent
            else:
                # Search for top-level or any method with this name
                function_query = self.get_query(self.FUNCTION_QUERY)
                for match in function_query.matches(tree.root_node):
                    for capture_id, capture_nodes in match[1].items():
                        if capture_id in ["method.name", "constructor.name"] and \
                           capture_nodes[0].text.decode('utf8') == entity_name:
                            return capture_nodes[0].parent

        elif entity_type in ['variable', 'field', 'constant']:
            variable_query = self.get_query(self.VARIABLE_QUERY)
            for match in variable_query.matches(tree.root_node):
                for capture_id, capture_nodes in match[1].items():
                    if capture_id in ["field.name", "constant.name"] and \
                       capture_nodes[0].text.decode('utf8') == entity_name:
                        return capture_nodes[0].parent.parent

        return None

    def get_module_docstring(self, tree: Tree, code: str) -> Optional[str]:
        """Extract the module-level docstring from a Java file.

        Args:
            tree: The parsed syntax tree.
            code: The original source code.

        Returns:
            The module docstring, or None if not found.
        """
        doc_query = self.get_query(self.DOCSTRING_QUERY)

        # Find the first comment at the beginning of the file
        javadoc_comments = []
        first_comment = None

        for match in doc_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id == "comment":
                    node = capture_nodes[0]
                    # Check if it's at the beginning of the file
                    if node.start_point[0] < 5:  # Within first 5 lines
                        comment_text = self.get_node_text(node, code)
                        # Check if it's a Javadoc comment (starts with /**)
                        if comment_text.strip().startswith("/**"):
                            javadoc_comments.append((node.start_point[0], comment_text))
                        # If we haven't found a regular comment yet, store this one
                        elif first_comment is None and node.type == 'block_comment':
                            first_comment = node

        # Prefer Javadoc over normal comments
        if javadoc_comments:
            # Sort by line number to ensure correct order
            javadoc_comments.sort(key=lambda x: x[0])
            combined_doc = "\n".join([text for _, text in javadoc_comments])
            return self._clean_javadoc(combined_doc)
        elif first_comment:
            return self._clean_comment(self.get_node_text(first_comment, code))

        return None

    def get_documentation(self, node: Node, code: str, tree: Tree = None) -> Optional[str]:
        """Extract documentation for a specific node.

        Args:
            node: The node to extract documentation for.
            code: The original source code.
            tree: The parsed syntax tree.

        Returns:
            The documentation for the node, or None if not found.
        """
        start_line = node.start_point[0]

        # Search for comments above the node that might be Javadoc
        javadoc_comments = []
        doc_query = self.get_query(self.DOCSTRING_QUERY)

        root_node = tree.root_node if tree else None
        if root_node is None:
            return None

        # Find all comments
        for match in doc_query.matches(root_node):
            for capture_id, capture_nodes in list(match[1].items()):
                if capture_id == "comment":
                    comment_node = capture_nodes[0]
                    comment_end_line = comment_node.end_point[0]
                    comment_text = self.get_node_text(comment_node, code)

                    # Check if this comment is just before our node
                    if comment_end_line < start_line and comment_end_line >= start_line - 10:
                        # Check if it's a Javadoc comment (starts with /**)
                        if comment_text.strip().startswith("/**"):
                            javadoc_comments.append((comment_end_line, comment_text))
                        # Regular comment that's immediately before the node
                        elif comment_end_line == start_line - 1:
                            return self._clean_comment(comment_text)

        # If we found Javadoc comments, combine them and return
        if javadoc_comments:
            # Sort by line number to ensure correct order
            javadoc_comments.sort(key=lambda x: x[0])
            combined_doc = "\n".join([text for _, text in javadoc_comments])
            return self._clean_javadoc(combined_doc)

        return None

    def get_imports(self, tree: Tree, code: str) -> List[str]:
        """Extract import statements from a Java file.

        Args:
            tree: The parsed syntax tree.
            code: The original source code.

        Returns:
            A list of import statements.
        """
        imports = []
        import_query = self.get_query(self.IMPORT_QUERY)

        for match in import_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id == "import":
                    imports.append(self.get_node_text(capture_nodes[0], code))

        return imports

    def get_public_interface(self, tree: Tree, code: str) -> Dict[str, Any]:
        """Extract the public interface from a Java syntax tree.

        Args:
            tree: The parsed syntax tree.
            code: The original source code.

        Returns:
            A dictionary representing the public interface.
        """
        result = {
            'classes': [],
            'interfaces': [],
            'enums': [],
            'annotations': [],
            'functions': [],
            'variables': []
        }

        # Extract classes, interfaces, enums, and annotations with their members
        class_query = self.get_query(self.CLASS_QUERY)
        for match in class_query.matches(tree.root_node):
            class_info = {}
            class_node = None
            class_name = None
            entity_type = None

            for capture_id, capture_nodes in match[1].items():
                if capture_id == "class.name":
                    class_name = capture_nodes[0].text.decode('utf8')
                    if not self._is_public_entity(capture_nodes[0].parent, tree):
                        continue

                    class_node = capture_nodes[0].parent
                    entity_type = 'classes'

                    # Get superclass and interfaces
                    base_classes = self._get_base_classes(class_node, code)

                    class_info = {
                        'name': class_name,
                        'type': 'class',
                        'base_classes': base_classes,
                        'methods': [],
                        'fields': [],
                        'line_range': self.get_entity_range(class_node),
                        'byte_range': self.get_entity_byte_range(class_node),
                        'docstring': self.get_documentation(class_node, code, tree)
                    }

                elif capture_id == "interface.name":
                    class_name = capture_nodes[0].text.decode('utf8')
                    if not self._is_public_entity(capture_nodes[0].parent, tree):
                        continue

                    class_node = capture_nodes[0].parent
                    entity_type = 'interfaces'

                    # Get extended interfaces
                    base_classes = self._get_base_classes(class_node, code)

                    class_info = {
                        'name': class_name,
                        'type': 'interface',
                        'base_classes': base_classes,
                        'methods': [],
                        'line_range': self.get_entity_range(class_node),
                        'byte_range': self.get_entity_byte_range(class_node),
                        'docstring': self.get_documentation(class_node, code, tree)
                    }

                elif capture_id == "enum.name":
                    class_name = capture_nodes[0].text.decode('utf8')
                    if not self._is_public_entity(capture_nodes[0].parent, tree):
                        continue

                    class_node = capture_nodes[0].parent
                    entity_type = 'enums'

                    class_info = {
                        'name': class_name,
                        'type': 'enum',
                        'constants': [],
                        'methods': [],
                        'line_range': self.get_entity_range(class_node),
                        'byte_range': self.get_entity_byte_range(class_node),
                        'docstring': self.get_documentation(class_node, code, tree)
                    }

                elif capture_id == "annotation.name":
                    class_name = capture_nodes[0].text.decode('utf8')
                    if not self._is_public_entity(capture_nodes[0].parent, tree):
                        continue

                    class_node = capture_nodes[0].parent
                    entity_type = 'annotations'

                    class_info = {
                        'name': class_name,
                        'type': 'annotation',
                        'methods': [],
                        'line_range': self.get_entity_range(class_node),
                        'byte_range': self.get_entity_byte_range(class_node),
                        'docstring': self.get_documentation(class_node, code, tree)
                    }

            # If we found a valid entity, extract its members
            if class_node and class_info:
                body_node = None
                for child in class_node.children:
                    if child.type in ['class_body', 'interface_body', 'enum_body', 'annotation_type_body']:
                        body_node = child
                        break

                if body_node:
                    # Get methods and constructors
                    function_query = self.get_query(self.FUNCTION_QUERY)
                    for method_match in function_query.matches(body_node):
                        for method_capture_id, method_capture_nodes in method_match[1].items():
                            if method_capture_id in ["method.name", "constructor.name"]:
                                method_node = method_capture_nodes[0]
                                method_name = method_node.text.decode('utf8')
                                method_def_node = method_node.parent

                                if not self._is_public_entity(method_def_node, tree):
                                    continue

                                # Get parameters for method signature
                                params_node = None
                                return_type = None
                                for child in method_def_node.children:
                                    if child.type == 'formal_parameters':
                                        params_node = child
                                    elif child.type in ['type_identifier', 'integral_type', 'floating_point_type',
                                                       'boolean_type', 'void_type', 'generic_type', 'array_type']:
                                        return_type = self.get_node_text(child, code)

                                params_text = self.get_node_text(params_node, code) if params_node else "()"

                                method_info = {
                                    'name': method_name,
                                    'signature': f"{method_name}{params_text}",
                                    'return_type': return_type,
                                    'line_range': self.get_entity_range(method_def_node),
                                    'byte_range': self.get_entity_byte_range(method_def_node),
                                    'docstring': self.get_documentation(method_def_node, code, tree)
                                }

                                class_info['methods'].append(method_info)

                    # Get fields for classes and enums
                    if entity_type in ['classes', 'enums']:
                        variable_query = self.get_query(self.VARIABLE_QUERY)
                        for var_match in variable_query.matches(body_node):
                            for var_capture_id, var_capture_nodes in var_match[1].items():
                                if var_capture_id in ["field.name", "constant.name"]:
                                    var_node = var_capture_nodes[0]
                                    field_name = var_node.text.decode('utf8')
                                    field_def_node = var_node.parent.parent

                                    if not self._is_public_entity(field_def_node, tree):
                                        continue

                                    # Get field type
                                    field_type = ""
                                    for child in field_def_node.children:
                                        if child.type in ['type_identifier', 'integral_type', 'floating_point_type',
                                                         'boolean_type', 'generic_type', 'array_type']:
                                            field_type = self.get_node_text(child, code)
                                            break

                                    field_info = {
                                        'name': field_name,
                                        'type_hint': field_type,
                                        'line_range': self.get_entity_range(field_def_node),
                                        'byte_range': self.get_entity_byte_range(field_def_node),
                                        'docstring': self.get_documentation(field_def_node, code, tree)
                                    }

                                    if entity_type == 'enums' and 'constants' in class_info:
                                        class_info['constants'].append(field_info)
                                    elif 'fields' in class_info:
                                        class_info['fields'].append(field_info)

                    # Get enum constants
                    if entity_type == 'enums':
                        for child in body_node.children:
                            if child.type == 'enum_constant':
                                name_node = None
                                for ec_child in child.children:
                                    if ec_child.type == 'identifier':
                                        name_node = ec_child
                                        break

                                if name_node:
                                    constant_name = name_node.text.decode('utf8')
                                    constant_info = {
                                        'name': constant_name,
                                        'line_range': self.get_entity_range(child),
                                        'byte_range': self.get_entity_byte_range(child),
                                        'docstring': self.get_documentation(child, code, tree)
                                    }

                                    class_info['constants'].append(constant_info)

                # Add to the appropriate collection
                result[entity_type].append(class_info)

        # Extract top-level variables (typically constants)
        variable_query = self.get_query(self.VARIABLE_QUERY)
        for match in variable_query.matches(tree.root_node):
            for capture_id, capture_nodes in match[1].items():
                if capture_id in ["field.name", "constant.name"]:
                    node = capture_nodes[0]
                    var_node = node.parent.parent

                    # Only process top-level variables
                    if var_node.parent != tree.root_node:
                        continue

                    if not self._is_public_entity(var_node, tree):
                        continue

                    var_name = node.text.decode('utf8')

                    # Get variable type
                    var_type = ""
                    for child in var_node.children:
                        if child.type in ['type_identifier', 'integral_type', 'floating_point_type',
                                         'boolean_type', 'generic_type', 'array_type']:
                            var_type = self.get_node_text(child, code)
                            break

                    result['variables'].append({
                        'name': var_name,
                        'type_hint': var_type,
                        'line_range': self.get_entity_range(var_node),
                        'byte_range': self.get_entity_byte_range(var_node),
                        'docstring': self.get_documentation(var_node, code, tree)
                    })

        return result

    def _is_public_entity(self, node: Node, tree: Tree = None) -> bool:
        """Check if an entity is public.

        Args:
            node: The entity node to check.
            tree: The parsed syntax tree.

        Returns:
            True if the entity is public, False otherwise.
        """
        # Check modifiers
        for child in node.children:
            if child.type == 'modifiers':
                modifiers_text = child.text.decode('utf8')
                if 'public' in modifiers_text:
                    return True
                # If it has private or protected, it's not public
                if 'private' in modifiers_text or 'protected' in modifiers_text:
                    return False

        # Interface members are public by default
        parent = node.parent
        if parent and parent.type in ['interface_body', 'annotation_type_body']:
            return True

        # For package-private (default access), we'll exclude them
        return False

    def _get_base_classes(self, node: Node, code: str) -> List[str]:
        """Extract base classes/interfaces for a class or interface.

        Args:
            node: The class or interface node.
            code: The original source code.

        Returns:
            A list of base class/interface names.
        """
        base_classes = []

        for child in node.children:
            if child.type == 'superclass':
                # extends clause
                for sc_child in child.children:
                    if sc_child.type in ['type_identifier', 'generic_type']:
                        base_classes.append(self.get_node_text(sc_child, code))
            elif child.type == 'super_interfaces':
                # implements clause
                for si_child in child.children:
                    if si_child.type == 'type_list':
                        for tl_child in si_child.children:
                            if tl_child.type in ['type_identifier', 'generic_type']:
                                base_classes.append(self.get_node_text(tl_child, code))
            elif child.type == 'extends_interfaces':
                # extends clause for interfaces
                for ei_child in child.children:
                    if ei_child.type == 'type_list':
                        for tl_child in ei_child.children:
                            if tl_child.type in ['type_identifier', 'generic_type']:
                                base_classes.append(self.get_node_text(tl_child, code))

        return base_classes

    def _clean_javadoc(self, doc_text: str) -> str:
        """Clean Javadoc comments.

        Args:
            doc_text: The raw Javadoc text.

        Returns:
            The cleaned documentation text.
        """
        if not doc_text:
            return ""

        # Remove the Javadoc markers
        lines = doc_text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            # Remove /** and */ markers
            if line.startswith('/**'):
                line = line[3:].strip()
            if line.endswith('*/'):
                line = line[:-2].strip()
            # Remove * prefix from each line
            if line.startswith('*'):
                line = line[1:].strip()

            cleaned_lines.append(line)

        # Remove empty lines from beginning and end
        while cleaned_lines and not cleaned_lines[0]:
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()

        return '\n'.join(cleaned_lines)

    def _clean_comment(self, doc_text: str) -> str:
        """Clean regular comment documentation.

        Args:
            doc_text: The raw comment text.

        Returns:
            The cleaned comment text.
        """
        if not doc_text:
            return ""

        # Remove the comment markers
        lines = doc_text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            # Remove // prefix from each line
            if line.startswith('//'):
                line = line[2:].strip()
            # Remove /* and */ markers
            if line.startswith('/*'):
                line = line[2:].strip()
            if line.endswith('*/'):
                line = line[:-2].strip()
            # Remove * prefix from each line in block comments
            if line.startswith('*'):
                line = line[1:].strip()

            cleaned_lines.append(line)

        # Remove empty lines from beginning and end
        while cleaned_lines and not cleaned_lines[0]:
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()

        return '\n'.join(cleaned_lines)
