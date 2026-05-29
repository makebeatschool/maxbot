import asyncio
from datetime import datetime, timezone

from services.users import calculate_next_send_time, load_users, save_users
from config import file_lock, MOSCOW
from texts import REMINDER_TEXT


async def reminder_worker(bot):
    while True:
        try:
            now = datetime.now(MOSCOW)
            async with file_lock:
                users = load_users()
            for key, user in users.items():
                send_time = user.get("send_message")
                if not send_time: continue
                try:
                    remind_time = datetime.fromisoformat(send_time)
                    if remind_time.tzinfo is None:
                        remind_time = remind_time.replace(tzinfo=MOSCOW)
                    else:
                        remind_time = remind_time.astimezone(MOSCOW)
                except:continue
                if now >= remind_time:
                    name = user.get("first_name") or "Здравствуйте"
                    text = f"{name}, {REMINDER_TEXT}"
                    try:
                        await calculate_next_send_time(user.get("user_id"))
                        await bot.send_message(chat_id=user["chat_id"], text=text)
                    except Exception as e:
                        print(f"Ошибка отправки {key}: {e}")
            # if keys_to_delete:
            #     async with file_lock:
            #         latest_users = load_users()
            #         for key in keys_to_delete:
            #             latest_users.pop(key, None)
            #         save_users(latest_users)
        except Exception as e:
            print(f"Ошибка reminder_worker: {e}")

        await asyncio.sleep(10)