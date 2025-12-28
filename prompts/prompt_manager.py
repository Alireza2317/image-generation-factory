from collections.abc import Generator
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
