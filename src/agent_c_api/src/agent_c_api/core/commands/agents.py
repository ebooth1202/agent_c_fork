from typing import List, TYPE_CHECKING

from agent_c_api.core.commands.base_command import Command

if TYPE_CHECKING:
    from agent_c_api.core.realtime_bridge import RealtimeBridge

class ReloadAgentsCommand(Command):
    @property
    def command_strings(self) -> List[str]:
        return ['!load_agents', '!la']

    @property
    def help_text(self) -> str:
        return "Reload all agent configurations from disk  - Usage: !la\n\n- Your current agent will be updated automatically."

    async def execute(self, context: 'RealtimeBridge', **kwargs):
        await context.reload_agents()