from aiogram import Bot, Dispatcher
from .config import config
from .tg_bot import handlers, middlewares
import asyncio


async def start():
    bot = Bot(config.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(handlers.router)
    dp.message.middleware(middlewares.IsAdminMiddleWare())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def main():
    asyncio.run(start())


if __name__ == '__main__':
    main()
