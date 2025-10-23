# Code Quality Python Component

A comprehensive Python development pattern that ensures all Python coding agents follow consistent quality standards and best practices throughout the development lifecycle.

## Binary Decision

**Does this agent write or modify Python code?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Python development agents (40% of coding agents)

**Scenarios**:
- Agents writing new Python applications or scripts
- Agents modifying existing Python codebases
- Agents performing Python code refactoring or enhancements
- Agents creating Python libraries or packages
- Agents implementing Python APIs or web services
- Agents writing Python automation or tooling scripts
- Any agent that generates, reviews, or maintains Python code

## Component Pattern

```markdown
## Python Code Quality Requirements

### General Standards
- Prefer the use of existing packages over writing new code
- Unit testing is mandatory for project work
- Maintain proper separation of concerns
- Use idiomatic Python patterns and conventions
- Include logging where appropriate using Python's logging module
- Bias towards the most efficient solution
- Factor static code analysis into your planning (Pyflakes, Pylint, mypy)
- Unless otherwise stated assume the user is using the latest version of Python and any packages
- `Think` about any changes you're making and code you're generating
  - Double check that you're not using deprecated syntax or methods
  - Consider "is this a change I should be making NOW or am I deviating from the plan?"

### Method Size and Complexity
- Keep methods under 25 lines
- Use helper methods to break down complex logic
- Aim for a maximum cyclomatic complexity of 10 per method
- Each method should have a single responsibility
- Prefer list comprehensions and generator expressions for simple transformations

### Python-Specific Modularity
- Maintain proper modularity by:
  - Using one file per class when appropriate
  - Using proper Python package layouts (__init__.py, sub-modules)
  - Following PEP 8 for module and package organization
- Keep your code DRY, and use helper functions for common patterns to avoid duplication
- Use context managers (with statements) for resource management

### Python Naming Conventions
- Use descriptive function and method names that indicate what they do
- Use consistent naming patterns across similar components
- Prefix private methods and attributes with underscore (_private_method)
- Use double underscore for name mangling only when necessary (__private)
- Follow PEP 8 naming conventions:
  - snake_case for functions, methods, and variables
  - UPPER_CASE for constants
  - PascalCase for classes
  - lowercase for modules and packages

### Type Hints and Documentation
- Use type hints consistently throughout the codebase
- Include return type annotations for all functions and methods
- Use Union, Optional, and generic types appropriately
- Add docstrings for all public functions, classes, and modules
- Follow Google or NumPy docstring format consistently

### Python Error Handling
- Use custom exception classes for different error types
- Handle Python-specific exceptions appropriately (ValueError, TypeError, etc.)
- Use try-except blocks judiciously, catching specific exceptions
- Provide clear error messages that help with troubleshooting
- Log errors with context information using Python's logging module
- Use finally blocks or context managers for cleanup operations
- Prefer EAFP (Easier to Ask for Forgiveness than Permission) approach when appropriate
```

## Usage Notes

**Positioning**: Place in dedicated "Code Quality Requirements" section after core guidelines.

**Implementation Notes**:
- Comprehensive coverage of Python development (syntax to architecture)
- Integrates industry tools (Pyflakes, Pylint, mypy) into workflow
- Assumes latest Python features and best practices
- Universal pattern - no variations across Python agents
- Embeds quality checks into natural development workflow

**Integration Tips**:
- Works independently, no dependencies
- Combines with reflection rules for code analysis/debugging
- Essential for multi-agent development teams
- Pairs with workspace organization for proper project structure
- Supports both new development and legacy maintenance

## Example Implementation

Use Component Pattern as-is for all Python coding agents.
