from aiogram import Router
from aiogram.filters import Command, Text, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from ..keyboards import reply
from cartography.config import config

router = Router()


@router.message(or_f(Command('stop', 'стоп'), Text('стоп', ignore_case=True), Text('stop', ignore_case=True)))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        await message.answer('Остановлено')
        return await state.clear()
    await message.answer('Останавливать нечего. `стоп` используется, чтобы прекратить ввод значений')


@router.message(
    or_f(Command(commands=['hide', 'скрыть']), Text('hide', ignore_case=True), Text('скрыть', ignore_case=True)))
async def hide_keyboard(message: Message):
    await message.answer('Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())


@router.message(
    or_f(Command(commands=['show', 'показать']), Text('show', ignore_case=True), Text('показать', ignore_case=True)))
async def show_keyboard(message: Message):
    await message.answer('Клавиатура показана', reply_markup=reply.get_buttons())


@router.message(Command(commands=['start', 'старт']))
async def start(message: Message):
    await message.answer('Бот для картографии, геодезии и ТМОГИ', reply_markup=reply.get_buttons())
