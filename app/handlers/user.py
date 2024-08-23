from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatType
from app.database.services import check_id, add_id, delete_id, get_all
from app.core.settings import get_settings

rt = Router()
rt.message.filter(F.chat.type == ChatType.PRIVATE and F.from_user.id in get_settings().ADMIN_IDS)

@rt.message(Command('add'))
async def add_chat_id(message: Message):
    args = message.text.split()[-1]
    if not args.isdigit():
        await message.answer("Пожалуйста, укажите числовой ID чата после команды /add.")
        return
    chat_id = args
    existing = check_id(chat_id=int(chat_id))
    if existing:
        await message.answer("Этот ID чата уже добавлен.")
    else:
       add_id(chat_id=chat_id)
       await message.answer(f"ID чата {chat_id} успешно добавлен.")

@rt.message(Command('del'))
async def delete_chat_id(message: Message):
    args = message.text.split()[-1]
    if not args.isdigit():
        await message.answer("Пожалуйста, укажите числовой ID чата после команды /del.")
        return
    chat_id = args
    existing =check_id(chat_id=int(chat_id))
    if existing:
        delete_id(existing)
        await message.answer(f"ID чата {chat_id} успешно удален.")
    else:
        await message.answer("Этот ID чата не найден в базе данных.")


@rt.message(Command('ids'))
async def list_chat_ids(message: Message):
    chat_ids = get_all()
    if chat_ids:
        response = "\n".join([f"Запись ID: {chat.id}, Чат ID: {chat.chat_id}" for chat in chat_ids])
        await message.answer(f"Список ID чатов:\n{response}")
    else:
        await message.answer("В базе данных нет сохраненных ID чатов.")