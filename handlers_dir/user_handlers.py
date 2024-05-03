import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from filters_dir.filters import CheckAdminFilter

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart(), CheckAdminFilter())
async def process_start_command(message: Message):
    logger.debug('Вошли в хэндлер /start для админа')

    admin_name = message.from_user.first_name
    await message.answer(text=f'Hello, admin {admin_name}')

    logger.debug('Вышли из хэндлера /start для админа')
