import typing as tp

from misc import generate_roman_number

LOWER_ALPHA: tp.Final = ["а", "б", "в", "г"]
LOWER_ALPHA_EXTENDED: tp.Final = ["а", "б", "в", "г", "д", "е", "ж", "з", "и"]
UPPER_ALPHA: tp.Final = ["А", "Б", "В", "Г"]
NUMBERS: tp.Final = ["1", "2", "3", "4"]
ROMAN: tp.Final = [generate_roman_number(n) for n in range(1, 10)]
ROMAN_EXTENDED: tp.Final = [generate_roman_number(n) for n in range(1, 37)]


INIT_GEO_ZONE: tp.Final = 30
FINISH_GEO_ZONE: tp.Final = 61
