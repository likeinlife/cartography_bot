from pathlib import Path

from container import ImageContainer
from dependency_injector.wiring import Provide, inject
from domain.types import ImageColorType
from PIL import Image, ImageDraw, ImageFont


@inject
def draw_labels(
    table_image: Image.Image,
    parts: int,
    x_values: list,
    y_values: list,
    pad: int,
    font_path: Path = Provide[ImageContainer.settings.path_to_font],
    text_color: ImageColorType = Provide[ImageContainer.settings.text_color],
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
    img_draw = ImageDraw.Draw(table_image)
    x_delta = (table_image.size[0] - pad * 2) // parts
    y_delta = (table_image.size[1] - pad * 2) // parts
    font_size = pad // 7

    pil_font = ImageFont.truetype(str(font_path), font_size)

    # print x values
    for column_label_number, value in zip(range(parts + 1), x_values):
        x = pad + column_label_number * x_delta
        y = table_image.size[1] - pad + bottom_label_offset

        box = img_draw.textbbox((x, y), value, pil_font, "ms")

        text_img = Image.new("RGBA", (box[2] - box[0], font_size + 1), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)

        text_x_size, _ = text_img.size

        text_draw.text((0, 0), value, text_color, pil_font)
        text_img = text_img.rotate(text_angle, expand=True)

        table_image.paste(text_img, (x - text_x_size // 4, y), text_img)

    # print y values
    for row_label_number, value in zip(range(parts + 1), y_values):
        x = table_image.size[0] - pad + right_label_offset
        y = pad + row_label_number * y_delta

        box = img_draw.textbbox((x, y), value, pil_font, "ls")
        img_draw.text(box, value, text_color, pil_font)  # type: ignore
