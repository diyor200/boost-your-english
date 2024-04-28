from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from tgbot.loader import db

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


async def get_book_keyboard() -> ReplyKeyboardMarkup:
    books = await db.get_all_books()
    keyboards = []
    for i in books:
        keyboard = KeyboardButton(text=i[0])
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)


async def get_test_by_book(book_title: str) -> ReplyKeyboardMarkup:
    tests = await db.get_book_tests(book_title)
    keyboards = []
    for i in tests:
        keyboard = KeyboardButton(text=str(i[0]))
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)


async def get_passage_by_test(test_number: int) -> ReplyKeyboardMarkup:
    passages = await db.get_book_passage(test_number)
    keyboards = []
    for i in passages:
        keyboard = KeyboardButton(text=str(i[0]))
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)
