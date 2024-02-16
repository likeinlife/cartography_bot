from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from misc import constants
from tg_bot.keyboards import inline

router = Router()


@router.message(Command(commands="help"))
@router.message(F.text == "Помощь")
@router.callback_query(F.data == "help_menu")
async def help_menu(message: Message | CallbackQuery):
    help_menu_text = "Выберите пункт"
    if isinstance(message, Message):
        await message.answer(help_menu_text, reply_markup=inline.get_inline_help(-1))
    else:
        await message.message.edit_text(help_menu_text, reply_markup=inline.get_inline_help(-1))  # type: ignore


@router.callback_query(F.data == "help_commands")
async def show_help_commands(call: CallbackQuery):
    await call.message.edit_text(constants.COMMANDS_HELP, reply_markup=inline.get_inline_help(0))  # type: ignore


@router.callback_query(F.data == "help_scales")
async def show_help_scales(call: CallbackQuery):
    await call.message.edit_text(constants.SCALES_HELP, reply_markup=inline.get_inline_help(1))  # type: ignore


@router.callback_query(F.data == "help_numenclature")
async def show_help_numenclature(call: CallbackQuery):
    await call.message.edit_text(constants.NUMENCLATURE_HELP, reply_markup=inline.get_inline_help(2))  # type: ignore
