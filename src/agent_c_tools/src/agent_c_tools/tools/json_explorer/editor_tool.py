"""JSON Editor Tools - Toolset for editing and manipulating JSON files."""

import json
from typing import Any, Optional
import yaml

from agent_c.toolsets.tool_set import Toolset
from agent_c.toolsets.json_schema import json_schema

from .json_editor import JSONEditor
from agent_c_tools.tools.workspace.tool import WorkspaceTools
from agent_c_tools.helpers.validate_kwargs import validate_required_fields


class JsonEditorTools(Toolset):
    """
    Enables your agent to modify, edit, and manipulate JSON files with full CRUD operations.
    Your agent can add/remove/update values, manage object keys, manipulate arrays,
    and perform complex operations. All operations support preview mode and
    automatic backup creation for safe editing.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(name='json_editor', **kwargs)
        self.workspace_tool: Optional[WorkspaceTools] = None

    async def post_init(self):
        self.workspace_tool = self.tool_chest.available_tools['WorkspaceTools']

    @json_schema(
        'Create a backup of a JSON file before making modifications.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file to backup',
                'required': True
            }
        }
    )
    async def backup(self, **kwargs: Any) -> str:
        """Create a timestamped backup of a JSON file."""
        unc_path = kwargs.get('path')
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.create_backup(relative_path)

    @json_schema(
        'Validate that a JSON file is well-formed and parseable.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file to validate',
                'required': True
            }
        }
    )
    async def validate(self, **kwargs: Any) -> str:
        """Validate a JSON file is well-formed and get structure information."""
        unc_path = kwargs.get('path')
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.validate_json(relative_path)

    @json_schema(
        'Set or update a value at a specific JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the location to set the value (e.g., "$.config.timeout" or "$.users[0].name")',
                'required': True
            },
            'value': {
                'description': 'The value to set (can be string, number, boolean, null, object, or array)',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def set_value(self, **kwargs: Any) -> str:
        """Set or update a value at a specific JSONPath."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        value = kwargs.get('value')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'value'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.set_value(relative_path, jsonpath, value, preview=preview)

    @json_schema(
        'Add a new key-value pair to an object at the specified JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the object where the key will be added',
                'required': True
            },
            'key': {
                'type': 'string',
                'description': 'The key name to add',
                'required': True
            },
            'value': {
                'description': 'The value to set for the key (can be string, number, boolean, null, object, or array)',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def add_to_object(self, **kwargs: Any) -> str:
        """Add a new key-value pair to an object."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        key = kwargs.get('key')
        value = kwargs.get('value')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'key', 'value'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.add_to_object(relative_path, jsonpath, key, value, preview=preview)

    @json_schema(
        'Remove a key from an object at the specified JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the object containing the key to remove',
                'required': True
            },
            'key': {
                'type': 'string',
                'description': 'The key name to remove',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would be removed without actually removing (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def remove_key(self, **kwargs: Any) -> str:
        """Remove a key from an object."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        key = kwargs.get('key')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'key'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.remove_key(relative_path, jsonpath, key, preview=preview)

    @json_schema(
        'Append a value to an array at the specified JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the array where the value will be appended',
                'required': True
            },
            'value': {
                'description': 'The value to append (can be string, number, boolean, null, object, or array)',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def append_to_array(self, **kwargs: Any) -> str:
        """Append a value to an array."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        value = kwargs.get('value')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'value'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.append_to_array(relative_path, jsonpath, value, preview=preview)

    @json_schema(
        'Insert a value at a specific index in an array at the specified JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the array where the value will be inserted',
                'required': True
            },
            'index': {
                'type': 'integer',
                'description': 'The index where the value will be inserted (0-based, negative indices count from end)',
                'required': True
            },
            'value': {
                'description': 'The value to insert (can be string, number, boolean, null, object, or array)',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def insert_into_array(self, **kwargs: Any) -> str:
        """Insert a value at a specific index in an array."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        index = kwargs.get('index')
        value = kwargs.get('value')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'index', 'value'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.insert_into_array(relative_path, jsonpath, index, value, preview=preview)

    @json_schema(
        'Remove an item at a specific index from an array at the specified JSONPath.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the JSON file',
                'required': True
            },
            'jsonpath': {
                'type': 'string',
                'description': 'JSONPath to the array from which the item will be removed',
                'required': True
            },
            'index': {
                'type': 'integer',
                'description': 'The index of the item to remove (0-based, negative indices count from end)',
                'required': True
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would be removed without actually removing (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def remove_from_array(self, **kwargs: Any) -> str:
        """Remove an item at a specific index from an array."""
        unc_path = kwargs.get('path')
        jsonpath = kwargs.get('jsonpath')
        index = kwargs.get('index')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'jsonpath', 'index'])
        if not success:
            return f"ERROR: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False, allow_unicode=True)

        editor = JSONEditor(workspace)
        return await editor.remove_from_array(relative_path, jsonpath, index, preview=preview)


# Register the toolset
Toolset.register(JsonEditorTools, required_tools=['WorkspaceTools'])
