import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Твій новий токен
TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    # Посилання на сайт з іграми
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎮 Відкрити Gorilla Games", 
            web_app=WebAppInfo(url="https://milan06736.github.io/Casinonell/")
        )]
    ])
    
    await message.answer(
        "💎 Вітаю у Gorilla Games! 💎\n\nНатисни кнопку нижче, щоб запустити ігри (Слоти, Плинко, Краш):",
        reply_markup=keyboard
    )

async def main():
    print("Бот успішно запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
