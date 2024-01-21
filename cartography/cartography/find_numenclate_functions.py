import string
from typing import Callable, Tuple

from ..utils.classes import Numenclat
from .find_geograph_functions import CoordinatePair, Degrees


def get_delta(bounds: Numenclat, parts_number) -> Tuple[Degrees, Degrees]:
    latitude_delta = (bounds.upper_bound.latitude - bounds.lower_bound.latitude) / parts_number
    longitude_delta = (bounds.upper_bound.longitude - bounds.lower_bound.longitude) / parts_number
    return latitude_delta, longitude_delta


def get_first(coordinate: CoordinatePair) -> Numenclat:
    """Find nomenclature by coordinate."""
    alphabet = string.ascii_uppercase
    lower_latitude = Degrees()
    upper_latitude = Degrees()
    lower_longitude = Degrees()
    upper_longitude = Degrees()

    longitude_index = None
    latitude_char = None
    for index, char in enumerate(alphabet):
        lower_latitude = Degrees(index * 4)
        upper_latitude = Degrees(4 * (index + 1))
        if lower_latitude < coordinate.latitude < upper_latitude:
            latitude_char = char
            break

    if not latitude_char:
        exit("Not found latitude char")

    for this_index in range(31, 61):
        lower_longitude = Degrees((this_index - 31) * 6)
        upper_longitude = Degrees(6 * (this_index + 1 - 31))

        if lower_longitude < coordinate.longitude < upper_longitude:
            longitude_index = this_index
            break

    if not longitude_index:
        exit("Not found longitude index")

    numenculat = f"{latitude_char}-{longitude_index}"
    lower_bound = CoordinatePair(lower_latitude, lower_longitude)
    uppder_bound = CoordinatePair(upper_latitude, upper_longitude)
    values = Numenclat(lower_bound, uppder_bound, numenculat)

    return values


def get_numenculat_by_parts(
    coordinate: CoordinatePair,
    parts_number: int,
    bounds: Numenclat,
    alphabet: list[str] | None = None,
    numenclature_format: Callable[[str, str], str] = lambda x, y: f"{x}-{y}",
) -> Numenclat:
    """Figure divided by :arg: parts_number parts, finds nomenclature by :arg: coordinate."""
    latitude_delta, longitude_delta = get_delta(bounds, parts_number)

    upper_latitude = bounds.upper_bound.latitude
    lower_longitude = bounds.lower_bound.longitude
    initional_longitude = (
        lower_longitude.degree,
        lower_longitude.minute,
        lower_longitude.second,
    )

    for this_part in range(1, parts_number**2 + 1):
        lower_latitude = upper_latitude - latitude_delta
        upper_longitude = lower_longitude + longitude_delta
        latitude_if = lower_latitude < coordinate.latitude < upper_latitude
        longitude_if = lower_longitude < coordinate.longitude < upper_longitude

        if latitude_if and longitude_if:
            current_part_name = alphabet[this_part - 1] if alphabet else str(this_part)
            full_numenclature_name = numenclature_format(bounds.numenculat, current_part_name)
            lower_bound = CoordinatePair(lower_latitude, lower_longitude)
            upper_bound = CoordinatePair(upper_latitude, upper_longitude)
            delta = CoordinatePair(latitude_delta, longitude_delta)
            values = Numenclat(
                lower_bound,
                upper_bound,
                full_numenclature_name,
                delta=delta,
                part=current_part_name,
            )
            return values

        if this_part % parts_number == 0:
            upper_latitude = upper_latitude - latitude_delta
            lower_longitude = Degrees(*initional_longitude)
        else:
            lower_longitude = lower_longitude + longitude_delta

    raise Exception("Неизвестная ошибка")
