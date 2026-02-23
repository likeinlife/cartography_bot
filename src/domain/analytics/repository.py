from abc import ABC, abstractmethod

from .models import AnalyticsEventCreate


class IAnalyticsRepository(ABC):
    @abstractmethod
    async def save_event(self, event: AnalyticsEventCreate) -> None:
        raise NotImplementedError
