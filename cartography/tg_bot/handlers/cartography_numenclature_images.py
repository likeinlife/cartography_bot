from itertools import islice

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message

from cartography.cartography.get_scale_class import get_scale
from cartography.tg_bot.states import ByCoordinatesImages
from cartography.utils import classes, utils

router = Router()


@router.message(Command("by_coordinates_images"))
async def images_numenclature_by_coordinates(message: Message, state: FSMContext):
    await state.set_state(ByCoordinatesImages.enter_first_coordinates)
    await message.reply('Введи координату(широту). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_first_coordinates)
@utils.validate_degrees_min_sec
async def coordinates_enter_first(message: Message, state: FSMContext):
    await state.update_data(first=message.text)
    await state.set_state(ByCoordinatesImages.enter_second_coordinates)
    await message.reply('Введи координаты(долготу). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_second_coordinates)
@utils.validate_degrees_min_sec
async def coordinates_enter_second(message: Message, state: FSMContext):
    await state.update_data(second=message.text)
    await state.set_state(ByCoordinatesImages.enter_operations_number)
    await message.answer("Введите количество операций. /help -> Масштабы")


@router.message(
    ByCoordinatesImages.enter_operations_number,
    flags={"chat_action": "upload_document"},
)
@utils.validate_operation_number
async def coordinates_enter_operations_number(message: Message, state: FSMContext):
    data = await state.update_data(operations_number=message.text)
    await state.clear()
    await message.answer("Генерирую ответ...")
    await send_numenclature_photo_by_coordinates(message, data)


async def send_numenclature_photo_by_coordinates(message: Message, data: dict[str, str]):
    operations_number = int(data["operations_number"])
    first = utils.make_float_list_from_str(data["first"])
    second = utils.make_float_list_from_str(data["second"])
    coordinate_pair = classes.CoordinatePair(classes.Degrees(*first), classes.Degrees(*second))
    media_group: list[InputMediaPhoto] = []

    def divide_to_chunks(arr_range, arr_size):
        arr_range = iter(arr_range)
        return iter(lambda: tuple(islice(arr_range, arr_size)), ())

    for answer in get_scale(operations_number)(coordinate_pair).get_images():
        document = BufferedInputFile(answer, "jpeg")
        media_group.append(InputMediaPhoto(media=document))
    for chunk in divide_to_chunks(media_group, 10):
        await message.answer_media_group(chunk)
