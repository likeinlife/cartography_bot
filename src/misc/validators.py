import re

from aiogram.types import Message

from misc.result import Err, Ok, Result

coordinate_pattern = re.compile(r"([0-9]{1,3}) ?([0-9]{1,2})? ?([0-9]{1,2})?")


async def validate_degrees_min_sec(message: Message) -> Result[None, str]:
    if message.text and coordinate_pattern.fullmatch(str(message.text)):
        text = message.text.split(" ")
        if int(text[1]) > 60:
            msg = "Некорректные минуты"
            await message.answer(msg)
            return Err(msg)
        if int(text[2]) > 60:
            msg = "Некорректные секунды"
            await message.answer(msg)
            return Err(msg)
        return Ok(None)
    msg = "Некорректные координаты. Пример ввода: 10 0 0"
    await message.answer(msg)
    return Err(msg)


async def validate_operation_number(message: Message) -> Result[None, str]:
    if message.text and message.text.isdigit() and int(message.text) <= 10:
        return Ok(None)
    msg = "Некорректные данные"
    await message.answer(msg)
    return Err(msg)
