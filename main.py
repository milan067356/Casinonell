import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
import asyncio

# Токен вашего бота от BotFather
TOKEN = "ВАШ_ТОКЕН_БОТА"

# Ссылка на ваш GitHub Pages
WEB_APP_URL = "https://milan067356.github.io/Casinonell/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

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
        "(Слоты, Плинко, Краш):"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
