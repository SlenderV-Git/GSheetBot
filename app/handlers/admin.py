from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatType
from gspread.worksheet import Worksheet
from app.models.sheets_entry import Client
from app.database.services import get_all
from app.services.command_converter import (convert_to_client, 
                                            clear_command_prefix, 
                                            validate_command, 
                                            validate_c_command)
from app.services.google_sheet import (get_day_result, 
                                       add_entry, 
                                       change_entry, 
                                       change_last_cash)

rt = Router()
rt.message.filter(F.chat.type != ChatType.PRIVATE and F.from_user.id in [chat.chat_id for chat in get_all()])

@rt.message(CommandStart())
async def start(message: Message):
    print(message.from_user, message.from_user.username)
    await message.answer("Добро пожаловать! Я бот для ведения учета грузоперевозок. Доступные команды:\n/a - Внесение данных\n/r - Редактирование данных\n/c - Корректировка кассы\n/summ - Итоговая сумма")

@rt.message(Command('a'))
async def add_record(message: Message, sheet : Worksheet):
    print(message.from_user, message.from_user.username)
    if validate_command(command=message.text):
        client = convert_to_client(clear_command_prefix("/a", message.text))
        await add_entry(sheet= sheet, client= client)
        await message.answer("Данные успешно добавлены.")
    else:
        await message.answer("Неверный формат команды")


@rt.message(Command('r'))
async def edit_record(message: Message, sheet : Worksheet):
    print(message.from_user, message.from_user.username)
    if validate_command(command=message.text):
        client = convert_to_client(clear_command_prefix("/r", message.text))
        await change_entry(sheet= sheet, client= client)
        await message.answer("Запись успешно обновлена.")
    else:
        await message.answer("Неверный формат команды")

@rt.message(Command('c'))
async def change_cash(message: Message, sheet : Worksheet):
    print(message.from_user, message.from_user.username)
    
    if validate_c_command(command=message.text) :
        summ, comment = clear_command_prefix("/c", command= message.text).split()
        client = Client(name= "Операция над кассой", summ= int(summ), comment=comment)
        await add_entry(sheet=sheet, client=client)
        await message.answer(f"Касса успешно обновлена.")
    else:
        await message.answer("Неверный формат команды")
    


@rt.message(Command('summ'))
async def summarize(message: Message, sheet : Worksheet):
    print(message.from_user, message.from_user.username)
    day_cash, cassa = await get_day_result(sheet=sheet)
    await message.answer(f"Итого за день: {day_cash}\nОстаток кассы: {cassa}")
