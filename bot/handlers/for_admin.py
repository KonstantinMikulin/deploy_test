from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import get_last_weights

router = Router(name='admin commands router')
router.message.filter(MagicData(F.event.chat.id == F.admin_id))


@router.message(Command('last3'))
async def cmd_last3(message: Message, session: AsyncSession):
    weights = await get_last_weights(
        session=session,
        number_of_weights=3
    )
    result = ['Last 3 weights:\n']
    
    for weight in weights:
        result.append(f"{weight.user.first_name} get {weight.weight} weight")
        
    await message.answer("\n".join(result))
