import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        user: User = data['event_from_user']

        if user.first_name == 'Konstantin':
            result = await handler(event, data)
            logger.debug('Вышли из внешней миддлвари')
            return result
        else:
            logger.debug('Вышли из внешней миддлвари')
            return



