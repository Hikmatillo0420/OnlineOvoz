from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def voice_bot():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔊 Voice joylash / o'chrish"), KeyboardButton(text="📌Majburiy Obuna")],
            [KeyboardButton(text="🛎 Obunachilar soni"), KeyboardButton(text="📤 Reklama yuborish")],
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
def add_or_delete_voice():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕Voice"), KeyboardButton(text="➖Voice")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button