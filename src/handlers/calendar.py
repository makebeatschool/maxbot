from datetime import datetime
from core.bot import dp, router
from keyboards.calendar import calendar_keyboard, time_keyboard
from maxapi import F
from services.users import set_reminder_time
from config import Write_Test, check_list



@router.message_callback(F.callback.payload.startswith("month:") | F.callback.payload.startswith("year:"))
async def change_month(event):
    _, y, m = event.callback.payload.split(":")
    await event.bot.edit_message(
        message_id=event.message.body.mid,
        text="Выберите дату",
        attachments=[calendar_keyboard(int(y), int(m))]
    )


@router.message_callback(F.callback.payload.startswith("day:"))
async def day(event):
    parts = event.callback.payload.split(":")
    if len(parts) != 4:
        return
    _, y, m, d = parts
    date = f"{d.zfill(2)}.{m.zfill(2)}.{y}"
    await set_reminder_time( user_id=event.from_user.user_id, day=date )
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text="Теперь выберите время",
        attachments=[time_keyboard()]
    )
@router.message_callback(F.callback.payload.startswith("today:"))
async def today(event):
    parts = event.callback.payload.split(":")
    if len(parts) != 4:
        return
    _, y, m, d = parts
    date = f"{d.zfill(2)}.{m.zfill(2)}.{y}"
    await set_reminder_time( user_id=event.from_user.user_id, day=date
    )
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text="Теперь выберите время",
        attachments=[time_keyboard()]
    )
    

@router.message_callback(F.callback.payload.startswith("time:"))
async def time(event):
    parts = event.callback.payload.split(":")
    if len(parts) != 3 and len(parts) != 2:
        return
    if len(parts) == 3:
        _, h, m = parts
        t = f"{h.zfill(2)}:{m.zfill(2)}"
    else:
        _, t = parts
    if ":" not in t:
        return
    await set_reminder_time( user_id=event.from_user.user_id, time=t )
    attachment = event.bot.checklist_attachment
    await event.message.answer(Write_Test)
    if attachment:
        await event.bot.send_message( chat_id=event.chat.chat_id,
            text=check_list, attachments=[attachment]
        )
    else:
        await event.message.answer("Чек-лист временно недоступен")