from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from domain.analytics.service import IAnalyticsService
from dishka.integrations.aiogram import setup_dishka

from . import commands

from .handlers.register_handlers import register_all_handlers

from .middlewares.register_middlewares import register_all_middlewares


async def run(
    bot_token: str,
    dev_mode: bool,
    admin_id: int,
    container,
    analytics_enabled: bool,
    analytics_service: IAnalyticsService | None,
) -> None:
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    await commands.set_commands(bot=bot, dev_mode=dev_mode, admin_id=admin_id)
    register_all_handlers(dp)
    register_all_middlewares(
        dp=dp,
        dev_mode=dev_mode,
        admin_id=admin_id,
        analytics_enabled=analytics_enabled,
        analytics_service=analytics_service,
    )
    setup_dishka(container=container, router=dp, auto_inject=True)
    dp.shutdown.register(container.close)

    await dp.start_polling(bot)
