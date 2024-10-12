from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def voice_bot():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Voice ➕"), KeyboardButton(text="Voice ➖")],
            [KeyboardButton(text="🛎 Obunachilar soni"), KeyboardButton(text="📤 Reklama yuborish")],
            [KeyboardButton(text="📌Majburiy Obuna")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button

def majburiy_obuna():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kanal qo'shish"), KeyboardButton(text="➖ Kanal o'chrish")],
            [KeyboardButton(text="👁‍🗨 Majburiy kanallarni ko'rish"), KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button
