import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from fluentogram import TranslatorHub
from handlers.other import other_router
from handlers.user import user_router
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.i18n import create_translator_hub

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
    "%(lineno)d - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    config: Config = load_config() #type:ignore
    
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode)
        )
    dp = Dispatcher()
    
    translator_hub: TranslatorHub = create_translator_hub() #type:ignore
    
    dp.include_routers(user_router, other_router)
    
    dp.update.middleware(TranslatorRunnerMiddleware())

    await dp.start_polling(bot, _translator_hub=translator_hub)
    
    
asyncio.run(main())
