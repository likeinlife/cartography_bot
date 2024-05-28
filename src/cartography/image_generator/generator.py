from io import BytesIO
from pathlib import Path

from domain.models import CoordinatePair
from PIL import Image

from cartography.image_drawer import draw_labels, draw_table
from cartography.math_actions import coordinate_actions
from cartography.types import ImageColorType, ImageType

from .interface import IImageGenerator


class ImageGenerator(IImageGenerator):
    def __init__(
        self,
        resolution: tuple[int, int],
        background_color: ImageColorType,
        font_path: Path,
        padding: int,
        text_color: ImageColorType,
        inverse_text_color: ImageColorType,
        filling_color: ImageColorType,
        text_size_coefficient: int,
        text_angle: int,
        bottom_label_offset: int,
        right_label_offset: int,
    ) -> None:
        self.resolution = resolution
        self.background_color = background_color
        self.inverse_text_color = inverse_text_color
        self.filling_color = filling_color
        self.padding = padding
        self.font_path = font_path
        self.text_color = text_color
        self.text_size_coefficient = text_size_coefficient
        self.text_angle = text_angle
        self.bottom_label_offset = bottom_label_offset
        self.right_label_offset = right_label_offset

    def generate(
        self,
        upper_bound: CoordinatePair,
        lower_bound: CoordinatePair,
        cell_to_fill: str | None,
        title: str,
        parts: int,
        alphabet: list[str],
    ) -> ImageType:
        in_memory_file = BytesIO()
        image = Image.new("RGB", self.resolution, self.background_color)

        draw_table(
            img=image,
            parts=parts,
            title=title,
            alphabet=alphabet,
            cell_to_fill=cell_to_fill,
            background_color=self.background_color,
            filling_color=self.filling_color,
            font_path=self.font_path,
            inverse_text_color=self.inverse_text_color,
            padding=self.padding,
            text_color=self.text_color,
        )
        x_values = coordinate_actions.get_middle_list(lower_bound.longitude, upper_bound.longitude, parts)
        y_values = coordinate_actions.get_middle_list(lower_bound.latitude, upper_bound.latitude, parts)
        y_values.reverse()

        draw_labels(
            img=image,
            parts=parts,
            x_values=x_values,
            y_values=y_values,
            bottom_label_offset=self.bottom_label_offset,
            font_path=self.font_path,
            padding=self.padding,
            right_label_offset=self.right_label_offset,
            text_angle=self.text_angle,
            text_color=self.text_color,
            text_size_coefficient=self.text_size_coefficient,
        )

        image.save(in_memory_file, "JPEG")

        return in_memory_file.getvalue()
