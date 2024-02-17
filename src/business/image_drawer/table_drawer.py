from pathlib import Path
from typing import Any

from container import ImageContainer
from dependency_injector.wiring import Provide, inject
from PIL import Image, ImageDraw, ImageFont

from business.types import ImageColorType


@inject
def draw_table(
    img: Image.Image,
    parts: int,
    alphabet: list[str],
    title: str = "Nomenclature",
    cell_to_fill: str | None = None,
    padding: int = Provide[ImageContainer.settings.padding],
    font_path: Path = Provide[ImageContainer.settings.font_path],
    text_color: ImageColorType = Provide[ImageContainer.settings.text_color],
    inverse_text_color: ImageColorType = Provide[ImageContainer.settings.inverse_text_color],
    background_color: ImageColorType = Provide[ImageContainer.settings.background_color],
    filling_color: ImageColorType = Provide[ImageContainer.settings.filling_color],
) -> None:
    """
    Draw table with cells content.

    Args:
        img: image instance
        parts: parts count. Example: 16x16, parts=16
        pad: Length to image borders
        title: Table name
        alphabet: Alphabet
        cell_to_fill: Cell name to fill
    """

    def need_to_fill(x: Any) -> bool:
        return cell_to_fill is not None and str(x) == cell_to_fill

    img_draw = ImageDraw.Draw(img)
    delta_x = (img.size[0] - padding * 2) // parts
    delta_y = (img.size[1] - padding * 2) // parts
    font_size = delta_x // 4
    name_size = padding // 4
    width = 2

    pil_font = ImageFont.truetype(str(font_path), font_size)
    name_font = ImageFont.truetype(str(font_path), name_size)

    # Draw title
    box = img_draw.textbbox((img.size[0] // 2, padding // 2), title, name_font, "mm")
    img_draw.text(box, title, text_color, name_font)  # type: ignore

    row = 0
    column = 0
    for cell_number in range(1, parts**2 + 1):
        left_x = padding + column * delta_x
        right_x = padding + (column + 1) * delta_x
        up_y = padding + row * delta_y
        lower_y = padding + (row + 1) * delta_y

        middle_x = (right_x + left_x) // 2
        middle_y = (lower_y + up_y) // 2

        cell_name: int | str = alphabet[cell_number - 1]

        box = img_draw.textbbox((middle_x, middle_y), str(cell_name), pil_font, "mm")

        # Draw cell: text, outline and fill
        if need_to_fill(cell_name):
            img_draw.rectangle(
                ((left_x, up_y), (right_x, lower_y)),
                filling_color,
                text_color,
                width,
            )
            img_draw.text(box, str(cell_name), inverse_text_color, pil_font)  # type: ignore
        else:
            img_draw.rectangle(
                ((left_x, up_y), (right_x, lower_y)),
                background_color,
                text_color,
                width,
            )
            img_draw.text(box, str(cell_name), text_color, pil_font)  # type: ignore

        if parts == 1:
            return

        if column % (parts - 1) == 0 and column != 0:
            row += 1
            column = 0
        else:
            column += 1
