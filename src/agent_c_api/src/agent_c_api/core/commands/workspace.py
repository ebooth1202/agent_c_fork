import argparse
import codecs

from typing import List, TYPE_CHECKING

from agent_c_api.core.commands.base_command import Command
from agent_c_api.core.commands.parsers import ArgparseParser
from agent_c_tools.tools.workspace.base import WorkspaceDataEntry

if TYPE_CHECKING:
    from agent_c_api.core.realtime_bridge import RealtimeBridge

def unescaped_str(arg_str):
    return codecs.decode(str(arg_str), 'unicode_escape')

class AddLocalWorkspaceCommand(Command):

    def __init__(self):
        parser = argparse.ArgumentParser(prog='!add_local_workspace', description='Add a local directory as a workspace', epilog='Example: !alw path/to/folder --name MyWorkspace')
        parser.add_argument('path', type=unescaped_str,  help='Path to the local directory to add as a workspace')
        parser.add_argument('--name', "-n",  type=str, required=False, help='Optional name for the workspace')
        parser.add_argument('--description', "-d", type=str, required=False, help='Optional description for the workspace')
        parser.add_argument('--readonly', "-r", required=False, action='store_true', help='Set to true for read-only access to the workspace')
        self.ap = parser
        super().__init__(ArgparseParser(parser))

    @property
    def command_strings(self) -> List[str]:
        return ['!alw', '!add_local_workspace']

    @property
    def help_text(self) -> str:
        return self.ap.format_help()

    async def execute(self, context: 'RealtimeBridge', **kwargs):
        path = kwargs.get('path')
        if path is None:
            await context.send_system_message("You must specify a path to the local workspace", severity="error")

        await context.add_user_workspace(WorkspaceDataEntry(path_or_bucket=path, name=kwargs.get('name'), type='local'))
