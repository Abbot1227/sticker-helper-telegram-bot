from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = 'YOUR_BOT_TOKEN'
HEROKU_APP = 'YOUR_HEROKU_APP_NAME'



bot = Bot(token = TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
dp.middleware.setup(LoggingMiddleware())
