import requests
import json

def get_ollama_output(prompt: str) -> dict[str, str] | None:
	URL = 'http://127.0.0.1:11434/api/generate'
	MODEL = 'llama3.2'

	payload = {
		'model': MODEL,
		'prompt': prompt,
		'stream': False,
		'format': 'json',
		'options': {
			'temperature': 1.0
		}
	}

	try:
		response = requests.post(URL, json=payload)
		response.raise_for_status()
		result_json = response.json()
		content: dict = json.loads(result_json['response'])
		return content

	except requests.exceptions.RequestException as e:
		print(f'OLLAMA: requests error: {e}')

	except json.JSONDecodeError as e:
		print(f'OLLAMA: json error: {e}')

	return None

