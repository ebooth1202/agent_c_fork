from typing import Any, Dict

from agent_c.util.dict import get_nested, set_nested, delete_nested
from agent_c.toolsets import json_schema, Toolset
from .prompt import MemorySection


class MemoryTools(Toolset):
    """
    Allows your agent to remember important information about you and your conversations across sessions.
    Your agent can store preferences, context, and key details that help personalize your interactions
    and maintain continuity between different conversations and tasks.
    """

    def __init__(self, **kwargs: Any):
        """Initialize MemoryTools with a MemorySection instance.

        Args:
            **kwargs (Any): Keyword arguments including those for ZepDependentToolset.
        """
        super().__init__(**kwargs, name='memory')
        self.section = kwargs.get('section', MemorySection())

    @json_schema(
        (
            'This tool allows you to store memory information in the metadata for the current user/session. '
            'You may store strings or more complex data objects depending on your need. '
            'Keys can be supplied using path syntax tp reach nested keys'

        ),
        {
            'location': {
                'type': 'string',
                'description': 'Where to store the metadata. Must be one of `user` or `session`.',
                'required': True
            },
            'key': {
                'type': 'string',
                'description': 'The key to store the value under. You may use "/" to denote nested keys.',
                'required': True
            },
            'value': {
                "anyOf": [{"type": "object", "additionalProperties": True}, {"type": "string"}],
                'description': ('The value to store, this can be a string or a dictionary type '
                                'structure to hold more complex information.'),
                'required': True
            }
        }
    )
    async def store(self, **kwargs: Any) -> str:
        """Store or update metadata associated with the current user or session.

        Args:
            key (str): The key to store the value under.
            location (str): Where to store the metadata ('user' or 'session').
            value (str | dict): The value to store, can be a string or a more complex data object.

        Returns:
            str: A message indicating that the value has been stored.
        """
        key: str = kwargs["key"]
        location: str = kwargs.get("location", "user")
        value: Any = kwargs["value"]
        context: Dict[str, Any] = kwargs.get("tool_context")

        if location != "user":
            source = context['prompt_metadata']['chat_session']
        else:
            source = context['prompt_metadata']['chat_user']

        mem_store = source.get_agent_memory_store()
        set_nested(mem_store, key, value, "/")
        source.set_agent_memory_store(mem_store)

        return f"Value for {key} stored in {location} memory"

    @json_schema(
        'This tool allows you to remove a key from the user/session. Keys can be supplied using path syntax tp reach nested keys',
        {
            'location': {
                'type': 'string',
                'description': 'Which set of metadata to update. Must be one of `user` or `session`.',
                'required': True
            },
            'key': {
                'type': 'string',
                'description': 'The key to remove. You may use "/" to denote nested keys.',
                'required': True
            }
        }
    )
    async def clear(self, **kwargs: Any) -> str:
        """Remove metadata associated with a specified key from the current user or session.

        Args:
            key (str): The key for which to clear the value.
            location (str): Which set of metadata to update ('user' or 'session').
        Returns:
            str: A message indicating that the key has been cleared.
        """
        key: str = kwargs["key"]
        location: str = kwargs.get("location", "user")
        context: Dict[str, Any] = kwargs.get("tool_context")

        if location != "user":
            source = context['prompt_metadata']['chat_session']
        else:
            source = context['prompt_metadata']['chat_user']

        mem_store = source.get_agent_memory_store()
        delete_nested(mem_store, key, "/")
        source.set_agent_memory_store(mem_store)

        return f"Value for {key} cleared from {location} metadata"

# This is broken so disabling it.
Toolset.register(MemoryTools)
