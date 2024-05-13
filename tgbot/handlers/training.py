import logging

import aiogram.filters
from openpyxl import load_workbook

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.filters import Command

from tgbot.loader import db, config
from tgbot.keyboards.reply import (get_book_keyboard, get_test_by_book, get_passage_by_test, end_next_keyboard,
                                   main_page_keyboard)
from tgbot.keyboards.inline import get_books_inline
from tgbot.services.broadcaster import broadcast
from tgbot.misc.states import VocabularyTraining, NewWord

train_router = Router()


@train_router.message(F.text == "finish")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
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
    await message.answer("kitobni tanlang:", reply_markup=markup)
    await state.set_state(VocabularyTraining.BookTitle)


@train_router.message(VocabularyTraining.BookTitle)
async def begin_registration(message: types.Message, state: FSMContext):
    markup = await get_test_by_book(message.text)
    if len(markup.keyboard[0]) < 1:
        await message.answer("test mavjud emas, <code>/new_test</code> - orqali yangi test raqamini qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer("testni tanlang:", reply_markup=markup)
    await state.update_data({"book": message.text})
    await state.set_state(VocabularyTraining.TestNumber)


@train_router.message(VocabularyTraining.TestNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    markup = await get_passage_by_test(int(message.text), data['book'])
    if len(markup.keyboard[0]) < 1:
        await message.answer("passage mavjud emas, <code>/new_passage</code> - orqali yangi passage qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    await message.answer("passage tanlang:", reply_markup=markup)
    await state.update_data({"test": int(message.text)})
    await state.set_state(VocabularyTraining.PassageNumber)


@train_router.message(VocabularyTraining.PassageNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    words = await db.get_vocabulary_by_passage(int(message.text), int(data["test"]), data["book"])
    if len(words) < 1:
        await message.answer(text="so'zlar mavjud emas. <code>/new_word</code> orqali yangi so'zlarni qo'shing",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    index = 0
    word = words[index]["word"]
    await message.answer(text=f"{index+1}.Word: <b>{word}</b>\nDefinition: <i>{words[index]['definition']}</i>"
                              f"\nTranslation: <code>{words[index]['translation']}</code>",
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
    data = await state.get_data()
    index = data["index"]
    words = data["words"]
    question_count = data["question_count"]
    answers: dict = data["answers"]
    answers[index-1] = message.text
    if index < question_count:
        word = words[index]["word"]
        text = (f"{index+1}.Word: <b>{word}</b>\nDefinition: <i>{words[index]['definition']}</i>"
                f"\nTranslation: <code>{words[index]['translation']}</code>")
        await state.update_data({"index": index+1, "answers": answers})
        await message.answer(text=text)
        await state.set_state(VocabularyTraining.Word)
    else:
        await message.answer(f"<b>Train is over</b>. You can test you knowledge in Quiz section",
                             reply_markup=main_page_keyboard())
        await state.clear()