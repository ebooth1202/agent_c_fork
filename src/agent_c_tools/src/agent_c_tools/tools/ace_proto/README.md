# ACE Proto Code Analysis Toolset

Provides AI agents with comprehensive source code analysis capabilities across multiple programming languages using the ACE Proto (ts_tool) library.

## Overview

The ACE Proto toolset enables agents to analyze source code structure, extract entities, get summaries, and understand code in various programming languages including Python, JavaScript, TypeScript, Java, C#, Go, Rust, and more.

All analysis results are automatically saved to the `code_explorer` folder in the workspace for future reference and can optionally be returned directly to the agent.

## Features

- **Multi-language support**: Analyze code in 10+ programming languages with automatic language detection
- **Comprehensive analysis**: Extract complete code structure including classes, functions, methods, and variables
- **Entity extraction**: Get specific classes, functions, or methods by name
- **Public interface filtering**: Extract only public APIs, hiding private implementation details
- **Flexible detail levels**: Choose between summary, signature, or full details for entities
- **Persistent storage**: All analyses are saved automatically for future reference
- **Line-range analysis**: Analyze specific sections of large files

## Supported Languages

- Python
- JavaScript
- TypeScript
- Java
- C# (CSharp)
- Go
- Rust
- PHP
- Ruby
- And more...

Use `list_supported_languages` to get the complete current list.

## Tools

### 1. `list_supported_languages`

Lists all programming languages that can be analyzed.

**Parameters:** None

**Returns:** Markdown-formatted list of supported languages

**Example:**
```
list_supported_languages()
```

### 2. `analyze_code_file`

Performs comprehensive analysis of a source code file, extracting all classes, functions, methods, variables, and their relationships.

**Parameters:**
- `file_path` (required): UNC path to source file (e.g., `//workspace/src/mycode.py`)
- `language` (optional): Programming language override (auto-detected if not provided)
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/{filename}_analyze.md`)
- `return_analysis` (optional, default True): If True, returns full markdown; if False, only returns save path

**Returns:** Full markdown analysis or save path

**Example:**
```
analyze_code_file(file_path="//workspace/src/database/manager.py")
```

### 3. `get_code_summary`

Provides a quick overview of code structure with counts of classes, functions, and variables.

**Parameters:**
- `file_path` (required): UNC path to source file
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/{filename}_summary.md`)
- `return_analysis` (optional, default True): Return full summary or just path

**Returns:** Summary markdown or save path

**Example:**
```
get_code_summary(file_path="//workspace/src/utils.py")
```

### 4. `get_public_interface`

Extracts only public classes, functions, and methods, filtering out private implementation details.

**Parameters:**
- `file_path` (required): UNC path to source file
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/{filename}_public_interface.md`)
- `return_analysis` (optional, default True): Return full interface or just path

**Returns:** Public interface markdown or save path

**Example:**
```
get_public_interface(file_path="//workspace/src/api.py")
```

### 5. `get_entity_from_file`

Extracts a specific class, function, method, or variable by name with configurable detail level.

**Parameters:**
- `file_path` (required): UNC path to source file
- `entity_type` (required): Type of entity - `'class'`, `'function'`, `'method'`, or `'variable'`
- `entity_name` (required): Name of the entity to extract
- `detail_level` (optional, default 'full'): `'summary'` (basic info), `'signature'` (signature only), or `'full'` (complete with source)
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/{filename}_entity_{entityname}.md`)
- `return_analysis` (optional, default True): Return full entity details or just path

**Returns:** Entity details markdown or save path

**Example:**
```
get_entity_from_file(
    file_path="//workspace/src/database.py",
    entity_type="class",
    entity_name="DatabaseManager",
    detail_level="full"
)
```

### 6. `get_entity_source`

Gets just the source code for a specific entity without additional metadata.

**Parameters:**
- `file_path` (required): UNC path to source file
- `entity_type` (required): Type of entity
- `entity_name` (required): Name of the entity
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path
- `return_analysis` (optional, default True): Return source or just path

**Returns:** Source code or save path

**Example:**
```
get_entity_source(
    file_path="//workspace/src/api.py",
    entity_type="function",
    entity_name="process_request"
)
```

### 7. `get_entity_signature`

Gets just the signature (declaration) of an entity without implementation.

**Parameters:**
- `file_path` (required): UNC path to source file
- `entity_type` (required): Type of entity (`'class'`, `'function'`, or `'method'`)
- `entity_name` (required): Name of the entity
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path
- `return_analysis` (optional, default True): Return signature or just path

**Returns:** Signature or save path

**Example:**
```
get_entity_signature(
    file_path="//workspace/src/models.py",
    entity_type="class",
    entity_name="User"
)
```

### 8. `get_entity_documentation`

Extracts just the documentation/docstring for an entity or module.

**Parameters:**
- `file_path` (required): UNC path to source file
- `entity_type` (required): Type - `'class'`, `'function'`, `'method'`, or `'module'`
- `entity_name` (optional): Name of entity (leave empty for module-level docs)
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path
- `return_analysis` (optional, default True): Return docs or just path

**Returns:** Documentation markdown or save path

**Example:**
```
get_entity_documentation(
    file_path="//workspace/src/api.py",
    entity_type="module"
)
```

### 9. `analyze_code_snippet`

Analyzes code provided as a string rather than from a file. Useful for analyzing generated code or code fragments.

**Parameters:**
- `code` (required): Source code string to analyze
- `language` (optional): Programming language (auto-detected if not provided)
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/snippet_{timestamp}.md`)
- `return_analysis` (optional, default True): Return analysis or just path

**Returns:** Analysis markdown or save path

**Example:**
```
analyze_code_snippet(
    code="def hello():\n    print('Hello, World!')",
    language="python"
)
```

### 10. `analyze_code_range`

Analyzes a specific line range from a source file.

**⚠️ WARNING:** Only use when the line range contains syntactically complete code (e.g., a complete class or function). Partial code may fail to parse or produce inaccurate results.

**Parameters:**
- `file_path` (required): UNC path to source file
- `start_line` (required): Starting line number (0-based)
- `end_line` (required): Ending line number (0-based, inclusive)
- `language` (optional): Programming language override
- `save_location` (optional): Custom save path (defaults to `//workspace/code_explorer/{filename}_lines_{start}_{end}_analyze.md`)
- `return_analysis` (optional, default True): Return analysis or just path

**Returns:** Analysis markdown or save path

**Example:**
```
analyze_code_range(
    file_path="//workspace/src/large_file.py",
    start_line=100,
    end_line=200
)
```

## File Management

### Storage Location

All analysis results are saved to the `code_explorer` folder in the workspace by default:
- Default: `//workspace/code_explorer/`
- Can be overridden with `save_location` parameter

### File Naming

Files are named automatically based on the source and operation:
- **File analysis**: `{source_path}_{operation}.md`
  - Example: `src_database_manager_py_analyze.md`
- **Entity extraction**: `{source_path}_entity_{entity_name}.md`
  - Example: `src_api_py_entity_DatabaseManager.md`
- **Code snippets**: `snippet_{timestamp}.md`
  - Example: `snippet_20250116_153045.md`
- **Line ranges**: `{source_path}_lines_{start}_{end}_analyze.md`
  - Example: `src_mycode_py_lines_100_200_analyze.md`

### Overwrite Behavior

Analyses of the same file with the same operation will overwrite previous results. This keeps the folder clean and ensures the latest analysis is always available.

To preserve multiple analyses, use custom `save_location` values.

## Usage Patterns

### Quick File Overview

```python
# Get a quick summary first
get_code_summary(file_path="//workspace/src/mycode.py")

# If you need more details, get full analysis
analyze_code_file(file_path="//workspace/src/mycode.py")
```

### Extract Specific Entity

```python
# First get summary to see what's available
get_code_summary(file_path="//workspace/src/api.py")

# Then extract the specific class you need
get_entity_from_file(
    file_path="//workspace/src/api.py",
    entity_type="class",
    entity_name="RequestHandler",
    detail_level="full"
)
```

### Analyze Generated Code

```python
# Analyze code you've just generated
generated_code = """
class MyClass:
    def __init__(self):
        self.value = 42
"""

analyze_code_snippet(code=generated_code, language="python")
```

### Large File Handling

```python
# For very large files, get summary first
get_code_summary(file_path="//workspace/src/huge_file.py")

# Then extract only what you need
get_entity_from_file(
    file_path="//workspace/src/huge_file.py",
    entity_type="class",
    entity_name="ImportantClass"
)
```

### Saving Without Returning

For operations where you just want to save results for later:

```python
# Save analysis but don't return the full markdown (saves tokens)
analyze_code_file(
    file_path="//workspace/src/mycode.py",
    return_analysis=False
)
# Returns: "Analysis saved to //workspace/code_explorer/src_mycode_py_analyze.md"

# Later, read it back with workspace tools
workspace_read(path="//workspace/code_explorer/src_mycode_py_analyze.md")
```

## Error Handling

All tools return descriptive error messages as strings starting with "ERROR:":

- `ERROR: File not found: {path}` - Source file doesn't exist
- `ERROR: Failed to parse code: {details}` - Code couldn't be parsed
- `ERROR: Language '{lang}' not supported` - Unsupported language
- `ERROR: Entity '{name}' of type '{type}' not found` - Entity doesn't exist in code
- `ERROR: ACE Proto (ts_tool) is not installed` - Missing dependency

## Dependencies

This toolset requires:
- **WorkspaceTools** - For file reading/writing operations
- **ts_tool** (ACE Proto) - The underlying code analysis engine

## Best Practices

1. **Start with summaries**: Use `get_code_summary` before doing full analysis
2. **Use specific extractions**: Use `get_entity_from_file` instead of analyzing entire files when you know what you need
3. **Leverage persistence**: Analyses are saved automatically, so you can reference them later
4. **Auto-detect language**: Let the tool detect the language unless you have a specific reason to override
5. **Use appropriate detail levels**: Choose `'summary'` or `'signature'` for entity extraction when you don't need full source
6. **Check supported languages**: Use `list_supported_languages` if you're unsure about language support

## Limitations

1. **Complete syntax required**: Code must be syntactically valid to be analyzed
2. **Line-range analysis risks**: Using `analyze_code_range` with incomplete code sections may fail or produce inaccurate results
3. **Large files**: Very large files may be slow to analyze; consider using entity extraction or line ranges
4. **Language detection**: While auto-detection is usually accurate, complex or mixed-language files may require manual language specification

## Examples

### Example 1: Analyzing a Python Module

```python
# Get overview
get_code_summary(file_path="//workspace/src/database.py")

# Get full analysis
analyze_code_file(file_path="//workspace/src/database.py")

# Extract specific class
get_entity_from_file(
    file_path="//workspace/src/database.py",
    entity_type="class",
    entity_name="DatabaseConnection",
    detail_level="full"
)
```

### Example 2: Understanding a JavaScript Library

```python
# Get public API only
get_public_interface(file_path="//workspace/lib/utils.js")

# Get documentation for a specific function
get_entity_documentation(
    file_path="//workspace/lib/utils.js",
    entity_type="function",
    entity_name="formatDate"
)
```

### Example 3: Refactoring Workflow

```python
# 1. Analyze current structure
analyze_code_file(
    file_path="//workspace/src/legacy_code.py",
    save_location="//workspace/.scratch/analysis_before.md"
)

# 2. Make changes to code...

# 3. Analyze new structure
analyze_code_file(
    file_path="//workspace/src/legacy_code.py",
    save_location="//workspace/.scratch/analysis_after.md"
)

# 4. Compare the two analyses
```

## Troubleshooting

### "ERROR: ACE Proto (ts_tool) is not installed"
The ts_tool package is not installed. Install it with:
```bash
pip install ts-tool
```

### "ERROR: Failed to parse code"
The code has syntax errors or is incomplete. Ensure the code is valid before analyzing.

### "ERROR: Entity 'X' not found"
The specified entity doesn't exist in the file. Check the entity name and type, or get a summary first to see what's available.

### Analysis is incomplete or inaccurate
If using `analyze_code_range`, ensure the line range contains complete, syntactically valid code. Consider analyzing the full file instead.

## Version History

- **1.0.0** (2025-01-16): Initial release with 10 core tools
