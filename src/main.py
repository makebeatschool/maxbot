import asyncio
from core.bot import bot, dp

import handlers.start
import handlers.callbacks
import handlers.messages
import handlers.blocked
from services.reminder import reminder_worker


async def main():
    await handlers.callbacks.preload_file(bot)
    asyncio.create_task(reminder_worker(bot))
    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()
        await bot.session.close()

if __name__ == "__main__":
    try:
        print("Bot started...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")


                # name = user.get("first_name") or "Здравствуйте"
                # text = f"{name}, напоминание о пробном занятии. Ждём вас 🤍"