from maxapi.types import MessageCreated
from core.bot import router
from texts import TEXT_START_BTN, CHECK_LIST
from handlers.group_work import on_group_message
from handlers.callbacks import on_contact

@router.message_created()
async def on_message(event: MessageCreated):
    if event.chat.type == "chat":
        await on_group_message(event)
    else:
        await on_contact(event)
    # text = (event.message.body.text or "").strip()
    # if text == TEXT_START_BTN:
    #     await event.message.answer(CHECK_LIST)