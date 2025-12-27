from pathlib import Path


class InstructionManager:
	"""Manages loading instructions from files."""

	def __init__(self, instructions_path: Path) -> None:
		"""
		Args:
			instructions_path: Path to the directory containing instruction files.
		Raises:
			ValueError: If instructions_path is not a valid directory.
		"""

		if not instructions_path.is_dir():
			raise ValueError(
				f"instructions_path must be a valid directory: {instructions_path}"
			)

		self.path = instructions_path
		self._instructions: dict[str, str] = {}
		self._load_instructions()

	def _load_instructions(self) -> None:
		"""Loads all .txt files from the instructions directory."""
		for filepath in self.path.glob("*.txt"):
			instruction_name = filepath.stem
			try:
				with filepath.open(mode="r", encoding="utf-8") as file:
					self._instructions[instruction_name] = file.read()
			except (IOError, UnicodeDecodeError) as e:
				print(f"Could not read or decode instruction file {filepath}: {e}")

	def get_instruction(self, name: str) -> str | None:
		"""
		Gets a specific instruction by name.

		Args:
			name: The name of the instruction (filename without extension).

		Returns:
			The instruction string, or None if not found.
		"""
		return self._instructions.get(name)
