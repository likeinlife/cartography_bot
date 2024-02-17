from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from container import AppContainer
from dependency_injector.wiring import Provide, inject
from tg_bot import middlewares
from tg_bot.callbacks import help
from tg_bot.commands import set_commands
from tg_bot.handlers import (
    geography_coordinates,
    micrometer,
    middle_values,
    nomenclature_title,
    util_handlers,
)


@inject
async def run(
    bot_token: str = Provide[AppContainer.settings.bot_token],
    dev_mode: bool = Provide[AppContainer.settings.dev_mode],
) -> None:
    bot = Bot(bot_token, parse_mode="HTML")
    await set_commands(bot)
    dp = Dispatcher()

    dp.include_router(help.router)
    dp.include_router(util_handlers.router)

    dp.include_router(micrometer.router)
    dp.include_router(geography_coordinates.router)
    dp.include_router(nomenclature_title.router)
    dp.include_router(middle_values.router)

    dp.message.middleware(ChatActionMiddleware())
    dp.message.middleware(middlewares.LoggingChatActions())
    dp.message.middleware(middlewares.ErrorHandlerMiddleware())

    if dev_mode:
        from tg_bot.handlers import dev_handlers

        dp.message.middleware(middlewares.IsAdminMiddleWare())

        dp.include_router(dev_handlers.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
