from db.repos.user_repo import (get_user, insert_user, update_user, 
                                reset_user_relations, delete_user)

async def upsert_user( user_id:int, chat_id:int,  first_name=None, last_name=None, 
                      username=None, role:str="none" ):
    user = await get_user(user_id)
    if user:
        await update_user( user_id,
                chat_id=chat_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                role=role
        )
    else:
        await insert_user( user_id, chat_id, first_name, last_name, username, role )
    await reset_user_relations(user_id)
    return True

async def remove_user_by_chat_id(user_id):
    await delete_user(user_id)

async def get_user_or_none( user_id ):
    return await get_user(user_id)















async def calculate_next_send_time(user_id):
    pass

async def load_users():
    return []
async def save_users():
    return []