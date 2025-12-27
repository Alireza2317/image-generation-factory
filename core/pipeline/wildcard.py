from typing import Any

from brains.base_brain import Brain
from artists.base_artist import Artist
from core.csv_manager import AdobeCsvManager
from core.models import ImageIdea
from prompts.wildcard_manager import WildcardResolver

from core.pipeline.base import BasePipeline, JobConfig


class WildcardConfig(JobConfig):
	raw_prompt: str
	image_name_stem: str
	paint_config: dict[str, Any]


class WildcardPipeline(BasePipeline[WildcardConfig]):
	def __init__(
		self,
		brain: Brain,
		artist: Artist,
		csv_manager: AdobeCsvManager,
		wildcard_resolver: WildcardResolver,
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager
		self.wildcard_resolver = wildcard_resolver

	def run_job(self, config: WildcardConfig) -> bool:
		resolved_prompt: str = self.wildcard_resolver.resolve(config.raw_prompt)
		print("🧠 Brainstorming... ", end="")

		# FIXME: improve instruction wording, just a quick draft for now
		instruction: str = f"""Generate a detailed image prompt based on the following idea. which is inside ``` symbols. Respond in JSON format with fields: 
		prompt, title, keywords (comma-separated). Be descriptive and imaginative.
		idea = ```{resolved_prompt}```
		"""

		image_idea: ImageIdea | None = self.brain.get_response(instruction)
		if not image_idea:
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
