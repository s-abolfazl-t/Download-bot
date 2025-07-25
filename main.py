import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")

keyboard = ReplyKeyboardMarkup([["📥 دانلود از یوتیوب", "📥 دانلود از اینستاگرام"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("http"):
        if "youtube.com" in text or "youtu.be" in text:
            await download_youtube(update, context, text)
        elif "instagram.com" in text:
            await download_instagram(update, context, text)
        else:
            await update.message.reply_text("لینک پشتیبانی نمی‌شود.")
    else:
        await update.message.reply_text("لینک رو بفرست یا از دکمه‌ها استفاده کن.", reply_markup=keyboard)

async def download_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            await update.message.reply_video(f)
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود: {str(e)}")

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    await update.message.reply_text("در حال حاضر فقط دانلود از یوتیوب پشتیبانی می‌شود.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()