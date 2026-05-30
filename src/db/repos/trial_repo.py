from db.database import get_db

async def upsert_trial_reminder(user_id: int, send_time: str):
    db = await get_db()
    try:
        await db.execute("""
            INSERT INTO trial_reminders(user_id, send_time)
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET send_time=excluded.send_time
        """, (user_id, send_time))
        await db.commit()
    finally:
        await db.close()

async def get_all_trial_reminders():
    db = await get_db()
    try:
        cur = await db.execute("""
            SELECT t.user_id, t.send_time, u.chat_id, u.first_name
            FROM trial_reminders t
            JOIN users u ON u.user_id = t.user_id
        """)
        rows = await cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()

async def get_trial_reminder(user_id: int):
    db = await get_db()
    try:
        cur = await db.execute("SELECT * FROM trial_reminders WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()

async def delete_trial_reminder(user_id: int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM trial_reminders WHERE user_id=?", (user_id,))
        await db.commit()
    finally:
        await db.close()