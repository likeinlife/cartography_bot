from enum import StrEnum, auto


class UtilCommandsEnum(StrEnum):
    START = auto()
    HELP = auto()
    STOP = auto()
    HIDE_KEYBOARD = auto()
    SHOW_KEYBOARD = auto()


class CartographyCommandsEnum(StrEnum):
    BY_NOMENCLATURE_TITLE = auto()
    BY_COORDINATE = auto()
    GET_MIDDLE = auto()


class GeodesyCommandsEnum(StrEnum):
    CALCULATE_MICROMETER = auto()
