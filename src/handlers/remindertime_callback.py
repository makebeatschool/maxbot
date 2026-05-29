from core.bot import dp
from services.users import set_reminder_time
from config import  Write_Test, check_list
from services.preload_file import attachment


def parse_timer(payload: str) -> int:
    mapping = {
        "24h": 24 * 60 * 60,
        "1h": 60 * 60,
        "15m": 15 * 60
    }
    return mapping.get(payload, 0)

@dp.message_callback()
async def on_timer_select(event):
    attachment = event.bot.checklist_attachment
    user_id = event.from_user.user_id
    payload = event.callback.payload
    seconds = parse_timer(payload)
    await set_reminder_time(user_id, seconds)
    await event.message.answer(Write_Test)
    if attachment:
        await event.bot.send_message( chat_id=event.chat.chat_id,
            text=check_list, attachments=[attachment]
        )
    else:
        await event.message.answer("Чек-лист временно недоступен")