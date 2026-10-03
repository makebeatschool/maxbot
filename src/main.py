import asyncio
from core.bot import bot, dp

import core.routers
import handlers.messages
import handlers.start
import handlers.callbacks
import handlers.group_work
import handlers.calendar
import handlers.blocked

from db.database import init_db
# from db.migrations import reset_notify_for_parent_groups
# from db.migrations import set_teacher_for_groups
from services.reminder import reminder_worker
from services.preload_file import preload_file
from db.database import save_all_tables_to_file

# from services.db_services.trial_reg_service import send_tg_trial_report

async def main():
    await preload_file(bot)
    await init_db()
    # today = "2026-06-09"
    # await send_tg_trial_report(today)
    # await set_curator_for_groups()
    # await set_teacher_for_groups()
    asyncio.create_task(reminder_worker(bot))
    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()
        await bot.session.close()

async def write_backup():
    try:
        await save_all_tables_to_file()
        print("write file is done")
    except: print("not write file")

if __name__ == "__main__":
    asyncio.run(write_backup())
    try:
        print("Bot started...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")    
    asyncio.run(write_backup())


# ======= тз-да-похуй-но-надо =========
# 1. заменить принты на что-то 
# 2. переделать работу с бд в ооп
