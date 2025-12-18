from collections.abc import Generator
import os
from pathlib import Path


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
		self.meta_prompts_path = meta_prompts_path

	def _get_meta_prompts_paths(self) -> list[Path]:
		return [
			(self.meta_prompts_path / prompt_file)
			for prompt_file in sorted(os.listdir(self.meta_prompts_path))
		]

	def meta_prompts(self) -> Generator[tuple[str, str], None, None]:
		for full_meta_prompt_path in self._get_meta_prompts_paths():
			with open(full_meta_prompt_path, "r") as file:
				prompt: str = file.read()

			niche_name: str = full_meta_prompt_path.stem

			yield niche_name, prompt
