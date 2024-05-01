import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers_dir.user_handlers import user_router


async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    var_1 = 'Hello from workflow'
    var_2 = 'Workflow is not a joke'

    dp.workflow_data.update({'first_var': var_1, 'second_var': var_2})
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

