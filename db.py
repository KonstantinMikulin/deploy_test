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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    
    
async def create_user(
    sessionmaker: async_sessionmaker,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name
    )
    
    async with sessionmaker() as session:
        session.add(user)
        await session.commit()
        print(user.created_at)
    
    
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
    )
    
    # Сделаем небольшую паузу, чтобы были разные отметки времени
    await asyncio.sleep(1)
    
    # Create second user without last name
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=20000,
        first_name="Alex",
        last_name='Craig'
    )
    
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=30000,
        first_name="Jack"
    )

    # Сделаем небольшую паузу, чтобы были разные отметки времени
    await asyncio.sleep(1)
    
    await create_user(
        sessionmaker=Sessionmaker,
        telegram_id=40000,
        first_name="Alex",
        last_name="Davis",
    )

if __name__ == '__main__':
    asyncio.run(main())
