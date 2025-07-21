from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from youtube import download_youtube
from instagram import download_instagram
import os

TOKEN = os.getenv("BOT_TOKEN")

menu_keyboard = [["📥 دانلود از یوتیوب"], ["📥 دانلود از اینستاگرام"]]
state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! یکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "📥 دانلود از یوتیوب":
        state[user_id] = "youtube"
        await update.message.reply_text("لینک یوتیوب رو بفرست:")
    elif text == "📥 دانلود از اینستاگرام":
        state[user_id] = "instagram"
        await update.message.reply_text("لینک اینستاگرام رو بفرست:")
    elif user_id in state:
        kind = state[user_id]
        if kind == "youtube":
            path = download_youtube(text)
            await update.message.reply_document(document=open(path, "rb"))
        elif kind == "instagram":
            file_paths = download_instagram(text)
            for path in file_paths:
                await update.message.reply_document(document=open(path, "rb"))
        else:
            await update.message.reply_text("اول انتخاب کن که از کجا می‌خوای دانلود کنی.")
    else:
        await update.message.reply_text("اول یکی از گزینه‌های کیبورد رو انتخاب کن.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    main()
