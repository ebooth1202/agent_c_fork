import re
import json
import mimetypes
from pathlib import Path

from typing import Any, List, Tuple, Optional, Callable, Awaitable, Union

from agent_c.toolsets.tool_set import Toolset
from agent_c.models.context.base import BaseContext
from agent_c.toolsets.json_schema import json_schema
from agent_c_tools.helpers.validate_kwargs import validate_required_fields
from agent_c_tools.tools.workspace.base import BaseWorkspace
from agent_c_tools.tools.workspace.executors.local_storage.secure_command_executor import CommandExecutionResult
from agent_c_tools.tools.workspace.executors.local_storage.media_event_helper.media_helper import MediaEventHelper
from agent_c_tools.tools.workspace.prompt import WorkspaceSection
from agent_c_tools.tools.workspace.util import ReplaceStringsHelper
from agent_c_tools.tools.workspace.context import WorkspaceToolsContext


class WorkspaceTools(Toolset):
    """
    Gives your agent comprehensive file management capabilities across multiple workspaces and storage systems.
    Your agent can read, write, search, organize files and folders, manage projects, and work with both local
    and cloud storage seamlessly using simple path-based commands.
    """

    UNC_PATH_PATTERN = r'^//([^/]+)(?:/(.*))?$'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, name="workspace")
        self.workspaces: List[BaseWorkspace] = kwargs.get('workspaces', [])
        self.section = WorkspaceSection(tool=self)

        self.replace_helper = ReplaceStringsHelper()

    @classmethod
    def default_context(cls) -> Optional[BaseContext]:
        """Return the default context for this toolset."""
        return WorkspaceToolsContext()

    def add_workspace(self, workspace: BaseWorkspace) -> None:
        """Add a workspace to the list of workspaces."""
        self.workspaces.append(workspace)

    def find_workspace_by_name(self, name):
        """Find a workspace by its name."""
        try:
            norm_name = name.lower()
            return next(workspace for workspace in self.workspaces if workspace.name == norm_name)
        except StopIteration:
            # Handle the case where no workspace with the given name is found
            self.logger.warning(f"No workspace found with the name: {name}")
            return None

    def _parse_unc_path(self, path: str) -> Tuple[Optional[str], Optional[BaseWorkspace], Optional[str]]:
        """
        Parse a UNC path (//WORKSPACE/path) into workspace name and relative path.

        Args:
            path (str): The UNC path to parse

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]]:
                - Error message (if any)
                - Workspace name (if no error)
                - Relative path (if no error)
        """
        if not path:
            return "Path cannot be empty", None, None

        match = re.match(self.UNC_PATH_PATTERN, path)
        if not match:
            return f"Invalid UNC path format: {path}. Expected format: //WORKSPACE/path", None, None

        workspace_name = match.group(1)
        relative_path = match.group(2) or ''

        workspace = self.find_workspace_by_name(workspace_name)
        if workspace is None:
            return f"No workspace found with the name: {workspace_name}", None, None

        return None, workspace, relative_path

    async def _run_cp_or_mv(self, operation: Callable[[object, str, str], Awaitable[str]], *, src_path: str,
                            dest_path: str) -> str:
        """
        Validate UNC paths, ensure same workspace, then perform the operation.
        """
        # Validate paths
        src_error, src_workspace, src_relative_path = self.validate_and_get_workspace_path(src_path)
        if src_error:
            return json.dumps({'error': src_error})

        dest_error, dest_workspace, dest_relative_path = self.validate_and_get_workspace_path(dest_path)
        if dest_error:
            return json.dumps({'error': dest_error})

        # Same-workspace check
        if src_workspace != dest_workspace:
            error_msg = ("Cross-workspace operations are not supported. "
                         "Source and destination must be in the same workspace.")
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})

        # Do the copy or move
        return await operation(src_workspace, src_relative_path, dest_relative_path)

    def validate_and_get_workspace_path(self, unc_path: str) -> Tuple[
        Optional[str], Optional[BaseWorkspace], Optional[str]]:
        """
        Validate a UNC path and return the workspace object and relative path.

        Args:
            unc_path (str): UNC-style path to validate

        Returns:
            Tuple[Optional[str], Optional[BaseWorkspace], Optional[str]]:
                - Error message (if any)
                - Workspace object (if no error)
                - Relative path (if no error)
        """
        error, workspace, relative_path = self._parse_unc_path(unc_path)
        if error:
            self.logger.error(error)
            return error, None, None

        return None, workspace, relative_path

    @json_schema(
        'List the contents of a directory using UNC-style path (//WORKSPACE/path)',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to list contents for',
                'required': True
            },
            'max_tokens': {
                'type': 'integer',
                'description': 'Maximum size in tokens for the response. Default is 5000.',
                'required': False
            },
        }
    )
    async def ls(self, **kwargs: Any) -> str:
        """Asynchronously lists the contents of a workspace directory.

        Args:
            **kwargs: Keyword arguments.
                path (str): UNC-style path (//WORKSPACE/path) to list contents for

        Returns:
            str: JSON string with the listing or an error message.
        """
        unc_path = kwargs.get('path', '')
        max_tokens = kwargs.get('max_tokens', 5000)

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f"Error: {str(error)}"

        content = await workspace.ls(relative_path)
        if not isinstance(content, str):
            content = self._yaml_dump(content)

        token_count = self._count_tokens(content, kwargs.get("tool_context"))
        if token_count > max_tokens:
            return (f"ERROR: The content of this directory listing exceeds max_tokens limit of {max_tokens}. "
                    f"Content token count: {token_count}. You will need use a clone with a raised token limit.")

        return content

    @json_schema(
        'Retrieve a string "tree" of the directory structure using UNC-style path',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to start the tree from',
                'required': True
            },
            'folder_depth': {
                'type': 'integer',
                'description': 'Depth of folders to include in the tree',
                'required': False
            },
            'file_depth': {
                'type': 'integer',
                'description': 'Depth of files to include in the tree',
                'required': False
            },
            "max_tokens": {
                "type": "integer",
                "description": "Maximum size in tokens for the response. Default is 4000.",
                "required": False
            }
        }
    )
    async def tree(self, **kwargs: Any) -> str:
        """Asynchronously generates a tree view of a directory.

        Args:
            **kwargs: Keyword arguments.
                path (str): UNC-style path (//WORKSPACE/path) to start the tree from
                folder_depth (int): Depth of folders to include in the tree, default 5
                file_depth (int): Depth of files to include in the tree, default 3

        Returns:
            str: JSON string with the tree view or an error message.
        """
        unc_path = kwargs.get('path', '')
        folder_depth = kwargs.get('folder_depth', 5)
        file_depth = kwargs.get('file_depth', 3)
        tool_context = kwargs.get("tool_context")
        max_tokens = kwargs.get("max_tokens", 4000)

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f'ERROR: {error}'

        tree_content = await workspace.tree(relative_path, folder_depth, file_depth)
        token_count = self._count_tokens(tree_content, tool_context)
        if token_count > max_tokens:
            return (f"ERROR: The content of this tree exceeds max_tokens limit of {max_tokens}. "
                    f"Content token count: {token_count}. You will need request less depth or raise the token limit.")

        return tree_content

    @json_schema(
        'Reads the contents of a text file using UNC-style path',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to read',
                'required': True
            },
            'encoding': {
                'type': 'string',
                'description': 'The encoding to use for reading the file, default is "utf-8"',
                'required': False
            },
            'max_tokens': {
                'type': 'integer',
                'description': 'Maximum number of tokens to read from the file. Default is 25k.',
                'required': False
            }
        }
    )
    async def read(self, **kwargs: Any) -> str:
        """Asynchronously reads the content of a text file.

        Args:
            **kwargs: Keyword arguments.
                path (str): UNC-style path (//WORKSPACE/path) to the file to read

        Returns:
            str: string with the file content or an error message.
        """
        unc_path = kwargs.get('path', '')
        encoding = kwargs.get('encoding', 'utf-8')
        max_tokens = kwargs.get('token_limit', 25000)
        tool_context = kwargs.get("tool_context")

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f'Error: {str(error)}'

        try:
            file_content = await workspace.read_internal(relative_path, encoding)
        except Exception as e:
            return f'Error reading file: {str(e)}'

        token_count = self._count_tokens(file_content, tool_context)
        if token_count > max_tokens:
            lines = file_content.splitlines()
            return (f"ERROR: File contents exceeds max_tokens limit of {max_tokens}. "
                    f"Current token count: {token_count}. This file has {len(lines)} lines. "
                    f"You will need to use `grep` or `read_lines` (to get a subset) instead."
                    f"Or you can raise the token limit in select situations.")

        return file_content

    @json_schema(
        'Writes or appends text data to a file using UNC-style path',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to write',
                'required': True
            },
            'data': {
                'type': 'string',
                'description': 'The text data to write or append to the file',
                'required': True
            },
            'mode': {
                'type': 'string',
                'description': 'The writing mode: "write" to overwrite or "append" to add to the file',
                'required': False
            }
        }
    )
    async def write(self, **kwargs: Any) -> str:
        """Asynchronously writes or appends data to a file.

        kwargs:
            path (str): UNC-style path (//WORKSPACE/path) to the file to write
            data (Union[str, bytes]): The text or binary data to write or append to the file
            mode (str): The writing mode, either 'write' to overwrite or 'append'
            data_type (str): Type of data being written, either 'text' for plain text or 'binary' for base64-encoded binary data

        Returns:
            str: JSON string with a success message or an error message.
        """
        unc_path = kwargs.get('path', '')
        data = kwargs['data']
        mode = kwargs.get('mode', 'write')

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        return await workspace.write(relative_path, mode, data)

    async def internal_write_bytes(self, path: str, data: Union[str, bytes], mode: str) -> str:
        """Asynchronously writes or appends binary data to a file.  This is an internal workspace function, not available to agents.

        Arguments:
            path (str): UNC-style path (//WORKSPACE/path) to the file to write
            data (Union[str, bytes]): The text or binary data to write or append to the file
            mode (str): The writing mode, either 'write' to overwrite or 'append'

        Returns:
            str: JSON string with a success message or an error message.
        """

        error, workspace, relative_path = self.validate_and_get_workspace_path(path)
        if error:
            return json.dumps({'error': error})

        return await workspace.write_bytes(relative_path, mode, data)

    @json_schema(
        'Copy a file or directory using UNC-style paths',
        {
            'src_path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the source',
                'required': True
            },
            'dest_path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the destination',
                'required': True
            }
        }
    )
    async def cp(self, **kwargs: Any) -> str:
        """Asynchronously copies a file or directory.

        Args:
            src_path (str): UNC-style path (//WORKSPACE/path) to the source
            dest_path (str): UNC-style path (//WORKSPACE/path) to the destination

        Returns:
            str: JSON string with the result or an error message.
        """
        src_unc_path = kwargs.get('src_path', '')
        dest_unc_path = kwargs.get('dest_path', '')

        return await self._run_cp_or_mv(
            operation=lambda workspace, source_path, destination_path: workspace.cp(source_path, destination_path),
            src_path=src_unc_path,
            dest_path=dest_unc_path,
        )

    @json_schema(
        'Check if a path is a directory using UNC-style path',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to check',
                'required': True
            }
        }
    )
    async def is_directory(self, **kwargs: Any) -> str:
        """Asynchronously checks if a path is a directory.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to check

        Returns:
            str: JSON string with the result or an error message.
        """
        unc_path = kwargs.get('path', '')

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return json.dumps({'error': error})

        try:
            result = await workspace.is_directory(relative_path)
            return json.dumps({'is_directory': result})
        except Exception as e:
            error_msg = f'Error checking if path is a directory: {e}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})

    @json_schema(
        'Move a file or directory using UNC-style paths',
        {
            'src_path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the source',
                'required': True
            },
            'dest_path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the destination',
                'required': True
            }
        }
    )
    async def mv(self, **kwargs: Any) -> str:
        """Asynchronously moves a file or directory.

        Args:
            src_path (str): UNC-style path (//WORKSPACE/path) to the source
            dest_path (str): UNC-style path (//WORKSPACE/path) to the destination

        Returns:
            str: JSON string with the result or an error message.
        """
        src_unc_path = kwargs.get('src_path', '')
        dest_unc_path = kwargs.get('dest_path', '')

        return await self._run_cp_or_mv(
            operation=lambda workspace, source_path, destination_path: workspace.mv(source_path, destination_path),
            src_path=src_unc_path,
            dest_path=dest_unc_path,
        )

    @json_schema(
        'Using a UNC-style path, update a text file with multiple string replacements. ',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to update',
                'required': True
            },
            'updates': {
                'type': 'array',
                'description': 'Array of update operations to perform',
                'items': {
                    'type': 'object',
                    'properties': {
                        'old_string': {
                            'type': 'string',
                            'description': 'The exact string to be replaced. This can be a multiline string. UTF8 encoding.'
                        },
                        'new_string': {
                            'type': 'string',
                            'description': 'The new string that will replace the old string. This can be a multiline string. UTF8 encoding'
                        }
                    },
                    'required': ['old_string', 'new_string']
                },
                'required': True
            },
            'encoding': {
                'type': 'string',
                'description': 'The encoding to use for reading and writing the file, default is "utf-8"',
                'required': False
            }
        }
    )
    async def replace_strings(self, **kwargs: Any) -> str:
        """
        Asynchronously updates a file with multiple string replacements

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to update
            updates (list): A list of update operations, each containing 'old_string' and 'new_string'

        Returns:
            str: JSON string with a success message or an error message.
        """
        updates: List = kwargs['updates']
        encoding: str = kwargs.get('encoding', 'utf-8')

        unc_path: str = kwargs.get('path', '')

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f"Error: {str(error)}"

        try:
            result = await self.replace_helper.process_replace_strings(
                read_function=workspace.read_internal, write_function=workspace.write,
                path=relative_path, updates=updates, encoding='utf-8')

            return self._yaml_dump(result)

        except Exception as e:
            self.logger.exception(f"Error in replace_strings operation for {unc_path}: {str(e)}")
            return f'Error in replace_strings operation: {str(e)}'

    @json_schema(
        'Read a subset of lines from a text file using UNC-style path',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to read',
                'required': True
            },
            'start_line': {
                'type': 'integer',
                'description': 'The 0-based index of the first line to read',
                'required': True
            },
            'end_line': {
                'type': 'integer',
                'description': 'The 0-based index of the last line to read (inclusive)',
                'required': True
            },
            'include_line_numbers': {
                'type': 'boolean',
                'description': 'Whether to include line numbers in the output',
                'required': False
            },
            'encoding': {
                'type': 'string',
                'description': 'The encoding to use for reading the file, default is "utf-8"',
                'required': False
            },
            'max_tokens': {
                'type': 'integer',
                'description': 'Maximum size in tokens for the response. Default is 25k.',
                'required': False
            }
        }
    )
    async def read_lines(self, **kwargs: Any) -> str:
        """Asynchronously reads a subset of lines from a text file.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to read
            start_line (int): The 0-based index of the first line to read
            end_line (int): The 0-based index of the last line to read (inclusive)
            include_line_numbers (bool, optional): If True, includes line numbers in the output

        Returns:
            str: JSON string containing the requested lines or an error message.
        """
        tool_context = kwargs.get("tool_context")
        unc_path = kwargs.get('path', '')
        start_line = kwargs.get('start_line')
        end_line = kwargs.get('end_line')
        encoding = kwargs.get('encoding', 'utf-8')
        include_line_numbers = kwargs.get('include_line_numbers', False)
        max_tokens = kwargs.get('max_tokens', 25000)

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f'Error: {str(error)}'

        try:
            # Validate line indices
            if not isinstance(start_line, int) or start_line < 0:
                return 'Error: Invalid start_line value'
            if not isinstance(end_line, int) or end_line < start_line:
                return 'Error: Invalid end_line value'

            try:
                file_content = await workspace.read_internal(relative_path, encoding)
            except Exception as e:
                self.logger.exception(f'Error reading file {unc_path}: {str(e)}', exc_info=True)
                return f'Error reading file: {str(e)}'

            # Split the content into lines
            lines = file_content.splitlines()

            # Check if end_line is beyond the file length
            if end_line >= len(lines):
                end_line = len(lines) - 1

            # Extract the requested subset of lines
            subset_lines = lines[start_line:end_line + 1]

            if include_line_numbers:
                # Format lines with line numbers
                formatted_lines = [f"{start_line + i}: {line}" for i, line in enumerate(subset_lines)]
                subset_content = '\n'.join(formatted_lines)
            else:
                subset_content = '\n'.join(subset_lines)

            token_count = self._count_tokens(subset_content, tool_context)
            if token_count > max_tokens:
                return (f"ERROR: The contents of those lines exceed the  max_tokens limit of {max_tokens}. "
                        f"Content token count: {token_count}. This file has {len(lines)} lines. "
                        f"You will need read fewer lines or raise the token limit. ")

            return subset_content

        except Exception as e:
            self.logger.exception(
                f'Error reading file lines for {unc_path}, start line {start_line}, end line {end_line},, error message: {str(e)}',
                exc_info=True)
            return f'Error reading file lines, for {unc_path}: {str(e)}'

    @json_schema(
        'Inspects a code file and returns details about its contents and usage.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the file to read',
                'required': True
            }
        }
    )
    async def inspect_code(self, **kwargs: Any) -> str:
        """Uses CodeExplorer to prepare code overviews.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the file to read

        Returns:
            str: A markdown overview of the code
        """
        unc_path = kwargs.get('path', '')

        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f'Error: {str(error)}'

        try:
            from ts_tool import api
            file_content = await workspace.read_internal(relative_path)
        except Exception as e:
            self.logger.exception(f'Error fetching file {unc_path}: {str(e)}', exc_info=True)
            return f'Error fetching {unc_path}: {str(e)}'

        try:
            context = api.get_code_context(file_content, format='markdown', filename=unc_path)
        except Exception as e:
            self.logger.warning(f'Error inspecting code {unc_path}: {str(e)}')
            return f'Error inspecting code {unc_path}: {str(e)}'

        return context

    @json_schema(
        description="Find files matching a glob pattern in a workspace. Equivalent to `glob.glob` in Python",
        params={
            "path": {
                "type": "string",
                "description": "UNC-style path (//WORKSPACE/path) with glob pattern to find matching files",
                "required": True
            },
            "recursive": {
                "type": "boolean",
                "description": "Whether to search recursively, matching ** patterns",
                "required": False
            },
            "include_hidden": {
                "type": "boolean",
                "description": "Whether to include hidden files in ** pattern matching",
                "required": False
            },
            "max_tokens": {
                "type": "integer",
                "description": "Maximum size in tokens for the response. Default is 2000.",
                "required": False
            }
        }
    )
    async def glob(self, **kwargs: Any) -> str:
        """Find files matching a glob pattern in a workspace.
        
        Args:
            **kwargs: Keyword arguments.
                path (str): UNC-style path (//WORKSPACE/path) with glob pattern to find matching files
                recursive (bool): Whether to search recursively (defaults to False)
                include_hidden (bool): Whether to include hidden files (defaults to False)
                
        Returns:
            str: JSON string with the list of matching files or an error message.
        """
        # Get the path with the glob pattern
        unc_path = kwargs.get('path', '')
        recursive = kwargs.get('recursive', False)
        include_hidden = kwargs.get('include_hidden', False)
        tool_context = kwargs.get("tool_context")
        max_tokens = kwargs.get("max_tokens", 4000)

        if not unc_path:
            return f"ERROR: `path` cannot be empty"

        workspace_name, workspace, relative_pattern = self._parse_unc_path(unc_path)

        if not workspace:
            return f"ERROR:'Invalid workspace: {workspace_name}'"

        try:
            # Use the workspace's glob method to find matching files
            matching_files = await workspace.glob(relative_pattern, recursive=recursive, include_hidden=include_hidden)

            # Convert the files back to UNC paths
            unc_files = [f'//{workspace_name}/{file}' for file in matching_files]
            response = f"Found {len(unc_files)} files matching '{relative_pattern}':\n" + "\n".join(unc_files)

            token_count = self._count_tokens(response, tool_context)
            if token_count > max_tokens:
                return (f"ERROR: Response exceeds max_tokens limit of {max_tokens}. Token count: {token_count}. "
                        f"You will need to adjust your pattern or raise the token limit")

            return response
        except Exception as e:
            self.logger.exception(f"Error during glob operation: {str(e)}", exc_info=True)
            return f'Error during glob operation: {str(e)}. This has been logged.'

    @json_schema(
        'Run `grep -n`  over files in workspaces using UNC-style paths',
        {
            'paths': {
                "type": "array",
                "items": {
                    "type": "string"
                },
                'description': 'UNC-style paths (//WORKSPACE/path) to grep, wildcards ARE supported',
                'required': True
            },
            'pattern': {
                'type': 'string',
                'description': 'Grep pattern to search for',
                'required': True
            },
            'ignore_case': {
                'type': 'boolean',
                'description': 'Set to true to ignore case',
                'required': False
            },
            'recursive': {
                'type': 'boolean',
                'description': 'Set to true to recursively search subdirectories',
                'required': False
            },
            'max_tokens': {
                'type': 'integer',
                'description': 'Maximum size in tokens for the response. Default is 10000.',
                'required': False
            }
        }
    )
    async def grep(self, **kwargs: Any) -> str:
        """Run grep over files in workspaces using UNC-style paths.
        
        Args:
            **kwargs: Keyword arguments.
                paths (list): UNC-style paths (//WORKSPACE/path) to grep
                pattern (str): Grep pattern to search for
                recursive (bool): Set to true to recursively search subdirectories
                ignore_case (bool): Set to true to ignore case
                
        Returns:
            str: Output of grep command with line numbers.
        """
        unc_paths = kwargs.get('paths', [])
        tool_context = kwargs.get("tool_context")
        max_tokens = kwargs.get("max_tokens", 10000)
        if not isinstance(unc_paths, list):
            if isinstance(unc_paths, str):
                unc_paths = [unc_paths]
            else:
                return f"ERROR `paths` must be a list of UNC-style paths"

        pattern = kwargs.get('pattern', '')
        ignore_case = kwargs.get('ignore_case', False)
        recursive = kwargs.get('recursive', False)
        errors = []
        queue = {}
        results = []

        if not pattern:
            return 'Error: `pattern` cannot be empty'

        if not unc_paths:
            return 'Error: `paths` cannot be empty'

        for punc_path in unc_paths:
            error, workspace, relative_path = self.validate_and_get_workspace_path(punc_path)
            if error:
                errors.append(f"Error processing path {punc_path}: {error}")
                continue
            if workspace not in queue:
                queue[workspace] = []

            queue[workspace].append(relative_path)

        # Now process each workspace's files
        for workspace, paths in queue.items():
            try:
                # Use the workspace's grep method to search for the pattern
                result = await workspace.grep(
                    pattern=pattern,
                    file_paths=paths,
                    ignore_case=ignore_case,
                    recursive=recursive
                )
                results.append(result)

            except Exception as e:
                self.logger.exception(
                    f"Error searching files in workspace {workspace.name} with pattern '{pattern}': {str(e)}")
                results.append(f'Error searching files: {str(e)}')

        err_str = ""
        if errors:
            err_str = f"Errors:\n{"\n".join(errors)}\n\n"

        response = f"{err_str}Results:\n" + "\n".join(results)
        token_count = self._count_tokens(response, tool_context)
        if token_count > max_tokens:
            return (f"ERROR: Match results exceed max_tokens limit of {max_tokens}. "
                    f"Results token count: {token_count} from {len(results)} results. "
                    f"You will need to adjust your pattern or raise the token limit.")

        return response

    @json_schema(
        description="Read a from the metadata for a workspace using a UNC style path. Nested paths are supported using slash notation ",
        params={
            "path": {
                "type": "string",
                "description": "UNC style path in the form of //[workspace]/meta/toplevel/subkey1/subkey2",
                "required": True
            },
            "max_tokens": {
                "type": "integer",
                "description": "Maximum size in tokens for the response.  Default is 20k.",
                "required": False
            }
        }
    )
    async def read_meta(self, **kwargs: Any) -> str:
        """
        Asynchronously reads a specific value from the workspace's metadata file.

        Args:
            **kwargs: Keyword arguments.
                path (str): The UNC path to the key to read, supports slash notation for nested keys (e.g., 'parent/child')
        Returns:
            str: The value for the specified key as a YAML formatted string or an error message.
        """
        path = kwargs.get("path")
        tool_context = kwargs.get("tool_context")
        max_tokens = kwargs.get("max_tokens", 20000)
        error, workspace, key = self._parse_unc_path(path)
        if not key:
            key = "meta/"

        if error is not None:
            return f"error {str(error)}"

        try:
            value = await workspace.safe_metadata(key)
            if value is None:
                self.logger.warning(f"Key '{key}' not found in metadata for workspace '{workspace.name}'")

            if isinstance(value, dict) or isinstance(value, list):
                response = self._yaml_dump(value)
                token_count = self._count_tokens(response, tool_context)
                if token_count > max_tokens:
                    return (f"ERROR: Key content exceeds max_tokens limit of {max_tokens}. "
                            f"Content token count: {token_count}. "
                            f"You can use `get_meta_keys` to list keys in this section in order to be more precise.")

                return response

            return str(value)
        except Exception as e:
            self.logger.exception(f"Failed to read metadata {key} from workspace {workspace.name}: {str(e)}")
            return f"Failed to read metadata {key} error: {str(e)}"

    @json_schema(
        description="List the keys in a section of the metadata for a workspace using a UNC style path. Nested paths are supported using slash notation ",
        params={
            "path": {
                "type": "string",
                "description": "UNC style path in the form of //[workspace]/meta/toplevel/subkey1/subkey2",
                "required": True
            },
            "max_tokens": {
                "type": "integer",
                "description": "Maximum size in tokens for the response.  Default is 20k.",
                "required": False
            }
        }
    )
    async def get_meta_keys(self, **kwargs: Any) -> str:
        """
        Asynchronously reads a specific value from the workspace's metadata file.

        Args:
            **kwargs: Keyword arguments.
                path (str): The UNC path to the key to read, supports slash notation for nested keys (e.g., 'parent/child')
        Returns:
            str: The value for the specified key as a YAML formatted string or an error message.
        """
        path = kwargs.get("path")
        tool_context = kwargs.get("tool_context")
        max_tokens = kwargs.get("max_tokens", 20000)
        error, workspace, key = self._parse_unc_path(path)

        if error is not None:
            return f"Error: {str(error)}"

        try:
            value = await workspace.safe_metadata(key)
            if value is None:
                self.logger.warning(f"Key '{key}' not found in metadata for workspace '{workspace.name}'")
            elif isinstance(value, dict):
                response = self._yaml_dump(list(value.keys()))
                token_count = self._count_tokens(response, tool_context)
                if token_count > max_tokens:
                    return f"ERROR: Response exceeds max_tokens limit of {max_tokens}. Current token count: {token_count}."

                return response

            return f"'{key}' is not a dictionary it is a {type(value).__name__}."
        except Exception as e:
            self.logger.exception(f"Failed to read metadata {key} from workspace {workspace.name}: {str(e)}")
            return f"Failed to read metadata {key} error: {str(e)}"

    @json_schema(
        description="Write to a key in the metadata for a workspace using a UNC style path. Nested paths are supported using slash notation ",
        params={
            "path": {
                "type": "string",
                "description": "Name of the workspace to write metadata to",
                "required": True
            },
            "data": {
                "oneOf": [
                    {"type": "object"},
                    {
                        "type": "array",
                        "items": {
                            "oneOf": [
                                {"type": "object"},
                                {"type": "string"},
                                {"type": "number"},
                                {"type": "boolean"},
                                {"type": "null"}
                            ]
                        }
                    },
                    {"type": "string"},
                    {"type": "number"},
                    {"type": "boolean"},
                    {"type": "null"}
                ],
                "description": "The metadata to write.",
                "required": True
            }
        }
    )
    async def write_meta(self, **kwargs: Any) -> str:
        data = kwargs.get("data")
        path = kwargs.get("path")
        error, workspace, key = self._parse_unc_path(path)

        if error is not None:
            return error

        if workspace.read_only:
            return f"Workspace '{workspace.name}' is read-only"

        try:
            await workspace.safe_metadata_write(key, data)
            return f"Saved metadata to '{key}' in {workspace.name} workspace."
        except Exception as e:
            return f"Failed to write metadata to '{key}' in {workspace.name} workspace: {str(e)}"

    @json_schema(
        description="Send a render media event to the UI to display file content from the workspace. "
                    "Supports images, text, code, markdown, and HTML files. Use this when a user asks you to show them a file in the workspace.",
        params={
            "path": {
                "type": "string",
                "description": "UNC-style workspace path (//WORKSPACE/path/to/file.ext)",
                "required": True
            },
            "mime_type": {
                "type": "string",
                "description": "Optional MIME type override (e.g., 'image/png', 'text/markdown'). "
                               "If not provided, will be detected from file extension.",
                "required": False
            },
            "start_line": {
                "type": "integer",
                "description": "Optional 0-based starting line for text files (inclusive)",
                "required": False
            },
            "end_line": {
                "type": "integer",
                "description": "Optional 0-based ending line for text files (inclusive)",
                "required": False
            }
        }
    )
    async def render_media(self, **kwargs: Any) -> str:
        """Render file content from workspace to the UI.
        
        Args:
            path (str): UNC-style workspace path
            mime_type (str, optional): MIME type override
            start_line (int, optional): Starting line for partial rendering
            end_line (int, optional): Ending line for partial rendering
            
        Returns:
            str: Success message or error description
        """
        unc_path = kwargs.get('path', '')
        mime_type_override = kwargs.get('mime_type')
        start_line = kwargs.get('start_line')
        end_line = kwargs.get('end_line')
        tool_context = kwargs.get('tool_context')
        
        # Validate path
        error, workspace, relative_path = self.validate_and_get_workspace_path(unc_path)
        if error:
            return f"ERROR: {error}"
        
        # Get file extension for mime type detection
        file_path = Path(relative_path)
        file_extension = file_path.suffix.lower()
        file_name = file_path.name
        
        # Determine mime type
        if mime_type_override:
            mime_type = mime_type_override
        else:
            mime_type = self._detect_mime_type(file_extension)
            if not mime_type:
                return (f"ERROR: Could not determine MIME type for file extension '{file_extension}'. "
                        f"Please specify a mime_type parameter.")
        
        try:
            # Determine if this is a binary or text file
            is_binary = self._is_binary_mime_type(mime_type)
            
            if is_binary:
                # Handle binary files (mainly images)
                if start_line is not None or end_line is not None:
                    return "ERROR: start_line and end_line are not supported for binary files"
                
                content_bytes = await workspace.read_bytes_internal(relative_path)
                
                await self.send_render_media_event(
                    content=content_bytes,
                    content_type=mime_type,
                    tool_context=tool_context,
                    file_name=unc_path,
                    sent_by="render_media"
                )
                
                return f"Successfully rendered {mime_type} file: {unc_path}"
            
            else:
                # Handle text files
                file_content = await workspace.read_internal(relative_path, encoding='utf-8')
                
                # Handle line ranges if specified
                if start_line is not None or end_line is not None:
                    lines = file_content.splitlines()
                    start = start_line if start_line is not None else 0
                    end = end_line + 1 if end_line is not None else len(lines)
                    
                    # Validate line indices
                    if start < 0 or start >= len(lines):
                        return f"ERROR: start_line {start} is out of range (file has {len(lines)} lines)"

                    if end < start:
                        return f"ERROR: end_line {end_line} must be greater than or equal to start_line {start_line}"

                    
                    file_content = '\n'.join(lines[start:end])
                
                # Format content based on mime type
                formatted_content = self._format_text_content(file_content, mime_type, file_extension, unc_path)
                
                # Determine final content type
                final_mime_type = "text/markdown" if mime_type != "text/html" else "text/html"
                
                await self.send_render_media_event(
                    content=formatted_content,
                    content_type=final_mime_type,
                    tool_context=tool_context,
                    file_name=unc_path,
                    sent_by="render_media"
                )
                
                line_info = ""
                if start_line is not None or end_line is not None:
                    line_info = f" (lines {start_line or 0}-{end_line or 'end'})"
                
                return f"Successfully rendered {mime_type} file: {unc_path}{line_info}"
                
        except Exception as e:
            self.logger.exception(f"Error rendering media for {unc_path}: {str(e)}")
            return f"ERROR: Failed to render file {unc_path}: {str(e)}"
    
    def _detect_mime_type(self, file_extension: str) -> Optional[str]:
        """Detect MIME type from file extension.
        
        Args:
            file_extension: File extension including the dot (e.g., '.py', '.png')
            
        Returns:
            MIME type string or None if not detected
        """
        # Common mappings for better detection
        extension_map = {
            # Images
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            
            # Text/Code
            '.py': 'text/x-python',
            '.js': 'text/javascript',
            '.ts': 'text/typescript',
            '.jsx': 'text/jsx',
            '.tsx': 'text/tsx',
            '.html': 'text/html',
            '.htm': 'text/html',
            '.css': 'text/css',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.yaml': 'text/yaml',
            '.yml': 'text/yaml',
            '.md': 'text/markdown',
            '.txt': 'text/plain',
            '.sh': 'text/x-shellscript',
            '.bash': 'text/x-shellscript',
            '.c': 'text/x-c',
            '.cpp': 'text/x-c++',
            '.h': 'text/x-c',
            '.java': 'text/x-java',
            '.cs': 'text/x-csharp',
            '.go': 'text/x-go',
            '.rs': 'text/x-rust',
            '.php': 'text/x-php',
            '.rb': 'text/x-ruby',
            '.sql': 'text/x-sql',
        }
        
        # Try our custom map first
        if file_extension in extension_map:
            return extension_map[file_extension]
        
        # Fall back to mimetypes library
        mime_type, _ = mimetypes.guess_type(f"file{file_extension}")
        return mime_type
    
    def _is_binary_mime_type(self, mime_type: str) -> bool:
        """Check if a MIME type represents binary content.
        
        Args:
            mime_type: MIME type string
            
        Returns:
            True if binary, False if text
        """
        binary_prefixes = ['image/', 'video/', 'audio/', 'application/octet-stream']
        return any(mime_type.startswith(prefix) for prefix in binary_prefixes)
    
    def _format_text_content(self, content: str, mime_type: str, file_extension: str, unc_path: str) -> str:
        """Format text content for display.
        
        Args:
            content: The file content
            mime_type: The MIME type of the file
            file_extension: The file extension
            unc_path: The UNC path of the file (for reference)
        Returns:
            Formatted content string
        """
        # Markdown files pass through as-is
        if mime_type == 'text/markdown':
            return content
        
        # HTML files pass through as-is
        if mime_type == 'text/html':
            return content
        
        # Get language identifier for code blocks
        language = self._get_language_identifier(file_extension, mime_type)
        
        # Wrap in code block with language specifier
        if language:
            return f"**{unc_path}:**\n```{language}\n{content}\n```"
        else:
            # Plain text in code block
            return f"**{unc_path}:**```\n{content}\n```"
    
    def _get_language_identifier(self, file_extension: str, mime_type: str) -> str:
        """Get the language identifier for markdown code blocks.
        
        Args:
            file_extension: File extension including dot
            mime_type: MIME type of the file
            
        Returns:
            Language identifier string (e.g., 'python', 'javascript')
        """
        # Map extensions to markdown language identifiers
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.bash': 'bash',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.java': 'java',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.sql': 'sql',
        }
        
        return language_map.get(file_extension, '')

    # @json_schema(
    #     'Execute allowlisted, non-interactive commands (git, npm, pytest, etc.) in workspace. '
    #     'No shell features (pipes, redirection, globbing). Returns stdout/stderr/exit_code.'
    #     'Prefer platform agnostic tools over OS commands for portability: e.g., git ls-files "*.md" instead of platform-specific find/where.',
    #     {
    #         'path': {
    #             "type": "string",
    #             'description': 'UNC workspace path (//workspace/subpath) as working directory. Must start with //',
    #             'required': True
    #         },
    #         'command': {
    #             'type': 'string',
    #             'description': 'Command and arguments (no shell). Examples: "git status", "npm -v", "dotnet build --no-restore"',
    #             'required': True
    #         },
    #         "timeout": {
    #             "type": "integer",
    #             "description": "Requested timeout (seconds). May be lowered by policy/validator.",
    #             "required": False,
    #         },
    #         'max_tokens': {
    #             'type': 'integer',
    #             'description': 'Max output tokens. Default 1000. Large outputs truncated.',
    #             'required': False,
    #             'default': 1000
    #         }
    #     }
    # )
    # We're moving to dynamically declaring allowed commands as separate tools so we can enable/disable commands at the agent level
    # Keeping this here for posterity in case we decide to bring it back as a generic command runner
    async def run_command(self, **kwargs: Any) -> str:
        """Run an os level command over files in workspaces using an UNC-style path.

        Args:
            **kwargs: Keyword arguments.
                path (list): UNC-style paths (//WORKSPACE/path) to grep
                command (str): Grep pattern to search for
                max_tokens (integer): max tokens to return to the agent
                suppress_success_output: Optional[bool] = None # if true, shorten successful response to optimize tokens
        Returns:
            str: output of the command.
        """
        unc_path = kwargs.get('path')
        tool_context = kwargs.get("tool_context", {})
        max_tokens = kwargs.get("max_tokens", 1000)
        command = kwargs.get('command', '').strip()
        timeout: Optional[int] = kwargs.get('timeout', None)
        suppress_success_output: Optional[bool] = kwargs.get('suppress_success_output', None)

        # validate required fields exist
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['command', 'path'])

        if not success:
            return message

        # Ensure workspace path is valid and get relative path
        # for Joe: this converts the UNC path to a workspace object and the relative path inside that workspace
        # so \\ALPHA\project\readme.md becomes (Workspace('ALPHA'), 'project/readme.md')
        err, workspace, rel_path = self.validate_and_get_workspace_path(unc_path)

        if err:
            return f"ERROR: {err}"

        if not workspace or not hasattr(workspace, 'run_command'):
            return f"ERROR: Workspace: {workspace.name if workspace else 'None'} does not support OS level run commands"

        try:
            # Get OS absolute path
            abs_path = workspace.full_path(rel_path or "", mkdirs=False)  # validated + normalized
            if not abs_path:
                return f"Invalid path: {rel_path!r}"
        except Exception as e:
            return f"Failed to resolve path: {e}"

        # pass command to underlying workspace run_command method, e.g. LocalWorkspace
        result: CommandExecutionResult = await workspace.run_command(command=command,
                                                                     working_directory=abs_path,
                                                                     timeout=timeout,
                                                                     suppress_success_output=suppress_success_output)

        # Create UI message
        html_content = await MediaEventHelper.stdout_html(result.to_dict())
        await self._raise_render_media(
            sent_by_class=workspace.__class__.__name__,
            sent_by_function='execute_command',
            content_type="text/html",
            content=html_content,
            tool_context=tool_context
        )

        # Trim response to max tokens back to LLM in a smart way if agent_runtime and count_token function exists
        counter = tool_context.get("agent_runtime").count_tokens if tool_context else None
        return result.to_yaml_capped(max_tokens, counter) if counter else result.to_yaml()


Toolset.register(WorkspaceTools)
