from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from micrometr.horizontal_angles import calculate_micrometer
from tg_bot.enums import GeodesyCommandsEnum
from tg_bot.states import MicrometerState

router = Router()


@router.message(Command(commands=GeodesyCommandsEnum.CALCULATE_MICROMETER))
async def calculate_micrometer_handler(message: Message, state: FSMContext):
    await state.set_state(MicrometerState.first_column)
    await message.answer("Введите первый столбец(КЛ и КП) через пробел")


@router.message(MicrometerState.first_column)
async def enter_first_column_handler(message: Message, state: FSMContext):
    await state.update_data(first_column=message.text)
    await state.set_state(MicrometerState.second_column)
    await message.answer("Введите второй столбец(КЛ и КП) через пробел")


@router.message(MicrometerState.second_column)
async def enter_second_column_handler(message: Message, state: FSMContext):
    data = await state.update_data(second_column=message.text)
    answer = handle_micrometer_data(data)
    for value in answer:
        await message.answer(text=str(round(value, 1)))


def handle_micrometer_data(data: dict):
    first_column = tuple(map(float, data["first_column"].split(" ")))
    second_column = tuple(map(float, (data["second_column"].split(" "))))
    return calculate_micrometer(first_value=first_column, second_value=second_column)
