from cartography.config import ImageConfig
from .create_image import draw_table, draw_values_on_table
from cartography.cartography.get_middle import get_middle_list
from PIL import Image
from io import BytesIO
from ..utils.classes import Alphabet, Numenculat, CoordinatePair
from .find_numenculate import get_first, get_numenculat_by_parts


def get_image(bounds: Numenculat, parts_number: int, alphabet: list[str] | None = None) -> bytes:
    """Делает изображение, вызывает все необходимые функции

    Args:
        bounds (Numenculat): Класс с данными
        parts_number (int): Количество частей

    Returns:
        bytes: Изображение в байтах
    """
    imaginary_doc = BytesIO()
    img = Image.new('RGB', ImageConfig.RESOLUTION, ImageConfig.BACKGROUND_COLOR)
    pad = 100
    draw_table(img, parts_number, pad, bounds.numenculat, alphabet)
    x_values = get_middle_list(bounds.lower_bound.longitude, bounds.upper_bound.longitude, parts_number)
    y_values = get_middle_list(bounds.lower_bound.latitude, bounds.upper_bound.latitude, parts_number)
    y_values.reverse()

    draw_values_on_table(img, parts_number, x_values, y_values, pad)

    img.save(imaginary_doc, 'JPEG')

    return imaginary_doc.getvalue()


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
