from PIL import Image
import PIL
from io import BytesIO
from aiogram.types.photo_size import PhotoSize



def photo_resize(bio: BytesIO):
	img = Image.open(BytesIO(bio))
	img = img.resize((512, 512))

	bio = BytesIO()
	#bio.name = 'resized.png'
	img.save(bio, format = 'png')
	bio.seek(0)
	
	return bio