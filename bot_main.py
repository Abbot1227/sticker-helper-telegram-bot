import logging
from aiogram import executor, types, Dispatcher
import os

from bot_helper import dp, bot, TOKEN, HEROKU_APP
from handlers import config


# Настройки вебхука
WEBHOOK_HOST = f'https://{HEROKU_APP}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


# Настройки вебсервера
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 80))




async def on_startup(dp: Dispatcher):
	logging.warning('Starting connection...')

	await bot.set_webhook(WEBHOOK_URL)

	config.register_handlers(dp)



async def on_shutdown(dp: Dispatcher):
	logging.warning('Shutting down...')

	await bot.delete_webhook()

	await dp.storage.close()
	await dp.storage.wait_closed()

	logging.warning('Finished.')


if __name__ == '__main__':

	logging.basicConfig(level = logging.INFO)

	executor.start_webhook(
		dispatcher = dp,
		webhook_path = WEBHOOK_PATH,
		on_startup = on_startup,
		on_shutdown = on_shutdown,
		skip_updates = True,
		host = WEBAPP_HOST,
		port = WEBAPP_PORT
	)
