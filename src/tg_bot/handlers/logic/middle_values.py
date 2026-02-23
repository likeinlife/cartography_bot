from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import misc
from misc import validators
from src.misc.result import Err
from tg_bot.enums.commands import CartographyCommandsEnum
from tg_bot.states import GetMiddle

router = Router()


class Data:
    first = "first"
    second = "second"
    part_number = "part_number"


@router.message(Command(CartographyCommandsEnum.GET_MIDDLE))
async def middle_get_handler(message: Message, state: FSMContext):
    await message.answer("Напиши первую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_first_coordinates)


@router.message(GetMiddle.enter_first_coordinates)
async def middle_first_coordinate_handler(message: Message, state: FSMContext):
    match await validators.validate_degrees_min_sec(message):
        case Err(_):
            return
    await state.update_data({Data.first: message.text})
    await message.answer("Напиши вторую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_second_coordinates)


@router.message(GetMiddle.enter_second_coordinates)
async def middle_second_coordinate_handler(message: Message, state: FSMContext):
    match await validators.validate_degrees_min_sec(message):
        case Err(_):
            return
    await state.update_data({Data.second: message.text})
    await message.answer("Напиши количество частей")
    await state.set_state(GetMiddle.enter_parts_number)


@router.message(GetMiddle.enter_parts_number)
async def middle_parts_coordinate_handler(message: Message, state: FSMContext):
    if message.text and message.text.isnumeric():
        parts = int(message.text)
    else:
        await message.answer("Некорректный ввод. Ожидается целое число до 50.")
        return
    if parts > 50:
        return await message.answer(
            "Вы ввели слишком большое количество частей. Вряд ли оно вам надо.\nВведите другое число"
        )
    data = await state.update_data({Data.part_number: message.text})

    await message.answer("Генерирую ответ...")
    await state.set_state(GetMiddle.enter_parts_number)
    await handle_middle(message, data)


async def handle_middle(message: Message, data: dict[str, str]):
    part_number = int(data[Data.part_number])
    first = misc.generate_coordinate_from_string(data[Data.first])
    second = misc.generate_coordinate_from_string(data[Data.second])
    answer = first.actions.get_middle_list(second, part_number)
    answer_text = "\n".join([i.to_str() for i in answer])
    await message.answer(answer_text)
