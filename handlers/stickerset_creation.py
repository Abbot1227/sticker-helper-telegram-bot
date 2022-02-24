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

ADMIN_ID = '2011969371'


# Начало создания набора стикеров

async def create_sticker_set(message: types.Message):
	await states.CreateStickerSet.title.set()

	await message.answer('Введите имя вашего набора стикеров', reply_markup = kb.cancel_kb())



# Вызов функции бота для создания нового набора стикеров

async def create_set(message: types.Message, state: FSMContext):
	data = await state.get_data()

	await bot.create_new_sticker_set(user_id = message.chat.id, 
			name = data['stickerset_name'] + '_by_StikerHelperBot', 
			title = data['stickerset_title'],
			png_sticker = data['photo'],
			emojis = data['emojis'])

	await bot.send_message(chat_id = ADMIN_ID, text = data['stickerset_name'] + '_by_StikerHelperBot')





# Вызов функции бота для добавления стикера в набор

async def add_sticker_to_set(message: types.Message, state: FSMContext):
	data = await state.get_data()

	await bot.add_sticker_to_set(user_id = message.chat.id, 
			name = data['stickerset_name'], 
			png_sticker = data['photo'], 
			emojis = data['emojis'])



# Установка имени набора стикеров

#@dp.message_handler(Text(equals = ~'Отменить текущую операцию'), state = states.CreateStickerSet.title)
async def set_stickerset_title(message: types.Message, state: FSMContext):
	await state.update_data(stickerset_title = message.text)
	await state.update_data(is_created = False)		# В дальнейшем используется для различия между созданием нового набора стикеров и добавлением стикера к новому набору

	await message.answer('Отправьте фото, которое будет использовано в качестве стикера, или стикер из другого стикерпака')

	await states.CreateStickerSet.next()



# Добавление стикера в набор стикеров

#@dp.message_handler(state = states.CreateStickerSet.image, content_types = ['sticker'])
async def add_sticker(message: types.Message, state: FSMContext):
	if message.sticker.is_animated:
		await message.answer('Добавление анимированных стикеров пока недоступно, отправьте обычный стикер')
		return

	sticker = message.sticker.file_id

	await state.update_data(photo = sticker)

	await message.answer('Отправьте эмодзи, которые соответствуют данному стикеру. Желательно не больше 2')

	await states.CreateStickerSet.next()



# Добавление фото в набор стикеров

#@dp.message_handler(state = states.CreateStickerSet.image, content_types = ['photo'])
async def add_photo(message: types.Message, state: FSMContext):
	bio = BytesIO()	
	bio.seek(0)
	await message.photo[-1].download(destination_file = bio)

	await states.CreateStickerSet.next()

	await message.answer('Отправьте эмодзи, которые соответствуют данному стикеру. Желательно не больше 2')		

	await state.update_data(photo = photo_resize(bio.read()))	# Конвертация фото в .png и изменение разрешения



# Добавление эмодзи к созданному стикеру

#@dp.message_handler(state = states.CreateStickerSet.emoji)
async def add_emoji_to_sticker(message: types.Message, state: FSMContext):
	sticker_emojis = str(emojis.get(message.text))
	data = await state.get_data()

	if len(sticker_emojis) == 0:
		await message.answer('Пожалуйста, отправьте эмодзи')

	elif data['is_created'] == False:
		await state.update_data(emojis = sticker_emojis)

		await message.answer('Введите имя, которое будет использоваться для отправки ссылки на набор стикеров. Оно должно начинаться с маленькой буквы, и не содержать никаких знаков кроме _ и латинских букв')
	
		await states.CreateStickerSet.next()

	else:
		await state.update_data(emojis = sticker_emojis)

		await message.answer('Стикер был успешно добавлен в пак')
		await message.answer('Хотите добавить ещё один стикер?', reply_markup = kb.yes_no_kb())

		await states.CreateStickerSet.continue_add.set()

		await add_sticker_to_set(message, state)



# Установка имени набора стикеров

#@dp.message_handler(state = states.CreateStickerSet.name)
async def set_stickerset_name(message: types.Message, state: FSMContext):
	await state.update_data(stickerset_name = message.text)
	data = await state.get_data()

	try:
		await bot.get_sticker_set(data['stickerset_name'] + '_by_StikerHelperBot')

	except InvalidStickersSet:
		await message.answer('Стикерпак был успешно создан и доступен по ссылке https://t.me/addstickers/' + data['stickerset_name'] + '_by_StikerHelperBot')
		await message.answer('Хотите добавить ещё один стикер?', reply_markup = kb.yes_no_kb())

		await state.update_data(is_created = True)
		await states.CreateStickerSet.next()

		await create_set(message, state)

	else:
		await message.answer('Это имя уже занято. Введите другое имя')



# Продолжить добавление стикеров

#@dp.message_handler(Text(equals = 'Да ✅'), state = states.CreateStickerSet.continue_add)
async def add_another_sticker(message: types.Message, state: FSMContext):
		await message.answer('Отправьте фото/стикер, которое будет использовано в качестве стикера', reply_markup = kb.ReplyKeyboardRemove())

		await states.CreateStickerSet.image.set()



# Закончить создание набора стикеров

#@dp.message_handler(Text(equals = 'Нет ❌'), state = states.CreateStickerSet.continue_add)
async def stop_adding_sticker(message: types.Message, state: FSMContext):
	await message.answer('Готово. Через некоторое время стикер/стикерпак обновится у всех пользователей', reply_markup = kb.menu_kb())

	await state.finish()



# Регистрация всех хэндлеров для создания нового набора стикеров

def register_handlers(dp: Dispatcher):

	dp.register_message_handler(set_stickerset_title,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.CreateStickerSet.title)

	dp.register_message_handler(add_sticker,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.CreateStickerSet.image,
		content_types = ['sticker'])

	dp.register_message_handler(add_photo,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.CreateStickerSet.image,
		content_types = ['photo'])

	dp.register_message_handler(add_emoji_to_sticker,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.CreateStickerSet.emoji)

	dp.register_message_handler(set_stickerset_name,
		~Text(equals = 'Отменить текущую операцию'),
		state = states.CreateStickerSet.name)

	dp.register_message_handler(add_another_sticker,
		Text(equals = 'Да ✅'),
		state = states.CreateStickerSet.continue_add)

	dp.register_message_handler(stop_adding_sticker,
		Text(equals = 'Нет ❌'),
		state = states.CreateStickerSet.continue_add)
