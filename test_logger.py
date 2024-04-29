import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers_dir.logger_test_handlers import log_handlers_router

logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()
stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(log_handlers_router)

    await dp.start_polling(bot)


asyncio.run(main())


