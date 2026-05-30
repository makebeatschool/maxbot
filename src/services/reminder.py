import asyncio
from datetime import datetime

from services.db_services.users_service import calculate_next_send_time
from config import MOSCOW
from texts import REMINDER_TEXT
from services.db_services.trial_service import delete_trial_for_user, get_all_trial_reminders
from services.db_services.lesson_service import get_all_lesson_reminders

async def reminder_worker(bot):
    while True:
        try:
            await process_trial_reminders(bot)
            await process_lesson_reminders(bot)

        except Exception as e:
            print(f"Ошибка reminder_worker: {e}")

        await asyncio.sleep(10)


async def process_trial_reminders(bot):
    now = datetime.now(MOSCOW)
    reminders = await get_all_trial_reminders()
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
    lessons = await get_all_lesson_reminders()

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
# async def reminder_worker(bot):
#     while True:
#         try:
#             now = datetime.now(MOSCOW)
#             async with file_lock:
#                 users = load_users()
#             for key, user in users.items():
#                 send_time = user.get("send_message")
#                 if not send_time: continue
#                 try:
#                     remind_time = datetime.fromisoformat(send_time)
#                     if remind_time.tzinfo is None:
#                         remind_time = remind_time.replace(tzinfo=MOSCOW)
#                     else:
#                         remind_time = remind_time.astimezone(MOSCOW)
#                 except:continue
#                 if now >= remind_time:
#                     name = user.get("first_name") or "Здравствуйте"
#                     text = f"{name}, {REMINDER_TEXT}"
#                     try:
#                         await calculate_next_send_time(user.get("user_id"))
#                         await bot.send_message(chat_id=user["chat_id"], text=text)
#                     except Exception as e:
#                         pass
#                         # print(f"Ошибка отправки {key}: {e}")
#             # if keys_to_delete:
#             #     async with file_lock:
#             #         latest_users = load_users()
#             #         for key in keys_to_delete:
#             #             latest_users.pop(key, None)
#             #         save_users(latest_users)
#         except Exception as e:
#             pass
#             # print(f"Ошибка reminder_worker: {e}")

#         await asyncio.sleep(10)