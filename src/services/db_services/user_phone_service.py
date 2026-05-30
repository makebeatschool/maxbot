from db.repos.users_phone_repo import upsert_phone

async def write_phone( user_id, phone ):
    await upsert_phone(user_id, phone)
    return True