from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from . import commands, handlers, middlewares


async def run(
    bot_token: str,
    dev_mode: bool,
    admin_id: int,
    container,
) -> None:
    bot = Bot(bot_token, parse_mode="HTML")
    dp = Dispatcher()

    await commands.set_commands(bot=bot, dev_mode=dev_mode, admin_id=admin_id)
    handlers.register_all_handlers(dp)
    middlewares.register_all_middlewares(dp, dev_mode, admin_id)
    setup_dishka(container=container, router=dp, auto_inject=True)
    dp.shutdown.register(container.close)

    await dp.start_polling(bot)
