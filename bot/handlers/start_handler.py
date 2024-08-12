from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def process_start_cmd(message: Message) -> None:
    await message.answer('You sent /start')
