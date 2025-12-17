from abc import ABC, abstractmethod
from typing import Any


class Artist(ABC):
	def __init__(self, config: dict[str, Any]) -> None:
		self.config = config

	@abstractmethod
	def paint(
		self, prompt: str, image_name_stem: str, paint_cfg: dict[str, Any]
	) -> bool:
		"""
		image_name_stem: Desired filename WITHOUT extension.
		paint_cfg: Per-image settings (aspect_ratio, style, etc.)
		Returns True if image generation was successful, else False"""
		pass
