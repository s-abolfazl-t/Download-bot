import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# --- دکمه‌های منو اصلی ---
def start_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔴 دانلود از یوتیوب", callback_data='youtube')],
        [InlineKeyboardButton("🟣 دانلود از اینستاگرام", callback_data='instagram')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=start_keyboard()
    )

# --- هندل انتخاب از منو ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'youtube':
        await query.message.reply_text("لینک ویدیوی یوتیوب رو بفرست:")
        context.user_data['mode'] = 'youtube'
    elif query.data == 'instagram':
        await query.message.reply_text("لینک پست اینستاگرام رو بفرست:")
        context.user_data['mode'] = 'instagram'

# --- هندل پیام‌های متنی (لینک‌ها) ---
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    url = update.message.text.strip()

    if mode == 'youtube':
        await update.message.reply_text(f"در حال پردازش لینک یوتیوب:\n{url}")
        # TODO: کد دانلود از یوتیوب
    elif mode == 'instagram':
        await update.message.reply_text(f"در حال پردازش لینک اینستاگرام:\n{url}")
        # TODO: کد دانلود از اینستاگ
