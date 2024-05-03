import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from handlers_dir.user_handlers import user_router
from handlers_dir.other_handlers import other_router

from middlewares_dir.outer_middlewares import SomeOuterMiddleware


def main():
    dp: Dispatcher = Dispatcher()

    dp.message.outer_middleware(SomeOuterMiddleware())
