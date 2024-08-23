import logging
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.handlers import get_root_rt
from app.core.settings import get_settings
from app.services.google_sheet import add_day_result
from pytz import timezone

scheduler = AsyncIOScheduler()

def setup_scheduler():
    trigger = CronTrigger(hour=10, minute=0)
    scheduler.add_job(add_day_result, trigger, timezone=timezone("Europe/Moscow"))
    scheduler.start()
    
async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=get_settings().API_TOKEN)
    dp = Dispatcher()
    dp.include_router(get_root_rt())
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
