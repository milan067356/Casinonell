import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"
# Ссылка на Mini App (с новым тегом v=100 для сброса кэша)
WEB_APP_URL = "https://milan067356.github.io/Casinonell/?v=100"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎰 Открыть NellCasino", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("💬 Админ (@Navi4563)", url="https://t.me/Navi4563")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👑 **Добро пожаловать в NellCasino!**\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение, сыграть в слоты, плинко, краш или перейти на рынок NFT подарков!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    print("Запуск бота NellCasino...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
