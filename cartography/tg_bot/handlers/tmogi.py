from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from cartography.config import config

STATIC_PATH: Path = config.static_path
router = Router()


@router.message(Command(commands=['laplas']))
async def get_laplas_table(message: Message):
    laplas_photo = FSInputFile(STATIC_PATH / 'Laplas.png', filename='laplas_table.png')
    await message.answer_document(laplas_photo)


@router.message(Command(commands=['student']))
async def get_student_table(message: Message):
    student_photo = FSInputFile(STATIC_PATH / 'Student.png')
    await message.answer_document(student_photo)