
from core.bot import router
from services.users import add_user
from keyboards.calendar import weekdays_keyboard
from maxapi import F

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
    added = await add_user(
        user_id=event.from_user.user_id,
        chat_id=event.chat.chat_id,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
    )
    if added:
        await event.bot.send_message(
            chat_id=event.chat.chat_id,
            text="Выберите день недели",
            attachments=[weekdays_keyboard()]
        )
    else:
        await event.message.answer("Вы уже записаны")