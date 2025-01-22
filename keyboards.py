from aiogram import types
from consts import SUBJECTS, DAYS
from db_work import is_admin


def get_subjects(id):
    buttons = [[]]
    for e in SUBJECTS:
        buttons[0].append(types.InlineKeyboardButton(text=f"{e}", callback_data=f"subjects_{id}_{e}"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_days(id):
    buttons = [[]]
    for e in DAYS:
        buttons[0].append(types.InlineKeyboardButton(text=f"{e}", callback_data=f"days_{id}_{e}"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_buttons(teg_id):

    if is_admin(teg_id):
        buttons = [[], [], [], []]
        buttons[0].append(types.InlineKeyboardButton(text="Мое расписание", callback_data=f"button_schedule"))
        buttons[0].append(types.InlineKeyboardButton(text="Послать сообщение", callback_data=f"button_send"))
        buttons[1].append(types.InlineKeyboardButton(text="Обновить расписание", callback_data=f"button_update"))
        buttons[1].append(types.InlineKeyboardButton(text="Поздравить с днем рождения", callback_data=f"button_happybirthday"))
        buttons[2].append(types.InlineKeyboardButton(text="Опубликовать опрос", callback_data=f"button_poll"))
        buttons[2].append(types.InlineKeyboardButton(text="Обновить домашнее задание", callback_data=f"button_hw_update"))
        buttons[3].append(
            types.InlineKeyboardButton(text="Мое домашнее задание", callback_data=f"button_hw_see"))
    else:
        buttons = [[]]
        buttons[0].append(types.InlineKeyboardButton(text="Мое расписание", callback_data=f"button_schedule"))
        buttons[0].append(types.InlineKeyboardButton(text="Мое домашнее задание", callback_data=f"button_hw_see"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_file():
    buttons = [[]]
    buttons[0].append(types.InlineKeyboardButton(text="Хочу прислать ещё файл", callback_data=f"file_yes"))
    buttons[0].append(types.InlineKeyboardButton(text="Все, файлов больше не будет", callback_data=f"file_no"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_name():
    buttons = [[]]
    buttons[0].append(types.InlineKeyboardButton(text="Хочу прислать ещё одно имя", callback_data=f"name_yes"))
    buttons[0].append(types.InlineKeyboardButton(text="Все, имен больше не будет", callback_data=f"name_no"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_poll(input_list):
    buttons = []
    for e in input_list:
        buttons.append([types.InlineKeyboardButton(text=f"{e.capitalize()}", callback_data=f"poll_{e}")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_poll_end():
    buttons = [[]]
    buttons[0].append(types.InlineKeyboardButton(text="Завершить опрос", callback_data=f"end_yes"))
    buttons[0].append(types.InlineKeyboardButton(text="Продолжить голосование", callback_data=f"end_no"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard