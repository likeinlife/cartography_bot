from io import BytesIO

from container import ImageContainer
from dependency_injector.wiring import Provide, inject
from domain.models import Nomenclature
from domain.types import ImageType
from PIL import Image

from business.image_drawer import draw_labels, draw_table
from business.math_actions import coordinate_actions


class ImageGeneratorFacade:
    @classmethod
    @inject
    def generate(
        cls,
        nomenclature: Nomenclature,
        parts: int,
        alphabet: list[str],
        resolution: tuple[int, int] = Provide[ImageContainer.settings.resolution],
        background_color: tuple[int, int] = Provide[ImageContainer.settings.background_color],
    ) -> ImageType:
        in_memory_file = BytesIO()
        image = Image.new("RGB", resolution, background_color)

        draw_table(
            img=image,
            parts=parts,
            title=nomenclature.title,
            alphabet=alphabet,
            cell_to_fill=nomenclature.cell_to_fill,
        )
        x_values = coordinate_actions.get_middle_list(
            nomenclature.lower_bound.longitude, nomenclature.upper_bound.longitude, parts
        )
        y_values = coordinate_actions.get_middle_list(
            nomenclature.lower_bound.latitude, nomenclature.upper_bound.latitude, parts
        )
        y_values.reverse()

        draw_labels(
            img=image,
            parts=parts,
            x_values=x_values,
            y_values=y_values,
        )

        image.save(in_memory_file, "JPEG")

        return in_memory_file.getvalue()
