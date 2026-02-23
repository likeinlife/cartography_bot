from aiogram import Dispatcher

from .utils.register_utils import register_utils_handlers
from .logic.register_logic import register_business_handlers
from .callbacks.register_callbacks import register_callback_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    register_utils_handlers(dp)
    register_business_handlers(dp)
    register_callback_handlers(dp)
