from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import get_last_games

router = Router(name='admin commands router')
router.message.filter(MagicData(F.event.chat.id == F.admin_id))


@router.message(Command('last3'))
async def cmd_last3(message: Message, session: AsyncSession):
    games = await get_last_games(
        session=session,
        number_of_games=3
    )
    result = ['Last 3 games:\n']
    
    for game in games:
        result.append(f"{game.user.first_name} get {game.score} score")
        
    await message.answer("\n".join(result))
