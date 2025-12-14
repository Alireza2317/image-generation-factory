import requests
from datetime import datetime
BASE_MODEL = 'juggernautXL_v8Rundiffusion.safetensors'
PERFORMANCE = 'Speed' # Quality, Speed
AR = '1344*768'
N = 3
STYLES = [
	'Fooocus V2',
]

OUTPUT_PATH = f'./fooocus_outputs/{datetime.now().strftime("%y-%m-%d")}'

def generate_image(prompt: str) -> None:
	URL = 'http://127.0.0.1:8888/v1/generation/text-to-image'

	payload = {
		'prompt': prompt,
		'negative_prompt': 'watermark,y signiture, logo, text',
		'style_selections': STYLES,
		'performance_selection': PERFORMANCE,
		'aspect_ratios_selection': AR,
		'image_number': N,
		'image_seed': -1,
		'sharpness': 2,
		'guidance_scale': 4,
		'base_model_name': BASE_MODEL,
		'refiner_model_name': 'None',
		'refiner_swith': 0.5,
		'loras': [
			{
				'model_name': 'sd_xl_offset_example-lora_1.0.safetensors',
				'weight': 0.2,
				'enabled': True
			},
		],
		'advanced_params': {
			'disable_preview': True
		},
		'require_base64': False,
		'async_process': False
	}

	try:
		response = requests.post(URL, json=payload)

		data = response.json()

		if response.status_code == 200:
			print(f'Successful: {data}')
		else:
			print(f'API Error: {response.text}')


	except Exception as e:
		print(f'Fooocus Error: {e}')