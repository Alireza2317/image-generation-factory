import os
from collections.abc import Generator
from ollama import get_ollama_output
from fooocus import generate_image
from services import ServerRunner

META_PROMPTS_DIR: str = 'meta_prompts'
N_TRIES_PER_NICHE: int = 2


def meta_prompts() -> Generator[tuple[str, str], None, None]:
	for filename in os.listdir(META_PROMPTS_DIR):
		with open(f'{META_PROMPTS_DIR}/{filename}', mode='r') as file:
			meta_prompt: str = file.read()
		yield filename.removesuffix('.txt'), meta_prompt


with ServerRunner():
	for niche_name, meta_prompt in meta_prompts():
		for try_count in range(1, N_TRIES_PER_NICHE+1):
			llm_output: dict[str, str] | None = get_ollama_output(meta_prompt)

			print(llm_output)

			if llm_output is None:
				print("Error; no llm output! Skipping...")
				continue

			generate_image(
				llm_output.get("prompt", "")
			)
