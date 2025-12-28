from datetime import datetime
from settings import settings, ArtistType, BrainType, PipelineType

from brains.base_brain import Brain
from artists.base_artist import Artist

from brains.brain_ollama import OllamaBrain
from brains.brain_gemini import GeminiBrain
from artists.artist_fooocus import FooocusArtist
from artists.artist_banana import BananaArtist

from core.csv_manager import AdobeCsvManager

from core.services import ServerRunner

from core.pipeline.meta import MetaPipeline, MetaJobConfig
from core.pipeline.wildcard import WildcardPipeline, WildcardConfig
from prompts.wildcard_manager import WildcardResolver
from prompts.instruction_manager import InstructionManager
from prompts.config_manager import ConfigManager
from prompts.prompt_manager import MetaPromptManager, NicheManager


def formatted_datetime() -> str:
	return datetime.now().strftime("%m%d%H%M%S")


def get_workers() -> tuple[Brain, Artist]:
	brain: Brain
	if settings.active_brain == BrainType.OLLAMA:
		brain = OllamaBrain(config=settings.ollama.model_dump())
	elif settings.active_brain == BrainType.GEMINI:
		brain = GeminiBrain(config=settings.gemini.model_dump())
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


def run_meta_pipeline(
	brain: Brain,
	artist: Artist,
	csv_manager: AdobeCsvManager,
	n_image_per_niche: int = 1,
) -> None:
	meta_prompt_manager = MetaPromptManager(settings.meta_prompts_path)
	pipeline = MetaPipeline(brain, artist, csv_manager)
	cfg = ConfigManager(settings.niche_configs_path).get_config()

	for niche_name, meta_prompt in meta_prompt_manager.meta_prompts():
		for i in range(1, n_image_per_niche + 1):
			image_name: str = f"{niche_name}_{i}_{formatted_datetime()}"
			job_config = MetaJobConfig(
				meta_prompt=meta_prompt,
				image_name_stem=image_name,
				paint_config=cfg,
			)
			pipeline.run_job(job_config)


def run_wildcard_pipeline(
	brain: Brain,
	artist: Artist,
	csv_manager: AdobeCsvManager,
	n_image_per_niche: int = 1,
) -> None:
	wildcard_resolver = WildcardResolver(settings.wildcards_path)
	instruction_manager = InstructionManager(settings.instruction_path)
	config_manager = ConfigManager(settings.niche_configs_path)
	niche_manager = NicheManager(settings.wildcard_prompts_path, config_manager)
	default_config = config_manager.get_config()

	pipeline = WildcardPipeline(
		brain,
		artist,
		csv_manager,
		wildcard_resolver,
		instruction_manager,
	)

	for niche in niche_manager.niches():
		print(f"Processing niche: {niche.name}")
		merged_config = default_config.copy()
		merged_config.update(niche.config)

		for i, raw_prompt in enumerate(niche.prompts, 1):
			for j in range(1, n_image_per_niche + 1):
				image_name: str = f"{niche.name}_{i}_{j}_{formatted_datetime()}"
				job_config = WildcardConfig(
					raw_prompt=raw_prompt,
					image_name_stem=image_name,
					paint_config=merged_config,
				)
				pipeline.run_job(job_config)


def run_pipeline(
	brain: Brain,
	artist: Artist,
	csv_manager: AdobeCsvManager,
	n_image_per_niche: int = 1,
) -> None:
	if settings.active_pipeline == PipelineType.META:
		run_meta_pipeline(brain, artist, csv_manager, n_image_per_niche)
	elif settings.active_pipeline == PipelineType.WILDCARD:
		run_wildcard_pipeline(brain, artist, csv_manager, n_image_per_niche)
	else:
		print(f"Unknown pipeline {settings.active_pipeline}!")
		exit(1)


def main() -> None:
	N_image_per_niche: int = 3
	brain, artist = get_workers()
	csv_manager = AdobeCsvManager(filepath=settings.csv_path)

	need_fooocus: bool = settings.active_artist == ArtistType.FOOOCUS
	need_ollama: bool = settings.active_brain == BrainType.OLLAMA

	with ServerRunner(run_ollama=need_ollama, run_fooocus=need_fooocus):
		run_pipeline(brain, artist, csv_manager, N_image_per_niche)


if __name__ == "__main__":
	main()
