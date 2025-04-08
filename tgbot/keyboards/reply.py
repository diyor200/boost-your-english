import logging

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from tgbot.loader import db


def main_page_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Training🏋️"),
        KeyboardButton(text="Quiz🤓"),
    ],
    ], resize_keyboard=True)

def go_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="🏠Bosh menu"),
    ]], resize_keyboard=True)

async def get_book_keyboard() -> ReplyKeyboardMarkup:
    categories = await db.get_all_categories()
    keyboards = []
    for i in categories:
        keyboard = KeyboardButton(text=i[1])
        keyboards.append([keyboard])

    keyboards.append([KeyboardButton(text='🏠Bosh menu')])
    return ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)

async def get_word_slices_markup(category_id: int) -> ReplyKeyboardMarkup:
    try:
        db_count = await db.get_vocabularies_count_by_category_id(category_id)
        count = db_count.get('count', 0)

        if count == 0:
            return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)

        keyboards = []
        step = 30

        for start in range(1, count + 1, step):
            end = min(start + step - 1, count)
            keyboards.append(KeyboardButton(text=f"{start}-{end}"))

        # Разбиение на строки по 3 кнопки
        row_size = 3
        res_markup = [keyboards[i:i + row_size] for i in range(0, len(keyboards), row_size)]
        res_markup.append([KeyboardButton(text="🏠Bosh menu")])
        return ReplyKeyboardMarkup(keyboard=res_markup, resize_keyboard=True)

    except Exception as e:
        logging.exception("Ошибка при создании клавиатуры выбора диапазона слов:")
        return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)


async def get_passage_by_test(test_number: int, book_title: str) -> ReplyKeyboardMarkup:
    passages = await db.get_book_passage(test_number, book_title)
    keyboards = []
    for i in passages:
        keyboard = KeyboardButton(text=str(i[0]))
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)


# collection
async def get_collections(user_id: str) -> ReplyKeyboardMarkup:
    collections = await db.select_all_collections(user_id)
    keyboards = []
    for i in collections:
        keyboard = KeyboardButton(text=str(i[1]))
        keyboards.append(keyboard)

    return ReplyKeyboardMarkup(keyboard=[keyboards], resize_keyboard=True)

end_next_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='next')],
    [KeyboardButton(text='finish')],
], resize_keyboard=True)

finish_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='finish')]
], resize_keyboard=True)
