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

async def add_user(user_id: int, chat_id: int, first_name: str = None,
                   last_name: str = None, username: str = None, phone:str = None, payload: str = None):
    async with file_lock:
        send_message_date = get_trial_datetime_by_phone(phone)
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
            "payload": payload,
            "send_message": send_message_date
        }
        save_users(users)
        return True