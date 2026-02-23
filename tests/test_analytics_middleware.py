import asyncio
from datetime import datetime, timezone

from aiogram.types import CallbackQuery, Message

from tg_bot.middlewares.analytics import AnalyticsMiddleware


def _build_message(text: str = "/start") -> Message:
    return Message.model_validate(
        {
            "message_id": 1,
            "date": datetime.now(timezone.utc).isoformat(),
            "chat": {"id": 10, "type": "private"},
            "from": {"id": 20, "is_bot": False, "first_name": "Test", "username": "tester"},
            "text": text,
        }
    )


def _build_callback() -> CallbackQuery:
    return CallbackQuery.model_validate(
        {
            "id": "cb-id",
            "from": {"id": 20, "is_bot": False, "first_name": "Test", "username": "tester"},
            "chat_instance": "chat-instance",
            "data": "help_menu",
            "message": {
                "message_id": 2,
                "date": datetime.now(timezone.utc).isoformat(),
                "chat": {"id": 10, "type": "private"},
                "text": "menu",
            },
        }
    )


class _ServiceStub:
    def __init__(self) -> None:
        self.success_calls = []
        self.error_calls = []

    async def collect_success(self, **kwargs) -> None:
        self.success_calls.append(kwargs)

    async def collect_error(self, **kwargs) -> None:
        self.error_calls.append(kwargs)


class _FailingService:
    async def collect_success(self, **kwargs) -> None:
        raise RuntimeError("db down")

    async def collect_error(self, **kwargs) -> None:
        raise RuntimeError("db down")


def test_collect_success_for_message() -> None:
    service = _ServiceStub()
    middleware = AnalyticsMiddleware(service)
    event = _build_message("/start hello")

    async def _handler(ev, data):
        return "ok"

    result = asyncio.run(middleware(_handler, event, {}))

    assert result == "ok"
    assert len(service.success_calls) == 1
    call = service.success_calls[0]
    assert call["update_type"] == "message"
    assert call["command_name"] == "start"
    assert call["callback_data"] is None
    assert call["user_id"] == 20
    assert call["chat_id"] == 10


def test_collect_error_for_callback() -> None:
    service = _ServiceStub()
    middleware = AnalyticsMiddleware(service)
    event = _build_callback()

    async def _handler(ev, data):
        raise ValueError("boom")

    try:
        asyncio.run(middleware(_handler, event, {}))
    except ValueError as error:
        assert str(error) == "boom"

    assert len(service.error_calls) == 1
    call = service.error_calls[0]
    assert call["update_type"] == "callback_query"
    assert call["command_name"] is None
    assert call["callback_data"] == "help_menu"
    assert call["user_id"] == 20
    assert call["chat_id"] == 10


def test_analytics_failure_does_not_break_handler() -> None:
    middleware = AnalyticsMiddleware(_FailingService())
    event = _build_message("/start")

    async def _handler(ev, data):
        return "ok"

    result = asyncio.run(middleware(_handler, event, {}))
    assert result == "ok"
