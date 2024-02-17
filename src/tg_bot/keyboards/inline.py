from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tg_bot.enums import CallbackDataEnum


def _get_help_buttons(pop: CallbackDataEnum | None) -> dict[CallbackDataEnum, str]:
    buttons = {
        CallbackDataEnum.HELP_COMMANDS: "Команды",
        CallbackDataEnum.HELP_SCALES: "Масштабы",
        CallbackDataEnum.HELP_NOMENCLATURE: "Номенклатуры",
    }

    if pop:
        buttons.pop(pop)

    return buttons


def get_inline_help(pop: CallbackDataEnum | None = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for callback_data, text in _get_help_buttons(pop).items():
        keyboard.button(text=text, callback_data=callback_data)

    if pop:
        keyboard.button(text="Вернуться", callback_data=CallbackDataEnum.HELP_MENU)
        keyboard.adjust(2, 1)
        return keyboard.as_markup()

    return keyboard.as_markup()
