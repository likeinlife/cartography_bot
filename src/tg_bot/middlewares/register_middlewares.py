from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from domain.analytics import IAnalyticsService

from .analytics import AnalyticsMiddleware
from .error_handler import ErrorHandlerMiddleware
from .is_admin import BlockNonAdminMiddleware
from .logging import LogCommandsMiddleware


def register_all_middlewares(
    dp: Dispatcher,
    dev_mode: bool,
    admin_id: int,
    analytics_enabled: bool,
    analytics_service: IAnalyticsService,
) -> None:
    if dev_mode:
        dp.message.middleware(BlockNonAdminMiddleware(admin_id))

    dp.message.middleware(ChatActionMiddleware())

    dp.message.middleware(LogCommandsMiddleware())
    dp.callback_query.middleware(LogCommandsMiddleware())

    dp.message.middleware(ErrorHandlerMiddleware())
    dp.callback_query.middleware(ErrorHandlerMiddleware())

    if analytics_enabled:
        dp.message.middleware(AnalyticsMiddleware(analytics_service))
        dp.callback_query.middleware(AnalyticsMiddleware(analytics_service))
