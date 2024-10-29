from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput, MessageInput

from . states import AddWeightSG
from . dialogs_handlers import validate_weight


add_weight_dialog = Dialog(
    Window(
        Const("Enter you current weight in kg, please\n\n"),
        TextInput(
            id="fill_weight",
            type_factory=validate_weight,
            on_success=weight_fill_correct_handler,  # type: ignore
            on_error=weight_error_handler,  # type: ignore
        ),
        Button(Const("Cancel"), id="cancel_fill", on_click=cancel_fill_profile),
        state=FillProfileSG.fill_init_weight,
    )
)
