from enum import StrEnum, auto

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from geodesy.micrometer import calculate_micrometer
from geodesy.models import MicrometerInput
from tg_bot.enums import GeodesyCommandsEnum
from tg_bot.states import MicrometerState

router = Router()


class MicrometerData(StrEnum):
    first = auto()
    second = auto()


@router.message(Command(commands=GeodesyCommandsEnum.CALCULATE_MICROMETER))
async def calculate_micrometer_handler(message: Message, state: FSMContext):
    await state.set_state(MicrometerState.first_column)
    await message.answer("Введите первый столбец(КЛ и КП) через пробел")


@router.message(MicrometerState.first_column)
async def enter_first_column_handler(message: Message, state: FSMContext):
    await state.update_data({MicrometerData.first: message.text})
    await state.set_state(MicrometerState.second_column)
    await message.answer("Введите второй столбец(КЛ и КП) через пробел")


@router.message(MicrometerState.second_column)
async def enter_second_column_handler(message: Message, state: FSMContext):
    data = await state.update_data({MicrometerData.second: message.text})
    answer = handle_micrometer_data(data)
    await message.answer(text=answer.to_str())


def handle_micrometer_data(data: dict):
    first = MicrometerInput.from_str(data[MicrometerData.first])
    second = MicrometerInput.from_str(data[MicrometerData.second])
    return calculate_micrometer(first=first, second=second)
