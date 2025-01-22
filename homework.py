from datetime import date
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType

from db_work import save_homework, get_homework
from keyboards import get_subjects, get_file, get_buttons

router = Router()

class Hw(StatesGroup):
    get_hw_text = State()
    get_hw_file_done = State()
    get_hw_file = State()


@router.callback_query(F.data == 'button_hw_update')
async def hw_update(callback: CallbackQuery):
    await callback.message.answer('По какому предмету вы хотите обновить домашнее задание?',
                                  reply_markup=get_subjects(1))
    await callback.answer()

@router.callback_query(F.data.startswith("subjects_1_"))
async def hw_update(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.split("_")[2]
    await state.update_data(subject=subject)
    await state.set_state(Hw.get_hw_text)
    await callback.message.answer('Введите новое домашнее задание')
    await callback.answer()


@router.message(F.text, Hw.get_hw_text)
async def hw_text(message: Message, state: FSMContext):
    time_now = date.today().strftime('%m.%d')
    result_text = message.text + '\n' + 'Обновлено '+ time_now
    await state.update_data(text=result_text)
    await state.update_data(counter=1)
    await message.answer('Новое домашнее задание сохранено', reply_markup=get_file())


@router.callback_query(F.data == "file_yes")
async def hw_text(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Hw.get_hw_file)
    await callback.message.answer('Пришлите файл')
    await callback.answer()


@router.message(Hw.get_hw_file, F.content_type == ContentType.DOCUMENT)
async def hw_file(message: Message, state: FSMContext):
    data = await state.get_data()
    counter = data['counter']
    if counter == 1:
        await state.update_data(file1=message.document.file_id)
    if counter == 2:
        await state.update_data(file2=message.document.file_id)
    if counter == 3:
        await state.update_data(file3=message.document.file_id)
    counter += 1
    await state.update_data(counter=counter)
    await state.set_state(Hw.get_hw_file_done)
    await message.answer('Файл сохранен', reply_markup=get_file())



@router.callback_query(F.data == "file_no")
async def hw_text(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject, text = data['subject'], data['text']
    files = []
    for i in range(1,4):
        if f'file{i}' in data.keys():
            files.append(data[f'file{i}'])
    await save_homework(subject, text, files)
    await state.clear()
    await callback.message.answer('Файл сохранен', reply_markup=get_buttons(callback.from_user.id))
    await callback.answer()



@router.callback_query(F.data == 'button_hw_see')
async def hw_update(callback: CallbackQuery):
    await callback.message.answer('По какому предмету вы хотите посмотреть домашнее задание?',
                                  reply_markup=get_subjects(2))
    await callback.answer()

