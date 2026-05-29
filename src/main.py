import asyncio
from core.bot import bot, dp

import handlers.start
import handlers.callbacks
import handlers.group_work
import handlers.calendar
import handlers.messages
import handlers.blocked
from services.reminder import reminder_worker
from services.preload_file import preload_file


async def main():
    await preload_file(bot)
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


# 1) Создать в боте функцию автоматического напоминания о пробном занятии 
# за 24 часа, 1 час и 15 минут по мск времени.

# 2) Как только куратор (или менеджер) добавляет ученика в группу, 
# бот видит это событие и мгновенно отправляет в чат приветственное сообщение 
# (из заранее заготовленного шаблона), упоминая ребенка по имени, знакомясь с ним. 

# 3) При добавлении новых клиентов, 
# также им в лс присылается пакет материалов для подготовки к уроку. 
# Это тоже надо автоматизировать. 

# 4) Также, при добавлении родителя в группу родителей, 
# бот в лс ему должен отправлять список правил школы. 