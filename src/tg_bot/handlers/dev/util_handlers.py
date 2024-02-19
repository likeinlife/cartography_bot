from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot import strings
from tg_bot.enums import UtilCommandsEnum
from tg_bot.keyboards import reply

router = Router()


@router.message(Command(commands=[UtilCommandsEnum.START, "start", "старт"]))
async def start(message: Message):
    await message.answer(
        strings.GREETING_MESSAGE,
        reply_markup=reply.get_reply_showButtons(),
    )


@router.message(Command(commands=[UtilCommandsEnum.STOP, "stop", "стоп"]))
@router.message(F.text.lower().in_(["stop", "стоп"]))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        await message.answer(strings.STOP_SUCCESS)
        return await state.clear()
    await message.answer(strings.STOP_ERROR)
