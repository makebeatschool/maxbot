from core.bot import dp
from texts import TITLE_START_BTN
from keyboards.start import start_keyboard
from services.sender import safe_send

@dp.bot_started()
async def on_bot_started(event):
    await safe_send(
        chat_id=event.chat_id,
        text=TITLE_START_BTN,
        attachments=[start_keyboard()]
    )