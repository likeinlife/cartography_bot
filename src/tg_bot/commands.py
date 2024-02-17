from typing import TypeAlias

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from container import AppContainer
from dependency_injector.wiring import Provide, inject

from .enums import CartographyCommandsEnum, GeodesyCommandsEnum, UtilCommandsEnum

CommandHelpType: TypeAlias = list[tuple[str, str]]

commands: CommandHelpType = [
    (UtilCommandsEnum.START, "Начало работы"),
    (UtilCommandsEnum.HELP, "Помощь"),
    (UtilCommandsEnum.STOP, "Остановить набор значений"),
    (UtilCommandsEnum.HIDE_KEYBOARD, "Скрыть клавиатуру"),
    (UtilCommandsEnum.SHOW_KEYBOARD, "Показать клавиатуру"),
    (CartographyCommandsEnum.BY_NOMENCLATURE_TITLE, "Сгенерировать изображения по номенклатуре"),
    (CartographyCommandsEnum.BY_COORDINATE, "Сгенерировать изображения по координатам и масштабу"),
    (CartographyCommandsEnum.GET_MIDDLE, "Получить промежуточные значения между границами рамки"),
    (GeodesyCommandsEnum.CALCULATE_MICROMETER, "Посчитать отсчеты по микрометру"),
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
