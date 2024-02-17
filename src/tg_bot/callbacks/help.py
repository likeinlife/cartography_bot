from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from tg_bot import strings
from tg_bot.enums import HelpCallbackEnum
from tg_bot.keyboards import inline

router = Router()


@router.message(Command(commands="help"))
@router.message(F.text == "Помощь")
@router.callback_query(F.data == HelpCallbackEnum.HELP_MENU)
async def help_menu(message: Message | CallbackQuery):
    help_menu_text = "Выберите пункт"
    if isinstance(message, Message):
        await message.answer(help_menu_text, reply_markup=inline.get_inline_help())
    else:
        await message.message.edit_text(help_menu_text, reply_markup=inline.get_inline_help())  # type: ignore


@router.callback_query(F.data == HelpCallbackEnum.HELP_COMMANDS)
async def show_help_commands(call: CallbackQuery):
    await call.message.edit_text(  # type: ignore
        strings.COMMANDS_HELP,
        reply_markup=inline.get_inline_help(HelpCallbackEnum.HELP_COMMANDS),
    )


@router.callback_query(F.data == HelpCallbackEnum.HELP_SCALES)
async def show_help_scales(call: CallbackQuery):
    await call.message.edit_text(  # type: ignore
        strings.SCALES_HELP,
        reply_markup=inline.get_inline_help(HelpCallbackEnum.HELP_SCALES),
    )


@router.callback_query(F.data == HelpCallbackEnum.HELP_NOMENCLATURE)
async def show_help_nomenclature(call: CallbackQuery):
    await call.message.edit_text(  # type: ignore
        strings.NOMENCLATURE_HELP,
        reply_markup=inline.get_inline_help(HelpCallbackEnum.HELP_NOMENCLATURE),
    )
