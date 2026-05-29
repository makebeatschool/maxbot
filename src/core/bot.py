from env import TOKEN
from maxapi import Bot, Dispatcher, Router

bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()
dp.include_routers(router)