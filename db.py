import asyncio
from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    Text,
    func,
    Uuid,
    text,
    ForeignKey
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Game(Base):
    __tablename__ = "games"

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    played_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    played_by: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id")
    )


async def main():
    engine = create_async_engine(
        # Строка подключения при использовании Docker-образов из репозитория
        # В противном случае подставьте свои значения
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False,
    )

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with Sessionmaker() as session:
        user_1 = User(telegram_id=1, first_name="Alex")
        user_2 = User(telegram_id=2, first_name="Alice", last_name="Smith")
        game_1 = Game(score=50, played_by=user_1.telegram_id)
        game_2 = Game(score=26, played_by=user_1.telegram_id)
        game_3 = Game(score=0, played_by=user_2.telegram_id)
        session.add_all([user_1, user_2, game_1, game_2, game_3])
        await session.commit()

    
# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
