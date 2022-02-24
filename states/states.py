from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateStickerSet(StatesGroup):
	title = State()
	image = State()
	emoji = State()
	name = State()
	continue_add = State()



class AddSticker(StatesGroup):
	name = State()
	image = State()
	emoji = State()
	continue_add = State()



class RemoveSticker(StatesGroup):
	sticker = State()
	continue_remove = State()



class PhotoConvert(StatesGroup):
	convert = State()