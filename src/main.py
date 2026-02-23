import asyncio

import core.logger_setup as logger_setup
from tg_bot.main import run as run_bot
from container import create_container
from core.database import healthcheck
from core.settings import Config
from domain.analytics.service import IAnalyticsService
from domain.analytics.repository import IAnalyticsRepository
from logic.analytics.service import AnalyticsService


async def run() -> None:
    analytics_service: IAnalyticsService | None = None

    container = create_container()
    app_settings = await container.get(Config)

    if app_settings.analytics_enabled:
        if not app_settings.database_url:
            raise RuntimeError("DATABASE_URL must be set when ANALYTICS_ENABLED=True")
        await healthcheck(app_settings.database_url)
        analytics_repository = await container.get(IAnalyticsRepository)
        analytics_service = AnalyticsService(
            analytics_repository=analytics_repository,
            source=app_settings.analytics_source,
        )

    logger_setup.configure_logging(
        debug_mode=app_settings.dev_mode,
        logging_level=app_settings.logging_level,
    )
    await run_bot(
        bot_token=app_settings.bot_token,
        dev_mode=app_settings.dev_mode,
        admin_id=app_settings.admin_id,
        analytics_enabled=app_settings.analytics_enabled,
        analytics_service=analytics_service,
        container=container,
    )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
