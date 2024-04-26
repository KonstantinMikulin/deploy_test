import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from filters_dir.filters import MyTrueFilter, MyFalseFilter
from lexicon_dir.lexicon import LEXICON_RU

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message) -> None:
    logger.debug('Вошли в хэндлер, обрабатывающий команду /start')

    button = InlineKeyboardButton(
        text='Кнопка',
        callback_data='button_pressed'
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

    await message.answer(text=LEXICON_RU['/start'], reply_markup=markup)

    logger.debug('Вышли из хэндлера, обрабатывающего команду /start')


@user_router.callback_query(F.data, MyTrueFilter())
async def process_button_click(callback: CallbackQuery):
    logger.debug('Вошли в хэндлер, обрабатывающий нажатие на инлайн-кнопку')

    await callback.answer(text=LEXICON_RU['button_pressed'])

    logger.debug('Выходим из хэндлера, обрабатывающего нажатие на инлайн-кнопку')


@user_router.message(F.text, MyFalseFilter())
async def process_text(message: Message) -> None:
    logger.debug('Вошли в хэндлер, обрабатывающий текст')
    logger.debug('Выходим из хэндлера, обрабатывающего текст')
