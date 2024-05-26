import asyncpg

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove

from tgbot.loader import db
from tgbot.keyboards.reply import main_page_keyboard

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    try:
        await db.add_user(telegram_id=str(message.from_user.id),
                          name=message.from_user.full_name,
                          username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)

    await message.answer("Xush kel`ibsiz!", reply_markup=main_page_keyboard())


@user_router.message(Command("help"))
async def admin_help(message: Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/new_collection - yangi kolleksiya"
            )

    return await message.answer(text="\n".join(text), reply_markup=main_page_keyboard())
