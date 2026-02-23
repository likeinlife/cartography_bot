from sqlalchemy import BigInteger, Column, DateTime, Integer, MetaData, String, Table, Text, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.analytics.models import AnalyticsEventCreate
from domain.analytics.repository import IAnalyticsRepository

_METADATA = MetaData()

_ANALYTICS_EVENTS = Table(
    "analytics_events",
    _METADATA,
    # Primary key is managed in migrations; we only define columns we write.
    # This keeps the repository decoupled from ORM models.
    Column("source", String(length=255), nullable=False),
    Column("update_type", String(length=255), nullable=False),
    Column("status", String(length=255), nullable=False),
    Column("command_name", String(length=255)),
    Column("callback_data", Text()),
    Column("handler_name", String(length=255)),
    Column("duration_ms", Integer()),
    Column("user_id", BigInteger()),
    Column("username", String(length=255)),
    Column("chat_id", BigInteger()),
    Column("error_type", String(length=255)),
    Column("error_message", Text()),
    Column("created_at", DateTime(), nullable=False),
)


class PsycopgAnalyticsRepository(IAnalyticsRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def save_event(self, event: AnalyticsEventCreate) -> None:
        statement = insert(_ANALYTICS_EVENTS).values(
            source=event.source,
            update_type=event.update_type,
            status=event.status,
            command_name=event.command_name,
            callback_data=event.callback_data,
            handler_name=event.handler_name,
            duration_ms=event.duration_ms,
            user_id=event.user_id,
            username=event.username,
            chat_id=event.chat_id,
            error_type=event.error_type,
            error_message=event.error_message,
            created_at=event.created_at,
        )
        async with self._session_factory() as session:
            await session.execute(statement)
            await session.commit()
