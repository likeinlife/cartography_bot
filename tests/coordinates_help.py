from decimal import Decimal as _

from domain.models import Coordinate


def from_tuple(coordinates: tuple[int, int, int]) -> Coordinate:
    return Coordinate(degrees=_(coordinates[0]), minutes=_(coordinates[1]), seconds=_(coordinates[2]))
