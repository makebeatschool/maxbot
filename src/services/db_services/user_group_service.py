from config import MOSCOW
from texts import CURATOR_DISAPEARED, KID_DESAPEARED
from datetime import datetime, timedelta
from db.repos.user_repo import get_user, delete_user
from db.repos.user_group_repo import get_all_group_users, delete_group_user, upsert_group_user
from services.db_services.group_service import get_group_by_id

async def remove_user_from_group(user_id: int, chat_id: int):
    await delete_group_user(chat_id, user_id)
    u = await get_user(user_id)
    if not u: return
    has_private = bool(u.get("chat_id"))
    has_groups = any(r["user_id"] == user_id for r in await get_all_group_users())
    if not has_private and not has_groups:
        await delete_user(user_id)

async def add_user_to_group(chat_id: int, user_id: int, notify_at=None):
    await upsert_group_user(chat_id, user_id, notify_at)

async def update_time_for_notify(chat_id: int, user_id: int):
    group = await get_group_by_id(chat_id)
    if not group: return False
    days = 3 if group["curator_id"] == user_id else 10
    notify_at = (datetime.now(MOSCOW) + timedelta(days==days)).strftime("%Y-%m-%d %H:%M:%S")
    # days = 10 if group["curator_id"] == user_id else 10
    # notify_at = (datetime.now(MOSCOW) + timedelta(seconds=days)).strftime("%Y-%m-%d %H:%M:%S")
    await upsert_group_user(chat_id, user_id, notify_at)
    return True

async def get_all_users_grou_activity():
    return await get_all_group_users()

async def get_message_for_group(chat_id: int, user_id: int):
    group = await get_group_by_id(chat_id)
    if not group: return False
    message = ""
    curator = await get_user(group["curator_id"])
    if not curator: return False
    if group["curator_id"] == user_id:
        message = CURATOR_DISAPEARED.format(
            name_curator=f"[{curator['first_name']}](max://user/{curator['user_id']})")
    else:
        u = await get_user(user_id)
        uName = "Ребёнок"
        if u:
            uName = u["first_name"]
        message = KID_DESAPEARED.format(
            name_curator=f"[{curator['first_name']}](max://user/{curator['user_id']})",
            name_kid=f"[{uName}](max://user/{u['user_id']})")
    await update_time_for_notify(chat_id, user_id)
    curator = await get_user(group["curator_id"])
    return curator["chat_id"], message