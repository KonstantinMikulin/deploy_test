import asyncio
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Text, func, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    
    def __repr__(self) -> str:
        if self.last_name is None:
            name = self.first_name
        else:
            name = f"{self.first_name} {self.last_name}"
        return f"[{self.telegram_id}] {name}"
    

async def create_user(
    sessimaker: async_sessionmaker,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
    created_at: datetime | None = None
):
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        created_at=created_at
    )

    async with sessimaker() as session:
        session.add(user)
        await session.commit()
        print(user.created_at)


async def main():
    engine = create_async_engine(
        # Строка подключения при использовании Docker-образов из репозитория
        # В противном случае подставьте свои значения
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False,
    )
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    stmt = select(User).where(User.telegram_id == 5000)
    async with Sessionmaker() as session:
        result = await session.execute(stmt)
        tim = result.scalar()
        await session.delete(tim)
        await session.commit()
        
if __name__ == '__main__':
    asyncio.run(main())
