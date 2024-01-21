from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message

from cartography.cartography import numenclature_parse
from cartography.tg_bot.states import ByNumenclatureImages

router = Router()


@router.message(Command("by_numenclature_images"))
async def numenclature_by(message: Message, state: FSMContext):
    await message.answer("Введи нуменклатуру. Например: U-32-4-Г-а или U-32-4-(128-и)")
    await state.set_state(ByNumenclatureImages.enter_numenclature)


@router.message(ByNumenclatureImages.enter_numenclature)
@flags.chat_action("upload_document")
async def numenclature_results(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("Вы не ввели значение нуменклатуры.")
    parsed = numenclature_parse.parse_nomenclature_string(message.text)
    if parsed is None:
        return await message.answer("Некорректная нуменклатура. Посмотрите примеры в /help")

    media_group: list[InputMediaPhoto] = []
    for images in parsed.get_images():
        document = BufferedInputFile(images, "jpeg")
        media_group.append(InputMediaPhoto(media=document))
    await message.answer_media_group(media_group)  # type: ignore
    await state.clear()
