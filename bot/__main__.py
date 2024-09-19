import asyncio

from aiogram import Bot, Dispatcher
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import get_config, BotConfig, DbConfig
from bot.db import Base
from bot.handlers import get_routers
from bot.middlewares import DbSessionMiddleware, TrackAllUsersMiddleware


async def main():
    # В get_config передается два аргумента
    # 1. Модель Pydantic, в которую будет преобразована часть конфига
    # 2. Корневой "ключ", из которого данные читаются и накладываются на модель
    db_config = get_config(DbConfig, 'db')
    
    engine = create_async_engine(
        url=str(db_config.dsn), # здесь требуется приведение к строке
        #TODO: check if 'is_echo' will also work
        echo=db_config.echo
    )
    
    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        await conn.execute(text('SELECT 1'))
        
    # Создание таблиц
    async with engine.begin() as connection:
        # Если ловите ошибку "таблица уже существует",
        # раскомментируйте следующую строку:
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        
    bot_config = get_config(BotConfig, 'bot')
    
    # Создание диспетчера
    dp = Dispatcher(admin_id=bot_config.admin_id)
    
    # Подключение миддлварей
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.update.outer_middleware(TrackAllUsersMiddleware())
    
    # Подключаем роутеры
    dp.include_routers(*get_routers())

    # Создание экземпляра бота
    bot = Bot(token=bot_config.token.get_secret_value())
    
    await dp.start_polling(bot)
    print('Start polling...')
    
    
asyncio.run(main())    
    