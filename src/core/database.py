import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession


async def healthcheck(sessionmaker: async_sessionmaker[AsyncSession]) -> None:

    async with sessionmaker() as session:
        await session.execute(sa.text("SELECT 2"))
