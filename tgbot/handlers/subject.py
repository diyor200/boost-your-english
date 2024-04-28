import logging
import re
import asyncpg

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from tgbot.loader import db, config
from tgbot.misc.states import  VocabularyTraining
from tgbot.keyboards.reply import markup, builder, adminKeyboards
from tgbot.services.broadcaster import broadcast

subject_router = Router()

@subject_router.message(F.text == '📝 Registratsiya')
async def begin_(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(VocabularyTraining.Name)
