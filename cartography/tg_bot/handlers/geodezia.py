from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from cartography import geodezia
from ..states import GeodeziaMocrometr

router = Router()


@router.message(Command(commands=['micro']))
async def calculate_micrometr(message: Message, state: FSMContext):
    await state.set_state(GeodeziaMocrometr.first_stolb)
    await message.answer('Введите первый столбец(КЛ и КП) через пробел')


@router.message(GeodeziaMocrometr.first_stolb)
async def enter_first_stolb(message: Message, state: FSMContext):
    await state.update_data(first_stolb=message.text)
    await state.set_state(GeodeziaMocrometr.second_stolb)
    await message.answer('Введите второй столбец(КЛ и КП) через пробел')


@router.message(GeodeziaMocrometr.second_stolb)
async def enter_second_stolb(message: Message, state: FSMContext):
    data = await state.update_data(second_stolb=message.text)
    answer = call_calculate_micrometr_func(data)
    for values in answer:
        await message.answer(round(values, 1))


def call_calculate_micrometr_func(data: dict):
    first_stolb = tuple(map(float, data['first_stolb'].split(' ')))
    second_stolb = tuple(map(float, (data['second_stolb'].split(' '))))
    return geodezia.micrometr_actions(first_stolb, second_stolb)
