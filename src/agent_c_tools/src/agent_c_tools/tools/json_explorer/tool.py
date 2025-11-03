"""JSON Explorer Tools - Toolset for navigating and querying JSON files."""

import json
from typing import Any, Optional
import yaml

from agent_c.toolsets.tool_set import Toolset
from agent_c.toolsets.json_schema import json_schema
from agent_c_tools.helpers.token_helper import is_content_too_large, token_count

from .json_navigator import JSONNavigator
from agent_c_tools.tools.workspace.tool import WorkspaceTools


class JsonExplorerTools(Toolset):
    """
    Enables your agent to explore, navigate, and extract data from JSON files efficiently.
    Your agent can analyze JSON structure, execute JSONPath queries, extract specific data sections
    with depth control, and work with JSON documents of any structure or depth.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(name='json_explorer', **kwargs)
        self.workspace_tool: Optional[WorkspaceTools] = None

    async def post_init(self):
        self.workspace_tool = self.tool_chest.available_tools['WorkspaceTools']

    @json_schema(
        'Get structure information about a JSON file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'max_depth': {
                'type': 'integer',
                'description': 'Maximum depth to traverse in the JSON structure. Defaults to 3.',
                'required': False
            },
            'sample_count': {
                'type': 'integer',
                'description': 'Number of sample elements to include at each level. Defaults to 5.',
                'required': False
            },
            'token_limit': {
                'type': 'integer',
                'description': 'Maximum tokens before saving to file. Defaults to 25000.',
                'required': False,
                'default': 25000
            }
        }
    )
    async def structure(self, **kwargs: Any) -> str:
        """
        Get a structural overview of a JSON file.

        Args:
            path: UNC-style path (//WORKSPACE/path) to the JSON file
            max_depth: Maximum depth to traverse (default: 3)
            sample_count: Number of samples at each level (default: 5)
            token_limit: Max tokens before saving to file (default: 25000)

        Returns:
            JSON string with structure information or error message
        """
        max_depth: int = kwargs.get('max_depth', 3)
        sample_count: int = kwargs.get('sample_count', 5)
        token_limit: int = kwargs.get('token_limit', 25000)
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        navigator = JSONNavigator(workspace)
        result = await navigator.get_structure(relative_path, max_depth, sample_count)

        # Check if content is too large and save to file if needed
        if is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large structure results
            safe_filename = relative_path.replace('/', '_').replace('\\', '_').replace('.', '_')[:50]
            filename = f"json_structure_{safe_filename}_depth{max_depth}_samples{sample_count}.json"
            save_location = f"//{workspace.name}/.scratch/json_explorer/{filename}"

            # Save the result to file
            try:
                await self.workspace_tool.write(
                    path=save_location,
                    data=result,
                    mode='write',
                    tool_context=tool_context
                )

                return yaml.dump({
                    'success': True,
                    'message': f'Structure results too large ({token_count(content=result, tool_context=tool_context)} tokens), saved to file',
                    'saved_to': save_location,
                    'max_depth': max_depth,
                    'sample_count': sample_count,
                    'token_limit': token_limit
                }, allow_unicode=True, sort_keys=False)
            except Exception as e:
                return f"ERROR: Failed to save large structure result: {str(e)}"

        return result

    @json_schema(
        'Execute a JSONPath query on a JSON file and return matching elements.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath query to execute (e.g., "$.users[*].name" or "$.data.items[0]")',
                'required': True
            },
            'limit': {
                'type': 'integer',
                'description': 'Maximum number of results to return. Defaults to 10.',
                'required': False
            },
            'token_limit': {
                'type': 'integer',
                'description': 'Maximum tokens before saving to file. Defaults to 25000.',
                'required': False,
                'default': 25000
            }
        }
    )
    async def query(self, **kwargs: Any) -> str:
        """
        Execute a JSONPath query on a JSON file.

        Args:
            path: UNC-style path (//WORKSPACE/path) to the JSON file
            jsonpath: JSONPath query to execute
            limit: Maximum number of results to return (default: 10)
            token_limit: Max tokens before saving to file (default: 25000)

        Returns:
            JSON string with query results or error message
        """
        jsonpath: str = kwargs['jsonpath']
        limit: int = kwargs.get('limit', 10)
        token_limit: int = kwargs.get('token_limit', 25000)
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        navigator = JSONNavigator(workspace)
        result = await navigator.jsonpath_query(relative_path, jsonpath, limit)

        # Check if content is too large and save to file if needed
        if is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large query results
            safe_jsonpath = jsonpath.replace('$', 'root').replace('.', '_').replace('[', '_').replace(']', '_')[:50]
            filename = f"json_query_{safe_jsonpath}_{limit}_results.json"
            save_location = f"//{workspace.name}/.scratch/json_explorer/{filename}"

            # Save the result to file
            try:
                await self.workspace_tool.write(
                    path=save_location,
                    data=result,
                    mode='write',
                    tool_context=tool_context
                )

                return yaml.dump({
                    'success': True,
                    'message': f'Query results too large ({token_count(content=result, tool_context=tool_context)} tokens), saved to file',
                    'saved_to': save_location,
                    'query': jsonpath,
                    'limit': limit,
                    'token_limit': token_limit
                }, allow_unicode=True, sort_keys=False)
            except Exception as e:
                return f"ERROR: Failed to save large query result: {str(e)}"

        return result

    @json_schema(
        'Extract a subtree from a JSON file with depth control.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the root of the subtree to extract (e.g., "$.users[0]" or "$.config")',
                'required': True
            },
            'max_depth': {
                'type': 'integer',
                'description': 'Maximum depth to include. None/omit = unlimited, 0 = just the node, 1 = node + immediate children, 2 = grandchildren, etc.',
                'required': False
            },
            'output_path': {
                'type': 'string',
                'description': 'Optional UNC-style path to save the extracted subtree',
                'required': False
            },
            'token_limit': {
                'type': 'integer',
                'description': 'Maximum tokens before saving to file. Defaults to 25000.',
                'required': False,
                'default': 25000
            }
        }
    )
    async def extract(self, **kwargs: Any) -> str:
        """
        Extract a subtree from a JSON file with depth control.

        Args:
            path: UNC-style path (//WORKSPACE/path) to the JSON file
            jsonpath: JSONPath to the root of the subtree
            max_depth: Number of levels to include (None = all, 0 = node only, 1 = node + children, etc.)
            output_path: Optional path to save the extracted subtree
            token_limit: Max tokens before saving to file (default: 25000)

        Returns:
            JSON string with the extracted subtree or status message
        """
        jsonpath: str = kwargs['jsonpath']
        max_depth: Optional[int] = kwargs.get('max_depth')
        output_path: Optional[str] = kwargs.get('output_path')
        token_limit: int = kwargs.get('token_limit', 25000)
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        # Validate input path
        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        # Validate output path if provided
        output_relative_path = None
        if output_path:
            if output_path.startswith('//'):
                # UNC path for output
                error, output_workspace, output_relative_path = self.workspace_tool.validate_and_get_workspace_path(output_path)
                if error:
                    return json.dumps({'error': f'Invalid output path: {error}'})
            else:
                # Assume relative path in same workspace
                output_relative_path = output_path

        navigator = JSONNavigator(workspace)
        result = await navigator.extract_subtree(relative_path, jsonpath, max_depth, output_relative_path)

        # Check if content is too large and save to file if needed (only if no output_path was specified)
        if not output_path and is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large extracted subtree
            safe_jsonpath = jsonpath.replace('$', 'root').replace('.', '_').replace('[', '_').replace(']', '_')[:50]
            depth_str = f"depth{max_depth}" if max_depth is not None else "unlimited"
            filename = f"json_extract_{safe_jsonpath}_{depth_str}.yaml"
            save_location = f"//{workspace.name}/.scratch/json_explorer/{filename}"

            # Save the result to file
            try:
                await self.workspace_tool.write(
                    path=save_location,
                    data=result,
                    mode='write',
                    tool_context=tool_context
                )

                return yaml.dump({
                    'success': True,
                    'message': f'Extracted subtree too large ({token_count(content=result, tool_context=tool_context)} tokens), saved to file',
                    'saved_to': save_location,
                    'jsonpath': jsonpath,
                    'max_depth': max_depth if max_depth is not None else 'unlimited',
                    'token_limit': token_limit
                }, allow_unicode=True, sort_keys=False)
            except Exception as e:
                return f"ERROR: Failed to save large extracted subtree: {str(e)}"

        return result

    @json_schema(
        'Get a simple value at a specific JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the value (e.g., "$.config.timeout" or "$.users[0].name")',
                'required': True
            }
        }
    )
    async def get_value(self, **kwargs: Any) -> str:
        """
        Get a simple value at a specific JSONPath.

        Args:
            path: UNC-style path (//WORKSPACE/path) to the JSON file
            jsonpath: JSONPath to the value

        Returns:
            JSON string with the value or error message
        """
        jsonpath: str = kwargs['jsonpath']
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        navigator = JSONNavigator(workspace)
        result = await navigator.get_value(relative_path, jsonpath)

        return result


# Register the toolset
Toolset.register(JsonExplorerTools, required_tools=['WorkspaceTools'])
