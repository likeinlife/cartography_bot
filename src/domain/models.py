from decimal import Decimal

from pydantic import BaseModel


class Coordinate(BaseModel):
    degrees: Decimal
    minutes: Decimal = Decimal(0)
    seconds: Decimal = Decimal(0)


class CoordinatePair(BaseModel):
    latitude: Coordinate
    longitude: Coordinate


# TODO: outer lower and upper bounds to draw image
class Nomenclature(BaseModel):
    title: str
    lower_bound: CoordinatePair
    upper_bound: CoordinatePair
    cell_to_fill: str | None = None
