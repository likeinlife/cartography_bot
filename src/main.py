import asyncio

import tg_bot
from container import AppContainer
from core.database import healthcheck
from core.settings import app_settings, image_settings


async def _run() -> None:
    if app_settings.analytics_enabled:
        if not app_settings.database_url:
            raise RuntimeError("DATABASE_URL must be set when ANALYTICS_ENABLED=True")
        await healthcheck(app_settings.database_url)

    app_container = AppContainer()
    app_container.settings.from_dict(app_settings.model_dump())
    app_container.image_settings.from_dict(image_settings.model_dump())
    app_container.init_resources()
    app_container.wire(packages=[tg_bot])
    await tg_bot.run()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
