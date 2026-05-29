from core.bot import router
from keyboards.calendar import open_weekdays_keyboard, time_keyboard, weekdays_keyboard, open_time_keyboard
from maxapi import F
from services.users import set_reminder_time
from texts import WRITE_TEST, CHECK_LIST
from config import DAYS


@router.message_callback(F.callback.payload == "change_weekday")
async def open_weekdays(event):
    await event.bot.send_message( chat_id=event.chat.chat_id,
            text="Выберите день недели",attachments=[weekdays_keyboard()] )
@router.message_callback(F.callback.payload == "change_time")
async def open_time(event):
    await event.bot.send_message( chat_id=event.chat.chat_id,
            text="Выберите время", attachments=[time_keyboard()] )


@router.message_callback(F.callback.payload.startswith("weekday:"))
async def weekday(event):
    parts = event.callback.payload.split(":")
    if len(parts) != 2: return
    _, day = parts
    weekdays = dict((value, text) for text, value in DAYS)
    if day not in weekdays: return
    flag = await set_reminder_time( user_id=event.from_user.user_id, day=day )
    if flag == "updated":
        await event.bot.send_message( chat_id=event.chat.chat_id,
            text=f"Напоминание обновлено на {weekdays[day]}",
            attachments=[open_time_keyboard()] )
    elif flag == "created":
        await event.bot.send_message( chat_id=event.chat.chat_id,
            text=f"Теперь выберите время",
            attachments=[time_keyboard()])

@router.message_callback(F.callback.payload.startswith("time:"))
async def time(event):
    parts = event.callback.payload.split(":")
    if len(parts) != 3 and len(parts) != 2: return
    if len(parts) == 3:
        _, h, m = parts
        t = f"{h.zfill(2)}:{m.zfill(2)}"
    else: 
        _, t = parts
    if ":" not in t: return
    flag = await set_reminder_time( user_id=event.from_user.user_id, time=t )
    if flag == "updated":
        await event.bot.send_message(
            chat_id=event.chat.chat_id,
            text=f"Напоминание обновлено на {t}",
            attachments=[open_weekdays_keyboard()]
        )
    elif flag == "created":
        attachment = event.bot.checklist_attachment
        await event.message.answer(WRITE_TEST)
        if attachment:
            await event.bot.send_message( chat_id=event.chat.chat_id,
                text=CHECK_LIST, attachments=[attachment] )
        else: await event.message.answer("Чек-лист временно недоступен")