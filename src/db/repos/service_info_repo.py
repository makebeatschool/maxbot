from db.database import get_db

async def get_service_value(key: str):
    db = await get_db()
    try:
        cur = await db.execute("SELECT value FROM service_info WHERE key = ?", (key,))
        row = await cur.fetchone()
        return row["value"] if row else None
    finally:
        await db.close()

async def set_service_value(key: str, value: str):
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT INTO service_info (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value)
        )
        await db.commit()
    finally:
        await db.close()