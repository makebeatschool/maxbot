from env import id_bot
from maxapi.types import UserAdded
from core.bot import dp, router
from texts import GROUP_KID_SCENARIO, GROUP_PARENT_SCENARIO
from keyboards.start import start_from_group_keyboard
from config import CURATORS_ID, TEACHERS_ID
from services.db_services.user_group_service import remove_user_from_group, add_user_to_group, update_time_for_notify, get_all_users_grou_activity
from services.db_services.group_service import set_group, get_group_by_id, delete_group_and_all_notify
from services.db_services.users_service import add_user_from_group, get_user_or_none

async def format_group_user(user_id, empty_text):
    if not user_id: return empty_text
    user = await get_user_or_none(user_id)
    if not user: return empty_text
    return f'[{user["first_name"]}](max://user/{user_id})'

async def hello_user(event, user):
    group_name = (event.chat.title or "").lower()
    full_name = user.first_name
    if user.last_name:
        full_name += f" {user.last_name}"
    group = await get_group_by_id(event.chat.chat_id)
    curator = "Куратор ещё не назначен"
    teacher = "Преподаватель ещё не назначен"
    if group:
        curator = await format_group_user(group.get("curator_id"), curator)
        teacher = await format_group_user(group.get("teacher_id"), teacher)
    if "родители" in group_name.lower():
        await event.bot.send_message( chat_id=event.chat.chat_id,
            text=GROUP_PARENT_SCENARIO.format(
                name=f'[{full_name}](max://user/{user.user_id})',
                link = f'https://max.ru/{id_bot}?start=parent',
                curator=curator, teacher=teacher ),
            format="markdown",
            attachments=[start_from_group_keyboard("parent")]
        )
        return
    await event.bot.send_message(
        chat_id=event.chat.chat_id,
        text=GROUP_KID_SCENARIO.format(
            name=f'[{full_name}](max://user/{user.user_id})',
            link=f'https://max.ru/{id_bot}?start=kid',
            curator=curator, teacher=teacher, ),
        format="markdown",
    )

@dp.user_added()
async def on_user_added(event: UserAdded):
    user = event.user
    await add_user_from_group(event.chat.chat_id, user.user_id, user.last_name)
    await add_user_to_group(event.chat.chat_id, user.user_id)
    if user.user_id in CURATORS_ID:
        await set_group(event.chat.chat_id, event.chat.title, curator_id=user.user_id)
        return
    if user.user_id in TEACHERS_ID:
        await set_group(event.chat.chat_id, event.chat.title, teacher_id=user.user_id)
        return
    user = event.user
    await hello_user(event, user)
    
@dp.user_removed()
async def on_user_removed(event):
    user = event.user
    await remove_user_from_group(user.user_id, event.chat.chat_id)

# print(dir(router))
@router.message_created()
async def on_message(event):
    print("ddd")
    if event.chat.type != "group": return
    user = event.from_user
    await update_time_for_notify(event.chat.chat_id, user.user_id)
    print(event)
    group_name = event.chat.title

@dp.bot_added()
async def on_bot_added(event):
    chat_id = event.chat.chat_id
    chat_members = await event.bot.get_chat_members(chat_id)
    me = await event.bot.get_me_from_chat(chat_id)
    curator_id = None
    teacher_id = None
    members_to_process = []
    for m in chat_members.members:
        if m.is_bot or m.is_admin: continue
        if m.user_id in CURATORS_ID:
            curator_id = m.user_id
        if m.user_id in TEACHERS_ID:
            teacher_id = m.user_id
        members_to_process.append(m)
    await set_group(chat_id, event.chat.title, curator_id, teacher_id)
    for m in members_to_process:
        await add_user_from_group(chat_id, m.user_id, m.first_name, m.last_name)
        await update_time_for_notify(chat_id, m.user_id)
        if m.user_id in CURATORS_ID or m.user_id in TEACHERS_ID: continue
        await hello_user(event, m)
    if not me.is_admin:
        await event.bot.send_message( chat_id=chat_id,
            text="Бот добавлен в группу, не забудьте сделать его администратором.")


@dp.bot_removed()
async def on_bot_removed(event):
    users = await get_all_users_grou_activity()
    for user in users: 
        await remove_user_from_group(user["user_id"], event.chat_id)
    await delete_group_and_all_notify(event.chat_id)