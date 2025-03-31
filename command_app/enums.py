import enum


class DataStoreKinds(enum.StrEnum):
    DB_ROOT = "RootDB"
    VARIABLE = "Variable"
    UNDO = "Undo"
    REDO = "Redo"


class ActionsCommands(enum.IntEnum):
    SET = 1
    UNSET = 2
