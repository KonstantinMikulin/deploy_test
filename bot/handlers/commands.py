from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode, ShowMode

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import add_weight, get_total_weight_for_user
from bot.agrm_dialogs import add_weight_dialog
from bot.agrm_dialogs.states import AddWeightSG

router = Router(name='commands router')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hi! Press /add')
    
    
@router.message(Command('add'))
async def cmd_add_weight(message: Message, dialog_manager: DialogManager, session: AsyncSession):
    await dialog_manager.start(state=AddWeightSG.add_weight, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO)
    weight = dialog_manager.dialog_data.get('weight')

    await add_weight(
        session=session,
        telegram_id=message.from_user.id,  #type:ignore
        weight=weight,
    )
    await message.answer(f"You got {weight}")


@router.message(Command('stats'))
async def cms_stats(message: Message, session: AsyncSession):
    total_weight: int = await get_total_weight_for_user(
        session=session,
        telegram_id=message.from_user.id,  #type:ignore
    )
    await message.answer(f"Your total weight is {total_weight}")
