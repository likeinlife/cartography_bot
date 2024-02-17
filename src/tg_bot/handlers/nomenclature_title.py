from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message
from cartography.facades.nomenclature_facade import NomenclatureFacade

from tg_bot.enums import CartographyCommandsEnum
from tg_bot.states import ByNomenclatureTitle

router = Router()


@router.message(Command(CartographyCommandsEnum.BY_NOMENCLATURE_TITLE))
async def by_nomenclature_title_handler(message: Message, state: FSMContext):
    await message.answer("Введи номенклатуру. Например: U-32-4-Г-а или U-32-4-(128-и)")
    await state.set_state(ByNomenclatureTitle.enter_nomenclature)


@router.message(ByNomenclatureTitle.enter_nomenclature)
@flags.chat_action("upload_document")
async def nomenclature_title_handler(
    message: Message,
    state: FSMContext,
):
    if not message.text:
        return await message.answer("Вы не ввели значение номенклатуры.")

    images = NomenclatureFacade.generate_from_nomenclature(message.text)

    media_group: list[InputMediaPhoto] = []
    for image in images:
        document = BufferedInputFile(image, "jpeg")
        media_group.append(InputMediaPhoto(media=document))

    await message.answer_media_group(media_group)  # type: ignore
    await state.clear()
