"""API for AI agents to explore and extract information from code.

This module provides a simple interface for AI agents to use the
Code Explorer functionality to analyze and extract information from code.
"""

from typing import Dict, List, Optional, Any, Union
import json

from ts_tool.core.code_explorer import CodeExplorer
from ts_tool.models.extraction_result import (
    DetailLevel, ExtractionResult, EntityExtractionResult,
    ModuleExtractionResult, PublicInterfaceResult, CodeSummaryResult
)
from ts_tool.utils.formatting import CodeFormatter, format_result_as_json

# Create a singleton instance of the CodeExplorer
_explorer = CodeExplorer()

# Lazily-created formatter so callers can optionally pass a template_dir
_formatter: Optional[CodeFormatter] = None

def _get_formatter(template_dir: Optional[str] = None) -> CodeFormatter:
    """Return a CodeFormatter, using given template_dir or default /templates next to module."""
    global _formatter
    if template_dir is not None:
        # Always make a fresh formatter if caller specifies a template_dir
        return CodeFormatter(template_dir=template_dir)
    if _formatter is None:
        _formatter = CodeFormatter()  # defaults to 'templates' next to this file
    return _formatter

def get_supported_languages() -> List[str]:
    """Get a list of supported programming languages.
    
    Returns:
        A list of supported language names.
    """
    return _explorer.get_supported_languages()

def detect_language(code: str, filename: Optional[str] = None) -> Optional[str]:
    """Detect the programming language of the given code.
    
    Args:
        code: The source code to analyze.
        filename: Optional filename which may contain an extension hint.
        
    Returns:
        The detected language name, or None if detection failed.
    """
    return _explorer.detect_language(code, filename)


def get_code_summary(
    code: str,
    language: Optional[str] = None,
    filename: Optional[str] = None,
    format: str = 'dict',
    template_dir: Optional[str] = None
) -> str | dict[str, Any] | CodeSummaryResult:
    """Get a high-level summary of code structure.

    Args:
        code: The source code to analyze.
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        format: Output format ('dict', 'json', or 'markdown').
        template_dir: Optional path to a directory containing custom templates.

    Returns:
        Code summary in the specified format.
    """
    result: CodeSummaryResult = _explorer.get_summary(code, language, filename)

    if format == 'dict':
        return result.to_dict()
    elif format == 'json':
        return format_result_as_json(result)
    elif format == 'markdown':
        formatter = _get_formatter(template_dir)
        return formatter.format_summary(result, filename=filename)
    else:
        return result

def get_code_context(
    code: str,
    language: Optional[str] = None,
    filename: Optional[str] = None,
    format: str = 'dict',
    style: str = "compact",
    template_dir: Optional[str] = None,
) -> str | dict[str, Any] | ModuleExtractionResult:
    """
    Render a concise, agent-friendly module overview using external Jinja2 templates.

    Args:
        code: Source code to analyze.
        language: Optional language override; if None, will be detected.
        filename: Optional filename for detection and display.
        format: 'dict' (default), 'json', or 'markdown'.
        style: 'standard' (default) or 'compact' — maps to context_<style>.jinja2 template
        template_dir: Optional path to a directory containing your jinja2 templates.
                      If not provided, defaults to a 'templates' directory alongside this file.

    Returns:
        Markdown string rendered by the selected template.
    """
    # Get a full module parse
    mod_result: ModuleExtractionResult = _explorer.explore_code(code, language, filename)

    if format == 'dict':
        return mod_result.to_dict()
    elif format == 'json':
        return format_result_as_json(mod_result)
    elif format == 'markdown':
        formatter = _get_formatter(template_dir)
        return formatter.format_module(mod_result.module, source_code=code, style=style)
    else:
        return mod_result

def get_public_interface(
    code: str,
    language: Optional[str] = None,
    filename: Optional[str] = None,
    format: str = 'dict',
    template_dir: Optional[str] = None
) -> str | dict[str, Any] | PublicInterfaceResult:
    """Extract the public interface from code.

    Args:
        code: The source code to analyze.
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        format: Output format ('dict', 'json', or 'markdown').
        template_dir: Optional path to a directory containing your jinja2 templates.
                      If not provided, defaults to a 'templates' directory alongside this file.

    Returns:
        Public interface in the specified format.
    """
    result = _explorer.get_public_interface(code, language, filename)

    if format == 'dict':
        return result.to_dict()
    elif format == 'json':
        return format_result_as_json(result)
    elif format == 'markdown':
        formatter = _get_formatter(template_dir)
        return formatter.format_public_interface(result, filename=filename)
    else:
        return result



def get_entity(
    code: str,
    entity_type: str,
    entity_name: str,
    detail_level: str = 'full',
    language: Optional[str] = None,
    filename: Optional[str] = None,
    format: str = 'dict',
    template_dir: Optional[str] = None
) -> Union[Dict[str, Any], str]:
    """Get a specific entity from code.

    Args:
        code: The source code to analyze.
        entity_type: The type of entity to extract ('class', 'function', 'method', 'variable').
        entity_name: The name of the entity to extract.
        detail_level: Level of detail ('summary', 'signature', or 'full').
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        format: Output format ('dict', 'json', or 'markdown').
        template_dir: Optional path to a directory containing your jinja2 templates.
                      If not provided, defaults to a 'templates' directory alongside this file.

    Returns:
        Entity information in the specified format.
    """
    result = _explorer.get_entity(code, entity_type, entity_name, detail_level, language, filename)

    if format == 'dict':
        return result.to_dict()
    elif format == 'json':
        return format_result_as_json(result)
    elif format == 'markdown':
        formatter = _get_formatter(template_dir)
        return formatter.format_entity(result, filename=filename)
    else:
        raise ValueError("Unsupported format. Use 'dict', 'json', or 'markdown'.")


def explore_code(
    code: str,
    language: Optional[str] = None,
    filename: Optional[str] = None,
    format: str = 'dict',
    style: str = 'standard',
    template_dir: Optional[str] = None
) -> str | dict[str, Any] | ModuleExtractionResult:
    """Explore code and extract its complete structure.

    Args:
        code: The source code to analyze.
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        format: Output format ('dict', 'json', or 'markdown').
        style: For markdown format, the style to use ('standard' or 'compact'). Maps to explore_<style>.jinja2 template
        template_dir: Optional path to a directory containing your jinja2 templates.
                      If not provided, defaults to a 'templates' directory alongside this file.

    Returns:
        Complete module structure in the specified format.
    """
    result = _explorer.explore_code(code, language, filename)

    if format == 'dict':
        return result.to_dict()
    elif format == 'json':
        return format_result_as_json(result)
    elif format == 'markdown':
        formatter = _get_formatter(template_dir)
        return formatter.format_explore(result, filename=filename, style=style)
    else:
        return result

def get_source_code(code: str,
                    entity_type: str,
                    entity_name: str,
                    language: Optional[str] = None,
                    filename: Optional[str] = None) -> Optional[str]:
    """Get the source code for a specific entity.
    
    This is a convenience function to directly get the source code
    of a specific entity without additional metadata.
    
    Args:
        code: The source code to analyze.
        entity_type: The type of entity to extract ('class', 'function', 'method', 'variable').
        entity_name: The name of the entity to extract.
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        
    Returns:
        The source code of the entity, or None if not found.
    """
    result = _explorer.get_entity(code, entity_type, entity_name, DetailLevel.FULL, language, filename)
    
    if result.successful and hasattr(result, 'source_code') and result.source_code:
        return result.source_code
    
    return None


def get_signature(code: str,
                  entity_type: str,
                  entity_name: str,
                  language: Optional[str] = None,
                  filename: Optional[str] = None) -> Optional[str]:
    """Get the signature for a specific entity.
    
    This is a convenience function to directly get the signature
    of a specific entity without additional metadata.
    
    Args:
        code: The source code to analyze.
        entity_type: The type of entity to extract ('class', 'function', 'method').
        entity_name: The name of the entity to extract.
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        
    Returns:
        The signature of the entity, or None if not found.
    """
    result = _explorer.get_entity(code, entity_type, entity_name, DetailLevel.SIGNATURE, language, filename)
    
    if result.successful and result.entity:
        if hasattr(result.entity, 'signature'):
            return result.entity.signature
    
    return None


def get_documentation(code: str,
                      entity_type: str,
                      entity_name: str,
                      language: Optional[str] = None,
                      filename: Optional[str] = None) -> Optional[str]:
    """Get the documentation for a specific entity.
    
    This is a convenience function to directly get the documentation
    of a specific entity without additional metadata.
    
    Args:
        code: The source code to analyze.
        entity_type: The type of entity to extract ('class', 'function', 'method', 'module').
        entity_name: The name of the entity to extract (use '' for module).
        language: Optional language name. If not provided, will be detected.
        filename: Optional filename which may help with language detection.
        
    Returns:
        The documentation of the entity, or None if not found or not documented.
    """
    if entity_type == 'module':
        result = _explorer.explore_code(code, language, filename)
        if result.successful and result.module and result.module.docstring:
            return result.module.docstring
    else:
        result = _explorer.get_entity(code, entity_type, entity_name, DetailLevel.SUMMARY, language, filename)
        if result.successful and result.entity and result.entity.docstring:
            return result.entity.docstring
    
    return None