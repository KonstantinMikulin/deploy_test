import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers_dir.other_handlers import other_router
from handlers_dir.user_handlers import user_router
from middlewares_dir.inner_middlewares import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from middlewares_dir.outer_middlewares import (
    FirstOuterMiddleware,
    SecondOuterMiddleware,
    ThirdOuterMiddleware,
)
from middlewares_dir.i18n import TranslatorMiddleware

from lexicon_dir.lexicon_ru import LEXICON_RU
from lexicon_dir.lexicon_en import LEXICON_EN

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    translations = {
        'default': 'ru',
        'en': LEXICON_EN,
        'ru': LEXICON_RU,
    }

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Здесь будем регистрировать миддлвари
    dp.update.middleware(TranslatorMiddleware())
    # i18n test done

    # Запускаем polling
    await dp.start_polling(bot, _translations=translations)


asyncio.run(main())
