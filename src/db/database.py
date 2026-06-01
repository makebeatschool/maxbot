import json
import aiosqlite
from config import DB_PATH, SCHEMA_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys=ON")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            await db.executescript(f.read())
        await db.commit()

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys=ON")
    return db

async def export_all_tables_to_json():
    db = await get_db()
    try:
        cur = await db.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        tables = [r["name"] for r in await cur.fetchall()]

        result = {}
        for table in tables:
            cur = await db.execute(f"SELECT * FROM {table}")
            rows = await cur.fetchall()
            result[table] = [dict(row) for row in rows]

        return result
    finally:
        await db.close()

async def export_all_tables_json_string():
    data = await export_all_tables_to_json()
    return json.dumps(data, ensure_ascii=False, indent=2)

async def save_all_tables_to_file(path="db_dump.json"):
    data = await export_all_tables_to_json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
