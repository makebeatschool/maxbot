import asyncio
import requests
from config import TELEGRAM_DOMEN
from env import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram_message(text: str) -> bool:
    if not text: return False
    url = f"{TELEGRAM_DOMEN}/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    def _send():
        try:
            r = requests.post(url, json=payload, timeout=30)
            return r.status_code == 200
        except Exception as e:
            print("Ошибка:", e)
            return False
    return await asyncio.to_thread(_send)