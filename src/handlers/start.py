from core.bot import dp
from services.db_services.users_service import upsert_user
from texts import TITLE_START_BTN
from keyboards.start import start_trial_keyboard
from keyboards.calendar import weekdays_keyboard
from services.sender import safe_send

# пробное
# https://max.ru/id645485463201_1_bot?start=trial
# не заплатил
# https://max.ru/id645485463201_1_bot?start=lead
# ребёнок
# https://max.ru/id645485463201_1_bot?start=kid
# родитель
# https://max.ru/id645485463201_1_bot?start=parent
# для теста
# https://max.ru/id645485463201_1_bot?start=admin
# https://max.ru/id645485463201_1_bot
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
        role = "kid"
        await safe_send( chat_id=event.chat_id, text=f"Ребёнок, привет!" )
        await safe_send( chat_id=event.chat_id, text=f"Вот тебе полезные материалы..." )
        await safe_send( chat_id=event.chat_id, text=f"Выбор времени занятия" )
    elif event.payload == 'parent':
        role = "parent"
        await safe_send( chat_id=event.chat_id, text=f"Родитель ребёнка, привет!" )
        await safe_send( chat_id=event.chat_id, text=f"Вот тебе полезные материалы  или мини-лекция..." )
        await safe_send( chat_id=event.chat_id,
            text=f"Укажи день в который будет заниматся твой ребёнок", attachments=[weekdays_keyboard()] )
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