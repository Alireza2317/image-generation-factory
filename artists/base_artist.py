from abc import ABC, abstractmethod
from pathlib import Path


class Artist(ABC):
	@abstractmethod
	def paint(self, prompt: str, output_path: Path) -> bool:
		'''Returns True if image generation was successful, else False'''
		pass