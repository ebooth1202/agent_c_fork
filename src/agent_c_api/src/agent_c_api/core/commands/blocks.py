from typing import List, TYPE_CHECKING

from agent_c_api.core.commands.base_command import Command

if TYPE_CHECKING:
    from agent_c_api.core.realtime_bridge import RealtimeBridge

class ReloadBlocksCommand(Command):
    @property
    def command_strings(self) -> List[str]:
        return ['!load_bocks', '!lb']

    @property
    def help_text(self) -> str:
        return "Reload all instruction blocks from disk  - Usage: !lb\n\n"

    async def execute(self, context: 'RealtimeBridge', **kwargs):
        await context.reload_blocks()