from asyncio import sleep

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import add_score, get_total_score_for_user

router = Router(name='commands router')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Нажми /play и играй!')


@router.message(Command('play'))
async def cmd_warn(message: Message, session: AsyncSession):
    dice_msg = await message.answer_dice(emoji=DiceEmoji.DICE)
    score = dice_msg.dice.value  # type:ignore

    await add_score(session, message.from_user.id, score)  # type:ignore
    await sleep(4.0)  # примерное время анимации кубика на клиенте
    await message.answer(f"Выпало число {score}")
    
    
@router.message(Command('stats'))
async def cmd_stats(message: Message, session: AsyncSession):
    total_score: int = await get_total_score_for_user(
        session,
        message.from_user.id #type:ignore
    )
    await message.answer(
        f"Hello, {message.from_user.first_name}! "  # type:ignore
        f"Your total score is {total_score}"
    )
