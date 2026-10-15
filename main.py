import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашого бота
TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"
# Посилання на ваш розміщений Mini App (GitHub Pages) з параметром версії для уникнення кешування
WEB_APP_URL = "https://milan067356.github.io/Casinonell/?v=33"
ADMIN_USERNAME = "@Navi4563"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"👑 **Вітаємо у NellCasino, {user.first_name}!**\n\n"
        f"Грайте в ігри, колекціонуйте офіційні 3D-подарунки Telegram Stars ⭐ та заробляйте.\n\n"
        f"🛠️ Адміністратор для зв'язку та виплат: {ADMIN_USERNAME}"
    )
    
    # Кнопка для відкриття міні-додатка
    keyboard = [
        [InlineKeyboardButton("🎮 Відкрити NellCasino", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("💬 Зв'язатися з адміном", url=f"https://t.me/Navi4563")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Відповідь на текстові повідомлення від користувачів (наприклад, чеки чи запити)
    text = update.message.text
    if text and "чек" in text.lower():
        await update.message.reply_text(
            f"📥 Ваш запит/чек прийнято в обробку!\n"
            f"Адміністратор {ADMIN_USERNAME} скоро перевірить баланс."
        )
    else:
        await update.message.reply_text(
            f"Використовуйте кнопку нижче, щоб відкрити казино, або зверніться до {ADMIN_USERNAME}.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎮 Відкрити NellCasino", web_app=WebAppInfo(url=WEB_APP_URL))]
            ])
        )

def main():
    # Ініціалізація бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Реєстрація обробників команд та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот успішно запущено і готовий до роботи!")
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
