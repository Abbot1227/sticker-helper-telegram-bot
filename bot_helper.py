from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = '5257424513:AAEDzrawY43HuNX_ajYnpIzJ9UShAVQfeNQ'
HEROKU_APP = 'stiker-helper-bot'



bot = Bot(token = TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
dp.middleware.setup(LoggingMiddleware())