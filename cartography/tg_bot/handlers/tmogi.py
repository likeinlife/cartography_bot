from pathlib import Path

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from cartography.config import config

STATIC_PATH: Path = config.STATIC_PATH
router = Router()


@router.message(Command(commands=['laplas']), flags={'chat_action': 'upload_document'})
async def get_laplas_table(message: Message):
    laplas_photo_id = 'BQACAgIAAxkBAAICEmQLXgW7HHbqMqhWvU-x7nNbiuZUAAIiKAACLvFgSDmDMr8NT5KvLwQ'
    try:
        return await message.answer_document(laplas_photo_id)
    except TelegramBadRequest:
        print(f'There is no picture in telegram servers. Uploading one...')
    laplas_photo = FSInputFile(STATIC_PATH / 'Laplas.png', filename='laplas_table.png')
    return await message.answer_document(laplas_photo)


@router.message(Command(commands=['student']), flags={'chat_action': 'upload_document'})
async def get_student_table(message: Message):
    student_photo_id = 'BQACAgIAAxkBAAICDmQLXYpSeTmOHDwkvvCWbzLGVA85AAIVKAACLvFgSFjQMXEVeWoDLwQ'
    try:
        return await message.answer_document(student_photo_id)
    except TelegramBadRequest as e:
        print(f'There is no picture in telegram servers. Uploading one...')
    student_photo = FSInputFile(STATIC_PATH / 'Student.png')
    return await message.answer_document(student_photo)
