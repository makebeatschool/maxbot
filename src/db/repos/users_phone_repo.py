from db.database import get_db


async def upsert_phone(user_id: int, phone: str):
    db = await get_db()
    try:
        await db.execute("""
            INSERT INTO users_phone(user_id, phone)
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET phone=excluded.phone
        """, (user_id, phone))
        await db.commit()
    finally:
        await db.close()

async def get_phone(user_id: int):
    db = await get_db()
    try:
        cur = await db.execute(
            "SELECT * FROM users_phone WHERE user_id=?",
            (user_id,)
        )
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def delete_phone(user_id: int):
    db = await get_db()
    try:
        await db.execute(
            "DELETE FROM users_phone WHERE user_id=?",
            (user_id,)
        )
        await db.commit()
    finally:
        await db.close()