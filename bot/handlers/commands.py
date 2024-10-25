from asyncio import sleep

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import add_weight, get_total_weight_for_user

router = Router(name='commands router')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hi! Press /add')
    
    
@router.message(Command('add'))
async def cmd_add_weight(message: Message, session: AsyncSession):

    await add_weight(
        session=session,
        telegram_id=message.from_user.id,  #type:ignore
        weight=weight,
    )
    await sleep(3)
    await message.answer(f"You got {weight}")


@router.message(Command('stats'))
async def cms_stats(message: Message, session: AsyncSession):
    total_weight: int = await get_total_weight_for_user(
        session=session,
        telegram_id=message.from_user.id,  #type:ignore
    )
    await message.answer(f"Your total weight is {total_weight}")
