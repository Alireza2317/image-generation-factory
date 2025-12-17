from abc import ABC, abstractmethod
from typing import Any


class Artist(ABC):
	def __init__(self, config: dict[str, Any]) -> None:
		self.config = config

	@abstractmethod
	def paint(self, prompt: str, image_name: str, paint_cfg: dict[str, Any]) -> bool:
		"""Returns True if image generation was successful, else False"""
		pass
