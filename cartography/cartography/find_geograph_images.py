from cartography.utils.classes import Alphabet
from .re_compilated import re_string
from .find_geograph import get_first, get_part
from .create_image import create_image


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
    for size, part in list_of_parts.items():  # type: ignore
        if size == 'mil':
            saved_bounds = get_first(part)  # type: ignore
            yield create_image(saved_bounds, 12)
        if size == '100':
            saved_bounds = get_part(part, saved_bounds, 12)  # type: ignore
            yield create_image(saved_bounds, 2, Alphabet.UPPER_ALPHA)
        if size == '50' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.UPPER_ALPHA)  # type: ignore
            yield create_image(saved_bounds, 2, Alphabet.LOWER_ALPHA)
        if size == '25' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.LOWER_ALPHA)  # type: ignore
            yield create_image(saved_bounds, 2, Alphabet.NUMBERS)
        if size == '10' and part:
            saved_bounds = get_part(part, saved_bounds, 2, Alphabet.NUMBERS)  # type: ignore

    if saved_bounds == ():
        yield 'Список со значениями пусть, где-то произошла ошибка'
        return
    yield create_image(saved_bounds, 1, [' '])
    return saved_bounds