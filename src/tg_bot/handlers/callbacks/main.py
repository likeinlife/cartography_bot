from aiogram import Dispatcher

from . import help


def register_callback_handlers(dp: Dispatcher) -> None:
    dp.include_routers(help.router)
