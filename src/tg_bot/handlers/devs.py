from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.document)
async def get_document_id(message: Message):
    if message.document:
        return await message.answer(text=str(message.document.file_id))
    return await message.answer(text="No document")
