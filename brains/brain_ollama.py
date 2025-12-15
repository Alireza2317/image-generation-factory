import json
import requests
from base_brain import Brain

#URL = 'http://127.0.0.1:11434/api/generate'
#MODEL = 'llama3.2'


class OllamaBrain(Brain):
	def __init__(self, model: str, url: str) -> None:
		self.model = model
		self.url = url

	def get_response(self, meta_prompt: str) -> dict[str, str] | None:
		payload = {
			'model': self.model,
			'prompt': meta_prompt,
			'stream': False,
			'format': 'json',
			'options': {
				'temperature': 0.8
			}
		}

		try:
			response = requests.post(self.url, json=payload)
			response.raise_for_status()

			raw_json = response.json().get('response')
			content: dict[str, str] = json.loads(raw_json)

			if self.validate_json(content):
				return content

			print('❌ JSON missing required keys!')

		except requests.exceptions.RequestException as e:
			print(f'OLLAMA: requests error: {e}')

		except json.JSONDecodeError as e:
			print(f'OLLAMA: json error: {e}')

		except Exception as e:
			print(f'OLLAMA Error: {e}')

		return None
