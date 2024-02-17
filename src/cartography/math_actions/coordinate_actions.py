from decimal import Decimal

from cartography.models import Coordinate


def _transform_to_coordinate(seconds: Decimal) -> Coordinate:
    degrees, remaining_seconds = divmod(seconds, 3600)
    minutes, remaining_seconds = divmod(remaining_seconds, 60)
    return Coordinate(degrees=degrees, minutes=minutes, seconds=remaining_seconds)


def _transform_to_seconds(coordinate: Coordinate) -> Decimal:
    return coordinate.degrees * 3600 + coordinate.minutes * 60 + coordinate.seconds


def greater(left: Coordinate, right: Coordinate) -> bool:
    return _transform_to_seconds(left) > _transform_to_seconds(right)


def between(left: Coordinate, this: Coordinate, right: Coordinate) -> bool:
    return all(
        (
            greater(this, left),
            not greater(this, right),
        )
    )


def minus(left: Coordinate, right: Coordinate) -> Coordinate:
    return _transform_to_coordinate(_transform_to_seconds(left) - _transform_to_seconds(right))


def plus(left: Coordinate, right: Coordinate) -> Coordinate:
    return _transform_to_coordinate(_transform_to_seconds(left) + _transform_to_seconds(right))


def multiply(left: Coordinate, multiplier: int) -> Coordinate:
    return _transform_to_coordinate(_transform_to_seconds(left) * multiplier)


def divide(left: Coordinate, divider: int) -> Coordinate:
    return _transform_to_coordinate(_transform_to_seconds(left) / divider)


def get_middle(left: Coordinate, right: Coordinate) -> Coordinate:
    return _transform_to_coordinate((_transform_to_seconds(left) + _transform_to_seconds(right)) / 2)


def get_middle_list(first: Coordinate, second: Coordinate, parts: int) -> list[Coordinate]:
    delta = divide(minus(second, first), parts)
    return [plus(multiply(delta, i), first) for i in range(parts + 1)]


def get_delta(left: Coordinate, right: Coordinate) -> Coordinate:
    return _transform_to_coordinate((_transform_to_seconds(left) + _transform_to_seconds(right)) / 2)


def to_str(coordinate: Coordinate) -> str:
    def _get(number: Decimal, symbol: str, rjust: int) -> str:
        if len(str(number)) > 4:
            number = round(number, 4)
        string = f"{number}{symbol}" if number != 0 else ""
        return string.rjust(rjust, " ")

    degree = _get(coordinate.degrees, "°", 4)
    minute = _get(coordinate.minutes, "'", 4)
    second = _get(coordinate.seconds, '"', 6)

    return f"{degree}{minute}{second}"
