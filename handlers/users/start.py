from aiogram.filters import CommandStart
from aiogram.types import InlineQueryResultCachedVoice, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, bot
from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from keyboards.inline.buttons import subscription_button, boshlash


async def is_user_subscribed(user_id: int) -> bool:
    channels = db.get_all_channels()
    print(f"Kanallar: {channels}")
    if not channels:
        print("Kanallar ro'yxati bo'sh, obunani tekshirmaymiz")
        return True

    for channel in channels:
        channel_id = int(channel['chat_id'])  # chat_id ni olamiz
        print(f"Tekshirilayotgan kanal ID: {channel_id}")
        try:
            chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            print(f"Foydalanuvchi statusi: {chat_member.status}")
            if chat_member.status not in ['member', 'administrator', 'creator']:
                print("Foydalanuvchi obuna emas")
                return False

        except TelegramBadRequest as e:
            print(f"Telegram xatosi: {e.message}")
            continue

        except Exception as e:
            print(f"Xato yuz berdi: {e}")
            continue

    print("Foydalanuvchi barcha kanallarga obuna")
    return True


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    user_id = message.from_user.id
    try:
        user = db.get_user(user_id=user_id)
        if not user:
            db.add_user(fullname=message.from_user.full_name, telegram_id=message.from_user.id)
            print(f"Yangi foydalanuvchi qo'shildi: {user_id}")
        else:
            print(f"Foydalanuvchi allaqachon mavjud: {user}")
    except Exception as e:
        print(f"Foydalanuvchini qo'shishda xatolik: {e}")

    await message.answer("Agar botdan foydalanishni boshlamoqchi bo'lsangiz, quyidagi tugmani bosing",
                              reply_markup= await boshlash())



@dp.callback_query(lambda c: c.data == "subscribe_true")
async def oldim(call: types.CallbackQuery):
    await call.message.delete()
    if await is_user_subscribed(call.from_user.id):

        await call.message.answer("Agar botdan foydalanishni boshlamoqchi bo'lsangiz, quyidagi tugmani bosing", reply_markup=await boshlash())
    else:
        await call.message.answer("Iltimos! ⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo'ling:",
                                  reply_markup=await subscription_button())
