from core.bot import dp
from services.db_services.users_service import remove_user_by_chat_id

@dp.bot_stopped()
async def on_bot_stopped(event):
    await remove_user_by_chat_id(event.from_user.user_id)
    # print(f"Бот остановлен: {event.chat_id}")

@dp.bot_removed()
async def on_bot_removed(event):
    await remove_user_by_chat_id(event.from_user.user_id)
    # print(f"Бот удалён: {event.chat_id}")

@dp.dialog_removed()
async def on_dialog_removed(event):
    await remove_user_by_chat_id(event.from_user.user_id)
    # print(f"Диалог удалён: {event.chat_id}")