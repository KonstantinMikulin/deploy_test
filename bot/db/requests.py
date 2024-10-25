from typing import cast

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from bot.db.models import User, Weight


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None
):
    stmt = upsert(User).values(
        {
        'telegram_id': telegram_id,
        'first_name': first_name,
        'last_name': last_name
        }
    )
    
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            first_name=first_name,
            last_name=last_name
        )
    )
    
    await session.execute(stmt)
    await session.commit()
    
    
async def add_weight(
    session: AsyncSession,
    telegram_id: int,
    weight: int
):
    new_weight = Weight(
        user_id=telegram_id,
        weight=weight
    )
    
    session.add(new_weight)
    await session.commit()


async def get_total_weight_for_user(
    session: AsyncSession,
    telegram_id: int
) -> int:
    user = await session.get(
        User,
        {'telegram_id': telegram_id},
        options=[selectinload(User.weights)]
    )

    return sum(item.weight for item in user.weights)


async def get_last_weights(
    session: AsyncSession,
    number_of_weights: int
) -> list[Weight]:
    stmt = (
        select(Weight)
        .order_by(Weight.created_at.desc())
        .limit(number_of_weights)
        .options(joinedload(Weight.user))
    )
    result = await session.execute(stmt)
    weights = result.scalars().all()
    weights = cast(list[Weight], weights)
    
    return weights
    