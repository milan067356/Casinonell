import logging
import json
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart

TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"
WEB_APP_URL = "https://milan067356.github.io/Casinonell/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    # Звичайна клавіатура (ReplyKeyboard) — СТРИКТНО НЕОБХІДНА ДЛЯ sendData()!
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🎰 Открыть NellCasino",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )
    
    welcome_text = (
        "💎 **Добро пожаловать в NellCasino!** 💎\n\n"
        "Нажмите кнопку ниже на клавиатуре, чтобы запустить игры "
        "(Слоты, Плинко, Краш) и выставить чек для пополнения ⭐:"
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# Обробник виставлення чеку зірок з WebApp
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "deposit":
            stars_amount = int(data.get("amount", 100))
            if stars_amount < 10:
                stars_amount = 10

            prices = [LabeledPrice(label="Пополнение баланса NellCasino", amount=stars_amount)]
            
            await bot.send_invoice(
                chat_id=message.chat.id,
                title="Пополнение баланса ⭐",
                description=f"Пополнение баланса в NellCasino на {stars_amount} ⭐",
                provider_token="",  # Порожньо для Telegram Stars (XTR)
                currency="XTR",
                prices=prices,
                start_parameter="deposit-stars",
                payload=f"deposit_{stars_amount}"
            )
    except Exception as e:
        logging.error(f"Ошибка при обработке WebApp данных: {e}")

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    stars_added = message.successful_payment.total_amount
    await message.answer(
        f"✅ **Оплата прошла успешно!**\n\n"
        f"Вам зачислено: **{stars_added} ⭐**.\n"
        f"Откройте NellCasino повторно для игры!"
    )

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
