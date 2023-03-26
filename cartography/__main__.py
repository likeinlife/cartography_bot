import asyncio

from aiogram import Bot, Dispatcher

from cartography.tg_bot.commands import set_default_commands, set_dev_commands

from .config import config
from .tg_bot import middlewares
from .tg_bot.handlers import (cartography_numenclature_images, cartography_geograph_images, geodezia, tmogi,
                              util_handlers, middle_values, ban, help)


async def start():
    bot = Bot(config.BOT_TOKEN, parse_mode='HTML')
    await set_default_commands(bot)
    await set_dev_commands(bot)
    dp = Dispatcher()

    dp.include_router(util_handlers.router)
    dp.include_router(tmogi.router)
    dp.include_router(geodezia.router)
    dp.include_router(cartography_numenclature_images.router)
    dp.include_router(cartography_geograph_images.router)
    dp.include_router(middle_values.router)
    dp.include_router(ban.router)
    dp.include_router(help.router)
    dp.message.middleware(middlewares.ChatActionMiddleware())
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


if __name__ == '__main__':
    main()
