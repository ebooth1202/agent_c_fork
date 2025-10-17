"""ACE Proto Code Analysis Toolset

Provides AI agents with comprehensive source code analysis capabilities across
multiple programming languages using the ACE Proto (ts_tool) library.
"""

import re
from typing import Optional, cast, Dict, Any, Tuple
from datetime import datetime

from agent_c.toolsets import Toolset, json_schema
from agent_c_tools.helpers.path_helper import os_file_system_path
from agent_c_tools.helpers.token_helper import is_content_too_large
from agent_c_tools.helpers.validate_kwargs import validate_required_fields
from agent_c_tools.tools.workspace.tool import WorkspaceTools

# Import ACE Proto API
try:
    from ts_tool import api as ace_proto
except ImportError:
    ace_proto = None


class AceProtoTools(Toolset):
    """
    Provides your agent with advanced source code analysis capabilities. Your agent can analyze code
    structure, extract entities, get summaries, and understand code across multiple programming languages
    including Python, JavaScript, TypeScript, Java, C#, Go, Rust, and more.
    
    All analysis results are automatically saved to the code_explorer folder for future reference.
    """

    def __init__(self, **kwargs):
        """Initialize the ACE Proto toolset.
        
        Args:
            **kwargs: Keyword arguments passed to parent Toolset class.
        """
        super().__init__(**kwargs, name='agent_code_explorer', use_prefix=False)
        self.workspace_tools: Optional[WorkspaceTools] = None
        
        # Verify ACE Proto is available
        if ace_proto is None:
            self.valid = False
            self.logger.error("ACE Proto (ts_tool) is not installed. This toolset will not function.")

    async def post_init(self):
        """Initialize after all toolsets are loaded."""
        self.workspace_tools = self.tool_chest.available_tools.get("WorkspaceTools")
        if not self.workspace_tools:
            raise RuntimeError("WorkspaceTools required but not available")

    # ===== Helper Methods =====

    def _validate_and_parse_path(self, unc_path: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Validate UNC path and extract workspace name and relative path.
        
        Args:
            unc_path: UNC-style path like //workspace/src/file.py
            
        Returns:
            Tuple of (error_message, workspace_name, relative_path)
            If error_message is not None, other values should be ignored
        """
        # Use WorkspaceTools validation method
        error, workspace_obj, relative_path = self.workspace_tools.validate_and_get_workspace_path(unc_path)
        
        if error:
            return error, None, None
        
        # Extract workspace name from the workspace object
        workspace_name = workspace_obj.name if workspace_obj else None
        
        return None, workspace_name, relative_path

    def _sanitize_filename(self, path: str) -> str:
        """Convert UNC path to safe filename component.
        
        Args:
            path: UNC-style path like //workspace/src/database/manager.py
            
        Returns:
            Sanitized filename like src_database_manager_py
        """
        # Remove leading //workspace_name/
        cleaned = re.sub(r'^//[^/]+/', '', path)
        
        # Replace path separators with underscores
        cleaned = cleaned.replace('/', '_').replace('\\', '_')
        
        # Replace dots with underscores (except we keep extension-like patterns)
        cleaned = cleaned.replace('.', '_')
        
        return cleaned

    def _generate_filename(
        self,
        source_path: Optional[str],
        operation: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        entity_name: Optional[str] = None
    ) -> str:
        """Generate filename for analysis results.
        
        Args:
            source_path: Source file UNC path (None for snippets)
            operation: Operation type (analyze, summary, entity, etc.)
            start_line: Optional start line for range analysis
            end_line: Optional end line for range analysis
            entity_name: Optional entity name for entity extraction
            
        Returns:
            Generated filename with .md extension
        """
        if source_path is None:
            # Snippet analysis - use timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"snippet_{timestamp}.md"
        
        # Sanitize the source path
        base = self._sanitize_filename(source_path)
        
        # Build filename based on operation type
        if start_line is not None and end_line is not None:
            # Range analysis
            return f"{base}_lines_{start_line}_{end_line}_{operation}.md"
        elif entity_name:
            # Entity extraction
            safe_entity = entity_name.replace('.', '_').replace('/', '_')
            return f"{base}_entity_{safe_entity}.md"
        else:
            # Standard analysis
            return f"{base}_{operation}.md"

    async def _read_file(self, file_path: str, tool_context: Dict[str, Any]) -> str:
        """Read file content via workspace tools.
        
        Args:
            file_path: UNC path to file
            tool_context: Tool context for the operation
            
        Returns:
            File content as string
            
        Raises:
            Exception: If file cannot be read
        """
        result = await self.workspace_tools.read(
            path=file_path,
            tool_context=tool_context,
            encoding='utf-8',
            token_limit=25000000 # We're doing in effect internal reads
        )
        
        # Check if result is an error
        if result.startswith('Error:') or result.startswith('ERROR:'):
            raise Exception(result)
        
        return result

    async def _read_file_lines(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        tool_context: Dict[str, Any]
    ) -> str:
        """Read specific lines from a file via workspace tools.
        
        Args:
            file_path: UNC path to file
            start_line: Starting line (0-based)
            end_line: Ending line (0-based, inclusive)
            tool_context: Tool context for the operation
            
        Returns:
            File content as string
            
        Raises:
            Exception: If file cannot be read
        """
        result = await self.workspace_tools.read_lines(
            path=file_path,
            start_line=start_line,
            end_line=end_line,
            tool_context=tool_context
        )
        
        # Check if result is an error
        if result.startswith('Error:') or result.startswith('ERROR:'):
            raise Exception(result)
        
        return result

    async def _ensure_directory(
        self,
        dir_path: str,
        workspace_name: str,
        tool_context: Dict[str, Any]
    ) -> None:
        """Ensure directory exists, create if it doesn't.
        
        Args:
            dir_path: UNC path to directory
            workspace_name: Name of the workspace
            tool_context: Tool context for the operation
        """
        # Check if directory exists using workspace tools
        result = await self.workspace_tools.is_directory(
            path=dir_path,
            tool_context=tool_context
        )
        
        # If it's not a directory (doesn't exist or is a file), we need to create it
        # The is_directory tool returns "True" or "False" as a string
        if result.strip().lower() != "true":
            # Create the directory by writing a dummy file and removing it
            # Actually, workspace tools should handle directory creation automatically
            # when writing files to non-existent directories
            pass

    async def _save_analysis(
        self,
        content: str,
        location: str,
        tool_context: Dict[str, Any]
    ) -> str:
        """Save analysis to file, creating directories as needed.
        
        Args:
            content: Markdown content to save
            location: UNC path where to save
            tool_context: Tool context for the operation
            
        Returns:
            The path where file was saved
            
        Raises:
            Exception: If file cannot be written
        """
        result = await self.workspace_tools.write(
            path=location,
            data=content,
            mode='write',
            tool_context=tool_context
        )
        
        # Check if result indicates an error
        if 'error' in result.lower():
            raise Exception(f"Failed to save analysis: {result}")
        
        return location

    def _format_result(
        self,
        markdown: str,
        save_path: str,
        return_analysis: bool
    ) -> str:
        """Format the return string consistently.
        
        Args:
            markdown: The analysis markdown content
            save_path: Path where file was saved
            return_analysis: Whether to include full markdown
            
        Returns:
            Formatted result string
        """
        if return_analysis:
            return f"Analysis saved to {save_path}\n\n{markdown}"
        else:
            return f"Analysis saved to {save_path}"

    # ===== Tool Methods =====
    @json_schema(
        description="Analyze a source code file and extract complete structure including all classes, functions, methods, and variables with full details. Results are saved for future reference.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file to analyze (e.g., //workspace/src/mycode.py)",
                "required": True
            },
            "compact": {
                "type": "boolean",
                "description": "If True, generates a more compact analysis. Defaults to False for full detail.",
                "required": False,
                "default": False
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. If not provided, language will be auto-detected.",
                "required": False
            },
            "save_location": {
                "type": "string",
                "description": "Optional UNC path where analysis should be saved. If not provided, saves to //workspace/code_explorer/{filename}_analyze.md",
                "required": False
            },
            "return_analysis": {
                "type": "boolean",
                "description": "If True (default), returns full analysis markdown. If False, only returns the save location path.",
                "required": False,
                "default": True
            }
        }
    )
    async def explore_code_file(self, **kwargs) -> str:
        # FYI, ace_proto.explore_code() and ace_proto.get_code_context() are the same with different default styles.,
        """Get the complete code context from a code file.

        Performs comprehensive analysis of a source code file, extracting all classes,
        functions, methods, and variables. Results include signatures,
        documentation, and line numbers.

        Returns:
            Markdown analysis or save path, depending on return_analysis parameter
        """
        try:
            # Extract parameters
            file_path = kwargs.get("file_path")
            language = kwargs.get("language")
            save_location = kwargs.get("save_location")
            compact = kwargs.get("compact", False)
            return_analysis = kwargs.get("return_analysis", True)
            tool_context = kwargs.get("tool_context", {})

            # Validate required params
            success, message = validate_required_fields(kwargs=kwargs, required_fields=['file_path'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            # Read file content
            self.logger.info(f"Reading file: {file_path}")
            code = await self._read_file(file_path, tool_context)

            # Get filename for language detection hint
            filename = file_path.split('/')[-1] if '/' in file_path else file_path

            params = {
                "code": code,
                "format": 'markdown',
                "style": "compact" if compact else "standard",
            }
            if language:
                params["language"] = language

            # Call ACE Proto API for comprehensive code exploration
            self.logger.info(f"Analyzing code structure for: {filename}")
            result = ace_proto.explore_code(**params)

            if not result:
                return f"ERROR: Analysis returned no results for {file_path}"

            should_save = save_location or is_content_too_large(content=result, tool_context=tool_context, max_tokens=25000)

            if should_save:
            # Generate save location if not provided
                if not save_location:
                    error, workspace_name, _ = self._validate_and_parse_path(file_path)
                    if error:
                        return f"ERROR: Invalid file path: {error}"
                    filename_base = self._generate_filename(file_path, f"explore_{'compact' if compact else 'standard'}")
                    save_location = f"//{workspace_name}/code_explorer/{filename_base}"

                # Save results
                self.logger.info(f"Saving analysis to: {save_location}")
                await self._save_analysis(result, save_location, tool_context)

                # Format and return
                return self._format_result(result, save_location, return_analysis)
            else:
                # Content is small enough and save not requested, just return it directly
                return result

        except Exception as e:
            self.logger.error(f"Error in analyze_code_file: {str(e)}")
            return f"ERROR: {str(e)}"



    @json_schema(
        description="Extract only the public interface from code (public classes, functions, methods). Filters out private/internal implementation details.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file to analyze",
                "required": True
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            },
            "save_location": {
                "type": "string",
                "description": "Optional UNC path where results should be saved. Defaults to //workspace/code_explorer/{filename}_public_interface.md",
                "required": False
            },
            "return_analysis": {
                "type": "boolean",
                "description": "If True (default), returns full interface markdown. If False, only returns save location.",
                "required": False,
                "default": True
            }
        }
    )
    async def get_public_interface(self, **kwargs) -> str:
        """Extract public interface from code.

        Extracts only the public elements of the code, such as public classes,
        functions, and constants, filtering out private implementation details.

        Returns:
            Markdown interface description or save path
        """
        try:
            file_path = kwargs.get("file_path")
            language = kwargs.get("language")
            save_location = kwargs.get("save_location")
            return_analysis = kwargs.get("return_analysis", True)
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs, required_fields=['file_path'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "format": 'markdown'
            }
            if language:
                params["language"] = language

            result = ace_proto.get_public_interface(**params)

            should_save = save_location or is_content_too_large(content=result, tool_context=tool_context,
                                                                max_tokens=25000)
            if should_save:
                if not save_location:
                    error, workspace_name, _ = self._validate_and_parse_path(file_path)
                    if error:
                        return f"ERROR: Invalid file path: {error}"
                    filename_base = self._generate_filename(file_path, "public_interface")
                    save_location = f"//{workspace_name}/code_explorer/{filename_base}"

                await self._save_analysis(result, save_location, tool_context)
                return self._format_result(result, save_location, return_analysis)
            else:
                return result

        except Exception as e:
            self.logger.error(f"Error in get_public_interface: {str(e)}")
            return f"ERROR: {str(e)}"

    @json_schema(
        description="Extract a specific entity (class, function, method, or variable) from code by name with configurable detail level.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file",
                "required": True
            },
            "entity_type": {
                "type": "string",
                "description": "Type of entity to extract: 'class', 'function', 'method', or 'variable'",
                "required": True
            },
            "entity_name": {
                "type": "string",
                "description": "Name of the entity to extract",
                "required": True
            },
            "detail_level": {
                "type": "string",
                "description": "Level of detail: 'summary' (basic info), 'signature' (signature only), or 'full' (complete with source code). Default is 'full'.",
                "enum": ["summary", "signature", "full"],
                "default": "full",
                "required": False
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            },
            "save_location": {
                "type": "string",
                "description": "Optional UNC path where results should be saved. Defaults to //workspace/code_explorer/{filename}_entity_{entityname}.md",
                "required": False
            },
            "return_analysis": {
                "type": "boolean",
                "description": "If True (default), returns full entity markdown. If False, only returns save location.",
                "required": False,
                "default": True
            }
        }
    )
    async def get_entity_from_file(self, **kwargs) -> str:
        """Extract specific entity from code.

        Extracts a specific named entity (class, function, method, or variable) from
        the code with the specified level of detail.

        Returns:
            Markdown entity description or save path
        """
        try:
            file_path = kwargs.get("file_path")
            entity_type = kwargs.get("entity_type")
            entity_name = kwargs.get("entity_name")
            detail_level = kwargs.get("detail_level", "full")
            language = kwargs.get("language")
            save_location = kwargs.get("save_location")
            return_analysis = kwargs.get("return_analysis", True)
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs, required_fields=['file_path', 'entity_type', 'entity_name'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "entity_type": entity_type,
                "entity_name": entity_name,
                "detail_level": detail_level,
                "format": 'markdown'
            }
            if language:
                params["language"] = language

            result = ace_proto.get_entity(**params )

            should_save = save_location or is_content_too_large(content=result, tool_context=tool_context,
                                                                max_tokens=15000)

            if should_save:
                # Generate save location if not provided
                if not save_location:
                    error, workspace_name, _ = self._validate_and_parse_path(file_path)
                    if error:
                        return f"ERROR: Invalid file path: {error}"
                    filename_base = self._generate_filename(
                        file_path, "entity", entity_name=entity_name
                    )
                    save_location = f"//{workspace_name}/code_explorer/{filename_base}"

                await self._save_analysis(result, save_location, tool_context)
                return self._format_result(result, save_location, return_analysis)
            else:
                return result

        except Exception as e:
            self.logger.error(f"Error in get_entity_from_file: {str(e)}")
            return f"ERROR: {str(e)}"

    ### These primarily return string data rather than markdown or saving to a file, with 1 exception on get_entity_source
    @json_schema(
        description="Get just the documentation/docstring for a specific entity or module without source code.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file",
                "required": True
            },
            "entity_type": {
                "type": "string",
                "description": "Type of entity: 'class', 'function', 'method', or 'module' (for module-level docs)",
                "required": True
            },
            "entity_name": {
                "type": "string",
                "description": "Name of the entity (leave empty string for module-level documentation)",
                "required": False
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            }
        }
    )
    async def get_entity_documentation(self, **kwargs) -> str:
        """Get documentation for a specific entity or module.

        Extracts just the documentation/docstring of a specific entity or the module
        itself, without source code or other details.

        Returns:
            Documentation or save path
        """
        try:
            file_path = kwargs.get("file_path")
            entity_type = kwargs.get("entity_type")
            entity_name = kwargs.get("entity_name")
            language = kwargs.get("language", None)
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs,
                                                        required_fields=['file_path', 'entity_type', 'entity_name'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "entity_type": entity_type,
                "entity_name": entity_name,
            }
            if language:
                params["language"] = language

            docs = ace_proto.get_documentation(**params)

            if docs is None:
                target = "module" if entity_type == "module" else f"{entity_type} '{entity_name}'"
                return f"INFORMATION: No documentation found for {target}: {entity_type} '{entity_name}' in {file_path}"

            result = f"{entity_name or 'Module'}\n\n{docs}"

            return result

        except Exception as e:
            self.logger.error(f"Error in get_entity_documentation: {str(e)}")
            return f"ERROR: {str(e)}"

    @json_schema(
        description="Get the source code for a specific entity (class, function, method, or variable) without additional metadata.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file",
                "required": True
            },
            "entity_type": {
                "type": "string",
                "description": "Type of entity: 'class', 'function', 'method', or 'variable' etc...",
                "required": True
            },
            "entity_name": {
                "type": "string",
                "description": "Name of the entity",
                "required": True
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            },
            "save_location": {
                "type": "string",
                "description": "Optional UNC path where source should be saved. Defaults to //workspace/code_explorer/{filename}_entity_{entityname}_source.md",
                "required": False
            },
            "return_analysis": {
                "type": "boolean",
                "description": "If True (default), returns the source code to the agent. If False, only returns save location.",
                "default": True,
                "required": False
            }
        }
    )
    async def get_entity_source(self, **kwargs) -> str:
        """Get source code for a specific entity.

        Extracts just the source code of a specific entity without additional metadata.

        Returns:
            Source code or save path
        """
        try:
            file_path = kwargs.get("file_path")
            entity_type = kwargs.get("entity_type")
            entity_name = kwargs.get("entity_name")
            language = kwargs.get("language")
            save_location = kwargs.get("save_location")
            return_analysis = kwargs.get("return_analysis", True)
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs,
                                                        required_fields=["file_path", "entity_type", "entity_name"])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "entity_type": entity_type,
                "entity_name": entity_name,
            }
            if language:
                params["language"] = language

            source = ace_proto.get_source_code(**params)

            if source is None:
                return f"ERROR: Entity '{entity_name}' of type '{entity_type}' not found in {file_path}"

            # Determine if we should save
            should_save = save_location or is_content_too_large(content=source, tool_context=tool_context,
                                                                max_tokens=15000)

            if should_save:
                # Generate save location if not provided
                if not save_location:
                    error, workspace_name, _ = self._validate_and_parse_path(file_path)
                    if error:
                        return f"ERROR: Invalid file path: {error}"
                    filename_base = self._generate_filename(
                        file_path, "source", entity_name=entity_name
                    )
                    save_location = f"//{workspace_name}/code_explorer/{filename_base}"

                # tiny markdown formatting
                result = f"# Source: {entity_name} ({entity_type})\n\n```\n{source}\n```"
                await self._save_analysis(result, save_location, tool_context)
                return self._format_result(result, save_location, return_analysis)
            else:
                # Content is small enough, just return it directly
                return source

        except Exception as e:
            self.logger.error(f"Error in get_entity_source: {str(e)}")
            return f"ERROR: {str(e)}"

    @json_schema(
        description="Get just the signature of a specific entity (class, function, or method) without implementation details.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file",
                "required": True
            },
            "entity_type": {
                "type": "string",
                "description": "Type of entity: 'class', 'function', or 'method'",
                "required": True
            },
            "entity_name": {
                "type": "string",
                "description": "Name of the entity",
                "required": True
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            }
        }
    )
    async def get_entity_signature(self, **kwargs) -> str:
        """Get signature for a specific entity.

        Extracts just the signature (declaration) of a specific entity without
        implementation details or documentation.

        Returns:
            Signature or save path
        """
        try:
            file_path = kwargs.get("file_path")
            entity_type = kwargs.get("entity_type")
            entity_name = kwargs.get("entity_name")
            language = kwargs.get("language")
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs,
                                                        required_fields=['file_path', 'entity_type', 'entity_name'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "entity_type": entity_type,
                "entity_name": entity_name,
            }
            if language:
                params["language"] = language

            signature = ace_proto.get_signature(**params)

            if signature is None:
                return f"ERROR: Entity '{entity_name}' of type '{entity_type}' not found in {file_path}"

            result = f"# Signature: {entity_name}\n\n```\n{signature}\n```"

            return result

        except Exception as e:
            self.logger.error(f"Error in get_entity_signature: {str(e)}")
            return f"ERROR: {str(e)}"

    @json_schema(
        description="Get a high-level summary of code structure with counts of classes, functions, and variables. Quick overview without full details.",
        params={
            "file_path": {
                "type": "string",
                "description": "UNC path to the source file to analyze",
                "required": True
            },
            "language": {
                "type": "string",
                "description": "Optional programming language override. Auto-detected if not provided.",
                "required": False
            }
        }
    )
    async def get_code_summary(self, **kwargs) -> str:
        """Get high-level code summary.

        Provides a quick overview of the code including counts of classes,
        functions, and variables, without detailed information about each entity.

        Returns:
            Markdown summary
        """
        try:
            # Extract parameters
            file_path = kwargs.get("file_path")
            language = kwargs.get("language")
            tool_context = kwargs.get("tool_context", {})

            success, message = validate_required_fields(kwargs=kwargs, required_fields=['file_path'])
            if not success:
                return message

            if ace_proto is None:
                return "ERROR: ACE Proto (ts_tool) is not installed"

            # Read file content
            code = await self._read_file(file_path, tool_context)

            params = {
                "code": code,
                "format": 'markdown'
            }
            if language:
                params["language"] = language

            # Call ACE Proto API
            result = ace_proto.get_code_summary(**params)

            return result

        except Exception as e:
            self.logger.error(f"Error in get_code_summary: {str(e)}")
            return f"ERROR: {str(e)}"


    # Removing for now, as we can control this via prompt, but leaving code here for future reference
    # @json_schema(
    #     description="List all programming languages supported by the code analyzer. Use this to check if a specific language can be analyzed.",
    #     params={}
    # )
    # async def list_supported_languages(self, **kwargs) -> str:
    #     """List all supported programming languages.
    #
    #     Returns:
    #         Markdown-formatted list of supported languages
    #     """
    #     try:
    #         if ace_proto is None:
    #             return "ERROR: ACE Proto (ts_tool) is not installed"
    #
    #         languages = ace_proto.get_supported_languages()
    #
    #         # Format as markdown list
    #         md_lines = ["# Supported Programming Languages\n"]
    #         for lang in sorted(languages):
    #             md_lines.append(f"- {lang}")
    #
    #         return "\n".join(md_lines)
    #
    #     except Exception as e:
    #         self.logger.error(f"Error listing languages: {str(e)}")
    #         return f"ERROR: {str(e)}"

# Register the toolset
Toolset.register(AceProtoTools, required_tools=['WorkspaceTools'])
