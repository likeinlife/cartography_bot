from aiogram import Bot, Dispatcher
from .config import config
from . import handlers
import asyncio


async def start():
    bot = Bot(config.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(handlers.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
