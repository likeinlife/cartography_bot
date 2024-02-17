from misc import generate_roman_number

LOWER_ALPHA = ["а", "б", "в", "г"]
LOWER_ALPHA_EXTENDED = ["а", "б", "в", "г", "д", "е", "ж", "з", "и"]
UPPER_ALPHA = ["А", "Б", "В", "Г"]
NUMBERS = ["1", "2", "3", "4"]
ROMAN = [generate_roman_number(n) for n in range(1, 10)]
ROMAN_EXTENDED = [generate_roman_number(n) for n in range(1, 37)]
