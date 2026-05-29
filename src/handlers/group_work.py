from maxapi.types import UserAdded
from core.bot import dp, router
from texts import ADDED_TO_GROUP_TEXT
from keyboards.start import start_from_group_keyboard

@dp.user_added()
async def on_user_added(event: UserAdded):
    user = event.user
    full_name = user.first_name
    if user.last_name:
        full_name += f" {user.last_name}"
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text=f"[{full_name}](max://user/{user.user_id}) {ADDED_TO_GROUP_TEXT}",
        format="markdown",
        attachments=[start_from_group_keyboard()]
    )

@dp.user_removed()
async def on_user_removed(event):
    user = event.user
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text=f"Пользователь {user.first_name} покинул группу."
    )

@router.message_created()
async def on_message(event):
    user = event.from_user
    text = event.message.body.text
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text=f"{user.first_name} написал: {text}"
    )