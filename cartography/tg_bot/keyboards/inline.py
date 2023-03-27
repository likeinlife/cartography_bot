from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_buttons(escape_item: int):
    buttons = [{
        'text': 'Команды',
        'callback_data': 'help_commands'
    }, {
        'text': 'Масштабы',
        'callback_data': 'help_scales'
    }, {
        'text': 'Нуменклатуры',
        'callback_data': 'help_numenclature'
    }]

    if escape_item != -1:
        buttons.pop(escape_item)

    return buttons


def get_inline_help(escape: int) -> InlineKeyboardMarkup:
    inl_keyb = InlineKeyboardBuilder()

    for button in get_buttons(escape):
        inl_keyb.button(**button)

    if escape != -1:
        inl_keyb.button(text='Вернуться', callback_data='help_menu')
        inl_keyb.adjust(2, 1)
        return inl_keyb.as_markup()

    return inl_keyb.as_markup()