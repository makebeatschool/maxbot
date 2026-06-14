from db.database import get_db

async def migrate_chat_groups():
    conn = await get_db()
    async with conn.execute("PRAGMA table_info(chat_groups)") as cur:
        rows = await cur.fetchall()
        cols = [r[1] for r in rows]
    if "next_message_time" not in cols:
        await conn.execute( "ALTER TABLE chat_groups ADD COLUMN next_message_time TEXT")
        await conn.commit()
        print("migration: next_message_time added")
    await conn.close()

async def reset_notify_for_parent_groups():
    db = await get_db()
    updated = 0

    try:
        cur = await db.execute("SELECT chat_id, title FROM chat_groups")
        groups = await cur.fetchall()

        for g in groups:
            if "родители" in g["title"].lower():
                cur = await db.execute(
                    "UPDATE group_users SET notify_at=NULL WHERE chat_id=?",
                    (g["chat_id"],)
                )
                updated += cur.rowcount

        await db.commit()

    finally:
        await db.close()

    print(f"updated: {updated}")