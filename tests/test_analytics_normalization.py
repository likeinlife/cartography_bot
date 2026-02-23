from datetime import datetime, timezone

from logic.analytics.service import AnalyticsService
from tg_bot.middlewares.analytics import _extract_command_name


class _RepoStub:
    def __init__(self) -> None:
        self.saved = []

    async def save_event(self, event) -> None:
        self.saved.append(event)


def test_extract_command_name() -> None:
    assert _extract_command_name("/start") == "start"
    assert _extract_command_name("/start@my_bot foo") == "start"
    assert _extract_command_name("hello") is None
    assert _extract_command_name(None) is None


def test_analytics_service_truncates_data() -> None:
    repo = _RepoStub()
    service = AnalyticsService(analytics_repository=repo, source="tg_bot")

    async def _run() -> None:
        await service.collect_error(
            update_type="message",
            command_name="/start",
            callback_data="x" * 400,
            handler_name="h" * 400,
            duration_ms=50,
            user_id=1,
            username="u" * 400,
            chat_id=2,
            error=RuntimeError("e" * 2000),
            created_at=datetime.now(timezone.utc),
        )

    import asyncio

    asyncio.run(_run())

    assert len(repo.saved) == 1
    saved = repo.saved[0]
    assert len(saved.callback_data) == 256
    assert len(saved.handler_name) == 255
    assert len(saved.username) == 255
    assert len(saved.error_message) == 1024
