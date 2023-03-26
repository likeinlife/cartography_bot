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
    ('by_numenclature_images', 'Определить координаты рамки, но с изображениями'),
    ('by_coordinates_images', 'Определить нуменклатуру по координатам и масштабу'),
    ('get_middle', 'Получить промежуточные значения между границами рамки'),
    ('laplas', 'Отправить таблицу функции Лапласа'),
    ('student', 'Отправить таблицу функции Стьюдента'),
    ('micro', 'Посчитать отсчеты по микрометру'),
]

dev_commands = [
    ('not_working_dev', 'Неработающая команда разработчика'),
]

admin_commands = [
    ('ban', 'Забанить'),
    ('unban', 'Разбанить'),
    ('banlist', 'Список забаненых'),
]

BotCommand_default = [BotCommand(command=command, description=description) for (command, description) in commands]
BotCommand_dev = [BotCommand(command=command, description=description) for (command, description) in dev_commands]
BotCommand_admin = [BotCommand(command=command, description=description) for (command, description) in admin_commands]

BotCommand_all = BotCommand_default + BotCommand_dev + BotCommand_admin


async def set_admin_commands(bot: Bot):
    await bot.set_my_commands(BotCommand_admin + BotCommand_default,
                              BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))


async def set_dev_commands(bot: Bot):
    if config.DEV_MODE:
        await bot.set_my_commands(BotCommand_all, BotCommandScopeChat(chat_id=config.ADMIN_ID, type='chat'))


async def set_default_commands(bot: Bot):

    if config.PUBLIC:
        await bot.set_my_commands(BotCommand_default, BotCommandScopeDefault())
