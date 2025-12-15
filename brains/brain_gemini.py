import json
from google import genai
from google.genai.types import (
	GenerateContentResponse, GenerateContentConfig, ThinkingConfig
)
from brains.base_brain import Brain


class GeminiBrain(Brain):
	def __init__(self, model: str = 'gemini-2.5-flash') -> None:
		self.model = model
		self.client = genai.Client()

	def get_response(self, meta_prompt: str) -> dict[str, str] | None:
		try:
			response: GenerateContentResponse | None = self.client.models.generate_content(
				model=self.model,
				contents=meta_prompt,
				config=GenerateContentConfig(
					thinking_config=ThinkingConfig(thinking_budget=0)
				)
			)
		except Exception as e:
			print(f'Gemini Error: {e}')
			return None

		if response.parts is None:
			print('Gemini Error: No proper response!')
			return None

		for part in response.parts:
			if part.text is None:
				continue

			json_str: str = part.text
			break
		else:
			print('Gemini Error: No proper response!')
			return None

		# since sometimes the json string output from gemini could start
		# with ```json, we should clean it up first
		clean_json_s: str = json_str.removeprefix('```json').removesuffix('```')

		content: dict[str, str] = json.loads(clean_json_s)

		if self.validate_json(content):
			return content

		print('Gemini Error: JSON missing required keys!')
		return None
