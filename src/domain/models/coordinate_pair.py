from typing import Any

from pydantic import BaseModel, ConfigDict

from .actions import CoordinatePairActions
from .coordinate import Coordinate


class CoordinatePair(BaseModel):
    model_config = ConfigDict(extra="allow")
    latitude: Coordinate
    longitude: Coordinate

    def model_post_init(self, __context: Any) -> None:
        self.actions = CoordinatePairActions(self)

    def __eq__(self, other: "CoordinatePair") -> bool:  # type: ignore
        return self.latitude == other.latitude and self.longitude == other.longitude
