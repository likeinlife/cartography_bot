from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from .mixins import MessageInfoGetterMixin


class BlockNonAdminMiddleware(BaseMiddleware, MessageInfoGetterMixin):
    def __init__(self, admin_id: int) -> None:
        self.admin_id = admin_id
        self.logger = structlog.get_logger("blocknonadmin_middleware")

    def _is_admin(
        self,
        user_id: int,
    ) -> bool:
        if user_id == self.admin_id:
            return True
        return False

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        message_info = self._get_message_info(event)
        if message_info.user is None:
            return await handler(event, data)
        if self._is_admin(message_info.user.id):
            return await handler(event, data)
        self.logger.warning("Block non-admin user", user_id=message_info.user.id, username=message_info.user.username)
