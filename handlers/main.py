from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt

from bot_helper import bot, dp
from keyboards import keyboards as kb
from states import states
from utils import access_checker
from . import stickerset_creation, sticker_addition, sticker_deletion


# Начало работы с ботом

#@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
	if access_checker.check_status(str(message.chat.id)):
		await message.answer('Greeting, sir. The desert awaits you',
			reply_markup = kb.admin_kb())

	else:
		await message.answer(f'''Привет! 👋

🤖 Этот бот поможет вам в создании и изменении стикерпаков. Пожалуйста, выберите один из вариантов ниже
    
🛍️ Чтобы завершить любую операцию используйте команду /cancel\nДля получения информации о боте вызовите /info

🌄 Если вы не хотите создавать стикеры с помощью этого бота, вы можете просто преобразовать ваши фото и отправить их официальному боту для стикеров. Команда /convert

💰 Для отправки доната используйте команду /donate

❓ Для сообщения о проблемах, багах и недочетах бота, а также отправки предложений или контакта с создателем используйте {fmt.hide_link('https://t.me/abbot1227')}
    ''', reply_markup = kb.menu_kb(), parse_mode = types.ParseMode.HTML)



# Меня действий

#@dp.message_handler(state = None, Text(equals = lambda tex: tex in ['Создать набор стикеров', 'Добавить стикер(ы) в набор', 'Удалить набор стикеров', 'Удалить стикеры(ы) из набора']))
async def check_menu_option(message: types.Message):
	if message.text == 'Создать набор стикеров 🆕':
		await stickerset_creation.create_sticker_set(message)

	elif message.text == 'Добавить стикер(ы) в набор ⏩':
		await sticker_addition.add_sticker_to_set(message)

	elif message.text == 'Удалить набор стикеров 💩':
		await delete_stickerset(message)

	elif message.text == 'Удалить стикеры(ы) из набора 🚮':
		await sticker_deletion.remove_sticker_from_set(message)



# Отмена любой текущей операции

#@dp.message_handler(commands = ['cancel'], state = '*')
#@dp.message_handler(Text(equals = 'Отменить текущую операцию'), state = '*')
async def cancel_operation(message: types.Message, state: FSMContext):
	current_state = await state.get_state()

	if current_state is None:
		await message.answer('Нечего завершать', reply_markup = kb.menu_kb())

		return

	await state.finish()

	await message.answer('Текущая операция была отменена', reply_markup = kb.menu_kb())



# Донат

#@dp.message_handler(commands = ['donate'], state = None)
async def donate(message = types.Message):
	await message.answer('Каспи: 4400 4231 5605 3125 :)\n(not real number)')



# Информация об изменениях бота

#@dp.message_handler(commands = ['info'], state = None)
async def info(message: types.Message):
	await message.answer(""" 
<b>Текущая версия бота 1.0.3</b>

<b>Добавлено в версии 1.0.3</b>:
- Админ-панель
- Chat Action при отправке фото ботом

<b>Добавлено в версии 1.0.2</b>:
- Inline клавиатура в удалении пака стикеров
- Обработка ошибки при попытке пользователя добавить анимированный стикер в набор стикеров

<b>Добавлено в версии 1.0.1</b>:
- Вывод информации о боте /info
- Простое преобразование фото /convert и /stop
- Вебхук на Heroku


<b>Планируется в версии 1.0.4:</b>
- Поддержка создания анимированных наборов стикеров
- Добавление обработчиков неизвестных команд и текста для всех состояний
""", parse_mode = types.ParseMode.HTML)



# Удалить набор стикеров с помощью официального бота

async def delete_stickerset(message: types.Message):
	await message.answer('Данная функция пока недоступна, т.к. автору слишком лень её допиливать. Для удаления набора стикеров воспользуйтесь официальным ботом Телеграм', reply_markup = kb.del_kb())



# Неизвестная команда/текст

#@dp.message_handler(state = None)
async def unknown(message: types.Message):
	await message.answer('Неизвестная команда/текст')



# Регистрация основных хэндлеров

def register_handlers(dp: Dispatcher):

	dp.register_message_handler(start_handler,
		commands = ['start'])

	dp.register_message_handler(cancel_operation,
		commands = ['cancel'],
		state = '*')

	dp.register_message_handler(cancel_operation,
		Text(equals = 'Отменить текущую операцию'),
		state = '*')

	dp.register_message_handler(check_menu_option,
		Text(equals = ['Создать набор стикеров 🆕','Добавить стикер(ы) в набор ⏩','Удалить набор стикеров 💩','Удалить стикеры(ы) из набора 🚮']),
		state = None)

	dp.register_message_handler(donate,
		commands = ['donate'],
		state = None)

	dp.register_message_handler(info,
		commands = ['info'],
		state = None)

	dp.register_message_handler(unknown,
		state = None)
