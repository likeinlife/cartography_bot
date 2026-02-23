from abc import ABC, abstractmethod
from datetime import datetime


class IAnalyticsService(ABC):
    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError
