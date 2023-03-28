from aiogram import Router
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from ..keyboards import reply, inline

router = Router()


@router.message(Command(commands=['start', 'старт']))
async def start(message: Message):
    await message.answer('Бот для картографии, геодезии и ТМОГИ', reply_markup=reply.get_reply_showButtons())


@router.message(Command('stop', 'стоп'))
@router.message(or_f(Text('стоп', ignore_case=True), Text('stop', ignore_case=True)))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        await message.answer('Остановлено')
        return await state.clear()
    await message.answer('Останавливать нечего. `стоп` используется, чтобы прекратить ввод значений')


@router.message(Command(commands=['hide', 'скрыть']))
@router.message(or_f(Text('hide', ignore_case=True), Text('скрыть', ignore_case=True)))
async def hide_keyboard(message: Message):
    await message.answer('Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=['show', 'показать']))
@router.message(or_f(Text('show', ignore_case=True), Text('показать', ignore_case=True)))
async def show_keyboard(message: Message):
    await message.answer('Клавиатура показана', reply_markup=reply.get_reply_showButtons())
