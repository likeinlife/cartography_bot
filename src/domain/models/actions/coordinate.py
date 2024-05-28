import typing as tp
from decimal import Decimal

if tp.TYPE_CHECKING:
    from domain.models import Coordinate


class CoordinateActions:
    def __init__(self, coordinate: "Coordinate") -> None:
        self._coordinate = coordinate

    def is_greater_than(self, coordinate: "Coordinate") -> bool:
        return self._coordinate.to_seconds() > coordinate.actions._coordinate.to_seconds()

    def equal(self, coordinate: "Coordinate") -> bool:
        return self._coordinate.to_seconds() == coordinate.actions._coordinate.to_seconds()

    def between(self, left: "Coordinate", right: "Coordinate") -> bool:
        return self._coordinate > left and self._coordinate < right

    def minus(self, right: "Coordinate") -> "Coordinate":
        return self._coordinate.from_seconds((self._coordinate.to_seconds() - right.actions._coordinate.to_seconds()))

    def plus(self, right: "Coordinate") -> "Coordinate":
        return self._coordinate.from_seconds(self._coordinate.to_seconds() + right.actions._coordinate.to_seconds())

    def multiply(self, multiplier: int) -> "Coordinate":
        return self._coordinate.from_seconds(self._coordinate.to_seconds() * multiplier)

    def divide(self, divider: int) -> "Coordinate":
        return self._coordinate.from_seconds(self._coordinate.to_seconds() / divider)

    def get_middle(self, coordinate: "Coordinate") -> "Coordinate":
        return self._coordinate.from_seconds((self._coordinate.to_seconds() + coordinate.to_seconds()) / 2)

    def get_middle_list(self, second: "Coordinate", parts: int) -> list["Coordinate"]:
        seconds_between = second - self._coordinate
        delta = seconds_between / parts
        return [self._coordinate + delta * i for i in range(parts + 1)]

    def to_str(self) -> str:
        def _get(number: Decimal, symbol: str, rjust: int) -> str:
            if len(str(number)) > 4:
                number = round(number, 4)
            string = f"{number}{symbol}" if number != 0 else ""
            return string.rjust(rjust, " ")

        degree = _get(self._coordinate.degrees, "°", 4)
        minute = _get(self._coordinate.minutes, "'", 4)
        second = _get(self._coordinate.seconds, '"', 6)

        return f"{degree}{minute}{second}"
