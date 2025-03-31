import dataclasses

from command_app.enums import ActionsCommands
from command_app.service import commands


@dataclasses.dataclass
class RedoUndoActionsHandler:
    """
       Helper class that help undo/redo
    """
    name: str
    value: str
    action: int
    old_value: str

    @property
    def it_was_set_command(self) -> bool:
        return self.action == ActionsCommands.SET.value

    @property
    def it_was_unset_command(self) -> bool:
        return self.action == ActionsCommands.SET.value

    def undo_set_command(self):
        if self.old_value:
            commands.set_variable_with(name=self.name, value=self.old_value)
            return

        commands.delete_variable_with(name=self.name)

    def undo_unset_command(self):
        commands.set_variable_with(name=self.name)
        return f"{self.name}={self.value}"



