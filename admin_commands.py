from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from db_work import set_schedule_by_class, is_admin
from keyboards import get_classes_numbers_keyboard, get_classes_letters_keyboard

router = Router()
user_data = []

class Admin(StatesGroup):
    setting_schedule = State()


@router.message(Command("update_schedule"))  # [2]
async def update_schedule(message: Message,  state: FSMContext):
    if is_admin(message.from_user.id):
        await state.set_state(Admin.setting_schedule)
        await  message.answer("Введите расписание")

@router.message(Admin.setting_schedule)  # [2]
async def update_schedule(message: Message,  state: FSMContext):
    await state.update_data(schedule=message.text)
    a = await state.get_data()
    user_data.append(a['schedule'])
    await message.answer(
        "Назовите класс", reply_markup=get_classes_numbers_keyboard(3))
    await state.clear()


@router.callback_query(F.data.startswith('class_number_3_'))
async def callbacks_num(callback: CallbackQuery):
    number = callback.data.split("_")[3]
    user_data.append(number)
    await callback.message.answer(
        "Назовите букву класса", reply_markup=get_classes_letters_keyboard(number, 3))
    await callback.answer()


@router.callback_query(F.data.startswith('class_letter_3_'))
async def callbacks_let(callback: CallbackQuery):
    letter = callback.data.split("_")[3]
    user_data.append(letter)
    await callback.message.answer(
        "Спасибо!")
    await set_schedule_by_class(user_data[1], user_data[2], user_data[0])
    await callback.answer()