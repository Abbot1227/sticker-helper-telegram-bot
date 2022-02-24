from aiogram.types import (
	ReplyKeyboardMarkup,
 	ReplyKeyboardRemove,
 	KeyboardButton,
 	InlineKeyboardButton,
 	InlineKeyboardMarkup)


btn_create_stickerset = KeyboardButton('Создать набор стикеров 🆕')
btn_add_sticker = KeyboardButton('Добавить стикер(ы) в набор ⏩')
btn_delete_stickerset =  KeyboardButton('Удалить набор стикеров 💩')
btn_remove_sticker = KeyboardButton('Удалить стикеры(ы) из набора 🚮')
btn_yes = KeyboardButton('Да ✅')
btn_no = KeyboardButton('Нет ❌')
btn_cancel = KeyboardButton('Отменить текущую операцию')

btn_delpack = InlineKeyboardButton(text = 'Удалить набор стикеров', url = 'https://t.me/Stickers')
btn_send_photo = InlineKeyboardButton(text = 'Отправить фото', url = 'https://t.me/Stickers')
btn_openAbbot = InlineKeyboardButton(text = 'Просто кнопка админа', url = 'https://t.me/Abbot1227')


def menu_kb():
	markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	markup.add(btn_create_stickerset).add(
	btn_add_sticker).add(
	btn_delete_stickerset).add(
	btn_remove_sticker)

	return markup



def admin_kb():
	markup = InlineKeyboardMarkup(row_width = 1)
	markup.add(btn_openAbbot)

	return markup



def yes_no_kb():
	markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	markup.add(btn_yes, btn_no)

	return markup



def cancel_kb():
	markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	markup.add(btn_cancel)

	return markup



def del_kb():
	markup = InlineKeyboardMarkup(row_width = 1)
	markup.add(btn_delpack)

	return markup



def send_photo_kb():
	markup = InlineKeyboardMarkup(row_width = 1)
	markup.add(btn_send_photo)

	return markup