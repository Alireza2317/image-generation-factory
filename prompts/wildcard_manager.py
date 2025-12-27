import os
import random
import re
from pathlib import Path


class WildcardManager:
	"""
	Manages and resolves wildcards in prompts.

	A wildcard is a placeholder in a prompt, like `__color__`, that gets replaced
	by a randomly chosen line from a corresponding file (e.g., `color.txt`).

	"""

	def __init__(self, wildcards_path: Path) -> None:
		"""
		wildcards_path: Path to directory containing wildcard files,
		where each file contains a list of wildcard prompts.

		Raises:
			ValueError: If wildcards_path is not a valid directory.
		"""
		if not wildcards_path.is_dir():
			raise ValueError(
				f"wildcards_path must be a valid directory: {wildcards_path}"
			)
		self.path = wildcards_path
		self._wildcards: dict[str, list[str]] = {}
		self._populate_wildcards()

	def _get_all_wildcard_files(self) -> list[Path]:
		wildcard_files: list[Path] = []
		for root, _, files in os.walk(self.path):
			for file in files:
				if not file.endswith(".txt"):
					continue
				full_path: Path = Path(root) / file
				wildcard_files.append(full_path)
		return wildcard_files

	def _populate_wildcards(self) -> None:
		for filepath in self._get_all_wildcard_files():
			wildcard_name = filepath.stem
			try:
				with filepath.open(mode="r", encoding="utf-8") as f:
					lines = [line.strip() for line in f.readlines() if line.strip()]

				if lines:
					self._wildcards[wildcard_name] = lines
			except (IOError, UnicodeDecodeError) as e:
				print(f"Could not read or decode wildcard file {filepath}: {e}")

	def _replacer(self, match: re.Match[str]) -> str:
		wildcard_name = match.group(1)
		if wildcard_name in self._wildcards:
			return random.choice(self._wildcards[wildcard_name])
		return ""

	def resolve(self, raw_prompt: str) -> str:
		"""
		Resolves wildcards in the given raw prompt by replacing
		wildcard placeholders with random choices from corresponding files.

		Args:
			raw_prompt: The prompt containing wildcard placeholders.
		"""
		resolved_prompt: str = raw_prompt

		for _ in range(20):  # recursion limit
			if "__" not in resolved_prompt:
				break

			previous_prompt = resolved_prompt
			resolved_prompt = re.sub(r"__(.*?)__", self._replacer, resolved_prompt)

			# This prevents infinite loops for non-existent wildcards.
			if previous_prompt == resolved_prompt:
				break
		else:
			print(f"Warning: Wildcard recursion limit reached for prompt: {raw_prompt}")

		return resolved_prompt
