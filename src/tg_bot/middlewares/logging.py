from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LogCommandsMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = structlog.get_logger("logger_middleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        self.logger.info(event.text, username=event.chat.username, chat_id=event.chat.id)  # type: ignore
        return await handler(event, data)
