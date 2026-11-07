import aiosqlite
from pathlib import Path

DB_PATH = Path("alldep.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 1000.0,
                username TEXT
            )
        """)
        await db.commit()

async def get_balance(user_id: int) -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            await db.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, ?)",
                (user_id, 1000.0)
            )
            await db.commit()
            return 1000.0

async def change_balance(user_id: int, amount: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()
