from aiogram import types
from consts import CLASSES

def get_classes_numbers_keyboard(id):
    buttons = [[]]
    for e in CLASSES.keys():
        buttons[0].append(types.InlineKeyboardButton(text=f"{e}", callback_data=f"class_number_{id}_{e}"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_classes_letters_keyboard(number, id):
    buttons = [[]]
    for e in CLASSES[number]:
        buttons[0].append(types.InlineKeyboardButton(text=f"{e}", callback_data=f"class_letter_{id}_{e}"))

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard