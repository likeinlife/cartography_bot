from dataclasses import dataclass

from .coordinate_pair import CoordinatePair


@dataclass
class Nomenclature:
    title: str
    outer_lower_bound: CoordinatePair
    outer_upper_bound: CoordinatePair
    lower_bound: CoordinatePair
    upper_bound: CoordinatePair
    cell_to_fill: str | None = None
