import json
from typing import Any, Optional, Dict
import yaml

from agent_c.toolsets.tool_set import Toolset
from agent_c.toolsets.json_schema import json_schema
from agent_c_tools.helpers.token_helper import is_content_too_large, token_count

from .xml_editor import XMLEditor
from agent_c_tools.tools.workspace.tool import WorkspaceTools
from ...helpers.validate_kwargs import validate_required_fields


class XmlEditorTools(Toolset):
    """
    Enables your agent to modify, edit, and manipulate XML files with full CRUD operations.
    Your agent can add/remove/replace elements, manage attributes, modify text content,
    handle namespaces, and manage comments. All operations support preview mode and
    automatic backup creation for safe editing.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(name='xml_editor', **kwargs)
        self.workspace_tool: Optional[WorkspaceTools] = None

    async def post_init(self):
        self.workspace_tool = self.tool_chest.available_tools['WorkspaceTools']

    @json_schema(
        'Create a backup of an XML file before making modifications.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file to backup',
                'required': True
            }
        }
    )
    async def backup(self, **kwargs: Any) -> str:
        """Create a timestamped backup of an XML file.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the XML file

        Returns:
            str: YAML string with backup information
        """
        unc_path = kwargs.get('path')
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.create_backup(relative_path)

    @json_schema(
        'Validate that an XML file is well-formed.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file to validate',
                'required': True
            }
        }
    )
    async def validate(self, **kwargs: Any) -> str:
        """Validate an XML file is well-formed and get structure information.

        Args:
            path (str): UNC-style path (//WORKSPACE/path) to the XML file

        Returns:
            str: YAML string with validation results
        """
        unc_path = kwargs.get('path')
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.validate_xml(relative_path)

    @json_schema(
        'Add a new element to an XML file at a specified location.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'parent_xpath': {
                'type': 'string',
                'description': 'XPath to the parent element where the new element will be added',
                'required': True
            },
            'element_name': {
                'type': 'string',
                'description': 'Name/tag of the new element to add',
                'required': True
            },
            'attributes': {
                'type': 'object',
                'description': 'Optional dictionary of attributes for the new element',
                'required': False
            },
            'text': {
                'type': 'string',
                'description': 'Optional text content for the new element',
                'required': False
            },
            'namespace': {
                'type': 'string',
                'description': 'Optional namespace URI for the new element',
                'required': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def add_element(self, **kwargs: Any) -> str:
        """Add a new element to an XML file.

        Args:
            path (str): UNC-style path to the XML file
            parent_xpath (str): XPath to the parent element
            element_name (str): Name/tag of the new element
            attributes (dict, optional): Attributes for the new element
            text (str, optional): Text content for the new element
            namespace (str, optional): Namespace URI for the new element
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        parent_xpath = kwargs.get('parent_xpath')
        element_name = kwargs.get('element_name')
        attributes = kwargs.get('attributes')
        text = kwargs.get('text')
        namespace = kwargs.get('namespace')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'parent_xpath', 'element_name'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.add_element(
            relative_path,
            parent_xpath,
            element_name,
            attributes=attributes,
            text=text,
            namespace=namespace,
            preview=preview
        )

    @json_schema(
        'Remove element(s) from an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to remove',
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
    async def remove_element(self, **kwargs: Any) -> str:
        """Remove element(s) from an XML file.

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to remove
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        preview = kwargs.get('preview', False)
        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.remove_element(relative_path, xpath, preview=preview)

    @json_schema(
        'Replace existing element(s) with new element(s) in an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to replace',
                'required': True
            },
            'new_element_name': {
                'type': 'string',
                'description': 'Name/tag of the replacement element',
                'required': True
            },
            'attributes': {
                'type': 'object',
                'description': 'Optional dictionary of attributes for the new element',
                'required': False
            },
            'text': {
                'type': 'string',
                'description': 'Optional text content for the new element',
                'required': False
            },
            'preserve_children': {
                'type': 'boolean',
                'description': 'If true, copy children from old element to new element (default: true)',
                'required': False,
                'default': True
            },
            'namespace': {
                'type': 'string',
                'description': 'Optional namespace URI for the new element',
                'required': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def replace_element(self, **kwargs: Any) -> str:
        """Replace existing element(s) with new element(s).

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to replace
            new_element_name (str): Name/tag of the replacement element
            attributes (dict, optional): Attributes for the new element
            text (str, optional): Text content for the new element
            preserve_children (bool, optional): Whether to preserve children (default: True)
            namespace (str, optional): Namespace URI for the new element
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        new_element_name = kwargs.get('new_element_name')
        attributes = kwargs.get('attributes')
        text = kwargs.get('text')
        preserve_children = kwargs.get('preserve_children', True)
        namespace = kwargs.get('namespace')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath', 'new_element_name'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.replace_element(
            relative_path,
            xpath,
            new_element_name,
            attributes=attributes,
            text=text,
            preserve_children=preserve_children,
            namespace=namespace,
            preview=preview
        )

    @json_schema(
        'Insert a new element before or after a reference element.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'reference_xpath': {
                'type': 'string',
                'description': 'XPath to the reference element',
                'required': True
            },
            'element_name': {
                'type': 'string',
                'description': 'Name/tag of the new element to insert',
                'required': True
            },
            'position': {
                'type': 'string',
                'description': 'Where to insert: "before" or "after" (default: "after")',
                'enum': ['before', 'after'],
                'required': False,
                'default': 'after'
            },
            'attributes': {
                'type': 'object',
                'description': 'Optional dictionary of attributes for the new element',
                'required': False
            },
            'text': {
                'type': 'string',
                'description': 'Optional text content for the new element',
                'required': False
            },
            'namespace': {
                'type': 'string',
                'description': 'Optional namespace URI for the new element',
                'required': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def insert_at_position(self, **kwargs: Any) -> str:
        """Insert a new element before or after a reference element.

        Args:
            path (str): UNC-style path to the XML file
            reference_xpath (str): XPath to the reference element
            element_name (str): Name/tag of the new element
            position (str, optional): "before" or "after" (default: "after")
            attributes (dict, optional): Attributes for the new element
            text (str, optional): Text content for the new element
            namespace (str, optional): Namespace URI for the new element
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        reference_xpath = kwargs.get('reference_xpath')
        element_name = kwargs.get('element_name')
        position = kwargs.get('position', 'after')
        attributes = kwargs.get('attributes')
        text = kwargs.get('text')
        namespace = kwargs.get('namespace')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'reference_xpath', 'element_name'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.insert_at_position(
            relative_path,
            reference_xpath,
            element_name,
            position=position,
            attributes=attributes,
            text=text,
            namespace=namespace,
            preview=preview
        )

    @json_schema(
        'Set or update an attribute on element(s) in an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to modify',
                'required': True
            },
            'attribute_name': {
                'type': 'string',
                'description': 'Name of the attribute to set',
                'required': True
            },
            'attribute_value': {
                'type': 'string',
                'description': 'Value to set for the attribute',
                'required': True
            },
            'namespace': {
                'type': 'string',
                'description': 'Optional namespace URI for the attribute',
                'required': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def set_attribute(self, **kwargs: Any) -> str:
        """Set or update an attribute on element(s).

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to modify
            attribute_name (str): Name of the attribute
            attribute_value (str): Value for the attribute
            namespace (str, optional): Namespace URI for the attribute
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        attribute_name = kwargs.get('attribute_name')
        attribute_value = kwargs.get('attribute_value')
        namespace = kwargs.get('namespace')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath', 'attribute_name', 'attribute_value'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.set_attribute(
            relative_path,
            xpath,
            attribute_name,
            attribute_value,
            namespace=namespace,
            preview=preview
        )

    @json_schema(
        'Remove an attribute from element(s) in an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to modify',
                'required': True
            },
            'attribute_name': {
                'type': 'string',
                'description': 'Name of the attribute to remove',
                'required': True
            },
            'namespace': {
                'type': 'string',
                'description': 'Optional namespace URI for the attribute',
                'required': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would be removed without actually removing (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def remove_attribute(self, **kwargs: Any) -> str:
        """Remove an attribute from element(s).

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to modify
            attribute_name (str): Name of the attribute to remove
            namespace (str, optional): Namespace URI for the attribute
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        attribute_name = kwargs.get('attribute_name')
        namespace = kwargs.get('namespace')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath', 'attribute_name'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.remove_attribute(
            relative_path,
            xpath,
            attribute_name,
            namespace=namespace,
            preview=preview
        )

    @json_schema(
        'Set or append text content to element(s) in an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to modify',
                'required': True
            },
            'text_content': {
                'type': 'string',
                'description': 'Text content to set or append',
                'required': True
            },
            'append': {
                'type': 'boolean',
                'description': 'If true, append to existing text; if false, replace text (default: false)',
                'required': False,
                'default': False
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def set_text(self, **kwargs: Any) -> str:
        """Set or append text content to element(s).

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to modify
            text_content (str): Text content to set or append
            append (bool, optional): Whether to append to existing text (default: False)
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        text_content = kwargs.get('text_content')
        append = kwargs.get('append', False)
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath', 'text_content'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.set_text(
            relative_path,
            xpath,
            text_content,
            append=append,
            preview=preview
        )

    @json_schema(
        'Add a namespace declaration to the root element of an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'prefix': {
                'type': 'string',
                'description': 'Namespace prefix (use empty string for default namespace)',
                'required': True
            },
            'uri': {
                'type': 'string',
                'description': 'Namespace URI',
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
    async def add_namespace(self, **kwargs: Any) -> str:
        """Add a namespace declaration to the root element.

        Args:
            path (str): UNC-style path to the XML file
            prefix (str): Namespace prefix (empty string for default namespace)
            uri (str): Namespace URI
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        prefix = kwargs.get('prefix')
        uri = kwargs.get('uri')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'prefix', 'uri'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.add_namespace(relative_path, prefix, uri, preview=preview)

    @json_schema(
        'Set the namespace of existing element(s) in an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the element(s) to modify',
                'required': True
            },
            'namespace_uri': {
                'type': 'string',
                'description': 'Namespace URI to apply to the element',
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
    async def set_namespace(self, **kwargs: Any) -> str:
        """Set the namespace of existing element(s).

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the element(s) to modify
            namespace_uri (str): Namespace URI to apply
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        namespace_uri = kwargs.get('namespace_uri')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath', 'namespace_uri'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.set_namespace(
            relative_path,
            xpath,
            namespace_uri,
            preview=preview
        )

    @json_schema(
        'Add a comment to an XML file at a specified location.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'parent_xpath': {
                'type': 'string',
                'description': 'XPath to the parent element where comment will be added',
                'required': True
            },
            'comment_text': {
                'type': 'string',
                'description': 'Text content of the comment',
                'required': True
            },
            'position': {
                'type': 'string',
                'description': 'Where to add: "append", "prepend", or "before" (default: "append")',
                'enum': ['append', 'prepend', 'before'],
                'required': False,
                'default': 'append'
            },
            'preview': {
                'type': 'boolean',
                'description': 'If true, show what would change without applying (default: false)',
                'required': False,
                'default': False
            }
        }
    )
    async def add_comment(self, **kwargs: Any) -> str:
        """Add a comment to an XML file.

        Args:
            path (str): UNC-style path to the XML file
            parent_xpath (str): XPath to the parent element
            comment_text (str): Text content of the comment
            position (str, optional): "append", "prepend", or "before" (default: "append")
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        parent_xpath = kwargs.get('parent_xpath')
        comment_text = kwargs.get('comment_text')
        position = kwargs.get('position', 'append')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'parent_xpath', 'comment_text'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.add_comment(
            relative_path,
            parent_xpath,
            comment_text,
            position=position,
            preview=preview
        )

    @json_schema(
        'Remove comment(s) from an XML file.',
        {
            'path': {
                'type': 'string',
                'description': 'UNC-style path (//WORKSPACE/path) to the XML file',
                'required': True
            },
            'xpath': {
                'type': 'string',
                'description': 'XPath to the comment(s) to remove (use comment() function, e.g., "//comment()[contains(., \'text\')]")',
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
    async def remove_comment(self, **kwargs: Any) -> str:
        """Remove comment(s) from an XML file.

        Args:
            path (str): UNC-style path to the XML file
            xpath (str): XPath to the comment(s) to remove
            preview (bool, optional): Preview mode without applying changes

        Returns:
            str: YAML string with operation results
        """
        unc_path = kwargs.get('path')
        xpath = kwargs.get('xpath')
        preview = kwargs.get('preview', False)

        success, message = validate_required_fields(kwargs=kwargs, required_fields=['path', 'xpath'])
        if not success:
            return f"Error: {message}"

        error, workspace, relative_path = self.workspace_tool.validate_and_get_workspace_path(unc_path)
        if error:
            return yaml.dump({'error': error}, default_flow_style=False, sort_keys=False)

        editor = XMLEditor(workspace)
        return await editor.remove_comment(relative_path, xpath, preview=preview)


# Register the toolset
Toolset.register(XmlEditorTools, required_tools=['WorkspaceTools'])