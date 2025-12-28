from collections.abc import Generator
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from prompts.config_manager import ConfigManager


class MetaPromptManager:
	def __init__(self, meta_prompts_path: Path) -> None:
		"""
		meta_prompts_path: Path to directory containing meta-prompt files,
		where each file contains a complete meta-prompt.

		Raises:
			ValueError: If meta_prompts_path is not a valid directory.
		"""
		if not meta_prompts_path.is_dir():
			raise ValueError(
				f"meta_prompts_path must be a valid directory: {meta_prompts_path}"
			)
		self.path = meta_prompts_path

	def meta_prompts(self) -> Generator[tuple[str, str], None, None]:
		for prompt_path in sorted(self.path.iterdir()):
			if prompt_path.suffix != ".txt":
				continue

			with open(prompt_path, mode="r", encoding="utf-8") as file:
				prompt: str = file.read()

			niche_name: str = prompt_path.stem

			yield niche_name, prompt


class WildcardPromptManager:
	def __init__(self, prompts_path: Path) -> None:
		self.path = prompts_path

	def prompts(self) -> Generator[tuple[str, str], None, None]:
		for prompt_path in sorted(self.path.iterdir()):
			if prompt_path.suffix != ".txt":
				continue

			with open(prompt_path, mode="r", encoding="utf-8") as file:
				raw_prompt: str = file.read()

			niche_name: str = prompt_path.stem

			yield niche_name, raw_prompt


class Niche(BaseModel):
	name: str
	config: dict[str, Any] = Field(default_factory=dict)
	prompts: list[str] = Field(default_factory=list)


class NicheManager:
	def __init__(self, niche_path: Path, config_manager: ConfigManager) -> None:
		self.path = niche_path
		self.config_manager = config_manager

	def niches(self) -> Generator[Niche, None, None]:
		for niche_dir in self.path.iterdir():
			if not niche_dir.is_dir():
				continue

			niche_name = niche_dir.name
			niche_config = self.config_manager.get_config(niche_name)

			prompts: list[str] = []
			for prompt_file in niche_dir.glob("*.txt"):
				with open(prompt_file, mode="r", encoding="utf-8") as file:
					prompts.append(file.read())

			if not prompts:
				print(f"Warning: Niche '{niche_name}' has no prompts, skipping.")
				continue

			yield Niche(name=niche_name, config=niche_config, prompts=prompts)
