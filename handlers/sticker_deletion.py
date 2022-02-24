from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states import states
from bot_helper import bot, dp
from keyboards import keyboards as kb



# Начать удаление стикера из набора

async def remove_sticker_from_set(message: types.Message):
	await states.RemoveSticker.sticker.set()

	await message.answer('Отправьте стикер, который вы хотите удалить. Учтите, что можно удалить стикеры только из наборов, созданных этим ботом)', reply_markup = kb.cancel_kb())



# Удаление стикера из набора

#@dp.message_handler(state = states.RemoveSticker.sticker, content_types = ['sticker'])	
async def remove_sticker(message: types.Message):
	sticker = message.sticker.file_id
	stickerset_name = (message.sticker).set_name

	if '_by_StikerHelperBot' in stickerset_name:
		await bot.delete_sticker_from_set(sticker = sticker)

		await message.answer('Стикер был успешно удалён')
		await message.answer('Хотите удалить ещё один стикер?', reply_markup = kb.yes_no_kb())

		await states.RemoveSticker.next()

	else:
		await message.answer('Пожалуйста, отправьте стикер, созданный с помощью этого бота')



# Продолжить удаление стикеров

#@dp.message_handler(Text(equals = 'Да ✅'), state = states.RemoveSticker.continue_remove)
async def remove_another_sticker(message: types.Message, state: FSMContext):
	await message.answer('Отправьте стикер, который вы хотите удалить', reply_markup = kb.menu_kb())
	
	await states.RemoveSticker.sticker.set()



# Завершить удаление стикеров

#@dp.message_handler(Text(equals = 'Нет ❌'), state = states.RemoveSticker.continue_remove)
async def stop_removing_sticker(message: types.Message, state: FSMContext):
	await message.answer('Готово. Через некоторое время стикер(ы) исчезнут у всех пользователей', reply_markup = kb.menu_kb())

	await state.finish()



# Регистрация всех хэндлеров для удаления стикера из набора

def register_handlers(dp: Dispatcher):

	dp.register_message_handler(remove_sticker,
		state = states.RemoveSticker.sticker,
		content_types = ['sticker'])

	dp.register_message_handler(remove_another_sticker,
		Text(equals = 'Да ✅'),
		state = states.RemoveSticker.continue_remove)

	dp.register_message_handler(stop_removing_sticker,
		Text(equals = 'Нет ❌'),
		state = states.RemoveSticker.continue_remove)
	