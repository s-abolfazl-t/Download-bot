# main.py
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from keyboards import menu_kb
from youtube import download_youtube_video
from instagram import download_instagram_post
import os

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

state = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("سلام! لطفاً یک گزینه را انتخاب کن:", reply_markup=menu_kb)

@dp.message_handler(lambda message: message.text == "📥 دانلود از یوتیوب")
async def yt_option(message: types.Message):
    state[message.from_user.id] = "youtube"
    await message.reply("لینک ویدیو یوتیوب را بفرست:")

@dp.message_handler(lambda message: message.text == "📥 دانلود از اینستاگرام")
async def insta_option(message: types.Message):
    state[message.from_user.id] = "instagram"
    await message.reply("لینک پست اینستاگرام را بفرست:")

@dp.message_handler()
async def handle_link(message: types.Message):
    user_state = state.get(message.from_user.id)
    if user_state == "youtube":
        path = download_youtube_video(message.text)
        await message.reply_document(open(path, "rb"))
    elif user_state == "instagram":
        folder = download_instagram_post(message.text)
        for fname in os.listdir(folder):
            if fname.endswith(('.mp4', '.jpg', '.jpeg')):
                await message.reply_document(open(os.path.join(folder, fname), "rb"))
    else:
        await message.reply("لطفاً ابتدا یک گزینه را انتخاب کن.")

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
