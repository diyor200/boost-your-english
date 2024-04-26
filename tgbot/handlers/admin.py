from datetime import datetime
import logging

import xlsxwriter
import os

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, Update

from tgbot.filters.admin import AdminFilter
from tgbot.loader import db
from tgbot.keyboards.reply import adminKeyboards


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Assalomu alaykum. Siz adminsiz!\n Buruqlarni ko'rish uchun /help buyrug'ini kiriting:",
                        reply_markup=adminKeyboards())


# @admin_router.message(Command("help"))
async def admin_help(message: Message):
    print(message.model_dump_json())
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",)
            # "/get_registration_info - ro'yhatdan o'tganlar",
            # "/get_contest_info - konkurs qatnashchilar ro'yhati")
    return await message.answer(text="\n".join(text))


@admin_router.message(Command("help"))
async def admin_help(update: Update):
    print(update)

@admin_router.message(F.text == "Konkurs ishtirokchilari")
async def get_contest_info(message: Message):
