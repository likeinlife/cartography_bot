from aiogram import Dispatcher

from . import dev_handlers, util_handlers


def register_utils_handlers(dp: Dispatcher) -> None:
    dp.include_routers(
        util_handlers.router,
        dev_handlers.router,
    )
