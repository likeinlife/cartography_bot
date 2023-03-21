from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_buttons():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Стоп')
    keyboard_builder.button(text='Скрыть')

    keyboard_builder.adjust(1, 1)

    return keyboard_builder.as_markup(resize_keyboard=True)