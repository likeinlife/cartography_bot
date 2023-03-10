from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.document)
async def function_name(message: Message):
    print(message.document.file_id)