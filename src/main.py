import asyncio

import bot_start
import tg_bot
from container import AppContainer
from core.settings import app_settings, image_settings


def main():
    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    app_container.image_settings.from_dict(image_settings.model_dump())
    app_container.wire(packages=[tg_bot], modules=[bot_start])

    asyncio.run(bot_start.run())


if __name__ == "__main__":
    main()
