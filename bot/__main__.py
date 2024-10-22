import asyncio

from aiogram import Bot, Dispatcher
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import get_config, BotConfig, DbConfig
from bot.db import Base
from bot.handlers import get_routers
from bot.middlewares import DbSessionMiddlware, TrackAllUsersMiddleware


async def main():
    db_config = get_config(DbConfig, 'db')
    
    engine = create_async_engine(
        url=str(db_config.dsn),
        echo=db_config.is_echo
    )
    
    # check DBMS connection
    async with engine.begin() as connection:
        # Если ловите ошибку "таблица уже существует",
        # раскомментируйте следующую строку:
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        
    bot_config = get_config(BotConfig, 'bot')
    
    dp = Dispatcher(admin_id=bot_config.admin_id)
    
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddlware(Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())
    
    dp.include_routers(*get_routers())
    
    bot = Bot(token=bot_config.token.get_secret_value())
    
    print('Start polling...')
    
    await dp.start_polling(bot)
    
    
asyncio.run(main())
