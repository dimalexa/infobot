from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from db_work import get_class_by_id, get_schedule_by_class

router = Router()

@router.message(Command("my_schedule"))  # [2]
async def get_schedule(message: Message):
    number, letter = get_class_by_id(message.from_user.id)
    print(number, letter)
    schedule = get_schedule_by_class(number, letter)
    await message.answer(f"{schedule}")