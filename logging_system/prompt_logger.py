from pathlib import Path
import csv
from core.models import ImageIdea


class PromptLogManager:
	"""
	Manages logging of image generation jobs to a CSV file, including the prompt.
	"""

	def __init__(self, filepath: Path) -> None:
		self.filepath = filepath
		self._initialize_csv()

	def _initialize_csv(self) -> None:
		"""
		Initializes the CSV file with a header row if it doesn't exist.
		"""
		if not self.filepath.exists():
			with open(self.filepath, "w", newline="", encoding="utf-8") as file:
				writer = csv.writer(file)
				writer.writerow(
					[
						"Filename",
						"Title",
						"Keywords",
						"Category",
						"Prompt",
					]
				)

	def log_job(
		self,
		image_idea: ImageIdea,
		image_name_stem: str,
	) -> None:
		"""
		Logs the details of an image generation job to the CSV file.
		"""
		with open(self.filepath, mode="a", newline="", encoding="utf-8") as file:
			writer = csv.writer(file)

			writer.writerow(
				[
					image_name_stem,
					image_idea.title,
					image_idea.keywords,
					image_idea.category,
					image_idea.prompt,
				]
			)
