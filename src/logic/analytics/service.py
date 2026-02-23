from datetime import datetime, timezone

from domain.analytics.service import IAnalyticsService
from domain.analytics.models import AnalyticsEventCreate
from domain.analytics.repository import IAnalyticsRepository


class AnalyticsService(IAnalyticsService):
    def __init__(self, analytics_repository: IAnalyticsRepository, source: str):
        self.analytics_repository = analytics_repository
        self.source = source

    async def collect_success(
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
        await self.analytics_repository.save_event(
            AnalyticsEventCreate(
                source=self.source,
                update_type=update_type,
                status="success",
                command_name=self._normalize(command_name, 128),
                callback_data=self._normalize(callback_data, 256),
                handler_name=self._normalize(handler_name, 255),
                duration_ms=duration_ms,
                user_id=user_id,
                username=self._normalize(username, 255),
                chat_id=chat_id,
                error_type=None,
                error_message=None,
                created_at=created_at.astimezone(timezone.utc),
            )
        )

    async def collect_error(
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
        await self.analytics_repository.save_event(
            AnalyticsEventCreate(
                source=self.source,
                update_type=update_type,
                status="error",
                command_name=self._normalize(command_name, 128),
                callback_data=self._normalize(callback_data, 256),
                handler_name=self._normalize(handler_name, 255),
                duration_ms=duration_ms,
                user_id=user_id,
                username=self._normalize(username, 255),
                chat_id=chat_id,
                error_type=self._normalize(type(error).__name__, 255),
                error_message=self._normalize(str(error), 1024),
                created_at=created_at.astimezone(timezone.utc),
            )
        )

    @staticmethod
    def _normalize(value: str | None, limit: int) -> str | None:
        if not value:
            return None
        return value.strip()[:limit] or None
