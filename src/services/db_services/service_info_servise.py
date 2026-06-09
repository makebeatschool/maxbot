from config import MOSCOW
from datetime import datetime
from db.repos.service_info_repo import set_service_value, get_service_value


async def get_service(key: str):
    value = await get_service_value(key)
    if value is None:
        value = datetime.now(MOSCOW).date().isoformat()
        await set_service_value(key, value)
    return value

async def set_service(s, value):
    try:
        await set_service_value(s, value)
    except: return False