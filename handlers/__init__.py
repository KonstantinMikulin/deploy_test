from aiogram import Router

from handlers import start_handler
from handlers import help_handler


def get_routers() -> list[Router]:
    return [start_handler.router, help_handler.router]
