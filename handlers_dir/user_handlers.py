import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def process_start_cmd(message: Message, first_var, second_var):
    logger.debug('Вошли в хэндлер /start')

    await message.answer(text=first_var)
    await message.reply(text=second_var)

    logger.debug('Вышли из хэндлера /start')


@user_router.message(Command(commands=['help']))
async def process_help_cmd(message: Message):
    logger.debug('Вошли в хэндлер /help')

    await message.answer(text='I can do many things!')

    logger.debug('Вышли из хэндлера /help')
