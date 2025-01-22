from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import get_name

router = Router()
user_data = []

class Poll(StatesGroup):
    get_name = State()


@router.callback_query(F.data == 'button_poll')
async def hw_update(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Poll.get_name)
    await callback.message.answer('Введите фамилию')
    await callback.answer()


@router.message(F.text, Poll.get_name)
async def append_name(message: Message, state: FSMContext):
    user_data.append(message.text.lower())
    await state.set_state()
    await message.answer('Фамилия сохранена', reply_markup=get_name())


@router.callback_query(F.data == 'name_yes')
async def another_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Poll.get_name)
    await callback.message.answer('Введите фамилию', reply_makup=get_name())
    await callback.answer()
