from business import facades, image_drawer
from business.facades import NomenclatureFacade
from container import AppContainer, ImageContainer
from domain.models import CoordinatePair
from misc import from_tuple
from settings import app_settings, image_settings


def main():
    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    image_container = ImageContainer()
    image_container.settings.from_dict(image_settings.model_dump())
    image_container.wire(packages=[image_drawer, facades])

    images = NomenclatureFacade.generate_from_coordinates(
        coordinate_pair=CoordinatePair(
            latitude=from_tuple(50, 54, 55),
            longitude=from_tuple(67, 19, 48),
        ),
        needed_scale=10,
    )
    for n, img in enumerate(images):
        with open(f"images/{n}.jpeg", "wb") as f:
            f.write(img)


if __name__ == "__main__":
    main()
