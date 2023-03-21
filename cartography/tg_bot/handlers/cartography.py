from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from cartography.cartography import (find_geograph, find_numenculate, get_middle, re_compilated)
from cartography.utils import classes, utils

from ..states import ByCoordinates, ByNumenclature, GetMiddle

router = Router()


@router.message(Command("by_numenclature"))
async def numenclature_by(message: Message, state: FSMContext):
    await message.answer("Введи нуменклатуру. Например: U-32-4-Г-а или U-32-4-(128-и)")
    await state.set_state(ByNumenclature.enter_numenclature)


@router.message(ByNumenclature.enter_numenclature, flags={'chat_action': 'typing'})
async def numenclature_results(message: Message, state: FSMContext):
    if not message.text or not re_compilated.re_string.match(message.text):
        await message.answer('Неверные данные. Проверьте, является ли первая буква английской')
        return

    for answer in find_geograph.find_coordinate_bounds_by_numenculature(message.text):
        await message.answer(str(answer))

    await state.clear()


@router.message(Command("by_coordinates"))
async def cordinates_by(message: Message, state: FSMContext):
    await state.set_state(ByCoordinates.enter_first_coordinates)
    await message.reply('Введи координату(широту). Например: "10 20 30"')


@router.message(ByCoordinates.enter_first_coordinates)
@utils.validate_degrees_min_sec
async def coordinates_enter_first(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await state.set_state(ByCoordinates.enter_second_coordinates)
    await message.reply('Введи координаты(долготу). Например: "10 20 30"')


@router.message(ByCoordinates.enter_second_coordinates)
@utils.validate_degrees_min_sec
async def coordinates_enter_second(message: Message, state: FSMContext):
    await state.update_data(second=message.text)
    await state.set_state(ByCoordinates.enter_operations_number)
    await message.answer('Введите количество операций. 1 - 1/1_000_000, 2 - 1/100_000, 3 - 1/50_000...')


@router.message(ByCoordinates.enter_operations_number)
async def coordinates_enter_operations_number(message: Message, state: FSMContext):
    data = await state.update_data(operations_number=message.text)
    await state.clear()
    await message.answer('Генерирую ответ...')
    await coordinates_results(message, data)


async def coordinates_results(message: Message, data: dict[str, str]):
    operations_number = int(data['operations_number'])
    first = utils.make_float_list_from_str(data['first'])
    second = utils.make_float_list_from_str(data['second'])
    coordinate_pair = classes.CoordinatePair(classes.Degrees(*first), classes.Degrees(*second))
    for answer in find_numenculate.get_numenculat_by_coordinates(coordinate_pair, operations_number):
        await message.answer(str(answer))
