import yaml
from typing import Any, Dict, TYPE_CHECKING
from agent_c.prompting import PromptSection, property_bag_item

if TYPE_CHECKING:
    from agent_c.models.chat_history import ChatSession

class MemorySection(PromptSection):
    def __init__(self, **data: Any):
        TEMPLATE = ("This section displays memory information you have stored for the current session and user. \n"
                    "Use `memory_store` to update this information, either by user request or when you have a need to store something outside of the chat log.\n"
                    "The data has have been converted to YAML below for readability\n\n"
                    "### Memory data (Session):\n"
                    "```yaml\n${session_memory}\n```\n"
                    "### Memory data (User):\n"
                    "```yaml\n${user_memory}\n```\n")
        super().__init__(template=TEMPLATE, required=True, name="Memory", render_section_header=True, **data)

    @property_bag_item
    async def session_memory(self, context: Dict[str, Any]) -> str:
        chat_session: 'ChatSession' = context.get("chat_session")
        return yaml.dump(chat_session.get_agent_memory_store(), allow_unicode=True, sort_keys=True)

    @property_bag_item
    async def user_memory(self, context: Dict[str, Any]) -> str:
        chat_user = context.get("chat_user")
        mem = chat_user.get_agent_memory_store()
        return yaml.dump(mem, allow_unicode=True, sort_keys=True)