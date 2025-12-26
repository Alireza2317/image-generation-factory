import json
from typing import Any
import requests
from brains.base_brain import Brain
from core.models import ImageIdea
from core.mappers import IdeaMapper


class OllamaBrain(Brain):
	def __init__(self, config: dict[str, Any]) -> None:
		self.model = config["model"]
		self.url = config["url"]

	def get_response(self, meta_prompt: str) -> ImageIdea | None:
		payload = {
			"model": self.model,
			"prompt": meta_prompt,
			"stream": False,
			"format": "json",
			"options": {"temperature": 0.8},
		}

		try:
			response = requests.post(self.url, json=payload)
			response.raise_for_status()

			raw_json = response.json().get("response")
			content: dict[str, Any] = json.loads(raw_json)

			if self.validate_json(content):
				try:
					return IdeaMapper.from_llm_json(content)
				except Exception as e:
					print(f"Error while mapping the json output to ImageIdea!\n{e}")
					return None

			print("❌OLLAMA: JSON missing required keys!")

		except requests.exceptions.RequestException as e:
			print(f"OLLAMA: requests error: {e}")

		except json.JSONDecodeError as e:
			print(f"OLLAMA: json error: {e}")

		except Exception as e:
			print(f"OLLAMA Error: {e}")

		return None
