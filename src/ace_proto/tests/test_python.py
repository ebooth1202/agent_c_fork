"""Tests for Python language support.

Tests Python-specific parsing including:
- Classes and methods
- Functions with type hints
- Decorators
- Properties
- Module-level variables
- Docstrings (multiple formats)
"""

import pytest
from ts_tool import api
from .conftest import assert_successful_result, assert_has_entity


class TestPythonClasses:
    """Tests for Python class parsing."""

    def test_simple_class(self):
        """Test parsing a simple class."""
        code = '''
class MyClass:
    """A simple class."""
    pass
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'MyClass'

    def test_class_with_methods(self, python_simple_code):
        """Test parsing a class with methods."""
        result = api.get_public_interface(python_simple_code, 'python', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        assert calc_class['name'] == 'Calculator'
        assert len(calc_class['methods']) == 2
        assert_has_entity(calc_class['methods'], 'add', 'method')
        assert_has_entity(calc_class['methods'], 'multiply', 'method')

    def test_class_with_init(self):
        """Test parsing a class with __init__ method."""
        code = '''
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        # __init__ is private, should not appear in public interface
        method_names = [m['name'] for m in person_class['methods']]
        assert 'greet' in method_names


class TestPythonFunctions:
    """Tests for Python function parsing."""

    def test_simple_function(self, python_simple_code):
        """Test parsing a simple function."""
        result = api.get_public_interface(python_simple_code, 'python', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        func = result['public_functions'][0]
        assert func['name'] == 'hello_world'

    def test_function_with_type_hints(self):
        """Test parsing functions with type hints."""
        code = '''
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        result = api.get_entity(code, 'function', 'add_numbers', 'signature', 'python', format='dict')
        assert_successful_result(result)

        entity = result['entity']
        assert 'int' in entity['signature']
        assert entity['return_type'] == 'int'

    def test_function_with_decorators(self):
        """Test parsing functions with decorators."""
        code = '''
@property
def my_property(self):
    return self._value

@staticmethod
def static_method():
    return "static"
'''
        result = api.get_code_summary(code, 'python', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 2


class TestPythonDocstrings:
    """Tests for Python docstring extraction."""

    def test_function_docstring(self):
        """Test extracting function docstring."""
        code = '''
def greet(name):
    """Greet someone by name."""
    print(f"Hello, {name}!")
'''
        doc = api.get_documentation(code, 'function', 'greet', language='python')
        assert doc is not None
        assert 'Greet someone' in doc

    def test_class_docstring(self):
        """Test extracting class docstring."""
        code = '''
class Calculator:
    """
    A calculator for basic arithmetic.

    This class provides methods for addition and multiplication.
    """
    pass
'''
        doc = api.get_documentation(code, 'class', 'Calculator', language='python')
        assert doc is not None
        assert 'calculator' in doc.lower()
        assert 'arithmetic' in doc.lower()

    def test_module_docstring(self):
        """Test extracting module-level docstring."""
        code = '''
"""
This is a module for calculations.

It provides various mathematical operations.
"""

def add(a, b):
    return a + b
'''
        result = api.explore_code(code, 'python', format='dict')
        assert_successful_result(result)

        module = result['module']
        assert module['docstring'] is not None
        assert 'module for calculations' in module['docstring']


class TestPythonVariables:
    """Tests for Python variable parsing."""

    def test_module_level_constants(self):
        """Test parsing module-level constants."""
        code = '''
MAX_SIZE = 100
DEFAULT_NAME = "John"
PI = 3.14159
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)

        constants = result['public_constants']
        assert len(constants) >= 3
        constant_names = [c['name'] for c in constants]
        assert 'MAX_SIZE' in constant_names
        assert 'DEFAULT_NAME' in constant_names
        assert 'PI' in constant_names

    def test_type_annotated_variables(self):
        """Test parsing type-annotated variables."""
        code = '''
count: int = 0
name: str = "test"
items: list[str] = []
'''
        result = api.get_code_summary(code, 'python', format='dict')
        assert_successful_result(result)
        assert result['variable_count'] >= 3


class TestPythonImports:
    """Tests for Python import statement parsing."""

    def test_simple_imports(self):
        """Test parsing simple import statements."""
        code = '''
import os
import sys
from typing import List, Dict
'''
        result = api.explore_code(code, 'python', format='dict')
        assert_successful_result(result)

        imports = result['module']['imports']
        assert len(imports) >= 2
        import_text = ' '.join(imports)
        assert 'os' in import_text
        assert 'sys' in import_text


class TestPythonPrivateMembers:
    """Tests for handling private members in Python."""

    def test_private_methods_excluded(self):
        """Test that private methods are excluded from public interface."""
        code = '''
class MyClass:
    def public_method(self):
        pass

    def _private_method(self):
        pass

    def __dunder_method__(self):
        pass
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        method_names = [m['name'] for m in my_class['methods']]

        assert 'public_method' in method_names
        assert '_private_method' not in method_names
        assert '__dunder_method__' not in method_names

    def test_private_functions_excluded(self):
        """Test that private functions are excluded from public interface."""
        code = '''
def public_function():
    pass

def _private_function():
    pass
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        assert result['public_functions'][0]['name'] == 'public_function'


class TestPythonReturnTypes:
    """Tests for Python return type handling."""

    def test_return_type_extraction(self):
        """Test extraction of return type from type hints."""
        code = '''
def get_number() -> int:
    return 42

def get_name() -> str:
    return "John"

def get_nothing() -> None:
    pass
'''
        result = api.get_public_interface(code, 'python', format='dict')
        assert_successful_result(result)

        functions = result['public_functions']
        assert len(functions) == 3

        # Check return types
        get_number = next(f for f in functions if f['name'] == 'get_number')
        assert get_number['return_type'] == 'int'

        get_name = next(f for f in functions if f['name'] == 'get_name')
        assert get_name['return_type'] == 'str'

        get_nothing = next(f for f in functions if f['name'] == 'get_nothing')
        assert get_nothing['return_type'] == 'None'
