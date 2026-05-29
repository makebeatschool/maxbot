from datetime import datetime, timedelta
import os
import json
from config import FILE_PATH, file_lock, DAYS, MOSCOW

# в идеале добавить норм бд
# и переделать в ооп

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
        users = load_users()
        key = str(user_id)
        if key in users:
            return False
        users[key] = {
            "user_id": user_id,
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "day": "None-None",
            "send_message": None
        }
        save_users(users)
        return True

async def set_reminder_time(user_id: int, day: str = None, time: str = None):
    flag = "created"
    async with file_lock:
        users = load_users()
        key = str(user_id)
        if key not in users: return "error"
        weekdays = [value for _, value in DAYS]
        current = users[key].get("day", "None-None")
        prev_day, prev_time = current.split("-")
        current_day, current_time = prev_day, prev_time
        if day:
            if day not in weekdays: return "error"
            current_day = day
            if prev_day != "None": flag = "updated"
        if time:
            try:
                h, m = map(int, time.split(":"))
                if not (0 <= h <= 23 and 0 <= m <= 59): return "error"
                current_time = f"{h:02d}:{m:02d}"
                if prev_time != "None": flag = "updated"
            except: return "error"
        users[key]["day"] = f"{current_day}-{current_time}"
        save_users(users)
    await calculate_next_send_time(user_id)
    return flag

async def calculate_next_send_time(user_id):
    async with file_lock:
        users = load_users()
        key = str(user_id)
        if key not in users: return False
        user = users[key]
        day = user.get("day", "None-None")
        if day == "None-None": return False
        d, t = day.split("-")
        if d == "None" or t == "None": return False
        weekdays = [value for _, value in DAYS]
        try:
            h, m = map(int, t.split(":"))
        except: return False
        now = datetime.now(MOSCOW)
        target_weekday = weekdays.index(d)
        diff = (target_weekday - now.weekday()) % 7
        lesson_date = now.date() + timedelta(days=diff)
        lesson_dt = datetime.combine(lesson_date, datetime.min.time()).replace(hour=h, minute=m)
        delta = lesson_dt - now
        if delta < timedelta(minutes=15):
            lesson_dt += timedelta(days=7)
            delta = lesson_dt - now
        if delta >= timedelta(hours=24):
            send_time = lesson_dt - timedelta(hours=24)
        elif delta >= timedelta(hours=1):
            send_time = lesson_dt - timedelta(hours=1)
        else:
            send_time = lesson_dt - timedelta(minutes=15)
        user["send_message"] = send_time.replace(tzinfo=MOSCOW).isoformat()
        save_users(users)
        return True