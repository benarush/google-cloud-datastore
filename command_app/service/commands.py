from typing import Optional
from functools import lru_cache

from command_app.enums import DataStoreKinds, ActionsCommands
from command_app.extensions import gcp_db
from google.cloud import datastore


@lru_cache(maxsize=1)
def get_root_key() -> datastore.Key:
    """
        Made it function even so that it will be better to be simple variable,
        if we want in future to switch between roots
    """
    return gcp_db.key(DataStoreKinds.DB_ROOT.value, "global_root")


def delete_variable_with(*, name: str):
    """
        Delete Variable
    :param name: the name of the variable, str
    :return:
    """
    root_key = get_root_key()
    key = gcp_db.key(DataStoreKinds.VARIABLE.value, name, parent=root_key)
    gcp_db.delete(key)


def get_current_undo() -> Optional[dict]:
    """
        get the latest Undo command that stored in undo_stack list.
    :return: dict | None
    """
    key = gcp_db.key(DataStoreKinds.UNDO.value, "undo_stack", parent=get_root_key())
    undo_entity = gcp_db.get(key)
    if undo_entity is not None and len(undo_entity['value']) > 0:
        last_action = undo_entity['value'].pop()
        gcp_db.put(undo_entity)  # need to save after the pop, to ensure it will not pop same value again
        return last_action
    return None


def get_current_redo() -> Optional[dict]:
    """
        get the latest redo command that stored in redo_stack list.
    :return: dict | None
    """
    key = gcp_db.key(DataStoreKinds.REDO.value, "redo_stack", parent=get_root_key())
    redo_entity = gcp_db.get(key)
    if redo_entity is not None and len(redo_entity['value']) > 0:
        last_action = redo_entity['value'].pop()
        gcp_db.put(redo_entity)  # need to save after the pop, to ensure it will not pop same value again
        return last_action
    return None


def set_variable_with(*, name: str, value: str):
    """
        Set Variale value
    :param name: the name of the variable
    :param value: the value to assign
    :return: None
    """
    var_key = gcp_db.key(DataStoreKinds.VARIABLE.value, name, parent=get_root_key())

    var_entity = gcp_db.get(var_key)

    if var_entity is None:
        var_entity = datastore.Entity(key=var_key)

    var_entity['value'] = value
    gcp_db.put(var_entity)


def get_variable_value_with(*, name: str) -> Optional[str]:
    root_key = get_root_key()
    var_key = gcp_db.key(DataStoreKinds.VARIABLE.value, name, parent=root_key)
    var_entity: Optional[datastore.Entity] = gcp_db.get(key=var_key)
    return var_entity['value'] if var_entity else None


def update_undo_state(name: str, value: str, action: ActionsCommands):
    """
        Update undo Stack
    :param name: variable name that has action
    :param value: his value that been set/unset
    :param action: set/unset
    :return:
    """
    root_key = get_root_key()

    # this previous value of the variable is important for knowing which value to return to.
    old_entity = get_variable_value_with(name=name)

    undo_stack = gcp_db.key(DataStoreKinds.UNDO.value, "undo_stack", parent=root_key)
    undo_stack_entity = gcp_db.get(undo_stack)
    if not undo_stack_entity:
        undo_stack_entity = datastore.Entity(key=undo_stack)
        undo_stack_entity['value'] = []

    undo_stack_entity['value'].append(
        {
            "name": name,
            "value": value,
            "old_value": old_entity,
            "action": action,
        }
    )
    gcp_db.put(undo_stack_entity)


def update_redo_state(name: str, value: str, action: ActionsCommands):
    """
        Update Redo state
    :param name: the name of the variable that been set/unset
    :param value: the value that been set/unset
    :param action: set/unset
    :return:
    """
    root_key = get_root_key()

    old_entity = get_variable_value_with(name=name)

    redo_stack = gcp_db.key(DataStoreKinds.REDO.value, "redo_stack", parent=root_key)
    undo_stack_entity = gcp_db.get(redo_stack)
    if not undo_stack_entity:
        undo_stack_entity = datastore.Entity(key=redo_stack)
        undo_stack_entity['value'] = []

    undo_stack_entity['value'].append(
        {
            "name": name,
            "value": value,
            "old_value": old_entity,
            "action": action,
        }
    )
    gcp_db.put(undo_stack_entity)
