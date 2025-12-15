from pathlib import Path
from artists.base_artist import Artist
from google import genai
from google.genai.types import (
	GenerateContentResponse, GenerateContentConfig, ImageConfig
)

class BananaArtist(Artist):
	def __init__(self, config: dict[str, str | int]) -> None:
		super().__init__(config)
		self.client = genai.Client()

	def paint(self, prompt: str, image_name: str) -> bool:
		try:
			# generate the image
			image_response: GenerateContentResponse = self.client.models.generate_content(
				model=self.config.get('model'),
				contents=[prompt],
				config=GenerateContentConfig(
					image_config=ImageConfig(
						aspect_ratio=self.config.get('aspect_ratio'),
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
				output_dir: Path = self.config.get('output_dir')
				output_image_path: Path = output_dir / image_name
				image.save(str(output_image_path.resolve()))
				break
		else:
			print('Banana Error: No image was generated!')
			return False

		return True