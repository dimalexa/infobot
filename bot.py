import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile

import polls, homework
from db_work import get_users, is_admin, save_user, get_homework
from keyboards import get_buttons, get_poll, get_poll_end
from file_work import update_results, get_results, get_winner, get_complited, update_complited, clear_complited, \
    new_results

message_data = []

class Admin(StatesGroup):
    setting_schedule = State()
    getting_message = State()
    getting_happy_birthday_text = State()
    getting_happy_birthday_photo = State()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="7869198567:AAFX-mD4L6wmduDh4qJ3WmwncrZ_0uzMjes")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def say_hello(message: Message):
    users = get_users()
    if message.from_user.id not in [x[0] for x in users]:
        await save_user(message.from_user.id)
    await message.answer("Hello! вот что я умею: ", reply_markup=get_buttons(message.from_user.id))

@dp.callback_query(F.data == "button_send")
async def getting_message(callback: CallbackQuery,  state: FSMContext):
    if is_admin(callback.from_user.id):
        await state.set_state(Admin.getting_message)
        await callback.message.answer(
        "Введите ваше сообщение - оно будет отправлено всем пользователям бота!")
    else:
        await callback.answer(
            "Эта функция доступна только админу:(", reply_markup=get_buttons(callback.from_user.id))


@dp.message(Admin.getting_message, F.text)
async def sending_message(message: Message,  state: FSMContext):
    teg_id = get_users()
    await state.clear()
    for e in teg_id:
        await bot.send_message(int(e[0]), f'{message.text}')
    await message.answer("Ваше сообщение отправлено!", reply_markup=get_buttons(message.from_user.id))


@dp.callback_query(F.data == 'button_update')  # [2]
async def update_schedule(callback: CallbackQuery,  state: FSMContext):
    if is_admin(callback.from_user.id):
        await state.set_state(Admin.setting_schedule)
        await  callback.message.answer("Пришлите новое расписание в формате pdf")
    else:
        await callback.answer(
            "Эта функция доступна только админу:(", reply_markup=get_buttons(callback.from_user.id))


@dp.message(Admin.setting_schedule, F.content_type == ContentType.DOCUMENT)
async def download_schedule(message: Message):
    await bot.download(
        message.document.file_id,
        destination=f"./schedule.pdf"
    )
    await message.answer('Расписание обновлено', reply_markup=get_buttons(message.from_user.id))


@dp.callback_query(F.data == 'button_schedule')  # [2]
async def get_schedule(callback: CallbackQuery):
    document = FSInputFile('data/schedule.pdf')
    await bot.send_document(callback.from_user.id, document)
    await callback.answer()


@dp.callback_query(F.data == 'button_happybirthday')  # [2]
async def update_schedule(callback: CallbackQuery,  state: FSMContext):
    if is_admin(callback.from_user.id):
        await state.set_state(Admin.getting_happy_birthday_text)
        await  callback.message.answer("Введите текст поздравления")
    else:
        await callback.answer(
            "Эта функция доступна только админу:(", reply_markup=get_buttons(callback.from_user.id))

@dp.message(Admin.getting_happy_birthday_text)
async def getting_happy_birthday_text(message: Message, state: FSMContext):
    await state.set_state(Admin.getting_happy_birthday_photo)
    teg_id = get_users()
    for e in teg_id:
        await bot.send_message(int(e[0]), f'{message.text}')
    await  message.answer("Пришлите праздничную картинку")


@dp.message(Admin.getting_happy_birthday_photo, F.photo)
async def getting_birthday_photo(message: Message, state: FSMContext):
    teg_id = get_users()
    for e in teg_id:
        await bot.send_photo(int(e[0]), message.photo[-1].file_id)
    await state.clear()
    await message.answer("Ваше поздравление отправлено!", reply_markup=get_buttons(message.from_user.id))


@dp.callback_query(F.data.startswith("subjects_2_"))
async def hw_update(callback: CallbackQuery):
    subject = callback.data.split("_")[2]
    text, file1, file2, file3 = await get_homework(subject)
    await callback.message.answer(f'{text}')

    if file1 != 'o':
        await bot.send_document(callback.from_user.id, file1)
    if file2 != 'o':
        await bot.send_document(callback.from_user.id, file2)
    if file3 != 'o':
        await bot.send_document(callback.from_user.id, file3)
    await callback.message.answer("Что я еще умею", reply_markup=get_buttons(callback.from_user.id))
    await callback.answer()


@dp.callback_query(F.data == 'name_no')
async def send_poll(callback: CallbackQuery):
    teg_id = get_users()
    for e in teg_id:
        if is_admin(callback.from_user.id):
            await bot.send_message(int(e[0]), "Новый опрос",
                                   reply_markup=get_poll(polls.user_data + ['Узнать результаты']))
        else:
            await bot.send_message(int(e[0]), "Новый опрос",
                                   reply_markup=get_poll(polls.user_data))
    new_results()
    await callback.answer()


@dp.callback_query(F.data.startswith('poll_'))
async def another_name(callback: CallbackQuery):
    name = callback.data.split("_")[1]
    complited_users = get_complited()
    results = get_results()

    if name == 'Узнать результаты':
        results_text = 'Вот такие получаются результаты:'
        for e in results:
            results_text += "\n"
            results_text += f"{e[0].capitalize()} набрал(а) {e[1]} голосов"
        await callback.message.answer(results_text, reply_markup=get_poll_end())
        await callback.answer()

    elif callback.from_user.id in complited_users:
        await callback.answer("Вы уже проголосовали")
    else:
        update_complited(callback.from_user.id)
        update_results(results, name)
        await callback.answer()


@dp.callback_query(F.data.startswith("end_"))
async def poll_end(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == 'yes':
        output = get_winner()
        teg_id = get_users()
        for e in teg_id:
            await bot.send_message(int(e[0]), output, reply_markup=get_buttons(callback.from_user.id))
        await callback.answer()
        clear_complited()
    else:
        await callback.message.answer("Отлично, продолжаем голосование!")
        await callback.answer()

async def main():
    dp.include_routers(homework.router, polls.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())