from abc import ABC, abstractmethod
from pydantic import BaseModel


class JobConfig(BaseModel):
	"""
	Base model for job configurations.
	Pipelines can subclass this to define their own configs.
	"""

	pass


class BasePipeline[T_JobConfig: JobConfig](ABC):
	@abstractmethod
	def run_job(self, config: T_JobConfig) -> bool:
		"""
		Runs the full cycle for one single batch of images.
		The implementation will be specific to each pipeline.
		"""
		pass
