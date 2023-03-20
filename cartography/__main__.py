import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from .config import config
from .tg_bot import middlewares
from .tg_bot.handlers import cartography, tmogi, geodezia, cartography_images


async def start():
    bot = Bot(config.BOT_TOKEN, parse_mode='HTML')
    await set_commands(bot)
    dp = Dispatcher()

    dp.include_router(cartography.router)
    dp.include_router(tmogi.router)
    dp.include_router(geodezia.router)
    dp.include_router(cartography_images.router)
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


async def set_commands(bot: Bot):
    commands = [
        ('start', 'Начало работы'),
        ('by_numenclature', 'Определить координаты рамки'),
        ('by_coordinates', 'Определить нуменклатуру'),
        ('by_coordinates_images', 'Определить нуменклатуру, но с изображениями'),
        ('get_middle', 'Получить промежуточные значения между границами рамки'),
        ('stop', 'Остановить ввод значений'),
        ('laplas', 'Отправить таблицу функции Лапласа'),
        ('student', 'Отправить таблицу функции Стьюдента'),
        ('micro', 'Посчитать отсчеты по микрометру'),
    ]

    dev_commands = [
        ('not_working_dev', 'Неработающая команда разработчика'),
    ]
    BotCommand_my_commands = [
        BotCommand(command=command, description=description) for (command, description) in commands
    ]
    BotCommand_dev_commands = [
        BotCommand(command=command, description=description) for (command, description) in dev_commands
    ]
    BotCommand_all_commands = BotCommand_my_commands + BotCommand_dev_commands

    if config.PUBLIC:
        await bot.set_my_commands(BotCommand_my_commands, BotCommandScopeDefault())

    if config.DEV_MODE:
        await bot.set_my_commands(BotCommand_all_commands, BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))
    else:
        return await bot.set_my_commands(BotCommand_my_commands,
                                         BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))


def main():
    asyncio.run(start())


if __name__ == '__main__':
    main()
