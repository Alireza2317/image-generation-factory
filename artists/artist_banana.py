from pathlib import Path
from artists.base_artist import Artist
from google import genai
from google.genai.types import (
	GenerateContentResponse, GenerateContentConfig, ImageConfig
)

class BananaArtist(Artist):
	def __init__(self, model: str = 'gemini-2.5-flash-image-preview') -> None:
		self.model = model
		self.client = genai.Client()


	def paint(self, prompt: str, ar: str, output_path: Path) -> bool:
		try:
			# generate the image
			image_response: GenerateContentResponse = self.client.models.generate_content(
				model=self.model,
				contents=[prompt],
				config=GenerateContentConfig(
					image_config=ImageConfig(
						aspect_ratio=ar,
						#image_size='1K'
					)
				)
			)
		except Exception as e:
			print(f'Banana Error: {e}')
			return False

		if image_response.parts is None:
			print('Banana Error: No proper response!')
			return False

		for part in image_response.parts:
			image = part.as_image()
			if image is not None:
				image.save(str(output_path.resolve()))
				break
		else:
			print('Banana Error: No image was generated!')
			return False

		return True