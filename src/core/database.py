async def healthcheck(database_url: str) -> None:
    from psycopg import AsyncConnection

    async with await AsyncConnection.connect(database_url) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
