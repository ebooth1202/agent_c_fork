"""Formatter using external Jinja2 template files.

This version loads templates from the filesystem, making them
even easier to edit without touching any Python code.
"""

from typing import Optional, Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

from ts_tool.models.code_entity import ModuleEntity
from ts_tool.models.extraction_result import (
    ExtractionResult, CodeSummaryResult, PublicInterfaceResult, ModuleExtractionResult, EntityExtractionResult
)


class CodeFormatter:
    """Formatter that uses external Jinja2 template files."""

    def __init__(self, template_dir: Optional[str] = None):
        """Initialize the formatter.

        Args:
            template_dir: Directory containing template files.
                         Defaults to 'templates' directory in ts_tool package.
        """
        if template_dir is None:
            # Default to templates directory in ts_tool package (parent of utils)
            template_dir = Path(__file__).parent.parent / 'templates'

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(['html', 'xml'])
        )

    def format_module(self, module: ModuleEntity, source_code: str = "",
                      style: str = 'compact') -> str:
        """Format a module entity as markdown.

        Args:
            module: The module entity to format
            source_code: Optional source code for statistics
            style: Format style ('ultra_compact' or 'compact')

        Returns:
            Formatted markdown string
        """
        # Prepare data in a clean, template-friendly format
        data = self._prepare_module_data(module, source_code)

        # Render using the appropriate template
        template = self.env.get_template(f'context_{style}.jinja2')
        return template.render(**data)

    def format_summary(self, summary: CodeSummaryResult, filename: Optional[str] = None) -> str:
        """Format a code summary result as markdown.

        Args:
            summary: The CodeSummaryResult to format
            filename: Optional filename for display

        Returns:
            Formatted markdown string
        """
        # Prepare data for template
        data = {
            'language': summary.language,
            'filename': filename,
            'total_lines': summary.total_lines,
            'class_count': summary.class_count,
            'function_count': summary.function_count,
            'variable_count': summary.variable_count,
            'class_names': summary.class_names,
            'function_names': summary.function_names,
            'has_documentation': summary.has_documentation
        }

        # Render using the appropriate template
        template = self.env.get_template(f'summary.jinja2')
        return template.render(**data)

    def format_public_interface(self, interface: PublicInterfaceResult,
                                filename: Optional[str] = None) -> str:
        """Format a public interface result as markdown.

        Args:
            interface: The PublicInterfaceResult to format
            filename: Optional filename for display

        Returns:
            Formatted markdown string
        """
        # Prepare data for template
        data = {
            'language': interface.language,
            'filename': filename,
            'class_count': len(interface.public_classes),
            'function_count': len(interface.public_functions),
            'constant_count': len(interface.public_constants),
            'public_classes': [],
            'public_functions': [],
            'public_constants': []
        }

        # Prepare class data
        for cls in interface.public_classes:
            cls_data = {
                'name': cls.name,
                'docstring': self._get_first_line(cls.docstring) if cls.docstring else None,
                'base_classes': cls.base_classes if cls.base_classes else None,
                'method_count': len(cls.methods),
                'methods': []
            }

            # Prepare method data
            for method in cls.methods:
                method_data = {
                    'name': method.name,
                    'signature': method.signature or self._build_signature(method),
                    'return_type': method.return_type,
                    'docstring': self._get_first_line(method.docstring) if method.docstring else None
                }
                cls_data['methods'].append(method_data)

            data['public_classes'].append(cls_data)

        # Prepare function data
        for func in interface.public_functions:
            func_data = {
                'name': func.name,
                'signature': func.signature or self._build_signature(func),
                'return_type': func.return_type,
                'docstring': self._get_first_line(func.docstring) if func.docstring else None
            }
            data['public_functions'].append(func_data)

        # Prepare constant data
        for const in interface.public_constants:
            const_data = {
                'name': const.name,
                'type_hint': const.type_hint,
                'value': self._format_value(const.value)
            }
            data['public_constants'].append(const_data)

        # Render using template
        template = self.env.get_template('public_interface.jinja2')
        return template.render(**data)

    def format_explore(self, explore_result: ModuleExtractionResult,
                      filename: Optional[str] = None, style: str = 'standard') -> str:
        """Format a module exploration result as markdown.

        Args:
            explore_result: The ModuleExtractionResult to format
            filename: Optional filename for display
            style: Format style ('standard' or 'compact')

        Returns:
            Formatted markdown string
        """
        # Prepare data using existing _prepare_module_data method
        module = explore_result.module
        source_code = explore_result.source_code or ""

        data = self._prepare_module_data(module, source_code)

        # Add language and imports which _prepare_module_data doesn't include
        data['language'] = explore_result.language
        data['imports'] = module.imports if module.imports else []

        # Override filename if provided
        if filename:
            data['filename'] = filename

        # Render using the appropriate template
        template = self.env.get_template(f'explore_{style}.jinja2')
        return template.render(**data)

    def format_entity(self, entity_result: EntityExtractionResult,
                     filename: Optional[str] = None) -> str:
        """Format an entity extraction result as markdown.

        Args:
            entity_result: The EntityExtractionResult to format
            filename: Optional filename for display

        Returns:
            Formatted markdown string
        """
        # Extract line numbers from entity
        start_line = 0
        end_line = 0
        if entity_result.entity:
            start_line = entity_result.entity.start_line + 1  # Convert 0-based to 1-based
            end_line = entity_result.entity.end_line + 1

        # Add line numbers to source code if present
        source_with_lines = None
        if entity_result.source_code and entity_result.entity:
            lines = entity_result.source_code.split('\n')
            numbered_lines = [f"{start_line + i:5d}  {line}" for i, line in enumerate(lines)]
            source_with_lines = '\n'.join(numbered_lines)

        # Prepare data for template
        data = {
            'entity_name': entity_result.entity_name,
            'entity_type': entity_result.entity_type,
            'detail_level': entity_result.detail_level.value if hasattr(entity_result.detail_level, 'value') else entity_result.detail_level,
            'entity': entity_result.entity.to_dict() if entity_result.entity else {},
            'start_line': start_line,
            'end_line': end_line,
            'source_code': source_with_lines or entity_result.source_code,
            'language': entity_result.language if hasattr(entity_result, 'language') else '',
            'filename': filename
        }

        # Render using template
        template = self.env.get_template('entity.jinja2')
        return template.render(**data)

    def _prepare_module_data(self, module: ModuleEntity, source_code: str) -> Dict[str, Any]:
        """Prepare module data for template rendering."""
        data = {
            'filename': module.filename or 'module',
            'module_doc': self._get_first_line(module.docstring) if module.docstring else None,
            'stats': {
                'lines': len(source_code.split('\n')) if source_code else 0,
                'chars': len(source_code) if source_code else 0,
            }
        }

        # Constants/Variables
        data['constants'] = [
            {
                'name': var.name,
                'type_hint': var.type_hint,
                'value': self._format_value(var.value),
                'line': var.start_line + 1,
                'is_constant': var.is_constant or var.name.isupper(),
            }
            for var in module.variables
            if not var.name.startswith('_')
        ]

        # Functions
        data['functions'] = [
            {
                'name': func.name,
                'signature': func.signature or self._build_signature(func),
                'start_line': func.start_line + 1,
                'end_line': func.end_line + 1,
                'doc': self._get_first_line(func.docstring) if func.docstring else None,
                'modifiers': self._get_function_modifiers(func),
            }
            for func in module.functions
            if not func.name.startswith('_')
        ]

        # Classes/Types
        data['types'] = [
            self._prepare_class_data(cls)
            for cls in module.classes
            if not cls.name.startswith('_')
        ]

        return data

    def _prepare_class_data(self, cls) -> Dict[str, Any]:
        """Prepare class data for template rendering."""
        public_members = []
        private_members = []

        for method in cls.methods:
            member_data = {
                'name': method.name,
                'signature': method.signature or self._build_signature(method),
                'start_line': method.start_line + 1,
                'end_line': method.end_line + 1,
                'doc': self._get_first_line(method.docstring) if method.docstring else None,
                'modifiers': self._get_function_modifiers(method),
            }

            if not method.name.startswith('_') or method.name == '__init__':
                public_members.append(member_data)
            else:
                private_members.append(member_data)

        return {
            'name': cls.name,
            'kind': 'class',  # Could be enhanced for interface/struct/etc
            'start_line': cls.start_line + 1,
            'end_line': cls.end_line + 1,
            'doc': self._get_first_line(cls.docstring) if cls.docstring else None,
            'inherits': cls.base_classes if cls.base_classes else None,
            'implements': None,
            'public_members': public_members,
            'private_members': private_members,
        }

    def _get_first_line(self, text: str) -> str:
        """Extract first line/sentence from docstring."""
        if not text:
            return ""

        first_line = text.strip().split('\n')[0].strip()

        if '.' in first_line:
            first_sentence = first_line.split('.')[0] + '.'
            if len(first_sentence) < len(first_line) and len(first_sentence) < 150:
                return first_sentence

        if len(first_line) > 150:
            return first_line[:147] + "..."

        return first_line

    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if value is None:
            return None

        value_str = str(value)
        if len(value_str) > 50:
            return value_str[:47] + "..."
        return value_str

    def _build_signature(self, func) -> str:
        """Build a signature string from a function entity."""
        if hasattr(func, 'signature') and func.signature:
            return func.signature

        params = ', '.join(func.parameters) if hasattr(func, 'parameters') else '...'
        sig = f"{func.name}({params})"

        if hasattr(func, 'return_type') and func.return_type:
            sig += f": {func.return_type}"

        return sig

    def _get_function_modifiers(self, func) -> list:
        """Extract modifiers from a function/method."""
        modifiers = []

        if hasattr(func, 'is_async') and func.is_async:
            modifiers.append('async')

        if hasattr(func, 'is_static') and func.is_static:
            modifiers.append('static')

        if hasattr(func, 'is_class_method') and func.is_class_method:
            modifiers.append('classmethod')

        if hasattr(func, 'is_property') and func.is_property:
            modifiers.append('property')

        return modifiers


def format_result_as_json(result: ExtractionResult, pretty: bool = True) -> str:
    """Format an extraction result as JSON.

    Args:
        result: The extraction result to format
        pretty: Whether to pretty-print the JSON

    Returns:
        A JSON string representation
    """
    result_dict = result.to_dict()

    if pretty:
        return json.dumps(result_dict, indent=2)
    else:
        return json.dumps(result_dict)