import asyncio
import os
from zoneinfo import ZoneInfo
from env import ACCESS_TOKEN

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(PARENT_DIR, 'data', 'users.json')
FILE_PATH_CHECKLIST = os.path.join(PARENT_DIR, 'data', 'checklist.pdf')
DB_PATH = os.path.join(os.path.dirname(PARENT_DIR), '', 'users.db')
SCHEMA_PATH = os.path.join(PARENT_DIR, 'db', 'schema.sql')

file_lock = asyncio.Lock()

BOT_NAME = "ДАЙБИТ_БОТ"
MOSCOW = ZoneInfo("Europe/Moscow")

BASE_URL = "https://makebeatschool.amocrm.ru"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}
PHONE_FIELD_ID = 3371021
TRIAL_DATETIME_FIELD_ID = 3372431
DAYS = [ ("Пн", "mon"), ("Вт", "tue"), ("Ср", "wed"), ("Чт", "thu"), ("Пт", "fri"), ("Сб", "sat"), ("Вс", "sun"), ]
