from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message
from container import AppContainer
from dependency_injector.wiring import Provide, inject
from domain.facades import INomenclatureFacade

from tg_bot.enums import CartographyCommandsEnum
from tg_bot.states import ByNomenclatureTitle

router = Router()


@router.message(Command(CartographyCommandsEnum.BY_NOMENCLATURE_TITLE))
async def by_nomenclature_title_handler(message: Message, state: FSMContext):
    await message.answer("Введи номенклатуру. Например: U-32-4-Г-а или U-32-4-(128)-(и)")
    await state.set_state(ByNomenclatureTitle.enter_nomenclature)


@router.message(ByNomenclatureTitle.enter_nomenclature)
@flags.chat_action("upload_document")
@inject
async def nomenclature_title_handler(
    message: Message,
    state: FSMContext,
    nomenclature_facade: INomenclatureFacade = Provide[AppContainer.nomenclature_facade],
):
    if not message.text:
        return await message.answer("Вы не ввели значение номенклатуры.")

    images = nomenclature_facade.generate_from_nomenclature(message.text)

    media_group = [InputMediaPhoto(media=BufferedInputFile(image, "jpeg")) for image in images]

    await message.answer_media_group(media_group)  # type: ignore
    await state.clear()
