"""Mock parser infrastructure for PL/SQL (no tree-sitter grammar available).

This module provides lightweight mock objects that satisfy the tree-sitter
interface without actually using tree-sitter. All parsing is done via
text-based regex scanning.

Since tree-sitter-plsql lacks Python bindings, we use this mock approach
to integrate PL/SQL support into the ace_proto framework while maintaining
compatibility with the BaseLanguage interface.
"""

from typing import Optional, Tuple, List


class MockPlsqlNode:
    """Mock tree-sitter Node for text-based extraction.

    This class provides the minimal interface expected by BaseLanguage
    methods, but doesn't contain actual parse tree information since
    PL/SQL extraction is done via text scanning.
    """

    def __init__(
        self,
        start_byte: int = 0,
        end_byte: int = 0,
        start_point: Tuple[int, int] = (0, 0),
        end_point: Tuple[int, int] = (0, 0),
        node_type: str = ""
    ):
        """Initialize a mock node.

        Args:
            start_byte: Starting byte position
            end_byte: Ending byte position
            start_point: Starting (line, column) position
            end_point: Ending (line, column) position
            node_type: Type identifier for the node
        """
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.start_point = start_point  # (line, column)
        self.end_point = end_point
        self.type = node_type
        self.children: List['MockPlsqlNode'] = []
        self.text = b""

    def __repr__(self):
        return f"MockPlsqlNode(type={self.type}, {self.start_point}-{self.end_point})"


class MockPlsqlTree:
    """Mock tree-sitter Tree for PL/SQL.

    This class stores the original code and provides a minimal tree interface.
    The actual parsing is done by PlsqlLanguage methods using text scanning.
    """

    def __init__(self, code: bytes):
        """Initialize a mock tree.

        Args:
            code: The source code as bytes
        """
        self.code = code
        self.root_node = MockPlsqlNode(
            start_byte=0,
            end_byte=len(code),
            start_point=(0, 0),
            end_point=(0, 0),  # Will be set if needed
            node_type="source_file"
        )

    def walk(self):
        """Return a tree cursor for traversal.

        Returns:
            MockTreeCursor for minimal tree traversal
        """
        return MockTreeCursor(self.root_node)


class MockTreeCursor:
    """Minimal tree cursor for traversal.

    Provides the interface expected by BaseLanguage.traverse_tree()
    but doesn't actually traverse anything since we use text-based extraction.
    """

    def __init__(self, node: MockPlsqlNode):
        """Initialize cursor at given node.

        Args:
            node: The starting node
        """
        self.node = node

    def goto_first_child(self) -> bool:
        """Attempt to move to first child.

        Returns:
            False (mock nodes have no children)
        """
        return False

    def goto_next_sibling(self) -> bool:
        """Attempt to move to next sibling.

        Returns:
            False (mock nodes have no siblings)
        """
        return False

    def goto_parent(self) -> bool:
        """Attempt to move to parent.

        Returns:
            False (mock cursor doesn't track parent)
        """
        return False


class MockPlsqlParser:
    """Mock parser for PL/SQL that performs text-based extraction.

    This parser doesn't actually parse using tree-sitter. Instead, it
    creates mock tree objects while the actual entity extraction is
    done by PlsqlLanguage methods using regex-based text scanning.
    """

    def __init__(self):
        """Initialize the mock parser."""
        self.language = None  # Not needed for text-based parsing

    def parse(self, code: bytes) -> MockPlsqlTree:
        """Create a mock tree (actual parsing happens in PlsqlLanguage methods).

        Args:
            code: Source code as bytes

        Returns:
            MockPlsqlTree containing the code
        """
        return MockPlsqlTree(code)
