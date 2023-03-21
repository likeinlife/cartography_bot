from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.chat_action import ChatActionSender

from cartography.config import config
from cartography.logger_setup import get_chat_actions_logger

logger = get_chat_actions_logger(__name__)


class BanListCheck(BaseMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        if event.from_user.id not in config.BAN_LIST:
            return await handler(event, data)


class IsAdminMiddleWare(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if data['event_from_user'].id == config.ADMIN_ID:
            return await handler(event, data)


class ChatActionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        chat_action = get_flag(data, 'chat_action')
        if not chat_action:
            return await handler(event, data)

        async with ChatActionSender(chat_id=event.chat.id, action=chat_action):
            return await handler(event, data)


class LoggingChatActions(BaseMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        handler_name = handler.__wrapped__.__self__.callback.__name__
        logger.info(f'{event.chat.username}({event.chat.id}) -> {handler_name} <- "{event.text}"')
        return await handler(event, data)
