from db.database import get_db

async def get_user(user_id:int):
    db = await get_db()
    try:
        cur = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()

async def insert_user(user_id, chat_id, first_name, last_name, username, role):
    db = await get_db()
    try:
        await db.execute("""
            INSERT INTO users
            (user_id, chat_id, first_name, last_name, username, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, chat_id, first_name, last_name, username, role))
        await db.commit()
    finally:
        await db.close()

async def update_user(user_id, **fields):
    if not fields:
        return
    db = await get_db()
    try:
        q = ", ".join(f"{k}=?" for k in fields)
        await db.execute(
            f"UPDATE users SET {q} WHERE user_id=?",
            (*fields.values(), user_id)
        )
        await db.commit()
    finally:
        await db.close()

async def delete_user(user_id:int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM trial_reminders WHERE user_id=?", (user_id,))
        await db.execute("DELETE FROM user_lessons WHERE user_id=?", (user_id,))
        await db.execute("DELETE FROM users_phone WHERE user_id=?", (user_id,))
        await db.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        await db.commit()
    finally:
        await db.close()

async def reset_user_relations(user_id:int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM trial_reminders WHERE user_id=?", (user_id,))
        await db.execute("DELETE FROM user_lessons WHERE user_id=?", (user_id,))
        await db.execute("DELETE FROM users_phone WHERE user_id=?", (user_id,))
        await db.commit()
    finally:
        await db.close()