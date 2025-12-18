from datetime import datetime
from pathlib import Path
from config import (
	FOOOCUS_CONFIG,
	OLLAMA_CONFIG,
	CSV_PATH,
	PAINT_CONFIG,
	BANANA_CONFIG,
	ACTIVE_ARTIST,
	ACTIVE_BRAIN,
	META_PROMPTS_PATH,
)
from brains.base_brain import Brain
from brains.brain_ollama import OllamaBrain
from brains.brain_gemini import GeminiBrain
from artists.base_artist import Artist
from artists.artist_fooocus import FooocusArtist
from artists.artist_banana import BananaArtist
from core.csv_manager import AdobeCsvManager
from core.pipeline import ProductionPipeline
from core.services import ServerRunner
from prompts.prompt_manager import MetaPromptManager


def formatted_datetime() -> str:
	return datetime.now().strftime("%m%d%H%M%S")


def get_workers() -> tuple[Brain, Artist]:
	if ACTIVE_BRAIN.lower() == "ollama":
		brain = OllamaBrain(config=OLLAMA_CONFIG)
	elif ACTIVE_BRAIN.lower() == "gemini":
		brain = GeminiBrain()
	else:
		print(f"Unkown brain {ACTIVE_BRAIN}! use `ollama` or `gemini`.")
		exit(1)

	if ACTIVE_ARTIST.lower() == "banana":
		artist = BananaArtist(BANANA_CONFIG)
	elif ACTIVE_ARTIST.lower() == "fooocus":
		artist = FooocusArtist(config=FOOOCUS_CONFIG)
	else:
		print(f"Unkown artist {ACTIVE_ARTIST}! use `banana` or `fooocus`.")
		exit(1)

	return brain, artist


def main():
	N_image_per_niche: int = 3
	brain, artist = get_workers()

	csv_manager = AdobeCsvManager(filepath=CSV_PATH)

	pipeline = ProductionPipeline(brain=brain, artist=artist, csv_manager=csv_manager)

	meta_prompt_manager = MetaPromptManager(META_PROMPTS_PATH)

	need_ollama: bool = ACTIVE_BRAIN.lower() == "ollama"
	need_fooocus: bool = ACTIVE_ARTIST.lower() == "fooocus"
	with ServerRunner(run_ollama=need_ollama, run_fooocus=need_fooocus):
		for niche_name, meta_prompt in meta_prompt_manager.meta_prompts():
			for i in range(1, N_image_per_niche + 1):
				image_name: str = f"{niche_name}_{i}_{formatted_datetime()}"
				pipeline.run_job(
					meta_prompt, image_name_stem=image_name, paint_config=PAINT_CONFIG
				)


if __name__ == "__main__":
	main()
