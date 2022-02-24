from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from io import BytesIO

from states import states
from bot_helper import bot, dp
from utils.photo_converter import photo_resize
from keyboards import keyboards as kb


# Начало конвертации фото

#@dp.message_handler(commands = ['convert'], state = None)
async def start_convertation(message: types.Message):
	await states.PhotoConvert.convert.set()

	await message.answer('Отправьте фото, которое нужно преобразовать. Отправьте /stop когда закончите отправлять фото', reply_markup = kb.ReplyKeyboardRemove())



# Конвертация фото из .jpg в .png и уменьшение размера

#@dp.message_handler(content_types = ['photo'], state = states.PhotoConvert.convert)
async def convert_photo(message: types.Message):
	bio = BytesIO()
	bio.seek(0)

	await bot.send_chat_action(chat_id = message.chat.id, action = 'upload_photo')
	await message.photo[-1].download(destination_file = bio)
	await message.answer_document(document = ('resized.png', photo_resize(bio.read())))



# Остановка отправки фото для конвертации

#@dp.message_handler(commands = ['stop'], state = states.PhotoConvert.convert)
async def stop_convertation(message: types.Message, state: FSMContext):
	await message.answer('Конвертация завершена', reply_markup = kb.menu_kb())
	await message.answer('Отправьте преобразованные фото боту', reply_markup = kb.send_photo_kb())

	await state.finish()


# Регистрация всех хэндлеров для конвертации фото

def register_handlers(dp: Dispatcher):

	dp.register_message_handler(start_convertation,
		commands = ['convert'],
		state = None)

	dp.register_message_handler(convert_photo,
		content_types = ['photo'],
		state = states.PhotoConvert.convert)

	dp.register_message_handler(stop_convertation,
		commands = ['stop'],
		state = states.PhotoConvert.convert)
