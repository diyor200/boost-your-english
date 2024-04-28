import logging
import re
import asyncpg

from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.filters import Command

from tgbot.loader import db, config
from tgbot.keyboards.reply import get_book_keyboard, get_test_by_book, get_passage_by_test
from tgbot.services.broadcaster import broadcast
from tgbot.misc.states import VocabularyTraining

contest_router = Router()


# training
@contest_router.message(Command('training'))
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("kitobni tanlang:", reply_markup=await get_book_keyboard())
    await state.set_state(VocabularyTraining.BookTitle)


@contest_router.message(VocabularyTraining.BookTitle)
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("testni tanlang:", reply_markup=await get_test_by_book(message.text))
    await state.set_state(VocabularyTraining.TestNumber)


@contest_router.message(VocabularyTraining.TestNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("passage tanlang:", reply_markup=await get_passage_by_test(int(message.text)))
    await state.set_state(VocabularyTraining.PassageNumber)


@contest_router.message(VocabularyTraining.PassageNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("test boshlandi. sizga 15 daqiqa vaqt ajratildi", reply_markup=await get_book_keyboard())
    await state.set_state(VocabularyTraining.BookTitle)


@contest_router.message(VocabularyTraining.TestNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("kitobni tanlang:", reply_markup=await get_book_keyboard())
    await state.set_state(VocabularyTraining.BookTitle)
