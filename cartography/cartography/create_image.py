from io import BytesIO
from cartography.cartography.draw_image import draw_table, draw_values_on_table
from cartography.cartography.get_middle import get_middle_list
from cartography.config import ImageConfig
from cartography.utils.classes import Numenculat
from PIL import Image


def create_image(bounds: Numenculat, parts_number: int, alphabet: list[str] | None = None) -> bytes:
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