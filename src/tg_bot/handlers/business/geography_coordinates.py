from enum import StrEnum, auto
from itertools import islice

import misc
from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message
from cartography.models import CoordinatePair
from container import AppContainer
from dependency_injector.wiring import Provide, inject
from domain.facades import INomenclatureFacade
from misc import decorators

from tg_bot.enums import CartographyCommandsEnum
from tg_bot.states import ByCoordinatesImages

router = Router()


class Data(StrEnum):
    longitude = auto()
    latitude = auto()
    scale_number = auto()


@router.message(Command(CartographyCommandsEnum.BY_COORDINATE))
async def by_coordinates_handler(message: Message, state: FSMContext):
    await state.set_state(ByCoordinatesImages.enter_first_coordinates)
    await message.reply('Введи координату(широту). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_first_coordinates)
@decorators.validate_degrees_min_sec
async def enter_latitude_handler(message: Message, state: FSMContext):
    await state.update_data({Data.latitude: message.text})

    await state.set_state(ByCoordinatesImages.enter_second_coordinates)
    await message.reply('Введи координаты(долготу). Например: "10 20 30"')


@router.message(ByCoordinatesImages.enter_second_coordinates)
@decorators.validate_degrees_min_sec
async def enter_longitude_handler(message: Message, state: FSMContext):
    await state.update_data({Data.longitude: message.text})

    await state.set_state(ByCoordinatesImages.enter_operations_number)
    await message.answer("Введите количество операций. /help -> Масштабы")


@router.message(ByCoordinatesImages.enter_operations_number)
@flags.chat_action("upload_document")
@decorators.validate_operation_number
async def enter_scale_number_handler(message: Message, state: FSMContext):
    data = await state.update_data({Data.scale_number: message.text})

    await state.clear()
    await message.answer("Генерирую ответ...")
    await handle_nomenclature_handler(message, data)


@inject
async def handle_nomenclature_handler(
    message: Message,
    data: dict[str, str],
    nomenclature_facade: INomenclatureFacade = Provide[AppContainer.nomenclature_facade],
):
    def _divide_to_chunks(arr_range, arr_size):
        arr_range = iter(arr_range)
        return iter(lambda: tuple(islice(arr_range, arr_size)), ())

    scale_number = int(data[Data.scale_number])
    latitude = misc.generate_coordinate_from_string(data[Data.latitude])
    longitude = misc.generate_coordinate_from_string(data[Data.longitude])
    coordinate_pair = CoordinatePair(latitude=latitude, longitude=longitude)

    images = nomenclature_facade.generate_from_coordinates(coordinate_pair, scale_number)

    media_group: list[InputMediaPhoto] = []

    for answer in images:
        document = BufferedInputFile(answer, "jpeg")
        media_group.append(InputMediaPhoto(media=document))
    for chunk in _divide_to_chunks(media_group, 10):
        await message.answer_media_group(chunk)  # type: ignore
