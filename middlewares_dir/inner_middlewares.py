import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)


class FirstInnerMiddleware(BaseMiddleware):
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

        # user: User = data['event_from_user']

        # if user.is_premium:
        #     result = await handler(event, data)
        #     logger.debug('Вышли из внутренней миддлвари')
        #     return result
        # else:
        #     await event.bot.send_message(
        #         chat_id=user.id,
        #         text='You don`t have Premium'
        #     )
        #     logger.debug('Вышли из внутренней миддлвари')
        #     return

        result = await handler(event, data)

        logger.debug('Вышли из внутренней миддлвари')

        return result
