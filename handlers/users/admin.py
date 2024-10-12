import asyncio

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import voice_bot, majburiy_obuna
from keyboards.inline.buttons import yes_no_button
from loader import dp, db
from states.voice_states import voiceStates
from aiogram.filters import Command


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=voice_bot())


@dp.message(F.text == "🛎 Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = db.count_users()
    await message.answer(f"👥  Foydalanuvchilar soni: {count_result}")


@dp.message(F.text == "📤 Reklama yuborish", IsBotAdmin())
async def reklama_start(message: types.Message, state: FSMContext):
    await message.answer("Reklama yuborish uchun rasm, video yoki matn yuboring.")
    await state.set_state(voiceStates.ask_ad_content)


@dp.message(F.text == "Voice ➕", IsBotAdmin())
async def admin_add_voice(message: types.Message, state: FSMContext):
    await message.answer("Voice'ni qisqa nomni yozing ! ")
    await state.set_state(voiceStates.voice_name)


@dp.message(F.text == "Voice ➖", IsBotAdmin())
async def admin_delete_voice(message: types.Message, state: FSMContext):
    await message.answer("voiceni nomni kiriting ! ")
    await state.set_state(voiceStates.voice_delete_name)

@dp.message(F.text == "📌Majburiy Obuna", IsBotAdmin())
async def force_channel(message: types.Message):
    await message.answer("🔝 Majburiy obunalar qo'shish bo'limi:", reply_markup=majburiy_obuna())



@dp.message(voiceStates.ask_ad_content)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = db.select_all_users()
    count = 0
    for user in users:
        user_id = user[2]  # `user[2]` bo'lib, u `telegram_id` yoki `user_id`ni anglatadi.
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
    await message.answer(text=f"Reklama {count} ta foydalanuvchiga muvaffaqiyatli yuborildi.")


@dp.message(voiceStates.voice_delete_name)
async def film_check_code(message: types.Message, state: FSMContext):
    voice_delete_name = message.text
    if db.check_code_exists(voice_delete_name):
        await message.answer("🗑 Voice o'chirildi !")
        db.delete_voice_name(voice_delete_name)
    else:
        await message.answer("Bu nomda orqal hech qanday VOICE topilmadi !")
    await state.clear()


@dp.message(voiceStates.voice_name)
async def admin_voice_id(message: types.Message, state: FSMContext):
    voice_name = message.text
    await state.update_data({'voice_name': voice_name})
    await message.answer("endi voice'ni yuboring !")
    await state.set_state(voiceStates.voice_id)


@dp.message(voiceStates.voice_id)
async def admin(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data({'voice_id': voice_id})

    data = await state.get_data()
    text = (
        f"{data['voice_name']}"
    )
    await message.answer("Barcha ma'lumotlar to'g'rimi ?")
    await message.answer_voice(voice_id, caption=text, reply_markup=await yes_no_button(), parse_mode="HTML")

    await state.set_state(voiceStates.chekk)


@dp.callback_query(F.data == 'yes', voiceStates.chekk)
async def get_check_1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.add_voice(data['voice_name'], data['voice_id'])

    await call.message.answer("Ma'lumotlari qabul qilindi\n")
    await call.message.delete()
    await state.clear()


@dp.callback_query(F.data == 'no', voiceStates.chekk)
async def get_check_0(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Kiritilgan ma'lumotlar o'chirib tashlandi !", reply_markup=voice_bot())
    await call.message.delete()
    await state.clear()
