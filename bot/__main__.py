import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_dialog import setup_dialogs

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config import Config, load_config
from bot.handlers import get_routers
from bot.db.base import Base
from bot.middlewares import DbSessionMiddlware, TrackAllUsersMiddleware
from bot.dialogs import score_dialog, delete_user_dialog

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
        "%(lineno)d - %(name)s - %(message)s",
    )

    engine = create_async_engine(
        url="postgresql+psycopg://costa:datatotest@127.0.0.1/test_db", echo=True
    )

    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    # Создание таблиц
    async with engine.begin() as connection:
        # Если ловите ошибку "таблица уже существует",
        # раскомментируйте следующую строку:
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    config: Config = load_config()  # type:ignore
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    dp.workflow_data.update({"sessionmaker": Sessionmaker})

    # Подключение мидлварей
    dp.update.outer_middleware(DbSessionMiddlware(Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    dp.include_routers(*get_routers())
    dp.include_router(score_dialog)
    dp.include_router(delete_user_dialog)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
