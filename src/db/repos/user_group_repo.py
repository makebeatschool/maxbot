from db.database import get_db

async def upsert_group_user(chat_id:int,user_id:int,notify_at:str|None=None):
    db=await get_db()
    try:
        await db.execute("""
            INSERT INTO group_users(chat_id,user_id,notify_at)
            VALUES(?,?,?)
            ON CONFLICT(chat_id,user_id) DO UPDATE SET notify_at=excluded.notify_at
        """,(chat_id,user_id,notify_at))
        await db.commit()
    finally:
        await db.close()

async def get_all_group_users():
    db=await get_db()
    try:
        cur=await db.execute("""
            SELECT gu.chat_id,gu.user_id,gu.notify_at,
                   u.first_name,u.last_name,u.username,
                   g.title
            FROM group_users gu
            JOIN users u ON u.user_id=gu.user_id
            JOIN chat_groups g ON g.chat_id=gu.chat_id
        """)
        return [dict(r) for r in await cur.fetchall()]
    finally:
        await db.close()

async def get_group_users(chat_id:int):
    db=await get_db()
    try:
        cur=await db.execute("""
            SELECT gu.chat_id,gu.user_id,gu.notify_at,
                   u.first_name,u.last_name,u.username
            FROM group_users gu
            JOIN users u ON u.user_id=gu.user_id
            WHERE gu.chat_id=?
        """,(chat_id,))
        return [dict(r) for r in await cur.fetchall()]
    finally:
        await db.close()

async def get_group_user(chat_id:int,user_id:int):
    db=await get_db()
    try:
        cur=await db.execute("""
            SELECT * FROM group_users WHERE chat_id=? AND user_id=?
        """,(chat_id,user_id))
        row=await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()

async def delete_group_user(chat_id:int,user_id:int):
    db=await get_db()
    try:
        await db.execute("DELETE FROM group_users WHERE chat_id=? AND user_id=?",(chat_id,user_id))
        await db.commit()
    finally:
        await db.close()

async def update_group_user_notify_at(chat_id:int,user_id:int,notify_at:str|None):
    db=await get_db()
    try:
        await db.execute("""
            UPDATE group_users SET notify_at=?
            WHERE chat_id=? AND user_id=?
        """,(notify_at,chat_id,user_id))
        await db.commit()
    finally:
        await db.close()