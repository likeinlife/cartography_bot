from aiogram import Dispatcher

from . import callbacks, logic, utils


def register_all_handlers(dp: Dispatcher, dev_mode: bool) -> None:
    if dev_mode:
        utils.register_utils_handlers(dp)
    logic.register_business_handlers(dp)
    callbacks.register_callback_handlers(dp)
