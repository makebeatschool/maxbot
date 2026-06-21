import asyncio
from datetime import datetime, timedelta
from config import MOSCOW, WEEK
from texts import REMINDER_TEXT, REMINDER_TEXTS, REMINDER_TEXT_PROBNOE
from services.db_services.trial_service import delete_trial_for_user, get_all_trials
from services.db_services.lesson_service import get_all_lessons, calculate_next_send_time, disable_lesson_reminder
from services.db_services.user_group_service import get_all_users_grou_activity, get_message_for_group, update_time_for_notify
from services.db_services.group_service import get_all_group_records, calculate_next_time_dz, get_message_for_dz
from services.db_services.trial_reg_service import send_tg_trial_report
from services.db_services.service_info_servise import get_service, set_service

async def reminder_worker(bot):
    while True:
        try:
            now = datetime.now(MOSCOW)
            await process_trial_reminders(bot, now)
            await process_lesson_reminders(bot, now)
            await process_group_reminders(bot, now)
            await process_group_homework(bot, now)
            await send_tg_report(now)
        except Exception as e:
            print(f"Ошибка reminder_worker: {e}")
        await asyncio.sleep(10)

def calculate_remind_time(send_time):
    try:
        remind_time = datetime.fromisoformat(send_time)
        if remind_time.tzinfo is None:
            remind_time = remind_time.replace(tzinfo=MOSCOW)
        else:
            remind_time = remind_time.astimezone(MOSCOW)
        return remind_time
    except ValueError: return False

async def process_trial_reminders(bot, now):
    reminders = await get_all_trials()
    for r in reminders:
        try:
            send_time = r.get("send_time")
            if not send_time: continue
            remind_time = calculate_remind_time(send_time)
            if not remind_time: continue
            if now >= remind_time:
                name = r.get("first_name") or "Здравствуйте"
                text = f"{name}, {REMINDER_TEXT_PROBNOE}"
                try:
                    if r["chat_id"] and (r["chat_id"]>0):
                        await bot.send_message( chat_id=r["chat_id"], text=text)
                    await delete_trial_for_user(r["user_id"])
                except Exception as e:
                    print(f"Ошибка отправки trial {r['user_id']}: {e}")
        except Exception as e:
            print(f"Ошибка отправки trial {r['user_id']}: {e}")

def reminder_step(obj: dict) -> str:
    msg_dt = datetime.fromisoformat(obj['next_message_time']).astimezone(MOSCOW)
    day_s, hm = obj['lesson_date'].split('-')
    h, m = map(int, hm.split(':'))
    target_wd = WEEK[day_s.lower()]
    cur = msg_dt.date()
    days_ahead = (target_wd - cur.weekday()) % 7
    lesson_dt = datetime.combine(cur + timedelta(days=days_ahead), datetime.min.time(), tzinfo=MOSCOW).replace(hour=h, minute=m)
    if lesson_dt <= msg_dt: lesson_dt += timedelta(days=7)
    diff = lesson_dt - msg_dt
    if timedelta(hours=1) < diff < timedelta(hours=24):
        return '24h'
    if timedelta(minutes=15) < diff <= timedelta(hours=1):
        return '1h'
    return '15m'
async def process_lesson_reminders(bot, now):
    lessons = await get_all_lessons()
    for r in lessons:
        try:
            send_time = r.get("next_message_time")
            if not send_time: continue
            remind_time = calculate_remind_time(send_time)
            if not remind_time: continue
            if now >= remind_time:
                name = r.get("first_name") or "Здравствуйте"
                text = f"{name}, {REMINDER_TEXT.format(time=REMINDER_TEXTS[reminder_step(r)])}"
                try:
                    if r and (r["chat_id"]>0):
                        await bot.send_message(chat_id=r["chat_id"], text=text)
                    await calculate_next_send_time(r["user_id"])
                except Exception as e:
                    err = str(e)
                    if "chat.denied" in err or "dialog.suspended" in err:
                        await disable_lesson_reminder(r["user_id"])
                    print(f"Ошибка отправки lesson {r['user_id']}: {e}")
        except Exception as e:
            print(f"Ошибка отправки lesson {r['user_id']}: {e}")

async def process_group_reminders(bot, now):
    userActivity = await get_all_users_grou_activity()
    for r in userActivity:
        try:
            send_time = r.get("notify_at")
            if not send_time: continue
            remind_time = calculate_remind_time(send_time)
            if not remind_time: continue
            if now >= remind_time:
                result = await get_message_for_group(r.get("chat_id"), r.get("user_id"))
                if not result: continue
                chat_id, text, Gladishew_id, text_to_Gladishew = result
                try:
                    if chat_id and (chat_id > 0):
                        await update_time_for_notify(r.get("chat_id"), r.get("user_id"))
                    await bot.send_message(chat_id=chat_id, text=text, format="markdown")
                    if Gladishew_id > 0:
                        await bot.send_message(chat_id=Gladishew_id, text=text_to_Gladishew, format="markdown")
                except Exception as e:
                    print(f"Ошибка отправки group {r['user_id']}: {e}")
        except Exception as e:
            print(f"Ошибка отправки group {r['user_id']}: {e}")


async def process_group_homework(bot, now):
    homework_time = await get_all_group_records()
    for r in homework_time:
        try:
            send_time = r.get("next_message_time")
            if not send_time: continue
            remind_time = calculate_remind_time(send_time)
            if not remind_time: continue
            if now >= remind_time:
                chat_id, text, Gladishew_id, text_to_Gladishew = await get_message_for_dz(r.get("title"), r.get("curator_id"))
                try:
                    await calculate_next_time_dz(r.get("chat_id"))
                    if chat_id and (chat_id>0):
                        await bot.send_message(chat_id=chat_id, text=text, format="markdown")
                    if Gladishew_id > 0:
                        await bot.send_message(chat_id=Gladishew_id, text=text_to_Gladishew, format="markdown")  
                except Exception as e:
                    print(f"Ошибка отправки group {r['user_id']}: {e}")
        except Exception as e:
            print(f"Ошибка отправки group {r['user_id']}: {e}")
            
async def send_tg_report(now):
    # if ((now.hour, now.minute) <= (12, 28)) or ((now.hour, now.minute) >= (12, 30)):return
    try:
        if ((now.hour, now.minute) <= (21, 31)) or ((now.hour, now.minute) >= (21, 40)):return
        today = now.date().isoformat()
        next_send_date = await get_service("next_trial_report_date")
        if next_send_date and next_send_date > today:return
        ok = await send_tg_trial_report(today)
        if not ok:return
        tomorrow = (now.date() + timedelta(days=1)).isoformat()
        await set_service("next_trial_report_date", tomorrow)
    except Exception as e:
        print(f"Ошибка отправки tg: {e}")