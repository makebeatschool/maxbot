from maxapi.types import MessageCreated
from core.bot import router
from texts import TEXT_START_BTN, CHECK_LIST
from handlers.group_work import on_group_message
from handlers.callbacks import on_contact

import os, json
from datetime import datetime
from config import PARENT_DIR
LOG_PATH = os.path.join(PARENT_DIR, "events.log")

def log_event(event):
    data = {
        "time": datetime.now().isoformat(),
        "chat_id": getattr(event.chat, "chat_id", None),
        "chat_type": getattr(event.chat, "type", None),
        "chat_title": getattr(event.chat, "title", None),
        "user_id": getattr(event.from_user, "user_id", None),
        "text": getattr(getattr(event.message, "body", None), "text", None),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

@router.message_created()
async def on_message(event: MessageCreated):
    # log_event(event)
    if event.chat.type == "dialog":
        await on_contact(event)
    else:
        try: await on_group_message(event)
        except: pass
        # except Exception as e:
        #     with open(LOG_PATH, "a", encoding="utf-8") as f:
        #         f.write(f'{{"time":"{datetime.now().isoformat()}","error":"{e}"}}\n')
    # text = (event.message.body.text or "").strip()
    # if text == TEXT_START_BTN:
    #     await event.message.answer(CHECK_LIST)