from business import image_drawer
from container import AppContainer, ImageContainer
from settings import app_settings, image_settings


def main():
    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    image_container = ImageContainer()
    image_container.settings.from_dict(image_settings.model_dump())
    image_container.wire(packages=[image_drawer])


if __name__ == "__main__":
    main()
