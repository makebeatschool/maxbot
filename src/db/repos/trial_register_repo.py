from db.database import get_db
from datetime import datetime, timedelta

def build_full_name(user):
    return " ".join(x for x in [user.first_name, user.last_name] if x) or "Без имени"

async def save_trial_registration(user_id: int, full_name: str, now: datetime):
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT OR IGNORE INTO trial_registrations (user_id, full_name, reg_date)
            VALUES (?, ?, ?)
            """,
            (user_id, full_name, now.date().isoformat())
        )
        await db.commit()
    finally: await db.close()

async def cleanup_old_trial_records(now: datetime):
    cutoff = (now.date() - timedelta(days=40)).isoformat()
    db = await get_db()
    try:
        await db.execute(
            "DELETE FROM trial_registrations WHERE reg_date < ?",
            (cutoff,)
        )
        await db.commit()
    finally: await db.close()

async def get_trial_count_by_date(report_date: str) -> int:
    db = await get_db()
    try:
        cur = await db.execute(
            "SELECT COUNT(*) FROM trial_registrations WHERE reg_date = ?",
            (report_date,)
        )
        row = await cur.fetchone()
        return int(row[0] or 0)
    finally: await db.close()