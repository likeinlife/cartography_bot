from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from .error_handler import ErrorHandlerMiddleware
from .is_admin import BlockNonAdminMiddleware
from .logging import LogCommandsMiddleware


def register_all_middlewares(dp: Dispatcher, dev_mode: bool, admin_id: int) -> None:
    if dev_mode:
        dp.message.middleware(BlockNonAdminMiddleware(admin_id))
    dp.message.middleware(ChatActionMiddleware())
    dp.message.middleware(LogCommandsMiddleware())
    dp.message.middleware(ErrorHandlerMiddleware())
