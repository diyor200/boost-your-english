import logging
import re
import asyncpg

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from tgbot.misc.states import Registration
from tgbot.loader import db, config
from tgbot.keyboards.reply import markup, builder, adminKeyboards
from tgbot.services.broadcaster import broadcast
from tgbot.config import load_config

contest_router = Router()

config = load_config(".env")

# register
@contest_router.message(F.text == '📝 Konkursda qatnashish')
async def begin_registration(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.Name)


@contest_router.message(Registration.Name)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Ismingizni qaytadan kiriting:")
        return await state.set_state(Registration.Name)

    name = message.text
    await state.update_data({
        "name": name
    })
    await message.answer("Familyangizni kiriting:")
    await state.set_state(Registration.Surname)


@contest_router.message(Registration.Surname)
async def get_phone(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Familyangizni qaytadan kiriting:")
        return await state.set_state(Registration.Surname)

    await state.update_data({
        "surname": message.text
    })
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(Registration.Age)


@contest_router.message(Registration.Age)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Noto'g'ri. Yoshingizni qaytadan kiriting:\nMisol: <b>22</b>")
        return await state.set_state(Registration.Age)
    age: int
    try:
        age = int(message.text)
    except:
        await message.answer("❌ Noto'g'ri. Yoshingizni qaytadan kiriting:\nMisol: <b>22</b>")
        return await state.set_state(Registration.Age)

    if message.from_user.id in config.tg_bot.admin_ids:
        markup = adminKeyboards()
    else :
        markup = builder.as_markup(resize_keyboard=True)

    if age > 20:
        await message.answer("❌ Konkursda 20 yoshdan katta insonlar qatnasha olmaydi",
                             reply_markup=markup)
        return await state.clear()

    try:
        await state.update_data({
            "age": int(message.text)
        })
    except Exception as ex:
        logging.warning(ex)
        await message.answer("❌ Noto'g'ri. Yoshingizni qaytadan kiriting:\nMisol:  <b>22</b>")
        return await state.set_state(Registration.Age)

    await message.answer("Manzilingizni kiriting:")
    await state.set_state(Registration.Address)


@contest_router.message(Registration.Address)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Manzilingizni qaytadan kiriting:")
        return await state.set_state(Registration.Address)

    await state.update_data({
        "address": message.text
    })
    await message.answer("Telefon raqamingizni kiriting:\nMisol: +998901234567")
    await state.set_state(Registration.Phone)


@contest_router.message(Registration.Phone)
async def f(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Telefon raqamingizni qaytadan kiriting:")
        return await state.set_state(Registration.Surname)

    if not bool(re.match("^\+998\d{9}$", message.text)):
        await message.answer("❌ Telefon raqam noto'g'ri kiritildi. Iltimos, qaytadan kiriting:\nMisol: +998901234567")
        return await state.set_state(Registration.Phone)

    await state.update_data({
        "phone": message.text
    })

    await message.answer("Qaysi tilda bo'lishini istaysiz:", reply_markup=markup)
    await state.set_state(Registration.Language)


@contest_router.message(Registration.Language)
async def f(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Tugmalardan foydalaning:")
        return await state.set_state(Registration.Language)
    if message.text not in ("🇺🇿 o'zbekcha", "🇷🇺 ruscha"):
        await message.answer("❌ Noto'g'ri. Iltimos, Tugmalardan foydalaning:")
        return await state.set_state(Registration.Language)

    data = await state.get_data()
    builder.adjust(1, 2)
    if message.from_user.id in config.tg_bot.admin_ids:
        markup = adminKeyboards()
    else :
        markup = builder.as_markup(resize_keyboard=True)
    await state.clear()
    text = (f"🗣Yangi foydalanuvchi <i>konkurs</i>da qatnashish uchun ro'yhatdan o'tdi:\n"+
            f"<b>Ismi:</b> {data['name']}\n"+
            f"<b>Familiya:</b> {data['surname']}\n"+
            f"<b>Yosh:</b> {data['age']}\n"+
            f"<b>Telefon:</b> {data['phone']}\n"+
            f"<b>Manzil:</b> {data['address']}\n"+
            f"<b>Til:</b> {message.text}\n")
    try:
        await db.add_registration_data(name=data["name"], surname=data["surname"], age=data["age"], lang=message.text,
                                       phone=data["phone"], address=data["address"])
        await broadcast(message.bot, config.tg_bot.admin_ids, text)
        await message.answer("✅ Siz ro'yhatdan muvaffaqiyatli o'tdingiz. Tez orada sizga aloqaga chiqamiz.",
                             reply_markup=markup)
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer("❌ Bu telefon raqami bilan allaqachon ro'yhatdan o'tilgan.",
                             reply_markup=markup)
    except Exception as ex:
        print(ex)
        await message.answer("❌ Ro'yhatdan o'tishda muammo yuzaga keldi.\nNoqulayliklar uchun uzur so'raymiz.",
                             reply_markup=markup())
