from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.cartography import get_middle
from src.tg_bot.states import GetMiddle
from src.utils import classes, utils

router = Router()


@router.message(Command("get_middle"))
async def middle_get(message: Message, state: FSMContext):
    await message.answer("Напиши первую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_first_coordinates)


@router.message(GetMiddle.enter_first_coordinates)
@utils.validate_degrees_min_sec
async def middle_first_coordinate(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await message.answer("Напиши вторую координату (градусы, мин, сек)")
    await state.set_state(GetMiddle.enter_second_coordinates)


@router.message(GetMiddle.enter_second_coordinates)
@utils.validate_degrees_min_sec
async def middle_second_coordinate(message: Message, state: FSMContext):
    await state.update_data(second=message.text)
    await message.answer("Напиши количество частей")
    await state.set_state(GetMiddle.enter_parts_number)


@router.message(GetMiddle.enter_parts_number)
async def middle_parts_coordinate(message: Message, state: FSMContext):
    if message.text and message.text.isnumeric():
        parts = int(message.text)
    if parts > 50:
        return await message.answer(
            "Вы ввели слишком большое количество частей. Вряд ли оно вам надо.\nВведите другое число"
        )
    data = await state.update_data(parts_number=parts)
    await message.answer("Генерирую ответ...")
    await state.set_state(GetMiddle.enter_parts_number)
    await middle_results(message, data)


async def middle_results(message: Message, data: dict[str, str]):
    number_of_parts = int(data["parts_number"])
    first = utils.make_float_list_from_str(data["first"])
    second = utils.make_float_list_from_str(data["second"])
    coordinate_pair = (classes.Degrees(*first), classes.Degrees(*second))
    answer = get_middle.get_middle(*coordinate_pair, number_of_parts)
    await message.answer(str(answer))
