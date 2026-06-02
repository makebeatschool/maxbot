from core.bot import dp
from services.db_services.users_service import upsert_user, get_user_or_none
from handlers.scenario.kid_scenario import kid_steps_before_date
from keyboards.start import start_trial_keyboard
from handlers.scenario.parent_scenario import parent_steps_before_date
from services.sender import safe_send

# пробное занятие
# https://max.ru/id645485463201_1_bot?start=trial
# ребёнок
# https://max.ru/id645485463201_1_bot?start=kid
# родитель
# https://max.ru/id645485463201_1_bot?start=parent
# для регистрации чатов рабочих юзеров
# https://max.ru/id645485463201_1_bot
# не заплатил(в разработке)
# https://max.ru/id645485463201_1_bot?start=lead
# для теста (пока не трогать)
# https://max.ru/id645485463201_1_bot?start=admin
@dp.bot_started()
async def on_bot_started(event):
    role = "none"
    if event.payload == 'trial':
        role = "trial"
        await safe_send( chat_id=event.chat_id,
            text=f"пробное занятие", attachments=[start_trial_keyboard()] )
    elif event.payload == 'lead':
        role = "lead"
        await safe_send( chat_id=event.chat_id, text=f"Не заплатил" )
        await safe_send( chat_id=event.chat_id, text=f"Самая вкусная и важная инфа..." )
    elif event.payload == 'kid':
        user = await get_user_or_none(event.from_user.user_id)
        if user and user["role"] == "parent":
            await safe_send( chat_id=event.chat_id, text=f"Вы уже зарегистрированы как родитель" )
            return
        role = "kid"
        await kid_steps_before_date(event)
    elif event.payload == 'parent':
        role = "parent"
        await parent_steps_before_date(event)
    elif event.payload == 'admin':
        role = "admin"
        await safe_send( chat_id=event.chat_id, text=f"админ" )
    else:
        await safe_send( chat_id=event.chat_id, text="неизвестный юзер" )
        await safe_send( chat_id=event.chat_id, text=f"chat_id : {event.chat_id}\nuser_id : {event.from_user.user_id}" )
    await upsert_user(
        user_id=event.from_user.user_id,
        chat_id=event.chat.chat_id,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
        role=role
    )