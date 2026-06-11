import re
from env import id_bot
from maxapi.types import UserAdded
from core.bot import dp, router, bot
from texts import GROUP_KID_SCENARIO, GROUP_PARENT_SCENARIO, GLADISHEW_TEXTS
from keyboards.start import start_from_group_keyboard
from config import CURATORS_ID, TEACHERS_ID, MANAGERS_ID, ANTON_GLADISHEW
from services.db_services.user_group_service import remove_user_from_group, add_user_to_group, update_time_for_notify, get_all_users_grou_activity
from services.db_services.group_service import (set_group, get_group_by_id, delete_group_and_all_notify, calculate_next_time_dz)
from services.db_services.users_service import add_user_from_group, get_user_or_none

async def format_group_user(user_id, empty_text):
    if not user_id: return empty_text
    user = await get_user_or_none(user_id)
    if not user: return empty_text
    return f'[{user["first_name"]}](max://user/{user_id})'

def extract_number(name):
    m = re.search(r"\d+", str(name))
    return int(m.group()) if m else None

async def send_message_to_Gladishev(group_name, admin_id, user_name):
    Gladishev = await get_user_or_none(ANTON_GLADISHEW['id'])
    if not Gladishev : return
    admin = await get_user_or_none(admin_id)
    try:
        if admin:
            await bot.send_message(chat_id=Gladishev.get("chat_id", ""), text=GLADISHEW_TEXTS['added']
                                .format( name_curator=admin.get("first_name", ""), 
                                    num = extract_number(group_name), name=user_name ), format="markdown")        
        else:
            await bot.send_message(chat_id=Gladishev.get('chat_id',""), text=GLADISHEW_TEXTS['added_from_lik']
                                .format( num = extract_number(group_name), name=user_name ), format="markdown")
    except: return

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
    await send_message_to_Gladishev(event.chat.title, event.inviter_id, event.user.first_name)

@dp.user_added()
async def on_user_added(event: UserAdded):
    user = event.user
    try:
        await add_user_from_group(event.chat.chat_id, user.user_id, user.last_name)
        await add_user_to_group(event.chat.chat_id, user.user_id)
        if user.user_id in CURATORS_ID:
            await set_group(event.chat.chat_id, event.chat.title, curator_id=user.user_id)
            return
        if user.user_id in TEACHERS_ID:
            await set_group(event.chat.chat_id, event.chat.title, teacher_id=user.user_id)
            return
        if user.user_id in MANAGERS_ID: return
    except: pass
    await hello_user(event, event.user)
    
@dp.user_removed()
async def on_user_removed(event):
    user = event.user
    await remove_user_from_group(user.user_id, event.chat.chat_id)

# @router.message_created()
async def on_group_message(event):
    user = event.from_user
    await update_time_for_notify(event.chat.chat_id, user.user_id)
    # await calculate_next_time_dz(event.chat.chat_id)
    if event.from_user.user_id in CURATORS_ID:
        text = event.message.body.text
        if text and "#домашка" in text:
            await calculate_next_time_dz(event.chat.chat_id)

@dp.bot_added()
async def on_bot_added(event):
    chat_id = event.chat.chat_id
    chat_members = await event.bot.get_chat_members(chat_id)
    me = await event.bot.get_me_from_chat(chat_id)
    curator_id = None
    teacher_id = None
    members_to_process = []
    for m in chat_members.members:
        is_important_user = False
        if m.user_id in CURATORS_ID:
            curator_id = m.user_id
            is_important_user = True
        if m.user_id in TEACHERS_ID:
            teacher_id = m.user_id
            is_important_user = True
        if (m.is_bot or m.is_admin) and not is_important_user: continue
        members_to_process.append(m)
    await set_group(chat_id, event.chat.title, curator_id, teacher_id)
    for m in members_to_process:
        await add_user_from_group(chat_id, m.user_id, m.first_name, m.last_name)
        await update_time_for_notify(chat_id, m.user_id)
        if m.user_id in CURATORS_ID or m.user_id in TEACHERS_ID: continue
        # await hello_user(event, m)
    if not me.is_admin:
        await event.bot.send_message( chat_id=chat_id,
            text="Бот добавлен в группу, не забудьте сделать его администратором.")


@dp.bot_removed()
async def on_bot_removed(event):
    users = await get_all_users_grou_activity()
    for user in users: 
        await remove_user_from_group(user["user_id"], event.chat_id)
    await delete_group_and_all_notify(event.chat_id)