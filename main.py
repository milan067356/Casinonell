import time
import requests
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "NellCasino Bot is active 24/7!"

TOKEN = "8823473148:AAHLZ8ndLQYGlmDjaCKtLXJEJrZjjiss5N0"
WEB_APP_URL = "https://milan067356.github.io/Casinonell/?v=103"
URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🎰 Открыть NellCasino", "web_app": {"url": WEB_APP_URL}}],
            [{"text": "💬 Админ (@Navi4563)", "url": "https://t.me/Navi4563"}]
        ]
    }
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    try:
        requests.post(f"{URL}/sendMessage", json=data)
    except Exception as e:
        print(f"Send error: {e}")

def check_updates():
    offset = 0
    print("Бот запущен через чистый API...")
    while True:
        try:
            response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30})
            data = response.json()
            if data.get("ok"):
                for result in data.get("result", []):
                    offset = result["update_id"] + 1
                    message = result.get("message")
                    if message and "text" in message:
                        chat_id = message["chat"]["id"]
                        text = message["text"]
                        if text.startswith("/start"):
                            send_message(chat_id, "👑 **Добро пожаловать в NellCasino!**\n\nНажмите кнопку ниже, чтобы открыть приложение:")
        except Exception as e:
            print(f"Polling error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    import threading
    # Запуск фонового прослушивания сообщений Telegram
    threading.Thread(target=check_updates, daemon=True).start()
    # Запуск веб-сервера для Render
    app.run(host="0.0.0.0", port=8080)
