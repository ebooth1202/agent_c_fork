import json
from typing import Any, Optional
import yaml

from agent_c.toolsets.tool_set import Toolset
from agent_c.toolsets.json_schema import json_schema
from agent_c_tools.helpers.token_helper import is_content_too_large, token_count

from .xml_navigator import XMLNavigator
from agent_c_tools.tools.workspace.tool import WorkspaceTools


class XmlExplorerTools(Toolset):
    """
    Enables your agent to explore, navigate, and extract data from complex XML files efficiently.
    Your agent can analyze XML structure, execute XPath queries, extract specific data sections,
    and work with large XML documents without loading them entirely into memory.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(name='xml', **kwargs)
        self.workspace_tool: Optional[WorkspaceTools] = None

    async def post_init(self):
        self.workspace_tool = self.tool_chest.available_tools['WorkspaceTools']

    @json_schema(
        'Get structure information about a large XML file without loading the entire file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to update',
                'required': True
            },
            'max_depth': {
                'type': 'integer',
                'description': 'Maximum depth to traverse in the XML structure.',
                'required': False
            },
            'sample_count': {
                'type': 'integer',
                'description': 'Number of sample elements to include at each level.',
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
        """Asynchronously retrieves structure information about a large XML file.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to analyze
            max_depth (int, optional): Maximum depth to traverse in the XML structure. Defaults to 3.
            sample_count (int, optional): Number of sample elements to include at each level. Defaults to 5.
            token_limit (int, optional): Maximum tokens before saving to file. Defaults to 25000.

        Returns:
            str: JSON string with structure information or an error message.
        """
        max_depth: int = kwargs.get('max_depth', 3)
        sample_count: int = kwargs.get('sample_count', 5)
        token_limit: int = kwargs.get('token_limit', 25000)
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        navigator = XMLNavigator(workspace)
        result = await navigator.get_structure(relative_path, max_depth, sample_count)

        # Check if content is too large and save to file if needed
        if is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large structure results
            safe_filename = relative_path.replace('/', '_').replace('\\', '_').replace('.', '_')[:50]
            filename = f"xml_structure_{safe_filename}_depth{max_depth}_samples{sample_count}.json"
            save_location = f"//{workspace.name}/xml_explorer/{filename}"

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
                return f"Error': f'Failed to save large structure result: {str(e)}"

        return result

    @json_schema(
        'Execute an XPath query on an XML file using lxml and return matching elements as YAML.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to update',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath query to execute',
                'required': True
            },
            'limit': {
                'type': 'integer',
                'description': 'Max results to return.',
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
        """Asynchronously executes an XPath query on an XML file.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to query
            xpath (str): XPath query to execute on the XML file.
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            token_limit (int, optional): Maximum tokens before saving to file. Defaults to 25000.

        Returns:
            str: JSON string with query results or an error message.
        """
        xpath: str = kwargs['xpath']
        limit: int = kwargs.get('limit', 10)
        token_limit: int = kwargs.get('token_limit', 25000)
        unc_path = kwargs.get('path', '')
        tool_context = kwargs.get('tool_context', {})

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        navigator = XMLNavigator(workspace)
        result = await navigator.xpath_query(relative_path, xpath, limit)

        # Check if content is too large and save to file if needed
        if is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large query results
            safe_xpath = xpath.replace('/', '_').replace('[', '_').replace(']', '_').replace('@', 'attr_')[:50]
            filename = f"xml_query_{safe_xpath}_{limit}_results.json"
            save_location = f"//{workspace.name}/xml_explorer/{filename}"

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
                    'query': xpath,
                    'limit': limit,
                    'token_limit': token_limit
                }, allow_unicode=True, sort_keys=False)
            except Exception as e:
                return f"Error': 'Failed to save large query result: {str(e)}"

        return result

    @json_schema(
        'Extract a subtree from an XML file as YAML using lxml.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to update',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the root element of the subtree to extract.',
                'required': True
            },
            'output_path': {
                'type': 'string',
                'description': 'Optional path to save the extracted subtree.',
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
        """Asynchronously extracts a subtree from an XML file.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to extract from
            xpath (str): XPath to the root element of the subtree to extract.
            output_path (str, optional): UNC-style path to save the extracted subtree.
            token_limit (int, optional): Maximum tokens before saving to file. Defaults to 25000.

        Returns:
            str: JSON string with the extracted subtree or a status message.
        """
        xpath: str = kwargs['xpath']
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
        output_workspace = None
        if output_path:
            if output_path.startswith('//'):
                # UNC path for output
                error, output_workspace, output_relative_path = self.workspace_tool.validate_and_get_workspace_path(output_path)
                if error:
                    return json.dumps({'error': f'Invalid output path: {error}'})
            else:
                # Assume relative path in same workspace
                output_workspace = workspace
                output_relative_path = output_path

        navigator = XMLNavigator(workspace)
        result = await navigator.extract_subtree(relative_path, xpath, output_relative_path)
        
        # Check if content is too large and save to file if needed (only if no output_path was specified)
        if not output_path and is_content_too_large(content=result, tool_context=tool_context, max_tokens=token_limit):
            # Generate save location for large extracted subtree
            safe_xpath = xpath.replace('/', '_').replace('[', '_').replace(']', '_').replace('@', 'attr_')[:50]
            filename = f"xml_extract_{safe_xpath}_subtree.json"
            save_location = f"//{workspace.name}/xml_explorer/{filename}"

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
                    'xpath': xpath,
                    'token_limit': token_limit
                }, allow_unicode=True, sort_keys=False)
            except Exception as e:
                return f"Error': 'Failed to save large extracted subtree: {str(e)}'"

        return result


# Register the toolset
Toolset.register(XmlExplorerTools, required_tools=['WorkspaceTools'])