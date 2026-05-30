from maxapi import F
from core.bot import router
from keyboards.calendar import weekdays_keyboard
from services.amoservice import get_trial_datetime_by_phone
from services.db_services.users_service import get_user_or_none
from services.db_services.trial_service import write_trial_time
from services.db_services.user_phone_service import write_phone
from texts import WRITE_TEST, CHECK_LIST

def extract_phone_from_contact(payload):
    vcf_info = payload.vcf_info
    phone = None
    for line in vcf_info.splitlines():
        if line.startswith("TEL"):
            phone = line.split(":")[1]
            break
    return phone


@router.message_callback(F.callback.payload == "start_bot")
async def start(event):
    added = True
    if added:
        await event.bot.send_message(
            chat_id=event.chat.chat_id,
            text="Выберите день недели",
            attachments=[weekdays_keyboard()]
        )
    else:
        await event.message.answer("Вы уже записаны")

@router.message_created()
async def on_contact(event):
    attachments = event.message.body.attachments or []
    for att in attachments:
        if att.type == "contact":
            phone = extract_phone_from_contact(att.payload)
            user_id = event.from_user.user_id
            user = await get_user_or_none(user_id)
            if user['role'] == "trial":
                await write_phone(user_id, phone)
                send_message_date = get_trial_datetime_by_phone(phone)
                send_message_date = "2026-05-30 17:26:00+03:00"
                await write_trial_time(user_id, send_message_date)          
                attachment = event.bot.checklist_attachment
                await event.bot.send_message( chat_id=event.chat.chat_id,
                        text=f"Записали вас на {send_message_date}")
                await event.message.answer(WRITE_TEST)
                if attachment:
                    await event.bot.send_message( chat_id=event.chat.chat_id,
                        text=CHECK_LIST, attachments=[attachment] )
                else: await event.message.answer("Чек-лист временно недоступен")





# @router.message_callback(F.callback.payload == "start_trial_bot")
# async def start_trial(event):
#     print("trial")
#     attachments = event.message.body.attachments or []
#     for att in attachments:
#         if att.type == "contact":
#             payload = att.payload
#             phone = extract_phone_from_contact(payload)
#             await event.bot.send_message(
#                     chat_id=event.chat.chat_id,
#                     text=f"Записали вас на пробное {phone}",
#                 )