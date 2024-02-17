from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from tg_bot.enums import UtilCommandsEnum
from tg_bot.keyboards import reply

router = Router()


@router.message(Command(commands=[UtilCommandsEnum.START, "start", "старт"]))
async def start(message: Message):
    await message.answer(
        "Бот для картографии, геодезии и ТМОГИ",
        reply_markup=reply.get_reply_showButtons(),
    )


@router.message(Command(commands=[UtilCommandsEnum.STOP, "stop", "стоп"]))
@router.message(F.text.lower().in_(["stop", "стоп"]))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        await message.answer("Остановлено")
        return await state.clear()
    await message.answer("Останавливать нечего. `стоп` используется, чтобы прекратить ввод значений")


@router.message(Command(commands=[UtilCommandsEnum.HIDE_KEYBOARD, "hide", "скрыть"]))
@router.message(F.text.lower().in_(["hide", "скрыть"]))
async def hide_keyboard(message: Message):
    await message.answer("Клавиатура скрыта", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=[UtilCommandsEnum.SHOW_KEYBOARD, "show", "показать"]))
@router.message(F.text == "show")
@router.message(F.text.lower().in_(["show", "показать"]))
async def show_keyboard(message: Message):
    await message.answer("Клавиатура показана", reply_markup=reply.get_reply_showButtons())
