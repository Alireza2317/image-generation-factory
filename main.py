from google import genai
from google.genai.types import (
	GenerateContentResponse, GenerateContentConfig, ThinkingConfig, ImageConfig
)
from collections.abc import Generator
import os
import json
from datetime import datetime

N: int = 10 # per niche
META_PROMPTS_DIR: str = 'meta_prompts'
ADOBE_CSV: str = 'metadata.csv'
LOG_DIR: str = 'log'
IMAGE_MODEL: str = 'gemini-2.5-flash-image-preview'
IMAGES_DIR: str = 'images'
AR: str = '16:9'
RESOLUTION: str = '1K'


def formatted_datetime() -> str:
	return datetime.now().strftime('%m%d%H%M%S')

def create_csv_if_not_exists() -> None:
	if not os.path.isfile(ADOBE_CSV):
		with open(ADOBE_CSV, mode='w') as file:
			file.write('Filename,Title,Keywords,Category,Releases\n')

def create_image_dir() -> None:
	if not os.path.isdir(IMAGES_DIR):
		os.makedirs(IMAGES_DIR)

def append_metadata_to_csv(metadata: dict[str, str]) -> None:
	filename: str = metadata.get('filename', '').replace('png', 'jpg')
	title: str = metadata.get('title', '')
	raw_keywords: str = metadata.get('keywords', '')
	keywords_list: list[str] = raw_keywords.split(',')

	keywords: str = '"' + ','.join(kw.strip() for kw in keywords_list) + '"'
	category: str = metadata.get('category', '')
	row: str = f'{filename},{title},{keywords},{category},\n'

	with open(ADOBE_CSV, mode='a') as file:
		file.write(row)

def clean_llm_output(llm_output: str) -> str:
	clean_json_s: str = llm_output.removeprefix('```json').removesuffix('```')
	return clean_json_s

def decompose_json(json_s: str, image_filename: str) -> tuple[str, dict[str, str]]:
	"""returns the image prompt, and the rest of the json(metadata) as a dict."""
	metadata: dict[str, str] = json.loads(json_s)

	image_prompt: str = metadata.pop('prompt', '')

	metadata['filename'] = image_filename
	metadata['releases'] = ''

	return image_prompt, metadata

def log_prompt_and_metadata(
	niche_name: str, image_prompt: str, metadata: dict[str, str],
):
	os.makedirs(LOG_DIR, exist_ok=True)
	log_filepath: str = f'{LOG_DIR}/{niche_name}.csv'

	if not os.path.isfile(log_filepath):
		with open(log_filepath, mode='a') as file:
			file.write('filename,title,keywords,prompt\n')

	filename: str = metadata.get('filename', '')
	title: str = metadata.get('title', '')
	keywords: str = metadata.get('keywords', '')

	row = f'{filename},{title},{keywords},{image_prompt}\n'
	with open(log_filepath, mode='a') as file:
		file.write(row)

def meta_prompts() -> Generator[tuple[str, str], None, None]:
	for filename in os.listdir(META_PROMPTS_DIR):
		with open(f'{META_PROMPTS_DIR}/{filename}', mode='r') as file:
			meta_prompt: str = file.read()
		yield filename.removesuffix('.txt'), meta_prompt


def main():
	create_image_dir()
	create_csv_if_not_exists()

	client = genai.Client()

	for niche_name, meta_prompt in meta_prompts():
		for image_count in range(1, N+1):
			first_response: GenerateContentResponse | None = client.models.generate_content(
				model='gemini-2.5-flash',
				contents=meta_prompt,
				config=GenerateContentConfig(
					thinking_config=ThinkingConfig(thinking_budget=0)
				)
			)

			if first_response.parts is None:
				print('NO RESPONSE PARTS!')
				continue

			for part in first_response.parts:
				if part.text is None:
					print('NO TEXT OUTPUT!')
					continue
				image_filename: str = \
					f'{niche_name}_{image_count}_{formatted_datetime()}.png'

				image_prompt, metadata = decompose_json(
					clean_llm_output(part.text), image_filename
				)

				append_metadata_to_csv(metadata)

				# generate the image
				image_response: GenerateContentResponse = client.models.generate_content(
					model=IMAGE_MODEL,
					contents=[image_prompt],
					config=GenerateContentConfig(
						image_config=ImageConfig(
							aspect_ratio=AR,
							#image_size=RESOLUTION
						)
					)
				)

				if image_response.parts is None:
					print('NO IMAGE_RESPONSE PARTS!')
					continue
				for part in image_response.parts:
					image = part.as_image()
					if image is not None:
						image.save(f'{IMAGES_DIR}/{image_filename}')
						log_prompt_and_metadata(niche_name, image_prompt, metadata)

if __name__ == "__main__":
	main()
