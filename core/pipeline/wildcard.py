from typing import Any

from brains.base_brain import Brain
from artists.base_artist import Artist
from core.csv_manager import AdobeCsvManager
from core.models import ImageIdea
from prompts.wildcard_manager import WildcardResolver
from prompts.instruction_manager import InstructionManager

from core.pipeline.base import BasePipeline, JobConfig


class WildcardConfig(JobConfig):
	raw_prompt: str
	image_name_stem: str
	paint_config: dict[str, Any]
	llm_instruction: str


class WildcardPipeline(BasePipeline[WildcardConfig]):
	def __init__(
		self,
		brain: Brain,
		artist: Artist,
		csv_manager: AdobeCsvManager,
		wildcard_resolver: WildcardResolver,
		instruction_manager: InstructionManager,
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager
		self.wildcard_resolver = wildcard_resolver
		self.instruction_manager = instruction_manager

	def run_job(self, config: WildcardConfig) -> bool:
		resolved_prompt: str = self.wildcard_resolver.resolve(config.raw_prompt)
		print("🧠 Brainstorming... ", end="")

		instruction: str | None = self.instruction_manager.get_instruction(
			config.llm_instruction
		)
		if not instruction:
			print("❌ Instruction not found!")
			return False

		instruction += f"\nidea=```{resolved_prompt}```"

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
