from datetime import datetime, timedelta
import re
from db.repos.group_repo import upsert_group, get_group, delete_group, get_all_groups
from services.google_spreas import get_group_info
from texts import GLADISHEW_TEXTS, FORGOT_GZ
from config import ANTON_GLADISHEW, URL_GOOGLE_GROUP_TABLE, WEEK, MOSCOW
from services.db_services.users_service import get_user_or_none

async def set_group(chat_id: int, title: str, curator_id: int | None = None, teacher_id: int | None = None):
    await upsert_group(chat_id, title, curator_id, teacher_id)

async def get_group_by_id(chat_id):
    return await get_group(chat_id)

async def delete_group_and_all_notify(chat_id):
    await delete_group(chat_id)

async def get_all_group_records():
    return await get_all_groups()


async def calculate_next_time_dz(chat_id):
    group = await get_group(chat_id)
    if not group: return False
    m = re.search(r"группа\s+(\d+)", group["title"], re.IGNORECASE)
    if not m: return False
    group_name = f"Группа {m.group(1)}"
    groups = get_group_info(URL_GOOGLE_GROUP_TABLE)
    lesson = next((g for g in groups if g["name"] == group_name), None)
    if not lesson: return False
    day, time_str = lesson["time"].split("-")
    hour, minute = map(int, time_str.split(":"))
    now = datetime.now(MOSCOW)
    target = now.replace( hour=hour, minute=minute, second=0, microsecond=0 )
    days_ahead = (WEEK[day] - now.weekday()) % 7
    if days_ahead == 0 and target <= now:
        days_ahead = 7
    target += timedelta(days=days_ahead)
    next_message_time = target + timedelta(hours=36)
    # next_message_time = datetime(2026, 6, 7, 9, 0)
    await upsert_group( chat_id=group["chat_id"], title=group["title"], next_message_time=next_message_time.isoformat())

async def get_message_for_dz(title, user_id):
    user = await get_user_or_none(user_id)
    AG = await get_user_or_none(ANTON_GLADISHEW['id'])
    AGID = AG['chat_id'] if AG else -1
    if not user: return None
    text = FORGOT_GZ.format(group_num=title)
    text_to_Gladishew = GLADISHEW_TEXTS['dz'].format(name_curator=user['first_name'])
    return user['chat_id'], text, AGID, text_to_Gladishew 