from dataclasses import dataclass

from .actions import CoordinatePairActions
from .coordinate import Coordinate


@dataclass
class CoordinatePair:
    """Pair of geographical coordinates."""

    latitude: Coordinate
    longitude: Coordinate

    def __post_init__(self) -> None:
        self.actions = CoordinatePairActions(self)

    def to_str(self) -> str:
        return self.actions.to_str()

    def __eq__(self, other: "CoordinatePair") -> bool:  # type: ignore
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __str__(self) -> str:
        return self.actions.to_str()
