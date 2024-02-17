from pathlib import Path

from container import ImageContainer
from dependency_injector.wiring import Provide, inject
from domain.models import Coordinate
from PIL import Image, ImageDraw, ImageFont

from business.math_actions import coordinate_actions
from business.types import ImageColorType


@inject
def draw_labels(
    img: Image.Image,
    parts: int,
    x_values: list[Coordinate],
    y_values: list[Coordinate],
    padding: int = Provide[ImageContainer.settings.padding],
    font_path: Path = Provide[ImageContainer.settings.font_path],
    text_color: ImageColorType = Provide[ImageContainer.settings.text_color],
    text_size_coefficient: int = Provide[ImageContainer.settings.text_size_coefficient],
    text_angle: int = Provide[ImageContainer.settings.text_angle],
    bottom_label_offset: int = Provide[ImageContainer.settings.bottom_label_offset],
    right_label_offset: int = Provide[ImageContainer.settings.right_label_offset],
) -> None:
    """
    Generate labels in bottom and right of table.

    Args:
    ----
        table_image (Image): Image with table
        parts (int): parts number. Example: 16x16 => parts=16
        x_values (list): columns labels
        y_values (list): rows labels
        x_delta (int): cell width
        y_delta (int): cell height
        pad (int): padding from image borders
    """
    img_draw = ImageDraw.Draw(img)
    x_delta = (img.size[0] - padding * 2) // parts
    y_delta = (img.size[1] - padding * 2) // parts
    font_size = padding // text_size_coefficient

    pil_font = ImageFont.truetype(str(font_path), font_size)

    # print x values
    for column_label_number, value in zip(range(parts + 1), x_values):
        x = padding + column_label_number * x_delta
        y = img.size[1] - padding + bottom_label_offset

        box = img_draw.textbbox((x, y), coordinate_actions.to_str(value), pil_font, "ms")

        text_img = Image.new("RGBA", (box[2] - box[0], font_size + 1), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)

        text_x_size, _ = text_img.size

        text_draw.text((0, 0), coordinate_actions.to_str(value), text_color, pil_font)
        text_img = text_img.rotate(text_angle, expand=True)

        img.paste(text_img, (x - text_x_size // 4, y), text_img)

    # print y values
    for row_label_number, value in zip(range(parts + 1), y_values):
        x = img.size[0] - padding + right_label_offset
        y = padding + row_label_number * y_delta

        box = img_draw.textbbox((x, y), coordinate_actions.to_str(value), pil_font, "ls")

        text_img = Image.new("RGBA", (box[2] - box[0], font_size + 1), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)

        text_x_size, _ = text_img.size

        text_draw.text((0, 0), coordinate_actions.to_str(value), text_color, pil_font)
        text_img = text_img.rotate(text_angle, expand=True)

        img.paste(text_img, (x, y - text_x_size // 4), text_img)
