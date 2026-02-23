from aiogram import Dispatcher

from . import help as help_


def register_callback_handlers(dp: Dispatcher) -> None:
    dp.include_routers(help_.router)
