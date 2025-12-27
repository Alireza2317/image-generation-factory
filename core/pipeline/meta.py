from typing import Any

from brains.base_brain import Brain
from artists.base_artist import Artist
from core.csv_manager import AdobeCsvManager

from core.models import ImageIdea
from core.pipeline.base import BasePipeline, JobConfig


class MetaJobConfig(JobConfig):
	meta_prompt: str
	image_name_stem: str
	paint_config: dict[str, Any]


class MetaPipeline(BasePipeline[MetaJobConfig]):
	def __init__(
		self, brain: Brain, artist: Artist, csv_manager: AdobeCsvManager
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager

	def run_job(self, config: MetaJobConfig) -> bool:
		"""Runs the full cycle for one single batch of images."""

		print("🧠 Brainstorming... ", end="")
		image_idea: ImageIdea | None = self.brain.get_response(config.meta_prompt)

		if image_idea is None:
			print("❌ LLM failed to generate idea!")
			return False

		print("✅ Idea generated.")

		print("🎨 Painting ... ", end="")
		success_paint: bool = self.artist.paint(
			image_idea.prompt,
			image_name_stem=config.image_name_stem,
			paint_cfg=config.paint_config,
		)

		if not success_paint:
			print("❌ Artist failed to generate image!")
			return False

		print("✅ Image generated.")

		self.csv_manager.save_job_metadata(
			image_idea, config.image_name_stem, config.paint_config["N_images"]
		)

		print(f"✅ {'-' * 5} Finished cycle. {'-' * 5}\n")
		return True
