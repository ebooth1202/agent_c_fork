"""Tests for the ts_tool API module.

Tests core API functionality including:
- Language detection
- Code summary generation
- Public interface extraction
- Entity retrieval
- Format options (dict, json, yaml, markdown)
"""

import pytest
import json
import yaml as yaml_lib
from ts_tool import api
from .conftest import assert_successful_result


class TestLanguageDetection:
    """Tests for language detection functionality."""

    def test_detect_python_from_content(self):
        """Test Python detection from code content."""
        code = "import sys\ndef foo(): pass"
        detected = api.detect_language(code)
        assert detected == 'python'

    def test_detect_python_from_filename(self):
        """Test Python detection from filename."""
        code = "x = 1"
        detected = api.detect_language(code, "script.py")
        assert detected == 'python'

    def test_detect_java_from_content(self):
        """Test Java detection from code content."""
        code = "package com.example; public class Test {}"
        detected = api.detect_language(code)
        assert detected == 'java'

    def test_detect_java_from_filename(self):
        """Test Java detection from filename."""
        code = "class Test {}"
        detected = api.detect_language(code, "Test.java")
        assert detected == 'java'

    def test_detect_csharp_from_content(self):
        """Test C# detection from code content."""
        code = "using System; namespace Test { }"
        detected = api.detect_language(code)
        assert detected == 'c_sharp'

    def test_detect_csharp_from_filename(self):
        """Test C# detection from filename."""
        code = "class Test {}"
        detected = api.detect_language(code, "Test.cs")
        assert detected == 'c_sharp'

    def test_detect_plsql_from_content(self):
        """Test PL/SQL detection from code content."""
        code = "CREATE OR REPLACE PROCEDURE test IS BEGIN NULL; END;"
        detected = api.detect_language(code)
        assert detected == 'plsql'


class TestCodeSummary:
    """Tests for code summary functionality."""

    def test_get_summary_dict_format(self, python_simple_code):
        """Test getting code summary in dict format."""
        result = api.get_code_summary(python_simple_code, 'python', format='dict')

        assert_successful_result(result)
        assert result['language'] == 'python'
        assert result['class_count'] == 1
        assert result['function_count'] == 1
        assert 'Calculator' in result['class_names']
        assert 'hello_world' in result['function_names']

    def test_get_summary_json_format(self, python_simple_code):
        """Test getting code summary in JSON format."""
        result = api.get_code_summary(python_simple_code, 'python', format='json')

        # Should be valid JSON string
        parsed = json.loads(result)
        assert parsed['successful'] is True
        assert parsed['language'] == 'python'

    def test_get_summary_yaml_format(self, python_simple_code):
        """Test getting code summary in YAML format."""
        result = api.get_code_summary(python_simple_code, 'python', format='yaml')

        # Should be valid YAML string
        parsed = yaml_lib.safe_load(result)
        assert parsed['successful'] is True
        assert parsed['language'] == 'python'

    def test_get_summary_markdown_format(self, python_simple_code):
        """Test getting code summary in Markdown format."""
        result = api.get_code_summary(python_simple_code, 'python', format='markdown')

        # Should be Markdown string
        assert isinstance(result, str)
        assert '**Language:**' in result or 'Language:' in result

    def test_get_summary_with_documentation(self):
        """Test summary correctly identifies documented code."""
        code = '''
def documented_function():
    """This function has documentation."""
    pass
'''
        result = api.get_code_summary(code, 'python', format='dict')
        assert_successful_result(result)
        assert result['has_documentation'] is True


class TestPublicInterface:
    """Tests for public interface extraction."""

    def test_get_public_interface_python(self, python_simple_code):
        """Test extracting public interface from Python code."""
        result = api.get_public_interface(python_simple_code, 'python', format='dict')

        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['function_count'] == 1

        # Check class
        classes = result['public_classes']
        assert len(classes) == 1
        assert classes[0]['name'] == 'Calculator'
        assert len(classes[0]['methods']) == 2

    def test_get_public_interface_excludes_private(self):
        """Test that private entities are excluded from public interface."""
        code = '''
def public_function():
    pass

def _private_function():
    pass

class PublicClass:
    pass

class _PrivateClass:
    pass
'''
        result = api.get_public_interface(code, 'python', format='dict')

        assert_successful_result(result)
        assert result['function_count'] == 1
        assert result['class_count'] == 1


class TestEntityRetrieval:
    """Tests for specific entity retrieval."""

    def test_get_entity_class_full_detail(self, python_simple_code):
        """Test getting a class entity with full detail."""
        result = api.get_entity(
            python_simple_code,
            'class',
            'Calculator',
            detail_level='full',
            language='python',
            format='dict'
        )

        assert_successful_result(result)
        assert result['entity_type'] == 'class'
        entity = result['entity']
        assert entity['name'] == 'Calculator'
        assert 'source_code' in result

    def test_get_entity_function_signature(self, python_simple_code):
        """Test getting a function entity with signature detail."""
        result = api.get_entity(
            python_simple_code,
            'function',
            'hello_world',
            detail_level='signature',
            language='python',
            format='dict'
        )

        assert_successful_result(result)
        entity = result['entity']
        assert entity['name'] == 'hello_world'
        assert 'signature' in entity

    def test_get_entity_method(self, python_simple_code):
        """Test getting a method entity."""
        result = api.get_entity(
            python_simple_code,
            'method',
            'Calculator.add',
            detail_level='signature',
            language='python',
            format='dict'
        )

        assert_successful_result(result)
        entity = result['entity']
        assert entity['name'] == 'add'

    def test_get_entity_not_found(self, python_simple_code):
        """Test getting an entity that doesn't exist."""
        result = api.get_entity(
            python_simple_code,
            'function',
            'nonexistent_function',
            language='python',
            format='dict'
        )

        assert result['successful'] is False
        assert 'not found' in result['error_message'].lower()


class TestSourceCodeRetrieval:
    """Tests for source code retrieval utilities."""

    def test_get_source_code(self, python_simple_code):
        """Test getting source code for an entity."""
        source = api.get_source_code(
            python_simple_code,
            'function',
            'hello_world',
            language='python'
        )

        assert source is not None
        assert 'def hello_world' in source
        assert 'Hello, World!' in source

    def test_get_signature(self, python_simple_code):
        """Test getting signature for an entity."""
        signature = api.get_signature(
            python_simple_code,
            'function',
            'hello_world',
            language='python'
        )

        assert signature is not None
        assert 'hello_world' in signature

    def test_get_documentation(self, python_simple_code):
        """Test getting documentation for an entity."""
        doc = api.get_documentation(
            python_simple_code,
            'function',
            'hello_world',
            language='python'
        )

        assert doc is not None
        assert 'Say hello' in doc


class TestExploreCode:
    """Tests for full code exploration."""

    def test_explore_code_dict_format(self, python_simple_code):
        """Test exploring code in dict format."""
        result = api.explore_code(python_simple_code, 'python', format='dict')

        assert_successful_result(result)
        module = result['module']
        assert module['language'] == 'python'
        assert len(module['classes']) == 1
        assert len(module['functions']) == 1

    def test_explore_code_with_imports(self):
        """Test that imports are captured during exploration."""
        code = '''
import sys
import os
from typing import List

def test():
    pass
'''
        result = api.explore_code(code, 'python', format='dict')

        assert_successful_result(result)
        module = result['module']
        assert len(module['imports']) > 0


class TestSupportedLanguages:
    """Tests for supported languages query."""

    def test_get_supported_languages(self):
        """Test getting list of supported languages."""
        languages = api.get_supported_languages()

        assert isinstance(languages, list)
        assert 'python' in languages
        assert 'java' in languages
        assert 'c_sharp' in languages
        assert 'plsql' in languages
        assert 'javascript' in languages


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_language(self):
        """Test handling of invalid language."""
        result = api.get_code_summary("code", 'invalid_lang', format='dict')
        assert result['successful'] is False

    def test_invalid_code(self):
        """Test handling of invalid/unparseable code."""
        # This should not crash, but may return empty results
        result = api.get_code_summary("@#$%^&*()", 'python', format='dict')
        # Should complete but with 0 entities found
        assert 'class_count' in result

    def test_invalid_format(self, python_simple_code):
        """Test handling of invalid format parameter."""
        with pytest.raises(ValueError):
            api.get_entity(
                python_simple_code,
                'function',
                'hello_world',
                language='python',
                format='invalid_format'
            )
