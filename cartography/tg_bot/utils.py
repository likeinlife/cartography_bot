import re
from typing import Callable
from aiogram.fsm.context import FSMContext

from aiogram.types import Message


def make_float_list_from_str(data: str):
    return list(map(float, data.strip(' ').split(' ')))


def validate_coordinate(func: Callable):

    async def wrapper(message: Message, state: FSMContext):
        if message.text is None:
            await message.answer('Некорректные данные')
            return
        if re.fullmatch(r'([0-9]{1,3}) ?([0-9]{1,2})? ?([0-9]{1,2})?', message.text):
            return await func(message, state)
        await message.answer('Некорректные данные')

    return wrapper
