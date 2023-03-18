import string
from typing import Tuple
from PIL import Image
from io import BytesIO

from cartography.cartography.get_middle import get_middle, get_middle_list

from ..utils.classes import Alphabet, Numenculat
from .find_geograph import CoordinatePair, Degrees
from .create_image import draw_table, draw_values_on_table


def get_image(bounds: Numenculat, parts_number: int, alphabet: list[str] | None = None) -> bytes:
    """Делает изображение, вызывает все необходимые функции

    Args:
        bounds (Numenculat): Класс с данными
        parts_number (int): Количество частей

    Returns:
        bytes: Изображение в байтах
    """
    imaginary_doc = BytesIO()
    img = Image.new('RGB', (1000, 1000), (255, 255, 255))
    pad = 100
    x_delta, y_delta = draw_table(img, parts_number, pad, bounds.numenculat, alphabet)
    x_values = get_middle_list(bounds.lower_bound.longitude, bounds.upper_bound.longitude, parts_number)
    y_values = get_middle_list(bounds.lower_bound.latitude, bounds.upper_bound.latitude, parts_number)
    y_values.reverse()

    draw_values_on_table(img, parts_number, x_values, y_values, x_delta, y_delta, pad)

    img.save(imaginary_doc, 'JPEG')

    return imaginary_doc.getvalue()


def get_numenculat_by_coordinates_yield_images(coordinate: CoordinatePair, operations: int):
    """
    Args:
        coordinate: coordinate pair
        operations: number of operations.
    """
    saved_values = None
    m_100_values = None
    for operation_number in range(1, operations + 1):
        if operation_number == 1:
            saved_values = get_first(coordinate)
            yield get_image(saved_values, 12)
        if operation_number == 2:
            saved_values = get_numenculat_by_parts(coordinate, 12, saved_values)  # type: ignore
            m_100_values = Numenculat(saved_values.lower_bound, saved_values.upper_bound, saved_values.numenculat)
            yield get_image(saved_values, 2, Alphabet.UPPER_ALPHA)
        if operation_number == 3:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.UPPER_ALPHA)  # type: ignore
            yield get_image(saved_values, 2, Alphabet.LOWER_ALPHA)
        if operation_number == 4:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.LOWER_ALPHA)  # type: ignore
            yield get_image(saved_values, 2)
        if operation_number == 5:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.NUMBERS)  # type: ignore
            yield get_image(saved_values, 2)
        if operation_number == 6:
            saved_values = get_numenculat_by_parts(coordinate, 16, m_100_values)  # type: ignore
            yield get_image(m_100_values, 16)  # type: ignore
        if operation_number == 7:
            yield get_image(saved_values, 3, Alphabet.LOWER_ALPHA_EXTENDENT)  # type: ignore
            saved_values = get_numenculat_by_parts(
                coordinate,
                3,
                saved_values,  # type: ignore
                Alphabet.LOWER_ALPHA_EXTENDENT)
    yield get_image(saved_values, 1, [' '])  # type: ignore


def get_numenculat_by_coordinates(coordinate: CoordinatePair, operations: int):
    """
    Args:
        coordinate: coordinate pair
        operations: number of operations.
    """
    saved_values = None
    m_100_values = None
    for operation_number in range(1, operations + 1):
        if operation_number == 1:
            saved_values = get_first(coordinate)
        if operation_number == 2:
            saved_values = get_numenculat_by_parts(coordinate, 12, saved_values)  # type: ignore
            m_100_values = Numenculat(saved_values.lower_bound, saved_values.upper_bound, saved_values.numenculat)
            yield saved_values
        if operation_number == 3:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.UPPER_ALPHA)  # type: ignore
            yield saved_values
        if operation_number == 4:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.LOWER_ALPHA)  # type: ignore
            yield saved_values
        if operation_number == 5:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.NUMBERS)  # type: ignore
            yield saved_values
        if operation_number == 6:
            saved_values = get_numenculat_by_parts(coordinate, 16, m_100_values)  # type: ignore
            yield saved_values
        if operation_number == 7:
            saved_values = get_numenculat_by_parts(
                coordinate,
                3,
                saved_values,  # type: ignore
                Alphabet.LOWER_ALPHA_EXTENDENT)  # type: ignore
            yield saved_values
    return saved_values


def get_delta(bounds: Numenculat, parts_number) -> Tuple[Degrees, Degrees]:
    latitude_delta = (bounds.upper_bound.latitude - bounds.lower_bound.latitude) / parts_number
    longitude_delta = (bounds.upper_bound.longitude - bounds.lower_bound.longitude) / parts_number
    return latitude_delta, longitude_delta


def get_first(coordinate: CoordinatePair) -> Numenculat:
    """Finds numenculat by coordinate

    Args:
        first_part (CoordinatePair): CoordinatePair()

    Returns : (latitude1, latitude2, longitude1, longitude2), part
    """
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
        exit('Not found latitude char')

    for this_index in range(31, 61):
        lower_longitude = Degrees((this_index - 31) * 6)
        upper_longitude = Degrees(6 * (this_index + 1 - 31))

        if lower_longitude < coordinate.longitude < upper_longitude:
            longitude_index = this_index
            break

    if not longitude_index:
        exit('Not found longitude index')

    numenculat = f'{latitude_char}-{longitude_index}'
    lower_bound = CoordinatePair(lower_latitude, lower_longitude)
    uppder_bound = CoordinatePair(upper_latitude, upper_longitude)
    values = Numenculat(lower_bound, uppder_bound, numenculat)

    return values


def get_numenculat_by_parts(
    coordinate: CoordinatePair,
    parts_number: int,
    bounds: Numenculat,
    alphabet: list | None = None,
) -> Numenculat:
    """
    Figure divided by :arg:parts_number parts, finds numenculat by :arg:coordinate
    Args:
        parts_number: 2, 3, 12, 16
        bounds: left lower, right upper
        alphabet: ('А', 'Б', 'В', 'Г')

    Returns: Numenculat
    """

    latitude_delta, longitude_delta = get_delta(bounds, parts_number)

    upper_latitude = bounds.upper_bound.latitude
    lower_longitude = bounds.lower_bound.longitude
    initional_longitude = (lower_longitude.degree, lower_longitude.minute, lower_longitude.second)

    for this_part in range(1, parts_number**2 + 1):
        lower_latitude = upper_latitude - latitude_delta
        upper_longitude = lower_longitude + longitude_delta
        latitude_if = lower_latitude < coordinate.latitude < upper_latitude
        longitude_if = lower_longitude < coordinate.longitude < upper_longitude

        if latitude_if and longitude_if:
            if parts_number == 16 or alphabet == Alphabet.LOWER_ALPHA_EXTENDENT:
                part_name = f'{bounds.numenculat}-({alphabet[this_part-1] if alphabet else this_part})'
            else:
                part_name = f'{bounds.numenculat}-{alphabet[this_part-1] if alphabet else this_part}'
            lower_bound = CoordinatePair(lower_latitude, lower_longitude)
            upper_bound = CoordinatePair(upper_latitude, upper_longitude)
            delta = CoordinatePair(latitude_delta, longitude_delta)
            values = Numenculat(lower_bound, upper_bound, str(part_name), delta=delta)
            return values

        if this_part % parts_number == 0:
            upper_latitude = upper_latitude - latitude_delta
            lower_longitude = Degrees(*initional_longitude)
        else:
            lower_longitude = lower_longitude + longitude_delta

    raise Exception('Неизвестная ошибка')


def main(coordinates: CoordinatePair, operations: int):
    """
    Args:
        coordinate: Your coordinates
        operations: Number of scaling. 1 - 1:1_000_000, 2 - 1:100_000, 3 - 1:50_000, 4 - 1:25_000, 5 - 10_000, 6 - 5000, 7 - 2000

    >>> main(CoordinatePair(Degrees(15, 34, 21), Degrees(165, 9, 17)), 5)
    lower: φ =  15° 32' 30.0" ;λ = 165°  7' 30.0"
    upper: φ =  15° 35'  0.0" ;λ = 165° 11' 15.0"
    numenculatura: D-58-19-А-г-1

    >>> main(CoordinatePair(Degrees(50, 54, 55), Degrees(67, 19, 48)), 7)
    lower: φ =  50° 54' 35.0" ;λ =  67° 19' 22.5"
    upper: φ =  50° 55'  0.0" ;λ =  67° 20'  0.0"
    numenculatura: M-42-39-(75)-(б)

    """
    return get_numenculat_by_coordinates(coordinates, operations)


if __name__ == "__main__":
    main(CoordinatePair(Degrees(55, 24, 55), Degrees(80, 21, 48)), 7)
