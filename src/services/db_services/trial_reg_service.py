from datetime import datetime, timedelta
from config import MOSCOW
from services.tg_sender import send_telegram_message
from db.repos.trial_register_repo import cleanup_old_trial_records, get_trial_count_by_date, save_trial_registration

async def send_tg_trial_report(report_date: str):
    await cleanup_old_trial_records(datetime.now(MOSCOW))
    count = await get_trial_count_by_date(report_date)
    text = (
        f"📊 <b>Отчёт из макс бота за {report_date}:</b>\n\n"
        f"Кол-во регистраций в боте на пробное: {count}\n"
    )
    return await send_telegram_message(text)

async def save_trial_reg(user_id, name):
    await save_trial_registration(user_id, name, datetime.now(MOSCOW))