from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from src.config import config
from src.logger_setup import get_chat_actions_logger

logger = get_chat_actions_logger(__name__)


class BanListCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id not in config.BAN_LIST:
            return await handler(event, data)


class IsAdminMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if data["event_from_user"].id == config.ADMIN_ID:
            return await handler(event, data)


class LoggingChatActions(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.info(f'{event.chat.username}({event.chat.id}) <- "{event.text}"')
        return await handler(event, data)
