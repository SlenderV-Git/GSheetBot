import logging
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import get_root_rt
from app.core.settings import get_settings

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=get_settings().API_TOKEN)
    dp = Dispatcher()
    dp.include_router(get_root_rt())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
