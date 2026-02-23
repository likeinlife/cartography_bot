import asyncio

import core.logger_setup as logger_setup
import tg_bot
from container import create_container
from core.settings import app_settings, image_settings


async def run() -> None:
    logger_setup.configure_logging(
        debug_mode=app_settings.dev_mode,
        logging_level=app_settings.logging_level,
    )
    container = create_container(image_settings)
    await tg_bot.run(
        bot_token=app_settings.bot_token,
        dev_mode=app_settings.dev_mode,
        admin_id=app_settings.admin_id,
        container=container,
    )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
