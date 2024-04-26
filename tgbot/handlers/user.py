import asyncpg

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile

from tgbot.loader import db
from tgbot.keyboards.reply import builder

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    print(message.from_user.id)
    try:
        await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)
    builder.adjust(1, 2)
    
    # await message.answer_photo("https://telegra.ph/file/9d19f625ff5734cedbb17.jpg",
    #     caption="Xush kelibsiz! Konkurs ishtirok etish uchun <code>Konkursda qatnashish</code> tugmasini bosing",
    #     reply_markup=builder.as_markup(resize_keyboard=True))
    
    await message.answer("Xush kelibsiz! Konkurs ishtirok etish uchun <code>Konkursda qatnashish</code> tugmasini bosing",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@user_router.message(Command("help"))
async def admin_help(message: Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
           )

    return await message.answer(text="\n".join(text))
