from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = structlog.get_logger()


class LogCommandsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.info(event.text, username=event.chat.username, chat_id=event.chat.id)  # type: ignore
        return await handler(event, data)
