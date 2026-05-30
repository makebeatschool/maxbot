from db.database import get_db

async def upsert_user_lesson(user_id: int, lesson_date: str = "None-None", next_message_time: str = None):
    db = await get_db()
    try:
        await db.execute("""
            INSERT INTO user_lessons(user_id, lesson_date, next_message_time)
            VALUES(?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                lesson_date=excluded.lesson_date,
                next_message_time=excluded.next_message_time
        """, (user_id, lesson_date, next_message_time))
        await db.commit()
    finally:
        await db.close()

async def get_all_lesson_reminders():
    db = await get_db()
    try:
        cur = await db.execute("""
            SELECT l.user_id, l.lesson_date, l.next_message_time,
                u.chat_id, u.first_name
            FROM user_lessons l
            JOIN users u ON u.user_id = l.user_id
        """)
        rows = await cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()

async def get_user_lesson(user_id: int):
    db = await get_db()
    try:
        cur = await db.execute("SELECT * FROM user_lessons WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()

async def delete_user_lesson(user_id: int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM user_lessons WHERE user_id=?", (user_id,))
        await db.commit()
    finally:
        await db.close()