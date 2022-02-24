from . import stickerset_creation, sticker_addition, sticker_deletion, photo_convertation, main
from bot_helper import dp
from aiogram import Dispatcher



# Регистрация всех хэндлеров

def register_handlers(dp: Dispatcher):

	stickerset_creation.register_handlers(dp)

	sticker_addition.register_handlers(dp)

	sticker_deletion.register_handlers(dp)

	photo_convertation.register_handlers(dp)

	main.register_handlers(dp)