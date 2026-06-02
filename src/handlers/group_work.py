from env import id_bot
from maxapi.types import UserAdded
from core.bot import dp, router
from texts import GROUP_KID_SCENARIO
from keyboards.start import start_from_group_keyboard
from config import CURATORS_ID, TEACHERS_ID
from services.db_services.user_group_service import remove_user_from_group, add_user_to_group, update_time_for_notify, get_all_users_grou_activity
from services.db_services.group_service import set_group, delete_group_and_all_notify
from services.db_services.users_service import add_user_from_group

@dp.user_added()
async def on_user_added(event: UserAdded):
    user = event.user
    group_name = (event.chat.title or "").lower()
    await add_user_from_group(event.chat.chat_id, user.user_id, user.last_name)
    await add_user_to_group(event.chat.chat_id, user.user_id)
    if user.user_id in CURATORS_ID:
        await set_group(event.chat.chat_id, event.chat.title, user.user_id)
        return
    if user.user_id in TEACHERS_ID:
        await set_group(event.chat.chat_id, event.chat.title, user.user_id)
        return
    full_name = user.first_name
    # if user.last_name:
    #     full_name += f" {user.last_name}"
    if "родители" in group_name:
        await event.bot.send_message(
            chat_id=event.chat.chat_id,
            text=f"[{full_name}](max://user/{user.user_id})\n hello",
            format="markdown",
            attachments=[start_from_group_keyboard("parent")]
        )
    else:
        await event.bot.send_message(
            chat_id=event.chat.chat_id,
            text=GROUP_KID_SCENARIO.format(
                name=f'[{full_name}](max://user/{user.user_id})', 
                link=f'https://max.ru/{id_bot}?start=kid',
                curator=f'[{full_name}](max://user/{user.user_id})',
                teacher=f'[{full_name}](max://user/{user.user_id})',),
            format="markdown",
        )

@dp.user_removed()
async def on_user_removed(event):
    user = event.user
    await remove_user_from_group(user.user_id, event.chat.chat_id)

@router.message_created()
async def on_message(event):
    if event.chat.type != "group": return
    user = event.from_user
    await update_time_for_notify(event.chat.chat_id, user.user_id)

@dp.bot_added()
async def on_bot_added(event):
    chat_id = event.chat.chat_id
    chat_members = await event.bot.get_chat_members(chat_id)
    me = await event.bot.get_me_from_chat(chat_id)
    curator_id = None
    members_to_process = []
    for m in chat_members.members:
        if m.is_bot or m.is_admin: continue
        if m.user_id in CURATORS_ID:
            curator_id = m.user_id
        members_to_process.append(m)
    await set_group(chat_id, event.chat.title, curator_id)
    for m in members_to_process:
        await add_user_from_group(chat_id, m.user_id, m.first_name, m.last_name)
        await update_time_for_notify(chat_id, m.user_id)
    if not me.is_admin:
        await event.bot.send_message(
            chat_id=chat_id,
            text="Бот добавлен в группу, не забудьте сделать его администратором."
        )


@dp.bot_removed()
async def on_bot_removed(event):
    users = await get_all_users_grou_activity()
    for user in users: 
        await remove_user_from_group(user["user_id"], event.chat_id)
    await delete_group_and_all_notify(event.chat_id)