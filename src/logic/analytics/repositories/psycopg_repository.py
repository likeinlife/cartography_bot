from psycopg import AsyncConnection

from domain.analytics import AnalyticsEventCreate, IAnalyticsRepository


class PsycopgAnalyticsRepository(IAnalyticsRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def save_event(self, event: AnalyticsEventCreate) -> None:
        query = """
        INSERT INTO analytics_events (
            source,
            update_type,
            status,
            command_name,
            callback_data,
            handler_name,
            duration_ms,
            user_id,
            username,
            chat_id,
            error_type,
            error_message,
            created_at
        ) VALUES (
            %(source)s,
            %(update_type)s,
            %(status)s,
            %(command_name)s,
            %(callback_data)s,
            %(handler_name)s,
            %(duration_ms)s,
            %(user_id)s,
            %(username)s,
            %(chat_id)s,
            %(error_type)s,
            %(error_message)s,
            %(created_at)s
        )
        """
        async with await AsyncConnection.connect(self.database_url) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    {
                        "source": event.source,
                        "update_type": event.update_type,
                        "status": event.status,
                        "command_name": event.command_name,
                        "callback_data": event.callback_data,
                        "handler_name": event.handler_name,
                        "duration_ms": event.duration_ms,
                        "user_id": event.user_id,
                        "username": event.username,
                        "chat_id": event.chat_id,
                        "error_type": event.error_type,
                        "error_message": event.error_message,
                        "created_at": event.created_at,
                    },
                )
            await conn.commit()
