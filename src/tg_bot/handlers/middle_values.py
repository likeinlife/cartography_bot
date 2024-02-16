import misc
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from business.math_actions import coordinate_actions
from misc import decorators

from src.tg_bot.states import GetMiddle

router = Router()


class Data:
    first = "first"
    second = "second"
    part_number = "part_number"


@router.message(Command("get_middle"))
async def middle_get_handler(message: Message, state: FSMContext):
    await message.answer("Напиши первую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_first_coordinates)


@router.message(GetMiddle.enter_first_coordinates)
@decorators.validate_degrees_min_sec
async def middle_first_coordinate_handler(message: Message, state: FSMContext):
    await state.update_data({Data.first: message.text})
    await message.answer("Напиши вторую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_second_coordinates)


@router.message(GetMiddle.enter_second_coordinates)
@decorators.validate_degrees_min_sec
async def middle_second_coordinate_handler(message: Message, state: FSMContext):
    await state.update_data({Data.second: message.text})
    await message.answer("Напиши количество частей")
    await state.set_state(GetMiddle.enter_parts_number)


@router.message(GetMiddle.enter_parts_number)
async def middle_parts_coordinate_handler(message: Message, state: FSMContext):
    if message.text and message.text.isnumeric():
        parts = int(message.text)
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
    answer = coordinate_actions.get_middle_list(first, second, part_number)
    answer_text = "\n".join([coordinate_actions.to_str(i) for i in answer])
    await message.answer(answer_text)
