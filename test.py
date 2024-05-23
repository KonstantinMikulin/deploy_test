from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

# ...


class StartSG(StatesGroup):
    window_1 = State()
    window_2 = State()
    window_3 = State()
    window_4 = State()


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()


async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        getter_data = {'username': event_from_user.username or 'Stranger',
                       'first_show': True}
        dialog_manager.start_data.clear()
    else:
        getter_data = {'first_show': False}
    return getter_data


start_dialog = Dialog(
    Window(
        # параметр when отвечает за то, показываем ли мы виджет Format
        # с приветствием только в первом окне Window
        # в остальных окнах этот виджет не нужен
        Format('<b>Привет, {username}!</b>\n', when='first_show'),
        Const('Это <b>первое</b> окно диалога'),
        Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        getter=username_getter,
        state=StartSG.window_1
    ),
    Window(
        Const('Это <b>второе</b> окно диалога'),
        Row(
            Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
            Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const('Это <b>третье</b> окно диалога'),
        Row(
            Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
            Button(Const('Вперед ▶️'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_3
    ),
    Window(
        Const('Это <b>четвертое</b> окно диалога'),
        Button(Const('◀️ Назад'), id='b_back', on_click=go_back),
        state=StartSG.window_4
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=StartSG.window_1, 
        mode=StartMode.RESET_STACK, 
        data={'first_show': True}
    )