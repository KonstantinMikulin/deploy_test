import random

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Start
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


class SecondDialogSG(StatesGroup):
    start = State()


# стек сбрасывается только здесь, потому что это стартовый диалог
async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


# переключение между диалогами происходит через вызов dialog_manager.start
async def start_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=SecondDialogSG.start)


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[str, str]:
    print(f'This is start data: {dialog_manager.start_data}')
    return {'username': event_from_user.username or 'Stranger'}


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('Нажми на кнопку,\nчтобы перейти во второй диалог 👇'),
        Start(Const('Go second'), id='go_second', state=SecondDialogSG.start, mode=StartMode.NORMAL),
        getter=username_getter,
        state=StartSG.start
    ),
)

second_dialog = Dialog(
    Window(
        Const('Нажми на кнопку,\nчтобы вернуться в стартовый диалог 👇'),
        Start(Const('Go start'), id='go_start', state=StartSG.start, mode=StartMode.RESET_STACK),
        state=SecondDialogSG.start
    ),
)


# /start handler with code for store data in dialog_manage.start_data
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager) -> None:
    user_is_prem = message.from_user.is_premium
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, data={'user_prem': user_is_prem})


dp.include_router(router)
# диалоги нужно регистрировать в роутере после классических хэндлеров
dp.include_routers(start_dialog, second_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
