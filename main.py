import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart
import asyncio

TOKEN = "ВАШ_ТОКЕН_БОТА"  # Вкажіть токен вашого бота від BotFather
WEB_APP_URL = "https://milan067356.github.io/Casinonell/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Сховище балансів (у реальному проекті краще використовувати базу даних)
user_balances = {}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎰 Открыть NellCasino",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    
    welcome_text = (
        "💎 **Добро пожаловать в NellCasino!** 💎\n\n"
        "Нажмите кнопку ниже, чтобы запустить игры "
        "(Слоты, Плинко, Краш) и пополнить баланс ⭐:"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# Обробка запиту на створення чека на оплату зірками
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "deposit":
            stars_amount = int(data.get("amount", 25))
            if stars_amount < 10:
                stars_amount = 10

            prices = [LabeledPrice(label="Пополнение баланса NellCasino", amount=stars_amount)]
            
            # Відправляємо чек Telegram Stars (provider_token порожній для XTR)
            await bot.send_invoice(
                chat_id=message.chat.id,
                title="Пополнение баланса ⭐",
                description=f"Пополнение баланса в NellCasino на {stars_amount} ⭐",
                provider_token="",  # Для Telegram Stars залишаємо порожнім
                currency="XTR",     # Код валюти Telegram Stars
                prices=prices,
                start_parameter="deposit-stars",
                payload=f"deposit_{stars_amount}"
            )
    except Exception as e:
        logging.error(f"Ошибка при обработке WebApp данных: {e}")

# Підтвердження готовності прийняти платеж
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Успішна оплата чека
@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    stars_added = message.successful_payment.total_amount
    user_id = message.from_user.id
    
    # Поповнюємо баланс
    user_balances[user_id] = user_balances.get(user_id, 0) + stars_added
    
    await message.answer(
        f"✅ **Оплата прошла успешно!**\n\n"
        f"Вам зачислено: **{stars_added} ⭐**.\n"
        f"Запустите NellCasino, чтобы начать игру!"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
