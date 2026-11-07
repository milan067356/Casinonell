import os
import time
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import init_db, get_balance, change_balance
from game_engine import engine
import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Налаштування бота
TOKEN = "8968346422:AAEvTRzVRD-5DFgbCL9tq8A8z2Lb9PjdWol"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Тут можна надіслати кнопку або вітання з посиланням на Web App
    web_app_url = "https://casinonell-3.onrender.com"
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🎮 Грати в Casinonell", web_app=types.WebAppInfo(url=web_app_url))]
        ]
    )
    await message.answer("Вітаємо у Casinonell! Натисніть кнопку нижче, щоб відкрити міні-апку:", reply_markup=kb)

app = FastAPI()
app.mount("/static", StaticFiles(directory="webapp"), name="static")

class BetRequest(BaseModel):
    user_id: int
    amount: float

class CashoutRequest(BaseModel):
    user_id: int
    multiplier: float

@app.on_event("startup")
async def startup():
    await init_db()
    if engine.current_round is None:
        engine.start_new_round()
    
    # Запускаємо бота у фоновому режимі, щоб він не блокував FastAPI
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def index():
    return FileResponse("webapp/index.html")

@app.get("/api/state")
async def get_state(user_id: int = 0):
    if engine.current_round is None:
        engine.start_new_round()

    r = engine.current_round
    now = time.time()
    current_mult = 1.00

    if r.status == "betting" and now >= r.betting_ends:
        r.status = "flying"

    if r.status == "flying":
        elapsed = now - r.betting_ends
        current_mult = round(1 + elapsed * 0.18, 2)
        if current_mult >= r.crash_point:
            r.status = "crashed"
            current_mult = r.crash_point

    state = engine.get_public_state()
    balance = await get_balance(user_id) if user_id else 0

    return {
        "state": state,
        "balance": balance,
        "current_multiplier": current_mult if r.status == "flying" else None
    }

@app.post("/api/bet")
async def place_bet(data: BetRequest):
    balance = await get_balance(data.user_id)
    if balance < data.amount:
        return {"ok": False, "error": "Недостатньо зірок"}
    if engine.place_bet(data.user_id, data.amount):
        await change_balance(data.user_id, -data.amount)
        return {"ok": True}
    return {"ok": False, "error": "Ставки зараз не приймаються"}

@app.post("/api/cashout")
async def cashout(data: CashoutRequest):
    mult = engine.cash_out(data.user_id, data.multiplier)
    if mult:
        bet_amount = engine.current_round.bets.get(data.user_id, 0)
        win = bet_amount * mult
        await change_balance(data.user_id, win)
        return {"ok": True, "win": round(win, 2), "multiplier": mult}
    return {"ok": False}

@app.post("/api/new_round")
async def new_round():
    engine.start_new_round()
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
