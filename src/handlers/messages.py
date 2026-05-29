from maxapi.types import MessageCreated
from core.bot import dp
from texts import TEXT_START_BTN, CHECK_LIST


@dp.message_created()
async def on_message(event: MessageCreated):
    text = (event.message.body.text or "").strip()
    if text == TEXT_START_BTN:
        await event.message.answer(CHECK_LIST)