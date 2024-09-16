import asyncio

from sqlalchemy import BigInteger, DateTime, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    def __repr__(self) -> str:
        if self.last_name is None:
            name = self.first_name
        else:
            name = f'{self.first_name} {self.last_name}'
        return f"[{self.telegram_id} {name}]"     
        
    
    
async def create_user(
    sessionmaker: async_sessionmaker,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
    created_at: int | None = None
):
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        created_at=created_at
    )
    
    async with sessionmaker() as session:
        session.add(user)
        await session.commit()
        print(user.created_at)
        
        
async def get_user(
    sessionmaker: async_sessionmaker,
    telegram_id: int
) -> User | None:
    async with sessionmaker() as session:
        result = await session.get(User, telegram_id)
    return result
    
    
async def main():
    engine = create_async_engine(
        # Строка подключения при использовании Docker-образов из репозитория
        # В противном случае подставьте свои значения
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False
    )

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        
    # async_sessionmaker – это класс, просто его название в SQLAlchemy
    # нарушает PEP 8 по именованию таких объектов
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
        
    # Create first user
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=1000,
        first_name="John",
        last_name="Preston",
        created_at=2022
    )
    
    # Сделаем небольшую паузу, чтобы были разные отметки времени
    await asyncio.sleep(1)
    
    # Create second user without last name
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=20000,
        first_name="Alex",
        last_name='Craig',
        created_at=2023
    )
    
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=30000,
        first_name="Jack",
        created_at=2024
    )

    # Сделаем небольшую паузу, чтобы были разные отметки времени
    await asyncio.sleep(1)
    
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=40000,
        first_name="Alex",
        last_name="Davis",
        created_at=2024
    )
    
    user_1000 = await get_user(Sessionmaker, 30000)
    print(user_1000)

if __name__ == '__main__':
    asyncio.run(main())
