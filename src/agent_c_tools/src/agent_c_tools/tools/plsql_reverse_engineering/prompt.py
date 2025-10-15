"""Prompt section for PL/SQL Reverse Engineering Tools."""

from typing import Any
from agent_c.prompting.prompt_section import PromptSection


class PlSqlRevEngSection(PromptSection):
    """Prompt section describing PL/SQL reverse engineering capabilities."""

    def __init__(self, **data: Any):
        TEMPLATE = (
            "The PL/SQL Reverse Engineering Tools are designed to assist you in analyzing and understanding "
            "Oracle PL/SQL codebases.\n\n"
            "## Available Tools\n\n"
            "- **plsql_analyze_source**: Perform an in-depth analysis of all PL/SQL files matching a glob pattern.\n"
            "  - Performs a two-pass analysis of the code files matching the pattern\n"
            "  - Understands PL/SQL structure: packages (spec/body), procedures, functions, triggers\n"
            "  - Analyzes both whole files and individual subprograms within package bodies\n"
            "  - Provides detailed analysis and reverse engineers requirements for each unit\n"
            "  - Output is saved to `<workspace>/.scratch/plsql_analyze_source/`\n\n"
            "- **plsql_analyze_tree**: Perform an in-depth analysis of all PL/SQL files in a directory tree.\n"
            "  - Walks through directories to find all PL/SQL files\n"
            "  - Supports filtering by file extensions (.sql, .pks, .pkb, .prc, .fnc, .trg, etc.)\n"
            "  - Performs the same comprehensive two-pass analysis as analyze_source\n\n"
            "- **plsql_query_analysis**: Query an expert about the analyzed PL/SQL codebase.\n"
            "  - The expert can answer questions about the codebase and/or the analysis results\n"
            "  - Requires prior execution of `plsql_analyze_source` or `plsql_analyze_tree`\n"
            "  - Saves your context window by allowing the expert to examine the detailed analysis\n\n"
            "## PL/SQL-Specific Features\n\n"
            "- **Package Awareness**: Understands the relationship between package specs (.pks) and bodies (.pkb)\n"
            "- **Subprogram Analysis**: Analyzes individual procedures and functions within package bodies\n"
            "- **Structure Detection**: Identifies packages, standalone procedures/functions, triggers, and types\n"
            "- **Signature Extraction**: Captures parameter lists and return types for subprograms\n"
            "- **Oracle Syntax**: Handles Oracle-specific constructs like q-quotes, quoted identifiers, and nested blocks\n"
        )
        super().__init__(
            template=TEMPLATE,
            required=True,
            name="PL/SQL Reverse Engineering",
            render_section_header=True,
            **data
        )
