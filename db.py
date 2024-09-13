import asyncio

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import CreateTable


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    
    
    