from pathlib import Path
import json
from typing import Any


class ConfigManager:
	def __init__(self, config_path: Path) -> None:
		self.path = config_path

	def get_config(self, name: str) -> dict[str, Any]:
		"""Load config for specific niche, fallback to default."""

		config_path = self.path / f"{name}.json"
		if not config_path.exists():
			print(f"{str(config_path)} was not found, using default config!")
			from settings import settings

			return settings.paint.model_dump()

		with open(config_path, mode="r", encoding="utf-8") as file:
			return dict(json.load(file))
