from datetime import datetime
from settings import settings, ArtistType, BrainType
from brains.base_brain import Brain
from artists.base_artist import Artist
from brains.brain_ollama import OllamaBrain
from brains.brain_gemini import GeminiBrain
from artists.artist_fooocus import FooocusArtist
from artists.artist_banana import BananaArtist
from core.csv_manager import AdobeCsvManager
from core.pipeline.meta import MetaPipeline, MetaJobConfig
from core.services import ServerRunner
from prompts.prompt_manager import MetaPromptManager


def formatted_datetime() -> str:
	return datetime.now().strftime("%m%d%H%M%S")


def get_workers() -> tuple[Brain, Artist]:
	brain: Brain
	if settings.active_brain == BrainType.OLLAMA:
		brain = OllamaBrain(config=settings.ollama.model_dump())
	elif settings.active_brain == BrainType.GEMINI:
		brain = GeminiBrain()
	else:
		print(f"Unknown brain {settings.active_brain}!")
		exit(1)

	artist: Artist
	if settings.active_artist == ArtistType.BANANA:
		artist = BananaArtist(config=settings.banana.model_dump())
	elif settings.active_artist == ArtistType.FOOOCUS:
		artist = FooocusArtist(config=settings.fooocus.model_dump())
	else:
		print(f"Unknown artist {settings.active_artist}!")
		exit(1)

	return brain, artist


def main() -> None:
	N_image_per_niche: int = 1
	brain, artist = get_workers()

	csv_manager = AdobeCsvManager(filepath=settings.csv_path)

	pipeline = MetaPipeline(brain=brain, artist=artist, csv_manager=csv_manager)

	meta_prompt_manager = MetaPromptManager(settings.meta_prompts_path)

	need_ollama: bool = settings.active_brain == BrainType.OLLAMA
	need_fooocus: bool = settings.active_artist == ArtistType.FOOOCUS

	with ServerRunner(run_ollama=need_ollama, run_fooocus=need_fooocus):
		for niche_name, meta_prompt in meta_prompt_manager.meta_prompts():
			for i in range(1, N_image_per_niche + 1):
				image_name: str = f"{niche_name}_{i}_{formatted_datetime()}"
				job_config = MetaJobConfig(
					meta_prompt=meta_prompt,
					image_name_stem=image_name,
					paint_config=settings.paint.model_dump(),
				)
				pipeline.run_job(job_config)


if __name__ == "__main__":
	main()
