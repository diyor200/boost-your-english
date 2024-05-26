import logging
import re

import aiogram.filters
from openpyxl import load_workbook

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.filters import Command

from tgbot.loader import db, config
from tgbot.keyboards.reply import main_page_keyboard, end_next_keyboard, get_collections
from tgbot.services.broadcaster import broadcast
from tgbot.misc.states import CollectionWord, Collection, CollectionWordTraining

collection_router = Router()


@collection_router.message(F.text.casefold() == "finish")
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

@collection_router.message(F.text == 'Collection')
async def collection_handler(message: types.Message, state: FSMContext):
    await message.answer(text="collectionni tanlang", reply_markup=await get_collections(str(message.from_user.id)))
    await state.set_state(CollectionWordTraining.Collection)


@collection_router.message(CollectionWordTraining.Collection)
async def get_collection(message: types.Message, state: FSMContext):
    try:
        collection_id = await db.get_collection_id(message.text, str(message.from_user.id))
        collection_words = await db.select_all_collection_words(collection_id[0])

        collection_words_count = len(collection_words)

        if collection_words_count < 1:
            await message.answer(text="so'zlar mavjud emas", reply_markup=main_page_keyboard())
            await state.clear()
            return

        index = 0
        await state.update_data({"collection_words": collection_words, "question_count": collection_words_count,
                                 "index": index+1})

        await message.answer(text=f"{index+1}.Word: <b>{collection_words[index]['word']}</b>"
                                  f"\nTranslation <code>{collection_words[index]['translation']}</code>",
                             reply_markup=end_next_keyboard)
        await state.set_state(CollectionWordTraining.Word)
    except Exception as e:
        logging.warning(e)
        await message.answer("muammo yuzaga keldi", reply_markup=main_page_keyboard())
        await state.clear()


@collection_router.message(CollectionWordTraining.Word)
async def begin_registration(message: types.Message, state: FSMContext):
    if message.text != "next":
        await message.answer("use keyboards, please")
        await state.set_state(CollectionWordTraining.Word)
        return

    data = await state.get_data()
    index = data["index"]
    words = data["collection_words"]
    question_count = data["question_count"]

    if index < question_count:
        text = (f"{index+1}.Word: <b>{words[index]['word']}</b>"
                f"\nTranslation: <code>{words[index]['translation']}</code>")

        await state.update_data({"index": index+1})
        await message.answer(text=text)
        await state.set_state(CollectionWordTraining.Word)
    else:
        await message.answer(f"<b>Train is over</b>. You can test your knowledge in Quiz section",
                             reply_markup=main_page_keyboard())
        await state.clear()
