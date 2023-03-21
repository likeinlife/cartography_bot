import asyncio

from aiogram import Bot, Dispatcher

from cartography.tg_bot.commands import set_default_commands, set_dev_commands

from .config import config
from .tg_bot import middlewares
from .tg_bot.handlers import (cartography, cartography_images, geodezia, tmogi, util_handlers)


async def start():
    bot = Bot(config.BOT_TOKEN, parse_mode='HTML')
    await set_default_commands(bot)
    await set_dev_commands(bot)
    dp = Dispatcher()

    dp.include_router(cartography.router)
    dp.include_router(tmogi.router)
    dp.include_router(geodezia.router)
    dp.include_router(cartography_images.router)
    dp.include_router(util_handlers.router)
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
