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
		self.path = meta_prompts_path

	def meta_prompts(self) -> Generator[tuple[str, str], None, None]:
		for prompt_path in sorted(self.path.iterdir()):
			with open(prompt_path, mode="r", encoding="utf-8") as file:
				prompt: str = file.read()

			niche_name: str = prompt_path.stem

			yield niche_name, prompt


class WildcardPromptManager:
	def __init__(self) -> None:
		pass

	def prompts(self) -> Generator[str, None, None]:
		yield "A futuristic __city__ at __time_of_day__ with flying __vehicle__s and __color__ lights."
		yield "A serene __nature_location__ with a crystal-clear river and __forest_animal__s."
		yield "A __sci_fi_job__ exploring an alien planet with __strange_adj__ rock formations."
		yield "A majestic __castle__ on a hilltop overlooking a vast __fantasy_kingdom__."
		yield "A bustling marketplace in a __fantasy_world__ with __colorful_adj__ stalls and __fantasy_character__s."
