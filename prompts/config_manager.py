from pathlib import Path
import json
from typing import Any


class ConfigManager:
	def __init__(self, config_path: Path) -> None:
		self.path = config_path

	def get_config(self, name: str = "default") -> dict[str, Any]:
		"""Load config for specific niche, fallback to default."""

		niche_config_path = self.path / f"{name}.json"
		default_config_path = self.path / "default.json"

		if niche_config_path.exists():
			config_to_load = niche_config_path
		elif default_config_path.exists():
			if name != "default":
				print(f"Warning: Config for '{name}' not found, using default.")
			config_to_load = default_config_path
		else:
			raise FileNotFoundError(
				f"Neither '{name}.json' nor 'default.json' found in {self.path}"
			)

		with open(config_to_load, mode="r", encoding="utf-8") as file:
			return dict(json.load(file))
