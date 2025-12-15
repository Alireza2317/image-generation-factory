from abc import ABC, abstractmethod

class Artist(ABC):
	def __init__(self, config: dict[str, str | int]) -> None:
		self.config = config

	@abstractmethod
	def paint(self, prompt: str, image_name: str) -> bool:
		'''Returns True if image generation was successful, else False'''
		pass