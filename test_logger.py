import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers_dir.logger_test_handlers import log_handlers_router

logging.basicConfig(
    level=logging.INFO,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)


class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return 'важно' in record.msg.lower()
        # return record.levelname == 'ERROR' and 'важно' in record.msg.lower()


logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()
stderr_handler.addFilter(ErrorLogFilter())

logger.addHandler(stderr_handler)

logger.warning('Важно! Это лог с предупреждением!')
logger.error('Важно! Это лог с ошибкой!')
logger.info('Важно! Это лог с уровня INFO!')
logger.error('Это лог с ошибкой!')


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(log_handlers_router)

    await dp.start_polling(bot)


asyncio.run(main())


