from db.repos.group_repo import upsert_group, get_group, delete_group

async def set_group(chat_id: int, title: str, curator_id: int | None = None, teacher_id: int | None = None):
    await upsert_group(chat_id, title, curator_id, teacher_id)

async def get_group_by_id(chat_id):
    return await get_group(chat_id)

async def delete_group_and_all_notify(chat_id):
    await delete_group(chat_id)