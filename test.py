import random

from aiogram_dialog.widgets.text import Case, Const


async def get_number(**kwargs):
    return {'number': random.randint(1, 3)}


start_dialog = Dialog(
    Window(
        Case(
            texts={
                1: Const('Это первый текст'),
                2: Const('Это второй текст'),
                3: Const('Это третий текст'),
            },
            selector='number',
        ),
        getter=get_number,
        state=StartSG.start,
    ),
)