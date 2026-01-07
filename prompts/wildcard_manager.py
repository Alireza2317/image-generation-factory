import random
import re
from pathlib import Path


class WildcardResolver:
	"""
	Manages and resolves wildcards in prompts.

	A wildcard is a placeholder in a prompt, like `__color__`, that gets replaced
	by a randomly chosen line from a corresponding file (e.g., `color.txt`).

	Wildcards are loaded from a base directory. Niche-specific wildcards can be
	loaded from subdirectories, which will override the base wildcards.
	"""

	def __init__(self, wildcards_path: Path, seed: int | None = None) -> None:
		"""
		wildcards_path: Path to directory containing wildcard files.
			It searches for .txt files in the base directory and in niche-specific
			subdirectories.
		Raises:
			ValueError: If wildcards_path is not a valid directory.
		"""
		if seed is not None:
			random.seed(seed)

		if not wildcards_path.is_dir():
			raise ValueError(
				f"wildcards_path must be a valid directory: {wildcards_path}"
			)
		self.path = wildcards_path
		self._wildcards: dict[str, list[str]] = {}
		self._ordered_indices: dict[str, int] = {}
		self._common_wildcards = self._load_wildcards_from_path(self.path)
		self.set_niche(None)

	def set_seed(self, seed: int | None = None) -> None:
		"""
		Sets the random seed for wildcard resolution.
		Args:
			seed: The seed value to set.
				If None, the random generator acts randomly.
		"""
		random.seed(seed)

	def set_niche(self, niche_name: str | None) -> None:
		"""
		Sets the current niche, loading niche-specific wildcards.

		Niche wildcards override common wildcards if they share the same name.
		If niche_name is None, only common wildcards are used.

		Args:
			niche_name: The name of the niche, corresponding to a subdirectory.
		"""
		self._wildcards = self._common_wildcards.copy()
		self.reset_order()
		if niche_name:
			niche_path = self.path / niche_name
			if niche_path.is_dir():
				niche_wildcards = self._load_wildcards_from_path(niche_path)
				self._wildcards.update(niche_wildcards)
			else:
				print(f"Warning: Niche directory not found: {niche_path}")

	def reset_order(self) -> None:
		"""Resets the indices for ordered wildcard resolution."""
		self._ordered_indices = {}

	def _get_wildcard_files(self, path: Path) -> list[Path]:
		"""Gets all .txt files directly under the given path."""
		return [f for f in path.iterdir() if f.is_file() and f.suffix == ".txt"]

	def _load_wildcards_from_path(self, path: Path) -> dict[str, list[str]]:
		"""Loads all wildcards from .txt files in a given directory."""
		wildcards: dict[str, list[str]] = {}
		for filepath in self._get_wildcard_files(path):
			wildcard_name = filepath.stem
			try:
				with filepath.open(mode="r", encoding="utf-8") as f:
					lines = [line.strip() for line in f.readlines() if line.strip()]

				if lines:
					wildcards[wildcard_name] = lines
			except (IOError, UnicodeDecodeError) as e:
				print(f"Could not read or decode wildcard file {filepath}: {e}")
		return wildcards

	def _random_replacer(self, match: re.Match[str]) -> str:
		wildcard_name = match.group(1)
		if wildcard_name in self._wildcards:
			return random.choice(self._wildcards[wildcard_name])
		return ""

	def _ordered_replacer(self, match: re.Match[str]) -> str:
		wildcard_name = match.group(1)
		if wildcard_name in self._wildcards:
			if wildcard_name not in self._ordered_indices:
				self._ordered_indices[wildcard_name] = 0

			values = self._wildcards[wildcard_name]
			index = self._ordered_indices[wildcard_name]
			value = values[index]

			self._ordered_indices[wildcard_name] = (index + 1) % len(values)
			return value
		return ""

	def resolve(self, raw_prompt: str, ordered: bool = False) -> str:
		"""
		Resolves wildcards in the given raw prompt by replacing
		wildcard placeholders with random choices from corresponding files.

		Args:
			raw_prompt: The prompt containing wildcard placeholders.
			ordered: If True, resolves wildcards sequentially.
		"""
		resolved_prompt: str = raw_prompt
		replacer = self._ordered_replacer if ordered else self._random_replacer

		for _ in range(20):  # recursion limit
			if "__" not in resolved_prompt:
				break

			previous_prompt = resolved_prompt
			resolved_prompt = re.sub(r"__(.*?)__", replacer, resolved_prompt)

			# This prevents infinite loops for non-existent wildcards.
			if previous_prompt == resolved_prompt:
				break
		else:
			print(f"Warning: Wildcard recursion limit reached for prompt: {raw_prompt}")

		return resolved_prompt
