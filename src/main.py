import asyncio

import bot_start
import tg_bot
from business import facades, image_drawer
from container import AppContainer, ImageContainer
from core.settings import app_settings, image_settings


def main():
    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    app_container.wire(packages=[tg_bot], modules=[bot_start])
    image_container = ImageContainer()
    image_container.settings.from_dict(image_settings.model_dump())
    image_container.wire(packages=[image_drawer, facades])

    asyncio.run(bot_start.run())


if __name__ == "__main__":
    main()
