from keyboards.users_kayboard import yes_no_keyboard
from texts import LS_KID_SCENARIO
from services.sender import safe_send
from keyboards.calendar import weekdays_keyboard

async def kid_steps_before_date(event):
    await safe_send( chat_id=event.chat.chat_id, format="markdown",
            text=LS_KID_SCENARIO['step1'].format(name=f"[{event.from_user.first_name}](max://user/{event.from_user.user_id})") )
    await safe_send( chat_id=event.chat.chat_id, text=LS_KID_SCENARIO['step2'] )
    await safe_send( chat_id=event.chat.chat_id,
            text=LS_KID_SCENARIO['step3'], attachments=[yes_no_keyboard()] )
    
async def kid_steps_after_date(event):
    await safe_send( chat_id=event.chat.chat_id, text="время выбрано" )