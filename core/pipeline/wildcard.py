from typing import Any

from brains.base_brain import Brain
from artists.base_artist import Artist
from core.csv_manager import AdobeCsvManager
from core.models import ImageIdea
from prompts.wildcard_manager import WildcardManager

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
		wildcard_manager: WildcardManager,
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager
		self.wildcard_manager = wildcard_manager

	def run_job(self, config: WildcardConfig) -> bool:
		return False