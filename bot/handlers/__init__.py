from aiogram import Router

from bot.handlers import start_handler
from bot.handlers import help_handler


def get_routers() -> list[Router]:
    return [start_handler.router, help_handler.router]
