import typing as tp

if tp.TYPE_CHECKING:
    from domain.models import CoordinatePair


class CoordinatePairActions:
    def __init__(self, coordinate_pair: "CoordinatePair") -> None:
        self._coordinate_pair = coordinate_pair

    def get_delta(self, upper_bound: "CoordinatePair", parts_number: int) -> "CoordinatePair":
        """
        Calculate the delta between upper and lower bounds for latitude and longitude based on the given parts number.

        Args:
            upper_bound ("CoordinatePair"): The upper bound coordinate pair
            lower_bound ("CoordinatePair"): The lower bound coordinate pair
            parts_number (int): The number of parts to divide the bounds into

        Returns:
            "CoordinatePair": The calculated latitude and longitude delta

        """
        latitude_delta = (upper_bound.latitude - self._coordinate_pair.latitude) / parts_number
        longitude_delta = (upper_bound.longitude - self._coordinate_pair.longitude) / parts_number
        return self._coordinate_pair.__class__(latitude=latitude_delta, longitude=longitude_delta)

    def to_str(self) -> str:
        return f"Latitude: {self._coordinate_pair.latitude.to_str()} {self._coordinate_pair.longitude.to_str()}"
