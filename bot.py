import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import csv

import admin_commands
import information
import register
from db_work import get_users_by_class, is_admin
from keyboards import get_classes_numbers_keyboard, get_classes_letters_keyboard

message_data = []

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="7869198567:AAFX-mD4L6wmduDh4qJ3WmwncrZ_0uzMjes")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def say_hello(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("send_message"))
async def send_message_get_class(message: types.Message,  state: FSMContext):
    if is_admin(message.from_user.id):
        await message.answer(
        "Назовите класс", reply_markup=get_classes_numbers_keyboard(2))


@dp.callback_query(F.data.startswith('class_number_2_'))
async def callbacks_num(callback: CallbackQuery):
    number = callback.data.split("_")[3]
    message_data.append(number)
    await callback.message.answer(
        "Назовите букву класса", reply_markup=get_classes_letters_keyboard(number, 2))
    await callback.answer()

@dp.callback_query(F.data.startswith('class_letter_2_'))
async def callbacks_let(callback: CallbackQuery):
    letter = callback.data.split("_")[3]
    message_data.append(letter)
    await callback.message.answer(
        "Ваше сообщение отправлено!")
    teg_id = get_users_by_class(message_data[0], message_data[1])
    for e in teg_id:
        await bot.send_message(int(e[0]), 'message')
    await callback.answer()

# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_routers(register.router, information.router, admin_commands.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())