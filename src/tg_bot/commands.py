from typing import TypeAlias

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from container import AppContainer
from dependency_injector.wiring import Provide, inject

CommandHelpType: TypeAlias = list[tuple[str, str]]

commands: CommandHelpType = [
    ("start", "Начало работы"),
    ("help", "Помощь"),
    ("stop", "Остановить набор значений"),
    ("hide", "Скрыть клавиатуру"),
    ("show", "Показать клавиатуру"),
    ("by_nomenclature_images", "Определить координаты рамки, но с изображениями"),
    ("by_coordinates_images", "Определить номенклатуру по координатам и масштабу"),
    ("get_middle", "Получить промежуточные значения между границами рамки"),
    ("micro", "Посчитать отсчеты по микрометру"),
]

dev_commands: CommandHelpType = []

admin_commands: CommandHelpType = []

BotCommand_default = [BotCommand(command=command, description=description) for (command, description) in commands]
BotCommand_dev = [BotCommand(command=command, description=description) for (command, description) in dev_commands]
BotCommand_admin = [BotCommand(command=command, description=description) for (command, description) in admin_commands]

BotCommand_all = BotCommand_default + BotCommand_dev + BotCommand_admin


@inject
async def set_commands(
    bot: Bot,
    dev_mode: bool = Provide[AppContainer.settings.dev_mode],
    admin_id: int = Provide[AppContainer.settings.admin_id],
):
    await bot.set_my_commands(
        BotCommand_admin + BotCommand_default,
        BotCommandScopeChat(chat_id=admin_id, type="chat"),  # type: ignore
    )
    if dev_mode:
        await bot.set_my_commands(BotCommand_all, BotCommandScopeChat(chat_id=admin_id, type="chat"))  # type: ignore
    else:
        await bot.set_my_commands(BotCommand_default, BotCommandScopeDefault())
