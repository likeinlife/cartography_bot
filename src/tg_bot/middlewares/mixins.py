from dataclasses import dataclass

from aiogram.types import CallbackQuery, Message, TelegramObject, User


@dataclass
class MessageInfo:
    user: User | None
    text: str | None


class MessageInfoGetterMixin:
    @staticmethod
    def _get_message_info(event: TelegramObject) -> MessageInfo:
        event_text = None
        user = None

        if isinstance(event, Message):
            user = event.from_user if event.from_user else None
            event_text = event.text
        if isinstance(event, CallbackQuery) and not user:
            user = event.from_user if event.from_user else None

        return MessageInfo(user=user, text=event_text)
