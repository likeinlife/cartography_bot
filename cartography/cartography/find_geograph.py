from typing import Optional, Tuple
from .classes import Degrees, CoordinatePair, Alphabet, Numenculat
from .re_compilated import re_string
import string


def find_coordinate_bounds_by_numenculature(part: str):
    """Finds geographic coordinates of edges by part name

    Args:
        part (str): R-41-112, D-58-19-A-г, D-58-17-(200-и)
                   ^^^       ^^^
                 English letters

    Returns (Tuple[float, float, float, float]): latitude1, longitude1, latitude2, longitude2
    latitude - широта
    longitude - долгота
    """
    if not (parts := re_string.match(part)):
        exit('Incorrect data')
    short = parts.group

    list_of_parts = {
        'mil': (short('one_mil'), short('one_mil2')),
        '100': short('one_100'),
        '5': short('one_5'),
        '2': short('one_2'),
        '50': short('one_50'),
        '25': short('one_25'),
        '10': short('one_10')
    }

    saved_bounds = ()
    for size, part in list_of_parts.items():
        if size == 'mil':
            saved_bounds = get_first(part)  # type: ignore
            yield saved_bounds
        if size == '100':
            saved_bounds = get_part(part, saved_bounds, 12)  # type: ignore
            yield saved_bounds
        if size == '5' and part:
            saved_bounds = get_part(part, saved_bounds, 16)  # type: ignore
            yield saved_bounds
        if size == '2' and part:
            saved_bounds = get_part(part, saved_bounds, 3, Alphabet.LOWER_ALPHA_EXTENDENT)  # type: ignore
            yield saved_bounds
        if size == '50' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.UPPER_ALPHA)  # type: ignore
            yield saved_bounds
        if size == '25' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.LOWER_ALPHA)  # type: ignore
            yield saved_bounds
        if size == '10' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.NUMBERS)  # type: ignore
            yield saved_bounds

    if saved_bounds == ():
        yield 'Список со значениями пусть, где-то произошла ошибка'
    return saved_bounds


def get_first(first_part: Tuple[str, str]) -> Numenculat:
    """Finds geographic coordinates of edges by first part name

    Args:
        first_part (tuple): (R, 41), (D, 58)

    Returns (Tuple[float, float, float, float]): latitude1, latitude2, longitude1, longitude2
    """
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
    return Numenculat(lower_bound, upper_bound, '-'.join(first_part))


def get_part(needed_part: str,
             numenculat: Numenculat,
             parts_number: int,
             alphabet: Optional[list] = None) -> Numenculat:
    """
    Figure divided by :parts_number: parts, finds coordinated of :needed_part:
    Args:
        part: "19", "24"
        numenculat: Numenculat instance
        parts_number: 2, 3, 12, 16

    Returns: new bounds
    """
    upper_latitude = numenculat.upper_bound.latitude
    lower_longitude = numenculat.lower_bound.longitude
    initional_longitude = (lower_longitude.degree, lower_longitude.minute, lower_longitude.second)

    latitude_delta = (numenculat.upper_bound.latitude - numenculat.lower_bound.latitude) / parts_number
    longitude_delta = (numenculat.upper_bound.longitude - numenculat.lower_bound.longitude) / parts_number

    if alphabet:
        parts_iterator = alphabet
    else:
        parts_iterator = list(range(1, parts_number**2 + 1))

    for iteration, this_part in enumerate(parts_iterator, start=1):
        if str(this_part) == needed_part:
            lower_latitude = upper_latitude - latitude_delta
            upper_longitude = lower_longitude + longitude_delta
            new_name = f'{numenculat.numenculat}-{needed_part}'
            upper_bound = CoordinatePair(upper_latitude, upper_longitude)
            lower_bound = CoordinatePair(lower_latitude, lower_longitude)
            delta = CoordinatePair(latitude_delta, longitude_delta)
            return Numenculat(lower_bound, upper_bound, new_name, delta)

        if iteration % (parts_number) == 0:
            upper_latitude = upper_latitude - latitude_delta
            lower_longitude = Degrees(*initional_longitude)
        else:
            lower_longitude = lower_longitude + longitude_delta

    raise Exception('Неизвестная ошибка')


if __name__ == "__main__":
    find_coordinate_bounds_by_numenculature('N-50-78-Г-в-1')
    # find_coordinate_bounds('U-32-4-Г-а')
    # find_coordinate_bounds('K-39-37-А')
