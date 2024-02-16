import re
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

coordinate_pattern = re.compile(r"([0-9]{1,3}) ?([0-9]{1,2})? ?([0-9]{1,2})?")


def validate_degrees_min_sec(func: Callable):
    async def wrapper(message: Message, state: FSMContext):
        if message.text and coordinate_pattern.fullmatch(str(message.text)):
            text = message.text.split(" ")
            if int(text[1]) > 60:
                return await message.answer("Некорректные минуты")
            if int(text[2]) > 60:
                return await message.answer("Некорректные секунды")
            return await func(message, state)
        return await message.answer("Некорректные координаты. Пример ввода: 10 0 0")

    return wrapper


def validate_operation_number(func: Callable):
    async def wrapper(message: Message, state: FSMContext):
        if message.text and message.text.isdigit() and int(message.text) <= 10:
            return await func(message, state)
        await message.answer("Некорректные данные")

    return wrapper
