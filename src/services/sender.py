from maxapi.exceptions import MaxApiError
from core.bot import bot

async def safe_send(chat_id: int, text: str, attachments=None):
    try:
        return await bot.send_message(
            chat_id=chat_id,
            text=text,
            attachments=attachments
        )
    # это надо починить чобы не было обшей ошибки (пока хз как)
    except MaxApiError as e:
        error_code = getattr(e, "code", None)
        raw = getattr(e, "raw", {}) or {}
        if ( error_code == 404 or raw.get("code") == "chat.not.found" ):
            return None
        raise

async def broadcast(chat_ids: list[int], text: str):
    for chat_id in chat_ids:
        await safe_send(chat_id, text)