from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_showButtons():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Стоп")
    keyboard_builder.button(text="Помощь")

    keyboard_builder.adjust(3)

    return keyboard_builder.as_markup(resize_keyboard=True)
