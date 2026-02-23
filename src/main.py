import asyncio

import core.logger_setup as logger_setup
import tg_bot
from container import create_container
from core.database import healthcheck
from core.settings import app_settings, image_settings
from domain.analytics import IAnalyticsService
from logic.analytics import AnalyticsService
from logic.analytics.repositories import PsycopgAnalyticsRepository


async def run() -> None:
    analytics_service: IAnalyticsService | None = None

    if app_settings.analytics_enabled:
        if not app_settings.database_url:
            raise RuntimeError("DATABASE_URL must be set when ANALYTICS_ENABLED=True")
        await healthcheck(app_settings.database_url)
        analytics_service = AnalyticsService(
            analytics_repository=PsycopgAnalyticsRepository(database_url=app_settings.database_url),
            source=app_settings.analytics_source,
        )

    logger_setup.configure_logging(
        debug_mode=app_settings.dev_mode,
        logging_level=app_settings.logging_level,
    )
    container = create_container(image_settings)
    await tg_bot.run(
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
