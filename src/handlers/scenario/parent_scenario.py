import asyncio
from texts import LS_PARENT_SCENARIO
from services.sender import safe_send
from keyboards.calendar import weekdays_keyboard
from env import id_bot

async def parent_steps_before_date(event):
    await safe_send( chat_id=event.chat.chat_id, 
                        text=LS_PARENT_SCENARIO['step1'].format(name=f"[{event.from_user.first_name}](max://user/{event.from_user.user_id})"), format="markdown" )
    await safe_send( chat_id=event.chat.chat_id,
            text=LS_PARENT_SCENARIO['step2'], attachments=[weekdays_keyboard()] )

async def parent_steps_after_date(event):
    await safe_send( chat_id=event.chat.chat_id, 
                        text=LS_PARENT_SCENARIO['step3'].format(link=f"https://max.ru/{id_bot}?start=kid"))
    asyncio.create_task(parent_handler(event.chat.chat_id))

async def parent_handler(chat_id: int):
    await asyncio.sleep(180)
    await safe_send(chat_id=chat_id, text=LS_PARENT_SCENARIO['step4'])
    await safe_send(chat_id=chat_id, text=LS_PARENT_SCENARIO['step5'])