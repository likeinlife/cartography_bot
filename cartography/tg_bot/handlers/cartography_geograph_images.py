from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from cartography.cartography import find_geograph_images, re_compilated

from cartography.tg_bot.states import ByNumenclatureImages

router = Router()


@router.message(Command("by_numenclature_images"))
async def numenclature_by(message: Message, state: FSMContext):
    await message.answer("Введи нуменклатуру. Например: U-32-4-Г-а или U-32-4-(128-и)")
    await state.set_state(ByNumenclatureImages.enter_numenclature)


@router.message(ByNumenclatureImages.enter_numenclature, flags={'chat_action': 'typing'})
async def numenclature_results(message: Message, state: FSMContext):
    if not message.text or not re_compilated.re_string.match(message.text):
        await message.answer('Неверные данные. Проверьте, является ли первая буква английской')
        return

    for answer in find_geograph_images.find_coordinate_bounds_by_numenculature(message.text):
        document = BufferedInputFile(answer, 'jpeg')
        await message.answer_photo(document)

    await state.clear()