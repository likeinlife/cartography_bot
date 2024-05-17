from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from .mixins import MessageInfoGetterMixin


class LogCommandsMiddleware(BaseMiddleware, MessageInfoGetterMixin):
    def __init__(self) -> None:
        self.logger = structlog.get_logger("logger_middleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        message_info = self._get_message_info(event)
        if message_info.user is None:
            return await handler(event, data)
        self.logger.info(message_info.text, username=message_info.user.username, chat_id=message_info.user.id)
        return await handler(event, data)
