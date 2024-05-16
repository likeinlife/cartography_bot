from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from errors import BaseMsgError


class ErrorHandlerMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = structlog.get_logger("error_handler_middleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await handler(event, data)
        except BaseMsgError as e:
            if isinstance(event, CallbackQuery):
                self.logger.error(e.msg, username=event.from_user.username, chat_id=event.from_user.id)
                await event.answer(e.msg)
            if isinstance(event, Message):
                self.logger.error(e.msg, username=event.chat.username, chat_id=event.chat.id)
                await event.answer(e.msg)
        except Exception as e:
            if isinstance(event, CallbackQuery):
                self.logger.error(e, username=event.from_user.username, chat_id=event.from_user.id, exc_info=True)
                await event.answer("Unexpected error")
            if isinstance(event, Message):
                self.logger.error(e, username=event.chat.username, chat_id=event.chat.id, exc_info=True)
                await event.answer("Unexpected error")
