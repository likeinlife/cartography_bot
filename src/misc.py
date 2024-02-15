romanNumeralMap = (
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
)


def generate_roman_number(n: int):
    """
    Convert integer to Roman numeral.

    >>> generate_roman_number(0)
    'N'
    >>> generate_roman_number(3)
    'III'
    >>> generate_roman_number(10)
    'X'
    """
    if n == 0:
        return "N"

    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result
