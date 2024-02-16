from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from container import AppContainer
from dependency_injector.wiring import Provide, inject

logger = structlog.get_logger()


class IsAdminMiddleWare(BaseMiddleware):
    @inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        admin_id: int = Provide[AppContainer.settings.admin_id],
    ) -> Any:
        if data["event_from_user"].id == admin_id:
            return await handler(event, data)


class LoggingChatActions(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.info(event.text, username=event.chat.username, chat_id=event.chat.id)  # type: ignore
        return await handler(event, data)
