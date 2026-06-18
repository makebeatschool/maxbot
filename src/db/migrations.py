import asyncio, aiohttp, requests

from db.database import get_db
from services.db_services.user_group_service import update_time_for_notify
from services.db_services.users_service import add_user_from_group

CHAT_IDS = [
    -73293115890968,
    -73293128342808,
    -73293084433688,
    -73293076110616,
]
async def sync_group_users(chat_id: int, members: list):
    db = await get_db()
    cur = await db.execute(
        "SELECT user_id FROM group_users WHERE chat_id = ?",
        (chat_id,)
    )
    db_users = {row["user_id"] for row in await cur.fetchall()}
    before_count = len(db_users)
    added_count = 0
    for m in members:
        if m["user_id"] not in db_users:
            await add_user_from_group( chat_id, m["user_id"],
                m["first_name"], m["last_name"], )
            added_count += 1
        await update_time_for_notify(chat_id, m["user_id"])
    cur = await db.execute( 
        "SELECT COUNT(*) cnt FROM group_users WHERE chat_id = ?",
        (chat_id,)
    )
    after_count = (await cur.fetchone())["cnt"]
    await db.close()
    print(  f"chat_id={chat_id} ")
    print( f"before={before_count} ")
    print( f"added={added_count} ")
    print(f"after={after_count}")

async def fetch_chat_users(token: str, chat_ids=CHAT_IDS):
    headers = {"Authorization": token}
    result = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        for chat_id in chat_ids:
            admins = set()
            members = []
            marker = None
            r = await session.get(f"https://platform-api.max.ru/chats/{chat_id}/members/admins")
            data = await r.json()
            for u in data.get("members", []):
                admins.add(u["user_id"])
            while True:
                params = {"count": 100}
                if marker is not None:
                    params["marker"] = marker
                r = await session.get(f"https://platform-api.max.ru/chats/{chat_id}/members", params=params)
                data = await r.json()
                for u in data.get("members", []):
                    if u.get("is_bot"): continue
                    if u["user_id"] in admins: continue
                    members.append({
                        "user_id": u["user_id"],
                        "first_name": u.get("first_name"),
                        "last_name": u.get("last_name"),
                    })
                marker = data.get("marker")
                if marker is None: break
            result[chat_id] = members
    for chat_id, members in result.items():
        await sync_group_users(chat_id, members)
    print("end")

async def reset_notify_for_parent_groups():
    db = await get_db()
    updated = 0
    try:
        cur = await db.execute("SELECT chat_id, title FROM chat_groups")
        groups = await cur.fetchall()
        for g in groups:
            if "родители" in g["title"].lower():
                cur = await db.execute(
                    "UPDATE group_users SET notify_at=NULL WHERE chat_id=?",
                    (g["chat_id"],)
                )
                updated += cur.rowcount
        await db.commit()
    finally:
        await db.close()
    print(f"updated: {updated}")