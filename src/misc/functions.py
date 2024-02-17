from decimal import Decimal as _

from business.models import Coordinate


def generate_roman_number(number: int) -> str:
    """Works for number 1-98 including."""
    variants = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    ten, ten_left = divmod(number, 10)
    if ten_left:
        return f'{"X"*ten}{variants[ten_left-1]}'
    return f'{"X"*ten}'


def from_tuple(degrees: int = 0, minutes: int = 0, seconds: int | float = 0) -> Coordinate:
    return Coordinate(degrees=_(degrees), minutes=_(minutes), seconds=_(seconds))


def generate_coordinate_from_string(string: str) -> Coordinate:
    degrees, minutes, seconds = string.split(" ")
    return from_tuple(int(degrees), int(minutes), float(seconds))
