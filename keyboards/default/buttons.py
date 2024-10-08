from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def voice_bot():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Voice ➕"), KeyboardButton(text="Voice ➖")],
            [KeyboardButton(text="🛎 Obunachilar soni"), KeyboardButton(text="📤 Reklama yuborish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button
