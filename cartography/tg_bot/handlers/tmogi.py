from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from cartography.config import config

router = Router()


@router.message(Command(commands=['laplas']), flags={'chat_action': 'upload_document'})
async def get_laplas_table(message: Message):
    laplas_photo = FSInputFile(config.STATIC_PATH / 'Laplas.png', filename='laplas_table.png')
    return await message.answer_document(laplas_photo)


@router.message(Command(commands=['student']), flags={'chat_action': 'upload_document'})
async def get_student_table(message: Message):
    student_photo = FSInputFile(config.STATIC_PATH / 'Student.png')
    return await message.answer_document(student_photo)
