from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AnalyticsEventCreate:
    source: str
    update_type: str
    status: str
    command_name: str | None
    callback_data: str | None
    handler_name: str | None
    duration_ms: int | None
    user_id: int | None
    username: str | None
    chat_id: int | None
    error_type: str | None
    error_message: str | None
    created_at: datetime
