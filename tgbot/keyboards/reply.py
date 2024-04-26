from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

builder = ReplyKeyboardBuilder()
builder.add(KeyboardButton(text="📝 Konkursda qatnashish"))
builder.add(KeyboardButton(text="📝 Registratsiya"))

def adminKeyboards():
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="📝 Konkursda qatnashish"),
        KeyboardButton(text="📝 Registratsiya")],
    [KeyboardButton(text="Konkurs ishtirokchilari")],
    [KeyboardButton(text="Ro'yhatdan o'tganlar")]],
      resize_keyboard=True)
    return markup


markup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="🇺🇿 o'zbekcha"),
    KeyboardButton(text="🇷🇺 ruscha"),
]], resize_keyboard=True)


def uz_subjects_list() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Matematika"),
        KeyboardButton(text="Fizika")],
        [KeyboardButton(text="Ingliz tili"),
        KeyboardButton(text="Kores tili")],
        [KeyboardButton(text="Biologiya")],
        [KeyboardButton(text="Kimyo"),
    ]],resize_keyboard=True)


def ru_subjects_list():
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Biologiya"),
        KeyboardButton(text="Kimyo"),
    ]], resize_keyboard=True)
    return markup