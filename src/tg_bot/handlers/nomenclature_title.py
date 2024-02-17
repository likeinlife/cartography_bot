import errors
from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message
from cartography.facades import NomenclatureFacade
from tg_bot.states import ByNomenclatureImages

router = Router()


@router.message(Command("by_nomenclature_images"))
async def enter_nomenclature_handler(message: Message, state: FSMContext):
    await message.answer("Введи номенклатуру. Например: U-32-4-Г-а или U-32-4-(128-и)")
    await state.set_state(ByNomenclatureImages.enter_nomenclature)


@router.message(ByNomenclatureImages.enter_nomenclature)
@flags.chat_action("upload_document")
async def handle_nomenclature(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("Вы не ввели значение номенклатуры.")
    try:
        images = NomenclatureFacade.generate_from_nomenclature(message.text)
    except errors.InvalidNomenclatureTitleError:
        return await message.answer("Некорректная номенклатура. Посмотрите примеры в /help")

    media_group: list[InputMediaPhoto] = []
    for image in images:
        document = BufferedInputFile(image, "jpeg")
        media_group.append(InputMediaPhoto(media=document))

    await message.answer_media_group(media_group)  # type: ignore
    await state.clear()
