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
    finally: await db.close()
    print(f"updated: {updated}")

async def update_groups_data():
    conn = await get_db()
    try:
        updated = 0
        updates = {
            -72734266116637: {"curator_id": 9419001},
            -72256072195352: {"curator_id": 9419001},
            -72160299845636: {"curator_id": 9419001},
            -72160629229572: {"teacher_id": 205787955},
            -72160608978948: {"teacher_id": 205787955},
            -72160395134980: {"teacher_id": 205787955},
            -72160366495748: {"teacher_id": 205787955},
            -72160351946756: {"teacher_id": 205787955},
            -72160267798532: {"teacher_id": 205787955},
            -72160228018180: {"teacher_id": 205787955},
            -72160213207044: {"teacher_id": 205787955},
            -72160183846916: {"teacher_id": 205787955},
            -72160171395076: {"teacher_id": 205787955},
            -72160158156804: {"teacher_id": 205787955},
            -72160145115140: {"teacher_id": 205787955},
            -72160380389380: {"teacher_id": 205787955},
        }
        for chat_id, fields in updates.items():
            if "curator_id" in fields:
                cur = await conn.execute(
                    "UPDATE chat_groups SET curator_id=? WHERE chat_id=?",
                    (fields["curator_id"], chat_id)
                )
                updated += cur.rowcount
            if "teacher_id" in fields:
                cur = await conn.execute(
                    "UPDATE chat_groups SET teacher_id=? WHERE chat_id=?",
                    (fields["teacher_id"], chat_id)
                )
                updated += cur.rowcount
        await conn.commit()
        print(f"updated: {updated}")
    finally:
        await conn.close()