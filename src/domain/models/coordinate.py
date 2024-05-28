from decimal import Decimal
from functools import total_ordering
from typing import Any

from pydantic import BaseModel, ConfigDict

from .actions import CoordinateActions


@total_ordering
class Coordinate(BaseModel):
    model_config = ConfigDict(extra="allow")
    degrees: Decimal
    minutes: Decimal = Decimal(0)
    seconds: Decimal = Decimal(0)

    def model_post_init(self, __context: Any) -> None:
        self.actions = CoordinateActions(self)

    @classmethod
    def from_seconds(cls, seconds: Decimal) -> "Coordinate":
        degrees, remaining_seconds = divmod(seconds, 3600)
        minutes, remaining_seconds = divmod(remaining_seconds, 60)
        return cls(degrees=degrees, minutes=minutes, seconds=remaining_seconds)

    @classmethod
    def from_tuple(cls, degrees: int, minutes: int = 0, seconds: float | str = 0) -> "Coordinate":
        return cls(degrees=Decimal(degrees), minutes=Decimal(minutes), seconds=Decimal(seconds))

    def to_seconds(self) -> Decimal:
        return self.degrees * 3600 + self.minutes * 60 + self.seconds

    def to_str(self) -> str:
        return self.actions.to_str()

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return self.actions.minus(other)

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return self.actions.plus(other)

    def __mul__(self, multiplier: int) -> "Coordinate":
        return self.actions.multiply(multiplier)

    def __truediv__(self, divider: int) -> "Coordinate":
        return self.actions.divide(divider)

    def __gt__(self, other: "Coordinate") -> bool:
        return self.actions.is_greater_than(other)

    def __eq__(self, other: "Coordinate") -> bool:  # type: ignore
        return self.actions.equal(other)

    def __str__(self) -> str:
        return self.actions.to_str()
