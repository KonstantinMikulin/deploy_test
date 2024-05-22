from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

# ...


class StartSG(StatesGroup):
    start = State()


class SecondDialogSG(StatesGroup):
    start = State()


async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


async def start_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=SecondDialogSG.start)


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username or 'Stranger'}


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('Нажми на кнопку,\nчтобы перейти во второй диалог 👇'),
        Button(Const('Кнопка'), id='go_second', on_click=start_second),
        getter=username_getter,
        state=StartSG.start
    ),
)

second_dialog = Dialog(
    Window(
        Const('Нажми на кнопку,\nчтобы вернуться в стартовый диалог 👇'),
        Button(Const('Кнопка'), id='button_start', on_click=go_start),
        state=SecondDialogSG.start
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

# ...

dp.include_routers(start_dialog, second_dialog)