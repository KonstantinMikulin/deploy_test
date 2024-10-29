from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput


def validate_weight(text: str) -> str | None:
    weight = round(float(text), 2)
    if 20 <= weight <= 500:
        return text

    raise ValueError


async def weight_correct_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    weight = round(float(text), 2)
    dialog_manager.dialog_data["initial_weight"] = weight

    # TODO: add html.escape()
    await message.answer(
        f"Your current weight is {weight}\nYou will achieve your goals!"
    )
    await dialog_manager.reset_stack()


async def weight_error_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
) -> None:
    await message.answer("The weight must be int or float")
