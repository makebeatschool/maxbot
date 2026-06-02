from db.repos.user_repo import (get_user, insert_user, update_user, 
                                reset_user_relations, delete_user)
from db.repos.user_group_repo import get_all_group_users, get_group_users_by_user_id

async def upsert_user( user_id:int, chat_id:int,  first_name=None, last_name=None, 
                      username=None, role:str="none" ):
    user = await get_user(user_id)
    if user:
        await update_user( user_id, chat_id=chat_id,
                first_name=first_name, last_name=last_name,
                username=username, role=role )
    else:
        await insert_user( user_id, chat_id, first_name, last_name, username, role )
    await reset_user_relations(user_id)
    return True

async def add_user_from_group(chat_id:int, user_id:int, first_name=None, last_name=None):
    if await get_user(user_id): return False
    await insert_user( user_id=user_id, chat_id=chat_id,
        first_name=first_name, last_name=last_name,
        username=None, role=None )
    return True

async def remove_user_by_chat_id(user_id: int):
    u = await get_user(user_id)
    if not u: return
    grou_for_user = await get_group_users_by_user_id(user_id)
    if grou_for_user:
        await update_user(user_id, chat_id=grou_for_user[0]['chat_id'])
    else:
        await delete_user(user_id)

async def get_user_or_none( user_id ):
    return await get_user(user_id)
