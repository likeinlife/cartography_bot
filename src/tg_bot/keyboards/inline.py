from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tg_bot.enums import HelpCallbackEnum


def _get_help_buttons(pop: HelpCallbackEnum | None) -> dict[HelpCallbackEnum, str]:
    buttons = {
        HelpCallbackEnum.HELP_COMMANDS: "Команды",
        HelpCallbackEnum.HELP_SCALES: "Масштабы",
        HelpCallbackEnum.HELP_NOMENCLATURE: "Номенклатуры",
    }

    if pop:
        buttons.pop(pop)

    return buttons


def get_inline_help(pop: HelpCallbackEnum | None = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for callback_data, text in _get_help_buttons(pop).items():
        keyboard.button(text=text, callback_data=callback_data)

    if pop:
        keyboard.button(text="Вернуться", callback_data=HelpCallbackEnum.HELP_MENU)
        keyboard.adjust(2, 1)
        return keyboard.as_markup()

    return keyboard.as_markup()
