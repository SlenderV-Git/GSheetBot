from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from app.core.settings import get_settings
from app.services.google_sheet import get_sheet


class BaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["sheet"] = await get_sheet(get_settings().GOOGLE_SHEET_ID)
        return await handler(event, data)