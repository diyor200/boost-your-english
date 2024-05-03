from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_books_inline() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="book 1", callback_data="id"),
        InlineKeyboardButton(text="book 2", callback_data="2"),
    ]])

    return markup
