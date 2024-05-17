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


async def button_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    another_button = dialog_manager.dialog_data.get('another_button')
    print(another_button)
    dialog_manager.dialog_data.update(another_button=not another_button)


async def get_button_status(dialog_manager: DialogManager, **kwargs) -> dict:
    another_button = dialog_manager.dialog_data.get('another_button')

    return {'button_status': another_button}


start_dialog = Dialog(
    Window(
        Const('На кнопки из этого сообщения можно нажать!'),
        Button(
            text=Const('Press this'),
            id='button_1',
            on_click=button_clicked
        ),
        Button(
            text=Const('Press this too'),
            id='button_2',
            when='button_status'
        ),
        state=StartSG.start,
        getter=get_button_status
    )
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_router(router)
dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
