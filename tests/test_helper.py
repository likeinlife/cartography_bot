from cartography.models import CoordinatePair
from misc import from_tuple


def generate_random_bound() -> CoordinatePair:
    return CoordinatePair(latitude=from_tuple(0, 0, 0), longitude=from_tuple(0, 0, 0))
