import logging

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message

from config_data.config_2 import admin_id

logger = logging.getLogger(__name__)


class CheckAdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, message: Message) -> bool:
        if message.from_user.id in admin_id:
            return True
        else:
            return False
