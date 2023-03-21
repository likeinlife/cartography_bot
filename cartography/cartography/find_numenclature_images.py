from cartography.cartography.create_image import create_image

from ..utils.classes import Alphabet, CoordinatePair, Numenculat
from .find_numenculate import get_first, get_numenculat_by_parts


def get_numenculat_yield_images(coordinate: CoordinatePair, operations: int):
    """
    Args:
        coordinate: coordinate pair
        operations: number of operations.

    Yields bytes images
    """
    saved_values = None
    m_100_values = None
    for operation_number in range(1, operations + 1):
        if operation_number == 1:
            saved_values = get_first(coordinate)
            yield create_image(saved_values, 12)
        if operation_number == 2:
            saved_values = get_numenculat_by_parts(coordinate, 12, saved_values)  # type: ignore
            m_100_values = Numenculat(saved_values.lower_bound, saved_values.upper_bound, saved_values.numenculat)
            yield create_image(saved_values, 2, Alphabet.UPPER_ALPHA)
        if operation_number == 3:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.UPPER_ALPHA)  # type: ignore
            yield create_image(saved_values, 2, Alphabet.LOWER_ALPHA)
        if operation_number == 4:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.LOWER_ALPHA)  # type: ignore
            yield create_image(saved_values, 2)
        if operation_number == 5:
            saved_values = get_numenculat_by_parts(coordinate, 2, saved_values, Alphabet.NUMBERS)  # type: ignore
            yield create_image(saved_values, 2)
        if operation_number == 6:
            saved_values = get_numenculat_by_parts(coordinate, 16, m_100_values)  # type: ignore
            yield create_image(m_100_values, 16)  # type: ignore
        if operation_number == 7:
            yield create_image(saved_values, 3, Alphabet.LOWER_ALPHA_EXTENDENT)  # type: ignore
            saved_values = get_numenculat_by_parts(
                coordinate,
                3,
                saved_values,  # type: ignore
                Alphabet.LOWER_ALPHA_EXTENDENT)
    yield create_image(saved_values, 1, [' '])  # type: ignore
