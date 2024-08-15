from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['help']))
async def process_help_cmd(message: Message) -> None:
    await message.answer('You sent /help')


@router.message(Command(commands=['desc']))
async def process_desc_cmd(message: Message) -> None:
    await message.answer('Some text after /desc command')
