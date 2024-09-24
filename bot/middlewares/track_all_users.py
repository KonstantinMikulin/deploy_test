from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache #type:ignore
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import upsert_user


class TrackAllUsersMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.cache = TTLCache(
            maxsize=1000,
            ttl=60 * 60 * 6,  # 6 часов
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = event.message.from_user #type:ignore
        user_id = user.id

        # Надо обновить данные пользователя, если он не в кэше
        if user_id not in self.cache:
            session: AsyncSession = data["session"]
            await upsert_user(
                session=session,
                telegram_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            self.cache[user_id] = None
        return await handler(event, data)
