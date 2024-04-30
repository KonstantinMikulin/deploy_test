import logging

from aiogram import Router
from aiogram.types import Message

logger = logging.getLogger(__name__)

other_router = Router()


@other_router.message()
async def send_echo(message: Message):
    logger.debug('Вошли в эхо-хэндлер')

    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Не могу послать эхо')

    logger.debug('Вышли из эхо-хэндлера')
