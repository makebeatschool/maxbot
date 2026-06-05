import asyncio
from core.bot import bot, dp

import handlers.start
import handlers.callbacks
import handlers.group_work
import handlers.calendar
import handlers.messages
import handlers.blocked

from db.database import init_db
from services.reminder import reminder_worker
from services.preload_file import preload_file
from db.database import save_all_tables_to_file


async def main():
    await preload_file(bot)
    await init_db()
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
        # это для записи всей бд в джисон и просмтора что там есть
        asyncio.run(save_all_tables_to_file())


# ======= тз-да-похуй-но-надо =========
# 1. заменить принты на что-то 
# 2. переделать работу с бд в ооп
