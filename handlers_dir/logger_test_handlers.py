import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

log_handlers_router = Router()


@log_handlers_router.message(CommandStart())
async def process_start_log(message: Message) -> None:
    logger.debug('Enter /start')

    await message.answer(text='Hello')

    logger.debug('Exit /start')
    logger.warning('Warn! Warn!')
