from aiogram import Dispatcher

from . import business, callbacks, dev


def register_all_handlers(dp: Dispatcher, dev_mode: bool) -> None:
    if dev_mode:
        dev.register_utils_handlers(dp)
    business.register_business_handlers(dp)
    callbacks.register_callback_handlers(dp)
