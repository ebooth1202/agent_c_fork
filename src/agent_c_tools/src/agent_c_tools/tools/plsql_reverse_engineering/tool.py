"""
PL/SQL Reverse Engineering Tools

Provides comprehensive analysis and understanding of Oracle PL/SQL codebases
through automated reverse engineering and documentation generation.
"""

import asyncio
import itertools
import threading
from typing import Any, Dict, List, Optional, cast

import yaml

from agent_c.models.agent_config import AgentConfiguration, AgentConfigurationV2
from agent_c.toolsets.json_schema import json_schema
from agent_c.toolsets.tool_set import Toolset
from agent_c_tools.tools.agent_assist.base import AgentAssistToolBase
from agent_c_tools.tools.plsql_reverse_engineering.prompt import PlSqlRevEngSection
from agent_c_tools.tools.plsql_reverse_engineering.plsql_parser import (
    extract_all_units,
    get_unit_source,
    PlSqlUnit
)
from agent_c_tools.tools.workspace.base import BaseWorkspace
from agent_c_tools.tools.workspace.tool import WorkspaceTools


class PlsqlReverseEngineeringTools(AgentAssistToolBase):
    """
    PL/SQL Reverse Engineering Tools provides methods for analyzing Oracle PL/SQL codebases.
    
    It performs deep structural analysis, understanding packages, procedures, functions,
    triggers, and other PL/SQL constructs to generate comprehensive documentation and
    reverse engineer business requirements from implementation.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(name='plsql_rev_eng', **kwargs)
        
        # Default PL/SQL file extensions
        self.default_extensions = [
            '.sql', '.pks', '.pkb', '.prc', '.fnc', '.trg',
            '.spc', '.bdy', '.pkg', '.pls', '.plb', '.pck'
        ]
        
        self.section = PlSqlRevEngSection()
        
        # Agent configurations for analysis
        self.recon_oneshot = self.agent_loader.catalog['recon_oneshot']
        self.recon_revise_oneshot = self.agent_loader.catalog['recon_revise_oneshot']
        self.recon_answers_oneshot = self.agent_loader.catalog['recon_answers_oneshot']
        
        # Maximum file size in tokens before using chunked reading (conservative estimate)
        self.max_file_tokens = 40000  # Stay under 50k limit with buffer

    def _get_safe_tool_context_values(self, tool_context: Dict[str, Any]) -> tuple:
        """
        Safely extract required values from tool_context with defaults.
        
        Returns:
            tuple: (client_wants_cancel, session_id)
        """
        # Get client_wants_cancel with a default Event if missing
        client_wants_cancel = tool_context.get('client_wants_cancel')
        if client_wants_cancel is None:
            self.logger.warning("client_wants_cancel not found in tool_context, creating default Event")
            client_wants_cancel = threading.Event()
        
        # Get session_id with a default if missing
        session_id = tool_context.get('session_id')
        if session_id is None:
            self.logger.warning("session_id not found in tool_context, using 'unknown-session'")
            session_id = 'unknown-session'
        
        return client_wants_cancel, session_id

    async def _parallel_agent_oneshots(
        self,
        messages: List[str],
        persona: AgentConfiguration,
        user_session_id: str,
        tool_context: Dict[str, Any],
        client_wants_cancel: threading.Event
    ) -> List[Optional[List[Dict[str, Any]]]]:
        """Run multiple agent oneshots in parallel using asyncio.gather."""
        # Get the calling agent config for prime_agent_key
        calling_agent_config = tool_context.get('agent_config', tool_context.get('active_agent'))
        prime_agent_key = calling_agent_config.key if calling_agent_config else "unknown"
        
        tasks = [
            self.agent_oneshot(
                user_message=msg,
                agent=persona,
                parent_session_id=user_session_id,
                user_session_id=user_session_id,
                parent_tool_context=tool_context,
                client_wants_cancel=client_wants_cancel,
                sub_agent_type="tool",
                prime_agent_key=prime_agent_key
            )
            for msg in messages
        ]
        return await asyncio.gather(*tasks)

    async def _read_large_file(self, workspace: BaseWorkspace, file_path: str) -> str:
        """
        Read a potentially large file, handling token limits gracefully.
        
        workspace.read_internal() bypasses token limits, so we use that directly.
        This allows us to read files of any size for parsing, then we only send
        individual units (which are smaller) to the AI agents.
        
        Args:
            workspace: The workspace containing the file
            file_path: Relative path to the file within the workspace
            
        Returns:
            Full file contents as a string
            
        Raises:
            Exception if the file cannot be read
        """
        try:
            # read_internal bypasses the token limit checks in the workspace.read() tool method
            content = await workspace.read_internal(file_path, encoding='utf-8')
            return content
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {str(e)}")
            raise Exception(f"Unable to read file {file_path}: {str(e)}")

    async def _prepare_unit_for_analysis(self, workspace_name: str, file_path: str, unit: PlSqlUnit, full_source: str) -> str:
        """
        Prepare a PL/SQL unit for analysis by providing context.
        
        Args:
            workspace_name: Name of the workspace
            file_path: Path to the file containing the unit
            unit: The PlSqlUnit to analyze
            full_source: The full source code of the file
            
        Returns:
            Formatted context string for analysis
        """
        unit_source = get_unit_source(full_source, unit)
        
        context_parts = [
            f"File: //{workspace_name}/{file_path}",
            f"Unit Type: {unit.unit_type}",
            f"Name: {unit.name}",
            f"Lines: {unit.start_line}-{unit.end_line}",
        ]
        
        if unit.signature:
            context_parts.append(f"Signature: {unit.signature}")
        
        if unit.package_name:
            context_parts.append(f"Package: {unit.package_name}")
        
        context_parts.extend([
            "",
            "Source Code:",
            "```sql",
            unit_source,
            "```"
        ])
        
        return "\n".join(context_parts)

    async def _analyze_plsql_file(
        self,
        workspace_name: str,
        file_path: str,
        source: str,
        tool_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Analyze a single PL/SQL file and extract all units.
        
        Returns:
            List of analysis contexts for each unit found
        """
        units = extract_all_units(source)
        
        if not units:
            # No structured units found, analyze as a whole file
            return [{
                'context': f"File: //{workspace_name}/{file_path}\n\nSource Code:\n```sql\n{source}\n```",
                'file_path': file_path,
                'unit_type': 'file',
                'unit_name': file_path
            }]
        
        # Prepare analysis contexts for each unit
        analysis_items = []
        for unit in units:
            context = await self._prepare_unit_for_analysis(workspace_name, file_path, unit, source)
            analysis_items.append({
                'context': context,
                'file_path': file_path,
                'unit_type': unit.unit_type,
                'unit_name': unit.name,
                'unit': unit
            })
        
        return analysis_items

    @json_schema(
        'Perform an in-depth analysis of all PL/SQL files matching a glob pattern. '
        'Output will be saved to the scratchpad of the workspace containing the code.',
        {
            'glob': {
                'type': 'string',
                'description': 'A glob pattern in workspace UNC format. Equivalent to `glob.glob` in Python '
                              'with recursive=True. e.g. //workspace/**/*.sql or //workspace/**/*.pkb',
                'required': True
            },
            'batch_size': {
                'type': 'integer',
                'description': 'Number of units to process in parallel (default: 2)',
                'required': False
            }
        }
    )
    async def plsql_analyze_source(self, **kwargs) -> str:
        """Analyze PL/SQL source files matching a glob pattern."""
        tool_context: Dict[str, Any] = kwargs['tool_context']
        client_wants_cancel, _ = self._get_safe_tool_context_values(tool_context)
        glob_pattern: str = kwargs.get('glob')
        batch_size: int = kwargs.get('batch_size', 2)
        
        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(glob_pattern)
        if error is not None:
            return f"Error: {error}"

        files = await workspace.glob(relative_path, True)
        
        if not files:
            return f"No files found matching pattern: {glob_pattern}"

        await self._render_media_markdown(
            f"## PL/SQL Analysis Started\n\nFound {len(files)} files matching pattern.\n",
            "plsql_analyze_source",
            tool_context=tool_context
        )

        # Extract all units from all files
        all_analysis_items = []
        for file_path in files:
            if client_wants_cancel.is_set():
                await self._render_media_markdown(
                    "**Processing cancelled by user.**",
                    "plsql_analyze_source",
                    tool_context=tool_context
                )
                return f"Analysis cancelled. Processed {len(all_analysis_items)} units before cancellation."

            try:
                # Use read_internal to bypass token limits for parsing
                # (we only send small units to agents, not the full file)
                source = await self._read_large_file(workspace, file_path)
                items = await self._analyze_plsql_file(workspace.name, file_path, source, tool_context)
                all_analysis_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
                await self._render_media_markdown(
                    f"⚠️ Error analyzing `{file_path}`: {str(e)}\n",
                    "plsql_analyze_source",
                    tool_context=tool_context
                )

        await self._render_media_markdown(
            f"\nExtracted {len(all_analysis_items)} PL/SQL units for analysis.\n",
            "plsql_analyze_source",
            tool_context=tool_context
        )

        # Perform two-pass analysis
        await self._pass_one(workspace, all_analysis_items, batch_size, tool_context, client_wants_cancel)
        await self._pass_two(workspace, all_analysis_items, tool_context, client_wants_cancel)

        return (
            f"Analysis complete! Processed {len(files)} files containing {len(all_analysis_items)} PL/SQL units.\n"
            f"Results saved to: //{workspace.name}/.scratch/plsql_analyze_source/"
        )

    @json_schema(
        'Perform an in-depth analysis of all PL/SQL code in a source tree. '
        'Output will be saved to the scratchpad of the workspace containing the code.',
        {
            'start_path': {
                'type': 'string',
                'description': 'A path to a folder, in workspace UNC format, to start the analysis from. '
                              'Equivalent to `os.walk` in Python. e.g. //workspace/database/packages',
                'required': True
            },
            'extensions': {
                'type': 'array',
                'description': 'A list of file extensions to include in the analysis. '
                              'e.g. [".sql", ".pks", ".pkb", ".prc", ".fnc"]',
                'items': {
                    'type': 'string'
                },
                'required': False
            },
            'batch_size': {
                'type': 'integer',
                'description': 'Number of units to process in parallel (default: 2)',
                'required': False
            }
        }
    )
    async def plsql_analyze_tree(self, **kwargs) -> str:
        """Analyze all PL/SQL files in a directory tree."""
        tool_context: Dict[str, Any] = kwargs['tool_context']
        client_wants_cancel, _ = self._get_safe_tool_context_values(tool_context)
        start_path: str = kwargs.get('start_path')
        batch_size: int = kwargs.get('batch_size', 2)
        extensions: List[str] = kwargs.get('extensions', self.default_extensions)
        
        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(start_path)
        if error is not None:
            return f"Error: {error}"

        error, files = await workspace.walk(relative_path, extensions)
        if error is not None:
            return f"Error: {error}"
        
        if not files:
            return f"No PL/SQL files found in: {start_path}"

        await self._render_media_markdown(
            f"## PL/SQL Tree Analysis Started\n\nFound {len(files)} PL/SQL files in tree.\n",
            "plsql_analyze_tree",
            tool_context=tool_context
        )

        # Extract all units from all files
        all_analysis_items = []
        for file_path in files:
            if client_wants_cancel.is_set():
                await self._render_media_markdown(
                    "**Processing cancelled by user.**",
                    "plsql_analyze_tree",
                    tool_context=tool_context
                )
                return f"Analysis cancelled. Processed {len(all_analysis_items)} units before cancellation."

            try:
                # Use read_internal to bypass token limits for parsing
                # (we only send small units to agents, not the full file)
                source = await self._read_large_file(workspace, file_path)
                items = await self._analyze_plsql_file(workspace.name, file_path, source, tool_context)
                all_analysis_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
                await self._render_media_markdown(
                    f"⚠️ Error analyzing `{file_path}`: {str(e)}\n",
                    "plsql_analyze_tree",
                    tool_context=tool_context
                )

        await self._render_media_markdown(
            f"\nExtracted {len(all_analysis_items)} PL/SQL units for analysis.\n",
            "plsql_analyze_tree",
            tool_context=tool_context
        )

        # Perform two-pass analysis
        await self._pass_one(workspace, all_analysis_items, batch_size, tool_context, client_wants_cancel)
        await self._pass_two(workspace, all_analysis_items, tool_context, client_wants_cancel)

        return (
            f"Analysis complete! Processed {len(files)} files containing {len(all_analysis_items)} PL/SQL units.\n"
            f"Results saved to: //{workspace.name}/.scratch/plsql_analyze_source/"
        )

    @json_schema(
        'Query an expert about the analyzed PL/SQL codebase in a given workspace. '
        'The expert can examine the analysis output and the code itself to answer your questions.',
        {
            'request': {
                'type': 'string',
                'description': 'A question or request for information about the PL/SQL codebase and/or its analysis.',
                'required': True
            },
            'workspace': {
                'type': 'string',
                'description': 'The workspace containing the output of `plsql_analyze_source` or `plsql_analyze_tree`.',
                'required': True
            }
        }
    )
    async def plsql_query_analysis(self, **kwargs) -> str:
        """Query an expert about the analyzed PL/SQL codebase."""
        tool_context: Dict[str, Any] = kwargs['tool_context']
        client_wants_cancel, session_id = self._get_safe_tool_context_values(tool_context)
        request: str = kwargs.get('request')
        workspace_name: str = kwargs.get('workspace')
        
        # Get the calling agent config for prime_agent_key
        calling_agent_config = tool_context.get('agent_config', tool_context.get('active_agent'))
        if calling_agent_config is None:
            return "ERROR: No agent configuration found in tool context. This tool requires an active agent configuration to function."

        workspace = self.workspace_tool.find_workspace_by_name(workspace_name)
        if not workspace:
            return f"Error: Workspace '{workspace_name}' not found."

        # Get the analysis tree structure
        try:
            tree = await workspace.tree('.scratch/plsql_analyze_source/enhanced', 10, 5)
        except Exception as e:
            return (
                f"Error: Could not find analysis results in workspace '{workspace_name}'.\n"
                f"Make sure you've run `plsql_analyze_source` or `plsql_analyze_tree` first.\n"
                f"Details: {str(e)}"
            )

        # Configure the expert agent
        agent_config = self.recon_answers_oneshot.model_dump()
        agent_config['persona'] = (
            agent_config['persona']
            .replace('[workspace]', workspace_name)
            .replace('[workspace_tree]', tree)
        )
        agent = AgentConfigurationV2(**agent_config)

        # Query the expert
        messages = await self.agent_oneshot(
            user_message=request,
            agent=agent,
            parent_session_id=session_id,
            user_session_id=session_id,
            parent_tool_context=tool_context,
            client_wants_cancel=client_wants_cancel,
            sub_agent_type="tool",
            prime_agent_key=calling_agent_config.key
        )
        
        last_message = messages[-1] if messages else None
        return yaml.dump(last_message, allow_unicode=True) if last_message else "No response from expert."

    async def _pass_one(
        self,
        workspace,
        analysis_items: List[Dict[str, Any]],
        batch_size: int,
        tool_context: Dict[str, Any],
        client_wants_cancel: threading.Event
    ) -> List[str]:
        """
        First pass: Initial analysis of each unit.
        
        Uses parallel processing for efficiency when batch_size > 1.
        """
        pass_one_results = []
        parallel = batch_size > 1
        session_id = tool_context.get('session_id', 'unknown-session')

        await self._render_media_markdown(
            f"\n### Pass 1: Initial Analysis\n\nProcessing {len(analysis_items)} units...\n",
            "plsql_analysis",
            tool_context=tool_context
        )

        if parallel:
            iterator = iter(analysis_items)
            batch_num = 0
            while batch := list(itertools.islice(iterator, batch_size)):
                if client_wants_cancel.is_set():
                    await self._render_media_markdown(
                        "**Processing cancelled by user.**",
                        "plsql_analysis",
                        tool_context=tool_context
                    )
                    return pass_one_results

                batch_num += 1
                unit_names = ", ".join([f"{item['unit_type']}:{item['unit_name']}" for item in batch])
                await self._render_media_markdown(
                    f"\n**Batch {batch_num}** (Pass 1): {unit_names}...",
                    "plsql_analysis",
                    tool_context=tool_context
                )

                contexts = [item['context'] for item in batch]
                results = await self._parallel_agent_oneshots(
                    messages=contexts,
                    persona=self.recon_oneshot,
                    user_session_id=session_id,
                    tool_context=tool_context,
                    client_wants_cancel=client_wants_cancel
                )
                
                pass_one_results.extend(results)
                await self._render_media_markdown(
                    f" ✓ Complete\n",
                    "plsql_analysis",
                    tool_context=tool_context
                )
        else:
            for idx, item in enumerate(analysis_items, 1):
                if client_wants_cancel.is_set():
                    await self._render_media_markdown(
                        "**Processing cancelled by user.**",
                        "plsql_analysis",
                        tool_context=tool_context
                    )
                    return pass_one_results

                await self._render_media_markdown(
                    f"\n**Unit {idx}/{len(analysis_items)}** (Pass 1): {item['unit_type']}:{item['unit_name']}...",
                    "plsql_analysis",
                    tool_context=tool_context
                )

                # Get the calling agent config for prime_agent_key
                calling_agent_config = tool_context.get('agent_config', tool_context.get('active_agent'))
                
                result = await self.agent_oneshot(
                    user_message=item['context'],
                    agent=self.recon_oneshot,
                    parent_session_id=session_id,
                    user_session_id=session_id,
                    parent_tool_context=tool_context,
                    client_wants_cancel=client_wants_cancel,
                    sub_agent_type="tool",
                    prime_agent_key=calling_agent_config.key if calling_agent_config else "unknown"
                )
                
                pass_one_results.append(result)
                await self._render_media_markdown(
                    f" ✓ Complete\n",
                    "plsql_analysis",
                    tool_context=tool_context
                )

        return pass_one_results

    async def _pass_two(
        self,
        workspace,
        analysis_items: List[Dict[str, Any]],
        tool_context: Dict[str, Any],
        client_wants_cancel: threading.Event
    ) -> List[str]:
        """
        Second pass: Refinement and enhancement of initial analysis.
        
        Sequential processing to ensure quality and depth.
        """
        pass_two_results = []
        session_id = tool_context.get('session_id', 'unknown-session')

        await self._render_media_markdown(
            f"\n### Pass 2: Refinement & Enhancement\n\nProcessing {len(analysis_items)} units...\n",
            "plsql_analysis",
            tool_context=tool_context
        )

        for idx, item in enumerate(analysis_items, 1):
            if client_wants_cancel.is_set():
                await self._render_media_markdown(
                    "**Processing cancelled by user.**",
                    "plsql_analysis",
                    tool_context=tool_context
                )
                return pass_two_results

            await self._render_media_markdown(
                f"\n**Unit {idx}/{len(analysis_items)}** (Pass 2): {item['unit_type']}:{item['unit_name']}...",
                "plsql_analysis",
                tool_context=tool_context
            )

            # Get the calling agent config for prime_agent_key
            calling_agent_config = tool_context.get('agent_config', tool_context.get('active_agent'))
            
            result = await self.agent_oneshot(
                user_message=item['context'],
                agent=self.recon_revise_oneshot,
                parent_session_id=session_id,
                user_session_id=session_id,
                parent_tool_context=tool_context,
                client_wants_cancel=client_wants_cancel,
                sub_agent_type="tool",
                prime_agent_key=calling_agent_config.key if calling_agent_config else "unknown"
            )
            
            pass_two_results.append(result)
            await self._render_media_markdown(
                f" ✓ Complete\n",
                "plsql_analysis",
                tool_context=tool_context
            )

        await self._render_media_markdown(
            f"\n## Analysis Complete! ✨\n\nAll {len(analysis_items)} units have been analyzed.\n",
            "plsql_analysis",
            tool_context=tool_context
        )

        return pass_two_results


# Register the toolset
Toolset.register(PlsqlReverseEngineeringTools, required_tools=['WorkspaceTools'])
