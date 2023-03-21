import json
from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from cartography.config import config

router = Router()


@router.message(Command(commands=['ban']), F.from_user.id == config.ADMIN_ID)
async def ban(message: Message, command: CommandObject):
    user_id = command.args
    if not user_id:
        return await message.answer('Нельзя забанить пустое значение')
    with open(config.BAN_LIST_PATH, 'r+') as file_obj:
        file_data: list = json.load(file_obj)
        if user_id not in file_data:
            file_data.append(user_id)
            file_obj.seek(0)
            json.dump(file_data, file_obj, indent=4)
            await message.answer(f'Пользователь {user_id=} добавлен в черный список')
        else:
            await message.answer(f'Пользователь {user_id=} уже в черном списке')
    config.updateBannedUsers()


@router.message(Command(commands=['banlist']), F.from_user.id == config.ADMIN_ID)
async def banlist(message: Message):
    if config.BAN_LIST:
        return await message.answer(';\n'.join(config.BAN_LIST))
    await message.answer('Черный список пуст')
    print(config.BAN_LIST)


@router.message(Command(commands=['unban']), F.from_user.id == config.ADMIN_ID)
async def unban(message: Message, command: CommandObject):
    user_id = command.args
    if not user_id:
        return await message.answer('Нельзя забанить пустое значение')
    with open(config.BAN_LIST_PATH, 'r') as file_obj:
        file_data: list = json.load(file_obj)

    with open(config.BAN_LIST_PATH, 'w') as file_obj:
        if user_id in file_data:
            file_data.remove(user_id)
            file_obj.seek(0)
            json.dump(file_data, file_obj, indent=4)
            await message.answer(f'Пользователь {user_id=} убран из черного списка')
        else:
            await message.answer(f'Пользователя с {user_id=} нет в черном списке')
    config.updateBannedUsers()