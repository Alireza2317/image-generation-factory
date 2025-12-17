import csv
from pathlib import Path
from core.models import ImageIdea


class AdobeCsvManager:
	def __init__(self, filepath: Path) -> None:
		self.filepath = filepath
		self._ensure_header()

	def _ensure_header(self) -> None:
		"""Creates the file with Adobe headers if it doesn't exist."""
		if not self.filepath.exists():
			with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
				writer = csv.writer(file, delimiter=",")
				writer.writerow(
					["Filename", "Title", "Keywords", "Category", "Releases"]
				)

	def save_record(self, image_idea: ImageIdea, final_filename: str) -> None:
		"""
		Appends a single record to the csv metadata file.
		"""

		with open(self.filepath, mode="a", newline="", encoding="utf-8") as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow(
				[
					final_filename,
					image_idea.title,
					image_idea.keywords,
					image_idea.category,
					"",  # empty for releases column
				]
			)
