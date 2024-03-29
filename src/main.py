import asyncio

import tg_bot
from container import AppContainer
from core.settings import app_settings, image_settings


def main():
    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    app_container.image_settings.from_dict(image_settings.model_dump())
    app_container.init_resources()
    app_container.wire(packages=[tg_bot])

    asyncio.run(tg_bot.run())


if __name__ == "__main__":
    main()
