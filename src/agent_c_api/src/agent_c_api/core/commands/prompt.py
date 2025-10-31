from typing import List, TYPE_CHECKING

from agent_c_api.core.commands.base_command import Command

if TYPE_CHECKING:
    from agent_c_api.core.realtime_bridge import RealtimeBridge

class PreviewPromptCommand(Command):
    @property
    def command_strings(self) -> List[str]:
        return ['!preview_prompt', '!preview_system_prompt', '!pp', '!psp']

    @property
    def help_text(self) -> str:
        return "Renders the system prompt for the current agent to the chat.  - Usage: !lb\n\n"

    async def execute(self, context: 'RealtimeBridge', **kwargs):
        await context.preview_system_prompt()