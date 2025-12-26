from abc import ABC, abstractmethod
from pydantic import BaseModel
from artists.base_artist import Artist
from brains.base_brain import Brain
from core.csv_manager import AdobeCsvManager


class JobConfig(BaseModel):
	"""
	Base model for job configurations.
	Pipelines can subclass this to define their own configs.
	"""

	pass


class BasePipeline[T_JobConfig: JobConfig](ABC):
	def __init__(
		self, brain: Brain, artist: Artist, csv_manager: AdobeCsvManager
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager

	@abstractmethod
	def run_job(self, config: T_JobConfig) -> bool:
		"""
		Runs the full cycle for one single batch of images.
		The implementation will be specific to each pipeline.
		"""
		pass
