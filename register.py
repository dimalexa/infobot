from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery


from db_work import save_user
from keyboards import get_classes_numbers_keyboard, get_classes_letters_keyboard

router = Router()
user_data = []

class Register(StatesGroup):
    setting_second_name = State()
    setting_first_name = State()
    setting_class_number = State()
    setting_class_letter = State()
    finish_registration = State()

@router.message(Command("register"))  # [2]
async def register(message: Message,  state: FSMContext):

    await message.answer(
        "Назовите вашу фамилию")
    await state.set_state(Register.setting_second_name)


@router.message(Register.setting_second_name)  # [2]
async def get_second_name(message: Message,  state: FSMContext):
    await state.update_data(second_name=message.text.lower().capitalize())
    await message.answer(
        "Назовите ваше имя")
    await state.set_state(Register.setting_first_name)

@router.message(Register.setting_first_name)  # [2]
async def get_first_name(message: Message,  state: FSMContext):
    await state.update_data(first_name=message.text.lower().capitalize())
    user_data.append(message.from_user.id)
    a = await state.get_data()
    user_data.append(a['second_name'])
    user_data.append(a['first_name'])
    await message.answer(
        "Назовите ваш класс", reply_markup=get_classes_numbers_keyboard(1))
    await state.clear()

@router.callback_query(F.data.startswith('class_number_1_'))
async def callbacks_num(callback: CallbackQuery):
    number = callback.data.split("_")[3]
    user_data.append(number)
    await callback.message.answer(
        "Назовите вашу букву класса", reply_markup=get_classes_letters_keyboard(number, 1))
    await callback.answer()


@router.callback_query(F.data.startswith('class_letter_1_'))
async def callbacks_let(callback: CallbackQuery):
    letter = callback.data.split("_")[3]
    user_data.append(letter)

    await callback.message.answer(
        "Спасибо!")
    await save_user(user_data[1], user_data[2], user_data[3], user_data[4], user_data[0])
    await callback.answer()
