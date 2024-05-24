import random

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Start, Next, Back
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
    window_1 = State()
    window_2 = State()
    window_3 = State()
    window_4 = State()


# стек сбрасывается только здесь, потому что это стартовый диалог
async def go_first(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.switch_to(state=StartSG.window_1)


async def go_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.switch_to(state=StartSG.window_2)


async def go_third(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.switch_to(state=StartSG.window_3)


async def go_fourth(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.switch_to(state=StartSG.window_4)


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.back()


async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.next()


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict[str, str | bool]:
    if dialog_manager.start_data:
        getter_data = {'username': event_from_user.username or 'Stranger',
                       'first_show': True}
        dialog_manager.start_data.clear()
    else:
        getter_data = {'first_show': False}
    return getter_data


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n', when='first_show'),
        Const('Это <b>первое</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('3'), id='b_third', on_click=go_third),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        getter=username_getter,
        state=StartSG.window_1
    ),
    Window(
        Const('Это <b>второе</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('3'), id='b_third', on_click=go_third),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        Row(
            Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
            Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const('Это <b>третье</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        Row(
            Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
            Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_3
    ),
    Window(
        Const('Это <b>четвертое</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('3'), id='b_third', on_click=go_third),
        ),
        Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
        state=StartSG.window_4
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=StartSG.window_1,
        mode=StartMode.RESET_STACK,
        data={'first_show': True}
    )


dp.include_router(router)
# диалоги нужно регистрировать в роутере после классических хэндлеров
dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
