from flask import Blueprint, request

from command_app.enums import DataStoreKinds, ActionsCommands
from command_app.extensions import gcp_db
from command_app.service import commands
from command_app.utils.actions_handler import RedoUndoActionsHandler

commands_bp = Blueprint("commands", __name__)


@commands_bp.route('/set', methods=['GET'])
def set_variable():
    """
        Set DS variable.
    """
    name = request.args.get('name')
    value = request.args.get('value')
    if not name or not value:
        return "Invalid request", 400

    commands.update_undo_state(name, value, ActionsCommands.SET.value)

    commands.set_variable_with(name=name, value=value)

    return f"{name}={value}", 200


@commands_bp.route('/get', methods=['GET'])
def get_variable():
    """
        Get Variable
    """
    name = request.args.get('name')
    if not name:
        return "Invalid request", 400

    var_value = commands.get_variable_value_with(name=name)

    return var_value or "None", 200


@commands_bp.route('/unset', methods=['GET'])
def unset_variable():
    name = request.args.get('name')
    if not name:
        return "Invalid request", 400

    root_key = commands.get_root_key()
    key = gcp_db.key(DataStoreKinds.VARIABLE.value, name, parent=root_key)
    entity = gcp_db.get(key)
    if entity:
        commands.update_undo_state(name, entity['value'], ActionsCommands.UNSET.value)
        gcp_db.delete(key)
        return f"{name}=None", 200
    return f"{name} not found", 200


@commands_bp.route('/numequalto', methods=['GET'])
def numequalto():
    value = request.args.get('value')
    if value is None:
        return "Invalid request", 400

    query = gcp_db.query(kind=DataStoreKinds.VARIABLE.value)
    query.add_filter('value', '=', value)  # one field search is O1 im most cases, google optimize it by their side.
    results = list(query.fetch())
    return str(len(results)), 200


# Undo last command
@commands_bp.route('/undo', methods=['GET'])
def undo():
    """
        Undo last Command
    """
    undo_last_command = commands.get_current_undo()

    if not undo_last_command:
        return "NO COMMANDS", 200

    undo_handler = RedoUndoActionsHandler(**undo_last_command)

    commands.update_redo_state(name=undo_handler.name,
                               action=undo_handler.action,
                               # old_value -> value in purpose, because we're doing the opposite with redo.
                               value=undo_handler.old_value)

    if undo_handler.it_was_set_command:
        undo_handler.undo_set_command()
        return f"{undo_handler.name}={undo_handler.old_value or 'None'}", 200
    elif undo_handler.it_was_unset_command:
        undo_handler.undo_unset_command()
        return f"{undo_handler.name}={undo_handler.old_value or 'None'}", 200

    return "NO COMMANDS", 200  # i should log it as an unwanted behavior.


@commands_bp.route('/redo', methods=['GET'])
def redo():
    undo_last_command = commands.get_current_redo()

    if not undo_last_command:
        return "NO COMMANDS", 200

    undo_handler = RedoUndoActionsHandler(**undo_last_command)

    commands.update_undo_state(name=undo_handler.name,
                               action=undo_handler.action,
                               # old_value -> value in purpose, because we're doing the opposite with undo.
                               value=undo_handler.old_value)

    if undo_handler.it_was_set_command:
        undo_handler.undo_set_command()
        return f"{undo_handler.name}={undo_handler.old_value or 'None'}", 200
    elif undo_handler.it_was_unset_command:
        undo_handler.undo_unset_command()
        return f"{undo_handler.name}={undo_handler.old_value or 'None'}", 200

    return "NO COMMANDS", 200  # i should log it as an unwanted behavior.


@commands_bp.route('/end', methods=['GET'])
def end():
    gcp_db.delete_multi(gcp_db.query(ancestor=commands.get_root_key()).fetch())
    return "CLEANED"


@commands_bp.route('/hello_world', methods=['GET'])
def hello_world():
    return "Hello Fast Samion :)", 200
