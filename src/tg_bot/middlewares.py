from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from container import AppContainer
from dependency_injector.wiring import Provide, inject
from errors import BaseMsgError

logger = structlog.get_logger()


class IsAdminMiddleWare(BaseMiddleware):
    @staticmethod
    @inject
    def _is_admin(
        user_id: int,
        admin_id: int = Provide[AppContainer.settings.admin_id],
    ) -> bool:
        if user_id == admin_id:
            return True
        return False

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if self._is_admin(event.chat.id):  # type: ignore
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


class ErrorHandlerMiddleware(BaseMiddleware):
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
                logger.error(e.msg, username=event.from_user.username, chat_id=event.from_user.id)
                await event.answer(e.msg)
            if isinstance(event, Message):
                logger.error(e.msg, username=event.chat.username, chat_id=event.chat.id)
                await event.answer(e.msg)
        except Exception as e:
            if isinstance(event, CallbackQuery):
                logger.error(e, username=event.from_user.username, chat_id=event.from_user.id, exc_info=True)
                await event.answer("Unexpected error")
            if isinstance(event, Message):
                logger.error(e, username=event.chat.username, chat_id=event.chat.id, exc_info=True)
                await event.answer("Unexpected error")
