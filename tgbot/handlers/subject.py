import logging
import re
import asyncpg

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from tgbot.misc.states import Subject
from tgbot.loader import db, config
from tgbot.keyboards.reply import markup, ru_subjects_list, uz_subjects_list, builder, adminKeyboards
from tgbot.services.broadcaster import broadcast

subject_router = Router()

@subject_router.message(F.text == '📝 Registratsiya')
async def begin_Subject(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Subject.Name)


@subject_router.message(Subject.Name)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Ismingizni qaytadan kiriting:")
        return await state.set_state(Subject.Name)

    name = message.text
    await state.update_data({
        "name": name
    })
    await message.answer("Familyangizni kiriting:")
    await state.set_state(Subject.Surname)


@subject_router.message(Subject.Surname)
async def get_phone(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Familyangizni qaytadan kiriting:")
        return await state.set_state(Subject.Surname)

    await state.update_data({
        "surname": message.text
    })
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(Subject.Age)


@subject_router.message(Subject.Age)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Noto'g'ri. Yoshingizni qaytadan kiriting:\nMisol: <b>22</b>")
        return await state.set_state(Subject.Age)

    try:
        await state.update_data({
            "age": int(message.text)
        })
    except Exception as ex:
        logging.warning(ex)
        await message.answer("❌ Noto'g'ri. Yoshingizni qaytadan kiriting:\nMisol:  <b>22</b>")
        return await state.set_state(Subject.Age)

    await message.answer("Manzilingizni kiriting:")
    await state.set_state(Subject.Address)


@subject_router.message(Subject.Address)
async def get_name(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Manzilingizni qaytadan kiriting:")
        return await state.set_state(Subject.Address)

    await state.update_data({
        "address": message.text
    })
    await message.answer("Telefon raqamingizni kiriting:\nMisol: +998901234567")
    await state.set_state(Subject.Phone)


@subject_router.message(Subject.Phone)
async def f(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Telefon raqamingizni qaytadan kiriting:")
        return await state.set_state(Subject.Surname)

    if not bool(re.match("^\+998\d{9}$", message.text)):
        await message.answer("❌ Telefon raqam noto'g'ri kiritildi. Iltimos, qaytadan kiriting:\nMisol: +998901234567")
        return await state.set_state(Subject.Phone)

    await state.update_data({
        "phone": message.text
    })

    await message.answer("Qaysi tilda bo'lishini istaysiz:", reply_markup=markup)
    await state.set_state(Subject.Language)


@subject_router.message(Subject.Language)
async def f(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Tugmalardan foydalaning:")
        return await state.set_state(Subject.Language)
    if message.text not in ("🇺🇿 o'zbekcha", "🇷🇺 ruscha"):
        await message.answer("❌ Noto'g'ri. Iltimos, Tugmalardan foydalaning:")
        return await state.set_state(Subject.Language)

    await state.update_data({
        "lang": message.text,
    })

    if message.text == "🇷🇺 ruscha":
        await message.answer("Qaysi fanga qatnashmoqchisiz:", reply_markup=ru_subjects_list())
    else:
        await message.answer("Qaysi fanga qatnashmoqchisiz:", reply_markup=uz_subjects_list())
    return await state.set_state(Subject.SubjectChoice)

@subject_router.message(Subject.SubjectChoice)
async def f(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("❌ Faqat text ko'rinishida kiriting. Tugmalardan foydalaning:")
        return await state.set_state(Subject.SubjectChoice)
    if message.text not in ("Matematika", "Fizika", "Ingliz tili", "Kores tili", "Biologiya", "Kimyo"):
        await message.answer("❌ Noto'g'ri. Iltimos, Tugmalardan foydalaning:")
        return await state.set_state(Subject.SubjectChoice)
    
    data = await state.get_data()
    builder.adjust(1, 2)
    await state.clear()
    text = (f"🗣Yangi foydalanuvchi ro'yhatdan o'tdi:\n"+
            f"<b>Ismi:</b> {data['name']}\n"+
            f"<b>Familiya:</b> {data['surname']}\n"+
            f"<b>Yosh:</b> {data['age']}\n"+
            f"<b>Telefon:</b> {data['phone']}\n"+
            f"<b>Manzil:</b> {data['address']}\n"+
            f"<b>Til:</b> {data['lang']}\n"+
            f"<b>Fan:</b> {message.text}")
    if message.from_user.id in config.tg_bot.admin_ids:
        markup = adminKeyboards()
    else :
        markup = builder.as_markup(resize_keyboard=True)
    try:
        await db.add_subject_registration_data(name=data["name"], surname=data["surname"], age=data["age"], lang=data['lang'],
                                       phone=data["phone"], address=data["address"], subject=message.text)
        await broadcast(message.bot, config.tg_bot.admin_ids, text)
        await message.answer("✅ Siz ro'yhatdan muvaffaqiyatli o'tdingiz. Tez orada sizga aloqaga chiqamiz.",
                             reply_markup=markup)
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer("❌ Bu telefon raqami bilan allaqachon ro'yhatdan o'tilgan.",
                             reply_markup=markup)
    except Exception as ex:
        logging.warning(ex)
        await message.answer("❌ Ro'yhatdan o'tishda muammo yuzaga keldi.\nNoqulayliklar uchun uzur so'raymiz.",
                             reply_markup=markup)
    