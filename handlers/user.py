from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from fluentogram import TranslatorRunner


user_router = Router()


@user_router.message
async def process_cmd_start(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    
    button = InlineKeyboardButton(
        text=i18n.button.button(),
        callback_data='button_pressed'
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    await message.answer(
        text=i18n.hello.user(username=username),
        reply_markup=markup
    )
    
    
@user_router.callback_query
async def process_button_click(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.answer(text=i18n.button.pressed())
