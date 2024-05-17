import random

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Case, List

from environs import Env

from config_data.config_2 import text_dict

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


class StartSG(StatesGroup):
    start = State()


async def yes_click_process(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager) -> None:
    await callback.message.edit_text(
        text='Thank you for YES!'
    )
    await dialog_manager.done()


async def no_click_proces(callback: CallbackQuery, widget: Button, dialog_manage: DialogManager) -> None:
    await callback.message.edit_text(
        text='Oh :( But thank you anyway'
    )
    await dialog_manage.done()


async def get_username(event_from_user: User, **kwargs) -> dict:
    return {'username': event_from_user.username}


async def get_random_number(**kwargs) -> dict:
    return {'number': random.randint(1, 3)}


async def get_items(**kwargs) -> dict:
    return {'items': (
        (1, 'Пункт 1'),
        (2, 'Пункт 2'),
        (3, 'Пункт 3'),
    )}


start_dialog = Dialog(
    Window(
        List(
            field=Format('<b>{item[0]}</b>. {item[1]}'),
            items='items'
        ),
        getter=get_items,
        state=StartSG.start
    )
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_router(router)
dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
