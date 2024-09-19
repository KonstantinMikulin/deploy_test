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
    ForeignKey,
    select
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    # Чтобы избежать циклических импортов, название модели
    # в Mapped указывайте в кавычках строкой,
    # а значение back_populates ссылается на атрибут в связанной модели
    games: Mapped[list["Game"]] = relationship(back_populates="user")
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
    played_by: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id")
    )
    # здесь атрибут назван user, поэтому выше в back_populates
    # указывается то же самое. Аналогично для "games"
    user: Mapped["User"] = relationship(back_populates="games")
    played_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"[{self.user.first_name}] {self.score} очков"

async def main():
    engine = create_async_engine(
        # Строка подключения при использовании Docker-образов из репозитория
        # В противном случае подставьте свои значения
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False,
    )

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    # async with engine.begin() as connection:
    #     await connection.run_sync(Base.metadata.drop_all)
    #     await connection.run_sync(Base.metadata.create_all)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    # async with Sessionmaker() as session:
    #     user_1 = User(telegram_id=1, first_name="Alex")
    #     user_2 = User(telegram_id=2, first_name="Alice", last_name="Smith")
    #     user_3 = User(telegram_id=3, first_name="Bob", last_name="Marlin")
    #     session.add_all([user_1, user_2, user_3])
    #     await session.flush()
    #     games = [
    #         Game(score=50, played_by=user_1.telegram_id),
    #         Game(score=26, played_by=user_1.telegram_id),
    #         Game(score=0, played_by=user_2.telegram_id),
    #         Game(score=10, played_by=user_3.telegram_id),
    #         Game(score=20, played_by=user_3.telegram_id),
    #     ]
    #     session.add_all([*games])
    #     await session.commit()

    async with Sessionmaker() as session:
        stmt = (select(User).where(User.telegram_id == 1).options(selectinload(User.games)))
        result = await session.execute(stmt)
        alex = result.unique().scalar()
        
        for game in alex.games:
            print(game)
    
    
# Точка входа _
if __name__ == "__main__":
    asyncio.run(main())
