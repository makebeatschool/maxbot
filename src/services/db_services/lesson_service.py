from config import DAYS, MOSCOW
from datetime import datetime, timedelta
from db.repos.user_repo import get_user
from db.repos.lessons_repo import upsert_user_lesson, get_all_lesson_reminders, get_user_lesson


async def get_all_lessons():
    await get_all_lesson_reminders()
    return True


async def set_reminder_time(user_id:int, day:str=None, time:str=None):
    user = await get_user(user_id)
    if not user: return "error"
    lesson = await get_user_lesson(user_id)
    flag = "created"
    current = (lesson or {}).get("lesson_date", "None-None")
    prev_day, prev_time = current.split("-")
    current_day, current_time = prev_day, prev_time
    weekdays = [v for _, v in DAYS]
    if day:
        if day not in weekdays: return "error"
        current_day = day
        if prev_day != "None":
            flag = "updated"
    if time:
        try:
            h, m = map(int, time.split(":"))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                return "error"
            current_time = f"{h:02d}:{m:02d}"
            if prev_time != "None":
                flag = "updated"
        except:
            return "error"
    new_lesson_date = f"{current_day}-{current_time}"
    await upsert_user_lesson(user_id, lesson_date=new_lesson_date, next_message_time=(lesson or {}).get("next_message_time"))
    await calculate_next_send_time(user_id)
    return flag

async def calculate_next_send_time(user_id:int):
    lesson = await get_user_lesson(user_id)
    if not lesson: return False
    day = lesson.get("lesson_date", "None-None")
    if day == "None-None": return False
    d, t = day.split("-")
    if d == "None" or t == "None":
        return False
    try:
        h, m = map(int, t.split(":"))
    except: return False
    weekdays = [v for _, v in DAYS]
    if d not in weekdays: return False
    now = datetime.now(MOSCOW)
    target_weekday = weekdays.index(d)
    diff = (target_weekday - now.weekday()) % 7
    lesson_date = now.date() + timedelta(days=diff)
    lesson_dt = datetime.combine( lesson_date, datetime.min.time(),
        tzinfo=MOSCOW ).replace(hour=h, minute=m)
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
    await upsert_user_lesson( user_id, lesson_date=day,
        next_message_time=send_time.replace(tzinfo=MOSCOW).isoformat() )
    return True