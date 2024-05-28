from pydantic import BaseModel

from .coordinate_pair import CoordinatePair


class Nomenclature(BaseModel):
    title: str
    outer_lower_bound: CoordinatePair
    outer_upper_bound: CoordinatePair
    lower_bound: CoordinatePair
    upper_bound: CoordinatePair
    cell_to_fill: str | None = None
