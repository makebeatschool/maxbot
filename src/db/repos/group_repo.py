from db.database import get_db

async def upsert_group(chat_id:int,title:str,curator_id:int|None=None, teacher_id:int|None=None, 
                       next_message_time:str|None=None):
    db=await get_db()
    try:
        await db.execute("""
            INSERT INTO chat_groups(chat_id,title,curator_id,teacher_id, next_message_time)
            VALUES(?,?,?,?,?)
            ON CONFLICT(chat_id) DO UPDATE SET
                title=excluded.title,
                curator_id=COALESCE(excluded.curator_id, chat_groups.curator_id),
                teacher_id=COALESCE(excluded.teacher_id, chat_groups.teacher_id),
                next_message_time=COALESCE(excluded.next_message_time, chat_groups.next_message_time)
        """,(chat_id,title,curator_id, teacher_id, next_message_time))
        await db.commit()
    finally:
        await db.close()

async def get_all_groups():
    db=await get_db()
    try:
        cur = await db.execute("""
            SELECT g.chat_id, g.title, g.curator_id, g.teacher_id, g.next_message_time
            FROM chat_groups g
        """)
        return [dict(r) for r in await cur.fetchall()]
    finally:
        await db.close()

async def get_group(chat_id:int):
    db=await get_db()
    try:
        cur=await db.execute("SELECT * FROM chat_groups WHERE chat_id=?",(chat_id,))
        row=await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()

async def delete_group(chat_id:int):
    db=await get_db()
    try:
        await db.execute("DELETE FROM group_users WHERE chat_id=?", (chat_id,))
        await db.execute("DELETE FROM chat_groups WHERE chat_id=?",(chat_id,))
        await db.commit()
    finally:
        await db.close()
