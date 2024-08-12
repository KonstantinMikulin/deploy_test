import asyncio

from aiogram import Bot, Dispatcher

from bot.config_reader import Config, load_config


async def main() -> None:
    config: Config = load_config()
    
    bot = Bot(
        token=config.tg_bot.token
    )
    dp = Dispatcher()
    
    dp.include_routers(pass)
