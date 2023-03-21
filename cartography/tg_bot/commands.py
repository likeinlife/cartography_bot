from aiogram import Bot
from aiogram.types import (BotCommand, BotCommandScopeChat, BotCommandScopeDefault)

from cartography.config import config

commands = [
    ('start', 'Начало работы'),
    ('help', 'Помощь'),
    ('stop', 'Остановить набор значений'),
    ('hide', 'Скрыть клавиатуру'),
    ('show', 'Показать клавиатуру'),
    ('by_numenclature', 'Определить координаты рамки по нуменклатуре'),
    ('by_coordinates', 'Определить нуменклатуру по координатам и масштабу'),
    ('by_coordinates_images', 'Определить нуменклатуру, но с изображениями'),
    ('get_middle', 'Получить промежуточные значения между границами рамки'),
    ('laplas', 'Отправить таблицу функции Лапласа'),
    ('student', 'Отправить таблицу функции Стьюдента'),
    ('micro', 'Посчитать отсчеты по микрометру'),
]

dev_commands = [
    ('not_working_dev', 'Неработающая команда разработчика'),
]

BotCommand_my_commands = [BotCommand(command=command, description=description) for (command, description) in commands]
BotCommand_dev_commands = [
    BotCommand(command=command, description=description) for (command, description) in dev_commands
]
BotCommand_all_commands = BotCommand_my_commands + BotCommand_dev_commands


async def set_dev_commands(bot: Bot):
    if config.DEV_MODE:
        await bot.set_my_commands(BotCommand_all_commands, BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))
    else:
        return await bot.set_my_commands(BotCommand_my_commands,
                                         BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))


async def set_default_commands(bot: Bot):

    if config.PUBLIC:
        await bot.set_my_commands(BotCommand_my_commands, BotCommandScopeDefault())
