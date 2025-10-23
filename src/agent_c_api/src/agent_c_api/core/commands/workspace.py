from typing import List, TYPE_CHECKING
from agent_c_api.core.commands.base_command import Command
from agent_c_tools.tools.workspace.base import WorkspaceDataEntry

if TYPE_CHECKING:
    from agent_c_api.core.realtime_bridge import RealtimeBridge

class AddLocalWorkspaceCommand(Command):
    @property
    def command_strings(self) -> List[str]:
        return ['!alw', '!add_local_workspace']

    @property
    def help_text(self) -> str:
        return "Add a local directory as a workspace - Usage: !alw --path [/path/to/folder] --name \"some name\"\n\n"

    async def execute(self, context: 'RealtimeBridge', **kwargs):
        path = kwargs.get('path')
        if path is None:
            await context.send_system_message("You must specify a path to the local workspace using --path", severity="error")

        await context.add_user_workspace(WorkspaceDataEntry(path_or_bucket=path, name=kwargs.get('name'), type='local'))
