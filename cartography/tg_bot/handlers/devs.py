from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.document)
async def get_document_id(message: Message):
    print(message.document.file_id)