from aiogram.types import Message
from aiogram.enums import ChatType
from app.core.settings import get_settings
from app.database.services import get_all


class IsPrivate():
    def __call__(self, message : Message) -> bool:
        return message.chat.type == ChatType.PRIVATE and message.from_user.id in get_settings().ADMIN_IDS
    
class IsChat():
    def __call__(self, message : Message) -> bool:
        return message.chat.type != ChatType.PRIVATE and message.chat.id in [chat.chat_id for chat in get_all()]