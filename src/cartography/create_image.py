from io import BytesIO

from PIL import Image

from src.cartography.draw_image import draw_table, draw_values_on_table
from src.cartography.get_middle import get_middle_list
from src.config import ImageConfig
from src.utils.classes import Numenclat


def create_image(
    bounds: Numenclat,
    parts_number: int,
    alphabet: list[str] | None = None,
    cell_to_fill: str = "",
) -> bytes:
    """
    Делает изображение, вызывает все необходимые функции.

    Args:
    ----
        bounds: Класс с данными
        parts_number: Количество частей
        alphabet: Количество частей
        cell_to_fill: Количество частей

    Returns:
    -------
        Изображение в байтах
    """
    imaginary_doc = BytesIO()
    img = Image.new("RGB", ImageConfig.RESOLUTION, ImageConfig.BACKGROUND_COLOR)
    pad = 100
    draw_table(img, parts_number, pad, bounds.numenculat, alphabet, cell_to_fill)
    x_values = get_middle_list(bounds.lower_bound.longitude, bounds.upper_bound.longitude, parts_number)
    y_values = get_middle_list(bounds.lower_bound.latitude, bounds.upper_bound.latitude, parts_number)
    y_values.reverse()

    draw_values_on_table(img, parts_number, x_values, y_values, pad)

    img.save(imaginary_doc, "JPEG")

    return imaginary_doc.getvalue()
