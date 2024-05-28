from domain.models import CoordinatePair

from .coordinate_actions import divide, minus
from .coordinate_actions import to_str as coordinate_to_str


def get_delta(upper_bound: CoordinatePair, lower_bound: CoordinatePair, parts_number: int) -> CoordinatePair:
    """
    Calculate the delta between upper and lower bounds for latitude and longitude based on the given parts number.

    Args:
        upper_bound (CoordinatePair): The upper bound coordinate pair
        lower_bound (CoordinatePair): The lower bound coordinate pair
        parts_number (int): The number of parts to divide the bounds into

    Returns:
        CoordinatePair: The calculated latitude and longitude delta
    """
    latitude_delta = divide(minus(upper_bound.latitude, lower_bound.latitude), parts_number)
    longitude_delta = divide(minus(upper_bound.longitude, lower_bound.longitude), parts_number)
    return CoordinatePair(latitude=latitude_delta, longitude=longitude_delta)


def to_str(coordinate_pair: CoordinatePair) -> str:
    return f"Latitude: {coordinate_to_str(coordinate_pair.latitude)} {coordinate_to_str(coordinate_pair.longitude)}"
