from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy import insert, delete, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bot.db.tables import users as users_table

router = Router(name="commands router")


@router.message(CommandStart())
async def cmd_start(message: Message, db_engine: AsyncEngine):
    stmt = insert(users_table).values(
        telegram_id=message.from_user.id,  # type:ignore
        first_name=message.from_user.first_name,  # type:ignore
        last_name=message.from_user.last_name,  # type:ignore
    )
    do_ignore = stmt.on_conflict_do_nothing(index_elements=["telegram_id"])  # type:ignore
    async with db_engine.connect() as conn:
        await conn.execute(do_ignore)
        await conn.commit()
    await message.answer("Привет!")


@router.message(Command("select"))
async def cmd_select(message: Message, db_engine: AsyncEngine):
    stmts = [
        select(column("telegram_id"), column("first_name")).select_from(
            users_table
        ),
        select("*").select_from(users_table),
        select("*")
        .select_from(users_table)
        .where(users_table.c.first_name == "Konstantin"),
        select(users_table.c.telegram_id, users_table.c.first_name).select_from(
            users_table
        ),
        select(users_table.c.telegram_id).where(
            users_table.c.telegram_id < 1_000_000
        ),
    ]

    async with db_engine.connect() as conn:
        for stmt in stmts:
            result = await conn.execute(stmt)
            for row in result:
                print(row)
        print("==========")
    await message.answer("Проверьте терминал, чтобы увидеть данные.")


@router.message(Command("deleteme"))
async def cmd_deleteme(message: Message, db_engine: AsyncEngine):
    stmt = delete(users_table).where(
        users_table.c.telegram_id == message.from_user.id  # type:ignore
    )
    async with db_engine.connect() as conn:
        await conn.execute(stmt)
        await conn.commit()
    await message.answer("Ваши данные удалены.")
