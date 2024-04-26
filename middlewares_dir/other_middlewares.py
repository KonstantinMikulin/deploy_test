from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

CACHE = {'banned': [254443334, 214454432, 112221212]}
CACHE_THROTTLING = TTLCache(maxsize=10_000, ttl=5)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')
        if user is not None:
            if user.id in CACHE.get('banned'):
                return

        return await handler(event, data)


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user.id in CACHE_THROTTLING:
            return

        CACHE_THROTTLING[user.id] = True

        return await handler(event, data)
