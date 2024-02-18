from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from cartography.math_actions import coordinate_actions
from cartography.models import Coordinate
from cartography.types import ImageColorType


def draw_labels(
    img: Image.Image,
    parts: int,
    x_values: list[Coordinate],
    y_values: list[Coordinate],
    padding: int,
    font_path: Path,
    text_color: ImageColorType,
    text_size_coefficient: int,
    text_angle: int,
    bottom_label_offset: int,
    right_label_offset: int,
) -> None:
    """
    Generate labels in bottom and right part of table.

    Args:
        table_image: Image with table
        parts: parts number. Example: 16x16 => parts=16
        x_values: columns labels
        y_values: rows labels
        x_delta: cell width
        y_delta: cell height
        padding: padding from image borders
        font_path: path to .otf file
        text_color: text color
        text_size_coefficient: font size calculates from padding
        text_angle: in degrees
        bottom_label_offset: offset from bottom
        right_label_offset: offset from right

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
