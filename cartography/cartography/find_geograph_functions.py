import string
from typing import Callable, Optional

from cartography.utils.classes import CoordinatePair, Degrees, Numenclat


def get_first(first_part_name: str) -> Numenclat:
    """Finds geographic coordinates of edges by first part name

    Args:
        first_part (str): R-41, D-58

    """
    first_part = first_part_name.split('-')
    alphabet = string.ascii_uppercase
    lower_latitude = Degrees()
    upper_latitude = Degrees()
    lower_longitude = Degrees()
    upper_longitude = Degrees()

    for index, char in enumerate(alphabet):
        if char == first_part[0]:
            lower_latitude = Degrees(index * 4)
            upper_latitude = Degrees(4 * (index + 1))
            break

    longitude_index = int(first_part[1])
    for this_index in range(30, 61):
        if this_index == longitude_index:
            this_index -= 31
            lower_longitude = Degrees(this_index * 6)
            upper_longitude = Degrees(6 * (this_index + 1))
            break

    lower_bound = CoordinatePair(lower_latitude, lower_longitude)
    upper_bound = CoordinatePair(upper_latitude, upper_longitude)
    return Numenclat(lower_bound, upper_bound, '-'.join(first_part))


def get_part(
    needed_part: str,
    numenclature: Numenclat,
    parts_number: int,
    alphabet: Optional[list] = None,
    numenclature_format: Callable[[str, str], str] = lambda x, y: f'{x}-{y}',
) -> Numenclat:
    """
    Figure divided by :parts_number: parts, finds coordinated of :needed_part:
    Args:
        part: "19", "24"
        numenclature: previous numenclature
        parts_number: 2, 3, 12, 16

    Returns: new bounds
    """
    upper_latitude = numenclature.upper_bound.latitude
    lower_longitude = numenclature.lower_bound.longitude
    initional_longitude = (lower_longitude.degree, lower_longitude.minute, lower_longitude.second)

    latitude_delta = (numenclature.upper_bound.latitude - numenclature.lower_bound.latitude) / parts_number
    longitude_delta = (numenclature.upper_bound.longitude - numenclature.lower_bound.longitude) / parts_number

    if alphabet:
        parts_labels = alphabet
    else:
        parts_labels = list(range(1, parts_number**2 + 1))

    for iteration, this_part in enumerate(parts_labels, start=1):
        if str(this_part) == needed_part:
            lower_latitude = upper_latitude - latitude_delta
            upper_longitude = lower_longitude + longitude_delta
            new_name = numenclature_format(numenclature.numenculat, needed_part)
            upper_bound = CoordinatePair(upper_latitude, upper_longitude)
            lower_bound = CoordinatePair(lower_latitude, lower_longitude)
            delta = CoordinatePair(latitude_delta, longitude_delta)
            return Numenclat(lower_bound, upper_bound, new_name, delta=delta, part=needed_part)

        if iteration % (parts_number) == 0:
            upper_latitude = upper_latitude - latitude_delta
            lower_longitude = Degrees(*initional_longitude)
        else:
            lower_longitude = lower_longitude + longitude_delta

    raise Exception(f'Неизвестная ошибка. Часть {needed_part} не найдена')
