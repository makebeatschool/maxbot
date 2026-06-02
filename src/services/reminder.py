import asyncio
from datetime import datetime
from config import MOSCOW
from texts import REMINDER_TEXT
from services.db_services.trial_service import delete_trial_for_user, get_all_trials
from services.db_services.lesson_service import get_all_lessons, calculate_next_send_time
from services.db_services.user_group_service import get_all_users_grou_activity, get_message_for_group

async def reminder_worker(bot):
    while True:
        try:
            await process_trial_reminders(bot)
            await process_lesson_reminders(bot)
            await process_group_reminders(bot)
        except Exception as e:
            print(f"Ошибка reminder_worker: {e}")

        await asyncio.sleep(10)


async def process_trial_reminders(bot):
    now = datetime.now(MOSCOW)
    reminders = await get_all_trials()
    for r in reminders:
        send_time = r.get("send_time")
        if not send_time:
            continue
        try:
            remind_time = datetime.fromisoformat(send_time)
            if remind_time.tzinfo is None:
                remind_time = remind_time.replace(tzinfo=MOSCOW)
            else:
                remind_time = remind_time.astimezone(MOSCOW)
        except ValueError:
            await delete_trial_for_user(r["user_id"])
            continue
        if now >= remind_time:
            name = r.get("first_name") or "Здравствуйте"
            text = f"{name}, {REMINDER_TEXT}"
            try:
                await bot.send_message( chat_id=r["chat_id"], text=text)
                await delete_trial_for_user(r["user_id"])
            except Exception as e:
                print(f"Ошибка отправки trial {r['user_id']}: {e}")

async def process_lesson_reminders(bot):
    now = datetime.now(MOSCOW)
    lessons = await get_all_lessons()
    for r in lessons:
        send_time = r.get("next_message_time")
        if not send_time: continue
        try:
            remind_time = datetime.fromisoformat(send_time)
            if remind_time.tzinfo is None:
                remind_time = remind_time.replace(tzinfo=MOSCOW)
            else:
                remind_time = remind_time.astimezone(MOSCOW)
        except ValueError:
            continue
        if now >= remind_time:
            name = r.get("first_name") or "Здравствуйте"
            text = f"{name}, {REMINDER_TEXT}"
            try:
                await bot.send_message(chat_id=r["chat_id"], text=text)
                await calculate_next_send_time(r["user_id"])
            except Exception as e:
                print(f"Ошибка отправки lesson {r['user_id']}: {e}")

async def process_group_reminders(bot):
    now = datetime.now(MOSCOW)
    userActivity = await get_all_users_grou_activity()
    for r in userActivity:
        send_time = r.get("notify_at")
        if not send_time: continue
        try:
            remind_time = datetime.fromisoformat(send_time)
            if remind_time.tzinfo is None:
                remind_time = remind_time.replace(tzinfo=MOSCOW)
            else:
                remind_time = remind_time.astimezone(MOSCOW)
        except ValueError: continue
        if now >= remind_time:
            chat_id, text, Gladishew_id, text_to_Gladishew = await get_message_for_group(r.get("chat_id"), r.get("user_id"))
            try:
                await bot.send_message(chat_id=chat_id, text=text, format="markdown")
                await bot.send_message(chat_id=Gladishew_id, text=text_to_Gladishew, format="markdown")
            except Exception as e:
                print(f"Ошибка отправки group {r['user_id']}: {e}")

