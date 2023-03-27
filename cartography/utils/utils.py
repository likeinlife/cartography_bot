import re
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


def make_float_list_from_str(data: str):
    return list(map(float, data.strip(' ').split(' ')))


def validate_degrees_min_sec(func: Callable):

    async def wrapper(message: Message, state: FSMContext):
        if message.text and re.fullmatch(r'([0-9]{1,3}) ?([0-9]{1,2})? ?([0-9]{1,2})?', str(message.text)):
            text = message.text.split(' ')
            if len(text) > 1:
                if int(text[1]) > 60:
                    return await message.answer('Некорректные минуты')
            if len(text) > 2:
                if int(text[2]) > 60:
                    return await message.answer('Некорректные секунды')
                return await func(message, state)
            return await message.answer('Некорректные координаты. Пример ввода: 10 0 0')

    return wrapper


def validate_operation_number(func: Callable):

    async def wrapper(message: Message, state: FSMContext):
        if message.text and message.text.isdigit() and int(message.text) <= 10:
            return await func(message, state)
        await message.answer('Некорректные данные')

    return wrapper


def make_roman_number(number: int) -> str:
    """Works for number 1-98 including"""
    variants = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    ten, ten_left = divmod(number, 10)
    if ten_left:
        return f'{"X"*ten}{variants[ten_left-1]}'
    return f'{"X"*ten}'
