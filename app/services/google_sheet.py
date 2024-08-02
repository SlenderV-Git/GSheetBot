import gspread
from gspread.worksheet import Worksheet
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

from app.core.settings import get_settings
from app.models.sheets_entry import Client


async def get_sheet(sheet_id):
    creds = ServiceAccountCredentials.from_json_keyfile_name(get_settings().CREDENTIALS_FILE, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1

async def get_last_cash(sheet : Worksheet):
    data = sheet.get_values()
    return data[-1][-2]

async def add_entry(sheet : Worksheet, client : Client):
    cash = await get_last_cash(sheet=sheet)
    if client.summ:
        client.cash = int(client.summ) + int(cash)
    return sheet.append_row([*client])

async def delete_last_row(sheet : Worksheet):
    data = sheet.get_values()
    sheet.delete_rows(start_index=len(data), end_index=len(data))

async def change_entry(sheet : Worksheet, client : Client):
    await delete_last_row(sheet=sheet)
    await add_entry(sheet=sheet, client=client)

async def change_last_cash(sheet : Worksheet, value : int):
    data = sheet.get_values()[-1][1:]
    client = Client(
        name= data[0],
        from_client= data[1],
        where_client=data[2],
        hours=data[3],
        trips=data[4],
        summ=data[5],
        cash = value + int(data[-2])
    )
    await delete_last_row(sheet=sheet)
    await add_entry(sheet=sheet, client=client)

async def add_day_result(sheet : Worksheet):
    value = await get_last_cash(sheet=sheet)
    client = Client(name= "Рез дня", cash= value)
    await add_entry(sheet=sheet, client=client)
    
async def get_day_result(sheet : Worksheet):
    value = await get_last_cash(sheet=sheet)
    data : list[list[str]] = sheet.get_values()
    today = datetime.today().strftime('%d.%m.%Y')
    return '{:,}'.format(sum([int(row[-3]) for row in data if row[0] == today and row[-3].isdigit()])).replace(',', '.'), '{:,}'.format(int(value)).replace(',', '.')