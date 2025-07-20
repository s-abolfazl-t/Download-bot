# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📥 دانلود از یوتیوب")],
        [KeyboardButton("📥 دانلود از اینستاگرام")]
    ],
    resize_keyboard=True
)
