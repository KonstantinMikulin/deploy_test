import asyncio

from aiogram import Bot, Dispatcher

from bot.config_reader import Config, load_config
from bot.handlers import get_routers


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()

    dp.include_routers(*get_routers())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
