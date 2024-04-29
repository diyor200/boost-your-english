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
    await state.update_data({"book": message.text})
    await state.set_state(VocabularyTraining.TestNumber)


@contest_router.message(VocabularyTraining.TestNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("passage tanlang:",
                         reply_markup=await get_passage_by_test(int(message.text), data['book']))
    await state.update_data({"test": int(message.text)})
    await state.set_state(VocabularyTraining.PassageNumber)


@contest_router.message(VocabularyTraining.PassageNumber)
async def begin_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    words = await db.get_vocabulary_by_passage(int(message.text), int(data["test"]), data["book"], 15)
    index = 0
    word = words[index]["word"]
    await message.answer(text=f"{index+1}.Word: <b>{word}</b>\nDefinition: <i>{words[index]['definition']}</i>",
                         reply_markup=types.ReplyKeyboardRemove())
    question_count = len(words)
    answers = []
    for i in range(question_count):
        answers.append(words[i]["translation"])
    await state.update_data({"words": words, "question_count": question_count, "index": index+1,
                             "true_answers": answers, "answers": {}}
                            )
    await state.set_state(VocabularyTraining.Word)


@contest_router.message(VocabularyTraining.Word)
async def begin_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    words = data["words"]
    question_count = data["question_count"]
    answers: dict = data["answers"]
    answers[index-1] = message.text
    if index < question_count:
        word = words[index]["word"]
        text = f"{index+1}.Word: <b>{word}</b>\nDefinition: <i>{words[index]['definition']}</i>"
        await state.update_data({"index": index+1, "answers": answers})
        await message.answer(text=text)
        await state.set_state(VocabularyTraining.Word)
    else:
        answers = data["answers"]
        true_answers = data["true_answers"]
        keys = answers.keys()
        correct, wrong = 0, 0

        details = ""
        for key in keys:
            details += f"{key + 1}. Correct: <code>{true_answers[key]}</code>, your_answer: <code>{answers[key]}</code>\n"
            if true_answers[key] == answers[key]:
                correct += 1
            else:
                wrong += 1

        await message.answer(f"<b>Quiz is over</b>\nCorrect:\t{correct}\nWrong:\t{wrong}\n\nDetails:\n{details}",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
