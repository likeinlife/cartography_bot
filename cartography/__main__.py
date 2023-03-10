import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat

from .config import config
from .tg_bot import middlewares
from .tg_bot.handlers import cartography, tmogi


async def start():
    bot = Bot(config.bot_token, parse_mode='HTML')
    await set_commands(bot)
    dp = Dispatcher()

    dp.include_router(cartography.router)
    dp.include_router(tmogi.router)
    dp.message.middleware(middlewares.IsAdminMiddleWare())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def set_commands(bot: Bot):
    commands = (
        ('start', 'Начало работы'),
        ('by_numenclature', 'Определить координаты рамки'),
        ('by_coordinates', 'Определить нуменклатуру'),
        ('get_middle', 'Получить промежуточные значения между границами рамки'),
        ('stop', 'Остановить ввод значений'),
        ('laplas', 'Отправить таблицу функции Лапласа'),
        ('student', 'Отправить таблицу функции Стьюдента'),
    )
    my_commands = [BotCommand(command=command, description=description) for (command, description) in commands]
    await bot.set_my_commands(my_commands, BotCommandScopeChat(chat_id=config.admin_id, type='chat'))


def main():
    asyncio.run(start())


if __name__ == '__main__':
    main()
