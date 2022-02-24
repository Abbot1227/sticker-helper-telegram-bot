from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import InvalidStickersSet
from io import BytesIO
import emojis

from states import states
from bot_helper import bot, dp
from keyboards import keyboards as kb
from utils.photo_converter import photo_resize


# Начало добавления стикера в набор

async def add_sticker_to_set(message: types.Message):
	await states.AddSticker.name.set()

	await message.answer('Отправьте стикер из набора, в который вы хотите добавить новый стикер', reply_markup = kb.cancel_kb())



# Вызов функции бота для добавления стикера в набор

async def add_sticker_toset(message: types.Message, state: FSMContext):
	data = await state.get_data()

	await bot.add_sticker_to_set(user_id = message.chat.id, 
			name = data['stickerset_name'], 
			png_sticker = data['photo'], 
			emojis = data['emojis'])



# Выбор набора стикеров для добавления нового стикера

#@dp.message_handler(state = states.AddSticker.name, content_types = ['sticker'])
async def choose_stickerset(message: types.Message, state: FSMContext):
	stickerset_name = (message.sticker).set_name

	if '_by_StikerHelperBot' in stickerset_name:
		await state.update_data(stickerset_name = stickerset_name)

		await message.answer('Отправьте фото/стикер, которое будет использовано в качестве стикера')

		await states.AddSticker.next()	

	else:
		await message.answer('Пожалуйста, отправьте стикерпак, созданный с помощью этого бота')



# Добавление стикера в набор стикеров

#@dp.message_handler(state = states.AddSticker.image, content_types = ['sticker'])
async def add_sticker(message: types.Message, state: FSMContext):
	if message.sticker.is_animated:
		await message.answer('Добавление анимированных стикеров пока недоступно, отправьте обычный стикер')
		return

	sticker = message.sticker.file_id

	await state.update_data(photo = sticker)

	await message.answer('Отправьте эмодзи, которые соответствую данному стикерому. Желательно не больше 2')

	await states.AddSticker.next()	



# Добавление фото в набор стикеров

#@dp.message_handler(state = states.AddSticker.image, content_types = ['photo'])
async def add_photo(message: types.Message, state: FSMContext):
	bio = BytesIO()
	bio.seek(0)
	await message.photo[-1].download(destination_file = bio)

	await message.answer('Отправьте эмодзи, которые соответствую данному стикерому. Желательно не больше 2')

	await states.AddSticker.next()

	await state.update_data(photo = photo_resize(bio.read()))



# Добавление эмодзи к созданному стикеру

#@dp.message_handler(state = states.AddSticker.emoji)
async def add_emoji_sticker(message: types.Message, state: FSMContext):
	sticker_emojis = emojis.get(message.text)
	data = await state.get_data()

	if len(sticker_emojis) == 0:
		await message.answer('Пожалуйста, отправьте корректное эмодзи')

	else:
		await state.update_data(emojis = sticker_emojis)

		await message.answer('Стикер был успешно добавлен в пак')
		await message.answer('Хотите добавить ещё один стикер?', reply_markup = kb.yes_no_kb())

		await states.AddSticker.next()

		await add_sticker_toset(message, state)



# Продолжить добавление стикеров

#@dp.message_handler(Text(equals = 'Да ✅'), state = states.AddSticker.continue_add)
async def add_another_sticker(message: types.Message, state: FSMContext):
	await message.answer('Отправьте фото/стикер, которое будет использовано в качестве стикера', reply_markup = kb.ReplyKeyboardRemove())

	await states.AddSticker.image.set()



# Закончить добавление стикеров

#@dp.message_handler(Text(equals = 'Нет ❌'), state = states.AddSticker.continue_add)
async def stop_adding_sticker(message: types.Message, state: FSMContext):
	await message.answer('Готово. Через некоторое время стикер/стикерпак обновится у всех пользователей', reply_markup = kb.menu_kb())

	await state.finish()



# Регистрация всех хэндлеров для добавления нового стикера в набор

def register_handlers(dp: Dispatcher):

	dp.register_message_handler(choose_stickerset,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.AddSticker.name,
		content_types = ['sticker'])

	dp.register_message_handler(add_sticker,
		state = states.AddSticker.image,
		content_types = ['sticker'])

	dp.register_message_handler(add_photo,
		state = states.AddSticker.image,
		content_types = ['photo'])

	dp.register_message_handler(add_emoji_sticker,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.AddSticker.emoji)

	dp.register_message_handler(add_another_sticker,
		Text(equals = 'Да ✅'),
		state = states.AddSticker.continue_add)

	dp.register_message_handler(stop_adding_sticker,
		Text(equals = 'Нет ❌'),
		state = states.AddSticker.continue_add)
