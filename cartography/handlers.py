from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .cartography import find_geograph

router = Router()


class States(StatesGroup):
    enter_numenclature = State()
    enter_first_coordinates = State()
    enter_second_coordinates = State()


@router.message(Command("by_numenclature"))
async def by_numenculature(message: Message, state: FSMContext):
    await message.answer("Введи нуменклатуру. Например: B-29-34-А-г-1 или B-29-34-(128-и)")
    await state.set_state(States.enter_numenclature)


@router.message(States.enter_numenclature)
async def coordinates_by_numenclature(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('No numenclature')
        return

    for answer in find_geograph.find_coordinate_bounds_by_numenculature(message.text):
        await message.answer(str(answer))

    await state.clear()


@router.message(Command("by_coordinates"))
async def by_coordinates(message: Message):
    await message.answer("1")


@router.message(Command("get_middle"))
async def get_middle(message: Message):
    await message.answer("1")
