from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import adminKeyboards

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Assalomu alaykum. Siz adminsiz!\n Buyruqlarni ko'rish uchun /help buyrug'ini kiriting:",
                        reply_markup=adminKeyboards())


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


# @admin_router.message(Command("training"))
# async def admin_help(message: Message, state: FSMContext):
#     await message.answer("Yangi kitob nomini kiriting:")


@admin_router.message(Command("new_book"))
async def admin_help(message: Message, state: FSMContext):
    await message.answer("Yangi kitob nomini kiriting:")


@admin_router.message(Command("new_test"))
async def admin_help(update: Update):
    print(update)


@admin_router.message(Command("new_passage"))
async def admin_help(update: Update):
    print(update)


@admin_router.message(Command("new_word"))
async def admin_help(update: Update):
    print(update)
