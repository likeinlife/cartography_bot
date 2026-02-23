from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from domain.analytics import IAnalyticsService


class AnalyticsMiddleware(BaseMiddleware):
    def __init__(self, analytics_service: IAnalyticsService):
        self.analytics_service = analytics_service
        self.logger = structlog.get_logger("analytics_middleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message | CallbackQuery):
            return await handler(event, data)

        created_at = datetime.now(timezone.utc)
        started_at = perf_counter()
        event_info = self._extract_info(event)
        handler_name = self._get_handler_name(handler)

        try:
            result = await handler(event, data)
        except Exception as error:
            duration_ms = int((perf_counter() - started_at) * 1000)
            await self._safe_collect_error(
                update_type=event_info["update_type"],
                command_name=event_info["command_name"],
                callback_data=event_info["callback_data"],
                handler_name=handler_name,
                duration_ms=duration_ms,
                user_id=event_info["user_id"],
                username=event_info["username"],
                chat_id=event_info["chat_id"],
                error=error,
                created_at=created_at,
            )
            raise

        duration_ms = int((perf_counter() - started_at) * 1000)
        await self._safe_collect_success(
            update_type=event_info["update_type"],
            command_name=event_info["command_name"],
            callback_data=event_info["callback_data"],
            handler_name=handler_name,
            duration_ms=duration_ms,
            user_id=event_info["user_id"],
            username=event_info["username"],
            chat_id=event_info["chat_id"],
            created_at=created_at,
        )
        return result

    async def _safe_collect_success(
        self,
        *,
        update_type: str,
        command_name: str | None,
        callback_data: str | None,
        handler_name: str | None,
        duration_ms: int,
        user_id: int | None,
        username: str | None,
        chat_id: int | None,
        created_at: datetime,
    ) -> None:
        try:
            await self.analytics_service.collect_success(
                update_type=update_type,
                command_name=command_name,
                callback_data=callback_data,
                handler_name=handler_name,
                duration_ms=duration_ms,
                user_id=user_id,
                username=username,
                chat_id=chat_id,
                created_at=created_at,
            )
        except Exception:
            self.logger.error("Analytics save failed on success event", exc_info=True)

    async def _safe_collect_error(
        self,
        *,
        update_type: str,
        command_name: str | None,
        callback_data: str | None,
        handler_name: str | None,
        duration_ms: int,
        user_id: int | None,
        username: str | None,
        chat_id: int | None,
        error: Exception,
        created_at: datetime,
    ) -> None:
        try:
            await self.analytics_service.collect_error(
                update_type=update_type,
                command_name=command_name,
                callback_data=callback_data,
                handler_name=handler_name,
                duration_ms=duration_ms,
                user_id=user_id,
                username=username,
                chat_id=chat_id,
                error=error,
                created_at=created_at,
            )
        except Exception:
            self.logger.error("Analytics save failed on error event", exc_info=True)

    @staticmethod
    def _extract_info(event: Message | CallbackQuery) -> dict[str, str | int | None]:
        if isinstance(event, Message):
            return {
                "update_type": "message",
                "command_name": _extract_command_name(event.text),
                "callback_data": None,
                "user_id": event.from_user.id if event.from_user else None,
                "username": event.from_user.username if event.from_user else None,
                "chat_id": event.chat.id if event.chat else None,
            }
        return {
            "update_type": "callback_query",
            "command_name": None,
            "callback_data": event.data,
            "user_id": event.from_user.id if event.from_user else None,
            "username": event.from_user.username if event.from_user else None,
            "chat_id": event.message.chat.id if event.message and event.message.chat else None,
        }

    @staticmethod
    def _get_handler_name(handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]) -> str | None:
        if hasattr(handler, "__qualname__"):
            return handler.__qualname__
        if hasattr(handler, "__name__"):
            return handler.__name__
        return handler.__class__.__name__


def _extract_command_name(text: str | None) -> str | None:
    if not text:
        return None
    first_token = text.strip().split(maxsplit=1)[0]
    if not first_token.startswith("/"):
        return None
    command = first_token[1:].split("@", maxsplit=1)[0]
    return command or None
