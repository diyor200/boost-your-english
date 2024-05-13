from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from tgbot.loader import db


def main_page_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Training🏋️"),
        KeyboardButton(text="Quiz🤓"),
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


async def get_passage_by_test(test_number: int, book_title: str) -> ReplyKeyboardMarkup:
    passages = await db.get_book_passage(test_number, book_title)
    keyboards = []
    for i in passages:
        keyboard = KeyboardButton(text=str(i[0]))
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)


end_next_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='next')],
    [KeyboardButton(text='finish')],
], resize_keyboard=True)
