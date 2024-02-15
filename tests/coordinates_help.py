from decimal import Decimal as _

from domain.models import Coordinate


def from_tuple(degrees: int = 0, minutes: int = 0, seconds: int = 0) -> Coordinate:
    return Coordinate(degrees=_(degrees), minutes=_(minutes), seconds=_(seconds))
