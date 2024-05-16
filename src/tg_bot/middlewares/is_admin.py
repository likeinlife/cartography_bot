from typing import Any, Awaitable, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class BlockNonAdminMiddleware(BaseMiddleware):
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
        if self._is_admin(event.chat.id):  # type: ignore
            return await handler(event, data)
