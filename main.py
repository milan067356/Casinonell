import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎮 Відкрити Gorilla Games", 
            web_app=WebAppInfo(url="https://milan067356.github.io/Casinonell/")
        )]
    ])
    
    await message.answer(
        "💎 Вітаю у Gorilla Games! 💎\n\nНатисни кнопку нижче, щоб запустити ігри (Слоти, Плинко, Краш):",
        reply_markup=keyboard
    )

async def main():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    print("Бот та веб-сервер успішно запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
