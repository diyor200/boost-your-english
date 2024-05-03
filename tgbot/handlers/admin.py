import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update, ReplyKeyboardRemove

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import adminKeyboards
from tgbot.loader import db

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    try:
        await db.add_user(name=message.from_user.full_name,
                          username=message.from_user.username,
                          telegram_id=str(message.from_user.id))
    except Exception as e:
        logging.error(msg=f"error during adding user: {e}")

    await message.reply("Assalomu alaykum. Siz adminsiz!\n Buyruqlarni ko'rish uchun /help buyrug'ini kiriting:",
                        reply_markup=ReplyKeyboardRemove())


@admin_router.message(Command("help"))
async def admin_help(message: Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/new_book - yangi kitob qo'shish",
            "/new_test - yangi test raqami yaratish",
            "/new_passage - yangi passage yaratish",
            "/new_word - yangi so'z qo'shish"
            "/training - vocabulary training",
            )

    return await message.answer(text="\n".join(text))
