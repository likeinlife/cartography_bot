from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from cartography.cartography import find_numenclature_images

from cartography.utils import utils, classes
from cartography.tg_bot.states import ByCoordinatesImages

router = Router()


@router.message(Command("by_coordinates_images"))
async def cordinates_by(message: Message, state: FSMContext):
    await state.set_state(ByCoordinatesImages.enter_first_coordinates)
    await message.reply('Введи координату(широту). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_first_coordinates)
@utils.validate_coordinate
async def coordinates_enter_first(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await state.set_state(ByCoordinatesImages.enter_second_coordinates)
    await message.reply('Введи координаты(долготу). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_second_coordinates)
@utils.validate_coordinate
async def coordinates_enter_second(message: Message, state: FSMContext):
    await state.update_data(second=message.text)
    await state.set_state(ByCoordinatesImages.enter_operations_number)
    await message.answer('Введите количество операций. 1 - 1/1_000_000, 2 - 1/100_000, 3 - 1/50_000...')


@router.message(ByCoordinatesImages.enter_operations_number, flags={'chat_action': 'upload_document'})
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
    for answer in find_numenclature_images.get_numenculat_yield_images(coordinate_pair, operations_number):
        document = BufferedInputFile(answer, 'jpeg')
        await message.answer_photo(document)