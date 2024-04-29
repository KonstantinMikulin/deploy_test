import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

log_handlers_router = Router()


@log_handlers_router.message(CommandStart())
async def process_start_log(message: Message) -> None:
    logger.debug('Enter /start')

    await message.answer(text='Hello, who are you?')
    new_user_data = (f'Someone new\n'
                     f'Their ID: {message.from_user.id}\n'
                     f'Name: {message.from_user.full_name}\n'
                     f'Nickname: {message.from_user.username}\n'
                     f'Is bot?: {message.from_user.is_bot}')

    for admin_id in [5903864970, 828900493]:
        await message.bot.send_message(chat_id=admin_id, text=new_user_data)

    logger.debug('Exit /start')
