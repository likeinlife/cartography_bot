from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from domain.errors import BaseError

from .mixins import MessageInfo, MessageInfoGetterMixin


class ErrorHandlerMiddleware(BaseMiddleware, MessageInfoGetterMixin):
    def __init__(self) -> None:
        self.logger = structlog.get_logger("error_handler_middleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            error = e
        message_info = self._get_message_info(event)
        if isinstance(error, BaseError):
            await self._process_msg_error(error, event, message_info)
        else:
            await self._process_unexpected_error(error, event, message_info)

    async def _process_msg_error(self, error: BaseError, event: TelegramObject, message_info: MessageInfo):
        if not message_info.user:
            self.logger.error("No user info", error=error.msg)
            return
        self.logger.error(error.msg, username=message_info.user.username, chat_id=message_info.user.id)
        if isinstance(event, CallbackQuery | Message):
            await event.answer(error.msg)

    async def _process_unexpected_error(self, error: Exception, event: TelegramObject, message_info: MessageInfo):
        if not message_info.user:
            self.logger.error("No user info", error=error, exc_info=True)
            return
        self.logger.error(error, username=message_info.user.username, chat_id=message_info.user.id, exc_info=True)
        if isinstance(event, CallbackQuery | Message):
            await event.answer("Unexpected error")
