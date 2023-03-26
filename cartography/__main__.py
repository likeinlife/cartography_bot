import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from cartography.tg_bot.commands import (
    set_admin_commands,
    set_default_commands,
    set_dev_commands,
)

from .config import config
from .tg_bot import middlewares
from .tg_bot.handlers import (
    ban,
    cartography_geograph_images,
    cartography_numenclature_images,
    geodezia,
    help,
    middle_values,
    tmogi,
    util_handlers,
)


async def start():
    bot = Bot(config.BOT_TOKEN, parse_mode="HTML")
    await set_default_commands(bot)
    await set_admin_commands(bot)
    await set_dev_commands(bot)
    dp = Dispatcher()

    dp.include_router(ban.router)
    dp.include_router(help.router)
    dp.include_router(util_handlers.router)
    dp.include_router(tmogi.router)
    dp.include_router(geodezia.router)
    dp.include_router(cartography_numenclature_images.router)
    dp.include_router(cartography_geograph_images.router)
    dp.include_router(middle_values.router)

    dp.message.middleware(ChatActionMiddleware())
    dp.message.middleware(middlewares.BanListCheck())
    dp.message.middleware(middlewares.LoggingChatActions())

    if not config.PUBLIC:
        dp.message.middleware(middlewares.IsAdminMiddleWare())

    if config.DEV_MODE:
        from .tg_bot.handlers import devs

        dp.include_router(devs.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
