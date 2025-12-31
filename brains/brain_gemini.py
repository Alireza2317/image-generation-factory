import json
from typing import Any
from google import genai
from google.genai.types import (
	GenerateContentResponse,
	GenerateContentConfig,
	ThinkingConfig,
)
from brains.base_brain import Brain
from core.models import ImageIdea
from core.mappers import IdeaMapper


class GeminiBrain(Brain):
	def __init__(self, config: dict[str, Any]) -> None:
		self.model = config["model"]
		self.client = genai.Client()

	def get_response(self, prompt: str) -> ImageIdea | None:
		try:
			response: GenerateContentResponse | None = (
				self.client.models.generate_content(
					model=self.model,
					contents=prompt,
					config=GenerateContentConfig(
						thinking_config=ThinkingConfig(thinking_budget=0)
					),
				)
			)
		except Exception as e:
			print(f"Gemini Error: {e}")
			return None

		if response is None:
			print("Gemini Error: No response!")
			return None

		try:
			json_str = response.text
			if not isinstance(json_str, str):
				raise ValueError
		except ValueError:
			print("Gemini Error: No proper response!")
			return None

		# since sometimes the json string output from gemini could start
		# with ```json, we should clean it up first
		clean_json_s: str = json_str.removeprefix("```json").removesuffix("```")

		content: dict[str, Any] = json.loads(clean_json_s)

		if self.validate_json(content):
			try:
				return IdeaMapper.from_llm_json(content)
			except Exception as e:
				print(f"Error while mapping the json output to ImageIdea!\n{e}")
				return None

		print("Gemini Error: JSON missing required keys!")
		return None
