from datetime import datetime, timedelta
import os
import json
from config import FILE_PATH, file_lock
from services.amoservice import get_trial_datetime_by_phone


def load_users():
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return {}

def save_users(data):
    tmp_path = FILE_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, FILE_PATH)

async def remove_user_by_chat_id(chat_id: int):
    async with file_lock:
        users = load_users()
        keys_to_delete = [
            key for key, user in users.items()
            if user.get("chat_id") == chat_id
        ]
        for key in keys_to_delete:
            users.pop(key, None)
        save_users(users)

async def add_user(user_id: int, chat_id: int, first_name: str = None,
                   last_name: str = None, username: str = None,):
    async with file_lock:
        # lesson_time = get_trial_datetime_by_phone(phone)
        users = load_users()
        key = str(user_id)
        if key in users:
            return False
        users[key] = {
            "user_id": user_id,
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "send_message": None
        }
        save_users(users)
        return True


async def set_reminder_time(user_id: int, day: str = None, time: str = None):
    async with file_lock:
        users = load_users()
        key = str(user_id)
        if key not in users:
            return False
        now = datetime.now()
        current = users[key].get("send_message")
        dt = (
            datetime.strptime(current, "%d.%m.%Y %H:%M")
            if current else
            now.replace(second=0, microsecond=0)
        )
        if day:
            d = datetime.strptime(day, "%d.%m.%Y")
            dt = dt.replace(year=d.year, month=d.month, day=d.day)
        if time:
            h, m = map(int, time.split(":"))
            dt = dt.replace(hour=h, minute=m)
        if not current:
            if day and not time:
                dt = dt.replace(hour=0, minute=0)
            elif time and not day:
                pass
        users[key]["send_message"] = dt.strftime("%d.%m.%Y %H:%M")
        save_users(users)
        return True
