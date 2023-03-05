from aiogram import Router
from aiogram.filters import Command, Text, or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from . import utils
from .states import ByCoordinates, GetMiddle, ByNumenclature
from cartography.cartography import find_geograph, find_numenculate, classes, re_compilated, get_middle

router = Router()


@router.message(or_f(Command('stop', 'стоп'), Text(text='стоп'), Text(text='stop')))
async def function_name(message: Message, state: FSMContext):
    await message.answer('Остановлено')
    await state.clear()


@router.message(Command("by_numenclature"))
async def numenclature_by(message: Message, state: FSMContext):
    await message.answer("Введи нуменклатуру. Например: B-29-34-А-г-1 или B-29-34-(128-и)")
    await state.set_state(ByNumenclature.enter_numenclature)


@router.message(ByNumenclature.enter_numenclature)
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
@utils.validate_coordinate
async def coordinates_enter_first(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await state.set_state(ByCoordinates.enter_second_coordinates)
    await message.reply('Введи координаты(долготу). Например: "10 20 30"')


@router.message(ByCoordinates.enter_second_coordinates)
@utils.validate_coordinate
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


@router.message(Command("get_middle"))
async def middle_get(message: Message, state: FSMContext):
    await message.answer('Напиши первую координату')
    await state.set_state(GetMiddle.enter_first_coordinates)


@router.message(GetMiddle.enter_first_coordinates)
@utils.validate_coordinate
async def middle_first_coordinate(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await message.answer('Напиши вторую координату')
    await state.set_state(GetMiddle.enter_second_coordinates)


@router.message(GetMiddle.enter_second_coordinates)
@utils.validate_coordinate
async def middle_second_coordinate(message: Message, state: FSMContext):
    await state.update_data(second=message.text)
    await message.answer('Напиши количество частей')
    await state.set_state(GetMiddle.enter_parts_number)


@router.message(GetMiddle.enter_parts_number)
async def middle_parts_coordinate(message: Message, state: FSMContext):
    data = await state.update_data(parts_number=message.text)
    await message.answer('Генерирую ответ...')
    await state.set_state(GetMiddle.enter_parts_number)
    await middle_results(message, data)


async def middle_results(message: Message, data: dict[str, str]):
    number_of_parts = int(data['parts_number'])
    first = utils.make_float_list_from_str(data['first'])
    second = utils.make_float_list_from_str(data['second'])
    coordinate_pair = (classes.Degrees(*first), classes.Degrees(*second))
    answer = get_middle.get_middle(*coordinate_pair, number_of_parts)
    await message.answer(str(answer))
