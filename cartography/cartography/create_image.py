from itertools import repeat
from PIL import Image, ImageDraw, ImageFont
from cartography.config import config


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


def draw_table(img: Image, parts: int, pad: int, name: str = "Numenclature", alphabet: list[str] | None = None):
    """Draw table

    Args:
        img (Image): image to edit
        parts (int): parts number. Example: 16x16, parts=16
        pad (int): Length to image borders
        name (str): Table name

    Returns: 
        Tuple[
            delta_x(int) - cell width,
            delta_y(int) - cell height
            ]
    """
    img_draw = ImageDraw.Draw(img)
    delta_x = (img.size[0] - pad * 2) // parts
    delta_y = (img.size[1] - pad * 2) // parts
    font_name, font_size = config.path_to_font, delta_x // 4
    name_size = pad // 4
    width = 2

    pil_font = ImageFont.truetype(font_name, font_size)
    name_font = ImageFont.truetype(font_name, name_size)
    box = img_draw.textbbox((img.size[0] // 2, pad // 2), name, name_font, 'mm')
    img_draw.text(box, name, Color.BLACK, name_font)

    row = 0
    column = 0
    for cell in range(1, parts**2 + 1):
        left_x = pad + column * delta_x
        right_x = pad + (column + 1) * delta_x
        up_y = pad + row * delta_y
        lower_y = pad + (row + 1) * delta_y

        middle_x = left_x + ((right_x - left_x) // 2)
        middle_y = up_y + ((lower_y - up_y) // 2)

        if alphabet:
            number: int | str = alphabet[cell - 1]
        else:
            number = cell

        img_draw.rectangle(((left_x, up_y), (right_x, lower_y)), Color.WHITE, Color.BLACK, width)
        box = img_draw.textbbox((middle_x, middle_y), str(number), pil_font, 'mm')
        img_draw.text(box, str(number), Color.BLACK, pil_font)

        if parts == 1:
            return delta_x, delta_y

        if column % (parts - 1) == 0 and column != 0:
            row += 1
            column = 0
        else:
            column += 1

    return delta_x, delta_y


def draw_values_on_table(
    table_image: Image,
    parts: int,
    x_values: list,
    y_values: list,
    x_delta: int,
    y_delta: int,
    pad: int,
):
    """Generates lables in bottom and right of table

    Args:
        table_image (Image): Image with table
        parts (int): parts number. Example: 16x16 => parts=16
        x_values (list): columns labels
        y_values (list): rows labels
        x_delta (int): cell width
        y_delta (int): cell height
        pad (int): padding from image borders
    """
    img_draw = ImageDraw.Draw(table_image)
    font_name, font_size = config.path_to_font, pad // 7

    pil_font = ImageFont.truetype(font_name, font_size)

    offset_y_from_table = 0  # vertical length to table bottom
    offset_x_from_table = 3  # horizontal length to table right

    # print x values
    for column_label_number, value in zip(range(parts + 1), x_values):
        x = pad + column_label_number * x_delta
        y = table_image.size[1] - pad + offset_y_from_table

        box = img_draw.textbbox((x, y), value, pil_font, 'ms')

        text_img = Image.new('RGBA', (box[2] - box[0], font_size + 1), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)

        text_x_size, _ = text_img.size

        text_draw.text((0, 0), value, Color.BLACK, pil_font)
        text_img = text_img.rotate(300, expand=1)

        table_image.paste(text_img, (x - text_x_size // 4, y), text_img)
    # print y values
    for row_label_number, value in zip(range(parts + 1), y_values):
        x = table_image.size[0] - pad + offset_x_from_table
        y = pad + row_label_number * y_delta

        box = img_draw.textbbox((x, y), value, pil_font, 'ls')
        img_draw.text(box, value, Color.BLACK, pil_font)


if __name__ == '__main__':
    img = Image.new('RGB', (1000, 1000), (255, 255, 255))
    parts = 3
    pad = 100
    x_delta, y_delta = draw_table(img, parts, pad)
    draw_values_on_table(
        img,
        parts,
        repeat('deg min sec'),  # type: ignore
        repeat('deg min sec'),  # type: ignore
        x_delta,
        y_delta,
        pad,
    )
    img.show()