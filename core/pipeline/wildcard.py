from core.pipeline.base import BasePipeline, JobConfig

class WildcardConfig(JobConfig):
	...

class WildcardPipeline(BasePipeline[WildcardConfig]):
	def run_job(self, config: WildcardConfig) -> bool:
		return False