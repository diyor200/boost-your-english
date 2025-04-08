import logging

import aiogram.filters
from openpyxl import load_workbook

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.filters import Command

from tgbot.loader import db, config
from tgbot.keyboards.reply import (get_book_keyboard, get_passage_by_test, end_next_keyboard,
                                   main_page_keyboard, get_word_slices_markup)
from tgbot.services.broadcaster import broadcast
from tgbot.misc.states import VocabularyTraining, NewWord



train_router = Router()


@train_router.message(F.text.casefold() == "finish")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=main_page_keyboard(),
    )

# training
@train_router.message(F.text == "Training🏋️")
async def begin_training(message: types.Message, state: FSMContext):
    markup = await get_book_keyboard()
    if len(markup.keyboard[0]) < 1:
        await message.answer("Kitob mavjud emas, <code>/new_book</code> - orqali yangi kitob qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer("Bo'limni tanlang:", reply_markup=markup)
    await state.set_state(VocabularyTraining.Category)


@train_router.message(VocabularyTraining.Category)
async def begin_registration(message: types.Message, state: FSMContext):
    if message.text == "🏠Bosh menu":
        await state.clear()
        await message.answer("Bo'limni tanlang", reply_markup=main_page_keyboard())
        return

    category = await db.get_category_id_by_name(message.text)
    markup = await get_word_slices_markup(category['id'])
    markup.resize_keyboard = True

    if markup is None or len(markup.keyboard) < 1:
        await message.answer("so'zlar mavjud emas, <code>/add_words</code> - orqali yangi so'zlar qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer("bo'limni tanlang:", reply_markup=markup)
    await state.update_data({"category_id": category['id']})
    await state.set_state(VocabularyTraining.Slices)


@train_router.message(VocabularyTraining.Slices)
async def begin_registration(message: types.Message, state: FSMContext):
    if message.text == "🏠Bosh menu":
        await state.clear()
        await message.answer("Bo'limni tanlang", reply_markup=main_page_keyboard())
        return

    parts = message.text.split('-')
    if len(parts) < 2:
        await message.answer("Iltimos tugmalardan foydalaning:")
        await state.set_state(VocabularyTraining.Slices)
        return

    try:
        offset = int(parts[0])
        limit = int(parts[1]) - int(parts[0]) + 1
    except Exception as e:
        logging.error(e)
        await message.answer("Iltimos tugmalardan foydalaning:")
        await state.set_state(VocabularyTraining.Slices)
        return

    data = await state.get_data()
    words = await db.get_vocabularies_by_category_id_and_limits(category_id=data['category_id'], limit=limit, offset=offset)
    if len(words) < 1:
        await message.answer(text="so'zlar mavjud emas. <code>/new_word</code> orqali yangi so'zlarni qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    index = 0
    word = words[index]["word"]
    await message.answer(text=f"{index+1}.Word: <b>{word}</b>\nTranslation: <code>{words[index]['translation']}</code>",
                         reply_markup=end_next_keyboard)

    question_count = len(words)
    answers = []
    for i in range(question_count):
        answers.append(words[i]["translation"])
    await state.update_data({"words": words, "question_count": question_count, "index": index+1,
                             "true_answers": answers, "answers": {}}
                            )
    await state.set_state(VocabularyTraining.Word)


@train_router.message(VocabularyTraining.Word)
async def begin_registration(message: types.Message, state: FSMContext):
    if message.text != "next":
        await message.answer("use keyboards, please")
        await state.set_state(VocabularyTraining.Word)
        return

    if message.text == "🏠Bosh menu":
        await state.clear()
        await message.answer("Bo'limni tanlang", reply_markup=main_page_keyboard())
        return

    data = await state.get_data()
    index = data["index"]
    words = data["words"]
    question_count = data["question_count"]
    if index < question_count:
        word = words[index]["word"]
        text = f"{index+1}.Word: <b>{word}</b>\nTranslation: <code>{words[index]['translation']}</code>"
        await state.update_data({"index": index+1})
        await message.answer(text=text)
        await state.set_state(VocabularyTraining.Word)
    else:
        await message.answer(f"<b>Train is over</b>. You can test your knowledge in Quiz section",
                             reply_markup=main_page_keyboard())
        await state.clear()
