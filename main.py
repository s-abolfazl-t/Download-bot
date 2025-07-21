import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# ساخت خودکار پوشه downloads
if not os.path.exists('downloads'):
    os.makedirs('downloads')

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("دانلود از یوتیوب", callback_data='youtube')],
        [InlineKeyboardButton("دانلود از اینستا", callback_data='instagram')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('یک گزینه انتخاب کن:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    await query.edit_message_text(text=f"گزینه انتخاب شده: {choice}\nلینک را ارسال کنید.")
    context.user_data['choice'] = choice

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = context.user_data.get('choice')
    url = update.message.text
    chat_id = update.message.chat_id

    if choice == 'youtube':
        await update.message.reply_text('در حال دانلود از یوتیوب...')
        ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(id)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        await context.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))
        os.remove(file_path)

    elif choice == 'instagram':
        await update.message.reply_text('در حال دانلود از اینستا...')
        ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(id)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        await context.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))
        os.remove(file_path)

    else:
        await update.message.reply_text('ابتدا گزینه دانلود را انتخاب کنید.')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
