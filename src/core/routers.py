from core.bot import dp
from handlers.calendar import calendar_router
from handlers.callbacks import callbacks_router
from handlers.messages import message_router

dp.include_routers(calendar_router)
dp.include_routers(callbacks_router)
dp.include_routers(message_router)