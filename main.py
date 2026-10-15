import logging
import json
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart

# Ваш токен бота
TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"

# Посилання на ваш інтерфейс GitHub Pages з версією ?v=30 для примусового скидання кешу Telegram
WEB_APP_URL = "https://milan067356.github.io/Casinonell/?v=30"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    # Клавіатура для запуску Mini App
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🎰 Відкрити NellCasino",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )
    
    welcome_text = (
        "👑 **Ласкаво просимо в NellCasino!** 👑\n\n"
        "Натисніть кнопку нижче, щоб відкрити додаток, зіграти в слоти, "
        "плінко, краш та переглянути ринок NFT подарунків зі зірками ⭐!"
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# Обробник поповнення зірок з WebApp (виставлення рахунку Telegram Stars)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "deposit":
            stars_amount = int(data.get("amount", 100))
            if stars_amount < 10:
                stars_amount = 10

            prices = [LabeledPrice(label="Поповнення балансу NellCasino", amount=stars_amount)]
            
            await bot.send_invoice(
                chat_id=message.chat.id,
                title="Поповнення балансу ⭐",
                description=f"Поповнення балансу в NellCasino на {stars_amount} ⭐",
                provider_token="",  # Порожній рядок обов'язковий для Telegram Stars (XTR)
                currency="XTR",
                prices=prices,
                start_parameter="deposit-stars",
                payload=f"deposit_{stars_amount}"
            )
    except Exception as e:
        logging.error(f"Помилка при обробці WebApp даних: {e}")

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    stars_added = message.successful_payment.total_amount
    await message.answer(
        f"✅ **Оплата пройшла успішно!**\n\n"
        f"Вам зараховано: **{stars_added} ⭐**.\n"
        f"Відкрийте NellCasino повторно для гри!"
    )

# Фоновий веб-сервер для підтримки активності Render (порт 10000)
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
