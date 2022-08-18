import enum


class GameChoice(enum.Enum):
    CHECK = 0
    PASS = 1
    TRAP_CARD = 2
    ACTION_CARD = 3
    COUNTER_CARD = 4
    NONE = 5
